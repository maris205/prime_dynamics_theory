"""Audit exact finite-history cocycle and adjoint identities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path[:0] = [str(ROOT / "src"), str(PAPERS / "RH-172-canonical-polar-reset-memory-realization" / "src")]

from history_cocycle import (  # noqa: E402
    apply_history_cocycle,
    apply_history_cocycle_adjoint,
    cocycle_extreme_singular_values,
    history_cocycle_matrix,
    normalization_ratio,
)
from history_realization import memory_gram, normalized_history_factor, polar_realization, subspace_distance, top_packet  # noqa: E402


def run(smoke: bool) -> dict[str, object]:
    rng = np.random.default_rng(173)
    dimensions = (3,) if smoke else (2, 3, 5, 8)
    blocks = (1, 2) if smoke else (1, 2, 4, 7)
    trials = 2 if smoke else 10
    records = []
    for dimension in dimensions:
        for input_blocks in blocks:
            for trial in range(trials):
                operator = rng.normal(size=(dimension, dimension)) / np.sqrt(dimension)
                ratio = float(rng.uniform(0.4, 1.8))
                values = rng.normal(size=(input_blocks * dimension, 3))
                target = rng.normal(size=((input_blocks + 1) * dimension, 3))
                matrix = history_cocycle_matrix(operator, input_blocks, ratio)
                applied = apply_history_cocycle(values, operator, ratio)
                adjoint = apply_history_cocycle_adjoint(target, operator, ratio)
                largest, smallest = cocycle_extreme_singular_values(operator, input_blocks, ratio)
                singular = np.linalg.svd(matrix, compute_uv=False)
                records.append({
                    "dimension": dimension,
                    "input_blocks": input_blocks,
                    "trial": trial,
                    "matrix_action_residual": float(np.linalg.norm(matrix @ values - applied, 2)),
                    "adjoint_action_residual": float(np.linalg.norm(matrix.T @ target - adjoint, 2)),
                    "largest_singular_formula_residual": abs(float(singular[0]) - largest),
                    "smallest_singular_formula_residual": abs(float(singular[-1]) - smallest),
                })

    epsilon = 1e-3
    source = np.diag([1.0, epsilon])
    operator = np.diag([epsilon, 1.0 / epsilon])
    states = [source, operator @ source]
    factor0 = normalized_history_factor(states[:1])
    factor1 = normalized_history_factor(states)
    _, packet0 = top_packet(memory_gram(states[:1]), 1)
    _, packet1 = top_packet(memory_gram(states), 1)
    realized0, _ = polar_realization(factor0, packet0)
    realized1, _ = polar_realization(factor1, packet1)
    ratio = normalization_ratio(states[0], states[1])
    transported = apply_history_cocycle(realized0, operator, ratio)
    transported, _ = polar_realization(transported, np.eye(1))
    counterexample_distance = subspace_distance(transported, realized1)

    metrics = tuple(key for key in records[0] if key.endswith("residual"))
    return {
        "status": "rh173_normalized_history_cocycle_audit",
        "case_count": len(records),
        "maximum_residuals": {metric: max(record[metric] for record in records) for metric in metrics},
        "orthogonal_reset_counterexample_distance": counterexample_distance,
        "records": records,
        "theorem_boundary": {
            "exact_rectangular_history_cocycle": True,
            "exact_adjoint_and_singular_value_formula": True,
            "gram_optimality_implies_cocycle_invariance": False,
            "physical_transfer_intertwining": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "cocycle_identity_smoke.json" if args.smoke else "cocycle_identity_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "case_count": payload["case_count"], "counterexample_distance": payload["orthogonal_reset_counterexample_distance"], **payload["maximum_residuals"]}, sort_keys=True))


if __name__ == "__main__":
    main()
