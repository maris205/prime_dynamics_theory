from __future__ import annotations

import numpy as np

from factor_transfer import (
    aggregate_left_masses,
    average_right_values,
    left_haar_detail_l2,
    left_mass_norms,
    normalize_l1,
    normalize_linf,
    rank_one_difference_frobenius,
    rank_one_frobenius,
    right_value_norms,
    weak_residue_budget,
    weak_to_l2_factor_upper,
)


def test_physical_cell_norm_conversions() -> None:
    mass = np.asarray((0.1, 0.2, 0.3, 0.4))
    values = np.asarray((1.0, -2.0, 3.0, -4.0))
    left = left_mass_norms(mass)
    right = right_value_norms(values)
    assert np.isclose(left.l1_or_linf, 1.0)
    assert np.isclose(left.l2, 2.0 * np.linalg.norm(mass))
    assert np.isclose(right.l1_or_linf, 4.0)
    assert np.isclose(right.l2, np.linalg.norm(values) / 2.0)


def test_adjacent_mass_detail_parseval_identity() -> None:
    rng = np.random.default_rng(5201)
    mass = rng.normal(size=12)
    aggregate = aggregate_left_masses(mass)
    fine_l2_square = mass.size * np.linalg.norm(mass) ** 2
    coarse_l2_square = (
        mass.size // 2
    ) * np.linalg.norm(aggregate) ** 2
    detail_l2_square = left_haar_detail_l2(mass) ** 2
    assert np.isclose(
        fine_l2_square,
        coarse_l2_square + detail_l2_square,
        rtol=2.0e-15,
    )


def test_right_value_averaging_and_factor_normalizations() -> None:
    values = np.asarray((2.0, 0.0, -1.0, 1.0))
    assert np.allclose(average_right_values(values), (1.0, 0.0))
    assert np.isclose(np.sum(np.abs(normalize_l1(values))), 1.0)
    assert np.isclose(np.max(np.abs(normalize_linf(values))), 1.0)


def test_rank_one_norms_match_dense_materialization() -> None:
    rng = np.random.default_rng(5202)
    ra = rng.normal(size=7) + 1j * rng.normal(size=7)
    la = rng.normal(size=5) + 1j * rng.normal(size=5)
    rb = rng.normal(size=7) + 1j * rng.normal(size=7)
    lb = rng.normal(size=5) + 1j * rng.normal(size=5)
    dense_a = np.outer(ra, np.conjugate(la))
    dense_b = np.outer(rb, np.conjugate(lb))
    assert np.isclose(
        rank_one_frobenius(ra, la), np.linalg.norm(dense_a, "fro")
    )
    assert np.isclose(
        rank_one_difference_frobenius(ra, la, rb, lb),
        np.linalg.norm(dense_a - dense_b, "fro"),
    )


def test_weak_to_l2_factor_upper_has_the_exact_two_terms() -> None:
    upper = weak_to_l2_factor_upper(
        kernel_l1_to_l2=5.0,
        weak_factor_error=0.02,
        eigenvalue_modulus_lower=0.5,
        eigenvalue_error=0.01,
        continuum_factor_l2=3.0,
    )
    assert np.isclose(upper, 0.2 + 0.12)


def test_direct_weak_residue_budget_cancels_every_power() -> None:
    rows = []
    for sigma in (0.1, 0.01, 0.001):
        budget = weak_residue_budget(
            cell_width=sigma**2,
            sigma=sigma,
            eigenvalue_modulus_lower=0.5,
            right_l2_upper=2.0,
            right_linf_upper=3.0,
            left_l1_upper=4.0,
            target_detail_constant=5.0,
            source_detail_constant=6.0,
            kernel_l1_to_l2_constant=7.0,
            detail_block_plus_eigenvalue_upper=8.0,
            outgoing_hs_lower_constant=9.0,
            incoming_hs_lower_constant=10.0,
        )
        rows.append(
            (
                budget.fine_residue_ratio_upper,
                budget.right_residue_ratio_upper,
            )
        )
    assert np.allclose(rows, rows[0])
