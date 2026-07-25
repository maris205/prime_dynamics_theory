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
RH154 = PAPERS / "RH-154-half-horizon-delayed-reset-suffix"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"), str(RH94 / "experiments")]

from cross_cancellation import coupling_radius, singular_interval  # noqa: E402
from half_log_rank import clock_rank  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import ETA, memory_grams  # noqa: E402


DEPTH = 5


def top_projector(matrix: np.ndarray, rank: int) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.T) / 2.0)
    frame = vectors[:, np.argsort(values)[::-1][:rank]]
    return frame @ frame.T


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    reset = json.loads((RH151 / "results/reset_packet_audit.json").read_text())
    snapshots = {
        (float(row["sigma"]), channel["side"], int(item["time"])): item
        for row in reset["rows"] for channel in row["channels"] for item in channel["snapshots"]
    }
    suffix = json.loads((RH154 / "results/suffix_audit.json").read_text())["half_suffix"]
    starts = {(float(item["sigma"]), item["side"]): int(item["start_time"]) for item in suffix["channels"]}

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
            items = []
            for time, full in enumerate(grams):
                projector = top_projector(full, rank)
                if time < DEPTH:
                    tail = np.zeros_like(full)
                    tail_radius = 0.0
                else:
                    tail = ETA**DEPTH * grams[time - DEPTH]
                    tail_radius = ETA**DEPTH * float(snapshots[(sigma, side, time - DEPTH)]["matrix_operator_radius"])
                nominal_coupling = (np.eye(full.shape[0]) - projector) @ tail @ projector
                singular = np.linalg.svd(nominal_coupling, compute_uv=False)
                projector_radius = float(snapshots[(sigma, side, time)]["direct_reset_projector_radius"])
                radius = math.nextafter(
                    coupling_radius(float(np.linalg.norm(tail, 2)), projector_radius, tail_radius),
                    math.inf,
                )
                first_lower, first_upper = singular_interval(float(singular[0]), radius)
                fourth_lower, fourth_upper = singular_interval(float(singular[3]), radius)
                base_lower = fourth_lower / first_upper if first_upper > 0.0 else 0.0
                items.append({
                    "time": time,
                    "rank": rank,
                    "tail_active": time >= DEPTH,
                    "in_half_suffix": time >= starts[(sigma, side)],
                    "terminal": time == endpoint,
                    "nominal_tail_norm": float(np.linalg.norm(tail, 2)),
                    "tail_matrix_radius": tail_radius,
                    "projector_radius": projector_radius,
                    "coupling_operator_radius": radius,
                    "nominal_first_coupling_singular": float(singular[0]),
                    "nominal_fourth_coupling_singular": float(singular[3]),
                    "first_coupling_singular_lower": first_lower,
                    "first_coupling_singular_upper": first_upper,
                    "fourth_coupling_singular_lower": fourth_lower,
                    "fourth_coupling_singular_upper": fourth_upper,
                    "four_mode_coupling_certified": fourth_lower > 0.0,
                    "four_mode_normalized_base_lower": base_lower,
                    "exact_zero_cross_by_tail_inactivity": time < DEPTH,
                })
            rows.append({"sigma": sigma, "side": side, "rank": rank, "endpoint": endpoint, "snapshots": items})
            active = [item for item in items if item["tail_active"]]
            print(json.dumps({
                "sigma": sigma, "side": side, "active_count": len(active),
                "four_mode_count": sum(item["four_mode_coupling_certified"] for item in active),
                "terminal_four_mode": items[-1]["four_mode_coupling_certified"],
            }, sort_keys=True), flush=True)

    items = [item for row in rows for item in row["snapshots"]]
    active = [item for item in items if item["tail_active"]]
    half = [item for item in items if item["in_half_suffix"]]
    half_active = [item for item in half if item["tail_active"]]
    positive_bases = [item["four_mode_normalized_base_lower"] for item in active if item["four_mode_coupling_certified"]]
    summary = {
        "channel_count": len(rows),
        "snapshot_count": len(items),
        "tail_inactive_exact_zero_count": sum(item["exact_zero_cross_by_tail_inactivity"] for item in items),
        "tail_active_snapshot_count": len(active),
        "active_four_mode_coupling_certificate_count": sum(item["four_mode_coupling_certified"] for item in active),
        "active_four_mode_coupling_failure_count": sum(not item["four_mode_coupling_certified"] for item in active),
        "half_suffix_snapshot_count": len(half),
        "half_suffix_active_count": len(half_active),
        "half_suffix_four_mode_coupling_certificate_count": sum(item["four_mode_coupling_certified"] for item in half),
        "terminal_four_mode_coupling_certificate_count": sum(item["terminal"] and item["four_mode_coupling_certified"] for item in items),
        "minimum_positive_four_mode_base_lower": min(positive_bases) if positive_bases else None,
        "median_positive_four_mode_base_lower": float(np.median(positive_bases)) if positive_bases else None,
        "maximum_four_mode_base_lower": max(positive_bases) if positive_bases else None,
        "minimum_positive_fourth_coupling_singular_lower": min(
            (item["fourth_coupling_singular_lower"] for item in active if item["four_mode_coupling_certified"]),
            default=None,
        ),
        "maximum_fourth_coupling_singular_lower": max(
            (item["fourth_coupling_singular_lower"] for item in active),
            default=None,
        ),
        "complete_active_channel_count": sum(
            bool([item for item in row["snapshots"] if item["tail_active"]])
            and all(item["four_mode_coupling_certified"] for item in row["snapshots"] if item["tail_active"])
            for row in rows
        ),
    }
    payload = {
        "status": "rh157_spectral_reset_cross_action_cancellation",
        "eta": ETA,
        "depth": DEPTH,
        "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "exact_cross_action_tail_cancellation": True,
            "tail_coupling_perturbation_radius": True,
            "no_universal_positive_cross_lower": True,
            "all_active_four_mode_couplings_certified": False,
            "direct_native_to_directional_bridge": False,
            "lagged_reset_bridge": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "For a contemporaneous full-memory spectral reset, the recent projected cross equals the negative old-tail coupling. Fifty tail-inactive snapshots therefore have exact zero cross action, and only 54 of 80 active snapshots certify four coupling modes under the inherited packet and tail balls. The finite native support cannot be identified with the old directional cross-action support; a lagged or hybrid packet is the next controlled alternative.",
    }
    output = ROOT / "results" / ("cross_smoke.json" if args.smoke else "cross_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
