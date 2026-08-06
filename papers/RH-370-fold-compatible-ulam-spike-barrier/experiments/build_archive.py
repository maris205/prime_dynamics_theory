"""Build the fixed RH-370 publication/dependency manifest."""

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
    "fold-compatible-ulam-spike-barrier.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "results/result.schema.json",
    "src/fold_ulam/__init__.py",
    "src/fold_ulam/core.py",
    "tests/test_archive.py",
    "tests/test_results.py",
    "tests/test_theory.py",
]

EXTERNAL_INPUTS = [
    "cyclic_ulam_map/cyclic_ulam/ulam.py",
    "cyclic_ulam_map/cyclic_ulam/spectrum.py",
    "cyclic_ulam_map/README.md",
    "prime_dynamics_theory/papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/main.tex",
    "prime_dynamics_theory/papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-14-square-root-parity-boundary-layer/main.tex",
    "prime_dynamics_theory/papers/RH-52-intrinsic-peripheral-residue-transfer/main.tex",
    "prime_dynamics_theory/papers/RH-55-strong-weak-riesz-cutoff-transfer/main.tex",
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
        "status": "RH-370_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": hash_map(ROOT, LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
        "external_inputs": hash_map(WORKSPACE, EXTERNAL_INPUTS),
        "source_commits": {
            "cyclic_ulam_map": "e7d21f646498d77e1c3213d1e4f35dc8466038ff",
            "rh367_release": "ed2076391759499d46a3d5f64d223cf469d63bbb",
            "rh14": "d5807dd061ad9ca48cf2f406f4b35c15b343d3d2",
            "rh52": "d50fc86981e6a02f9c12d2a5aa150b8acd192f73",
            "rh55": "72af2d407592cd6c697e673e3d64267747b01021",
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
