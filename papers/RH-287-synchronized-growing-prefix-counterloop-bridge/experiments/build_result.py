from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from prefix_bridge import admissible_level, prefix_weight_upper  # noqa: E402


def main() -> None:
    rows = []
    for sigma in (1e-1, 1e-2, 1e-3, 1e-4, 1e-6):
        errors = [sigma * order**2 for order in range(2, 80)]
        level = admissible_level(errors)
        maximum = max(errors[: max(level - 1, 0)], default=0.0)
        rows.append(
            {
                "sigma": sigma,
                "synthetic_admissible_level": level,
                "unweighted_maximum": maximum,
                "radius_1_4_weight_upper": (
                    prefix_weight_upper(maximum, level, 1.4) if level >= 2 else 0.0
                ),
            }
        )
    payload = {
        "status": "rh287_synchronized_growing_prefix_counterloop_bridge",
        "rows": rows,
        "growing_prefix_exists": True,
        "explicit_noise_rate": False,
        "weighted_radius_prefix_proved": False,
        "noisy_spectral_identification": False,
        "gate_A": False,
        "gates_B_to_E": False,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "last_level": rows[-1]["synthetic_admissible_level"]}))


if __name__ == "__main__":
    main()
