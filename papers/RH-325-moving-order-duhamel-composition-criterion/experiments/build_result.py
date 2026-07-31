from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from moving_duhamel import (  # noqa: E402
    ALIAS_EXPONENT,
    PACKET_CONDITIONING_LOWER_EXPONENT,
    LAMBDA,
    QUARTER_POWER_SLACK,
    STABILITY_GROWTH_THRESHOLD,
    TRACE_RADIUS,
    U_C,
    cyclic_trace_counterexample,
    moving_order_budget,
    phase_transport_counterexample,
    stability_power,
)


def main() -> None:
    exponents = (
        ("markov_contraction", 0.0),
        ("quarter_power_model", PACKET_CONDITIONING_LOWER_EXPONENT),
        ("critical_threshold", STABILITY_GROWTH_THRESHOLD),
        ("supercritical_example", 0.4),
    )
    stability_rows = [
        {
            "label": label,
            "growth_exponent": exponent,
            "residual_power": stability_power(exponent),
            "classification": (
                "subcritical"
                if exponent < STABILITY_GROWTH_THRESHOLD
                else "critical"
                if exponent == STABILITY_GROWTH_THRESHOLD
                else "supercritical"
            ),
        }
        for label, exponent in exponents
    ]
    clock_rows = []
    for sigma in (1e-4, 1e-6, 1e-8, 1e-10, 1e-12):
        models = {
            label: moving_order_budget(sigma, growth_exponent=exponent)
            for label, exponent in exponents
        }
        clock_rows.append({"sigma": sigma, "models": models})

    trace_rows = [
        cyclic_trace_counterexample(dimension)
        for dimension in (8, 32, 128, 512)
    ]
    payload = {
        "status": "rh325_moving_order_duhamel_composition_criterion",
        "constants": {
            "u_c": U_C,
            "lambda": LAMBDA,
            "trace_radius": TRACE_RADIUS,
            "alias_exponent": ALIAS_EXPONENT,
            "stability_growth_threshold": STABILITY_GROWTH_THRESHOLD,
            "gaussian_conditioning_lower_exponent": PACKET_CONDITIONING_LOWER_EXPONENT,
            "quarter_power_residual_slack": QUARTER_POWER_SLACK,
        },
        "stability_rows": stability_rows,
        "clock_rows": clock_rows,
        "phase_transport_counterexample": phase_transport_counterexample(),
        "trace_counterexamples": trace_rows,
        "retained_coordinate_markov_duhamel_criterion_proved": True,
        "endpoint_marginal_contraction_proved": True,
        "phase_transport_same_seed_obstruction_proved": True,
        "operator_trace_observation_duhamel_criterion_proved": True,
        "sharp_stability_growth_threshold_proved": True,
        "dimension_free_markov_to_trace_bound_proved": False,
        "growing_state_trace_counterexample_proved": True,
        "all_physical_legs_have_uniform_order_sigma_remainders": False,
        "second_physical_critical_leg_controlled": False,
        "actual_full_cycle_duhamel_bound_proved": False,
        "weighted_trace_observation_norm_controlled": False,
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
                "clock_rows": len(clock_rows),
                "stability_rows": len(stability_rows),
                "trace_counterexamples": len(trace_rows),
                "threshold": STABILITY_GROWTH_THRESHOLD,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
