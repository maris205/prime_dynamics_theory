"""Davis--Kahan packet bounds with an explicit approximate-gap gate."""

from __future__ import annotations

import math

import numpy as np


def projector_enclosure(approximate_gap: float, operator_radius: float) -> dict[str, float | bool | None]:
    """Certify a top-cluster projector from an approximate spectral gap.

    The gate gap > 2*radius prevents eigenvalue crossing.  Under the gate,
    radius/(gap-radius) bounds the largest principal-angle sine.
    """
    gap = float(approximate_gap)
    radius = float(operator_radius)
    if not math.isfinite(gap) or not math.isfinite(radius) or gap < 0.0 or radius < 0.0:
        raise ValueError("gap and radius must be finite and nonnegative")
    stable = bool(gap > 2.0 * radius)
    if not stable:
        return {"stable": False, "gap_margin": gap - 2.0 * radius, "projector_radius": None, "frame_radius": None}
    sine = min(1.0, radius / (gap - radius))
    return {
        "stable": True,
        "gap_margin": gap - 2.0 * radius,
        "projector_radius": sine,
        "frame_radius": aligned_frame_radius(sine),
    }


def aligned_frame_radius(projector_radius: float) -> float:
    """Operator distance after canonical polar alignment of equal-rank frames."""
    sine = float(projector_radius)
    if not math.isfinite(sine) or sine < 0.0 or sine > 1.0:
        raise ValueError("projector radius must lie in [0,1]")
    return math.sqrt(max(0.0, 2.0 - 2.0 * math.sqrt(max(0.0, 1.0 - sine * sine))))


def top_projector(matrix: np.ndarray, rank: int) -> np.ndarray:
    """Orthogonal projector onto the top rank eigenvectors of a Hermitian matrix."""
    values = np.asarray(matrix, dtype=float)
    width = int(rank)
    if values.ndim != 2 or values.shape[0] != values.shape[1] or width <= 0 or width >= values.shape[0]:
        raise ValueError("invalid matrix or projector rank")
    eigenvalues, eigenvectors = np.linalg.eigh((values + values.T) / 2.0)
    frame = eigenvectors[:, np.argsort(eigenvalues)[-width:]]
    return frame @ frame.T

