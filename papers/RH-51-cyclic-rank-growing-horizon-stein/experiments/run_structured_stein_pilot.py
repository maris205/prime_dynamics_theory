"""Dense exact-Gramian audit for RH-51.

The matrices are binary64 cell-average folded-Gaussian models.  The
Lyapunov equations are solved densely, so this audit deliberately uses a
smaller fixed resolution ``N*sigma=5.12`` than the matrix-free RH-50 pilot.
It is evidence about certificate geometry, not an interval validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import eig


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH50 = PAPERS / "RH-50-two-pole-hilbert-schmidt-hardy"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH14 / "src"))

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from structured_stein import (  # noqa: E402
    conic_vector_witness,
    controllability_gramian,
    cyclic_rank_profile,
    gramian_spectrum,
    isotropic_block_completion,
    low_rank_isotropic_floor,
    stein_defect,
)


OUTPUT = ROOT / "results" / "structured_stein_pilot.json"
FULL_SIGMAS = (0.16, 0.08, 0.04, 0.02, 0.01)
SMOKE_SIGMAS = (0.16, 0.08)
FINE_RESOLUTION = 5.12
HARDY_RADIUS = 0.85
CYCLIC_MAXIMUM_POWER = 9
CYCLIC_RELATIVE_TOLERANCE = 1.0e-8
POWER_CHECKPOINTS = (1, 2, 4, 8, 12, 16, 24, 32, 48, 64)
BLOCK_FLOOR_TARGET = 0.25


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


def spectral_bulk(matrix: np.ndarray) -> dict[str, object]:
    """Resolve Perron/parity factors and remove both rank-one channels."""

    values, left_raw, right_raw = eig(
        matrix, left=True, right=True, check_finite=False
    )
    perron_index = int(np.argmin(np.abs(values - 1.0)))
    real_negative = np.flatnonzero(
        (np.abs(values.imag) < 2.0e-8) & (values.real < -1.0e-8)
    )
    if not real_negative.size:
        raise RuntimeError("no negative real parity eigenvalue was resolved")
    parity_index = int(real_negative[np.argmin(values[real_negative].real)])
    selected = np.asarray(
        (values[perron_index], values[parity_index]),
        dtype=np.complex128,
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
    gram = left.conjugate().T @ right
    left = left @ np.linalg.inv(gram).conjugate().T
    projection = right @ left.conjugate().T
    bulk = matrix - right @ np.diag(selected) @ left.conjugate().T
    complement = np.eye(matrix.shape[0]) - projection
    remaining = np.delete(values, (perron_index, parity_index))
    return {
        "right": real_if_small(right),
        "left": real_if_small(left),
        "projection": real_if_small(projection),
        "complement": real_if_small(complement),
        "bulk": real_if_small(bulk),
        "eigenvalues": real_if_small(selected),
        "bulk_radius": float(np.max(np.abs(remaining), initial=0.0)),
        "biorthogonality_defect": float(
            np.max(np.abs(left.conjugate().T @ right - np.eye(2)))
        ),
    }


def energy(gramian: np.ndarray, observation: np.ndarray) -> float:
    value = np.trace(
        observation @ gramian @ observation.conjugate().T
    ).real
    return float(math.sqrt(max(float(value), 0.0)))


def spectrum_payload(summary) -> dict[str, object]:
    eigenvalues = np.asarray(summary.eigenvalues, dtype=np.float64)
    total = float(np.sum(eigenvalues))
    normalized = eigenvalues / total if total > 0.0 else eigenvalues
    return {
        "trace": float(summary.trace),
        "participation_rank": float(summary.participation_rank),
        "rank_for_99_percent_trace": int(summary.rank_for_99_percent_trace),
        "numerical_rank": int(summary.numerical_rank),
        "normalized_eigenvalues": normalized.tolist(),
    }


def power_norm_ledger(operator: np.ndarray) -> list[dict[str, float | int]]:
    checkpoints = set(POWER_CHECKPOINTS)
    power = np.eye(operator.shape[0], dtype=operator.dtype)
    rows = []
    for horizon in range(1, max(POWER_CHECKPOINTS) + 1):
        power = operator @ power
        if horizon in checkpoints:
            norm = float(np.linalg.norm(power, 2))
            rows.append(
                {
                    "horizon": horizon,
                    "power_norm": norm,
                    "power_norm_squared": norm * norm,
                }
            )
    return rows


def block_completion_payload(
    operator: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
) -> dict[str, object]:
    ledger = power_norm_ledger(operator)
    observation_hs_squared = float(np.linalg.norm(observation, "fro") ** 2)
    contracting = [row for row in ledger if row["power_norm"] < 1.0]
    controlled = [
        row
        for row in contracting
        if row["power_norm_squared"] * observation_hs_squared
        <= BLOCK_FLOOR_TARGET
    ]
    selected = controlled[0] if controlled else (contracting[-1] if contracting else None)
    if selected is None:
        return {
            "power_norm_ledger": ledger,
            "observation_hilbert_schmidt_squared": observation_hs_squared,
            "selected_horizon": None,
            "completion_available_through_maximum_checkpoint": False,
        }
    completion = isotropic_block_completion(
        operator, source, int(selected["horizon"])
    )
    return {
        "power_norm_ledger": ledger,
        "observation_hilbert_schmidt_squared": observation_hs_squared,
        "selected_horizon": int(completion.horizon),
        "selected_power_norm": float(completion.power_norm),
        "selected_power_floor_clock": float(
            completion.power_norm**2 * observation_hs_squared
        ),
        "isotropic_floor": float(completion.isotropic_floor),
        "block_defect_minimum_eigenvalue": float(
            completion.block_defect_minimum_eigenvalue
        ),
        "energy_upper": energy(completion.candidate, observation),
        "completion_available_through_maximum_checkpoint": True,
    }


def low_rank_floor_payload(gramian: np.ndarray) -> list[dict[str, float | int]]:
    ranks = sorted({0, 4, 8, 16, 32, gramian.shape[0] // 8})
    return [
        {
            "factor_rank": int(rank),
            "necessary_isotropic_floor": low_rank_isotropic_floor(
                gramian, rank
            ),
        }
        for rank in ranks
        if rank < gramian.shape[0]
    ]


def run_sigma(sigma: float) -> dict[str, object]:
    started = time.perf_counter()
    fine_dimension = max(32, 2 * int(round(FINE_RESOLUTION / sigma / 2.0)))
    coarse_dimension = fine_dimension // 2
    fine_sparse = sparse_folded_gaussian_matrix(fine_dimension, sigma)
    fine = fine_sparse.toarray()
    u = coarse_embedding(fine_dimension)
    w = detail_embedding(fine_dimension)
    fine_u = fine @ u
    fine_w = fine @ w
    coarse = u.T @ fine_u
    coupling_b = u.T @ fine_w
    coupling_c = w.T @ fine_u

    fine_data = spectral_bulk(fine)
    coarse_data = spectral_bulk(coarse)
    fine_bulk = np.asarray(fine_data["bulk"])
    coarse_bulk = np.asarray(coarse_data["bulk"])
    fine_q = np.asarray(fine_data["complement"])
    coarse_q = np.asarray(coarse_data["complement"])
    scaled_fine = fine_bulk / HARDY_RADIUS
    scaled_coarse = coarse_bulk / HARDY_RADIUS

    b_norm = float(np.linalg.norm(coupling_b, "fro"))
    c_norm = float(np.linalg.norm(coupling_c, "fro"))
    left_source = fine_q @ u @ coupling_b / b_norm
    left_observation = u.T
    right_source = coupling_c.conjugate().T / c_norm
    right_operator = scaled_coarse.conjugate().T
    right_observation = coarse_q.conjugate().T

    left_gramian = controllability_gramian(scaled_fine, left_source)
    right_gramian = controllability_gramian(right_operator, right_source)
    left_summary = gramian_spectrum(left_gramian)
    right_summary = gramian_spectrum(right_gramian)

    identity_defect = np.eye(fine_dimension) - (
        scaled_fine @ scaled_fine.conjugate().T
    )
    identity_values, identity_vectors = np.linalg.eigh(
        0.5 * (identity_defect + identity_defect.conjugate().T)
    )
    witness = conic_vector_witness(
        scaled_fine,
        left_source,
        (np.eye(fine_dimension),),
        identity_vectors[:, 0],
    )
    diagonal_candidate = np.diag(np.diag(left_gramian))
    diagonal_defect = stein_defect(
        scaled_fine, diagonal_candidate, left_source
    )

    left_block = block_completion_payload(
        scaled_fine, left_source, left_observation
    )
    right_block = block_completion_payload(
        right_operator, right_source, right_observation
    )
    row = {
        "sigma": float(sigma),
        "fine_dimension": fine_dimension,
        "coarse_dimension": coarse_dimension,
        "fine_dimension_times_sigma": fine_dimension * sigma,
        "hardy_radius": HARDY_RADIUS,
        "fine_bulk_radius_candidate": float(fine_data["bulk_radius"]),
        "coarse_bulk_radius_candidate": float(coarse_data["bulk_radius"]),
        "fine_scaled_bulk_radius_candidate": float(
            fine_data["bulk_radius"] / HARDY_RADIUS
        ),
        "fine_biorthogonality_defect": float(
            fine_data["biorthogonality_defect"]
        ),
        "coarse_biorthogonality_defect": float(
            coarse_data["biorthogonality_defect"]
        ),
        "B_hilbert_schmidt_norm": b_norm,
        "C_hilbert_schmidt_norm": c_norm,
        "left_exact_hardy_energy": energy(left_gramian, left_observation),
        "right_exact_hardy_energy": energy(right_gramian, right_observation),
        "left_exact_stein_defect_norm": float(
            np.linalg.norm(
                stein_defect(scaled_fine, left_gramian, left_source), 2
            )
        ),
        "right_exact_stein_defect_norm": float(
            np.linalg.norm(
                stein_defect(right_operator, right_gramian, right_source), 2
            )
        ),
        "left_gramian": spectrum_payload(left_summary),
        "right_gramian": spectrum_payload(right_summary),
        "left_cyclic_rank_profile": cyclic_rank_profile(
            scaled_fine,
            left_source,
            CYCLIC_MAXIMUM_POWER,
            relative_tolerance=CYCLIC_RELATIVE_TOLERANCE,
        ),
        "identity_metric": {
            "minimum_unforced_defect_eigenvalue": float(identity_values[0]),
            "scalar_cone_witness_source_quadratic_form": float(
                witness.source_quadratic_form
            ),
            "scalar_identity_cone_obstructed": bool(witness.obstructs_cone),
        },
        "diagonal_of_exact_gramian": {
            "minimum_stein_defect_eigenvalue": float(
                np.min(np.linalg.eigvalsh(diagonal_defect)).real
            ),
            "is_a_supersolution": bool(
                np.min(np.linalg.eigvalsh(diagonal_defect)).real >= -1.0e-10
            ),
        },
        "left_low_rank_plus_identity_floors": low_rank_floor_payload(
            left_gramian
        ),
        "left_block_completion": left_block,
        "right_block_completion": right_block,
        "elapsed_seconds": time.perf_counter() - started,
    }
    return row


def fit_power(rows: list[dict[str, object]], field: str) -> dict[str, float]:
    x = np.log(np.asarray([float(row["sigma"]) for row in rows]))
    y = np.log(np.asarray([float(row[field]) for row in rows]))
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return {
        "sigma_power": float(slope),
        "growth_exponent": float(max(0.0, -slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "levels": len(rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    rows = []
    for sigma in (SMOKE_SIGMAS if args.smoke else FULL_SIGMAS):
        row = run_sigma(float(sigma))
        rows.append(row)
        print(
            json.dumps(
                {
                    "sigma": row["sigma"],
                    "fine_dimension": row["fine_dimension"],
                    "left_energy": row["left_exact_hardy_energy"],
                    "right_energy": row["right_exact_hardy_energy"],
                    "left_effective_rank": row["left_gramian"][
                        "participation_rank"
                    ],
                    "left_cyclic_rank_at_9": row[
                        "left_cyclic_rank_profile"
                    ][-1]["numerical_rank"],
                    "left_block_horizon": row["left_block_completion"][
                        "selected_horizon"
                    ],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    source_path = RH14 / "src" / "parity_boundary" / "operators.py"
    payload = {
        "status": "floating_dense_exact_gramian_and_structured_stein_audit",
        "evidence_level": (
            "binary64 dense Lyapunov, eigenspectrum, Krylov-rank, and block-completion diagnostic; not interval validated"
        ),
        "fine_resolution": FINE_RESOLUTION,
        "hardy_radius": HARDY_RADIUS,
        "cyclic_maximum_power": CYCLIC_MAXIMUM_POWER,
        "cyclic_relative_singular_tolerance": CYCLIC_RELATIVE_TOLERANCE,
        "power_checkpoints": list(POWER_CHECKPOINTS),
        "block_floor_target": BLOCK_FLOOR_TARGET,
        "sources": {
            "folded_gaussian": {
                "path": str(source_path.relative_to(REPOSITORY)),
                "sha256": sha256_file(source_path),
            },
            "rh50_manuscript": {
                "path": str((RH50 / "main.tex").relative_to(REPOSITORY)),
                "sha256": sha256_file(RH50 / "main.tex"),
            },
        },
        "rows": rows,
        "fits": {
            "left_exact_hardy_energy": fit_power(
                rows, "left_exact_hardy_energy"
            ),
            "right_exact_hardy_energy": fit_power(
                rows, "right_exact_hardy_energy"
            ),
            "left_participation_rank": fit_power(
                [
                    {
                        **row,
                        "rank_value": row["left_gramian"][
                            "participation_rank"
                        ],
                    }
                    for row in rows
                ],
                "rank_value",
            ),
            "right_participation_rank": fit_power(
                [
                    {
                        **row,
                        "rank_value": row["right_gramian"][
                            "participation_rank"
                        ],
                    }
                    for row in rows
                ],
                "rank_value",
            ),
        },
        "limitations": [
            "The dense audit uses N*sigma=5.12, below the production resolution N*sigma=20.48 used in RH-50.",
            "All eigendata, Lyapunov solves, singular values, and minimum eigenvalues are binary64 and are not interval enclosures.",
            "The cyclic ranks are numerical ranks at the explicitly stored relative singular-value threshold.",
            "The isotropic block completions are finite-matrix certificates in floating arithmetic; no dyadically uniform small-noise trace budget is inferred.",
            "Failure of the scalar identity cone or of the diagonal extracted from the exact Gramian does not rule out all diagonal, banded, multilevel, or anisotropic metrics.",
        ],
    }
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "structured_stein_pilot_smoke.json"
    )
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "fits": payload["fits"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
