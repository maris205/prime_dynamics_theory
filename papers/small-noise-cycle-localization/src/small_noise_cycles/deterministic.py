"""Deterministic quadratic cocycles and their fixed-length cycle traces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from numpy.polynomial import Polynomial
from scipy.optimize import brentq, newton


@dataclass(frozen=True)
class CycleOrbit:
    """One closed deterministic orbit of a time-ordered parameter word."""

    root: float
    points: tuple[float, ...]
    multiplier: float
    weight: float
    boundary_clearance: float
    closure_error: float


def _parameters(parameters: Iterable[float]) -> tuple[float, ...]:
    values = tuple(float(value) for value in parameters)
    if not values:
        raise ValueError("at least one parameter is required")
    if not np.all(np.isfinite(values)):
        raise ValueError("parameters must be finite")
    return values


def quadratic_map(x: np.ndarray | float, parameter: float) -> np.ndarray | float:
    """Return ``f_u(x)=1-u*x**2``."""

    return 1.0 - float(parameter) * np.asarray(x) ** 2


def compose_value(x: np.ndarray | float, parameters: Iterable[float]) -> np.ndarray:
    """Apply a parameter word in chronological order."""

    value = np.asarray(x, dtype=np.float64)
    for parameter in _parameters(parameters):
        value = 1.0 - parameter * value * value
    return value


def compose_value_derivative(x: float, parameters: Iterable[float]) -> tuple[float, float]:
    """Return the value and spatial derivative of the ordered composition."""

    value = float(x)
    derivative = 1.0
    for parameter in _parameters(parameters):
        derivative *= -2.0 * parameter * value
        value = 1.0 - parameter * value * value
    return value, derivative


def composition_polynomial(parameters: Iterable[float]) -> Polynomial:
    """Return the polynomial ``f_um o ... o f_u1``."""

    polynomial = Polynomial((0.0, 1.0))
    one = Polynomial((1.0,))
    for parameter in _parameters(parameters):
        polynomial = one - parameter * polynomial * polynomial
    return polynomial


def _polynomial_candidates(parameters: Sequence[float], tolerance: float) -> list[float]:
    fixed_polynomial = composition_polynomial(parameters) - Polynomial((0.0, 1.0))
    candidates: list[float] = []
    for value in fixed_polynomial.roots():
        if abs(value.imag) <= tolerance and -1.0 - tolerance <= value.real <= 1.0 + tolerance:
            candidates.append(float(np.clip(value.real, -1.0, 1.0)))
    return candidates


def fixed_points(
    parameters: Iterable[float],
    *,
    grid_size: int = 40_001,
    root_tolerance: float = 2.0e-10,
) -> np.ndarray:
    """Find every simple real fixed point of the ordered composition on ``[-1,1]``.

    Sign-changing brackets provide the robust path.  Polynomial roots are added
    as candidates so closely spaced roots are not silently missed at length six.
    Every accepted candidate is refined against the composed map itself.
    """

    values = _parameters(parameters)
    if grid_size < 1001:
        raise ValueError("grid_size must be at least 1001")
    grid = np.linspace(-1.0, 1.0, int(grid_size), dtype=np.float64)
    residual = compose_value(grid, values) - grid
    candidates: list[float] = []

    endpoint_tolerance = 1.0e-12
    if abs(residual[0]) <= endpoint_tolerance:
        candidates.append(-1.0)
    if abs(residual[-1]) <= endpoint_tolerance:
        candidates.append(1.0)

    changes = np.flatnonzero(residual[:-1] * residual[1:] < 0.0)
    for index in changes:
        left = float(grid[index])
        right = float(grid[index + 1])
        root = brentq(
            lambda point: compose_value_derivative(point, values)[0] - point,
            left,
            right,
            xtol=5.0e-15,
            rtol=5.0e-15,
        )
        candidates.append(float(root))

    candidates.extend(_polynomial_candidates(values, tolerance=1.0e-7))
    refined: list[float] = []
    for candidate in candidates:
        try:
            root = float(
                newton(
                    lambda point: compose_value_derivative(point, values)[0] - point,
                    candidate,
                    fprime=lambda point: compose_value_derivative(point, values)[1] - 1.0,
                    tol=5.0e-14,
                    maxiter=50,
                )
            )
        except (RuntimeError, OverflowError, ZeroDivisionError):
            root = candidate
        value, _ = compose_value_derivative(root, values)
        if -1.0 - root_tolerance <= root <= 1.0 + root_tolerance and abs(value - root) < 2.0e-9:
            refined.append(float(np.clip(root, -1.0, 1.0)))

    refined.sort()
    unique: list[float] = []
    for root in refined:
        if not unique or abs(root - unique[-1]) > root_tolerance:
            unique.append(root)
    return np.asarray(unique, dtype=np.float64)


def orbit_from_root(root: float, parameters: Iterable[float]) -> tuple[tuple[float, ...], float, float]:
    """Return orbit points, multiplier, and closure error for one fixed point."""

    values = _parameters(parameters)
    point = float(root)
    points: list[float] = []
    multiplier = 1.0
    for parameter in values:
        points.append(point)
        multiplier *= -2.0 * parameter * point
        point = 1.0 - parameter * point * point
    return tuple(points), float(multiplier), float(point - root)


def cycle_orbits(
    parameters: Iterable[float],
    *,
    grid_size: int = 40_001,
) -> list[CycleOrbit]:
    """Return all nondegenerate deterministic cycles for one parameter word."""

    values = _parameters(parameters)
    records: list[CycleOrbit] = []
    for root in fixed_points(values, grid_size=grid_size):
        points, multiplier, closure_error = orbit_from_root(float(root), values)
        determinant = abs(1.0 - multiplier)
        if determinant <= 1.0e-10:
            raise ValueError("the ordered composition has a degenerate fixed point")
        records.append(
            CycleOrbit(
                root=float(root),
                points=points,
                multiplier=multiplier,
                weight=1.0 / determinant,
                boundary_clearance=min(1.0 - abs(point) for point in points),
                closure_error=abs(closure_error),
            )
        )
    return records


def periodic_orbit_trace(parameters: Iterable[float], *, grid_size: int = 40_001) -> float:
    """Return the deterministic trace ``sum |1-F'(x)|^{-1}``."""

    return float(sum(record.weight for record in cycle_orbits(parameters, grid_size=grid_size)))


