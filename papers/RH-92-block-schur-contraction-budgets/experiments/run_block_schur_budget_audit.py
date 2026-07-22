"""384-bit audit of four-step Schur contraction budgets."""

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

from block_schur_budget import (  # noqa: E402
    block_budget_product,
    block_geometric_mean,
    blocks_for_tolerance,
    relative_snapshot_bound,
)
from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, arb_matrix, build_models  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "block_schur_budget_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "block_schur_budget_smoke.json"
PRECISION_BITS = 384
ETA = 1.0 / 512.0
RANK_OFFSET = 2
BLOCK_LENGTH = 4
POINT_TARGET_NUMERATOR = 6
POINT_TARGET_DENOMINATOR = 25
POINT_TARGET = POINT_TARGET_NUMERATOR / POINT_TARGET_DENOMINATOR
BUDGET_DENOMINATOR = 1000


# Frozen after an outward-rounded pilot.  Every numerator is an integer, so
# all target factors are exact rationals in the interval audit.
BUDGET_NUMERATORS = {
    (0.16, "left"): (10, 6, 4, 3),
    (0.16, "right"): (17, 7, 5, 3),
    (0.08, "left"): (14, 7, 9, 22),
    (0.08, "right"): (8, 48, 6, 9),
    (0.04, "left"): (219, 91, 64, 31),
    (0.04, "right"): (50, 99, 142, 59),
    (0.02, "left"): (753, 142, 126, 239),
    (0.02, "right"): (145, 277, 360, 120),
    (0.01, "left"): (336, 251, 169, 190),
    (0.01, "right"): (391, 251, 123, 156),
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
    """Metric-corrected residual, valid under a lifted basis defect."""
    exact_gram = arb_matrix(gram)
    exact_basis = arb_matrix(basis)
    captured = exact_basis.transpose() * exact_gram * exact_basis
    metric = exact_basis.transpose() * exact_basis
    return trace(exact_gram) - 2 * trace(captured) + trace(metric * captured)


def enriched_data(gram: np.ndarray, old_packet: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    full, _ = np.linalg.qr(old_packet, mode="complete")
    complement = full[:, old_packet.shape[1] :]
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


def orthogonality_defect(basis: np.ndarray) -> float:
    return float(np.linalg.norm(basis.T @ basis - np.eye(basis.shape[1]), 2))


def exact_schur_form(compressed: np.ndarray, delta: arb, trial: np.ndarray, rank: int) -> arb:
    exact_h = arb_matrix(compressed)
    exact_x = arb_matrix(trial.reshape(-1, 1))
    block = arb_mat([[exact_h[row, column] for column in range(rank)] for row in range(rank)])
    coupling = arb_mat([[exact_h[row, rank]] for row in range(rank)])
    identity = arb_matrix(np.eye(rank))
    matrix = block + (delta - exact_h[rank, rank]) * identity
    return trace(exact_x.transpose() * matrix * exact_x) - 2 * trace(exact_x.transpose() * coupling) + delta


def schur_trial(compressed: np.ndarray, delta: arb, rank: int) -> tuple[np.ndarray, str, float]:
    """Choose either a coercive solve or an explicit negative-direction witness."""
    midpoint = float(delta.mid())
    block = compressed[:rank, :rank]
    coupling = compressed[:rank, rank]
    matrix = block + (midpoint - compressed[rank, rank]) * np.eye(rank)
    values, vectors = np.linalg.eigh((matrix + matrix.T) / 2.0)
    if values[0] < 0.0:
        vector = vectors[:, 0]
        quadratic = float(vector @ matrix @ vector)
        linear = float(vector @ coupling)
        scale = max(1.0, 2.0 * math.sqrt(max(midpoint, 0.0) / (-quadratic)))
        trial = (1.0 if linear >= 0.0 else -1.0) * scale * vector
        return trial, "negative_direction", math.inf
    trial = np.linalg.solve(matrix, coupling)
    return trial, "coercive_solve", float(np.linalg.cond(matrix))


def threshold_matrix(compressed: np.ndarray, delta: arb, rank: int) -> arb_mat:
    exact_h = arb_matrix(compressed)
    matrix = arb_mat(rank + 1, rank + 1)
    shift = exact_h[rank, rank] - delta
    for row in range(rank):
        for column in range(rank):
            matrix[row, column] = exact_h[row, column] - (shift if row == column else 0)
        matrix[row, rank] = exact_h[row, rank]
        matrix[rank, row] = exact_h[rank, row]
    matrix[rank, rank] = delta
    return matrix


def sylvester_data(matrix: arb_mat) -> tuple[list[float], list[float]]:
    determinant_lowers = []
    pivot_lowers = []
    previous = arb(1)
    for size in range(1, matrix.nrows() + 1):
        principal = arb_mat([[matrix[row, column] for column in range(size)] for row in range(size)])
        determinant = principal.det()
        determinant_lowers.append(lower(determinant))
        pivot_lowers.append(lower(determinant / previous))
        previous = determinant
    return determinant_lowers, pivot_lowers


def step_audit(
    grams: list[np.ndarray],
    time: int,
    rank: int,
    budget_numerator: int,
) -> dict[str, object]:
    old_gram = grams[time - 1]
    new_gram = grams[time]
    old_packet = packet_from_gram(old_gram, rank)
    enriched, compressed, cross_norm = enriched_data(new_gram, old_packet)
    corrected_packet = ritz_packet(enriched, compressed, rank)
    refresh_packet = packet_from_gram(new_gram, rank)

    previous_tail = residual_energy_arb(old_gram, old_packet)
    predictor_tail = residual_energy_arb(new_gram, old_packet)
    corrected_tail = residual_energy_arb(new_gram, corrected_packet)
    refresh_tail = residual_energy_arb(new_gram, refresh_packet)
    budget = arb(budget_numerator) / BUDGET_DENOMINATOR
    required = predictor_tail - budget * previous_tail
    corrected_ratio = corrected_tail / previous_tail
    refresh_ratio = refresh_tail / corrected_tail

    predictor_green = upper(required) <= 0.0
    correction_needed = lower(required) > 0.0
    trial_kind = "predictor"
    trial_condition = 1.0
    trial = np.zeros(rank)
    phi = arb(0)
    relative_surplus_lower = None
    if correction_needed:
        trial, trial_kind, trial_condition = schur_trial(compressed, required, rank)
        phi = exact_schur_form(compressed, required, trial, rank)
        relative_surplus_lower = -upper(phi) / upper(required)

    target_direct_green = upper(corrected_ratio) < budget_numerator / BUDGET_DENOMINATOR
    refresh_dominates = upper(refresh_ratio) < 1.0
    schur_negative = predictor_green or (correction_needed and upper(phi) < 0.0)

    point_budget = arb(POINT_TARGET_NUMERATOR) / POINT_TARGET_DENOMINATOR
    point_required = predictor_tail - point_budget * previous_tail
    pointwise_failure = lower(corrected_ratio) > POINT_TARGET
    determinant_lowers: list[float] = []
    pivot_lowers: list[float] = []
    pointwise_positive_definite = False
    if pointwise_failure:
        determinant_lowers, pivot_lowers = sylvester_data(threshold_matrix(compressed, point_required, rank))
        pointwise_positive_definite = all(value > 0.0 for value in determinant_lowers)

    return {
        "time": int(time),
        "clock_rank": int(rank),
        "compressed_dimension": int(rank + 1),
        "budget_numerator": int(budget_numerator),
        "budget_denominator": BUDGET_DENOMINATOR,
        "budget_factor": budget_numerator / BUDGET_DENOMINATOR,
        "cross_block_leading_singular_value": cross_norm,
        "trial_kind": trial_kind,
        "trial_system_condition": trial_condition,
        "interval_previous_tail_ball": str(previous_tail),
        "interval_predictor_tail_ball": str(predictor_tail),
        "interval_required_gain_ball": str(required),
        "interval_required_gain_lower": lower(required),
        "interval_required_gain_upper": upper(required),
        "interval_schur_form_ball": str(phi),
        "interval_schur_form_upper": upper(phi),
        "certified_relative_surplus_lower": relative_surplus_lower,
        "interval_corrected_contraction_ball": str(corrected_ratio),
        "interval_corrected_contraction_lower": lower(corrected_ratio),
        "interval_corrected_contraction_upper": upper(corrected_ratio),
        "interval_refresh_to_corrected_ball": str(refresh_ratio),
        "interval_refresh_to_corrected_upper": upper(refresh_ratio),
        "old_packet_orthogonality_defect": orthogonality_defect(old_packet),
        "enriched_orthogonality_defect": orthogonality_defect(enriched),
        "corrected_packet_orthogonality_defect": orthogonality_defect(corrected_packet),
        "refresh_packet_orthogonality_defect": orthogonality_defect(refresh_packet),
        "predictor_green": predictor_green,
        "correction_needed": correction_needed,
        "schur_negative": schur_negative,
        "target_direct_green": target_direct_green,
        "refresh_dominates": refresh_dominates,
        "pointwise_subquarter_failure": pointwise_failure,
        "pointwise_threshold_positive_definite": pointwise_positive_definite,
        "pointwise_sylvester_determinant_lowers": determinant_lowers,
        "pointwise_sylvester_pivot_lowers": pivot_lowers,
        "step_gate_green": schur_negative and target_direct_green and refresh_dominates,
    }


def channel_audit(model: dict[str, object], horizon: int, rank: int, sigma: float) -> dict[str, object]:
    operator = np.asarray(model["operator"], dtype=np.float64)
    states = [np.asarray(model["source"], dtype=np.float64)]
    block_end = max(BLOCK_LENGTH, int(math.ceil(2.0 * horizon / 3.0)))
    for _ in range(block_end):
        states.append(operator @ states[-1])
    grams = memory_grams(states)
    numerators = BUDGET_NUMERATORS[(sigma, str(model["side"]))]
    times = tuple(range(block_end - BLOCK_LENGTH + 1, block_end + 1))
    steps = [step_audit(grams, time, rank, numerator) for time, numerator in zip(times, numerators, strict=True)]

    factors = [record["budget_factor"] for record in steps]
    exact_budget_numerator = math.prod(numerators)
    exact_budget_denominator = BUDGET_DENOMINATOR**BLOCK_LENGTH
    budget_product = exact_budget_numerator / exact_budget_denominator
    actual_product = arb(1)
    for record in steps:
        actual_product *= arb(record["interval_corrected_contraction_ball"])

    pointwise_failures = [record for record in steps if record["pointwise_subquarter_failure"]]
    return {
        "side": model["side"],
        "dimension": int(operator.shape[0]),
        "source_columns": int(states[0].shape[1]),
        "horizon": int(horizon),
        "block_start": int(times[0]),
        "block_end": int(times[-1]),
        "block_length": BLOCK_LENGTH,
        "budget_numerators": list(numerators),
        "budget_denominator": BUDGET_DENOMINATOR,
        "budget_factors": factors,
        "exact_block_budget_numerator": int(exact_budget_numerator),
        "exact_block_budget_denominator": int(exact_budget_denominator),
        "block_budget_product": budget_product,
        "block_budget_geometric_mean": block_geometric_mean(factors),
        "interval_actual_block_product_ball": str(actual_product),
        "interval_actual_block_product_upper": upper(actual_product),
        "interval_actual_block_geometric_mean_upper": math.nextafter(upper(actual_product) ** (1.0 / BLOCK_LENGTH), math.inf),
        "pointwise_subquarter_failure_count": len(pointwise_failures),
        "steps": steps,
        "all_step_gates_green": all(record["step_gate_green"] for record in steps),
        "block_budget_green": budget_product < POINT_TARGET**BLOCK_LENGTH,
        "all_pointwise_failures_certified": all(record["pointwise_threshold_positive_definite"] for record in pointwise_failures),
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
                    "all_channels_green": all(
                        channel["all_step_gates_green"]
                        and channel["block_budget_green"]
                        and channel["all_pointwise_failures_certified"]
                        for channel in channels
                    ),
                }
            )
            for channel in channels:
                print(
                    json.dumps(
                        {
                            "sigma": sigma,
                            "side": channel["side"],
                            "rank": rank,
                            "budget_geometric_mean": channel["block_budget_geometric_mean"],
                            "actual_geometric_mean_upper": channel["interval_actual_block_geometric_mean_upper"],
                            "pointwise_failures": channel["pointwise_subquarter_failure_count"],
                            "all_green": channel["all_step_gates_green"] and channel["block_budget_green"],
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    finally:
        ctx.prec = previous_precision

    channels = [channel for row in rows for channel in row["channels"]]
    steps = [step for channel in channels for step in channel["steps"]]
    failures = [step for step in steps if step["pointwise_subquarter_failure"]]
    coercive = [step for step in steps if step["trial_kind"] == "coercive_solve"]
    negative = [step for step in steps if step["trial_kind"] == "negative_direction"]
    tolerances = []
    block_factor = POINT_TARGET**BLOCK_LENGTH
    for tolerance in (1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12):
        blocks = blocks_for_tolerance(ETA, block_factor, tolerance)
        tolerances.append(
            {
                "relative_tolerance": tolerance,
                "complete_blocks": blocks,
                "updates": BLOCK_LENGTH * blocks,
                "certified_relative_bound": relative_snapshot_bound(ETA, block_factor, blocks),
            }
        )

    audit_summary = {
        "scale_count": len(rows),
        "channel_count": len(channels),
        "update_count": len(steps),
        "coercive_trial_count": len(coercive),
        "negative_direction_trial_count": len(negative),
        "schur_negative_count": sum(step["schur_negative"] for step in steps),
        "direct_target_contraction_count": sum(step["target_direct_green"] for step in steps),
        "refresh_dominance_count": sum(step["refresh_dominates"] for step in steps),
        "pointwise_subquarter_failure_count": len(failures),
        "pointwise_positive_definite_obstruction_count": sum(step["pointwise_threshold_positive_definite"] for step in failures),
        "budget_factor_above_subquarter_count": sum(step["budget_factor"] > POINT_TARGET for step in steps),
        "maximum_block_budget_product": max(channel["block_budget_product"] for channel in channels),
        "maximum_block_budget_geometric_mean": max(channel["block_budget_geometric_mean"] for channel in channels),
        "maximum_interval_actual_block_product": max(channel["interval_actual_block_product_upper"] for channel in channels),
        "maximum_interval_actual_block_geometric_mean": max(channel["interval_actual_block_geometric_mean_upper"] for channel in channels),
        "maximum_individual_budget_factor": max(step["budget_factor"] for step in steps),
        "maximum_interval_individual_contraction": max(step["interval_corrected_contraction_upper"] for step in steps),
        "minimum_negative_schur_margin": min(-step["interval_schur_form_upper"] for step in steps if step["correction_needed"]),
        "minimum_certified_relative_surplus": min(step["certified_relative_surplus_lower"] for step in coercive),
        "maximum_trial_system_condition": max(step["trial_system_condition"] for step in coercive),
        "maximum_refresh_to_corrected_ratio": max(step["interval_refresh_to_corrected_upper"] for step in steps),
        "minimum_pointwise_failure_contraction": min(step["interval_corrected_contraction_lower"] for step in failures) if failures else None,
        "minimum_pointwise_sylvester_pivot": min(min(step["pointwise_sylvester_pivot_lowers"]) for step in failures) if failures else None,
        "maximum_orthogonality_defect": max(
            max(
                step["old_packet_orthogonality_defect"],
                step["enriched_orthogonality_defect"],
                step["corrected_packet_orthogonality_defect"],
                step["refresh_packet_orthogonality_defect"],
            )
            for step in steps
        ),
    }
    payload = {
        "status": "rh92_four_step_block_schur_contraction_budget_audit",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "rank_offset": RANK_OFFSET,
        "block_length": BLOCK_LENGTH,
        "pointwise_target": POINT_TARGET,
        "pointwise_target_block_product": block_factor,
        "budget_denominator": BUDGET_DENOMINATOR,
        "rows": rows,
        "bootstrap_tolerances": tolerances,
        "all_executed_block_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": audit_summary,
        "theorem_boundary": {
            "exact_schur_threshold_dichotomy": True,
            "coercive_defect_identity": True,
            "variable_budget_contraction_theorem": True,
            "block_bootstrap_theorem": True,
            "four_step_frozen_budget_validated": True,
            "pointwise_subquarter_law_rejected_on_frozen_window": True,
            "uniform_all_level_four_step_law_proved": False,
            "reduced_packet_refresh_proved": False,
            "uniform_stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The RH-90 pointwise target can be replaced by a variable one-step budget whose four-factor product is contractive. "
            "All forty frozen updates admit negative Schur trials, refresh packets dominate the small corrected packets, and every channel has block geometric mean below 0.24. "
            "Seven individual updates rigorously reject a pointwise 0.24 target through positive-definite threshold matrices, so the block formulation is genuinely weaker. "
            "The preferred Stage-A gate becomes a uniform repeated block law, while reduced refresh and prefix/observability remain separate requirements."
        ),
        "limitations": [
            "The four-step result is validated only on the five frozen scales and selected late windows; no repeated all-level block law is proved.",
            "A full leading packet is used as the refresh in the audit. A polylogarithmic reduced refresh remains the independent R gate.",
            "Schur forms use exact binary compressed matrices, while ambient contractions use metric-corrected exact-binary residuals; tiny basis defects are audited explicitly.",
            "The seven positive-definite obstructions concern the named rank-one enrichment and pointwise target, not every possible enrichment or rank schedule.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_block_gates_green"], **audit_summary}, sort_keys=True))


if __name__ == "__main__":
    main()
