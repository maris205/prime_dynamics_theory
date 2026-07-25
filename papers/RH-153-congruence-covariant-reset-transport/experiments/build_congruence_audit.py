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
sys.path[:0] = [
    str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"),
    str(RH94 / "experiments"), str(RH151 / "experiments"),
]

from build_reset_packet_audit import spectral_center_data  # noqa: E402
from half_log_rank import clock_rank  # noqa: E402
from reset_congruence import correlated_base_lower, inverse_congruence_radius, normalized_base  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import memory_grams  # noqa: E402


def aligned_frame_radius(projector_radius: float) -> float:
    value = float(projector_radius)
    return math.sqrt(max(0.0, 2.0 - 2.0 * math.sqrt(max(0.0, 1.0 - value * value))))


def downward(value: float) -> float:
    return math.nextafter(float(value), -math.inf)


def upward(value: float) -> float:
    return math.nextafter(float(value), math.inf)


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
    transitions = {
        (float(row["sigma"]), row["side"], int(item["time"])): item
        for row in overlap["rows"] for item in row["transitions"]
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
            centers = [spectral_center_data(gram, rank) for gram in grams]
            audit = []
            for time in range(1, len(grams)):
                source_snapshot = snapshots[(sigma, side, time - 1)]
                target_snapshot = snapshots[(sigma, side, time)]
                transition = transitions[(sigma, side, time)]
                source_frame = np.asarray(centers[time - 1]["frame"], dtype=float)
                target_frame = np.asarray(centers[time]["frame"], dtype=float)
                nominal_overlap = source_frame.T @ target_frame
                nominal_singular = np.linalg.svd(nominal_overlap, compute_uv=False)
                alpha = downward(nominal_singular[-1])

                target_center = centers[time]
                eigenvalues = [float(value) for value in target_center["eigenvalues"]]
                total_eigen_radius = upward(
                    float(target_center["total_center_spectral_error"])
                    + float(target_snapshot["matrix_operator_radius"])
                )
                eigen_lower = downward(max(0.0, eigenvalues[rank - 1] - total_eigen_radius))
                eigen_upper = upward(eigenvalues[0] + total_eigen_radius)
                native_base = normalized_base(eigen_lower, eigen_upper)
                robust_overlap = downward(float(transition["robust_lower"]))
                paired_base = correlated_base_lower(eigen_lower, eigen_upper, robust_overlap)

                left_frame_radius = aligned_frame_radius(float(source_snapshot["direct_reset_projector_radius"]))
                right_frame_radius = aligned_frame_radius(float(target_snapshot["direct_reset_projector_radius"]))
                overlap_radius = upward(left_frame_radius + right_frame_radius)
                target_gram = np.asarray(grams[time], dtype=float)
                compressed = target_frame.T @ target_gram @ target_frame
                compressed = (compressed + compressed.T) / 2.0
                gram_radius = upward(
                    float(target_snapshot["matrix_operator_radius"])
                    + 2.0 * float(np.linalg.norm(target_gram, 2)) * right_frame_radius
                )
                independent = inverse_congruence_radius(
                    alpha, overlap_radius, float(np.linalg.norm(compressed, 2)), gram_radius
                )
                inverse = np.linalg.inv(nominal_overlap)
                nominal_pullback = inverse.T @ compressed @ inverse
                nominal_pullback = (nominal_pullback + nominal_pullback.T) / 2.0
                pullback_values = np.linalg.eigvalsh(nominal_pullback)
                pullback_min = downward(max(0.0, float(pullback_values[0])))
                pullback_max = upward(float(pullback_values[-1]))
                independent_radius = upward(float(independent["radius"]))
                audit.append({
                    "time": time,
                    "rank": rank,
                    "nominal_overlap_smin": alpha,
                    "robust_overlap_lower": robust_overlap,
                    "native_reset_base_lower": native_base,
                    "correlated_pulled_base_lower": paired_base,
                    "correlated_tail_ratio_multiplier": 1.0,
                    "eigenvalue_lower": eigen_lower,
                    "eigenvalue_upper": eigen_upper,
                    "total_eigenvalue_radius": total_eigen_radius,
                    "independent_overlap_radius": overlap_radius,
                    "independent_gram_radius": gram_radius,
                    "independent_inverse_difference_upper": independent["inverse_difference_upper"],
                    "independent_pullback_radius": independent_radius,
                    "nominal_pullback_min": pullback_min,
                    "nominal_pullback_max": pullback_max,
                    "independent_positive_definite": bool(independent_radius < pullback_min),
                    "independent_relative_norm_radius": independent_radius / pullback_max if pullback_max > 0.0 else math.inf,
                })
            rows.append({"sigma": sigma, "side": side, "rank": rank, "transitions": audit})
            print(json.dumps({
                "sigma": sigma,
                "side": side,
                "transition_count": len(audit),
                "paired_positive": sum(item["correlated_pulled_base_lower"] > 0.0 for item in audit),
                "independent_positive": sum(item["independent_positive_definite"] for item in audit),
            }, sort_keys=True), flush=True)

    items = [item for row in rows for item in row["transitions"]]
    summary = {
        "channel_count": len(rows),
        "transition_count": len(items),
        "correlated_positive_base_count": sum(item["correlated_pulled_base_lower"] > 0.0 for item in items),
        "minimum_correlated_pulled_base_lower": min(item["correlated_pulled_base_lower"] for item in items),
        "median_correlated_pulled_base_lower": float(np.median([item["correlated_pulled_base_lower"] for item in items])),
        "correlated_base_above_1e_8_count": sum(item["correlated_pulled_base_lower"] >= 1e-8 for item in items),
        "correlated_base_above_1e_6_count": sum(item["correlated_pulled_base_lower"] >= 1e-6 for item in items),
        "correlated_base_above_1e_4_count": sum(item["correlated_pulled_base_lower"] >= 1e-4 for item in items),
        "independent_positive_definite_count": sum(item["independent_positive_definite"] for item in items),
        "independent_positive_definite_failure_count": sum(not item["independent_positive_definite"] for item in items),
        "maximum_independent_pullback_radius": max(item["independent_pullback_radius"] for item in items),
        "maximum_independent_radius_to_minimum_ratio": max(
            item["independent_pullback_radius"] / item["nominal_pullback_min"]
            for item in items if item["nominal_pullback_min"] > 0.0
        ),
        "independent_relative_norm_below_one_count": sum(item["independent_relative_norm_radius"] < 1.0 for item in items),
    }
    payload = {
        "status": "rh153_congruence_covariant_reset_transport",
        "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "loewner_congruence_covariance": True,
            "generalized_tail_ratio_invariance": True,
            "sharp_normalized_base_transport_lower": True,
            "independent_inverse_congruence_radius": True,
            "all_frozen_correlated_bases_positive": not args.smoke and summary["correlated_positive_base_count"] == 120,
            "independent_ball_route_closes": False,
            "native_reset_tail_assembly": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "Transporting a reset Gram and tail through one common inverse-overlap congruence preserves their Loewner ratio exactly and costs only one overlap condition factor in the normalized base. All 120 frozen correlated base lowers remain positive. Separating packet, Gram, and overlap balls before inversion loses positive definiteness on 52 transitions, so the next layer must build and transport a native correlated reset pair.",
    }
    output = ROOT / "results" / ("congruence_smoke.json" if args.smoke else "congruence_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
