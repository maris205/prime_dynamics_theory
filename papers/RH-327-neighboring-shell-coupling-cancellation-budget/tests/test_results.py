import json
from pathlib import Path


def test_result_ledger_and_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    for key in (
        "exact_basepoint_localized_trace_partition_proved",
        "actual_raw_trace_packet_decomposition_proved",
        "actual_neighboring_shell_trace_slot_defined",
        "exact_signed_boundary_shell_remainder_identity_proved",
        "both_critical_sibling_slots_retained",
        "scoped_exchange_channel_model_proved",
        "branch_blind_all_power_nonidentifiability_proved",
        "fixed_reference_defect_interval_proved",
        "fixed_reference_sharp_residual_formula_proved",
        "free_pair_information_class_budget_proved",
        "same_order_unit_contrast_necessity_proved",
        "clearance_phase_retained_in_interface",
        "retained_coordinate_frame_recorded",
        "rh325_operator_duhamel_weight_schema_retained",
        "rh328_joint_matching_interface_typed",
    ):
        assert data[key] is True
    for key in (
        "one_sibling_tail_negligibility_proved",
        "localized_shell_magnitude_or_sign_controlled",
        "local_affine_probability_packet_identified_with_localized_trace",
        "physical_exchange_completion_identified",
        "physical_exchange_contrast_identified",
        "physical_fixed_contrast_mismatch_little_o_proved",
        "actual_shell_scale_identified",
        "certified_trace_remainder_little_o_proved",
        "separate_boundary_shell_majorant_closes_matching",
        "finite_shell_diagnostics_promoted_to_asymptotic_theorem",
        "archived_decimal_constants_interval_certified",
        "second_physical_critical_leg_controlled",
        "all_physical_legs_have_uniform_order_sigma_remainders",
        "actual_full_cycle_duhamel_bound_proved",
        "weighted_trace_observation_norm_controlled",
        "joint_alias_parity_shell_matching_equation_proved",
        "parity_weighting_combined_into_full_trace",
        "joint_first_alias_trace_law_proved",
        "full_trace_replacement_proved",
        "actual_full_trace_divergence_proved",
        "hilbert_polya_constructed",
        "riemann_zeros_identified",
        "von_mangoldt_trace_proved",
        "zeta_divisor_equality",
        "riemann_hypothesis_proved",
    ):
        assert data[key] is False
    assert len(data["contrast_rows"]) == 5
    assert len(data["fixed_reference_budget_rows"]) == 5
    assert len(data["free_pair_budget_rows"]) == 5
    assert len(data["edge_rows"]) == 5
    assert len(data["target_rows"]) == 4
    assert not any(data["gates"].values())
