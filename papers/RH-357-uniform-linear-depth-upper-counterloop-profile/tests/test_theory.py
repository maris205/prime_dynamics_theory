from decimal import Decimal
from fractions import Fraction

import pytest

from linear_depth_profile import (
    FIXTURE_LAMBDA,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    R,
    R_H,
    endpoint_error_envelope,
    exact_alias_budget,
    exact_constants,
    exact_endpoint_certificate,
    exact_post_budget,
    linear_depth_diagnostic,
    rational_phase_orbit,
)


def test_exact_physical_constants_are_strict():
    data = exact_constants()
    assert R_H == Fraction(17, 20)
    assert R == Fraction(7, 5)
    assert LAMBDA_LOWER < FIXTURE_LAMBDA < LAMBDA_UPPER
    assert data["x"] == Fraction(2352, 1445)
    assert data["x_identity"] is True
    assert data["x_is_superunit"] is True


@pytest.mark.parametrize("k,L", [(4, 1), (8, 3), (16, 8), (24, 23)])
def test_exact_budget_ratio_and_endpoint_rows(k, L):
    row = exact_endpoint_certificate(k, L)
    assert row["alias_budget"] == exact_alias_budget(k)
    assert row["post_budget"] == exact_post_budget(k, L)
    assert row["ratio"] == row["post_budget"] / row["alias_budget"]
    assert row["ratio_identity"] is True
    assert row["post_over_endpoint_proxy"] >= 1
    assert row["ratio_over_proxy"] >= 1
    assert row["finite_formula_only"] is True


def test_uniform_endpoint_error_is_order_one_over_k_on_full_band():
    rows = [endpoint_error_envelope(k) for k in (8, 16, 32, 64)]
    errors = [float(row["post_max_relative_error"]) for row in rows]
    assert errors[0] > errors[1] > errors[2] > errors[3]
    assert all(float(row["k_times_post_max_relative_error"]) < 2 for row in rows)
    assert all(row["depth_count"] == row["k"] - 1 for row in rows)


def test_bounded_depth_factor_cannot_be_deleted():
    row = exact_endpoint_certificate(512, 1)
    x_value = exact_constants()["x"]
    deleted_factor_proxy = x_value ** (513 + 1) / (513 * (x_value - 1))
    observed = row["post_budget"] / deleted_factor_proxy
    assert abs(float(observed - (1 - x_value**-1))) < 0.01
    assert row["bounded_depth_factor"] == 1 - x_value**-1


def test_terminal_depth_is_complete_strict_upper_band():
    k = 32
    row = exact_endpoint_certificate(k, k - 1)
    x_value = exact_constants()["x"]
    full_band = sum(
        (x_value**m / m for m in range(k + 1, 2 * k)), Fraction(0)
    )
    assert row["post_budget"] == full_band


def test_linear_phase_safe_law_converges():
    rows = [
        linear_depth_diagnostic(k, "0.5", "-0.25")
        for k in (32, 64, 128, 256)
    ]
    post_errors = [abs(Decimal(row["phase_safe_post_over_law"]) - 1) for row in rows]
    ratio_errors = [abs(Decimal(row["phase_safe_ratio_over_law"]) - 1) for row in rows]
    assert post_errors[0] > post_errors[1] > post_errors[2] > post_errors[3]
    assert ratio_errors[0] > ratio_errors[1] > ratio_errors[2] > ratio_errors[3]
    assert all(row["finite_formula_only"] for row in rows)
    assert all(row["synthetic_multiplier_law"] for row in rows)


def test_rational_phase_orbits_are_exact_and_not_collapsed():
    half = rational_phase_orbit(1, 2, 1, 7)
    thirds = rational_phase_orbit(2, 3, -1, 5)
    endpoint = rational_phase_orbit(1, 1, -1, 2)
    assert half["period"] == half["phase_count"] == 2
    assert thirds["period"] == thirds["phase_count"] == 3
    assert endpoint["period"] == endpoint["phase_count"] == 1
    assert endpoint["single_phase"] is True
    assert all(Fraction(0) <= phase < Fraction(1) for phase in thirds["phases"])


@pytest.mark.parametrize("bad", [True, 2.0, "2"])
def test_integer_fields_reject_nonexact_types(bad):
    with pytest.raises(TypeError):
        exact_alias_budget(bad)
    with pytest.raises(TypeError):
        exact_post_budget(8, bad)


@pytest.mark.parametrize("k,L", [(1, 1), (8, 0), (8, 8), (8, -1)])
def test_depth_domain_fails_closed(k, L):
    with pytest.raises(ValueError):
        exact_post_budget(k, L)


@pytest.mark.parametrize("bad_lambda", [LAMBDA_LOWER, LAMBDA_UPPER, 1, 2, True])
def test_lambda_domain_fails_closed(bad_lambda):
    with pytest.raises((TypeError, ValueError)):
        exact_constants(bad_lambda)


def test_phase_inputs_and_endpoint_domain_fail_closed():
    with pytest.raises(TypeError):
        linear_depth_diagnostic(32, 0.5)
    with pytest.raises(ValueError):
        linear_depth_diagnostic(32, "1", "0")
    with pytest.raises(ValueError):
        rational_phase_orbit(0, 1)
