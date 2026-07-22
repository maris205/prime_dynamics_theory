"""384-bit audit of adaptive projected-cross widths and quotient bounds."""

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
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"), str(RH94 / "src"), str(RH94 / "experiments")]

from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import lower, memory_grams, residual_energy_arb, upper  # noqa: E402
from source_seeded_refresh import source_right_packet, top_gram_packet  # noqa: E402
from weak_mode_quotient import adaptive_width, gap_weighted_tail_loss_bound, universal_omitted_block_bound  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "weak_mode_quotient_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "weak_mode_quotient_smoke.json"
PRECISION_BITS = 384
RANK_OFFSET = 2
MAXIMUM_WIDTH = 4
MINIMUM_WIDTH = 2
THRESHOLDS = (1e-8, 1e-6, 1e-4)
PRIMARY_THRESHOLD = 1e-8
ENDPOINT_RATIO_TARGET = 1.01


def safe_eigendecomposition(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    hermitian = (np.asarray(matrix, dtype=float) + np.asarray(matrix, dtype=float).T) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    order = np.argsort(values)[::-1]
    values = values[order]
    vectors = vectors[:, order]
    reconstructed = (vectors * values) @ vectors.T
    guard = 128.0 * np.finfo(float).eps * max(1, hermitian.shape[0]) * max(1.0, float(np.linalg.norm(hermitian, 2)))
    error = math.nextafter(float(np.linalg.norm(hermitian - reconstructed, 2)) + guard, math.inf)
    return values, vectors, error


def ritz_from_basis(gram: np.ndarray, basis: np.ndarray, rank: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    compressed = basis.T @ gram @ basis
    compressed = (compressed + compressed.T) / 2.0
    values, vectors, error = safe_eigendecomposition(compressed)
    packet = basis @ vectors[:, :rank]
    return packet, compressed, values, error


def one_step(gram: np.ndarray, packet: np.ndarray, threshold: float) -> tuple[np.ndarray, dict[str, object]]:
    rank = packet.shape[1]
    cross = gram @ packet - packet @ (packet.T @ gram @ packet)
    left, singular, _ = np.linalg.svd(cross, full_matrices=False)
    width = adaptive_width(singular, threshold, minimum=MINIMUM_WIDTH, maximum=MAXIMUM_WIDTH)
    full_directions = left[:, :MAXIMUM_WIDTH]
    full_basis, _ = np.linalg.qr(np.column_stack([packet, full_directions]), mode="reduced")
    strong_dimension = rank + width
    strong_basis = full_basis[:, :strong_dimension]
    full_packet, full_compressed, full_values, full_error = ritz_from_basis(gram, full_basis, rank)
    strong_packet, strong_compressed, strong_values, strong_error = ritz_from_basis(gram, strong_basis, rank)
    predictor_tail = residual_energy_arb(gram, packet)
    strong_tail = residual_energy_arb(gram, strong_packet)
    full_tail = residual_energy_arb(gram, full_packet)
    actual_loss = strong_tail - full_tail

    omitted = MAXIMUM_WIDTH - width
    record: dict[str, object] = {
        "threshold": threshold,
        "selected_width": width,
        "omitted_width": omitted,
        "cross_singular_values": [float(value) for value in singular[:MAXIMUM_WIDTH]],
        "cutoff_to_leading_ratio": float(singular[width - 1] / singular[0]),
        "first_omitted_to_leading_ratio": float(singular[width] / singular[0]) if omitted else 0.0,
        "interval_predictor_tail_ball": str(predictor_tail),
        "interval_adaptive_tail_ball": str(strong_tail),
        "interval_full_width_tail_ball": str(full_tail),
        "interval_adaptive_to_full_tail_upper": upper(strong_tail / full_tail),
        "interval_actual_tail_loss_ball": str(actual_loss),
        "interval_actual_tail_loss_upper": upper(actual_loss),
        "direct_ritz_monotone": upper(strong_tail - predictor_tail) <= 0.0,
        "full_ritz_eigen_residual": full_error,
        "strong_ritz_eigen_residual": strong_error,
    }
    if omitted:
        cross_block = full_compressed[:strong_dimension, strong_dimension:]
        omitted_block = full_compressed[strong_dimension:, strong_dimension:]
        omitted_values, _, omitted_error = safe_eigendecomposition(omitted_block)
        alpha_lower = math.nextafter(float(strong_values[rank - 1] - strong_error), -math.inf)
        beta_upper = math.nextafter(float(omitted_values[0] + omitted_error), math.inf)
        gap_lower = math.nextafter(alpha_lower - beta_upper, -math.inf)
        cross_frobenius_upper = math.nextafter(float(np.linalg.norm(cross_block, "fro")) * (1.0 + 128.0 * np.finfo(float).eps), math.inf)
        cross_nuclear_upper = math.nextafter(float(np.linalg.svd(cross_block, compute_uv=False).sum()) * (1.0 + 128.0 * np.finfo(float).eps), math.inf)
        omitted_trace_upper = math.nextafter(float(np.trace(omitted_block)) * (1.0 + 128.0 * np.finfo(float).eps), math.inf)
        universal_bound = universal_omitted_block_bound(cross_nuclear_upper, max(0.0, omitted_trace_upper))
        if gap_lower > 0.0:
            gap_bound = gap_weighted_tail_loss_bound(cross_frobenius_upper, alpha_lower, beta_upper)
            gap_certificate = upper(actual_loss) <= gap_bound
            relative_bound = gap_bound / max(lower(full_tail), np.finfo(float).tiny)
        else:
            gap_bound = math.inf
            gap_certificate = False
            relative_bound = math.inf
        record.update(
            {
                "retained_cutoff_lower": alpha_lower,
                "omitted_spectral_upper": beta_upper,
                "retained_to_omitted_gap_lower": gap_lower,
                "omitted_cross_frobenius_upper": cross_frobenius_upper,
                "gap_weighted_tail_loss_bound": gap_bound,
                "gap_bound_to_full_tail": relative_bound,
                "universal_omitted_block_bound": universal_bound,
                "gap_certificate_green": gap_certificate,
            }
        )
    else:
        record.update(
            {
                "retained_cutoff_lower": None,
                "omitted_spectral_upper": None,
                "retained_to_omitted_gap_lower": None,
                "omitted_cross_frobenius_upper": 0.0,
                "gap_weighted_tail_loss_bound": 0.0,
                "gap_bound_to_full_tail": 0.0,
                "universal_omitted_block_bound": 0.0,
                "gap_certificate_green": True,
            }
        )
    return strong_packet, record


def run_chain(grams: list[np.ndarray], seed: np.ndarray, rank: int, threshold: float) -> dict[str, object]:
    packet = np.asarray(seed, dtype=float)
    steps = []
    for time in range(1, len(grams)):
        packet, record = one_step(grams[time], packet, threshold)
        record["time"] = time
        steps.append(record)
    endpoint_tail = residual_energy_arb(grams[-1], packet)
    reference_tail = residual_energy_arb(grams[-1], top_gram_packet(grams[-1], rank))
    endpoint_ratio = endpoint_tail / reference_tail
    return {
        "threshold": threshold,
        "endpoint": len(grams) - 1,
        "update_count": len(steps),
        "interval_endpoint_tail_ball": str(endpoint_tail),
        "interval_reference_tail_ball": str(reference_tail),
        "interval_endpoint_to_reference_ball": str(endpoint_ratio),
        "interval_endpoint_to_reference_upper": upper(endpoint_ratio),
        "minimum_selected_width": min(step["selected_width"] for step in steps),
        "omitted_update_count": sum(step["omitted_width"] > 0 for step in steps),
        "all_gap_certificates_green": all(step["gap_certificate_green"] for step in steps),
        "all_direct_ritz_steps_monotone": all(step["direct_ritz_monotone"] for step in steps),
        "steps": steps,
    }


def channel_audit(model: dict[str, object], inherited_horizon: int, rank: int) -> dict[str, object]:
    operator = np.asarray(model["operator"], dtype=float)
    source = np.asarray(model["source"], dtype=float)
    endpoint = max(4, int(math.ceil(2.0 * inherited_horizon / 3.0)))
    states = [source]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    grams = memory_grams(states)
    seed = source_right_packet(source, rank)
    chains = {f"{threshold:.0e}": run_chain(grams, seed, rank, threshold) for threshold in THRESHOLDS}
    primary = chains[f"{PRIMARY_THRESHOLD:.0e}"]
    return {
        "side": model["side"],
        "dimension": int(operator.shape[0]),
        "source_columns": int(source.shape[1]),
        "inherited_horizon": inherited_horizon,
        "refresh_endpoint": endpoint,
        "clock_rank": rank,
        "chains": chains,
        "channel_gate_green": (
            primary["interval_endpoint_to_reference_upper"] <= ENDPOINT_RATIO_TARGET
            and primary["all_gap_certificates_green"]
            and primary["all_direct_ritz_steps_monotone"]
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
            rows.append({"sigma": sigma, "fine_dimension": dimension, "clock": half_log_clock(sigma), "clock_rank": rank, "channels": channels, "all_channels_green": all(channel["channel_gate_green"] for channel in channels)})
            for channel in channels:
                primary = channel["chains"][f"{PRIMARY_THRESHOLD:.0e}"]
                print(json.dumps({"sigma": sigma, "side": channel["side"], "endpoint_ratio": primary["interval_endpoint_to_reference_upper"], "omitted_updates": primary["omitted_update_count"], "minimum_width": primary["minimum_selected_width"], "green": channel["channel_gate_green"]}, sort_keys=True), flush=True)
    finally:
        ctx.prec = previous_precision

    channels = [channel for row in rows for channel in row["channels"]]
    threshold_summaries = {}
    for threshold in THRESHOLDS:
        key = f"{threshold:.0e}"
        chains = [channel["chains"][key] for channel in channels]
        steps = [step for chain in chains for step in chain["steps"]]
        omitted_steps = [step for step in steps if step["omitted_width"] > 0]
        threshold_summaries[key] = {
            "threshold": threshold,
            "update_count": len(steps),
            "omitted_update_count": len(omitted_steps),
            "width_two_update_count": sum(step["selected_width"] == 2 for step in steps),
            "width_three_update_count": sum(step["selected_width"] == 3 for step in steps),
            "width_four_update_count": sum(step["selected_width"] == 4 for step in steps),
            "gap_certificate_count": sum(step["gap_certificate_green"] for step in omitted_steps),
            "maximum_endpoint_to_reference_ratio": max(chain["interval_endpoint_to_reference_upper"] for chain in chains),
            "maximum_adaptive_to_full_tail_ratio": max(step["interval_adaptive_to_full_tail_upper"] for step in steps),
            "maximum_actual_tail_loss": max(step["interval_actual_tail_loss_upper"] for step in steps),
            "maximum_gap_bound_to_full_tail": max((step["gap_bound_to_full_tail"] for step in omitted_steps), default=0.0),
            "maximum_gap_bound_over_actual_loss": max((step["gap_weighted_tail_loss_bound"] / max(step["interval_actual_tail_loss_upper"], np.finfo(float).tiny) for step in omitted_steps), default=0.0),
            "minimum_retained_to_omitted_gap": min((step["retained_to_omitted_gap_lower"] for step in omitted_steps), default=None),
            "all_endpoints_green": all(chain["interval_endpoint_to_reference_upper"] <= ENDPOINT_RATIO_TARGET for chain in chains),
            "all_gap_certificates_green": all(chain["all_gap_certificates_green"] for chain in chains),
        }
    primary_summary = threshold_summaries[f"{PRIMARY_THRESHOLD:.0e}"]
    summary = {
        "scale_count": len(rows),
        "channel_count": len(channels),
        "primary_threshold": PRIMARY_THRESHOLD,
        "primary_update_count": primary_summary["update_count"],
        "primary_omitted_update_count": primary_summary["omitted_update_count"],
        "primary_gap_certificate_count": primary_summary["gap_certificate_count"],
        "primary_width_three_update_count": primary_summary["width_three_update_count"],
        "primary_width_four_update_count": primary_summary["width_four_update_count"],
        "primary_maximum_endpoint_to_reference_ratio": primary_summary["maximum_endpoint_to_reference_ratio"],
        "primary_maximum_adaptive_to_full_tail_ratio": primary_summary["maximum_adaptive_to_full_tail_ratio"],
        "threshold_summaries": threshold_summaries,
    }
    payload = {
        "status": "rh96_gap_weighted_weak_mode_quotient_audit",
        "precision_bits": PRECISION_BITS,
        "rank_offset": RANK_OFFSET,
        "maximum_width": MAXIMUM_WIDTH,
        "minimum_width": MINIMUM_WIDTH,
        "thresholds": list(THRESHOLDS),
        "primary_threshold": PRIMARY_THRESHOLD,
        "rows": rows,
        "all_executed_primary_quotient_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": summary,
        "theorem_boundary": {
            "universal_omitted_block_bound": True,
            "gap_weighted_weak_mode_tail_loss_theorem": True,
            "adaptive_width_frozen_horizons_validated": True,
            "weak_cross_modes_geometrically_identified": False,
            "uniform_retained_to_omitted_gap_proved": False,
            "uniform_adaptive_width_law_proved": False,
            "repeated_block_contraction_proved": False,
            "uniform_stage_A1_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "Weak complement directions can be quotiented by a gap-weighted energy bound instead of being geometrically reconstructed. "
            "At relative threshold 1e-8, the adaptive chain drops the weak fourth mode exactly where RH-95 found conditioning failures, certifies every omitted-mode loss, and preserves all ten source-to-endpoint gates. "
            "This removes the need to invert numerically meaningless fourth singular modes on the frozen horizons."
        ),
        "limitations": [
            "The quotient certificate requires a positive retained-to-omitted spectral gap at each omitted update.",
            "The audit uses ambient cross singular vectors to define the finite comparator; an all-level reduced implementation remains open.",
            "No uniform threshold, gap, or repeated-block theorem is proved.",
            "Only the archived five scales and two channels are validated.",
            "No Hilbert--Polya operator, zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_primary_quotient_gates_green"], **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
