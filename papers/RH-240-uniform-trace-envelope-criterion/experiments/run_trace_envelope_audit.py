"""Measure the observed order-2--12 envelope and expose the missing tail."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH236 = PAPERS / "RH-236-cloud-extracted-trace-moment-atlas"
sys.path.insert(0, str(ROOT / "src"))

from trace_envelope import (  # noqa: E402
    finite_log_majorant,
    geometric_log_bound,
    observed_unit_amplitude_rate,
)


def run() -> dict[str, object]:
    source = json.loads((RH236 / "results/trace_moment_atlas.json").read_text(encoding="utf-8"))
    order_rows = [row for row in source["order_rows"] if row["order"] >= 2]
    orders = np.asarray([row["order"] for row in order_rows])
    global_moments = np.asarray([row["maximum_all_endpoint_modulus"] for row in order_rows])
    fine_moments = np.asarray([row["maximum_fine_endpoint_modulus"] for row in order_rows])
    global_rate = observed_unit_amplitude_rate(orders, global_moments)
    fine_rate = observed_unit_amplitude_rate(orders, fine_moments)
    return {
        "status": "rh240_uniform_trace_envelope_criterion",
        "first_observed_order": int(orders[0]),
        "last_observed_order": int(orders[-1]),
        "observed_order_count": int(orders.size),
        "global_observed_unit_amplitude_rate": global_rate,
        "fine_observed_unit_amplitude_rate": fine_rate,
        "global_finite_unit_disk_log_majorant": finite_log_majorant(orders, global_moments),
        "fine_finite_unit_disk_log_majorant": finite_log_majorant(orders, fine_moments),
        "conditional_global_all_order_unit_disk_bound": geometric_log_bound(1.0, global_rate, 1.0),
        "conditional_fine_all_order_unit_disk_bound": geometric_log_bound(1.0, fine_rate, 1.0),
        "order_rows": order_rows,
        "theorem_boundary": {
            "all_order_geometric_trace_envelope_implies_normal_relative_det2": True,
            "orders_two_to_twelve_fit_a_subunit_unit_amplitude_envelope": global_rate < 1.0,
            "order_thirteen_and_above_controlled": False,
            "conditional_bound_is_an_unconditional_determinant_bound": False,
            "uniform_relative_det2_family": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/trace_envelope_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "observed_orders": payload["observed_order_count"],
        "global_rate": payload["global_observed_unit_amplitude_rate"],
        "fine_rate": payload["fine_observed_unit_amplitude_rate"],
        "missing_tail_starts_at": payload["last_observed_order"] + 1,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
