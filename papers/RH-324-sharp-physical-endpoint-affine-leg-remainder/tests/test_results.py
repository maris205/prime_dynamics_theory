import json
from pathlib import Path


def test_result_firewall_and_remainder_ledger():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["exact_physical_first_leg_kernel_formula_proved"] is True
    assert data["exact_curved_gaussian_boundary_l1_identity_proved"] is True
    assert data["uniform_fold_normalization_tail_proved"] is True
    assert data["finite_seed_physical_to_affine_joint_bound_proved"] is True
    assert data["sharp_linear_curvature_coefficient_proved"] is True
    assert data["first_alias_scale_compatibility_proved"] is True
    assert data["exponentially_small_affine_remainder_proved"] is False
    assert data["second_leg_physical_remainder_proved"] is False
    assert data["actual_two_leg_curvature_remainder_proved"] is False
    assert data["moving_order_duhamel_composition_proved"] is False
    assert data["parity_weighting_combined"] is False
    assert data["neighboring_shell_combined"] is False
    assert data["joint_first_alias_trace_law_proved"] is False
    assert data["full_trace_replacement_proved"] is False
    assert data["hilbert_polya_constructed"] is False
    assert data["riemann_zeros_identified"] is False
    assert data["von_mangoldt_trace_proved"] is False
    assert data["zeta_divisor_equality"] is False
    assert data["riemann_hypothesis_proved"] is False
    assert len(data["row_cases"]) == 3
    assert len(data["phase_coefficients"]) == 4
    assert len(data["finite_cases"]) == 3
    assert len(data["curvature_proxy_rows"]) == 6
    assert not any(data["gates"].values())
