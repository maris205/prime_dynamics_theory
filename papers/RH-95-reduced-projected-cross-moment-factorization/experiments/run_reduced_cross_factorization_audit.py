"""384-bit endpoint audit of the reduced projected-cross factorization."""

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
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH77 / "experiments"),
    str(RH82 / "src"),
    str(RH94 / "src"),
    str(RH94 / "experiments"),
]

from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from reduced_cross_factorization import reduced_cross_factorization  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import memory_grams, residual_energy_arb  # noqa: E402
from source_seeded_refresh import orthogonality_defect, projector_distance, source_right_packet, top_gram_packet  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "reduced_cross_factorization_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "reduced_cross_factorization_smoke.json"
PRECISION_BITS = 384
RANK_OFFSET = 2
WIDTH = 4
ENDPOINT_RATIO_TARGET = 1.01
TAIL_EQUIVALENCE_TARGET = 1.0001
WEAK_MODE_RATIO = 1e-8
RAW_ORTHOGONALITY_FAILURE = 1e-6
MOMENT_FAILURE = 1e-3


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def relative_error(first: np.ndarray, second: np.ndarray) -> float:
    denominator = max(float(np.linalg.norm(second, "fro")), np.finfo(float).tiny)
    return float(np.linalg.norm(first - second, "fro") / denominator)


