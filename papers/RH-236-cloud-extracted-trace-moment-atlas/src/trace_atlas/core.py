"""Sparse power traces and cloud-extracted moment jets."""

from __future__ import annotations

import numpy as np


def sparse_power_traces(matrix, maximum_order: int) -> np.ndarray:
    order = int(maximum_order)
    if order < 1:
        raise ValueError("a positive maximum order is required")
    operator = matrix.tocsr()
    power = operator.copy()
    traces: list[complex] = []
    for current in range(1, order + 1):
        if current > 1:
            power = (power @ operator).tocsr()
            power.eliminate_zeros()
        traces.append(complex(power.diagonal().sum()))
    return np.asarray(traces, dtype=complex)


def extracted_trace_moments(
    full_traces: np.ndarray,
    perron: complex,
    parity: complex,
    cloud: np.ndarray,
) -> np.ndarray:
    traces = np.asarray(full_traces, dtype=complex).reshape(-1)
    roots = np.asarray(cloud, dtype=complex).reshape(-1)
    orders = np.arange(1, traces.size + 1)
    cloud_powers = np.asarray([np.sum(roots**order) for order in orders])
    return traces - complex(perron) ** orders - complex(parity) ** orders - cloud_powers


def weighted_jet_norm(
    moments: np.ndarray,
    *,
    radius: float = 1.0,
    first_order: int = 2,
) -> float:
    values = np.asarray(moments, dtype=complex).reshape(-1)
    first = int(first_order)
    if first < 1 or first > values.size:
        raise ValueError("invalid first order")
    disk = float(radius)
    if disk < 0.0:
        raise ValueError("radius must be nonnegative")
    orders = np.arange(first, values.size + 1)
    return float(np.sum(np.abs(values[first - 1 :]) * disk**orders / orders))


def complex_payload(values: np.ndarray) -> dict[str, list[float]]:
    data = np.asarray(values, dtype=complex).reshape(-1)
    return {
        "real": [float(value.real) for value in data],
        "imag": [float(value.imag) for value in data],
    }
