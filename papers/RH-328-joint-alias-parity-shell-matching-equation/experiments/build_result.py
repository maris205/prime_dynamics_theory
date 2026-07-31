"""Build the deterministic RH-328 result ledger."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from joint_matching import (  # noqa: E402
    ALPHA,
    BETA,
    CLEARANCE_CONSTANT,
    HARDY_RADIUS,
    KAPPA_AFF,
    LAMBDA,
    MULTIPLIER_CONSTANT,
    PARITY_CONSTANT,
    TARGET_RADIUS,
    U_C,
    fixed_reference_reachability,
    hardy_target,
    joint_matching_decomposition,
    leading_alias_model,
    leading_clearance_ratio,
    leading_parity_ratio,
    normalized_required_power,
    reachability_false_positive,
    target_contrast_radius,
    typed_interface,
    uncertainty_interval,
)


def main() -> None:
    phase_rows = []
    phase_k = 16
    boundary_ratio = 0.2
    shell_ratio = 1.0
    reference_contrast = 0.8
    reference_power = reference_contrast ** (2 * phase_k)
    for phase in (-1.0, -0.5, 0.0, 0.5, 1.0):
        parity_ratio = leading_parity_ratio(phase)
        required_power = normalized_required_power(
            parity_to_alias=parity_ratio,
            boundary_to_alias=boundary_ratio,
            shell_to_alias=shell_ratio,
            reference_power=reference_power,
        )
        phase_rows.append(
            {
                "phase": phase,
                "clearance_ratio": leading_clearance_ratio(phase),
                "leading_parity_to_alias_ratio": parity_ratio,
                "boundary_to_alias_diagnostic": boundary_ratio,
                "shell_to_alias_diagnostic": shell_ratio,
                "reference_power": reference_power,
                "required_power": required_power,
                "reachable": 0.0 <= required_power <= 1.0,
                "target_contrast_radius": target_contrast_radius(
                    phase_k, required_power
                ),
                "scaled_unit_edge_gap": 2.0
                * phase_k
                * (
                    1.0
                    - target_contrast_radius(phase_k, required_power)
                ),
                "status": "formula_evaluation_with_synthetic_boundary_and_scale_ratios",
            }
        )

    precision_rows = []
    for k in (8, 16, 32, 64):
        alias = leading_alias_model(k)
        target = hardy_target(k)
        parity_ratio = leading_parity_ratio(0.0)
        required_power = normalized_required_power(
            parity_to_alias=parity_ratio,
            boundary_to_alias=boundary_ratio,
            shell_to_alias=shell_ratio,
            reference_power=reference_contrast ** (2 * k),
        )
        precision_rows.append(
            {
                "k": k,
                "alias_leading_model": alias,
                "target": target,
                "alias_to_target_ratio": alias / target,
                "required_power": required_power,
                "target_contrast_radius": target_contrast_radius(
                    k, required_power
                ),
                "power_tolerance_scale_H_over_L": target / alias,
                "radius_tolerance_scale_H_over_kL": target / (k * alias),
                "status": "leading_scale_diagnostic_not_physical_precision_certificate",
            }
        )

    false_positive_rows = []
    for k in (8, 16, 32, 64):
        alias = leading_alias_model(k)
        target = hardy_target(k)
        row = reachability_false_positive(
            theta=0.25, scale=alias, target=target
        )
        row.update(
            {
                "k": k,
                "scale_model": alias,
                "target": target,
                "status": "synthetic_scalar_information_class_counterexample",
            }
        )
        false_positive_rows.append(row)

    uncertainty_rows = []
    for mismatch in (-2.0, -0.5, 0.0, 0.5, 2.0):
        row = uncertainty_interval(mismatch, 0.25, 0.1)
        row.update(
            {
                "model_mismatch_in_target_units": mismatch,
                "observation_bound_in_target_units": 0.25,
                "remainder_bound_in_target_units": 0.1,
            }
        )
        uncertainty_rows.append(row)

    identity_check = joint_matching_decomposition(
        k=8,
        alias_defect=2.0,
        parity_packet=0.4,
        boundary_packet=0.3,
        scale=1.7,
        contrast=0.9,
        reference_contrast=0.8,
        observation_error=0.02,
        remainder=-0.01,
    )
    reachability_check = fixed_reference_reachability(
        8,
        identity_check["demand"],
        1.7,
        0.8,
    )

    data = {
        "status": "rh328_joint_alias_parity_shell_matching_equation",
        "actual_localized_trace_slots_retained": True,
        "exact_typed_joint_matching_equation_proved": True,
        "conditional_fixed_reference_shell_ledger_proved": True,
        "fixed_reference_required_power_formula_proved": True,
        "fixed_reference_reachability_distance_identity_proved": True,
        "phase_normalized_required_power_law_proved": True,
        "fixed_phase_clearance_dictionary_retained": True,
        "unit_edge_target_contrast_law_proved": True,
        "exponential_contrast_radius_precision_law_proved": True,
        "sharp_symmetric_uncertainty_interval_proved": True,
        "rh325_duhamel_majorant_inserted_into_joint_certificate": True,
        "reachability_zero_false_positive_counterexample_proved": True,
        "conditional_joint_alias_parity_shell_matching_equation_proved": True,
        "actual_physical_shell_representation_proved": False,
        "actual_shell_scale_identified": False,
        "physical_exchange_contrast_identified": False,
        "physical_fixed_reference_contrast_identified": False,
        "weighted_trace_observation_norm_controlled": False,
        "all_prefix_suffix_duhamel_weights_controlled": False,
        "actual_full_cycle_duhamel_bound_proved": False,
        "certified_trace_remainder_little_o_proved": False,
        "actual_fixed_contrast_power_mismatch_little_o_proved": False,
        "actual_contrast_radius_precision_proved": False,
        "even_order_contrast_sign_identified": False,
        "archived_decimal_constants_interval_certified": False,
        "finite_formula_diagnostics_promoted_to_physical_asymptotics": False,
        "actual_joint_alias_parity_shell_matching_little_o_proved": False,
        "joint_first_alias_trace_law_proved": False,
        "full_trace_replacement_proved": False,
        "actual_full_trace_divergence_proved": False,
        "parity_weighting_combined_into_full_trace": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
        "gates": {
            "A_canonical_intrinsic_dynamical_spectral_determinant": False,
            "B_time_oriented_scattering_or_unitary_completion": False,
            "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
            "D_von_mangoldt_weighted_prime_power_traces": False,
            "E_completed_zeta_divisor_equality": False,
        },
        "constants": {
            "u_c": U_C,
            "lambda": LAMBDA,
            "hardy_radius": HARDY_RADIUS,
            "target_radius": TARGET_RADIUS,
            "counterloop_beta_limit": BETA,
            "multiplier_constant": MULTIPLIER_CONSTANT,
            "parity_constant": PARITY_CONSTANT,
            "clearance_constant": CLEARANCE_CONSTANT,
            "alpha": ALPHA,
            "kappa_aff": KAPPA_AFF,
            "diagnostic_status": "ordinary_floating_point_formula_evaluations_not_interval_certificates",
        },
        "identity_check": identity_check,
        "reachability_check": reachability_check,
        "phase_rows": phase_rows,
        "precision_rows": precision_rows,
        "false_positive_rows": false_positive_rows,
        "uncertainty_rows": uncertainty_rows,
        "rh329_interface": typed_interface(),
    }

    output = ROOT / "results" / "result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "phase_rows": len(phase_rows),
                "precision_rows": len(precision_rows),
                "false_positive_rows": len(false_positive_rows),
                "uncertainty_rows": len(uncertainty_rows),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
