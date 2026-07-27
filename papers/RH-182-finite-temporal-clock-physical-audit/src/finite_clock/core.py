"""Finite temporal clocks built directly from normalized matrix orbits."""

from __future__ import annotations

import cmath
import itertools
import math

import numpy as np


def adjoint(matrix: np.ndarray) -> np.ndarray:
    return np.asarray(matrix).conj().T


def column_operator_norm(matrix: np.ndarray) -> float:
    """Operator norm of a tall matrix computed from its small column Gram."""
    values = np.linalg.eigvalsh(adjoint(matrix) @ np.asarray(matrix))
    return math.sqrt(max(0.0, float(values[-1])))


def normalized_orbit(
    operator: np.ndarray,
    seed: np.ndarray,
    endpoint: int,
) -> tuple[list[np.ndarray], list[float], list[np.ndarray]]:
    dynamics = np.asarray(operator)
    state = np.asarray(seed)
    if dynamics.ndim != 2 or dynamics.shape[0] != dynamics.shape[1]:
        raise ValueError("operator must be square")
    if state.ndim != 2 or state.shape[0] != dynamics.shape[0]:
        raise ValueError("seed and operator dimensions do not compose")
    if int(endpoint) < 1:
        raise ValueError("endpoint must be positive")
    states = [state]
    for _ in range(int(endpoint)):
        states.append(dynamics @ states[-1])
    norms = [float(np.linalg.norm(item, "fro")) for item in states]
    if min(norms) == 0.0:
        raise ValueError("orbit contains a zero state")
    units = [item / norm for item, norm in zip(states, norms)]
    return states, norms, units


def temporal_synthesis(
    units: list[np.ndarray],
    start: int,
    length: int,
    *,
    stride: int = 1,
) -> np.ndarray:
    first = int(start)
    size = int(length)
    step = int(stride)
    if first < 0 or size < 2 or step < 1:
        raise ValueError("invalid start, length, or stride")
    indices = [first + step * index for index in range(size)]
    if indices[-1] >= len(units):
        raise ValueError("temporal window exceeds the orbit")
    shape = units[0].shape
    if any(np.asarray(units[index]).shape != shape for index in indices):
        raise ValueError("orbit states must have one common shape")
    return np.column_stack([np.asarray(units[index]).reshape(-1) for index in indices])


