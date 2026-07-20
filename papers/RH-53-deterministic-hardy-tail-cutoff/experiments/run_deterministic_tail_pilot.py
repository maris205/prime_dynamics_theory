"""Dense deterministic Hardy-tail and cutoff audit for RH-53."""

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
RH50 = PAPERS / "RH-50-two-pole-hilbert-schmidt-hardy"
RH51 = PAPERS / "RH-51-cyclic-rank-growing-horizon-stein"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH14 / "src"))

from hardy_tail import (  # noqa: E402
    adaptive_cutoff_multiple,
    cutoff_bound,
    deterministic_hardy_certificate,
    deterministic_main_sum,
)
from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402


OUTPUT = ROOT / "results" / "deterministic_tail_pilot.json"
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


def real_if_small(value: np.ndarray, tolerance: float = 2.0e-9) -> np.ndarray:
    array = np.asarray(value)
    if np.max(np.abs(array.imag), initial=0.0) <= tolerance:
        return array.real.astype(np.float64)
    return array.astype(np.complex128)


def spectral_bulk(matrix: np.ndarray) -> dict[str, np.ndarray | float]:
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
        (np.ones(matrix.shape[0], dtype=np.complex128), right_raw[:, parity_index])
    )
    left = np.column_stack((left_raw[:, perron_index], left_raw[:, parity_index]))
    left = left @ np.linalg.inv(left.conjugate().T @ right).conjugate().T
    projection = right @ left.conjugate().T
    bulk = matrix - right @ np.diag(selected) @ left.conjugate().T
    return {
        "bulk": real_if_small(bulk),
        "complement": real_if_small(np.eye(matrix.shape[0]) - projection),
    }


def exact_energy(operator: np.ndarray, source: np.ndarray, observation: np.ndarray) -> float:
    gramian = solve_discrete_lyapunov(
        operator, source @ source.conjugate().T
    )
    value = np.trace(observation @ gramian @ observation.conjugate().T).real
    return math.sqrt(max(float(value), 0.0))


def certificate_payload(certificate, exact: float) -> dict[str, float | int]:
    return {
        "horizon": certificate.horizon,
        "deterministic_main_energy_squared": certificate.main_energy_squared,
        "block_power_norm": certificate.block_power_norm,
        "contraction_margin": certificate.contraction_margin,
        "simple_infinite_tail_upper": certificate.simple_tail_upper,
        "stein_infinite_tail_upper": certificate.stein_tail_upper,
        "selected_infinite_tail_upper": min(
            certificate.simple_tail_upper, certificate.stein_tail_upper
        ),
        "full_energy_upper": certificate.energy_upper,
        "exact_dense_energy": exact,
        "relative_energy_excess": certificate.energy_upper / exact - 1.0,
    }


def full_folded_gaussian_matrix(
    dimension: int, sigma: float, *, u: float = 1.5436890126920764
) -> np.ndarray:
    nodes = (np.arange(dimension, dtype=np.float64) + 0.5) / dimension
    means = 1.0 - u * nodes * nodes
    positive = -0.5 * ((nodes[None, :] - means[:, None]) / sigma) ** 2
    negative = -0.5 * ((-nodes[None, :] - means[:, None]) / sigma) ** 2
    logs = np.logaddexp(positive, negative)
    logs -= np.max(logs, axis=1, keepdims=True)
    weights = np.exp(logs)
    return weights / np.sum(weights, axis=1, keepdims=True)


