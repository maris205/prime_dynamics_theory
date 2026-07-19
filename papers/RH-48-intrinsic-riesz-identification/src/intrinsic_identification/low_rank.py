"""Gauge-free low-rank and nested-cell compression utilities."""

from __future__ import annotations

import numpy as np


def _factors(
    left: np.ndarray, right: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    u = np.asarray(left)
    v = np.asarray(right)
    if u.ndim == 1:
        u = u[:, None]
    if v.ndim == 1:
        v = v[:, None]
    if u.ndim != 2 or v.ndim != 2 or u.shape[1] != v.shape[1]:
        raise ValueError("low-rank factors must have matching ranks")
    return u, v


def low_rank_frobenius(left: np.ndarray, right: np.ndarray) -> float:
    r"""Return ``||left right^T||_F`` without forming the full matrix."""

    u, v = _factors(left, right)
    gram_u = u.conj().T @ u
    gram_v = v.conj().T @ v
    square = np.trace(gram_u @ gram_v.T).real
    return float(np.sqrt(max(0.0, square)))


def low_rank_singular_values(
    left: np.ndarray, right: np.ndarray
) -> np.ndarray:
    """Return all nonzero singular values of a factored operator."""

    u, v = _factors(left, right)
    _, ru = np.linalg.qr(u, mode="reduced")
    _, rv = np.linalg.qr(v, mode="reduced")
    return np.linalg.svd(ru @ rv.T, compute_uv=False)


def low_rank_difference_frobenius(
    first_left: np.ndarray,
    first_right: np.ndarray,
    second_left: np.ndarray,
    second_right: np.ndarray,
) -> float:
    """Return the Frobenius norm of two low-rank operators' difference."""

    u1, v1 = _factors(first_left, first_right)
    u2, v2 = _factors(second_left, second_right)
    if u1.shape[0] != u2.shape[0] or v1.shape[0] != v2.shape[0]:
        raise ValueError("the two operators must act on the same space")
    return low_rank_frobenius(
        np.concatenate((u1, -u2), axis=1),
        np.concatenate((v1, v2), axis=1),
    )


def compress_factors(
    left: np.ndarray, right: np.ndarray, ratio: int
) -> tuple[np.ndarray, np.ndarray]:
    r"""Orthogonally compress fine value/mass factors to nested cells.

    Value factors are averaged over child cells and cell-mass factors are
    summed.  Their outer product is exactly the top-left Haar block.
    """

    u, v = _factors(left, right)
    ratio = int(ratio)
    if ratio < 1 or u.shape != v.shape or u.shape[0] % ratio:
        raise ValueError("invalid nested factor compression")
    dimension = u.shape[0] // ratio
    rank = u.shape[1]
    coarse_u = u.reshape(dimension, ratio, rank).mean(axis=1)
    coarse_v = v.reshape(dimension, ratio, rank).sum(axis=1)
    return coarse_u, coarse_v
