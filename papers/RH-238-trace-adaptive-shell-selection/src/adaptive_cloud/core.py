"""Shell-complete cloud selection by a finite logarithmic trace tolerance."""

from __future__ import annotations

import numpy as np


def extracted_moments(
    full_traces: np.ndarray,
    perron: complex,
    parity: complex,
    cloud: np.ndarray,
) -> np.ndarray:
    traces = np.asarray(full_traces, dtype=complex).reshape(-1)
    roots = np.asarray(cloud, dtype=complex).reshape(-1)
    orders = np.arange(1, traces.size + 1)
    return traces - complex(perron) ** orders - complex(parity) ** orders - np.asarray([
        np.sum(roots**order) for order in orders
    ])


def log_jet_norm(moments: np.ndarray, radius: float = 1.0) -> float:
    values = np.asarray(moments, dtype=complex).reshape(-1)
    disk = float(radius)
    if values.size < 2 or disk < 0.0:
        raise ValueError("orders through at least two and a nonnegative radius are required")
    orders = np.arange(2, values.size + 1)
    return float(np.sum(np.abs(values[1:]) * disk**orders / orders))


def shell_prefixes(
    shells: list[np.ndarray],
    *,
    minimum_rank: int = 1,
) -> list[np.ndarray]:
    minimum = int(minimum_rank)
    if minimum < 1:
        raise ValueError("minimum rank must be positive")
    prefixes: list[np.ndarray] = []
    roots: list[complex] = []
    for shell in shells:
        roots.extend(np.asarray(shell, dtype=complex).reshape(-1).tolist())
        if len(roots) >= minimum:
            prefixes.append(np.asarray(roots, dtype=complex))
    return prefixes


def first_admissible_prefix(
    shells: list[np.ndarray],
    full_traces: np.ndarray,
    perron: complex,
    parity: complex,
    tolerance: float,
    *,
    minimum_rank: int = 1,
    radius: float = 1.0,
) -> dict[str, object]:
    threshold = float(tolerance)
    if threshold < 0.0:
        raise ValueError("tolerance must be nonnegative")
    rows = []
    for cloud in shell_prefixes(shells, minimum_rank=minimum_rank):
        moments = extracted_moments(full_traces, perron, parity, cloud)
        rows.append({
            "cloud": cloud,
            "moments": moments,
            "jet_norm": log_jet_norm(moments, radius),
        })
    admissible = [row for row in rows if row["jet_norm"] <= threshold]
    return {
        "rows": rows,
        "admissible_rows": admissible,
        "selected": admissible[0] if admissible else None,
    }


def complex_payload(values: np.ndarray) -> dict[str, list[float]]:
    data = np.asarray(values, dtype=complex).reshape(-1)
    return {
        "real": [float(value.real) for value in data],
        "imag": [float(value.imag) for value in data],
    }
