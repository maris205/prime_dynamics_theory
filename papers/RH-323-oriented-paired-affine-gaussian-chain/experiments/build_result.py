from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from paired_affine import (  # noqa: E402
    ALPHA,
    BETA,
    KAPPA_AFF,
    LAMBDA,
    S1,
    S2,
    U_C,
    conditioning_bias,
    covariance_matrix,
    entrance_mean,
    entrance_variance,
    intermediate_positive_probability_at_zero,
    joint_l1_bound,
    mean_vector,
    output_negative_probability_at_zero,
    output_tail_ratio_limit,
)


def main() -> None:
    phases = [
        {
            "clearance_ratio": ratio,
            "entrance_mean": entrance_mean(ratio),
            "entrance_variance": entrance_variance(ratio),
            "mean_vector": mean_vector(ratio),
            "conditioning_bias": conditioning_bias(ratio),
            "covariance_matrix": covariance_matrix(ratio),
            "output_right_tail_ratio_limit": output_tail_ratio_limit(ratio),
        }
        for ratio in (0.0, 0.5, 1.0, 2.0)
    ]
    finite_cases = [
        {
            "sigma": sigma,
            "clearance_ratio": ratio,
            "limiting_ratio": limiting,
            "joint_l1_bound": joint_l1_bound(sigma, ratio, limiting),
        }
        for sigma, ratio, limiting in (
            (0.20, 0.8, 0.8),
            (0.20, 0.8, 0.7),
            (0.125, 1.0, 1.0),
        )
    ]
    payload = {
        "status": "rh323_oriented_paired_affine_gaussian_chain",
        "constants": {
            "u_c": U_C,
            "lambda": LAMBDA,
            "alpha": ALPHA,
            "kappa_aff": KAPPA_AFF,
            "beta": BETA,
            "s1": S1,
            "s2": S2,
        },
        "orientation_leakage_at_zero": {
            "probability_u_positive": intermediate_positive_probability_at_zero(),
            "probability_w_negative": output_negative_probability_at_zero(),
        },
        "phase_profiles": phases,
        "finite_cases": finite_cases,
        "oriented_two_leg_affine_chain_proved": True,
        "exact_joint_tv_transfer_proved": True,
        "source_coordinate_retained_in_isometry": True,
        "marginal_l1_contraction_proved": True,
        "marginal_l1_isometry_proved": False,
        "intermediate_extended_skew_normal_proved": True,
        "final_extended_skew_normal_proved": True,
        "conditioning_bias_moments_proved": True,
        "non_gaussian_output_proved": True,
        "actual_two_leg_curvature_remainder_proved": False,
        "parity_weighting_combined": False,
        "neighboring_shell_combined": False,
        "moving_order_remainder_proved": False,
        "joint_first_alias_trace_law_proved": False,
        "full_trace_replacement_proved": False,
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
                "phase_profiles": len(phases),
                "u_positive_at_zero": intermediate_positive_probability_at_zero(),
                "w_negative_at_zero": output_negative_probability_at_zero(),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
