import json
from pathlib import Path


def test_result_firewall_and_quantitative_record():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["oriented_two_leg_affine_chain_proved"] is True
    assert data["exact_joint_tv_transfer_proved"] is True
    assert data["source_coordinate_retained_in_isometry"] is True
    assert data["marginal_l1_contraction_proved"] is True
    assert data["marginal_l1_isometry_proved"] is False
    assert data["intermediate_extended_skew_normal_proved"] is True
    assert data["final_extended_skew_normal_proved"] is True
    assert data["conditioning_bias_moments_proved"] is True
    assert data["non_gaussian_output_proved"] is True
    assert data["actual_two_leg_curvature_remainder_proved"] is False
    assert data["parity_weighting_combined"] is False
    assert data["neighboring_shell_combined"] is False
    assert data["moving_order_remainder_proved"] is False
    assert data["joint_first_alias_trace_law_proved"] is False
    assert data["full_trace_replacement_proved"] is False
    assert data["hilbert_polya_constructed"] is False
    assert data["riemann_zeros_identified"] is False
    assert data["von_mangoldt_trace_proved"] is False
    assert data["zeta_divisor_equality"] is False
    assert data["riemann_hypothesis_proved"] is False
    assert "kappa_aff" in data["constants"]
    assert "kappa" not in data["constants"]
    assert data["constants"]["kappa_aff"] > 5.0
    assert len(data["phase_profiles"]) == 4
    assert len(data["finite_cases"]) == 3
    assert not any(data["gates"].values())
