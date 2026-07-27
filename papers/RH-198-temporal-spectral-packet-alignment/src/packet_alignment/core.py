"""Graph coordinates and finite decay diagnostics for packet alignment."""

from __future__ import annotations

import math
import numpy as np


def graph_tangent(exact_basis: np.ndarray, approximate_basis: np.ndarray) -> dict[str, float]:
    exact = np.linalg.qr(np.asarray(exact_basis, dtype=complex), mode="reduced")[0]
    approximate = np.linalg.qr(np.asarray(approximate_basis, dtype=complex), mode="reduced")[0]
    if exact.shape[1] != approximate.shape[1]:
        raise ValueError("subspaces must have equal dimension")
    overlap = exact.conj().T @ approximate
    if np.linalg.matrix_rank(overlap) < overlap.shape[0]:
        return {"maximum_tangent": math.inf, "maximum_sine": 1.0, "minimum_cosine": 0.0}
    residual = approximate - exact @ overlap
    graph = residual @ np.linalg.inv(overlap)
    tangent = float(np.linalg.norm(graph, 2))
    sine = tangent / math.sqrt(1.0 + tangent**2)
    return {
        "maximum_tangent": tangent,
        "maximum_sine": sine,
        "minimum_cosine": 1.0 / math.sqrt(1.0 + tangent**2),
    }


def log_linear_decay(indices, values) -> dict[str, float]:
    x = np.asarray(list(indices), dtype=float)
    y = np.asarray(list(values), dtype=float)
    if x.size < 2 or x.size != y.size or np.min(y) <= 0.0:
        raise ValueError("positive paired sequences of length at least two are required")
    slope, intercept = np.polyfit(x, np.log(y), 1)
    predicted = intercept + slope * x
    denominator = float(np.sum((np.log(y) - np.mean(np.log(y))) ** 2))
    r_squared = 1.0 if denominator == 0.0 else 1.0 - float(np.sum((np.log(y) - predicted) ** 2)) / denominator
    return {
        "log_slope": float(slope),
        "log_intercept": float(intercept),
        "per_step_ratio": float(np.exp(slope)),
        "r_squared": float(r_squared),
        "initial": float(y[0]),
        "final": float(y[-1]),
        "final_over_initial": float(y[-1] / y[0]),
    }


def endpoint_is_minimum(values, tolerance: float = 1e-14) -> bool:
    data = np.asarray(list(values), dtype=float)
    return bool(data[-1] <= float(np.min(data)) + float(tolerance))