def polar_frame(synthesis: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    matrix = np.asarray(synthesis)
    gram = adjoint(matrix) @ matrix
    gram = (gram + adjoint(gram)) / 2.0
    values, vectors = np.linalg.eigh(gram)
    tolerance = np.finfo(float).eps * max(matrix.shape) * float(values[-1])
    if float(values[0]) <= tolerance:
        raise ValueError("temporal synthesis is rank deficient")
    square_root = (vectors * np.sqrt(values)) @ adjoint(vectors)
    inverse_root = (vectors * (1.0 / np.sqrt(values))) @ adjoint(vectors)
    frame = matrix @ inverse_root
    return frame, gram, square_root, inverse_root


def projective_phase(seed: np.ndarray, endpoint: np.ndarray) -> complex:
    inner = complex(np.vdot(np.asarray(seed).reshape(-1), np.asarray(endpoint).reshape(-1)))
    if abs(inner) <= np.finfo(float).tiny:
        return 1.0 + 0.0j
    return inner / abs(inner)


def weighted_cycle(
    norms: list[float],
    start: int,
    length: int,
    *,
    stride: int = 1,
    wrap_phase: complex = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    first = int(start)
    size = int(length)
    step = int(stride)
    if size < 2 or step < 1 or first < 0:
        raise ValueError("invalid weighted cycle parameters")
    indices = [first + step * index for index in range(size + 1)]
    if indices[-1] >= len(norms):
        raise ValueError("cycle exceeds norm history")
    weights = np.asarray(
        [float(norms[indices[index + 1]]) / float(norms[indices[index]]) for index in range(size)],
        dtype=float,
    )
    phase = complex(wrap_phase)
    if not math.isclose(abs(phase), 1.0, rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError("wrap phase must be unimodular")
    cycle = np.zeros((size, size), dtype=np.result_type(phase, float))
    for index in range(size - 1):
        cycle[index + 1, index] = weights[index]
    cycle[0, size - 1] = phase * weights[-1]
    return cycle, weights


def apply_left_operator(
    operator: np.ndarray,
    columns: np.ndarray,
    state_shape: tuple[int, int],
    *,
    adjoint_action: bool = False,
    power: int = 1,
) -> np.ndarray:
    dynamics = np.linalg.matrix_power(np.asarray(operator), int(power))
    if adjoint_action:
        dynamics = adjoint(dynamics)
    values = np.asarray(columns)
    if values.ndim != 2 or values.shape[0] != state_shape[0] * state_shape[1]:
        raise ValueError("columns do not match the state shape")
    return np.column_stack(
        [(dynamics @ values[:, index].reshape(state_shape)).reshape(-1) for index in range(values.shape[1])]
    )


def _phase_distance(left: float, right: float) -> float:
    difference = abs(left - right) % (2.0 * math.pi)
    return min(difference, 2.0 * math.pi - difference)


def cycle_spectral_errors(cycle: np.ndarray, wrap_phase: complex) -> dict[str, float]:
    matrix = np.asarray(cycle)
    size = matrix.shape[0]
    if matrix.ndim != 2 or matrix.shape[1] != size:
        raise ValueError("cycle must be square")
    eigenvalues = np.linalg.eigvals(matrix)
    radius = abs(np.linalg.det(matrix)) ** (1.0 / size)
    offset = cmath.phase(complex(wrap_phase)) / size
    expected = [offset + 2.0 * math.pi * index / size for index in range(size)]
    observed = [cmath.phase(complex(value)) for value in eigenvalues]
    best = math.inf
    for permutation in itertools.permutations(observed):
        error = math.sqrt(sum(_phase_distance(a, b) ** 2 for a, b in zip(permutation, expected)) / size)
        best = min(best, error)
    radial = math.sqrt(sum((abs(value) - radius) ** 2 for value in eigenvalues) / size)
    return {
        "predicted_radius": float(radius),
        "radial_rms_error": float(radial),
        "phase_rms_error": float(best),
    }


def clock_window_metrics(
    operator: np.ndarray,
    norms: list[float],
    units: list[np.ndarray],
    start: int,
    length: int,
    *,
    stride: int = 1,
    use_projective_mark: bool = True,
) -> dict[str, float | int | complex]:
    synthesis = temporal_synthesis(units, start, length, stride=stride)
    frame, gram, square_root, inverse_root = polar_frame(synthesis)
    endpoint_index = int(start) + int(length) * int(stride)
    phase = projective_phase(units[int(start)], units[endpoint_index]) if use_projective_mark else 1.0 + 0.0j
    cycle, weights = weighted_cycle(
        norms,
        start,
        length,
        stride=stride,
        wrap_phase=phase,
    )
    reduced = square_root @ cycle @ inverse_root
    state_shape = tuple(np.asarray(units[0]).shape)
    forward = apply_left_operator(operator, frame, state_shape, power=stride)
    backward = apply_left_operator(operator, frame, state_shape, adjoint_action=True, power=stride)
    primal = forward - frame @ reduced
    dual = backward - frame @ adjoint(reduced)
    inner = complex(np.vdot(np.asarray(units[int(start)]).reshape(-1), np.asarray(units[endpoint_index]).reshape(-1)))
    marked_chord = float(np.linalg.norm(np.asarray(units[endpoint_index]) - phase * np.asarray(units[int(start)]), "fro"))
    unmarked_chord = float(np.linalg.norm(np.asarray(units[endpoint_index]) - np.asarray(units[int(start)]), "fro"))
    projective = math.sqrt(max(0.0, 1.0 - min(1.0, abs(inner)) ** 2))
    spectral = cycle_spectral_errors(reduced, phase)
    predicted_radius = float(np.prod(weights) ** (1.0 / int(length)))
    return {
        "start": int(start),
        "length": int(length),
        "stride": int(stride),
        "gram_condition_number": float(np.linalg.cond(gram)),
        "endpoint_seed_inner_real": float(inner.real),
        "endpoint_seed_inner_imag": float(inner.imag),
        "endpoint_seed_absolute_inner": float(abs(inner)),
        "orientation_mark_real": float(phase.real),
        "orientation_mark_imag": float(phase.imag),
        "unmarked_wrap_chord": unmarked_chord,
        "marked_wrap_chord": marked_chord,
        "projective_wrap_distance": float(projective),
        "primal_relative_residual": float(column_operator_norm(primal) / max(column_operator_norm(forward), np.finfo(float).tiny)),
        "adjoint_relative_residual": float(column_operator_norm(dual) / max(column_operator_norm(backward), np.finfo(float).tiny)),
        "cycle_radius": predicted_radius,
        "cycle_radius_formula_residual": float(abs(predicted_radius - spectral["predicted_radius"])),
        "cycle_radial_rms_error": spectral["radial_rms_error"],
        "cycle_phase_rms_error": spectral["phase_rms_error"],
        "frame_isometry_defect": float(column_operator_norm(adjoint(frame) @ frame - np.eye(int(length)))),
    }
