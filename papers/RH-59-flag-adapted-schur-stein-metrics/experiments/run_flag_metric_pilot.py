"""Five-scale packetwise flag-metric Stein audit for RH-59."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import solve_discrete_lyapunov
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH58 = PAPERS / "RH-58-time-ordered-schur-cross-gramian"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH58 / "src"))
sys.path.insert(0, str(RH58 / "experiments"))
sys.path.insert(0, str(RH14 / "src"))

from flag_stein import (  # noqa: E402
    build_flag_metric,
    comparison_contraction_log_upper,
    evaluate_packet_certificate,
    packet_log_upper_objective,
    scaled_normalized_prefix,
)
from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from run_schur_fusion_pilot import (  # noqa: E402
    BLOCK_HORIZON,
    FINE_RESOLUTION,
    HARDY_RADIUS,
    RADIAL_CUTS,
    RADIAL_NAMES,
    coarse_embedding,
    detail_embedding,
    spectral_bulk,
)
from schur_fusion import (  # noqa: E402
    gram_budget,
    ordered_radial_schur,
    schur_source_gram,
)


OUTPUT = ROOT / "results" / "flag_metric_pilot.json"
FULL_SIGMAS = (0.16, 0.08, 0.04, 0.02, 0.01)
SMOKE_SIGMAS = (0.16, 0.08)
MINIMUM_DISSIPATION_MARGIN = 1.0e-8
MAXIMUM_DIRECT_ITERATIONS = 260


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fit_power(rows: list[dict[str, object]], path: tuple[str, ...]) -> dict[str, float]:
    def extract(row: dict[str, object]) -> float:
        value: object = row
        for key in path:
            value = value[key]  # type: ignore[index]
        return float(value)

    x = np.log(np.asarray([float(row["sigma"]) for row in rows]))
    y = np.log(np.asarray([extract(row) for row in rows]))
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return {
        "sigma_power": float(slope),
        "growth_exponent": float(max(0.0, -slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "levels": len(rows),
    }


def _infeasible_penalty(
    family, packet_index: int, log_scales: np.ndarray
) -> float:
    normalized = scaled_normalized_prefix(family, packet_index, log_scales)
    contraction = float(np.linalg.norm(normalized, 2))
    overflow = float(
        np.sum(np.maximum(np.abs(log_scales[:-1]) - 14.0, 0.0) ** 2)
    )
    return 20.0 + 200.0 * max(0.0, contraction - 1.0) + overflow


def comparison_seed(
    source: np.ndarray,
    observation: np.ndarray,
    family,
    packet_index: int,
) -> tuple[np.ndarray, dict[str, object]]:
    if packet_index == 0:
        return np.zeros(1), {
            "success": True,
            "evaluations": 1,
            "message": "single diagonal block",
        }

    initial = -2.4 * (packet_index - np.arange(packet_index, dtype=float))

    def objective(values: np.ndarray) -> float:
        log_scales = np.concatenate((np.asarray(values), np.zeros(1)))
        try:
            return comparison_contraction_log_upper(
                source,
                observation,
                family,
                packet_index,
                log_scales,
            )
        except ValueError:
            return _infeasible_penalty(family, packet_index, log_scales)

    result = minimize(
        objective,
        initial,
        method="Powell",
        bounds=[(-14.0, 2.0)] * packet_index,
        options={"maxiter": 300, "xtol": 1.0e-7, "ftol": 1.0e-9},
    )
    candidates = (initial, np.asarray(result.x))
    best = min(candidates, key=objective)
    return np.concatenate((best, np.zeros(1))), {
        "success": bool(result.success),
        "evaluations": int(result.nfev),
        "message": str(result.message),
    }


def optimize_packet(
    source: np.ndarray,
    observation: np.ndarray,
    family,
    packet_index: int,
) -> tuple[np.ndarray, dict[str, object]]:
    seed, seed_record = comparison_seed(
        source, observation, family, packet_index
    )
    if packet_index == 0:
        return seed, {
            "seed": seed_record,
            "direct_success": True,
            "direct_evaluations": 1,
            "direct_message": "single diagonal block",
            "improved_from_seed": False,
        }

    def objective(values: np.ndarray) -> float:
        log_scales = np.concatenate((np.asarray(values), np.zeros(1)))
        if np.max(np.abs(log_scales[:-1]), initial=0.0) > 16.0:
            return _infeasible_penalty(family, packet_index, log_scales)
        try:
            return packet_log_upper_objective(
                source,
                observation,
                family,
                packet_index,
                log_scales,
            )
        except ValueError:
            return _infeasible_penalty(family, packet_index, log_scales)

    initial = seed[:-1]
    result = minimize(
        objective,
        initial,
        method="Nelder-Mead",
        options={
            "maxiter": MAXIMUM_DIRECT_ITERATIONS,
            "xatol": 2.0e-5,
            "fatol": 1.0e-8,
            "adaptive": True,
        },
    )
    candidates = (initial, np.asarray(result.x))
    best = min(candidates, key=objective)
    return np.concatenate((best, np.zeros(1))), {
        "seed": seed_record,
        "direct_success": bool(result.success),
        "direct_evaluations": int(result.nfev),
        "direct_message": str(result.message),
        "improved_from_seed": bool(objective(best) < objective(initial) - 1.0e-10),
    }


def channel_audit(
    operator: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
    inherited: dict[str, object],
) -> dict[str, object]:
    observability = solve_discrete_lyapunov(
        operator.conjugate().T,
        observation.conjugate().T @ observation,
    )
    observability = 0.5 * (
        observability + observability.conjugate().T
    )
    partition = ordered_radial_schur(
        operator,
        RADIAL_CUTS,
        physical_scale=HARDY_RADIUS,
        names=RADIAL_NAMES,
    )
    transformed_source = partition.unitary.conjugate().T @ source
    transformed_observation = observation @ partition.unitary
    source_budget = gram_budget(
        schur_source_gram(observability, source, partition),
        tolerance=2.0e-10,
    )
    family = build_flag_metric(partition.triangular, partition.sizes)

    packets = []
    for packet_index, (name, block_slice) in enumerate(
        zip(partition.names, partition.slices)
    ):
        log_scales, optimizer = optimize_packet(
            transformed_source,
            transformed_observation,
            family,
            packet_index,
        )
        certificate = evaluate_packet_certificate(
            transformed_source,
            transformed_observation,
            family,
            packet_index,
            log_scales,
            positivity_tolerance=MINIMUM_DISSIPATION_MARGIN,
        )
        try:
            comparison_upper = math.exp(
                comparison_contraction_log_upper(
                    transformed_source,
                    transformed_observation,
                    family,
                    packet_index,
                    log_scales,
                )
            )
        except ValueError:
            comparison_upper = None
        exact_packet = float(source_budget.block_energies[packet_index])
        packets.append(
            {
                "name": name,
                "dimension": partition.sizes[packet_index],
                "minimum_physical_modulus": float(
                    np.min(partition.physical_moduli[block_slice])
                ),
                "maximum_physical_modulus": float(
                    np.max(partition.physical_moduli[block_slice])
                ),
                "exact_packet_energy": exact_packet,
                "metric_energy_upper": certificate.energy_upper,
                "metric_upper_over_exact": certificate.energy_upper
                / max(exact_packet, 1.0e-300),
                "comparison_contraction_upper": comparison_upper,
                "exact_contraction_upper": (
                    certificate.contraction_energy_upper
                ),
                "log_scales": list(certificate.log_scales),
                "kappa": certificate.kappa,
                "source_metric_squared": certificate.source_metric_squared,
                "normalized_contraction": (
                    certificate.normalized_contraction
                ),
                "comparison_contraction": (
                    certificate.comparison_contraction
                ),
                "minimum_dissipation_eigenvalue": (
                    certificate.minimum_dissipation_eigenvalue
                ),
                "minimum_supersolution_eigenvalue": (
                    certificate.minimum_supersolution_eigenvalue
                ),
                "optimizer": optimizer,
            }
        )

    exact_squared = float(
        np.trace(source.conjugate().T @ observability @ source).real
    )
    packet_uppers = np.asarray(
        [float(packet["metric_energy_upper"]) for packet in packets]
    )
    absolute_upper = float(np.sum(packet_uppers))
    coherence_assisted = math.sqrt(
        source_budget.coherence_constant * float(np.sum(packet_uppers**2))
    )
    observability_residual = (
        observability
        - operator.conjugate().T @ observability @ operator
        - observation.conjugate().T @ observation
    )
    inherited_exact = float(inherited["exact_hardy_energy"])
    return {
        "exact_hardy_energy": math.sqrt(max(0.0, exact_squared)),
        "rh58_exact_relative_defect": abs(
            math.sqrt(max(0.0, exact_squared)) - inherited_exact
        )
        / max(inherited_exact, 1.0e-300),
        "exact_packet_square_sum": source_budget.square_sum_energy,
        "exact_packet_absolute_sum": source_budget.absolute_packet_upper,
        "exact_packet_coherence": source_budget.coherence_constant,
        "minimum_packet_gram_eigenvalue": (
            source_budget.minimum_gram_eigenvalue
        ),
        "metric_packet_square_sum": float(np.linalg.norm(packet_uppers)),
        "metric_absolute_upper": absolute_upper,
        "empirical_coherence_assisted_metric_upper": coherence_assisted,
        "metric_absolute_upper_over_exact": absolute_upper
        / max(math.sqrt(max(0.0, exact_squared)), 1.0e-300),
        "maximum_packet_upper_over_exact": max(
            float(packet["metric_upper_over_exact"]) for packet in packets
        ),
        "packets": packets,
        "local_metrics": [
            {
                "name": name,
                "dimension": size,
                "contraction": block.contraction,
                "condition_number": block.condition_number,
                "minimum_eigenvalue": block.minimum_eigenvalue,
                "maximum_eigenvalue": block.maximum_eigenvalue,
                "residual_relative": block.residual_relative,
            }
            for name, size, block in zip(
                partition.names, partition.sizes, family.blocks
            )
        ],
        "maximum_local_metric_residual": max(
            block.residual_relative for block in family.blocks
        ),
        "maximum_local_metric_condition_number": max(
            block.condition_number for block in family.blocks
        ),
        "observability_stein_residual_relative": float(
            np.linalg.norm(observability_residual, 2)
            / max(1.0, np.linalg.norm(observability, 2))
        ),
        "schur_reconstruction_defect": partition.reconstruction_defect,
        "schur_unitary_defect": partition.unitary_defect,
        "inherited_rh58": {
            "scalar_path_upper": inherited["scalar_path_majorant"][
                "energy_upper"
            ],
            "source_packet_coherence_upper": inherited[
                "source_packet_gram"
            ]["coherence_upper"],
            "state_block_coherence_upper": inherited["state_block_gram"][
                "coherence_upper"
            ],
        },
    }


def run_sigma(
    sigma: float, inherited_row: dict[str, object]
) -> dict[str, object]:
    started = time.perf_counter()
    fine_dimension = max(32, 2 * int(round(FINE_RESOLUTION / sigma / 2.0)))
    fine = sparse_folded_gaussian_matrix(fine_dimension, sigma).toarray()
    u = coarse_embedding(fine_dimension)
    w = detail_embedding(fine_dimension)
    fine_u = fine @ u
    coarse = u.T @ fine_u
    coupling_b = u.T @ fine @ w
    coupling_c = w.T @ fine_u
    fine_data = spectral_bulk(fine)
    coarse_data = spectral_bulk(coarse)
    fine_operator = np.asarray(fine_data["bulk"]) / HARDY_RADIUS
    coarse_operator = (
        np.asarray(coarse_data["bulk"]).conjugate().T / HARDY_RADIUS
    )
    left_source = (
        np.asarray(fine_data["complement"])
        @ u
        @ coupling_b
        / np.linalg.norm(coupling_b, "fro")
    )
    right_source = coupling_c.conjugate().T / np.linalg.norm(
        coupling_c, "fro"
    )
    left_observation = u.T
    right_observation = np.asarray(coarse_data["complement"]).conjugate().T
    return {
        "sigma": sigma,
        "fine_dimension": fine_dimension,
        "coarse_dimension": fine_dimension // 2,
        "fine_dimension_times_sigma": fine_dimension * sigma,
        "left": channel_audit(
            fine_operator,
            left_source,
            left_observation,
            inherited_row["left"],
        ),
        "right": channel_audit(
            coarse_operator,
            right_source,
            right_observation,
            inherited_row["right"],
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    inherited = json.loads(
        (RH58 / "results" / "schur_fusion_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    inherited_rows = {
        float(row["sigma"]): row for row in inherited["rows"]
    }
    sigmas = SMOKE_SIGMAS if args.smoke else FULL_SIGMAS
    rows = []
    for sigma in sigmas:
        row = run_sigma(float(sigma), inherited_rows[float(sigma)])
        rows.append(row)
        print(
            json.dumps(
                {
                    "sigma": row["sigma"],
                    "dimension": row["fine_dimension"],
                    "left_exact": row["left"]["exact_hardy_energy"],
                    "left_metric_upper": row["left"][
                        "metric_absolute_upper"
                    ],
                    "left_outer_upper": row["left"]["packets"][-1][
                        "metric_energy_upper"
                    ],
                    "right_exact": row["right"]["exact_hardy_energy"],
                    "right_metric_upper": row["right"][
                        "metric_absolute_upper"
                    ],
                    "right_outer_upper": row["right"]["packets"][-1][
                        "metric_energy_upper"
                    ],
                    "elapsed_seconds": row["elapsed_seconds"],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    payload = {
        "status": "binary64_packetwise_flag_metric_stein_audit",
        "evidence_level": (
            "deterministic all-column dense binary64 Schur, local Lyapunov, "
            "and exact-dissipation packet audit; not interval validated"
        ),
        "fine_resolution": FINE_RESOLUTION,
        "hardy_radius": HARDY_RADIUS,
        "radial_cuts": list(RADIAL_CUTS),
        "radial_names": list(RADIAL_NAMES),
        "inherited_block_horizon": BLOCK_HORIZON,
        "minimum_dissipation_margin": MINIMUM_DISSIPATION_MARGIN,
        "maximum_direct_iterations": MAXIMUM_DIRECT_ITERATIONS,
        "sources": {
            "folded_gaussian": {
                "path": str(
                    (
                        RH14
                        / "src"
                        / "parity_boundary"
                        / "operators.py"
                    ).relative_to(REPOSITORY)
                ),
                "sha256": sha256_file(
                    RH14 / "src" / "parity_boundary" / "operators.py"
                ),
            },
            "rh58_pilot": {
                "path": str(
                    (
                        RH58 / "results" / "schur_fusion_pilot.json"
                    ).relative_to(REPOSITORY)
                ),
                "sha256": sha256_file(
                    RH58 / "results" / "schur_fusion_pilot.json"
                ),
            },
            "rh58_algebra": {
                "path": str(
                    (
                        RH58 / "src" / "schur_fusion" / "algebra.py"
                    ).relative_to(REPOSITORY)
                ),
                "sha256": sha256_file(
                    RH58 / "src" / "schur_fusion" / "algebra.py"
                ),
            },
        },
        "rows": rows,
        "fits": {
            "left_exact": fit_power(rows, ("left", "exact_hardy_energy")),
            "right_exact": fit_power(rows, ("right", "exact_hardy_energy")),
            "left_metric_absolute_upper": fit_power(
                rows, ("left", "metric_absolute_upper")
            ),
            "right_metric_absolute_upper": fit_power(
                rows, ("right", "metric_absolute_upper")
            ),
            "left_outer_packet_upper": fit_power_rows_outer(rows, "left"),
            "right_outer_packet_upper": fit_power_rows_outer(rows, "right"),
        },
        "limitations": [
            "The production Schur forms, Lyapunov solves, and optimized weights are binary64 diagnostics, not interval enclosures.",
            "Flag-metric existence is finite-dimensional; no noise-uniform control of the hierarchical weights is proved.",
            "The empirical coherence-assisted upper uses the measured packet Gram coherence and is not a standalone analytic certificate.",
            "The dense audit uses N*sigma=5.12, below the RH-50 production resolution N*sigma=20.48.",
            "Five levels do not prove a polylogarithmic packet budget; Stage A1 and Stage A4 remain open.",
        ],
    }
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "flag_metric_pilot_smoke.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output.relative_to(ROOT))}, sort_keys=True))


def fit_power_rows_outer(
    rows: list[dict[str, object]], side: str
) -> dict[str, float]:
    x = np.log(np.asarray([float(row["sigma"]) for row in rows]))
    y = np.log(
        np.asarray(
            [
                float(row[side]["packets"][-1]["metric_energy_upper"])
                for row in rows
            ]
        )
    )
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return {
        "sigma_power": float(slope),
        "growth_exponent": float(max(0.0, -slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "levels": len(rows),
    }


if __name__ == "__main__":
    main()
