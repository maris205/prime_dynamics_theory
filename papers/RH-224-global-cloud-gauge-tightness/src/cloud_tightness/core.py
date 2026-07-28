"""Moment identities and tightness bounds for globally normalized clouds."""

from __future__ import annotations

import math

import numpy as np


def centered_rms_normalize(values: np.ndarray) -> tuple[np.ndarray, complex, float]:
    roots = np.asarray(values, dtype=complex).reshape(-1)
    if roots.size < 2:
        raise ValueError("at least two roots are required")
    center = complex(np.mean(roots))
    centered = roots - center
    radius = float(np.sqrt(np.mean(np.abs(centered) ** 2)))
    if radius <= np.finfo(float).tiny:
        raise ValueError("the RMS radius is zero")
    return centered / radius, center, radius


def empirical_moments(values: np.ndarray) -> dict[str, complex | float]:
    roots = np.asarray(values, dtype=complex).reshape(-1)
    return {
        "mean": complex(np.mean(roots)),
        "second_absolute_moment": float(np.mean(np.abs(roots) ** 2)),
        "fourth_absolute_moment": float(np.mean(np.abs(roots) ** 4)),
        "maximum_modulus": float(np.max(np.abs(roots))),
    }


def empirical_tail_mass(values: np.ndarray, radius: float) -> float:
    threshold = float(radius)
    if threshold <= 0.0:
        raise ValueError("radius must be positive")
    roots = np.asarray(values, dtype=complex).reshape(-1)
    return float(np.mean(np.abs(roots) > threshold))


def second_moment_tail_bound(radius: float, moment: float = 1.0) -> float:
    threshold = float(radius)
    if threshold <= 0.0:
        raise ValueError("radius must be positive")
    return min(1.0, float(moment) / threshold**2)


def tightness_radius(epsilon: float, moment: float = 1.0) -> float:
    tolerance = float(epsilon)
    if not 0.0 < tolerance < 1.0:
        raise ValueError("epsilon must lie in (0,1)")
    return math.sqrt(float(moment) / tolerance)
