"""Audit cost-minimal nested finite-memory certificates on five scales."""

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
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH77 / "experiments"),
    str(RH82 / "src"),
    str(RH94 / "src"),
    str(RH96 / "experiments"),
    str(RH101 / "src"),
]

from finite_memory_gram import normalized_snapshot  # noqa: E402
from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from memory_depth import (  # noqa: E402
    finite_history_tail_bound,
    first_certifying_depth,
    snapshot_action_cost,
    weyl_ratio_lower_bound,
)
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_weak_mode_quotient_audit import one_step  # noqa: E402
from source_seeded_refresh import source_right_packet  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "memory_depth_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "memory_depth_smoke.json"
PRECISION_BITS = 384
ETA = 1.0 / 512.0
RANK_OFFSET = 2
THRESHOLDS = (1e-8, 1e-6, 1e-4)
MONOTONE_TOLERANCE = 8e-14
DOMINANCE_TOLERANCE = 3e-12


def state_history(model: dict[str, object], endpoint: int) -> list[np.ndarray]:
    operator = np.asarray(model["operator"], dtype=float)
    source = np.asarray(model["source"], dtype=float)
    states = [source]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    return states


def weighted_gram(snapshots: list[np.ndarray], time: int, depth: int) -> np.ndarray:
    """Assemble every depth through one newest-to-oldest binary64 path."""
    used = min(int(depth), time + 1)
    gram = np.zeros_like(snapshots[time])
    for age in range(used):
        gram += ETA**age * snapshots[time - age]
    return (gram + gram.T) / 2.0


def projected_cross(gram: np.ndarray, packet: np.ndarray) -> np.ndarray:
    return gram @ packet - packet @ (packet.T @ gram @ packet)


