"""Quantitative consequences of one contractive operator-power block."""

from __future__ import annotations

import numpy as np


def _validate(
    trace_norm_block: float,
    operator_norm_block: float,
    remainder_norms: list[float] | np.ndarray,
    block_size: int,
) -> tuple[float, float, np.ndarray, int]:
    size = int(block_size)
    trace_norm = float(trace_norm_block)
    contraction = float(operator_norm_block)
    remainders = np.asarray(remainder_norms, dtype=float).reshape(-1)
    if size < 2 or remainders.size != size:
        raise ValueError("remainder norms must cover orders 0 through m-1")
    if trace_norm < 0.0 or not 0.0 <= contraction < 1.0 or np.any(remainders < 0.0):
        raise ValueError("norm bounds must be nonnegative and block norm must be below one")
    return trace_norm, contraction, remainders, size


def block_trace_bound(
    trace_norm_block: float,
    operator_norm_block: float,
    remainder_norms: list[float] | np.ndarray,
    block_size: int,
    order: int,
) -> float:
    """Bound |Tr C^n| after writing n=ell*m+r, for n>=m."""

    trace_norm, contraction, remainders, size = _validate(
        trace_norm_block,
        operator_norm_block,
        remainder_norms,
        block_size,
    )
    n = int(order)
    if n < size:
        raise ValueError("the block bound starts at order m")
    quotient, remainder = divmod(n, size)
    return float(trace_norm * remainders[remainder] * contraction ** (quotient - 1))


def geometric_envelope_constant(
    trace_norm_block: float,
    operator_norm_block: float,
    remainder_norms: list[float] | np.ndarray,
    block_size: int,
) -> dict[str, float]:
    """Convert the block bound into M q^n for all n>=m."""

    trace_norm, contraction, remainders, size = _validate(
        trace_norm_block,
        operator_norm_block,
        remainder_norms,
        block_size,
    )
    rate = contraction ** (1.0 / size)
    if rate == 0.0:
        constant = trace_norm * float(np.max(remainders))
    else:
        constant = trace_norm * max(
            float(remainders[remainder]) * rate ** (-(remainder + size))
            for remainder in range(size)
        )
    return {"M": float(constant), "q": float(rate)}


def logarithmic_tail_bound(
    trace_norm_block: float,
    operator_norm_block: float,
    remainder_norms: list[float] | np.ndarray,
    block_size: int,
    radius: float,
) -> float:
    """Bound sum_(n>=m) |Tr C^n| R^n/n."""

    trace_norm, contraction, remainders, size = _validate(
        trace_norm_block,
        operator_norm_block,
        remainder_norms,
        block_size,
    )
    disk = float(radius)
    if disk < 0.0 or contraction * disk**size >= 1.0:
        raise ValueError("radius must be nonnegative and eta*R^m must be below one")
    weighted_remainders = sum(
        float(remainders[remainder]) * disk**remainder
        for remainder in range(size)
    )
    return float(
        trace_norm
        * disk**size
        * weighted_remainders
        / (size * (1.0 - contraction * disk**size))
    )
