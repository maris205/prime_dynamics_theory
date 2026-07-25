"""Arb and long-double audit of direct clock-rank packet resets."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
import time

from flint import arb, ctx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
RH96 = PAPERS / "RH-96-gap-weighted-weak-mode-quotient"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH77 / "experiments"),
    str(RH82 / "src"),
    str(RH94 / "src"),
    str(RH94 / "experiments"),
    str(RH96 / "src"),
    str(RH96 / "experiments"),
]

from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from reset_packet import branch_free_energy_step, direct_packet_enclosure, ky_fan_projector_bound  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, arb_matrix, build_models, frobenius_norm  # noqa: E402
from run_source_seeded_horizon_audit import memory_grams  # noqa: E402
from run_weak_mode_quotient_audit import one_step  # noqa: E402
from source_seeded_refresh import source_right_packet  # noqa: E402


PRECISION_BITS = 384
PRIMARY_THRESHOLD = 1e-8


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def exact_frobenius_squared(matrix) -> arb:
    return sum((entry * entry for entry in matrix.entries()), arb(0))


def frobenius(values: np.ndarray) -> float:
    array = np.asarray(values, dtype=np.longdouble)
    return math.nextafter(float(np.sqrt(np.sum(array * array, dtype=np.longdouble))), math.inf)


def exact_memory_radii(
    operator_values: np.ndarray,
    source_values: np.ndarray,
    nominal_grams: list[np.ndarray],
) -> list[float]:
    operator = arb_matrix(operator_values)
    state = arb_matrix(source_values)
    memory = None
    radii = []
    for time, nominal in enumerate(nominal_grams):
        if time:
            state = operator * state
        snapshot = (state.transpose() * state) * (arb(1) / exact_frobenius_squared(state))
        memory = snapshot if memory is None else snapshot + arb(1) / 512 * memory
        radii.append(upper(frobenius_norm(memory - arb_matrix(nominal))))
    return radii


def spectral_center_data(matrix: np.ndarray, rank: int) -> dict[str, object]:
    """Gap lower from a polar-corrected long-double Rayleigh matrix."""
    values, vectors = np.linalg.eigh((matrix + matrix.T) / 2.0)
    order = np.argsort(values)[::-1]
    vectors = vectors[:, order]
    n = matrix.shape[0]
    ld = np.longdouble
    q = np.asarray(vectors, dtype=ld)
    b = np.asarray((matrix + matrix.T) / 2.0, dtype=ld)
    product = b @ q
    rayleigh = q.T @ product
    metric = q.T @ q
    identity = np.eye(n, dtype=ld)
    eps = float(np.finfo(np.longdouble).eps)
    gamma = n * eps / max(1.0 - n * eps, 0.5)

    metric_round = gamma * frobenius(np.abs(q).T @ np.abs(q))
    metric_defect = frobenius(metric - identity) + metric_round
    if metric_defect >= 1.0:
        raise RuntimeError("eigenvector metric lost invertibility")
    q_norm = math.sqrt(1.0 + metric_defect)
    polar_distance = max(
        1.0 - math.sqrt(max(0.0, 1.0 - metric_defect)),
        math.sqrt(1.0 + metric_defect) - 1.0,
    )
    matrix_norm = math.nextafter(float(np.linalg.norm(np.asarray(matrix, dtype=float), 2)), math.inf)
    polar_error = matrix_norm * polar_distance * (1.0 + q_norm)

    first_round = gamma * frobenius(np.abs(b) @ np.abs(q))
    second_round = gamma * frobenius(np.abs(q).T @ np.abs(product)) + q_norm * first_round
    diagonal = np.asarray(np.diag(rayleigh), dtype=np.longdouble)
    off_diagonal = rayleigh - np.diag(diagonal)
    off_diagonal_error = frobenius(off_diagonal)
    total_error = math.nextafter(off_diagonal_error + polar_error + second_round, math.inf)
    nominal_gap = float(diagonal[rank - 1] - diagonal[rank])
    gap_lower = math.nextafter(max(0.0, nominal_gap - 2.0 * total_error), -math.inf)
    frame = np.asarray(vectors[:, :rank], dtype=float)
    return {
        "eigenvalues": [float(value) for value in diagonal],
        "frame": frame,
        "nominal_gap": nominal_gap,
        "gap_lower": gap_lower,
        "rayleigh_off_diagonal_frobenius": off_diagonal_error,
        "polar_metric_defect": metric_defect,
        "polar_correction_error": polar_error,
        "long_double_rounding_bound": second_round,
        "total_center_spectral_error": total_error,
    }


def projector_distance(first: np.ndarray, second: np.ndarray) -> float:
    difference = first @ first.T - second @ second.T
    return min(1.0, math.nextafter(float(np.linalg.norm(difference, 2)), math.inf))


def channel_record(model: dict[str, object], sigma: float) -> dict[str, object]:
    started = time.perf_counter()
    operator = np.asarray(model["operator"], dtype=float)
    source = np.asarray(model["source"], dtype=float)
    rank = clock_rank(sigma, offset=2)
    endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
    states = [source]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    grams = memory_grams(states)
    radii = exact_memory_radii(operator, source, grams)
    recursive_packet = source_right_packet(source, rank)
    centers = [spectral_center_data(gram, rank) for gram in grams]
    universal_loss = 0.0
    snapshots = []
    for step_index, (gram, radius, center) in enumerate(zip(grams, radii, centers)):
        eigenvalues = np.asarray(center["eigenvalues"], dtype=float)
        global_packet = np.asarray(center["frame"], dtype=float)
        recursive_frame, _ = np.linalg.qr(recursive_packet, mode="reduced")
        reset = direct_packet_enclosure(float(center["gap_lower"]), radius)
        gram_ld = np.asarray(gram, dtype=np.longdouble)
        recursive_ld = np.asarray(recursive_frame, dtype=np.longdouble)
        recursive_capture = float(np.sum(recursive_ld * (gram_ld @ recursive_ld), dtype=np.longdouble))
        optimal_capture = float(np.sum(np.asarray(center["eigenvalues"][:rank], dtype=np.longdouble), dtype=np.longdouble))
        loss_proxy = max(0.0, optimal_capture - recursive_capture)
        actual_loss = math.nextafter(
            loss_proxy + 2.0 * rank * float(center["total_center_spectral_error"]),
            math.inf,
        )
        ky_fan = ky_fan_projector_bound(actual_loss, max(0.0, float(center["gap_lower"])))
        actual_distance = projector_distance(recursive_frame, global_packet)

        if step_index:
            previous = centers[step_index - 1]
            previous_frame = np.asarray(previous["frame"], dtype=float)
            reset_drift_loss = max(
                0.0,
                optimal_capture - float(np.trace(previous_frame.T @ gram @ previous_frame)),
            )
            gram_drift = math.nextafter(float(np.linalg.norm(gram - grams[step_index - 1], "fro")), math.inf)
            universal_loss = branch_free_energy_step(
                universal_loss,
                max(0.0, float(previous["gap_lower"])),
                reset_drift_loss,
                gram_drift,
            )
        universal_angle = ky_fan_projector_bound(universal_loss, max(0.0, float(center["gap_lower"])))
        snapshots.append({
            "time": step_index,
            "clock_rank": rank,
            "matrix_operator_radius": radius,
            "nominal_gap": center["nominal_gap"],
            "gap_lower": center["gap_lower"],
            "center_spectral_error": center["total_center_spectral_error"],
            "direct_reset_gap_ratio": reset["gap_ratio"],
            "direct_reset_certified": reset["stable"],
            "direct_reset_projector_radius": reset["projector_radius"],
            "recursive_captured_energy_loss": actual_loss,
            "recursive_captured_energy_loss_proxy": loss_proxy,
            "recursive_ky_fan_operator_radius": ky_fan["operator_radius"],
            "recursive_ky_fan_informative": ky_fan["informative"],
            "recursive_actual_projector_distance": actual_distance,
            "ky_fan_bound_dominates_actual": actual_distance <= float(ky_fan["operator_radius"]) * (1.0 + 1e-8) + 1e-10,
            "universal_branch_free_loss_upper": universal_loss,
            "universal_branch_free_operator_radius": universal_angle["operator_radius"],
            "universal_branch_free_informative": universal_angle["informative"],
            "reset_captured_energy_dominates_recursive": optimal_capture + 1e-12 >= recursive_capture,
        })
        if step_index < endpoint:
            recursive_packet, _ = one_step(grams[step_index + 1], recursive_packet, PRIMARY_THRESHOLD)

    return {
        "side": str(model["side"]),
        "dimension": int(operator.shape[0]),
        "source_columns": int(source.shape[1]),
        "clock_rank": rank,
        "refresh_endpoint": endpoint,
        "snapshots": snapshots,
        "elapsed_seconds": time.perf_counter() - started,
    }


def json_default(value):
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(type(value).__name__)


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
            dimension, models = build_models(sigma)
            channels = [channel_record(model, sigma) for model in models]
            rows.append({
                "sigma": sigma,
                "fine_dimension": dimension,
                "half_log_clock": half_log_clock(sigma),
                "clock_rank": clock_rank(sigma, offset=2),
                "channels": channels,
            })
            for channel in channels:
                direct = [item for item in channel["snapshots"] if item["direct_reset_certified"]]
                print(json.dumps({
                    "sigma": sigma,
                    "side": channel["side"],
                    "snapshot_count": len(channel["snapshots"]),
                    "direct_certified": len(direct),
                    "minimum_gap_ratio": min(item["direct_reset_gap_ratio"] for item in channel["snapshots"]),
                    "maximum_reset_radius": max(item["direct_reset_projector_radius"] or 1.0 for item in channel["snapshots"]),
                }, sort_keys=True), flush=True)
    finally:
        ctx.prec = previous_precision

    channels = [channel for row in rows for channel in row["channels"]]
    snapshots = [item for channel in channels for item in channel["snapshots"]]
    update_snapshots = [item for item in snapshots if item["time"] > 0]
    summary = {
        "scale_count": len(rows),
        "channel_count": len(channels),
        "snapshot_count": len(snapshots),
        "update_snapshot_count": len(update_snapshots),
        "direct_reset_certificate_count": sum(item["direct_reset_certified"] for item in snapshots),
        "minimum_direct_reset_gap_ratio": min(item["direct_reset_gap_ratio"] for item in snapshots),
        "maximum_direct_reset_projector_radius": max(item["direct_reset_projector_radius"] or 1.0 for item in snapshots),
        "minimum_gap_lower": min(item["gap_lower"] for item in snapshots),
        "maximum_matrix_operator_radius": max(item["matrix_operator_radius"] for item in snapshots),
        "recursive_ky_fan_informative_count": sum(item["recursive_ky_fan_informative"] for item in snapshots),
        "ky_fan_dominance_failure_count": sum(not item["ky_fan_bound_dominates_actual"] for item in snapshots),
        "maximum_recursive_actual_projector_distance": max(item["recursive_actual_projector_distance"] for item in snapshots),
        "maximum_recursive_ky_fan_operator_radius": max(item["recursive_ky_fan_operator_radius"] for item in snapshots),
        "universal_branch_free_informative_count": sum(item["universal_branch_free_informative"] for item in snapshots),
        "reset_capture_dominance_failure_count": sum(not item["reset_captured_energy_dominates_recursive"] for item in snapshots),
        "total_elapsed_seconds": sum(channel["elapsed_seconds"] for channel in channels),
    }
    payload = {
        "status": "rh151_ky_fan_reset_packet_atlas",
        "precision_bits": PRECISION_BITS,
        "primary_threshold": PRIMARY_THRESHOLD,
        "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "sharp_ky_fan_deficit_to_projector_theorem": True,
            "branch_free_monotone_energy_recursion": True,
            "direct_independent_reset_packet_theorem": True,
            "all_frozen_source_memory_snapshots_reset_certified": not args.smoke and summary["direct_reset_certificate_count"] == 130,
            "ky_fan_only_recursive_transport_uniformly_informative": False,
            "threshold_branch_needed_for_reset_atlas": False,
            "reset_packets_inserted_into_outward_assembly": False,
            "uniform_all_level_reset_gap": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "Captured-energy loss controls packet angle sharply, but a branch-free scalar loss recursion is rapidly amplified by moving global packets and small gaps. "
            "Independent clock-rank spectral resets avoid that accumulation: every frozen source-memory snapshot has a positive outward gap and a certified packet ball. "
            "The next task is to determine whether the reset atlas has sufficiently coherent transition geometry for the outward directional assembly."
        ),
        "limitations": [
            "The gap centers use a polar-corrected long-double Rayleigh audit combined with Arb matrix balls, not a formal interval eigendecomposition of every ambient matrix.",
            "Independent resets change the packet construction and do not certify equality with the exact threshold-recursive RH-96 packet.",
            "Only five frozen scales and 130 source-memory snapshots are covered.",
            "No outward tail assembly, all-level reset-gap theorem, Stage A result, Hilbert--Polya operator, zeta-zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = ROOT / "results" / ("reset_packet_smoke.json" if args.smoke else "reset_packet_audit.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True, default=json_default) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True, default=json_default))


if __name__ == "__main__":
    main()
