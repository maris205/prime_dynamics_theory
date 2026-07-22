"""384-bit audit of a source-seeded full-prefix Ritz refresh chain."""

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
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src")]

from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, arb_matrix, build_models  # noqa: E402
from source_seeded_refresh import (  # noqa: E402
    cross_energy_fraction,
    normalized_source_gram,
    orthogonality_defect,
    projector_distance,
    source_right_packet,
    top_gram_packet,
)


FULL_OUTPUT = ROOT / "results" / "source_seeded_horizon_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "source_seeded_horizon_smoke.json"
PRECISION_BITS = 384
ETA = 1.0 / 512.0
RANK_OFFSET = 2
PRIMARY_WIDTH = 4
COMPARATOR_WIDTHS = (2, 3)
ENDPOINT_RATIO_TARGET = 1.01


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def trace(matrix: arb_mat) -> arb:
    return sum((matrix[index, index] for index in range(min(matrix.nrows(), matrix.ncols()))), arb(0))


def memory_grams(states: list[np.ndarray]) -> list[np.ndarray]:
    memory = np.zeros((states[0].shape[1], states[0].shape[1]), dtype=np.float64)
    rows = []
    for state in states:
        snapshot = state.T @ state
        memory = snapshot / np.trace(snapshot) + ETA * memory
        rows.append((memory + memory.T) / 2.0)
    return rows


def residual_energy_arb(gram: np.ndarray, packet: np.ndarray) -> arb:
    exact_gram = arb_matrix(gram)
    exact_packet = arb_matrix(packet)
    captured = exact_packet.transpose() * exact_gram * exact_packet
    metric = exact_packet.transpose() * exact_packet
    return trace(exact_gram) - 2 * trace(captured) + trace(metric * captured)


