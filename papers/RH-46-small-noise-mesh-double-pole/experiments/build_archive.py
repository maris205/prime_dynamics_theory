"""Build dependency and publication archives for RH-46."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH15 = PAPERS / "RH-15-parity-extracted-bulk-scattering"
RH16 = PAPERS / "RH-16-endpoint-gaussian-resolution-rank"
RH42 = PAPERS / "RH-42-uniform-euclidean-parity-contour"
RH45 = PAPERS / "RH-45-bulk-two-step-trace-norm-determinant"


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
        "rh14_square_root_summary": RH14
        / "results"
        / "square_root_boundary_layer_summary.json",
        "rh15_bulk_scattering_manuscript": RH15 / "main.tex",
        "rh15_bulk_scattering_summary": RH15
        / "results"
        / "bulk_scattering_summary.json",
        "rh15_outer_resonance_cloud": RH15
        / "results"
        / "outer_resonance_cloud.csv",
        "rh16_endpoint_rank_summary": RH16
        / "results"
        / "endpoint_rank_audit.json",
        "rh42_fixed_noise_hilbert_envelope": RH42
        / "results"
        / "hilbert_schmidt_envelope_certificate.json",
        "rh45_fixed_noise_trace_determinant": RH45
        / "results"
        / "bulk_trace_norm_determinant_certificate.json",
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
        ROOT / "figures" / "small_noise_mesh_double_pole.pdf",
        ROOT / "figures" / "small_noise_mesh_double_pole.png",
        ROOT / "small-noise-mesh-double-pole.pdf",
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
        ROOT / "results" / "small_noise_mesh_double_pole_certificate.json"
    )
    row_path = ROOT / "results" / "gaussian_row_projection_pilot.json"
    cloud_path = ROOT / "results" / "two_step_square_cloud_pilot.json"
    certificate = load(certificate_path)
    row_pilot = load(row_path)
    cloud_pilot = load(cloud_path)

    envelope = certificate["uniform_gaussian_envelope"]
    reference = envelope["rows"]["0.01"]
    a0 = reference["kernel_scaled_constant"]
    a1 = reference["combined_first_scaled_constant"]
    selected = cloud_pilot["levels"]["0.0001"]
    central_rows = [
        row for row in selected["rows"] if abs(row["coordinate"]) <= 1.0
    ]
    hashed_results = [
        certificate_path,
        row_path,
        cloud_path,
        dependency_path,
    ]
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_level": certificate["evidence_level"],
        "mesh_constants": {
            "sigma_maximum": envelope["sigma_maximum"],
            "normalizer_linear_lower": envelope[
                "normalizer_linear_lower"
            ],
            "kernel_hilbert_schmidt_scaled_constant": a0,
            "combined_first_derivative_scaled_constant": a1,
            "galerkin_hilbert_schmidt_error_constant": a1 / math.pi,
            "square_trace_norm_linear_constant": 2.0 * a0 * a1 / math.pi,
            "square_trace_norm_quadratic_constant": (a1 / math.pi) ** 2,
        },
        "mesh_laws": certificate["raw_markov_resolution_theorems"],
        "double_pole_obstruction": certificate[
            "two_step_small_noise_obstruction"
        ],
        "conditional_bulk_route": certificate["conditional_bulk_extension"],
        "canonical_square_cloud_model": certificate[
            "canonical_square_cloud_model"
        ],
        "gaussian_row_pilot": {
            "status": row_pilot["status"],
            "evidence_level": row_pilot["evidence_level"],
            "asymptotic_constant": row_pilot["asymptotic_constant"],
            "finest_cell_to_sigma_ratio": row_pilot["rows"][-1][
                "cell_to_sigma_ratio"
            ],
            "finest_relative_error": row_pilot["finest_relative_error"],
        },
        "archived_square_cloud_pilot": {
            "status": cloud_pilot["status"],
            "evidence_level": cloud_pilot["evidence_level"],
            "noise_levels": sorted(
                (float(value) for value in cloud_pilot["levels"]),
                reverse=True,
            ),
            "maximum_ideal_cloud_polynomial_identity_error": cloud_pilot[
                "maximum_ideal_cloud_polynomial_identity_error"
            ],
            "selected_sigma": selected["sigma"],
            "selected_dimension": selected["dimension"],
            "selected_effective_degree": selected["effective_degree"],
            "selected_one_step_cloud_size": selected["one_step_cloud_size"],
            "selected_radial_mean": selected["radial_mean"],
            "selected_two_step_edge_center": selected[
                "two_step_edge_center"
            ],
            "selected_all_coordinate_mean_error": selected[
                "mean_observed_to_finite_error"
            ],
            "selected_central_mean_error": sum(
                row["observed_to_finite_error"] for row in central_rows
            )
            / len(central_rows),
            "selected_central_maximum_error": max(
                row["observed_to_finite_error"] for row in central_rows
            ),
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
