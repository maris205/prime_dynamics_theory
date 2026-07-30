from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from bridge_clock import (  # noqa: E402
    block_clock,
    complement_tail_bound,
    critical_slope,
    target_tail_bound,
)


def main() -> None:
    slope = critical_slope()
    rows = []
    for sigma in (1e-2, 1e-3, 1e-4, 1e-6, 1e-8):
        rows.append(
            {
                "sigma": sigma,
                "minimal_bridge_clock": block_clock(sigma, slope),
                "slope_four_clock": block_clock(sigma, 4.0),
                "complement_tail_upper": complement_tail_bound(sigma),
                "target_tail_upper": target_tail_bound(sigma),
            }
        )
    payload = {
        "status": "rh292_tail_absorbed_weighted_bridge_clock",
        "radius": 1.4,
        "cutoff": 0.5,
        "minimal_bridge_slope": slope,
        "slope_four": 4.0,
        "clock_shortening_proved": True,
        "critical_tail_absorption_proved": True,
        "direct_weighted_prefix_proved": False,
        "weighted_full_trace_bridge_proved": False,
        "weighted_head_transport_proved": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "minimal_slope": slope}))


if __name__ == "__main__":
    main()
