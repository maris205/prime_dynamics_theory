from decimal import Decimal
from fractions import Fraction

import pytest

from log_window_accuracy import (
    FIXTURE_LAMBDA,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    R,
    R_H,
    exact_constants,
    exact_full_budget,
    exact_minimal_width,
    exact_tail_ratio,
    exact_window_certificate,
    logarithmic_window_diagnostic,
    phase_cover_diagnostic,
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
def test_zero_width_is_full_tail(k):
    assert exact_tail_ratio(k, 0) == 1
    assert exact_full_budget(k) > 0


def test_exact_tail_is_strictly_decreasing():
    rows = [exact_tail_ratio(24, q) for q in range(23)]
    assert all(left > right for left, right in zip(rows, rows[1:]))


@pytest.mark.parametrize("k", [16, 32, 64, 128])
def test_exact_minimal_width_certificate(k):
    row = exact_window_certificate(k, 2, 0)
    width = row["minimal_width"]
    target = row["target"]
    assert width == exact_minimal_width(k, 2, 0)
    assert row["tail_at_width"] <= target
    assert row["previous_tail"] > target
    assert row["tail_meets_target"] is True
    assert row["previous_fails_target"] is True
    assert row["strict_tail_monotonicity"] is True
    assert row["finite_formula_only"] is True


def test_x_shift_changes_exact_target_and_width_monotonically():
    low = exact_window_certificate(64, 2, -1)
    middle = exact_window_certificate(64, 2, 0)
    high = exact_window_certificate(64, 2, 1)
    assert low["target"] > middle["target"] > high["target"]
    assert low["minimal_width"] <= middle["minimal_width"] <= high["minimal_width"]


def test_logarithmic_phase_law_converges():
    rows = [logarithmic_window_diagnostic(k) for k in (32, 64, 128, 256)]
    errors = [
        abs(Decimal(row["normalized_over_phase_law"]) - 1) for row in rows
    ]
    assert errors == sorted(errors, reverse=True)
    assert errors[-1] < errors[0]
    assert all(row["finite_formula_only"] for row in rows)


def test_minimal_width_correction_stays_in_coarse_bracket():
    rows = [logarithmic_window_diagnostic(k) for k in (32, 64, 128, 256)]
    assert all(row["correction_in_coarse_interval"] for row in rows)
    assert all(
        Decimal(-1) < Decimal(row["minimal_width_correction"]) < Decimal(2)
        for row in rows
    )


def test_finite_phase_cover_is_explicitly_not_a_proof():
    rows = [phase_cover_diagnostic(10, stop, 10) for stop in (100, 1000, 10000)]
    counts = [row["occupied_count"] for row in rows]
    assert counts == sorted(counts)
    assert rows[-1]["occupied_count"] == 10
    assert all(row["finite_coverage_is_not_density_proof"] for row in rows)


@pytest.mark.parametrize("bad", [True, 2.0, "2"])
def test_integer_fields_reject_nonexact_types(bad):
    with pytest.raises(TypeError):
        exact_full_budget(bad)
    with pytest.raises(TypeError):
        exact_tail_ratio(8, bad)
    with pytest.raises(TypeError):
        exact_minimal_width(16, bad)


@pytest.mark.parametrize("k,q", [(1, 0), (8, -1), (8, 7), (8, 8)])
def test_tail_domain_fails_closed(k, q):
    with pytest.raises(ValueError):
        exact_tail_ratio(k, q)


@pytest.mark.parametrize("bad_lambda", [LAMBDA_LOWER, LAMBDA_UPPER, 1, 2, True])
def test_lambda_domain_fails_closed(bad_lambda):
    with pytest.raises((TypeError, ValueError)):
        exact_constants(bad_lambda)


def test_accuracy_power_must_be_positive():
    with pytest.raises(ValueError):
        exact_minimal_width(16, 0)
    with pytest.raises(ValueError):
        exact_window_certificate(16, -1)


def test_decimal_inputs_fail_closed():
    with pytest.raises(TypeError):
        logarithmic_window_diagnostic(32, a_text=2)
    with pytest.raises(ValueError):
        logarithmic_window_diagnostic(32, a_text="0")
    with pytest.raises(ValueError):
        logarithmic_window_diagnostic(32, lambda_text="1")


def test_phase_cover_domain_fails_closed():
    with pytest.raises(ValueError):
        phase_cover_diagnostic(100, 10)
    with pytest.raises(ValueError):
        phase_cover_diagnostic(10, 100, bins=1)
    with pytest.raises(TypeError):
        phase_cover_diagnostic(10, 100, a_text=2)
