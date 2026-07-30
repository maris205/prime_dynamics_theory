from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from weighted_diagonal import certified_budget, level_tolerance, weighted_sum  # noqa: E402


def main() -> None:
    rows = []
    for level in (2, 4, 8, 16, 32, 64):
        rows.append(
            {
                "level": level,
                "weighted_sum": weighted_sum(level),
                "coefficient_tolerance": level_tolerance(level),
                "certified_weighted_budget": certified_budget(level),
            }
        )
    payload = {
        "status": "rh294_rate_free_weighted_full_trace_diagonal_bridge",
        "radius": 1.4,
        "rate_free_weighted_full_trace_bridge": True,
        "prealias_selected_clock": True,
        "minimal_logarithmic_clock_reached": False,
        "weighted_head_transport_proved": False,
        "determinant_gluing_activated": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "last_budget": rows[-1]["certified_weighted_budget"]}))


if __name__ == "__main__":
    main()
