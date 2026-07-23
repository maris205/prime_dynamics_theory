"""Audit finite-memory exterior-power fourth-cross support certificates."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

from flint import ctx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
RH95 = PAPERS / "RH-95-reduced-projected-cross-moment-factorization"
RH96 = PAPERS / "RH-96-gap-weighted-weak-mode-quotient"
RH101 = PAPERS / "RH-101-finite-memory-packet-gram-action"
RH108 = PAPERS / "RH-108-finite-memory-fourth-cross-support"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH77 / "experiments"),
    str(RH82 / "src"),
    str(RH94 / "src"),
    str(RH94 / "experiments"),
    str(RH95 / "src"),
    str(RH96 / "src"),
    str(RH96 / "experiments"),
    str(RH101 / "src"),
    str(RH108 / "src"),
]

from exterior_fourth_support import (  # noqa: E402
    elementary_symmetric_four,
    exterior_dimension,
    finite_memory_exterior_certificate,
    normalized_spectral_four_volume,
    normalized_trace_four_volume,
    sharp_scalar_volume_barrier,
    trace_four_volume,
    volume_loss_factor,
)
from finite_memory_gram import packet_action, truncated_memory_gram  # noqa: E402
from fourth_cross_support import finite_tail_operator_bound, fourth_support_certificate  # noqa: E402
from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from reduced_cross_factorization import cross_moment_matrices  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import ETA, memory_grams  # noqa: E402
from run_weak_mode_quotient_audit import one_step  # noqa: E402
from source_seeded_refresh import source_right_packet  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "exterior_fourth_support_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "exterior_fourth_support_smoke.json"
PRECISION_BITS = 384
DEPTH = 5
RANK_OFFSET = 2
MAXIMUM_WIDTH = 4
THRESHOLDS = (1e-8, 1e-6, 1e-4)
BINARY64_ACTION_GUARD = 2e-14


def relative_error(first: float | np.ndarray, second: float | np.ndarray) -> float:
    left = np.asarray(first, dtype=float)
    right = np.asarray(second, dtype=float)
    denominator = max(float(np.linalg.norm(right.ravel())), np.finfo(float).tiny)
    return float(np.linalg.norm((left - right).ravel()) / denominator)


def state_history(model: dict[str, object], endpoint: int) -> list[np.ndarray]:
    operator = np.asarray(model["operator"], dtype=float)
    source = np.asarray(model["source"], dtype=float)
    states = [source]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    return states


def scale_channel_audit(
    model: dict[str, object],
    sigma: float,
    inherited_horizon: int,
    threshold: float,
    rank: int,
) -> dict[str, object]:
    endpoint = max(4, int(math.ceil(2.0 * inherited_horizon / 3.0)))
    states = state_history(model, endpoint)
    grams = memory_grams(states)
    packet = source_right_packet(states[0], rank)
    steps: list[dict[str, object]] = []

    for time in range(1, endpoint + 1):
        gram = grams[time]
        applied = packet_action(states, packet, eta=ETA, time=time, depth=DEPTH)
        recent_gram = truncated_memory_gram(states, eta=ETA, time=time, depth=DEPTH)
        projected_recent = applied - packet @ (packet.T @ applied)
        recent_singular = np.linalg.svd(projected_recent, compute_uv=False)
        past_count = max(0, time - DEPTH + 1)
        analytic_tail_bound = finite_tail_operator_bound(ETA, DEPTH, past_count)
        tail_bound = math.nextafter(analytic_tail_bound + BINARY64_ACTION_GUARD, math.inf)
        exterior = finite_memory_exterior_certificate(recent_singular, tail_bound, threshold)
        direct = fourth_support_certificate(recent_singular, tail_bound, threshold)

        full_cross = gram @ packet - packet @ (packet.T @ gram @ packet)
        full_singular = np.linalg.svd(full_cross, compute_uv=False)
        actual_ratio = float(full_singular[3] / full_singular[0])
        actual_volume = normalized_spectral_four_volume(full_singular)
        actual_trace_volume = normalized_trace_four_volume(full_singular)
        actual_loss_factor = volume_loss_factor(full_singular)
        observed_cross_error = float(np.linalg.norm(full_cross - projected_recent, 2))

        first, second, _, moment_cross, _ = cross_moment_matrices(recent_gram, packet)
        direct_cross_gram = projected_recent.T @ projected_recent
        direct_eigenvalues = np.linalg.eigvalsh((direct_cross_gram + direct_cross_gram.T) / 2.0)
        direct_eigenvalues = np.clip(direct_eigenvalues, 0.0, None)
        direct_trace_from_gram = math.sqrt(elementary_symmetric_four(direct_eigenvalues))
        direct_trace_from_singular = trace_four_volume(recent_singular)
        cancellation_index = (
            float(np.linalg.norm(second, "fro")) + float(np.linalg.norm(first @ first, "fro"))
        ) / max(float(np.linalg.norm(direct_cross_gram, "fro")), np.finfo(float).tiny)

        next_packet, selector_record = one_step(gram, packet, threshold)
        selected_width = int(selector_record["selected_width"])
        expected_width_four = actual_ratio >= threshold
        volume_tolerance = 5e-14
        exterior_count = exterior_dimension(rank)
        steps.append(
            {
                "time": time,
                "threshold": threshold,
                "selected_width": selected_width,
                "actual_ratio": actual_ratio,
                "actual_support": expected_width_four,
                "actual_normalized_spectral_volume": actual_volume,
                "actual_normalized_trace_volume": actual_trace_volume,
                "actual_volume_loss_factor": actual_loss_factor,
                "actual_volume_identity_relative_error": relative_error(actual_volume, actual_ratio * actual_loss_factor),
                "spectral_volume_lower_bound": float(exterior["spectral_volume_lower_bound"]),
                "trace_volume_lower_bound": float(exterior["trace_volume_lower_bound"]),
                "weyl_ratio_lower_bound": float(direct["ratio_lower_bound"]),
                "spectral_support_certified": bool(exterior["spectral_support_certified"]),
                "trace_support_certified": bool(exterior["trace_support_certified"]),
                "weyl_support_certified": bool(direct["support_certified"]),
                "packet_rank": rank,
                "exterior_dimension": exterior_count,
                "recent_leading_singular_value": float(recent_singular[0]),
                "recent_fourth_singular_value": float(recent_singular[3]),
                "tail_operator_bound": tail_bound,
                "analytic_tail_operator_bound": analytic_tail_bound,
                "binary64_action_guard": BINARY64_ACTION_GUARD,
                "observed_cross_error": observed_cross_error,
                "observed_cross_error_bounded": observed_cross_error <= tail_bound,
                "tail_snapshot_count": past_count,
                "moment_cross_gram_relative_error": relative_error(moment_cross, direct_cross_gram),
                "moment_cancellation_index": cancellation_index,
                "direct_exterior_trace_identity_relative_error": relative_error(
                    direct_trace_from_gram, direct_trace_from_singular
                ),
                "trace_below_spectral_certificate": (
                    float(exterior["trace_volume_lower_bound"])
                    <= float(exterior["spectral_volume_lower_bound"]) + volume_tolerance
                ),
                "spectral_certificate_implication_holds": (
                    not bool(exterior["spectral_support_certified"])
                )
                or expected_width_four,
                "trace_certificate_implication_holds": (
                    not bool(exterior["trace_support_certified"])
                )
                or expected_width_four,
                "volume_ordering_holds": (
                    actual_ratio**3 <= actual_volume + volume_tolerance
                    and actual_volume <= actual_ratio + volume_tolerance
                    and actual_volume <= actual_trace_volume + volume_tolerance
                    and actual_trace_volume <= math.sqrt(exterior_count) * actual_volume + volume_tolerance
                ),
                "selector_equivalence_holds": (selected_width == MAXIMUM_WIDTH) == expected_width_four,
            }
        )
        packet = next_packet

    return {
        "sigma": sigma,
        "side": model["side"],
        "dimension": int(np.asarray(model["operator"]).shape[0]),
        "refresh_endpoint": endpoint,
        "clock_rank": rank,
        "threshold": threshold,
        "steps": steps,
    }


def barrier_audit() -> dict[str, object]:
    volumes = [1.0, 1e-1, 1e-3, 1e-6, 1e-9, 1e-12, 0.0]
    reference = sharp_scalar_volume_barrier(volumes[0], eta=ETA)["linear"]
    rows = []
    for volume in volumes:
        data = sharp_scalar_volume_barrier(volume, eta=ETA)
        linear = data["linear"]
        cubic = data["cubic"]
        rows.append(
            {
                "normalized_volume": volume,
                "linear_ratio": float(linear["ratio"]),
                "cubic_ratio": float(cubic["ratio"]),
                "expected_linear_ratio": volume,
                "expected_cubic_ratio": volume ** (1.0 / 3.0),
                "linear_volume": float(linear["normalized_volume"]),
                "cubic_volume": float(cubic["normalized_volume"]),
                "linear_minimum_snapshot_eigenvalue": float(np.linalg.eigvalsh(linear["snapshot"]).min()),
                "cubic_minimum_snapshot_eigenvalue": float(np.linalg.eigvalsh(cubic["snapshot"]).min()),
                "linear_trace_clock": float(linear["trace_clock"]),
                "cubic_trace_clock": float(cubic["trace_clock"]),
                "packet_block_distance": max(
                    float(np.linalg.norm(linear["packet_block"] - reference["packet_block"], 2)),
                    float(np.linalg.norm(cubic["packet_block"] - reference["packet_block"], 2)),
                ),
                "complement_block_distance": max(
                    float(np.linalg.norm(linear["complement_block"] - reference["complement_block"], 2)),
                    float(np.linalg.norm(cubic["complement_block"] - reference["complement_block"], 2)),
                ),
            }
        )
    return {
        "eta": ETA,
        "rows": rows,
        "all_trace_clocks_constant": all(
            abs(row["linear_trace_clock"] - (1.0 + ETA)) < 1e-13
            and abs(row["cubic_trace_clock"] - (1.0 + ETA)) < 1e-13
            for row in rows
        ),
        "all_diagonal_blocks_constant": all(
            row["packet_block_distance"] < 1e-13 and row["complement_block_distance"] < 1e-13
            for row in rows
        ),
        "all_snapshots_psd": all(
            row["linear_minimum_snapshot_eigenvalue"] > -1e-13
            and row["cubic_minimum_snapshot_eigenvalue"] > -1e-13
            for row in rows
        ),
        "maximum_volume_formula_error": max(
            max(abs(row["linear_volume"] - row["normalized_volume"]), abs(row["cubic_volume"] - row["normalized_volume"]))
            for row in rows
        ),
        "maximum_endpoint_ratio_error": max(
            max(
                abs(row["linear_ratio"] - row["expected_linear_ratio"]),
                abs(row["cubic_ratio"] - row["expected_cubic_ratio"]),
            )
            for row in rows
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows: list[dict[str, object]] = []
    try:
        sigmas = SIGMAS[:1] if args.smoke else SIGMAS
        for sigma in sigmas:
            rank = clock_rank(sigma, offset=RANK_OFFSET)
            _, models = build_models(sigma)
            channels = []
            for model in models:
                thresholds = [
                    scale_channel_audit(model, sigma, HORIZONS[sigma], threshold, rank)
                    for threshold in THRESHOLDS
                ]
                channels.append({"side": model["side"], "thresholds": thresholds})
            rows.append(
                {
                    "sigma": sigma,
                    "clock": half_log_clock(sigma),
                    "clock_rank": rank,
                    "channels": channels,
                }
            )
            for channel in channels:
                primary = channel["thresholds"][0]
                print(
                    json.dumps(
                        {
                            "sigma": sigma,
                            "side": channel["side"],
                            "minimum_actual_volume": min(
                                step["actual_normalized_spectral_volume"] for step in primary["steps"]
                            ),
                            "minimum_spectral_lower": min(
                                step["spectral_volume_lower_bound"] for step in primary["steps"]
                            ),
                            "spectral_support_count": sum(
                                step["spectral_support_certified"] for step in primary["steps"]
                            ),
                            "update_count": len(primary["steps"]),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    finally:
        ctx.prec = previous_precision

    records = [
        (row["sigma"], channel["side"], record)
        for row in rows
        for channel in row["channels"]
        for record in channel["thresholds"]
    ]
    all_steps = [step for _, _, record in records for step in record["steps"]]
    threshold_summary: dict[str, object] = {}
    executed_sigmas = [float(value) for value in (SIGMAS[:1] if args.smoke else SIGMAS)]
    for threshold in THRESHOLDS:
        key = f"{threshold:.0e}"
        selected = [record for _, _, record in records if record["threshold"] == threshold]
        scale_summary = []
        for sigma in executed_sigmas:
            scale_records = [record for record in selected if record["sigma"] == sigma]
            steps = [step for record in scale_records for step in record["steps"]]
            scale_summary.append(
                {
                    "sigma": sigma,
                    "update_count": len(steps),
                    "spectral_support_count": sum(step["spectral_support_certified"] for step in steps),
                    "trace_support_count": sum(step["trace_support_certified"] for step in steps),
                    "weyl_support_count": sum(step["weyl_support_certified"] for step in steps),
                    "actual_support_count": sum(step["actual_support"] for step in steps),
                    "minimum_spectral_volume_lower_bound": min(
                        (step["spectral_volume_lower_bound"] for step in steps), default=None
                    ),
                    "minimum_trace_volume_lower_bound": min(
                        (step["trace_volume_lower_bound"] for step in steps), default=None
                    ),
                    "minimum_actual_normalized_volume": min(
                        (step["actual_normalized_spectral_volume"] for step in steps), default=None
                    ),
                    "minimum_actual_ratio": min((step["actual_ratio"] for step in steps), default=None),
                }
            )
        fine_scales = [item for item in scale_summary if item["sigma"] <= 0.02]
        threshold_summary[key] = {
            "threshold": threshold,
            "scale_summary": scale_summary,
            "spectral_certificate_count": sum(record["spectral_support_count"] for record in scale_summary),
            "trace_certificate_count": sum(record["trace_support_count"] for record in scale_summary),
            "weyl_certificate_count": sum(record["weyl_support_count"] for record in scale_summary),
            "actual_support_count": sum(record["actual_support_count"] for record in scale_summary),
            "fine_update_count": sum(record["update_count"] for record in fine_scales),
            "fine_spectral_certificate_count": sum(record["spectral_support_count"] for record in fine_scales),
            "fine_trace_certificate_count": sum(record["trace_support_count"] for record in fine_scales),
            "fine_weyl_certificate_count": sum(record["weyl_support_count"] for record in fine_scales),
            "fine_spectral_certificate_green": bool(fine_scales) and all(
                record["spectral_support_count"] == record["update_count"] for record in fine_scales
            ),
            "fine_trace_certificate_green": bool(fine_scales) and all(
                record["trace_support_count"] == record["update_count"] for record in fine_scales
            ),
            "minimum_fine_spectral_volume_lower_bound": min(
                (record["minimum_spectral_volume_lower_bound"] for record in fine_scales), default=None
            ),
            "minimum_fine_trace_volume_lower_bound": min(
                (record["minimum_trace_volume_lower_bound"] for record in fine_scales), default=None
            ),
        }

    barrier = barrier_audit()
    fine_steps = [step for sigma, _, record in records if sigma <= 0.02 for step in record["steps"]]
    reported_fine_steps = fine_steps if fine_steps else all_steps
    summary = {
        "scale_count": len(rows),
        "channel_count": sum(len(row["channels"]) for row in rows),
        "threshold_count": len(THRESHOLDS),
        "update_count": len(all_steps),
        "fine_update_count": len(fine_steps),
        "minimum_fine_spectral_volume_lower_bound": min(
            step["spectral_volume_lower_bound"] for step in reported_fine_steps
        ),
        "minimum_fine_trace_volume_lower_bound": min(step["trace_volume_lower_bound"] for step in reported_fine_steps),
        "minimum_fine_actual_normalized_volume": min(
            step["actual_normalized_spectral_volume"] for step in reported_fine_steps
        ),
        "minimum_fine_actual_ratio": min(step["actual_ratio"] for step in reported_fine_steps),
        "minimum_fine_volume_loss_factor": min(step["actual_volume_loss_factor"] for step in reported_fine_steps),
        "maximum_fine_volume_loss_factor": max(step["actual_volume_loss_factor"] for step in reported_fine_steps),
        "maximum_actual_volume_identity_relative_error": max(
            step["actual_volume_identity_relative_error"] for step in all_steps
        ),
        "maximum_direct_exterior_trace_identity_relative_error": max(
            step["direct_exterior_trace_identity_relative_error"] for step in all_steps
        ),
        "maximum_moment_cross_gram_relative_error": max(step["moment_cross_gram_relative_error"] for step in all_steps),
        "maximum_moment_cancellation_index": max(step["moment_cancellation_index"] for step in all_steps),
        "spectral_certificate_implication_violation_count": sum(
            not step["spectral_certificate_implication_holds"] for step in all_steps
        ),
        "trace_certificate_implication_violation_count": sum(
            not step["trace_certificate_implication_holds"] for step in all_steps
        ),
        "spectral_trace_certificate_order_failure_count": sum(
            not step["trace_below_spectral_certificate"] for step in all_steps
        ),
        "volume_ordering_violation_count": sum(not step["volume_ordering_holds"] for step in all_steps),
        "selector_equivalence_failure_count": sum(not step["selector_equivalence_holds"] for step in all_steps),
        "observed_cross_error_bound_failure_count": sum(
            not step["observed_cross_error_bounded"] for step in all_steps
        ),
        "maximum_tail_operator_bound": max(step["tail_operator_bound"] for step in all_steps),
    }
    payload = {
        "status": "rh109_exterior_power_fourth_cross_support_audit",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "depth": DEPTH,
        "binary64_action_guard": BINARY64_ACTION_GUARD,
        "rank_offset": RANK_OFFSET,
        "thresholds": list(THRESHOLDS),
        "rows": rows,
        "threshold_summary": threshold_summary,
        "barrier": barrier,
        "audit_summary": summary,
        "theorem_boundary": {
            "finite_memory_spectral_exterior_certificate": True,
            "finite_memory_trace_exterior_certificate": True,
            "sharp_scalar_volume_interval": True,
            "exact_source_seeded_scalar_volume_barrier": True,
            "reduced_moment_spectral_trace_distinction": True,
            "fine_tau_1e8_exterior_support_validated": not args.smoke,
            "all_level_physical_exterior_lower_bound_proved": False,
            "all_level_loss_factor_control_proved": False,
            "uniform_fine_support_separation_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "zero_identification": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The recent projected cross supplies a rigorous finite-memory spectral four-volume lower bound, and the two finest archived scales clear tau=1e-8 at every update. The normalized four-volume equals the fourth ratio times the second/third relative capacity factor. Its scalar inversion interval is sharp, so volume alone cannot recover the direct fourth-mode certificate inside the band between tau^3 and tau. An all-level continuation needs a physical wedge lower bound together with capacity information, or a direct fourth-mode transversality law."
        ),
        "limitations": [
            "The five-scale replay is a finite binary64 validation with an explicit action guard, not an all-level interval proof.",
            "For packet rank above four, e4(K*K) is the trace of the fourth exterior Gramian, not its leading eigenvalue; the trace certificate pays the exact binomial dimension factor.",
            "The sharp barrier lies in the admissible normalized-memory/source-seed class but is not a counterexample to the folded-Gaussian physical family.",
            "No uniform Stage A, Hilbert--Polya operator, zero identification, or Riemann Hypothesis conclusion is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
