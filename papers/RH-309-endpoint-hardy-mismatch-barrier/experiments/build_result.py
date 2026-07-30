from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from endpoint_hardy import (  # noqa: E402
    RHO_STAR,
    complement_endpoint_product,
    endpoint_h2_lower_bound,
    endpoint_conversion_constant,
    model_target_hardy_tail_bounds,
    normalized_logarithmic_scale,
)


def main() -> None:
    rows = []
    for mass in (1e4, 1e8, 1e16):
        cutoff, lower = endpoint_h2_lower_bound(mass)
        rows.append(
            {
                "mass": mass,
                "forced_odd_cutoff": cutoff,
                "certified_endpoint_h2_lower": lower,
                "normalized_logarithmic_scale": normalized_logarithmic_scale(mass),
            }
        )
    payload = {
        "status": "rh309_endpoint_hardy_mismatch_barrier",
        "rho_star": RHO_STAR,
        "q_rho_star": complement_endpoint_product(),
        "endpoint_h2_conversion_constant": endpoint_conversion_constant(),
        "mismatch_belongs_to_endpoint_h2": True,
        "mismatch_belongs_to_endpoint_hinfinity": False,
        "endpoint_h2_convergence_proved": False,
        "endpoint_h2_nonconvergence_proved": False,
        "mass_logarithmic_rate_barrier_proved": True,
        "small_noise_logarithmic_rate_barrier_proved": True,
        "model_tail_bounds_at_100": model_target_hardy_tail_bounds(100),
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"endpoint_constant": endpoint_conversion_constant()}))


if __name__ == "__main__":
    main()
