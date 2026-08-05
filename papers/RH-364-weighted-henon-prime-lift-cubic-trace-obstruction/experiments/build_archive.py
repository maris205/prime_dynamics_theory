"""Build the fixed-membership RH-364 publication and dependency manifest."""

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
    "weighted-henon-prime-lift-cubic-trace-obstruction.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "src/weighted_prime_lift/__init__.py",
    "src/weighted_prime_lift/core.py",
    "tests/test_archive.py",
    "tests/test_results.py",
    "tests/test_theory.py",
]

EXTERNAL_INPUTS = [
    "henon_weighted_zeta/paper/sections/3_geometry_setup.tex",
    "henon_weighted_zeta/paper/sections/B_contraction_proof.tex",
    "henon_weighted_zeta/paper/sections/4_weighted_zeta.tex",
    "henon_weighted_zeta/paper/sections/5_certified_orbits.tex",
    "henon_weighted_zeta/paper/sections/7_discussion.tex",
    "henon_weighted_zeta/results/certified_domain_r059.json",
    "henon_prime_returns/paper/sections/07_discussion.tex",
    "prime_dynamics_theory/papers/RH-363-prime-return-entropy-tower/README.md",
    "prime_dynamics_theory/papers/RH-363-prime-return-entropy-tower/main.tex",
    "prime_dynamics_theory/papers/RH-363-prime-return-entropy-tower/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-363-prime-return-entropy-tower/results/result.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/"
    "results/four_volume_archive_manifest.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/"
    "results/four_volume_archive_verification.json",
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
        "status": "RH-364_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": hash_map(ROOT, LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
        "external_inputs": hash_map(WORKSPACE, EXTERNAL_INPUTS),
        "source_commits": {
            "prime_dynamics_theory_rh363_release":
                "863aeaadedccb178a3fa9aaeb06ed0a4d33981d3",
            "henon_weighted_zeta":
                "ff44f961261349848c9f65ede6a031b7e155aca9",
            "henon_prime_returns":
                "c37d191672d30de49b2054be3a03cf2db068694f",
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"publication_file_count": len(LOCAL_MEMBERS)}, sort_keys=True))


if __name__ == "__main__":
    main()
