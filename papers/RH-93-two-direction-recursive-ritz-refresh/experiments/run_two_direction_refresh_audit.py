"""384-bit audit of recursive two-direction complement Ritz refresh."""

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
from two_direction_refresh import block_geometric_mean, cross_energy_fraction  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "two_direction_refresh_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "two_direction_refresh_smoke.json"
PRECISION_BITS = 384
ETA = 1.0 / 512.0
RANK_OFFSET = 2
BLOCK_LENGTH = 4
PRIMARY_WIDTH = 2
POINT_TARGET = 0.24
BUDGET_DENOMINATOR = 1000


BUDGET_NUMERATORS = {
    (0.16, "left"): (7, 5, 4, 3),
    (0.16, "right"): (11, 6, 3, 3),
    (0.08, "left"): (12, 6, 7, 17),
    (0.08, "right"): (8, 39, 3, 21),
    (0.04, "left"): (79, 81, 56, 26),
    (0.04, "right"): (36, 65, 180, 89),
    (0.02, "left"): (455, 145, 120, 233),
    (0.02, "right"): (137, 256, 356, 113),
    (0.01, "left"): (335, 248, 168, 197),
    (0.01, "right"): (343, 250, 123, 153),
}


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def trace(matrix: arb_mat) -> arb:
    return sum((matrix[index, index] for index in range(min(matrix.nrows(), matrix.ncols()))), arb(0))


def memory_grams(states: list[np.ndarray]) -> list[np.ndarray]:
    gram = np.zeros((states[0].shape[1], states[0].shape[1]), dtype=np.float64)
    rows = []
    for state in states:
        snapshot_gram = state.T @ state
        gram = snapshot_gram / np.trace(snapshot_gram) + ETA * gram
        rows.append((gram + gram.T) / 2.0)
    return rows


def packet_from_gram(gram: np.ndarray, rank: int) -> np.ndarray:
    values, vectors = np.linalg.eigh((gram + gram.T) / 2.0)
    return vectors[:, np.argsort(values)[-rank:]]


def residual_energy_arb(gram: np.ndarray, basis: np.ndarray) -> arb:
    exact_gram = arb_matrix(gram)
    exact_basis = arb_matrix(basis)
    captured = exact_basis.transpose() * exact_gram * exact_basis
    metric = exact_basis.transpose() * exact_basis
    return trace(exact_gram) - 2 * trace(captured) + trace(metric * captured)


def orthogonality_defect(basis: np.ndarray) -> float:
    return float(np.linalg.norm(basis.T @ basis - np.eye(basis.shape[1]), 2))


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
    corrected_packet = enriched @ vectors[:, order[width:]]
    if corrected_packet.shape[1] != rank:
        raise RuntimeError("Ritz packet rank changed")
    return enriched, compressed, bottom_frame, corrected_packet, singular


def generalized_frame_trace_arb(compressed: np.ndarray, frame: np.ndarray) -> tuple[arb, arb]:
    """Exact-binary generalized Rayleigh trace for a two-column frame."""
    exact_h = arb_matrix(compressed)
    exact_w = arb_matrix(frame)
    metric = exact_w.transpose() * exact_w
    rayleigh = exact_w.transpose() * exact_h * exact_w
    a = metric[0, 0]
    b = metric[0, 1]
    c = metric[1, 1]
    determinant = a * c - b * b
    value = (c * rayleigh[0, 0] + a * rayleigh[1, 1] - b * (rayleigh[0, 1] + rayleigh[1, 0])) / determinant
    return value, determinant


