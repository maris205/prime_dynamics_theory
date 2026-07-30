"""Build publication manifests for RH-302 through RH-311."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
DIRECTORY_NAMES = (
    "RH-302-annular-tail-moving-head-reduction",
    "RH-303-annular-fixed-order-head-transport-necessity",
    "RH-304-minimal-clock-complement-mass-demand",
    "RH-305-interior-annular-norm-rate-barrier",
    "RH-306-sharp-annular-coefficient-envelope-saturation",
    "RH-307-critical-shrinking-annulus-tail-threshold",
    "RH-308-hardy-dominant-annular-coefficient-conversion",
    "RH-309-endpoint-hardy-mismatch-barrier",
    "RH-310-critical-alias-parity-localization-coincidence",
    "RH-311-ten-layer-annular-mass-frontier-review",
)
NUMBERS = tuple(range(302, 312))
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
    "batch_dependency_manifest.json",
    "batch_archive_verification.json",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def paper_directories() -> list[Path]:
    directories = [PAPERS / name for name in DIRECTORY_NAMES]
    missing = [str(path) for path in directories if not path.is_dir()]
    if missing:
        raise RuntimeError(f"missing publication directories: {missing}")
    return directories


def publication_files(directory: Path) -> list[Path]:
    return sorted(
        path
        for path in directory.rglob("*")
        if path.is_file()
        and not any(
            part in EXCLUDED_DIRECTORIES
            for part in path.relative_to(directory).parts
        )
        and path.name not in EXCLUDED_NAMES
        and path.suffix != ".pyc"
    )


def main() -> None:
    counts = {}
    for directory in paper_directories():
        files = publication_files(directory)
        payload = {
            "status": f"{directory.name}_publication_manifest",
            "file_count": len(files),
            "files": {
                str(path.relative_to(directory)): digest(path) for path in files
            },
        }
        (directory / "results/dependency_manifest.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        counts[directory.name] = len(files)
    print(
        json.dumps(
            {"paper_count": len(counts), "file_counts": counts},
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
