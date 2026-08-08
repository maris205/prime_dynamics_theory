"""Offline-by-default verifier for RH-388's non-vendored Maynard source.

The default invocation verifies only the immutable local lock and performs
zero network requests.  ``--network`` explicitly opts in to one allowlisted
publisher-PDF request.  Downloaded bytes remain in memory or in the temporary
directory used by ``pdfinfo`` and are never copied into the publication tree.
"""

from __future__ import annotations

import argparse
from contextlib import closing
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Callable
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "results" / "maynard_external_source_lock.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class RemoteVerificationError(RuntimeError):
    """A fail-closed remote-source verification error."""


def _reject_constant(_value: str) -> None:
    raise ValueError("nonfinite JSON constant is forbidden")


def _object_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def loads_strict(text: str) -> object:
    if type(text) is not str:
        raise TypeError("JSON input must be exact text")
    return json.loads(
        text,
        object_pairs_hook=_object_no_duplicates,
        parse_constant=_reject_constant,
    )


def exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        if set(left) != set(right):  # type: ignore[arg-type]
            return False
        return all(exact_equal(left[key], right[key]) for key in left)  # type: ignore[index]
    if type(left) is list:
        return len(left) == len(right) and all(  # type: ignore[arg-type]
            exact_equal(a, b) for a, b in zip(left, right)  # type: ignore[arg-type]
        )
    return left == right


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def maynard_source_lock() -> dict[str, object]:
    """Return the sealed semantic lock independently of the stored JSON."""
    return {
        "artifact_role": "official_publisher_version_of_record",
        "author": "James Maynard",
        "bytes": 528115,
        "copyright": "Copyright 2015 Department of Mathematics, Princeton University",
        "doi": "10.4007/annals.2015.181.1.7",
        "issue": 1,
        "journal": "Annals of Mathematics",
        "license": {
            "applicability_to_2015_article": "not_established",
            "article_specific_redistribution_grant_established": False,
            "current_copyright_agreement_date": 2022,
            "current_copyright_agreement_url": "https://annals.math.princeton.edu/wp-content/uploads/AoM_Copyright_Agreement.pdf",
            "evidence_retrieved": "2026-08-08",
            "evidence_scope": "current official policy materials support a conservative non-CC-BY, nonredistributable release boundary; they are not treated as evidence of the agreement signed for this 2015 article",
            "publisher_policy_url": "https://annals.math.princeton.edu/submission-guidelines",
            "published_version_cc_by": False,
            "scope": "publisher version; no article-specific third-party redistribution grant established",
        },
        "locators": [
            {
                "label": "Theorem 1.3",
                "pdf_page": 3,
                "pdf_page_base": 1,
                "printed_page": 385,
                "role": "unconditional bounded-consecutive-prime-gap input only",
                "statement": "liminf_{n->infinity}(p_{n+1}-p_n)<=600",
            }
        ],
        "mime": "application/pdf",
        "network_verification": {
            "checks": [
                "HTTP status 200",
                "exact allowlisted final URL; every redirect target change rejected",
                "Content-Type application/pdf",
                "byte count 528115",
                "SHA-256",
                "page count 31 via pdfinfo",
            ],
            "default": "disabled",
            "fixed_url_only": True,
            "offline_build_claim": "lock-object verification only; no claim of refetching",
            "opt_in_flag": "--network",
        },
        "pages": 31,
        "pages_range": "383-413",
        "pdf_final_url": "https://annals.math.princeton.edu/wp-content/uploads/annals-v181-n1-p07-p.pdf",
        "pdf_url": "https://annals.math.princeton.edu/wp-content/uploads/annals-v181-n1-p07-p.pdf",
        "pdf_vendored": False,
        "publisher_article_url": "https://annals.math.princeton.edu/2015/181-1/p07",
        "redistributable_in_release": False,
        "sha256": "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349",
        "source_key": "maynard-annals-2015-small-gaps",
        "title": "Small gaps between primes",
        "version_of_record_doi_url": "https://doi.org/10.4007/annals.2015.181.1.7",
        "volume": 181,
        "year": 2015,
    }


def lock_canonical_sha256(lock: dict[str, object]) -> str:
    if type(lock) is not dict:
        raise TypeError("lock must be an exact object")
    return sha256(canonical_json_bytes(lock)).hexdigest()


def _validate_lock(lock: object) -> dict[str, object]:
    expected = maynard_source_lock()
    if not exact_equal(lock, expected):
        raise RemoteVerificationError("Maynard lock differs from the sealed semantic contract")
    if type(lock) is not dict:
        raise RemoteVerificationError("Maynard lock must be an object")
    source_sha = lock["sha256"]
    if type(source_sha) is not str or not SHA256_RE.fullmatch(source_sha):
        raise RemoteVerificationError("Maynard PDF SHA-256 is malformed")
    return lock


