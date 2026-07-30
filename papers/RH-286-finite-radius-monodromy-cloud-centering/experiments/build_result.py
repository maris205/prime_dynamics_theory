from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))
from finite_radius import audit_cloud, moment_bias_constant, root_l1_bias_limit  # noqa: E402
from finite_radius.core import BETA  # noqa: E402


def main() -> None:
    cloud = PAPERS / "RH-15-parity-extracted-bulk-scattering/results/outer_resonance_cloud.csv"
    radii = PAPERS / "RH-17-time-ordered-boundary-monodromy/results/boundary_cycle_monodromy.csv"
    rows = audit_cloud(cloud, radii)
    multiplier_constant = 1.9463429052009678
    payload = {
        "status": "rh286_finite_radius_monodromy_cloud_centering",
        "row_count": len(rows),
        "rows": rows,
        "limiting_total_root_error_range": [
            min(row["limiting_total_root_error"] for row in rows),
            max(row["limiting_total_root_error"] for row in rows),
        ],
        "finite_total_root_error_range": [
            min(row["finite_total_root_error"] for row in rows),
            max(row["finite_total_root_error"] for row in rows),
        ],
        "limiting_maximum_moment_error_range": [
            min(row["limiting_maximum_moment_error"] for row in rows),
            max(row["limiting_maximum_moment_error"] for row in rows),
        ],
        "finite_maximum_moment_error_range": [
            min(row["finite_maximum_moment_error"] for row in rows),
            max(row["finite_maximum_moment_error"] for row in rows),
        ],
        "all_rows_root_error_improved": all(
            row["finite_total_root_error"] < row["limiting_total_root_error"]
            for row in rows
        ),
        "multiplier_constant_diagnostic": multiplier_constant,
        "root_l1_bias_limit_diagnostic": root_l1_bias_limit(BETA, multiplier_constant),
        "second_moment_bias_constant_diagnostic": moment_bias_constant(
            2, BETA, multiplier_constant
        ),
        "multiplier_constant_interval_certified": False,
        "aggregate_cloud_transport_proved": False,
        "gate_A": False,
        "gates_B_to_E": False,
    }
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": len(rows), "all_improved": payload["all_rows_root_error_improved"]}))


if __name__ == "__main__":
    main()
