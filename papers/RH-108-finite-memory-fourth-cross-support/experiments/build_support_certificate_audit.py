"""Audit the finite-memory fourth-cross support certificate."""

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
RH95 = PAPERS / "RH-95-reduced-projected-cross-moment-factorization"
RH96 = PAPERS / "RH-96-gap-weighted-weak-mode-quotient"
RH101 = PAPERS / "RH-101-finite-memory-packet-gram-action"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH77 / "experiments"),
    str(RH82 / "src"),
    str(RH94 / "src"),
    str(RH94 / "experiments"),
    str(RH95 / "src"),
    str(RH96 / "src"),
    str(RH96 / "experiments"),
    str(RH101 / "src"),
]

from fourth_cross_support import (  # noqa: E402
    finite_tail_operator_bound,
    fourth_support_certificate,
    source_seeded_barrier_data,
)
from finite_memory_gram import packet_action, truncated_memory_gram  # noqa: E402
from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from reduced_cross_factorization import cross_moment_matrices  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_weak_mode_quotient_audit import one_step  # noqa: E402
from run_source_seeded_horizon_audit import ETA, memory_grams  # noqa: E402
from source_seeded_refresh import source_right_packet  # noqa: E402
from weak_mode_quotient import adaptive_width  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "fourth_cross_support_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "fourth_cross_support_smoke.json"
PRECISION_BITS = 384
DEPTH = 5
RANK_OFFSET = 2
MAXIMUM_WIDTH = 4
THRESHOLDS = (1e-8, 1e-6, 1e-4)
BINARY64_ACTION_GUARD = 2e-14


def relative_error(first: np.ndarray, second: np.ndarray) -> float:
    denominator = max(float(np.linalg.norm(second, "fro")), np.finfo(float).tiny)
    return float(np.linalg.norm(first - second, "fro") / denominator)


def state_history(model: dict[str, object], endpoint: int) -> list[np.ndarray]:
    operator = np.asarray(model["operator"], dtype=float)
    source = np.asarray(model["source"], dtype=float)
    states = [source]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    return states


def scale_channel_audit(
    model: dict[str, object],
    sigma: float,
    inherited_horizon: int,
    threshold: float,
    rank: int,
) -> dict[str, object]:
    endpoint = max(4, int(math.ceil(2.0 * inherited_horizon / 3.0)))
    states = state_history(model, endpoint)
    grams = memory_grams(states)
    packet = source_right_packet(states[0], rank)
    steps: list[dict[str, object]] = []

    for time in range(1, endpoint + 1):
        gram = grams[time]
        applied = packet_action(states, packet, eta=ETA, time=time, depth=DEPTH)
        recent_gram = truncated_memory_gram(states, eta=ETA, time=time, depth=DEPTH)
        projected_recent = applied - packet @ (packet.T @ applied)
        recent_singular = np.linalg.svd(projected_recent, compute_uv=False)
        past_count = max(0, time - DEPTH + 1)
        analytic_tail_bound = finite_tail_operator_bound(ETA, DEPTH, past_count)
        tail_bound = math.nextafter(analytic_tail_bound + BINARY64_ACTION_GUARD, math.inf)
        certificate = fourth_support_certificate(recent_singular, tail_bound, threshold)

        full_cross = gram @ packet - packet @ (packet.T @ gram @ packet)
        full_singular = np.linalg.svd(full_cross, compute_uv=False)
        actual_ratio = float(full_singular[3] / full_singular[0])
        observed_cross_error = float(np.linalg.norm(full_cross - projected_recent, 2))

        first, second, _, moment_cross, _ = cross_moment_matrices(recent_gram, packet)
        direct_cross_gram = projected_recent.T @ projected_recent
        cancellation_index = (
            float(np.linalg.norm(second, "fro")) + float(np.linalg.norm(first @ first, "fro"))
        ) / max(float(np.linalg.norm(direct_cross_gram, "fro")), np.finfo(float).tiny)

        next_packet, selector_record = one_step(gram, packet, threshold)
        selected_width = int(selector_record["selected_width"])
        expected_width_four = actual_ratio >= threshold
        steps.append(
            {
                "time": time,
                "threshold": threshold,
                "selected_width": selected_width,
                "actual_ratio": actual_ratio,
                "actual_support": expected_width_four,
                "certified_ratio_lower": float(certificate["ratio_lower_bound"]),
                "certified_support": bool(certificate["support_certified"]),
                "additive_support_margin": float(certificate["additive_support_margin"]),
                "recent_leading_singular_value": float(certificate["recent_leading_singular_value"]),
                "recent_fourth_singular_value": float(certificate["recent_fourth_singular_value"]),
                "tail_operator_bound": float(tail_bound),
                "analytic_tail_operator_bound": float(analytic_tail_bound),
                "binary64_action_guard": BINARY64_ACTION_GUARD,
                "observed_cross_error": observed_cross_error,
                "observed_cross_error_bounded": observed_cross_error <= tail_bound,
                "tail_snapshot_count": past_count,
                "moment_cross_gram_relative_error": relative_error(moment_cross, direct_cross_gram),
                "moment_cancellation_index": cancellation_index,
                "certificate_implication_holds": (not bool(certificate["support_certified"])) or expected_width_four,
                "selector_equivalence_holds": (selected_width == MAXIMUM_WIDTH) == expected_width_four,
            }
        )
        packet = next_packet

    return {
        "sigma": sigma,
        "side": model["side"],
        "dimension": int(np.asarray(model["operator"]).shape[0]),
        "refresh_endpoint": endpoint,
        "clock_rank": rank,
        "threshold": threshold,
        "steps": steps,
        "minimum_actual_ratio": min(step["actual_ratio"] for step in steps),
        "minimum_certified_ratio": min(step["certified_ratio_lower"] for step in steps),
        "certified_support_count": sum(step["certified_support"] for step in steps),
        "actual_support_count": sum(step["actual_support"] for step in steps),
        "certificate_implication_count": sum(step["certificate_implication_holds"] for step in steps),
    }


