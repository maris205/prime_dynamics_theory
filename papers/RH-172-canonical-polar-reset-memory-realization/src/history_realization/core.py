"""Finite-history Gram factorizations and their canonical polar packets."""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np


DEFAULT_ETA = 1.0 / 512.0


def _adjoint(matrix: np.ndarray) -> np.ndarray:
    return np.asarray(matrix).conj().T


def _validated_states(states: Sequence[np.ndarray]) -> tuple[np.ndarray, ...]:
    arrays = tuple(np.asarray(state) for state in states)
    if not arrays:
        raise ValueError("at least one state is required")
    shape = arrays[0].shape
    if len(shape) != 2 or any(array.shape != shape for array in arrays):
        raise ValueError("states must be nonempty matrices with one common shape")
    if any(float(np.linalg.norm(array, "fro")) == 0.0 for array in arrays):
        raise ValueError("zero states cannot be normalized")
    return arrays


def _validated_eta(eta: float) -> float:
    value = float(eta)
    if not 0.0 <= value < 1.0:
        raise ValueError("eta must lie in [0,1)")
    return value


def normalized_history_factor(
    states: Sequence[np.ndarray],
    *,
    eta: float = DEFAULT_ETA,
) -> np.ndarray:
    """Return F_t with blocks ordered from the current state to the seed."""
    arrays = _validated_states(states)
    decay = _validated_eta(eta)
    current = len(arrays) - 1
    blocks = []
    for index in range(current, -1, -1):
        state = arrays[index]
        weight = decay ** ((current - index) / 2.0)
        blocks.append(weight * state / np.linalg.norm(state, "fro"))
    return np.vstack(blocks)


def memory_gram(
    states: Sequence[np.ndarray],
    *,
    eta: float = DEFAULT_ETA,
) -> np.ndarray:
    """Return the recursive normalized memory Gram M_t."""
    arrays = _validated_states(states)
    decay = _validated_eta(eta)
    columns = arrays[0].shape[1]
    dtype = np.result_type(*arrays, np.float64)
    memory = np.zeros((columns, columns), dtype=dtype)
    for state in arrays:
        norm_squared = float(np.linalg.norm(state, "fro")) ** 2
        snapshot = _adjoint(state) @ state / norm_squared
        memory = snapshot + decay * memory
    return (memory + _adjoint(memory)) / 2.0


def top_packet(gram: np.ndarray, rank: int) -> tuple[np.ndarray, np.ndarray]:
    """Return descending selected eigenvalues and an orthonormal eigenframe."""
    matrix = np.asarray(gram)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("gram must be square")
    selected_rank = int(rank)
    if not 1 <= selected_rank <= matrix.shape[0]:
        raise ValueError("rank outside matrix dimension")
    hermitian = (matrix + _adjoint(matrix)) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    order = np.argsort(values)[::-1][:selected_rank]
    selected = np.asarray(values[order], dtype=float)
    if selected[-1] <= 0.0:
        raise ValueError("selected packet is not positive definite")
    return selected, vectors[:, order]


def polar_realization(
    factor: np.ndarray,
    packet: np.ndarray,
    *,
    tolerance: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the stable thin polar factor V and positive factor H of F U."""
    analysis = np.asarray(factor)
    frame = np.asarray(packet)
    if analysis.ndim != 2 or frame.ndim != 2 or analysis.shape[1] != frame.shape[0]:
        raise ValueError("factor and packet dimensions do not compose")
    image = analysis @ frame
    left, singular, right_adjoint = np.linalg.svd(image, full_matrices=False)
    threshold = tolerance
    if threshold is None:
        threshold = np.finfo(singular.dtype).eps * max(image.shape) * singular[0]
    if singular[-1] <= float(threshold):
        raise ValueError("packet image is numerically rank deficient")
    isometry = left @ right_adjoint
    positive = _adjoint(isometry) @ image
    return isometry, (positive + _adjoint(positive)) / 2.0


def spectral_formula_realization(
    factor: np.ndarray,
    packet: np.ndarray,
    eigenvalues: np.ndarray,
) -> np.ndarray:
    """Evaluate the exact formula F U Lambda^{-1/2} directly."""
    values = np.asarray(eigenvalues, dtype=float)
    if values.ndim != 1 or np.any(values <= 0.0):
        raise ValueError("eigenvalues must be a positive vector")
    frame = np.asarray(packet)
    if frame.shape[1] != values.size:
        raise ValueError("one eigenvalue is required per packet column")
    return (np.asarray(factor) @ frame) / np.sqrt(values)[None, :]


def subspace_distance(first: np.ndarray, second: np.ndarray) -> float:
    """Operator distance between equal-rank orthogonal range projections."""
    left = np.asarray(first)
    right = np.asarray(second)
    if left.ndim != 2 or right.ndim != 2 or left.shape != right.shape:
        raise ValueError("frames must have one common shape")
    # The residual form avoids the square-root cancellation in
    # sqrt(1-s_min(U^*V)^2) when the two spaces agree to machine precision.
    right_residual = right - left @ (_adjoint(left) @ right)
    left_residual = left - right @ (_adjoint(right) @ left)
    return max(
        float(np.linalg.norm(right_residual, 2)),
        float(np.linalg.norm(left_residual, 2)),
    )
