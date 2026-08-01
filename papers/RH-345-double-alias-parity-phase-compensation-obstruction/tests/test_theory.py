from decimal import Decimal, localcontext

import pytest

from double_alias_phase import balance_phase, completion_row, physical_constants


def test_balance_phase_solves_the_diagnostic_double_alias_equation():
    row = completion_row(8)
    assert abs(row["phase_ratio"] - 2) < Decimal("1e-90")


def test_positive_demand_approaches_twice_the_alias():
    rows = [completion_row(k) for k in (8, 16, 24, 32)]
    errors = [abs(row["demand_over_alias"] - 2) for row in rows]
    assert errors[-1] < errors[0]


def test_desired_parity_packets_lie_in_the_exact_scalar_domain():
    for k in (8, 16, 24, 32):
        row = completion_row(k)
        assert 0 < row["scaled_close_packet"] < 1
        assert 0 < row["scaled_far_packet"] < 1


def test_inverse_parity_map_recovers_both_packets():
    for k in (8, 16, 24, 32):
        row = completion_row(k)
        assert row["close_recovery_error"] < Decimal("1e-90")
        assert row["far_recovery_error"] < Decimal("1e-90")


def test_both_scalar_sequences_share_the_square_root_law():
    rows = [completion_row(k) for k in (8, 16, 24, 32)]
    close_errors = [abs(row["close_delta_ratio"] - 1) for row in rows]
    far_errors = [abs(row["far_delta_ratio"] - 1) for row in rows]
    assert close_errors[-1] < close_errors[0]
    assert far_errors[-1] < far_errors[0]
    assert close_errors[-1] < Decimal("0.05")
    assert far_errors[-1] < Decimal("0.05")


def test_close_and_far_scalar_ledgers_have_opposite_target_behavior():
    rows = [completion_row(k) for k in (8, 16, 24, 32)]
    assert all(row["close_direct_residual"] == 0 for row in rows)
    with localcontext() as context:
        context.prec = 100
        assert all(
            abs(row["far_direct_residual"] - row["alias"] / row["k"])
            < Decimal("1e-90")
            for row in rows
        )
    assert rows[-1]["far_weighted_critical"] > rows[0]["far_weighted_critical"]
    assert rows[-1]["far_weighted_critical"] > Decimal(10000)


def test_physical_constants_keep_beta_R_superunit():
    constants = physical_constants()
    assert constants["lambda"] > 1
    assert constants["beta"] * Decimal("1.4") > 1
    assert balance_phase() > 0


def test_invalid_domains_fail_closed():
    with pytest.raises(ValueError):
        physical_constants(40)
    with pytest.raises(ValueError):
        completion_row(1)
