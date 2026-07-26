"""Build a publication manifest for the complete RH-162--171 batch."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
NUMBERS = tuple(range(162, 172))
EXCLUDED_NAMES = {
    "main.aux",
    "main.bbl",
    "main.blg",
    "main.fdb_latexmk",
    "main.fls",
    "main.log",
    "main.out",
    "dependency_manifest.json",
    "archive_verification.json",
}


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
            relative_parts = path.relative_to(directory).parts
            if any(part in {".pytest_cache", "__pycache__", ".ipynb_checkpoints"} for part in relative_parts):
                continue
            if path.name in EXCLUDED_NAMES or path.suffix == ".pyc":
                continue
            files.append(path)
    return tuple(sorted(files))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    files = publication_files()
    payload = {
        "status": "rh162_171_publication_manifest",
        "paper_numbers": list(NUMBERS),
        "file_count": len(files),
        "files": {
            str(path.relative_to(PAPERS)): sha256(path)
            for path in files
        },
    }
    output = ROOT / "results" / "dependency_manifest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files)}, sort_keys=True))


if __name__ == "__main__":
    main()