def directed_parameter_words(
    a: float,
    b: float,
    c: float,
    *,
    block_length: int = 1,
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    """Return forward and one-transposition parameter words."""

    if block_length < 1:
        raise ValueError("block_length must be positive")
    forward = (float(a),) * block_length + (float(b),) * block_length + (float(c),) * block_length
    reverse = (float(a),) * block_length + (float(c),) * block_length + (float(b),) * block_length
    return forward, reverse


def directed_orbit_trace(
    a: float,
    b: float,
    c: float,
    *,
    block_length: int = 1,
    grid_size: int = 40_001,
) -> float:
    """Return the deterministic directed three-block cycle trace."""

    forward, reverse = directed_parameter_words(a, b, c, block_length=block_length)
    return periodic_orbit_trace(forward, grid_size=grid_size) - periodic_orbit_trace(
        reverse, grid_size=grid_size
    )


def vandermonde(a: float, b: float, c: float) -> float:
    return float((a - b) * (b - c) * (c - a))


def directed_curvature_extrapolation(
    u: float,
    separations: Iterable[float],
    *,
    block_length: int = 1,
    grid_size: int = 100_001,
) -> dict[str, np.ndarray | float]:
    """Extrapolate the diagonal deterministic Vandermonde quotient in ``e**2``."""

    epsilon = np.asarray(tuple(float(value) for value in separations), dtype=np.float64)
    if epsilon.size < 3 or np.any(epsilon <= 0.0):
        raise ValueError("at least three positive separations are required")
    quotients = []
    for value in epsilon:
        a, b, c = u - value, u, u + value
        directed = directed_orbit_trace(
            a,
            b,
            c,
            block_length=block_length,
            grid_size=grid_size,
        )
        quotients.append(directed / vandermonde(a, b, c))
    quotient = np.asarray(quotients, dtype=np.float64)
    coefficients = np.polyfit(epsilon * epsilon, quotient, deg=2)
    return {
        "separations": epsilon,
        "quotients": quotient,
        "coefficients": coefficients,
        "limit": float(coefficients[-1]),
    }
