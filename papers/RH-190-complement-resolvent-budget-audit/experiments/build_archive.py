"""Build a stable local publication manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRECTORIES = {".pytest_cache", "__pycache__", ".ipynb_checkpoints"}
EXCLUDED_NAMES = {
    "main.aux", "main.bbl", "main.blg", "main.fdb_latexmk", "main.fls",
    "main.log", "main.out", "dependency_manifest.json",
    "archive_verification.json", "batch_dependency_manifest.json",
    "batch_archive_verification.json",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def publication_files() -> tuple[Path, ...]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED_DIRECTORIES for part in relative.parts):
            continue
        if path.name in EXCLUDED_NAMES or path.suffix == ".pyc":
            continue
        files.append(path)
    return tuple(sorted(files))


def main() -> None:
    files = publication_files()
    payload = {
        "status": f"{ROOT.name}_publication_manifest",
        "file_count": len(files),
        "files": {str(path.relative_to(ROOT)): sha256(path) for path in files},
    }
    output = ROOT / "results/dependency_manifest.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files)}, sort_keys=True))


if __name__ == "__main__":
    main()
