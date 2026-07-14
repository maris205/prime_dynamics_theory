"""Compressed critical-branch cycles and dense endpoint returns."""

from __future__ import annotations

from typing import Callable

import numpy as np


VectorOperator = Callable[[np.ndarray], np.ndarray]


def dense_matrix(operator: VectorOperator, dimension: int) -> np.ndarray:
    """Materialize a small matrix-free operator column by column."""

    columns = []
    for index in range(int(dimension)):
        vector = np.zeros(int(dimension), dtype=np.float64)
        vector[index] = 1.0
        columns.append(np.asarray(operator(vector)))
    return np.column_stack(columns)


def branch_profile_basis(
    profile: np.ndarray,
    left_mask: np.ndarray,
    right_mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Normalize the two disjoint lobes of one critical pullback profile."""

    source = np.asarray(profile, dtype=np.float64)
    basis = []
    for mask in (left_mask, right_mask):
        vector = source.copy()
        vector[~np.asarray(mask, dtype=bool)] = 0.0
        norm = np.linalg.norm(vector)
        if norm == 0.0:
            raise ValueError("critical branch profile has zero mass")
        basis.append(vector / norm)
    return basis[0], basis[1]


def compressed_branch_cycle(
    two_step: VectorOperator,
    intermediate_masks: list[np.ndarray],
    branch_basis: tuple[np.ndarray, np.ndarray],
) -> np.ndarray:
    """Compress one full cycle from the final two-branch slice to itself."""

    if len(intermediate_masks) < 1:
        raise ValueError("at least the endpoint mask is required")
    both = (np.abs(branch_basis[0]) > 0.0) | (np.abs(branch_basis[1]) > 0.0)
    columns: list[list[complex]] = []
    for vector in branch_basis:
        result = np.asarray(vector).copy()
        for index in range(len(intermediate_masks) - 1, -1, -1):
            result = np.asarray(two_step(result))
            result[~intermediate_masks[index]] = 0.0
        result = np.asarray(two_step(result))
        result[~both] = 0.0
        columns.append([np.vdot(test, result) for test in branch_basis])
    return np.asarray(columns, dtype=np.complex128).T
