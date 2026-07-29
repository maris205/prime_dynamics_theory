"""Resolve a candidate window with twice the archived spectral margin."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
sys.path[:0] = [str(ROOT / "src"), str(RH14 / "src"), str(RH222 / "src")]

from expanded_window import (  # noqa: E402
    complex_payload,
    match_reference_roots,
    shell_count_and_rank,
    values,
)
from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from resonance_cloud import (  # noqa: E402
    conjugacy_error,
    conjugate_shells,
    haar_coarse_embedding,
    resolve_bulk,
)


EXPANDED_MARGIN = 32
ORDERS = np.arange(2, 13)


def scalar(payload: dict[str, float]) -> complex:
    return complex(payload["real"], payload["imag"])


def endpoint_row(reference: dict[str, object], matrix) -> dict[str, object]:
    target = int(reference["target_rank"])
    resolution = resolve_bulk(matrix, target + EXPANDED_MARGIN)
    expanded = np.asarray(resolution.bulk, dtype=complex)
    old = values(reference["candidate_roots"])
    matching = match_reference_roots(old, expanded)
    unmatched = np.asarray(matching["unmatched"], dtype=complex)
    shells = conjugate_shells(expanded)
    shell_count, complete_rank = shell_count_and_rank(shells)
    new_shells = conjugate_shells(unmatched) if unmatched.size else []
    new_shell_count, new_complete_rank = shell_count_and_rank(new_shells)
    nested_margin = float(np.min(np.abs(old)) - np.max(np.abs(unmatched))) if unmatched.size else float("inf")
    new_power_traces = np.asarray([np.sum(unmatched**order) for order in ORDERS])
    return {
        "sigma": float(reference["sigma"]),
        "side": str(reference["side"]),
        "dimension": int(matrix.shape[0]),
        "target_rank": target,
        "reference_candidate_rank": int(old.size),
        "expanded_candidate_rank": int(expanded.size),
        "new_candidate_rank": int(unmatched.size),
        "expanded_shell_count": shell_count,
        "expanded_complete_shell_rank": complete_rank,
        "new_shell_count": new_shell_count,
        "new_complete_shell_rank": new_complete_rank,
        "expanded_conjugacy_error": conjugacy_error(expanded),
        "new_conjugacy_error": conjugacy_error(unmatched) if unmatched.size else 0.0,
        "maximum_reference_matching_error": matching["maximum_matching_error"],
        "mean_reference_matching_error": matching["mean_matching_error"],
        "perron_discrepancy_from_reference": abs(resolution.perron - scalar(reference["perron_scaled"])),
        "parity_discrepancy_from_reference": abs(resolution.parity - scalar(reference["parity_scaled"])),
        "nested_radial_margin": nested_margin,
        "expanded_outer_modulus": float(np.max(np.abs(expanded))),
        "expanded_inner_modulus": float(np.min(np.abs(expanded))),
        "new_outer_modulus": float(np.max(np.abs(unmatched))) if unmatched.size else 0.0,
        "new_inner_modulus": float(np.min(np.abs(unmatched))) if unmatched.size else 0.0,
        "expanded_candidate_roots": complex_payload(expanded),
        "newly_resolved_roots": complex_payload(unmatched),
        "newly_resolved_power_traces_orders_2_to_12": complex_payload(new_power_traces),
    }


def run() -> dict[str, object]:
    started = time.perf_counter()
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text())
    reference = {
        (float(row["sigma"]), str(row["side"])): row
        for row in atlas["endpoint_rows"]
    }
    rows = []
    for sigma, target in zip(atlas["sigmas"], atlas["target_ranks"]):
        dimension = max(32, 2 * int(round(float(atlas["fine_resolution"]) / sigma / 2.0)))
        fine = sparse_folded_gaussian_matrix(dimension, sigma).tocsr()
        embedding = haar_coarse_embedding(dimension)
        coarse = (embedding.T @ fine @ embedding).tocsr()
        rows.append(endpoint_row(reference[(float(sigma), "left")], fine))
        rows.append(endpoint_row(reference[(float(sigma), "right")], coarse))

    return {
        "status": "rh254_expanded_resolved_candidate_window_atlas",
        "reference_candidate_margin": int(atlas["candidate_margin"]),
        "expanded_candidate_margin": EXPANDED_MARGIN,
        "endpoint_count": len(rows),
        "orders_for_new_root_power_traces": ORDERS.tolist(),
        "minimum_reference_candidate_rank": min(row["reference_candidate_rank"] for row in rows),
        "maximum_reference_candidate_rank": max(row["reference_candidate_rank"] for row in rows),
        "minimum_expanded_candidate_rank": min(row["expanded_candidate_rank"] for row in rows),
        "maximum_expanded_candidate_rank": max(row["expanded_candidate_rank"] for row in rows),
        "minimum_expanded_complete_shell_rank": min(row["expanded_complete_shell_rank"] for row in rows),
        "maximum_expanded_complete_shell_rank": max(row["expanded_complete_shell_rank"] for row in rows),
        "minimum_new_candidate_rank": min(row["new_candidate_rank"] for row in rows),
        "maximum_new_candidate_rank": max(row["new_candidate_rank"] for row in rows),
        "maximum_matching_error": max(row["maximum_reference_matching_error"] for row in rows),
        "maximum_perron_discrepancy": max(row["perron_discrepancy_from_reference"] for row in rows),
        "maximum_parity_discrepancy": max(row["parity_discrepancy_from_reference"] for row in rows),
        "minimum_nested_radial_margin": min(row["nested_radial_margin"] for row in rows),
        "maximum_expanded_conjugacy_error": max(row["expanded_conjugacy_error"] for row in rows),
        "maximum_new_conjugacy_error": max(row["new_conjugacy_error"] for row in rows),
        "expanded_shell_complete_endpoint_count": sum(
            row["expanded_complete_shell_rank"] == row["expanded_candidate_rank"]
            for row in rows
        ),
        "expanded_shell_incomplete_endpoint_count": sum(
            row["expanded_complete_shell_rank"] != row["expanded_candidate_rank"]
            for row in rows
        ),
        "maximum_discarded_incomplete_expanded_root_count": max(
            row["expanded_candidate_rank"] - row["expanded_complete_shell_rank"]
            for row in rows
        ),
        "all_expanded_shells_conjugate_closed": all(
            row["expanded_complete_shell_rank"] == row["expanded_candidate_rank"]
            for row in rows
        ),
        "all_new_shells_conjugate_closed": all(
            row["new_complete_shell_rank"] == row["new_candidate_rank"]
            for row in rows
        ),
        "endpoint_rows": rows,
        "elapsed_seconds": time.perf_counter() - started,
        "route_coordinate": "expanded_resolved_window_ready_for_anchored_reachability_audit",
        "theorem_boundary": {
            "expanded_window_finite": True,
            "expanded_window_interval_certified": False,
            "fixed_count_boundary_always_shell_complete": False,
            "anchored_reachability_completed": False,
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
    output = ROOT / "results/expanded_window_atlas.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "endpoint_count": payload["endpoint_count"],
        "rank_range": [payload["minimum_expanded_candidate_rank"], payload["maximum_expanded_candidate_rank"]],
        "new_rank_range": [payload["minimum_new_candidate_rank"], payload["maximum_new_candidate_rank"]],
        "maximum_matching_error": payload["maximum_matching_error"],
        "minimum_nested_radial_margin": payload["minimum_nested_radial_margin"],
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
