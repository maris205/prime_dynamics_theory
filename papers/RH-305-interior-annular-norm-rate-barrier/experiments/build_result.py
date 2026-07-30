from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from annular_rate import (  # noqa: E402
    coefficient_norm_lower_bound,
    forced_odd_order,
    rate_ceiling,
)


def main() -> None:
    rows = []
    for rho in (1.405, 1.41, 1.42):
        rows.append(
            {
                "rho": rho,
                "power_rate_ceiling": rate_ceiling(rho),
                "forced_odd_order_at_mass_1e12": forced_odd_order(1e12),
                "certified_norm_lower_at_mass_1e12": coefficient_norm_lower_bound(
                    1e12, rho
                ),
            }
        )
    payload = {
        "status": "rh305_interior_annular_norm_rate_barrier",
        "mass_to_norm_lower_bound_proved": True,
        "lower_bound_scope": "modulus-cap trace powers versus the exact odd anchor",
        "rate_variable": "complement_hilbert_schmidt_mass",
        "hinfinity_mass_power_rate_above_ceiling_excluded": True,
        "h2_mass_power_rate_above_ceiling_excluded": True,
        "actual_annular_convergence_excluded": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "rho_1p41_ceiling": rate_ceiling(1.41),
                "mass_1e12_forced_order": forced_odd_order(1e12),
            }
        )
    )


if __name__ == "__main__":
    main()
