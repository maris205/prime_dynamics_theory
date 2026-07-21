"""Validated scalar algebra for directional Stein-tail horizon budgets.

The functions here do not estimate a production transfer operator.  They
encode the exact scalar consequences of a packetwise bound
``t_j(L) <= t_j(0) q_j**L`` and the corresponding slow-mode obstruction.
Keeping this layer separate makes it possible to audit the numerical input
without silently promoting a fitted contraction law to a theorem.
"""

from __future__ import annotations

import math
from typing import Mapping, Sequence


def _finite_nonnegative(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def _contraction(value: float, name: str = "contraction") -> float:
    result = float(value)
    if not math.isfinite(result) or result < 0.0 or result >= 1.0:
        raise ValueError(f"{name} must lie in [0, 1)")
    return result


def geometric_tail_envelope(
    initial_tails: Sequence[float],
    contractions: Sequence[float],
    horizon: int,
) -> float:
    r"""Return ``sum_j t_j(0) q_j**horizon``.

    If ``S_j`` is a normalized packet operator with
    ``||S_j|| <= q_j < 1``, then the Stein tail term obeys this envelope:

    ``||S_j**L z_j|| <= q_j**L ||z_j||``.
    """

    tails = tuple(_finite_nonnegative(value, "initial tail") for value in initial_tails)
    rates = tuple(_contraction(value) for value in contractions)
    if len(tails) != len(rates) or not tails:
        raise ValueError("initial_tails and contractions must be nonempty and aligned")
    count = int(horizon)
    if count < 0:
        raise ValueError("horizon must be nonnegative")
    return float(sum(tail * rate**count for tail, rate in zip(tails, rates)))


def minimum_geometric_horizon(
    initial_tails: Sequence[float],
    contractions: Sequence[float],
    tolerance: float,
    *,
    maximum_horizon: int = 1 << 30,
) -> int:
    """Find the smallest integer horizon with a geometric envelope below ``tolerance``."""

    target = float(tolerance)
    if not math.isfinite(target) or target <= 0.0:
        raise ValueError("tolerance must be finite and positive")
    # Validate the vectors once and use the same routine for the search.
    geometric_tail_envelope(initial_tails, contractions, 0)
    if geometric_tail_envelope(initial_tails, contractions, 0) <= target:
        return 0
    upper = 1
    limit = int(maximum_horizon)
    if limit <= 0:
        raise ValueError("maximum_horizon must be positive")
    while upper < limit and geometric_tail_envelope(
        initial_tails, contractions, upper
    ) > target:
        upper = min(2 * upper, limit)
    if geometric_tail_envelope(initial_tails, contractions, upper) > target:
        raise ValueError("maximum_horizon is too small for the requested tolerance")
    lower = 0
    while lower < upper:
        middle = (lower + upper) // 2
        if geometric_tail_envelope(initial_tails, contractions, middle) <= target:
            upper = middle
        else:
            lower = middle + 1
    return lower


def slow_mode_horizon_lower_bound(
    contraction: float,
    amplitude: float,
    tolerance: float,
) -> int:
    r"""Return the exact integer lower bound from ``amplitude*q**L <= tolerance``.

    This is the horizon forced by a reducing slow mode whose tail contribution
    is at least ``amplitude*q**L``.  It is a lower bound on any certificate
    that claims the tail is at most ``tolerance``.
    """

    q = _contraction(contraction)
    a = _finite_nonnegative(amplitude, "amplitude")
    target = float(tolerance)
    if not math.isfinite(target) or target <= 0.0:
        raise ValueError("tolerance must be finite and positive")
    if a <= target:
        return 0
    value = math.log(a / target) / (-math.log(q))
    # The small upward cushion avoids returning one integer too few when the
    # exact ratio happens to be very close to an integer in binary64.
    return max(0, int(math.ceil(value - 1.0e-12)))


def observed_horizon(
    upper_by_horizon: Mapping[int | str, float],
    exact_energy: float,
    relative_tolerance: float,
) -> int | None:
    """Return the first stored horizon whose upper is within a relative error."""

    exact = _finite_nonnegative(exact_energy, "exact_energy")
    eta = float(relative_tolerance)
    if not math.isfinite(eta) or eta < 0.0:
        raise ValueError("relative_tolerance must be finite and nonnegative")
    target = (1.0 + eta) * exact
    candidates = []
    for key, value in upper_by_horizon.items():
        horizon = int(key)
        if horizon < 0:
            raise ValueError("horizons must be nonnegative")
        upper = _finite_nonnegative(value, "upper")
        if upper <= target:
            candidates.append(horizon)
    return min(candidates) if candidates else None


def log_power_fit(sigmas: Sequence[float], values: Sequence[float]) -> dict[str, float]:
    """Fit ``values = exp(intercept) * sigma**power`` without dependencies."""

    xs = tuple(float(value) for value in sigmas)
    ys = tuple(float(value) for value in values)
    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("a power fit needs at least two aligned values")
    if any(not math.isfinite(value) or value <= 0.0 for value in xs + ys):
        raise ValueError("power-fit inputs must be finite and positive")
    xbar = sum(math.log(value) for value in xs) / len(xs)
    ybar = sum(math.log(value) for value in ys) / len(ys)
    denominator = sum((math.log(value) - xbar) ** 2 for value in xs)
    if denominator == 0.0:
        raise ValueError("power-fit sigma values must not all coincide")
    slope = sum(
        (math.log(x) - xbar) * (math.log(y) - ybar)
        for x, y in zip(xs, ys)
    ) / denominator
    intercept = ybar - slope * xbar
    residuals = [
        math.log(y) - (intercept + slope * math.log(x))
        for x, y in zip(xs, ys)
    ]
    return {
        "power": float(slope),
        "growth_exponent": float(max(0.0, -slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(max(abs(value) for value in residuals)),
        "levels": len(xs),
    }
