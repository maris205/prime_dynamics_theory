"""Audit a stopped exact-hybrid quotient clock on the RH-96 chains."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

from flint import arb, ctx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
RH96 = PAPERS / "RH-96-gap-weighted-weak-mode-quotient"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH77 / "experiments"),
    str(RH82 / "src"),
    str(RH94 / "src"),
    str(RH94 / "experiments"),
    str(RH96 / "src"),
    str(RH96 / "experiments"),
]

from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import lower, memory_grams, residual_energy_arb, upper  # noqa: E402
from run_weak_mode_quotient_audit import one_step  # noqa: E402
from source_seeded_refresh import source_right_packet, top_gram_packet  # noqa: E402
from stopped_hybrid_clock import (  # noqa: E402
    certified_endpoint_upper,
    debit_fits,
    gate_slack,
    remaining_budget,
    stopped_allowance,
)


FULL_OUTPUT = ROOT / "results" / "stopped_hybrid_clock_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "stopped_hybrid_clock_smoke.json"
PRECISION_BITS = 384
RANK_OFFSET = 2
FULL_WIDTH = 4
THRESHOLDS = (1e-8, 1e-6, 1e-4)
PRIMARY_THRESHOLD = 1e-8
ENDPOINT_GATE = 1.01
SAFETY_FRACTION = 0.99


def abs_upper(value: arb) -> float:
    return math.nextafter(max(abs(float(value.lower())), abs(float(value.upper()))), math.inf)


def ritz_refresh(gram: np.ndarray, packet: np.ndarray, width: int) -> np.ndarray:
    cross = gram @ packet - packet @ (packet.T @ gram @ packet)
    left, _, _ = np.linalg.svd(cross, full_matrices=False)
    basis, _ = np.linalg.qr(np.column_stack([packet, left[:, :width]]), mode="reduced")
    compressed = basis.T @ gram @ basis
    compressed = (compressed + compressed.T) / 2.0
    values, vectors = np.linalg.eigh(compressed)
    return basis @ vectors[:, np.argsort(values)[-packet.shape[1] :]]


def propagate_full(grams: list[np.ndarray], packet: np.ndarray, first_time: int) -> np.ndarray:
    current = np.asarray(packet, dtype=float)
    for time in range(first_time, len(grams)):
        current = ritz_refresh(grams[time], current, FULL_WIDTH)
    return current


def unrestricted_chain(grams: list[np.ndarray], seed: np.ndarray, rank: int, threshold: float) -> dict[str, object]:
    packet = np.asarray(seed, dtype=float)
    omissions = 0
    for time in range(1, len(grams)):
        packet, record = one_step(grams[time], packet, threshold)
        omissions += int(record["omitted_width"] > 0)
    endpoint = residual_energy_arb(grams[-1], packet)
    reference = residual_energy_arb(grams[-1], top_gram_packet(grams[-1], rank))
    return {
        "omission_count": omissions,
        "interval_endpoint_tail_ball": str(endpoint),
        "interval_endpoint_to_reference_ball": str(endpoint / reference),
        "interval_endpoint_to_reference_upper": upper(endpoint / reference),
    }


def run_stopped_chain(grams: list[np.ndarray], seed: np.ndarray, rank: int, threshold: float) -> dict[str, object]:
    reference_packet = top_gram_packet(grams[-1], rank)
    reference_tail = residual_energy_arb(grams[-1], reference_packet)
    full_endpoint_packet = propagate_full(grams, seed, 1)
    full_endpoint_tail = residual_energy_arb(grams[-1], full_endpoint_packet)
    reference_lower = max(lower(reference_tail), np.finfo(float).tiny)
    baseline_upper = upper(full_endpoint_tail)
    slack = gate_slack(reference_lower, baseline_upper, ENDPOINT_GATE)
    allowance = stopped_allowance(
        reference_lower,
        baseline_upper,
        gate=ENDPOINT_GATE,
        safety_fraction=SAFETY_FRACTION,
    )

    current = np.asarray(seed, dtype=float)
    spent = 0.0
    events = []
    accepted_hybrid_tails = [full_endpoint_tail]
    stopped = False
    stop_time = None
    stop_reason = None
    final_packet: np.ndarray | None = None

    for time in range(1, len(grams)):
        adaptive_packet, local = one_step(grams[time], current, threshold)
        full_packet = ritz_refresh(grams[time], current, FULL_WIDTH)
        if int(local["omitted_width"]) == 0:
            current = full_packet
            continue

        baseline_candidate_packet = propagate_full(grams, full_packet, time + 1)
        quotient_candidate_packet = propagate_full(grams, adaptive_packet, time + 1)
        baseline_candidate_tail = residual_energy_arb(grams[-1], baseline_candidate_packet)
        quotient_candidate_tail = residual_energy_arb(grams[-1], quotient_candidate_packet)
        contribution = quotient_candidate_tail - baseline_candidate_tail
        debit = abs_upper(contribution)
        continuity_error = baseline_candidate_tail - accepted_hybrid_tails[-1]
        local_green = bool(local["gap_certificate_green"])
        fits = debit_fits(spent, debit, allowance)
        accepted = local_green and fits
        event = {
            "time": time,
            "selected_width": int(local["selected_width"]),
            "local_gap_certificate_green": local_green,
            "local_gap_weighted_tail_loss_bound": float(local["gap_weighted_tail_loss_bound"]),
            "interval_local_quotient_loss_ball": local["interval_actual_tail_loss_ball"],
            "interval_baseline_hybrid_tail_ball": str(baseline_candidate_tail),
            "interval_candidate_hybrid_tail_ball": str(quotient_candidate_tail),
            "interval_propagated_contribution_ball": str(contribution),
            "propagated_debit_abs_upper": debit,
            "interval_hybrid_continuity_error_ball": str(continuity_error),
            "hybrid_continuity_error_contains_zero": lower(continuity_error) <= 0.0 <= upper(continuity_error),
            "spent_before": spent,
            "remaining_before": remaining_budget(allowance, spent),
            "debit_fits": fits,
            "accepted": accepted,
        }
        if accepted:
            spent = math.nextafter(spent + debit, math.inf)
            event["spent_after"] = spent
            event["remaining_after"] = remaining_budget(allowance, spent)
            current = adaptive_packet
            accepted_hybrid_tails.append(quotient_candidate_tail)
            events.append(event)
            continue

        event["spent_after"] = spent
        event["remaining_after"] = remaining_budget(allowance, spent)
        events.append(event)
        stopped = True
        stop_time = time
        stop_reason = "local_gap_certificate" if not local_green else "endpoint_allowance"
        final_packet = baseline_candidate_packet
        break

    if final_packet is None:
        final_packet = current

    final_tail = residual_energy_arb(grams[-1], final_packet)
    endpoint_shift = final_tail - full_endpoint_tail
    signed_sum = sum(
        (arb(event["interval_propagated_contribution_ball"]) for event in events if event["accepted"]),
        arb(0),
    )
    telescoping_error = signed_sum - endpoint_shift
    certified_upper = certified_endpoint_upper(baseline_upper, spent)
    certified_ratio = math.nextafter(certified_upper / reference_lower, math.inf)
    actual_ratio = final_tail / reference_tail
    unrestricted = unrestricted_chain(grams, seed, rank, threshold)
    return {
        "threshold": threshold,
        "endpoint": len(grams) - 1,
        "interval_reference_tail_ball": str(reference_tail),
        "interval_full_endpoint_tail_ball": str(full_endpoint_tail),
        "interval_full_endpoint_to_reference_ball": str(full_endpoint_tail / reference_tail),
        "interval_full_endpoint_to_reference_upper": upper(full_endpoint_tail / reference_tail),
        "gate_slack_lower": slack,
        "stopped_allowance": allowance,
        "safety_fraction": SAFETY_FRACTION,
        "candidate_count_before_stop": len(events),
        "accepted_quotient_count": sum(event["accepted"] for event in events),
        "rejected_quotient_count": sum(not event["accepted"] for event in events),
        "stopped": stopped,
        "stop_time": stop_time,
        "stop_reason": stop_reason,
        "spent_budget": spent,
        "remaining_budget": remaining_budget(allowance, spent),
        "interval_final_endpoint_tail_ball": str(final_tail),
        "interval_final_endpoint_to_reference_ball": str(actual_ratio),
        "interval_final_endpoint_to_reference_upper": upper(actual_ratio),
        "certified_endpoint_upper": certified_upper,
        "certified_endpoint_to_reference_upper": certified_ratio,
        "interval_endpoint_shift_ball": str(endpoint_shift),
        "interval_signed_accepted_hybrid_sum_ball": str(signed_sum),
        "interval_telescoping_error_ball": str(telescoping_error),
        "telescoping_error_contains_zero": lower(telescoping_error) <= 0.0 <= upper(telescoping_error),
        "all_hybrid_continuity_errors_contain_zero": all(event["hybrid_continuity_error_contains_zero"] for event in events),
        "all_accepted_local_gap_certificates_green": all(
            event["local_gap_certificate_green"] for event in events if event["accepted"]
        ),
        "endpoint_gate_green": upper(actual_ratio) < ENDPOINT_GATE and certified_ratio < ENDPOINT_GATE,
        "events": events,
        "unrestricted": unrestricted,
    }


def channel_audit(model: dict[str, object], inherited_horizon: int, rank: int) -> dict[str, object]:
    operator = np.asarray(model["operator"], dtype=float)
    source = np.asarray(model["source"], dtype=float)
    endpoint = max(4, int(math.ceil(2.0 * inherited_horizon / 3.0)))
    states = [source]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    grams = memory_grams(states)
    seed = source_right_packet(source, rank)
    chains = {f"{threshold:.0e}": run_stopped_chain(grams, seed, rank, threshold) for threshold in THRESHOLDS}
    return {
        "side": model["side"],
        "dimension": int(operator.shape[0]),
        "source_columns": int(source.shape[1]),
        "refresh_endpoint": endpoint,
        "clock_rank": rank,
        "chains": chains,
        "all_threshold_clocks_green": all(
            chain["endpoint_gate_green"]
            and chain["telescoping_error_contains_zero"]
            and chain["all_hybrid_continuity_errors_contain_zero"]
            and chain["all_accepted_local_gap_certificates_green"]
            for chain in chains.values()
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
            dimension, models = build_models(sigma)
            channels = [channel_audit(model, HORIZONS[sigma], rank) for model in models]
            rows.append(
                {
                    "sigma": sigma,
                    "fine_dimension": dimension,
                    "clock": half_log_clock(sigma),
                    "clock_rank": rank,
                    "channels": channels,
                    "all_threshold_clocks_green": all(channel["all_threshold_clocks_green"] for channel in channels),
                }
            )
            for channel in channels:
                print(
                    json.dumps(
                        {
                            "sigma": sigma,
                            "side": channel["side"],
                            "chains": {
                                key: {
                                    "accepted": chain["accepted_quotient_count"],
                                    "stopped": chain["stopped"],
                                    "stop_time": chain["stop_time"],
                                    "final_ratio": chain["interval_final_endpoint_to_reference_upper"],
                                    "unrestricted_ratio": chain["unrestricted"]["interval_endpoint_to_reference_upper"],
                                }
                                for key, chain in channel["chains"].items()
                            },
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    finally:
        ctx.prec = previous_precision

    channels = [channel for row in rows for channel in row["channels"]]
    threshold_summary = {}
    for threshold in THRESHOLDS:
        key = f"{threshold:.0e}"
        chains = [channel["chains"][key] for channel in channels]
        events = [event for chain in chains for event in chain["events"]]
        threshold_summary[key] = {
            "threshold": threshold,
            "candidate_count_before_stop": sum(chain["candidate_count_before_stop"] for chain in chains),
            "accepted_quotient_count": sum(chain["accepted_quotient_count"] for chain in chains),
            "rejected_quotient_count": sum(chain["rejected_quotient_count"] for chain in chains),
            "stopped_channel_count": sum(chain["stopped"] for chain in chains),
            "endpoint_green_count": sum(chain["endpoint_gate_green"] for chain in chains),
            "unrestricted_endpoint_green_count": sum(
                chain["unrestricted"]["interval_endpoint_to_reference_upper"] < ENDPOINT_GATE for chain in chains
            ),
            "maximum_final_endpoint_to_reference_ratio": max(
                chain["interval_final_endpoint_to_reference_upper"] for chain in chains
            ),
            "maximum_certified_endpoint_to_reference_ratio": max(
                chain["certified_endpoint_to_reference_upper"] for chain in chains
            ),
            "maximum_unrestricted_endpoint_to_reference_ratio": max(
                chain["unrestricted"]["interval_endpoint_to_reference_upper"] for chain in chains
            ),
            "maximum_spent_fraction_of_allowance": max(
                chain["spent_budget"] / max(chain["stopped_allowance"], np.finfo(float).tiny) for chain in chains
            ),
            "negative_accepted_contribution_count": sum(
                event["accepted"] and float(arb(event["interval_propagated_contribution_ball"]).upper()) < 0.0
                for event in events
            ),
            "positive_accepted_contribution_count": sum(
                event["accepted"] and float(arb(event["interval_propagated_contribution_ball"]).lower()) > 0.0
                for event in events
            ),
        }
    primary = threshold_summary[f"{PRIMARY_THRESHOLD:.0e}"]
    summary = {
        "scale_count": len(rows),
        "channel_count": len(channels),
        "primary_threshold": PRIMARY_THRESHOLD,
        "primary_accepted_quotient_count": primary["accepted_quotient_count"],
        "primary_stopped_channel_count": primary["stopped_channel_count"],
        "all_threshold_endpoint_green_count": sum(
            chain["endpoint_gate_green"] for channel in channels for chain in channel["chains"].values()
        ),
        "all_threshold_chain_count": len(channels) * len(THRESHOLDS),
        "threshold_summary": threshold_summary,
    }
    payload = {
        "status": "rh102_stopped_hybrid_quotient_clock_audit",
        "precision_bits": PRECISION_BITS,
        "rank_offset": RANK_OFFSET,
        "thresholds": list(THRESHOLDS),
        "primary_threshold": PRIMARY_THRESHOLD,
        "endpoint_gate": ENDPOINT_GATE,
        "safety_fraction": SAFETY_FRACTION,
        "rows": rows,
        "all_executed_stopped_clock_gates_green": all(row["all_threshold_clocks_green"] for row in rows),
        "audit_summary": summary,
        "theorem_boundary": {
            "stopped_hybrid_budget_theorem": True,
            "exact_accepted_hybrid_telescoping": True,
            "gap_certificate_and_endpoint_debit_clock_composed": True,
            "all_frozen_threshold_endpoint_gates_certified": True,
            "hybrid_replay_removed": False,
            "uniform_gap_aware_quotient_law_proved": False,
            "uniform_stage_A_closed": False,
            "moving_cloud_A5_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "limitations": [
            "Each proposed quotient still requires an exact full-suffix hybrid replay to price its endpoint debit.",
            "The clock guarantees a finite endpoint gate but does not prove a scale-uniform supply of admissible quotient updates.",
            "Stopping at the first unaffordable debit is conservative and can reject later harmless or cancelling quotients.",
            "The audit covers five frozen scales and two channels.",
            "No Stage A, moving-cloud, Hilbert--Polya, zero-identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    payload["route_consequence"] = (
        "Exact hybrid replay can be organized as a stopped debit clock rather than an unrestricted adaptive chain. "
        "Every accepted quotient has a local gap certificate and an exact propagated endpoint price; the process switches permanently to full width before the next debit would exhaust the channel's rigorous 1.01 gate slack. "
        "This closes the stopped-horizon logic on the frozen channels while leaving hybrid replay and the all-level quotient supply open."
    )
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
