from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from endpoint_obstruction import (  # noqa: E402
    endpoint_packet_coefficient,
    escaping_multiplicity,
    higher_endpoint_packet_coefficient,
    packet_mass_upper,
    packet_squared_mass,
    strict_radius_packet_coefficient,
)


def main() -> None:
    rows = []
    for order in (8, 16, 32):
        multiplicity = escaping_multiplicity(order)
        rows.append(
            {
                "order": order,
                "multiplicity": multiplicity,
                "endpoint_coefficient": endpoint_packet_coefficient(order, multiplicity),
                "second_endpoint_coefficient": higher_endpoint_packet_coefficient(order, 2, multiplicity),
                "strict_1p41_coefficient": strict_radius_packet_coefficient(order, 1.41),
                "squared_mass": packet_squared_mass(order, multiplicity),
                "mass_upper": packet_mass_upper(order, multiplicity),
            }
        )
    payload = {
        "status": "rh320_escaping_packet_endpoint_energy_obstruction",
        "escaping_spectral_packet_counterexample_proved": True,
        "strict_annulus_convergence_with_endpoint_failure_proved": True,
        "endpoint_energy_tightness_criterion_proved": True,
        "actual_endpoint_nonconvergence_proved": False,
        "rows": rows,
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "escaping_packet": True}))


if __name__ == "__main__":
    main()