def run_sigma(sigma: float, horizon: int) -> dict[str, object]:
    started = time.perf_counter()
    fine_dimension = max(32, 2 * int(round(FINE_RESOLUTION / sigma / 2.0)))
    sparse = sparse_folded_gaussian_matrix(fine_dimension, sigma).toarray()
    u = coarse_embedding(fine_dimension)
    w = detail_embedding(fine_dimension)
    sparse_u = sparse @ u
    sparse_w = sparse @ w
    coarse = u.T @ sparse_u
    coupling_b = u.T @ sparse_w
    coupling_c = w.T @ sparse_u
    fine_data = spectral_bulk(sparse)
    coarse_data = spectral_bulk(coarse)
    fine_operator = np.asarray(fine_data["bulk"]) / HARDY_RADIUS
    coarse_operator = np.asarray(coarse_data["bulk"]).conjugate().T / HARDY_RADIUS
    left_source = (
        np.asarray(fine_data["complement"])
        @ u
        @ coupling_b
        / np.linalg.norm(coupling_b, "fro")
    )
    right_source = coupling_c.conjugate().T / np.linalg.norm(coupling_c, "fro")
    left_observation = u.T
    right_observation = np.asarray(coarse_data["complement"]).conjugate().T
    left_exact = exact_energy(fine_operator, left_source, left_observation)
    right_exact = exact_energy(coarse_operator, right_source, right_observation)
    left = deterministic_hardy_certificate(
        fine_operator, left_source, left_observation, horizon
    )
    right = deterministic_hardy_certificate(
        coarse_operator, right_source, right_observation, horizon
    )

    full_comparison = None
    if fine_dimension <= 128:
        full = full_folded_gaussian_matrix(fine_dimension, sigma)
        defect = sparse - full
        full_comparison = {
            "actual_frobenius_defect": float(np.linalg.norm(defect, "fro")),
            "actual_spectral_defect": float(np.linalg.norm(defect, 2)),
        }
    cutoffs = []
    for multiple in CUTOFF_MULTIPLES:
        bound = cutoff_bound(fine_dimension, sigma, multiple)
        cutoffs.append(
            {
                "declared_multiple": multiple,
                "effective_multiple": bound.effective_multiple,
                "omitted_mass_upper": bound.omitted_mass_upper,
                "two_norm_upper": bound.two_norm_upper,
            }
        )
    adaptive = adaptive_cutoff_multiple(1.0 / fine_dimension)
    adaptive_bound = cutoff_bound(fine_dimension, sigma, adaptive)
    return {
        "sigma": sigma,
        "fine_dimension": fine_dimension,
        "fine_dimension_times_sigma": fine_dimension * sigma,
        "left": certificate_payload(left, left_exact),
        "right": certificate_payload(right, right_exact),
        "deterministic_main_identity_check": {
            "left_absolute_difference": abs(
                deterministic_main_sum(
                    fine_operator, left_source, left_observation, horizon
                )
                - left.main_energy_squared
            ),
            "right_absolute_difference": abs(
                deterministic_main_sum(
                    coarse_operator, right_source, right_observation, horizon
                )
                - right.main_energy_squared
            ),
        },
        "cutoff_bounds": cutoffs,
        "adaptive_cutoff": {
            "declared_multiple": adaptive,
            "two_norm_upper": adaptive_bound.two_norm_upper,
        },
        "dense_full_kernel_comparison": full_comparison,
        "elapsed_seconds": time.perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    sigmas = SMOKE_SIGMAS if args.smoke else FULL_SIGMAS
    horizons = HORIZONS[: len(sigmas)]
    rows = []
    for sigma, horizon in zip(sigmas, horizons):
        row = run_sigma(sigma, horizon)
        rows.append(row)
        print(
            json.dumps(
                {
                    "sigma": sigma,
                    "dimension": row["fine_dimension"],
                    "horizon": horizon,
                    "left_upper": row["left"]["full_energy_upper"],
                    "right_upper": row["right"]["full_energy_upper"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    payload = {
        "status": "binary64_deterministic_full_hardy_and_cutoff_mechanism_audit",
        "evidence_level": (
            "deterministic all-column Frobenius sums and analytic infinite-tail "
            "formulas evaluated in binary64; no Hutchinson probes; not interval validated"
        ),
        "fine_resolution": FINE_RESOLUTION,
        "hardy_radius": HARDY_RADIUS,
        "cutoff_multiples": list(CUTOFF_MULTIPLES),
        "rows": rows,
        "sources": {
            "folded_gaussian_builder": {
                "path": str(
                    (RH14 / "src" / "parity_boundary" / "operators.py").relative_to(
                        REPOSITORY
                    )
                ),
                "sha256": sha256_file(
                    RH14 / "src" / "parity_boundary" / "operators.py"
                ),
            },
            "rh51_pilot": {
                "path": str(
                    (RH51 / "results" / "structured_stein_pilot.json").relative_to(
                        REPOSITORY
                    )
                ),
                "sha256": sha256_file(
                    RH51 / "results" / "structured_stein_pilot.json"
                ),
            },
            "rh50_pilot": {
                "path": str(
                    (RH50 / "results" / "two_pole_hardy_pilot.json").relative_to(
                        REPOSITORY
                    )
                ),
                "sha256": sha256_file(
                    RH50 / "results" / "two_pole_hardy_pilot.json"
                ),
            },
        },
        "limitations": [
            "All dense matrix and eigensolver quantities in this pilot are binary64 diagnostics.",
            "The full-kernel comparison is formed only through dimension 128.",
            "The analytic cutoff upper controls the Markov matrix before intrinsic factors are recomputed.",
            "No uniform small-noise Hardy bound is inferred from five stored levels.",
        ],
    }
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "deterministic_tail_pilot_smoke.json"
    )
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"output": str(output.relative_to(ROOT))}, sort_keys=True))


if __name__ == "__main__":
    main()
