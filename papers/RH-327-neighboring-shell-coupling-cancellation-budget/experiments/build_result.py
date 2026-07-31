"""Build the deterministic RH-327 result ledger."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shell_coupling import (  # noqa: E402
    HARDY_RADIUS,
    TRACE_RADIUS,
    contrast_row,
    first_alias_target,
    fixed_budget_row,
    free_pair_distance,
    localized_raw_packets,
    raw_packet_from_totals,
    realize_free_pair_fraction,
    rh328_interface,
    scaled_edge_gap,
)


def main() -> None:
    contrast_rows = [contrast_row(value, 8) for value in (-0.9, -0.5, 0.0, 0.5, 0.9)]
    fixed_rows = [
        fixed_budget_row(value, 0.8, 8)
        for value in (-0.25, -0.1, 0.0, 0.5, 0.9)
    ]
    free_rows = []
    for fraction in (-1.0, -0.5, 0.0, 0.5, 1.0):
        contrast, reference = realize_free_pair_fraction(fraction, 16)
        free_rows.append(
            {
                "demand_fraction": fraction,
                "order": 16,
                "noisy_contrast": contrast,
                "reference_contrast": reference,
                "absolute_residual_fraction": free_pair_distance(fraction),
            }
        )
    edge_rows = [
        {
            "fraction": 0.25,
            "k": k,
            "minimum_contrast_radius": 0.25 ** (1.0 / (2 * k)),
            "scaled_edge_gap": scaled_edge_gap(0.25, k),
            "limit": -math.log(0.25),
        }
        for k in (4, 8, 16, 32, 64)
    ]

    noisy = (1.5, 0.75, 0.25)
    deterministic = (1.1, 0.4, 0.2)
    order = 8
    packets = localized_raw_packets(noisy, deterministic, order)
    direct_total = HARDY_RADIUS ** (-order) * (
        sum(noisy) - sum(deterministic)
    )
    partition_check = {
        "order": order,
        "noisy_localized_traces": list(noisy),
        "deterministic_localized_flat_traces": list(deterministic),
        "boundary_packet": packets[0],
        "neighboring_shell_packet": packets[1],
        "far_remainder_packet": packets[2],
        "sum_of_packets": raw_packet_from_totals(noisy, deterministic, order),
        "direct_total_packet": direct_total,
        "identity_error": sum(packets) - direct_total,
        "status": "exact_finite_bookkeeping_example_not_physical_data",
    }

    data = {
        "status": "rh327_neighboring_shell_coupling_cancellation_budget",
        "exact_basepoint_localized_trace_partition_proved": True,
        "actual_raw_trace_packet_decomposition_proved": True,
        "actual_neighboring_shell_trace_slot_defined": True,
        "exact_signed_boundary_shell_remainder_identity_proved": True,
        "both_critical_sibling_slots_retained": True,
        "scoped_exchange_channel_model_proved": True,
        "branch_blind_all_power_nonidentifiability_proved": True,
        "fixed_reference_defect_interval_proved": True,
        "fixed_reference_sharp_residual_formula_proved": True,
        "free_pair_information_class_budget_proved": True,
        "same_order_unit_contrast_necessity_proved": True,
        "clearance_phase_retained_in_interface": True,
        "retained_coordinate_frame_recorded": True,
        "rh325_operator_duhamel_weight_schema_retained": True,
        "rh328_joint_matching_interface_typed": True,
        "one_sibling_tail_negligibility_proved": False,
        "localized_shell_magnitude_or_sign_controlled": False,
        "local_affine_probability_packet_identified_with_localized_trace": False,
        "physical_exchange_completion_identified": False,
        "physical_exchange_contrast_identified": False,
        "physical_fixed_contrast_mismatch_little_o_proved": False,
        "actual_shell_scale_identified": False,
        "certified_trace_remainder_little_o_proved": False,
        "separate_boundary_shell_majorant_closes_matching": False,
        "finite_shell_diagnostics_promoted_to_asymptotic_theorem": False,
        "archived_decimal_constants_interval_certified": False,
        "second_physical_critical_leg_controlled": False,
        "all_physical_legs_have_uniform_order_sigma_remainders": False,
        "actual_full_cycle_duhamel_bound_proved": False,
        "weighted_trace_observation_norm_controlled": False,
        "joint_alias_parity_shell_matching_equation_proved": False,
        "parity_weighting_combined_into_full_trace": False,
        "joint_first_alias_trace_law_proved": False,
        "full_trace_replacement_proved": False,
        "actual_full_trace_divergence_proved": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
        "constants": {
            "hardy_radius": HARDY_RADIUS,
            "target_radius": TRACE_RADIUS,
            "fixed_reference_contrast_diagnostic": 0.8,
            "fixed_reference_order_diagnostic": 8,
            "diagnostic_status": "exact_formula_evaluations_not_physical_shell_data",
        },
        "target_rows": [
            {"k": k, "order": 2 * k, "target_scale": first_alias_target(k)}
            for k in (4, 8, 16, 32)
        ],
        "contrast_rows": contrast_rows,
        "fixed_reference_budget_rows": fixed_rows,
        "free_pair_budget_rows": free_rows,
        "edge_rows": edge_rows,
        "localized_partition_check": partition_check,
        "rh328_interface": rh328_interface(),
        "gates": {
            "A_canonical_intrinsic_dynamical_spectral_determinant": False,
            "B_time_oriented_scattering_or_unitary_completion": False,
            "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
            "D_von_mangoldt_weighted_prime_power_traces": False,
            "E_completed_zeta_divisor_equality": False,
        },
    }
    output = ROOT / "results" / "result.json"
    output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "contrast_rows": len(contrast_rows),
                "fixed_reference_rows": len(fixed_rows),
                "free_pair_rows": len(free_rows),
                "edge_rows": len(edge_rows),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
