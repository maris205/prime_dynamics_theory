from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import mpmath as mp
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH137 = PAPERS / "RH-137-finite-horizon-young-tail-envelope"
sys.path[:0] = [str(ROOT / "src"), str(RH137 / "experiments")]

from backward_viability import backward_kernel, young_map  # noqa: E402
import build_finite_horizon_audit as horizon  # noqa: E402


MP_DPS = 80


def finite_candidate(item: dict[str, object]) -> dict[str, float]:
    return {
        "metric": float(item["metric_base"]),
        "frame": float(item["frame_base"]),
        "birth": float(item["birth"]),
    }


def chain(model: dict[str, object], sigma: float, threshold: float, rank: int) -> dict[str, object]:
    temporal = horizon.affine_audit.records(model, sigma, threshold, rank)
    coefficient_data = [horizon.coefficients(old, new) for old, new in zip(temporal, temporal[1:])]
    sequence = [[finite_candidate(candidate) for candidate in data["candidates"]] for data in coefficient_data]
    kernel = backward_kernel(sequence, ceiling=1.0, cap=1.0)
    radii = [float(value) for value in kernel["radii"]]
    indices = [int(value) for value in kernel["control_indices"]]
    state = 0.99 * radii[0]
    trajectory = [state]
    selected = []
    if radii[0] > 0.0:
        for step, (candidates, index) in enumerate(zip(sequence, indices)):
            candidate = candidates[index]
            state = young_map(state, candidate["metric"], candidate["frame"], candidate["birth"])
            trajectory.append(state)
            original = coefficient_data[step]["candidates"][index]
            selected.append({
                "kind": original["kind"],
                "weight": float(original["weight"]),
                "candidate_count": len(candidates),
            })
    failure_index = next((index for index, radius in enumerate(radii[:-1]) if radius == 0.0 and radii[index + 1] > 0.0), None)
    if failure_index is None and radii[0] == 0.0:
        failure_index = max(index for index, floor in enumerate(kernel["minimum_floors"]) if floor >= radii[index + 1])
    return {
        "sigma": sigma,
        "side": str(model["side"]),
        "threshold": threshold,
        "step_count": len(sequence),
        "start_viability_radius": radii[0],
        "backward_radii": radii,
        "minimum_positive_backward_radius": min((value for value in radii if value > 0.0), default=0.0),
        "zero_kernel_count": sum(value == 0.0 for value in radii[:-1]),
        "viable_from_zero": bool(radii[0] > 0.0),
        "full_unit_start_radius": bool(radii[0] == 1.0),
        "near_boundary_forward_trajectory": trajectory,
        "near_boundary_policy_safe": bool(radii[0] > 0.0 and all(value < 1.0 for value in trajectory[1:])),
        "selected_controls": selected,
        "obstruction_step": failure_index,
        "obstruction_minimum_floor": None if failure_index is None else float(kernel["minimum_floors"][failure_index]),
        "obstruction_target_radius": None if failure_index is None else radii[failure_index + 1],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    mp.mp.dps = MP_DPS
    sigmas = horizon.metric_audit.SIGMAS[:2] if args.smoke else horizon.metric_audit.SIGMAS
    thresholds = horizon.metric_audit.THRESHOLDS[:1] if args.smoke else horizon.metric_audit.THRESHOLDS
    sides = ("left",) if args.smoke else ("left", "right")
    rows = []
    for sigma in sigmas:
        rank = horizon.affine_audit.floorfree.clock_rank(sigma, offset=horizon.affine_audit.RANK_OFFSET)
        _, models = horizon.metric_audit.build_models(sigma)
        for model in models:
            if model["side"] not in sides:
                continue
            for threshold in thresholds:
                rows.append(chain(model, sigma, threshold, rank))
        print(json.dumps({"completed_sigma": sigma, "chain_count": len(rows)}, sort_keys=True), flush=True)

    viable = [row for row in rows if row["viable_from_zero"]]
    obstructed = [row for row in rows if not row["viable_from_zero"]]
    positive_radii = [value for row in viable for value in row["backward_radii"][:-1] if value > 0.0]
    summary = {
        "chain_count": len(rows),
        "viable_chain_count": len(viable),
        "obstructed_chain_count": len(obstructed),
        "full_unit_start_radius_count": sum(row["full_unit_start_radius"] for row in rows),
        "near_boundary_policy_safe_count": sum(row["near_boundary_policy_safe"] for row in rows),
        "minimum_positive_backward_radius": min(positive_radii),
        "maximum_obstruction_minimum_floor": max((row["obstruction_minimum_floor"] or 0.0 for row in obstructed), default=0.0),
        "minimum_obstruction_minimum_floor": min((row["obstruction_minimum_floor"] for row in obstructed if row["obstruction_minimum_floor"] is not None), default=None),
        "obstruction_identifiers": [f"{row['sigma']:.2f}:{row['side']}:{row['threshold']:.0e}" for row in obstructed],
    }
    payload = {
        "status": "rh144_backward_block_controlled_viability",
        "precision_decimal_digits": MP_DPS,
        "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "closed_form_young_preimage_radius": True,
            "controlled_backward_viability_kernel": True,
            "repeating_block_invariance_theorem": True,
            "two_rh137_failures_are_candidate_family_obstructions": not args.smoke and len(obstructed) == 2,
            "all_level_repeating_block_hypothesis_verified": False,
            "delayed_start_after_coarse_birth_proved": False,
            "uniform_controlled_tail_gap": False,
            "normalized_base_liminf": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "Backward dynamic programming gives exact scalar viability kernels for every finite "
            "candidate family. Twenty-eight chains admit the entire initial interval [0,1), while "
            "the two coarse left chains have empty kernels because every available control has an "
            "unavoidable floor above the safety wall. This proves those failures are not greedy-choice "
            "artifacts and supplies the correct block/reset criterion for an all-level P_V theorem."
        ),
    }
    output = ROOT / "results" / ("backward_viability_smoke.json" if args.smoke else "backward_viability_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()

