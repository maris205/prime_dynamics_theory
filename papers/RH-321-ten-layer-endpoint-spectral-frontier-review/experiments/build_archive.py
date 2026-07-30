"""Build publication manifests for RH-312 through RH-321."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
DIRECTORY_NAMES = (
    "RH-312-endpoint-logarithmic-singularity-decomposition",
    "RH-313-parity-orthogonal-endpoint-hardy-splitting",
    "RH-314-optimal-endpoint-logarithm-polynomial-approximation",
    "RH-315-root-of-unity-moment-packet-isolation",
    "RH-316-recursive-integer-spectral-prefix-realization",
    "RH-317-sharp-spectral-prefix-rank-mass-law",
    "RH-318-optimal-endpoint-spectral-mass-approximation",
    "RH-319-genuine-spectral-annular-envelope-saturation",
    "RH-320-escaping-packet-endpoint-energy-obstruction",
    "RH-321-ten-layer-endpoint-spectral-frontier-review",
)
NUMBERS = tuple(range(312, 322))
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
        and not any(part in EXCLUDED_DIRECTORIES for part in path.relative_to(directory).parts)
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
            "files": {str(path.relative_to(directory)): digest(path) for path in files},
        }
        (directory / "results/dependency_manifest.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        counts[directory.name] = len(files)
    print(json.dumps({"paper_count": len(counts), "file_counts": counts}, sort_keys=True))


if __name__ == "__main__":
    main()
