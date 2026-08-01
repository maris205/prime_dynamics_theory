import json
import math
from pathlib import Path

from repelling_return import total_transported_linear_coefficient


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results/result.json").read_text(encoding="utf-8"))


def test_result_structure_and_deterministic_counts():
    data = _result()
    assert len(data["row_cases"]) == 3
    assert len(data["transported_sector_coefficients"]) == 3
    assert len(data["curvature_proxy_rows"]) == 12
    assert len(data["global_uniformity_obstruction_rows"]) == 3
    for row in data["transported_sector_coefficients"]:
        assert math.isclose(
            row["exact_total_linear_coefficient"],
            total_transported_linear_coefficient(row["phase_d"]),
            rel_tol=1e-14,
        )
        assert math.isclose(
            row["sector_coefficient_sum"],
            row["exact_total_linear_coefficient"],
            rel_tol=3e-9,
            abs_tol=3e-9,
        )


def test_result_positive_claims_are_typed_to_second_hybrid_term():
    data = _result()
    assert data["exact_scaled_physical_second_row_formula_proved"] is True
    assert data["exact_physical_to_curved_l1_identity_proved"] is True
    assert data["exact_curved_to_tangent_l1_identity_proved"] is True
    assert data["sharp_fixed_row_linear_coefficient_proved"] is True
    assert data["actual_first_leg_prefix_uniform_fourth_moment_proved"] is True
    assert data["actual_first_leg_prefix_sector_second_moment_convergence_proved"] is True
    assert data["sharp_second_hybrid_sector_coefficients_proved"] is True
    assert data["both_repelling_orientation_coefficients_strictly_positive"] is True
    assert data["physical_first_leg_prefix_used_in_both_hybrids"] is True
    assert data["retained_u_hybrid_l1_isometry_used"] is True
    assert data["exponentially_small_second_hybrid_accuracy_disproved"] is True
    assert data["little_o_sigma_second_hybrid_accuracy_disproved"] is True
    assert data["global_uniform_row_O_sigma_disproved"] is True
    assert "second_hybrid_duhamel_row_term" in data["data_type"]


def test_result_scope_firewall_and_gates():
    data = _result()
    false_fields = (
        "exponentially_small_second_hybrid_accuracy_proved",
        "little_o_sigma_second_hybrid_accuracy_proved",
        "global_uniform_row_O_sigma_proved",
        "row_coefficient_at_u_zero_positive",
        "fully_physical_vs_fully_affine_two_leg_equality_proved",
        "w_marginal_equality_proved",
        "all_cycle_O_k_sigma_transport_proved",
        "cyclic_trace_control_proved",
        "parity_shell_cancellation_proved",
        "full_trace_replacement_proved",
        "determinant_gluing_activated",
        "hilbert_polya_constructed",
        "riemann_zeros_identified",
        "von_mangoldt_trace_proved",
        "zeta_divisor_equality",
        "riemann_hypothesis_proved",
    )
    assert all(data[field] is False for field in false_fields)
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())
