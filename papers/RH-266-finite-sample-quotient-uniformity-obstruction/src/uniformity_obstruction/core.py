"""Logical separation between finite pointwise data and uniform bounds."""

from __future__ import annotations


def triangular_bump(samples: tuple[float, ...], center: float, height: float):
    """Return a continuous bump vanishing at every finite sample point."""

    points = tuple(sorted(float(value) for value in samples))
    x0 = float(center)
    amplitude = float(height)
    if not points or x0 in points or amplitude <= 0.0:
        raise ValueError("need finite samples, an unsampled center, and positive height")
    distance = min(abs(x0 - value) for value in points)
    radius = 0.5 * distance

    def bump(value: float) -> float:
        scaled = abs(float(value) - x0) / radius
        return amplitude * max(0.0, 1.0 - scaled)

    return bump


def finite_sample_uniformity_status(
    *, sample_count: int, missing_archived_count: int, continuum_modulus_available: bool
) -> dict[str, object]:
    if sample_count < 0 or missing_archived_count < 0:
        raise ValueError("counts must be nonnegative")
    complete_archived = missing_archived_count == 0
    uniform = complete_archived and bool(continuum_modulus_available)
    return {
        "finite_sample_count": sample_count,
        "missing_archived_count": missing_archived_count,
        "all_archived_points_covered": complete_archived,
        "continuum_modulus_available": bool(continuum_modulus_available),
        "uniform_conclusion_available": uniform,
    }