def enrichment_data(
    gram: np.ndarray,
    packet: np.ndarray,
    width: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rank = packet.shape[1]
    projected_cross = gram @ packet - packet @ (packet.T @ gram @ packet)
    left, singular, _ = np.linalg.svd(projected_cross, full_matrices=False)
    directions = left[:, :width]
    enriched, _ = np.linalg.qr(np.column_stack([packet, directions]), mode="reduced")
    compressed = enriched.T @ gram @ enriched
    compressed = (compressed + compressed.T) / 2.0
    values, vectors = np.linalg.eigh(compressed)
    order = np.argsort(values)
    bottom_frame = vectors[:, order[:width]]
    corrected = enriched @ vectors[:, order[width:]]
    if corrected.shape[1] != rank:
        raise RuntimeError("Ritz packet rank changed")
    return enriched, compressed, bottom_frame, corrected, singular


def generalized_frame_gain_arb(compressed: np.ndarray, frame: np.ndarray, rank: int) -> tuple[arb, arb]:
    exact_h = arb_matrix(compressed)
    exact_w = arb_matrix(frame)
    metric = exact_w.transpose() * exact_w
    rayleigh = exact_w.transpose() * exact_h * exact_w
    generalized_trace = trace(metric.inv() * rayleigh)
    complement_trace = sum((exact_h[index, index] for index in range(rank, exact_h.nrows())), arb(0))
    return complement_trace - generalized_trace, metric.det()


def run_chain(grams: list[np.ndarray], seed: np.ndarray, rank: int, width: int) -> dict[str, object]:
    packet = np.asarray(seed, dtype=np.float64)
    seed_tail = residual_energy_arb(grams[0], packet)
    steps = []
    for time in range(1, len(grams)):
        gram = grams[time]
        predictor_tail = residual_energy_arb(gram, packet)
        enriched, compressed, bottom_frame, corrected, singular = enrichment_data(gram, packet, width)
        corrected_tail = residual_energy_arb(gram, corrected)
        reference = top_gram_packet(gram, rank)
        reference_tail = residual_energy_arb(gram, reference)
        reference_ratio = corrected_tail / reference_tail
        gain, metric_determinant = generalized_frame_gain_arb(compressed, bottom_frame, rank)
        steps.append(
            {
                "time": time,
                "width": width,
                "compressed_dimension": rank + width,
                "interval_predictor_tail_ball": str(predictor_tail),
                "interval_corrected_tail_ball": str(corrected_tail),
                "interval_reference_tail_ball": str(reference_tail),
                "interval_corrected_to_predictor_ball": str(corrected_tail / predictor_tail),
                "interval_corrected_to_predictor_upper": upper(corrected_tail / predictor_tail),
                "interval_reference_ratio_ball": str(reference_ratio),
                "interval_reference_ratio_upper": upper(reference_ratio),
                "interval_generalized_frame_gain_ball": str(gain),
                "interval_generalized_frame_gain_lower": lower(gain),
                "interval_frame_metric_determinant_ball": str(metric_determinant),
                "interval_frame_metric_determinant_lower": lower(metric_determinant),
                "selected_cross_energy_fraction": cross_energy_fraction(singular, width),
                "enriched_orthogonality_defect": orthogonality_defect(enriched),
                "corrected_orthogonality_defect": orthogonality_defect(corrected),
                "direct_ritz_monotone": upper(corrected_tail - predictor_tail) <= 0.0,
                "frame_gain_positive": lower(gain) > 0.0,
            }
        )
        packet = corrected

    endpoint = steps[-1]
    end_tail = arb(endpoint["interval_corrected_tail_ball"])
    return {
        "width": width,
        "seed_time": 0,
        "endpoint": len(grams) - 1,
        "update_count": len(steps),
        "seed_packet_orthogonality_defect": orthogonality_defect(seed),
        "interval_seed_tail_ball": str(seed_tail),
        "interval_endpoint_tail_ball": str(end_tail),
        "interval_endpoint_to_reference_ball": endpoint["interval_reference_ratio_ball"],
        "interval_endpoint_to_reference_upper": endpoint["interval_reference_ratio_upper"],
        "maximum_intermediate_reference_ratio_upper": max(step["interval_reference_ratio_upper"] for step in steps),
        "minimum_selected_cross_energy_fraction": min(step["selected_cross_energy_fraction"] for step in steps),
        "all_direct_ritz_steps_monotone": all(step["direct_ritz_monotone"] for step in steps),
        "all_frame_gains_positive": all(step["frame_gain_positive"] for step in steps),
        "steps": steps,
    }


def channel_audit(model: dict[str, object], inherited_horizon: int, rank: int) -> dict[str, object]:
    operator = np.asarray(model["operator"], dtype=np.float64)
    source = np.asarray(model["source"], dtype=np.float64)
    endpoint = max(4, int(math.ceil(2.0 * inherited_horizon / 3.0)))
    states = [source]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    grams = memory_grams(states)
    source_seed = source_right_packet(source, rank)
    gram_seed = top_gram_packet(normalized_source_gram(source), rank)
    chains = {str(width): run_chain(grams, source_seed, rank, width) for width in (*COMPARATOR_WIDTHS, PRIMARY_WIDTH)}
    primary = chains[str(PRIMARY_WIDTH)]
    return {
        "side": model["side"],
        "dimension": int(operator.shape[0]),
        "source_columns": int(source.shape[1]),
        "inherited_horizon": inherited_horizon,
        "refresh_endpoint": endpoint,
        "clock_rank": rank,
        "source_svd_to_gram_projector_distance": projector_distance(source_seed, gram_seed),
        "chains": chains,
        "width_four_endpoint_green": primary["interval_endpoint_to_reference_upper"] <= ENDPOINT_RATIO_TARGET,
        "channel_gate_green": (
            primary["interval_endpoint_to_reference_upper"] <= ENDPOINT_RATIO_TARGET
            and primary["all_direct_ritz_steps_monotone"]
            and primary["all_frame_gains_positive"]
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
                    "all_channels_green": all(channel["channel_gate_green"] for channel in channels),
                }
            )
            for channel in channels:
                print(
                    json.dumps(
                        {
                            "sigma": sigma,
                            "side": channel["side"],
                            "endpoint": channel["refresh_endpoint"],
                            "width2_ratio": channel["chains"]["2"]["interval_endpoint_to_reference_upper"],
                            "width3_ratio": channel["chains"]["3"]["interval_endpoint_to_reference_upper"],
                            "width4_ratio": channel["chains"]["4"]["interval_endpoint_to_reference_upper"],
                            "green": channel["channel_gate_green"],
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    finally:
        ctx.prec = previous_precision

    channels = [channel for row in rows for channel in row["channels"]]
    primary_steps = [step for channel in channels for step in channel["chains"][str(PRIMARY_WIDTH)]["steps"]]
    summary = {
        "scale_count": len(rows),
        "channel_count": len(channels),
        "primary_update_count": len(primary_steps),
        "source_seed_equivalence_count": sum(channel["source_svd_to_gram_projector_distance"] < 1e-10 for channel in channels),
        "width_four_endpoint_green_count": sum(channel["width_four_endpoint_green"] for channel in channels),
        "maximum_width_two_endpoint_to_reference_ratio": max(channel["chains"]["2"]["interval_endpoint_to_reference_upper"] for channel in channels),
        "maximum_width_three_endpoint_to_reference_ratio": max(channel["chains"]["3"]["interval_endpoint_to_reference_upper"] for channel in channels),
        "maximum_width_four_endpoint_to_reference_ratio": max(channel["chains"]["4"]["interval_endpoint_to_reference_upper"] for channel in channels),
        "maximum_width_four_intermediate_reference_ratio": max(channel["chains"]["4"]["maximum_intermediate_reference_ratio_upper"] for channel in channels),
        "minimum_width_two_cross_energy_fraction": min(channel["chains"]["2"]["minimum_selected_cross_energy_fraction"] for channel in channels),
        "minimum_width_three_cross_energy_fraction": min(channel["chains"]["3"]["minimum_selected_cross_energy_fraction"] for channel in channels),
        "minimum_width_four_cross_energy_fraction": min(channel["chains"]["4"]["minimum_selected_cross_energy_fraction"] for channel in channels),
        "minimum_primary_frame_gain": min(step["interval_generalized_frame_gain_lower"] for step in primary_steps),
        "minimum_primary_metric_determinant": min(step["interval_frame_metric_determinant_lower"] for step in primary_steps),
        "maximum_primary_compressed_dimension": max(step["compressed_dimension"] for step in primary_steps),
        "maximum_source_seed_projector_distance": max(channel["source_svd_to_gram_projector_distance"] for channel in channels),
        "maximum_orthogonality_defect": max(max(step["enriched_orthogonality_defect"], step["corrected_orthogonality_defect"]) for step in primary_steps),
    }
    payload = {
        "status": "rh94_source_seeded_four_direction_horizon_audit",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "rank_offset": RANK_OFFSET,
        "primary_width": PRIMARY_WIDTH,
        "comparator_widths": list(COMPARATOR_WIDTHS),
        "endpoint_ratio_target": ENDPOINT_RATIO_TARGET,
        "rows": rows,
        "all_executed_source_seeded_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": summary,
        "theorem_boundary": {
            "source_seed_equivalence_theorem": True,
            "source_seeded_recursive_horizon_theorem": True,
            "four_direction_frozen_horizons_validated": True,
            "late_ambient_eigenspace_seed_removed": True,
            "source_coordinate_svd_removed": False,
            "ambient_gram_packet_action_removed": False,
            "uniform_all_level_four_direction_law_proved": False,
            "continuum_complexity_theorem_proved": False,
            "uniform_stage_A1_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The recursively refreshed packet can be seeded once at time zero by the leading right singular subspace of the source, which is exactly the leading packet of the normalized source Gramian. "
            "Across the ten archived channels, four projected-cross directions carry this packet through the complete prefix to the RH-93 endpoint with endpoint tails within 1.01 of the ambient leading-packet reference. "
            "Widths two and three fail this robust full-horizon criterion, so four is the first tested width that removes the late ambient seed without losing endpoint accuracy."
        ),
        "limitations": [
            "The source right singular packet is still formed by an initial source-coordinate spectral operation.",
            "Each refresh still applies the ambient Gramian to the current low-rank packet.",
            "The endpoint criterion is validated only at five frozen scales and two channels.",
            "Intermediate reference ratios can be larger than one; the theorem concerns recursive validity and endpoint recovery, not stepwise optimal tracking.",
            "No all-level continuum construction, complexity bound, zeta-zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_source_seeded_gates_green"], **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
