"""Common-assembly, floor-free audit of the RH-121/RH-125 packet."""

from __future__ import annotations

import argparse
import collections
import json
import math
from pathlib import Path
import sys

import mpmath as mp
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
RH96 = PAPERS / "RH-96-gap-weighted-weak-mode-quotient"
RH108 = PAPERS / "RH-108-finite-memory-fourth-cross-support"
RH110 = PAPERS / "RH-110-finite-memory-three-mode-capacity"
RH113 = PAPERS / "RH-113-right-frame-directional-wedge"
sys.path[:0] = [
    str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"),
    str(RH94 / "src"), str(RH94 / "experiments"), str(RH96 / "src"),
    str(RH96 / "experiments"), str(RH108 / "src"), str(RH110 / "src"),
    str(RH113 / "src"),
]

from directional_wedge import top_right_frame  # noqa: E402
from fourth_cross_support import finite_tail_operator_bound  # noqa: E402
from half_log_rank import clock_rank  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import ETA  # noqa: E402
from run_weak_mode_quotient_audit import one_step  # noqa: E402
from semidefinite_directional import fp_supported_rank  # noqa: E402
from source_seeded_refresh import source_right_packet  # noqa: E402
from three_mode_capacity import finite_memory_capacity_interval  # noqa: E402


DEPTH = 5
RANK_OFFSET = 2
THRESHOLDS = (1e-8, 1e-6, 1e-4)
PHASES = (0.25, 0.5, 0.75, 1.0)
MP_DPS = 90
FP_MULTIPLIER = 128.0


def mp_number(value: object) -> mp.mpf:
    if isinstance(value, np.longdouble):
        return mp.mpf(np.format_float_scientific(value, unique=False, precision=35))
    return mp.mpf(repr(float(value)))


def mp_matrix(value: np.ndarray) -> mp.matrix:
    array = np.asarray(value)
    return mp.matrix([[mp_number(array[i, j]) for j in range(array.shape[1])] for i in range(array.shape[0])])


def mp_gram(action: np.ndarray) -> mp.matrix:
    a = mp_matrix(action)
    return a.T * a


def mp_relative_spectrum(gram: mp.matrix, tail: mp.matrix) -> list[mp.mpf]:
    lower = mp.cholesky(gram)
    inverse = lower**-1
    relative = inverse * tail * inverse.T
    relative = (relative + relative.T) / 2
    values, _ = mp.eigsy(relative)
    raw = sorted(mp.mpf(values[i]) for i in range(values.rows))
    scale = max([abs(value) for value in raw] + [mp.mpf("1")])
    zero_tolerance = mp.power(10, -(MP_DPS - 20)) * scale
    return [mp.mpf("0") if abs(value) <= zero_tolerance else max(mp.mpf("0"), value) for value in raw]


def finite_or_log(value: mp.mpf) -> dict[str, object]:
    if not mp.isfinite(value):
        return {"value": None, "log10": None, "infinite": True}
    if value <= 0:
        return {"value": 0.0, "log10": None, "infinite": False}
    log_value = mp.log10(value)
    as_float = float(value) if -300 < log_value < 300 else None
    return {"value": as_float, "log10": float(log_value), "infinite": False}


def ordered_semidefinite_factor(alpha: list[mp.mpf], beta: list[mp.mpf]) -> mp.mpf:
    """Least ordered factor, allowing zero source eigenvalues."""
    ratios: list[mp.mpf] = []
    for source, target in zip(alpha, beta):
        if source == 0:
            if target > 0:
                return mp.inf
            continue
        ratios.append(target / source)
    return max(ratios, default=mp.mpf("0"))


def normalized_snapshot(state: np.ndarray) -> np.ndarray:
    values = np.asarray(state, dtype=float)
    scale = np.sum(values * values, dtype=float)
    gram = values.T @ values / scale
    return (gram + gram.T) / 2.0


def state_history(model: dict[str, object], endpoint: int) -> list[np.ndarray]:
    operator = np.asarray(model["operator"], dtype=float)
    states = [np.asarray(model["source"], dtype=float)]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    return states


