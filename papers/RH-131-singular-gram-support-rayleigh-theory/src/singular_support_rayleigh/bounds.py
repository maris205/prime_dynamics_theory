"""Kernel compatibility, pseudodeterminants, and outward support bounds."""

from __future__ import annotations

import math
import numpy as np


def _sym(matrix: np.ndarray, name: str) -> np.ndarray:
    value = np.asarray(matrix, dtype=float)
    if value.ndim != 2 or value.shape[0] != value.shape[1] or np.any(~np.isfinite(value)):
        raise ValueError(f"{name} must be a finite square matrix")
    return (value + value.T) / 2.0


def _radius(value: float, name: str) -> float:
    radius = float(value)
    if not math.isfinite(radius) or radius < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return radius


def support_rayleigh_constant(
    gram: np.ndarray,
    tail: np.ndarray,
    *,
    support_tolerance: float | None = None,
    compatibility_tolerance: float | None = None,
) -> dict[str, object]:
    """Return the exact compressed quotient and the full-space obstruction.

    ``support_tolerance`` selects the positive spectrum of ``gram``.  The
    full-space quotient is finite precisely when ``tail`` annihilates the
    selected kernel, up to ``compatibility_tolerance``.
    """
    g = _sym(gram, "gram")
    d = _sym(tail, "tail")
    values, vectors = np.linalg.eigh(g)
    scale = max(float(np.linalg.norm(g, 2)), np.finfo(float).tiny)
    tol = (
        256.0 * np.finfo(float).eps * g.shape[0] * scale
        if support_tolerance is None
        else float(support_tolerance)
    )
    if not math.isfinite(tol) or tol < 0.0:
        raise ValueError("support tolerance must be finite and nonnegative")
    if values[0] < -tol:
        raise ValueError("gram must be positive semidefinite at the declared tolerance")
    mask = values > tol
    basis = vectors[:, mask]
    kernel = vectors[:, ~mask]
    positive = values[mask]
    if positive.size:
        compressed = basis.T @ d @ basis
        inverse = np.diag(positive**-0.5)
        relative = inverse @ compressed @ inverse
        relative = (relative + relative.T) / 2.0
        spectrum = np.linalg.eigvalsh(relative)
        relative_tolerance = 256.0 * np.finfo(float).eps * max(1.0, float(np.linalg.norm(relative, 2)))
        if spectrum[0] < -relative_tolerance:
            raise ValueError("tail must be positive semidefinite on the Gram support")
        spectrum = np.maximum(spectrum, 0.0)
        gamma_squared = float(spectrum[-1])
        pseudodeterminant = float(np.prod(positive))
    else:
        spectrum = np.empty(0)
        gamma_squared = 0.0
        pseudodeterminant = 1.0
    leakage = float(np.linalg.norm(d @ kernel, 2)) if kernel.shape[1] else 0.0
    dscale = max(float(np.linalg.norm(d, 2)), np.finfo(float).tiny)
    compat_tol = (
        256.0 * np.finfo(float).eps * d.shape[0] * dscale
        if compatibility_tolerance is None
        else float(compatibility_tolerance)
    )
    if not math.isfinite(compat_tol) or compat_tol < 0.0:
        raise ValueError("compatibility tolerance must be finite and nonnegative")
    compatible = leakage <= compat_tol
    gamma = math.sqrt(max(0.0, gamma_squared))
    return {
        "support_rank": int(positive.size),
        "support_basis": basis,
        "kernel_basis": kernel,
        "positive_gram_eigenvalues": positive,
        "relative_spectrum": spectrum,
        "support_gamma_squared": gamma_squared,
        "support_gamma": gamma,
        "pseudodeterminant": pseudodeterminant,
        "pseudovolume": math.sqrt(pseudodeterminant),
        "kernel_leakage_norm": leakage,
        "kernel_compatible": compatible,
        "full_space_gamma": gamma if compatible else math.inf,
        "support_tolerance": tol,
        "compatibility_tolerance": compat_tol,
    }


def support_volume_lower(pseudovolume: float, gamma: float, rank: int) -> float:
    """Return the sharp ``(1-gamma)^rank`` supported-volume lower bound."""
    volume = float(pseudovolume)
    relative = float(gamma)
    degree = int(rank)
    if not math.isfinite(volume) or volume < 0.0:
        raise ValueError("pseudovolume must be finite and nonnegative")
    if not math.isfinite(relative) or relative < 0.0:
        raise ValueError("gamma must be finite and nonnegative")
    if degree < 0:
        raise ValueError("rank must be nonnegative")
    return max(0.0, 1.0 - relative) ** degree * volume


def outward_support_rayleigh_upper(
    gram_hat: np.ndarray,
    tail_hat: np.ndarray,
    support_basis: np.ndarray,
    gram_radius: float,
    tail_radius: float,
) -> dict[str, float]:
    """Certify a support quotient from independent spectral-norm radii."""
    g = _sym(gram_hat, "gram approximation")
    d = _sym(tail_hat, "tail approximation")
    basis = np.asarray(support_basis, dtype=float)
    if basis.ndim != 2 or basis.shape[0] != g.shape[0] or basis.shape[1] == 0:
        raise ValueError("support basis has incompatible shape")
    orthogonality = float(np.linalg.norm(basis.T @ basis - np.eye(basis.shape[1]), 2))
    if orthogonality > 1e-9:
        raise ValueError("support basis must be orthonormal")
    rg = _radius(gram_radius, "gram radius")
    rd = _radius(tail_radius, "tail radius")
    gp = (basis.T @ g @ basis + basis.T @ g.T @ basis) / 2.0
    dp = (basis.T @ d @ basis + basis.T @ d.T @ basis) / 2.0
    values, vectors = np.linalg.eigh(gp)
    minimum_hat = float(values[0])
    exact_lower = minimum_hat - rg
    if exact_lower <= 0.0:
        raise ValueError("the support is not separated from the Gram radius")
    inverse = (vectors * values**-0.5) @ vectors.T
    relative = inverse @ dp @ inverse
    relative = (relative + relative.T) / 2.0
    numerical = max(0.0, float(np.linalg.eigvalsh(relative)[-1]))
    additive_guard = (rd + numerical * rg) / exact_lower
    return {
        "numerical_gamma_squared": numerical,
        "outward_gamma_squared_upper": numerical + additive_guard,
        "outward_gamma_upper": math.sqrt(numerical + additive_guard),
        "minimum_gram_eigenvalue_hat": minimum_hat,
        "exact_support_lower": exact_lower,
        "additive_radius_guard": additive_guard,
    }
