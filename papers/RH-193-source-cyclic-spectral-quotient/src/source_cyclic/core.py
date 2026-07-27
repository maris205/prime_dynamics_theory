"""Source-cyclic restrictions of a left-multiplication matrix orbit."""

from __future__ import annotations

import numpy as np


def frobenius_inner(left: np.ndarray, right: np.ndarray) -> complex:
    return complex(np.vdot(np.asarray(left).reshape(-1), np.asarray(right).reshape(-1)))


def source_cyclic_arnoldi(
    operator: np.ndarray,
    source: np.ndarray,
    *,
    tolerance: float = 1e-11,
    maximum_dimension: int | None = None,
) -> dict[str, np.ndarray | float | int | bool]:
    """Build an orthonormal basis for span{S, AS, ...} in Frobenius norm."""

    dynamics = np.asarray(operator, dtype=complex)
    seed = np.asarray(source, dtype=complex)
    if dynamics.ndim != 2 or dynamics.shape[0] != dynamics.shape[1]:
        raise ValueError("operator must be square")
    if seed.ndim != 2 or seed.shape[0] != dynamics.shape[0]:
        raise ValueError("source has the wrong row dimension")
    scale = float(np.linalg.norm(seed, "fro"))
    if scale == 0.0:
        raise ValueError("source must be nonzero")
    limit = dynamics.shape[0] if maximum_dimension is None else int(maximum_dimension)
    if limit < 1:
        raise ValueError("maximum dimension must be positive")

    basis_states = [seed / scale]
    hessenberg = np.zeros((limit + 1, limit), dtype=complex)
    closed = False
    closure_residual = np.inf
    for column in range(limit):
        if column >= len(basis_states):
            break
        work = dynamics @ basis_states[column]
        # Two passes make the finite audit robust without changing the algebra.
        for _ in range(2):
            for row, vector in enumerate(basis_states):
                coefficient = frobenius_inner(vector, work)
                hessenberg[row, column] += coefficient
                work = work - coefficient * vector
        closure_residual = float(np.linalg.norm(work, "fro"))
        if closure_residual <= float(tolerance) * max(1.0, float(np.linalg.norm(dynamics @ basis_states[column], "fro"))):
            closed = True
            break
        if len(basis_states) == limit:
            break
        hessenberg[len(basis_states), column] = closure_residual
        basis_states.append(work / closure_residual)

    dimension = len(basis_states)
    basis = np.column_stack([state.reshape(-1) for state in basis_states])
    reduced = hessenberg[:dimension, :dimension]
    return {
        "basis": basis,
        "reduced_operator": reduced,
        "source_coordinate": basis.conj().T @ seed.reshape(-1),
        "dimension": dimension,
        "closed": closed,
        "closure_residual": closure_residual,
        "orthogonality_defect": float(np.linalg.norm(basis.conj().T @ basis - np.eye(dimension), 2)),
    }


def apply_reduced_basis(
    basis: np.ndarray,
    reduced_operator: np.ndarray,
    power: int,
    coordinate: np.ndarray,
) -> np.ndarray:
    return np.asarray(basis) @ np.linalg.matrix_power(np.asarray(reduced_operator), int(power)) @ np.asarray(coordinate)


def moment_sequence(
    operator: np.ndarray,
    source: np.ndarray,
    observation_seed: np.ndarray,
    count: int,
) -> np.ndarray:
    dynamics = np.asarray(operator, dtype=complex)
    state = np.asarray(source, dtype=complex)
    observation = np.asarray(observation_seed, dtype=complex)
    if observation.shape != state.shape:
        raise ValueError("observation seed and source must have the same matrix shape")
    values = []
    for _ in range(int(count)):
        values.append(frobenius_inner(observation, state))
        state = dynamics @ state
    return np.asarray(values)


def reduced_moment_sequence(
    basis: np.ndarray,
    reduced_operator: np.ndarray,
    source_coordinate: np.ndarray,
    observation_seed: np.ndarray,
    count: int,
) -> np.ndarray:
    frame = np.asarray(basis)
    reduced = np.asarray(reduced_operator)
    state = np.asarray(source_coordinate)
    observation_coordinate = frame.conj().T @ np.asarray(observation_seed).reshape(-1)
    values = []
    for _ in range(int(count)):
        values.append(np.vdot(observation_coordinate, state))
        state = reduced @ state
    return np.asarray(values)


def synthesis_inclusion_defect(basis: np.ndarray, synthesis: np.ndarray) -> float:
    frame = np.asarray(basis)
    values = np.asarray(synthesis)
    residual = values - frame @ (frame.conj().T @ values)
    return float(np.linalg.norm(residual, 2))
