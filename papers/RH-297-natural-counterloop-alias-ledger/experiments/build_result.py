from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from alias_ledger import (  # noqa: E402
    alias_count,
    alias_growth_exponent,
    alias_order_slope,
    alias_weight,
    beta_limit,
    minimal_bridge_slope,
)


def main() -> None:
    payload = {
        "status": "rh297_natural_counterloop_alias_ledger",
        "beta": beta_limit(),
        "beta_times_radius": beta_limit() * 1.4,
        "alias_slopes": [alias_order_slope(index) for index in (1, 2, 3)],
        "minimal_bridge_slope": minimal_bridge_slope(),
        "slope_four": 4.0,
        "aliases_below_minimal_bridge": alias_count(minimal_bridge_slope()),
        "aliases_below_slope_four": alias_count(4.0),
        "alias_growth_exponents": [
            alias_growth_exponent(index) for index in (1, 2)
        ],
        "sample_weights": [
            {
                "period": period,
                "first_alias": alias_weight(period, 1),
                "second_alias": alias_weight(period, 2),
            }
            for period in (4, 8, 12, 16)
        ],
        "natural_rank_equals_noisy_head_proved": False,
        "actual_alias_cancellation_proved": False,
        "typed_errors_diverge_proved": False,
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "minimal_aliases": payload["aliases_below_minimal_bridge"],
                "slope_four_aliases": payload["aliases_below_slope_four"],
            }
        )
    )


if __name__ == "__main__":
    main()
