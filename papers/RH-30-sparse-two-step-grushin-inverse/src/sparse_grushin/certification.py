"""A posteriori Frobenius--Neumann inverse certificates."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class NeumannInverseCertificate:
    """Upper bounds entering a right-inverse Neumann argument."""

    approximate_inverse_frobenius_upper: float
    residual_frobenius_upper: float
    inverse_two_norm_upper: float
    admissible: bool


def upward_add(left: float, right: float) -> float:
    """Add nonnegative binary64 bounds and round one step upward."""

    first = float(left)
    second = float(right)
    if first < 0.0 or second < 0.0 or np.isnan(first + second):
        raise ValueError("upward bounds must be nonnegative")
    return float(np.nextafter(first + second, np.inf))


def upward_multiply(left: float, right: float) -> float:
    """Multiply nonnegative binary64 bounds and round one step upward."""

    first = float(left)
    second = float(right)
    if first < 0.0 or second < 0.0 or np.isnan(first + second):
        raise ValueError("upward bounds must be nonnegative")
    return float(np.nextafter(first * second, np.inf))


def combine_frobenius_bounds(bounds) -> float:
    r"""Combine block Frobenius upper bounds by an outward Euclidean sum."""

    total = 0.0
    count = 0
    for value in bounds:
        item = float(value)
        total = upward_add(total, upward_multiply(item, item))
        count += 1
    if count == 0:
        return 0.0
    return float(np.nextafter(np.sqrt(total), np.inf))


def neumann_inverse_certificate(
    approximate_inverse_frobenius_upper: float,
    residual_frobenius_upper: float,
) -> NeumannInverseCertificate:
    r"""Certify ``||A^{-1}||_2`` from ``R`` and ``||I-AR||_F < 1``.

    The exact inequality is

    ``||A^{-1}||_2 <= ||R||_F / (1 - ||I - A R||_F)``.
    """

    inverse_upper = float(approximate_inverse_frobenius_upper)
    residual_upper = float(residual_frobenius_upper)
    if inverse_upper < 0.0 or residual_upper < 0.0:
        raise ValueError("certificate inputs must be nonnegative")
    admissible = bool(np.isfinite(inverse_upper) and residual_upper < 1.0)
    if not admissible:
        bound = float("inf")
    else:
        denominator = float(np.nextafter(1.0 - residual_upper, 0.0))
        bound = float(np.nextafter(inverse_upper / denominator, np.inf))
    return NeumannInverseCertificate(
        approximate_inverse_frobenius_upper=inverse_upper,
        residual_frobenius_upper=residual_upper,
        inverse_two_norm_upper=bound,
        admissible=admissible,
    )
