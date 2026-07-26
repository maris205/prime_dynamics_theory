"""Verify the local publication manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    manifest = json.loads((ROOT / "results/dependency_manifest.json").read_text(encoding="utf-8"))
    failures = []
    for relative, expected in manifest["files"].items():
        path = ROOT / relative
        if not path.is_file() or sha256(path) != expected:
            failures.append(relative)
    if failures:
        raise RuntimeError(f"archive verification failed: {failures}")
    payload = {
        "status": f"{ROOT.name}_archive_verified",
        "file_count": manifest["file_count"],
        "failure_count": 0,
    }
    output = ROOT / "results/archive_verification.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **payload}, sort_keys=True))


if __name__ == "__main__":
    main()
