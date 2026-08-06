"""Build the fixed-membership RH-365 publication and dependency manifest."""

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
    "prime-return-bouquet-height-radius-and-prime-order-anchors.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "results/result.schema.json",
    "src/prime_return_bouquet/__init__.py",
    "src/prime_return_bouquet/core.py",
    "tests/test_archive.py",
    "tests/test_results.py",
    "tests/test_theory.py",
]

EXTERNAL_INPUTS = [
    "henon_prime_returns/PRIME_RETURN_THEOREMS.md",
    "henon_prime_returns/paper/sections/03_reversible_structure.tex",
    "henon_prime_returns/paper/sections/04_divisibility.tex",
    "henon_prime_returns/paper/sections/app_diagnostics.tex",
    "prime_dynamics_theory/papers/RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/README.md",
    "prime_dynamics_theory/papers/RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/main.tex",
    "prime_dynamics_theory/papers/RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/results/result.json",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/README.md",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/main.tex",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/UPDATED_ROADMAP.md",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/results/result.json",
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
        "status": "RH-365_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": hash_map(ROOT, LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
        "external_inputs": hash_map(WORKSPACE, EXTERNAL_INPUTS),
        "source_commits": {
            "prime_dynamics_theory_rh364_release":
                "ba4d11aab349d3301a713e4a6e4f16c0cd84d45a",
            "henon_prime_returns":
                "c37d191672d30de49b2054be3a03cf2db068694f",
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"publication_file_count": len(LOCAL_MEMBERS)}, sort_keys=True))


if __name__ == "__main__":
    main()
