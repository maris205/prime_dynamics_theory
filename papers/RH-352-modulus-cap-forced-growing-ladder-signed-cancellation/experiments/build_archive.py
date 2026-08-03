"""Build the RH-352 individual SHA-256 publication manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRECTORIES = {".pytest_cache", "__pycache__", ".ipynb_checkpoints"}
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


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def publication_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not any(
            part in EXCLUDED_DIRECTORIES for part in path.relative_to(ROOT).parts
        )
        and path.name not in EXCLUDED_NAMES
        and path.suffix != ".pyc"
    )


def manifest_payload() -> dict[str, object]:
    files = publication_files()
    return {
        "status": f"{ROOT.name}_publication_manifest",
        "file_count": len(files),
        "files": {str(path.relative_to(ROOT)): digest(path) for path in files},
    }


def main() -> None:
    output = ROOT / "results" / "dependency_manifest.json"
    output.write_text(
        json.dumps(manifest_payload(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"file_count": manifest_payload()["file_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
