"""Reduced projected-cross moment identities and elementary stability bounds."""

from __future__ import annotations

import math

import numpy as np


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    values = np.asarray(matrix, dtype=float)
    return (values + values.T) / 2.0


def projected_cross(gram: np.ndarray, packet: np.ndarray) -> np.ndarray:
    matrix = np.asarray(gram, dtype=float)
    basis = np.asarray(packet, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or basis.ndim != 2 or basis.shape[0] != matrix.shape[0]:
        raise ValueError("incompatible Gram and packet")
    return matrix @ basis - basis @ (basis.T @ matrix @ basis)


def cross_moment_matrices(gram: np.ndarray, packet: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    matrix = _hermitian(np.asarray(gram, dtype=float))
    basis = np.asarray(packet, dtype=float)
    if basis.ndim != 2 or basis.shape[0] != matrix.shape[0]:
        raise ValueError("incompatible Gram and packet")
    gv = matrix @ basis
    g2v = matrix @ gv
    g3v = matrix @ g2v
    first = _hermitian(basis.T @ gv)
    second = _hermitian(basis.T @ g2v)
    third = _hermitian(basis.T @ g3v)
    cross_gram = _hermitian(second - first @ first)
    cross_cubic = _hermitian(third - second @ first - first @ second + first @ first @ first)
    return first, second, third, cross_gram, cross_cubic


def reduced_cross_factorization(gram: np.ndarray, packet: np.ndarray, width: int) -> dict[str, np.ndarray]:
    matrix = _hermitian(np.asarray(gram, dtype=float))
    basis = np.asarray(packet, dtype=float)
    selected = int(width)
    cross = projected_cross(matrix, basis)
    cross_gram = _hermitian(cross.T @ cross)
    # A small SVD is used as a PSD repair: normal equations square the cross
    # condition number, so the weakest positive eigenvalue can acquire a tiny
    # negative sign in a symmetric eigensolve at binary64 precision.
    vectors, values, _ = np.linalg.svd(cross_gram, full_matrices=False)
    values = np.maximum(values, 0.0)
    if selected <= 0 or selected > vectors.shape[1] or values[selected - 1] <= 0.0:
        raise ValueError("selected cross width must have positive singular values")
    right = vectors[:, :selected]
    singular = np.sqrt(values[:selected])
    directions = cross @ (right / singular)
    first, second, third, moment_cross, moment_cubic = cross_moment_matrices(matrix, basis)
    diagonal = (right.T @ moment_cubic @ right) / singular[:, None] / singular[None, :]
    top_right = right * singular
    compressed = np.block([[first, top_right], [top_right.T, diagonal]])
    return {
        "cross": cross,
        "cross_gram": cross_gram,
        "moment_cross_gram": moment_cross,
        "moment_cross_cubic": moment_cubic,
        "right_vectors": right,
        "singular_values": singular,
        "squared_singular_values": values,
        "directions": directions,
        "compressed_moment": _hermitian(compressed),
        "first_moment": first,
        "second_moment": second,
        "third_moment": third,
    }


def reconstruction_error_bound(cross_error: float, cutoff_singular_value: float) -> float:
    error = float(cross_error)
    cutoff = float(cutoff_singular_value)
    if not math.isfinite(error) or error < 0.0 or not math.isfinite(cutoff) or cutoff <= 0.0:
        raise ValueError("invalid reconstruction data")
    return math.nextafter(error / cutoff, math.inf)


def cutoff_projector_bound(gram_error: float, spectral_gap: float) -> float:
    error = float(gram_error)
    gap = float(spectral_gap)
    if not math.isfinite(error) or error < 0.0 or not math.isfinite(gap) or gap <= 0.0 or 2.0 * error >= gap:
        raise ValueError("a separated cutoff is required")
    return math.nextafter(2.0 * error / gap, math.inf)
