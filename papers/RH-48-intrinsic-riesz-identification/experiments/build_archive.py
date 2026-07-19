"""Build dependency and publication archives for RH-48."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH43 = PAPERS / "RH-43-validated-weighted-riesz-parity-kernel"
RH46 = PAPERS / "RH-46-small-noise-mesh-double-pole"
RH47 = PAPERS / "RH-47-logarithmic-peripheral-conditioning"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def repository_entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def external_inputs() -> dict[str, Path]:
    return {
        "rh14_folded_gaussian_operator_source": RH14
        / "src"
        / "parity_boundary"
        / "operators.py",
        "rh43_weighted_schur_source": RH43
        / "src"
        / "weighted_kernel"
        / "bounds.py",
        "rh46_small_noise_mesh_certificate": RH46
        / "results"
        / "small_noise_mesh_double_pole_certificate.json",
        "rh47_logarithmic_conditioning_certificate": RH47
        / "results"
        / "logarithmic_peripheral_conditioning_certificate.json",
        "rh47_logarithmic_conditioning_manuscript": RH47 / "main.tex",
    }


def dependency_manifest() -> dict[str, object]:
    local_sources = sorted(
        {
            *(ROOT / "src").rglob("*.py"),
            *(ROOT / "experiments").glob("*.py"),
            *(ROOT / "tests").glob("*.py"),
        }
    )
    publication_paths = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "intrinsic_riesz_identification.pdf",
        ROOT / "figures" / "intrinsic_riesz_identification.png",
        ROOT / "quadratic-schur-intrinsic-riesz-identification.pdf",
    ]
    return {
        "status": (
            "all_consumed_inputs_sources_and_publication_artifacts_hashed"
        ),
        "external_inputs": {
            name: repository_entry(path)
            for name, path in external_inputs().items()
        },
        "local_sources": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in local_sources
        },
        "publication_artifacts": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in publication_paths
        },
    }


def main() -> None:
    dependency = dependency_manifest()
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(
        json.dumps(dependency, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    certificate_path = (
        ROOT / "results" / "intrinsic_riesz_identification_certificate.json"
    )
    pilot_path = ROOT / "results" / "dyadic_identification_pilot.json"
    replay_path = (
        ROOT / "results" / "dyadic_identification_pilot_smoke.json"
    )
    certificate = load(certificate_path)
    pilot = load(pilot_path)
    replay = load(replay_path)
    audit = certificate["floating_exact_haar_audit"]
    hashed_results = [
        certificate_path,
        pilot_path,
        replay_path,
        dependency_path,
    ]
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_level": certificate["evidence_level"],
        "exact_schur_identification": certificate[
            "exact_schur_identification"
        ],
        "directional_bound": certificate["directional_bound"],
        "residue_reduced_split": certificate["residue_reduced_split"],
        "gaussian_block_scaling": certificate["gaussian_block_scaling"],
        "dyadic_telescoping": certificate["dyadic_telescoping"],
        "conditional_small_noise_closure": certificate[
            "conditional_small_noise_closure"
        ],
        "floating_exact_haar_audit": {
            "status": pilot["status"],
            "replay_status": replay["status"],
            "noise_levels": audit["noise_levels"],
            "adjacent_defects": audit["adjacent_defects"],
            "largest_dimension": audit["largest_dimension"],
            "largest_nonzeros": audit["largest_nonzeros"],
            "mesh_power_minimum": audit["mesh_power_minimum"],
            "mesh_power_maximum": audit["mesh_power_maximum"],
            "joint_power_fit": audit["joint_power_fit"],
            "double_resolution_replay": audit[
                "double_resolution_replay"
            ],
            "observed_candidate_law": audit["observed_candidate_law"],
            "candidate_law_is_a_theorem": audit[
                "candidate_law_is_a_theorem"
            ],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in hashed_results
        },
        "publication_artifact_hashes": dependency[
            "publication_artifacts"
        ],
        "limitations": certificate["limitations"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
