"""Run the RH-238 shell-prefix scan against the RH-243 anchor."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
RH236 = PAPERS / "RH-236-cloud-extracted-trace-moment-atlas"
RH238 = PAPERS / "RH-238-trace-adaptive-shell-selection"
RH243 = PAPERS / "RH-243-deterministic-numerator-coefficient-anchor-dictionary"
sys.path[:0] = [str(ROOT / "src"), str(RH222 / "src")]

from anchored_prefix import (  # noqa: E402
    anchored_log_jet_distance,
    disjoint_ball_margin,
    scan_anchored_prefixes,
)
from resonance_cloud import conjugate_shells  # noqa: E402


MINIMUM_RANK = 4
RADIUS = 1.0


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def scalar(payload: dict[str, float]) -> complex:
    return complex(payload["real"], payload["imag"])


def run() -> dict[str, object]:
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    traces = json.loads((RH236 / "results/trace_moment_atlas.json").read_text(encoding="utf-8"))
    adaptive = json.loads((RH238 / "results/adaptive_shell_selection.json").read_text(encoding="utf-8"))
    anchor = json.loads((RH243 / "results/coefficient_anchor_audit.json").read_text(encoding="utf-8"))

    target = np.asarray([
        row["hardy_scaled_one_step_anchor"] for row in anchor["coefficient_rows"]
    ], dtype=complex)
    target_norm = float(anchor["one_step_target_unit_disk_log_jet_norm_orders_2_to_12"])
    trace_rows = {
        (float(row["sigma"]), str(row["side"])): row
        for row in traces["endpoint_rows"]
    }
    adaptive_rows = {
        (float(row["sigma"]), str(row["side"])): row
        for row in adaptive["endpoint_rows"]
    }

    rows = []
    for endpoint in atlas["endpoint_rows"]:
        sigma = float(endpoint["sigma"])
        side = str(endpoint["side"])
        key = (sigma, side)
        trace_row = trace_rows[key]
        full = values(trace_row["full_trace_powers"])
        shells = conjugate_shells(values(endpoint["candidate_roots"]))
        scan = scan_anchored_prefixes(
            shells,
            full,
            scalar(endpoint["perron_scaled"]),
            scalar(endpoint["parity_scaled"]),
            target,
            tolerance=sigma,
            minimum_rank=MINIMUM_RANK,
            radius=RADIUS,
        )
        best = scan["best"]
        if best is None:
            raise RuntimeError("every archived endpoint must contain an eligible prefix")

        zero_row = adaptive_rows[key]
        zero_moments = values(zero_row["adaptive_trace_powers"])
        zero_norm = float(zero_row["adaptive_jet_norm"])
        zero_to_anchor = anchored_log_jet_distance(zero_moments, target, RADIUS)
        triangle_lower = target_norm - zero_norm
        rows.append({
            "sigma": sigma,
            "side": side,
            "dimension": int(endpoint["dimension"]),
            "current_atlas_rank": int(endpoint["actual_rank"]),
            "complete_candidate_rank": int(sum(np.asarray(shell).size for shell in shells)),
            "evaluated_prefix_count": len(scan["rows"]),
            "anchored_admissible_prefix_count": len(scan["admissible_rows"]),
            "anchored_selection_pass": scan["selected"] is not None,
            "best_anchored_rank": int(np.asarray(best["cloud"]).size),
            "best_anchored_jet_distance": float(best["distance"]),
            "best_distance_over_tolerance": float(best["distance"] / sigma),
            "rh238_zero_selected_rank": int(zero_row["adaptive_rank"]),
            "rh238_zero_selected_jet_norm": zero_norm,
            "rh238_zero_selected_anchored_distance": zero_to_anchor,
            "triangle_lower_bound_for_zero_selected_anchor_distance": triangle_lower,
            "triangle_bound_slack": float(zero_to_anchor - triangle_lower),
            "equal_tolerance_ball_margin": disjoint_ball_margin(target_norm, sigma),
        })

    passing = [row for row in rows if row["anchored_selection_pass"]]
    return {
        "status": "rh244_anchored_shell_prefix_availability_obstruction",
        "maximum_order": int(traces["maximum_order"]),
        "minimum_rank": MINIMUM_RANK,
        "radius": RADIUS,
        "tolerance_rule": "epsilon_sigma=sigma",
        "target_source": "RH-243 Hardy-scaled deterministic numerator anchor",
        "target_unit_disk_log_jet_norm_orders_2_to_12": target_norm,
        "endpoint_count": len(rows),
        "anchored_selection_pass_count": len(passing),
        "anchored_selection_failure_count": len(rows) - len(passing),
        "all_archived_endpoints_fail": not passing,
        "total_evaluated_prefix_count": sum(row["evaluated_prefix_count"] for row in rows),
        "minimum_best_anchored_rank": min(row["best_anchored_rank"] for row in rows),
        "maximum_best_anchored_rank": max(row["best_anchored_rank"] for row in rows),
        "minimum_best_anchored_jet_distance": min(row["best_anchored_jet_distance"] for row in rows),
        "maximum_best_anchored_jet_distance": max(row["best_anchored_jet_distance"] for row in rows),
        "minimum_best_distance_over_tolerance": min(row["best_distance_over_tolerance"] for row in rows),
        "maximum_best_distance_over_tolerance": max(row["best_distance_over_tolerance"] for row in rows),
        "minimum_equal_tolerance_ball_margin": min(row["equal_tolerance_ball_margin"] for row in rows),
        "minimum_triangle_bound_slack": min(row["triangle_bound_slack"] for row in rows),
        "endpoint_rows": rows,
        "route_coordinate": "anchored_prefix_class_obstructed_open_nonprefix_cloud_and_uniform_envelope",
        "theorem_boundary": {
            "zero_and_anchor_equal_tolerance_balls_disjoint_for_all_archived_sigmas": all(
                row["equal_tolerance_ball_margin"] > 0.0 for row in rows
            ),
            "frozen_shell_complete_prefix_class_fails_anchored_tolerance": not passing,
            "alternative_cloud_classes_excluded": False,
            "asymptotic_candidate_nonexistence": False,
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
    output = ROOT / "results/anchored_prefix_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "passes": payload["anchored_selection_pass_count"],
        "failures": payload["anchored_selection_failure_count"],
        "best_distance_range": [
            payload["minimum_best_anchored_jet_distance"],
            payload["maximum_best_anchored_jet_distance"],
        ],
        "best_rank_range": [
            payload["minimum_best_anchored_rank"],
            payload["maximum_best_anchored_rank"],
        ],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
