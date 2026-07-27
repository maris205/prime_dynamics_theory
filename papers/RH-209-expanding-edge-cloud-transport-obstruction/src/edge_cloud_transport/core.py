"""Subspace transport for growing outer spectral clouds."""

from __future__ import annotations

import math

import numpy as np


def ordered_edge_indices(values: np.ndarray, rank: int) -> np.ndarray:
    spectrum = np.asarray(values, dtype=complex).reshape(-1)
    count = int(rank)
    if count < 1 or count > spectrum.size:
        raise ValueError("rank is outside the spectrum")
    return np.argsort(-np.abs(spectrum))[:count]


def cloud_transport_data(
    coarse_frame: np.ndarray, fine_frame: np.ndarray, embedding: np.ndarray
) -> dict[str, object]:
    coarse = np.asarray(coarse_frame, dtype=complex)
    fine = np.asarray(fine_frame, dtype=complex)
    lift = np.asarray(embedding, dtype=complex)
    if coarse.ndim != 2 or fine.ndim != 2 or coarse.shape[1] != fine.shape[1]:
        raise ValueError("equal-rank frames are required")
    coarse_basis = np.linalg.qr(lift @ coarse, mode="reduced")[0]
    fine_basis = np.linalg.qr(fine, mode="reduced")[0]
    singular = np.clip(np.linalg.svd(coarse_basis.conj().T @ fine_basis, compute_uv=False), 0.0, 1.0)
    minimum = float(singular[-1])
    return {
        "principal_cosines": [float(value) for value in singular],
        "mean_principal_cosine": float(np.mean(singular)),
        "minimum_principal_cosine": minimum,
        "maximum_principal_sine": float(math.sqrt(max(0.0, 1.0 - minimum**2))),
    }
