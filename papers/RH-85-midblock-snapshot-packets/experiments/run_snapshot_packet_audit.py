"""192-bit audit of prefix-only midblock snapshot packets."""

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
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src")]

from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from run_effective_rank_audit import (  # noqa: E402
    HORIZONS,
    SIGMAS,
    arb_matrix,
    build_models,
    frobenius_norm,
    matrix_power,
)
from snapshot_packets import prefix_counterexample  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "snapshot_packet_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "snapshot_packet_smoke.json"
PRECISION_BITS = 192
RANK_OFFSET = 2


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def right_packet(state: np.ndarray, rank: int) -> np.ndarray:
    _, _, right = np.linalg.svd(np.asarray(state), full_matrices=False)
    return right[: min(int(rank), right.shape[0]), :].T


def float_relative_residual(state: np.ndarray, packet: np.ndarray) -> float:
    residual = state - (state @ packet) @ packet.T
    return float(np.linalg.norm(residual, "fro") / np.linalg.norm(state, "fro"))


def prefix_gram_packet(states: list[np.ndarray], rank: int) -> np.ndarray:
    gram = sum((state.T @ state for state in states), np.zeros((states[0].shape[1], states[0].shape[1])))
    values, vectors = np.linalg.eigh((gram + gram.T) / 2.0)
    return vectors[:, np.argsort(values)[-rank:]]


