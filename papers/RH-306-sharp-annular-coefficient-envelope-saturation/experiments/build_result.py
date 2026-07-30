from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from envelope_saturation import (  # noqa: E402
    envelope_mass,
    model_hardy_tail_bounds,
    model_sup_tail_bounds,
    saturation_identity_ratio,
)


def main() -> None:
    rows = []
    for order in (20, 40, 80):
        sup_lower, sup_upper = model_sup_tail_bounds(order, 1.41)
        h2_lower, h2_upper = model_hardy_tail_bounds(order, 1.41)
        rows.append(
            {
                "order": order,
                "coefficient_envelope_mass": envelope_mass(order),
                "infinite_model_hinfinity_lower": sup_lower,
                "infinite_model_hinfinity_upper": sup_upper,
                "infinite_model_h2_lower": h2_lower,
                "infinite_model_h2_upper": h2_upper,
                "saturation_identity_ratio": saturation_identity_ratio(order),
            }
        )
    payload = {
        "status": "rh306_sharp_annular_coefficient_envelope_saturation",
        "truncated_target_coefficient_family_constructed": True,
        "coefficient_envelope_information_class_power_exponent_sharp": True,
        "coefficient_envelope_information_class_logarithmic_factor_sharp": True,
        "actual_noisy_complement_function_realization": False,
        "spectral_power_sum_realization": False,
        "actual_annular_convergence_rate_sharp": False,
        "actual_annular_convergence_proved": False,
        "gates": {key: False for key in "ABCDE"},
        "rows": rows,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "rows": len(rows),
                "coefficient_envelope_information_class_sharp": True,
            }
        )
    )


if __name__ == "__main__":
    main()
