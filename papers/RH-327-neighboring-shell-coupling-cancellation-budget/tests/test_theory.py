import math

import pytest

from shell_coupling import (
    HARDY_RADIUS,
    best_fixed_reference_shell,
    exchange_matrix,
    exchange_power,
    exchange_shell_defect,
    first_alias_residual,
    first_alias_target,
    fixed_reference_interval,
    free_pair_distance,
    free_pair_interval,
    localized_branch_trace,
    localized_raw_packets,
    minimum_pair_contrast_radius,
    raw_packet_from_totals,
    realize_fixed_reference_shell,
    realize_free_pair_fraction,
    required_shell_demand,
    reset_completion_trace,
    rh328_interface,
    scaled_edge_gap,
    symmetric_compression,
    trace_power,
)


def multiply(left, right):
    return tuple(
        tuple(sum(left[i][h] * right[h][j] for h in range(2)) for j in range(2))
        for i in range(2)
    )


def test_exchange_matrix_is_symmetric_markov_and_has_expected_channels():
    for contrast in (-1.0, -0.4, 0.0, 0.7, 1.0):
        matrix = exchange_matrix(contrast)
        assert matrix[0][1] == matrix[1][0]
        assert all(entry >= 0.0 for row in matrix for entry in row)
        assert all(math.isclose(sum(row), 1.0) for row in matrix)
        assert math.isclose(matrix[0][0] - matrix[0][1], contrast)


def test_exchange_power_formula_matches_direct_multiplication():
    contrast = -0.63
    direct = exchange_matrix(contrast)
    for order in range(2, 10):
        direct = multiply(direct, exchange_matrix(contrast))
        closed = exchange_power(contrast, order)
        for direct_row, closed_row in zip(direct, closed):
            for direct_value, closed_value in zip(direct_row, closed_row):
                assert math.isclose(direct_value, closed_value, abs_tol=2e-15)


def test_branch_blind_compression_is_constant_while_trace_varies():
    values = []
    for contrast in (-0.9, -0.2, 0.0, 0.5, 0.95):
        assert symmetric_compression(contrast, 8) == 1.0
        assert reset_completion_trace(contrast, 8) == trace_power(contrast, 8)
        values.append(trace_power(contrast, 8))
    assert len(set(values)) == len(values)


def test_two_localized_branch_traces_are_equal_and_sum_to_total():
    for contrast in (-0.8, 0.0, 0.7):
        left = localized_branch_trace(contrast, 10)
        right = localized_branch_trace(contrast, 10)
        assert left == right
        assert math.isclose(left + right, trace_power(contrast, 10))


def test_fixed_reference_interval_and_realization_are_sharp():
    reference = 0.8
    order = 8
    lower, upper = fixed_reference_interval(reference, order, scale=3.0)
    assert math.isclose(lower, -3.0 * reference**order)
    assert math.isclose(upper, 3.0 * (1.0 - reference**order))
    for demand in (lower, -0.1, 0.0, 1.0, upper):
        contrast = realize_fixed_reference_shell(
            demand, reference, order, scale=3.0
        )
        realized = exchange_shell_defect(
            contrast, reference, order, scale=3.0
        )
        assert math.isclose(realized, demand, abs_tol=2e-14)
    with pytest.raises(ValueError, match="outside"):
        realize_fixed_reference_shell(lower - 0.1, reference, order, scale=3.0)


def test_fixed_reference_best_residual_is_interval_distance():
    lower, upper = fixed_reference_interval(0.75, 12)
    for demand in (lower - 0.3, lower, 0.0, upper, upper + 0.4):
        row = best_fixed_reference_shell(demand, 0.75, 12)
        expected = max(lower - demand, demand - upper, 0.0)
        assert math.isclose(row["absolute_residual"], expected)
        assert row["reachable"] is (expected == 0.0)


def test_free_pair_budget_and_minimum_radius_are_exact():
    assert free_pair_interval(scale=2.5) == (-2.5, 2.5)
    assert free_pair_distance(3.0, scale=2.5) == 0.5
    assert free_pair_distance(-1.0, scale=2.5) == 0.0
    for fraction in (-1.0, -0.4, 0.0, 0.3, 1.0):
        contrast, reference = realize_free_pair_fraction(fraction, 20)
        realized = exchange_shell_defect(contrast, reference, 20)
        assert math.isclose(realized, fraction, abs_tol=2e-15)
        assert math.isclose(
            max(abs(contrast), abs(reference)),
            minimum_pair_contrast_radius(fraction, 20),
        )


def test_same_order_fraction_forces_a_near_unit_contrast():
    fraction = 0.25
    rows = [scaled_edge_gap(fraction, k) for k in (8, 16, 32, 64, 128)]
    limit = -math.log(fraction)
    assert all(value < limit for value in rows)
    assert all(left < right for left, right in zip(rows, rows[1:]))
    assert abs(rows[-1] - limit) < 0.004


def test_actual_localized_raw_trace_partition_bookkeeping_is_exact():
    noisy = (1.5, 0.75, 0.25)
    deterministic = (1.1, 0.4, 0.2)
    packets = localized_raw_packets(noisy, deterministic, 8)
    direct = HARDY_RADIUS ** (-8) * (sum(noisy) - sum(deterministic))
    assert math.isclose(sum(packets), direct)
    assert math.isclose(
        raw_packet_from_totals(noisy, deterministic, 8), direct
    )
    with pytest.raises(ValueError, match="three"):
        localized_raw_packets((1.0, 2.0), (0.5, 0.5), 8)


def test_rh326_signed_ledger_and_rh328_interface_are_preserved():
    alias = 9.0
    parity = 2.0
    boundary = 1.5
    shell = required_shell_demand(alias, parity, boundary)
    assert shell == 5.5
    assert first_alias_residual(boundary, shell, 0.0, parity, alias) == 0.0
    assert first_alias_target(5) == 5 * 1.4 ** (-10)
    interface = rh328_interface()
    assert interface["raw_packet_identity"] == "T=B+S+R"
    assert interface["joint_residual_identity"] == "e=B+S+R+P-A"
    assert interface["retained_coordinates"] == ["V", "U", "W"]
    assert interface["coordinate_orientation"] == [
        "positive",
        "negative",
        "positive",
    ]
    assert interface["actual_localized_trace_slots"] == "defined_exactly"
    assert interface["physical_fixed_contrast_mismatch"] == "open"
    assert interface["little_o_remainder"] == "open"


def test_domain_validation_rejects_illegal_exchange_inputs():
    with pytest.raises(ValueError, match=r"\[-1, 1\]"):
        exchange_matrix(1.01)
    with pytest.raises(ValueError, match="even order"):
        fixed_reference_interval(0.5, 7)
    with pytest.raises(ValueError, match="positive"):
        first_alias_target(0)