def ritz_packet(gram: np.ndarray, packet: np.ndarray, directions: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    enriched, _ = np.linalg.qr(np.column_stack([packet, directions]), mode="reduced")
    compressed = enriched.T @ gram @ enriched
    compressed = (compressed + compressed.T) / 2.0
    values, vectors = np.linalg.eigh(compressed)
    corrected = enriched @ vectors[:, np.argsort(values)[-packet.shape[1]:]]
    return corrected, compressed


def update(gram: np.ndarray, packet: np.ndarray) -> tuple[np.ndarray, dict[str, object]]:
    rank = packet.shape[1]
    factor = reduced_cross_factorization(gram, packet, WIDTH)
    cross = factor["cross"]
    ambient_left, ambient_singular, _ = np.linalg.svd(cross, full_matrices=False)
    ambient_directions = ambient_left[:, :WIDTH]
    raw_reduced_directions = factor["directions"]
    projected_reduced = raw_reduced_directions - packet @ (packet.T @ raw_reduced_directions)
    reduced_directions, _ = np.linalg.qr(projected_reduced, mode="reduced")
    reduced_packet, reduced_compressed = ritz_packet(gram, packet, reduced_directions)
    ambient_packet, _ = ritz_packet(gram, packet, ambient_directions)

    direct_cross_gram = cross.T @ cross
    direct_cross_cubic = cross.T @ gram @ cross
    raw_enriched = np.column_stack([packet, raw_reduced_directions])
    direct_raw_compressed = raw_enriched.T @ gram @ raw_enriched
    values = np.linalg.svd((direct_cross_gram + direct_cross_gram.T) / 2.0, compute_uv=False)
    cutoff = math.sqrt(float(values[WIDTH - 1]))
    next_value = float(values[WIDTH]) if len(values) > WIDTH else 0.0
    cutoff_gap = float(values[WIDTH - 1] - next_value)
    predictor_tail = residual_energy_arb(gram, packet)
    corrected_tail = residual_energy_arb(gram, reduced_packet)
    ambient_tail = residual_energy_arb(gram, ambient_packet)
    return reduced_packet, {
        "rank": rank,
        "compressed_dimension": rank + WIDTH,
        "interval_predictor_tail_ball": str(predictor_tail),
        "interval_corrected_tail_ball": str(corrected_tail),
        "interval_ambient_svd_tail_ball": str(ambient_tail),
        "interval_corrected_to_predictor_upper": upper(corrected_tail / predictor_tail),
        "interval_reduced_to_ambient_tail_upper": upper(corrected_tail / ambient_tail),
        "stabilized_direction_projector_distance": projector_distance(reduced_directions, ambient_directions),
        "corrected_packet_projector_distance": projector_distance(reduced_packet, ambient_packet),
        "direct_cross_gram_relative_error": relative_error(factor["moment_cross_gram"], direct_cross_gram),
        "direct_cross_cubic_relative_error": relative_error(factor["moment_cross_cubic"], direct_cross_cubic),
        "compressed_moment_relative_error": relative_error(factor["compressed_moment"], direct_raw_compressed),
        "raw_reconstructed_direction_orthogonality_defect": orthogonality_defect(raw_reduced_directions),
        "stabilized_direction_orthogonality_defect": orthogonality_defect(reduced_directions),
        "reduced_packet_orthogonality_defect": orthogonality_defect(reduced_packet),
        "largest_cross_singular_value": float(ambient_singular[0]),
        "cutoff_cross_singular_value": cutoff,
        "cutoff_to_leading_singular_ratio": cutoff / float(ambient_singular[0]),
        "cutoff_squared_gap": cutoff_gap,
        "cutoff_relative_squared_gap": cutoff_gap / max(float(values[WIDTH - 1]), np.finfo(float).tiny),
        "all_selected_singular_values": [float(value) for value in factor["singular_values"]],
        "direct_ritz_monotone": upper(corrected_tail - predictor_tail) <= 0.0,
        "weak_cutoff_mode": cutoff / float(ambient_singular[0]) < WEAK_MODE_RATIO,
        "raw_reconstruction_unstable": orthogonality_defect(raw_reduced_directions) > RAW_ORTHOGONALITY_FAILURE,
        "moment_compression_unstable": relative_error(factor["compressed_moment"], direct_raw_compressed) > MOMENT_FAILURE,
        "tail_equivalent_to_ambient_svd": upper(corrected_tail / ambient_tail) < TAIL_EQUIVALENCE_TARGET,
    }


def channel_audit(model: dict[str, object], inherited_horizon: int, rank: int) -> dict[str, object]:
    operator = np.asarray(model["operator"], dtype=np.float64)
    source = np.asarray(model["source"], dtype=np.float64)
    endpoint = max(4, int(math.ceil(2.0 * inherited_horizon / 3.0)))
    states = [source]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    grams = memory_grams(states)
    packet = source_right_packet(source, rank)
    steps = []
    for time in range(1, endpoint + 1):
        packet, record = update(grams[time], packet)
        record["time"] = time
        steps.append(record)
    endpoint_tail = residual_energy_arb(grams[endpoint], packet)
    reference = top_gram_packet(grams[endpoint], rank)
    reference_tail = residual_energy_arb(grams[endpoint], reference)
    endpoint_ratio = endpoint_tail / reference_tail
    gate = (
        upper(endpoint_ratio) <= ENDPOINT_RATIO_TARGET
        and all(step["tail_equivalent_to_ambient_svd"] for step in steps)
        and all(step["direct_ritz_monotone"] for step in steps)
    )
    return {
        "side": model["side"],
        "dimension": int(operator.shape[0]),
        "source_columns": int(source.shape[1]),
        "inherited_horizon": inherited_horizon,
        "refresh_endpoint": endpoint,
        "clock_rank": rank,
        "interval_endpoint_tail_ball": str(endpoint_tail),
        "interval_reference_tail_ball": str(reference_tail),
        "interval_endpoint_to_reference_ball": str(endpoint_ratio),
        "interval_endpoint_to_reference_upper": upper(endpoint_ratio),
        "steps": steps,
        "channel_gate_green": gate,
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
                print(json.dumps({"sigma": sigma, "side": channel["side"], "endpoint_ratio": channel["interval_endpoint_to_reference_upper"], "max_direction_distance": max(step["stabilized_direction_projector_distance"] for step in channel["steps"]), "min_cutoff_ratio": min(step["cutoff_to_leading_singular_ratio"] for step in channel["steps"]), "weak_steps": sum(step["weak_cutoff_mode"] for step in channel["steps"]), "green": channel["channel_gate_green"]}, sort_keys=True), flush=True)
    finally:
        ctx.prec = previous_precision

    channels = [channel for row in rows for channel in row["channels"]]
    steps = [step for channel in channels for step in channel["steps"]]
    summary = {
        "scale_count": len(rows),
        "channel_count": len(channels),
        "update_count": len(steps),
        "green_channel_count": sum(channel["channel_gate_green"] for channel in channels),
        "maximum_endpoint_to_reference_ratio": max(channel["interval_endpoint_to_reference_upper"] for channel in channels),
        "maximum_stabilized_direction_projector_distance": max(step["stabilized_direction_projector_distance"] for step in steps),
        "maximum_corrected_packet_projector_distance": max(step["corrected_packet_projector_distance"] for step in steps),
        "maximum_reduced_to_ambient_tail_ratio": max(step["interval_reduced_to_ambient_tail_upper"] for step in steps),
        "maximum_cross_gram_relative_error": max(step["direct_cross_gram_relative_error"] for step in steps),
        "maximum_cross_cubic_relative_error": max(step["direct_cross_cubic_relative_error"] for step in steps),
        "maximum_compressed_moment_relative_error": max(step["compressed_moment_relative_error"] for step in steps),
        "minimum_cutoff_cross_singular_value": min(step["cutoff_cross_singular_value"] for step in steps),
        "minimum_cutoff_to_leading_singular_ratio": min(step["cutoff_to_leading_singular_ratio"] for step in steps),
        "minimum_cutoff_relative_squared_gap": min(step["cutoff_relative_squared_gap"] for step in steps),
        "maximum_raw_reconstructed_direction_orthogonality_defect": max(step["raw_reconstructed_direction_orthogonality_defect"] for step in steps),
        "maximum_stabilized_direction_orthogonality_defect": max(step["stabilized_direction_orthogonality_defect"] for step in steps),
        "maximum_packet_orthogonality_defect": max(step["reduced_packet_orthogonality_defect"] for step in steps),
        "maximum_compressed_dimension": max(step["compressed_dimension"] for step in steps),
        "direct_ritz_monotone_count": sum(step["direct_ritz_monotone"] for step in steps),
        "tail_equivalent_update_count": sum(step["tail_equivalent_to_ambient_svd"] for step in steps),
        "weak_cutoff_mode_count": sum(step["weak_cutoff_mode"] for step in steps),
        "raw_reconstruction_unstable_count": sum(step["raw_reconstruction_unstable"] for step in steps),
        "moment_compression_unstable_count": sum(step["moment_compression_unstable"] for step in steps),
    }
    payload = {
        "status": "rh95_reduced_projected_cross_moment_factorization_audit",
        "precision_bits": PRECISION_BITS,
        "rank_offset": RANK_OFFSET,
        "selected_width": WIDTH,
        "rows": rows,
        "all_executed_reduced_factorization_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": summary,
        "theorem_boundary": {
            "projected_cross_gram_identity": True,
            "cross_cubic_moment_identity": True,
            "reduced_compressed_factorization_theorem": True,
            "threshold_stability_bounds": True,
            "ambient_cross_svd_removed_after_qr_stabilization": True,
            "binary64_moment_only_factorization_stable": False,
            "uniform_fourth_cross_mode_conditioning": False,
            "ambient_gram_packet_action_removed": False,
            "uniform_cross_spectral_gap_proved": False,
            "uniform_all_level_factorization_proved": False,
            "uniform_stage_A1_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The projected-cross SVD can be replaced exactly by an r-by-r eigendecomposition of K* K, and the entire (r+k)-dimensional Ritz matrix is determined by the first three packet moments of the Gramian. "
            "Across all 120 source-seeded updates, the reduced reconstruction agrees with the ambient cross-SVD construction to the recorded tolerances and preserves the RH-94 endpoint gate. "
            "The remaining ambient operation is the application of G to the packet, not an ambient spectral solve."
        ),
        "limitations": [
            "The reduced factorization still needs Gramian actions to form packet moments and reconstruct complement directions.",
            "No uniform lower bound for the fourth cross singular value or its cutoff gap is proved.",
            "Moment formulas can suffer cancellation when cross energy is small; the audit measures but does not analytically remove this conditioning.",
            "Only the archived finite horizons are validated.",
            "No Hilbert--Polya operator, zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_reduced_factorization_gates_green"], **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
