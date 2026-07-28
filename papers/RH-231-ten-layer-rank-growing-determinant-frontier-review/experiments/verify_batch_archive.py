"""Verify the RH-222--RH-231 publication manifest."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    manifest = json.loads((ROOT / "results/batch_dependency_manifest.json").read_text(encoding="utf-8"))
    failures = []
    for relative, expected in manifest["files"].items():
        path = PAPERS / relative
        if not path.is_file():
            failures.append({"file": relative, "reason": "missing"})
        elif digest(path) != expected:
            failures.append({"file": relative, "reason": "sha256_mismatch"})
    payload = {
        "status": "rh222_231_batch_archive_verified",
        "paper_numbers": manifest["paper_numbers"],
        "file_count": manifest["file_count"],
        "failure_count": len(failures),
        "failures": failures,
    }
    output = ROOT / "results/batch_archive_verification.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
