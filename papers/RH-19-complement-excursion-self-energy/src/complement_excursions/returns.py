"""Matrix-free restricted and unrestricted endpoint returns."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


VectorOperator = Callable[[np.ndarray], np.ndarray]


@dataclass(frozen=True)
class PowerEigenpair:
    """Principal power-iteration result for a positive return operator."""

    eigenvalue: float
    vector: np.ndarray
    residual: float
    iterations: int


def power_eigenpair(
    operator: VectorOperator,
    initial: np.ndarray,
    *,
    iterations: int = 12,
) -> PowerEigenpair:
    """Compute a normalized principal eigenpair of a positive operator."""

    vector = np.asarray(initial, dtype=np.float64).copy()
    norm = np.linalg.norm(vector)
    if norm == 0.0:
        raise ValueError("initial vector must be nonzero")
    vector /= norm
    for _ in range(int(iterations)):
        updated = np.asarray(operator(vector), dtype=np.float64)
        norm = np.linalg.norm(updated)
        if norm == 0.0:
            raise RuntimeError("return operator annihilated the iterate")
        vector = updated / norm
    updated = np.asarray(operator(vector), dtype=np.float64)
    eigenvalue = float(np.vdot(vector, updated).real)
    residual = float(
        np.linalg.norm(updated - eigenvalue * vector) / np.linalg.norm(updated)
    )
    return PowerEigenpair(eigenvalue, vector, residual, int(iterations))


def apply_restricted_return(
    two_step: VectorOperator,
    masks: list[np.ndarray],
    endpoint_indices: np.ndarray,
    vector: np.ndarray,
    *,
    dimension: int,
) -> np.ndarray:
    """Apply the all-stay return through a prescribed cyclic mask sequence."""

    result = np.zeros(int(dimension), dtype=np.float64)
    result[np.asarray(endpoint_indices)] = np.asarray(vector, dtype=np.float64)
    for index in range(len(masks) - 1, -1, -1):
        result = np.asarray(two_step(result), dtype=np.float64)
        result[~masks[index]] = 0.0
    return result[np.asarray(endpoint_indices)]


def apply_endpoint_return(
    two_step: VectorOperator,
    endpoint_mask: np.ndarray,
    endpoint_indices: np.ndarray,
    vector: np.ndarray,
    *,
    period: int,
    dimension: int,
) -> np.ndarray:
    """Apply the unrestricted finite-horizon return to the endpoint window."""

    result = np.zeros(int(dimension), dtype=np.float64)
    result[np.asarray(endpoint_indices)] = np.asarray(vector, dtype=np.float64)
    for _ in range(int(period)):
        result = np.asarray(two_step(result), dtype=np.float64)
    result[~endpoint_mask] = 0.0
    return result[np.asarray(endpoint_indices)]


def critical_branch_masks(
    grid: np.ndarray,
    base_masks: list[np.ndarray],
    final_center: float,
    final_width: float,
    *,
    window_multiple: float,
    partition: float,
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    """Return left, right-sibling, and branch-complete mask sequences."""

    nodes = np.asarray(grid, dtype=np.float64)
    left = [np.asarray(mask, dtype=bool).copy() for mask in base_masks]
    both = [mask.copy() for mask in left]
    both[-1] = (
        np.abs(nodes - float(final_center))
        <= float(window_multiple) * float(final_width)
    )
    right = [mask.copy() for mask in left]
    right[-1] = both[-1] & (nodes >= float(partition))
    left[-1] = both[-1] & (nodes < float(partition))
    return left, right, both
