from decimal import Decimal
from fractions import Fraction

import pytest

from tilt_phase_transition import (
    FIXTURE_LAMBDA,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    R,
    R_H,
    critical_metrics,
    exact_constants,
    exact_generating_function,
    exact_terminal_distribution,
    subcritical_metrics,
    supercritical_metrics,
    transform_certificate,
)


def test_exact_physical_constants_are_strict():
    data = exact_constants()
    assert R_H == Fraction(17, 20)
    assert R == Fraction(7, 5)
    assert LAMBDA_LOWER < FIXTURE_LAMBDA < LAMBDA_UPPER
    assert data["x"] == Fraction(2352, 1445)
    assert data["x_identity"] is True
    assert data["x_is_superunit"] is True


@pytest.mark.parametrize("k", [4, 8, 16, 24])
def test_terminal_distribution_is_exact_probability(k):
    probabilities = exact_terminal_distribution(k)
    assert len(probabilities) == k - 1
    assert sum(probabilities, Fraction(0)) == 1
    assert all(probability > 0 for probability in probabilities)


def test_generating_function_special_values():
    assert exact_generating_function(16, 0) == exact_terminal_distribution(16)[0]
    assert exact_generating_function(16, 1) == 1


def test_subcritical_transform_converges():
    rows = [transform_certificate(k, Fraction(1, 2)) for k in (16, 32, 64, 128)]
    errors = [abs(float(row["observed_over_target_or_k"] - 1)) for row in rows]
    assert errors == sorted(errors, reverse=True)
    assert all(row["regime"] == "subcritical" for row in rows)


def test_supercritical_transform_converges():
    rows = [transform_certificate(k, 2) for k in (16, 32, 64, 128)]
    errors = [abs(float(row["observed_over_target_or_k"] - 1)) for row in rows]
    assert errors == sorted(errors, reverse=True)
    assert all(row["regime"] == "supercritical" for row in rows)


def test_critical_transform_and_scaled_mean_converge():
    rows = [critical_metrics(k) for k in (16, 32, 64, 128)]
    transform_errors = [abs(Decimal(row["transform_ratio"]) - 1) for row in rows]
    mean_errors = [Decimal(row["absolute_mean_error"]) for row in rows]
    assert transform_errors == sorted(transform_errors, reverse=True)
    assert mean_errors == sorted(mean_errors, reverse=True)
    assert all(row["finite_formula_only"] for row in rows)


def test_subcritical_tilt_converges_in_total_variation():
    rows = [subcritical_metrics(k) for k in (16, 32, 64, 128)]
    errors = [float(row["l1_to_geometric"]) for row in rows]
    assert errors == sorted(errors, reverse=True)
    assert all(row["probability_sum"] == 1 for row in rows)
    assert all(row["total_variation_to_geometric"] * 2 == row["l1_to_geometric"] for row in rows)


def test_supercritical_opposite_endpoint_tilt_converges():
    rows = [supercritical_metrics(k) for k in (16, 32, 64, 128)]
    errors = [float(row["l1_to_geometric"]) for row in rows]
    assert errors == sorted(errors, reverse=True)
    assert all(row["ell_probability_sum"] == 1 for row in rows)
    assert all(row["total_variation_to_geometric"] * 2 == row["l1_to_geometric"] for row in rows)


def test_zero_subcritical_tilt_is_delta_zero():
    row = subcritical_metrics(16, 0)
    assert row["l1_to_geometric"] == 0


@pytest.mark.parametrize("bad", [True, 2.0, "2"])
def test_integer_fields_reject_nonexact_types(bad):
    with pytest.raises(TypeError):
        exact_terminal_distribution(bad)


@pytest.mark.parametrize("bad_z", [True, 1.5, "1"])
def test_tilt_rejects_nonexact_types(bad_z):
    with pytest.raises(TypeError):
        exact_generating_function(16, bad_z)


def test_negative_tilt_fails_closed():
    with pytest.raises(ValueError):
        exact_generating_function(16, -1)
    with pytest.raises(ValueError):
        transform_certificate(16, -1)


def test_regime_domains_fail_closed():
    with pytest.raises(ValueError):
        subcritical_metrics(16, 1)
    with pytest.raises(ValueError):
        supercritical_metrics(16, 1)


@pytest.mark.parametrize("bad_lambda", [LAMBDA_LOWER, LAMBDA_UPPER, 1, 2, True])
def test_lambda_domain_fails_closed(bad_lambda):
    with pytest.raises((TypeError, ValueError)):
        exact_constants(bad_lambda)


def test_order_domain_fails_closed():
    with pytest.raises(ValueError):
        exact_terminal_distribution(1)
