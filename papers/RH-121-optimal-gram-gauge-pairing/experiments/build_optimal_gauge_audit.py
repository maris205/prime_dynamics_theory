"""Audit optimal exact-Gram gauges on phase-matched adjacent scales."""

from __future__ import annotations

import argparse
import itertools
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
RH110 = PAPERS / "RH-110-finite-memory-three-mode-capacity"
RH113 = PAPERS / "RH-113-right-frame-directional-wedge"
RH114 = PAPERS / "RH-114-psd-rayleigh-directional-tail"
sys.path[:0] = [
    str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"),
    str(RH94 / "src"), str(RH94 / "experiments"), str(RH96 / "src"),
    str(RH96 / "experiments"), str(RH101 / "src"), str(RH108 / "src"),
    str(RH110 / "src"), str(RH113 / "src"), str(RH114 / "src"),
]

from directional_wedge import top_right_frame  # noqa: E402
from finite_memory_gram import memory_grams, truncated_memory_gram  # noqa: E402
from fourth_cross_support import finite_tail_operator_bound  # noqa: E402
from half_log_rank import clock_rank  # noqa: E402
from optimal_gram_gauge import optimal_exact_gram_gauge  # noqa: E402
from psd_rayleigh_tail import positive_tail_cross_gram_upper, relative_tail_constant  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import ETA  # noqa: E402
from run_weak_mode_quotient_audit import one_step  # noqa: E402
from source_seeded_refresh import source_right_packet  # noqa: E402
from three_mode_capacity import finite_memory_capacity_interval  # noqa: E402


PRECISION_BITS = 384
DEPTH = 5
RANK_OFFSET = 2
THRESHOLDS = (1e-8, 1e-6, 1e-4)
PHASES = (0.25, 0.5, 0.75, 1.0)
ACTION_GUARD = 2e-14
ROUNDING_FACTOR = 96.0


def state_history(model: dict[str, object], endpoint: int) -> list[np.ndarray]:
    operator = np.asarray(model["operator"], dtype=float)
    states = [np.asarray(model["source"], dtype=float)]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    return states


def psd_upper(theoretical: np.ndarray, actual: np.ndarray) -> np.ndarray:
    difference = (theoretical - actual + theoretical.T - actual.T) / 2.0
    scale = max(float(np.linalg.norm(theoretical, 2)), float(np.linalg.norm(actual, 2)), np.finfo(float).tiny)
    correction = max(0.0, -float(np.linalg.eigvalsh(difference)[0])) + ROUNDING_FACTOR * np.finfo(float).eps * scale
    return (theoretical + theoretical.T) / 2.0 + correction * np.eye(4)


