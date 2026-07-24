"""Finite-dimensional forms of the normalized-snapshot enclosure theorem."""

from __future__ import annotations

import math

import numpy as np


def normalized_snapshot(state: np.ndarray) -> np.ndarray:
    """Return S* S / ||S||_F^2 for a nonzero finite matrix S."""
    matrix = np.asarray(state, dtype=float)
    if matrix.ndim != 2 or np.any(~np.isfinite(matrix)):
        raise ValueError("state must be a finite matrix")
    scale = float(np.sum(matrix * matrix))
    if scale <= 0.0:
        raise ValueError("state must be nonzero")
    gram = matrix.T @ matrix / scale
    return (gram + gram.T) / 2.0


def snapshot_bounds(error_norm: float, source_norm: float, approximant_norm: float | None = None) -> dict[str, float]:
    """Sharp universal bounds from a Hilbert--Schmidt perturbation.

    If both endpoint norms are known, the smaller relative radius is used.
    The returned operator, Frobenius and trace bounds are respectively
    delta, sqrt(2) delta and 2 delta, capped at their global state-space
    diameters.
    """
    error = float(error_norm)
    source = float(source_norm)
    approximate = source if approximant_norm is None else float(approximant_norm)
    if not all(math.isfinite(value) for value in (error, source, approximate)):
        raise ValueError("norms must be finite")
    if error < 0.0 or source <= 0.0 or approximate <= 0.0:
        raise ValueError("error must be nonnegative and endpoint norms positive")
    delta = min(1.0, error / max(source, approximate))
    return {
        "relative_radius": delta,
        "operator_radius": delta,
        "frobenius_radius": math.sqrt(2.0) * delta,
        "trace_radius": 2.0 * delta,
    }


def svd_split_bounds(residual_fraction: float) -> dict[str, float]:
    """Bounds for an exact orthogonal singular-value truncation.

    residual_fraction is ||R||_F / ||S||_F for an orthogonal singular split:
    both the left and right singular supports of H and R are disjoint.
    """
    q = float(residual_fraction)
    if not math.isfinite(q) or q < 0.0 or q > 1.0:
        raise ValueError("residual fraction must lie in [0,1]")
    squared = q * q
    return {
        "operator_radius": squared,
        "frobenius_radius": math.sqrt(2.0) * squared,
        "trace_radius": 2.0 * squared,
    }


def sharp_witness(delta: float) -> tuple[np.ndarray, np.ndarray]:
    """One-row matrices attaining all three universal constants."""
    value = float(delta)
    if not math.isfinite(value) or not 0.0 <= value < 1.0:
        raise ValueError("delta must lie in [0,1)")
    root = math.sqrt(1.0 - value * value)
    approximant = np.array([[1.0, 0.0]])
    source = np.array([[1.0 - value * value, value * root]])
    return source, approximant
