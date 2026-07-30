from __future__ import annotations

import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from hardy_conversion import (  # noqa: E402
    cauchy_constant,
    hardy_constant,
    rudin_shapiro_block_lower,
    shrinking_hardy_scale,
)


def main() -> None:
    rows = []
    for eta in (1e-1, 1e-2, 1e-3):
        length = 2 ** math.floor(math.log2(1.0 / eta))
        rows.append(
            {
                "eta": eta,
                "rudin_shapiro_length": length,
                "hardy_constant": shrinking_hardy_scale(eta),
                "rudin_shapiro_order_lower": rudin_shapiro_block_lower(
                    eta, length
                ),
            }
        )
    payload = {
        "status": "rh308_hardy_dominant_annular_coefficient_conversion",
        "rho_1p41_cauchy_constant": cauchy_constant(1.4, 1.41),
        "rho_1p41_hardy_constant": hardy_constant(1.4, 1.41),
        "hinfinity_improved_by_hardy_embedding": True,
        "hinfinity_unit_ball_square_root_gap_order_sharp": True,
        "actual_norm_decay_proved": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"hardy_constant": hardy_constant(1.4, 1.41)}))


if __name__ == "__main__":
    main()
