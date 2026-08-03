from decimal import Decimal

import pytest

from lower_sideband_balance import (
    balance_phase,
    completion_row,
    physical_constants,
)


def test_balance_phase_solves_shifted_lower_equation():
    row = completion_row(8)
    assert abs(row["phase_ratio"] - 1) < Decimal("1e-90")


def test_same_clock_retains_k_equal_m_plus_one_and_order_2m():
    for m in (8, 16, 24, 40):
        row = completion_row(m)
        assert row["k"] == m + 1
        assert row["sideband_order"] == 2 * m
        assert row["root_exponent_denominator"] == 2 * m


def test_combined_demand_approaches_the_complete_orbit_atom():
    rows = [completion_row(m) for m in (8, 16, 24, 40)]
    errors = [abs(row["demand_over_full"] - 1) for row in rows]
    assert errors[-1] < errors[0]


def test_desired_packets_lie_in_exact_order_2m_inverse_domain():
    for m in (8, 16, 24, 40):
        row = completion_row(m)
        assert 0 < row["scaled_close_packet"] < 1
        assert 0 < row["scaled_far_packet"] < 1


def test_inverse_parity_map_recovers_both_packets():
    for m in (8, 16, 24, 40):
        row = completion_row(m)
        assert row["close_recovery_error"] < Decimal("1e-90")
        assert row["far_recovery_error"] < Decimal("1e-90")


def test_both_scalar_sequences_share_the_square_root_law():
    rows = [completion_row(m) for m in (8, 16, 24, 40)]
    close_errors = [abs(row["close_delta_ratio"] - 1) for row in rows]
    far_errors = [abs(row["far_delta_ratio"] - 1) for row in rows]
    assert close_errors[-1] < close_errors[0]
    assert far_errors[-1] < far_errors[0]
    assert close_errors[-1] < Decimal("0.05")
    assert far_errors[-1] < Decimal("0.05")


def test_close_and_far_ledgers_have_opposite_target_behavior():
    rows = [completion_row(m) for m in (8, 16, 24, 40)]
    assert all(row["close_direct_residual"] == 0 for row in rows)
    assert all(
        abs(row["far_direct_residual"] - row["two_point_weights"])
        < Decimal("1e-90")
        for row in rows
    )
    assert rows[-1]["far_weighted_lower"] > rows[0]["far_weighted_lower"]
    assert rows[-1]["far_weighted_lower"] > Decimal(10000)


def test_far_weighted_term_is_exactly_point_weight_over_target():
    for m in (8, 16, 24, 40):
        row = completion_row(m)
        assert row["far_weighted_identity_error"] < Decimal("1e-90")


def test_physical_constants_keep_beta_R_superunit():
    constants = physical_constants()
    assert constants["lambda"] > 1
    assert constants["beta"] * Decimal("1.4") > 1
    assert balance_phase() > 1


def test_invalid_domains_fail_closed():
    with pytest.raises(ValueError):
        physical_constants(40)
    with pytest.raises(ValueError):
        completion_row(1)
