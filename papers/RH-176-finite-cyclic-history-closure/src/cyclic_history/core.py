"""Exact determinant algebra for finite cyclic memory."""

from __future__ import annotations

import numpy as np


def cycle_matrix(length: int, *, direction: int = 1) -> np.ndarray:
    size = int(length)
    orientation = int(direction)
    if size < 2 or orientation not in (-1, 1):
        raise ValueError("length >= 2 and direction in {-1,1} are required")
    cycle = np.zeros((size, size), dtype=complex)
    for index in range(size):
        cycle[(index + orientation) % size, index] = 1.0
    return cycle


def zero_mean_projection(length: int) -> np.ndarray:
    size = int(length)
    if size < 2:
        raise ValueError("length must be at least two")
    constant = np.ones((size, 1), dtype=complex) / np.sqrt(size)
    return np.eye(size, dtype=complex) - constant @ constant.conj().T


def reduced_cycle_eigenvalues(length: int, *, direction: int = 1) -> np.ndarray:
    size = int(length)
    orientation = int(direction)
    if size < 2 or orientation not in (-1, 1):
        raise ValueError("invalid cycle")
    indices = np.arange(1, size)
    return np.exp(orientation * 2j * np.pi * indices / size)


def geometric_section(degree: int, value: complex) -> complex:
    order = int(degree)
    q = complex(value)
    if order < 0:
        raise ValueError("degree must be nonnegative")
    if q == 1.0:
        return complex(order + 1)
    return (1.0 - q ** (order + 1)) / (1.0 - q)


def reduced_cycle_determinant(length: int, value: complex, *, direction: int = 1) -> complex:
    roots = reduced_cycle_eigenvalues(length, direction=direction)
    return complex(np.prod(1.0 - complex(value) * roots))
