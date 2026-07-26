"""Audit orientation separation and perturbative marked-trace stability."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from directed_cycle_marks import (  # noqa: E402
    cycle_matrix,
    edge_marker,
    marked_power_stability_bound,
    ordinary_cycle_trace,
    reduced_marked_trace,
    zero_mean_projection,
)


def normalized_random_matrix(rng: np.random.Generator, size: int, norm: float) -> np.ndarray:
    raw = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    return raw * (float(norm) / np.linalg.norm(raw, 2))


def run(smoke: bool) -> dict[str, object]:
    rng = np.random.default_rng(178)
    lengths = (3, 5) if smoke else (3, 4, 5, 7, 11, 16, 24, 32, 48, 64)
    trials = 2 if smoke else 12
    exact_records = []
    stability_records = []
    for length in lengths:
        forward_mark = reduced_marked_trace(length, 1, 1)
        reverse_mark = reduced_marked_trace(length, 1, -1)
        exact_records.append({
            "length": length,
            "forward_reduced_mark_real": forward_mark.real,
            "reverse_reduced_mark_real": reverse_mark.real,
            "orientation_gap": abs(forward_mark - reverse_mark),
            "ordinary_trace_difference_power_one": abs(ordinary_cycle_trace(length, 1, 1) - ordinary_cycle_trace(length, 1, -1)),
            "ordinary_trace_difference_power_length_minus_one": abs(ordinary_cycle_trace(length, length - 1, 1) - ordinary_cycle_trace(length, length - 1, -1)),
        })

        projection = zero_mean_projection(length)
        marker = projection @ edge_marker(length) @ projection
        marker_trace_norm = float(np.sum(np.linalg.svd(marker, compute_uv=False)))
        cycle = cycle_matrix(length, 1)
        for trial in range(trials):
            perturbation_norm = 0.01 + 0.01 * (trial % 3)
            perturbation = normalized_random_matrix(rng, length, perturbation_norm)
            perturbed = cycle + perturbation
            power = 1 + trial % min(5, length - 1)
            observed_error = abs(np.trace(marker @ np.linalg.matrix_power(perturbed, power)) - np.trace(marker @ np.linalg.matrix_power(cycle, power)))
            common_bound = max(float(np.linalg.norm(cycle, 2)), float(np.linalg.norm(perturbed, 2)))
            bound = marked_power_stability_bound(marker_trace_norm, power, common_bound, perturbation_norm)
            stability_records.append({
                "length": length,
                "trial": trial,
                "power": power,
                "observed_error": float(observed_error),
                "stability_bound": bound,
                "bound_dominates": bool(observed_error <= bound * (1.0 + 1e-12) + 1e-14),
            })
    return {
        "status": "rh178_orientation_marked_cycle_trace_audit",
        "exact_case_count": len(exact_records),
        "stability_case_count": len(stability_records),
        "minimum_exact_orientation_gap": min(record["orientation_gap"] for record in exact_records),
        "maximum_ordinary_trace_difference": max(max(record["ordinary_trace_difference_power_one"], record["ordinary_trace_difference_power_length_minus_one"]) for record in exact_records),
        "stability_failure_count": sum(not record["bound_dominates"] for record in stability_records),
        "maximum_bound_ratio": max(record["observed_error"] / record["stability_bound"] for record in stability_records),
        "exact_records": exact_records,
        "stability_records": stability_records,
        "theorem_boundary": {
            "scalar_determinant_orientation_blind": True,
            "rank_one_reduced_marker_separates_orientation": True,
            "marked_word_perturbation_bound": True,
            "physical_directed_trace_limit": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "orientation_mark_smoke.json" if args.smoke else "orientation_mark_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "stability_cases": payload["stability_case_count"], "failures": payload["stability_failure_count"], "minimum_orientation_gap": payload["minimum_exact_orientation_gap"]}, sort_keys=True))


if __name__ == "__main__":
    main()
