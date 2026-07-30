from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from block_clock import critical_slope, decay_exponent, root_rate_limit, saturation_lower  # noqa: E402


def main() -> None:
    alpha, cutoff, radius = 1.0, 0.5, 1.4
    critical = critical_slope(alpha, cutoff, radius)
    slopes = (2.0, critical, 4.0)
    rows = [
        {
            "slope": slope,
            "decay_exponent": decay_exponent(alpha, slope, cutoff, radius),
            "root_rate_limit": root_rate_limit(alpha, slope, cutoff, radius),
            "saturation_lower_sigma_1e_8": saturation_lower(
                1e-8, alpha, slope, cutoff, radius
            ),
        }
        for slope in slopes
    ]
    payload = {
        "status": "rh283_sharp_logarithmic_spectral_block_clock",
        "alpha": alpha,
        "cutoff": cutoff,
        "radius": radius,
        "critical_slope": critical,
        "rows": rows,
        "sharp_for_mass_cap_class": True,
        "physical_saturation_claimed": False,
        "gate_A": False,
        "gates_B_to_E": False,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"critical_slope": critical, "rows": len(rows)}))


if __name__ == "__main__":
    main()
