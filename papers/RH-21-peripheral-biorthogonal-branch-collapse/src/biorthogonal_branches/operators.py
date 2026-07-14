"""Matrix-free propagation and reduction of two critical branch histories."""

from __future__ import annotations

from typing import Callable

import numpy as np


VectorOperator = Callable[[np.ndarray], np.ndarray]


def _branch_columns(branch_basis: tuple[np.ndarray, np.ndarray] | np.ndarray) -> np.ndarray:
    if isinstance(branch_basis, tuple):
        values = np.column_stack(branch_basis)
    else:
        values = np.asarray(branch_basis)
    if values.ndim != 2 or values.shape[1] != 2:
        raise ValueError("the branch synthesis must have exactly two columns")
    return values.copy()


def propagate_branch_histories(
    two_step: VectorOperator,
    intermediate_masks: list[np.ndarray],
    branch_basis: tuple[np.ndarray, np.ndarray] | np.ndarray,
) -> tuple[np.ndarray, ...]:
    """Propagate both critical branches to every earlier packet slice.

    The returned tuple is indexed in physical slice order: index zero is the
    endpoint history and the final index is the original critical pair.
    """

    if not intermediate_masks:
        raise ValueError("at least the endpoint mask is required")
    histories: list[np.ndarray | None] = [None] * (len(intermediate_masks) + 1)
    current = _branch_columns(branch_basis)
    histories[-1] = current.copy()
    for index in range(len(intermediate_masks) - 1, -1, -1):
        current = np.asarray(two_step(current))
        current[~np.asarray(intermediate_masks[index], dtype=bool), :] = 0.0
        histories[index] = current.copy()
    return tuple(np.asarray(history) for history in histories)


def close_branch_histories(
    two_step: VectorOperator,
    critical_mask: np.ndarray,
    endpoint_histories: np.ndarray,
) -> np.ndarray:
    """Apply the final endpoint-to-critical channel to two histories."""

    values = _branch_columns(endpoint_histories)
    result = np.asarray(two_step(values))
    result[~np.asarray(critical_mask, dtype=bool), :] = 0.0
    return result


def reduced_branch_cycle(
    two_step: VectorOperator,
    intermediate_masks: list[np.ndarray],
    critical_mask: np.ndarray,
    synthesis: np.ndarray,
    analysis: np.ndarray,
) -> np.ndarray:
    """Return the 2x2 cycle compressed by supplied synthesis/analysis maps."""

    histories = propagate_branch_histories(
        two_step, intermediate_masks, np.asarray(synthesis)
    )
    closed = close_branch_histories(two_step, critical_mask, histories[0])
    test = np.asarray(analysis)
    if test.ndim != 2 or test.shape[0] != 2 or test.shape[1] != closed.shape[0]:
        raise ValueError("analysis must have shape (2, ambient dimension)")
    return np.asarray(test @ closed)
