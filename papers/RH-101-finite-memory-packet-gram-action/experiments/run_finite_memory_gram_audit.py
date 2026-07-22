"""Audit finite-memory packet actions on the RH-94 frozen prefix."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

from flint import arb, arb_mat, ctx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"), str(RH94 / "src")]

from finite_memory_gram import (  # noqa: E402
    memory_grams,
    packet_action,
    packet_action_tail_bound,
    projected_cross_from_action,
    tail_trace_bound,
)
from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, arb_matrix, build_models  # noqa: E402
from source_seeded_refresh import projector_distance, source_right_packet, top_gram_packet  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "finite_memory_gram_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "finite_memory_gram_smoke.json"
PRECISION_BITS = 384
ETA = 1.0 / 512.0
RANK_OFFSET = 2
WIDTH = 4
DEPTHS = (2, 3, 4, 5, 6, 7, 8)
ENDPOINT_RATIO_TARGET = 1.01


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def trace(matrix: arb_mat) -> arb:
    return sum((matrix[index, index] for index in range(min(matrix.nrows(), matrix.ncols()))), arb(0))


def residual_energy_arb(gram: np.ndarray, packet: np.ndarray) -> arb:
    exact_gram = arb_matrix(gram)
    exact_packet = arb_matrix(packet)
    captured = exact_packet.transpose() * exact_gram * exact_packet
    metric = exact_packet.transpose() * exact_packet
    return trace(exact_gram) - 2 * trace(captured) + trace(metric * captured)


def refresh_from_action(
    states: list[np.ndarray],
    time: int,
    packet: np.ndarray,
    depth: int | None,
) -> tuple[np.ndarray, dict[str, float]]:
    rank = packet.shape[1]
    action = packet_action(states, packet, eta=ETA, time=time, depth=depth)
    projected_cross = projected_cross_from_action(action, packet)
    left, singular, _ = np.linalg.svd(projected_cross, full_matrices=False)
    directions = left[:, :WIDTH]
    enriched, _ = np.linalg.qr(np.column_stack([packet, directions]), mode="reduced")
    enriched_action = packet_action(states, enriched, eta=ETA, time=time, depth=depth)
    compressed = enriched.T @ enriched_action
    compressed = (compressed + compressed.T) / 2.0
    values, vectors = np.linalg.eigh(compressed)
    corrected = enriched @ vectors[:, np.argsort(values)[-rank:]]
    total_cross = float(singular @ singular)
    selected = 1.0 if total_cross == 0.0 else float(singular[:WIDTH] @ singular[:WIDTH] / total_cross)
    return corrected, {
        "selected_cross_energy_fraction": selected,
        "enriched_orthogonality_defect": float(np.linalg.norm(enriched.T @ enriched - np.eye(enriched.shape[1]), 2)),
        "corrected_orthogonality_defect": float(np.linalg.norm(corrected.T @ corrected - np.eye(rank), 2)),
    }


def direct_refresh(gram: np.ndarray, packet: np.ndarray) -> np.ndarray:
    rank = packet.shape[1]
    action = gram @ packet
    projected_cross = projected_cross_from_action(action, packet)
    left, _, _ = np.linalg.svd(projected_cross, full_matrices=False)
    enriched, _ = np.linalg.qr(np.column_stack([packet, left[:, :WIDTH]]), mode="reduced")
    compressed = enriched.T @ gram @ enriched
    compressed = (compressed + compressed.T) / 2.0
    values, vectors = np.linalg.eigh(compressed)
    return enriched @ vectors[:, np.argsort(values)[-rank:]]


def run_chain(
    states: list[np.ndarray],
    grams: list[np.ndarray],
    seed: np.ndarray,
    rank: int,
    depth: int | None,
) -> dict[str, object]:
    packet = np.asarray(seed, dtype=float)
    diagnostics = []
    for time in range(1, len(states)):
        packet, row = refresh_from_action(states, time, packet, depth)
        diagnostics.append({"time": time, **row})
    gram = grams[-1]
    reference = top_gram_packet(gram, rank)
    tail = residual_energy_arb(gram, packet)
    reference_tail = residual_energy_arb(gram, reference)
    ratio = tail / reference_tail
    return {
        "depth": "full" if depth is None else depth,
        "packet": packet,
        "interval_endpoint_tail_ball": str(tail),
        "interval_reference_tail_ball": str(reference_tail),
        "interval_endpoint_to_reference_ball": str(ratio),
        "interval_endpoint_to_reference_upper": upper(ratio),
        "minimum_cross_energy_fraction": min(row["selected_cross_energy_fraction"] for row in diagnostics),
        "maximum_orthogonality_defect": max(
            max(row["enriched_orthogonality_defect"], row["corrected_orthogonality_defect"])
            for row in diagnostics
        ),
    }


def channel_audit(model: dict[str, object], inherited_horizon: int, rank: int) -> dict[str, object]:
    operator = np.asarray(model["operator"], dtype=float)
    source = np.asarray(model["source"], dtype=float)
    endpoint = max(4, int(math.ceil(2.0 * inherited_horizon / 3.0)))
    states = [source]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    grams = memory_grams(states, ETA)
    seed = source_right_packet(source, rank)

    direct_packet = seed.copy()
    structured_packet = seed.copy()
    action_rows = []
    for time in range(1, len(states)):
        direct_action = grams[time] @ structured_packet
        full_action = packet_action(states, structured_packet, eta=ETA, time=time)
        action_row: dict[str, object] = {
            "time": time,
            "full_history_to_assembled_action_error": float(np.linalg.norm(full_action - direct_action, "fro")),
            "depths": {},
        }
        for depth in DEPTHS:
            recent = packet_action(states, structured_packet, eta=ETA, time=time, depth=depth)
            omitted_count = max(0, time - depth + 1)
            if omitted_count:
                tail_matrix = ETA**depth * grams[time - depth]
                tail_action = tail_matrix @ structured_packet
            else:
                tail_matrix = np.zeros_like(grams[time])
                tail_action = np.zeros_like(structured_packet)
            error = float(np.linalg.norm(tail_action, "fro"))
            finite_bound = packet_action_tail_bound(ETA, depth, rank, omitted_count)
            uniform_bound = packet_action_tail_bound(ETA, depth, rank)
            action_row["depths"][str(depth)] = {
                "omitted_snapshot_count": omitted_count,
                "action_error": error,
                "truncation_identity_defect": float(np.linalg.norm((full_action - recent) - tail_action, "fro")),
                "finite_trace_action_bound": finite_bound,
                "uniform_trace_action_bound": uniform_bound,
                "error_to_finite_bound_ratio": 0.0 if omitted_count == 0 else error / finite_bound,
                "tail_trace": float(np.trace(tail_matrix)),
                "tail_trace_bound": tail_trace_bound(ETA, depth, omitted_count),
                "tail_operator_norm": float(np.linalg.norm(tail_matrix, 2)),
            }
        direct_packet = direct_refresh(grams[time], direct_packet)
        structured_packet, _ = refresh_from_action(states, time, structured_packet, None)
        action_rows.append(action_row)

    full_chain = run_chain(states, grams, seed, rank, None)
    depth_chains = {str(depth): run_chain(states, grams, seed, rank, depth) for depth in DEPTHS}
    direct_tail = residual_energy_arb(grams[-1], direct_packet)
    structured_tail = arb(full_chain["interval_endpoint_tail_ball"])
    full_chain["direct_to_structured_projector_distance"] = projector_distance(direct_packet, full_chain.pop("packet"))
    full_chain["interval_direct_endpoint_tail_ball"] = str(direct_tail)
    full_chain["interval_structured_to_direct_tail_ball"] = str(structured_tail / direct_tail)
    for chain in depth_chains.values():
        chain.pop("packet")

    return {
        "side": model["side"],
        "dimension": int(operator.shape[0]),
        "source_columns": int(source.shape[1]),
        "refresh_endpoint": endpoint,
        "clock_rank": rank,
        "full_chain": full_chain,
        "depth_chains": depth_chains,
        "action_rows": action_rows,
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
                }
            )
            for channel in channels:
                print(
                    json.dumps(
                        {
                            "sigma": sigma,
                            "side": channel["side"],
                            "endpoint": channel["refresh_endpoint"],
                            "full_ratio": channel["full_chain"]["interval_endpoint_to_reference_upper"],
                            "depth_ratios": {
                                depth: chain["interval_endpoint_to_reference_upper"]
                                for depth, chain in channel["depth_chains"].items()
                            },
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    finally:
        ctx.prec = previous_precision

    channels = [channel for row in rows for channel in row["channels"]]
    action_rows = [action for channel in channels for action in channel["action_rows"]]
    depth_summary = {}
    for depth in DEPTHS:
        key = str(depth)
        eligible = [
            record
            for action in action_rows
            if (record := action["depths"][key])["omitted_snapshot_count"] > 0
        ]
        chains = [channel["depth_chains"][key] for channel in channels]
        depth_summary[key] = {
            "omitted_action_count": len(eligible),
            "maximum_action_error": max((record["action_error"] for record in eligible), default=0.0),
            "maximum_error_to_finite_bound_ratio": max(
                (record["error_to_finite_bound_ratio"] for record in eligible), default=0.0
            ),
            "maximum_tail_trace_to_bound_ratio": max(
                (record["tail_trace"] / record["tail_trace_bound"] for record in eligible), default=0.0
            ),
            "maximum_endpoint_to_reference_ratio": max(chain["interval_endpoint_to_reference_upper"] for chain in chains),
            "endpoint_green_count": sum(
                chain["interval_endpoint_to_reference_upper"] <= ENDPOINT_RATIO_TARGET for chain in chains
            ),
        }
    successful_depths = [
        depth for depth in DEPTHS if depth_summary[str(depth)]["endpoint_green_count"] == len(channels)
    ]
    summary = {
        "scale_count": len(rows),
        "channel_count": len(channels),
        "update_count": len(action_rows),
        "maximum_full_history_to_assembled_action_error": max(
            row["full_history_to_assembled_action_error"] for row in action_rows
        ),
        "maximum_direct_to_structured_projector_distance": max(
            channel["full_chain"]["direct_to_structured_projector_distance"] for channel in channels
        ),
        "maximum_full_chain_endpoint_to_reference_ratio": max(
            channel["full_chain"]["interval_endpoint_to_reference_upper"] for channel in channels
        ),
        "minimum_successful_uniform_depth": min(successful_depths) if successful_depths else None,
        "depth_summary": depth_summary,
    }
    payload = {
        "status": "rh101_finite_memory_packet_gram_action_audit",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "rank_offset": RANK_OFFSET,
        "refresh_width": WIDTH,
        "depths": list(DEPTHS),
        "endpoint_ratio_target": ENDPOINT_RATIO_TARGET,
        "rows": rows,
        "audit_summary": summary,
        "all_action_bounds_green": all(
            record["error_to_finite_bound_ratio"] <= 1.0 + 1e-10
            and record["tail_trace"] <= record["tail_trace_bound"] * (1.0 + 1e-10)
            for action in action_rows
            for record in action["depths"].values()
            if record["omitted_snapshot_count"] > 0
        ),
        "theorem_boundary": {
            "exact_finite_history_packet_action": True,
            "uniform_geometric_tail_bound": True,
            "ambient_gram_assembly_removed": True,
            "fixed_depth_frozen_prefix_validated": bool(successful_depths),
            "state_packet_multiplication_removed": False,
            "source_coordinate_svd_removed": False,
            "uniform_all_level_ritz_stability_proved": False,
            "uniform_stage_A_closed": False,
            "moving_cloud_A5_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The normalized memory Gramian has an exact state-action expansion on every trial packet, so neither the Gramian nor its recent-history truncation must be assembled in ambient coordinates. "
            "Its omitted positive tail has a dimension-free geometric trace bound. On the ten RH-94 frozen channels, depth five is the first tested common memory depth preserving every 1.01 endpoint gate. "
            "The remaining state-packet products and gap-aware stability of the nonlinear Ritz branch are separate gates."
        ),
        "limitations": [
            "The action still requires the recent state products X_s V and X_s^*(X_s V).",
            "A fixed-depth action error does not by itself imply a scale-uniform Ritz projector error without a gap-aware stability law.",
            "The endpoint audit covers five frozen scales and two channels rather than an all-level family.",
            "The source singular packet and state propagation are inherited and are not removed here.",
            "No moving-cloud, zeta-zero, Hilbert--Polya, or Riemann Hypothesis conclusion is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
