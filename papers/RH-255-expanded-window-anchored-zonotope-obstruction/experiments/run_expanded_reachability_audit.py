"""Audit the deterministic anchor over the expanded shell zonotope."""

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
RH248 = PAPERS / "RH-248-anchored-shell-zonotope-reachability-obstruction"
RH254 = PAPERS / "RH-254-expanded-resolved-candidate-window-atlas"
sys.path[:0] = [str(ROOT / "src"), str(RH222 / "src"), str(RH248 / "src")]

from expanded_reachability import (  # noqa: E402
    best_prefix_distance,
    shell_power_matrix,
    single_coefficient_box_gap,
)
from resonance_cloud import conjugate_shells  # noqa: E402
from shell_zonotope import binary_subset_count, solve_box_zonotope  # noqa: E402


MINIMUM_RANK = 4
ORDERS = np.arange(2, 13)


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def scalar(payload: dict[str, float]) -> complex:
    return complex(payload["real"], payload["imag"])


def run() -> dict[str, object]:
    expanded = json.loads((RH254 / "results/expanded_window_atlas.json").read_text())
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text())
    traces = json.loads((RH236 / "results/trace_moment_atlas.json").read_text())
    anchor = json.loads((RH243 / "results/coefficient_anchor_audit.json").read_text())
    frozen = json.loads((RH248 / "results/zonotope_audit.json").read_text())
    target = np.asarray([row["hardy_scaled_one_step_anchor"] for row in anchor["coefficient_rows"]])
    reference = {(float(row["sigma"]), str(row["side"])): row for row in atlas["endpoint_rows"]}
    trace_rows = {(float(row["sigma"]), str(row["side"])): row for row in traces["endpoint_rows"]}
    frozen_rows = {(float(row["sigma"]), str(row["side"])): row for row in frozen["endpoint_rows"]}

    rows = []
    maximum_imaginary_leakage = 0.0
    for endpoint in expanded["endpoint_rows"]:
        key = (float(endpoint["sigma"]), str(endpoint["side"]))
        old = reference[key]
        trace = trace_rows[key]
        full = values(trace["full_trace_powers"])[1:]
        base = full - scalar(old["perron_scaled"]) ** ORDERS - scalar(old["parity_scaled"]) ** ORDERS
        shells = conjugate_shells(values(endpoint["expanded_candidate_roots"]))
        complex_matrix = shell_power_matrix(shells, ORDERS)
        maximum_imaginary_leakage = max(
            maximum_imaginary_leakage,
            float(np.max(np.abs(base.imag))),
            float(np.max(np.abs(complex_matrix.imag))),
        )
        difference = np.asarray((base - target).real, dtype=float)
        matrix = np.asarray(complex_matrix.real, dtype=float)
        shell_sizes = np.asarray([np.asarray(shell).size for shell in shells], dtype=int)
        prefix = best_prefix_distance(difference, matrix, ORDERS, shell_sizes, MINIMUM_RANK)
        box = solve_box_zonotope(difference, matrix, ORDERS)
        weights = np.asarray(box["weights"])
        coordinate = single_coefficient_box_gap(difference, matrix, ORDERS)
        old_distance = float(frozen_rows[key]["best_box_distance"])
        rows.append({
            "sigma": key[0],
            "side": key[1],
            "shell_count": len(shells),
            "complete_candidate_rank": int(np.sum(shell_sizes)),
            "eligible_prefix_count": int(np.sum(np.cumsum(shell_sizes) >= MINIMUM_RANK)),
            "eligible_binary_subset_count": binary_subset_count(shell_sizes, MINIMUM_RANK),
            "best_prefix_distance": float(prefix["distance"]),
            "best_prefix_rank": int(prefix["rank"]),
            "best_box_distance": float(box["distance"]),
            "box_effective_rank": float(shell_sizes @ weights),
            "box_primal_dual_gap": float(box["primal_dual_gap"]),
            "box_distance_over_tolerance": float(box["distance"] / key[0]),
            "box_failure_margin": float(box["distance"] - key[0]),
            "frozen_box_distance": old_distance,
            "expanded_distance_improvement": float(old_distance - box["distance"]),
            "single_coefficient_weighted_gap": coordinate["weighted_gap"],
            "single_coefficient_gap_order": coordinate["order"],
            "single_coefficient_gap_exceeds_tolerance": coordinate["weighted_gap"] > key[0],
        })

    certificate_orders = Counter(
        row["single_coefficient_gap_order"]
        for row in rows if row["single_coefficient_gap_exceeds_tolerance"]
    )
    return {
        "status": "rh255_expanded_window_anchored_zonotope_obstruction",
        "endpoint_count": len(rows),
        "orders": ORDERS.tolist(),
        "minimum_rank": MINIMUM_RANK,
        "maximum_imaginary_leakage_before_real_lp": maximum_imaginary_leakage,
        "total_eligible_prefix_count": sum(row["eligible_prefix_count"] for row in rows),
        "total_eligible_binary_subset_count": sum(row["eligible_binary_subset_count"] for row in rows),
        "prefix_pass_count": sum(row["best_prefix_distance"] <= row["sigma"] for row in rows),
        "box_zonotope_pass_count": sum(row["best_box_distance"] <= row["sigma"] for row in rows),
        "minimum_box_distance": min(row["best_box_distance"] for row in rows),
        "maximum_box_distance": max(row["best_box_distance"] for row in rows),
        "minimum_box_failure_margin": min(row["box_failure_margin"] for row in rows),
        "minimum_box_distance_over_tolerance": min(row["box_distance_over_tolerance"] for row in rows),
        "maximum_box_distance_over_tolerance": max(row["box_distance_over_tolerance"] for row in rows),
        "maximum_box_primal_dual_gap": max(abs(row["box_primal_dual_gap"]) for row in rows),
        "minimum_expanded_distance_improvement": min(row["expanded_distance_improvement"] for row in rows),
        "maximum_expanded_distance_improvement": max(row["expanded_distance_improvement"] for row in rows),
        "improved_endpoint_count": sum(row["expanded_distance_improvement"] > 0.0 for row in rows),
        "single_coefficient_certificate_count": sum(
            row["single_coefficient_gap_exceeds_tolerance"] for row in rows
        ),
        "single_coefficient_certificate_order_histogram": {
            str(order): count for order, count in sorted(certificate_orders.items())
        },
        "endpoint_rows": rows,
        "route_coordinate": "expanded_single_use_shell_class_obstructed_open_invariant_signed_complex_selector",
        "theorem_boundary": {
            "expanded_box_zonotope_primal_dual_certificate": True,
            "all_expanded_single_use_shell_subsets_excluded": True,
            "unbounded_shell_multiplicities_excluded": False,
            "signed_or_complex_selector_excluded": False,
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
    output = ROOT / "results/expanded_reachability_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "passes": {"prefix": payload["prefix_pass_count"], "box": payload["box_zonotope_pass_count"]},
        "box_distance_range": [payload["minimum_box_distance"], payload["maximum_box_distance"]],
        "binary_subset_count": payload["total_eligible_binary_subset_count"],
        "maximum_primal_dual_gap": payload["maximum_box_primal_dual_gap"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
