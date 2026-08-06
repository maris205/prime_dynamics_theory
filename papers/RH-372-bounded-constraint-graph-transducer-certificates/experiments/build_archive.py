"""Build the fixed RH-372 publication and dependency manifest.

The manifest deliberately excludes itself and the verification report.  This
keeps the hash set stable: a verifier can rewrite its report without changing
the publication digest set.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "dependency_manifest.json"

# Keep this list explicit.  It is the release surface, not a recursive scan of
# the working tree (which could silently include caches or generated debris).
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
    "bounded-constraint-graph-transducer-certificates.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "results/result.schema.json",
    "src/constraint_transducers/__init__.py",
    "src/constraint_transducers/core.py",
    "tests/test_archive.py",
    "tests/test_results.py",
    "tests/test_theory.py",
]

EXTERNAL_INPUTS = [
    "henon_mobius_correlations/henon_mobius/sft.py",
    "henon_mobius_correlations/henon_mobius/arithmetic.py",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json",
    "prime_dynamics_theory/papers/RH-368-parity-factor-mobius-capacity-limit/README.md",
    "prime_dynamics_theory/papers/RH-368-parity-factor-mobius-capacity-limit/results/result.json",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/README.md",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
    "dyna_zeta_map/paper/sections/6_quadratic_application.tex",
]

SOURCE_COMMITS = {
    "henon_mobius_correlations": "34490443f50cfe9af9ff93888e51e7e7e534a5a7",
    "dyna_zeta_map": "7fd3a3fdd5a6a25827a0965345459baf4a47b816",
    "rh366_release": "6da1b94deaa865bbb297546f3de238433184772a",
    "rh368_release": "ebcf29a4a2d248d8320067d85899b3b8039a7b12",
    "rh371_release": "241b78a89ccbc0bad96d9ef20ee9256d61b4eaca",
}


def digest(path: Path) -> str:
    """Return the SHA-256 digest of *path* in streaming mode."""

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
    """Hash an explicit, path-safe member list and fail closed on omissions."""

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
        "status": "RH-372_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": hash_map(ROOT, LOCAL_MEMBERS),
        "external_input_count": len(EXTERNAL_INPUTS),
        "external_inputs": hash_map(WORKSPACE, EXTERNAL_INPUTS),
        "source_commits": SOURCE_COMMITS,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "publication_file_count": len(LOCAL_MEMBERS),
                "external_input_count": len(EXTERNAL_INPUTS),
                "status": payload["status"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
