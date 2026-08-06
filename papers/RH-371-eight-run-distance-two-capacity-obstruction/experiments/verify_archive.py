"""Verify every RH-371 manifest hash and fixed membership count."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
MANIFEST = ROOT / "results" / "dependency_manifest.json"
OUTPUT = ROOT / "results" / "archive_verification.json"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    failures: list[str] = []
    local = manifest["publication_artifacts"]
    external = manifest["external_inputs"]
    for relative, expected in local.items():
        path = ROOT / relative
        if not path.is_file() or digest(path) != expected:
            failures.append(f"local:{relative}")
    for relative, expected in external.items():
        path = WORKSPACE / relative
        if not path.is_file() or digest(path) != expected:
            failures.append(f"external:{relative}")
    payload = {
        "status": "RH-371_archive_verified" if not failures else "RH-371_archive_failed",
        "publication_file_count": len(local),
        "external_input_count": len(external),
        "failure_count": len(failures),
        "failures": failures,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
