"""Construct floating biorthogonal cloud projectors at all RH-222 endpoints."""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigs


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
sys.path[:0] = [str(ROOT / "src"), str(RH14 / "src"), str(RH222 / "src")]

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from resonance_cloud import deterministic_start  # noqa: E402
from riesz_cloud import (  # noqa: E402
    biorthogonal_projector_metrics,
    commutator_frobenius_norm,
    eigenpair_residuals,
    match_eigenvalues,
)


def complex_values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def scalar_complex(payload: dict[str, float]) -> complex:
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
        data = np.full(fine_dimension, 1.0 / math.sqrt(2.0))
        embedding = sparse.coo_matrix(
            (data, (rows, columns)), shape=(fine_dimension, dimension)
        ).tocsr()
        matrix = (embedding.T @ fine @ embedding).tocsr()
    return matrix / float(endpoint["hardy_radius"])


def endpoint_targets(endpoint: dict[str, object]) -> np.ndarray:
    return np.concatenate((
        np.asarray([
            scalar_complex(endpoint["perron_scaled"]),
            scalar_complex(endpoint["parity_scaled"]),
        ]),
        complex_values(endpoint["selected_roots"]),
    ))


def audit_endpoint(endpoint: dict[str, object]) -> dict[str, object]:
    matrix = endpoint_matrix(endpoint)
    targets = endpoint_targets(endpoint)
    dimension = matrix.shape[0]
    count = min(targets.size, dimension - 2)
    if count != targets.size:
        raise RuntimeError("the endpoint is too small for its cloud")
    ncv = min(dimension, max(2 * count + 1, 48))
    start = deterministic_start(dimension)
    right_values, right_vectors = eigs(
        matrix,
        k=count,
        which="LM",
        tol=3.0e-11,
        maxiter=max(20000, 40 * dimension),
        ncv=ncv,
        v0=start,
    )
    left_values, left_vectors = eigs(
        matrix.T,
        k=count,
        which="LM",
        tol=3.0e-11,
        maxiter=max(20000, 40 * dimension),
        ncv=ncv,
        v0=start,
    )
    right_indices, right_match = match_eigenvalues(right_values, targets)
    left_indices, left_match = match_eigenvalues(
        left_values, targets, conjugate_targets=True
    )
    right = right_vectors[:, right_indices]
    left = left_vectors[:, left_indices]
    matched_right_values = right_values[right_indices]
    matched_left_values = left_values[left_indices]
    metrics = biorthogonal_projector_metrics(right, left)
    right_residuals = eigenpair_residuals(matrix, right, matched_right_values)
    left_residuals = eigenpair_residuals(matrix.T, left, matched_left_values)
    commutator = commutator_frobenius_norm(
        matrix, right, left, metrics["inverse_overlap"]
    )
    return {
        "sigma": endpoint["sigma"],
        "side": endpoint["side"],
        "dimension": dimension,
        "cloud_rank": endpoint["actual_rank"],
        "projector_rank_with_peripheral_modes": int(targets.size),
        "radial_gap_after_cloud": endpoint["radial_gap_after_cloud"],
        "maximum_right_target_match_error": right_match,
        "maximum_left_target_match_error": left_match,
        "maximum_right_eigenpair_residual": float(np.max(right_residuals)),
        "maximum_left_eigenpair_residual": float(np.max(left_residuals)),
        "minimum_overlap_singular_value": metrics["minimum_overlap_singular_value"],
        "overlap_condition_number": metrics["overlap_condition_number"],
        "projector_operator_norm": metrics["projector_operator_norm"],
        "projector_frobenius_norm": metrics["projector_frobenius_norm"],
        "commutator_frobenius_norm": commutator,
        "gap_to_projector_norm_ratio": float(
            endpoint["radial_gap_after_cloud"] / metrics["projector_operator_norm"]
        ),
    }


def run() -> dict[str, object]:
    started = time.perf_counter()
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    rows = []
    for endpoint in atlas["endpoint_rows"]:
        row = audit_endpoint(endpoint)
        rows.append(row)
        print(json.dumps({
            "sigma": row["sigma"],
            "side": row["side"],
            "rank": row["projector_rank_with_peripheral_modes"],
            "projector_norm": row["projector_operator_norm"],
        }, sort_keys=True), flush=True)
    norms = np.asarray([row["projector_operator_norm"] for row in rows])
    return {
        "status": "rh232_biorthogonal_riesz_cloud_projection",
        "endpoint_count": len(rows),
        "minimum_projector_operator_norm": float(np.min(norms)),
        "maximum_projector_operator_norm": float(np.max(norms)),
        "maximum_overlap_condition_number": max(
            row["overlap_condition_number"] for row in rows
        ),
        "minimum_overlap_singular_value": min(
            row["minimum_overlap_singular_value"] for row in rows
        ),
        "maximum_right_eigenpair_residual": max(
            row["maximum_right_eigenpair_residual"] for row in rows
        ),
        "maximum_left_eigenpair_residual": max(
            row["maximum_left_eigenpair_residual"] for row in rows
        ),
        "maximum_commutator_frobenius_norm": max(
            row["commutator_frobenius_norm"] for row in rows
        ),
        "minimum_gap_to_projector_norm_ratio": min(
            row["gap_to_projector_norm_ratio"] for row in rows
        ),
        "projector_norm_above_million_count": int(np.sum(norms > 1.0e6)),
        "endpoint_rows": rows,
        "elapsed_seconds": time.perf_counter() - started,
        "theorem_boundary": {
            "finite_biorthogonal_projector_formula": True,
            "all_endpoint_projector_candidates_constructed": True,
            "uniform_projector_bound_supported": False,
            "interval_riesz_projection_certified": False,
            "uniform_complement_ideal_bound": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/riesz_projection_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "endpoint_count": payload["endpoint_count"],
        "projector_norm_range": [
            payload["minimum_projector_operator_norm"],
            payload["maximum_projector_operator_norm"],
        ],
        "above_million": payload["projector_norm_above_million_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
