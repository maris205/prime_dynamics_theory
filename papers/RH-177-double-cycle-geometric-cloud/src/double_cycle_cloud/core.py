"""Exact determinant and trace formulas for the doubled cyclic cloud."""

from __future__ import annotations

import cmath

import numpy as np


DEFAULT_LAMBDA = 1.6785735104283224


def geometric_section(degree: int, value: complex) -> complex:
    order = int(degree)
    q = complex(value)
    if order < 0:
        raise ValueError("degree must be nonnegative")
    if q == 1.0:
        return complex(order + 1)
    return (1.0 - q ** (order + 1)) / (1.0 - q)


def cloud_factor(degree: int, spectral_parameter: complex, *, pole: float = DEFAULT_LAMBDA) -> complex:
    return geometric_section(degree, complex(spectral_parameter) / float(pole)) ** 2


def double_cycle_eigenvalues(degree: int, *, pole: float = DEFAULT_LAMBDA) -> np.ndarray:
    order = int(degree)
    if order < 1 or float(pole) <= 0.0:
        raise ValueError("positive degree and pole are required")
    length = order + 1
    roots = np.exp(2j * np.pi * np.arange(1, length) / length) / float(pole)
    return np.concatenate([roots, roots])


def double_cycle_determinant(degree: int, spectral_parameter: complex, *, pole: float = DEFAULT_LAMBDA) -> complex:
    eigenvalues = double_cycle_eigenvalues(degree, pole=pole)
    return complex(np.prod(1.0 - complex(spectral_parameter) * eigenvalues))


def double_cycle_trace(degree: int, power: int, *, pole: float = DEFAULT_LAMBDA) -> complex:
    order = int(degree)
    exponent = int(power)
    if order < 1 or exponent < 1:
        raise ValueError("degree and power must be positive")
    length = order + 1
    reduced_trace = order if exponent % length == 0 else -1
    return complex(2.0 * reduced_trace / float(pole) ** exponent)


def scaled_geometric_profile(degree: int, coordinate: complex) -> complex:
    order = int(degree)
    if order < 1:
        raise ValueError("degree must be positive")
    q = cmath.exp(complex(coordinate) / (order + 1))
    return geometric_section(order, q) / (order + 1)
