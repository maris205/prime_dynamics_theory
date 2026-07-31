"""Build the deterministic RH-329 isolated-model audit ledger."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from isolated_audit import (  # noqa: E402
    BOUNDARY_CONTRAST,
    CLEARANCE_CONSTANT,
    EXPANSION,
    HARDY_RADIUS,
    MODEL_CONTRAST,
    MULTIPLIER_CONSTANT,
    PARITY_CONSTANT,
    PHASE,
    REFERENCE_CONTRAST,
    TARGET_RADIUS,
    audit_row,
    beta_squared,
    fraction_string,
    frozen_certificates,
    isolated_interface,
    outward_decimal_interval,
)


ORDERS = (2, 4, 8, 16, 24, 32)


def encoded_exact(value: Fraction | bool) -> bool | dict[str, object]:
    """Encode an exact verdict or rational with a directed display interval."""

    if isinstance(value, bool):
        return value
    return {
        "exact": fraction_string(value),
        "interval": outward_decimal_interval(value),
    }


def main() -> None:
    certificates = frozen_certificates()
    rows = [audit_row(k) for k in ORDERS]
    phase_limit = PARITY_CONSTANT * MULTIPLIER_CONSTANT
    required_power_limit = 1 - phase_limit
    growth_base = TARGET_RADIUS**2 * beta_squared()

    data = {
        "status": "rh329_validated_isolated_exchange_model_audit",
        "scope": "frozen_graded_finite_dimensional_isolated_model_only",
        "verdict_source": "exact_fraction_arithmetic",
        "finite_rows_status": "reproduction_checks_not_asymptotic_evidence",
        "frozen_isolated_model_from_exact_rational_data": True,
        "graded_family_not_one_all_order_operator": True,
        "exact_exchange_block_trace_law_proved": True,
        "exact_alias_block_identity_proved": True,
        "exact_parity_block_identity_proved": True,
        "exact_boundary_block_identity_proved": True,
        "exact_shell_block_identity_proved": True,
        "model_boundary_packet_exact_zero": True,
        "model_observation_error_exact_zero": True,
        "model_far_remainder_exact_zero": True,
        "model_all_prefix_suffix_duhamel_weights_retained": True,
        "model_all_duhamel_leg_defects_exact_zero": True,
        "model_duhamel_majorant_exact_zero": True,
        "parity_to_alias_limit_proved": True,
        "required_power_interior_limit_proved": True,
        "eventual_zero_reachability_screen_proved": True,
        "fixed_model_contrast_matching_failure_proved": True,
        "residual_to_alias_negative_limit_proved": True,
        "alias_to_target_divergence_proved_in_model": True,
        "residual_to_target_negative_divergence_proved_in_model": True,
        "required_contrast_radius_tends_to_one_proved": True,
        "model_exponential_precision_barrier_violated": True,
        "scoped_isolated_model_negative_result_proved": True,
        "all_reported_rows_reachable_exact": all(
            bool(row["reachability_screen_zero_exact"]) for row in rows
        ),
        "all_reported_rows_fail_target_window_exact": all(
            not bool(row["within_one_target_unit_exact"]) for row in rows
        ),
        "actual_noisy_operator_identified": False,
        "actual_physical_shell_representation_proved": False,
        "actual_shell_scale_or_contrast_theorem_proved": False,
        "actual_trace_observation_duhamel_bound_proved": False,
        "actual_far_remainder_little_o_proved": False,
        "actual_joint_alias_parity_shell_matching_little_o_proved": False,
        "joint_first_alias_full_trace_law_proved": False,
        "full_trace_replacement_proved": False,
        "actual_full_trace_divergence_proved": False,
        "single_all_order_operator_constructed": False,
        "finite_rows_promoted_to_physical_asymptotics": False,
        "archived_decimal_constants_interval_certified": False,
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
            "hardy_radius": fraction_string(HARDY_RADIUS),
            "target_radius": fraction_string(TARGET_RADIUS),
            "expansion": fraction_string(EXPANSION),
            "multiplier_constant": fraction_string(MULTIPLIER_CONSTANT),
            "parity_constant": fraction_string(PARITY_CONSTANT),
            "clearance_constant": fraction_string(CLEARANCE_CONSTANT),
            "model_contrast": fraction_string(MODEL_CONTRAST),
            "reference_contrast": fraction_string(REFERENCE_CONTRAST),
            "boundary_contrast": fraction_string(BOUNDARY_CONTRAST),
            "phase": fraction_string(PHASE),
            "constant_status": (
                "model_defining_exact_rationals_not_certified_intervals_for_"
                "physical_constants"
            ),
        },
        "block_definitions": {
            "exchange": "K_c=1/2*[[1+c,1-c],[1-c,1+c]]",
            "alias": "C_k=diag(beta_k*I_(2k-2),beta*I_2)",
            "alias_root_law": "beta_k^(2k)=beta^(2k)/C_M",
            "parity_gap": "delta_k=C_*Lambda^(-k)",
            "boundary": "identical_scaled_exchange_blocks_with_c_b=1/2",
            "shell": "Q_(c,k)=A_k^(1/(2k))*K_c",
            "noise_clock": "sigma_k=Lambda^(-2k)",
        },
        "exact_certificates": {
            key: encoded_exact(value) for key, value in certificates.items()
        },
        "asymptotic_certificate": {
            "parity_to_alias_limit_exact": fraction_string(phase_limit),
            "required_power_limit_exact": fraction_string(required_power_limit),
            "residual_to_alias_limit_exact": fraction_string(-required_power_limit),
            "alias_target_growth_base_exact": fraction_string(growth_base),
            "parity_expansion": (
                "1-(1-C_*Lambda^(-k))^(2k)~2k*C_*Lambda^(-k)"
            ),
            "alias_expansion": "A_k~(2k/C_M)*beta^(2k)",
            "power_tolerance": "H_k/A_k=(k/a_k)*(beta*R)^(-2k)",
            "radius_tolerance": "H_k/(k*A_k)=a_k^(-1)*(beta*R)^(-2k)",
            "fixed_radius_gap_limit_exact": "1/5",
            "conclusion": (
                "fixed power and radius mismatches violate both exponential "
                "precision scales; e_k/H_k->-infinity"
            ),
        },
        "row_orders": list(ORDERS),
        "row_count": len(rows),
        "total_retained_duhamel_weight_count": sum(4 * k for k in ORDERS),
        "rows": rows,
        "rh330_interface": isolated_interface(),
    }

    output = ROOT / "results" / "result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n"
    )
    print(
        json.dumps(
            {
                "all_rows_fail": data["all_reported_rows_fail_target_window_exact"],
                "all_rows_reachable": data["all_reported_rows_reachable_exact"],
                "rows": len(rows),
                "total_duhamel_weights": data[
                    "total_retained_duhamel_weight_count"
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
