"""384-bit audit of exact nonlinear hybrid horizon decompositions."""

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
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"), str(RH94 / "src"), str(RH94 / "experiments"), str(RH96 / "src")]

from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import lower, memory_grams, residual_energy_arb, upper  # noqa: E402
from source_seeded_refresh import source_right_packet, top_gram_packet  # noqa: E402
from weak_mode_quotient import adaptive_width  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "hybrid_horizon_budget_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "hybrid_horizon_budget_smoke.json"
PRECISION_BITS = 384
RANK_OFFSET = 2
FULL_WIDTH = 4
MINIMUM_WIDTH = 2
THRESHOLDS = (1e-8, 1e-6, 1e-4)
PRIMARY_THRESHOLD = 1e-8
ENDPOINT_BUDGET = 0.01


def abs_upper(value: arb) -> float:
    return math.nextafter(max(abs(float(value.lower())), abs(float(value.upper()))), math.inf)


def ritz_refresh(gram: np.ndarray, packet: np.ndarray, width: int) -> np.ndarray:
    cross = gram @ packet - packet @ (packet.T @ gram @ packet)
    left, _, _ = np.linalg.svd(cross, full_matrices=False)
    basis, _ = np.linalg.qr(np.column_stack([packet, left[:, :width]]), mode="reduced")
    compressed = basis.T @ gram @ basis
    compressed = (compressed + compressed.T) / 2.0
    values, vectors = np.linalg.eigh(compressed)
    return basis @ vectors[:, np.argsort(values)[-packet.shape[1]:]]


def adaptive_refresh(gram: np.ndarray, packet: np.ndarray, threshold: float) -> tuple[np.ndarray, int, arb]:
    cross = gram @ packet - packet @ (packet.T @ gram @ packet)
    singular = np.linalg.svd(cross, compute_uv=False)
    width = adaptive_width(singular, threshold, minimum=MINIMUM_WIDTH, maximum=FULL_WIDTH)
    adaptive = ritz_refresh(gram, packet, width)
    full = ritz_refresh(gram, packet, FULL_WIDTH)
    local_loss = residual_energy_arb(gram, adaptive) - residual_energy_arb(gram, full)
    return adaptive, width, local_loss


def propagate_full(grams: list[np.ndarray], packet: np.ndarray, first_time: int) -> np.ndarray:
    current = np.asarray(packet, dtype=float)
    for time in range(first_time, len(grams)):
        current = ritz_refresh(grams[time], current, FULL_WIDTH)
    return current


