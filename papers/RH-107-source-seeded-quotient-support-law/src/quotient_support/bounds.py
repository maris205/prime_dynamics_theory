"""Support-to-price bookkeeping for source-seeded weak-mode quotients."""

from __future__ import annotations

import math


def _finite_nonnegative(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def fourth_cross_ratio(singular_values: list[float] | tuple[float, ...]) -> float:
    """Return s_4/s_1 for a four-direction projected-cross spectrum."""
    values = [float(value) for value in singular_values]
    if len(values) < 4 or any(not math.isfinite(value) or value < 0.0 for value in values):
        raise ValueError("at least four finite nonnegative singular values are required")
    if values[0] <= 0.0:
        raise ValueError("leading singular value must be positive")
    return values[3] / values[0]


def weak_mode_event(singular_values: list[float] | tuple[float, ...], threshold: float) -> bool:
    """Return whether the max-width adaptive rule omits a direction."""
    cutoff = float(threshold)
    if not math.isfinite(cutoff) or cutoff <= 0.0:
        raise ValueError("threshold must be finite and positive")
    return fourth_cross_ratio(singular_values) < cutoff


def support_margin(ratio: float, threshold: float) -> float:
    value = _finite_nonnegative(ratio, "cross ratio")
    cutoff = float(threshold)
    if not math.isfinite(cutoff) or cutoff <= 0.0:
        raise ValueError("threshold must be finite and positive")
    return value / cutoff


def local_quotient_price(coupling: float, gap: float) -> float:
    cross = _finite_nonnegative(coupling, "coupling")
    spectral_gap = float(gap)
    if not math.isfinite(spectral_gap) or spectral_gap <= 0.0:
        raise ValueError("gap must be finite and positive")
    return math.nextafter(cross**2 / spectral_gap, math.inf)


def coarse_support_price_upper(event_count: int, propagation_factor: float, maximum_local_price: float) -> float:
    if int(event_count) < 0:
        raise ValueError("event count must be nonnegative")
    propagation = _finite_nonnegative(propagation_factor, "propagation factor")
    price = _finite_nonnegative(maximum_local_price, "maximum local price")
    return math.nextafter(int(event_count) * propagation * price, math.inf)


def finite_support_reduction(event_counts: list[int], fine_start: int) -> bool:
    """Check that all event counts from fine_start onward vanish."""
    start = int(fine_start)
    if start < 0 or start > len(event_counts):
        raise ValueError("fine start is outside the event-count array")
    return all(int(count) == 0 for count in event_counts[start:])
