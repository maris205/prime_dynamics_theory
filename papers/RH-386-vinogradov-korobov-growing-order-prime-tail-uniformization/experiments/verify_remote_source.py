"""Explicit opt-in verifier for the non-redistributed Johnston--Yang source.

The default invocation performs no network request.  ``--network`` fetches
only the two versioned, allowlisted arXiv URLs and checks every byte-level
field recorded by ``results/external_source_lock.json``.  Downloaded bytes
exist only in memory or a temporary directory and are never copied into the
publication tree.
"""

from __future__ import annotations

import argparse
from contextlib import closing
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
from typing import Callable
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "results" / "external_source_lock.json"
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from vk_prime_tail.core import exact_equal, loads_strict, remote_source_lock  # noqa: E402


class RemoteVerificationError(RuntimeError):
    """A fail-closed remote-source verification error."""


def _load_lock(path: Path = LOCK_PATH) -> dict[str, object]:
    if not isinstance(path, Path):
        raise TypeError("lock path must be a pathlib.Path")
    lock = loads_strict(path.read_text())
    if not exact_equal(lock, remote_source_lock()):
        raise RemoteVerificationError("remote lock differs from the sealed core contract")
    return lock


def _response_status(response: object) -> int:
    status = getattr(response, "status", None)
    if status is None and hasattr(response, "getcode"):
        status = response.getcode()
    if type(status) is not int:
        raise RemoteVerificationError("HTTP response has no exact integer status")
    return status


def _content_type(response: object) -> str:
    headers = getattr(response, "headers", None)
    if headers is None:
        raise RemoteVerificationError("HTTP response has no headers")
    if hasattr(headers, "get_content_type"):
        value = headers.get_content_type()
    else:
        raw = headers.get("Content-Type", "")
        value = raw.split(";", 1)[0].strip().lower()
    if type(value) is not str:
        raise RemoteVerificationError("HTTP Content-Type is not text")
    return value.lower()


def _fetch_exact(
    requested_url: str,
    allowed_final_url: str,
    expected_bytes: int,
    *,
    opener: Callable[..., object],
) -> tuple[bytes, str]:
    if type(requested_url) is not str or type(allowed_final_url) is not str:
        raise TypeError("remote URLs must be text")
    if type(expected_bytes) is not int or expected_bytes <= 0:
        raise TypeError("expected byte count must be a positive exact integer")
    if "v2" not in requested_url or "v2" not in allowed_final_url:
        raise RemoteVerificationError("latest or unversioned source URLs are forbidden")
    request = Request(requested_url, headers={"User-Agent": "RH-386-source-lock-verifier/1.0"})
    try:
        response = opener(request, timeout=60)
    except Exception as exc:  # urllib has several transport exception classes
        raise RemoteVerificationError(f"network request failed: {type(exc).__name__}") from exc
    with closing(response):
        status = _response_status(response)
        if status != 200:
            raise RemoteVerificationError(f"HTTP status is {status}, expected 200")
        final_url = response.geturl()
        if type(final_url) is not str or final_url != allowed_final_url:
            raise RemoteVerificationError("redirect/final URL is outside the exact allowlist")
        content_type = _content_type(response)
        data = response.read(expected_bytes + 1)
        if type(data) is not bytes:
            raise RemoteVerificationError("HTTP body is not bytes")
        if len(data) != expected_bytes:
            raise RemoteVerificationError(
                f"byte count is {len(data)}, expected {expected_bytes}"
            )
    return data, content_type


