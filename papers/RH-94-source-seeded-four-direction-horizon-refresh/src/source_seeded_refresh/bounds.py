"""Finite-dimensional source-seed and packet diagnostics for RH-94."""

from __future__ import annotations

import math

import numpy as np


def normalized_source_gram(source: np.ndarray) -> np.ndarray:
    values = np.asarray(source, dtype=float)
    if values.ndim != 2 or values.size == 0:
        raise ValueError("source must be a nonempty matrix")
    gram = values.T @ values
    scale = float(np.trace(gram))
    if not math.isfinite(scale) or scale <= 0.0:
        raise ValueError("source must have positive Frobenius norm")
    return (gram / scale + (gram / scale).T) / 2.0


def source_right_packet(source: np.ndarray, rank: int) -> np.ndarray:
    values = np.asarray(source, dtype=float)
    width = int(rank)
    if values.ndim != 2 or width <= 0 or width > min(values.shape):
        raise ValueError("invalid source packet rank")
    _, _, right = np.linalg.svd(values, full_matrices=False)
    return right[:width].T


def top_gram_packet(gram: np.ndarray, rank: int) -> np.ndarray:
    values = np.asarray(gram, dtype=float)
    width = int(rank)
    if values.ndim != 2 or values.shape[0] != values.shape[1] or width <= 0 or width > values.shape[0]:
        raise ValueError("invalid Gram packet rank")
    eigenvalues, eigenvectors = np.linalg.eigh((values + values.T) / 2.0)
    return eigenvectors[:, np.argsort(eigenvalues)[-width:]]


def projector_distance(first: np.ndarray, second: np.ndarray) -> float:
    left = np.asarray(first, dtype=float)
    right = np.asarray(second, dtype=float)
    if left.ndim != 2 or right.ndim != 2 or left.shape != right.shape:
        raise ValueError("packets must have the same shape")
    return float(np.linalg.norm(left @ left.T - right @ right.T, 2))


def orthogonality_defect(packet: np.ndarray) -> float:
    values = np.asarray(packet, dtype=float)
    if values.ndim != 2 or values.shape[1] == 0:
        raise ValueError("packet must be a nonempty matrix")
    return float(np.linalg.norm(values.T @ values - np.eye(values.shape[1]), 2))


def cross_energy_fraction(singular_values: np.ndarray, width: int) -> float:
    singular = np.asarray(singular_values, dtype=float)
    selected = int(width)
    if singular.ndim != 1 or singular.size == 0 or selected <= 0 or selected > singular.size or np.any(singular < 0.0):
        raise ValueError("invalid singular-value data")
    total = float(singular @ singular)
    if total == 0.0:
        return 1.0
    return math.nextafter(float(singular[:selected] @ singular[:selected] / total), -math.inf)
