from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from folded_halfline import (  # noqa: E402
    direct_wasserstein_tail,
    exact_l1_tail,
    exact_tv_tail,
    limit_l1_distance,
    limit_mean,
    limit_second_moment,
    limit_variance,
)


def main() -> None:
    row_cases = (
        (0.25, 0.0),
        (0.25, 0.75),
        (0.25, 1.5),
        (0.20, 1.5),
        (1.0 / 6.0, 1.5),
        (0.125, 1.5),
    )
    rows = [
        {
            "sigma": sigma,
            "clearance_ratio": ratio,
            "exact_l1_tail": exact_l1_tail(sigma, ratio),
            "exact_total_variation_tail": exact_tv_tail(sigma, ratio),
            "direct_wasserstein_tail": direct_wasserstein_tail(sigma, ratio),
        }
        for sigma, ratio in row_cases
    ]
    profiles = [
        {
            "clearance_ratio": ratio,
            "mean": limit_mean(ratio),
            "second_moment": limit_second_moment(ratio),
            "variance": limit_variance(ratio),
        }
        for ratio in (0.0, 0.5, 1.0, 2.0)
    ]
    separations = [
        {
            "first_ratio": first,
            "second_ratio": second,
            "exact_l1_distance": limit_l1_distance(first, second),
        }
        for first, second in ((0.0, 0.5), (0.0, 1.0), (1.0, 2.0))
    ]
    payload = {
        "status": "rh322_certified_critical_folded_row_half_line_profile",
        "tv_convention": "total_variation_equals_one_half_l1",
        "physical_folded_row_formula_proved": True,
        "exact_same_clearance_tv_identity_proved": True,
        "clearance_parameter_l1_stability_proved": True,
        "all_polynomial_moment_convergence_proved": True,
        "clearance_phase_nonuniversality_proved": True,
        "phase_independent_universal_profile_proved": False,
        "joint_first_alias_trace_law_proved": False,
        "parity_layer_combined": False,
        "neighboring_shell_combined": False,
        "moving_order_remainder_proved": False,
        "full_trace_replacement_proved": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
        "rows": rows,
        "limit_profiles": profiles,
        "profile_separations": separations,
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "row_cases": len(rows),
                "largest_tv_tail": max(row["exact_total_variation_tail"] for row in rows),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
