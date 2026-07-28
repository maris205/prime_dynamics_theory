"""Finite anchored scans over shell-complete cloud prefixes."""

from __future__ import annotations

import numpy as np


def extracted_moments(
    full_traces: np.ndarray,
    perron: complex,
    parity: complex,
    cloud: np.ndarray,
) -> np.ndarray:
    """Return orders 1 through N after subtracting three spectral sectors."""

    traces = np.asarray(full_traces, dtype=complex).reshape(-1)
    roots = np.asarray(cloud, dtype=complex).reshape(-1)
    orders = np.arange(1, traces.size + 1)
    cloud_powers = np.asarray([np.sum(roots**order) for order in orders])
    return traces - complex(perron) ** orders - complex(parity) ** orders - cloud_powers


def anchored_log_jet_distance(
    moments: np.ndarray,
    target_orders_2_to_n: np.ndarray,
    radius: float = 1.0,
) -> float:
    """Weighted logarithmic distance from a residual jet to its anchor."""

    values = np.asarray(moments, dtype=complex).reshape(-1)
    target = np.asarray(target_orders_2_to_n, dtype=complex).reshape(-1)
    disk = float(radius)
    if values.size < 2 or target.size != values.size - 1 or disk < 0.0:
        raise ValueError("target must cover orders 2 through N and radius must be nonnegative")
    orders = np.arange(2, values.size + 1)
    return float(np.sum(np.abs(values[1:] - target) * disk**orders / orders))


def shell_prefixes(
    shells: list[np.ndarray],
    *,
    minimum_rank: int = 1,
) -> list[np.ndarray]:
    """Return every shell-complete prefix meeting the rank floor."""

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


def scan_anchored_prefixes(
    shells: list[np.ndarray],
    full_traces: np.ndarray,
    perron: complex,
    parity: complex,
    target_orders_2_to_n: np.ndarray,
    tolerance: float,
    *,
    minimum_rank: int = 1,
    radius: float = 1.0,
) -> dict[str, object]:
    """Scan the frozen prefix class and return all and admissible rows."""

    threshold = float(tolerance)
    if threshold < 0.0:
        raise ValueError("tolerance must be nonnegative")
    rows = []
    for cloud in shell_prefixes(shells, minimum_rank=minimum_rank):
        moments = extracted_moments(full_traces, perron, parity, cloud)
        rows.append({
            "cloud": cloud,
            "moments": moments,
            "distance": anchored_log_jet_distance(
                moments,
                target_orders_2_to_n,
                radius,
            ),
        })
    admissible = [row for row in rows if row["distance"] <= threshold]
    best = min(rows, key=lambda row: row["distance"]) if rows else None
    return {
        "rows": rows,
        "admissible_rows": admissible,
        "selected": admissible[0] if admissible else None,
        "best": best,
    }


def disjoint_ball_margin(target_norm: float, tolerance: float) -> float:
    """Positive exactly when equal-radius zero and anchor balls are disjoint."""

    anchor = float(target_norm)
    threshold = float(tolerance)
    if anchor < 0.0 or threshold < 0.0:
        raise ValueError("norm and tolerance must be nonnegative")
    return anchor - 2.0 * threshold


def complex_payload(values: np.ndarray) -> dict[str, list[float]]:
    data = np.asarray(values, dtype=complex).reshape(-1)
    return {
        "real": [float(value.real) for value in data],
        "imag": [float(value.imag) for value in data],
    }
