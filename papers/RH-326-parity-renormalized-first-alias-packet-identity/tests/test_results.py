import json
from pathlib import Path


def test_result_identity_ledger_and_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    for key in (
        "exact_hardy_parity_decomposition_proved",
        "exact_counterloop_defect_decomposition_proved",
        "exact_counterloop_first_alias_moment_identity_proved",
        "uniform_scalar_parity_packet_expansion_proved",
        "even_first_alias_parity_correction_positive_proved",
        "parity_renormalized_first_alias_packet_identity_proved",
        "alias_parity_common_weighted_exponent_proved",
        "scalar_balance_phase_law_proved",
        "canonical_integer_phase_scalar_only_obstruction_proved",
        "clearance_phase_retained_in_packet",
        "retained_coordinate_frame_recorded",
        "rh327_shell_interface_typed",
    ):
        assert data[key] is True
    for key in (
        "separate_alias_parity_majorant_closes_bridge",
        "scalar_parity_alone_closes_first_alias_matching",
        "local_boundary_probability_packet_identified_with_trace",
        "second_physical_critical_leg_controlled",
        "all_physical_legs_have_uniform_order_sigma_remainders",
        "actual_full_cycle_duhamel_bound_proved",
        "weighted_trace_observation_norm_controlled",
        "neighboring_shell_included",
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
    assert len(data["packet_rows"]) == 4
    assert len(data["phase_rows"]) == 6
    assert len(data["sign_rows"]) == 5
    assert not any(data["gates"].values())
