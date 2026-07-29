"""Build the RH-252--RH-261 publication manifest."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
NUMBERS = tuple(range(252, 262))
EXCLUDED_DIRECTORIES = {".pytest_cache", "__pycache__", ".ipynb_checkpoints"}
EXCLUDED_NAMES = {
    "main.aux", "main.bbl", "main.blg", "main.fdb_latexmk", "main.fls",
    "main.log", "main.out", "dependency_manifest.json", "archive_verification.json",
    "batch_dependency_manifest.json", "batch_archive_verification.json",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def paper_directories() -> list[Path]:
    directories = []
    for number in NUMBERS:
        matches = tuple(PAPERS.glob(f"RH-{number}-*"))
        if len(matches) != 1:
            raise RuntimeError(
                f"expected one RH-{number} directory, found {len(matches)}"
            )
        directories.append(matches[0])
    return directories


def main() -> None:
    files = []
    for directory in paper_directories():
        files.extend(
            path for path in directory.rglob("*")
            if path.is_file()
            and not any(
                part in EXCLUDED_DIRECTORIES
                for part in path.relative_to(directory).parts
            )
            and path.name not in EXCLUDED_NAMES
            and path.suffix != ".pyc"
        )
    files = sorted(files)
    payload = {
        "status": "rh252_261_batch_publication_manifest",
        "paper_numbers": list(NUMBERS),
        "file_count": len(files),
        "files": {str(path.relative_to(PAPERS)): digest(path) for path in files},
    }
    output = ROOT / "results/batch_dependency_manifest.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"file_count": len(files)}))


if __name__ == "__main__":
    main()
