from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from moment_no_go import shell_factor, shell_moment  # noqa: E402


def main() -> None:
    rows = []
    for order in (5, 8, 13, 21):
        radius = 0.7
        prefix_error = max(abs(shell_moment(order, radius, power)) for power in range(1, order))
        hidden = shell_moment(order, radius, order)
        z = 0.8 + 0.1j
        factor_error = abs(shell_factor(order, radius, z) - (1.0 - (radius * z) ** order))
        rows.append(
            {
                "shell_order": order,
                "maximum_prefix_roundoff": prefix_error,
                "hidden_moment_real": hidden.real,
                "hidden_moment_imag": hidden.imag,
                "factorization_roundoff": factor_error,
            }
        )
    payload = {
        "status": "rh289_finite_moment_shell_nonidentifiability",
        "rows": rows,
        "finite_prefix_identifies_cloud": False,
        "weighted_or_contour_routes_excluded": False,
        "scoped_negative_result": True,
        "gate_A": False,
        "gates_B_to_E": False,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "scoped": True}))


if __name__ == "__main__":
    main()
