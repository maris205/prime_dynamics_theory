"""High-precision boundary ladder for the quadratic band-merging map."""

from __future__ import annotations

from functools import lru_cache

import mpmath as mp
import numpy as np


U_CRITICAL = 1.5436890126920763615708559718017479865
R_FIXED = U_CRITICAL - 1.0
LAMBDA_FIXED = 2.0 * U_CRITICAL * R_FIXED
CONTRACTION_FIXED = LAMBDA_FIXED**-2


@lru_cache(maxsize=12)
def _boundary_clearance_tuple(count: int, decimal_digits: int) -> tuple[float, ...]:
    count = int(count)
    decimal_digits = int(decimal_digits)
    if count < 1:
        raise ValueError("count must be positive")
    if decimal_digits < 50:
        raise ValueError("decimal_digits must be at least fifty")

    with mp.workdps(decimal_digits):
        u = mp.findroot(
            lambda value: value**3 - 2 * value**2 + 2 * value - 2,
            (mp.mpf("1.5"), mp.mpf("1.6")),
        )

        def positive(value: mp.mpf) -> mp.mpf:
            return mp.sqrt((1 - value) / u)

        def h_map(value: mp.mpf) -> mp.mpf:
            return positive(positive(value))

        def q_map(value: mp.mpf) -> mp.mpf:
            return positive(-positive(value))

        tolerance = mp.power(10, -(decimal_digits - 15))
        clearances: list[float] = []
        for index in range(1, count + 1):

            def inverse_composition(value: mp.mpf) -> mp.mpf:
                for _ in range(index - 1):
                    value = h_map(value)
                return q_map(value)

            point = mp.mpf(1)
            for _ in range(600):
                updated = inverse_composition(point)
                if abs(updated - point) <= tolerance:
                    point = updated
                    break
                point = updated
            else:
                raise RuntimeError(f"boundary fixed-point iteration failed at k={index}")
            clearances.append(float(1 - point))

    return tuple(clearances)


def boundary_clearances(
    count: int = 80, *, decimal_digits: int = 100
) -> np.ndarray:
    r"""Return ``delta_k = 1-p_{2k}`` for the distinguished boundary cycles."""

    return np.asarray(
        _boundary_clearance_tuple(int(count), int(decimal_digits)),
        dtype=np.float64,
    )


def scaled_boundary_constants(clearances: np.ndarray) -> np.ndarray:
    r"""Return ``delta_k lambda^(2k)`` along a supplied boundary ladder."""

    values = np.asarray(clearances, dtype=np.float64)
    indices = np.arange(1, values.size + 1, dtype=np.float64)
    return values * LAMBDA_FIXED ** (2.0 * indices)


def boundary_ratios(clearances: np.ndarray) -> np.ndarray:
    """Return successive clearance ratios ``delta_(k+1)/delta_k``."""

    values = np.asarray(clearances, dtype=np.float64)
    if values.size < 2:
        return np.asarray([], dtype=np.float64)
    return values[1:] / values[:-1]
