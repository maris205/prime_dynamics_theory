"""Operator-norm diagnostics for powers of an orthogonal quotient block."""

from __future__ import annotations

import numpy as np
from scipy import linalg


def power_norm_profile(matrix: np.ndarray, maximum_order: int) -> dict[str, object]:
    operator = np.asarray(matrix, dtype=complex)
    maximum = int(maximum_order)
    if operator.ndim != 2 or operator.shape[0] != operator.shape[1] or maximum < 1:
        raise ValueError("a square matrix and positive maximum order are required")
    current = np.eye(operator.shape[0], dtype=complex)
    norms = []
    last_trace_norm = 0.0
    for order in range(1, maximum + 1):
        current = current @ operator
        singular = linalg.svdvals(current, check_finite=False) if current.size else np.asarray([])
        norms.append(float(singular[0]) if singular.size else 0.0)
        if order == maximum:
            last_trace_norm = float(np.sum(singular))
    first = next((order for order, value in enumerate(norms, start=1) if value < 1.0), None)
    return {
        "operator_norms": norms,
        "first_contractive_depth": first,
        "last_trace_norm": last_trace_norm,
    }


def block_root_rate(power_norm: float, order: int) -> float:
    value = float(power_norm)
    depth = int(order)
    if value < 0.0 or depth < 1:
        raise ValueError("a nonnegative norm and positive order are required")
    return float(value ** (1.0 / depth))
