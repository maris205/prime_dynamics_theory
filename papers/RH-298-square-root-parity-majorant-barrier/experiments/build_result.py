from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from parity_majorant import (  # noqa: E402
    growth_exponent,
    minimal_bridge_slope,
    parity_budget,
)


def main() -> None:
    slope = minimal_bridge_slope()
    rows = [
        {"sigma": sigma, "separate_parity_budget": parity_budget(sigma)}
        for sigma in (1e-2, 1e-3, 1e-4, 1e-6, 1e-8)
    ]
    payload = {
        "status": "rh298_square_root_parity_majorant_barrier",
        "minimal_bridge_slope": slope,
        "minimal_clock_growth_exponent": growth_exponent(slope),
        "slope_four_growth_exponent": growth_exponent(4.0),
        "critical_separate_parity_slope": 0.5 / __import__("math").log(1.4 / 0.85),
        "fixed_order_bulk_leakage_law": True,
        "separate_parity_majorant_diverges": True,
        "combined_full_trace_error_diverges_proved": False,
        "moving_order_cancellation_excluded": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "growth_exponent": growth_exponent(slope)}))


if __name__ == "__main__":
    main()
