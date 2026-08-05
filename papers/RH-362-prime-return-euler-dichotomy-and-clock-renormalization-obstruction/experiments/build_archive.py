"""Build a fixed-membership RH-362 publication and dependency manifest."""

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
    "prime-return-euler-dichotomy-and-clock-renormalization-obstruction.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "src/prime_return_zeta/__init__.py",
    "src/prime_return_zeta/core.py",
    "tests/test_archive.py",
    "tests/test_results.py",
    "tests/test_theory.py",
]

EXTERNAL_INPUTS = [
    "henon_prime_returns/PRIME_RETURN_THEOREMS.md",
    "henon_prime_returns/paper/sections/03_reversible_structure.tex",
    "henon_prime_returns/paper/sections/04_divisibility.tex",
    "henon_prime_returns/paper/sections/07_discussion.tex",
    "dyna_zeta_map/paper/sections/3_5_core.tex",
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
        "status": "RH-362_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": hash_map(ROOT, LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
        "external_inputs": hash_map(WORKSPACE, EXTERNAL_INPUTS),
        "source_commits": {
            "henon_prime_returns":
                "c37d191672d30de49b2054be3a03cf2db068694f",
            "dyna_zeta_map":
                "7fd3a3fdd5a6a25827a0965345459baf4a47b816",
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"publication_file_count": len(LOCAL_MEMBERS)}, sort_keys=True))


if __name__ == "__main__":
    main()
