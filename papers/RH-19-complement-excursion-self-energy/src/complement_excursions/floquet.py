"""Finite-dimensional time lifts and exact Feshbach maps."""

from __future__ import annotations

import numpy as np


def cyclic_time_lift(operator: np.ndarray, period: int) -> np.ndarray:
    r"""Return ``C`` with ``(Cv)_j = T v_(j+1)``."""

    matrix = np.asarray(operator, dtype=np.complex128)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("operator must be square")
    period = int(period)
    if period < 1:
        raise ValueError("period must be positive")
    dimension = matrix.shape[0]
    lifted = np.zeros((period * dimension, period * dimension), dtype=np.complex128)
    for index in range(period):
        row = slice(index * dimension, (index + 1) * dimension)
        next_index = (index + 1) % period
        column = slice(next_index * dimension, (next_index + 1) * dimension)
        lifted[row, column] = matrix
    return lifted


def time_fourier_blocks(operator: np.ndarray, period: int) -> list[np.ndarray]:
    """Return the exact Fourier-sector blocks of the cyclic time lift."""

    matrix = np.asarray(operator, dtype=np.complex128)
    roots = np.exp(2j * np.pi * np.arange(int(period)) / int(period))
    return [root * matrix for root in roots]


def phase_projection(dimension: int, period: int, phase_index: int) -> np.ndarray:
    """Return the orthogonal projection onto one time-Fourier sector."""

    dimension = int(dimension)
    period = int(period)
    phase = np.exp(2j * np.pi * int(phase_index) / period)
    vector = phase ** np.arange(period) / np.sqrt(period)
    temporal = np.outer(vector, np.conjugate(vector))
    return np.kron(temporal, np.eye(dimension, dtype=np.complex128))


def feshbach_map(
    operator: np.ndarray,
    projection: np.ndarray,
    spectral_value: complex,
) -> tuple[np.ndarray, np.ndarray]:
    r"""Return the finite-dimensional Feshbach map and self-energy.

    The returned matrices act in an orthonormal basis for ``ran(P)``.
    """

    matrix = np.asarray(operator, dtype=np.complex128)
    projection = np.asarray(projection, dtype=np.complex128)
    if matrix.shape != projection.shape or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("operator and projection must be equal-size square matrices")
    values, vectors = np.linalg.eigh((projection + projection.conj().T) / 2.0)
    p_basis = vectors[:, values > 0.5]
    q_basis = vectors[:, values <= 0.5]
    cpp = p_basis.conj().T @ matrix @ p_basis
    cpq = p_basis.conj().T @ matrix @ q_basis
    cqp = q_basis.conj().T @ matrix @ p_basis
    cqq = q_basis.conj().T @ matrix @ q_basis
    resolvent = np.linalg.inv(complex(spectral_value) * np.eye(cqq.shape[0]) - cqq)
    self_energy = cpq @ resolvent @ cqp
    feshbach = complex(spectral_value) * np.eye(cpp.shape[0]) - cpp - self_energy
    return feshbach, self_energy
