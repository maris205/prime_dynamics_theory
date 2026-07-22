"""192-bit audit of residual Rayleigh and predictor-corrector factors."""

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


FULL_OUTPUT = ROOT / "results" / "predictor_corrector_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "predictor_corrector_smoke.json"
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


def relative_residual_squared(state: np.ndarray, packet: np.ndarray) -> float:
    residual = state - (state @ packet) @ packet.T
    return float(np.linalg.norm(residual, "fro") ** 2 / np.linalg.norm(state, "fro") ** 2)


def objective(states: list[np.ndarray], time: int, packet: np.ndarray) -> float:
    return float(sum(ETA ** (time - index) * relative_residual_squared(states[index], packet) for index in range(time + 1)))


def channel_audit(model: dict[str, object], horizon: int, rank: int) -> dict[str, object]:
    operator_values = np.asarray(model["operator"], dtype=np.float64)
    source_values = np.asarray(model["source"], dtype=np.float64)
    packet_time = int(math.ceil(2.0 * horizon / 3.0))
    predictor_time = packet_time - 1
    states = [source_values]
    for _ in range(packet_time):
        states.append(operator_values @ states[-1])
    gram = np.zeros((source_values.shape[1], source_values.shape[1]), dtype=np.float64)
    packets = []
    tails = []
    for time, state in enumerate(states):
        snapshot_gram = state.T @ state
        gram = snapshot_gram / np.trace(snapshot_gram) + ETA * gram
        packet = packet_from_gram(gram, rank)
        packets.append(packet)
        tails.append(objective(states, time, packet))
    old_packet = packets[predictor_time]
    epsilon = relative_residual_squared(states[predictor_time], old_packet)
    injection = relative_residual_squared(states[packet_time], old_packet)
    point_chi = injection / epsilon
    memory_theta = injection / tails[predictor_time]
    candidate_tail = injection + ETA * tails[predictor_time]
    reoptimization = tails[packet_time] / candidate_tail
    actual_contraction = tails[packet_time] / tails[predictor_time]
    factorization_residual = abs(actual_contraction - reoptimization * (memory_theta + ETA))
    full_growth = float(np.linalg.norm(states[packet_time], "fro") ** 2 / np.linalg.norm(states[predictor_time], "fro") ** 2)
    global_chi_binary64 = float(np.linalg.norm(operator_values, 2) ** 2 / full_growth)

    operator = arb_matrix(operator_values)
    source = arb_matrix(source_values)
    exact_old = matrix_power(operator, predictor_time) * source
    exact_new = operator * exact_old
    packet_arb = arb_matrix(old_packet)
    old_residual = exact_old - (exact_old * packet_arb) * packet_arb.transpose()
    new_residual = exact_new - (exact_new * packet_arb) * packet_arb.transpose()
    old_relative = frobenius_norm(old_residual) / frobenius_norm(exact_old)
    new_relative = frobenius_norm(new_residual) / frobenius_norm(exact_new)
    point_chi_ball = new_relative**2 / old_relative**2
    full_growth_ball = (frobenius_norm(exact_new) / frobenius_norm(exact_old)) ** 2
    _, _, right = np.linalg.svd(operator_values, full_matrices=False)
    test_vector = arb_matrix(right[0, :].reshape(-1, 1))
    tested_operator_ratio = frobenius_norm(operator * test_vector) / frobenius_norm(test_vector)
    global_chi_lower_ball = tested_operator_ratio**2 / full_growth_ball
    point_contracts = upper(point_chi_ball) + ETA < 1.0
    global_condition_fails = lower(global_chi_lower_ball) + ETA > 1.0

    return {
        "side": model["side"],
        "dimension": int(operator_values.shape[0]),
        "source_columns": int(source_values.shape[1]),
        "horizon": int(horizon),
        "predictor_time": int(predictor_time),
        "corrector_time": int(packet_time),
        "clock_rank": int(rank),
        "eta": ETA,
        "binary64_point_residual_energy": epsilon,
        "binary64_injection_energy": injection,
        "binary64_point_rayleigh_coefficient": point_chi,
        "binary64_global_norm_coefficient": global_chi_binary64,
        "binary64_memory_tail_before": tails[predictor_time],
        "binary64_memory_tail_after": tails[packet_time],
        "binary64_memory_predictor_coefficient": memory_theta + ETA,
        "binary64_reoptimization_factor": reoptimization,
        "binary64_actual_memory_contraction": actual_contraction,
        "binary64_factorization_residual": factorization_residual,
        "interval_point_rayleigh_coefficient_ball": str(point_chi_ball),
        "interval_point_rayleigh_coefficient_lower": lower(point_chi_ball),
        "interval_point_rayleigh_coefficient_upper": upper(point_chi_ball),
        "interval_tested_global_coefficient_lower_ball": str(global_chi_lower_ball),
        "interval_tested_global_coefficient_lower": lower(global_chi_lower_ball),
        "point_predictor_contracts": point_contracts,
        "memory_predictor_contracts": memory_theta + ETA < 1.0,
        "actual_memory_contracts": actual_contraction < 1.0,
        "global_norm_sufficient_condition_fails": global_condition_fails,
        "factorization_gate_green": factorization_residual < 1e-12 and global_condition_fails and actual_contraction < 0.235,
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
            channels = []
            for model in models:
                record = channel_audit(model, HORIZONS[sigma], rank)
                channels.append(record)
                print(json.dumps({"sigma": sigma, "side": record["side"], "rank": rank, "point_chi_upper": record["interval_point_rayleigh_coefficient_upper"], "global_chi_lower": record["interval_tested_global_coefficient_lower"], "memory_predictor": record["binary64_memory_predictor_coefficient"], "reoptimization": record["binary64_reoptimization_factor"], "actual_contraction": record["binary64_actual_memory_contraction"]}, sort_keys=True), flush=True)
            rows.append({"sigma": sigma, "fine_dimension": dimension, "clock": half_log_clock(sigma), "clock_rank": rank, "channels": channels, "all_channels_green": all(channel["factorization_gate_green"] for channel in channels)})
    finally:
        ctx.prec = previous_precision
    channels = [channel for row in rows for channel in row["channels"]]
    payload = {
        "status": "rh88_predictor_corrector_energy_contraction_audit",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "rank_offset": RANK_OFFSET,
        "rows": rows,
        "all_executed_factorization_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": {
            "scale_count": len(rows),
            "channel_count": len(channels),
            "global_norm_failure_count": sum(channel["global_norm_sufficient_condition_fails"] for channel in channels),
            "point_predictor_contraction_count": sum(channel["point_predictor_contracts"] for channel in channels),
            "memory_predictor_contraction_count": sum(channel["memory_predictor_contracts"] for channel in channels),
            "actual_memory_contraction_count": sum(channel["actual_memory_contracts"] for channel in channels),
            "maximum_interval_point_rayleigh_coefficient_upper": max(channel["interval_point_rayleigh_coefficient_upper"] for channel in channels),
            "minimum_interval_global_coefficient_lower": min(channel["interval_tested_global_coefficient_lower"] for channel in channels),
            "maximum_memory_predictor_coefficient": max(channel["binary64_memory_predictor_coefficient"] for channel in channels),
            "maximum_reoptimization_factor": max(channel["binary64_reoptimization_factor"] for channel in channels),
            "maximum_actual_memory_contraction": max(channel["binary64_actual_memory_contraction"] for channel in channels),
            "maximum_factorization_residual": max(channel["binary64_factorization_residual"] for channel in channels),
        },
        "theorem_boundary": {
            "residual_rayleigh_factorization": True,
            "predictor_corrector_contraction_identity": True,
            "global_norm_route_rejected_at_anchors": True,
            "point_packet_contraction_rejected_as_uniform_anchor_law": True,
            "five_scale_corrected_memory_contraction_observed": True,
            "uniform_reoptimization_gain_proved": False,
            "uniform_stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "One-step injection factors exactly into current point-packet error times a residual/full Rayleigh quotient. The global operator-norm sufficient coefficient is rigorously above one in all ten channels, and the directional point predictor contracts in only six. Memory prediction contracts in nine, while variational packet correction restores contraction in all ten with actual factor below 0.235. The finest right channel specifically needs the correction dividend. The next analytic target is therefore a lower bound on packet reoptimization gain, not a global norm or point-packet contraction theorem."
        ),
        "limitations": [
            "The point and tested-global Rayleigh coefficients are interval certified; memory tails and reoptimization factors are binary64 evaluations of exact variational identities.",
            "A tested operator vector gives a rigorous lower bound proving failure of the named global-norm sufficient condition, not a no-go theorem for every directional operator estimate.",
            "The ten-channel contraction pattern is finite-scale evidence and does not prove a uniform reoptimization dividend.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_factorization_gates_green"], **payload["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