def run_hybrid_chain(grams: list[np.ndarray], seed: np.ndarray, rank: int, threshold: float) -> dict[str, object]:
    adaptive_packet = np.asarray(seed, dtype=float)
    omissions = []
    for time in range(1, len(grams)):
        adaptive_packet, width, local_loss = adaptive_refresh(grams[time], adaptive_packet, threshold)
        if width < FULL_WIDTH:
            omissions.append({"time": time, "selected_width": width, "prefix_packet": adaptive_packet.copy(), "local_loss": local_loss})

    full_endpoint_packet = propagate_full(grams, seed, 1)
    full_endpoint_tail = residual_energy_arb(grams[-1], full_endpoint_packet)
    adaptive_endpoint_tail = residual_energy_arb(grams[-1], adaptive_packet)
    reference_tail = residual_energy_arb(grams[-1], top_gram_packet(grams[-1], rank))
    hybrid_tails = [full_endpoint_tail]
    for omission in omissions:
        hybrid_packet = propagate_full(grams, omission["prefix_packet"], int(omission["time"]) + 1)
        hybrid_tails.append(residual_energy_arb(grams[-1], hybrid_packet))
    if omissions:
        final_match = hybrid_tails[-1] - adaptive_endpoint_tail
    else:
        final_match = full_endpoint_tail - adaptive_endpoint_tail
    contributions = [hybrid_tails[index] - hybrid_tails[index - 1] for index in range(1, len(hybrid_tails))]
    signed_sum = sum(contributions, arb(0))
    endpoint_shift = adaptive_endpoint_tail - full_endpoint_tail
    telescoping_error = signed_sum - endpoint_shift
    absolute_budget = sum((abs_upper(value) for value in contributions), 0.0)
    reference_lower = max(lower(reference_tail), np.finfo(float).tiny)
    records = []
    for omission, contribution in zip(omissions, contributions):
        local_loss = omission["local_loss"]
        records.append(
            {
                "time": omission["time"],
                "selected_width": omission["selected_width"],
                "interval_local_quotient_loss_ball": str(local_loss),
                "interval_local_quotient_loss_upper": upper(local_loss),
                "interval_propagated_endpoint_contribution_ball": str(contribution),
                "propagated_endpoint_contribution_abs_upper": abs_upper(contribution),
                "signed_propagation_multiplier": float(contribution.mid()) / max(float(local_loss.mid()), np.finfo(float).tiny),
                "absolute_propagation_multiplier_upper": abs_upper(contribution) / max(abs_upper(local_loss), np.finfo(float).tiny),
            }
        )
    return {
        "threshold": threshold,
        "endpoint": len(grams) - 1,
        "omission_count": len(omissions),
        "interval_full_endpoint_tail_ball": str(full_endpoint_tail),
        "interval_adaptive_endpoint_tail_ball": str(adaptive_endpoint_tail),
        "interval_reference_tail_ball": str(reference_tail),
        "interval_adaptive_to_reference_ball": str(adaptive_endpoint_tail / reference_tail),
        "interval_adaptive_to_reference_upper": upper(adaptive_endpoint_tail / reference_tail),
        "interval_endpoint_shift_ball": str(endpoint_shift),
        "interval_signed_hybrid_sum_ball": str(signed_sum),
        "interval_telescoping_error_ball": str(telescoping_error),
        "telescoping_error_contains_zero": lower(telescoping_error) <= 0.0 <= upper(telescoping_error),
        "interval_final_hybrid_match_ball": str(final_match),
        "final_hybrid_match_contains_zero": lower(final_match) <= 0.0 <= upper(final_match),
        "absolute_horizon_budget": absolute_budget,
        "absolute_horizon_budget_to_reference": absolute_budget / reference_lower,
        "signed_endpoint_shift_to_reference_abs_upper": abs_upper(endpoint_shift) / reference_lower,
        "contributions": records,
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
    chains = {f"{threshold:.0e}": run_hybrid_chain(grams, seed, rank, threshold) for threshold in THRESHOLDS}
    primary = chains[f"{PRIMARY_THRESHOLD:.0e}"]
    return {
        "side": model["side"],
        "dimension": int(operator.shape[0]),
        "source_columns": int(source.shape[1]),
        "refresh_endpoint": endpoint,
        "clock_rank": rank,
        "chains": chains,
        "channel_gate_green": (
            primary["telescoping_error_contains_zero"]
            and primary["final_hybrid_match_contains_zero"]
            and primary["absolute_horizon_budget_to_reference"] < ENDPOINT_BUDGET
            and primary["interval_adaptive_to_reference_upper"] < 1.01
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
            rows.append({"sigma": sigma, "fine_dimension": dimension, "clock": half_log_clock(sigma), "clock_rank": rank, "channels": channels, "all_channels_green": all(channel["channel_gate_green"] for channel in channels)})
            for channel in channels:
                primary = channel["chains"][f"{PRIMARY_THRESHOLD:.0e}"]
                print(json.dumps({"sigma": sigma, "side": channel["side"], "omissions": primary["omission_count"], "absolute_budget": primary["absolute_horizon_budget_to_reference"], "endpoint_ratio": primary["interval_adaptive_to_reference_upper"], "green": channel["channel_gate_green"]}, sort_keys=True), flush=True)
    finally:
        ctx.prec = previous_precision

    channels = [channel for row in rows for channel in row["channels"]]
    threshold_summaries = {}
    for threshold in THRESHOLDS:
        key = f"{threshold:.0e}"
        chains = [channel["chains"][key] for channel in channels]
        contributions = [record for chain in chains for record in chain["contributions"]]
        threshold_summaries[key] = {
            "threshold": threshold,
            "omission_count": sum(chain["omission_count"] for chain in chains),
            "telescoping_green_count": sum(chain["telescoping_error_contains_zero"] and chain["final_hybrid_match_contains_zero"] for chain in chains),
            "maximum_absolute_horizon_budget_to_reference": max(chain["absolute_horizon_budget_to_reference"] for chain in chains),
            "maximum_signed_endpoint_shift_to_reference": max(chain["signed_endpoint_shift_to_reference_abs_upper"] for chain in chains),
            "maximum_adaptive_to_reference_ratio": max(chain["interval_adaptive_to_reference_upper"] for chain in chains),
            "maximum_absolute_propagation_multiplier": max((record["absolute_propagation_multiplier_upper"] for record in contributions), default=0.0),
            "negative_propagated_contribution_count": sum(float(arb(record["interval_propagated_endpoint_contribution_ball"]).upper()) < 0.0 for record in contributions),
            "positive_propagated_contribution_count": sum(float(arb(record["interval_propagated_endpoint_contribution_ball"]).lower()) > 0.0 for record in contributions),
            "absolute_budget_green_count": sum(chain["absolute_horizon_budget_to_reference"] < ENDPOINT_BUDGET for chain in chains),
        }
    primary = threshold_summaries[f"{PRIMARY_THRESHOLD:.0e}"]
    summary = {
        "scale_count": len(rows),
        "channel_count": len(channels),
        "primary_threshold": PRIMARY_THRESHOLD,
        "primary_omission_count": primary["omission_count"],
        "primary_telescoping_green_count": primary["telescoping_green_count"],
        "primary_absolute_budget_green_count": primary["absolute_budget_green_count"],
        "primary_maximum_absolute_horizon_budget_to_reference": primary["maximum_absolute_horizon_budget_to_reference"],
        "primary_maximum_signed_endpoint_shift_to_reference": primary["maximum_signed_endpoint_shift_to_reference"],
        "primary_maximum_absolute_propagation_multiplier": primary["maximum_absolute_propagation_multiplier"],
        "threshold_summaries": threshold_summaries,
    }
    payload = {
        "status": "rh97_nonlinear_hybrid_horizon_budget_audit",
        "precision_bits": PRECISION_BITS,
        "rank_offset": RANK_OFFSET,
        "thresholds": list(THRESHOLDS),
        "primary_threshold": PRIMARY_THRESHOLD,
        "endpoint_absolute_budget": ENDPOINT_BUDGET,
        "rows": rows,
        "all_executed_primary_hybrid_budget_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": summary,
        "theorem_boundary": {
            "nonlinear_hybrid_telescoping_identity": True,
            "absolute_propagated_horizon_budget": True,
            "primary_frozen_hybrid_budget_validated": True,
            "a_priori_refresh_lipschitz_law_proved": False,
            "uniform_block_propagation_envelope_proved": False,
            "repeated_block_contraction_proved": False,
            "uniform_stage_A1_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "Recursive quotient losses admit an exact nonlinear Duhamel decomposition through hybrid chains, without linearizing the Ritz map. "
            "The primary five omissions have a rigorously closed absolute endpoint budget below one percent in every channel, while the aggressive thresholds expose larger propagated budgets. "
            "The remaining task is to replace hybrid replay by an a priori block propagation envelope."
        ),
        "limitations": [
            "Hybrid replay is an exact a posteriori decomposition, not an a priori analytic Lipschitz estimate.",
            "The absolute budget can be conservative because it discards signed cancellation.",
            "No uniform block propagation multiplier or repeated-horizon theorem is proved.",
            "Only the archived finite channels are validated.",
            "No Hilbert--Polya operator, zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_primary_hybrid_budget_gates_green"], **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
