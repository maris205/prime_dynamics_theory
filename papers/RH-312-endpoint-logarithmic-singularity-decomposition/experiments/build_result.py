from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from endpoint_singularity import (  # noqa: E402
    Q_STAR,
    RHO_STAR,
    odd_normalized_anchor,
    regularity_radius_lower_bound,
)


def main() -> None:
    rows = [
        {
            "order": order,
            "normalized_anchor": odd_normalized_anchor(order),
            "remainder": odd_normalized_anchor(order) - 1.0,
        }
        for order in (3, 9, 21)
    ]
    payload = {
        "status": "rh312_endpoint_logarithmic_singularity_decomposition",
        "q_star": Q_STAR,
        "rho_star": RHO_STAR,
        "regularity_radius_lower_bound": regularity_radius_lower_bound(),
        "exact_logarithmic_singularity_proved": True,
        "analytic_remainder_beyond_unit_circle_proved": True,
        "actual_endpoint_h2_convergence_proved": False,
        "rows": rows,
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"regularity_radius": payload["regularity_radius_lower_bound"]}))


if __name__ == "__main__":
    main()