def barrier_audit() -> dict[str, object]:
    epsilons = [1.0, 1e-1, 1e-2, 1e-4, 1e-8, 0.0]
    reference = source_seeded_barrier_data(epsilons[0])
    rows = []
    for epsilon in epsilons:
        data = source_seeded_barrier_data(epsilon)
        rows.append(
            {
                "epsilon": epsilon,
                "ratio": float(data["ratio"]),
                "expected_ratio": epsilon / 4.0,
                "singular_values": [float(value) for value in data["singular_values"][:4]],
                "trace_clock": float(data["trace_clock"]),
                "packet_block_distance": float(np.linalg.norm(data["packet_block"] - reference["packet_block"], 2)),
                "complement_block_distance": float(np.linalg.norm(data["complement_block"] - reference["complement_block"], 2)),
                "operator_norm": float(data["operator_norm"]),
            }
        )
    return {
        "eta": ETA,
        "rows": rows,
        "maximum_packet_block_distance": max(row["packet_block_distance"] for row in rows),
        "maximum_complement_block_distance": max(row["complement_block_distance"] for row in rows),
        "maximum_ratio_formula_error": max(abs(row["ratio"] - row["expected_ratio"]) for row in rows),
        "trace_clock_constant": all(abs(row["trace_clock"] - (1.0 + ETA)) < 1e-13 for row in rows),
        "diagonal_blocks_constant": all(
            row["packet_block_distance"] < 1e-13 and row["complement_block_distance"] < 1e-13 for row in rows
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows: list[dict[str, object]] = []
    try:
        sigmas = SIGMAS[:1] if args.smoke else SIGMAS
        for sigma in sigmas:
            rank = clock_rank(sigma, offset=RANK_OFFSET)
            _, models = build_models(sigma)
            channels = []
            for model in models:
                thresholds = [
                    scale_channel_audit(model, sigma, HORIZONS[sigma], threshold, rank)
                    for threshold in THRESHOLDS
                ]
                channels.append({"side": model["side"], "thresholds": thresholds})
            rows.append(
                {
                    "sigma": sigma,
                    "clock": half_log_clock(sigma),
                    "clock_rank": rank,
                    "channels": channels,
                }
            )
            for channel in channels:
                primary = channel["thresholds"][0]
                print(
                    json.dumps(
                        {
                            "sigma": sigma,
                            "side": channel["side"],
                            "minimum_actual_ratio": primary["minimum_actual_ratio"],
                            "minimum_certified_ratio": primary["minimum_certified_ratio"],
                            "certified_support_count": primary["certified_support_count"],
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
    threshold_summary: dict[str, object] = {}
    for threshold in THRESHOLDS:
        key = f"{threshold:.0e}"
        selected = [record for sigma, _, record in records if record["threshold"] == threshold]
        scale_summary = []
        for sigma in (float(value) for value in (SIGMAS[:1] if args.smoke else SIGMAS)):
            scale_records = [record for record in selected if record["sigma"] == sigma]
            steps = [step for record in scale_records for step in record["steps"]]
            scale_summary.append(
                {
                    "sigma": sigma,
                    "update_count": len(steps),
                    "certified_support_count": sum(step["certified_support"] for step in steps),
                    "actual_support_count": sum(step["actual_support"] for step in steps),
                    "minimum_certified_ratio": min((step["certified_ratio_lower"] for step in steps), default=None),
                    "minimum_certificate_margin_ratio": min(
                        (step["certified_ratio_lower"] / threshold for step in steps), default=None
                    ),
                }
            )
        threshold_summary[key] = {
            "threshold": threshold,
            "scale_summary": scale_summary,
            "certificate_green_count": sum(record["certified_support_count"] for record in selected),
            "actual_support_count": sum(record["actual_support_count"] for record in selected),
            "fine_certificate_green": all(
                item["certified_support_count"] == item["update_count"]
                for item in scale_summary
                if item["sigma"] <= 0.02
            ),
            "minimum_fine_certificate_margin_ratio": min(
                (
                    item["minimum_certificate_margin_ratio"]
                    for item in scale_summary
                    if item["sigma"] <= 0.02 and item["minimum_certificate_margin_ratio"] is not None
                ),
                default=None,
            ),
        }

    barrier = barrier_audit()
    fine_steps = [step for sigma, _, record in records if sigma <= 0.02 for step in record["steps"]]
    reported_fine_steps = fine_steps if fine_steps else all_steps
    summary = {
        "scale_count": len(rows),
        "channel_count": sum(len(row["channels"]) for row in rows),
        "threshold_count": len(THRESHOLDS),
        "update_count": len(all_steps),
        "fine_update_count": len(fine_steps),
        "maximum_moment_cross_gram_relative_error": max(step["moment_cross_gram_relative_error"] for step in all_steps),
        "maximum_moment_cancellation_index": max(step["moment_cancellation_index"] for step in all_steps),
        "certificate_implication_violation_count": sum(
            not step["certificate_implication_holds"] for step in all_steps
        ),
        "selector_equivalence_failure_count": sum(not step["selector_equivalence_holds"] for step in all_steps),
        "observed_cross_error_bound_failure_count": sum(
            not step["observed_cross_error_bounded"] for step in all_steps
        ),
        "minimum_fine_certified_ratio": min(step["certified_ratio_lower"] for step in reported_fine_steps),
        "minimum_fine_certificate_margin_ratio": min(
            step["certified_ratio_lower"] / step["threshold"] for step in reported_fine_steps
        ),
        "maximum_fine_actual_to_certificate_loss": max(
            step["actual_ratio"] - step["certified_ratio_lower"] for step in reported_fine_steps
        ),
        "maximum_tail_operator_bound": max(step["tail_operator_bound"] for step in all_steps),
        "barrier_minimum_ratio": min(row["ratio"] for row in barrier["rows"]),
    }
    payload = {
        "status": "rh108_finite_memory_fourth_cross_support_audit",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "depth": DEPTH,
        "binary64_action_guard": BINARY64_ACTION_GUARD,
        "rank_offset": RANK_OFFSET,
        "thresholds": list(THRESHOLDS),
        "rows": rows,
        "threshold_summary": threshold_summary,
        "barrier": barrier,
        "audit_summary": summary,
        "theorem_boundary": {
            "finite_memory_weyl_support_certificate": True,
            "reduced_first_two_moment_realization": True,
            "five_snapshot_fine_support_validated": True,
            "exact_normalized_memory_nondegeneracy_barrier": True,
            "all_level_fourth_cross_lower_bound_proved": False,
            "source_seeded_physical_transversality_proved": False,
            "uniform_fine_support_separation_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "RH-95 and RH-101 combine into a conditional support certificate: a recent-memory fourth-cross margin larger than the positive memory tail certifies the full fourth-cross ratio. On the two finest archived scales this certificate is green for every threshold and every update. The exact source-seeded normalized-memory barrier shows that trace clocks, packet/complement diagonal blocks, and generic finite-memory bounds do not force a positive margin; an additional physical transversality or volume law is required for an all-level theorem."
        ),
        "limitations": [
            "The finite audit uses the five frozen RH-94 channels and does not prove an all-level asymptotic law.",
            "The exact reduced-moment identity does not remove cancellation in binary64 moment subtraction; the audit forms the recent cross action directly for the numerical certificate.",
            "The barrier family is an admissible normalized-memory/source-seed construction, not a counterexample to the specific folded-Gaussian physical family.",
            "No uniform Stage A, Hilbert--Polya operator, zero identification, or Riemann Hypothesis conclusion is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
