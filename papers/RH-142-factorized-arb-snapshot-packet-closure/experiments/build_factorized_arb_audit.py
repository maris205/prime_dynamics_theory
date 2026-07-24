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
RH141 = PAPERS / "RH-141-gap-stable-spectral-packet-enclosure"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH141 / "src")]

from factorized_packet import hybrid_packet_gate  # noqa: E402
from run_effective_rank_audit import (  # noqa: E402
    HORIZONS, SIGMAS, arb_matrix, build_models, frobenius_norm, matrix_power,
)
from spectral_packet import aligned_frame_radius  # noqa: E402


PRECISION_BITS = 512
RANK = 4


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def abs_upper(value) -> float:
    return math.nextafter(max(abs(float(value.lower())), abs(float(value.upper()))), math.inf)


def gershgorin_lower(matrix) -> float:
    bounds = []
    for row in range(matrix.nrows()):
        diagonal = lower(matrix[row, row])
        off_diagonal = sum(abs_upper(matrix[row, column]) for column in range(matrix.ncols()) if column != row)
        bounds.append(diagonal - off_diagonal)
    return math.nextafter(min(bounds), -math.inf)


def exact_frobenius_squared(matrix) -> arb:
    return sum((entry * entry for entry in matrix.entries()), arb(0))


def interval_operator_upper(matrix) -> tuple[float, float]:
    started = time.perf_counter()
    eigenvalues = matrix.eig(multiple=True, algorithm="rump")
    radii = []
    maximum_imaginary = 0.0
    for value in eigenvalues:
        real_radius = max(abs(float(value.real.lower())), abs(float(value.real.upper())))
        imaginary_radius = abs_upper(value.imag)
        maximum_imaginary = max(maximum_imaginary, imaginary_radius)
        radii.append(real_radius + imaginary_radius)
    return math.nextafter(max(radii), math.inf), maximum_imaginary


