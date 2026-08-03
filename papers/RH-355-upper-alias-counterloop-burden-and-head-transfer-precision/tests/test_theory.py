from decimal import Decimal
from fractions import Fraction

import pytest

from upper_alias_burden import (
    C_M_DIAGNOSTIC,
    FIXTURE_LAMBDA,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    R,
    R_H,
    counterexample_certificate,
    exact_constants,
    exact_terminal_term,
    exact_upper_budget,
    strict_upper_weighted_term,
    synthetic_asymptotic_row,
)


def test_physical_constants_and_fixture_are_exact():
    assert R_H == Fraction(17, 20)
    assert R == Fraction(7, 5)
    assert LAMBDA_LOWER == Fraction(28, 17)
    assert LAMBDA_UPPER == Fraction(17, 10)
    assert LAMBDA_LOWER < FIXTURE_LAMBDA < LAMBDA_UPPER


def test_x_identity_and_superunit_certificate():
    data = exact_constants()
    assert data["x"] == Fraction(2352, 1445)
    assert data["x_identity"] is True
    assert data["x_is_superunit"] is True


@pytest.mark.parametrize("k", [2, 5, 12])
def test_strict_upper_ledger_has_zero_odd_terms(k):
    for n in range(2 * k + 1, 4 * k):
        if n % 2:
            assert strict_upper_weighted_term(k, n) == 0


@pytest.mark.parametrize("k", [2, 5, 12])
def test_strict_upper_even_terms_match_exact_formula(k):
    x_value = exact_constants()["x"]
    for m in range(k + 1, 2 * k):
        assert strict_upper_weighted_term(k, 2 * m) == x_value**m / m


@pytest.mark.parametrize("k", [3, 8, 16])
def test_exact_budget_is_sum_of_all_strict_upper_orders(k):
    direct = sum(
        (
            strict_upper_weighted_term(k, n)
            for n in range(2 * k + 1, 4 * k)
        ),
        Fraction(0),
    )
    data = exact_upper_budget(k)
    assert direct == data["raw_budget"]
    assert data["even_term_count"] == k - 1
    assert data["finite_formula_only"] is True


def test_exact_budget_asymptotic_ratio_moves_toward_one():
    rows = [exact_upper_budget(k) for k in (8, 16, 32, 64)]
    errors = [abs(float(row["normalized_asymptotic_ratio"]) - 1) for row in rows]
    assert errors[0] > errors[1] > errors[2] > errors[3]


@pytest.mark.parametrize("k", [3, 8, 16])
def test_terminal_term_matches_last_budget_summand(k):
    x_value = exact_constants()["x"]
    data = exact_terminal_term(k)
    assert data["n"] == 4 * k - 2
    assert data["raw_term"] == x_value ** (2 * k - 1) / (2 * k - 1)
    assert data["raw_term"] == strict_upper_weighted_term(k, 4 * k - 2)


def test_terminal_asymptotic_and_share_move_to_limits():
    x_value = exact_constants()["x"]
    limit = float((x_value - 1) / x_value)
    rows = [exact_terminal_term(k) for k in (8, 16, 32, 64)]
    ratio_errors = [abs(float(row["normalized_asymptotic_ratio"]) - 1) for row in rows]
    share_errors = [abs(float(row["terminal_over_budget"]) - limit) for row in rows]
    assert ratio_errors[0] > ratio_errors[-1]
    assert share_errors[0] > share_errors[1] > share_errors[2] > share_errors[3]


@pytest.mark.parametrize("k", [2, 8, 32])
def test_complete_shell_counterexample_is_exact(k):
    data = counterexample_certificate(k)
    assert data["N"] == 2 * k + 2
    assert data["N_in_strict_upper_band"] is True
    assert data["only_one_shell_multiple_in_band"] is True
    assert data["relative_error_at_N"] == 1
    assert data["normalized_identity"] is True
    assert data["finite_formula_only"] is True


def test_counterexample_normalized_defect_decays_but_raw_grows():
    rows = [counterexample_certificate(k) for k in (8, 16, 32, 64)]
    normalized = [row["normalized_defect"] for row in rows]
    raw = [row["raw_defect"] for row in rows]
    assert normalized[0] > normalized[1] > normalized[2] > normalized[3] > 0
    assert raw[0] < raw[1] < raw[2] < raw[3]


def test_physical_synthetic_rows_converge_to_declared_ratios():
    rows = [synthetic_asymptotic_row(k) for k in (8, 16, 32, 64)]
    budget_errors = [abs(Decimal(row["budget_asymptotic_ratio"]) - 1) for row in rows]
    terminal_errors = [abs(Decimal(row["terminal_asymptotic_ratio"]) - 1) for row in rows]
    shell_errors = [abs(Decimal(row["counterexample_scaled_ratio"]) - 1) for row in rows]
    assert budget_errors[0] > budget_errors[-1]
    assert terminal_errors[0] > terminal_errors[-1]
    assert shell_errors[0] > shell_errors[1] > shell_errors[2] > shell_errors[3]


def test_normalized_budget_root_moves_toward_x():
    rows = [synthetic_asymptotic_row(k) for k in (16, 32, 64)]
    x_value = Decimal(rows[-1]["x"])
    errors = [abs(Decimal(row["normalized_budget_root"]) - x_value) for row in rows]
    assert errors[0] > errors[1] > errors[2]


@pytest.mark.parametrize("bad", [True, 2.0, "2"])
def test_integer_fields_reject_nonexact_types(bad):
    with pytest.raises(TypeError):
        exact_upper_budget(bad)
    with pytest.raises(TypeError):
        exact_terminal_term(bad)
    with pytest.raises(TypeError):
        counterexample_certificate(bad)


@pytest.mark.parametrize("bad_k", [0, 1, -3])
def test_k_domain_fails_closed(bad_k):
    with pytest.raises(ValueError):
        exact_upper_budget(bad_k)
    with pytest.raises(ValueError):
        synthetic_asymptotic_row(bad_k)


@pytest.mark.parametrize("bad_lambda", [LAMBDA_LOWER, LAMBDA_UPPER, 1, 2])
def test_lambda_domain_fails_closed(bad_lambda):
    with pytest.raises(ValueError):
        exact_constants(bad_lambda)


def test_strict_band_domain_fails_closed():
    with pytest.raises(ValueError):
        strict_upper_weighted_term(8, 16)
    with pytest.raises(ValueError):
        strict_upper_weighted_term(8, 32)


def test_decimal_inputs_are_strict_and_positive():
    with pytest.raises(TypeError):
        synthetic_asymptotic_row(8, 1.67, C_M_DIAGNOSTIC)
    with pytest.raises(ValueError):
        synthetic_asymptotic_row(8, "1.67", "0")
    with pytest.raises(ValueError):
        synthetic_asymptotic_row(8, "2", C_M_DIAGNOSTIC)
