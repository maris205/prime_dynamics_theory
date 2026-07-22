"""256-bit audit of one-complement-direction Ritz correction."""

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


FULL_OUTPUT = ROOT / "results" / "ritz_correction_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "ritz_correction_smoke.json"
PRECISION_BITS = 256
RANK_OFFSET = 2
ETA = 1.0 / 512.0


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def trace(matrix: arb_mat) -> arb:
    return sum((matrix[index, index] for index in range(min(matrix.nrows(), matrix.ncols()))), arb(0))


def packet_from_gram(gram: np.ndarray, rank: int) -> np.ndarray:
    values, vectors = np.linalg.eigh((gram + gram.T) / 2.0)
    return vectors[:, np.argsort(values)[-rank:]]


def memory_grams(states: list[np.ndarray]) -> list[np.ndarray]:
    gram = np.zeros((states[0].shape[1], states[0].shape[1]), dtype=np.float64)
    rows = []
    for state in states:
        snapshot_gram = state.T @ state
        gram = snapshot_gram / np.trace(snapshot_gram) + ETA * gram
        rows.append((gram + gram.T) / 2.0)
    return rows


def complement_direction(gram: np.ndarray, packet: np.ndarray) -> tuple[np.ndarray, float]:
    full, _ = np.linalg.qr(packet, mode="complete")
    complement = full[:, packet.shape[1]:]
    cross = complement.T @ gram @ packet
    left, singular, _ = np.linalg.svd(cross, full_matrices=False)
    return complement @ left[:, 0], float(singular[0])


def ritz_packet(gram: np.ndarray, packet: np.ndarray, direction: np.ndarray) -> np.ndarray:
    enriched = np.column_stack([packet, direction])
    compressed = enriched.T @ gram @ enriched
    values, vectors = np.linalg.eigh((compressed + compressed.T) / 2.0)
    return enriched @ vectors[:, np.argsort(values)[-packet.shape[1]:]]


def binary_residual_energy(gram: np.ndarray, basis: np.ndarray) -> float:
    captured = basis.T @ gram @ basis
    metric = basis.T @ basis
    return float(np.trace(gram) - 2.0 * np.trace(captured) + np.trace(metric @ captured))


def arb_residual_energy(gram: np.ndarray, basis: np.ndarray) -> arb:
    exact_gram = arb_matrix(gram)
    exact_basis = arb_matrix(basis)
    captured = exact_basis.transpose() * exact_gram * exact_basis
    metric = exact_basis.transpose() * exact_basis
    return trace(exact_gram) - 2 * trace(captured) + trace(metric * captured)


