from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from parity_hardy import singular_coefficient, split_energy  # noqa: E402


def main() -> None:
    coefficients = [0.0] + [singular_coefficient(n) for n in range(1, 17)]
    even, odd, total = split_energy(coefficients)
    payload = {
        "status": "rh313_parity_orthogonal_endpoint_hardy_splitting",
        "orthogonal_parity_split_proved": True,
        "endpoint_convergence_equivalence_proved": True,
        "actual_endpoint_h2_convergence_proved": False,
        "finite_energy": {"even": even, "odd": odd, "total": total},
        "gates": {key: False for key in "ABCDE"},
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload["finite_energy"], sort_keys=True))


if __name__ == "__main__":
    main()
