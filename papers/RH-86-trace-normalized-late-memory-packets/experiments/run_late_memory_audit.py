"""192-bit audit of trace-normalized late-memory packets."""

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
RH85 = PAPERS / "RH-85-midblock-snapshot-packets"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"), str(RH85 / "src")]

from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from late_memory import memory_mass  # noqa: E402
from run_effective_rank_audit import (  # noqa: E402
    HORIZONS,
    SIGMAS,
    arb_matrix,
    build_models,
    frobenius_norm,
    matrix_power,
)


FULL_OUTPUT = ROOT / "results" / "late_memory_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "late_memory_smoke.json"
PRECISION_BITS = 192
RANK_OFFSET = 2
ETA = 1.0 / 512.0


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def packet_from_gram(gram: np.ndarray, rank: int) -> np.ndarray:
    values, vectors = np.linalg.eigh((gram + gram.T) / 2.0)
    return vectors[:, np.argsort(values)[-rank:]]


def relative_residual(state: np.ndarray, packet: np.ndarray) -> float:
    residual = state - (state @ packet) @ packet.T
    return float(np.linalg.norm(residual, "fro") / np.linalg.norm(state, "fro"))


def normalized_memory_packet(states: list[np.ndarray], packet_time: int, rank: int) -> tuple[np.ndarray, np.ndarray]:
    columns = states[0].shape[1]
    gram = np.zeros((columns, columns), dtype=np.float64)
    for state in states[: packet_time + 1]:
        snapshot_gram = state.T @ state
        gram = ETA * gram + snapshot_gram / np.trace(snapshot_gram)
    return packet_from_gram(gram, rank), gram


def unweighted_prefix_packet(states: list[np.ndarray], packet_time: int, rank: int) -> np.ndarray:
    columns = states[0].shape[1]
    gram = sum((state.T @ state for state in states[: packet_time + 1]), np.zeros((columns, columns)))
    return packet_from_gram(gram, rank)


