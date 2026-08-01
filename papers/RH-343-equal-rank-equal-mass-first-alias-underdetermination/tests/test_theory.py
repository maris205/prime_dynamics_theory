from fractions import Fraction

import pytest

from first_alias_underdetermination import (
    A_RADIUS,
    B_RADIUS,
    C_RADIUS_SQUARED,
    Q_HEAD,
    R_H,
    R_TRACE,
    candidate_rank,
    counterloop_rank,
    extra_squared_mass,
    finite_diagnostic,
    full_shell_power_sum,
    genus_one_quotient_factor,
    invisible_shell_power_sum,
    moment_difference,
    pre_alias_certificate,
    radius_order_certificate,
    strict_prefix_budget,
    total_squared_mass,
    visible_budget_formula,
    visible_shell_power_sum,
)


def test_exact_constants_and_radius_order():
    assert Q_HEAD == Fraction(1, 2)
    assert R_H == Fraction(17, 20)
    assert R_TRACE == Fraction(7, 5)
    assert A_RADIUS == Fraction(3, 4)
    assert B_RADIUS == Fraction(4, 5)
    assert C_RADIUS_SQUARED == Fraction(481, 800)
    cert = radius_order_certificate()
    assert cert["q_lt_a"] is True
    assert cert["a_lt_c_lt_b_exact_by_squares"] is True
    assert cert["b_lt_beta_limit"] is True
    assert cert["beta_limit_lt_global_cap"] is True


def test_complete_shell_power_identity_for_rational_radii():
    for length in (4, 6, 10):
        for radius in (A_RADIUS, B_RADIUS):
            assert all(
                full_shell_power_sum(length, radius, order) == 0
                for order in range(1, length)
            )
            assert full_shell_power_sum(length, radius, length) == length * radius**length


def test_invisible_irrational_radius_shell_is_exactly_handled_by_its_square():
    for k in (2, 3, 5, 9):
        assert all(invisible_shell_power_sum(k, n) == 0 for n in range(1, 4 * k))
        assert invisible_shell_power_sum(k, 4 * k) == 4 * k * C_RADIUS_SQUARED ** (2 * k)


def test_common_rank_is_6k_minus_2():
    for k in (2, 3, 5, 9):
        assert counterloop_rank(k) == 2 * k - 2
        assert candidate_rank(k) == counterloop_rank(k) + 4 * k == 6 * k - 2


def test_extra_squared_spectral_masses_are_exactly_equal():
    for k in (2, 3, 5, 9):
        expected = Fraction(481 * k, 200)
        assert extra_squared_mass("invisible", k) == expected
        assert extra_squared_mass("visible", k) == expected


def test_total_squared_mass_equality_retains_the_counterloop_term():
    beta_squared = Fraction(81, 100)
    for k in (2, 5, 9):
        expected = (2 * k - 2) * beta_squared + Fraction(481 * k, 200)
        assert total_squared_mass("invisible", k, beta_squared) == expected
        assert total_squared_mass("visible", k, beta_squared) == expected


def test_both_candidates_equal_Y_before_first_alias_and_split_at_2k():
    for k in (2, 3, 5, 9):
        cert = pre_alias_certificate(k)
        assert cert["invisible_equals_Y_pre_alias"] is True
        assert cert["visible_equals_Y_pre_alias"] is True
        assert cert["split_order"] == 2 * k
        assert cert["invisible_difference_at_split"] == 0
        assert cert["visible_difference_at_split"] == 2 * k * (
            A_RADIUS ** (2 * k) + B_RADIUS ** (2 * k)
        )


def test_candidates_are_not_equal_on_the_whole_strict_prefix():
    for k in (2, 3, 5, 9):
        assert moment_difference("invisible", k, 2 * k) == 0
        assert moment_difference("visible", k, 2 * k) > 0
        assert visible_shell_power_sum(k, 4 * k - 1) == 0


def test_strict_prefix_budgets_keep_the_exact_one_over_n_cancellation():
    for k in (2, 3, 5, 9):
        direct_alias_term = (
            2 * k * (A_RADIUS ** (2 * k) + B_RADIUS ** (2 * k))
            * R_TRACE ** (2 * k)
            / (2 * k)
        )
        assert strict_prefix_budget("invisible", k) == 0
        assert strict_prefix_budget("visible", k) == direct_alias_term
        assert direct_alias_term == visible_budget_formula(k)


def test_visible_budget_has_two_superunit_bases_and_grows():
    assert A_RADIUS * R_TRACE == Fraction(21, 20) > 1
    assert B_RADIUS * R_TRACE == Fraction(28, 25) > 1
    values = [visible_budget_formula(k) for k in (2, 3, 5, 9)]
    assert values == sorted(values)
    assert len(set(values)) == len(values)


def test_genus_one_quotient_factors_are_exactly_declared():
    assert genus_one_quotient_factor("invisible") == "1-(c*z)^(4k)"
    assert genus_one_quotient_factor("visible") == "[1-(a*z)^(2k)][1-(b*z)^(2k)]"


def test_finite_rows_are_identity_checks_only():
    for k in (3, 5, 9, 17):
        row = finite_diagnostic(k)
        assert row["common_rank"] == 6 * k - 2
        assert row["mass_equal"] is True
        assert row["both_pre_alias_equal_Y"] is True
        assert row["D_4k_invisible"] == 0
        assert row["D_4k_visible"] == row["visible_budget_formula"]
        assert row["finite_row_is_exact_reproduction_only"] is True


def test_invalid_inputs_fail_closed():
    with pytest.raises(ValueError):
        candidate_rank(True)
    with pytest.raises(ValueError):
        full_shell_power_sum(1, A_RADIUS, 2)
    with pytest.raises(ValueError):
        full_shell_power_sum(4, Fraction(0), 2)
    with pytest.raises(ValueError):
        extra_squared_mass("other", 2)
    with pytest.raises(ValueError):
        total_squared_mass("invisible", 2, Fraction(0))
    with pytest.raises(ValueError):
        strict_prefix_budget("other", 2)
