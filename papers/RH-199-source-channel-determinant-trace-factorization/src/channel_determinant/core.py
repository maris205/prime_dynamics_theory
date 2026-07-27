"""Finite determinant, trace, and residue-weighted moment identities."""

from __future__ import annotations

import numpy as np


def spectral_determinant(matrix: np.ndarray, z: complex) -> complex:
    values = np.asarray(matrix, dtype=complex)
    return complex(np.linalg.det(complex(z) * np.eye(values.shape[0]) - values))


def power_traces(matrix: np.ndarray, maximum_power: int) -> np.ndarray:
    values = np.asarray(matrix, dtype=complex)
    return np.asarray([np.trace(np.linalg.matrix_power(values, power)) for power in range(1, int(maximum_power) + 1)])


def channel_transfer(matrix: np.ndarray, source_coordinate: np.ndarray, observation_coordinate: np.ndarray, z: complex) -> complex:
    values = np.asarray(matrix, dtype=complex)
    source = np.asarray(source_coordinate, dtype=complex).reshape(-1)
    observation = np.asarray(observation_coordinate, dtype=complex).reshape(-1)
    state = np.linalg.solve(complex(z) * np.eye(values.shape[0]) - values, source)
    return complex(np.vdot(observation, state))


def weighted_moments(matrix: np.ndarray, source_coordinate: np.ndarray, observation_coordinate: np.ndarray, count: int) -> np.ndarray:
    values = np.asarray(matrix, dtype=complex)
    state = np.asarray(source_coordinate, dtype=complex).reshape(-1)
    observation = np.asarray(observation_coordinate, dtype=complex).reshape(-1)
    moments = []
    for _ in range(int(count)):
        moments.append(np.vdot(observation, state))
        state = values @ state
    return np.asarray(moments)


def feedback_determinant_ratio(
    matrix: np.ndarray,
    source_coordinate: np.ndarray,
    observation_coordinate: np.ndarray,
    z: complex,
) -> complex:
    values = np.asarray(matrix, dtype=complex)
    source = np.asarray(source_coordinate, dtype=complex).reshape(-1, 1)
    observation = np.asarray(observation_coordinate, dtype=complex).reshape(-1, 1)
    numerator = spectral_determinant(values + source @ observation.conj().T, z)
    denominator = spectral_determinant(values, z)
    return numerator / denominator


def modal_weighted_moments(eigenvalues: np.ndarray, residues: np.ndarray, count: int) -> np.ndarray:
    values = np.asarray(eigenvalues, dtype=complex)
    weights = np.asarray(residues, dtype=complex)
    return np.asarray([np.sum(weights * values**power) for power in range(int(count))])