def _pdf_pages_pdfinfo(data: bytes) -> int:
    if type(data) is not bytes:
        raise TypeError("PDF data must be bytes")
    with tempfile.TemporaryDirectory(prefix="rh386-pdf-") as directory:
        path = Path(directory) / "source.pdf"
        path.write_bytes(data)
        completed = subprocess.run(
            ["pdfinfo", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode:
            raise RemoteVerificationError("pdfinfo rejected the downloaded PDF")
        page_rows = [line for line in completed.stdout.splitlines() if line.startswith("Pages:")]
        if len(page_rows) != 1:
            raise RemoteVerificationError("pdfinfo did not report exactly one Pages field")
        try:
            pages = int(page_rows[0].split(":", 1)[1].strip())
        except ValueError as exc:
            raise RemoteVerificationError("pdfinfo Pages field is not an integer") from exc
        if type(pages) is not int or pages <= 0:
            raise RemoteVerificationError("PDF page count is not positive")
        return pages


def _source_main_sha(data: bytes) -> tuple[str, int]:
    if type(data) is not bytes:
        raise TypeError("source tar data must be bytes")
    try:
        with tarfile.open(fileobj=BytesIO(data), mode="r:*") as archive:
            files = []
            for member in archive.getmembers():
                path = Path(member.name)
                if path.is_absolute() or ".." in path.parts:
                    raise RemoteVerificationError("source tar contains an unsafe path")
                normalized = path.as_posix()
                if normalized.startswith("./"):
                    normalized = normalized[2:]
                if member.isfile() and normalized == "main.tex":
                    files.append(member)
            if len(files) != 1:
                raise RemoteVerificationError("source tar must contain exactly one top-level main.tex")
            stream = archive.extractfile(files[0])
            if stream is None:
                raise RemoteVerificationError("source tar main.tex is unreadable")
            main_data = stream.read()
    except (tarfile.TarError, OSError) as exc:
        raise RemoteVerificationError("source tar is unreadable") from exc
    return sha256(main_data).hexdigest(), len(main_data)


def verify_remote_source(
    lock: dict[str, object],
    *,
    network: bool,
    opener: Callable[..., object] = urlopen,
    page_counter: Callable[[bytes], int] = _pdf_pages_pdfinfo,
) -> dict[str, object]:
    if type(network) is not bool:
        raise TypeError("network must be an exact Boolean")
    if not exact_equal(lock, remote_source_lock()):
        raise RemoteVerificationError("remote lock differs from the sealed core contract")
    if not network:
        return {
            "status": "NETWORK_DISABLED",
            "network_opt_in": False,
            "requests_made": 0,
            "lock_verified_offline": True,
        }

    pdf, pdf_type = _fetch_exact(
        lock["versioned_url"],
        lock["versioned_url"],
        lock["bytes"],
        opener=opener,
    )
    if pdf_type != lock["mime"]:
        raise RemoteVerificationError(f"PDF MIME is {pdf_type!r}, expected {lock['mime']!r}")
    pdf_sha = sha256(pdf).hexdigest()
    if pdf_sha != lock["sha256"]:
        raise RemoteVerificationError("PDF SHA-256 mismatch")
    pages = page_counter(pdf)
    if type(pages) is not int or pages != lock["pages"]:
        raise RemoteVerificationError("PDF page count mismatch")

    source_tar, _tar_type = _fetch_exact(
        lock["source_tar_url"],
        lock["source_tar_final_url"],
        lock["source_tar_bytes"],
        opener=opener,
    )
    source_sha = sha256(source_tar).hexdigest()
    if source_sha != lock["source_tar_sha256"]:
        raise RemoteVerificationError("source tar SHA-256 mismatch")
    main_sha, main_bytes = _source_main_sha(source_tar)
    if main_sha != lock["source_main_tex_sha256"]:
        raise RemoteVerificationError("source tar main.tex SHA-256 mismatch")

    return {
        "status": "PASS",
        "network_opt_in": True,
        "requests_made": 2,
        "pdf": {
            "final_url": lock["versioned_url"],
            "mime": pdf_type,
            "bytes": len(pdf),
            "sha256": pdf_sha,
            "pages": pages,
        },
        "source_tar": {
            "requested_url": lock["source_tar_url"],
            "final_url": lock["source_tar_final_url"],
            "bytes": len(source_tar),
            "sha256": source_sha,
            "main_tex_bytes": main_bytes,
            "main_tex_sha256": main_sha,
        },
        "downloaded_source_vendored": False,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--network",
        action="store_true",
        help="explicitly opt in to the two allowlisted network downloads",
    )
    parser.add_argument(
        "--lock",
        type=Path,
        default=LOCK_PATH,
        help="path to the sealed lock object (content must still match exactly)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        lock = _load_lock(args.lock)
        result = verify_remote_source(lock, network=args.network)
    except (OSError, RemoteVerificationError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
