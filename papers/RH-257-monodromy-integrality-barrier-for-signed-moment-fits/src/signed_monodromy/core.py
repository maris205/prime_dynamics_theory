"""Signed finite-moment fits and their monodromy diagnostics."""

from __future__ import annotations

import numpy as np


def minimum_norm_signed_fit(matrix: np.ndarray, target: np.ndarray) -> dict[str, object]:
    shell_matrix = np.asarray(matrix, dtype=float)
    difference = np.asarray(target, dtype=float).reshape(-1)
    if shell_matrix.ndim != 2 or shell_matrix.shape[0] != difference.size:
        raise ValueError("matrix rows must match the target")
    weights, _, rank, singular = np.linalg.lstsq(shell_matrix, difference, rcond=None)
    residual = difference - shell_matrix @ weights
    return {
        "weights": weights,
        "residual": residual,
        "rank": int(rank),
        "singular_values": singular,
    }


def integer_lattice_distance(weights: np.ndarray) -> np.ndarray:
    values = np.asarray(weights, dtype=float).reshape(-1)
    return np.abs(values - np.rint(values))


def monodromy_defect(weights: np.ndarray) -> np.ndarray:
    """Return ``|exp(2 pi i w)-1|`` for real exponents."""

    values = np.asarray(weights, dtype=float).reshape(-1)
    return np.abs(np.exp(2j * np.pi * values) - 1.0)


def weighted_moment_distance(residual: np.ndarray, orders: np.ndarray) -> float:
    values = np.asarray(residual, dtype=float).reshape(-1)
    powers = np.asarray(orders, dtype=float).reshape(-1)
    if values.size != powers.size or np.any(powers <= 0.0):
        raise ValueError("residual and positive orders must match")
    return float(np.sum(np.abs(values) / powers))