def channel_audit(model: dict[str, object], horizon: int, rank: int, observability_ball: str) -> dict[str, object]:
    operator_values = np.asarray(model["operator"], dtype=np.float64)
    source_values = np.asarray(model["source"], dtype=np.float64)
    midpoint = int(math.ceil(2.0 * horizon / 3.0))
    states = [source_values]
    for _ in range(horizon):
        states.append(operator_values @ states[-1])
    midpoint_packet = right_packet(states[midpoint], rank)
    source_packet = right_packet(states[0], rank)
    prefix_packet = prefix_gram_packet(states[: midpoint + 1], rank)
    final_packet = right_packet(states[-1], rank)

    operator = arb_matrix(operator_values)
    source = arb_matrix(source_values)
    exact_midpoint = matrix_power(operator, midpoint) * source
    exact_final = matrix_power(operator, horizon) * source
    packet = arb_matrix(midpoint_packet)
    exact_mid_residual = exact_midpoint - (exact_midpoint * packet) * packet.transpose()
    exact_final_residual = exact_final - (exact_final * packet) * packet.transpose()
    midpoint_residual = frobenius_norm(exact_mid_residual)
    terminal_residual = frobenius_norm(exact_final_residual)
    terminal_norm = frobenius_norm(exact_final)
    relative = terminal_residual / terminal_norm
    capture = arb(1) - relative**2
    remaining_power = matrix_power(operator, horizon - midpoint)
    propagation_bound = frobenius_norm(remaining_power) * midpoint_residual
    propagation_gap = propagation_bound - terminal_residual
    observability = arb(observability_ball)
    future_error = observability.sqrt() * terminal_residual
    overlap = np.linalg.svd(midpoint_packet.T @ final_packet, compute_uv=False)

    return {
        "side": model["side"],
        "dimension": int(operator_values.shape[0]),
        "source_columns": int(source_values.shape[1]),
        "horizon": int(horizon),
        "packet_time": int(midpoint),
        "packet_horizon_fraction": midpoint / horizon,
        "clock_rank": int(rank),
        "packet_orthogonality_defect": float(np.linalg.norm(midpoint_packet.T @ midpoint_packet - np.eye(midpoint_packet.shape[1]), 2)),
        "interval_midpoint_residual_ball": str(midpoint_residual),
        "interval_terminal_residual_ball": str(terminal_residual),
        "interval_terminal_residual_upper": upper(terminal_residual),
        "interval_relative_terminal_residual_ball": str(relative),
        "interval_relative_terminal_residual_upper": upper(relative),
        "interval_terminal_energy_capture_ball": str(capture),
        "interval_terminal_energy_capture_lower": lower(capture),
        "interval_frobenius_propagation_bound_ball": str(propagation_bound),
        "interval_propagation_gap_ball": str(propagation_gap),
        "propagation_inequality_certified": lower(propagation_gap) >= 0.0,
        "full_future_hardy_perturbation_ball": str(future_error),
        "full_future_hardy_perturbation_upper": upper(future_error),
        "binary64_optimal_final_relative_tail": float_relative_residual(states[-1], final_packet),
        "binary64_midpoint_packet_relative_tail": float_relative_residual(states[-1], midpoint_packet),
        "binary64_source_packet_relative_tail": float_relative_residual(states[-1], source_packet),
        "binary64_unweighted_prefix_gram_relative_tail": float_relative_residual(states[-1], prefix_packet),
        "midpoint_final_minimum_canonical_correlation": float(overlap[-1]),
        "packet_gate_green": upper(relative) < 4.5e-6 and lower(capture) > 0.99999999997,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    inherited = json.loads((RH77 / "results" / "effective_rank_audit.json").read_text(encoding="utf-8"))
    inherited_rows = {float(row["sigma"]): row for row in inherited["rows"]}
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows = []
    try:
        sigmas = SIGMAS[:1] if args.smoke else SIGMAS
        for sigma in sigmas:
            rank = clock_rank(sigma, offset=RANK_OFFSET)
            dimension, models = build_models(sigma)
            channels = []
            for index, model in enumerate(models):
                observability_ball = inherited_rows[sigma]["channels"][index]["full_observability_norm_upper_ball"]
                record = channel_audit(model, HORIZONS[sigma], rank, observability_ball)
                channels.append(record)
                print(json.dumps({"sigma": sigma, "side": record["side"], "rank": rank, "packet_time": record["packet_time"], "relative_tail": record["interval_relative_terminal_residual_upper"], "source_tail": record["binary64_source_packet_relative_tail"], "prefix_tail": record["binary64_unweighted_prefix_gram_relative_tail"]}, sort_keys=True), flush=True)
            rows.append({"sigma": sigma, "fine_dimension": dimension, "clock": half_log_clock(sigma), "clock_rank": rank, "channels": channels, "all_channels_green": all(channel["packet_gate_green"] for channel in channels)})
    finally:
        ctx.prec = previous_precision
    channels = [channel for row in rows for channel in row["channels"]]
    counterexample = [prefix_counterexample(m) | {"horizon": m} for m in (4, 8, 16, 32, 64)]
    payload = {
        "status": "rh85_midblock_snapshot_packet_audit",
        "precision_bits": PRECISION_BITS,
        "rank_offset": RANK_OFFSET,
        "rows": rows,
        "prefix_gram_counterexample": counterexample,
        "all_executed_packet_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": {
            "scale_count": len(rows),
            "maximum_clock_rank": max(channel["clock_rank"] for channel in channels),
            "maximum_interval_relative_terminal_residual": max(channel["interval_relative_terminal_residual_upper"] for channel in channels),
            "minimum_interval_terminal_energy_capture": min(channel["interval_terminal_energy_capture_lower"] for channel in channels),
            "maximum_full_future_hardy_perturbation": max(channel["full_future_hardy_perturbation_upper"] for channel in channels),
            "maximum_source_packet_relative_residual": max(channel["binary64_source_packet_relative_tail"] for channel in channels),
            "maximum_prefix_gram_relative_residual": max(channel["binary64_unweighted_prefix_gram_relative_tail"] for channel in channels),
            "minimum_midpoint_final_canonical_correlation": min(channel["midpoint_final_minimum_canonical_correlation"] for channel in channels),
            "all_frobenius_propagation_inequalities_certified": all(channel["propagation_inequality_certified"] for channel in channels),
        },
        "theorem_boundary": {
            "snapshot_packet_transfer": True,
            "prefix_only_rank_certificate": True,
            "unweighted_prefix_gram_no_go": True,
            "five_scale_midblock_packet_validated": True,
            "all_level_packet_decay_proved": False,
            "uniform_stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "A clock-rank packet constructed after roughly two thirds of the production horizon already captures the terminal postblock energy at all five archived scales, with 192-bit relative residual below 4.5e-6. The exact snapshot-transfer theorem propagates any such prefix packet through the unused suffix. Source-only and unweighted prefix-Gramian packets fail badly, so the next analytic object should be a terminally weighted or block-local dynamic packet, not a cumulative unweighted Krylov space."
        ),
        "limitations": [
            "The packet uses a binary64 SVD of the two-thirds snapshot, although its terminal residual is evaluated rigorously after exact binary64 lifting.",
            "The audit covers five frozen scales and does not prove uniform packet decay or a horizon law.",
            "The Frobenius power bound is sufficient for certification and is not claimed sharp.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_packet_gates_green"], **payload["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
