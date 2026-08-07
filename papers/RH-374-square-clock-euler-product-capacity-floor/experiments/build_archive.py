"""Build the fixed RH-374 publication and dependency manifest."""

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
    "square-clock-euler-product-capacity-floor.pdf",
    "experiments/build_archive.py",
    "experiments/build_result.py",
    "experiments/verify_archive.py",
    "main.pdf",
    "main.tex",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "results/result.schema.json",
    "src/square_clock/__init__.py",
    "src/square_clock/core.py",
    "tests/test_archive.py",
    "tests/test_core.py",
    "tests/test_results.py",
]

EXTERNAL_INPUTS = [
    "henon_mobius_correlations/THEOREM_PACKAGE.md",
    "henon_mobius_correlations/henon_mobius/arithmetic.py",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/README.md",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/results/result.json",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/README.md",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/results/result.json",
    "prime_dynamics_theory/papers/RH-373-composite-clock-mobius-capacity-floor/README.md",
    "prime_dynamics_theory/papers/RH-373-composite-clock-mobius-capacity-floor/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-373-composite-clock-mobius-capacity-floor/results/result.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
]

SOURCE_COMMITS = {
    "henon_mobius_correlations": "34490443f50cfe9af9ff93888e51e7e7e534a5a7",
    "rh366_release": "0396fab97bbe3348c8237f8734dec0e1893fd3bf",
    "rh371_release": "241b78a89ccbc0bad96d9ef20ee9256d61b4eaca",
    "rh372_release": "7a7b10b74722b520b145064923af8df6d4e2e73f",
    "rh373_release": "e46a0b0ef0e459fc26711c379ce8c1b68deb9c58",
    "rh_mvp2_archive": "c0aed13a34b8bbc53061aed23738660adcd3624c",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _check_members(members: list[str]) -> None:
    if len(members) != len(set(members)):
        raise ValueError("manifest member list contains duplicates")
    for relative in members:
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"manifest member escapes its base: {relative}")


def hash_map(base: Path, members: list[str]) -> dict[str, str]:
    _check_members(members)
    output: dict[str, str] = {}
    for relative in members:
        path = base / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        output[relative] = digest(path)
    return output


def main() -> None:
    payload = {
        "status": "RH-374_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": hash_map(ROOT, LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
        "external_inputs": hash_map(WORKSPACE, EXTERNAL_INPUTS),
        "source_commits": SOURCE_COMMITS,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "publication_file_count": len(LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
