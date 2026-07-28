"""All-order geometric trace envelopes for regularized determinants."""

from __future__ import annotations

import math
import numpy as np


def geometric_log_bound(amplitude: float, rate: float, radius: float) -> float:
    size = float(amplitude)
    q = float(rate)
    disk = float(radius)
    if size < 0.0 or q < 0.0 or disk < 0.0:
        raise ValueError("bounds must be nonnegative")
    if q * disk >= 1.0:
        raise ValueError("the geometric envelope does not converge on this disk")
    return float(size * (q * disk) ** 2 / (2.0 * (1.0 - q * disk)))


def observed_unit_amplitude_rate(orders: np.ndarray, moments: np.ndarray) -> float:
    n = np.asarray(orders, dtype=int)
    values = np.asarray(moments, dtype=float)
    if n.shape != values.shape or np.min(n) < 1 or np.min(values) < 0.0:
        raise ValueError("nonnegative moments at positive orders are required")
    return float(np.max(values ** (1.0 / n)))


def finite_log_majorant(orders: np.ndarray, moments: np.ndarray, radius: float = 1.0) -> float:
    n = np.asarray(orders, dtype=int)
    values = np.asarray(moments, dtype=float)
    disk = float(radius)
    if n.shape != values.shape or np.min(n) < 1 or np.min(values) < 0.0 or disk < 0.0:
        raise ValueError("valid paired orders and moments are required")
    return float(np.sum(values * disk**n / n))
