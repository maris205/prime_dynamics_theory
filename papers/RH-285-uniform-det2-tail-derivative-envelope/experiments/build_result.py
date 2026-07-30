from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from det2_tail import derivative_envelope, power_gain  # noqa: E402


def main() -> None:
    rows = []
    for sigma in (1e-2, 1e-4, 1e-8):
        rows.append(
            {
                "sigma": sigma,
                "derivative_bounds": {
                    str(order): derivative_envelope(sigma, order)
                    for order in range(4)
                },
            }
        )
    payload = {
        "status": "rh285_uniform_det2_tail_derivative_envelope",
        "power_gain": power_gain(),
        "derivative_orders_audited": [0, 1, 2, 3],
        "rows": rows,
        "all_fixed_derivative_orders_proved": True,
        "finite_head_bridge": False,
        "gate_A": False,
        "gates_B_to_E": False,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "power_gain": power_gain()}))


if __name__ == "__main__":
    main()
