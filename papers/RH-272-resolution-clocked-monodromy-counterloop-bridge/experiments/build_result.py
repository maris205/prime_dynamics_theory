from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from counterloop import BETA, LAMBDA, bridge_error, counterloop_moment  # noqa: E402


def main() -> None:
    rows = []
    for k in (3, 5, 10, 15, 28):
        max_err = max(
            abs(counterloop_moment(k, n) - (-2 * BETA**n if n % 2 == 0 else 0.0))
            for n in range(1, 2 * k)
        )
        rows.append({"k": k, "pre_alias_orders": 2 * k - 1, "max_moment_error": max_err,
                     "interior_error_R_0_8": bridge_error(k, 0.8)})
    payload = {
        "status": "rh272_resolution_clocked_monodromy_counterloop_bridge",
        "lambda": LAMBDA, "beta": BETA, "hardy_radius": 0.85,
        "rows": rows,
        "spectral_cloud_identification": False,
        "gate_A": False, "gates_B_to_E": False,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"rows": len(rows), "max_error": max(r["max_moment_error"] for r in rows)}))


if __name__ == "__main__":
    main()
