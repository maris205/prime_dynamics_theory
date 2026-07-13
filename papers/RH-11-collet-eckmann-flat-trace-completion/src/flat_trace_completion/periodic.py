"""Periodic data for the postcritically finite quadratic band merge."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Iterator, Sequence

import numpy as np
from scipy.optimize import brentq


SYMBOLS = ("A", "B", "C")
TRANSITIONS: dict[str, tuple[str, ...]] = {
    "A": ("C",),
    "B": ("C",),
    "C": ("A", "B"),
}


def critical_parameter() -> float:
    return float(brentq(lambda u: u**3 - 2.0 * u**2 + 2.0 * u - 2.0, 1.0, 2.0))


U_CRITICAL = critical_parameter()
R_FIXED = U_CRITICAL - 1.0
LAMBDA_FIXED = 2.0 * U_CRITICAL * R_FIXED
H_CRITICAL = U_CRITICAL ** -0.5


def quadratic_map(x: np.ndarray | float) -> np.ndarray:
    return 1.0 - U_CRITICAL * np.asarray(x) ** 2


def iterate_map(x: np.ndarray | float, length: int) -> np.ndarray:
    value = np.asarray(x, dtype=np.float64)
    for _ in range(int(length)):
        value = quadratic_map(value)
    return value


def critical_orbit() -> tuple[float, ...]:
    values = [0.0]
    for _ in range(4):
        values.append(float(quadratic_map(values[-1])))
    return tuple(values)


def critical_value_derivative(length: int) -> float:
    """Absolute derivative of ``f^length`` at the critical value ``f(0)=1``."""

    if length < 1:
        raise ValueError("length must be positive")
    return float(2.0 * U_CRITICAL * LAMBDA_FIXED ** (length - 1))


def component_critical_value_derivative(component: str, length: int) -> float:
    """CE derivative for ``T=f^2`` on the central or high component."""

    if length < 1:
        raise ValueError("length must be positive")
    if component == "central":
        return float(LAMBDA_FIXED ** (2 * length))
    if component == "high":
        return float(2.0 * U_CRITICAL * LAMBDA_FIXED ** (2 * length - 1))
    raise ValueError("component must be 'central' or 'high'")


def component_geometry(component: str) -> dict[str, float | tuple[float, float]]:
    if component == "central":
        return {
            "interval": (-R_FIXED, R_FIXED),
            "critical_point": 0.0,
            "critical_value": -R_FIXED,
            "critical_value_next": R_FIXED,
        }
    if component == "high":
        return {
            "interval": (R_FIXED, 1.0),
            "critical_point": H_CRITICAL,
            "critical_value": 1.0,
            "critical_value_next": R_FIXED,
        }
    raise ValueError("component must be 'central' or 'high'")


def cyclic_words(length: int) -> Iterator[tuple[str, ...]]:
    if length < 1:
        raise ValueError("length must be positive")

    def extend(word: tuple[str, ...]) -> Iterator[tuple[str, ...]]:
        if len(word) == length:
            if word[0] in TRANSITIONS[word[-1]]:
                yield word
            return
        choices = SYMBOLS if not word else TRANSITIONS[word[-1]]
        for symbol in choices:
            yield from extend(word + (symbol,))

    yield from extend(())


def physical_fixed_point_count(length: int) -> int:
    if length < 1:
        raise ValueError("length must be positive")
    return 1 if length % 2 else 2 ** (length // 2 + 1) - 1


def symbol_interval(symbol: str) -> tuple[float, float]:
    if symbol == "A":
        return -R_FIXED, 0.0
    if symbol == "B":
        return 0.0, R_FIXED
    if symbol == "C":
        return R_FIXED, 1.0
    raise ValueError(f"unknown symbol {symbol!r}")


def inverse_branch(symbol: str, value: float) -> float:
    if symbol not in SYMBOLS:
        raise ValueError(f"unknown symbol {symbol!r}")
    sign = -1.0 if symbol == "A" else 1.0
    return sign * float(np.sqrt(max(0.0, (1.0 - float(value)) / U_CRITICAL)))


def inverse_word(word: Sequence[str], value: float) -> float:
    result = float(value)
    for symbol in reversed(tuple(word)):
        result = inverse_branch(symbol, result)
    return result


def inverse_word_fixed_point(word: Sequence[str]) -> float:
    symbols = tuple(word)
    if not symbols:
        raise ValueError("word must be nonempty")
    left, right = symbol_interval(symbols[0])
    value = 0.5 * (left + right)
    for _ in range(220):
        updated = inverse_word(symbols, value)
        if abs(updated - value) < 3.0e-15:
            value = updated
            break
        value = updated
    inverse_residual = abs(inverse_word(symbols, value) - value)
    if (
        left - 2.0e-11 <= value <= right + 2.0e-11
        and inverse_residual < 2.0e-12
    ):
        return float(np.clip(value, left, right))

    grid = np.linspace(left, right, 1201)
    residual = np.asarray([inverse_word(symbols, point) - point for point in grid])
    exact = np.flatnonzero(np.abs(residual) < 2.0e-13)
    if exact.size:
        return float(grid[int(exact[0])])
    changes = np.flatnonzero(residual[:-1] * residual[1:] < 0.0)
    if not changes.size:
        raise RuntimeError("failed to bracket inverse-word fixed point")
    index = int(changes[0])
    return float(
        brentq(
            lambda point: inverse_word(symbols, point) - point,
            float(grid[index]),
            float(grid[index + 1]),
            xtol=5.0e-15,
            rtol=5.0e-15,
        )
    )


@lru_cache(maxsize=64)
def periodic_points(length: int) -> tuple[float, ...]:
    if length < 1:
        raise ValueError("length must be positive")
    if length % 2:
        return (R_FIXED,)
    candidates = sorted(inverse_word_fixed_point(word) for word in cyclic_words(length))
    unique: list[float] = []
    for value in candidates:
        if not unique or abs(value - unique[-1]) > 2.0e-11:
            unique.append(value)
    expected = physical_fixed_point_count(length)
    if len(unique) != expected:
        raise RuntimeError(f"expected {expected} roots at length {length}, found {len(unique)}")
    return tuple(unique)


def orbit_multiplier(point: float, length: int) -> float:
    value = float(point)
    derivative = 1.0
    for _ in range(int(length)):
        derivative *= -2.0 * U_CRITICAL * value
        value = float(quadratic_map(value))
    return float(derivative)


@lru_cache(maxsize=64)
def weighted_periodic_trace(length: int) -> float:
    return float(
        sum(1.0 / abs(orbit_multiplier(point, length)) for point in periodic_points(length))
    )


@lru_cache(maxsize=64)
def flat_periodic_trace(length: int) -> float:
    return float(
        sum(
            1.0 / abs(1.0 - orbit_multiplier(point, length))
            for point in periodic_points(length)
        )
    )


def component_weighted_traces(length: int) -> tuple[float, float]:
    """Weighted traces on the two ``f^2`` components, each including ``r``."""

    if length < 2 or length % 2:
        raise ValueError("component traces require a positive even length")
    points = periodic_points(length)
    weighted = [(point, 1.0 / abs(orbit_multiplier(point, length))) for point in points]
    central = sum(weight for point, weight in weighted if point <= R_FIXED + 1.0e-11)
    high = sum(weight for point, weight in weighted if point >= R_FIXED - 1.0e-11)
    return float(central), float(high)


@dataclass(frozen=True)
class TraceComparison:
    length: int
    fixed_point_count: int
    flat_trace: float
    weighted_trace: float
    flat_minus_weighted: float
    parity_centered_flat: float
    parity_centered_weighted: float
    central_weighted: float | None
    high_weighted: float | None
    component_difference: float | None
    component_reconstruction_error: float | None
    minimum_multiplier: float
    elementary_comparison_bound: float


def audit_length(length: int) -> TraceComparison:
    points = periodic_points(length)
    multipliers = np.abs([orbit_multiplier(point, length) for point in points])
    flat = flat_periodic_trace(length)
    weighted = weighted_periodic_trace(length)
    baseline = float(1 + (-1) ** length)
    central: float | None = None
    high: float | None = None
    component_difference: float | None = None
    reconstruction_error: float | None = None
    if length % 2 == 0:
        central, high = component_weighted_traces(length)
        component_difference = central - high
        reconstruction = central + high - LAMBDA_FIXED ** (-length)
        reconstruction_error = reconstruction - weighted
    minimum = float(np.min(multipliers))
    bound = float(2.0 * weighted / minimum) if minimum >= 2.0 else float("inf")
    return TraceComparison(
        length=length,
        fixed_point_count=len(points),
        flat_trace=flat,
        weighted_trace=weighted,
        flat_minus_weighted=flat - weighted,
        parity_centered_flat=flat - baseline,
        parity_centered_weighted=weighted - baseline,
        central_weighted=central,
        high_weighted=high,
        component_difference=component_difference,
        component_reconstruction_error=reconstruction_error,
        minimum_multiplier=minimum,
        elementary_comparison_bound=bound,
    )
