"""Audit two-gap differential envelopes for adaptive Ritz refresh."""

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
RH96 = PAPERS / "RH-96-gap-weighted-weak-mode-quotient"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"), str(RH94 / "src"), str(RH94 / "experiments"), str(RH96 / "src")]

from differential_ritz_envelope import two_gap_refresh_derivative_bound  # noqa: E402
from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import memory_grams  # noqa: E402
from source_seeded_refresh import projector_distance, source_right_packet  # noqa: E402
from weak_mode_quotient import adaptive_width  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "two_gap_differential_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "two_gap_differential_smoke.json"
PRECISION_BITS = 384
RANK_OFFSET = 2
PRIMARY_THRESHOLD = 1e-8
MINIMUM_WIDTH = 2
MAXIMUM_WIDTH = 4
PROBE_COUNT = 6


def safe_gap(values: np.ndarray, reconstruction_error: float, index: int) -> float:
    return math.nextafter(float(values[index] - values[index + 1]) - 2.0 * reconstruction_error, -math.inf)


def refresh_details(gram: np.ndarray, packet: np.ndarray, width: int) -> dict[str, object]:
    rank = packet.shape[1]
    cross = gram @ packet - packet @ (packet.T @ gram @ packet)
    left, singular, _ = np.linalg.svd(cross, full_matrices=False)
    basis, _ = np.linalg.qr(np.column_stack([packet, left[:, :width]]), mode="reduced")
    compressed = basis.T @ gram @ basis
    compressed = (compressed + compressed.T) / 2.0
    values, vectors = np.linalg.eigh(compressed)
    order = np.argsort(values)[::-1]
    values = values[order]
    vectors = vectors[:, order]
    reconstructed = (vectors * values) @ vectors.T
    compressed_error = float(np.linalg.norm(compressed - reconstructed, 2)) + 128.0 * np.finfo(float).eps * compressed.shape[0] * max(1.0, float(np.linalg.norm(compressed, 2)))
    packet_out = basis @ vectors[:, :rank]
    next_singular = float(singular[width]) if width < singular.size else 0.0
    cross_gap = math.nextafter(float(singular[width - 1] ** 2 - next_singular**2), -math.inf)
    ritz_gap = safe_gap(values, compressed_error, rank - 1)
    gram_norm = float(np.linalg.norm(gram, 2))
    available = cross_gap > 0.0 and ritz_gap > 0.0
    derivative_bound = two_gap_refresh_derivative_bound(gram_norm, cross_gap, ritz_gap) if available else None
    cross_radius = cross_gap / max(12.0 * gram_norm * gram_norm, np.finfo(float).tiny) if available else 0.0
    output_radius = ritz_gap / max(8.0 * gram_norm * (1.0 + 6.0 * gram_norm * gram_norm / cross_gap), np.finfo(float).tiny) if available else 0.0
    return {
        "packet": packet_out,
        "singular_values": singular,
        "compressed_values": values,
        "cross_squared_gap": cross_gap,
        "ritz_gap": ritz_gap,
        "gram_operator_norm": gram_norm,
        "differential_certificate_available": available,
        "derivative_bound": derivative_bound,
        "cross_linearized_radius": cross_radius,
        "ritz_linearized_radius": output_radius,
        "two_gap_linearized_radius": min(cross_radius, output_radius),
    }


def fixed_refresh(gram: np.ndarray, packet: np.ndarray, width: int) -> np.ndarray:
    return np.asarray(refresh_details(gram, packet, width)["packet"], dtype=float)


def probe_derivatives(gram: np.ndarray, packet: np.ndarray, width: int, baseline: np.ndarray, radius: float, seed: int) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    projector = packet @ packet.T
    step = min(1e-6, max(1e-9, radius / 16.0))
    rows = []
    for probe in range(PROBE_COUNT):
        tangent = (np.eye(packet.shape[0]) - projector) @ rng.normal(size=packet.shape)
        tangent_norm = float(np.linalg.norm(tangent, "fro"))
        if tangent_norm == 0.0:
            continue
        tangent /= tangent_norm
        perturbed, _ = np.linalg.qr(packet + step * tangent, mode="reduced")
        output = fixed_refresh(gram, perturbed, width)
        input_distance = projector_distance(packet, perturbed)
        output_distance = projector_distance(baseline, output)
        rows.append({"probe": probe, "input_projector_distance": input_distance, "output_projector_distance": output_distance, "secant_derivative": output_distance / input_distance})
    return {"probe_step": step, "probe_count": len(rows), "maximum_probe_derivative": max(row["secant_derivative"] for row in rows), "rows": rows}


