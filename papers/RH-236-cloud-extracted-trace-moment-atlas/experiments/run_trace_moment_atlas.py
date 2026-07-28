"""Compute orders one through twelve for every RH-222 endpoint."""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy import sparse


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
sys.path[:0] = [str(ROOT / "src"), str(RH14 / "src")]

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from trace_atlas import (  # noqa: E402
    complex_payload,
    extracted_trace_moments,
    sparse_power_traces,
    weighted_jet_norm,
)


MAXIMUM_ORDER = 12
FINE_SIGMA_THRESHOLD = 0.005


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def scalar(payload: dict[str, float]) -> complex:
    return complex(payload["real"], payload["imag"])


def endpoint_matrix(endpoint: dict[str, object]):
    dimension = int(endpoint["dimension"])
    sigma = float(endpoint["sigma"])
    if endpoint["side"] == "left":
        matrix = sparse_folded_gaussian_matrix(dimension, sigma).tocsr()
    else:
        fine_dimension = 2 * dimension
        fine = sparse_folded_gaussian_matrix(fine_dimension, sigma).tocsr()
        rows = np.arange(fine_dimension)
        columns = np.repeat(np.arange(dimension), 2)
        embedding = sparse.coo_matrix(
            (np.full(fine_dimension, 1.0 / math.sqrt(2.0)), (rows, columns)),
            shape=(fine_dimension, dimension),
        ).tocsr()
        matrix = (embedding.T @ fine @ embedding).tocsr()
    return matrix / float(endpoint["hardy_radius"])


def run() -> dict[str, object]:
    started = time.perf_counter()
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    rows = []
    for endpoint in atlas["endpoint_rows"]:
        full = sparse_power_traces(endpoint_matrix(endpoint), MAXIMUM_ORDER)
        residual = extracted_trace_moments(
            full,
            scalar(endpoint["perron_scaled"]),
            scalar(endpoint["parity_scaled"]),
            values(endpoint["selected_roots"]),
        )
        moduli = np.abs(residual)
        orders = np.arange(1, MAXIMUM_ORDER + 1)
        root_rates = moduli ** (1.0 / orders)
        row = {
            "sigma": endpoint["sigma"],
            "side": endpoint["side"],
            "dimension": endpoint["dimension"],
            "cloud_rank": endpoint["actual_rank"],
            "full_trace_powers": complex_payload(full),
            "cloud_extracted_trace_powers": complex_payload(residual),
            "cloud_extracted_trace_moduli": [float(value) for value in moduli],
            "cloud_extracted_root_rates": [float(value) for value in root_rates],
            "unit_disk_log_jet_norm_orders_2_to_12": weighted_jet_norm(residual),
            "maximum_root_rate_orders_2_to_12": float(np.max(root_rates[1:])),
        }
        rows.append(row)
        print(json.dumps({
            "sigma": row["sigma"],
            "side": row["side"],
            "jet_norm": row["unit_disk_log_jet_norm_orders_2_to_12"],
        }, sort_keys=True), flush=True)
    order_rows = []
    for order in range(1, MAXIMUM_ORDER + 1):
        all_values = [row["cloud_extracted_trace_moduli"][order - 1] for row in rows]
        fine_values = [
            row["cloud_extracted_trace_moduli"][order - 1]
            for row in rows if float(row["sigma"]) <= FINE_SIGMA_THRESHOLD
        ]
        order_rows.append({
            "order": order,
            "maximum_all_endpoint_modulus": max(all_values),
            "maximum_fine_endpoint_modulus": max(fine_values),
            "all_endpoint_root_rate": max(all_values) ** (1.0 / order),
            "fine_endpoint_root_rate": max(fine_values) ** (1.0 / order),
        })
    return {
        "status": "rh236_cloud_extracted_trace_moment_atlas",
        "maximum_order": MAXIMUM_ORDER,
        "fine_sigma_threshold": FINE_SIGMA_THRESHOLD,
        "endpoint_count": len(rows),
        "trace_case_count": len(rows) * MAXIMUM_ORDER,
        "maximum_unit_disk_log_jet_norm": max(
            row["unit_disk_log_jet_norm_orders_2_to_12"] for row in rows
        ),
        "maximum_fine_unit_disk_log_jet_norm": max(
            row["unit_disk_log_jet_norm_orders_2_to_12"]
            for row in rows if float(row["sigma"]) <= FINE_SIGMA_THRESHOLD
        ),
        "maximum_observed_root_rate_orders_2_to_12": max(
            row["maximum_root_rate_orders_2_to_12"] for row in rows
        ),
        "order_rows": order_rows,
        "endpoint_rows": rows,
        "elapsed_seconds": time.perf_counter() - started,
        "theorem_boundary": {
            "finite_sparse_trace_powers_exact_for_archived_matrices": True,
            "cloud_extracted_orders_two_to_twelve_audited": True,
            "finite_trace_jet_is_small_at_fine_scales": True,
            "uniform_all_order_trace_envelope": False,
            "locally_uniform_relative_det2": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/trace_moment_atlas.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "trace_cases": payload["trace_case_count"],
        "maximum_jet_norm": payload["maximum_unit_disk_log_jet_norm"],
        "maximum_fine_jet_norm": payload["maximum_fine_unit_disk_log_jet_norm"],
        "maximum_root_rate": payload["maximum_observed_root_rate_orders_2_to_12"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
