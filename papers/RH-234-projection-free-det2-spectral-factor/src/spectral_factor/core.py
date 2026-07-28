"""Projection-free finite spectral factors for the regularized determinant."""

from __future__ import annotations

import numpy as np


def det2_product(eigenvalues: np.ndarray, variable: complex) -> complex:
    values = np.asarray(eigenvalues, dtype=complex).reshape(-1)
    z = complex(variable)
    return complex(np.prod((1.0 - z * values) * np.exp(z * values)))


def det2_log_jet(eigenvalues: np.ndarray, variable: complex, maximum_order: int) -> complex:
    values = np.asarray(eigenvalues, dtype=complex).reshape(-1)
    z = complex(variable)
    order = int(maximum_order)
    if order < 2:
        raise ValueError("the det2 jet starts at order two")
    return complex(-sum(z**n * np.sum(values**n) / n for n in range(2, order + 1)))


def factorization_error(
    cloud: np.ndarray,
    complement: np.ndarray,
    variable: complex,
) -> float:
    first = np.asarray(cloud, dtype=complex).reshape(-1)
    second = np.asarray(complement, dtype=complex).reshape(-1)
    whole = det2_product(np.concatenate((first, second)), variable)
    factored = det2_product(first, variable) * det2_product(second, variable)
    return float(abs(whole - factored))
