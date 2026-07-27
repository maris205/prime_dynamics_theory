"""Physical eigenmode matching for temporal packet roots."""

from __future__ import annotations

import numpy as np


def normalize_left_eigenvector(right: np.ndarray, left: np.ndarray) -> np.ndarray:
    """Scale a left eigenvector so that left^* right = 1."""

    vector = np.asarray(right, dtype=complex)
    dual = np.asarray(left, dtype=complex)
    overlap = complex(np.vdot(dual, vector))
    if abs(overlap) <= np.finfo(float).tiny:
        raise ValueError("left and right eigenvectors have zero pairing")
    return dual / np.conj(overlap)


def nearest_unique_matching(packet_values: np.ndarray, physical_values: np.ndarray) -> list[int]:
    """Greedily match packet roots to distinct nearest physical eigenvalues."""

    packet = np.asarray(packet_values, dtype=complex)
    physical = np.asarray(physical_values, dtype=complex)
    pairs = sorted(
        (float(abs(packet[i] - physical[j])), i, j)
        for i in range(packet.size)
        for j in range(physical.size)
    )
    assignment: dict[int, int] = {}
    used = set()
    for _, packet_index, physical_index in pairs:
        if packet_index in assignment or physical_index in used:
            continue
        assignment[packet_index] = physical_index
        used.add(physical_index)
        if len(assignment) == packet.size:
            break
    if len(assignment) != packet.size:
        raise RuntimeError("unique matching failed")
    return [assignment[index] for index in range(packet.size)]


def contour_count(values: np.ndarray, center: complex, radius: float) -> int:
    return int(np.sum(np.abs(np.asarray(values, dtype=complex) - complex(center)) < float(radius)))


def contour_spectral_clearance(values: np.ndarray, center: complex, radius: float) -> float:
    """Minimum radial distance of a discrete eigenvalue from a circle."""

    distances = np.abs(np.asarray(values, dtype=complex) - complex(center))
    return float(np.min(np.abs(distances - float(radius))))


def source_observation_mode(
    right: np.ndarray,
    normalized_left: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
) -> dict[str, np.ndarray | complex | float]:
    """Build X=P S, Y=P^* O^*, and their scalar transfer residue."""

    vector = np.asarray(right, dtype=complex)
    dual = np.asarray(normalized_left, dtype=complex)
    seed = np.asarray(source, dtype=complex)
    output = np.asarray(observation, dtype=complex)
    source_coefficient = dual.conj().T @ seed
    observation_coefficient = output @ vector
    right_state = np.outer(vector, source_coefficient)
    left_state = np.outer(dual, np.conj(observation_coefficient))
    residue = complex(source_coefficient @ observation_coefficient)
    right_norm = float(np.linalg.norm(right_state, "fro"))
    left_norm = float(np.linalg.norm(left_state, "fro"))
    normalized_overlap = abs(residue) / max(right_norm * left_norm, np.finfo(float).tiny)
    return {
        "right_state": right_state,
        "left_state": left_state,
        "residue": residue,
        "right_state_norm": right_norm,
        "left_state_norm": left_norm,
        "source_activation_norm": float(np.linalg.norm(source_coefficient)),
        "observation_activation_norm": float(np.linalg.norm(observation_coefficient)),
        "normalized_cross_overlap": float(normalized_overlap),
        "spectral_projector_norm": float(np.linalg.norm(vector) * np.linalg.norm(dual)),
    }


def orthonormal_range(matrix: np.ndarray) -> np.ndarray:
    return np.linalg.qr(np.asarray(matrix), mode="reduced")[0]


def subspace_gap(left: np.ndarray, right: np.ndarray) -> dict[str, float]:
    """Principal-angle data for two equal-dimensional column spaces."""

    first = orthonormal_range(left)
    second = orthonormal_range(right)
    singular = np.linalg.svd(first.conj().T @ second, compute_uv=False)
    minimum = float(np.clip(singular[-1], 0.0, 1.0))
    return {
        "minimum_principal_cosine": minimum,
        "maximum_principal_cosine": float(np.clip(singular[0], 0.0, 1.0)),
        "maximum_principal_sine": float(np.sqrt(max(0.0, 1.0 - minimum**2))),
    }


def trace_power_errors(packet: np.ndarray, physical_values: np.ndarray, maximum_power: int = 8) -> list[dict[str, float | int]]:
    reduced = np.asarray(packet, dtype=complex)
    values = np.asarray(physical_values, dtype=complex)
    records = []
    for power in range(1, int(maximum_power) + 1):
        packet_trace = complex(np.trace(np.linalg.matrix_power(reduced, power)))
        physical_trace = complex(np.sum(values**power))
        records.append({
            "power": power,
            "packet_trace_real": float(packet_trace.real),
            "packet_trace_imag": float(packet_trace.imag),
            "physical_trace_real": float(physical_trace.real),
            "physical_trace_imag": float(physical_trace.imag),
            "absolute_error": float(abs(packet_trace - physical_trace)),
            "relative_error": float(abs(packet_trace - physical_trace) / max(1.0, abs(physical_trace))),
        })
    return records
