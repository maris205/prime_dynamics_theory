"""Optimize anchored reachability over prefixes, subsets, and the shell box."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
RH236 = PAPERS / "RH-236-cloud-extracted-trace-moment-atlas"
RH243 = PAPERS / "RH-243-deterministic-numerator-coefficient-anchor-dictionary"
sys.path[:0] = [str(ROOT / "src"), str(RH222 / "src")]

from resonance_cloud import conjugate_shells  # noqa: E402
from shell_zonotope import (  # noqa: E402
    binary_subset_count,
    solve_binary_selection,
    solve_box_zonotope,
    weighted_distance,
)


MINIMUM_RANK = 4
ORDERS = np.arange(2, 13)


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def scalar(payload: dict[str, float]) -> complex:
    return complex(payload["real"], payload["imag"])


def shell_power_matrix(shells: list[np.ndarray]) -> np.ndarray:
    return np.column_stack([
        [np.sum(np.asarray(shell, dtype=complex) ** order) for order in ORDERS]
        for shell in shells
    ])


def discrete_scans(
    difference: np.ndarray,
    matrix: np.ndarray,
    shell_sizes: np.ndarray,
) -> dict[str, object]:
    prefix_rows = []
    interval_rows = []
    for stop in range(1, shell_sizes.size + 1):
        rank = int(np.sum(shell_sizes[:stop]))
        if rank >= MINIMUM_RANK:
            weights = np.zeros(shell_sizes.size)
            weights[:stop] = 1.0
            prefix_rows.append((weighted_distance(difference - matrix @ weights, ORDERS), rank, stop))
    for start in range(shell_sizes.size):
        for stop in range(start + 1, shell_sizes.size + 1):
            rank = int(np.sum(shell_sizes[start:stop]))
            if rank >= MINIMUM_RANK:
                weights = np.zeros(shell_sizes.size)
                weights[start:stop] = 1.0
                interval_rows.append((
                    weighted_distance(difference - matrix @ weights, ORDERS),
                    rank,
                    start,
                    stop,
                ))
    return {
        "prefix_rows": prefix_rows,
        "interval_rows": interval_rows,
        "best_prefix": min(prefix_rows),
        "best_interval": min(interval_rows),
    }


def single_coefficient_certificate(difference: np.ndarray, matrix: np.ndarray) -> tuple[float, int]:
    lower = np.sum(np.minimum(matrix, 0.0), axis=1)
    upper = np.sum(np.maximum(matrix, 0.0), axis=1)
    gaps = np.maximum(lower - difference, 0.0) + np.maximum(difference - upper, 0.0)
    weighted = gaps / ORDERS
    index = int(np.argmax(weighted))
    return float(weighted[index]), int(ORDERS[index])


def run() -> dict[str, object]:
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    traces = json.loads((RH236 / "results/trace_moment_atlas.json").read_text(encoding="utf-8"))
    anchor = json.loads((RH243 / "results/coefficient_anchor_audit.json").read_text(encoding="utf-8"))
    target = np.asarray([
        row["hardy_scaled_one_step_anchor"] for row in anchor["coefficient_rows"]
    ])
    trace_rows = {
        (float(row["sigma"]), str(row["side"])): row
        for row in traces["endpoint_rows"]
    }

    rows = []
    maximum_imaginary_leakage = 0.0
    for endpoint in atlas["endpoint_rows"]:
        sigma = float(endpoint["sigma"])
        side = str(endpoint["side"])
        trace_row = trace_rows[(sigma, side)]
        full = values(trace_row["full_trace_powers"])[1:]
        perron = scalar(endpoint["perron_scaled"])
        parity = scalar(endpoint["parity_scaled"])
        base = full - perron**ORDERS - parity**ORDERS
        shells = conjugate_shells(values(endpoint["candidate_roots"]))
        complex_matrix = shell_power_matrix(shells)
        maximum_imaginary_leakage = max(
            maximum_imaginary_leakage,
            float(np.max(np.abs(base.imag))),
            float(np.max(np.abs(complex_matrix.imag))),
        )
        difference = np.asarray((base - target).real, dtype=float)
        matrix = np.asarray(complex_matrix.real, dtype=float)
        shell_sizes = np.asarray([np.asarray(shell).size for shell in shells], dtype=int)
        discrete = discrete_scans(difference, matrix, shell_sizes)
        binary = solve_binary_selection(difference, matrix, ORDERS)
        box = solve_box_zonotope(difference, matrix, ORDERS)
        binary_weights = np.asarray(binary["weights"])
        box_weights = np.asarray(box["weights"])
        single_value, single_order = single_coefficient_certificate(difference, matrix)
        best_prefix = discrete["best_prefix"]
        best_interval = discrete["best_interval"]
        rows.append({
            "sigma": sigma,
            "side": side,
            "shell_count": int(shell_sizes.size),
            "candidate_rank": int(np.sum(shell_sizes)),
            "eligible_prefix_count": len(discrete["prefix_rows"]),
            "eligible_contiguous_interval_count": len(discrete["interval_rows"]),
            "eligible_binary_subset_count": binary_subset_count(shell_sizes, MINIMUM_RANK),
            "best_prefix_distance": float(best_prefix[0]),
            "best_prefix_rank": int(best_prefix[1]),
            "best_contiguous_interval_distance": float(best_interval[0]),
            "best_contiguous_interval_rank": int(best_interval[1]),
            "best_contiguous_interval_start_shell": int(best_interval[2]),
            "best_binary_subset_distance": float(binary["distance"]),
            "best_binary_subset_rank": int(round(float(shell_sizes @ np.rint(binary_weights)))),
            "binary_mip_gap": float(binary["mip_gap"]),
            "best_box_distance": float(box["distance"]),
            "box_effective_rank": float(shell_sizes @ box_weights),
            "box_primal_dual_gap": float(box["primal_dual_gap"]),
            "box_distance_over_tolerance": float(box["distance"] / sigma),
            "box_failure_margin": float(box["distance"] - sigma),
            "single_coefficient_lower_certificate": single_value,
            "single_coefficient_certificate_order": single_order,
            "single_coefficient_certificate_exceeds_tolerance": single_value > sigma,
        })

    certificate_orders = Counter(
        row["single_coefficient_certificate_order"]
        for row in rows if row["single_coefficient_certificate_exceeds_tolerance"]
    )
    return {
        "status": "rh248_anchored_shell_zonotope_reachability_obstruction",
        "endpoint_count": len(rows),
        "orders": ORDERS.tolist(),
        "minimum_rank": MINIMUM_RANK,
        "maximum_imaginary_leakage_before_real_lp": maximum_imaginary_leakage,
        "total_eligible_prefix_count": sum(row["eligible_prefix_count"] for row in rows),
        "total_eligible_contiguous_interval_count": sum(
            row["eligible_contiguous_interval_count"] for row in rows
        ),
        "total_eligible_binary_subset_count": sum(
            row["eligible_binary_subset_count"] for row in rows
        ),
        "prefix_pass_count": sum(row["best_prefix_distance"] <= row["sigma"] for row in rows),
        "contiguous_interval_pass_count": sum(
            row["best_contiguous_interval_distance"] <= row["sigma"] for row in rows
        ),
        "binary_subset_pass_count": sum(
            row["best_binary_subset_distance"] <= row["sigma"] for row in rows
        ),
        "box_zonotope_pass_count": sum(row["best_box_distance"] <= row["sigma"] for row in rows),
        "all_best_contiguous_intervals_are_prefixes": all(
            row["best_contiguous_interval_start_shell"] == 0 for row in rows
        ),
        "minimum_binary_subset_distance": min(row["best_binary_subset_distance"] for row in rows),
        "maximum_binary_subset_distance": max(row["best_binary_subset_distance"] for row in rows),
        "minimum_box_distance": min(row["best_box_distance"] for row in rows),
        "maximum_box_distance": max(row["best_box_distance"] for row in rows),
        "minimum_box_failure_margin": min(row["box_failure_margin"] for row in rows),
        "minimum_box_distance_over_tolerance": min(row["box_distance_over_tolerance"] for row in rows),
        "maximum_box_distance_over_tolerance": max(row["box_distance_over_tolerance"] for row in rows),
        "maximum_box_primal_dual_gap": max(abs(row["box_primal_dual_gap"]) for row in rows),
        "maximum_binary_mip_gap": max(row["binary_mip_gap"] for row in rows),
        "minimum_box_effective_rank": min(row["box_effective_rank"] for row in rows),
        "maximum_box_effective_rank": max(row["box_effective_rank"] for row in rows),
        "single_coefficient_certificate_count": sum(
            row["single_coefficient_certificate_exceeds_tolerance"] for row in rows
        ),
        "single_coefficient_certificate_order_histogram": {
            str(order): count for order, count in sorted(certificate_orders.items())
        },
        "endpoint_rows": rows,
        "route_coordinate": "anchored_shell_zonotope_unreachable_open_expanded_window_or_signed_grouping",
        "theorem_boundary": {
            "box_zonotope_primal_dual_certificate": True,
            "all_frozen_shell_subsets_excluded_at_archived_tolerance": True,
            "expanded_candidate_windows_excluded": False,
            "unbounded_shell_multiplicities_excluded": False,
            "signed_or_complex_grouping_excluded": False,
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
    output = ROOT / "results/zonotope_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "passes": {
            "prefix": payload["prefix_pass_count"],
            "interval": payload["contiguous_interval_pass_count"],
            "binary": payload["binary_subset_pass_count"],
            "box": payload["box_zonotope_pass_count"],
        },
        "box_distance_range": [payload["minimum_box_distance"], payload["maximum_box_distance"]],
        "maximum_primal_dual_gap": payload["maximum_box_primal_dual_gap"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
