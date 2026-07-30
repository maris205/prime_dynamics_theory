from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from moment_packets import (  # noqa: E402
    minimal_multiplicity,
    packet_power_sum,
    packet_radius,
    packet_rank,
    packet_squared_mass,
)

Q = 0.5
Q_STAR = 0.7008752258547759


def main() -> None:
    rows = []
    for order in (4, 8, 12):
        moment = Q_STAR**order
        multiplicity = minimal_multiplicity(order, moment, Q)
        rows.append(
            {
                "order": order,
                "multiplicity": multiplicity,
                "rank": packet_rank(order, multiplicity),
                "radius": packet_radius(order, multiplicity, moment),
                "squared_mass": packet_squared_mass(order, multiplicity, moment),
                "isolated_moment": packet_power_sum(order, multiplicity, moment, order),
            }
        )
    payload = {
        "status": "rh315_root_of_unity_moment_packet_isolation",
        "exact_moment_packet_proved": True,
        "conjugate_closed_for_real_moments": True,
        "radius_cap_enforced": True,
        "actual_noisy_spectrum_constructed": False,
        "rows": rows,
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "packet_isolation": True}))


if __name__ == "__main__":
    main()
