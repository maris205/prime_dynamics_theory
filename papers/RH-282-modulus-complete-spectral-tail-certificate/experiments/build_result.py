from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from spectral_tail import (  # noqa: E402
    block_clock,
    head_rank_bound,
    logarithmic_tail_bound,
    root_rate_limit,
)


def main() -> None:
    rows = []
    for sigma in (1e-2, 1e-3, 1e-4, 1e-6, 1e-8):
        rows.append(
            {
                "sigma": sigma,
                "block_clock": block_clock(sigma),
                "head_rank_upper": head_rank_bound(sigma),
                "log_tail_upper": logarithmic_tail_bound(sigma),
            }
        )
    payload = {
        "status": "rh282_modulus_complete_spectral_tail_certificate",
        "cutoff": 0.5,
        "radius": 1.4,
        "clock_slope": 4.0,
        "root_rate_limit_upper": root_rate_limit(),
        "tail_decay_exponent": 4.0 * __import__("math").log(10.0 / 7.0) - 1.0,
        "rows": rows,
        "uniform_variable_rank_certificate": True,
        "physical_riesz_quotient_certificate": False,
        "counterloop_spectral_identification": False,
        "gate_A": False,
        "gates_B_to_E": False,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "root_rate": root_rate_limit()}))


if __name__ == "__main__":
    main()
