"""Floating small-noise Perron/parity factor and conditioning audit."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH14 / "src"))

from parity_boundary import (  # noqa: E402
    R_FIXED,
    sparse_folded_gaussian_matrix,
)
from peripheral_conditioning import (  # noqa: E402
    contour_resolvent_lower,
    endpoint_log_coefficient,
    endpoint_tail_constant,
    low_rank_frobenius,
    low_rank_singular_values,
)


OUTPUT = ROOT / "results" / "small_noise_peripheral_factor_pilot.json"
FULL_SIGMAS = (0.03, 0.02, 0.01, 0.004, 0.002, 0.001, 0.0005, 0.0002, 0.0001)
SMOKE_SIGMAS = (0.03, 0.01, 0.004, 0.002, 0.001)
RESOLUTION = 20.48
CONTOUR_RADIUS = 0.05


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def deterministic_start(dimension: int, phase: float) -> np.ndarray:
    index = np.arange(int(dimension), dtype=np.float64)
    vector = np.sin((index + 0.5) * math.sqrt(2.0 + phase))
    vector += 0.37 * np.cos((index + 0.5) * math.sqrt(3.0 + phase))
    return vector / np.linalg.norm(vector)


def resolve_factors(
    matrix: csr_matrix, sigma: float
) -> dict[str, object]:
    dimension = matrix.shape[0]
    count = min(8, dimension - 2)
    values, right = eigs(
        matrix,
        k=count,
        which="LM",
        tol=3.0e-10,
        maxiter=18000,
        v0=deterministic_start(dimension, 0.0),
    )
    left_values, left = eigs(
        matrix.T,
        k=count,
        which="LM",
        tol=3.0e-10,
        maxiter=18000,
        v0=deterministic_start(dimension, 0.41),
    )

    perron_index = int(np.argmin(np.abs(values - 1.0)))
    remaining = np.delete(np.arange(values.size), perron_index)
    real_candidates = remaining[np.abs(values[remaining].imag) < 3.0e-7]
    if not real_candidates.size:
        raise RuntimeError("no real negative parity eigenvalue was resolved")
    parity_index = int(
        real_candidates[np.argmin(values[real_candidates].real)]
    )
    parity = float(values[parity_index].real)

    perron_left_index = int(np.argmin(np.abs(left_values - 1.0)))
    perron_mass = np.asarray(left[:, perron_left_index].real)
    if float(np.sum(perron_mass)) < 0.0:
        perron_mass *= -1.0
    perron_mass /= float(np.sum(perron_mass))

    parity_left_index = int(np.argmin(np.abs(left_values - parity)))
    parity_right = np.asarray(right[:, parity_index].real)
    grid = (np.arange(dimension, dtype=np.float64) + 0.5) / dimension
    margin = max(12.0 * float(sigma), 0.02)
    lower = grid < R_FIXED - margin
    upper = grid > R_FIXED + margin
    lower_mean = float(np.mean(parity_right[lower]))
    upper_mean = float(np.mean(parity_right[upper]))
    parity_right *= 2.0 / (lower_mean - upper_mean)
    if float(np.mean(parity_right[lower])) < 0.0:
        parity_right *= -1.0

    parity_mass = np.asarray(left[:, parity_left_index].real)
    parity_mass /= float(np.dot(parity_mass, parity_right))
    if float(np.sum(parity_mass[grid < R_FIXED])) < 0.0:
        parity_mass *= -1.0
        parity_right *= -1.0

    bulk = np.delete(values, (perron_index, parity_index))
    return {
        "eigenvalues": values,
        "perron_mass": perron_mass,
        "parity_eigenvalue": parity,
        "parity_right": parity_right,
        "parity_mass": parity_mass,
        "bulk_radius": float(np.max(np.abs(bulk), initial=0.0)),
    }


def factor_row(
    sigma: float, dimension: int, factors: dict[str, object]
) -> dict[str, object]:
    n = int(dimension)
    width = float(sigma)
    perron_mass = np.asarray(factors["perron_mass"])
    parity_mass = np.asarray(factors["parity_mass"])
    parity_right = np.asarray(factors["parity_right"])
    parity = float(factors["parity_eigenvalue"])
    ones = np.ones(n, dtype=np.float64)

    perron_density_l2 = float(math.sqrt(n) * np.linalg.norm(perron_mass))
    parity_density_l2 = float(math.sqrt(n) * np.linalg.norm(parity_mass))
    parity_observable_l2 = float(np.linalg.norm(parity_right) / math.sqrt(n))
    perron_projector = perron_density_l2
    parity_projector = parity_observable_l2 * parity_density_l2
    weighted_parity = abs(parity) * parity_projector

    left = np.column_stack((ones, parity_right))
    right = np.column_stack((perron_mass, parity * parity_mass))
    weighted_singular_values = low_rank_singular_values(left, right)
    weighted_frobenius = low_rank_frobenius(left, right)

    grid = (np.arange(n, dtype=np.float64) + 0.5) / n
    clearance = 1.0 - grid
    lower = max(8.0 * width, 1.0 / n)
    upper = 0.08
    endpoint_mask = (clearance >= lower) & (clearance <= upper)
    perron_density = n * perron_mass
    parity_density = n * parity_mass
    if np.count_nonzero(endpoint_mask) >= 4:
        endpoint_perron_energy = float(
            np.sum(perron_density[endpoint_mask] ** 2) / n
        )
        endpoint_parity_energy = float(
            np.sum(parity_density[endpoint_mask] ** 2) / n
        )
        endpoint_perron_coefficient = float(
            np.median(
                np.sqrt(clearance[endpoint_mask])
                * perron_density[endpoint_mask]
            )
        )
        endpoint_parity_coefficient = float(
            np.median(
                -np.sqrt(clearance[endpoint_mask])
                * parity_density[endpoint_mask]
            )
        )
    else:
        endpoint_perron_energy = None
        endpoint_parity_energy = None
        endpoint_perron_coefficient = None
        endpoint_parity_coefficient = None

    logarithm = math.log(1.0 / width)
    return {
        "sigma": width,
        "dimension": n,
        "dimension_times_sigma": n * width,
        "parity_eigenvalue": parity,
        "parity_gap": 1.0 + parity,
        "bulk_radius": factors["bulk_radius"],
        "perron_density_l2": perron_density_l2,
        "parity_density_l2": parity_density_l2,
        "parity_observable_l2": parity_observable_l2,
        "parity_observable_linf": float(np.max(np.abs(parity_right))),
        "perron_projector_norm": perron_projector,
        "parity_projector_norm": parity_projector,
        "weighted_parity_norm": weighted_parity,
        "weighted_rank_two_frobenius": weighted_frobenius,
        "weighted_rank_two_singular_values": weighted_singular_values.tolist(),
        "perron_projector_square_over_log": perron_projector**2 / logarithm,
        "parity_projector_square_over_log": parity_projector**2 / logarithm,
        "rank_two_frobenius_square_over_log": weighted_frobenius**2
        / logarithm,
        "perron_contour_resolvent_lower": contour_resolvent_lower(
            perron_projector, CONTOUR_RADIUS
        ),
        "parity_contour_resolvent_lower": contour_resolvent_lower(
            parity_projector, CONTOUR_RADIUS
        ),
        "endpoint_window": [lower, upper],
        "endpoint_perron_energy": endpoint_perron_energy,
        "endpoint_parity_energy": endpoint_parity_energy,
        "endpoint_perron_tail_coefficient": endpoint_perron_coefficient,
        "endpoint_parity_tail_coefficient": endpoint_parity_coefficient,
    }


def fit_log_law(rows: list[dict[str, object]], field: str) -> dict[str, float]:
    selected = rows[-min(6, len(rows)) :]
    x = np.asarray([math.log(1.0 / float(row["sigma"])) for row in selected])
    y = np.asarray([float(row[field]) ** 2 for row in selected])
    slope, intercept = np.polyfit(x, y, 1)
    fitted = slope * x + intercept
    residual = y - fitted
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "maximum_absolute_residual": float(np.max(np.abs(residual))),
        "levels": len(selected),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    sigmas = SMOKE_SIGMAS if args.smoke else FULL_SIGMAS
    rows = []
    for sigma in sigmas:
        dimension = max(64, int(round(RESOLUTION / sigma)))
        started = time.perf_counter()
        matrix = sparse_folded_gaussian_matrix(dimension, sigma)
        factors = resolve_factors(matrix, sigma)
        row = factor_row(sigma, dimension, factors)
        row["elapsed_seconds"] = time.perf_counter() - started
        rows.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)
        del matrix, factors
        gc.collect()

    payload = {
        "status": "floating_small_noise_peripheral_factor_conditioning_pilot",
        "evidence_level": "binary64_sparse_eigenfactor_diagnostic_not_validated",
        "resolution": RESOLUTION,
        "contour_radius": CONTOUR_RADIUS,
        "source": {
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
        "analytic_endpoint_tail_constant": endpoint_tail_constant(),
        "analytic_endpoint_log_coefficient": endpoint_log_coefficient(),
        "rows": rows,
        "perron_log_fit": fit_log_law(rows, "perron_projector_norm"),
        "parity_log_fit": fit_log_law(rows, "parity_projector_norm"),
        "rank_two_log_fit": fit_log_law(rows, "weighted_rank_two_frobenius"),
        "limitations": [
            "The sparse matrices use an eight-sigma support cutoff and exact row renormalization.",
            "Eigenfactors and fitted slopes are binary64 diagnostics, not interval enclosures.",
            "Projector growth does not by itself upper-bound the reduced contour resolvent.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "small_noise_peripheral_factor_pilot_smoke.json"
    )
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
