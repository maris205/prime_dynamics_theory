"""Compose the stored Grushin, exact midpoint, Galerkin, and continuum gates."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH38 = PAPERS / "RH-38-dyadic-haar-block-decay"
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"
RH40 = PAPERS / "RH-40-weighted-riesz-projector-bridge"
sys.path.insert(0, str(ROOT / "src"))

from parity_contour import (  # noqa: E402
    continuum_galerkin_defect,
    derivative_envelope,
    galerkin_haar_bounds,
    midpoint_galerkin_defect,
    neumann_transfer,
    schur_resolvent_step,
)


COARSE_PATH = ROOT / "results" / "coarse_grushin_contour_certificate.json"
MIDPOINT_PATH = ROOT / "results" / "stored_to_midpoint_bridge_certificate.json"
OUTPUT = ROOT / "results" / "validated_parity_continuum_certificate.json"
U_UPPER = 1.544
SIGMA = 0.01
MIDPOINT_FAMILY_THRESHOLD = 32768


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def upward_sum(*values: float) -> float:
    total = 0.0
    for value in values:
        total = math.nextafter(total + float(value), math.inf)
    return total


def main() -> None:
    coarse = load(COARSE_PATH)
    midpoint = load(MIDPOINT_PATH)
    if coarse["status"] != "rigorous_exact_stored_parity_circle_count_one":
        raise RuntimeError("the coarse stored Grushin gate is not closed")
    if midpoint["status"] != "arb_exact_stored_to_exact_continuum_midpoint_bridge":
        raise RuntimeError("the stored-to-midpoint gate is not closed")

    center = float(coarse["center"])
    radius = float(coarse["radius"])
    minimum_boundary_modulus = math.nextafter(abs(center) - radius, 0.0)
    stored_resolvent = float(
        coarse["contour_ledger"]["contour_resolvent_upper"]
    )
    envelope = derivative_envelope(U_UPPER, SIGMA)
    midpoint_to_galerkin = midpoint_galerkin_defect(4096, envelope)
    stored_to_midpoint = float(midpoint["maximum_total_row_l1_difference_upper"])
    stored_to_galerkin = upward_sum(stored_to_midpoint, midpoint_to_galerkin)
    initial_transfer = neumann_transfer(stored_resolvent, stored_to_galerkin)

    first_blocks = galerkin_haar_bounds(4096, envelope)
    first_step = schur_resolvent_step(
        initial_transfer.transferred_resolvent_upper,
        minimum_boundary_modulus,
        first_blocks,
    )
    second_blocks = galerkin_haar_bounds(8192, envelope)
    second_step = schur_resolvent_step(
        first_step.fine_resolvent_upper,
        minimum_boundary_modulus,
        second_blocks,
    )
    continuum_defect = continuum_galerkin_defect(16384, envelope)
    complement_zero_resolvent = math.nextafter(
        2.0 / minimum_boundary_modulus, math.inf
    )
    finite_rank_operator_resolvent = upward_sum(
        second_step.fine_resolvent_upper, complement_zero_resolvent
    )
    continuum_transfer = neumann_transfer(
        finite_rank_operator_resolvent, continuum_defect
    )
    midpoint_family_defect = upward_sum(
        continuum_galerkin_defect(MIDPOINT_FAMILY_THRESHOLD, envelope),
        midpoint_galerkin_defect(MIDPOINT_FAMILY_THRESHOLD, envelope),
    )
    midpoint_family_transfer = neumann_transfer(
        continuum_transfer.transferred_resolvent_upper,
        midpoint_family_defect,
    )

    all_gates = bool(
        initial_transfer.admissible
        and first_step.count_transfers
        and second_step.count_transfers
        and continuum_transfer.admissible
        and center + radius < 0.0
    )
    status = (
        "rigorous_continuum_parity_count_one_with_uniform_resolvent"
        if all_gates
        else "continuum_parity_contour_not_closed"
    )
    payload = {
        "status": status,
        "scope": (
            "exact fixed-noise folded-Gaussian continuum Markov operator on "
            "L-infinity([0,1]) at sigma=1/100 and the first band-merging parameter"
        ),
        "evidence_level": "analytic_operator_theorem_plus_outward_computer_assisted_constants",
        "critical_parameter": {
            "definition": midpoint["critical_u_exact_definition"],
            "validated_bracket": midpoint["critical_u_bracket"],
            "analytic_upper_used": U_UPPER,
        },
        "sigma_exact": "1/100",
        "contour": {
            "center": center,
            "radius": radius,
            "left_endpoint": center - radius,
            "right_endpoint": center + radius,
            "minimum_modulus_lower": minimum_boundary_modulus,
            "lies_strictly_in_negative_half_plane": bool(center + radius < 0.0),
        },
        "analytic_derivative_envelope": envelope.as_dict(),
        "coarse_stored_theorem": {
            "inside_count": 1,
            "algebraic_multiplicity_counted": True,
            "contour_resolvent_upper": stored_resolvent,
            "grushin_scalar_error_upper": coarse["contour_ledger"][
                "scalar_error_upper"
            ],
            "effective_scalar_boundary_lower": coarse["contour_ledger"][
                "effective_scalar_boundary_lower"
            ],
        },
        "stored_to_galerkin_4096": {
            "stored_to_exact_midpoint_upper": stored_to_midpoint,
            "midpoint_to_cell_average_galerkin_upper": midpoint_to_galerkin,
            "total_upper": stored_to_galerkin,
            "neumann_transfer": initial_transfer.as_dict(),
            "inside_count_after_transfer": 1 if initial_transfer.admissible else None,
        },
        "dyadic_galerkin_steps": {
            "4096_to_8192": {
                "blocks": first_blocks.as_dict(),
                "resolvent_step": first_step.as_dict(),
                "inside_count_after_transfer": 1 if first_step.count_transfers else None,
            },
            "8192_to_16384": {
                "blocks": second_blocks.as_dict(),
                "resolvent_step": second_step.as_dict(),
                "inside_count_after_transfer": 1 if second_step.count_transfers else None,
            },
        },
        "galerkin_to_continuum": {
            "dimension": 16384,
            "galerkin_matrix_resolvent_upper": second_step.fine_resolvent_upper,
            "zero_complement_resolvent_addition_upper": complement_zero_resolvent,
            "finite_rank_operator_resolvent_upper": finite_rank_operator_resolvent,
            "operator_norm_defect_upper": continuum_defect,
            "neumann_transfer": continuum_transfer.as_dict(),
        },
        "continuum_conclusion": {
            "inside_count": 1 if all_gates else None,
            "algebraic_multiplicity_counted": True,
            "eigenvalue_is_simple": all_gates,
            "eigenvalue_is_real": all_gates,
            "eigenvalue_is_negative": all_gates,
            "contour_resolvent_upper": (
                continuum_transfer.transferred_resolvent_upper
                if all_gates
                else math.inf
            ),
            "reality_reason": (
                "the operator and contour are conjugation invariant, so a unique enclosed "
                "eigenvalue must equal its complex conjugate"
            ),
        },
        "continuum_to_exact_midpoint_family": {
            "normalization": "exact continuum row normalizer sampled at cell midpoints",
            "first_dimension_with_uniform_bound": MIDPOINT_FAMILY_THRESHOLD,
            "applies_to_every_larger_dimension": True,
            "operator_norm_defect_upper_at_threshold": midpoint_family_defect,
            "neumann_transfer_at_threshold": midpoint_family_transfer.as_dict(),
            "inside_count_for_every_larger_dimension": (
                1 if all_gates and midpoint_family_transfer.admissible else None
            ),
        },
        "weighted_riesz_consequence": {
            "rh40_full_kernel_parity_hypothesis_closed": all_gates,
            "uniform_continuum_Linfinity_contour_resolvent_available": all_gates,
            "adaptive_cutoff_transfer_in_Linfinity_available": all_gates,
            "exact_continuum_normalized_midpoint_family_uniform_from_dimension": (
                MIDPOINT_FAMILY_THRESHOLD
                if midpoint_family_transfer.admissible
                else None
            ),
            "uniform_euclidean_sparse_matrix_resolvent_claimed": False,
        },
        "gate_summary": {
            "coarse_grushin_count_one": coarse["contour_ledger"]["rouche_count_one"],
            "stored_to_galerkin_neumann_product_upper": initial_transfer.neumann_product_upper,
            "first_schur_product_upper": first_step.schur_neumann_product_upper,
            "second_schur_product_upper": second_step.schur_neumann_product_upper,
            "continuum_neumann_product_upper": continuum_transfer.neumann_product_upper,
            "all_gates_closed": all_gates,
        },
        "dependencies": {
            "coarse_grushin_certificate": repository_entry(COARSE_PATH),
            "stored_to_midpoint_certificate": repository_entry(MIDPOINT_PATH),
            "rh27_componentwise_rounding": repository_entry(
                RH27 / "src" / "outward_residuals" / "componentwise.py"
            ),
            "rh36_factor_snapshot": repository_entry(
                RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
            ),
            "rh38_haar_manuscript": repository_entry(RH38 / "main.tex"),
            "rh39_cutoff_certificate": repository_entry(
                RH39 / "results" / "uniform_gaussian_cutoff_bridge_certificate.json"
            ),
            "rh40_weighted_riesz_manuscript": repository_entry(RH40 / "main.tex"),
        },
        "limitations": [
            "The theorem is at the fixed positive noise width sigma=1/100.",
            "The continuum resonance is isolated and simple but no closed-form eigenvalue is asserted.",
            "The validated resolvent is in the continuum/Galerkin L-infinity norm; no dimension-uniform Euclidean resolvent theorem for sparse midpoint matrices is claimed.",
            "The result does not take a zero-noise limit or identify any zeta zero.",
            "No self-adjoint Hilbert-Polya operator or Riemann-hypothesis claim is made.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if status != "rigorous_continuum_parity_count_one_with_uniform_resolvent":
        raise RuntimeError("the continuum parity contour certificate did not close")


if __name__ == "__main__":
    main()
