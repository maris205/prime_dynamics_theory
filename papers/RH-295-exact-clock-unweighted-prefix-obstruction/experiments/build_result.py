from __future__ import annotations

import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from prefix_obstruction import escaping_spike, minimal_clock  # noqa: E402


def main() -> None:
    rows = []
    for sigma in (1e-2, 1e-3, 1e-4, 1e-6, 1e-8):
        cut = minimal_clock(sigma)
        amplitude, budget = escaping_spike(cut)
        rows.append(
            {
                "sigma": sigma,
                "minimal_clock": cut,
                "uniform_error": amplitude,
                "weighted_prefix": budget,
            }
        )
    payload = {
        "status": "rh295_exact_clock_unweighted_prefix_obstruction",
        "radius": 1.4,
        "minimal_clock_uniform_decay_exponent": math.log(1.4)
        / (2.0 * math.log(10.0 / 7.0)),
        "minimal_clock_weighted_growth_exponent": math.log(1.4)
        / (2.0 * math.log(10.0 / 7.0)),
        "fixed_order_convergence": True,
        "exact_clock_uniform_error_vanishes": True,
        "weighted_prefix_diverges": True,
        "physical_noisy_spike_claimed": False,
        "global_nonexistence_claimed": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "last_prefix": rows[-1]["weighted_prefix"]}))


if __name__ == "__main__":
    main()
