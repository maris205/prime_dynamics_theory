from decimal import Decimal
from fractions import Fraction

import pytest

from terminal_lag_localization import (
    FIXTURE_LAMBDA,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    R,
    R_H,
    distribution_metrics,
    exact_constants,
    exact_full_budget,
    exact_partial_budget,
    exact_profile_certificate,
    exact_profile_proxy,
    exact_terminal_distribution,
    synthetic_profile_diagnostic,
    uniform_profile_error_envelope,
)


def test_exact_physical_constants_are_strict():
    data = exact_constants()
    assert R_H == Fraction(17, 20)
    assert R == Fraction(7, 5)
    assert LAMBDA_LOWER < FIXTURE_LAMBDA < LAMBDA_UPPER
    assert data["x"] == Fraction(2352, 1445)
    assert data["x_identity"] is True
    assert data["x_is_superunit"] is True


@pytest.mark.parametrize("k,q", [(4, 0), (8, 3), (16, 8), (24, 22)])
def test_exact_tail_identity_and_probability_normalization(k, q):
    row = exact_profile_certificate(k, q)
    distribution = exact_terminal_distribution(k)
    assert row["full_budget"] == exact_full_budget(k)
    assert row["partial_budget"] == exact_partial_budget(k, q)
    assert row["tail_ratio"] == row["partial_budget"] / row["full_budget"]
    assert row["tail_ratio"] == sum(distribution[q:], Fraction(0))
    assert row["tail_identity"] is True
    assert row["probability_normalization"] is True
    assert row["finite_formula_only"] is True


def test_zero_lag_is_the_complete_band_exactly():
    row = exact_profile_certificate(20, 0)
    assert row["partial_budget"] == row["full_budget"]
    assert row["tail_ratio"] == 1
    assert row["profile_proxy"] == 1
    assert row["retained_terminal_mass"] == 0


def test_maximum_lag_is_the_first_post_alias_coordinate():
    k = 24
    x_value = exact_constants()["x"]
    row = exact_profile_certificate(k, k - 2)
    assert row["residual_depth"] == 1
    assert row["partial_budget"] == x_value ** (k + 1) / (k + 1)


def test_uniform_profile_error_is_order_one_over_k_on_full_lag_range():
    rows = [uniform_profile_error_envelope(k) for k in (8, 16, 32, 64)]
    errors = [float(row["max_relative_error"]) for row in rows]
    assert errors[0] > errors[1] > errors[2] > errors[3]
    assert all(float(row["k_times_max_relative_error"]) < 1.5 for row in rows)
    assert all(row["lag_count"] == row["k"] - 1 for row in rows)


def test_fixed_lag_tail_converges_to_x_minus_q():
    x_value = exact_constants()["x"]
    q = 3
    errors = [
        abs(float(exact_profile_certificate(k, q)["tail_ratio"] / x_value**-q - 1))
        for k in (32, 64, 128)
    ]
    assert errors[0] > errors[1] > errors[2]


def test_linear_lag_prefactor_is_not_one():
    x_value = exact_constants()["x"]
    rows = []
    for k in (32, 64, 128):
        q = k // 4
        target = Fraction(8, 7) * x_value**(-q)
        rows.append(abs(float(exact_profile_certificate(k, q)["tail_ratio"] / target - 1)))
    assert rows[0] > rows[1] > rows[2]


def test_fixed_residual_depth_retains_finite_tail_factor():
    x_value = exact_constants()["x"]
    ell = 3
    errors = []
    for k in (32, 64, 128):
        q = k - 1 - ell
        target = 2 * x_value**(-q) * (1 - x_value**-ell)
        ratio = exact_profile_certificate(k, q)["tail_ratio"]
        errors.append(abs(float(ratio / target - 1)))
    assert errors[0] > errors[1] > errors[2]


def test_distribution_converges_in_l1_and_moments():
    rows = [distribution_metrics(k) for k in (16, 32, 64, 128)]
    l1_errors = [float(row["l1_to_geometric"]) for row in rows]
    mean_errors = [float(row["absolute_mean_error"]) for row in rows]
    variance_errors = [float(row["absolute_variance_error"]) for row in rows]
    assert l1_errors == sorted(l1_errors, reverse=True)
    assert mean_errors == sorted(mean_errors, reverse=True)
    assert variance_errors == sorted(variance_errors, reverse=True)
    assert all(row["probability_sum"] == 1 for row in rows)
    assert all(row["total_variation_to_geometric"] * 2 == row["l1_to_geometric"] for row in rows)


def test_synthetic_source_locked_linear_profile_converges():
    rows = [synthetic_profile_diagnostic(k, k // 4) for k in (32, 64, 128, 256)]
    source_errors = [
        abs(Decimal(row["tail_over_source_proxy"]) - 1) for row in rows
    ]
    theta_errors = [
        abs(Decimal(row["tail_over_linear_theta_law"]) - 1) for row in rows
    ]
    assert source_errors == sorted(source_errors, reverse=True)
    assert theta_errors == sorted(theta_errors, reverse=True)
    assert all(row["finite_formula_only"] for row in rows)
    assert all(row["synthetic_multiplier_law"] for row in rows)


def test_synthetic_fixed_residual_depth_law_converges():
    rows = [synthetic_profile_diagnostic(k, k - 4) for k in (32, 64, 128, 256)]
    errors = [
        abs(Decimal(row["tail_over_fixed_residual_depth_law"]) - 1)
        for row in rows
    ]
    assert errors == sorted(errors, reverse=True)


@pytest.mark.parametrize("bad", [True, 2.0, "2"])
def test_integer_fields_reject_nonexact_types(bad):
    with pytest.raises(TypeError):
        exact_full_budget(bad)
    with pytest.raises(TypeError):
        exact_partial_budget(8, bad)


@pytest.mark.parametrize("k,q", [(1, 0), (8, -1), (8, 7), (8, 8)])
def test_lag_domain_fails_closed(k, q):
    with pytest.raises(ValueError):
        exact_partial_budget(k, q)
    with pytest.raises(ValueError):
        exact_profile_proxy(k, q)


@pytest.mark.parametrize("bad_lambda", [LAMBDA_LOWER, LAMBDA_UPPER, 1, 2, True])
def test_lambda_domain_fails_closed(bad_lambda):
    with pytest.raises((TypeError, ValueError)):
        exact_constants(bad_lambda)


def test_decimal_diagnostic_inputs_fail_closed():
    with pytest.raises(TypeError):
        synthetic_profile_diagnostic(32, 8, lambda_text=1.67)
    with pytest.raises(ValueError):
        synthetic_profile_diagnostic(32, 8, lambda_text="1")
    with pytest.raises(ValueError):
        synthetic_profile_diagnostic(32, 8, c_m_text="0")
