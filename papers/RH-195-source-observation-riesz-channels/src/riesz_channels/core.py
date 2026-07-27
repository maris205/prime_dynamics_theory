"""Source-observation channels cut out by finite Riesz projectors."""

from __future__ import annotations

import numpy as np


def normalized_eigenprojector(right: np.ndarray, left: np.ndarray) -> np.ndarray:
    vector = np.asarray(right, dtype=complex)
    dual = np.asarray(left, dtype=complex)
    overlap = complex(np.vdot(dual, vector))
    if abs(overlap) <= np.finfo(float).tiny:
        raise ValueError("left/right eigenvector pairing vanishes")
    return np.outer(vector, np.conj(dual / np.conj(overlap)))


def source_observation_channel(
    projector: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
) -> dict[str, np.ndarray | complex | float]:
    projection = np.asarray(projector, dtype=complex)
    seed = np.asarray(source, dtype=complex)
    output = np.asarray(observation, dtype=complex)
    right_state = projection @ seed
    left_state = projection.conj().T @ output.conj().T
    residue = complex(np.trace(output @ projection @ seed))
    pairing = complex(np.vdot(left_state.reshape(-1), right_state.reshape(-1)))
    return {
        "right_state": right_state,
        "left_state": left_state,
        "residue": residue,
        "pairing": pairing,
        "pairing_error": float(abs(pairing - residue)),
        "right_norm": float(np.linalg.norm(right_state, "fro")),
        "left_norm": float(np.linalg.norm(left_state, "fro")),
    }


def cross_channel_gram(right_states: list[np.ndarray], left_states: list[np.ndarray]) -> np.ndarray:
    if len(right_states) != len(left_states):
        raise ValueError("right and left channel counts differ")
    return np.asarray([
        [np.vdot(np.asarray(left).reshape(-1), np.asarray(right).reshape(-1)) for right in right_states]
        for left in left_states
    ])


def transfer_value(operator: np.ndarray, source: np.ndarray, observation: np.ndarray, z: complex) -> complex:
    dynamics = np.asarray(operator, dtype=complex)
    state = np.linalg.solve(complex(z) * np.eye(dynamics.shape[0]) - dynamics, np.asarray(source, dtype=complex))
    return complex(np.trace(np.asarray(observation, dtype=complex) @ state))


def simple_channel_transfer(eigenvalues: np.ndarray, residues: np.ndarray, z: complex) -> complex:
    return complex(np.sum(np.asarray(residues, dtype=complex) / (complex(z) - np.asarray(eigenvalues, dtype=complex))))


def residue_normalized_frames(right_states: list[np.ndarray], left_states: list[np.ndarray], residues: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(residues, dtype=complex)
    if len(right_states) != len(left_states) or len(right_states) != values.size:
        raise ValueError("channel data have inconsistent sizes")
    if np.min(np.abs(values)) <= np.finfo(float).tiny:
        raise ValueError("all residues must be nonzero")
    right = np.column_stack([np.asarray(state).reshape(-1) for state in right_states])
    left = np.column_stack([
        np.asarray(state).reshape(-1) / np.conj(value)
        for state, value in zip(left_states, values)
    ])
    return right, left
