"""Semidefinite relative pencils without artificial positive floors."""

from __future__ import annotations

import math
import numpy as np


def _symmetric(matrix: np.ndarray, name: str) -> np.ndarray:
    value = np.asarray(matrix, dtype=float)
    if value.ndim != 2 or value.shape[0] != value.shape[1] or np.any(~np.isfinite(value)):
        raise ValueError(f"{name} must be a finite square matrix")
    return (value + value.T) / 2.0


def fp_supported_rank(action: np.ndarray, multiplier: float = 128.0) -> dict[str, object]:
    """Return the directions separated from a conservative fp64 noise scale.

    This is a conditioning diagnostic, not a claim that the input action is
    itself an enclosure of an infinite-dimensional operator.
    """
    value = np.asarray(action, dtype=float)
    if value.ndim != 2 or value.shape[1] == 0 or np.any(~np.isfinite(value)):
        raise ValueError("action must be a finite nonempty matrix")
    factor = float(multiplier)
    if not math.isfinite(factor) or factor <= 0.0:
        raise ValueError("multiplier must be positive")
    singular = np.linalg.svd(value, compute_uv=False)
    scale = float(singular[0]) if singular.size else 0.0
    radius = factor * np.finfo(float).eps * max(value.shape) * scale
    rank = int(np.sum(singular > radius))
    return {
        "rank": rank,
        "radius": radius,
        "singular_values": singular,
        "minimum_certified_margin": float(singular[rank - 1] - radius) if rank else 0.0,
        "first_uncertified_margin": float(singular[rank] - radius) if rank < singular.size else None,
    }


def support_restricted_rayleigh(
    gram: np.ndarray,
    tail: np.ndarray,
    *,
    tolerance: float | None = None,
) -> dict[str, object]:
    """Analyze ``D <= gamma^2 G`` on ``ran(G)`` and on the full space.

    The full-space quotient is finite exactly when the tail annihilates the
    numerical kernel selected by ``tolerance``.  The returned support
    spectrum is the ordinary spectrum of the compressed relative pencil.
    """
    g = _symmetric(gram, "gram")
    d = _symmetric(tail, "tail")
    values, vectors = np.linalg.eigh(g)
    scale = max(float(abs(values[-1])), np.finfo(float).tiny)
    tol = float(tolerance) if tolerance is not None else 128.0 * np.finfo(float).eps * g.shape[0] * scale
    if not math.isfinite(tol) or tol < 0.0:
        raise ValueError("tolerance must be finite and nonnegative")
    support = values > tol
    basis = vectors[:, support]
    kernel = vectors[:, ~support]
    if basis.shape[1]:
        compressed_tail = basis.T @ d @ basis
        inverse = np.diag(values[support] ** -0.5)
        relative = inverse @ compressed_tail @ inverse
        relative = (relative + relative.T) / 2.0
        spectrum = np.linalg.eigvalsh(relative)
        gamma = math.sqrt(max(0.0, float(spectrum[-1])))
    else:
        spectrum = np.empty(0)
        gamma = 0.0
    kernel_tail_norm = float(np.linalg.norm(d @ kernel, 2)) if kernel.shape[1] else 0.0
    tail_scale = max(float(np.linalg.norm(d, 2)), np.finfo(float).tiny)
    compatible = kernel_tail_norm <= 128.0 * np.finfo(float).eps * d.shape[0] * tail_scale
    return {
        "support_rank": int(basis.shape[1]),
        "support_spectrum": spectrum,
        "support_gamma": gamma,
        "kernel_tail_norm": kernel_tail_norm,
        "kernel_compatible": compatible,
        "full_space_gamma": gamma if compatible else math.inf,
        "tolerance": tol,
    }


def floor_distortion(eigenvalues: np.ndarray, floor: float) -> dict[str, float]:
    """Quantify how much ``G + floor I`` changes the weak spectrum."""
    values = np.asarray(eigenvalues, dtype=float)
    shift = float(floor)
    if values.ndim != 1 or values.size == 0 or np.any(~np.isfinite(values)):
        raise ValueError("eigenvalues must be a finite nonempty vector")
    if not math.isfinite(shift) or shift < 0.0:
        raise ValueError("floor must be finite and nonnegative")
    positive = values[values > 0.0]
    weakest = float(np.min(positive)) if positive.size else 0.0
    ratio = math.inf if weakest == 0.0 and shift > 0.0 else (weakest + shift) / weakest if weakest else 1.0
    return {
        "weakest_positive_eigenvalue": weakest,
        "floor_to_weakest_ratio": shift / weakest if weakest else math.inf,
        "weak_eigenvalue_inflation": ratio,
    }
