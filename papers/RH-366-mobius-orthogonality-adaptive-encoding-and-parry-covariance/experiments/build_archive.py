"""Build the fixed-membership RH-366 publication/dependency manifest."""

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
    "mobius-orthogonality-adaptive-encoding-and-parry-covariance.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "results/result.schema.json",
    "src/mobius_henon_dichotomy/__init__.py",
    "src/mobius_henon_dichotomy/core.py",
    "tests/test_archive.py",
    "tests/test_results.py",
    "tests/test_theory.py",
]

EXTERNAL_INPUTS = [
    "henon_mobius_correlations/THEOREM_PACKAGE.md",
    "henon_mobius_correlations/paper/main.tex",
    "henon_mobius_correlations/paper/main.pdf",
    "henon_mobius_correlations/paper/sections/3_henon_setup.tex",
    "henon_mobius_correlations/paper/sections/4_periodic_exceptional.tex",
    "henon_mobius_correlations/paper/sections/5_parry_typical.tex",
    "henon_mobius_correlations/paper/sections/6_capacity_audit.tex",
    "henon_mobius_correlations/research/refine-logs/R001_MOBIUS_DICHOTOMY_PROTOCOL.json",
    "henon_mobius_correlations/results/r001_deterministic.json",
    "henon_mobius_correlations/results/r001_ensembles.json",
    "henon_mobius_correlations/results/r001_analysis.json",
    "henon_mobius_correlations/results/r001_independent_check.json",
    "henon_mobius_correlations/scripts/check_r001_independent.py",
    "henon_weighted_zeta/paper/main.pdf",
    "henon_weighted_zeta/paper/sections/B_contraction_proof.tex",
    "henon_weighted_zeta/research/refine-logs/R059_EXPECTED_SYMBOLIC_WORDS.json",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/README.md",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/main.tex",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/results/result.json",
    "prime_dynamics_theory/papers/RH-365-prime-return-bouquet-height-radius-and-prime-order-anchors/README.md",
    "prime_dynamics_theory/papers/RH-365-prime-return-bouquet-height-radius-and-prime-order-anchors/results/result.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_manifest.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


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
        "status": "RH-366_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": hash_map(ROOT, LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
        "external_inputs": hash_map(WORKSPACE, EXTERNAL_INPUTS),
        "source_commits": {
            "prime_dynamics_theory_rh365_release":
                "fbc8b00d38e0e83dafb10a1f1316ff8778039075",
            "henon_mobius_correlations":
                "34490443f50cfe9af9ff93888e51e7e7e534a5a7",
            "henon_weighted_zeta":
                "ff44f961261349848c9f65ede6a031b7e155aca9",
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
