from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_coarse_grushin_archive_closes_one_root() -> None:
    data = load("coarse_grushin_contour_certificate.json")
    assert data["status"] == "rigorous_exact_stored_parity_circle_count_one"
    assert data["residual_infinity_upper"] < 1.0e-8
    assert data["contour_ledger"]["rouche_count_one"]
    assert data["contour_ledger"]["contour_resolvent_upper"] < 43.0


def test_stored_to_midpoint_archive_is_small() -> None:
    data = load("stored_to_midpoint_bridge_certificate.json")
    assert data["status"] == "arb_exact_stored_to_exact_continuum_midpoint_bridge"
    assert data["support_geometry_verified_for_all_rows"]
    assert data["maximum_total_row_l1_difference_upper"] < 8.0e-6


def test_continuum_archive_closes_simple_negative_resonance() -> None:
    data = load("validated_parity_continuum_certificate.json")
    assert data["status"] == (
        "rigorous_continuum_parity_count_one_with_uniform_resolvent"
    )
    conclusion = data["continuum_conclusion"]
    assert conclusion["inside_count"] == 1
    assert conclusion["eigenvalue_is_simple"]
    assert conclusion["eigenvalue_is_real"]
    assert conclusion["eigenvalue_is_negative"]
    assert data["gate_summary"]["continuum_neumann_product_upper"] < 0.8
    midpoint_family = data["continuum_to_exact_midpoint_family"]
    assert midpoint_family["first_dimension_with_uniform_bound"] == 32768
    assert midpoint_family["inside_count_for_every_larger_dimension"] == 1
    assert (
        midpoint_family["neumann_transfer_at_threshold"][
            "neumann_product_upper"
        ]
        < 1.0
    )
    consequence = data["weighted_riesz_consequence"]
    assert consequence["rh40_full_kernel_parity_hypothesis_closed"]
    assert consequence[
        "uniform_continuum_Linfinity_contour_resolvent_available"
    ]
    assert not consequence["uniform_euclidean_sparse_matrix_resolvent_claimed"]
