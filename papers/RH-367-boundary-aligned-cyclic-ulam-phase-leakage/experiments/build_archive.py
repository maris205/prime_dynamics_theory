"""Build the fixed-membership RH-367 publication/dependency manifest."""

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
    "boundary-aligned-cyclic-ulam-phase-leakage.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "results/result.schema.json",
    "src/cyclic_ulam_edge/__init__.py",
    "src/cyclic_ulam_edge/core.py",
    "tests/test_archive.py",
    "tests/test_results.py",
    "tests/test_theory.py",
]

EXTERNAL_INPUTS = [
    "cyclic_ulam_map/README.md",
    "cyclic_ulam_map/research/PROOF_PACKAGE.md",
    "cyclic_ulam_map/research/PAPER2_GATE_REPORT.md",
    "cyclic_ulam_map/paper/main.tex",
    "cyclic_ulam_map/paper/sections/3_map_observables.tex",
    "cyclic_ulam_map/paper/sections/4_ulam_theory.tex",
    "cyclic_ulam_map/paper/sections/5_experiments.tex",
    "cyclic_ulam_map/paper/sections/6_limitations_conclusion.tex",
    "cyclic_ulam_map/results/geometry_certificate.json",
    "cyclic_ulam_map/results/deterministic_gate.json",
    "cyclic_ulam_map/results/phase_scan.json",
    "cyclic_ulam_map/results/noise_gate.json",
    "cyclic_ulam_map/cyclic_ulam/ulam.py",
    "cyclic_ulam_map/cyclic_ulam/geometry.py",
    "prime_dynamics_theory/papers/RH-3-parity-resolved-band-merging-spectrum/README.md",
    "prime_dynamics_theory/papers/RH-3-parity-resolved-band-merging-spectrum/main.tex",
    "prime_dynamics_theory/papers/RH-10-parity-renormalized-long-cycle-determinant/README.md",
    "prime_dynamics_theory/papers/RH-10-parity-renormalized-long-cycle-determinant/main.tex",
    "prime_dynamics_theory/papers/RH-55-strong-weak-riesz-cutoff-transfer/README.md",
    "prime_dynamics_theory/papers/RH-55-strong-weak-riesz-cutoff-transfer/main.tex",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json",
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
        "status": "RH-367_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": hash_map(ROOT, LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
        "external_inputs": hash_map(WORKSPACE, EXTERNAL_INPUTS),
        "source_commits": {
            "cyclic_ulam_map": "e7d21f646498d77e1c3213d1e4f35dc8466038ff",
            "prime_dynamics_theory_rh366_release":
                "6da1b94deaa865bbb297546f3de238433184772a",
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
