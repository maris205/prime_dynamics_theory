"""Build the fixed-membership RH-368 publication/dependency manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "dependency_manifest.json"

LOCAL_MEMBERS = [
    ".gitignore", "Makefile", "README.md", "THEOREM_LEDGER.md",
    "UPDATED_ROADMAP.md", "experiments/build_archive.py",
    "experiments/build_result.py", "experiments/verify_archive.py",
    "main.pdf", "main.tex", "parity-factor-mobius-capacity-limit.pdf",
    "pyproject.toml", "references.bib", "requirements.txt",
    "results/result.json", "results/result.schema.json",
    "src/parity_capacity/__init__.py", "src/parity_capacity/core.py",
    "tests/test_archive.py", "tests/test_results.py", "tests/test_theory.py",
]

EXTERNAL_INPUTS = [
    "dyna_zeta_map/README.md",
    "dyna_zeta_map/research/PROOF_PACKAGE.md",
    "dyna_zeta_map/paper/main.tex",
    "dyna_zeta_map/paper/sections/6_quadratic_application.tex",
    "dyna_zeta_map/results/verification_summary.md",
    "dyna_zeta_map/results/wheel_zeta_data.json",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json",
    "prime_dynamics_theory/papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/README.md",
    "prime_dynamics_theory/papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/results/result.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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
        "status": "RH-368_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": hash_map(ROOT, LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
        "external_inputs": hash_map(WORKSPACE, EXTERNAL_INPUTS),
        "source_commits": {
            "dyna_zeta_map": "7fd3a3fdd5a6a25827a0965345459baf4a47b816",
            "prime_dynamics_theory_rh366_release": "6da1b94deaa865bbb297546f3de238433184772a",
            "prime_dynamics_theory_rh367_release": "032316d0e0bfd5b07f161d9bed05d552efd5dd97",
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