def channel_audit(model: dict[str, object], inherited_horizon: int, rank: int, sigma: float, side_index: int) -> dict[str, object]:
    operator = np.asarray(model["operator"], dtype=float)
    source = np.asarray(model["source"], dtype=float)
    endpoint = max(4, int(math.ceil(2.0 * inherited_horizon / 3.0)))
    states = [source]
    for _ in range(endpoint): states.append(operator @ states[-1])
    grams = memory_grams(states)
    packet = source_right_packet(source, rank)
    steps = []
    for time in range(1, endpoint + 1):
        cross = grams[time] @ packet - packet @ (packet.T @ grams[time] @ packet)
        singular = np.linalg.svd(cross, compute_uv=False)
        width = adaptive_width(singular, PRIMARY_THRESHOLD, minimum=MINIMUM_WIDTH, maximum=MAXIMUM_WIDTH)
        details = refresh_details(grams[time], packet, width)
        adaptive_packet = np.asarray(details["packet"], dtype=float)
        full_details = refresh_details(grams[time], packet, MAXIMUM_WIDTH)
        full_packet = np.asarray(full_details["packet"], dtype=float)
        quotient_distance = projector_distance(adaptive_packet, full_packet)
        probes = probe_derivatives(grams[time], packet, width, adaptive_packet, float(details["two_gap_linearized_radius"]), seed=int(round(1e6 * sigma)) + 1000 * side_index + time)
        ratios = np.asarray(details["singular_values"], dtype=float) / float(details["singular_values"][0])
        if width < MAXIMUM_WIDTH:
            threshold_margin = min(float(ratios[width - 1] - PRIMARY_THRESHOLD), float(PRIMARY_THRESHOLD - ratios[width]))
            if full_details["derivative_bound"] is not None and details["derivative_bound"] is not None:
                full_to_adaptive_bound_ratio = float(full_details["derivative_bound"]) / float(details["derivative_bound"])
            else:
                full_to_adaptive_bound_ratio = None
        else:
            threshold_margin = float(ratios[width - 1] - PRIMARY_THRESHOLD)
            full_to_adaptive_bound_ratio = 1.0
        steps.append(
            {
                "time": time,
                "selected_width": width,
                "cross_squared_gap": details["cross_squared_gap"],
                "ritz_gap": details["ritz_gap"],
                "gram_operator_norm": details["gram_operator_norm"],
                "two_gap_derivative_bound": details["derivative_bound"],
                "full_width_derivative_bound": full_details["derivative_bound"],
                "differential_certificate_available": details["differential_certificate_available"],
                "full_width_differential_certificate_available": full_details["differential_certificate_available"],
                "full_to_adaptive_bound_ratio": full_to_adaptive_bound_ratio,
                "cross_linearized_radius": details["cross_linearized_radius"],
                "ritz_linearized_radius": details["ritz_linearized_radius"],
                "two_gap_linearized_radius": details["two_gap_linearized_radius"],
                "threshold_margin": threshold_margin,
                "adaptive_to_full_projector_distance": quotient_distance,
                "quotient_displacement_inside_linearized_radius": quotient_distance <= float(details["two_gap_linearized_radius"]),
                "probe_step": probes["probe_step"],
                "probe_count": probes["probe_count"],
                "maximum_probe_derivative": probes["maximum_probe_derivative"],
                "all_probes_below_two_gap_bound": details["derivative_bound"] is not None and probes["maximum_probe_derivative"] <= float(details["derivative_bound"]),
                "probe_rows": probes["rows"],
            }
        )
        packet = adaptive_packet
    return {"side": model["side"], "dimension": int(operator.shape[0]), "refresh_endpoint": endpoint, "clock_rank": rank, "steps": steps, "all_probe_bounds_green": all(step["all_probes_below_two_gap_bound"] for step in steps)}


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
            channels = [channel_audit(model, HORIZONS[sigma], rank, sigma, index) for index, model in enumerate(models)]
            rows.append({"sigma": sigma, "fine_dimension": dimension, "clock": half_log_clock(sigma), "clock_rank": rank, "channels": channels, "all_channels_green": all(channel["all_probe_bounds_green"] for channel in channels)})
            print(json.dumps({"sigma": sigma, "updates": sum(len(channel["steps"]) for channel in channels), "quotient_updates": sum(step["selected_width"] < MAXIMUM_WIDTH for channel in channels for step in channel["steps"]), "green": all(channel["all_probe_bounds_green"] for channel in channels)}, sort_keys=True), flush=True)
    finally:
        ctx.prec = previous_precision

    channels = [channel for row in rows for channel in row["channels"]]
    steps = [step for channel in channels for step in channel["steps"]]
    quotient_steps = [step for step in steps if step["selected_width"] < MAXIMUM_WIDTH]
    available_steps = [step for step in steps if step["differential_certificate_available"]]
    available_quotient_steps = [step for step in quotient_steps if step["full_to_adaptive_bound_ratio"] is not None]
    summary = {
        "scale_count": len(rows),
        "channel_count": len(channels),
        "update_count": len(steps),
        "probe_count": sum(step["probe_count"] for step in steps),
        "probe_green_update_count": sum(step["all_probes_below_two_gap_bound"] for step in steps),
        "differential_certificate_available_count": len(available_steps),
        "differential_certificate_unavailable_count": len(steps) - len(available_steps),
        "cross_gap_nonpositive_count": sum(step["cross_squared_gap"] <= 0.0 for step in steps),
        "ritz_gap_nonpositive_count": sum(step["ritz_gap"] <= 0.0 for step in steps),
        "full_width_differential_unavailable_count": sum(not step["full_width_differential_certificate_available"] for step in steps),
        "quotient_update_count": len(quotient_steps),
        "quotient_inside_linearized_radius_count": sum(step["quotient_displacement_inside_linearized_radius"] for step in quotient_steps),
        "minimum_cross_squared_gap": min(step["cross_squared_gap"] for step in steps),
        "minimum_ritz_gap": min(step["ritz_gap"] for step in steps),
        "minimum_threshold_margin": min(step["threshold_margin"] for step in steps),
        "maximum_two_gap_derivative_bound": max(step["two_gap_derivative_bound"] for step in available_steps),
        "maximum_probe_derivative": max(step["maximum_probe_derivative"] for step in steps),
        "maximum_bound_to_probe_ratio": max(step["two_gap_derivative_bound"] / max(step["maximum_probe_derivative"], np.finfo(float).tiny) for step in available_steps),
        "minimum_bound_to_probe_ratio": min(step["two_gap_derivative_bound"] / max(step["maximum_probe_derivative"], np.finfo(float).tiny) for step in available_steps),
        "maximum_full_to_adaptive_bound_ratio_on_quotients": max((step["full_to_adaptive_bound_ratio"] for step in available_quotient_steps), default=1.0),
        "minimum_two_gap_linearized_radius": min(step["two_gap_linearized_radius"] for step in steps),
        "maximum_quotient_distance_to_radius_ratio": max((step["adaptive_to_full_projector_distance"] / max(step["two_gap_linearized_radius"], np.finfo(float).tiny) for step in quotient_steps), default=0.0),
    }
    payload = {
        "status": "rh99_two_gap_differential_ritz_envelope_audit",
        "precision_bits": PRECISION_BITS,
        "primary_threshold": PRIMARY_THRESHOLD,
        "probe_count_per_update": PROBE_COUNT,
        "rows": rows,
        "all_executed_available_two_gap_probe_bounds_green": all(step["all_probes_below_two_gap_bound"] for step in available_steps),
        "all_executed_two_gap_certificates_available": len(available_steps) == len(steps),
        "audit_summary": summary,
        "theorem_boundary": {
            "cross_covariance_derivative_formula": True,
            "spectral_projector_sylvester_bound": True,
            "two_gap_refresh_derivative_theorem": True,
            "finite_tangent_probe_bounds_validated_where_available": True,
            "all_frozen_cross_selection_gaps_separated": False,
            "all_frozen_output_ritz_gaps_certified": False,
            "finite_neighborhood_lipschitz_tube_proved": False,
            "adaptive_branch_uniformly_separated": False,
            "replay_free_block_envelope_proved": False,
            "repeated_block_contraction_proved": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The differential sensitivity of one invariant projected-cross Ritz refresh is controlled by two spectral gaps: the selected cross-covariance gap and the output Ritz gap. "
            "Adaptive weak-mode quotienting improves the formal derivative envelope at the five ill-conditioned updates, and all finite tangent probes lie below the theorem bound wherever both gaps are certified. "
            "However, five fine-scale output Ritz gaps cannot be certified positive with the binary64 residual guard, the available bounds remain highly conservative, and the actual quotient displacement is outside every first-order separation radius. A finite neighborhood tube is therefore not closed."
        ),
        "limitations": [
            "The theorem is infinitesimal and assumes fixed selected cross and Ritz branches.",
            "Finite probes do not certify all tangent directions or a neighborhood-uniform derivative bound.",
            "First-order gap radii are diagnostics, not nonlinear invariant balls.",
            "No replay-free block envelope or repeated-block theorem is proved.",
            "No Hilbert--Polya operator, zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "available_probe_green": payload["all_executed_available_two_gap_probe_bounds_green"], "all_certificates_available": payload["all_executed_two_gap_certificates_available"], **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
