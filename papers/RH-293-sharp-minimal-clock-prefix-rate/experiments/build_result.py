from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from prefix_rate import (  # noqa: E402
    critical_exponent,
    minimal_bridge_slope,
    saturated_budget,
)


def main() -> None:
    slope = minimal_bridge_slope()
    beta_star = critical_exponent(slope)
    rows = []
    for sigma in (1e-2, 1e-3, 1e-4, 1e-6, 1e-8):
        rows.append(
            {
                "sigma": sigma,
                "below_budget": saturated_budget(sigma, 0.8),
                "critical_budget": saturated_budget(sigma, beta_star),
                "above_budget": saturated_budget(sigma, 1.1),
            }
        )
    payload = {
        "status": "rh293_sharp_minimal_clock_prefix_rate",
        "radius": 1.4,
        "minimal_bridge_slope": slope,
        "critical_uniform_error_exponent": beta_star,
        "uniform_error_class_threshold_sharp": True,
        "actual_noisy_uniform_rate_proved": False,
        "direct_weighted_prefix_proved": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "critical_exponent": beta_star}))


if __name__ == "__main__":
    main()