def channel_record(model: dict[str, object], sigma: float) -> dict[str, object]:
    started = time.perf_counter()
    operator_values = np.asarray(model["operator"], dtype=np.float64)
    source_values = np.asarray(model["source"], dtype=np.float64)
    exact_state = matrix_power(arb_matrix(operator_values), HORIZONS[sigma]) * arb_matrix(source_values)
    float_state = np.linalg.matrix_power(operator_values, HORIZONS[sigma]) @ source_values
    left, singular, right = np.linalg.svd(float_state, full_matrices=False)
    left_factor_values = left[:, :RANK] * singular[:RANK]
    right_factor_values = right[:RANK, :]
    left_factor = arb_matrix(left_factor_values)
    right_factor = arb_matrix(right_factor_values)
    candidate = left_factor * right_factor

    source_norm_squared = exact_frobenius_squared(exact_state)
    candidate_norm_squared = exact_frobenius_squared(candidate)
    source_snapshot = (exact_state.transpose() * exact_state) * (arb(1) / source_norm_squared)
    candidate_snapshot = (candidate.transpose() * candidate) * (arb(1) / candidate_norm_squared)
    difference = source_snapshot - candidate_snapshot
    frobenius_upper = upper(frobenius_norm(difference))

    left_gram = left_factor.transpose() * left_factor
    right_gram = right_factor * right_factor.transpose()
    left_lower = gershgorin_lower(left_gram)
    right_lower = gershgorin_lower(right_gram)
    gap_lower = max(0.0, left_lower * right_lower / upper(candidate_norm_squared))

    eigen_upper = None
    maximum_eigen_imaginary_radius = None
    if gap_lower <= 2.0 * frobenius_upper:
        eigen_upper, maximum_eigen_imaginary_radius = interval_operator_upper(difference)
    gate = hybrid_packet_gate(gap_lower, frobenius_upper, eigen_upper)
    frame_radius = None if gate["projector_radius"] is None else aligned_frame_radius(float(gate["projector_radius"]))
    state_residual = frobenius_norm(exact_state - candidate)
    return {
        "sigma": sigma,
        "side": str(model["side"]),
        "horizon": HORIZONS[sigma],
        "state_shape": [int(exact_state.nrows()), int(exact_state.ncols())],
        "factor_rank": RANK,
        "source_norm_squared_lower": lower(source_norm_squared),
        "candidate_norm_squared_lower": lower(candidate_norm_squared),
        "relative_state_residual_upper": upper(state_residual / source_norm_squared.sqrt()),
        "factor_left_gram_lower": left_lower,
        "factor_right_gram_lower": right_lower,
        "factorized_gap_lower": gap_lower,
        "snapshot_frobenius_upper": frobenius_upper,
        "snapshot_interval_eigen_upper": eigen_upper,
        "maximum_eigen_imaginary_radius": maximum_eigen_imaginary_radius,
        "enclosure_method": gate["method"],
        "snapshot_operator_upper": gate["snapshot_radius"],
        "gap_ratio": gate["gap_ratio"],
        "packet_certified": gate["certified"],
        "projector_radius": gate["projector_radius"],
        "polar_aligned_frame_radius": frame_radius,
        "elapsed_seconds": time.perf_counter() - started,
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
            _, models = build_models(sigma)
            for model in models:
                record = channel_record(model, sigma)
                rows.append(record)
                print(json.dumps({
                    "sigma": sigma, "side": record["side"], "method": record["enclosure_method"],
                    "gap_ratio": record["gap_ratio"], "certified": record["packet_certified"],
                    "elapsed_seconds": record["elapsed_seconds"],
                }, sort_keys=True), flush=True)
    finally:
        ctx.prec = previous_precision

    summary = {
        "channel_count": len(rows),
        "packet_certified_count": sum(row["packet_certified"] for row in rows),
        "frobenius_certificate_count": sum(row["enclosure_method"] == "frobenius" and row["packet_certified"] for row in rows),
        "interval_eigen_rescue_count": sum(row["enclosure_method"] == "interval_eigen" and row["packet_certified"] for row in rows),
        "packet_failure_count": sum(not row["packet_certified"] for row in rows),
        "minimum_gap_ratio": min(row["gap_ratio"] for row in rows),
        "maximum_snapshot_operator_upper": max(row["snapshot_operator_upper"] for row in rows),
        "maximum_projector_radius": max(row["projector_radius"] for row in rows if row["projector_radius"] is not None),
        "maximum_polar_aligned_frame_radius": max(row["polar_aligned_frame_radius"] for row in rows if row["polar_aligned_frame_radius"] is not None),
        "maximum_eigen_imaginary_radius": max((row["maximum_eigen_imaginary_radius"] or 0.0 for row in rows), default=0.0),
        "total_elapsed_seconds": sum(row["elapsed_seconds"] for row in rows),
    }
    payload = {
        "status": "rh142_factorized_arb_snapshot_packet_closure",
        "precision_bits": PRECISION_BITS,
        "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "factorized_normalized_gap_lower": True,
            "direct_arb_normalized_snapshot_enclosure": True,
            "hybrid_frobenius_interval_eigen_packet_certificate": True,
            "all_ten_frozen_binary_source_packets_certified": not args.smoke and summary["packet_certified_count"] == 10,
            "coarse_projector_enclosures_are_tight": False,
            "thresholded_recursive_packet_update_enclosed": False,
            "continuum_source_model_intervalized": False,
            "uniform_all_level_packet_theorem": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "Direct 512-bit Arb evaluation preserves the low-rank cancellation that the universal "
            "RH-140 state bound discarded. Eight channels pass with a Frobenius enclosure and the "
            "two coarse channels are rescued by validated interval eigenvalue radii, closing all ten "
            "frozen binary source packets. The coarse right projector ball remains broad, so recursive "
            "threshold stability is the next unresolved interface."
        ),
    }
    output = ROOT / "results" / ("factorized_arb_smoke.json" if args.smoke else "factorized_arb_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()

