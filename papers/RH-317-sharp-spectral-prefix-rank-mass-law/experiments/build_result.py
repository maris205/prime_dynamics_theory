from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from rank_mass import (  # noqa: E402
    BASE,
    LOG_BASE,
    mass_lower_bound,
    normalized_divisor_feedback,
    rank_lower_bound,
)

Q_STAR = 0.7008752258547759


def main() -> None:
    rows = []
    for order in (8, 16, 32):
        model_anchor = Q_STAR**order
        rows.append(
            {
                "order": order,
                "rank_lower": rank_lower_bound(order, model_anchor),
                "mass_lower": mass_lower_bound(order, model_anchor),
                "normalized_divisor_feedback": normalized_divisor_feedback(order),
            }
        )
    payload = {
        "status": "rh317_sharp_spectral_prefix_rank_mass_law",
        "growth_base": BASE,
        "log_growth_base": LOG_BASE,
        "minimal_rank_theta_law_proved": True,
        "minimal_squared_mass_theta_law_proved": True,
        "actual_noisy_rank_law_proved": False,
        "rows": rows,
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"base": BASE, "log_base": LOG_BASE}))


if __name__ == "__main__":
    main()
