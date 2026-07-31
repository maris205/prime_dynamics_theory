import json
from pathlib import Path


def test_result_ledger_and_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    for key in (
        "actual_localized_trace_slots_retained",
        "exact_typed_joint_matching_equation_proved",
        "conditional_fixed_reference_shell_ledger_proved",
        "fixed_reference_required_power_formula_proved",
        "fixed_reference_reachability_distance_identity_proved",
        "phase_normalized_required_power_law_proved",
        "fixed_phase_clearance_dictionary_retained",
        "unit_edge_target_contrast_law_proved",
        "exponential_contrast_radius_precision_law_proved",
        "sharp_symmetric_uncertainty_interval_proved",
        "rh325_duhamel_majorant_inserted_into_joint_certificate",
        "reachability_zero_false_positive_counterexample_proved",
        "conditional_joint_alias_parity_shell_matching_equation_proved",
    ):
        assert data[key] is True
    for key in (
        "actual_physical_shell_representation_proved",
        "actual_shell_scale_identified",
        "physical_exchange_contrast_identified",
        "physical_fixed_reference_contrast_identified",
        "weighted_trace_observation_norm_controlled",
        "all_prefix_suffix_duhamel_weights_controlled",
        "actual_full_cycle_duhamel_bound_proved",
        "certified_trace_remainder_little_o_proved",
        "actual_fixed_contrast_power_mismatch_little_o_proved",
        "actual_contrast_radius_precision_proved",
        "even_order_contrast_sign_identified",
        "archived_decimal_constants_interval_certified",
        "finite_formula_diagnostics_promoted_to_physical_asymptotics",
        "actual_joint_alias_parity_shell_matching_little_o_proved",
        "joint_first_alias_trace_law_proved",
        "full_trace_replacement_proved",
        "actual_full_trace_divergence_proved",
        "parity_weighting_combined_into_full_trace",
        "hilbert_polya_constructed",
        "riemann_zeros_identified",
        "von_mangoldt_trace_proved",
        "zeta_divisor_equality",
        "riemann_hypothesis_proved",
    ):
        assert data[key] is False
    assert len(data["phase_rows"]) == 5
    assert len(data["precision_rows"]) == 4
    assert len(data["false_positive_rows"]) == 4
    assert len(data["uncertainty_rows"]) == 5
    assert abs(data["identity_check"]["identity_error"]) < 1e-14
    assert not any(data["gates"].values())


def test_result_interfaces_are_explicitly_conditional():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    interface = data["rh329_interface"]
    assert interface["conditional_shell_representation"].startswith("S=L*")
    assert interface["physical_trace_observation_identified"] is False
    assert interface["physical_shell_scale_identified"] is False
    assert interface["physical_contrast_identified"] is False
    assert interface["far_remainder_little_o_proved"] is False
