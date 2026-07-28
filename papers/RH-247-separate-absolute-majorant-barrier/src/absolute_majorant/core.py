"""Absolute-value-before-cancellation diagnostics."""

from __future__ import annotations

import numpy as np


def separate_absolute_majorant(
    full_traces: np.ndarray,
    perron: complex,
    parity: complex,
    cloud: np.ndarray,
) -> np.ndarray:
    """Add absolute values of physical, atomic, and cloud sectors."""

    traces = np.asarray(full_traces, dtype=complex).reshape(-1)
    roots = np.asarray(cloud, dtype=complex).reshape(-1)
    orders = np.arange(1, traces.size + 1)
    cloud_mass = np.asarray([
        np.sum(np.abs(roots) ** order) for order in orders
    ])
    return np.abs(traces) + abs(complex(perron)) ** orders + abs(complex(parity)) ** orders + cloud_mass


def root_rates(majorant: np.ndarray) -> np.ndarray:
    values = np.asarray(majorant, dtype=float).reshape(-1)
    if values.size < 2 or np.any(values < 0.0):
        raise ValueError("a nonnegative majorant with at least two orders is required")
    orders = np.arange(1, values.size + 1)
    return values[1:] ** (1.0 / orders[1:])


def cancellation_gain(majorant: np.ndarray, residual: np.ndarray) -> np.ndarray:
    upper = np.asarray(majorant, dtype=float).reshape(-1)
    target = np.abs(np.asarray(residual, dtype=complex).reshape(-1))
    if upper.size != target.size:
        raise ValueError("majorant and residual lengths must agree")
    if np.any(target <= 0.0):
        raise ValueError("gain is undefined at a zero residual")
    return upper / target
