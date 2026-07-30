from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from determinant_gluing import gluing_relative_error, weighted_prefix  # noqa: E402


def main() -> None:
    rows = []
    for scale in (1e-1, 1e-2, 1e-3, 1e-4):
        errors = [scale * 0.4**order for order in range(2, 14)]
        prefix = weighted_prefix(errors, 1.4)
        rows.append(
            {
                "scale": scale,
                "weighted_prefix": prefix,
                "relative_error_upper": gluing_relative_error(prefix, scale, scale),
            }
        )
    payload = {
        "status": "rh288_prefix_tail_determinant_gluing_criterion",
        "rows": rows,
        "three_budget_theorem": True,
        "noisy_spectral_tail_leaf": True,
        "target_tail_leaf": True,
        "direct_weighted_complement_anchor_prefix_leaf": False,
        "weighted_full_trace_counterloop_anchor_leaf": False,
        "weighted_head_counterloop_leaf": False,
        "criterion_activated": False,
        "gate_A": False,
        "gates_B_to_E": False,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "activated": False}))


if __name__ == "__main__":
    main()
