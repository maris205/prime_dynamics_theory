"""Finite block-cyclic operators and their exact root rings."""

from __future__ import annotations

import numpy as np


def scalar_cyclic_matrix(weights: np.ndarray) -> np.ndarray:
    """Return the scalar weighted cyclic shift in backward-channel order."""

    values = np.asarray(weights, dtype=np.complex128)
    if values.ndim != 1 or values.size < 1:
        raise ValueError("weights must be a nonempty vector")
    matrix = np.zeros((values.size, values.size), dtype=np.complex128)
    columns = np.arange(values.size)
    matrix[columns, (columns + 1) % values.size] = values
    return matrix


def block_cyclic_matrix(channels: list[np.ndarray]) -> np.ndarray:
    r"""Assemble ``(Cv)_j=A_j v_(j+1)`` from finite channel matrices."""

    if not channels:
        raise ValueError("at least one channel is required")
    arrays = [np.asarray(channel, dtype=np.complex128) for channel in channels]
    dimensions = [array.shape[0] for array in arrays]
    for index, array in enumerate(arrays):
        expected_columns = dimensions[(index + 1) % len(arrays)]
        if array.ndim != 2 or array.shape[1] != expected_columns:
            raise ValueError("channel dimensions do not close cyclically")
    offsets = np.cumsum((0, *dimensions))
    matrix = np.zeros((offsets[-1], offsets[-1]), dtype=np.complex128)
    for index, array in enumerate(arrays):
        row = slice(offsets[index], offsets[index + 1])
        next_index = (index + 1) % len(arrays)
        column = slice(offsets[next_index], offsets[next_index + 1])
        matrix[row, column] = array
    return matrix


def return_product(channels: list[np.ndarray], base_index: int = 0) -> np.ndarray:
    """Return the full cyclic product acting on one selected component."""

    arrays = [np.asarray(channel, dtype=np.complex128) for channel in channels]
    count = len(arrays)
    base_index = int(base_index) % count
    product = np.eye(arrays[base_index].shape[0], dtype=np.complex128)
    for offset in range(count):
        index = (base_index + offset) % count
        product = product @ arrays[index]
    return product


def root_ring(return_eigenvalue: complex, period: int) -> np.ndarray:
    """Return all ``period`` roots of a nonzero return eigenvalue."""

    value = complex(return_eigenvalue)
    period = int(period)
    if value == 0.0 or period < 1:
        raise ValueError("return_eigenvalue must be nonzero and period positive")
    principal = np.exp(np.log(value) / period)
    return principal * np.exp(2j * np.pi * np.arange(period) / period)


def bipartite_root_ring(return_eigenvalue: complex, period: int) -> np.ndarray:
    """Return the ``2*period`` one-step roots of a component return value."""

    value = complex(return_eigenvalue)
    period = int(period)
    principal = np.exp(np.log(value) / (2 * period))
    return principal * np.exp(1j * np.pi * np.arange(2 * period) / period)
