"""Build the fixed RH-377 publication and dependency manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "dependency_manifest.json"

LOCAL_MEMBERS = [
    ".gitignore",
    "INTEGRITY_AUDIT.md",
    "Makefile",
    "README.md",
    "THEOREM_LEDGER.md",
    "UPDATED_ROADMAP.md",
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
    "mixed-exponent-run-hierarchy-two-envelope-capacity.pdf",
    "src/mixed_run_hierarchy/__init__.py",
    "src/mixed_run_hierarchy/core.py",
    "tests/test_archive.py",
    "tests/test_core.py",
    "tests/test_results.py",
]

EXTERNAL_INPUTS = [
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/README.md",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/main.tex",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/src/distance_capacity/core.py",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/results/result.json",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/references.bib",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/README.md",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/main.tex",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/references.bib",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/src/shift_two_chowla/core.py",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/results/result.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
]

SOURCE_COMMITS = {
    "rh371_release": "241b78a89ccbc0bad96d9ef20ee9256d61b4eaca",
    "rh374_release": "2bb3baa6a09491c2d679d10c0dbcd39587d1f831",
    "rh376_release": "0cf6179084bc8151318bb8f0955e529c12c0661a",
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
        "status": "RH-377_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": hash_map(ROOT, LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
        "external_inputs": hash_map(WORKSPACE, EXTERNAL_INPUTS),
        "source_commits": SOURCE_COMMITS,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "publication_file_count": len(LOCAL_MEMBERS),
                "external_input_count": len(EXTERNAL_INPUTS),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
