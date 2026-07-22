"""Max-plus sigma-power bookkeeping for directional Hardy bridges."""

from __future__ import annotations

import math


def _signed_power(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _growth_power(value: float, name: str) -> float:
    number = _signed_power(value, name)
    if number < 0.0:
        raise ValueError(f"{name} must be nonnegative")
    return number


def side_hardy_power(
    *,
    normalization: float,
    upstream_bridge: float,
    finite_prefix: float,
    reduced_future: float,
    observability: float,
    packet_residual: float,
) -> float:
    """Return the max-plus power of U + N(P + Z + Omega R)."""
    n = _signed_power(normalization, "normalization power")
    u = _signed_power(upstream_bridge, "upstream bridge power")
    p = _signed_power(finite_prefix, "finite prefix power")
    z = _signed_power(reduced_future, "reduced future power")
    o = _signed_power(observability, "observability power")
    r = _signed_power(packet_residual, "packet residual power")
    return max(0.0, u, n + p, n + z, n + o + r)


def two_side_hardy_power(left: float, right: float) -> float:
    return _growth_power(left, "left Hardy power") + _growth_power(right, "right Hardy power")


def quarter_power_margin(total_hardy_power: float) -> float:
    return 0.25 - _growth_power(total_hardy_power, "total Hardy power")


def rh49_full_range_green(total_hardy_power: float) -> bool:
    return quarter_power_margin(total_hardy_power) >= 0.0


def stress_mesh_decay_power(total_hardy_power: float) -> float:
    """Power of sigma on n=sigma^-2 L(sigma) in the RH-54 envelope."""
    return 0.75 - _growth_power(total_hardy_power, "total Hardy power")


def identification_sigma_power(total_hardy_power: float, mesh_power: float) -> float:
    """Decay exponent for n=sigma^-mesh_power in n^-2 sigma^(-13/4-delta)."""
    mesh = _growth_power(mesh_power, "mesh power")
    total = _growth_power(total_hardy_power, "total Hardy power")
    return 2.0 * mesh - 3.25 - total


def zero_power_overheads(
    *,
    logarithmic_rank: bool,
    fixed_memory_depth: bool,
    fixed_endpoint_gate: bool,
    normalized_source: bool,
) -> bool:
    return bool(logarithmic_rank and fixed_memory_depth and fixed_endpoint_gate and normalized_source)