def channel_audit(
    model: dict[str, object],
    sigma: float,
    threshold: float,
    rank: int,
) -> dict[str, object]:
    endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
    states = state_history(model, endpoint)
    snapshots = [normalized_snapshot(state) for state in states]
    packet = source_right_packet(states[0], rank)
    steps = []
    for time in range(1, endpoint + 1):
        history_length = time + 1
        full_gram = weighted_gram(snapshots, time, history_length)
        full_cross = projected_cross(full_gram, packet)
        full_singular = np.linalg.svd(full_cross, compute_uv=False)
        actual_ratio = float(full_singular[3] / full_singular[0])
        depths = []
        for depth in range(1, history_length + 1):
            recent_gram = weighted_gram(snapshots, time, depth)
            recent_cross = projected_cross(recent_gram, packet)
            recent_singular = np.linalg.svd(recent_cross, compute_uv=False)
            tail_bound = finite_history_tail_bound(ETA, depth, history_length)
            ratio_lower = weyl_ratio_lower_bound(recent_singular, tail_bound)
            actual_tail_norm = float(np.linalg.norm(full_cross - recent_cross, 2))
            depths.append(
                {
                    "depth": depth,
                    "tail_bound": tail_bound,
                    "actual_tail_cross_norm": actual_tail_norm,
                    "tail_enclosed": actual_tail_norm <= tail_bound + MONOTONE_TOLERANCE,
                    "leading_singular_value": float(recent_singular[0]),
                    "fourth_singular_value": float(recent_singular[3]),
                    "ratio_lower": ratio_lower,
                    "support_certified": ratio_lower >= threshold,
                    "dominance_holds": ratio_lower <= actual_ratio + DOMINANCE_TOLERANCE,
                    "snapshot_action_cost": snapshot_action_cost(depth, rank),
                }
            )
        first_depth = first_certifying_depth(
            ((entry["depth"], entry["ratio_lower"]) for entry in depths), threshold
        )
        monotone_failure_count = sum(
            right["ratio_lower"] + MONOTONE_TOLERANCE < left["ratio_lower"]
            for left, right in zip(depths, depths[1:])
        )
        raw_decrease_count = sum(
            right["ratio_lower"] < left["ratio_lower"] for left, right in zip(depths, depths[1:])
        )
        first_cost = snapshot_action_cost(first_depth, rank) if first_depth is not None else None
        full_cost = snapshot_action_cost(history_length, rank)
        steps.append(
            {
                "time": time,
                "threshold": threshold,
                "packet_rank": rank,
                "history_length": history_length,
                "actual_ratio": actual_ratio,
                "actual_support": actual_ratio >= threshold,
                "first_certifying_depth": first_depth,
                "certificate_found": first_depth is not None,
                "completeness_holds": (first_depth is not None) == (actual_ratio >= threshold),
                "minimum_depth_holds": first_depth is None
                or all(not entry["support_certified"] for entry in depths[: first_depth - 1]),
                "monotone_failure_count": monotone_failure_count,
                "raw_decrease_count": raw_decrease_count,
                "full_snapshot_action_cost": full_cost,
                "minimum_snapshot_action_cost": first_cost,
                "saved_snapshot_actions": full_cost - first_cost if first_cost is not None else None,
                "relative_cost": first_cost / full_cost if first_cost is not None else None,
                "depths": depths,
            }
        )
        packet, _ = one_step(full_gram, packet, threshold)
    return {
        "sigma": sigma,
        "side": model["side"],
        "threshold": threshold,
        "clock_rank": rank,
        "refresh_endpoint": endpoint,
        "steps": steps,
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
            rows.append(
                {
                    "sigma": sigma,
                    "clock": half_log_clock(sigma),
                    "clock_rank": rank,
                    "channels": channels,
                }
            )
            print(json.dumps({"sigma": sigma, "clock_rank": rank}, sort_keys=True), flush=True)
    finally:
        ctx.prec = previous_precision

    records = [
        (row["sigma"], record)
        for row in rows
        for channel in row["channels"]
        for record in channel["thresholds"]
    ]
    all_steps = [step for _, record in records for step in record["steps"]]
    all_depths = [depth for step in all_steps for depth in step["depths"]]
    threshold_summary = {}
    for threshold in THRESHOLDS:
        selected = [(sigma, record) for sigma, record in records if record["threshold"] == threshold]
        steps = [step for _, record in selected for step in record["steps"]]
        supported = [step for step in steps if step["actual_support"]]
        fine = [step for sigma, record in selected if sigma <= 0.02 for step in record["steps"]]
        certified_depths = [step["first_certifying_depth"] for step in supported]
        depth_histogram = {
            str(depth): sum(value == depth for value in certified_depths)
            for depth in sorted(set(certified_depths))
        }
        threshold_summary[f"{threshold:.0e}"] = {
            "threshold": threshold,
            "update_count": len(steps),
            "actual_support_count": len(supported),
            "adaptive_certificate_count": sum(step["certificate_found"] for step in steps),
            "fine_update_count": len(fine),
            "fine_certificate_count": sum(step["certificate_found"] for step in fine),
            "minimum_certifying_depth": min(certified_depths, default=None),
            "maximum_certifying_depth": max(certified_depths, default=None),
            "median_certifying_depth": float(np.median(certified_depths)) if certified_depths else None,
            "depth_histogram": depth_histogram,
            "mean_relative_cost": float(np.mean([step["relative_cost"] for step in supported])) if supported else None,
            "maximum_relative_cost": max((step["relative_cost"] for step in supported), default=None),
            "saved_snapshot_actions": sum(step["saved_snapshot_actions"] for step in supported),
        }
    max_depth = max(depth["depth"] for depth in all_depths)
    depth_envelope = [
        {
            "depth": depth,
            "infinite_tail_bound": ETA**depth / (1.0 - ETA),
            "certified_by_depth": sum(
                step["actual_support"]
                and step["first_certifying_depth"] is not None
                and step["first_certifying_depth"] <= depth
                for step in all_steps
            ),
            "eligible_supported_records": sum(
                step["actual_support"] and step["history_length"] >= depth for step in all_steps
            ),
        }
        for depth in range(1, max_depth + 1)
    ]
    supported_steps = [step for step in all_steps if step["actual_support"]]
    total_full_cost = sum(step["full_snapshot_action_cost"] for step in supported_steps)
    total_minimum_cost = sum(step["minimum_snapshot_action_cost"] for step in supported_steps)
    summary = {
        "scale_count": len(rows),
        "channel_count": sum(len(row["channels"]) for row in rows),
        "update_count": len(all_steps),
        "supported_update_count": len(supported_steps),
        "adaptive_certificate_count": sum(step["certificate_found"] for step in all_steps),
        "fine_update_count": sum(
            len(record["steps"]) for sigma, record in records if sigma <= 0.02
        ),
        "tail_enclosure_failure_count": sum(not depth["tail_enclosed"] for depth in all_depths),
        "dominance_failure_count": sum(not depth["dominance_holds"] for depth in all_depths),
        "monotone_failure_count": sum(step["monotone_failure_count"] for step in all_steps),
        "raw_floating_decrease_count": sum(step["raw_decrease_count"] for step in all_steps),
        "completeness_failure_count": sum(not step["completeness_holds"] for step in all_steps),
        "minimum_depth_failure_count": sum(not step["minimum_depth_holds"] for step in all_steps),
        "maximum_certifying_depth": max(
            step["first_certifying_depth"] for step in supported_steps
        ),
        "mean_relative_cost": float(np.mean([step["relative_cost"] for step in supported_steps])),
        "total_full_snapshot_actions": total_full_cost,
        "total_minimum_snapshot_actions": total_minimum_cost,
        "total_saved_snapshot_actions": sum(step["saved_snapshot_actions"] for step in supported_steps),
        "aggregate_cost_reduction": 1.0 - total_minimum_cost / total_full_cost,
    }
    payload = {
        "status": "rh116_monotone_memory_depth_optimization_audit",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "thresholds": list(THRESHOLDS),
        "rows": rows,
        "threshold_summary": threshold_summary,
        "depth_envelope": depth_envelope,
        "audit_summary": summary,
        "theorem_boundary": {
            "nested_weyl_lower_monotonicity": True,
            "first_passage_depth_is_cost_minimal": True,
            "finite_full_history_search_is_complete": True,
            "five_scale_adaptive_depth_audit_validated": not args.smoke,
            "all_level_uniform_depth_proved": False,
            "all_level_physical_support_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "For additive memory windows whose discarded budgets split one increment at a time, the Weyl fourth-mode ratio lower bound is monotone in depth. Consequently the first passing depth is the exact cost minimizer within this certificate family, and full-history enumeration is complete. The five-scale audit uses one Gram assembly path and tests every available depth; it does not infer an all-level uniform depth law."
        ),
        "limitations": [
            "Completeness concerns the nested Weyl certificate family, not every possible support argument.",
            "The depth distribution is a five-scale observation and is not an asymptotic theorem.",
            "No uniform Stage A, Hilbert--Polya, zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
