from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from mass_demand import (  # noqa: E402
    mass_exponent,
    mass_ratio,
    mass_saturation_slope,
    minimal_slope,
    necessary_mass,
)


def main() -> None:
    payload = {
        "status": "rh304_minimal_clock_complement_mass_demand",
        "mass_ratio": mass_ratio(),
        "minimal_bridge_slope": minimal_slope(),
        "minimal_clock_mass_exponent": mass_exponent(),
        "mass_exponent_slack": 1.0 - mass_exponent(),
        "mass_saturation_slope": mass_saturation_slope(),
        "single_order_mass_lower_bound_proved": True,
        "minimal_clock_relative_matching_proved": False,
        "gates": {key: False for key in "ABCDE"},
        "sample_odd_order_bounds": {
            str(order): necessary_mass(order) for order in (9, 19, 39)
        },
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"mass_exponent": mass_exponent()}))


if __name__ == "__main__":
    main()
