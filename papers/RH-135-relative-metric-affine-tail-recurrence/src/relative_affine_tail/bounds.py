"""Metric amplification and contraction/forcing optimization."""

from __future__ import annotations

import math
import numpy as np


def _positive(matrix: np.ndarray, name: str) -> np.ndarray:
    value = np.asarray(matrix, dtype=float)
    if value.ndim != 2 or value.shape[0] != value.shape[1] or np.any(~np.isfinite(value)):
        raise ValueError(f"{name} must be a finite square matrix")
    value = (value + value.T) / 2.0
    if np.linalg.eigvalsh(value)[0] <= 0.0:
        raise ValueError(f"{name} must be positive definite")
    return value


def _psd(matrix: np.ndarray, name: str) -> np.ndarray:
    value = np.asarray(matrix, dtype=float)
    if value.ndim != 2 or value.shape[0] != value.shape[1] or np.any(~np.isfinite(value)):
        raise ValueError(f"{name} must be a finite square matrix")
    value = (value + value.T) / 2.0
    tolerance = 256.0 * np.finfo(float).eps * max(1.0, float(np.linalg.norm(value, 2)))
    if np.linalg.eigvalsh(value)[0] < -tolerance:
        raise ValueError(f"{name} must be positive semidefinite")
    return value


def _generalized_max(metric: np.ndarray, operator: np.ndarray) -> float:
    values, vectors = np.linalg.eigh(metric)
    inverse = (vectors * values**-0.5) @ vectors.T
    relative = inverse @ operator @ inverse
    return max(0.0, float(np.linalg.eigvalsh((relative + relative.T) / 2.0)[-1]))


def relative_affine_coefficients(
    source_gram: np.ndarray,
    target_gram: np.ndarray,
    target_to_source: np.ndarray,
    raw_multiplicative_factor: float,
    forcing: np.ndarray,
) -> dict[str, float]:
    """Convert ``D' <= r O.T D O + F`` into a scalar gamma recurrence."""
    source = _positive(source_gram, "source gram")
    target = _positive(target_gram, "target gram")
    positive_forcing = _psd(forcing, "forcing")
    orthogonal = np.asarray(target_to_source, dtype=float)
    factor = float(raw_multiplicative_factor)
    if source.shape != target.shape or positive_forcing.shape != source.shape or orthogonal.shape != source.shape:
        raise ValueError("all reduced matrices must have the same shape")
    if np.linalg.norm(orthogonal.T @ orthogonal - np.eye(source.shape[0]), 2) > 1e-9:
        raise ValueError("target-to-source map must be orthogonal")
    if not math.isfinite(factor) or factor < 0.0:
        raise ValueError("raw factor must be finite and nonnegative")
    metric_factor = _generalized_max(target, orthogonal.T @ source @ orthogonal)
    forcing_factor = _generalized_max(target, positive_forcing)
    return {
        "metric_factor": metric_factor,
        "rho": factor * metric_factor,
        "q": forcing_factor,
    }


def optimize_fixed_floor(metric_decay: float, frame_forcing_base: float, birth_forcing: float, grid_size: int = 2048) -> dict[str, float | bool | None]:
    """Minimize ``q(tau)/(1-rho(tau))`` over contractive ``tau``.

    Here ``rho=A(1+tau)`` and
    ``q=q_birth+B(1+1/tau)``.
    """
    a = float(metric_decay)
    b = float(frame_forcing_base)
    c = float(birth_forcing)
    count = int(grid_size)
    if any(not math.isfinite(value) or value < 0.0 for value in (a, b, c)):
        raise ValueError("coefficients must be finite and nonnegative")
    if count < 16:
        raise ValueError("grid size is too small")
    if a >= 1.0:
        return {"contractive_feasible": False, "tau": None, "rho": a, "q": math.inf, "fixed_floor": math.inf}
    upper = math.inf if a == 0.0 else 1.0 / a - 1.0
    if math.isinf(upper):
        upper = 1e8
    safe_upper = max(1e-12, upper * (1.0 - 1e-10))
    lower = min(1e-8, safe_upper * 1e-6)
    taus = np.geomspace(max(lower, 1e-14), safe_upper, count)
    rho = a * (1.0 + taus)
    q = c + b * (1.0 + 1.0 / taus)
    floors = q / np.maximum(1.0 - rho, np.finfo(float).tiny)
    index = int(np.argmin(floors))
    return {
        "contractive_feasible": True,
        "tau": float(taus[index]),
        "rho": float(rho[index]),
        "q": float(q[index]),
        "fixed_floor": float(floors[index]),
    }
