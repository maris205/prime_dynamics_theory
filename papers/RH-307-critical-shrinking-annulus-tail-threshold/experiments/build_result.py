from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from shrinking_annulus import (  # noqa: E402
    critical_gap_constant,
    critical_tail_scale,
    logarithmic_gap,
    minimal_slope,
    radius_is_certified,
    shrinking_radius,
)


def main() -> None:
    critical = critical_gap_constant()
    sigma = 1e-80
    rows = []
    for coefficient in (0.5 * critical, critical, 1.5 * critical):
        rows.append(
            {
                "coefficient": coefficient,
                "sigma": sigma,
                "eta": logarithmic_gap(sigma, coefficient),
                "rho": shrinking_radius(sigma, coefficient),
                "radius_is_certified": radius_is_certified(sigma, coefficient),
                "tail_scale": critical_tail_scale(sigma, coefficient),
            }
        )
    payload = {
        "status": "rh307_critical_shrinking_annulus_tail_threshold",
        "minimal_slope": minimal_slope(),
        "critical_gap_constant": critical,
        "mass_and_cap_information_class_threshold_proved": True,
        "repeated_q_model_saturation_proved": True,
        "actual_moving_head_control_proved": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"critical_gap_constant": critical}))


if __name__ == "__main__":
    main()
