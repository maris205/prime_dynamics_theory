"""Verify every hash in the RH-367 publication manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
MANIFEST = ROOT / "results" / "dependency_manifest.json"
OUTPUT = ROOT / "results" / "archive_verification.json"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def verify_map(base: Path, mapping: dict[str, str]) -> list[dict[str, object]]:
    failures = []
    for relative, expected in sorted(mapping.items()):
        path = base / relative
        actual = digest(path) if path.is_file() else None
        if actual != expected:
            failures.append({
                "path": relative,
                "expected": expected,
                "actual": actual,
            })
    return failures


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    failures = verify_map(ROOT, manifest["publication_artifacts"])
    failures.extend(verify_map(WORKSPACE, manifest["external_inputs"]))
    payload = {
        "status": "RH-367_archive_verified" if not failures else "RH-367_archive_failed",
        "publication_file_count": manifest["publication_file_count"],
        "external_input_count": manifest["external_input_count"],
        "failure_count": len(failures),
        "failures": failures,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
