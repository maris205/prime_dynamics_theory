"""Extend the ordered-Schur quotient power audit to dimension 1024."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.optimize import linear_sum_assignment


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
RH236 = PAPERS / "RH-236-cloud-extracted-trace-moment-atlas"
RH245 = PAPERS / "RH-245-orthogonal-quotient-superloop-compression"
RH246 = PAPERS / "RH-246-block-power-quotient-envelope-criterion"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH14 / "src"),
    str(RH222 / "src"),
    str(RH245 / "src"),
    str(RH246 / "src"),
]

from block_envelope import geometric_envelope_constant, logarithmic_tail_bound  # noqa: E402
from orthogonal_quotient import ordered_schur_quotient, selected_quotient_trace_partition  # noqa: E402
from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from quotient_stability import block_root_rate, power_norm_profile  # noqa: E402
from resonance_cloud import HARDY_RADIUS, haar_coarse_embedding  # noqa: E402


MAXIMUM_DIMENSION = 1024
MAXIMUM_ORDER = 12


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def scalar(payload: dict[str, float]) -> complex:
    return complex(payload["real"], payload["imag"])


def endpoint_matrix(row: dict[str, object]) -> np.ndarray:
    sigma = float(row["sigma"])
    dimension = int(row["dimension"])
    if row["side"] == "left":
        matrix = sparse_folded_gaussian_matrix(dimension, sigma).tocsr()
    else:
        fine = sparse_folded_gaussian_matrix(2 * dimension, sigma).tocsr()
        embedding = haar_coarse_embedding(2 * dimension)
        matrix = (embedding.T @ fine @ embedding).tocsr()
    return np.asarray(matrix.toarray(), dtype=complex) / HARDY_RADIUS


def spectral_matching_error(computed: np.ndarray, archived: np.ndarray) -> float:
    costs = np.abs(computed[:, None] - archived[None, :])
    rows, columns = linear_sum_assignment(costs)
    return float(np.max(costs[rows, columns], initial=0.0))


def run() -> dict[str, object]:
    started = time.perf_counter()
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text())
    traces = json.loads((RH236 / "results/trace_moment_atlas.json").read_text())
    inherited = json.loads((RH245 / "results/orthogonal_quotient_audit.json").read_text())
    criterion = json.loads((RH246 / "results/block_power_audit.json").read_text())
    inherited_keys = {
        (float(row["sigma"]), str(row["side"])) for row in inherited["endpoint_rows"]
    }
    residual_rows = {
        (float(row["sigma"]), str(row["side"])): row for row in traces["endpoint_rows"]
    }
    eligible = [row for row in atlas["endpoint_rows"] if int(row["dimension"]) <= MAXIMUM_DIMENSION]
    rows = []
    for endpoint in eligible:
        endpoint_started = time.perf_counter()
        key = (float(endpoint["sigma"]), str(endpoint["side"]))
        operator = endpoint_matrix(endpoint)
        cutoff = float(endpoint["minimum_selected_modulus"]) - 0.5 * float(
            endpoint["radial_gap_after_cloud"]
        )
        decomposition = ordered_schur_quotient(operator, cutoff)
        selected_dimension = int(decomposition["selected_dimension"])
        expected_dimension = int(endpoint["actual_rank"]) + 2
        triangular = np.asarray(decomposition["triangular"])
        selected = np.asarray(decomposition["selected_block"])
        quotient = np.asarray(decomposition["quotient_block"])
        partition = selected_quotient_trace_partition(triangular, selected_dimension, MAXIMUM_ORDER)
        quotient_traces = np.asarray(partition["quotient"])
        archived_residual = values(residual_rows[key]["cloud_extracted_trace_powers"])
        expected_spectrum = np.concatenate((
            np.asarray([scalar(endpoint["perron_scaled"]), scalar(endpoint["parity_scaled"])]),
            values(endpoint["selected_roots"]),
        ))
        profile = power_norm_profile(quotient, MAXIMUM_ORDER)
        norms = profile["operator_norms"]
        q12 = block_root_rate(norms[-1], MAXIMUM_ORDER)
        rows.append({
            "sigma": key[0],
            "side": key[1],
            "dimension": int(endpoint["dimension"]),
            "new_beyond_rh245": key not in inherited_keys,
            "selected_dimension": selected_dimension,
            "expected_selected_dimension": expected_dimension,
            "radial_cutoff": cutoff,
            "selected_spectral_matching_error": spectral_matching_error(np.diag(selected), expected_spectrum),
            "maximum_schur_partition_error_orders_2_to_12": float(
                np.max(np.abs(np.asarray(partition["partition_error"])[1:]))
            ),
            "maximum_archived_residual_error_orders_2_to_12": float(
                np.max(np.abs(quotient_traces[1:] - archived_residual[1:]))
            ),
            "quotient_operator_norm": norms[0],
            "quotient_power_operator_norms_orders_1_to_12": norms,
            "first_contractive_power_depth": profile["first_contractive_depth"],
            "quotient_power_12_operator_norm": norms[-1],
            "quotient_power_12_trace_norm": profile["last_trace_norm"],
            "q12": q12,
            "elapsed_seconds": time.perf_counter() - endpoint_started,
        })

    worst = max(rows, key=lambda row: row["q12"])
    new_rows = [row for row in rows if row["new_beyond_rh245"]]
    inherited_q12 = float(criterion["finite_sample_geometric_rate_q12"])
    eta = max(row["quotient_power_12_operator_norm"] for row in rows)
    trace_norm = max(row["quotient_power_12_trace_norm"] for row in rows)
    remainder_norms = [1.0] + [
        max(row["quotient_power_operator_norms_orders_1_to_12"][order - 1] for row in rows)
        for order in range(1, MAXIMUM_ORDER)
    ]
    envelope = geometric_envelope_constant(trace_norm, eta, remainder_norms, MAXIMUM_ORDER)
    tail = logarithmic_tail_bound(trace_norm, eta, remainder_norms, MAXIMUM_ORDER, 1.0)
    return {
        "status": "rh259_extended_quotient_block_power_diagnostic",
        "maximum_dimension": MAXIMUM_DIMENSION,
        "maximum_order": MAXIMUM_ORDER,
        "eligible_endpoint_count": len(rows),
        "inherited_endpoint_count": len(rows) - len(new_rows),
        "new_endpoint_count": len(new_rows),
        "rank_mismatch_count": sum(
            row["selected_dimension"] != row["expected_selected_dimension"] for row in rows
        ),
        "maximum_selected_spectral_matching_error": max(row["selected_spectral_matching_error"] for row in rows),
        "maximum_schur_partition_error_orders_2_to_12": max(
            row["maximum_schur_partition_error_orders_2_to_12"] for row in rows
        ),
        "maximum_archived_residual_error_orders_2_to_12": max(
            row["maximum_archived_residual_error_orders_2_to_12"] for row in rows
        ),
        "one_step_contractive_count": sum(row["quotient_operator_norm"] < 1.0 for row in rows),
        "power_12_contractive_count": sum(row["quotient_power_12_operator_norm"] < 1.0 for row in rows),
        "minimum_first_contractive_power_depth": min(row["first_contractive_power_depth"] for row in rows),
        "maximum_first_contractive_power_depth": max(row["first_contractive_power_depth"] for row in rows),
        "minimum_q12": min(row["q12"] for row in rows),
        "maximum_q12": worst["q12"],
        "maximum_q12_endpoint": {"sigma": worst["sigma"], "side": worst["side"], "dimension": worst["dimension"]},
        "maximum_new_q12": max(row["q12"] for row in new_rows),
        "inherited_rh246_q12": inherited_q12,
        "q12_deterioration_factor": worst["q12"] / inherited_q12,
        "maximum_quotient_power_12_operator_norm": max(row["quotient_power_12_operator_norm"] for row in rows),
        "maximum_quotient_power_12_trace_norm": max(row["quotient_power_12_trace_norm"] for row in rows),
        "finite_sample_remainder_operator_norm_bounds_orders_0_to_11": remainder_norms,
        "finite_sample_geometric_constant_M12": envelope["M"],
        "finite_sample_unit_disk_logarithmic_tail_bound_from_order_12": tail,
        "endpoint_rows": rows,
        "elapsed_seconds": time.perf_counter() - started,
        "route_coordinate": "dimension1024_quotient_power12_subunit_but_deteriorating_open_uniform_small_noise_theorem",
        "theorem_boundary": {
            "orthogonal_quotient_trace_identity_fixed_noise": True,
            "finite_dimension_1024_diagnostic": True,
            "all_eligible_power_12_blocks_contractive": True,
            "uniform_small_noise_block_power": False,
            "all_archived_endpoints_audited": False,
            "uniform_all_order_trace_envelope": False,
            "current_cloud_coefficient_bridge": False,
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
    output = ROOT / "results/extended_quotient_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "endpoints": payload["eligible_endpoint_count"],
        "new_endpoints": payload["new_endpoint_count"],
        "rank_mismatches": payload["rank_mismatch_count"],
        "q12_range": [payload["minimum_q12"], payload["maximum_q12"]],
        "q12_deterioration_factor": payload["q12_deterioration_factor"],
        "first_contractive_depth_range": [payload["minimum_first_contractive_power_depth"], payload["maximum_first_contractive_power_depth"]],
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
