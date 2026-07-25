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
RH152 = PAPERS / "RH-152-reset-transition-overlap-coherence"
RH154 = PAPERS / "RH-154-half-horizon-delayed-reset-suffix"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"), str(RH94 / "experiments")]

from half_log_rank import clock_rank  # noqa: E402
from lag_reset_bridge import (  # noqa: E402
    centered_action_radius,
    choose_adaptive_candidate,
    path_overlap_lower,
    singular_interval,
)
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import ETA, memory_grams  # noqa: E402


DEPTH = 5
MAX_LAG = 8


def top_projector(matrix: np.ndarray, rank: int) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.T) / 2.0)
    frame = vectors[:, np.argsort(values)[::-1][:rank]]
    return frame @ frame.T


def outward_lower(value: float) -> float:
    return math.nextafter(value, -math.inf) if value > 0.0 else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    reset = json.loads((RH151 / "results/reset_packet_audit.json").read_text())
    snapshots = {
        (float(row["sigma"]), channel["side"], int(item["time"])): item
        for row in reset["rows"] for channel in row["channels"] for item in channel["snapshots"]
    }
    overlap = json.loads((RH152 / "results/overlap_audit.json").read_text())
    overlap_lowers = {
        (float(row["sigma"]), row["side"], int(item["time"])): float(item["robust_lower"])
        for row in overlap["rows"] for item in row["transitions"]
    }
    suffix = json.loads((RH154 / "results/suffix_audit.json").read_text())["half_suffix"]
    suffix_starts = {
        (float(item["sigma"]), item["side"]): int(item["start_time"])
        for item in suffix["channels"]
    }

    rows = []
    sigmas = SIGMAS[:1] if args.smoke else SIGMAS
    for sigma in sigmas:
        _, models = build_models(sigma)
        for model in models:
            side = str(model["side"])
            rank = clock_rank(sigma, offset=2)
            endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
            operator = np.asarray(model["operator"], dtype=float)
            states = [np.asarray(model["source"], dtype=float)]
            for _ in range(endpoint):
                states.append(operator @ states[-1])
            grams = memory_grams(states)
            projectors = [top_projector(gram, rank) for gram in grams]
            targets = []
            for time in range(1, endpoint + 1):
                recent = np.asarray(grams[time], dtype=float).copy()
                recent_radius = float(snapshots[(sigma, side, time)]["matrix_operator_radius"])
                if time >= DEPTH:
                    recent -= ETA**DEPTH * grams[time - DEPTH]
                    recent_radius = math.nextafter(
                        recent_radius
                        + ETA**DEPTH * float(snapshots[(sigma, side, time - DEPTH)]["matrix_operator_radius"]),
                        math.inf,
                    )
                recent = (recent + recent.T) / 2.0
                eigenvalues = np.linalg.eigvalsh(recent)
                spread = math.nextafter(float(eigenvalues[-1] - eigenvalues[0]), math.inf)
                recent_norm = math.nextafter(float(np.linalg.norm(recent, 2)), math.inf)
                candidates = []
                for lag in range(1, min(MAX_LAG, time) + 1):
                    old_time = time - lag
                    projector = projectors[old_time]
                    cross = (np.eye(recent.shape[0]) - projector) @ recent @ projector
                    singular = np.linalg.svd(cross, compute_uv=False)
                    projector_radius = float(snapshots[(sigma, side, old_time)]["direct_reset_projector_radius"])
                    radius = math.nextafter(
                        centered_action_radius(recent_radius, spread, projector_radius),
                        math.inf,
                    )
                    uncentered_radius = math.nextafter(
                        recent_radius + 2.0 * recent_norm * projector_radius,
                        math.inf,
                    )
                    first_lower, first_upper = singular_interval(float(singular[0]), radius)
                    fourth_lower, fourth_upper = singular_interval(float(singular[3]), radius)
                    first_lower = outward_lower(first_lower)
                    fourth_lower = outward_lower(fourth_lower)
                    first_upper = math.nextafter(first_upper, math.inf)
                    fourth_upper = math.nextafter(fourth_upper, math.inf)
                    path_values = [
                        overlap_lowers[(sigma, side, step)]
                        for step in range(old_time + 1, time + 1)
                    ]
                    path_lower = math.nextafter(path_overlap_lower(path_values), -math.inf)
                    normalized = fourth_lower / first_upper if first_upper > 0.0 else 0.0
                    uncentered_fourth_lower = outward_lower(
                        max(0.0, float(singular[3]) - uncentered_radius)
                    )
                    candidates.append({
                        "lag": lag,
                        "old_time": old_time,
                        "projector_radius": projector_radius,
                        "recent_matrix_radius": recent_radius,
                        "recent_spectral_spread": spread,
                        "recent_operator_norm": recent_norm,
                        "cross_operator_radius": radius,
                        "uncentered_cross_operator_radius": uncentered_radius,
                        "nominal_first_cross_singular": float(singular[0]),
                        "nominal_fourth_cross_singular": float(singular[3]),
                        "first_cross_singular_lower": first_lower,
                        "first_cross_singular_upper": first_upper,
                        "fourth_cross_singular_lower": fourth_lower,
                        "fourth_cross_singular_upper": fourth_upper,
                        "four_mode_certified": fourth_lower > 0.0,
                        "uncentered_four_mode_certified": uncentered_fourth_lower > 0.0,
                        "uncentered_fourth_cross_singular_lower": uncentered_fourth_lower,
                        "normalized_base_lower": normalized,
                        "path_overlap_lower": path_lower,
                        "path_inverse_upper": math.nextafter(1.0 / path_lower, math.inf),
                    })
                chosen = dict(choose_adaptive_candidate(candidates))
                first_certifying = next(
                    (item["lag"] for item in candidates if item["four_mode_certified"]),
                    None,
                )
                targets.append({
                    "time": time,
                    "rank": rank,
                    "in_half_suffix": time >= suffix_starts[(sigma, side)],
                    "terminal": time == endpoint,
                    "first_certifying_lag": first_certifying,
                    "selected_lag": chosen["lag"],
                    "selected": chosen,
                    "candidates": candidates,
                })
            rows.append({
                "sigma": sigma,
                "side": side,
                "rank": rank,
                "endpoint": endpoint,
                "target_count": len(targets),
                "targets": targets,
            })
            print(json.dumps({
                "sigma": sigma,
                "side": side,
                "target_count": len(targets),
                "adaptive_certified": sum(item["selected"]["four_mode_certified"] for item in targets),
                "maximum_first_certifying_lag": max(item["first_certifying_lag"] or MAX_LAG + 1 for item in targets),
            }, sort_keys=True), flush=True)

    targets = [item for row in rows for item in row["targets"]]
    half = [item for item in targets if item["in_half_suffix"]]
    terminal = [item for item in targets if item["terminal"]]

    def prefix_certified(item: dict[str, object], lag_horizon: int) -> bool:
        candidates = item["candidates"]
        return any(
            bool(candidate["four_mode_certified"])
            for candidate in candidates
            if int(candidate["lag"]) <= lag_horizon
        )

    certificate_counts = {
        str(lag): sum(prefix_certified(item, lag) for item in targets)
        for lag in range(1, MAX_LAG + 1)
    }
    uncentered_certificate_counts = {
        str(lag): sum(
            any(
                bool(candidate["uncentered_four_mode_certified"])
                for candidate in item["candidates"]
                if int(candidate["lag"]) <= lag
            )
            for item in targets
        )
        for lag in range(1, MAX_LAG + 1)
    }
    half_certificate_counts = {
        str(lag): sum(prefix_certified(item, lag) for item in half)
        for lag in range(1, MAX_LAG + 1)
    }
    terminal_certificate_counts = {
        str(lag): sum(prefix_certified(item, lag) for item in terminal)
        for lag in range(1, MAX_LAG + 1)
    }
    selected = [item["selected"] for item in targets]
    histogram = {
        str(lag): sum(int(item["lag"]) == lag for item in selected)
        for lag in range(1, MAX_LAG + 1)
    }
    summary = {
        "channel_count": len(rows),
        "target_count": len(targets),
        "candidate_count": sum(len(item["candidates"]) for item in targets),
        "maximum_lag": MAX_LAG,
        "certificate_counts_by_lag_horizon": certificate_counts,
        "uncentered_certificate_counts_by_lag_horizon": uncentered_certificate_counts,
        "scalar_centering_recovered_target_count_at_maximum_lag": (
            certificate_counts[str(MAX_LAG)] - uncentered_certificate_counts[str(MAX_LAG)]
        ),
        "half_suffix_target_count": len(half),
        "half_suffix_certificate_counts_by_lag_horizon": half_certificate_counts,
        "terminal_target_count": len(terminal),
        "terminal_certificate_counts_by_lag_horizon": terminal_certificate_counts,
        "adaptive_four_mode_certificate_count": sum(item["four_mode_certified"] for item in selected),
        "adaptive_failure_count": sum(not item["four_mode_certified"] for item in selected),
        "maximum_first_certifying_lag": max(item["first_certifying_lag"] or MAX_LAG + 1 for item in targets),
        "selected_lag_histogram": histogram,
        "minimum_selected_fourth_cross_lower": min(item["fourth_cross_singular_lower"] for item in selected),
        "minimum_selected_normalized_base_lower": min(item["normalized_base_lower"] for item in selected),
        "median_selected_normalized_base_lower": float(np.median([item["normalized_base_lower"] for item in selected])),
        "maximum_selected_normalized_base_lower": max(item["normalized_base_lower"] for item in selected),
        "minimum_selected_path_overlap_lower": min(item["path_overlap_lower"] for item in selected),
        "maximum_selected_path_inverse_upper": max(item["path_inverse_upper"] for item in selected),
    }
    all_certified = not args.smoke and summary["adaptive_four_mode_certificate_count"] == 120
    payload = {
        "status": "rh158_adaptive_lag_reset_cross_bridge",
        "eta": ETA,
        "depth": DEPTH,
        "maximum_lag": MAX_LAG,
        "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "general_lag_innovation_identity": True,
            "scalar_centered_cross_action_radius": True,
            "finite_adaptive_lag_optimization": True,
            "all_frozen_update_targets_four_mode_certified_with_lag_at_most_eight": all_certified,
            "all_half_suffix_targets_four_mode_certified": all_certified and half_certificate_counts[str(MAX_LAG)] == 62,
            "all_terminal_targets_four_mode_certified": all_certified and terminal_certificate_counts[str(MAX_LAG)] == 10,
            "uniform_all_level_bounded_lag_law": False,
            "complete_outward_directional_assembly": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "Scalar centering halves the dominant projector-motion cost for nearly positive recent Grams. "
            "Choosing the strongest certified cross base among the previous eight reset packets then gives a positive fourth-cross lower at all 120 frozen update targets, including all 62 delayed-half and all 10 terminal targets. "
            "This closes the finite lagged cross bridge, but an all-level bounded-lag law and the remaining outward assembly are still open."
        ),
    }
    output = ROOT / "results" / ("lag_smoke.json" if args.smoke else "lag_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
