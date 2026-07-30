from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from annular_reduction import annular_exponents, tail_bounds  # noqa: E402


def main() -> None:
    rows = []
    for rho in (1.405, 1.41, 1.42):
        noisy_exp, target_exp = annular_exponents(rho)
        noisy_inf, target_inf = tail_bounds(1e-8, rho)
        noisy_h2, target_h2 = tail_bounds(1e-8, rho, hardy=True)
        rows.append(
            {
                "rho": rho,
                "noisy_power_exponent": noisy_exp,
                "target_power_exponent": target_exp,
                "hinfinity_tail_upper": noisy_inf + target_inf,
                "h2_tail_upper": noisy_h2 + target_h2,
            }
        )
    payload = {
        "status": "rh302_annular_tail_moving_head_reduction",
        "slope_four_annular_tail_proved": True,
        "full_norm_equivalent_to_moving_head": True,
        "actual_moving_head_convergence": False,
        "actual_annular_convergence": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "tail_reduction": True}))


if __name__ == "__main__":
    main()
