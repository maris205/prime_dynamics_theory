import json
from fractions import Fraction
from pathlib import Path


RESULT = Path(__file__).parents[1] / "results" / "result.json"


def load_result():
    return json.loads(RESULT.read_text())


def test_result_positive_model_claims():
    data = load_result()
    for key in (
        "frozen_isolated_model_from_exact_rational_data",
        "graded_family_not_one_all_order_operator",
        "exact_exchange_block_trace_law_proved",
        "exact_alias_block_identity_proved",
        "exact_parity_block_identity_proved",
        "exact_boundary_block_identity_proved",
        "exact_shell_block_identity_proved",
        "model_boundary_packet_exact_zero",
        "model_observation_error_exact_zero",
        "model_far_remainder_exact_zero",
        "model_all_prefix_suffix_duhamel_weights_retained",
        "model_all_duhamel_leg_defects_exact_zero",
        "model_duhamel_majorant_exact_zero",
        "parity_to_alias_limit_proved",
        "required_power_interior_limit_proved",
        "eventual_zero_reachability_screen_proved",
        "fixed_model_contrast_matching_failure_proved",
        "residual_to_alias_negative_limit_proved",
        "alias_to_target_divergence_proved_in_model",
        "residual_to_target_negative_divergence_proved_in_model",
        "required_contrast_radius_tends_to_one_proved",
        "model_exponential_precision_barrier_violated",
        "scoped_isolated_model_negative_result_proved",
        "all_reported_rows_reachable_exact",
        "all_reported_rows_fail_target_window_exact",
    ):
        assert data[key] is True


def test_result_firewall_claims_are_false():
    data = load_result()
    for key in (
        "actual_noisy_operator_identified",
        "actual_physical_shell_representation_proved",
        "actual_shell_scale_or_contrast_theorem_proved",
        "actual_trace_observation_duhamel_bound_proved",
        "actual_far_remainder_little_o_proved",
        "actual_joint_alias_parity_shell_matching_little_o_proved",
        "joint_first_alias_full_trace_law_proved",
        "full_trace_replacement_proved",
        "actual_full_trace_divergence_proved",
        "single_all_order_operator_constructed",
        "finite_rows_promoted_to_physical_asymptotics",
        "archived_decimal_constants_interval_certified",
        "hilbert_polya_constructed",
        "riemann_zeros_identified",
        "von_mangoldt_trace_proved",
        "zeta_divisor_equality",
        "riemann_hypothesis_proved",
    ):
        assert data[key] is False
    assert not any(data["gates"].values())


def test_exact_certificates_round_trip_and_have_correct_signs():
    data = load_result()
    certificates = data["exact_certificates"]
    ratio = Fraction(certificates["phase_ratio"]["exact"])
    ratio_margin = Fraction(certificates["phase_ratio_margin"]["exact"])
    growth = Fraction(certificates["growth_base"]["exact"])
    growth_margin = Fraction(certificates["growth_base_margin"]["exact"])
    assert 0 < ratio < 1
    assert ratio + ratio_margin == 1
    assert growth > 1
    assert growth - growth_margin == 1


def test_row_ledger_counts_and_exact_verdicts():
    data = load_result()
    assert data["row_orders"] == [2, 4, 8, 16, 24, 32]
    assert data["row_count"] == 6
    assert data["total_retained_duhamel_weight_count"] == 344
    for row in data["rows"]:
        assert row["reachability_screen_zero_exact"] is True
        assert row["residual_negative_exact"] is True
        assert row["within_one_target_unit_exact"] is False
        assert row["boundary_packet_exact"] == "0/1"
        assert row["observation_error_exact"] == "0/1"
        assert row["far_remainder_exact"] == "0/1"
        assert row["shell_scale_identity"] == "L_k=A_k"
        assert row["observation_duhamel_majorant_to_target_exact"] == "0/1"
        assert row["far_remainder_bound_to_target_exact"] == "0/1"
        assert row["duhamel"]["total_prefix_suffix_weight_count"] == 4 * row["k"]
        assert row["duhamel"]["all_leg_defects_exact"] == "0/1"
        assert row["duhamel"]["duhamel_majorant_exact"] == "0/1"


def test_rh330_interface_is_explicitly_scoped():
    interface = load_result()["rh330_interface"]
    assert interface["model_type"] == "graded_finite_dimensional_isolated_trace_model"
    assert interface["isolated_model_joint_matching"] == "fails"
    assert interface["actual_noisy_operator_identified"] is False
    assert interface["full_trace_transfer_proved"] is False
