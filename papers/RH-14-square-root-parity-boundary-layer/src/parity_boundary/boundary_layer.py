"""Deterministic component density and the two universal boundary layers."""

from __future__ import annotations

from dataclasses import dataclass
from math import comb

import numpy as np
from scipy.integrate import quad
from scipy.linalg import eig
from scipy.special import erf, erfc, ndtr

from .operators import LAMBDA_FIXED, R_FIXED, U_CRITICAL


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
    for k in range((degree + 1) // 2):
        index = 2 * k
        if index < degree:
            result[index] = comb(2 * k, k) * (R_FIXED / (2.0 * radius)) ** (2 * k)
    return result


def beta_one_circle_matrix(degree: int = 120, radius: float = 0.7) -> np.ndarray:
    """Return the Wiener--Taylor matrix for the even beta-one circle sector."""

    if degree < 20:
        raise ValueError("degree must be at least twenty")
    if not R_FIXED < radius < 1.0:
        raise ValueError("radius must lie between r and one")

    one_minus_x = np.zeros(degree)
    one_minus_x[0] = 1.0
    one_minus_x[1] = -radius
    root = _square_root(one_minus_x, degree)
    t = -root / (U_CRITICAL * np.sqrt(U_CRITICAL))
    t[0] += 1.0 / U_CRITICAL

    one = np.zeros(degree)
    one[0] = 1.0
    one_minus_ut = one - U_CRITICAL * t
    two_minus_ut = one_minus_ut.copy()
    two_minus_ut[0] += 1.0
    radicand = U_CRITICAL * _multiply(two_minus_ut, one - t, degree)
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
        power = _multiply(power, t, degree)
    return matrix


@dataclass(frozen=True)
class ComponentDensity:
    """Normalized analytic factor and central density value."""

    coefficients: np.ndarray
    radius: float
    eigenvalue: float
    analytic_value_at_zero: float
    interval_density_at_zero: float


def component_density(degree: int = 120, radius: float = 0.7) -> ComponentDensity:
    """Compute the normalized invariant density of the central square component.

    If ``v`` is the invariant analytic circle density normalized to circle mean
    one, its interval pushforward is

    ``rho_D(x) = v(x) / (pi*sqrt(r**2-x**2))``.
    """

    matrix = beta_one_circle_matrix(degree, radius)
    values, vectors = eig(matrix)
    index = int(np.argmin(np.abs(values - 1.0)))
    coefficients = np.asarray(vectors[:, index].real)
    coefficients /= float(np.dot(_circle_mean(degree, radius), coefficients))
    analytic_zero = float(coefficients[0])
    interval_zero = analytic_zero / (np.pi * R_FIXED)
    return ComponentDensity(
        coefficients=coefficients,
        radius=float(radius),
        eigenvalue=float(values[index].real),
        analytic_value_at_zero=analytic_zero,
        interval_density_at_zero=interval_zero,
    )


def parity_profile_rate(lam: float = LAMBDA_FIXED) -> float:
    """Return the exact error-function rate at the component boundary."""

    return float(np.sqrt((float(lam) ** 2 - 1.0) / 2.0))


def endpoint_response_rate(
    *,
    u: float = U_CRITICAL,
    lam: float = LAMBDA_FIXED,
) -> float:
    """Return the rate appearing after the endpoint maps into the boundary."""

    return float(2.0 * u * parity_profile_rate(lam) / lam)


def parity_boundary_profile(xi: np.ndarray | float) -> np.ndarray | float:
    """The exact local left profile ``H(xi)=-erf(kappa*xi)``."""

    return -erf(parity_profile_rate() * np.asarray(xi))


def standard_normal_density(value: float | np.ndarray) -> float | np.ndarray:
    return np.exp(-0.5 * np.asarray(value) ** 2) / np.sqrt(2.0 * np.pi)


def endpoint_density_profile(
    xi: float,
    *,
    rho_c: float,
    u: float = U_CRITICAL,
) -> float:
    """Return the critical-value endpoint density profile ``R(xi)``.

    The row normalizer at the upper truncation contributes the denominator
    ``Phi(u*q**2)``.  Omitting it gives the wrong splitting constant.
    """

    xi = float(xi)
    if xi < 0.0:
        raise ValueError("the endpoint coordinate xi must be nonnegative")

    def integrand(q: float) -> float:
        value = float(u) * q * q
        return float(standard_normal_density(value - xi) / ndtr(value))

    return float(rho_c * quad(integrand, 0.0, np.inf, epsabs=2.0e-11, limit=250)[0])


@dataclass(frozen=True)
class BoundaryLayerConstant:
    """All scalar ingredients of the square-root splitting constant."""

    rho_c: float
    kappa: float
    endpoint_rate: float
    value: float
    quadrature_error: float


def square_root_gap_constant(
    *,
    rho_c: float | None = None,
    u: float = U_CRITICAL,
    lam: float = LAMBDA_FIXED,
) -> BoundaryLayerConstant:
    r"""Evaluate

    .. math::

       C_* = \rho_c\int_0^\infty \frac{dq}{\Phi(uq^2)}
       \int_0^\infty \phi(uq^2-\xi)\operatorname{erfc}(a\xi)\,d\xi.
    """

    if rho_c is None:
        rho_c = component_density().interval_density_at_zero
    rate = endpoint_response_rate(u=u, lam=lam)

    def outer_integrand(q: float) -> float:
        value = float(u) * q * q

        def inner_integrand(xi: float) -> float:
            return float(standard_normal_density(value - xi) * erfc(rate * xi))

        inner, _ = quad(inner_integrand, 0.0, np.inf, epsabs=1.0e-11, limit=220)
        return float(inner / ndtr(value))

    # For q>=6 one has u*q^2>55, while the erfc factor forces an
    # exponentially smaller overlap than double precision can resolve.
    integral, error = quad(
        outer_integrand,
        0.0,
        6.0,
        epsabs=2.0e-12,
        epsrel=2.0e-12,
        limit=260,
    )
    return BoundaryLayerConstant(
        rho_c=float(rho_c),
        kappa=parity_profile_rate(lam),
        endpoint_rate=rate,
        value=float(rho_c * integral),
        quadrature_error=float(abs(rho_c) * error),
    )


def boundary_eigen_equation_residual(xi: float) -> float:
    """Numerically audit ``E H(-lambda*xi+Z) = -H(xi)``."""

    xi = float(xi)

    def integrand(z: float) -> float:
        return float(
            standard_normal_density(z)
            * parity_boundary_profile(-LAMBDA_FIXED * xi + z)
        )

    expectation = quad(integrand, -10.0, 10.0, epsabs=2.0e-12, limit=200)[0]
    return float(expectation + parity_boundary_profile(xi))


def endpoint_residual_profile(xi: np.ndarray | float) -> np.ndarray | float:
    """Return ``erfc(a*xi)``, the unsigned endpoint solvability defect."""

    return erfc(endpoint_response_rate() * np.asarray(xi))
