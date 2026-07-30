"""Exact parity formulas for the deterministic numerator trace anchor."""

from __future__ import annotations

import math


def odd_anchor(order: int, lam: float, hardy_radius: float = 0.85) -> float:
    """Return the exact Hardy-scaled odd numerator coefficient for order >=3."""

    n = int(order)
    if n < 3 or n % 2 == 0:
        raise ValueError("odd_anchor requires an odd order at least three")
    if lam <= 1.0 or not 0.0 < hardy_radius < 1.0:
        raise ValueError("invalid lambda or Hardy radius")
    return float((hardy_radius * lam) ** (-n) / (1.0 + lam ** (-n)))


def reduced_trace_from_physical_trace(
    physical_trace: float, iterate: int, lam: float
) -> float:
    """Recover tr(T^k) from the RH-15 even physical trace identity."""

    k = int(iterate)
    if k < 1 or lam <= 1.0:
        raise ValueError("invalid iterate or lambda")
    a = lam ** (-k)
    return float(
        0.5 * (physical_trace + 2.0 * a / (1.0 + a) + a * a / (1.0 - a * a))
        - 1.0
    )


def even_anchor_from_reduced_trace(
    iterate: int,
    reduced_trace: float,
    lam: float,
    hardy_radius: float = 0.85,
) -> float:
    """Return a_{2k} from the reduced trace tr(T^k)."""

    k = int(iterate)
    if k < 1 or lam <= 1.0 or not 0.0 < hardy_radius < 1.0:
        raise ValueError("invalid iterate, lambda, or Hardy radius")
    a = lam ** (-k)
    scalar = 2.0 * a * a / (1.0 + a) - a * a / (1.0 - a * a)
    return float(hardy_radius ** (-2 * k) * (2.0 * reduced_trace + scalar))


def parity_anchor_from_physical_trace(
    order: int,
    physical_trace: float,
    lam: float,
    hardy_radius: float = 0.85,
) -> float:
    """Evaluate the one-step deterministic anchor at one physical trace."""

    n = int(order)
    if n < 2:
        raise ValueError("the numerator anchor starts at order two")
    if n % 2:
        return odd_anchor(n, lam, hardy_radius)
    reduced = reduced_trace_from_physical_trace(physical_trace, n // 2, lam)
    return even_anchor_from_reduced_trace(n // 2, reduced, lam, hardy_radius)


def geometric_odd_tail(
    first_order: int, lam: float, hardy_radius: float = 0.85
) -> float:
    """A simple all-order upper bound for the odd logarithmic tail."""

    n = int(first_order)
    if n < 3 or n % 2 == 0:
        raise ValueError("first_order must be odd and at least three")
    q = 1.0 / (hardy_radius * lam)
    return float(q**n / (n * (1.0 - q * q)))


def validate_parameters(lam: float, hardy_radius: float) -> None:
    if not math.isfinite(lam) or lam <= 1.0:
        raise ValueError("lambda must be finite and greater than one")
    if not math.isfinite(hardy_radius) or not 0.0 < hardy_radius < 1.0:
        raise ValueError("Hardy radius must lie in (0,1)")
