from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_affine import (  # noqa: E402
    ALPHA,
    CANONICAL_ETA,
    CRITICAL_PARTITION,
    LAMBDA,
    R_FIXED,
    TRACE_RADIUS,
    U_C,
    alias_scale_exponent,
    curvature_shift_l1,
    endpoint_branch_margin,
    entrance_second_moment,
    exact_curved_boundary_l1,
    finite_joint_l1_bound,
    halfline_density,
    remainder_components,
    sharp_linear_coefficient,
)


def _simpson(function, lower: float, upper: float, intervals: int = 20000) -> float:
    if intervals % 2:
        intervals += 1
    step = (upper - lower) / intervals
    total = function(lower) + function(upper)
    total += 4.0 * sum(function(lower + step * index) for index in range(1, intervals, 2))
    total += 2.0 * sum(function(lower + step * index) for index in range(2, intervals, 2))
    return total * step / 3.0


def _curvature_proxy(sigma: float, clearance_ratio: float) -> float:
    upper = max(14.0, clearance_ratio + 12.0)
    return _simpson(
        lambda entrance: halfline_density(entrance, clearance_ratio)
        * curvature_shift_l1(sigma, entrance),
        0.0,
        upper,
    )


def main() -> None:
    row_cases = [
        {
            "sigma": sigma,
            "entrance": entrance,
            "exact_curved_boundary_l1": exact_curved_boundary_l1(sigma, entrance),
            "exact_curvature_shift_l1": curvature_shift_l1(sigma, entrance),
        }
        for sigma, entrance in ((0.10, 0.2), (0.05, 1.0), (0.02, 2.0))
    ]
    phases = [
        {
            "clearance_ratio": ratio,
            "entrance_second_moment": entrance_second_moment(ratio),
            "sharp_linear_coefficient": sharp_linear_coefficient(ratio),
        }
        for ratio in (0.0, 0.5, 1.0, 2.0)
    ]
    finite_cases = []
    for sigma, ratio, limiting in (
        (0.025, 0.0, 0.0),
        (0.025, 0.5, 0.5),
        (0.025, 0.5, 0.45),
    ):
        finite_cases.append(
            {
                "sigma": sigma,
                "clearance_ratio": ratio,
                "limiting_ratio": limiting,
                "components": remainder_components(sigma, ratio),
                "joint_l1_bound": finite_joint_l1_bound(sigma, ratio, limiting),
            }
        )
    proxy_rows = []
    for ratio in (0.0, 0.5):
        coefficient = sharp_linear_coefficient(ratio)
        for sigma in (0.05, 0.025, 0.0125):
            proxy = _curvature_proxy(sigma, ratio)
            proxy_rows.append(
                {
                    "clearance_ratio": ratio,
                    "sigma": sigma,
                    "curvature_proxy": proxy,
                    "proxy_over_sigma": proxy / sigma,
                    "sharp_linear_coefficient": coefficient,
                }
            )
    payload = {
        "status": "rh324_sharp_physical_endpoint_affine_leg_remainder",
        "constants": {
            "u_c": U_C,
            "r": R_FIXED,
            "lambda": LAMBDA,
            "alpha": ALPHA,
            "critical_partition": CRITICAL_PARTITION,
            "canonical_eta": CANONICAL_ETA,
            "canonical_margin": endpoint_branch_margin(),
            "trace_radius": TRACE_RADIUS,
            "alias_scale_exponent": alias_scale_exponent(),
        },
        "row_cases": row_cases,
        "phase_coefficients": phases,
        "finite_cases": finite_cases,
        "curvature_proxy_rows": proxy_rows,
        "exact_physical_first_leg_kernel_formula_proved": True,
        "exact_curved_gaussian_boundary_l1_identity_proved": True,
        "uniform_fold_normalization_tail_proved": True,
        "finite_seed_physical_to_affine_joint_bound_proved": True,
        "sharp_linear_curvature_coefficient_proved": True,
        "first_alias_scale_compatibility_proved": True,
        "exponentially_small_affine_remainder_proved": False,
        "second_leg_physical_remainder_proved": False,
        "actual_two_leg_curvature_remainder_proved": False,
        "moving_order_duhamel_composition_proved": False,
        "parity_weighting_combined": False,
        "neighboring_shell_combined": False,
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
                "row_cases": len(row_cases),
                "phase_coefficients": len(phases),
                "alias_scale_exponent": alias_scale_exponent(),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
