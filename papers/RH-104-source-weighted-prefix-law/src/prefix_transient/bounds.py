"""Scalar bounds for source-weighted finite-prefix transient laws."""

from __future__ import annotations

import math


def _nonnegative(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def crude_prefix_upper(observation_norm: float, source_block_energy: float) -> float:
    """Return ||Y|| sqrt(sum ||A^r X||_F^2)."""
    observation = _nonnegative(observation_norm, "observation norm")
    source = _nonnegative(source_block_energy, "source block energy")
    return math.nextafter(observation * math.sqrt(source), math.inf)


def block_tail_energy_squared_upper(
    observation_norm: float,
    block_contraction: float,
    source_block_energy: float,
) -> float:
    observation = _nonnegative(observation_norm, "observation norm")
    contraction = _nonnegative(block_contraction, "block contraction")
    source = _nonnegative(source_block_energy, "source block energy")
    if contraction >= 1.0:
        raise ValueError("block contraction must be below one")
    value = observation**2 * contraction**2 * source / (1.0 - contraction**2)
    return math.nextafter(value, math.inf)


def full_hardy_upper(prefix_energy: float, tail_energy_squared: float) -> float:
    prefix = _nonnegative(prefix_energy, "prefix energy")
    tail2 = _nonnegative(tail_energy_squared, "tail energy squared")
    return math.nextafter(math.sqrt(prefix**2 + tail2), math.inf)


def crude_prefix_power(observation_power: float, source_energy_squared_power: float) -> float:
    """Signed sigma power of ||Y|| sqrt(S_M)."""
    observation = float(observation_power)
    source2 = float(source_energy_squared_power)
    if not math.isfinite(observation) or not math.isfinite(source2):
        raise ValueError("powers must be finite")
    return observation + 0.5 * source2


def directional_prefix_power(prefix_energy_squared_power: float) -> float:
    power2 = float(prefix_energy_squared_power)
    if not math.isfinite(power2):
        raise ValueError("power must be finite")
    return max(0.0, 0.5 * power2)
