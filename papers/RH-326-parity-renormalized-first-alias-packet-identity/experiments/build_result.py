from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from parity_alias_packet import (  # noqa: E402
    AFFINE_NOISE_BETA,
    ALIAS_GROWTH_EXPONENT,
    ALPHA,
    CLEARANCE_CONSTANT,
    COUNTERLOOP_BETA_LIMIT,
    C_STAR,
    HARDY_RADIUS,
    KAPPA_AFF,
    LAMBDA,
    MATCHING_EXPONENT,
    MULTIPLIER_CONSTANT,
    SCALAR_BALANCE_CLEARANCE,
    SCALAR_BALANCE_PHASE,
    TRACE_RADIUS,
    asymptotic_beta_k,
    packet_row,
    phase_row,
    scalar_balance_ratio,
    sign_rows,
)


def main() -> None:
    packet_rows = [packet_row(k, 0.0) for k in (8, 16, 32, 64)]
    phase_rows = [
        phase_row(phase)
        for phase in (-1.0, -0.5, 0.0, 0.5, 1.0, SCALAR_BALANCE_PHASE)
    ]
    parity_rows = sign_rows(6, 0.02, asymptotic_beta_k(6))
    payload = {
        "status": "rh326_parity_renormalized_first_alias_packet_identity",
        "constants": {
            "lambda": LAMBDA,
            "hardy_radius": HARDY_RADIUS,
            "trace_radius": TRACE_RADIUS,
            "counterloop_beta_limit": COUNTERLOOP_BETA_LIMIT,
            "parity_constant": C_STAR,
            "multiplier_constant": MULTIPLIER_CONSTANT,
            "clearance_constant": CLEARANCE_CONSTANT,
            "alias_growth_exponent": ALIAS_GROWTH_EXPONENT,
            "matching_exponent": MATCHING_EXPONENT,
            "scalar_balance_phase": SCALAR_BALANCE_PHASE,
            "scalar_balance_clearance": SCALAR_BALANCE_CLEARANCE,
            "canonical_phase_ratio_upper_bound": scalar_balance_ratio(1.0),
            "alpha": ALPHA,
            "kappa_aff": KAPPA_AFF,
            "affine_noise_beta": AFFINE_NOISE_BETA,
        },
        "packet_rows": packet_rows,
        "phase_rows": phase_rows,
        "sign_rows": parity_rows,
        "exact_hardy_parity_decomposition_proved": True,
        "exact_counterloop_defect_decomposition_proved": True,
        "exact_counterloop_first_alias_moment_identity_proved": True,
        "uniform_scalar_parity_packet_expansion_proved": True,
        "even_first_alias_parity_correction_positive_proved": True,
        "parity_renormalized_first_alias_packet_identity_proved": True,
        "alias_parity_common_weighted_exponent_proved": True,
        "scalar_balance_phase_law_proved": True,
        "canonical_integer_phase_scalar_only_obstruction_proved": True,
        "clearance_phase_retained_in_packet": True,
        "retained_coordinate_frame_recorded": True,
        "rh327_shell_interface_typed": True,
        "separate_alias_parity_majorant_closes_bridge": False,
        "scalar_parity_alone_closes_first_alias_matching": False,
        "local_boundary_probability_packet_identified_with_trace": False,
        "second_physical_critical_leg_controlled": False,
        "all_physical_legs_have_uniform_order_sigma_remainders": False,
        "actual_full_cycle_duhamel_bound_proved": False,
        "weighted_trace_observation_norm_controlled": False,
        "neighboring_shell_included": False,
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
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "packet_rows": len(packet_rows),
                "phase_rows": len(phase_rows),
                "sign_rows": len(parity_rows),
                "balance_phase": SCALAR_BALANCE_PHASE,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
