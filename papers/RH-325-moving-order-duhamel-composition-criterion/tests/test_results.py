import json
from pathlib import Path


def test_result_firewall_and_criterion_ledger():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["retained_coordinate_markov_duhamel_criterion_proved"] is True
    assert data["endpoint_marginal_contraction_proved"] is True
    assert data["phase_transport_same_seed_obstruction_proved"] is True
    assert data["operator_trace_observation_duhamel_criterion_proved"] is True
    assert data["dimension_free_markov_to_trace_bound_proved"] is False
    assert data["growing_state_trace_counterexample_proved"] is True
    assert data["sharp_stability_growth_threshold_proved"] is True
    assert data["all_physical_legs_have_uniform_order_sigma_remainders"] is False
    assert data["second_physical_critical_leg_controlled"] is False
    assert data["actual_full_cycle_duhamel_bound_proved"] is False
    assert data["weighted_trace_observation_norm_controlled"] is False
    assert data["parity_weighting_combined"] is False
    assert data["neighboring_shell_combined"] is False
    assert data["joint_first_alias_trace_law_proved"] is False
    assert data["full_trace_replacement_proved"] is False
    assert data["hilbert_polya_constructed"] is False
    assert data["riemann_zeros_identified"] is False
    assert data["von_mangoldt_trace_proved"] is False
    assert data["zeta_divisor_equality"] is False
    assert data["riemann_hypothesis_proved"] is False
    assert len(data["clock_rows"]) == 5
    assert len(data["stability_rows"]) == 4
    assert len(data["trace_counterexamples"]) == 4
    assert not any(data["gates"].values())