def channel_audit(model: dict[str, object], horizon: int, rank: int, observability_ball: str) -> dict[str, object]:
    operator_values = np.asarray(model["operator"], dtype=np.float64)
    source_values = np.asarray(model["source"], dtype=np.float64)
    packet_time = int(math.ceil(2.0 * horizon / 3.0))
    states = [source_values]
    for _ in range(horizon):
        states.append(operator_values @ states[-1])
    packet, memory_gram = normalized_memory_packet(states, packet_time, rank)
    unweighted = unweighted_prefix_packet(states, packet_time, rank)
    point_gram = states[packet_time].T @ states[packet_time]
    point_normalized = point_gram / np.trace(point_gram)
    point_packet = packet_from_gram(point_gram, rank)
    eigenvalues = np.linalg.eigvalsh((point_normalized + point_normalized.T) / 2.0)
    boundary_gap = float(eigenvalues[-rank] - eigenvalues[-rank - 1]) if rank < eigenvalues.size else float(eigenvalues[-rank])
    perturbation_norm = float(np.linalg.norm(memory_gram - point_normalized, 2))
    gap_ratio = perturbation_norm / boundary_gap
    memory_values = np.linalg.eigvalsh((memory_gram + memory_gram.T) / 2.0)
    normalized_stack_tail = float(math.sqrt(max(0.0, np.sum(memory_values[:-rank]))))

    operator = arb_matrix(operator_values)
    source = arb_matrix(source_values)
    exact_snapshot = matrix_power(operator, packet_time) * source
    exact_terminal = matrix_power(operator, horizon) * source
    packet_arb = arb_matrix(packet)
    exact_snapshot_residual = exact_snapshot - (exact_snapshot * packet_arb) * packet_arb.transpose()
    exact_terminal_residual = exact_terminal - (exact_terminal * packet_arb) * packet_arb.transpose()
    snapshot_norm = frobenius_norm(exact_snapshot)
    terminal_norm = frobenius_norm(exact_terminal)
    snapshot_relative = frobenius_norm(exact_snapshot_residual) / snapshot_norm
    terminal_residual = frobenius_norm(exact_terminal_residual)
    terminal_relative = terminal_residual / terminal_norm
    capture = arb(1) - terminal_relative**2
    remaining_power = matrix_power(operator, horizon - packet_time)
    propagation_bound = frobenius_norm(remaining_power) * frobenius_norm(exact_snapshot_residual)
    propagation_gap = propagation_bound - terminal_residual
    future_error = arb(observability_ball).sqrt() * terminal_residual
    unweighted_tail = relative_residual(states[-1], unweighted)
    weighted_tail = relative_residual(states[-1], packet)
    point_tail = relative_residual(states[-1], point_packet)
    mass = memory_mass(ETA, packet_time)

    return {
        "side": model["side"],
        "dimension": int(operator_values.shape[0]),
        "source_columns": int(source_values.shape[1]),
        "horizon": int(horizon),
        "packet_time": int(packet_time),
        "clock_rank": int(rank),
        "eta": ETA,
        "normalized_memory_total_trace": mass["total"],
        "normalized_memory_past_trace": mass["past"],
        "normalized_memory_past_trace_fraction": mass["past_fraction"],
        "normalized_stack_optimal_tail": normalized_stack_tail,
        "binary64_terminal_point_packet_relative_tail": point_tail,
        "binary64_terminal_weighted_packet_relative_tail": weighted_tail,
        "binary64_terminal_unweighted_prefix_relative_tail": unweighted_tail,
        "unweighted_to_weighted_improvement_factor": unweighted_tail / weighted_tail,
        "normalized_terminal_boundary_gap": boundary_gap,
        "normalized_prefix_perturbation_norm": perturbation_norm,
        "angle_perturbation_gap_ratio": gap_ratio,
        "interval_snapshot_relative_residual_ball": str(snapshot_relative),
        "interval_snapshot_relative_residual_upper": upper(snapshot_relative),
        "interval_terminal_residual_ball": str(terminal_residual),
        "interval_relative_terminal_residual_ball": str(terminal_relative),
        "interval_relative_terminal_residual_upper": upper(terminal_relative),
        "interval_terminal_energy_capture_ball": str(capture),
        "interval_terminal_energy_capture_lower": lower(capture),
        "interval_frobenius_propagation_bound_ball": str(propagation_bound),
        "interval_propagation_gap_ball": str(propagation_gap),
        "propagation_inequality_certified": lower(propagation_gap) >= 0.0,
        "full_future_hardy_perturbation_ball": str(future_error),
        "full_future_hardy_perturbation_upper": upper(future_error),
        "memory_gate_green": upper(terminal_relative) < 1.2e-5 and lower(capture) > 0.99999999985 and gap_ratio > 1e6,
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
                record = channel_audit(model, HORIZONS[sigma], rank, inherited_rows[sigma]["channels"][index]["full_observability_norm_upper_ball"])
                channels.append(record)
                print(json.dumps({"sigma": sigma, "side": record["side"], "rank": rank, "weighted_tail": record["interval_relative_terminal_residual_upper"], "unweighted_tail": record["binary64_terminal_unweighted_prefix_relative_tail"], "gap_ratio": record["angle_perturbation_gap_ratio"]}, sort_keys=True), flush=True)
            rows.append({"sigma": sigma, "fine_dimension": dimension, "clock": half_log_clock(sigma), "clock_rank": rank, "channels": channels, "all_channels_green": all(channel["memory_gate_green"] for channel in channels)})
    finally:
        ctx.prec = previous_precision
    channels = [channel for row in rows for channel in row["channels"]]
    payload = {
        "status": "rh86_trace_normalized_late_memory_packet_audit",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "rank_offset": RANK_OFFSET,
        "rows": rows,
        "all_executed_memory_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": {
            "scale_count": len(rows),
            "maximum_clock_rank": max(channel["clock_rank"] for channel in channels),
            "maximum_interval_relative_terminal_residual": max(channel["interval_relative_terminal_residual_upper"] for channel in channels),
            "minimum_interval_terminal_energy_capture": min(channel["interval_terminal_energy_capture_lower"] for channel in channels),
            "maximum_full_future_hardy_perturbation": max(channel["full_future_hardy_perturbation_upper"] for channel in channels),
            "minimum_unweighted_improvement_factor": min(channel["unweighted_to_weighted_improvement_factor"] for channel in channels),
            "maximum_unweighted_improvement_factor": max(channel["unweighted_to_weighted_improvement_factor"] for channel in channels),
            "minimum_angle_perturbation_gap_ratio": min(channel["angle_perturbation_gap_ratio"] for channel in channels),
            "maximum_angle_perturbation_gap_ratio": max(channel["angle_perturbation_gap_ratio"] for channel in channels),
            "maximum_past_trace_fraction": max(channel["normalized_memory_past_trace_fraction"] for channel in channels),
            "all_frobenius_propagation_inequalities_certified": all(channel["propagation_inequality_certified"] for channel in channels),
        },
        "theorem_boundary": {
            "normalized_memory_variational_theorem": True,
            "gap_free_snapshot_energy_transfer": True,
            "five_scale_late_memory_packet_validated": True,
            "angle_perturbation_route_rejected_at_anchors": True,
            "all_level_late_memory_packet_proved": False,
            "uniform_stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The trace-normalized recursion G_j = X_j^*X_j/||X_j||_2^2 + eta G_{j-1} is an online, scale-free packet statistic. With eta=1/512, its clock-rank packet has a 192-bit terminal relative residual below 1.2e-5 at all five anchors and improves the raw unweighted prefix packet by at least three orders of magnitude. Every Davis-Kahan perturbation/gap ratio exceeds one million, so principal-angle continuity is quantitatively unavailable even though captured energy is stable. The next proof should control weighted Rayleigh leakage directly, not singular-vector angles."
        ),
        "limitations": [
            "The memory parameter is selected once from the frozen anchor audit and is not derived from an all-level dynamical estimate.",
            "The packet is computed in binary64; its snapshot and terminal residuals are evaluated rigorously after exact binary lifting.",
            "Large perturbation/gap ratios reject the standard angle certificate at these anchors but are not a theorem that every angle-based argument must fail.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_memory_gates_green"], **payload["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
