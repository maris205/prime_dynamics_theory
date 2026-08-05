from __future__ import annotations

from decimal import Decimal
from math import isclose

import pytest

from weighted_prime_lift.core import (
    A,
    analytic_constants,
    euler_tail_bound,
    exact_polynomial_coefficients,
    fixed_point_counts,
    primitive_orbit_counts,
    scalar_normalization_ledger,
    survivor_fixed_point_data,
    trace_formula_counts,
)


def test_symbolic_matrix_and_all_finite_trace_rows() -> None:
    assert A == (
        (1, 0, 1, 0),
        (1, 0, 0, 0),
        (0, 1, 0, 1),
        (0, 1, 0, 0),
    )
    assert fixed_point_counts(12) == trace_formula_counts(12)
    assert fixed_point_counts(3) == [1, 1, 4]


def test_primitive_orbit_ledger_and_polynomial() -> None:
    assert primitive_orbit_counts(12) == [1, 0, 1, 2, 2, 2, 4, 5, 8, 11, 18, 25]
    assert exact_polynomial_coefficients() == [1, -1, 0, -1, -1]


def test_exact_survivor_fixed_atom_is_in_negative_branch() -> None:
    row = survivor_fixed_point_data()
    x_star = Decimal(row["x_star"])
    multiplier = Decimal(row["unstable_multiplier"])
    flat_trace = Decimal(row["flat_trace_order_one"])
    assert x_star < 0
    assert multiplier > Decimal(7)
    assert Decimal("0.18") < flat_trace < Decimal("0.19")


def test_analytic_constants_and_certified_radii() -> None:
    row = analytic_constants()
    assert isclose(row["kappa"], 773 / 224, rel_tol=0, abs_tol=1e-15)
    assert isclose(row["euler_beta_one_radius"], 2.132769077248, abs_tol=1e-12)
    assert isclose(row["flat_correction_radius"], 7.359957574612, abs_tol=1e-12)
    assert isclose(row["log2_phi"], 0.694241913630, abs_tol=1e-12)
    assert isclose(row["beta_zero"], 0.290834898770, abs_tol=1e-12)


def test_scalar_normalization_matches_two_orders_and_fails_at_cubes() -> None:
    period_three_multiplier = 131.90727397193268
    for beta in (0.0, analytic_constants()["beta_zero"] / 2.0, 1.0):
        row = scalar_normalization_ledger(beta, period_three_multiplier)
        assert isclose(row["Q1"], 1.0)
        assert isclose(row["Q2"], 1.0)
        assert row["Q3"] > 1.0
    assert scalar_normalization_ledger(0.0, period_three_multiplier)["Q3"] == 4.0


def test_tail_bound_is_positive_and_decreases_with_cutoff() -> None:
    first = euler_tail_bound(radius=1.0, beta=1.0, cutoff=4)
    second = euler_tail_bound(radius=1.0, beta=1.0, cutoff=8)
    assert 0 < second < first


def test_tail_bound_rejects_radius_outside_certified_domain() -> None:
    with pytest.raises(ValueError, match="outside the certified tail domain"):
        euler_tail_bound(radius=3.0, beta=1.0, cutoff=4)
