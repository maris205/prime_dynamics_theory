"""Gauge-free low-rank Hilbert--Schmidt utilities."""

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
        raise ValueError("low-rank factors must be two-dimensional")
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
    r"""Return the nonzero singular values of ``left right^T``."""

    u, v = _factors(left, right)
    qu, ru = np.linalg.qr(u, mode="reduced")
    qv, rv = np.linalg.qr(v, mode="reduced")
    del qu, qv
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
        raise ValueError("the two operators must act on the same dimensions")
    return low_rank_frobenius(
        np.concatenate((u1, -u2), axis=1),
        np.concatenate((v1, v2), axis=1),
    )


def dyadic_lift_factors(
    left: np.ndarray, right: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    r"""Lift a coarse cell operator to the dyadically refined value grid.

    Right/value factors are repeated. Left cell-mass factors are split
    equally between the two child cells.
    """

    u, v = _factors(left, right)
    return np.repeat(u, 2, axis=0), np.repeat(v / 2.0, 2, axis=0)
