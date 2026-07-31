from fractions import Fraction

import pytest

from isolated_audit import (
    EXPANSION,
    HARDY_RADIUS,
    MODEL_CONTRAST,
    MULTIPLIER_CONSTANT,
    PARITY_CONSTANT,
    REFERENCE_CONTRAST,
    TARGET_RADIUS,
    alias_coefficient,
    alias_packet,
    alias_to_target,
    audit_row,
    beta_squared,
    boundary_packet,
    demand,
    duhamel_ledger,
    exchange_matrix,
    exchange_trace_power,
    far_remainder,
    frozen_certificates,
    isolated_interface,
    matrix_power,
    matrix_trace,
    noise_scale,
    observation_error,
    outward_decimal_interval,
    parity_gap,
    parity_packet,
    power_mismatch,
    reachability_screen_zero,
    required_power,
    residual,
    residual_to_target,
    shell_packet,
    target,
)


def test_frozen_exact_inequality_certificates():
    certificates = frozen_certificates()
    assert certificates["phase_ratio"] == PARITY_CONSTANT * MULTIPLIER_CONSTANT
    assert certificates["phase_ratio_strictly_between_zero_and_one"] is True
    assert certificates["phase_ratio_margin"] > 0
    assert certificates["growth_base"] == TARGET_RADIUS**2 * beta_squared()
    assert certificates["growth_base_greater_than_one"] is True
    assert certificates["growth_base_margin"] > 0


@pytest.mark.parametrize("contrast", [Fraction(0), Fraction(3, 5), Fraction(4, 5), Fraction(1)])
@pytest.mark.parametrize("order", [1, 2, 7, 16])
def test_exchange_block_trace_identity(contrast, order):
    matrix = exchange_matrix(contrast)
    assert matrix_trace(matrix_power(matrix, order)) == 1 + contrast**order
    assert exchange_trace_power(contrast, order) == 1 + contrast**order


def test_alias_and_parity_block_formulas_are_exact():
    for k in (1, 2, 4, 8):
        assert alias_packet(k) == alias_coefficient(k) * beta_squared() ** k
        assert parity_gap(k) == PARITY_CONSTANT * EXPANSION ** (-k)
        assert noise_scale(k) == EXPANSION ** (-2 * k)
        assert parity_packet(k) == HARDY_RADIUS ** (-2 * k) * (
            1 - (1 - parity_gap(k)) ** (2 * k)
        )


def test_boundary_observation_and_far_slots_are_exactly_zero():
    for k in (1, 4, 16):
        assert boundary_packet(k) == 0
        assert observation_error(k) == 0
        assert far_remainder(k) == 0


def test_shell_block_trace_realization():
    for k in (2, 5, 8):
        model_trace = matrix_trace(
            matrix_power(exchange_matrix(MODEL_CONTRAST), 2 * k)
        )
        reference_trace = matrix_trace(
            matrix_power(exchange_matrix(REFERENCE_CONTRAST), 2 * k)
        )
        assert shell_packet(k) == alias_packet(k) * (model_trace - reference_trace)


def test_exact_matching_ledger_and_fixed_contrast_mismatch():
    for k in (2, 4, 8, 16):
        assert demand(k) == alias_packet(k) - parity_packet(k)
        assert residual(k) == alias_packet(k) * power_mismatch(k)
        assert power_mismatch(k) == MODEL_CONTRAST ** (2 * k) - required_power(k)


def test_selected_audit_rows_are_reachable_but_fail_matching():
    for k in (2, 4, 8, 16, 24, 32):
        assert reachability_screen_zero(k)
        assert residual(k) < -target(k)
        row = audit_row(k)
        assert row["reachability_screen_zero_exact"] is True
        assert row["residual_negative_exact"] is True
        assert row["within_one_target_unit_exact"] is False


def test_k_one_is_outside_the_published_audit_domain():
    with pytest.raises(ValueError):
        audit_row(1)


def test_reachability_matches_the_exact_attainable_interval():
    for k in (2, 4, 8, 16):
        scale = alias_packet(k)
        reference_power = REFERENCE_CONTRAST ** (2 * k)
        attainable = (-scale * reference_power, scale * (1 - reference_power))
        value = demand(k)
        assert reachability_screen_zero(k) is (attainable[0] <= value <= attainable[1])


def test_model_residual_ratios_move_on_the_proved_side():
    assert alias_to_target(16) > alias_to_target(8) > 1
    assert residual_to_target(16) < residual_to_target(8) < -1


def test_all_duhamel_legs_are_retained_and_exactly_zero():
    for k in (2, 7, 16):
        ledger = duhamel_ledger(k)
        assert ledger["channel_count"] == 2
        assert ledger["legs_per_channel"] == 2 * k
        assert ledger["total_prefix_suffix_weight_count"] == 4 * k
        assert ledger["all_weights_equal"] is True
        assert ledger["all_leg_defects_exact"] == "0/1"
        assert ledger["duhamel_majorant_exact"] == "0/1"


def test_interface_keeps_model_and_actual_operator_separate():
    interface = isolated_interface()
    assert interface["isolated_model_joint_matching"] == "fails"
    assert interface["actual_noisy_operator_identified"] is False
    assert interface["full_trace_transfer_proved"] is False


def test_directed_decimal_intervals_enclose_all_signs():
    for value in (Fraction(-7, 3), Fraction(0), Fraction(11, 7)):
        lower, upper = outward_decimal_interval(value, digits=8)
        assert Fraction(lower) <= value <= Fraction(upper)


@pytest.mark.parametrize("bad", [0, -1, True, 1.5])
def test_positive_integer_validation(bad):
    with pytest.raises(ValueError):
        target(bad)


def test_contrast_validation():
    with pytest.raises(ValueError):
        exchange_matrix(Fraction(6, 5))
