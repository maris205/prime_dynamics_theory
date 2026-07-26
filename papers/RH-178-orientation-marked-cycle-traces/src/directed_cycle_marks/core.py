"""Directed marker identities for forward and reverse finite cycles."""

from __future__ import annotations

import numpy as np


def cycle_matrix(length: int, direction: int = 1) -> np.ndarray:
    size = int(length)
    orientation = int(direction)
    if size < 3 or orientation not in (-1, 1):
        raise ValueError("length >= 3 and direction +/-1 are required")
    cycle = np.zeros((size, size), dtype=complex)
    for index in range(size):
        cycle[(index + orientation) % size, index] = 1.0
    return cycle


def zero_mean_projection(length: int) -> np.ndarray:
    size = int(length)
    constant = np.ones((size, 1), dtype=complex) / np.sqrt(size)
    return np.eye(size, dtype=complex) - constant @ constant.conj().T


def edge_marker(length: int) -> np.ndarray:
    size = int(length)
    if size < 3:
        raise ValueError("length must be at least three")
    marker = np.zeros((size, size), dtype=complex)
    marker[0, 1] = 1.0
    return marker


def ordinary_cycle_trace(length: int, power: int, direction: int = 1) -> complex:
    cycle = cycle_matrix(length, direction)
    return complex(np.trace(np.linalg.matrix_power(cycle, int(power))))


def reduced_marked_trace(length: int, power: int, direction: int = 1) -> complex:
    cycle = cycle_matrix(length, direction)
    projection = zero_mean_projection(length)
    marker = projection @ edge_marker(length) @ projection
    return complex(np.trace(marker @ np.linalg.matrix_power(cycle, int(power))))


def marked_power_stability_bound(
    marker_trace_norm: float,
    power: int,
    common_norm_bound: float,
    perturbation_norm: float,
) -> float:
    exponent = int(power)
    if exponent < 1 or min(marker_trace_norm, common_norm_bound, perturbation_norm) < 0.0:
        raise ValueError("invalid stability parameters")
    return float(marker_trace_norm) * exponent * float(common_norm_bound) ** (exponent - 1) * float(perturbation_norm)