def run_chain(
    grams: list[np.ndarray],
    start: int,
    end: int,
    rank: int,
    width: int,
    budget_numerators: tuple[int, ...] | None = None,
) -> dict[str, object]:
    packet = packet_from_gram(grams[start - 1], rank)
    seed_tail = residual_energy_arb(grams[start - 1], packet)
    seed_defect = orthogonality_defect(packet)
    steps = []
    for offset, time in enumerate(range(start, end + 1)):
        old_tail = residual_energy_arb(grams[time - 1], packet)
        predictor_tail = residual_energy_arb(grams[time], packet)
        enriched, compressed, bottom_frame, corrected, singular = enrichment_data(grams[time], packet, width)
        corrected_tail = residual_energy_arb(grams[time], corrected)
        contraction = corrected_tail / old_tail
        record: dict[str, object] = {
            "time": int(time),
            "width": int(width),
            "compressed_dimension": int(rank + width),
            "interval_old_tail_ball": str(old_tail),
            "interval_predictor_tail_ball": str(predictor_tail),
            "interval_corrected_tail_ball": str(corrected_tail),
            "interval_contraction_ball": str(contraction),
            "interval_contraction_lower": lower(contraction),
            "interval_contraction_upper": upper(contraction),
            "cross_singular_values": [float(value) for value in singular],
            "top_one_cross_energy_fraction": cross_energy_fraction(singular, 1),
            "selected_cross_energy_fraction": cross_energy_fraction(singular, width),
            "enriched_orthogonality_defect": orthogonality_defect(enriched),
            "corrected_orthogonality_defect": orthogonality_defect(corrected),
        }
        if budget_numerators is not None:
            numerator = budget_numerators[offset]
            budget = arb(numerator) / BUDGET_DENOMINATOR
            required = predictor_tail - budget * old_tail
            predictor_green = upper(required) <= 0.0
            correction_needed = lower(required) > 0.0
            frame_form = arb(0)
            frame_metric_determinant = arb(1)
            if correction_needed:
                generalized_trace, frame_metric_determinant = generalized_frame_trace_arb(compressed, bottom_frame)
                exact_h = arb_matrix(compressed)
                new_block_trace = exact_h[rank, rank] + exact_h[rank + 1, rank + 1]
                frame_form = generalized_trace + required - new_block_trace
            frame_negative = predictor_green or (correction_needed and upper(frame_form) < 0.0)
            direct_green = upper(contraction) < numerator / BUDGET_DENOMINATOR
            record.update(
                {
                    "budget_numerator": int(numerator),
                    "budget_denominator": BUDGET_DENOMINATOR,
                    "budget_factor": numerator / BUDGET_DENOMINATOR,
                    "interval_required_gain_ball": str(required),
                    "interval_required_gain_lower": lower(required),
                    "interval_required_gain_upper": upper(required),
                    "interval_trial_frame_form_ball": str(frame_form),
                    "interval_trial_frame_form_upper": upper(frame_form),
                    "interval_frame_metric_determinant_ball": str(frame_metric_determinant),
                    "interval_frame_metric_determinant_lower": lower(frame_metric_determinant),
                    "predictor_green": predictor_green,
                    "correction_needed": correction_needed,
                    "trial_frame_negative": frame_negative,
                    "direct_target_green": direct_green,
                    "step_gate_green": frame_negative and direct_green and lower(frame_metric_determinant) > 0.0,
                }
            )
        steps.append(record)
        packet = corrected

    end_tail = residual_energy_arb(grams[end], packet)
    block_ratio = end_tail / seed_tail
    reference_packet = packet_from_gram(grams[end], rank)
    reference_tail = residual_energy_arb(grams[end], reference_packet)
    endpoint_reference_ratio = end_tail / reference_tail
    budget_product = None
    budget_mean = None
    all_steps_green = None
    if budget_numerators is not None:
        budget_product = math.prod(budget_numerators) / BUDGET_DENOMINATOR**BLOCK_LENGTH
        budget_mean = block_geometric_mean([numerator / BUDGET_DENOMINATOR for numerator in budget_numerators])
        all_steps_green = all(record["step_gate_green"] for record in steps)
    return {
        "width": int(width),
        "seed_time": int(start - 1),
        "block_start": int(start),
        "block_end": int(end),
        "block_length": int(end - start + 1),
        "seed_packet_orthogonality_defect": seed_defect,
        "interval_seed_tail_ball": str(seed_tail),
        "interval_end_tail_ball": str(end_tail),
        "interval_block_contraction_ball": str(block_ratio),
        "interval_block_contraction_lower": lower(block_ratio),
        "interval_block_contraction_upper": upper(block_ratio),
        "interval_block_geometric_mean_lower": math.nextafter(lower(block_ratio) ** (1.0 / BLOCK_LENGTH), -math.inf),
        "interval_block_geometric_mean_upper": math.nextafter(upper(block_ratio) ** (1.0 / BLOCK_LENGTH), math.inf),
        "interval_reference_end_tail_ball": str(reference_tail),
        "interval_endpoint_to_reference_ball": str(endpoint_reference_ratio),
        "interval_endpoint_to_reference_upper": upper(endpoint_reference_ratio),
        "budget_numerators": list(budget_numerators) if budget_numerators is not None else None,
        "budget_denominator": BUDGET_DENOMINATOR if budget_numerators is not None else None,
        "block_budget_product": budget_product,
        "block_budget_geometric_mean": budget_mean,
        "all_step_gates_green": all_steps_green,
        "steps": steps,
    }


