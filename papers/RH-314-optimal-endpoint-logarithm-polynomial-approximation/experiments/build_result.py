from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from endpoint_approximation import best_log_error, tail_energy_bounds  # noqa: E402


def main() -> None:
    rows = []
    for degree in (8, 32, 128):
        lower, upper = tail_energy_bounds(degree)
        rows.append(
            {
                "degree": degree,
                "best_h2_error": best_log_error(degree),
                "scaled_error": best_log_error(degree) * degree**0.5,
                "energy_lower": lower,
                "energy_upper": upper,
            }
        )
    payload = {
        "status": "rh314_optimal_endpoint_logarithm_polynomial_approximation",
        "taylor_projection_exactly_optimal": True,
        "inverse_square_root_rate_proved": True,
        "spectral_realization_rate_proved": False,
        "rows": rows,
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "optimal": True}))


if __name__ == "__main__":
    main()
