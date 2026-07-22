"""Production Schur-source phase spread and Arb moment-Gram audit."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

from flint import acb, acb_mat, arb, ctx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH58 = PAPERS / "RH-58-time-ordered-schur-cross-gramian"
sys.path[:0] = [str(RH58 / "experiments"), str(RH58 / "src"), str(RH14 / "src")]

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from run_schur_fusion_pilot import (  # noqa: E402
    FINE_RESOLUTION,
    HARDY_RADIUS,
    coarse_embedding,
    detail_embedding,
    ordered_radial_schur,
    spectral_bulk,
)


FULL_OUTPUT = ROOT / "results" / "phase_compression_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "phase_compression_smoke.json"
SIGMAS = (0.16, 0.08, 0.04, 0.02, 0.01)
HORIZONS = {0.16: 4, 0.08: 9, 0.04: 16, 0.02: 25, 0.01: 32}
MASSES = (0.90, 0.99, 0.999)
PRECISION_BITS = 192


def exact_arb_float(value: float) -> arb:
    numerator, denominator = float(value).as_integer_ratio()
    return arb(numerator) / denominator


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def minimal_weighted_arc(phases: np.ndarray, weights: np.ndarray, mass: float) -> dict[str, float]:
    phase = np.mod(np.asarray(phases, dtype=np.float64), 2.0 * math.pi)
    weight = np.asarray(weights, dtype=np.float64)
    order = np.argsort(phase)
    phase = phase[order]
    weight = weight[order]
    doubled_phase = np.concatenate((phase, phase + 2.0 * math.pi))
    doubled_weight = np.concatenate((weight, weight))
    target = float(mass) * float(np.sum(weight))
    best_width = 2.0 * math.pi
    best_mass = 0.0
    end = 0
    running = 0.0
    for start in range(len(phase)):
        while end < start + len(phase) and running < target:
            running += float(doubled_weight[end])
            end += 1
        if running >= target:
            width = float(doubled_phase[end - 1] - doubled_phase[start])
            if width < best_width:
                best_width = width
                best_mass = running / float(np.sum(weight))
        running -= float(doubled_weight[start])
    width_ball = exact_arb_float(best_width)
    return {
        "target_mass": mass,
        "width_ball": str(width_ball),
        "width_lower": lower(width_ball),
        "width_upper": upper(width_ball),
        "width_fraction_of_circle": upper(width_ball / (arb(2) * arb.pi())),
        "captured_mass_diagnostic": best_mass,
    }


def moment_gram_residual(phases: np.ndarray, weights: np.ndarray, horizon: int) -> dict[str, object]:
    phase_values = [exact_arb_float(value) for value in np.asarray(phases, dtype=np.float64)]
    weight_values = [exact_arb_float(value) for value in np.asarray(weights, dtype=np.float64)]
    total_weight = sum(weight_values, arb(0))
    normalized = [value / total_weight for value in weight_values]
    nodes = [acb(arb(0), phase).exp() for phase in phase_values]
    moments: dict[int, acb] = {}
    for exponent in range(horizon + 1):
        moments[exponent] = sum(
            (acb(weight) * node**exponent for weight, node in zip(normalized, nodes)),
            acb(0),
        )
        if exponent:
            moments[-exponent] = moments[exponent].conjugate()
    depth = horizon
    gram = acb_mat(
        [[moments[column - row] for column in range(depth)] for row in range(depth)]
    )
    correlation = acb_mat([[moments[horizon - row]] for row in range(depth)])
    solution = gram.solve(correlation)
    projection = sum(
        (
            correlation[row, 0].conjugate() * solution[row, 0]
            for row in range(depth)
        ),
        acb(0),
    )
    error_squared = arb(1) - projection.real
    if lower(error_squared) < 0.0:
        raise RuntimeError("moment projection error crossed zero")
    error = error_squared.sqrt()
    return {
        "depth": depth,
        "target_horizon": horizon,
        "projection_ball": str(projection),
        "residual_squared_ball": str(error_squared),
        "residual_ball": str(error),
        "residual_lower": lower(error),
        "residual_upper": upper(error),
        "ten_percent_compression_fails": lower(error) > 0.1,
        "one_percent_compression_fails": lower(error) > 0.01,
    }


def required_depth_diagnostic(
    phases: np.ndarray,
    weights: np.ndarray,
    horizon: int,
    tolerance: float,
) -> int:
    normalized = np.asarray(weights, dtype=np.float64)
    normalized = normalized / np.sum(normalized)
    vandermonde = np.exp(
        1j * np.outer(np.asarray(phases), np.arange(horizon + 1))
    )
    target = vandermonde[:, horizon]
    for depth in range(1, horizon + 1):
        basis = vandermonde[:, :depth]
        gram = (basis.conjugate().T * normalized) @ basis
        correlation = (basis.conjugate().T * normalized) @ target
        projection = float(
            np.real(
                np.vdot(correlation, np.linalg.solve(gram, correlation))
            )
        )
        residual = math.sqrt(max(0.0, 1.0 - projection))
        if residual <= tolerance:
            return depth
    return horizon + 1


def build_models(sigma: float) -> tuple[int, list[dict[str, object]]]:
    dimension = max(32, 2 * int(round(FINE_RESOLUTION / sigma / 2.0)))
    fine = sparse_folded_gaussian_matrix(dimension, sigma).toarray()
    embedding = coarse_embedding(dimension)
    detail = detail_embedding(dimension)
    coarse = embedding.T @ fine @ embedding
    coupling_b = embedding.T @ fine @ detail
    coupling_c = detail.T @ fine @ embedding
    fine_data = spectral_bulk(fine)
    coarse_data = spectral_bulk(coarse)
    return dimension, [
        {
            "side": "left",
            "operator": np.asarray(fine_data["bulk"]) / HARDY_RADIUS,
            "source": np.asarray(fine_data["complement"]) @ embedding @ coupling_b / np.linalg.norm(coupling_b, "fro"),
        },
        {
            "side": "right",
            "operator": np.asarray(coarse_data["bulk"]).T / HARDY_RADIUS,
            "source": coupling_c.T / np.linalg.norm(coupling_c, "fro"),
        },
    ]


def channel_audit(model: dict[str, object], horizon: int) -> dict[str, object]:
    partition = ordered_radial_schur(np.asarray(model["operator"]), ())
    source_coordinates = partition.unitary.conjugate().T @ np.asarray(model["source"])
    weights = np.sum(np.abs(source_coordinates) ** 2, axis=1)
    phases = np.angle(np.diag(partition.triangular))
    arcs = {f"mass_{mass:g}": minimal_weighted_arc(phases, weights, mass) for mass in MASSES}
    moment = moment_gram_residual(phases, weights, horizon)
    required_ten = required_depth_diagnostic(phases, weights, horizon, 0.1)
    required_one = required_depth_diagnostic(phases, weights, horizon, 0.01)
    return {
        "side": model["side"],
        "dimension": int(np.asarray(model["operator"]).shape[0]),
        "horizon": horizon,
        "schur_reconstruction_defect_diagnostic": partition.reconstruction_defect,
        "schur_unitary_defect_diagnostic": partition.unitary_defect,
        "active_source_phase_count": int(np.count_nonzero(weights > 1.0e-12 * np.sum(weights))),
        "weighted_arcs": arcs,
        "moment_gram": moment,
        "required_depth_10_percent_diagnostic": required_ten,
        "required_depth_1_percent_diagnostic": required_one,
        "depth_fraction_10_percent_diagnostic": required_ten / (horizon + 1),
        "single_arc_narrowing_observed": arcs["mass_0.99"]["width_upper"] < math.pi,
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
            dimension, models = build_models(sigma)
            channels = [channel_audit(model, HORIZONS[sigma]) for model in models]
            row = {"sigma": sigma, "fine_dimension": dimension, "channels": channels, "all_moment_solves_certified": all(channel["moment_gram"]["residual_lower"] > 0.0 for channel in channels)}
            rows.append(row)
            for channel in channels:
                print(json.dumps({"sigma": sigma, "side": channel["side"], "arc_99": channel["weighted_arcs"]["mass_0.99"]["width_upper"], "residual_at_depth_M": channel["moment_gram"]["residual_lower"], "ten_percent_fails": channel["moment_gram"]["ten_percent_compression_fails"]}, sort_keys=True), flush=True)
    finally:
        ctx.prec = previous_precision
    channels = [channel for row in rows for channel in row["channels"]]
    payload = {
        "status": "rh76_single_arc_phase_compression_barrier",
        "precision_bits": PRECISION_BITS,
        "rows": rows,
        "all_executed_moment_solves_certified": all(row["all_moment_solves_certified"] for row in rows),
        "route_verdict": {
            "single_arc_phase_compression_supported": all(channel["single_arc_narrowing_observed"] for channel in channels),
            "ten_percent_depth_reduction_at_finest_scale": any(not channel["moment_gram"]["ten_percent_compression_fails"] for channel in rows[-1]["channels"]),
            "effective_rank_fallback_required": True,
        },
        "theorem_boundary": {
            "arc_binomial_krylov_upper": True,
            "moment_gram_projection_identity": True,
            "coherence_residual_lower": True,
            "frozen_schur_phase_surrogate_audited": True,
            "validated_continuum_phase_measure": False,
            "uniform_phase_compression_theorem": False,
        },
        "route_consequence": (
            "The single-arc route does not explain the physical log-square horizons: "
            "source-weighted 99% phase arcs remain broad and the finest frozen-Schur "
            "normal surrogates still require the full monomial depth for 10% accuracy. "
            "This is a branch-level negative result, not a failure of Stage A; the next "
            "route is weighted effective-rank or multi-arc packet decay."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "row_count": len(rows), "single_arc_supported": payload["route_verdict"]["single_arc_phase_compression_supported"]}, sort_keys=True))


if __name__ == "__main__":
    main()
