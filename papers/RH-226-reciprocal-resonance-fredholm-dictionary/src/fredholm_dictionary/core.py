"""Finite resonance-polynomial and Fredholm-product identities."""

from __future__ import annotations

import numpy as np


def characteristic_value(resonances: np.ndarray, spectral_value: complex) -> complex:
    values = np.asarray(resonances, dtype=complex).reshape(-1)
    return complex(np.prod(complex(spectral_value) - values))


def fredholm_product(resonances: np.ndarray, variable: complex) -> complex:
    values = np.asarray(resonances, dtype=complex).reshape(-1)
    return complex(np.prod(1.0 - complex(variable) * values))


def regularized_fredholm_product(resonances: np.ndarray, variable: complex) -> complex:
    values = np.asarray(resonances, dtype=complex).reshape(-1)
    z = complex(variable)
    return complex(np.prod((1.0 - z * values) * np.exp(z * values)))


def reciprocal_zeros(resonances: np.ndarray) -> np.ndarray:
    values = np.asarray(resonances, dtype=complex).reshape(-1)
    if np.min(np.abs(values)) <= np.finfo(float).tiny:
        raise ValueError("zero resonance")
    return 1.0 / values


def reciprocal_polynomial_identity_error(resonances: np.ndarray, variable: complex) -> float:
    values = np.asarray(resonances, dtype=complex).reshape(-1)
    z = complex(variable)
    if z == 0.0:
        return 0.0
    left = fredholm_product(values, z)
    right = z**values.size * characteristic_value(values, 1.0 / z)
    return float(abs(left - right))
