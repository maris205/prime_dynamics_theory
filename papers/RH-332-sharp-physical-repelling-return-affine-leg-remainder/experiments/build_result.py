from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from repelling_return import (  # noqa: E402
    ALPHA,
    CRITICAL_PARTITION,
    CURVATURE_L1_SLOPE,
    LAMBDA,
    R_FIXED,
    TRACE_RADIUS,
    U_C,
    alias_scale_exponent,
    composite_simpson,
    critical_partition_obstruction_lower_bound,
    critical_partition_source,
    exact_curvature_shift_l1,
    exact_curved_boundary_l1,
    fixed_row_linear_coefficient,
    normal_cdf,
    normal_survival,
    physical_second_row_density,
    physical_tangent_triangle_bounds,
    sector_curvature_proxy,
    sector_intermediate_second_moment,
    sector_transported_linear_coefficient,
    state_interval,
    tangent_second_density,
    total_intermediate_second_moment,
    total_transported_linear_coefficient,
)


def numerical_physical_tangent_l1(sigma: float, source: float) -> float:
    lower, upper = state_interval(sigma)
    inside = composite_simpson(
        lambda output: abs(
            physical_second_row_density(output, sigma, source)
            - tangent_second_density(output, source)
        ),
        lower,
        upper,
        30000,
    )
    tangent_lower = normal_cdf(lower + LAMBDA * source)
    tangent_upper = normal_survival(upper + LAMBDA * source)
    return inside + tangent_lower + tangent_upper


def main() -> None:
    row_cases = []
    for sigma, source in ((0.10, -0.75), (0.08, 0.0), (0.05, 1.25)):
        lower_bound, upper_bound = physical_tangent_triangle_bounds(sigma, source)
        row_cases.append(
            {
                "sigma": sigma,
                "source_u": source,
                "exact_physical_to_curved_l1": exact_curved_boundary_l1(
                    sigma, source
                ),
                "exact_curved_to_tangent_l1": exact_curvature_shift_l1(
                    sigma, source
                ),
                "physical_to_tangent_l1_numerical": numerical_physical_tangent_l1(
                    sigma, source
                ),
                "triangle_lower_bound": lower_bound,
                "triangle_upper_bound": upper_bound,
                "fixed_row_linear_coefficient": fixed_row_linear_coefficient(source),
            }
        )

    sector_coefficients = []
    for phase in (0.0, 0.5, 1.0):
        negative_moment = sector_intermediate_second_moment(
            phase, positive=False
        )
        positive_moment = sector_intermediate_second_moment(phase, positive=True)
        sector_coefficients.append(
            {
                "phase_d": phase,
                "negative_orientation_second_moment": negative_moment,
                "positive_orientation_second_moment": positive_moment,
                "negative_orientation_linear_coefficient": (
                    CURVATURE_L1_SLOPE * negative_moment
                ),
                "positive_orientation_linear_coefficient": (
                    CURVATURE_L1_SLOPE * positive_moment
                ),
                "sector_coefficient_sum": sector_transported_linear_coefficient(
                    phase, positive=False
                )
                + sector_transported_linear_coefficient(phase, positive=True),
                "exact_total_second_moment": total_intermediate_second_moment(phase),
                "exact_total_linear_coefficient": (
                    total_transported_linear_coefficient(phase)
                ),
            }
        )

    proxy_rows = []
    for phase in (0.0, 0.5):
        for sigma in (0.05, 0.025, 0.0125):
            for positive, orientation in ((False, "negative"), (True, "positive")):
                proxy = sector_curvature_proxy(
                    sigma, phase, positive=positive
                )
                proxy_rows.append(
                    {
                        "phase_d": phase,
                        "sigma": sigma,
                        "orientation": orientation,
                        "curvature_proxy": proxy,
                        "proxy_over_sigma": proxy / sigma,
                        "sharp_sector_coefficient": (
                            sector_transported_linear_coefficient(
                                phase, positive=positive
                            )
                        ),
                    }
                )

    global_rows = [
        {
            "sigma": sigma,
            "source_u_at_x_equals_b": critical_partition_source(sigma),
            "reverse_triangle_lower_bound": (
                critical_partition_obstruction_lower_bound(sigma)
            ),
        }
        for sigma in (0.08, 0.04, 0.02)
    ]

    payload = {
        "status": "rh332_sharp_physical_repelling_return_affine_leg_remainder",
        "data_type": (
            "exact_second_hybrid_duhamel_row_term_with_actual_physical_"
            "first_leg_prefix_and_retained_u"
        ),
        "constants": {
            "u_c": U_C,
            "r": R_FIXED,
            "lambda": LAMBDA,
            "alpha": ALPHA,
            "critical_partition": CRITICAL_PARTITION,
            "curvature_l1_slope": CURVATURE_L1_SLOPE,
            "trace_radius": TRACE_RADIUS,
            "alias_scale_exponent": alias_scale_exponent(),
        },
        "row_cases": row_cases,
        "transported_sector_coefficients": sector_coefficients,
        "curvature_proxy_rows": proxy_rows,
        "global_uniformity_obstruction_rows": global_rows,
        "exact_scaled_physical_second_row_formula_proved": True,
        "exact_physical_to_curved_l1_identity_proved": True,
        "exact_curved_to_tangent_l1_identity_proved": True,
        "sharp_fixed_row_linear_coefficient_proved": True,
        "actual_first_leg_prefix_uniform_fourth_moment_proved": True,
        "actual_first_leg_prefix_sector_second_moment_convergence_proved": True,
        "sharp_second_hybrid_sector_coefficients_proved": True,
        "both_repelling_orientation_coefficients_strictly_positive": True,
        "exponentially_small_second_hybrid_accuracy_proved": False,
        "little_o_sigma_second_hybrid_accuracy_proved": False,
        "global_uniform_row_O_sigma_proved": False,
        "exponentially_small_second_hybrid_accuracy_disproved": True,
        "little_o_sigma_second_hybrid_accuracy_disproved": True,
        "global_uniform_row_O_sigma_disproved": True,
        "row_coefficient_at_u_zero_positive": False,
        "physical_first_leg_prefix_used_in_both_hybrids": True,
        "retained_u_hybrid_l1_isometry_used": True,
        "fully_physical_vs_fully_affine_two_leg_equality_proved": False,
        "w_marginal_equality_proved": False,
        "all_cycle_O_k_sigma_transport_proved": False,
        "cyclic_trace_control_proved": False,
        "parity_shell_cancellation_proved": False,
        "full_trace_replacement_proved": False,
        "determinant_gluing_activated": False,
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
                "global_obstruction_rows": len(global_rows),
                "proxy_rows": len(proxy_rows),
                "row_cases": len(row_cases),
                "sector_coefficients": len(sector_coefficients),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