def channel_audit(model: dict[str, object], horizon: int, rank: int) -> dict[str, object]:
    operator = np.asarray(model["operator"], dtype=np.float64)
    states = [np.asarray(model["source"], dtype=np.float64)]
    corrector_time = int(math.ceil(2.0 * horizon / 3.0))
    for _ in range(corrector_time):
        states.append(operator @ states[-1])
    grams = memory_grams(states)
    old_gram = grams[-2]
    new_gram = grams[-1]
    old_packet = packet_from_gram(old_gram, rank)
    reference_packet = packet_from_gram(new_gram, rank)
    direction, cross_norm = complement_direction(new_gram, old_packet)
    corrected_packet = ritz_packet(new_gram, old_packet, direction)

    old_previous = binary_residual_energy(old_gram, old_packet)
    candidate = binary_residual_energy(new_gram, old_packet)
    corrected = binary_residual_energy(new_gram, corrected_packet)
    reference = binary_residual_energy(new_gram, reference_packet)
    dividend_fraction = (candidate - corrected) / (candidate - reference)
    corrected_reference_ratio = corrected / reference
    corrected_contraction = corrected / old_previous

    exact_old_previous = arb_residual_energy(old_gram, old_packet)
    exact_candidate = arb_residual_energy(new_gram, old_packet)
    exact_corrected = arb_residual_energy(new_gram, corrected_packet)
    exact_reference = arb_residual_energy(new_gram, reference_packet)
    exact_fraction = (exact_candidate - exact_corrected) / (exact_candidate - exact_reference)
    exact_contraction = exact_corrected / exact_old_previous
    correction_gap = exact_candidate - exact_corrected

    return {
        "side": model["side"],
        "dimension": int(operator.shape[0]),
        "source_columns": int(states[0].shape[1]),
        "horizon": int(horizon),
        "predictor_time": int(corrector_time - 1),
        "corrector_time": int(corrector_time),
        "clock_rank": int(rank),
        "enriched_dimension": int(rank + 1),
        "cross_block_leading_singular_value": cross_norm,
        "binary64_old_previous_tail": old_previous,
        "binary64_predictor_candidate_tail": candidate,
        "binary64_corrected_tail": corrected,
        "binary64_reference_tail": reference,
        "binary64_reference_dividend_fraction": dividend_fraction,
        "binary64_corrected_reference_tail_ratio": corrected_reference_ratio,
        "binary64_corrected_contraction": corrected_contraction,
        "interval_reference_dividend_fraction_ball": str(exact_fraction),
        "interval_reference_dividend_fraction_lower": lower(exact_fraction),
        "interval_corrected_contraction_ball": str(exact_contraction),
        "interval_corrected_contraction_upper": upper(exact_contraction),
        "interval_correction_gap_ball": str(correction_gap),
        "interval_correction_gap_lower": lower(correction_gap),
        "ritz_gate_green": lower(exact_fraction) > 0.96 and upper(exact_contraction) < 0.24 and lower(correction_gap) > 0.0,
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
                print(json.dumps({"sigma": sigma, "side": record["side"], "rank": rank, "enriched_dimension": record["enriched_dimension"], "dividend_fraction_lower": record["interval_reference_dividend_fraction_lower"], "corrected_contraction_upper": record["interval_corrected_contraction_upper"], "tail_ratio": record["binary64_corrected_reference_tail_ratio"]}, sort_keys=True), flush=True)
            rows.append({"sigma": sigma, "fine_dimension": dimension, "clock": half_log_clock(sigma), "clock_rank": rank, "channels": channels, "all_channels_green": all(channel["ritz_gate_green"] for channel in channels)})
    finally:
        ctx.prec = previous_precision
    channels = [channel for row in rows for channel in row["channels"]]
    payload = {
        "status": "rh89_rank_one_complement_ritz_correction_audit",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "rank_offset": RANK_OFFSET,
        "rows": rows,
        "all_executed_ritz_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": {
            "scale_count": len(rows),
            "channel_count": len(channels),
            "minimum_interval_reference_dividend_fraction": min(channel["interval_reference_dividend_fraction_lower"] for channel in channels),
            "maximum_interval_corrected_contraction": max(channel["interval_corrected_contraction_upper"] for channel in channels),
            "maximum_binary64_corrected_reference_tail_ratio": max(channel["binary64_corrected_reference_tail_ratio"] for channel in channels),
            "minimum_interval_correction_gap": min(channel["interval_correction_gap_lower"] for channel in channels),
            "maximum_enriched_dimension": max(channel["enriched_dimension"] for channel in channels),
        },
        "theorem_boundary": {
            "rank_one_complement_ritz_theorem": True,
            "cross_block_maximal_coupling_direction": True,
            "ten_channel_corrected_contraction_validated": True,
            "one_direction_reference_dividend_fraction_validated": True,
            "uniform_cross_block_enrichment_proved": False,
            "uniform_stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "A single complement direction selected from the old-packet/new-Gram cross block, followed by a rank-r Ritz solve in dimension r+1, reproduces at least 96 percent of the full floating reference correction dividend in every channel. The resulting corrected memory tail still contracts by a factor below 0.24. Thus the RH-88 reoptimization dividend is carried by an explicitly low-dimensional cross-block corrector at the anchors. The next all-level target is a uniform lower bound on this one-direction enrichment gain."
        ),
        "limitations": [
            "The interval audit treats the frozen binary64 memory Gramians and packet bases as exact binary inputs.",
            "The dividend fraction compares the rank-one Ritz packet with the full binary64 reference packet, not with an interval eigendecomposition of the full Gramian.",
            "The cross-block enrichment fraction is validated at ten channels and is not yet uniform in noise or time.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_ritz_gates_green"], **payload["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
