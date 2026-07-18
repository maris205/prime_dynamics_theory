from __future__ import annotations

import math

from parity_contour import (
    continuum_galerkin_defect,
    derivative_envelope,
    galerkin_haar_bounds,
    grushin_contour_ledger,
    midpoint_galerkin_defect,
    neumann_transfer,
    schur_resolvent_step,
)


def test_folded_derivative_envelope_matches_closed_form() -> None:
    envelope = derivative_envelope(1.544, 0.01)
    assert envelope.parameter_first >= 100.0
    assert envelope.target_first >= 100.0
    assert envelope.parameter_second >= 20000.0
    assert envelope.parameter_target >= 20000.0
    assert envelope.source_first >= 308.8
    assert envelope.source_target >= 61760.0


def test_galerkin_bounds_have_exact_consistency_and_dyadic_rates() -> None:
    envelope = derivative_envelope(1.544, 0.01)
    first = galerkin_haar_bounds(4096, envelope)
    second = galerkin_haar_bounds(8192, envelope)
    assert first.coarse_consistency == second.coarse_consistency == 0.0
    assert math.isclose(
        second.coarse_to_detail / first.coarse_to_detail,
        0.5,
        rel_tol=2.0e-15,
    )
    assert math.isclose(
        second.detail_to_coarse / first.detail_to_coarse,
        0.5,
        rel_tol=2.0e-15,
    )
    assert math.isclose(
        second.detail_block / first.detail_block,
        0.25,
        rel_tol=2.0e-15,
    )


def test_expected_three_level_resolvent_budget_closes() -> None:
    envelope = derivative_envelope(1.544, 0.01)
    midpoint = midpoint_galerkin_defect(4096, envelope)
    assert midpoint < 0.0017
    initial = neumann_transfer(42.5, midpoint + 8.0e-6)
    assert initial.admissible
    minimum_modulus = 0.9865 - 0.05
    first = schur_resolvent_step(
        initial.transferred_resolvent_upper,
        minimum_modulus,
        galerkin_haar_bounds(4096, envelope),
    )
    second = schur_resolvent_step(
        first.fine_resolvent_upper,
        minimum_modulus,
        galerkin_haar_bounds(8192, envelope),
    )
    finite_rank_operator = second.fine_resolvent_upper + 2.0 / minimum_modulus
    continuum = neumann_transfer(
        finite_rank_operator,
        continuum_galerkin_defect(16384, envelope),
    )
    assert first.count_transfers and second.count_transfers
    assert continuum.admissible
    assert continuum.neumann_product_upper < 0.8


def test_one_center_grushin_ledger_closes_expected_circle() -> None:
    ledger = grushin_contour_ledger(
        radius=0.05,
        center_reduced_inverse_upper=10.0,
        right_mode_infinity_upper=0.0171,
        left_mode_one_upper=64.3,
        right_residual_infinity_upper=2.0e-15,
        left_residual_one_upper=2.0e-12,
        gram_lower=0.999999999999,
        gram_upper=1.000000000001,
        border_scale=20.0,
    )
    assert ledger.bordered_disk_invertible
    assert ledger.rouche_count_one
    assert ledger.contour_resolvent_upper < 43.0
