"""Conditioned Gaussian--quadratic profile at the critical return."""

from __future__ import annotations

import numpy as np
from scipy.special import ndtr


def critical_geometry(
    coordinate: np.ndarray | float,
    clearance_ratio: float,
    u: float,
) -> tuple[np.ndarray, np.ndarray]:
    r"""Return ``A=(sqrt(d)-2u q)^2`` and ``B=d-A``."""

    q = np.asarray(coordinate, dtype=np.float64)
    d = float(clearance_ratio)
    u = float(u)
    if d <= 0.0:
        raise ValueError("clearance_ratio must be positive")
    a_value = (np.sqrt(d) - 2.0 * u * q) ** 2
    return a_value, d - a_value


def conditioned_critical_profile(
    coordinate: np.ndarray | float,
    clearance_ratio: float,
    endpoint_width: float,
    u: float,
) -> np.ndarray:
    r"""Evaluate the exact limiting conditioned critical pullback profile."""

    width = float(endpoint_width)
    if width <= 0.0:
        raise ValueError("endpoint_width must be positive")
    a_value, b_value = critical_geometry(coordinate, clearance_ratio, u)
    variance = 1.0 + width * width
    argument = (a_value + b_value / variance) * np.sqrt(variance) / width
    base = (
        width
        / np.sqrt(variance)
        * np.exp(-0.5 * b_value * b_value / variance)
    )
    return base * ndtr(argument) / ndtr(a_value)


def unconditioned_critical_profile(
    coordinate: np.ndarray | float,
    clearance_ratio: float,
    endpoint_width: float,
    u: float,
) -> np.ndarray:
    """Evaluate the Gaussian--quadratic profile without state conditioning."""

    width = float(endpoint_width)
    a_value, b_value = critical_geometry(coordinate, clearance_ratio, u)
    del a_value
    variance = 1.0 + width * width
    return width / np.sqrt(variance) * np.exp(-0.5 * b_value**2 / variance)


def affine_critical_profile(
    coordinate: np.ndarray | float,
    clearance_ratio: float,
    endpoint_width: float,
    u: float,
) -> np.ndarray:
    """Return the purely affine Gaussian approximation at the selected lobe."""

    q = np.asarray(coordinate, dtype=np.float64)
    d = float(clearance_ratio)
    width = float(endpoint_width)
    variance = 1.0 + width * width
    linear_defect = 4.0 * float(u) * np.sqrt(d) * q
    return width / np.sqrt(variance) * np.exp(
        -0.5 * linear_defect**2 / variance
    )


def critical_branch_midpoint(clearance_ratio: float, u: float) -> float:
    r"""Return the scaled critical partition ``sqrt(d)/(2u)``."""

    d = float(clearance_ratio)
    if d <= 0.0:
        raise ValueError("clearance_ratio must be positive")
    return float(np.sqrt(d) / (2.0 * float(u)))
