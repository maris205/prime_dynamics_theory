"""Build dependency and publication archives for RH-44."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH37 = PAPERS / "RH-37-iterated-dyadic-physical-count"
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"
RH40 = PAPERS / "RH-40-weighted-riesz-projector-bridge"
RH41 = PAPERS / "RH-41-validated-parity-continuum-contour"
RH42 = PAPERS / "RH-42-uniform-euclidean-parity-contour"
RH43 = PAPERS / "RH-43-validated-weighted-riesz-parity-kernel"


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
    paths = {
        "rh36_factor_snapshot": RH36
        / "results"
        / "nested_grid_snapshot_sigma_1e-02.npz",
        "rh37_factor_snapshot": RH37
        / "results"
        / "second_dyadic_fine_object_sigma_1e-02.npz",
        "rh39_cutoff_certificate": RH39
        / "results"
        / "uniform_gaussian_cutoff_bridge_certificate.json",
        "rh40_projector_builder": RH40
        / "experiments"
        / "build_projector_certificate.py",
        "rh40_weighted_riesz_certificate": RH40
        / "results"
        / "weighted_riesz_projector_bridge_certificate.json",
        "rh41_grushin_source": RH41
        / "experiments"
        / "run_coarse_grushin_certificate.py",
        "rh42_uniform_euclidean_certificate": RH42
        / "results"
        / "uniform_euclidean_parity_certificate.json",
        "rh42_midpoint_bridge": RH42
        / "results"
        / "euclidean_stored_to_midpoint_bridge.json",
        "rh43_intrinsic_parity_certificate": RH43
        / "results"
        / "validated_weighted_parity_kernel.json",
        "rh43_multilevel_grushin_engine": RH43
        / "experiments"
        / "run_multilevel_euclidean_grushin.py",
        "rh43_weighted_kernel_source": RH43
        / "src"
        / "weighted_kernel"
        / "bounds.py",
    }
    for path in sorted((RH27 / "src" / "outward_residuals").glob("*.py")):
        name = path.stem.replace("__init__", "package_exports")
        paths[f"rh27_outward_{name}_source"] = path
    for path in sorted((RH41 / "src" / "parity_contour").glob("*.py")):
        name = path.stem.replace("__init__", "package_exports")
        paths[f"rh41_parity_{name}_source"] = path
    for path in sorted((RH42 / "src" / "euclidean_contour").glob("*.py")):
        name = path.stem.replace("__init__", "package_exports")
        paths[f"rh42_euclidean_{name}_source"] = path
    for path in sorted((RH43 / "src" / "weighted_kernel").glob("*.py")):
        name = path.stem.replace("__init__", "package_exports")
        paths.setdefault(f"rh43_weighted_{name}_source", path)
    return paths


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
        ROOT / "figures" / "validated_rank_two_peripheral_complement.pdf",
        ROOT / "figures" / "validated_rank_two_peripheral_complement.png",
        ROOT / "validated-rank-two-peripheral-complement.pdf",
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
    multilevel_path = ROOT / "results" / "multilevel_perron_grushin.json"
    rank_two_path = (
        ROOT / "results" / "validated_rank_two_peripheral_complement.json"
    )
    rank_two = load(rank_two_path)
    factors = rank_two["stored_perron_factor_validation"]["levels"]
    ratios = rank_two["stored_rank_two_haar_law"]["actual_spectral_ratios"]
    perron = rank_two["perron_continuum_contour"]
    family = rank_two["uniform_perron_and_rank_two_families"]
    hashed_results = [multilevel_path, rank_two_path, dependency_path]
    summary = {
        "status": rank_two["status"],
        "scope": rank_two["scope"],
        "evidence_level": rank_two["evidence_level"],
        "contours": rank_two["contours"],
        "stored_perron_factor_validation": rank_two[
            "stored_perron_factor_validation"
        ],
        "stored_rank_two_haar_law": rank_two["stored_rank_two_haar_law"],
        "perron_continuum_contour": perron,
        "intrinsic_perron_kernel": rank_two["intrinsic_perron_kernel"],
        "intrinsic_rank_two_kernel": rank_two["intrinsic_rank_two_kernel"],
        "uniform_perron_and_rank_two_families": family,
        "intrinsic_bulk_operator": rank_two["intrinsic_bulk_operator"],
        "rh40_completion_status": rank_two["rh40_completion_status"],
        "gate_summary": {
            "all_three_stored_perron_factors_are_spectral": rank_two[
                "stored_perron_factor_validation"
            ]["all_three_levels_are_actual_spectral_factors"],
            "maximum_perron_factor_error_upper": max(
                row["weighted_term_error_upper"] for row in factors.values()
            ),
            "maximum_rank_two_haar_target_deviation": max(
                row["maximum_target_deviation"] for row in ratios.values()
            ),
            "perron_continuum_resolvent_upper": perron[
                "continuum_L2_resolvent_upper"
            ],
            "uniform_threshold_dimension": family[
                "certified_threshold_dimension"
            ],
            "uniform_union_contour_resolvent_upper": family[
                "uniform_union_contour_resolvent_upper"
            ],
            "uniform_rank_two_weighted_cutoff_upper": family[
                "uniform_rank_two_weighted_riesz_cutoff_upper"
            ],
            "uniform_rank_two_deflated_cutoff_upper": family[
                "uniform_rank_two_intrinsically_deflated_cutoff_upper"
            ],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in hashed_results
        },
        "publication_artifact_hashes": dependency[
            "publication_artifacts"
        ],
        "limitations": rank_two["limitations"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
