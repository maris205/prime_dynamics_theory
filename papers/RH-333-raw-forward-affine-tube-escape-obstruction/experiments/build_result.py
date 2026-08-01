"""Build the deterministic RH-333 reproduction and claim ledger."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from raw_affine_escape import (  # noqa: E402
    C_B_REPRODUCTION,
    C_M_REPRODUCTION,
    LAMBDA,
    R_FIXED,
    TRACE_RADIUS,
    U_C,
    finite_orbit_row,
    phase_row,
    reproduction_C_s,
)


def result_payload() -> dict[str, object]:
    """Return the complete deterministic result ledger."""

    finite_rows = [finite_orbit_row(k) for k in (4, 8, 12, 16, 20, 24)]
    phase_rows = [phase_row(eta) for eta in (-0.5, 0.0, 0.5)]
    false_claims = {
        "adapted_reference_refuted": False,
        "all_cycle_physical_affine_transport_proved": False,
        "branch_complete_nonlinear_closing_profile_refuted": False,
        "closing_row_endpoint_failure_proved": False,
        "cyclic_bridge_refuted": False,
        "cyclic_trace_control_proved": False,
        "determinant_gluing_activated": False,
        "doob_transform_refuted": False,
        "final_endpoint_marginal_lower_bound_proved": False,
        "full_trace_replacement_proved": False,
        "hilbert_polya_constructed": False,
        "physical_truncated_folded_affine_kernel_refuted": False,
        "probability_retained_path_identified_with_cyclic_trace": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "signed_shell_parity_cancellation_proved": False,
        "trace_observation_map_proved": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    return {
        "status": "rh333_raw_forward_affine_tube_escape_obstruction",
        "data_type": (
            "raw_mass_one_full_line_forward_affine_k_minus_1_component_row_"
            "prefix_with_retained_preclosing_coordinate"
        ),
        "period_scope": {
            "component_period": "k",
            "minimum_component_period": 2,
            "sigma_domain": "sigma>0",
            "physical_one_step_period": "2k",
            "raw_prefix_component_rows": "k-1",
            "excluded_component_row": "tiny_closing_row_j_equals_k_minus_1",
            "retained_coordinate": "q_k_minus_1_preclosing",
        },
        "phase_scope": {
            "eta_sigma": "k-log(1/sigma)/(2*log(lambda))",
            "fixed_phase": "eta_sigma_converges_to_a_finite_eta",
            "compact_phase": "eta_sigma_stays_in_one_fixed_compact_interval",
            "rate_refutation_scope": "fixed_or_compact_first_alias_phase",
        },
        "theorem_constants": {
            "symbolic": {
                "absolute_multiplier": "C_M*lambda^k*(1+o(1))",
                "boundary_clearance": "C_b*lambda^(-2k)*(1+o(1))",
                "C_s": (
                    "C_M*sqrt(1+lambda^2)/"
                    "(8*u_c^2*lambda*sqrt(C_b))"
                ),
            },
            "decimal_reproduction": {
                "u_c": U_C,
                "r": R_FIXED,
                "lambda": LAMBDA,
                "C_b": C_B_REPRODUCTION,
                "C_M": C_M_REPRODUCTION,
                "C_s": reproduction_C_s(),
                "trace_radius": TRACE_RADIUS,
            },
            "decimal_values_are_interval_certificates": False,
        },
        "finite_orbit_rows": finite_rows,
        "limiting_phase_rows": phase_rows,
        "exact_forward_affine_expansion_proved": True,
        "sigma_scaled_coordinate_about_cycle_point_used": True,
        "canonical_two_step_tangent_coarsening_derived": True,
        "exact_first_innovation_sd_product_identity_proved": True,
        "signed_forward_mean_slopes_used": True,
        "forward_variance_recurrence_with_plus_noise_proved": True,
        "rh18_widths_identified_as_peak_normalized_backward_observables": True,
        "gaussian_maximum_interval_mass_lemma_proved": True,
        "physical_preclosing_support_interval_length_is_one_over_sigma": True,
        "factor_four_unhalved_l1_lower_bound_proved": True,
        "marginal_contraction_lifts_bound_to_retained_paths": True,
        "full_retained_extensions_including_preclosing_coordinate_covered": True,
        "fixed_phase_positive_path_l1_liminf_proved": True,
        "compact_phase_uniform_positive_path_l1_liminf_proved": True,
        "fixed_or_compact_phase_raw_forward_retained_path_O_k_sigma_disproved": True,
        "fixed_or_compact_phase_raw_forward_retained_path_o_H_k_disproved": True,
        "raw_full_line_mass_one_affine_reference_refuted_at_preclosing_path_scope": True,
        "finite_rows_promoted_to_asymptotic_evidence": False,
        "symbolic_constants_used_in_theorem": True,
        "unhalved_l1_convention": True,
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
    }


def main() -> None:
    payload = result_payload()
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "false_claims": len(payload["false_claims"]),
                "finite_orbit_rows": len(payload["finite_orbit_rows"]),
                "phase_rows": len(payload["limiting_phase_rows"]),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