def _load_lock(path: Path = LOCK_PATH) -> dict[str, object]:
    if not isinstance(path, Path):
        raise TypeError("lock path must be a pathlib.Path")
    return _validate_lock(loads_strict(path.read_text(encoding="utf-8")))


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
        raise TypeError("remote URLs must be exact text")
    if requested_url != maynard_source_lock()["pdf_url"] or allowed_final_url != requested_url:
        raise RemoteVerificationError("remote PDF URL was rebound")
    if type(expected_bytes) is not int or expected_bytes != maynard_source_lock()["bytes"]:
        raise RemoteVerificationError("remote PDF byte contract was rebound")
    request = Request(requested_url, headers={"User-Agent": "RH-388-source-lock-verifier/1.0"})
    try:
        response = opener(request, timeout=60)
    except Exception as exc:
        raise RemoteVerificationError(f"network request failed: {type(exc).__name__}") from exc
    with closing(response):
        status = _response_status(response)
        if status != 200:
            raise RemoteVerificationError(f"HTTP status is {status}, expected 200")
        final_url = response.geturl()
        if type(final_url) is not str or final_url != allowed_final_url:
            raise RemoteVerificationError("redirect/final URL is outside the exact allowlist")
        content_type = _content_type(response)
        chunks: list[bytes] = []
        total = 0
        while total <= expected_bytes:
            chunk = response.read(min(1 << 16, expected_bytes + 1 - total))
            if type(chunk) is not bytes:
                raise RemoteVerificationError("HTTP body is not bytes")
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
        data = b"".join(chunks)
        if len(data) != expected_bytes:
            raise RemoteVerificationError(f"byte count is {len(data)}, expected {expected_bytes}")
    return data, content_type


def _pdf_pages_pdfinfo(data: bytes) -> int:
    if type(data) is not bytes:
        raise TypeError("PDF data must be exact bytes")
    with tempfile.TemporaryDirectory(prefix="rh388-maynard-pdf-") as directory:
        path = Path(directory) / "source.pdf"
        path.write_bytes(data)
        completed = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=False)
        if completed.returncode:
            raise RemoteVerificationError("pdfinfo rejected the downloaded PDF")
        rows = [line for line in completed.stdout.splitlines() if line.startswith("Pages:")]
        if len(rows) != 1:
            raise RemoteVerificationError("pdfinfo did not report exactly one Pages field")
        try:
            pages = int(rows[0].split(":", 1)[1].strip())
        except ValueError as exc:
            raise RemoteVerificationError("pdfinfo Pages field is not an integer") from exc
        if type(pages) is not int or pages <= 0:
            raise RemoteVerificationError("PDF page count is not positive")
        return pages


def verify_remote_source(
    lock: dict[str, object],
    *,
    network: bool,
    opener: Callable[..., object] = urlopen,
    page_counter: Callable[[bytes], int] = _pdf_pages_pdfinfo,
) -> dict[str, object]:
    if type(network) is not bool:
        raise TypeError("network must be an exact Boolean")
    lock = _validate_lock(lock)
    if not network:
        return {
            "lock_canonical_sha256": lock_canonical_sha256(lock),
            "lock_verified_offline": True,
            "network_opt_in": False,
            "requests_made": 0,
            "status": "NETWORK_DISABLED",
        }
    data, content_type = _fetch_exact(
        lock["pdf_url"],  # type: ignore[arg-type]
        lock["pdf_final_url"],  # type: ignore[arg-type]
        lock["bytes"],  # type: ignore[arg-type]
        opener=opener,
    )
    if content_type != lock["mime"]:
        raise RemoteVerificationError(f"PDF MIME is {content_type!r}, expected {lock['mime']!r}")
    source_sha = sha256(data).hexdigest()
    if source_sha != lock["sha256"]:
        raise RemoteVerificationError("PDF SHA-256 mismatch")
    pages = page_counter(data)
    if type(pages) is not int or pages != lock["pages"]:
        raise RemoteVerificationError("PDF page count mismatch")
    return {
        "downloaded_source_vendored": False,
        "lock_canonical_sha256": lock_canonical_sha256(lock),
        "network_opt_in": True,
        "pdf": {
            "bytes": len(data),
            "final_url": lock["pdf_final_url"],
            "mime": content_type,
            "pages": pages,
            "sha256": source_sha,
        },
        "requests_made": 1,
        "status": "PASS",
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", action="store_true", help="explicitly opt in to the one allowlisted PDF request")
    parser.add_argument("--lock", type=Path, default=LOCK_PATH, help="path to the exact sealed Maynard lock")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = verify_remote_source(_load_lock(args.lock), network=args.network)
    except (OSError, TypeError, ValueError, RemoteVerificationError) as exc:
        print(json.dumps({"error": str(exc), "status": "FAIL"}, sort_keys=True), file=__import__("sys").stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
