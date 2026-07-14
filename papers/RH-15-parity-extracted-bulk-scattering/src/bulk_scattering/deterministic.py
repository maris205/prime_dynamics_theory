"""Exact physical flat-trace reconstruction and determinant factors."""

from __future__ import annotations

from functools import lru_cache
from math import comb

import numpy as np


U_CRITICAL = 1.5436890126920763615708559718017479865
R_FIXED = U_CRITICAL - 1.0
LAMBDA_FIXED = 2.0 * U_CRITICAL * R_FIXED


def _multiply(left: np.ndarray, right: np.ndarray, degree: int) -> np.ndarray:
    return np.convolve(left, right)[:degree]


def _reciprocal(values: np.ndarray, degree: int) -> np.ndarray:
    result = np.zeros(degree, dtype=np.float64)
    result[0] = 1.0 / values[0]
    for index in range(1, degree):
        result[index] = (
            -np.dot(values[1 : index + 1], result[index - 1 :: -1]) / values[0]
        )
    return result


def _square_root(values: np.ndarray, degree: int) -> np.ndarray:
    result = np.zeros(degree, dtype=np.float64)
    result[0] = np.sqrt(values[0])
    for index in range(1, degree):
        middle = np.dot(result[1:index], result[index - 1 : 0 : -1])
        result[index] = (values[index] - middle) / (2.0 * result[0])
    return result


