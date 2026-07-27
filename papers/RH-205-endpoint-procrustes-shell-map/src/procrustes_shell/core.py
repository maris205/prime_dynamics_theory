"""Orthogonal Procrustes transport between finite spectral packets."""

from __future__ import annotations

import math

import numpy as np


def _basis(matrix: np.ndarray) -> np.ndarray:
    values = np.asarray(matrix, dtype=complex)
    return np.linalg.qr(values, mode="reduced")[0]


def procrustes_residual_from_cosines(cosines: np.ndarray) -> dict[str, float]:
    """Return the optimal absolute and rank-normalized frame residual."""

    singular = np.asarray(cosines, dtype=float).reshape(-1)
    if singular.size < 1 or np.any(singular < 0.0) or np.any(singular > 1.0 + 1e-12):
        raise ValueError("principal cosines must lie in [0,1]")
    square = max(0.0, 2.0 * singular.size - 2.0 * float(np.sum(singular)))
    return {
        "optimal_frobenius_residual": float(math.sqrt(square)),
        "rank_normalized_residual": float(math.sqrt(square / singular.size)),
        "mean_principal_cosine": float(np.mean(singular)),
    }


def optimal_shell_map(
    coarse_frame: np.ndarray,
    fine_frame: np.ndarray,
    embedding: np.ndarray,
) -> dict[str, np.ndarray | float | list[float]]:
    """Construct the endpoint-determined optimal packet partial isometry."""

    coarse = _basis(coarse_frame)
    fine = _basis(fine_frame)
    lift = np.asarray(embedding, dtype=complex)
    if lift.shape != (fine.shape[0], coarse.shape[0]) or coarse.shape[1] != fine.shape[1]:
        raise ValueError("incompatible packet and embedding dimensions")
    overlap = fine.conj().T @ lift @ coarse
    left, singular, right_adjoint = np.linalg.svd(overlap)
    gauge = left @ right_adjoint
    transport = fine @ gauge @ coarse.conj().T
    target = fine @ gauge
    reference = lift @ coarse
    data = procrustes_residual_from_cosines(singular)
    return {
        "transport": transport,
        "gauge": gauge,
        "principal_cosines": [float(value) for value in singular],
        "actual_frobenius_residual": float(np.linalg.norm(target - reference, "fro")),
        **data,
    }
