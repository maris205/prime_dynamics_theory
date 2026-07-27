"""Verify the RH-212--RH-221 publication manifest."""

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
    failures = [
        name for name, expected in manifest["files"].items()
        if not (PAPERS / name).is_file() or digest(PAPERS / name) != expected
    ]
    if failures:
        raise RuntimeError(failures)
    payload = {
        "status": "rh212_221_batch_archive_verified",
        "paper_numbers": manifest["paper_numbers"],
        "file_count": manifest["file_count"],
        "failure_count": 0,
    }
    (ROOT / "results/batch_archive_verification.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
