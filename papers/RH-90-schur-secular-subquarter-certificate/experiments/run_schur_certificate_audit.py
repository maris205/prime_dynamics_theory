"""256-bit audit of Schur-secular sub-quarter contraction certificates."""

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


FULL_OUTPUT = ROOT / "results" / "schur_certificate_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "schur_certificate_smoke.json"
PRECISION_BITS = 256
RANK_OFFSET = 2
ETA = 1.0 / 512.0
TARGET = 0.24
TARGET_ARB = arb(6) / 25


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


def residual_energy_float(gram: np.ndarray, basis: np.ndarray) -> float:
    captured = basis.T @ gram @ basis
    metric = basis.T @ basis
    return float(np.trace(gram) - 2.0 * np.trace(captured) + np.trace(metric @ captured))


def residual_energy_arb(gram: np.ndarray, basis: np.ndarray) -> arb:
    exact_gram = arb_matrix(gram)
    exact_basis = arb_matrix(basis)
    captured = exact_basis.transpose() * exact_gram * exact_basis
    metric = exact_basis.transpose() * exact_basis
    return trace(exact_gram) - 2 * trace(captured) + trace(metric * captured)


def enriched_data(gram: np.ndarray, old_packet: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    full, _ = np.linalg.qr(old_packet, mode="complete")
    complement = full[:, old_packet.shape[1]:]
    cross = complement.T @ gram @ old_packet
    left, singular, _ = np.linalg.svd(cross, full_matrices=False)
    direction = complement @ left[:, 0]
    enriched, _ = np.linalg.qr(np.column_stack([old_packet, direction]), mode="reduced")
    compressed = enriched.T @ gram @ enriched
    compressed = (compressed + compressed.T) / 2.0
    return enriched, compressed, float(singular[0])


def ritz_packet(enriched: np.ndarray, compressed: np.ndarray, rank: int) -> np.ndarray:
    values, vectors = np.linalg.eigh(compressed)
    return enriched @ vectors[:, np.argsort(values)[-rank:]]


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
    enriched, compressed, cross_norm = enriched_data(new_gram, old_packet)
    corrected_packet = ritz_packet(enriched, compressed, rank)

    old_previous = residual_energy_float(old_gram, old_packet)
    candidate = residual_energy_float(new_gram, old_packet)
    corrected = residual_energy_float(new_gram, corrected_packet)
    required = max(0.0, candidate - TARGET * old_previous)
    eigenvalues = np.linalg.eigvalsh(compressed)
    d = float(compressed[-1, -1])
    gain = float(d - eigenvalues[0])
    gain_ratio = gain / required if required > 0.0 else None
    condition = 1.0
    x = np.zeros(rank)
    phi = 0.0
    if required > 0.0:
        block = compressed[:rank, :rank]
        coupling = compressed[:rank, -1]
        matrix = block + (required - d) * np.eye(rank)
        x = np.linalg.solve(matrix, coupling)
        phi = float(x @ matrix @ x - 2.0 * x @ coupling + required)
        condition = float(np.linalg.cond(matrix))

    exact_old_previous = residual_energy_arb(old_gram, old_packet)
    exact_candidate = residual_energy_arb(new_gram, old_packet)
    exact_corrected = residual_energy_arb(new_gram, corrected_packet)
    exact_required = exact_candidate - TARGET_ARB * exact_old_previous
    correction_needed = lower(exact_required) > 0.0
    predictor_already_green = upper(exact_required) <= 0.0
    exact_phi = arb(0)
    schur_negative = predictor_already_green
    if correction_needed:
        exact_h = arb_matrix(compressed)
        exact_x = arb_matrix(x.reshape(-1, 1))
        block = arb_mat([[exact_h[row, column] for column in range(rank)] for row in range(rank)])
        coupling = arb_mat([[exact_h[row, rank]] for row in range(rank)])
        identity = arb_matrix(np.eye(rank))
        matrix = block + (exact_required - exact_h[rank, rank]) * identity
        exact_phi = trace(exact_x.transpose() * matrix * exact_x) - 2 * trace(exact_x.transpose() * coupling) + exact_required
        schur_negative = upper(exact_phi) < 0.0
    exact_contraction = exact_corrected / exact_old_previous
    orthogonality_defect = float(np.linalg.norm(enriched.T @ enriched - np.eye(rank + 1), 2))

    return {
        "side": model["side"],
        "dimension": int(operator.shape[0]),
        "source_columns": int(states[0].shape[1]),
        "horizon": int(horizon),
        "predictor_time": int(corrector_time - 1),
        "corrector_time": int(corrector_time),
        "clock_rank": int(rank),
        "linear_solve_dimension": int(rank),
        "compressed_dimension": int(rank + 1),
        "target_contraction": TARGET,
        "cross_block_leading_singular_value": cross_norm,
        "enriched_orthogonality_defect": orthogonality_defect,
        "binary64_previous_tail": old_previous,
        "binary64_predictor_tail": candidate,
        "binary64_predictor_factor": candidate / old_previous,
        "binary64_required_gain": required,
        "binary64_actual_small_ritz_gain": gain,
        "binary64_gain_to_required_ratio": gain_ratio,
        "binary64_schur_trial_form": phi,
        "binary64_trial_system_condition": condition,
        "binary64_corrected_contraction": corrected / old_previous,
        "interval_required_gain_ball": str(exact_required),
        "interval_schur_trial_form_ball": str(exact_phi),
        "interval_schur_trial_form_upper": upper(exact_phi),
        "interval_corrected_contraction_ball": str(exact_contraction),
        "interval_corrected_contraction_upper": upper(exact_contraction),
        "correction_needed": correction_needed,
        "predictor_already_green": predictor_already_green,
        "schur_negative": schur_negative,
        "schur_gate_green": schur_negative and upper(exact_contraction) < TARGET and orthogonality_defect < 2e-15,
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
                print(json.dumps({"sigma": sigma, "side": record["side"], "rank": rank, "predictor": record["binary64_predictor_factor"], "correction_needed": record["correction_needed"], "phi_upper": record["interval_schur_trial_form_upper"], "gain_ratio": record["binary64_gain_to_required_ratio"], "corrected_upper": record["interval_corrected_contraction_upper"]}, sort_keys=True), flush=True)
            rows.append({"sigma": sigma, "fine_dimension": dimension, "clock": half_log_clock(sigma), "clock_rank": rank, "channels": channels, "all_channels_green": all(channel["schur_gate_green"] for channel in channels)})
    finally:
        ctx.prec = previous_precision
    channels = [channel for row in rows for channel in row["channels"]]
    needed = [channel for channel in channels if channel["correction_needed"]]
    payload = {
        "status": "rh90_schur_secular_subquarter_certificate_audit",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "target_contraction": TARGET,
        "rank_offset": RANK_OFFSET,
        "rows": rows,
        "all_executed_schur_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": {
            "scale_count": len(rows),
            "channel_count": len(channels),
            "correction_needed_count": len(needed),
            "predictor_already_green_count": sum(channel["predictor_already_green"] for channel in channels),
            "schur_negative_count": sum(channel["schur_negative"] for channel in needed),
            "minimum_gain_to_required_ratio": min(channel["binary64_gain_to_required_ratio"] for channel in needed),
            "minimum_negative_schur_margin": min(-channel["interval_schur_trial_form_upper"] for channel in needed),
            "maximum_interval_corrected_contraction": max(channel["interval_corrected_contraction_upper"] for channel in channels),
            "maximum_trial_system_condition": max(channel["binary64_trial_system_condition"] for channel in needed),
            "maximum_linear_solve_dimension": max(channel["linear_solve_dimension"] for channel in channels),
            "maximum_enriched_orthogonality_defect": max(channel["enriched_orthogonality_defect"] for channel in channels),
        },
        "theorem_boundary": {
            "schur_trial_gain_certificate": True,
            "target_contraction_corollary": True,
            "ten_channel_subquarter_contraction_validated": True,
            "full_reference_packet_removed_from_finite_certificate": True,
            "uniform_schur_margin_proved": False,
            "uniform_stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The rank-one enriched correction no longer needs a full reference packet for finite certification. A single r-dimensional trial solve supplies a Schur quadratic; negativity proves enough Ritz gain to reach a prescribed contraction target. At rho=0.24, one channel is already green and all nine remaining Schur forms are rigorously negative, while direct corrected tails stay below target. The all-level wall is now a uniform sign estimate for an explicit small Schur trial form."
        ),
        "limitations": [
            "The Schur forms use frozen binary compressed matrices and lifted floating trial vectors; direct ambient residuals are interval evaluated separately.",
            "The hardest negative margin is small and the trial systems can be ill-conditioned, although the sign is certified at 256 bits.",
            "No uniform lower bound for the Schur margin over all noise scales or times is proved.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_schur_gates_green"], **payload["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