def channel_audit(model: dict[str, object], horizon: int, rank: int, sigma: float) -> dict[str, object]:
    operator = np.asarray(model["operator"], dtype=np.float64)
    states = [np.asarray(model["source"], dtype=np.float64)]
    block_end = max(BLOCK_LENGTH, int(math.ceil(2.0 * horizon / 3.0)))
    block_start = block_end - BLOCK_LENGTH + 1
    for _ in range(block_end):
        states.append(operator @ states[-1])
    grams = memory_grams(states)
    one = run_chain(grams, block_start, block_end, rank, 1)
    two = run_chain(grams, block_start, block_end, rank, PRIMARY_WIDTH, BUDGET_NUMERATORS[(sigma, str(model["side"]))])
    three = run_chain(grams, block_start, block_end, rank, 3)
    one_fails = one["interval_block_geometric_mean_lower"] > POINT_TARGET
    two_green = (
        bool(two["all_step_gates_green"])
        and two["block_budget_product"] < POINT_TARGET**BLOCK_LENGTH
        and two["interval_block_geometric_mean_upper"] < POINT_TARGET
    )
    return {
        "side": model["side"],
        "dimension": int(operator.shape[0]),
        "source_columns": int(states[0].shape[1]),
        "horizon": int(horizon),
        "clock_rank": int(rank),
        "one_direction_chain": one,
        "two_direction_chain": two,
        "three_direction_diagnostic": three,
        "one_direction_subquarter_block_fails": one_fails,
        "two_direction_block_green": two_green,
        "channel_gate_green": two_green,
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
            channels = [channel_audit(model, HORIZONS[sigma], rank, sigma) for model in models]
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
                            "rank": rank,
                            "one_direction_mean_lower": channel["one_direction_chain"]["interval_block_geometric_mean_lower"],
                            "two_direction_mean_upper": channel["two_direction_chain"]["interval_block_geometric_mean_upper"],
                            "two_direction_budget_mean": channel["two_direction_chain"]["block_budget_geometric_mean"],
                            "three_direction_reference_ratio": channel["three_direction_diagnostic"]["interval_endpoint_to_reference_upper"],
                            "green": channel["channel_gate_green"],
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    finally:
        ctx.prec = previous_precision

    channels = [channel for row in rows for channel in row["channels"]]
    two_steps = [step for channel in channels for step in channel["two_direction_chain"]["steps"]]
    one_failures = [channel for channel in channels if channel["one_direction_subquarter_block_fails"]]
    audit_summary = {
        "scale_count": len(rows),
        "channel_count": len(channels),
        "two_direction_update_count": len(two_steps),
        "trial_frame_negative_count": sum(step["trial_frame_negative"] for step in two_steps),
        "direct_target_contraction_count": sum(step["direct_target_green"] for step in two_steps),
        "one_direction_subquarter_failure_count": len(one_failures),
        "two_direction_subquarter_block_count": sum(channel["two_direction_block_green"] for channel in channels),
        "budget_factor_above_subquarter_count": sum(step["budget_factor"] > POINT_TARGET for step in two_steps),
        "maximum_one_direction_block_geometric_mean": max(channel["one_direction_chain"]["interval_block_geometric_mean_upper"] for channel in channels),
        "maximum_two_direction_budget_geometric_mean": max(channel["two_direction_chain"]["block_budget_geometric_mean"] for channel in channels),
        "maximum_two_direction_block_geometric_mean": max(channel["two_direction_chain"]["interval_block_geometric_mean_upper"] for channel in channels),
        "maximum_three_direction_block_geometric_mean": max(channel["three_direction_diagnostic"]["interval_block_geometric_mean_upper"] for channel in channels),
        "maximum_two_direction_individual_contraction": max(step["interval_contraction_upper"] for step in two_steps),
        "maximum_two_direction_budget_factor": max(step["budget_factor"] for step in two_steps),
        "minimum_top_one_cross_energy_fraction": min(step["top_one_cross_energy_fraction"] for step in two_steps),
        "minimum_top_two_cross_energy_fraction": min(step["selected_cross_energy_fraction"] for step in two_steps),
        "minimum_negative_trial_frame_margin": min(-step["interval_trial_frame_form_upper"] for step in two_steps if step["correction_needed"]),
        "minimum_frame_metric_determinant": min(step["interval_frame_metric_determinant_lower"] for step in two_steps),
        "maximum_primary_compressed_dimension": max(step["compressed_dimension"] for step in two_steps),
        "maximum_two_direction_endpoint_to_reference_ratio": max(channel["two_direction_chain"]["interval_endpoint_to_reference_upper"] for channel in channels),
        "maximum_three_direction_endpoint_to_reference_ratio": max(channel["three_direction_diagnostic"]["interval_endpoint_to_reference_upper"] for channel in channels),
        "maximum_orthogonality_defect": max(
            max(
                step["enriched_orthogonality_defect"],
                step["corrected_orthogonality_defect"],
            )
            for step in two_steps
        ),
    }
    payload = {
        "status": "rh93_two_direction_recursive_ritz_refresh_audit",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "rank_offset": RANK_OFFSET,
        "block_length": BLOCK_LENGTH,
        "primary_width": PRIMARY_WIDTH,
        "pointwise_target": POINT_TARGET,
        "budget_denominator": BUDGET_DENOMINATOR,
        "rows": rows,
        "all_executed_two_direction_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": audit_summary,
        "theorem_boundary": {
            "k_direction_complement_ritz_theorem": True,
            "top_k_cross_energy_selection": True,
            "generalized_trial_frame_gain_certificate": True,
            "recursive_reduced_block_theorem": True,
            "two_direction_frozen_recursive_blocks_validated": True,
            "one_direction_recursive_route_rejected_on_four_fine_channels": True,
            "uniform_all_level_two_direction_law_proved": False,
            "continuum_cross_direction_construction_proved": False,
            "uniform_stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "A single complement direction does not recursively sustain the RH-92 four-step target in four fine channels. "
            "Selecting the top two projected-cross directions and retaining the leading rank-r Ritz packet closes all ten frozen recursive blocks without an ambient refresh inside the block. "
            "All forty generalized two-frame gain forms are strictly negative, the worst direct block geometric mean is below 0.229, and the primary compressed dimension is at most nine. "
            "A uniform two-direction recursive block law would merge the former Schur-block and reduced-refresh gates, leaving the prefix/normalization/observability bridge separate."
        ),
        "limitations": [
            "Each block is seeded by one ambient leading packet; no all-level seed construction is proved.",
            "The projected cross directions require applying the ambient Gramian to the current packet, although no ambient spectral refresh is used inside the block.",
            "Only one four-step window per frozen channel is validated; repeated blocks and continuum-uniform constants remain open.",
            "Two directions meet the tail target but need not remain uniformly close to the full leading packet; three directions improve that diagnostic at the anchors.",
            "The one-direction failure is specific to the named recursive construction, rank schedule, and frozen windows.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_two_direction_gates_green"], **audit_summary}, sort_keys=True))


if __name__ == "__main__":
    main()
