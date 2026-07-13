"""High-accuracy periodic weights for the central two-step component."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def critical_parameter() -> np.longdouble:
    """Algebraic band-merging parameter at long-double precision."""

    u = np.longdouble("1.543689012692076")
    for _ in range(20):
        polynomial = u**3 - np.longdouble(2) * u**2 + np.longdouble(2) * u - 2
        derivative = np.longdouble(3) * u**2 - np.longdouble(4) * u + 2
        updated = u - polynomial / derivative
        if updated == u:
            break
        u = updated
    return u


U_CRITICAL = np.longdouble(critical_parameter())
R_FIXED = U_CRITICAL - 1.0
LAMBDA_FIXED = 2.0 * U_CRITICAL * R_FIXED


@dataclass(frozen=True)
class TraceAudit:
    two_step_length: int
    weighted_trace: np.longdouble
    fixed_point_count: int
    maximum_inverse_residual: np.longdouble
    maximum_iterations: int


def quadratic_component_map(
    x: np.ndarray | np.longdouble,
    *,
    dtype: type = np.longdouble,
) -> np.ndarray:
    """The central component map T=f^2 on [-r,r]."""

    value = np.asarray(x, dtype=dtype)
    u = dtype(U_CRITICAL)
    r = dtype(R_FIXED)
    return -r + dtype(2) * u**2 * value**2 - u**3 * value**4


def positive_inverse_branch(
    value: np.ndarray | np.longdouble,
    *,
    dtype: type = np.longdouble,
) -> np.ndarray:
    """Stable positive inverse branch of T=f^2.

    The rationalized form avoids cancellation at the critical value -r.
    """

    y = np.asarray(value, dtype=dtype)
    u = dtype(U_CRITICAL)
    r = dtype(R_FIXED)
    inner = np.maximum(dtype(0), (dtype(1) - y) / u)
    numerator = np.maximum(dtype(0), y + r)
    denominator = u**2 * (dtype(1) + np.sqrt(inner))
    return np.sqrt(numerator / denominator)


def _apply_inverse_words(
    values: np.ndarray,
    codes: np.ndarray,
    length: int,
    *,
    with_weight: bool,
) -> tuple[np.ndarray, np.ndarray | None]:
    dtype = values.dtype.type
    u = dtype(U_CRITICAL)
    result = values
    weight = np.ones_like(result) if with_weight else None
    for shift in range(length - 1, -1, -1):
        positive = positive_inverse_branch(result, dtype=dtype)
        if with_weight:
            derivative_denominator = (
                dtype(4) * u**2 * positive * (dtype(1) - u * positive**2)
            )
            assert weight is not None
            weight *= dtype(1) / derivative_denominator
        right = ((codes >> np.uint64(shift)) & np.uint64(1)).astype(bool)
        result = np.where(right, positive, -positive)
    return result, weight


def _chunk_trace(
    length: int,
    start: int,
    stop: int,
    *,
    maximum_iterations: int,
) -> tuple[np.longdouble, np.longdouble, int]:
    dtype = np.longdouble
    codes = np.arange(start, stop, dtype=np.uint64)
    values = np.zeros(stop - start, dtype=dtype)
    # The postcritical remainder is about 10^-14 by n=20, so a loose fixed-point
    # tolerance contaminates the final subtraction even when the trace itself
    # looks converged.  Iterate essentially to the long-double rounding floor.
    tolerance = dtype(8) * np.finfo(dtype).eps
    iterations = 0
    for iterations in range(1, maximum_iterations + 1):
        updated, _ = _apply_inverse_words(values, codes, length, with_weight=False)
        error = np.max(np.abs(updated - values))
        values = updated
        if error <= tolerance:
            break
    else:
        raise RuntimeError(
            f"inverse words of length {length} did not converge in "
            f"{maximum_iterations} iterations"
        )

    fixed_images, weights = _apply_inverse_words(
        values, codes, length, with_weight=True
    )
    assert weights is not None
    residual = np.max(np.abs(fixed_images - values))
    return np.sum(weights, dtype=dtype), residual, iterations


def component_weighted_trace(
    two_step_length: int,
    *,
    chunk_size: int = 1 << 17,
    maximum_iterations: int = 80,
) -> TraceAudit:
    """Sum the inverse multiplier over all 2^n component fixed points."""

    if two_step_length < 1:
        raise ValueError("two_step_length must be positive")
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")

    count = 1 << two_step_length
    total = np.longdouble(0)
    maximum_residual = np.longdouble(0)
    used_iterations = 0
    for start in range(0, count, chunk_size):
        stop = min(start + chunk_size, count)
        partial, residual, iterations = _chunk_trace(
            two_step_length,
            start,
            stop,
            maximum_iterations=maximum_iterations,
        )
        total += partial
        maximum_residual = max(maximum_residual, residual)
        used_iterations = max(used_iterations, iterations)
    return TraceAudit(
        two_step_length=two_step_length,
        weighted_trace=total,
        fixed_point_count=count,
        maximum_inverse_residual=maximum_residual,
        maximum_iterations=used_iterations,
    )
