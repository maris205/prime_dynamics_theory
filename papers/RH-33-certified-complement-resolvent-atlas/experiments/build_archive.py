"""Build compact RH-33 center, dependency, and theorem archives."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from resolvent_atlas import (  # noqa: E402
    center_identifier,
    sha256_file,
    verify_leaf_ledger,
)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_center_table(records: list[dict[str, object]], path: Path) -> None:
    fields = [
        "center_id",
        "source_kind",
        "source_arc",
        "turn_numerator",
        "turn_denominator",
        "spectral_parameter_real",
        "spectral_parameter_imag",
        "physical_dimension",
        "border_rank",
        "bordered_dimension",
        "matrix_nnz",
        "factor_nnz",
        "approximate_inverse_frobenius_upper",
        "residual_frobenius_upper",
        "residual_center_frobenius_upper",
        "residual_radius_frobenius_upper",
        "center_inverse_two_norm_upper",
        "factor_seconds",
        "certificate_seconds",
        "closed_arc_count",
        "inverse_sha256",
        "residual_center_sha256",
        "residual_radius_sha256",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for record in sorted(records, key=center_identifier):
            row = {key: record.get(key, "") for key in fields}
            row["center_id"] = center_identifier(record)
            row["source_kind"] = record.get(
                "source_kind", "rh28_parent_arc_midpoint"
            )
            writer.writerow(row)


def main() -> None:
    results = ROOT / "results"
    center_dir = results / "centers" / "sigma_1e-02"
    center_paths = sorted(center_dir.glob("*.json"))
    centers = [load_json(path) for path in center_paths]
    if not centers:
        raise RuntimeError("no center certificates found")
    if any(
        row["status"] != "rigorous_direct_center_certificate" for row in centers
    ):
        raise RuntimeError("the center archive contains a failed certificate")

    center_table = results / "center_certificates_sigma_1e-02.csv"
    write_center_table(centers, center_table)
    center_manifest = {
        "status": "all_centers_rigorous_direct_inverse_certificates",
        "sigma": 1.0e-2,
        "center_count": len(centers),
        "centers": [
            {
                "center_id": center_identifier(record),
                "path": str(path.relative_to(ROOT)),
                "sha256": sha256_file(path),
                "inverse_sha256": record["inverse_sha256"],
                "residual_center_sha256": record["residual_center_sha256"],
                "residual_radius_sha256": record["residual_radius_sha256"],
                "inverse_upper": record["center_inverse_two_norm_upper"],
                "residual_upper": record["residual_frobenius_upper"],
            }
            for path, record in zip(center_paths, centers)
        ],
    }
    manifest_path = results / "center_manifest_sigma_1e-02.json"
    manifest_path.write_text(
        json.dumps(center_manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    parent_summary_path = results / "atlas_sigma_1e-02_summary.json"
    refined_summary_path = results / "refined_atlas_sigma_1e-02.json"
    leaf_path = results / "refined_atlas_sigma_1e-02_leaves.csv"
    parent_summary = load_json(parent_summary_path)
    refined_summary = load_json(refined_summary_path)
    leaf_audit = verify_leaf_ledger(leaf_path)
    if not (
        refined_summary["status"] == "full_refined_atlas"
        and refined_summary["exact_rational_partition_verified"]
        and leaf_audit["exact_rational_partition_verified"]
        and leaf_audit["unresolved_leaf_count"] == 0
        and float(leaf_audit["maximum_neumann_product_upper"]) < 1.0
        and float(leaf_audit["maximum_budget_ratio_upper"]) < 1.0
    ):
        raise RuntimeError("the refined atlas is not a rigorous full cover")

    rh28_arcs = (
        PAPERS
        / "RH-28-arcwise-rational-arnoldi-enclosure"
        / "results"
        / "arcwise_contour_arcs.csv"
    )
    rh28_scales = (
        PAPERS
        / "RH-28-arcwise-rational-arnoldi-enclosure"
        / "results"
        / "arcwise_scale_summary.csv"
    )
    rh32_projected = (
        PAPERS
        / "RH-32-end-to-end-certificate-ledger"
        / "results"
        / "projected_count_certificates.json"
    )
    projected_payload = load_json(rh32_projected)
    projected = next(
        row for row in projected_payload["scales"] if float(row["sigma"]) == 1.0e-2
    )
    if not (
        projected["projected_determinant_winding"] == 1
        and projected["projected_pole_count"] == 0
        and projected["augmented"]["ambiguous_count"] == 0
        and projected["projected_poles"]["ambiguous_count"] == 0
    ):
        raise RuntimeError("the upstream projected winding is not certified")

    source_dependencies = {
        "rh27_componentwise": PAPERS
        / "RH-27-outward-rounded-primal-dual-residuals"
        / "src"
        / "outward_residuals"
        / "componentwise.py",
        "rh27_enclosures": PAPERS
        / "RH-27-outward-rounded-primal-dual-residuals"
        / "src"
        / "outward_residuals"
        / "enclosures.py",
        "rh27_factor_graph": PAPERS
        / "RH-27-outward-rounded-primal-dual-residuals"
        / "src"
        / "outward_residuals"
        / "factor_graph.py",
        "rh28_arc_geometry": PAPERS
        / "RH-28-arcwise-rational-arnoldi-enclosure"
        / "src"
        / "arcwise_feshbach"
        / "geometry.py",
        "rh30_sparse_grushin": PAPERS
        / "RH-30-sparse-two-step-grushin-inverse"
        / "src"
        / "sparse_grushin"
        / "certification.py",
    }
    dependency_payload = {
        "status": "all_consumed_upstream_files_hashed",
        "inputs": {
            "rh28_arcwise_contour_arcs": {
                "path": str(rh28_arcs.relative_to(REPOSITORY)),
                "sha256": sha256_file(rh28_arcs),
            },
            "rh28_arcwise_scale_summary": {
                "path": str(rh28_scales.relative_to(REPOSITORY)),
                "sha256": sha256_file(rh28_scales),
            },
            "rh32_projected_count_certificates": {
                "path": str(rh32_projected.relative_to(REPOSITORY)),
                "sha256": sha256_file(rh32_projected),
            },
        },
        "sources": {
            name: {
                "path": str(path.relative_to(REPOSITORY)),
                "sha256": sha256_file(path),
            }
            for name, path in source_dependencies.items()
        },
    }
    dependency_path = results / "dependency_manifest.json"
    dependency_path.write_text(
        json.dumps(dependency_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    inverse_bounds = [float(row["center_inverse_two_norm_upper"]) for row in centers]
    residual_bounds = [float(row["residual_frobenius_upper"]) for row in centers]
    approximate_bounds = [
        float(row["approximate_inverse_frobenius_upper"]) for row in centers
    ]
    source_kinds = [
        str(row.get("source_kind", "rh28_parent_arc_midpoint")) for row in centers
    ]
    result_files = {
        "atlas_sigma_1e-02_summary.json": parent_summary_path,
        "refined_atlas_sigma_1e-02.json": refined_summary_path,
        "refined_atlas_sigma_1e-02_leaves.csv": leaf_path,
        "center_certificates_sigma_1e-02.csv": center_table,
        "center_manifest_sigma_1e-02.json": manifest_path,
        "dependency_manifest.json": dependency_path,
    }
    summary = {
        "status": (
            "rigorous_full_boundary_resolvent_atlas_and_relative_winding_one_"
            "interior_complement_count_open"
        ),
        "scope": "exact finite model defined by stored binary64 factors",
        "sigma": 1.0e-2,
        "physical_dimension": int(centers[0]["physical_dimension"]),
        "border_rank": int(centers[0]["border_rank"]),
        "bordered_dimension": int(centers[0]["bordered_dimension"]),
        "center_count": len(centers),
        "rh28_parent_center_count": source_kinds.count(
            "rh28_parent_arc_midpoint"
        ),
        "adaptive_center_count": source_kinds.count("adaptive_gap_midpoint"),
        "minimum_center_inverse_upper": min(inverse_bounds),
        "maximum_center_inverse_upper": max(inverse_bounds),
        "maximum_approximate_inverse_frobenius_upper": max(approximate_bounds),
        "maximum_residual_frobenius_upper": max(residual_bounds),
        "minimum_residual_frobenius_upper": min(residual_bounds),
        "sum_factor_seconds": sum(float(row["factor_seconds"]) for row in centers),
        "sum_certificate_seconds": sum(
            float(row["certificate_seconds"]) for row in centers
        ),
        "parent_arc_count": int(parent_summary["arc_count"]),
        "whole_parent_arc_count": int(parent_summary["covered_arc_count"]),
        "whole_parent_uncovered_count": int(parent_summary["uncovered_arc_count"]),
        "refined_leaf_count": int(leaf_audit["leaf_count"]),
        "maximum_extra_refinement_used": int(
            refined_summary["maximum_extra_refinement_used"]
        ),
        "exact_rational_partition_verified": bool(
            leaf_audit["exact_rational_partition_verified"]
        ),
        "maximum_neumann_product_upper": float(
            leaf_audit["maximum_neumann_product_upper"]
        ),
        "minimum_neumann_denominator_lower": math.nextafter(
            1.0 - float(leaf_audit["maximum_neumann_product_upper"]),
            -math.inf,
        ),
        "maximum_budget_ratio_upper": float(
            leaf_audit["maximum_budget_ratio_upper"]
        ),
        "minimum_transported_inverse_upper": float(
            leaf_audit["minimum_transported_inverse_upper"]
        ),
        "maximum_transported_inverse_upper": float(
            leaf_audit["maximum_transported_inverse_upper"]
        ),
        "minimum_rh28_budget_lower": float(leaf_audit["minimum_budget_lower"]),
        "maximum_rh28_budget_lower": float(leaf_audit["maximum_budget_lower"]),
        "minimum_budget_margin_factor_lower": math.nextafter(
            1.0 / float(leaf_audit["maximum_budget_ratio_upper"]),
            -math.inf,
        ),
        "all_centers_used": len(leaf_audit["used_center_ids"]) == len(centers),
        "projected_determinant_winding": 1,
        "full_boundary_rouche_inequality_certified": True,
        "stored_feshbach_boundary_winding": 1,
        "exact_augmented_block_minus_complement_count": 1,
        "ordinary_feshbach_zero_count_certified": False,
        "interior_complement_pole_count_certified": False,
        "claims_excluded": [
            "one-zero count for the exact stored Feshbach determinant",
            "one-eigenvalue count for the original physical discretization",
            "continuum or zero-noise limit",
            "Hilbert-Polya construction or zeta-zero identification",
            "Riemann hypothesis implication",
        ],
        "result_hashes": {
            name: sha256_file(path) for name, path in result_files.items()
        },
    }
    (results / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
