"""Finite-dimensional realizations of the orthogonal quotient theorem."""

from __future__ import annotations

import numpy as np
from scipy import linalg


def ordered_schur_quotient(
    matrix: np.ndarray,
    radial_cutoff: float,
) -> dict[str, np.ndarray | int]:
    """Put eigenvalues outside a radial cutoff in the leading Schur block."""

    operator = np.asarray(matrix, dtype=complex)
    if operator.ndim != 2 or operator.shape[0] != operator.shape[1]:
        raise ValueError("a square matrix is required")
    cutoff = float(radial_cutoff)
    if cutoff < 0.0:
        raise ValueError("the cutoff must be nonnegative")
    triangular, unitary, selected_dimension = linalg.schur(
        operator,
        output="complex",
        sort=lambda value: abs(value) > cutoff,
    )
    count = int(selected_dimension)
    return {
        "triangular": triangular,
        "unitary": unitary,
        "selected_dimension": count,
        "selected_block": triangular[:count, :count],
        "cross_block": triangular[:count, count:],
        "quotient_block": triangular[count:, count:],
    }


def power_traces(matrix: np.ndarray, maximum_order: int) -> np.ndarray:
    """Return traces of powers one through maximum_order."""

    operator = np.asarray(matrix, dtype=complex)
    if operator.ndim != 2 or operator.shape[0] != operator.shape[1]:
        raise ValueError("a square matrix is required")
    maximum = int(maximum_order)
    if maximum < 1:
        raise ValueError("maximum_order must be positive")
    current = np.eye(operator.shape[0], dtype=complex)
    traces = []
    for _ in range(maximum):
        current = current @ operator
        traces.append(np.trace(current))
    return np.asarray(traces, dtype=complex)


def selected_quotient_trace_partition(
    triangular: np.ndarray,
    selected_dimension: int,
    maximum_order: int,
) -> dict[str, np.ndarray]:
    """Audit the exact block-triangular trace partition."""

    block = np.asarray(triangular, dtype=complex)
    count = int(selected_dimension)
    if block.ndim != 2 or block.shape[0] != block.shape[1]:
        raise ValueError("a square triangular matrix is required")
    if count < 0 or count > block.shape[0]:
        raise ValueError("invalid selected dimension")
    full = power_traces(block, maximum_order)
    selected = power_traces(block[:count, :count], maximum_order)
    quotient = power_traces(block[count:, count:], maximum_order)
    return {
        "full": full,
        "selected": selected,
        "quotient": quotient,
        "partition_error": full - selected - quotient,
    }


def riesz_projection_norm_2x2(
    selected_eigenvalue: complex,
    quotient_eigenvalue: complex,
    coupling: complex,
) -> float:
    """Euclidean norm of the selected spectral projection in the 2x2 model."""

    gap = complex(selected_eigenvalue) - complex(quotient_eigenvalue)
    if gap == 0.0:
        raise ValueError("the eigenvalues must be distinct")
    ratio = abs(complex(coupling) / gap)
    return float(np.sqrt(1.0 + ratio**2))