def phase_records(model: dict[str, object], sigma: float, threshold: float, rank: int) -> dict[float, dict[str, object]]:
    endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
    times = {phase: max(1, min(endpoint, int(round(phase * endpoint)))) for phase in PHASES}
    states = state_history(model, endpoint)
    full_grams = memory_grams(states, ETA)
    packet = source_right_packet(states[0], rank)
    records: dict[float, dict[str, object]] = {}
    for time in range(1, endpoint + 1):
        full_gram = full_grams[time]
        recent_gram = truncated_memory_gram(states, eta=ETA, time=time, depth=DEPTH)
        tail_gram = (full_gram - recent_gram + full_gram.T - recent_gram.T) / 2.0
        recent = recent_gram @ packet - packet @ (packet.T @ recent_gram @ packet)
        full = full_gram @ packet - packet @ (packet.T @ full_gram @ packet)
        residual = full - recent
        frame = top_right_frame(recent)
        action = recent @ frame
        residual_action = residual @ frame
        gram = action.T @ action
        gram = (gram + gram.T) / 2.0
        gram_scale = max(float(np.linalg.norm(gram, 2)), np.finfo(float).tiny)
        gram_floor = max(0.0, -float(np.linalg.eigvalsh(gram)[0])) + 1e-12 * gram_scale
        gram += gram_floor * np.eye(4)
        recent_singular = np.linalg.svd(recent, compute_uv=False)
        full_singular = np.linalg.svd(full, compute_uv=False)
        past_count = max(0, time - DEPTH + 1)
        analytic = finite_tail_operator_bound(ETA, DEPTH, past_count)
        delta = math.nextafter(max(analytic + ACTION_GUARD, float(np.linalg.norm(tail_gram, 2)) + ACTION_GUARD), math.inf)
        packet_block = frame.T @ packet.T @ tail_gram @ packet @ frame
        packet_block = (packet_block + packet_block.T) / 2.0
        block_scale = max(float(np.linalg.norm(packet_block, 2)), np.finfo(float).tiny)
        packet_block += (max(0.0, -float(np.linalg.eigvalsh(packet_block)[0])) + ROUNDING_FACTOR * np.finfo(float).eps * block_scale) * np.eye(4)
        tail = psd_upper(positive_tail_cross_gram_upper(packet_block, delta), residual_action.T @ residual_action)
        tail_scale = max(float(np.linalg.norm(tail, 2)), np.finfo(float).tiny)
        tail_floor = max(0.0, -float(np.linalg.eigvalsh(tail)[0])) + 1e-12 * tail_scale
        tail += tail_floor * np.eye(4)
        gamma = relative_tail_constant(gram, tail)
        leading = float(recent_singular[0] + delta)
        capacity = float(finite_memory_capacity_interval(recent_singular, delta)["upper"])
        volume = float(np.sqrt(max(0.0, np.linalg.det(gram))))
        directional = max(0.0, 1.0 - gamma) ** 4 * volume / leading**4 / capacity if leading and capacity else 0.0
        actual_ratio = float(full_singular[3] / full_singular[0]) if full_singular[0] else 0.0
        for phase, selected_time in times.items():
            if selected_time == time:
                records[phase] = {
                    "time": time, "gram": gram, "tail": tail, "gamma": gamma,
                    "gram_floor": gram_floor, "tail_floor": tail_floor,
                    "frame_volume": volume, "leading_upper": leading, "capacity_upper": capacity,
                    "directional_candidate": directional, "actual_ratio": actual_ratio,
                    "full_singular_values": full_singular[:4],
                }
        packet, _ = one_step(full_gram, packet, threshold)
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    sigmas = SIGMAS[:2] if args.smoke else SIGMAS
    thresholds = THRESHOLDS[:1] if args.smoke else THRESHOLDS
    sides = ("left",) if args.smoke else ("left", "right")
    previous = ctx.prec
    ctx.prec = PRECISION_BITS
    states: dict[tuple[float, str, float], dict[float, dict[str, object]]] = {}
    try:
        for sigma in sigmas:
            rank = clock_rank(sigma, offset=RANK_OFFSET)
            _, models = build_models(sigma)
            for model in models:
                if model["side"] not in sides:
                    continue
                for threshold in thresholds:
                    states[(sigma, str(model["side"]), threshold)] = phase_records(model, sigma, threshold, rank)
    finally:
        ctx.prec = previous
    pairs = []
    for source_sigma, target_sigma in zip(sigmas, sigmas[1:]):
        for side in sides:
            for threshold in thresholds:
                for phase in PHASES:
                    source = states[(source_sigma, side, threshold)][phase]
                    target = states[(target_sigma, side, threshold)][phase]
                    result = optimal_exact_gram_gauge(source["gram"], source["tail"], target["gram"], target["tail"])
                    alpha = np.asarray(result["source_spectrum"])
                    beta = np.asarray(result["target_spectrum"])
                    trial_factors = [float(np.max(beta / alpha[list(permutation)])) for permutation in itertools.permutations(range(4))]
                    scale = max(float(np.linalg.norm(target["gram"], 2)), 1.0)
                    pairs.append({
                        "pair_id": f"{source_sigma:.2f}-{target_sigma:.2f}:{side}:{threshold:.0e}:p{phase:.2f}",
                        "source_sigma": source_sigma, "target_sigma": target_sigma, "side": side,
                        "threshold": threshold, "phase": phase, "source_time": source["time"], "target_time": target["time"],
                        "source_gamma": source["gamma"], "target_gamma": target["gamma"],
                        "source_gram_floor": source["gram_floor"], "target_gram_floor": target["gram_floor"],
                        "source_tail_floor": source["tail_floor"], "target_tail_floor": target["tail_floor"],
                        "optimal_tail_factor": result["optimal_tail_factor"], "gamma_transfer_upper": result["gamma_upper"],
                        "gamma_transfer_efficiency": target["gamma"] / result["gamma_upper"] if result["gamma_upper"] else 1.0,
                        "source_relative_spectrum": [float(x) for x in result["source_spectrum"]],
                        "target_relative_spectrum": [float(x) for x in result["target_spectrum"]],
                        "matched_ratios": [float(x) for x in result["matched_ratios"]],
                        "gram_alignment_error": result["gram_alignment_error"],
                        "gram_alignment_holds": bool(result["gram_alignment_error"] <= 2e-9 * scale),
                        "tail_minimum_slack": result["tail_minimum_slack"],
                        "tail_dominance_holds": bool(result["tail_minimum_slack"] >= -2e-9 * max(float(np.linalg.norm(target["tail"], 2)), 1.0)),
                        "gamma_transfer_holds": bool(target["gamma"] <= result["gamma_upper"] + 2e-10),
                        "sampled_optimality_holds": bool(result["optimal_tail_factor"] <= min(trial_factors) + 2e-8 * max(1.0, min(trial_factors))),
                        "minimum_sampled_tail_factor": min(trial_factors),
                        "gauge_determinant": result["gauge_determinant"],
                        "source_frame_volume": source["frame_volume"], "target_frame_volume": target["frame_volume"],
                        "source_leading_upper": source["leading_upper"], "target_leading_upper": target["leading_upper"],
                        "source_capacity_upper": source["capacity_upper"], "target_capacity_upper": target["capacity_upper"],
                        "source_directional_candidate": source["directional_candidate"],
                        "target_directional_candidate": target["directional_candidate"],
                        "source_actual_ratio": source["actual_ratio"], "target_actual_ratio": target["actual_ratio"],
                        "source_full_singular_values": [float(x) for x in source["full_singular_values"]],
                        "target_full_singular_values": [float(x) for x in target["full_singular_values"]],
                    })
    summary = {
        "scale_count": len(sigmas), "pair_count": len(pairs),
        "gram_alignment_failure_count": sum(not p["gram_alignment_holds"] for p in pairs),
        "tail_dominance_failure_count": sum(not p["tail_dominance_holds"] for p in pairs),
        "gamma_transfer_failure_count": sum(not p["gamma_transfer_holds"] for p in pairs),
        "sampled_optimality_failure_count": sum(not p["sampled_optimality_holds"] for p in pairs),
        "contractive_tail_pair_count": sum(p["optimal_tail_factor"] < 1.0 for p in pairs),
        "nonexpansive_gamma_pair_count": sum(p["gamma_transfer_upper"] <= p["source_gamma"] for p in pairs),
        "subunit_target_gamma_count": sum(p["target_gamma"] < 1.0 for p in pairs),
        "minimum_optimal_tail_factor": min(p["optimal_tail_factor"] for p in pairs),
        "median_optimal_tail_factor": float(np.median([p["optimal_tail_factor"] for p in pairs])),
        "maximum_optimal_tail_factor": max(p["optimal_tail_factor"] for p in pairs),
        "minimum_gamma_transfer_efficiency": min(p["gamma_transfer_efficiency"] for p in pairs),
        "median_gamma_transfer_efficiency": float(np.median([p["gamma_transfer_efficiency"] for p in pairs])),
        "maximum_gamma_transfer_efficiency": max(p["gamma_transfer_efficiency"] for p in pairs),
    }
    payload = {
        "status": "rh121_optimal_gram_gauge_pairing_audit", "phases": list(PHASES), "pairs": pairs,
        "audit_summary": summary,
        "theorem_boundary": {
            "optimal_exact_gram_gauge_theorem": True, "generalized_eigenframe_matching": True,
            "five_scale_phase_pairing_audited": not args.smoke, "uniform_tail_inflation_proved": False,
            "all_level_physical_gauge_law_proved": False, "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False, "riemann_hypothesis": False,
        },
        "route_consequence": "Exact recent-Gram alignment has an explicit optimal gauge: match the ordered generalized tail eigenframes. Its least tail inflation is the maximum ordered eigenvalue ratio. The five-scale audit measures this intrinsic finite obstruction but does not turn its extrema into an all-level law.",
    }
    name = "optimal_gauge_smoke.json" if args.smoke else "optimal_gauge_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
