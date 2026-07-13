"""Exact Markov coding and periodic-orbit traces at band merging."""

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
    """Unique root of ``u^3-2u^2+2u-2`` in ``(1,2)``."""

    return float(brentq(lambda u: u**3 - 2.0 * u**2 + 2.0 * u - 2.0, 1.0, 2.0))


U_CRITICAL = critical_parameter()
R_FIXED = U_CRITICAL - 1.0
LAMBDA_FIXED = 2.0 * U_CRITICAL * R_FIXED


def markov_matrix() -> np.ndarray:
    return np.asarray(((0, 0, 1), (0, 0, 1), (1, 1, 0)), dtype=np.int64)


def quadratic_map(x: np.ndarray | float, u: float = U_CRITICAL) -> np.ndarray:
    return 1.0 - float(u) * np.asarray(x) ** 2


def critical_orbit() -> tuple[float, float, float, float, float]:
    values = [0.0]
    for _ in range(4):
        values.append(float(quadratic_map(values[-1])))
    return tuple(values)  # type: ignore[return-value]


def cyclic_words(length: int) -> Iterator[tuple[str, ...]]:
    """Generate all closed paths of the three-state Markov graph."""

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


def symbolic_closed_path_count(length: int) -> int:
    return int(np.trace(np.linalg.matrix_power(markov_matrix(), int(length))))


def physical_fixed_point_count(length: int) -> int:
    """Exact number of distinct real roots of ``f^length(x)=x`` on the core."""

    if length < 1:
        raise ValueError("length must be positive")
    if length % 2:
        return 1
    return 2 ** (length // 2 + 1) - 1


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
    radicand = max(0.0, (1.0 - float(value)) / U_CRITICAL)
    return sign * float(np.sqrt(radicand))


def inverse_word(word: Sequence[str], value: float) -> float:
    result = float(value)
    for symbol in reversed(tuple(word)):
        result = inverse_branch(symbol, result)
    return result


def _bracketed_inverse_fixed_point(word: Sequence[str]) -> float:
    left, right = symbol_interval(word[0])
    grid = np.linspace(left, right, 1001)
    residual = np.asarray([inverse_word(word, value) - value for value in grid])
    exact = np.flatnonzero(np.abs(residual) < 2.0e-13)
    if exact.size:
        return float(grid[int(exact[0])])
    changes = np.flatnonzero(residual[:-1] * residual[1:] < 0.0)
    if not changes.size:
        raise RuntimeError("failed to bracket inverse-word fixed point")
    index = int(changes[0])
    return float(
        brentq(
            lambda value: inverse_word(word, value) - value,
            float(grid[index]),
            float(grid[index + 1]),
            xtol=5.0e-15,
            rtol=5.0e-15,
        )
    )


def inverse_word_fixed_point(word: Sequence[str]) -> float:
    """Solve the inverse-branch contraction attached to a closed symbolic word."""

    symbols = tuple(word)
    if not symbols:
        raise ValueError("word must be nonempty")
    left, right = symbol_interval(symbols[0])
    value = 0.5 * (left + right)
    for _ in range(200):
        updated = inverse_word(symbols, value)
        if abs(updated - value) < 3.0e-15:
            value = updated
            break
        value = updated
    residual = float(iterate_map(value, len(symbols)) - value)
    if not (left - 2.0e-11 <= value <= right + 2.0e-11) or abs(residual) > 2.0e-9:
        value = _bracketed_inverse_fixed_point(symbols)
    return float(np.clip(value, left, right))


def iterate_map(x: np.ndarray | float, length: int) -> np.ndarray:
    value = np.asarray(x, dtype=np.float64)
    for _ in range(int(length)):
        value = quadratic_map(value)
    return value


@lru_cache(maxsize=64)
def periodic_points(length: int) -> tuple[float, ...]:
    """Enumerate all distinct real fixed points using the finite Markov graph."""

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
def deterministic_flat_trace(length: int) -> float:
    return float(
        sum(1.0 / abs(1.0 - orbit_multiplier(point, length)) for point in periodic_points(length))
    )


def parity_baseline(length: int) -> float:
    return float(1 + (-1) ** int(length))


def parity_centered_flat_trace(length: int) -> float:
    return deterministic_flat_trace(length) - parity_baseline(length)


def boundary_word(length: int) -> tuple[str, ...]:
    """Closed word whose fixed point approaches the upper boundary fastest."""

    if length < 2 or length % 2:
        raise ValueError("boundary word requires a positive even length")
    return ("C", "A") + ("C", "B") * (length // 2 - 1)


def boundary_periodic_point(length: int) -> float:
    return inverse_word_fixed_point(boundary_word(length))


@dataclass(frozen=True)
class LongCycleAudit:
    length: int
    fixed_point_count: int
    flat_trace: float
    parity_baseline: float
    centered_trace: float
    boundary_clearance: float
    boundary_scaled: float
    minimum_multiplier: float
    maximum_multiplier: float


def audit_length(length: int) -> LongCycleAudit:
    points = periodic_points(length)
    multipliers = np.abs([orbit_multiplier(point, length) for point in points])
    trace = deterministic_flat_trace(length)
    clearance = min(1.0 - abs(point) for point in points)
    return LongCycleAudit(
        length=int(length),
        fixed_point_count=len(points),
        flat_trace=trace,
        parity_baseline=parity_baseline(length),
        centered_trace=trace - parity_baseline(length),
        boundary_clearance=float(clearance),
        boundary_scaled=float(clearance * LAMBDA_FIXED**length),
        minimum_multiplier=float(np.min(multipliers)),
        maximum_multiplier=float(np.max(multipliers)),
    )
