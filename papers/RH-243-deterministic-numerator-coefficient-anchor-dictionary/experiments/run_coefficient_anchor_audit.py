"""Build the deterministic numerator target and compare the archived finite jets."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH11 = PAPERS / "RH-11-collet-eckmann-flat-trace-completion"
RH236 = PAPERS / "RH-236-cloud-extracted-trace-moment-atlas"
sys.path[:0] = [str(ROOT / "src"), str(RH11 / "src")]

from coefficient_anchor import (  # noqa: E402
    HARDY_RADIUS,
    anchored_jet_distance,
    exponential_coefficients_from_trace,
    one_step_anchor_array,
    trace_log_jet,
    two_step_anchor_from_one_step,
)
from flat_trace_completion import LAMBDA_FIXED, flat_periodic_trace  # noqa: E402


MAXIMUM_ORDER = 12


def complex_values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def run() -> dict[str, object]:
    orders = np.arange(2, MAXIMUM_ORDER + 1)
    flat = np.asarray([flat_periodic_trace(int(order)) for order in orders])
    anchors = one_step_anchor_array(flat, 2, LAMBDA_FIXED)
    centered = flat - 1.0 - (-1.0) ** orders
    corrections = np.where(orders % 2 == 0, 2.0 * LAMBDA_FIXED ** (-orders / 2.0), 0.0)
    unscaled = centered + corrections
    two_orders, two_anchors = two_step_anchor_from_one_step(orders, anchors)

    coefficient_array = np.zeros(MAXIMUM_ORDER + 1, dtype=complex)
    coefficient_array[orders] = anchors
    numerator_taylor = exponential_coefficients_from_trace(
        coefficient_array, MAXIMUM_ORDER
    )

    z = 0.23 + 0.07j
    one_step_symmetric = trace_log_jet(orders, anchors, z) + trace_log_jet(
        orders, anchors, -z
    )
    two_step = trace_log_jet(two_orders, two_anchors, z * z)

    atlas = json.loads(
        (RH236 / "results/trace_moment_atlas.json").read_text(encoding="utf-8")
    )
    target_full = np.zeros(MAXIMUM_ORDER, dtype=complex)
    target_full[1:] = anchors
    endpoint_rows = []
    for row in atlas["endpoint_rows"]:
        residual = complex_values(row["cloud_extracted_trace_powers"])
        distance = anchored_jet_distance(residual, target_full)
        endpoint_rows.append({
            "sigma": row["sigma"],
            "side": row["side"],
            "cloud_rank": row["cloud_rank"],
            "anchored_unit_disk_log_jet_distance_orders_2_to_12": distance,
            "zero_target_unit_disk_log_jet_norm_orders_2_to_12": row[
                "unit_disk_log_jet_norm_orders_2_to_12"
            ],
        })

    coefficient_rows = []
    for index, order in enumerate(orders):
        coefficient_rows.append({
            "one_step_order": int(order),
            "flat_periodic_trace": float(flat[index]),
            "parity_centered_trace": float(centered[index]),
            "pole_correction": float(corrections[index]),
            "unscaled_one_step_numerator_trace_coefficient": float(unscaled[index]),
            "hardy_scaled_one_step_anchor": float(anchors[index]),
            "ordinary_numerator_taylor_coefficient": {
                "real": float(numerator_taylor[order].real),
                "imag": float(numerator_taylor[order].imag),
            },
            "two_step_order_if_even": int(order // 2) if order % 2 == 0 else None,
        })

    return {
        "status": "rh243_deterministic_numerator_coefficient_anchor_dictionary",
        "route_coordinate": "deterministic_anchor_target_defined_open_cloud_bridge_and_envelope",
        "maximum_one_step_order": MAXIMUM_ORDER,
        "determinant_lambda": LAMBDA_FIXED,
        "hardy_radius": HARDY_RADIUS,
        "one_step_anchor_formula": (
            "a_n=r_H^(-n)[P_n-1-(-1)^n+2*1_(2|n)*lambda^(-n/2)]"
        ),
        "two_step_anchor_formula": "b_k=a_(2k)",
        "coefficient_rows": coefficient_rows,
        "two_step_orders": [int(value) for value in two_orders],
        "two_step_hardy_scaled_anchors": [float(value.real) for value in two_anchors],
        "one_step_target_unit_disk_log_jet_norm_orders_2_to_12": float(
            np.sum(np.abs(anchors) / orders)
        ),
        "symmetric_jet_identity_error": float(abs(one_step_symmetric - two_step)),
        "endpoint_count": len(endpoint_rows),
        "minimum_archived_anchored_jet_distance": min(
            row["anchored_unit_disk_log_jet_distance_orders_2_to_12"]
            for row in endpoint_rows
        ),
        "maximum_archived_anchored_jet_distance": max(
            row["anchored_unit_disk_log_jet_distance_orders_2_to_12"]
            for row in endpoint_rows
        ),
        "minimum_archived_zero_target_jet_norm": min(
            row["zero_target_unit_disk_log_jet_norm_orders_2_to_12"]
            for row in endpoint_rows
        ),
        "endpoint_rows": endpoint_rows,
        "theorem_boundary": {
            "deterministic_one_step_trace_style_anchor_target_defined": True,
            "hardy_scaling_conversion_exact": True,
            "symmetric_two_step_anchor_equals_even_one_step_subsequence": True,
            "two_step_anchor_identifies_odd_one_step_coefficients": False,
            "ordinary_taylor_coefficients_distinguished_from_trace_coefficients": True,
            "current_cloud_coefficient_bridge": False,
            "uniform_all_order_trace_envelope": False,
            "hilbert_polya_operator": False,
            "zeta_divisor_identification": False,
            "riemann_hypothesis_implication": False,
            "gate_A": False,
            "gate_B": False,
            "gate_C": False,
            "gate_D": False,
            "gate_E": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/coefficient_anchor_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "target_jet_norm": payload[
            "one_step_target_unit_disk_log_jet_norm_orders_2_to_12"
        ],
        "minimum_archived_anchor_distance": payload[
            "minimum_archived_anchored_jet_distance"
        ],
        "symmetric_identity_error": payload["symmetric_jet_identity_error"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
