"""Gauge-invariant low-rank algebra for stored peripheral terms."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class PeripheralData:
    """Right/left modes and eigenvalues defining ``R diag(values) L^T``."""

    right: np.ndarray
    left: np.ndarray
    values: np.ndarray

    def __post_init__(self) -> None:
        right = np.asarray(self.right)
        left = np.asarray(self.left)
        values = np.asarray(self.values)
        if right.ndim != 2 or left.shape != right.shape:
            raise ValueError("right and left modes must have equal matrix shapes")
        if values.shape != (right.shape[1],):
            raise ValueError("one eigenvalue is required for each mode")


def weighted_term(data: PeripheralData) -> np.ndarray:
    """Materialize the finite weighted spectral term for small tests."""

    return (np.asarray(data.right) * np.asarray(data.values)[None, :]) @ np.asarray(
        data.left
    ).T


def _average(values: np.ndarray) -> np.ndarray:
    return 0.5 * (values[0::2] + values[1::2])


def _difference(values: np.ndarray) -> np.ndarray:
    return 0.5 * (values[0::2] - values[1::2])


def _sum_pairs(values: np.ndarray) -> np.ndarray:
    return values[0::2] + values[1::2]


def _difference_pairs(values: np.ndarray) -> np.ndarray:
    return values[0::2] - values[1::2]


def block_factors(
    coarse: PeripheralData, fine: PeripheralData
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """Return ``A,B`` factors with each Haar block equal to ``A B^T``."""

    coarse_right = np.asarray(coarse.right)
    coarse_left = np.asarray(coarse.left)
    coarse_values = np.asarray(coarse.values)
    fine_right = np.asarray(fine.right)
    fine_left = np.asarray(fine.left)
    fine_values = np.asarray(fine.values)
    if fine_right.shape[0] != 2 * coarse_right.shape[0]:
        raise ValueError("fine dimension must be twice the coarse dimension")
    if fine_right.shape[1] != coarse_right.shape[1]:
        raise ValueError("coarse and fine peripheral ranks must agree")

    averaged_right = _average(fine_right)
    detailed_right = _difference(fine_right)
    summed_left = _sum_pairs(fine_left)
    detailed_left = _difference_pairs(fine_left)
    return {
        "coarse_consistency": (
            np.column_stack(
                (averaged_right * fine_values[None, :], -coarse_right * coarse_values[None, :])
            ),
            np.column_stack((summed_left, coarse_left)),
        ),
        "coarse_to_detail": (
            detailed_right * fine_values[None, :],
            summed_left,
        ),
        "detail_to_coarse": (
            averaged_right * fine_values[None, :],
            detailed_left,
        ),
        "detail_block": (
            detailed_right * fine_values[None, :],
            detailed_left,
        ),
    }


def low_rank_frobenius_norm(left_factor: np.ndarray, right_factor: np.ndarray) -> float:
    """Compute ``||A B^T||_F`` from its small Gram matrices."""

    a = np.asarray(left_factor)
    b = np.asarray(right_factor)
    if a.ndim != 2 or b.ndim != 2 or a.shape[1] != b.shape[1]:
        raise ValueError("low-rank factors must have the same column count")
    square = float(np.trace((a.T @ a) @ (b.T @ b)))
    return float(np.sqrt(max(square, 0.0)))


def low_rank_singular_values(
    left_factor: np.ndarray, right_factor: np.ndarray
) -> np.ndarray:
    """Return all nonzero singular values through thin QR factorizations."""

    a = np.asarray(left_factor)
    b = np.asarray(right_factor)
    qa, ra = np.linalg.qr(a, mode="reduced")
    qb, rb = np.linalg.qr(b, mode="reduced")
    del qa, qb
    return np.linalg.svd(ra @ rb.T, compute_uv=False)


def biorthogonality_defect(data: PeripheralData) -> float:
    """Return ``||L^T R-I||_2`` for the stored mode pair."""

    gram = np.asarray(data.left).T @ np.asarray(data.right)
    return float(np.linalg.norm(gram - np.eye(gram.shape[0]), 2))
