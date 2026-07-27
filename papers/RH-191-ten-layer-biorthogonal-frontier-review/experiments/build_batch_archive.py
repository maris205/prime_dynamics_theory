"""Build the RH-182--191 batch publication manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
NUMBERS = tuple(range(182, 192))
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


def paper_directories() -> tuple[Path, ...]:
    directories = []
    for number in NUMBERS:
        matches = tuple(PAPERS.glob(f"RH-{number}-*"))
        if len(matches) != 1:
            raise RuntimeError(f"expected one RH-{number} directory, found {len(matches)}")
        directories.append(matches[0])
    return tuple(directories)


def publication_files() -> tuple[Path, ...]:
    files = []
    for directory in paper_directories():
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(directory)
            if any(part in EXCLUDED_DIRECTORIES for part in relative.parts):
                continue
            if path.name in EXCLUDED_NAMES or path.suffix == ".pyc":
                continue
            files.append(path)
    return tuple(sorted(files))


def main() -> None:
    files = publication_files()
    payload = {
        "status": "rh182_191_batch_publication_manifest",
        "paper_numbers": list(NUMBERS),
        "file_count": len(files),
        "files": {
            str(path.relative_to(PAPERS)): sha256(path)
            for path in files
        },
    }
    output = ROOT / "results/batch_dependency_manifest.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files)}, sort_keys=True))


if __name__ == "__main__":
    main()
