from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from clock_separation import (  # noqa: E402
    clearance_exponent,
    localization_slope,
    tail_decay_exponent,
    tail_slope,
)


def main() -> None:
    tail = tail_slope()
    local = localization_slope()
    payload = {
        "status": "rh296_tail_localization_clock_separation",
        "tail_critical_slope": tail,
        "localization_ceiling_slope": local,
        "slope_gap": tail - local,
        "slope_ratio": tail / local,
        "tail_exponent_at_localization_ceiling": tail_decay_exponent(local),
        "clearance_exponent_at_tail_clock": clearance_exponent(tail),
        "clearance_exponent_at_slope_four": clearance_exponent(4.0),
        "clock_intersection_empty_for_current_methods": True,
        "actual_trace_nonconvergence_proved": False,
        "new_boundary_layer_route_excluded": False,
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"gap": tail - local, "ratio": tail / local}))


if __name__ == "__main__":
    main()
