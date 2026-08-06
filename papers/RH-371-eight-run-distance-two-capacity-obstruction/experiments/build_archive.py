"""Build the fixed RH-371 publication/dependency manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "dependency_manifest.json"

LOCAL_MEMBERS = [
    ".gitignore",
    "Makefile",
    "README.md",
    "THEOREM_LEDGER.md",
    "UPDATED_ROADMAP.md",
    "experiments/build_archive.py",
    "experiments/build_result.py",
    "experiments/verify_archive.py",
    "main.pdf",
    "main.tex",
    "eight-run-distance-two-capacity-obstruction.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "results/result.schema.json",
    "src/distance_capacity/__init__.py",
    "src/distance_capacity/core.py",
    "tests/test_archive.py",
    "tests/test_results.py",
    "tests/test_theory.py",
]

EXTERNAL_INPUTS = [
    "henon_mobius_correlations/henon_mobius/capacity.py",
    "henon_mobius_correlations/THEOREM_PACKAGE.md",
    "henon_mobius_correlations/tests/test_capacity.py",
    "henon_mobius_correlations/paper/sections/6_capacity_audit.tex",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/main.tex",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json",
    "prime_dynamics_theory/papers/RH-370-fold-compatible-ulam-spike-barrier/UPDATED_ROADMAP.md",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
]


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def hash_map(base: Path, members: list[str]) -> dict[str, str]:
    output: dict[str, str] = {}
    for relative in members:
        path = base / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        output[relative] = digest(path)
    return output


def main() -> None:
    payload = {
        "status": "RH-371_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": hash_map(ROOT, LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
        "external_inputs": hash_map(WORKSPACE, EXTERNAL_INPUTS),
        "source_commits": {
            "henon_mobius_correlations": "34490443f50cfe9af9ff93888e51e7e7e534a5a7",
            "prime_dynamics_theory_rh366_release": "6da1b94deaa865bbb297546f3de238433184772a",
            "prime_dynamics_theory_rh370_release": "9ad958a1f326eae6f43f026c84ab9378a4a42f16",
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "publication_file_count": len(LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