def direct_memory_parts(states: list[np.ndarray], time: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    width = states[time].shape[1]
    recent = np.zeros((width, width), dtype=float)
    tail = np.zeros_like(recent)
    for age in range(time + 1):
        term = ETA**age * normalized_snapshot(states[time - age])
        if age < DEPTH:
            recent += term
        else:
            tail += term
    return recent, tail, recent + tail


def projected_cross(gram: np.ndarray, packet: np.ndarray) -> np.ndarray:
    p = np.asarray(packet, dtype=float)
    applied = gram @ p
    return applied - p @ (p.T @ applied)


def phase_records(model: dict[str, object], sigma: float, threshold: float, rank: int) -> dict[float, dict[str, object]]:
    endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
    selected = {phase: max(1, min(endpoint, int(round(phase * endpoint)))) for phase in PHASES}
    states = state_history(model, endpoint)
    packet = source_right_packet(np.asarray(states[0], dtype=float), rank)
    records: dict[float, dict[str, object]] = {}
    for time in range(1, endpoint + 1):
        recent_gram, tail_gram, full_gram = direct_memory_parts(states, time)
        recent_cross = projected_cross(recent_gram, packet)
        frame = top_right_frame(np.asarray(recent_cross, dtype=float))
        action = recent_cross @ np.asarray(frame, dtype=float)
        tail_cross = projected_cross(tail_gram, packet)
        residual_action = tail_cross @ np.asarray(frame, dtype=float)
        packet_frame = np.asarray(packet, dtype=float) @ np.asarray(frame, dtype=float)
        block = packet_frame.T @ tail_gram @ packet_frame
        block = (block + block.T) / 2.0
        past_count = max(0, time - DEPTH + 1)
        delta = mp.mpf(repr(float(finite_tail_operator_bound(ETA, DEPTH, past_count))))
        gram_mp = mp_gram(action)
        block_mp = mp_matrix(block)
        tail_mp = delta * block_mp
        residual_mp = mp_gram(residual_action)
        residual_slack_values, _ = mp.eigsy((tail_mp - residual_mp + (tail_mp - residual_mp).T) / 2)
        spectrum = mp_relative_spectrum(gram_mp, tail_mp)
        gamma = mp.sqrt(max(mp.mpf("0"), spectrum[-1]))
        volume = mp.sqrt(max(mp.mpf("0"), mp.det(gram_mp)))
        recent_singular = np.linalg.svd(np.asarray(recent_cross, dtype=float), compute_uv=False)
        leading = mp.mpf(repr(float(recent_singular[0]))) + delta
        capacity = mp.mpf(repr(float(finite_memory_capacity_interval(recent_singular, float(delta))["upper"])))
        factor = max(mp.mpf("0"), 1 - gamma) ** 4
        candidate = factor * volume / leading**4 / capacity if leading > 0 and capacity > 0 else mp.mpf("0")
        fp = fp_supported_rank(np.asarray(action, dtype=float), FP_MULTIPLIER)
        singular = [mp.sqrt(max(mp.mpf("0"), x)) for x in mp.eigsy(gram_mp)[0]]
        singular = sorted(singular, reverse=True)
        condition = singular[0] / singular[-1] if singular[-1] > 0 else mp.inf
        for phase, chosen_time in selected.items():
            if chosen_time == time:
                records[phase] = {
                    "time": time,
                    "relative_spectrum_mp": spectrum,
                    "gamma_mp": gamma,
                    "volume_mp": volume,
                    "candidate_mp": candidate,
                    "leading": float(leading),
                    "capacity": float(capacity),
                    "fp64_supported_rank": fp["rank"],
                    "fp64_support_radius": fp["radius"],
                    "singular_values_mp": singular,
                    "condition_log10": float(mp.log10(condition)),
                    "residual_tail_slack": float(residual_slack_values[0]),
                }
        packet, _ = one_step(np.asarray(full_gram, dtype=float), packet, threshold)
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    mp.mp.dps = MP_DPS
    sigmas = SIGMAS[:2] if args.smoke else SIGMAS
    thresholds = THRESHOLDS[:1] if args.smoke else THRESHOLDS
    sides = ("left",) if args.smoke else ("left", "right")
    states: dict[tuple[float, str, float], dict[float, dict[str, object]]] = {}
    for sigma in sigmas:
        rank = clock_rank(sigma, offset=RANK_OFFSET)
        _, models = build_models(sigma)
        for model in models:
            if model["side"] not in sides:
                continue
            for threshold in thresholds:
                states[(sigma, str(model["side"]), threshold)] = phase_records(model, sigma, threshold, rank)
        print(json.dumps({"assembled_sigma": sigma, "state_groups": len(states)}, sort_keys=True), flush=True)

    state_rows = []
    for (sigma, side, threshold), phases in states.items():
        for phase, record in phases.items():
            row = {
                "state_id": f"{sigma:.2f}:{side}:{threshold:.0e}:p{phase:.2f}",
                "sigma": sigma, "side": side, "threshold": threshold, "phase": phase,
                "time": record["time"], "exact_discrete_rank": 4,
                "fp64_supported_rank": record["fp64_supported_rank"],
                "fp64_support_radius": record["fp64_support_radius"],
                "condition_log10": record["condition_log10"],
                "relative_spectrum": [finite_or_log(x) for x in record["relative_spectrum_mp"]],
                "gamma": finite_or_log(record["gamma_mp"]),
                "frame_volume": finite_or_log(record["volume_mp"]),
                "directional_candidate": finite_or_log(record["candidate_mp"]),
                "leading_upper": record["leading"], "capacity_upper": record["capacity"],
                "minimum_tail_dominance_slack": record["residual_tail_slack"],
            }
            state_rows.append(row)

    pairs = []
    for source_sigma, target_sigma in zip(sigmas, sigmas[1:]):
        for side in sides:
            for threshold in thresholds:
                for phase in PHASES:
                    source = states[(source_sigma, side, threshold)][phase]
                    target = states[(target_sigma, side, threshold)][phase]
                    alpha = source["relative_spectrum_mp"]
                    beta = target["relative_spectrum_mp"]
                    factor = ordered_semidefinite_factor(alpha, beta)
                    gamma_upper = mp.inf if not mp.isfinite(factor) else mp.sqrt(factor) * source["gamma_mp"]
                    determinant = target["volume_mp"] / source["volume_mp"]
                    lower = mp.mpf("0") if not mp.isfinite(gamma_upper) else (
                        max(mp.mpf("0"), 1 - gamma_upper) ** 4
                        * source["volume_mp"] * determinant
                        / mp.mpf(repr(target["leading"])) ** 4
                        / mp.mpf(repr(target["capacity"]))
                    )
                    pairs.append({
                        "pair_id": f"{source_sigma:.2f}-{target_sigma:.2f}:{side}:{threshold:.0e}:p{phase:.2f}",
                        "source_sigma": source_sigma, "target_sigma": target_sigma,
                        "side": side, "threshold": threshold, "phase": phase,
                        "source_fp64_rank": source["fp64_supported_rank"],
                        "target_fp64_rank": target["fp64_supported_rank"],
                        "optimal_tail_factor": finite_or_log(factor),
                        "gamma_transfer_upper": finite_or_log(gamma_upper),
                        "target_lower": finite_or_log(lower),
                        "target_candidate": finite_or_log(target["candidate_mp"]),
                        "positive_transfer": bool(lower > 0),
                    })

    grouped: dict[tuple[str, float, float], list[dict[str, object]]] = collections.defaultdict(list)
    for pair in pairs:
        grouped[(str(pair["side"]), float(pair["threshold"]), float(pair["phase"]))].append(pair)
    chains = []
    for key, rows in grouped.items():
        rows.sort(key=lambda row: float(row["source_sigma"]), reverse=True)
        positive = all(bool(row["positive_transfer"]) for row in rows)
        terminal_log = rows[-1]["target_lower"]["log10"] if positive else None
        chains.append({
            "side": key[0], "threshold": key[1], "phase": key[2],
            "edge_count": len(rows), "all_edges_positive": positive,
            "terminal_one_step_lower_log10": terminal_log,
            "all_states_fp64_rank_four": all(int(row["source_fp64_rank"]) == 4 and int(row["target_fp64_rank"]) == 4 for row in rows),
        })

    state_rank_counts = collections.Counter(int(row["fp64_supported_rank"]) for row in state_rows)
    summary = {
        "scale_count": len(sigmas), "state_count": len(state_rows), "pair_count": len(pairs),
        "chain_count": len(chains), "exact_discrete_rank_four_count": len(state_rows),
        "fp64_supported_rank_counts": {str(k): v for k, v in sorted(state_rank_counts.items())},
        "maximum_condition_log10": max(row["condition_log10"] for row in state_rows),
        "subunit_floor_free_gamma_count": sum(row["gamma"]["value"] is not None and row["gamma"]["value"] < 1.0 for row in state_rows),
        "positive_floor_free_candidate_count": sum(row["directional_candidate"]["value"] not in (None, 0.0) for row in state_rows),
        "positive_transfer_count": sum(pair["positive_transfer"] for pair in pairs),
        "infinite_tail_factor_count": sum(pair["optimal_tail_factor"]["infinite"] for pair in pairs),
        "finite_superunit_gamma_transfer_count": sum(
            (not pair["gamma_transfer_upper"]["infinite"])
            and pair["gamma_transfer_upper"]["value"] is not None
            and pair["gamma_transfer_upper"]["value"] >= 1.0
            for pair in pairs
        ),
        "positive_chain_count": sum(chain["all_edges_positive"] for chain in chains),
        "fp64_rank_four_chain_count": sum(chain["all_states_fp64_rank_four"] for chain in chains),
        "minimum_tail_dominance_slack": min(row["minimum_tail_dominance_slack"] for row in state_rows),
    }
    payload = {
        "status": "rh130_floor_free_semidefinite_directional_audit",
        "precision_decimal_digits": MP_DPS,
        "common_assembly": True,
        "positive_gram_floor": 0.0,
        "positive_tail_floor": 0.0,
        "state_rows": state_rows, "pairs": pairs, "chains": chains,
        "audit_summary": summary,
        "theorem_boundary": {
            "floor_free_common_assembly_completed": not args.smoke,
            "exact_discrete_action_rank_distinguished_from_fp64_supported_rank": True,
            "artificial_positive_gram_floor_removed": True,
            "four_directional_chain_survives_floor_removal": bool(summary["positive_chain_count"] == len(chains)),
            "physical_all_level_recurrence_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "A common extended-precision assembly removes the RH-121 conditioning floor and separates exact rank in the frozen discrete model from directions certifiable at fp64 scale. The resulting floor-free Rayleigh and transfer counts decide whether the previous regularized chains represented genuine four-directional support.",
    }
    name = "floor_free_smoke.json" if args.smoke else "floor_free_audit.json"
    output = ROOT / "results" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
