"""Best identity-gauge constants and a sharp coordinate obstruction."""

from __future__ import annotations

import math
import numpy as np


def _spd(matrix: np.ndarray, name: str) -> np.ndarray:
    value = np.asarray(matrix, dtype=float)
    if value.ndim != 2 or value.shape[0] != value.shape[1] or np.any(~np.isfinite(value)):
        raise ValueError(f"{name} must be a finite square matrix")
    value = (value + value.T) / 2.0
    if np.linalg.eigvalsh(value)[0] <= 0.0:
        raise ValueError(f"{name} must be positive definite")
    return value


def _inverse_root(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(matrix)
    return (vectors * values**-0.5) @ vectors.T


def _gamma(gram: np.ndarray, tail: np.ndarray) -> float:
    inverse = _inverse_root(gram)
    return math.sqrt(float(np.linalg.eigvalsh(inverse @ tail @ inverse)[-1]))


def fixed_coordinate_constants(
    source_gram: np.ndarray,
    source_tail: np.ndarray,
    target_gram: np.ndarray,
    target_tail: np.ndarray,
) -> dict[str, float]:
    """Return the sharp constants for the identity-gauge RH-120 theorem."""
    g = _spd(source_gram, "source gram")
    d = _spd(source_tail, "source tail")
    gp = _spd(target_gram, "target gram")
    dp = _spd(target_tail, "target tail")
    gi = _inverse_root(g)
    di = _inverse_root(d)
    a = float(np.linalg.eigvalsh(gi @ gp @ gi)[0])
    b = float(np.linalg.eigvalsh(di @ dp @ di)[-1])
    source_gamma = _gamma(g, d)
    target_gamma = _gamma(gp, dp)
    factor = math.sqrt(b / a)
    return {
        "gram_lower_factor": a,
        "tail_upper_factor": b,
        "fixed_transfer_factor": factor,
        "source_gamma": source_gamma,
        "target_gamma": target_gamma,
        "fixed_gamma_upper": factor * source_gamma,
    }


def swap_obstruction_family(epsilon: float, gamma: float = 0.2) -> dict[str, object]:
    """Return the four-dimensional swapped-axis obstruction."""
    eps = float(epsilon)
    rayleigh = float(gamma)
    if not math.isfinite(eps) or not 0.0 < eps <= 1.0:
        raise ValueError("epsilon must lie in (0,1]")
    if not math.isfinite(rayleigh) or rayleigh <= 0.0:
        raise ValueError("gamma must be finite and positive")
    g = np.diag([eps, 1.0, 2.0, 3.0])
    permutation = np.eye(4)[[1, 0, 2, 3]]
    gp = permutation.T @ g @ permutation
    d = rayleigh**2 * g
    dp = rayleigh**2 * gp
    constants = fixed_coordinate_constants(g, d, gp, dp)
    constants.update({
        "epsilon": eps,
        "source_gram": g,
        "target_gram": gp,
        "source_tail": d,
        "target_tail": dp,
        "exact_gauge": permutation,
        "gauged_transfer_factor": 1.0,
    })
    return constants

