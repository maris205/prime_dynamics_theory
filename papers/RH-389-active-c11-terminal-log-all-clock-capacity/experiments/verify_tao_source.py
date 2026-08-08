"""Offline-by-default verifier for RH-389's non-vendored Tao source.

The default invocation validates only the sealed local object and performs
zero network requests.  ``--network`` opts in to one request for the exact
Cambridge VOR PDF.  Retrieved bytes are held in memory (and in a temporary
directory only while ``pdfinfo`` runs), never in the publication tree.
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
LOCK_PATH = ROOT / "results" / "tao_external_source_lock.json"
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


def tao_source_lock() -> dict[str, object]:
    """Return the sealed semantic lock independently of stored JSON."""
    return {
        "article_number": "e8",
        "artifact_role": "official_publisher_open_access_version_of_record",
        "author": "Terence Tao",
        "bytes": 534086,
        "doi": "10.1017/fmp.2016.6",
        "journal": "Forum of Mathematics, Pi",
        "known_source_typos": [{
            "location": "immediately after Theorem 2, equation (3), printed/PDF page 3",
            "printed_text": "as n tends to infinity",
            "resolution": "read as x tends to infinity, consistently with the theorem variable, abstract, and surrounding context",
            "scope": "typographical only; no mathematical strengthening or changed hypothesis",
        }],
        "license": {
            "copyright": "Copyright The Author 2016",
            "evidence_retrieved": "2026-08-09",
            "license_name": "Creative Commons Attribution 4.0 International",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "published_version_cc_by": True,
            "publisher_evidence_url": "https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/logarithmically-averaged-chowla-and-elliott-conjectures-for-twopoint-correlations/48514F53D73B2C1277BD7232630F0694",
            "scope": "official publisher version; reuse is permitted with attribution under CC BY 4.0",
        },
        "locators": [{
            "equation": "(3)",
            "label": "Theorem 2",
            "pdf_page": 3,
            "pdf_page_base": 1,
            "printed_page": 3,
            "role": "fixed nonparallel affine two-point logarithmic Liouville cancellation",
            "statement": "for fixed natural a1,a2 and integer b1,b2 with a1*b2-a2*b1!=0, and every 1<=omega(x)<=x with omega(x)->infinity, sum_(x/omega(x)<n<=x) lambda(a1*n+b1)*lambda(a2*n+b2)/n=o(log omega(x)) as x->infinity",
        }],
        "mime": "application/pdf",
        "network_verification": {
            "checks": [
                "HTTP status 200",
                "exact allowlisted final URL; every redirect target change rejected",
                "Content-Type application/pdf",
                "byte count 534086",
                "SHA-256",
                "page count 36 via pdfinfo",
            ],
            "default": "disabled",
            "fixed_url_only": True,
            "offline_build_claim": "lock-object verification only; article metadata and DOI are sealed but not live-refetched",
            "opt_in_flag": "--network",
        },
        "pages": 36,
        "pdf_final_url": "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/48514F53D73B2C1277BD7232630F0694/S2050508616000068a.pdf/the-logarithmically-averaged-chowla-and-elliott-conjectures-for-two-point-correlations.pdf",
        "pdf_url": "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/48514F53D73B2C1277BD7232630F0694/S2050508616000068a.pdf/the-logarithmically-averaged-chowla-and-elliott-conjectures-for-two-point-correlations.pdf",
        "pdf_vendored": False,
        "publisher_article_url": "https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/logarithmically-averaged-chowla-and-elliott-conjectures-for-twopoint-correlations/48514F53D73B2C1277BD7232630F0694",
        "redistributable_in_release": True,
        "sha256": "a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2",
        "source_key": "tao-cambridge-2016-logarithmic-chowla",
        "title": "The logarithmically averaged Chowla and Elliott conjectures for two-point correlations",
        "version_of_record_doi_url": "https://doi.org/10.1017/fmp.2016.6",
        "volume": 4,
        "year": 2016,
    }


def lock_canonical_sha256(lock: dict[str, object]) -> str:
    if type(lock) is not dict:
        raise TypeError("lock must be an exact object")
    return sha256(canonical_json_bytes(lock)).hexdigest()


def _validate_lock(lock: object) -> dict[str, object]:
    expected = tao_source_lock()
    if not exact_equal(lock, expected):
        raise RemoteVerificationError("Tao lock differs from the sealed semantic contract")
    if type(lock) is not dict:
        raise RemoteVerificationError("Tao lock must be an object")
    source_sha = lock["sha256"]
    if type(source_sha) is not str or not SHA256_RE.fullmatch(source_sha):
        raise RemoteVerificationError("Tao PDF SHA-256 is malformed")
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
        value = headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
    if type(value) is not str:
        raise RemoteVerificationError("HTTP Content-Type is not text")
    return value.lower()


def _fetch_exact(lock: dict[str, object], opener: Callable[..., object]) -> tuple[bytes, str]:
    expected = tao_source_lock()
    if lock["pdf_url"] != expected["pdf_url"] or lock["pdf_final_url"] != lock["pdf_url"]:
        raise RemoteVerificationError("remote PDF URL was rebound")
    if type(lock["bytes"]) is not int or lock["bytes"] != expected["bytes"]:
        raise RemoteVerificationError("remote PDF byte contract was rebound")
    request = Request(lock["pdf_url"], headers={"User-Agent": "RH-389-source-lock-verifier/1.0"})  # type: ignore[arg-type]
    try:
        response = opener(request, timeout=60)
    except Exception as exc:
        raise RemoteVerificationError(f"network request failed: {type(exc).__name__}") from exc
    with closing(response):
        status = _response_status(response)
        if status != 200:
            raise RemoteVerificationError(f"HTTP status is {status}, expected 200")
        final_url = response.geturl()
        if type(final_url) is not str or final_url != lock["pdf_final_url"]:
            raise RemoteVerificationError("redirect/final URL is outside the exact allowlist")
        content_type = _content_type(response)
        expected_bytes = lock["bytes"]
        chunks: list[bytes] = []
        total = 0
        while total <= expected_bytes:  # type: ignore[operator]
            chunk = response.read(min(1 << 16, expected_bytes + 1 - total))  # type: ignore[operator]
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
    with tempfile.TemporaryDirectory(prefix="rh389-tao-pdf-") as directory:
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
    data, content_type = _fetch_exact(lock, opener)
    if content_type != lock["mime"]:
        raise RemoteVerificationError(f"PDF MIME is {content_type!r}, expected {lock['mime']!r}")
    if sha256(data).hexdigest() != lock["sha256"]:
        raise RemoteVerificationError("PDF SHA-256 mismatch")
    pages = page_counter(data)
    if type(pages) is not int or pages != lock["pages"]:
        raise RemoteVerificationError(f"PDF page count is {pages!r}, expected {lock['pages']!r}")
    return {
        "bytes": len(data),
        "downloaded_source_vendored": False,
        "lock_canonical_sha256": lock_canonical_sha256(lock),
        "network_opt_in": True,
        "pages": pages,
        "requests_made": 1,
        "sha256": lock["sha256"],
        "status": "PASS",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", action="store_true", help="explicitly retrieve the exact allowlisted PDF")
    args = parser.parse_args(argv)
    try:
        result = verify_remote_source(_load_lock(), network=args.network)
    except (OSError, TypeError, ValueError, RemoteVerificationError) as exc:
        print(json.dumps({"error": str(exc), "status": "FAIL"}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
