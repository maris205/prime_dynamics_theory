"""Build dependency and publication archives for RH-43."""

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
        "rh40_weighted_riesz_manuscript": RH40 / "main.tex",
        "rh41_grushin_source": RH41
        / "experiments"
        / "run_coarse_grushin_certificate.py",
        "rh42_uniform_euclidean_certificate": RH42
        / "results"
        / "uniform_euclidean_parity_certificate.json",
        "rh42_hilbert_envelope": RH42
        / "results"
        / "hilbert_schmidt_envelope_certificate.json",
        "rh42_hilbert_source": RH42
        / "src"
        / "euclidean_contour"
        / "hilbert.py",
        "rh42_euclidean_grushin_source": RH42
        / "src"
        / "euclidean_contour"
        / "grushin.py",
    }
    for path in sorted((RH27 / "src" / "outward_residuals").glob("*.py")):
        name = path.stem.replace("__init__", "package_exports")
        paths[f"rh27_outward_{name}_source"] = path
    for path in sorted((RH41 / "src" / "parity_contour").glob("*.py")):
        name = path.stem.replace("__init__", "package_exports")
        paths[f"rh41_parity_{name}_source"] = path
    for path in sorted((RH42 / "src" / "euclidean_contour").glob("*.py")):
        name = path.stem.replace("__init__", "package_exports")
        paths.setdefault(f"rh42_euclidean_{name}_source", path)
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
        ROOT / "figures" / "validated_weighted_parity_kernel.pdf",
        ROOT / "figures" / "validated_weighted_parity_kernel.png",
        ROOT / "validated-weighted-riesz-parity-kernel.pdf",
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

    multilevel_path = ROOT / "results" / "multilevel_euclidean_grushin.json"
    weighted_path = (
        ROOT / "results" / "validated_weighted_parity_kernel.json"
    )
    weighted = load(weighted_path)
    levels = weighted["stored_factor_validation"]["levels"]
    ratios = weighted["stored_parity_haar_law"]["actual_spectral_ratios"]
    complement = weighted["continuum_complement_schur"]
    family = weighted["improved_uniform_matrix_family"]
    hashed_results = [multilevel_path, weighted_path, dependency_path]
    summary = {
        "status": weighted["status"],
        "scope": weighted["scope"],
        "evidence_level": weighted["evidence_level"],
        "contour": weighted["contour"],
        "stored_factor_validation": weighted["stored_factor_validation"],
        "stored_parity_haar_law": weighted["stored_parity_haar_law"],
        "continuum_complement_schur": complement,
        "intrinsic_continuum_kernel": weighted[
            "intrinsic_continuum_kernel"
        ],
        "weighted_transport_chain": weighted["weighted_transport_chain"],
        "improved_uniform_matrix_family": family,
        "intrinsic_deflation": weighted["intrinsic_deflation"],
        "rh40_condition_status": weighted["rh40_condition_status"],
        "gate_summary": {
            "all_three_stored_factors_are_spectral": weighted[
                "stored_factor_validation"
            ]["all_three_levels_are_actual_spectral_factors"],
            "maximum_factor_correction_product_upper": max(
                row["correction_neumann_product_upper"]
                for row in levels.values()
            ),
            "maximum_stored_weighted_term_error_upper": max(
                row["weighted_term_error_upper"] for row in levels.values()
            ),
            "maximum_haar_target_deviation": max(
                row["maximum_target_deviation"] for row in ratios.values()
            ),
            "continuum_complement_schur_product_upper": complement[
                "resolvent_step"
            ]["schur_neumann_product_upper"],
            "continuum_L2_resolvent_upper": complement[
                "improved_continuum_L2_resolvent_upper"
            ],
            "uniform_matrix_threshold_dimension": family[
                "certified_threshold_dimension"
            ],
            "uniform_fixed_and_adaptive_sparse_resolvent_upper": family[
                "uniform_fixed_and_adaptive_sparse_resolvent_upper"
            ],
            "uniform_weighted_riesz_cutoff_upper": family[
                "uniform_weighted_riesz_cutoff_upper"
            ],
            "uniform_intrinsically_deflated_cutoff_upper": family[
                "uniform_intrinsically_deflated_cutoff_upper"
            ],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in hashed_results
        },
        "publication_artifact_hashes": dependency[
            "publication_artifacts"
        ],
        "limitations": weighted["limitations"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
