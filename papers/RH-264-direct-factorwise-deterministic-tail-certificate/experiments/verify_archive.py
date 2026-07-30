"""Verify the paper publication manifest."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    manifest = json.loads((ROOT / "results/dependency_manifest.json").read_text())
    failures = []
    for relative, expected in manifest["files"].items():
        path = ROOT / relative
        if not path.is_file():
            failures.append({"file": relative, "reason": "missing"})
        elif digest(path) != expected:
            failures.append({"file": relative, "reason": "sha256_mismatch"})
    payload = {
        "status": f"{ROOT.name}_archive_verified",
        "file_count": manifest["file_count"],
        "failure_count": len(failures),
        "failures": failures,
    }
    (ROOT / "results/archive_verification.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(payload, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
