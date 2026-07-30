from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from spectral_saturation import annular_kappa, annular_mass_scale  # noqa: E402


def main() -> None:
    rows = [
        {
            "radius": radius,
            "kappa": annular_kappa(radius),
            "scale_at_mass_1e12": annular_mass_scale(1e12, radius),
        }
        for radius in (1.401, 1.41, 1.42)
    ]
    payload = {
        "status": "rh319_genuine_spectral_annular_envelope_saturation",
        "genuine_spectral_saturation_proved": True,
        "coefficient_envelope_only": False,
        "actual_noisy_rate_sharpness_proved": False,
        "rows": rows,
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "genuine_spectral": True}))


if __name__ == "__main__":
    main()