def _circle_mean(degree: int, radius: float) -> np.ndarray:
    result = np.zeros(degree, dtype=np.float64)
    ratio = R_FIXED / radius
    for k in range((degree + 1) // 2):
        index = 2 * k
        if index < degree:
            result[index] = comb(2 * k, k) * (ratio / 2.0) ** (2 * k)
    return result


def beta_one_circle_matrix(degree: int = 120, radius: float = 0.7) -> np.ndarray:
    """Return the even beta-one Wiener--Taylor matrix of the circle lift."""

    if degree < 20:
        raise ValueError("degree must be at least twenty")
    if not R_FIXED < radius < 1.0:
        raise ValueError("radius must lie between r and one")

    one_minus_x = np.zeros(degree)
    one_minus_x[0] = 1.0
    one_minus_x[1] = -radius
    root = _square_root(one_minus_x, degree)
    inverse_square = -root / (U_CRITICAL * np.sqrt(U_CRITICAL))
    inverse_square[0] += 1.0 / U_CRITICAL

    one = np.zeros(degree)
    one[0] = 1.0
    one_minus_ut = one - U_CRITICAL * inverse_square
    two_minus_ut = one_minus_ut.copy()
    two_minus_ut[0] += 1.0
    radicand = U_CRITICAL * _multiply(
        two_minus_ut, one - inverse_square, degree
    )
    weight = 0.25 * _multiply(
        _square_root(radicand, degree),
        _reciprocal(one_minus_ut, degree),
        degree,
    )

    matrix = np.zeros((degree, degree), dtype=np.float64)
    power = np.zeros(degree)
    power[0] = 1.0
    for k in range((degree + 1) // 2):
        column = 2 * k
        if column < degree:
            matrix[:, column] = (
                2.0 * _multiply(weight, power, degree) / radius**column
            )
        power = _multiply(power, inverse_square, degree)
    return matrix


@lru_cache(maxsize=8)
def beta_one_reduced_matrix(degree: int = 120, radius: float = 0.7) -> np.ndarray:
    """Return the beta-one sector after exact removal of its Perron mode."""

    matrix = beta_one_circle_matrix(int(degree), float(radius))
    mean = _circle_mean(int(degree), float(radius))
    embedding = np.zeros((degree, degree - 1), dtype=np.float64)
    embedding[0, :] = -mean[1:]
    embedding[1:, :] = np.eye(degree - 1)
    return (matrix @ embedding)[1:, :]


def component_physical_trace(even_beta_one_trace: float, iterate: int) -> float:
    r"""Recover the physical trace of the component square.

    If ``E_{1,n}`` is the even beta-one circle trace, then

    ``p_n = E_{1,n} - lambda**(-n)/(1+lambda**(-n))``.
    """

    iterate = int(iterate)
    if iterate < 1:
        raise ValueError("iterate must be positive")
    a = LAMBDA_FIXED ** (-iterate)
    return float(even_beta_one_trace - a / (1.0 + a))


def full_even_physical_trace(even_beta_one_trace: float, iterate: int) -> float:
    r"""Return ``P_{2n}`` from ``E_{1,n}``, with the shared endpoint removed."""

    iterate = int(iterate)
    if iterate < 1:
        raise ValueError("iterate must be positive")
    a = LAMBDA_FIXED ** (-iterate)
    return float(
        2.0 * even_beta_one_trace
        - 2.0 * a / (1.0 + a)
        - a * a / (1.0 - a * a)
    )


def odd_physical_trace(length: int) -> float:
    """Return the exact odd trace, supplied only by the fixed endpoint."""

    length = int(length)
    if length < 1 or length % 2 != 1:
        raise ValueError("length must be a positive odd integer")
    a = LAMBDA_FIXED ** (-length)
    return float(a / (1.0 + a))


def physical_centered_trace(length: int, *, degree: int = 120) -> float:
    """Evaluate ``P_m-1-(-1)^m`` from the reduced circle operator."""

    length = int(length)
    if length < 1:
        raise ValueError("length must be positive")
    if length % 2:
        return odd_physical_trace(length)
    iterate = length // 2
    reduced = beta_one_reduced_matrix(degree)
    centered_sector = np.sum(np.linalg.eigvals(reduced) ** iterate).real
    trace = full_even_physical_trace(1.0 + centered_sector, iterate)
    return float(trace - 2.0)


def _regular_endpoint_logs(
    z: complex, maximum_length: int = 240
) -> tuple[complex, complex, complex]:
    """Return endpoint logarithms after extracting ``1/(1-z**2/lambda)``."""

    z = complex(z)
    w = z * z
    log_a_remainder = 0.0j
    log_b = 0.0j
    log_c = 0.0j
    for n in range(1, int(maximum_length) + 1):
        a = LAMBDA_FIXED ** (-n)
        component_correction = a / (1.0 + a)
        shared_endpoint = a * a / (1.0 - a * a)
        log_a_remainder += (component_correction - a) * w**n / n
        log_b += 0.5 * shared_endpoint * w**n / n
        if n % 2:
            log_c -= component_correction * z**n / n
    return log_a_remainder, log_b, log_c


def pole_removed_bulk_determinant(
    z: complex,
    *,
    degree: int = 120,
    maximum_length: int = 240,
) -> complex:
    r"""Evaluate ``(1-z**2/lambda) D_bulk,2(z)`` for ``|z|<lambda``."""

    z = complex(z)
    if abs(z) >= LAMBDA_FIXED:
        raise ValueError("regular endpoint series require |z| < lambda")
    reduced_values = np.linalg.eigvals(beta_one_reduced_matrix(degree))
    reduced_determinant = np.prod(1.0 - z * z * reduced_values)
    log_a_remainder, log_b, log_c = _regular_endpoint_logs(z, maximum_length)
    p_one = odd_physical_trace(1)
    return complex(
        np.exp(p_one * z + log_a_remainder + log_b + log_c)
        * reduced_determinant
    )


def bulk_determinant(
    z: complex,
    *,
    degree: int = 120,
    maximum_length: int = 240,
) -> complex:
    r"""Evaluate the exact-factorization model for the deterministic bulk.

    The formula is

    ``exp(P_1*z) * det(I-z**2*T_10) * A(z**2) * B(z**2) * C(z)``.

    It is evaluated by absolutely convergent series for ``|z|<sqrt(lambda)``.
    """

    z = complex(z)
    if abs(z) >= np.sqrt(LAMBDA_FIXED):
        raise ValueError("series evaluation requires |z| < sqrt(lambda)")
    residual = pole_removed_bulk_determinant(
        z, degree=degree, maximum_length=maximum_length
    )
    return complex(residual / (1.0 - z * z / LAMBDA_FIXED))
