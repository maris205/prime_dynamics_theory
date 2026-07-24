from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    summary = json.loads((ROOT / "results" / "summary.json").read_text(encoding="utf-8"))
    dependency = json.loads((ROOT / "results" / "dependency_manifest.json").read_text(encoding="utf-8"))
    for path, expected in summary["result_hashes"].items():
        assert sha(ROOT / path) == expected
    for path, expected in dependency["local_sources"].items():
        assert sha(ROOT / path) == expected
    for path, expected in dependency["publication_artifacts"].items():
        assert sha(ROOT / path) == expected
    for record in dependency["external_inputs"].values():
        assert sha(REPO / record["path"]) == record["sha256"]
    files = {path: sha(ROOT / path) for path in dependency["publication_artifacts"]}
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(json.dumps({"status": "all_rh134_archive_hashes_verified", "file_count": len(files), "files": files}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files)}, sort_keys=True))


if __name__ == "__main__":
    main()
