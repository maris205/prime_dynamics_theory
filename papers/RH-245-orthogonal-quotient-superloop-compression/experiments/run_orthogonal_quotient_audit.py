"""Audit ordered-Schur orthogonal quotients on tractable RH-222 endpoints."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
from scipy import linalg
from scipy.optimize import linear_sum_assignment


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
RH236 = PAPERS / "RH-236-cloud-extracted-trace-moment-atlas"
sys.path[:0] = [str(ROOT / "src"), str(RH14 / "src"), str(RH222 / "src")]

from orthogonal_quotient import (  # noqa: E402
    ordered_schur_quotient,
    power_traces,
    selected_quotient_trace_partition,
)
from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from resonance_cloud import HARDY_RADIUS, haar_coarse_embedding  # noqa: E402


MAXIMUM_DIMENSION = 512
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
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    traces = json.loads((RH236 / "results/trace_moment_atlas.json").read_text(encoding="utf-8"))
    residual_rows = {
        (float(row["sigma"]), str(row["side"])): row
        for row in traces["endpoint_rows"]
    }
    eligible = [row for row in atlas["endpoint_rows"] if int(row["dimension"]) <= MAXIMUM_DIMENSION]
    rows = []
    for endpoint in eligible:
        key = (float(endpoint["sigma"]), str(endpoint["side"]))
        operator = endpoint_matrix(endpoint)
        cutoff = float(endpoint["minimum_selected_modulus"]) - 0.5 * float(
            endpoint["radial_gap_after_cloud"]
        )
        decomposition = ordered_schur_quotient(operator, cutoff)
        selected_dimension = int(decomposition["selected_dimension"])
        expected_dimension = int(endpoint["actual_rank"]) + 2
        if selected_dimension != expected_dimension:
            raise RuntimeError(f"ordered Schur rank mismatch at {key}")
        triangular = np.asarray(decomposition["triangular"])
        selected = np.asarray(decomposition["selected_block"])
        cross = np.asarray(decomposition["cross_block"])
        quotient = np.asarray(decomposition["quotient_block"])
        partition = selected_quotient_trace_partition(
            triangular,
            selected_dimension,
            MAXIMUM_ORDER,
        )
        quotient_traces = np.asarray(partition["quotient"])
        archived_residual = values(residual_rows[key]["cloud_extracted_trace_powers"])
        expected_spectrum = np.concatenate((
            np.asarray([scalar(endpoint["perron_scaled"]), scalar(endpoint["parity_scaled"])]),
            values(endpoint["selected_roots"]),
        ))

        quotient_power = np.eye(quotient.shape[0], dtype=complex)
        first_contractive_depth = None
        operator_norms = []
        for order in range(1, MAXIMUM_ORDER + 1):
            quotient_power = quotient_power @ quotient
            norm = float(linalg.svdvals(quotient_power)[0]) if quotient.size else 0.0
            operator_norms.append(norm)
            if first_contractive_depth is None and norm < 1.0:
                first_contractive_depth = order
        trace_norm_order_12 = float(np.sum(linalg.svdvals(quotient_power))) if quotient.size else 0.0
        quotient_frobenius_squared = float(np.linalg.norm(quotient, "fro") ** 2)
        original_budget = float(endpoint["frobenius_tail_budget_after_perron_parity_cloud"])
        rows.append({
            "sigma": key[0],
            "side": key[1],
            "dimension": int(endpoint["dimension"]),
            "selected_dimension": selected_dimension,
            "expected_selected_dimension": expected_dimension,
            "radial_cutoff": cutoff,
            "orthogonal_projection_norm": 1.0,
            "selected_spectral_matching_error": spectral_matching_error(
                np.diag(selected), expected_spectrum
            ),
            "maximum_schur_partition_error_orders_2_to_12": float(
                np.max(np.abs(np.asarray(partition["partition_error"])[1:]))
            ),
            "maximum_archived_residual_error_orders_2_to_12": float(
                np.max(np.abs(quotient_traces[1:] - archived_residual[1:]))
            ),
            "cross_block_frobenius_squared": float(np.linalg.norm(cross, "fro") ** 2),
            "quotient_frobenius_squared": quotient_frobenius_squared,
            "original_frobenius_tail_budget": original_budget,
            "frobenius_budget_improvement_factor": float(original_budget / quotient_frobenius_squared),
            "quotient_operator_norm": operator_norms[0],
            "quotient_power_operator_norms_orders_1_to_12": operator_norms,
            "first_contractive_power_depth": first_contractive_depth,
            "quotient_power_12_operator_norm": operator_norms[-1],
            "quotient_power_12_trace_norm": trace_norm_order_12,
        })

    return {
        "status": "rh245_orthogonal_quotient_superloop_compression",
        "maximum_dimension": MAXIMUM_DIMENSION,
        "maximum_order": MAXIMUM_ORDER,
        "eligible_endpoint_count": len(rows),
        "minimum_selected_dimension": min(row["selected_dimension"] for row in rows),
        "maximum_selected_dimension": max(row["selected_dimension"] for row in rows),
        "rank_mismatch_count": sum(
            row["selected_dimension"] != row["expected_selected_dimension"] for row in rows
        ),
        "maximum_selected_spectral_matching_error": max(
            row["selected_spectral_matching_error"] for row in rows
        ),
        "maximum_schur_partition_error_orders_2_to_12": max(
            row["maximum_schur_partition_error_orders_2_to_12"] for row in rows
        ),
        "maximum_archived_residual_error_orders_2_to_12": max(
            row["maximum_archived_residual_error_orders_2_to_12"] for row in rows
        ),
        "minimum_quotient_frobenius_squared": min(row["quotient_frobenius_squared"] for row in rows),
        "maximum_quotient_frobenius_squared": max(row["quotient_frobenius_squared"] for row in rows),
        "minimum_frobenius_budget_improvement_factor": min(
            row["frobenius_budget_improvement_factor"] for row in rows
        ),
        "maximum_frobenius_budget_improvement_factor": max(
            row["frobenius_budget_improvement_factor"] for row in rows
        ),
        "minimum_quotient_operator_norm": min(row["quotient_operator_norm"] for row in rows),
        "maximum_quotient_operator_norm": max(row["quotient_operator_norm"] for row in rows),
        "one_step_contractive_count": sum(row["quotient_operator_norm"] < 1.0 for row in rows),
        "minimum_first_contractive_power_depth": min(
            row["first_contractive_power_depth"] for row in rows
        ),
        "maximum_first_contractive_power_depth": max(
            row["first_contractive_power_depth"] for row in rows
        ),
        "maximum_quotient_power_12_operator_norm": max(
            row["quotient_power_12_operator_norm"] for row in rows
        ),
        "maximum_quotient_power_12_trace_norm": max(
            row["quotient_power_12_trace_norm"] for row in rows
        ),
        "endpoint_rows": rows,
        "route_coordinate": "orthogonal_quotient_exact_open_uniform_block_power_certificate_and_anchor",
        "theorem_boundary": {
            "orthogonal_quotient_trace_identity_fixed_noise": True,
            "orthogonal_projection_norm_one": True,
            "quotient_kernel_superloop_representation": True,
            "all_archived_endpoints_audited": False,
            "uniform_selected_subspace_stability": False,
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
    output = ROOT / "results/orthogonal_quotient_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "endpoints": payload["eligible_endpoint_count"],
        "rank_mismatches": payload["rank_mismatch_count"],
        "maximum_partition_error": payload["maximum_schur_partition_error_orders_2_to_12"],
        "maximum_archived_error": payload["maximum_archived_residual_error_orders_2_to_12"],
        "first_contractive_depth_range": [
            payload["minimum_first_contractive_power_depth"],
            payload["maximum_first_contractive_power_depth"],
        ],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
