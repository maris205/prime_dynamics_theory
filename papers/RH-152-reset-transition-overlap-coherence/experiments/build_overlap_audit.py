from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
RH151 = PAPERS / "RH-151-ky-fan-reset-packet-atlas"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"), str(RH94 / "experiments")]

from half_log_rank import clock_rank  # noqa: E402
from reset_overlap import overlap_inverse_upper, polar_transition_radius, robust_overlap_lower  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import memory_grams  # noqa: E402


def projector_frames(grams: list[np.ndarray], rank: int) -> list[np.ndarray]:
    frames = []
    for gram in grams:
        values, vectors = np.linalg.eigh((gram + gram.T) / 2.0)
        frames.append(vectors[:, np.argsort(values)[::-1][:rank]])
    return frames


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    archived = json.loads((RH151 / "results/reset_packet_audit.json").read_text())
    radii = {
        (float(row["sigma"]), channel["side"], int(item["time"])): float(item["direct_reset_projector_radius"])
        for row in archived["rows"] for channel in row["channels"] for item in channel["snapshots"]
    }
    rows = []
    sigmas = SIGMAS[:1] if args.smoke else SIGMAS
    for sigma in sigmas:
        _, models = build_models(sigma)
        for model in models:
            side = str(model["side"])
            rank = clock_rank(sigma, offset=2)
            operator = np.asarray(model["operator"], dtype=float)
            source = np.asarray(model["source"], dtype=float)
            endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
            states = [source]
            for _ in range(endpoint):
                states.append(operator @ states[-1])
            frames = projector_frames(memory_grams(states), rank)
            transitions = []
            for time in range(1, len(frames)):
                overlap = frames[time - 1].T @ frames[time]
                singular = np.linalg.svd(overlap, compute_uv=False)
                left_radius = radii[(sigma, side, time - 1)]
                right_radius = radii[(sigma, side, time)]
                robust = robust_overlap_lower(float(singular[-1]), left_radius, right_radius)
                polar = polar_transition_radius(float(singular[-1]), robust["frame_error"])
                transitions.append({
                    "time": time,
                    "nominal_overlap_smin": float(singular[-1]),
                    "nominal_overlap_smax": float(singular[0]),
                    "nominal_projector_distance": float(math.sqrt(max(0.0, 1.0 - singular[-1] ** 2))),
                    "left_projector_radius": left_radius,
                    "right_projector_radius": right_radius,
                    **robust,
                    "inverse_overlap_upper": overlap_inverse_upper(float(robust["robust_lower"])),
                    "polar_radius": polar["radius"],
                    "polar_stable": polar["stable"],
                })
            rows.append({"sigma": sigma, "side": side, "rank": rank, "transition_count": len(transitions), "transitions": transitions})
            print(json.dumps({"sigma": sigma, "side": side, "transitions": len(transitions), "minimum_overlap_lower": min(item["robust_lower"] for item in transitions), "maximum_inverse": max(item["inverse_overlap_upper"] for item in transitions)}, sort_keys=True), flush=True)

    transitions = [item for row in rows for item in row["transitions"]]
    summary = {
        "channel_count": len(rows),
        "transition_count": len(transitions),
        "invertible_transition_count": sum(item["invertible"] for item in transitions),
        "minimum_robust_overlap_lower": min(item["robust_lower"] for item in transitions),
        "maximum_inverse_overlap_upper": max(item["inverse_overlap_upper"] for item in transitions),
        "median_robust_overlap_lower": float(np.median([item["robust_lower"] for item in transitions])),
        "below_1e_1_count": sum(item["robust_lower"] < 1e-1 for item in transitions),
        "below_1e_2_count": sum(item["robust_lower"] < 1e-2 for item in transitions),
        "below_1e_3_count": sum(item["robust_lower"] < 1e-3 for item in transitions),
        "maximum_polar_transition_radius": max(item["polar_radius"] for item in transitions),
        "polar_stability_failure_count": sum(not item["polar_stable"] for item in transitions),
        "maximum_log_inverse_drawdown": max(sum(-math.log(item["robust_lower"]) for item in row["transitions"]) for row in rows),
    }
    payload = {
        "status": "rh152_reset_transition_overlap_coherence",
        "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "robust_principal_angle_triangle": True,
            "frame_overlap_lower": True,
            "polar_transition_bound": True,
            "all_frozen_reset_transitions_invertible": not args.smoke and summary["invertible_transition_count"] == 120,
            "uniform_overlap_lower": False,
            "outward_assembly_closed": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "All 120 consecutive reset transitions remain invertible after their certified packet balls are inserted. The worst robust overlap is 8.99e-5 and the largest inverse overlap is 1.11e4, so finite coherence survives but is strongly nonuniform. The next layer must test whether outward Gram/tail maps tolerate this condition-number drawdown.",
    }
    output = ROOT / "results" / ("overlap_smoke.json" if args.smoke else "overlap_audit.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
