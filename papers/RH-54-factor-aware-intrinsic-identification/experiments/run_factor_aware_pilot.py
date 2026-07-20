"""Dense sparse/full intrinsic-factor transfer audit for RH-54."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import eig, solve_discrete_lyapunov


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"
RH48 = PAPERS / "RH-48-intrinsic-riesz-identification"
RH49 = PAPERS / "RH-49-directional-reduced-resolvent"
RH50 = PAPERS / "RH-50-two-pole-hilbert-schmidt-hardy"
RH52 = PAPERS / "RH-52-intrinsic-peripheral-residue-transfer"
RH53 = PAPERS / "RH-53-deterministic-hardy-tail-cutoff"
for path in (ROOT / "src", RH14 / "src", RH53 / "src"):
    sys.path.insert(0, str(path))

from hardy_tail import (  # noqa: E402
    adaptive_cutoff_multiple,
    cutoff_bound,
    deterministic_hardy_certificate,
    deterministic_main_sum,
)
from intrinsic_transfer import (  # noqa: E402
    factor_aware_left_defects,
    factor_aware_right_defects,
    finite_directional_perturbation_bound,
    growing_horizon_energy_upper,
    semigroup_power_defect_upper,
)
from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402


OUTPUT = ROOT / "results" / "factor_aware_transfer_pilot.json"
FULL_SIGMAS = (0.16, 0.08, 0.04, 0.02, 0.01)
SMOKE_SIGMAS = (0.16, 0.08)
FINE_RESOLUTION = 5.12
HARDY_RADIUS = 0.85
HORIZONS = (4, 8, 16, 24, 32)
CUTOFF_MULTIPLES = (5.0, 6.0, 8.0)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def coarse_embedding(dimension: int) -> np.ndarray:
    coarse = dimension // 2
    result = np.zeros((dimension, coarse), dtype=np.float64)
    indices = np.arange(coarse)
    result[2 * indices, indices] = 1.0 / math.sqrt(2.0)
    result[2 * indices + 1, indices] = 1.0 / math.sqrt(2.0)
    return result


def detail_embedding(dimension: int) -> np.ndarray:
    coarse = dimension // 2
    result = np.zeros((dimension, coarse), dtype=np.float64)
    indices = np.arange(coarse)
    result[2 * indices, indices] = 1.0 / math.sqrt(2.0)
    result[2 * indices + 1, indices] = -1.0 / math.sqrt(2.0)
    return result


def full_folded_gaussian_matrix(
    dimension: int,
    sigma: float,
    *,
    u: float = 1.5436890126920764,
) -> np.ndarray:
    nodes = (np.arange(dimension, dtype=np.float64) + 0.5) / dimension
    means = 1.0 - u * nodes * nodes
    positive = -0.5 * ((nodes[None, :] - means[:, None]) / sigma) ** 2
    negative = -0.5 * ((-nodes[None, :] - means[:, None]) / sigma) ** 2
    logs = np.logaddexp(positive, negative)
    logs -= np.max(logs, axis=1, keepdims=True)
    weights = np.exp(logs)
    return weights / np.sum(weights, axis=1, keepdims=True)


def real_if_small(value: np.ndarray, tolerance: float = 2.0e-9) -> np.ndarray:
    array = np.asarray(value)
    if np.max(np.abs(array.imag), initial=0.0) <= tolerance:
        return array.real.astype(np.float64)
    return array.astype(np.complex128)


def spectral_factors(matrix: np.ndarray) -> dict[str, np.ndarray | float | complex]:
    values, left_raw, right_raw = eig(
        matrix, left=True, right=True, check_finite=False
    )
    perron_index = int(np.argmin(np.abs(values - 1.0)))
    negative = np.flatnonzero(
        (np.abs(values.imag) < 2.0e-8) & (values.real < -1.0e-8)
    )
    if not negative.size:
        raise RuntimeError("no negative real parity eigenvalue was resolved")
    parity_index = int(negative[np.argmin(values[negative].real)])
    selected = np.asarray(
        (values[perron_index], values[parity_index]), dtype=np.complex128
    )
    right = np.column_stack(
        (
            np.ones(matrix.shape[0], dtype=np.complex128),
            right_raw[:, parity_index],
        )
    )
    left = np.column_stack(
        (left_raw[:, perron_index], left_raw[:, parity_index])
    )
    left = left @ np.linalg.inv(left.conjugate().T @ right).conjugate().T
    projection = right @ left.conjugate().T
    weighted = right @ np.diag(selected) @ left.conjugate().T
    bulk = matrix - weighted
    complement = np.eye(matrix.shape[0]) - projection
    excluded = np.ones(values.size, dtype=bool)
    excluded[[perron_index, parity_index]] = False
    return {
        "eigenvalues": selected,
        "projection": real_if_small(projection),
        "weighted": real_if_small(weighted),
        "bulk": real_if_small(bulk),
        "complement": real_if_small(complement),
        "bulk_radius_observed": float(
            np.max(np.abs(values[excluded]), initial=0.0)
        ),
    }


def spectral_norm(value: np.ndarray) -> float:
    return float(np.linalg.norm(value, 2))


def hs_norm(value: np.ndarray) -> float:
    return float(np.linalg.norm(value, "fro"))


def power_ledger(operator: np.ndarray, horizon: int) -> tuple[list[np.ndarray], list[float]]:
    powers = [np.eye(operator.shape[0], dtype=np.complex128)]
    for _ in range(horizon):
        powers.append(operator @ powers[-1])
    return powers, [spectral_norm(value) for value in powers]


def exact_energy(operator: np.ndarray, source: np.ndarray, observation: np.ndarray) -> float:
    gramian = solve_discrete_lyapunov(
        operator, source @ source.conjugate().T
    )
    value = np.trace(observation @ gramian @ observation.conjugate().T).real
    return math.sqrt(max(float(value), 0.0))


def certificate_payload(certificate, exact: float) -> dict[str, float | int]:
    return {
        "horizon": certificate.horizon,
        "finite_energy_squared": certificate.main_energy_squared,
        "block_power_norm": certificate.block_power_norm,
        "contraction_margin": certificate.contraction_margin,
        "simple_tail_upper": certificate.simple_tail_upper,
        "stein_tail_upper": certificate.stein_tail_upper,
        "selected_tail_upper": min(
            certificate.simple_tail_upper, certificate.stein_tail_upper
        ),
        "full_energy_upper": certificate.energy_upper,
        "exact_lyapunov_energy": exact,
    }


def build_model(
    matrix: np.ndarray,
    coarse_isometry: np.ndarray,
    detail_isometry: np.ndarray,
    horizon: int,
) -> dict[str, object]:
    matrix_u = matrix @ coarse_isometry
    matrix_w = matrix @ detail_isometry
    coarse = coarse_isometry.T @ matrix_u
    coupling_b = coarse_isometry.T @ matrix_w
    coupling_c = detail_isometry.T @ matrix_u
    fine_factors = spectral_factors(matrix)
    coarse_factors = spectral_factors(coarse)
    b_norm = hs_norm(coupling_b)
    c_norm = hs_norm(coupling_c)
    left_operator = np.asarray(fine_factors["bulk"]) / HARDY_RADIUS
    left_source = (
        np.asarray(fine_factors["complement"])
        @ coarse_isometry
        @ coupling_b
        / b_norm
    )
    left_observation = coarse_isometry.T
    right_operator = (
        np.asarray(coarse_factors["bulk"]).conjugate().T / HARDY_RADIUS
    )
    right_source = coupling_c.conjugate().T / c_norm
    right_observation = np.asarray(
        coarse_factors["complement"]
    ).conjugate().T
    left_exact = exact_energy(left_operator, left_source, left_observation)
    right_exact = exact_energy(right_operator, right_source, right_observation)
    left_certificate = deterministic_hardy_certificate(
        left_operator, left_source, left_observation, horizon
    )
    right_certificate = deterministic_hardy_certificate(
        right_operator, right_source, right_observation, horizon
    )
    left_powers, left_norms = power_ledger(left_operator, horizon)
    right_powers, right_norms = power_ledger(right_operator, horizon)
    return {
        "matrix": matrix,
        "coarse": coarse,
        "coupling_b": coupling_b,
        "coupling_c": coupling_c,
        "fine_factors": fine_factors,
        "coarse_factors": coarse_factors,
        "left": {
            "operator": left_operator,
            "source": left_source,
            "observation": left_observation,
            "powers": left_powers,
            "power_norms": left_norms,
            "certificate": left_certificate,
            "exact": left_exact,
        },
        "right": {
            "operator": right_operator,
            "source": right_source,
            "observation": right_observation,
            "powers": right_powers,
            "power_norms": right_norms,
            "certificate": right_certificate,
            "exact": right_exact,
        },
    }


def model_payload(model: dict[str, object]) -> dict[str, object]:
    fine = model["fine_factors"]
    coarse = model["coarse_factors"]
    return {
        "coupling_b_hilbert_schmidt": hs_norm(model["coupling_b"]),
        "coupling_c_hilbert_schmidt": hs_norm(model["coupling_c"]),
        "fine_projector_norm": spectral_norm(fine["projection"]),
        "coarse_projector_norm": spectral_norm(coarse["projection"]),
        "fine_weighted_riesz_norm": spectral_norm(fine["weighted"]),
        "coarse_weighted_riesz_norm": spectral_norm(coarse["weighted"]),
        "fine_bulk_radius_observed": fine["bulk_radius_observed"],
        "coarse_bulk_radius_observed": coarse["bulk_radius_observed"],
        "fine_peripheral_eigenvalues": [
            float(np.real(value)) for value in fine["eigenvalues"]
        ],
        "coarse_peripheral_eigenvalues": [
            float(np.real(value)) for value in coarse["eigenvalues"]
        ],
        "left": certificate_payload(
            model["left"]["certificate"], model["left"]["exact"]
        ),
        "right": certificate_payload(
            model["right"]["certificate"], model["right"]["exact"]
        ),
    }


def side_transfer_payload(
    side: str,
    sparse: dict[str, object],
    full: dict[str, object],
    defects,
    horizon: int,
) -> dict[str, object]:
    sparse_side = sparse[side]
    full_side = full[side]
    actual_operator = spectral_norm(
        sparse_side["operator"] - full_side["operator"]
    )
    actual_source = hs_norm(sparse_side["source"] - full_side["source"])
    actual_observation = spectral_norm(
        sparse_side["observation"] - full_side["observation"]
    )
    perturbation = finite_directional_perturbation_bound(
        sparse_side["operator"],
        sparse_side["source"],
        sparse_side["observation"],
        full_side["operator"],
        full_side["source"],
        full_side["observation"],
        horizon,
        operator_defect_upper=defects.operator,
        source_defect_upper=defects.source,
        observation_defect_upper=defects.observation,
        reference_power_norms=sparse_side["power_norms"],
        perturbed_power_norms=full_side["power_norms"],
    )
    d_horizon = semigroup_power_defect_upper(
        sparse_side["power_norms"],
        full_side["power_norms"],
        defects.operator,
        horizon,
    )
    actual_power_defect = spectral_norm(
        sparse_side["powers"][horizon] - full_side["powers"][horizon]
    )
    sparse_certificate = sparse_side["certificate"]
    full_certificate = full_side["certificate"]
    transferred_block_upper = sparse_certificate.block_power_norm + d_horizon
    sparse_finite = deterministic_main_sum(
        sparse_side["operator"],
        sparse_side["source"],
        sparse_side["observation"],
        horizon,
    )
    full_finite = deterministic_main_sum(
        full_side["operator"],
        full_side["source"],
        full_side["observation"],
        horizon,
    )
    actual_energy_squared_difference = abs(
        sparse_side["exact"] ** 2 - full_side["exact"] ** 2
    )
    infinite_transfer_upper = (
        perturbation.energy_squared_difference_upper
        + min(
            sparse_certificate.simple_tail_upper,
            sparse_certificate.stein_tail_upper,
        )
        + min(
            full_certificate.simple_tail_upper,
            full_certificate.stein_tail_upper,
        )
    )
    growing_transfer = growing_horizon_energy_upper(
        reference_finite_energy=math.sqrt(sparse_finite),
        finite_sequence_difference_upper=(
            perturbation.sequence_difference_upper
        ),
        reference_block_norm=sparse_certificate.block_power_norm,
        power_defect_upper=d_horizon,
        perturbed_source_norm_upper=(
            hs_norm(sparse_side["source"]) + defects.source
        ),
        perturbed_observation_norm_upper=(
            spectral_norm(sparse_side["observation"])
            + defects.observation
        ),
        perturbed_power_norms=full_side["power_norms"],
        horizon=horizon,
    )
    return {
        "actual_operator_defect": actual_operator,
        "factor_aware_operator_defect_upper": defects.operator,
        "actual_source_defect": actual_source,
        "factor_aware_source_defect_upper": defects.source,
        "actual_observation_defect": actual_observation,
        "factor_aware_observation_defect_upper": defects.observation,
        "normalized_coupling_defect_upper": defects.normalized_coupling,
        "factor_bounds_dominate_actual": (
            actual_operator <= defects.operator * (1.0 + 2.0e-8) + 2.0e-14
            and actual_source <= defects.source * (1.0 + 2.0e-8) + 2.0e-14
            and actual_observation
            <= defects.observation * (1.0 + 2.0e-8) + 2.0e-14
        ),
        "sparse_block_power_norm": sparse_certificate.block_power_norm,
        "full_block_power_norm": full_certificate.block_power_norm,
        "actual_block_power_defect": actual_power_defect,
        "semigroup_telescope_upper": d_horizon,
        "transferred_block_norm_upper": transferred_block_upper,
        "transferred_contraction_margin": 1.0 - transferred_block_upper,
        "telescope_over_sparse_contraction_margin": (
            d_horizon / (1.0 - sparse_certificate.block_power_norm)
        ),
        "actual_finite_energy_squared_difference": abs(
            sparse_finite - full_finite
        ),
        "finite_energy_squared_perturbation_upper": (
            perturbation.energy_squared_difference_upper
        ),
        "actual_full_energy_squared_difference": actual_energy_squared_difference,
        "full_energy_squared_transfer_upper": infinite_transfer_upper,
        "transferred_full_energy_squared_upper": (
            growing_transfer.perturbed_full_energy_squared_upper
        ),
        "transferred_full_energy_upper": (
            growing_transfer.perturbed_full_energy_upper
        ),
        "transferred_tail_energy_squared_upper": (
            growing_transfer.perturbed_tail_energy_squared_upper
        ),
        "sparse_exact_hardy_energy": sparse_side["exact"],
        "full_exact_hardy_energy": full_side["exact"],
        "sparse_hardy_certificate_upper": sparse_certificate.energy_upper,
        "full_hardy_certificate_upper": full_certificate.energy_upper,
    }


def comparison_payload(
    sparse: dict[str, object],
    full: dict[str, object],
    horizon: int,
    sigma: float,
    dimension: int,
    multiple: float,
) -> dict[str, object]:
    matrix_defect = np.asarray(sparse["matrix"]) - np.asarray(full["matrix"])
    coarse_defect = np.asarray(sparse["coarse"]) - np.asarray(full["coarse"])
    b_defect = np.asarray(sparse["coupling_b"]) - np.asarray(full["coupling_b"])
    c_defect = np.asarray(sparse["coupling_c"]) - np.asarray(full["coupling_c"])
    sparse_fine = sparse["fine_factors"]
    full_fine = full["fine_factors"]
    sparse_coarse = sparse["coarse_factors"]
    full_coarse = full["coarse_factors"]
    fine_projector = spectral_norm(
        sparse_fine["projection"] - full_fine["projection"]
    )
    coarse_projector = spectral_norm(
        sparse_coarse["projection"] - full_coarse["projection"]
    )
    fine_weighted = spectral_norm(
        sparse_fine["weighted"] - full_fine["weighted"]
    )
    coarse_weighted = spectral_norm(
        sparse_coarse["weighted"] - full_coarse["weighted"]
    )
    matrix_spectral = spectral_norm(matrix_defect)
    coarse_spectral = spectral_norm(coarse_defect)
    b_hs = hs_norm(b_defect)
    c_hs = hs_norm(c_defect)
    left_defects = factor_aware_left_defects(
        hardy_radius=HARDY_RADIUS,
        markov_defect=matrix_spectral,
        weighted_riesz_defect=fine_weighted,
        projector_defect=fine_projector,
        coupling_norm=hs_norm(sparse["coupling_b"]),
        coupling_defect=b_hs,
        perturbed_complement_norm=spectral_norm(full_fine["complement"]),
    )
    right_defects = factor_aware_right_defects(
        hardy_radius=HARDY_RADIUS,
        markov_defect=coarse_spectral,
        weighted_riesz_defect=coarse_weighted,
        projector_defect=coarse_projector,
        coupling_norm=hs_norm(sparse["coupling_c"]),
        coupling_defect=c_hs,
    )
    normalized_b_actual = hs_norm(
        sparse["coupling_b"] / hs_norm(sparse["coupling_b"])
        - full["coupling_b"] / hs_norm(full["coupling_b"])
    )
    normalized_c_actual = hs_norm(
        sparse["coupling_c"] / hs_norm(sparse["coupling_c"])
        - full["coupling_c"] / hs_norm(full["coupling_c"])
    )
    analytic = cutoff_bound(dimension, sigma, multiple)
    return {
        "cutoff_multiple": multiple,
        "effective_cutoff_multiple": analytic.effective_multiple,
        "analytic_markov_frobenius_upper": analytic.two_norm_upper,
        "matrix_defects": {
            "markov_frobenius": hs_norm(matrix_defect),
            "markov_spectral": matrix_spectral,
            "coarse_markov_spectral": coarse_spectral,
            "coupling_b_hilbert_schmidt": b_hs,
            "coupling_c_hilbert_schmidt": c_hs,
        },
        "intrinsic_factor_defects": {
            "fine_projector_spectral": fine_projector,
            "coarse_projector_spectral": coarse_projector,
            "fine_weighted_riesz_spectral": fine_weighted,
            "coarse_weighted_riesz_spectral": coarse_weighted,
            "fine_bulk_spectral": spectral_norm(
                sparse_fine["bulk"] - full_fine["bulk"]
            ),
            "coarse_bulk_spectral": spectral_norm(
                sparse_coarse["bulk"] - full_coarse["bulk"]
            ),
            "normalized_coupling_b_actual": normalized_b_actual,
            "normalized_coupling_c_actual": normalized_c_actual,
        },
        "left": side_transfer_payload(
            "left", sparse, full, left_defects, horizon
        ),
        "right": side_transfer_payload(
            "right", sparse, full, right_defects, horizon
        ),
    }


def run_sigma(sigma: float, horizon: int) -> dict[str, object]:
    started = time.perf_counter()
    dimension = max(32, 2 * int(round(FINE_RESOLUTION / sigma / 2.0)))
    coarse = coarse_embedding(dimension)
    detail = detail_embedding(dimension)
    full = build_model(
        full_folded_gaussian_matrix(dimension, sigma),
        coarse,
        detail,
        horizon,
    )
    comparisons = []
    sparse_models = {}
    for multiple in CUTOFF_MULTIPLES:
        matrix = sparse_folded_gaussian_matrix(
            dimension,
            sigma,
            support_standard_deviations=multiple,
        ).toarray()
        sparse = build_model(matrix, coarse, detail, horizon)
        sparse_models[multiple] = sparse
        comparisons.append(
            comparison_payload(
                sparse,
                full,
                horizon,
                sigma,
                dimension,
                multiple,
            )
        )
    adaptive = adaptive_cutoff_multiple(1.0 / dimension)
    matching = next(
        (
            value
            for value in CUTOFF_MULTIPLES
            if abs(value - adaptive) <= 8.0 * np.finfo(float).eps
        ),
        None,
    )
    if matching is None:
        adaptive_matrix = sparse_folded_gaussian_matrix(
            dimension,
            sigma,
            support_standard_deviations=adaptive,
        ).toarray()
        adaptive_model = build_model(
            adaptive_matrix, coarse, detail, horizon
        )
        adaptive_comparison = comparison_payload(
            adaptive_model,
            full,
            horizon,
            sigma,
            dimension,
            adaptive,
        )
    else:
        adaptive_comparison = next(
            item for item in comparisons if item["cutoff_multiple"] == matching
        )
    return {
        "sigma": sigma,
        "fine_dimension": dimension,
        "fine_dimension_times_sigma": dimension * sigma,
        "horizon": horizon,
        "full_model": model_payload(full),
        "comparisons": comparisons,
        "adaptive_cutoff": {
            "declared_multiple": adaptive,
            "coincides_with_stored_comparison": matching,
            "comparison": adaptive_comparison,
        },
        "elapsed_seconds": time.perf_counter() - started,
    }


def extrema(rows: list[dict[str, object]]) -> dict[str, float | bool]:
    comparisons = [item for row in rows for item in row["comparisons"]]
    stress = [item for item in comparisons if item["cutoff_multiple"] == 5.0]
    return {
        "maximum_stress_markov_spectral_defect": max(
            item["matrix_defects"]["markov_spectral"] for item in stress
        ),
        "maximum_stress_fine_weighted_riesz_defect": max(
            item["intrinsic_factor_defects"]["fine_weighted_riesz_spectral"]
            for item in stress
        ),
        "maximum_stress_normalized_b_defect": max(
            item["intrinsic_factor_defects"]["normalized_coupling_b_actual"]
            for item in stress
        ),
        "maximum_stress_block_margin_ratio": max(
            item[side]["telescope_over_sparse_contraction_margin"]
            for item in stress
            for side in ("left", "right")
        ),
        "maximum_stress_full_energy_squared_transfer_upper": max(
            item[side]["full_energy_squared_transfer_upper"]
            for item in stress
            for side in ("left", "right")
        ),
        "all_factor_bounds_dominate_actual": all(
            item[side]["factor_bounds_dominate_actual"]
            for item in comparisons
            for side in ("left", "right")
        ),
        "all_transferred_blocks_contract": all(
            item[side]["transferred_block_norm_upper"] < 1.0
            for item in comparisons
            for side in ("left", "right")
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    sigmas = SMOKE_SIGMAS if args.smoke else FULL_SIGMAS
    rows = []
    for sigma, horizon in zip(sigmas, HORIZONS):
        row = run_sigma(sigma, horizon)
        rows.append(row)
        stress = row["comparisons"][0]
        print(
            json.dumps(
                {
                    "sigma": sigma,
                    "dimension": row["fine_dimension"],
                    "horizon": horizon,
                    "L5_markov_defect": stress["matrix_defects"][
                        "markov_spectral"
                    ],
                    "L5_left_transfer": stress["left"][
                        "full_energy_squared_transfer_upper"
                    ],
                    "elapsed_seconds": row["elapsed_seconds"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    payload = {
        "status": "binary64_factor_aware_sparse_full_intrinsic_transfer_audit",
        "evidence_level": (
            "dense binary64 recomputation of full and sparse intrinsic Riesz "
            "factors, deterministic all-column Hardy sums, and exact finite-time "
            "ledgers; diagnostic rather than interval validated"
        ),
        "fine_resolution": FINE_RESOLUTION,
        "hardy_radius": HARDY_RADIUS,
        "cutoff_multiples": list(CUTOFF_MULTIPLES),
        "rows": rows,
        "extrema": extrema(rows),
        "sources": {
            name: {
                "path": str(path.relative_to(REPOSITORY)),
                "sha256": sha256_file(path),
            }
            for name, path in {
                "folded_gaussian_builder": RH14
                / "src"
                / "parity_boundary"
                / "operators.py",
                "rh39_cutoff_theorem": RH39 / "main.tex",
                "rh48_identification_theorem": RH48 / "main.tex",
                "rh49_quarter_power_theorem": RH49 / "main.tex",
                "rh50_hardy_theorem": RH50 / "main.tex",
                "rh52_factor_theorem": RH52 / "main.tex",
                "rh53_tail_theorem": RH53 / "main.tex",
            }.items()
        },
        "limitations": [
            "All matrix, eigensolver, Lyapunov, and norm quantities are binary64 diagnostics.",
            "Directly recomputed projector and weighted-Riesz defects are not contour-resolvent enclosures.",
            "The five levels do not prove a dyadically uniform Riesz-conditioning modulus or Hardy trace budget.",
            "The adaptive multiple equals five on these pilot dimensions; its asymptotic distinction begins on finer grids.",
        ],
    }
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "factor_aware_transfer_pilot_smoke.json"
    )
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output.relative_to(ROOT))}, sort_keys=True))


if __name__ == "__main__":
    main()
