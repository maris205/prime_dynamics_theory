from __future__ import annotations

import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from root_l1_clock import critical_exponent, radial_pair_budget  # noqa: E402


def main() -> None:
    slope = 1.0 / math.log(10.0 / 7.0)
    beta = 1.0 / (0.85 * math.sqrt(1.678573510428322))
    gamma_star = critical_exponent(slope, beta)
    rows = []
    for sigma in (1e-2, 1e-3, 1e-4, 1e-6, 1e-8):
        rows.append(
            {
                "sigma": sigma,
                "below_budget": radial_pair_budget(sigma, 0.5, slope, beta),
                "critical_budget": radial_pair_budget(sigma, gamma_star, slope, beta),
                "above_budget": radial_pair_budget(sigma, 0.8, slope, beta),
            }
        )
    payload = {
        "status": "rh299_zero_padded_root_l1_bridge_clock",
        "minimal_bridge_slope": slope,
        "shell_radius": beta,
        "local_shell_critical_exponent": gamma_star,
        "global_hardy_cap_critical_exponent": critical_exponent(slope, 1.0 / 0.85),
        "zero_padded_transport_proved": True,
        "sharp_rate_law_proved": True,
        "actual_modulus_head_matching_proved": False,
        "weighted_head_budget_activated": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "critical_exponent": gamma_star}))


if __name__ == "__main__":
    main()
