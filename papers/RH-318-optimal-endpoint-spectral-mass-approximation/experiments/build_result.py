from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from spectral_approximation import (  # noqa: E402
    BASE,
    LOG_BASE,
    SQRT_LOG_BASE,
    asymptotic_endpoint_energy,
    asymptotic_endpoint_norm,
    logarithmic_degree_clock,
)


def main() -> None:
    rows = [
        {
            "mass": mass,
            "degree_clock": logarithmic_degree_clock(mass),
            "asymptotic_energy": asymptotic_endpoint_energy(mass),
            "asymptotic_norm": asymptotic_endpoint_norm(mass),
        }
        for mass in (1e4, 1e8, 1e16)
    ]
    payload = {
        "status": "rh318_optimal_endpoint_spectral_mass_approximation",
        "mass_growth_base": BASE,
        "sharp_energy_constant": LOG_BASE,
        "sharp_norm_constant": SQRT_LOG_BASE,
        "optimal_genuine_spectral_mass_law_proved": True,
        "actual_endpoint_h2_convergence_proved": False,
        "rows": rows,
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"energy_constant": LOG_BASE, "norm_constant": SQRT_LOG_BASE}))


if __name__ == "__main__":
    main()
