"""Audit the separate-absolute majorant on the 352 RH-236 trace cases."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
RH236 = PAPERS / "RH-236-cloud-extracted-trace-moment-atlas"
sys.path.insert(0, str(ROOT / "src"))

from absolute_majorant import cancellation_gain, root_rates, separate_absolute_majorant  # noqa: E402


HARDY_RADIUS = 0.85


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def scalar(payload: dict[str, float]) -> complex:
    return complex(payload["real"], payload["imag"])


def run() -> dict[str, object]:
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    traces = json.loads((RH236 / "results/trace_moment_atlas.json").read_text(encoding="utf-8"))
    atlas_rows = {
        (float(row["sigma"]), str(row["side"])): row
        for row in atlas["endpoint_rows"]
    }
    rows = []
    root_rate_values = []
    gain_values = []
    order_rows = []
    for trace_row in traces["endpoint_rows"]:
        key = (float(trace_row["sigma"]), str(trace_row["side"]))
        endpoint = atlas_rows[key]
        full = values(trace_row["full_trace_powers"])
        residual = values(trace_row["cloud_extracted_trace_powers"])
        majorant = separate_absolute_majorant(
            full,
            scalar(endpoint["perron_scaled"]),
            scalar(endpoint["parity_scaled"]),
            values(endpoint["selected_roots"]),
        )
        rates = root_rates(majorant)
        gains = cancellation_gain(majorant, residual)
        relevant_gains = gains[1:]
        root_rate_values.extend(rates.tolist())
        gain_values.extend(relevant_gains.tolist())
        for order, (upper, target, rate, gain) in enumerate(
            zip(majorant[1:], residual[1:], rates, relevant_gains), start=2
        ):
            order_rows.append({
                "sigma": key[0],
                "side": key[1],
                "order": order,
                "majorant": float(upper),
                "residual_modulus": float(abs(target)),
                "root_rate": float(rate),
                "majorant_over_residual": float(gain),
            })
        rows.append({
            "sigma": key[0],
            "side": key[1],
            "maximum_root_rate_orders_2_to_12": float(np.max(rates)),
            "minimum_root_rate_orders_2_to_12": float(np.min(rates)),
            "minimum_majorant_over_residual_orders_2_to_12": float(np.min(relevant_gains)),
            "maximum_majorant_over_residual_orders_2_to_12": float(np.max(relevant_gains)),
        })

    lower_rate = 1.0 / HARDY_RADIUS
    return {
        "status": "rh247_separate_absolute_majorant_barrier",
        "hardy_radius": HARDY_RADIUS,
        "theoretical_perron_root_rate_lower_bound": lower_rate,
        "endpoint_count": len(rows),
        "case_count": len(order_rows),
        "minimum_case_root_rate": min(root_rate_values),
        "maximum_case_root_rate": max(root_rate_values),
        "case_root_rates_above_one_count": sum(value > 1.0 for value in root_rate_values),
        "case_root_rates_at_least_perron_rate_count": sum(value >= lower_rate - 1e-12 for value in root_rate_values),
        "minimum_case_majorant_over_residual": min(gain_values),
        "maximum_case_majorant_over_residual": max(gain_values),
        "maximum_gain_location": max(order_rows, key=lambda row: row["majorant_over_residual"]),
        "endpoint_rows": rows,
        "order_rows": order_rows,
        "route_coordinate": "cancellation_blind_absolute_majorant_ruled_out_open_grouped_signed_envelope_and_anchor",
        "theorem_boundary": {
            "separate_absolute_majorant_root_rate_lower_bound": True,
            "all_archived_order_cases_exceed_one": all(value > 1.0 for value in root_rate_values),
            "absolute_majorant_can_prove_subunit_envelope": False,
            "signed_or_grouped_quotient_route_excluded": False,
            "uniform_all_order_trace_envelope": False,
            "deterministic_numerator_identification": False,
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
    output = ROOT / "results/absolute_majorant_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "cases": payload["case_count"],
        "root_rate_range": [payload["minimum_case_root_rate"], payload["maximum_case_root_rate"]],
        "gain_range": [payload["minimum_case_majorant_over_residual"], payload["maximum_case_majorant_over_residual"]],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
