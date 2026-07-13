"""Finite-noise spectra, parity extraction, and regularized cycle products."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import scipy.linalg as la

from .markov import U_CRITICAL


def positive_midpoints(dimension: int) -> np.ndarray:
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    return (np.arange(int(dimension), dtype=np.float64) + 0.5) / dimension


def folded_gaussian_matrix(
    dimension: int,
    sigma: float,
    *,
    u: float = U_CRITICAL,
) -> np.ndarray:
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    grid = positive_midpoints(dimension)
    means = 1.0 - float(u) * grid * grid
    destination = grid[None, :]
    mean = means[:, None]
    log_positive = -0.5 * ((destination - mean) / float(sigma)) ** 2
    log_negative = -0.5 * ((-destination - mean) / float(sigma)) ** 2
    log_weights = np.logaddexp(log_positive, log_negative)
    log_weights -= np.max(log_weights, axis=1, keepdims=True)
    weights = np.exp(log_weights)
    return weights / np.sum(weights, axis=1, keepdims=True)


@dataclass(frozen=True)
class ResolvedSpectrum:
    eigenvalues: np.ndarray
    perron: complex
    parity: complex
    bulk: np.ndarray
    bulk_radius: float


def resolve_spectrum(matrix: np.ndarray) -> ResolvedSpectrum:
    values = la.eigvals(np.asarray(matrix))
    perron_index = int(np.argmin(np.abs(values - 1.0)))
    remaining_indices = np.delete(np.arange(values.size), perron_index)
    real_candidates = remaining_indices[np.abs(values[remaining_indices].imag) < 1.0e-9]
    if not real_candidates.size:
        raise RuntimeError("no real parity resonance found")
    parity_index = int(real_candidates[np.argmin(values[real_candidates].real)])
    bulk_indices = np.delete(np.arange(values.size), (perron_index, parity_index))
    bulk = values[bulk_indices]
    return ResolvedSpectrum(
        eigenvalues=values,
        perron=complex(values[perron_index]),
        parity=complex(values[parity_index]),
        bulk=bulk,
        bulk_radius=float(np.max(np.abs(bulk), initial=0.0)),
    )


def trace_from_spectrum(spectrum: ResolvedSpectrum, length: int) -> complex:
    return complex(np.sum(spectrum.eigenvalues ** int(length)))


def bulk_trace_from_spectrum(spectrum: ResolvedSpectrum, length: int) -> complex:
    return complex(np.sum(spectrum.bulk ** int(length)))


def regularized_determinant_from_traces(
    traces: dict[int, complex | float],
    z: complex,
    *,
    maximum_length: int | None = None,
) -> complex:
    """Return ``exp(-sum_(m>=2) trace_m z^m/m)`` at finite truncation."""

    lengths = sorted(length for length in traces if length >= 2)
    if maximum_length is not None:
        lengths = [length for length in lengths if length <= maximum_length]
    exponent = -sum(complex(traces[length]) * complex(z) ** length / length for length in lengths)
    return complex(np.exp(exponent))


def exact_bulk_det2(spectrum: ResolvedSpectrum, z: complex) -> complex:
    factors = (1.0 - complex(z) * spectrum.bulk) * np.exp(complex(z) * spectrum.bulk)
    return complex(np.prod(factors))
