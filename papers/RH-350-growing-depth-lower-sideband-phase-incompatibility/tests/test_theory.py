from decimal import Decimal, localcontext

import pytest

from growing_sideband_phase import (
    balance_phase,
    growing_row,
    physical_constants,
    relative_minimax,
    relative_objective,
    sideband_entry,
    weighted_minimax,
    weighted_objective,
)


def test_balance_phase_solves_a_k_equal_one():
    constants = physical_constants()
    lam = constants["lambda"]
    from growing_sideband_phase import C_M_DIAGNOSTIC, C_STAR_DIAGNOSTIC

    value = (
        C_STAR_DIAGNOSTIC
        * C_M_DIAGNOSTIC
        * ((balance_phase() - 2) * lam.ln()).exp()
    )
    assert abs(value - 1) < Decimal("1e-25")


def test_x_lambda_has_the_exact_rational_value_and_exceeds_two():
    constants = physical_constants()
    with localcontext() as context:
        context.prec = 100
        exact = (Decimal(28) / Decimal(17)) ** 2
    assert abs(constants["x_lambda"] - exact) < Decimal("1e-90")
    assert constants["x_lambda"] > 2


def test_relative_minimax_formula_is_attained_for_multiple_depths():
    constants = physical_constants()
    for depth in (3, 5, 8, 12):
        ledger = relative_minimax(depth)
        assert abs(
            ledger["objective_at_optimizer"] - ledger["minimum"]
        ) < Decimal("1e-90")
        with localcontext() as context:
            context.prec = 100
            objective = relative_objective(
                ledger["optimizer"], constants["lambda"], depth
            )
        assert abs(objective - ledger["minimum"]) < Decimal("1e-90")


def test_relative_minimax_increases_toward_one():
    values = [relative_minimax(depth)["minimum"] for depth in (3, 5, 8, 12)]
    assert values == sorted(values)
    assert values[-1] < 1
    assert values[-1] > Decimal("0.98")


def test_weighted_minimax_is_attained_at_a_one():
    constants = physical_constants()
    for n in (1, 3, 6, 10):
        ledger = weighted_minimax(n)
        assert ledger["optimizer"] == 1
        assert abs(
            ledger["objective_at_optimizer"] - ledger["minimum"]
        ) < Decimal("1e-90")
        with localcontext() as context:
            context.prec = 100
            objective = weighted_objective(
                Decimal(1), constants["lambda"], constants["x"], n
            )
        assert abs(objective - ledger["minimum"]) < Decimal("1e-90")


def test_weighted_minimum_is_strict_near_the_optimizer():
    constants = physical_constants()
    ledger = weighted_minimax(6)
    for value in (Decimal("0.9"), Decimal("1.1"), Decimal("1.5")):
        assert weighted_objective(
            value, constants["lambda"], constants["x"], 6
        ) > ledger["minimum"]


def test_weighted_minima_increase_to_the_positive_limit():
    ledgers = [weighted_minimax(n) for n in (1, 3, 6, 10)]
    minima = [ledger["minimum"] for ledger in ledgers]
    gaps = [ledger["gap_to_limit"] for ledger in ledgers]
    assert minima == sorted(minima)
    assert gaps == sorted(gaps, reverse=True)
    assert ledgers[-1]["limit"] > 0


def test_sideband_indexing_and_phase_targets_are_exact():
    constants = physical_constants()
    lam = constants["lambda"]
    entries = [sideband_entry(28, j) for j in range(2, 6)]
    assert [entry["m"] for entry in entries] == [26, 25, 24, 23]
    assert [entry["order"] for entry in entries] == [52, 50, 48, 46]
    with localcontext() as context:
        context.prec = 100
        expected = [lam ** (2 - j) for j in range(2, 6)]
    assert [entry["phase_target"] for entry in entries] == expected


def test_finite_uniform_formula_errors_decrease_across_rows():
    rows = [growing_row(k, depth) for k, depth in ((18, 4), (28, 5), (40, 6), (56, 7))]
    demand = [row["max_demand_uniform_error"] for row in rows]
    parity = [row["max_parity_uniform_error"] for row in rows]
    assert demand == sorted(demand, reverse=True)
    assert parity == sorted(parity, reverse=True)
    assert demand[-1] < Decimal("0.02")
    assert parity[-1] < Decimal("1e-9")


def test_finite_weighted_fixture_approaches_its_minimax_reference():
    rows = [growing_row(k, depth) for k, depth in ((18, 4), (28, 5), (40, 6), (56, 7))]
    errors = [row["normalized_absolute_error"] for row in rows]
    assert errors == sorted(errors, reverse=True)
    assert errors[-1] < Decimal("0.03")


def test_invalid_domains_fail_closed():
    constants = physical_constants()
    with pytest.raises(ValueError):
        physical_constants(40)
    with pytest.raises(ValueError):
        relative_minimax(2)
    with pytest.raises(ValueError):
        weighted_minimax(0)
    with pytest.raises(ValueError):
        relative_objective(Decimal(0), constants["lambda"], 3)
    with pytest.raises(ValueError):
        weighted_objective(Decimal(1), constants["lambda"], Decimal(1), 2)
    with pytest.raises(ValueError):
        sideband_entry(8, 7)
    with pytest.raises(ValueError):
        growing_row(8, 7)
