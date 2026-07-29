"""Enumerate deterministic numerator anchors through order twenty-eight."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH11 = PAPERS / "RH-11-collet-eckmann-flat-trace-completion"
sys.path[:0] = [str(ROOT / "src"), str(RH11 / "src")]

from anchor_atlas import (  # noqa: E402
    finite_logarithmic_norm,
    hardy_scaled_anchor,
    log_linear_root_rate,
    ordinary_coefficients_from_traces,
)
from flat_trace_completion import LAMBDA_FIXED, flat_periodic_trace  # noqa: E402
from flat_trace_completion.periodic import physical_fixed_point_count  # noqa: E402


HARDY_RADIUS = 0.85
MINIMUM_ORDER = 2
PREVIOUS_MAXIMUM_ORDER = 12
MAXIMUM_ORDER = 28


def run() -> dict[str, object]:
    orders = np.arange(MINIMUM_ORDER, MAXIMUM_ORDER + 1)
    flat = np.asarray([flat_periodic_trace(int(order)) for order in orders])
    anchors = np.asarray([
        hardy_scaled_anchor(value, int(order), LAMBDA_FIXED, HARDY_RADIUS)
        for order, value in zip(orders, flat)
    ])
    unscaled = anchors * HARDY_RADIUS**orders

    trace_array = np.zeros(MAXIMUM_ORDER + 1, dtype=float)
    trace_array[orders] = anchors
    ordinary = ordinary_coefficients_from_traces(trace_array)

    rows = []
    for order, flat_value, raw, anchor in zip(orders, flat, unscaled, anchors):
        rows.append({
            "order": int(order),
            "flat_periodic_trace": float(flat_value),
            "unscaled_numerator_trace_coefficient": float(raw),
            "hardy_scaled_anchor": float(anchor),
            "ordinary_numerator_taylor_coefficient": {
                "real": float(ordinary[int(order)].real),
                "imag": float(ordinary[int(order)].imag),
            },
            "physical_fixed_point_count": physical_fixed_point_count(int(order)),
        })

    old = orders <= PREVIOUS_MAXIMUM_ORDER
    new = orders > PREVIOUS_MAXIMUM_ORDER
    odd_new = new & (orders % 2 == 1)
    even_new = new & (orders % 2 == 0)
    return {
        "status": "rh253_extended_deterministic_anchor_atlas",
        "minimum_order": MINIMUM_ORDER,
        "previous_maximum_order": PREVIOUS_MAXIMUM_ORDER,
        "maximum_order": MAXIMUM_ORDER,
        "new_order_count": int(np.sum(new)),
        "hardy_radius": HARDY_RADIUS,
        "determinant_lambda": LAMBDA_FIXED,
        "physical_fixed_point_count_at_order_28": physical_fixed_point_count(28),
        "order_2_to_12_unit_disk_log_norm": finite_logarithmic_norm(orders[old], anchors[old]),
        "order_13_to_28_unit_disk_log_norm": finite_logarithmic_norm(orders[new], anchors[new]),
        "order_2_to_28_unit_disk_log_norm": finite_logarithmic_norm(orders, anchors),
        "order_13_to_28_radius_08_log_norm": finite_logarithmic_norm(
            orders[new], anchors[new], 0.8
        ),
        "new_odd_log_linear_root_rate": log_linear_root_rate(orders[odd_new], anchors[odd_new]),
        "new_even_log_linear_root_rate": log_linear_root_rate(orders[even_new], anchors[even_new]),
        "new_all_log_linear_root_rate": log_linear_root_rate(orders[new], anchors[new]),
        "maximum_new_anchor": float(np.max(np.abs(anchors[new]))),
        "minimum_new_anchor": float(np.min(np.abs(anchors[new]))),
        "coefficient_rows": rows,
        "route_coordinate": "analytic_target_tail_with_order_28_anchor_atlas_open_cloud_bridge",
        "theorem_boundary": {
            "orders_13_to_28_finite_atlas": True,
            "exact_coefficient_dictionary_used": True,
            "finite_root_rate_is_all_order_theorem": False,
            "analytic_all_order_tail_inherited_from_rh252": True,
            "current_cloud_coefficient_bridge": False,
            "uniform_all_order_trace_envelope": False,
            "gate_A": False,
            "gate_B": False,
            "gate_C": False,
            "gate_D": False,
            "gate_E": False,
            "hilbert_polya_operator": False,
            "zeta_divisor_identification": False,
            "riemann_hypothesis_implication": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/extended_anchor_atlas.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "new_log_norm": payload["order_13_to_28_unit_disk_log_norm"],
        "new_root_rate": payload["new_all_log_linear_root_rate"],
        "fixed_points_order_28": payload["physical_fixed_point_count_at_order_28"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
