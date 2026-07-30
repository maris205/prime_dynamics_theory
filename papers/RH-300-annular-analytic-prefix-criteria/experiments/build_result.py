from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from annular_criteria import endpoint_hardy_example, hardy_bound, hinfty_bound  # noqa: E402


def main() -> None:
    rows = [
        {
            "norm": norm,
            "hinfty_prefix_upper": hinfty_bound(norm),
            "hardy_prefix_upper": hardy_bound(norm),
        }
        for norm in (1e-1, 1e-2, 1e-3, 1e-4)
    ]
    endpoint_rows = [
        {
            "term_count": count,
            "hardy_norm": endpoint_hardy_example(count)[0],
            "weighted_l1": endpoint_hardy_example(count)[1],
        }
        for count in (4, 16, 64, 256)
    ]
    payload = {
        "status": "rh300_annular_analytic_prefix_criteria",
        "target_radius": 1.4,
        "outer_radius": 1.41,
        "certified_target_radius": 1.4267874838640739,
        "hinfty_unit_constant": hinfty_bound(1.0),
        "hardy_unit_constant": hardy_bound(1.0),
        "annular_hinfty_criterion_proved": True,
        "annular_hardy_criterion_proved": True,
        "endpoint_hardy_implication_false": True,
        "actual_noisy_annular_convergence_proved": False,
        "direct_weighted_prefix_activated": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
        "endpoint_rows": endpoint_rows,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "endpoint_rows": len(endpoint_rows)}))


if __name__ == "__main__":
    main()
