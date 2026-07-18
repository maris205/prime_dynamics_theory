"""Measure the actual floating full-versus-cutoff defect at stored grids."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cutoff_bridge import cutoff_bound, support_half_width  # noqa: E402


U_CRITICAL = 1.5436890126920764


def audit_dimension(
    dimension: int,
    sigma: float,
    multiple: float,
    chunk_rows: int,
) -> dict[str, object]:
    n = int(dimension)
    h = 1.0 / n
    nodes = (np.arange(n, dtype=np.float64) + 0.5) * h
    indices = np.arange(n, dtype=np.int64)[None, :]
    half_width = support_half_width(n, sigma, multiple)
    column_sums = np.zeros(n, dtype=np.float64)
    maximum_omitted = 0.0
    maximum_row_l1 = 0.0
    maximum_tail_identity_error = 0.0
    minimum_omitted_distance = np.inf
    frobenius_square = 0.0
    begun = time.perf_counter()

    for lower in range(0, n, int(chunk_rows)):
        upper = min(n, lower + int(chunk_rows))
        x = nodes[lower:upper]
        means = 1.0 - U_CRITICAL * x * x
        absolute_means = np.abs(means)
        centers = np.floor(absolute_means * n - 0.5).astype(np.int64)
        retained = np.abs(indices - centers[:, None]) <= half_width

        positive_log = -0.5 * ((nodes[None, :] - means[:, None]) / sigma) ** 2
        negative_log = -0.5 * ((-nodes[None, :] - means[:, None]) / sigma) ** 2
        log_weights = np.logaddexp(positive_log, negative_log)
        log_weights -= np.max(log_weights, axis=1, keepdims=True)
        weights = np.exp(log_weights)
        probabilities = weights / np.sum(weights, axis=1, keepdims=True)
        omitted = np.sum(np.where(retained, 0.0, probabilities), axis=1)
        alpha = omitted / (1.0 - omitted)
        absolute_difference = np.where(
            retained,
            probabilities * alpha[:, None],
            probabilities,
        )
        row_l1 = np.sum(absolute_difference, axis=1)

        maximum_omitted = max(maximum_omitted, float(np.max(omitted)))
        maximum_row_l1 = max(maximum_row_l1, float(np.max(row_l1)))
        maximum_tail_identity_error = max(
            maximum_tail_identity_error,
            float(np.max(np.abs(row_l1 - 2.0 * omitted))),
        )
        frobenius_square += float(np.sum(absolute_difference**2))
        column_sums += np.sum(absolute_difference, axis=0)

        omitted_mask = ~retained
        distances = np.abs(nodes[None, :] - absolute_means[:, None])
        if np.any(omitted_mask):
            minimum_omitted_distance = min(
                minimum_omitted_distance,
                float(np.min(distances[omitted_mask])),
            )

    analytic = cutoff_bound(n, sigma, multiple)
    one_norm = float(np.max(column_sums))
    infinity_norm = maximum_row_l1
    schur_upper = float(np.sqrt(one_norm * infinity_norm))
    frobenius = float(np.sqrt(frobenius_square))
    return {
        "dimension": n,
        "mesh": h,
        "support_half_width": half_width,
        "effective_support_multiple": half_width * h / sigma,
        "minimum_omitted_distance": minimum_omitted_distance,
        "minimum_omitted_distance_multiple": minimum_omitted_distance / sigma,
        "maximum_omitted_mass": maximum_omitted,
        "infinity_norm": infinity_norm,
        "one_norm": one_norm,
        "schur_two_norm_upper": schur_upper,
        "frobenius_norm": frobenius,
        "tail_identity_maximum_error": maximum_tail_identity_error,
        "analytic_omitted_mass_upper": analytic.omitted_mass_upper,
        "analytic_two_norm_upper": analytic.two_norm_upper,
        "analytic_over_floating_frobenius": analytic.two_norm_upper / frobenius,
        "seconds": time.perf_counter() - begun,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimensions", type=int, nargs="+", default=[2048, 4096, 8192])
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--multiple", type=float, default=8.0)
    parser.add_argument("--chunk-rows", type=int, default=64)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/cutoff_pilot_sigma_1e-02.json"),
    )
    arguments = parser.parse_args()
    rows = [
        audit_dimension(
            dimension,
            float(arguments.sigma),
            float(arguments.multiple),
            int(arguments.chunk_rows),
        )
        for dimension in arguments.dimensions
    ]
    payload = {
        "status": "floating_full_versus_archived_cutoff_pilot",
        "evidence_level": "floating_not_validated",
        "critical_parameter": U_CRITICAL,
        "sigma": float(arguments.sigma),
        "declared_support_multiple": float(arguments.multiple),
        "dimensions": rows,
    }
    output = arguments.output
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
