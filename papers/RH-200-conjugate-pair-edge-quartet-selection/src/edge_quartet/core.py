"""Conjugation and outer-edge quartet diagnostics."""

from __future__ import annotations

import numpy as np


def nearest_conjugate_errors(values: np.ndarray, selected_indices: list[int]) -> list[float]:
    spectrum = np.asarray(values, dtype=complex)
    return [float(np.min(np.abs(spectrum - np.conj(spectrum[index])))) for index in selected_indices]


def outer_edge_indices(values: np.ndarray, count: int = 4) -> list[int]:
    spectrum = np.asarray(values, dtype=complex)
    size = int(count)
    if size < 1 or size > spectrum.size:
        raise ValueError("invalid edge count")
    return [int(index) for index in np.argsort(-np.abs(spectrum))[:size]]


def radial_edge_gap(values: np.ndarray, count: int = 4) -> float:
    spectrum = np.sort(np.abs(np.asarray(values, dtype=complex)))[::-1]
    size = int(count)
    if size >= spectrum.size:
        return float("inf")
    return float(spectrum[size - 1] - spectrum[size])


def nonreal_count(values: np.ndarray, tolerance: float = 1e-10) -> int:
    return int(np.sum(np.abs(np.asarray(values, dtype=complex).imag) > float(tolerance)))


def conjugate_closed(values: np.ndarray, tolerance: float = 1e-10) -> bool:
    spectrum = np.asarray(values, dtype=complex)
    return max(nearest_conjugate_errors(spectrum, list(range(spectrum.size))), default=0.0) <= float(tolerance)
