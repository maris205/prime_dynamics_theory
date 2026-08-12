"""Strict offline verification for the four non-vendored RH-397 source locks.

This program has no network implementation.  It verifies the exact local
pretty JSON bytes, the canonical semantic object, source identity, and the
rights/non-vendoring boundary, then reports zero requests.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCKS = {
    "johnston-yang-arxiv-2204.01980v2": {
        "path": "results/external_source_lock.json",
        "blob": "d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058",
        "canonical": "d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786",
        "redistributable": False,
    },
    "maynard-annals-2015-small-gaps": {
        "path": "results/maynard_external_source_lock.json",
        "blob": "9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba",
        "canonical": "bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e",
        "redistributable": False,
    },
    "tao-cambridge-2016-logarithmic-chowla": {
        "path": "results/tao_external_source_lock.json",
        "blob": "825b3455be5eac151b7478f537fa6c503ae8eb02004cd8da821ca802d4ebdd8f",
        "canonical": "d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84",
        "redistributable": True,
    },
    "tao-teravainen-arxiv-1708.02610v2": {
        "path": "results/tao_teravainen_external_source_lock.json",
        "blob": "52ade551d8bef9aa35e850d03cefede1239cb9611b9211fdcda522f02fb501ec",
        "canonical": "a1448fb540b6f8fcf17cace1ff7d7218a6126cb3265699bbd43c444fcc558058",
        "redistributable": False,
    },
}


class OfflineSourceError(RuntimeError):
    """A fail-closed local-lock verification error."""


def _reject_constant(value: str) -> object:
    raise ValueError(f"non-finite JSON constant: {value}")


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
    return json.loads(text, object_pairs_hook=_object_no_duplicates, parse_constant=_reject_constant)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def verify_source(source_key: str, *, path: Path | None = None) -> dict[str, object]:
    if type(source_key) is not str or source_key not in LOCKS:
        raise OfflineSourceError("unknown source key")
    contract = LOCKS[source_key]
    lock_path = ROOT / contract["path"] if path is None else path
    if not isinstance(lock_path, Path) or not lock_path.is_file() or lock_path.is_symlink():
        raise OfflineSourceError("lock is absent or nonregular")
    raw = lock_path.read_bytes()
    if sha256(raw).hexdigest() != contract["blob"]:
        raise OfflineSourceError("pretty lock digest changed")
    try:
        lock = loads_strict(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise OfflineSourceError("lock is not strict UTF-8 JSON") from exc
    if type(lock) is not dict or sha256(canonical_bytes(lock)).hexdigest() != contract["canonical"]:
        raise OfflineSourceError("canonical lock object changed")
    if lock.get("source_key") != source_key:
        raise OfflineSourceError("source key changed")
    if lock.get("pdf_vendored") is not False:
        raise OfflineSourceError("PDF vendoring boundary opened")
    if lock.get("redistributable_in_release") is not contract["redistributable"]:
        raise OfflineSourceError("redistribution boundary changed")
    if source_key.startswith("johnston-yang") and lock.get("source_tar_vendored") is not False:
        raise OfflineSourceError("source-tar vendoring boundary opened")
    network = lock.get("network_verification")
    if type(network) is not dict or network.get("default") != "disabled":
        raise OfflineSourceError("default network boundary changed")
    return {
        "lock_canonical_sha256": contract["canonical"],
        "lock_verified_offline": True,
        "network_opt_in": False,
        "requests_made": 0,
        "source_key": source_key,
        "status": "NETWORK_DISABLED",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, choices=tuple(LOCKS))
    args = parser.parse_args(argv)
    try:
        result = verify_source(args.source)
    except (OSError, TypeError, ValueError, OfflineSourceError) as exc:
        print(json.dumps({"error": str(exc), "status": "FAIL"}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
