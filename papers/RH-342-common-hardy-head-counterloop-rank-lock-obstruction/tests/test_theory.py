from decimal import Decimal, localcontext
from fractions import Fraction

import pytest

from head_rank_lock import (
    HIDDEN_RADIUS,
    Q_HEAD,
    R_H,
    R_TRACE,
    common_clock_thresholds,
    counterloop_power_sum,
    counterloop_rank,
    finite_diagnostic,
    genus_one_log_coefficient,
    hidden_shell_power_sum,
    hidden_shell_rank,
    physical_constants,
    rank_lock_lower_bound,
    root_l1_budget_bound,
    shifted_uniqueness_certificate,
    strict_prefix_aliases,
)


def test_exact_radii_and_source_head_cut():
    assert Q_HEAD == Fraction(1, 2)
    assert R_H == Fraction(17, 20)
    assert R_TRACE == Fraction(7, 5)
    assert HIDDEN_RADIUS == Fraction(3, 4)
    assert HIDDEN_RADIUS > Q_HEAD


def test_counterloop_rank_moment_and_alias_ledger():
    beta = Decimal("0.9")
    for k in (2, 3, 5, 9):
        assert counterloop_rank(k) == 2 * k - 2
        assert counterloop_power_sum(k, 1, beta) == 0
        assert counterloop_power_sum(k, 2, beta) == -2 * beta**2
        assert counterloop_power_sum(k, 2 * k, beta) == (2 * k - 2) * beta ** (2 * k)
        aliases = strict_prefix_aliases(k)
        assert aliases["contains_first_alias"] is True
        assert aliases["contains_second_alias"] is False
        assert aliases["cut"] == 4 * k


def test_rank_lock_is_zero_only_at_equal_rank():
    beta = physical_constants()["beta"]
    for k in (3, 5, 9):
        model_rank = counterloop_rank(k)
        assert rank_lock_lower_bound(model_rank, model_rank, beta) == 0
        assert rank_lock_lower_bound(model_rank + 1, model_rank, beta) == Decimal("0.5")
        assert rank_lock_lower_bound(model_rank - 1, model_rank, beta) == beta


def test_shifted_moment_degree_certificate():
    for cap in (2, 4, 8):
        cert = shifted_uniqueness_certificate(cap, cap, cap)
        assert cert["moment_first"] == 2
        assert cert["moment_last"] == 2 * cap + 1
        assert cert["coefficient_count"] == 2 * cap
        assert cert["numerator_degree_bound"] == 2 * cap - 1
        assert cert["vanishing_order"] == 2 * cap
        assert cert["degree_forces_zero_numerator"] is True


def test_shifted_certificate_rejects_missing_rank_cap():
    with pytest.raises(ValueError):
        shifted_uniqueness_certificate(3, 4, 3)
    with pytest.raises(ValueError):
        shifted_uniqueness_certificate(0, 0, 0)


def test_hidden_shell_is_invisible_exactly_below_4k():
    for k in (2, 3, 5, 9):
        assert hidden_shell_rank(k) == 4 * k
        assert all(hidden_shell_power_sum(k, n) == 0 for n in range(2, 4 * k))
        assert hidden_shell_power_sum(k, 4 * k) == 4 * k * Fraction(3, 4) ** (4 * k)
        model_rank = counterloop_rank(k)
        enlarged_rank = model_rank + hidden_shell_rank(k)
        beta = physical_constants()["beta"]
        assert rank_lock_lower_bound(enlarged_rank, model_rank, beta) == Decimal(2 * k)


def test_genus_one_log_coefficient_is_shifted():
    assert genus_one_log_coefficient(Fraction(7, 5), 2) == Fraction(-7, 10)
    assert genus_one_log_coefficient(Fraction(-3, 2), 3) == Fraction(1, 2)
    with pytest.raises(ValueError):
        genus_one_log_coefficient(Fraction(1), 1)


def test_rh299_thresholds_are_the_two_distinct_values():
    thresholds = common_clock_thresholds()
    assert abs(thresholds["global_threshold"] - Decimal("1.9268138890340046")) < Decimal("1e-16")
    assert abs(thresholds["local_threshold"] - Decimal("0.9268138890340046")) < Decimal("1e-16")
    assert abs(thresholds["threshold_gap"] - Decimal(1)) < Decimal("1e-80")
    assert abs(thresholds["global_cap"] - Decimal(20) / 17) < Decimal("1e-27")
    assert thresholds["local_shell_cap"] > Decimal("0.9")


def test_root_l1_budget_bound_matches_direct_geometric_sum():
    distance = Fraction(1, 100)
    cap = Fraction(20, 17)
    cut = 12
    bound = root_l1_budget_bound(distance, cap, cut)
    with localcontext() as context:
        context.prec = 100
        ratio = Decimal(28) / 17
        expected = Decimal(1) / 100 * Decimal(7) / 5 * sum(
            (ratio**j for j in range(1, cut - 1)), Decimal(0)
        )
    assert abs(bound - expected) < Decimal("1e-90")


def test_finite_rows_remain_formula_checks_only():
    for k in (3, 5, 9, 17):
        row = finite_diagnostic(k)
        assert row["hidden_shell_prefix_moment_zero"] is True
        assert row["padded_distance_lower_bound"] == Decimal(2 * k)
        assert row["enlarged_rank"] == 6 * k - 2
        assert row["finite_row_is_reproduction_only"] is True


def test_invalid_inputs_fail_closed():
    with pytest.raises(ValueError):
        counterloop_rank(True)
    with pytest.raises(ValueError):
        hidden_shell_power_sum(1, 4)
    with pytest.raises(ValueError):
        rank_lock_lower_bound(-1, 2, Decimal("0.9"))
    with pytest.raises(ValueError):
        root_l1_budget_bound(Fraction(-1), Fraction(1), 4)
