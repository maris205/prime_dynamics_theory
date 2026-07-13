"""Asymptotic dimension windows for logarithmic response scales."""

from __future__ import annotations

import numpy as np


def response_windows(T: np.ndarray | float, p: float) -> dict[str, np.ndarray]:
    """Return deterministic lower, weak upper, and strong upper scales."""
    T = np.asarray(T, dtype=np.float64)
    if np.any(T <= 1.0) or p <= 0.0:
        raise ValueError("T must exceed one and p must be positive")
    log_t = np.log(T)
    return {
        "deterministic_lower": log_t ** (p / 2.0),
        "weak_upper": T / log_t ** (2.0 * p),
        "strong_upper": np.sqrt(T) / log_t**p,
    }
