"""Build the compact RH-34 theorem and dependency archives."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
PAPERS = ROOT.parent
RH33 = PAPERS / "RH-33-certified-complement-resolvent-atlas"
sys.path.insert(0, str(ROOT / "src"))

from complement_poles import (  # noqa: E402
    classify_binary64_diagonal,
    sha256_array,
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    results = ROOT / "results"
    certificate_path = results / "schur_similarity_sigma_1e-02.json"
    certificate = load_json(certificate_path)
    if certificate["status"] != (
        "rigorous_stored_complement_count_zero_and_ordinary_winding_one"
    ):
        raise RuntimeError("the Schur-similarity certificate is not closed")

    diagonal_path = ROOT / str(certificate["diagonal_ledger"])
    diagonal_npz_path = ROOT / str(certificate["diagonal_npz"])
    homotopy_path = ROOT / str(certificate["homotopy_ledger"])
    if sha256_file(diagonal_path) != certificate["diagonal_ledger_sha256"]:
        raise RuntimeError("diagonal ledger hash mismatch")
    if sha256_file(diagonal_npz_path) != certificate["diagonal_npz_sha256"]:
        raise RuntimeError("diagonal NPZ hash mismatch")
    if sha256_file(homotopy_path) != certificate["homotopy_ledger_sha256"]:
        raise RuntimeError("homotopy ledger hash mismatch")

    with np.load(diagonal_npz_path) as archive:
        diagonal = np.asarray(archive["diagonal"])
        contour_center = complex(archive["contour_center"].item())
        contour_radius = float(archive["contour_radius"].item())
    if sha256_array(diagonal) != certificate["triangular_diagonal_sha256"]:
        raise RuntimeError("stored triangular diagonal hash mismatch")
    classification = classify_binary64_diagonal(
        diagonal, contour_center, contour_radius
    )
    if not (
        classification.inside_count == 0
        and classification.outside_count == 2048
        and classification.boundary_count == 0
    ):
        raise RuntimeError("exact dyadic diagonal classification did not close")

    homotopy_rows = read_csv(homotopy_path)
    if not (
        len(homotopy_rows) == 949
        and all(row["homotopy_certified"] == "True" for row in homotopy_rows)
        and max(
            float(row["homotopy_neumann_product_upper"])
            for row in homotopy_rows
        )
        < 1.0
        and min(
            float(row["homotopy_denominator_lower"])
            for row in homotopy_rows
        )
        > 0.0
    ):
        raise RuntimeError("the leafwise Schur homotopy ledger is not closed")

    rh33_summary_path = RH33 / "results" / "summary.json"
    rh33_leaf_path = RH33 / "results" / "refined_atlas_sigma_1e-02_leaves.csv"
    rh33_summary = load_json(rh33_summary_path)
    if not (
        rh33_summary["full_boundary_rouche_inequality_certified"]
        and rh33_summary["stored_feshbach_boundary_winding"] == 1
        and rh33_summary["exact_augmented_block_minus_complement_count"] == 1
    ):
        raise RuntimeError("the inherited RH-33 theorem gates are not closed")
    if sha256_file(rh33_leaf_path) != certificate["rh33_leaf_ledger_sha256"]:
        raise RuntimeError("the inherited RH-33 leaf ledger changed")

    input_paths = {
        "rh28_arcwise_scale_summary": PAPERS
        / "RH-28-arcwise-rational-arnoldi-enclosure"
        / "results"
        / "arcwise_scale_summary.csv",
        "rh33_summary": rh33_summary_path,
        "rh33_refined_leaf_ledger": rh33_leaf_path,
    }
    source_paths = {
        "rh24_physical_model": PAPERS
        / "RH-24-contour-feshbach-root-count"
        / "experiments"
        / "run_contour_feshbach_audit.py",
        "rh25_environment_builder": PAPERS
        / "RH-25-directional-rouche-closure"
        / "experiments"
        / "run_global_resolvent_probe.py",
        "rh27_componentwise_arithmetic": PAPERS
        / "RH-27-outward-rounded-primal-dual-residuals"
        / "src"
        / "outward_residuals"
        / "componentwise.py",
        "rh27_componentwise_factor_graph": PAPERS
        / "RH-27-outward-rounded-primal-dual-residuals"
        / "src"
        / "outward_residuals"
        / "componentwise_graph.py",
        "rh27_norm_enclosures": PAPERS
        / "RH-27-outward-rounded-primal-dual-residuals"
        / "src"
        / "outward_residuals"
        / "enclosures.py",
        "rh33_atlas_verification": RH33
        / "src"
        / "resolvent_atlas"
        / "archive.py",
        "rh34_certificate_core": ROOT
        / "src"
        / "complement_poles"
        / "certificate.py",
        "rh34_certificate_driver": ROOT
        / "experiments"
        / "run_schur_similarity_certificate.py",
        "rh34_floating_pilot": ROOT
        / "experiments"
        / "run_full_complement_spectrum_pilot.py",
        "rh34_archive_builder": ROOT / "experiments" / "build_archive.py",
        "rh34_figure_builder": ROOT / "experiments" / "make_figures.py",
        "rh34_archive_verifier": ROOT / "experiments" / "verify_archive.py",
    }
    dependency = {
        "status": "all_consumed_inputs_and_sources_hashed",
        "inputs": {
            name: {
                "path": str(path.relative_to(REPOSITORY)),
                "sha256": sha256_file(path),
            }
            for name, path in input_paths.items()
        },
        "sources": {
            name: {
                "path": str(path.relative_to(REPOSITORY)),
                "sha256": sha256_file(path),
            }
            for name, path in source_paths.items()
        },
    }
    dependency_path = results / "dependency_manifest.json"
    dependency_path.write_text(
        json.dumps(dependency, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    result_paths = {
        "schur_similarity_sigma_1e-02.json": certificate_path,
        "schur_diagonal_sigma_1e-02.csv": diagonal_path,
        "schur_diagonal_sigma_1e-02.npz": diagonal_npz_path,
        "schur_homotopy_leaves_sigma_1e-02.csv": homotopy_path,
        "floating_full_spectrum_sigma_1e-02.json": results
        / "floating_full_spectrum_sigma_1e-02.json",
        "floating_full_spectrum_sigma_1e-02.npz": results
        / "floating_full_spectrum_sigma_1e-02.npz",
        "dependency_manifest.json": dependency_path,
    }
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "sigma": certificate["sigma"],
        "physical_dimension": certificate["physical_dimension"],
        "schur_residual_frobenius_upper": certificate[
            "schur_residual_frobenius_upper"
        ],
        "unitarity_defect_frobenius_upper": certificate[
            "unitarity_defect_frobenius_upper"
        ],
        "z_two_norm_upper": certificate["similarity_certificate"][
            "z_two_norm_upper"
        ],
        "z_inverse_two_norm_upper": certificate["similarity_certificate"][
            "z_inverse_two_norm_upper"
        ],
        "maximum_complement_resolvent_upper": certificate[
            "maximum_complement_resolvent_upper"
        ],
        "maximum_homotopy_neumann_product_upper": certificate[
            "maximum_homotopy_neumann_product_upper"
        ],
        "minimum_homotopy_denominator_lower": certificate[
            "minimum_homotopy_denominator_lower"
        ],
        "minimum_floating_diagonal_boundary_distance": certificate[
            "minimum_floating_diagonal_boundary_distance"
        ],
        "exact_triangular_inside_count": classification.inside_count,
        "exact_triangular_boundary_count": classification.boundary_count,
        "interior_complement_pole_count_certified": certificate[
            "interior_complement_pole_count_certified"
        ],
        "interior_complement_pole_count": certificate[
            "interior_complement_pole_count"
        ],
        "stored_feshbach_boundary_winding": certificate[
            "inherited_stored_feshbach_boundary_winding"
        ],
        "ordinary_feshbach_zero_count_certified": certificate[
            "ordinary_feshbach_zero_count_certified"
        ],
        "ordinary_feshbach_zero_count": certificate[
            "ordinary_feshbach_zero_count"
        ],
        "stored_augmented_block_inside_count": certificate[
            "stored_augmented_block_inside_count"
        ],
        "rh33_leaf_count": len(homotopy_rows),
        "result_hashes": {
            name: sha256_file(path) for name, path in result_paths.items()
        },
        "limitations": certificate["limitations"],
    }
    summary_path = results / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
