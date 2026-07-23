"""Bounds and signed-power bookkeeping for observation/residual cancellation."""

from __future__ import annotations

import math


def _nonnegative(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def full_observability_factor(full_observability_norm_upper: float) -> float:
    """Return an outward-rounded upper for sqrt(||O||)."""
    observability = _nonnegative(full_observability_norm_upper, "full observability norm")
    return math.nextafter(math.sqrt(observability), math.inf)


def block_observability_factor(prefix_observability_norm: float, block_contraction: float) -> float:
    """Return sqrt(||O_M||/(1-q^2))."""
    prefix = _nonnegative(prefix_observability_norm, "prefix observability norm")
    contraction = _nonnegative(block_contraction, "block contraction")
    if contraction >= 1.0:
        raise ValueError("block contraction must be below one")
    return math.nextafter(math.sqrt(prefix / (1.0 - contraction**2)), math.inf)


def weighted_residual_upper(observation_factor: float, residual: float) -> float:
    """Return an outward-rounded upper for Omega times tau."""
    observation = _nonnegative(observation_factor, "observation factor")
    tail = _nonnegative(residual, "residual")
    return math.nextafter(observation * tail, math.inf)


def signed_cancellation_power(observation_growth_power: float, residual_decay_power: float) -> float:
    """Return the signed power o-rho of Omega*tau."""
    observation = float(observation_growth_power)
    residual = float(residual_decay_power)
    if not math.isfinite(observation) or not math.isfinite(residual):
        raise ValueError("powers must be finite")
    return observation - residual


def nonnegative_cancellation_power(observation_growth_power: float, residual_decay_power: float) -> float:
    """Return the growth power max(0,o-rho)."""
    return max(0.0, signed_cancellation_power(observation_growth_power, residual_decay_power))


def matched_scale_factors(
    sigma: float,
    observation_factor: float,
    residual: float,
    split_power: float = 0.5,
) -> tuple[float, float]:
    """Return sigma^theta Omega and sigma^-theta tau."""
    scale = float(sigma)
    observation = _nonnegative(observation_factor, "observation factor")
    tail = _nonnegative(residual, "residual")
    theta = float(split_power)
    if not math.isfinite(scale) or not 0.0 < scale < 1.0:
        raise ValueError("sigma must lie in (0,1)")
    if not math.isfinite(theta):
        raise ValueError("split power must be finite")
    left = math.nextafter(scale**theta * observation, math.inf)
    right = math.nextafter(scale ** (-theta) * tail, math.inf)
    return left, right
