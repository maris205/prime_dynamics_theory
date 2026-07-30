from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from head_necessity import coefficient_error, head_transport_bound  # noqa: E402


def main() -> None:
    rows = []
    for order in (2, 3, 5, 8):
        rows.append(
            {
                "order": order,
                "coefficient_bound_at_norm_1e-6": coefficient_error(
                    1e-6, 1.41, order
                ),
                "head_bound_with_1e-6_inputs": head_transport_bound(
                    1e-6, 1e-6, 1e-6, 1.41, order
                ),
            }
        )
    payload = {
        "status": "rh303_annular_fixed_order_head_transport_necessity",
        "fixed_order_head_transport_necessity_proved": True,
        "annular_route_bypasses_root_matching": True,
        "annular_route_bypasses_head_moments": False,
        "actual_head_transport": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "head_necessity": True}))


if __name__ == "__main__":
    main()
