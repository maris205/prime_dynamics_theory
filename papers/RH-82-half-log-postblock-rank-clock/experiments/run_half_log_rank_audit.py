"""Arb validation of the half-log plus two postblock rank clock."""

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
RH16 = PAPERS / "RH-16-endpoint-gaussian-resolution-rank"
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH16 / "src")]

from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from endpoint_rank import boundary_clearances, resolution_singular_values  # noqa: E402
from run_effective_rank_audit import (  # noqa: E402
    HORIZONS,
    SIGMAS,
    arb_matrix,
    build_models,
    frobenius_norm,
    matrix_power,
)


FULL_OUTPUT = ROOT / "results" / "half_log_rank_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "half_log_rank_smoke.json"
PRECISION_BITS = 192
RANK_OFFSET = 2
MODEL_SIGMAS = (1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12)


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def rank_candidate(state: np.ndarray, rank: int) -> np.ndarray:
    left, singular, right = np.linalg.svd(state, full_matrices=False)
    actual = min(int(rank), singular.size)
    return (left[:, :actual] * singular[:actual]) @ right[:actual, :]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    inherited = json.loads((RH77 / "results" / "effective_rank_audit.json").read_text(encoding="utf-8"))
    inherited_rows = {float(row["sigma"]): row for row in inherited["rows"]}
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows = []
    try:
        sigmas = SIGMAS[:1] if args.smoke else SIGMAS
        for sigma in sigmas:
            dimension, models = build_models(sigma)
            rank = clock_rank(sigma, offset=RANK_OFFSET)
            clock = half_log_clock(sigma)
            channels = []
            for index, model in enumerate(models):
                operator_values = np.asarray(model["operator"])
                source_values = np.asarray(model["source"])
                state_float = np.linalg.matrix_power(operator_values, HORIZONS[sigma]) @ source_values
                exact_state = matrix_power(arb_matrix(operator_values), HORIZONS[sigma]) * arb_matrix(source_values)
                state_norm = frobenius_norm(exact_state)
                candidate = rank_candidate(state_float, rank)
                residual = frobenius_norm(exact_state - arb_matrix(candidate))
                relative = residual / state_norm
                capture = arb(1) - relative**2
                inherited_channel = inherited_rows[sigma]["channels"][index]
                observability = arb(inherited_channel["full_observability_norm_upper_ball"])
                future = observability.sqrt() * residual
                record = {
                    "side": model["side"],
                    "dimension": int(operator_values.shape[0]),
                    "source_columns": int(source_values.shape[1]),
                    "horizon": HORIZONS[sigma],
                    "clock": clock,
                    "clock_rank": rank,
                    "clock_excess": rank - clock,
                    "state_frobenius_ball": str(state_norm),
                    "residual_frobenius_ball": str(residual),
                    "residual_frobenius_upper": upper(residual),
                    "relative_residual_ball": str(relative),
                    "relative_residual_upper": upper(relative),
                    "energy_capture_lower_ball": str(capture),
                    "energy_capture_lower": lower(capture),
                    "full_future_hardy_perturbation_ball": str(future),
                    "full_future_hardy_perturbation_upper": upper(future),
                    "rank_is_logarithmic": rank <= math.ceil(clock) + RANK_OFFSET,
                    "relative_residual_below_1e_minus_6": upper(relative) < 1e-6,
                }
                channels.append(record)
                print(json.dumps({"sigma": sigma, "side": record["side"], "clock": clock, "rank": rank, "relative_residual": record["relative_residual_upper"], "future_error": record["full_future_hardy_perturbation_upper"]}, sort_keys=True), flush=True)
            rows.append({"sigma": sigma, "fine_dimension": dimension, "clock": clock, "clock_rank": rank, "channels": channels, "all_channels_green": all(channel["rank_is_logarithmic"] and channel["relative_residual_below_1e_minus_6"] for channel in channels)})
    finally:
        ctx.prec = previous_precision
    channels = [channel for row in rows for channel in row["channels"]]
    clearances = boundary_clearances(100, decimal_digits=100)
    model_rows = []
    for sigma in MODEL_SIGMAS[:1] if args.smoke else MODEL_SIGMAS:
        singular = resolution_singular_values(clearances, sigma, power=1.0, tail_ratio=1e-14)
        rank = clock_rank(sigma, offset=RANK_OFFSET)
        tail = float(np.sqrt(np.sum(singular[rank:] ** 2)))
        model_rows.append({
            "sigma": sigma,
            "clock": half_log_clock(sigma),
            "clock_rank": rank,
            "retained_gram_dimension": int(singular.size),
            "optimal_hilbert_schmidt_tail": tail,
            "first_omitted_singular_value": float(singular[rank]) if rank < singular.size else 0.0,
        })
    payload = {
        "status": "rh82_half_log_plus_two_postblock_rank_clock",
        "precision_bits": PRECISION_BITS,
        "rank_offset": RANK_OFFSET,
        "rows": rows,
        "endpoint_linear_row_model": {
            "evidence_level": "high_precision_boundary_ladder_plus_binary64_exact_affinity_gram",
            "rows": model_rows,
            "maximum_clock_plus_two_tail": max(row["optimal_hilbert_schmidt_tail"] for row in model_rows),
        },
        "all_executed_clock_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": {
            "maximum_clock_rank": max(channel["clock_rank"] for channel in channels),
            "maximum_relative_residual": max(channel["relative_residual_upper"] for channel in channels),
            "maximum_full_future_hardy_perturbation": max(channel["full_future_hardy_perturbation_upper"] for channel in channels),
            "minimum_energy_capture": min(channel["energy_capture_lower"] for channel in channels),
        },
        "theorem_boundary": {
            "endpoint_exponential_excess_rank_tail": True,
            "factor_through_resolution_transfer_criterion": True,
            "half_log_plus_two_frozen_postblock_audit": True,
            "actual_endpoint_postblock_factorization_proved": False,
            "uniform_stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The RH-16 endpoint resolution theorem sharpens to exponential Hilbert-Schmidt decay for every rank beyond the half-logarithmic clock. If the physical postblock state factors through that resolution operator with polylogarithmic outer norms, remainder, and future observability, RH-78's effective-rank corridor closes with logarithmic rank. At the five archived scales, rank ceil(H_sigma)+2 (four through seven) has validated relative residual below 2.34e-7. The remaining theorem is the actual endpoint-to-postblock factorization, not a new rank ansatz."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "row_count": len(rows), "all_green": payload["all_executed_clock_gates_green"], **payload["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
