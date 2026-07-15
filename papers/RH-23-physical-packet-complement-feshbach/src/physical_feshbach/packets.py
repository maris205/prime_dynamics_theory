"""Packet trial spaces assembled from propagated critical-branch histories."""

from __future__ import annotations

import numpy as np


def _normalized(vector: np.ndarray) -> np.ndarray:
    values = np.asarray(vector, dtype=np.float64).reshape(-1)
    norm = np.linalg.norm(values)
    if norm == 0.0:
        raise ValueError("packet history must be nonzero")
    return values / norm


def bright_history_trial(histories: tuple[np.ndarray, ...]) -> np.ndarray:
    """Return one bright packet per regular slice and two critical branches.

    Each regular-slice column is the normalized sum of the separately
    normalized left- and right-label histories.  The final two columns retain
    the disjoint critical branch labels.
    """

    if len(histories) < 2:
        raise ValueError("at least one regular slice and one critical slice are required")
    arrays = [np.asarray(history, dtype=np.float64) for history in histories]
    ambient = arrays[0].shape[0]
    if any(array.shape != (ambient, 2) for array in arrays):
        raise ValueError("every history must have two equal-length columns")
    columns: list[np.ndarray] = []
    for history in arrays[:-1]:
        bright = _normalized(history[:, 0]) + _normalized(history[:, 1])
        columns.append(_normalized(bright))
    columns.extend((_normalized(arrays[-1][:, 0]), _normalized(arrays[-1][:, 1])))
    return np.column_stack(columns)


def critical_bright_trial(histories: tuple[np.ndarray, ...]) -> np.ndarray:
    """Return one merged bright packet at every slice, including critical."""

    arrays = [np.asarray(history, dtype=np.float64) for history in histories]
    if len(arrays) < 2:
        raise ValueError("at least two packet slices are required")
    ambient = arrays[0].shape[0]
    if any(array.shape != (ambient, 2) for array in arrays):
        raise ValueError("every history must have two equal-length columns")
    columns = []
    for history in arrays:
        bright = _normalized(history[:, 0]) + _normalized(history[:, 1])
        columns.append(_normalized(bright))
    return np.column_stack(columns)


def label_resolved_trial(histories: tuple[np.ndarray, ...]) -> np.ndarray:
    """Retain both propagated branch labels at every packet slice."""

    arrays = [np.asarray(history, dtype=np.float64) for history in histories]
    if len(arrays) < 2:
        raise ValueError("at least two packet slices are required")
    ambient = arrays[0].shape[0]
    if any(array.shape != (ambient, 2) for array in arrays):
        raise ValueError("every history must have two equal-length columns")
    columns = []
    for history in arrays:
        columns.extend((_normalized(history[:, 0]), _normalized(history[:, 1])))
    return np.column_stack(columns)


def single_label_trial(
    histories: tuple[np.ndarray, ...],
    label: int = 0,
) -> np.ndarray:
    """Retain one propagated branch label at every slice."""

    if int(label) not in (0, 1):
        raise ValueError("label must be zero or one")
    arrays = [np.asarray(history, dtype=np.float64) for history in histories]
    if len(arrays) < 2:
        raise ValueError("at least two packet slices are required")
    ambient = arrays[0].shape[0]
    if any(array.shape != (ambient, 2) for array in arrays):
        raise ValueError("every history must have two equal-length columns")
    return np.column_stack([_normalized(array[:, int(label)]) for array in arrays])
