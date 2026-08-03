from decimal import Decimal

import pytest

from two_sideband_phase import (
    balance_phase_j2,
    minimax_ledger,
    physical_constants,
    relative_objective,
    sideband_entry,
    two_sideband_row,
    weighted_objective,
)


def test_j2_balance_phase_solves_the_exact_diagnostic_equation():
    constants = physical_constants()
    lam = constants["lambda"]
    from two_sideband_phase import C_M_DIAGNOSTIC, C_STAR_DIAGNOSTIC

    ratio = (
        C_STAR_DIAGNOSTIC
        * C_M_DIAGNOSTIC
        * ((balance_phase_j2() - 2) * lam.ln()).exp()
    )
    assert abs(ratio - 1) < Decimal("1e-26")


def test_sideband_indexing_is_exactly_j2_and_j3():
    for k in (10, 18, 30):
        entries = [sideband_entry(k, j) for j in (2, 3)]
        assert [entry["m"] for entry in entries] == [k - 2, k - 3]
        assert [entry["order"] for entry in entries] == [2 * k - 4, 2 * k - 6]


def test_fixed_phase_ratios_approach_one_and_inverse_lambda():
    constants = physical_constants()
    lam = constants["lambda"]
    rows = [two_sideband_row(k) for k in (10, 18, 30, 46)]
    last = rows[-1]["entries"]
    assert abs(last[0]["parity_over_demand"] - 1) < Decimal("0.04")
    assert abs(last[1]["parity_over_demand"] - 1 / lam) < Decimal("0.04")
    for index, target in ((0, Decimal(1)), (1, 1 / lam)):
        errors = [abs(row["entries"][index]["parity_over_demand"] - target) for row in rows]
        assert errors[-1] < errors[0]


def test_demand_scale_is_reproduced_at_both_fixed_sidebands():
    rows = [two_sideband_row(k) for k in (10, 18, 30, 46)]
    for index in (0, 1):
        errors = [abs(row["entries"][index]["demand_over_reference"] - 1) for row in rows]
        assert errors[-1] < errors[0]
        assert errors[-1] < Decimal("0.04")


def test_relative_minimax_identity_and_optimizer():
    constants = physical_constants()
    lam = constants["lambda"]
    ledger = minimax_ledger()
    assert abs(
        ledger["relative_objective_at_optimizer"]
        - ledger["relative_minimum"]
    ) < Decimal("1e-95")
    optimizer = ledger["relative_optimizer"]
    assert relative_objective(Decimal(1), lam) > relative_objective(optimizer, lam)
    assert relative_objective(lam, lam) > relative_objective(optimizer, lam)


def test_physically_weighted_minimum_occurs_at_a_one():
    constants = physical_constants()
    lam = constants["lambda"]
    x = constants["x"]
    ledger = minimax_ledger()
    assert ledger["weighted_objective_at_optimizer"] == ledger["weighted_minimum"]
    assert weighted_objective(Decimal("0.9"), lam, x) > ledger["weighted_minimum"]
    assert weighted_objective(Decimal("1.1"), lam, x) > ledger["weighted_minimum"]


def test_weighted_optimal_fixture_converges_to_strict_positive_limit():
    rows = [two_sideband_row(k) for k in (10, 18, 30, 46)]
    errors = [row["C_M_scaled_absolute_error"] for row in rows]
    assert errors[-1] < errors[0]
    assert errors[-1] < Decimal("0.08")
    assert rows[-1]["C_M_scaled_normalized_sum"] > 0


def test_superunit_constants_are_retained():
    constants = physical_constants()
    assert constants["lambda"] > 1
    assert constants["x"] > 1


def test_invalid_domains_fail_closed():
    constants = physical_constants()
    with pytest.raises(ValueError):
        physical_constants(40)
    with pytest.raises(ValueError):
        sideband_entry(8, 1)
    with pytest.raises(ValueError):
        sideband_entry(4, 3)
    with pytest.raises(ValueError):
        two_sideband_row(5)
    with pytest.raises(ValueError):
        relative_objective(Decimal(0), constants["lambda"])
    with pytest.raises(ValueError):
        weighted_objective(Decimal(1), constants["lambda"], Decimal(1))
