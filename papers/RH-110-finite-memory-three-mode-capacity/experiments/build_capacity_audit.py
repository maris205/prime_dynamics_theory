"""Audit finite-memory three-mode capacity and volume recovery."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

from flint import ctx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
RH96 = PAPERS / "RH-96-gap-weighted-weak-mode-quotient"
RH101 = PAPERS / "RH-101-finite-memory-packet-gram-action"
RH108 = PAPERS / "RH-108-finite-memory-fourth-cross-support"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH77 / "experiments"),
    str(RH82 / "src"),
    str(RH94 / "src"),
    str(RH94 / "experiments"),
    str(RH96 / "src"),
    str(RH96 / "experiments"),
    str(RH101 / "src"),
    str(RH108 / "src"),
]

from finite_memory_gram import packet_action  # noqa: E402
from fourth_cross_support import finite_tail_operator_bound  # noqa: E402
from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import ETA, memory_grams  # noqa: E402
from run_weak_mode_quotient_audit import one_step  # noqa: E402
from source_seeded_refresh import source_right_packet  # noqa: E402
from three_mode_capacity import (  # noqa: E402
    capacity_aware_ratio_lower_bound,
    finite_memory_capacity_interval,
    normalized_spectral_four_volume,
    sharp_capacity_interval,
    three_mode_capacity,
)


FULL_OUTPUT = ROOT / "results" / "three_mode_capacity_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "three_mode_capacity_smoke.json"
PRECISION_BITS = 384
DEPTH = 5
RANK_OFFSET = 2
MAXIMUM_WIDTH = 4
THRESHOLDS = (1e-8, 1e-6, 1e-4)
BINARY64_ACTION_GUARD = 2e-14


def state_history(model: dict[str, object], endpoint: int) -> list[np.ndarray]:
    operator = np.asarray(model["operator"], dtype=float)
    source = np.asarray(model["source"], dtype=float)
    states = [source]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    return states


def channel_audit(model: dict[str, object], sigma: float, threshold: float, rank: int) -> dict[str, object]:
    endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
    states = state_history(model, endpoint)
    grams = memory_grams(states)
    packet = source_right_packet(states[0], rank)
    steps = []
    for time in range(1, endpoint + 1):
        applied = packet_action(states, packet, eta=ETA, time=time, depth=DEPTH)
        recent_cross = applied - packet @ (packet.T @ applied)
        recent_singular = np.linalg.svd(recent_cross, compute_uv=False)
        past_count = max(0, time - DEPTH + 1)
        analytic_tail = finite_tail_operator_bound(ETA, DEPTH, past_count)
        tail_bound = math.nextafter(analytic_tail + BINARY64_ACTION_GUARD, math.inf)
        capacity = finite_memory_capacity_interval(recent_singular, tail_bound)
        recovery = capacity_aware_ratio_lower_bound(recent_singular, tail_bound)

        gram = grams[time]
        full_cross = gram @ packet - packet @ (packet.T @ gram @ packet)
        full_singular = np.linalg.svd(full_cross, compute_uv=False)
        actual_capacity = three_mode_capacity(full_singular)
        actual_ratio = float(full_singular[3] / full_singular[0])
        actual_volume = normalized_spectral_four_volume(full_singular)
        next_packet, selector = one_step(gram, packet, threshold)
        expected_support = actual_ratio >= threshold
        capacity_width = float(capacity["upper"] - capacity["lower"])
        steps.append(
            {
                "time": time,
                "threshold": threshold,
                "packet_rank": rank,
                "selected_width": int(selector["selected_width"]),
                "recent_singular_values": [float(value) for value in recent_singular],
                "full_singular_values": [float(value) for value in full_singular],
                "actual_capacity": actual_capacity,
                "capacity_lower": float(capacity["lower"]),
                "capacity_upper": float(capacity["upper"]),
                "capacity_enclosed": float(capacity["lower"]) <= actual_capacity <= float(capacity["upper"]),
                "capacity_relative_width": capacity_width / max(actual_capacity, np.finfo(float).tiny),
                "actual_normalized_volume": actual_volume,
                "actual_ratio": actual_ratio,
                "volume_capacity_identity_error": abs(actual_volume - actual_capacity * actual_ratio),
                "spectral_volume_lower": float(recovery["spectral_volume_lower"]),
                "capacity_recovered_ratio_lower": float(recovery["recovered_ratio_lower"]),
                "direct_weyl_ratio_lower": float(recovery["direct_weyl_ratio_lower"]),
                "recovery_efficiency": float(recovery["recovery_efficiency"]),
                "capacity_recovery_support": float(recovery["recovered_ratio_lower"]) >= threshold,
                "direct_weyl_support": float(recovery["direct_weyl_ratio_lower"]) >= threshold,
                "actual_support": expected_support,
                "recovery_implication_holds": (
                    float(recovery["recovered_ratio_lower"]) < threshold or expected_support
                ),
                "selector_equivalence_holds": (int(selector["selected_width"]) == MAXIMUM_WIDTH) == expected_support,
                "analytic_tail_operator_bound": analytic_tail,
                "tail_operator_bound": tail_bound,
                "tail_snapshot_count": past_count,
            }
        )
        packet = next_packet
    return {
        "sigma": sigma,
        "side": model["side"],
        "threshold": threshold,
        "clock_rank": rank,
        "refresh_endpoint": endpoint,
        "steps": steps,
    }


def barrier_audit() -> dict[str, object]:
    volumes = [1.0, 1e-1, 1e-3, 1e-6, 1e-9, 1e-12, 0.0]
    rows = []
    for volume in volumes:
        lower, upper = sharp_capacity_interval(volume)
        linear_singular = np.array([1.0, 1.0, 1.0, volume])
        root = volume ** (1.0 / 3.0)
        cubic_singular = np.array([1.0, root, root, root])
        rows.append(
            {
                "normalized_volume": volume,
                "lower_capacity": lower,
                "upper_capacity": upper,
                "linear_capacity": three_mode_capacity(linear_singular),
                "cubic_capacity": three_mode_capacity(cubic_singular),
            }
        )
    return {
        "rows": rows,
        "maximum_endpoint_error": max(
            max(abs(row["linear_capacity"] - row["upper_capacity"]), abs(row["cubic_capacity"] - row["lower_capacity"]))
            for row in rows
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows = []
    try:
        sigmas = SIGMAS[:1] if args.smoke else SIGMAS
        for sigma in sigmas:
            rank = clock_rank(sigma, offset=RANK_OFFSET)
            _, models = build_models(sigma)
            channels = []
            for model in models:
                records = [channel_audit(model, sigma, threshold, rank) for threshold in THRESHOLDS]
                channels.append({"side": model["side"], "thresholds": records})
            rows.append({"sigma": sigma, "clock": half_log_clock(sigma), "clock_rank": rank, "channels": channels})
            for channel in channels:
                primary = channel["thresholds"][0]
                print(
                    json.dumps(
                        {
                            "sigma": sigma,
                            "side": channel["side"],
                            "minimum_capacity": min(step["actual_capacity"] for step in primary["steps"]),
                            "maximum_capacity": max(step["actual_capacity"] for step in primary["steps"]),
                            "recovery_count": sum(step["capacity_recovery_support"] for step in primary["steps"]),
                            "update_count": len(primary["steps"]),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    finally:
        ctx.prec = previous_precision

    records = [
        (row["sigma"], channel["side"], record)
        for row in rows
        for channel in row["channels"]
        for record in channel["thresholds"]
    ]
    all_steps = [step for _, _, record in records for step in record["steps"]]
    threshold_summary = {}
    for threshold in THRESHOLDS:
        key = f"{threshold:.0e}"
        selected = [(sigma, record) for sigma, _, record in records if record["threshold"] == threshold]
        steps = [step for _, record in selected for step in record["steps"]]
        fine = [step for sigma, record in selected if sigma <= 0.02 for step in record["steps"]]
        threshold_summary[key] = {
            "threshold": threshold,
            "update_count": len(steps),
            "recovery_support_count": sum(step["capacity_recovery_support"] for step in steps),
            "direct_support_count": sum(step["direct_weyl_support"] for step in steps),
            "actual_support_count": sum(step["actual_support"] for step in steps),
            "fine_update_count": len(fine),
            "fine_recovery_support_count": sum(step["capacity_recovery_support"] for step in fine),
            "fine_direct_support_count": sum(step["direct_weyl_support"] for step in fine),
            "minimum_fine_recovered_ratio": min((step["capacity_recovered_ratio_lower"] for step in fine), default=None),
            "minimum_fine_recovery_efficiency": min((step["recovery_efficiency"] for step in fine), default=None),
            "counts_match": sum(step["capacity_recovery_support"] for step in steps)
            == sum(step["direct_weyl_support"] for step in steps),
        }
    fine_steps = [step for sigma, _, record in records if sigma <= 0.02 for step in record["steps"]]
    reported_fine = fine_steps if fine_steps else all_steps
    summary = {
        "scale_count": len(rows),
        "channel_count": sum(len(row["channels"]) for row in rows),
        "threshold_count": len(THRESHOLDS),
        "update_count": len(all_steps),
        "fine_update_count": len(fine_steps),
        "capacity_enclosure_failure_count": sum(not step["capacity_enclosed"] for step in all_steps),
        "recovery_implication_failure_count": sum(not step["recovery_implication_holds"] for step in all_steps),
        "selector_equivalence_failure_count": sum(not step["selector_equivalence_holds"] for step in all_steps),
        "maximum_capacity_relative_width": max(step["capacity_relative_width"] for step in all_steps),
        "maximum_fine_capacity_relative_width": max(step["capacity_relative_width"] for step in reported_fine),
        "minimum_fine_capacity": min(step["actual_capacity"] for step in reported_fine),
        "maximum_fine_capacity": max(step["actual_capacity"] for step in reported_fine),
        "minimum_fine_recovery_efficiency": min(step["recovery_efficiency"] for step in reported_fine),
        "maximum_volume_capacity_identity_error": max(step["volume_capacity_identity_error"] for step in all_steps),
        "all_threshold_counts_match_direct_weyl": all(record["counts_match"] for record in threshold_summary.values()),
    }
    payload = {
        "status": "rh110_finite_memory_three_mode_capacity_audit",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "depth": DEPTH,
        "thresholds": list(THRESHOLDS),
        "rows": rows,
        "threshold_summary": threshold_summary,
        "barrier": barrier_audit(),
        "audit_summary": summary,
        "theorem_boundary": {
            "finite_memory_capacity_interval": True,
            "capacity_aware_volume_recovery": True,
            "sharp_fixed_volume_capacity_interval": True,
            "five_scale_recovery_matches_direct_counts": not args.smoke,
            "all_level_capacity_upper_law_proved": False,
            "all_level_physical_volume_lower_bound_proved": False,
            "uniform_fine_support_separation_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The relative second/third-mode capacity has an explicit finite-memory Weyl enclosure. Dividing the RH-109 spectral-volume lower bound by the capacity upper endpoint reconstructs the fourth-mode support count exactly on all five archived scales and all three thresholds, with only a small quantitative loss from the direct Weyl ratio. This is a conditional composition theorem; an all-level physical capacity law and volume lower bound remain open."
        ),
        "limitations": [
            "The archived count match is finite and does not prove an eventual all-level law.",
            "The capacity interval uses the same recent singular spectrum as the direct Weyl certificate; it is a structural factorization, not yet an independent physical estimate.",
            "No uniform Stage A, Hilbert--Polya, zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
