"""Biorthogonal Perron/parity deflation for sparse Markov operators."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse.linalg import eigs


@dataclass(frozen=True)
class PeripheralProjector:
    eigenvalue: float
    right: np.ndarray
    left: np.ndarray
    right_residual: float
    left_residual: float


def resolve_peripheral_projectors(
    matrix,
    *,
    count: int = 6,
    tolerance: float = 2.0e-11,
) -> tuple[PeripheralProjector, PeripheralProjector]:
    """Resolve biorthogonal projectors for the Perron and parity modes."""

    values_r, vectors_r = eigs(
        matrix, k=int(count), which="LM", tol=float(tolerance), maxiter=5000
    )
    values_l, vectors_l = eigs(
        matrix.T, k=int(count), which="LM", tol=float(tolerance), maxiter=5000
    )
    real = np.flatnonzero(np.abs(values_r.imag) < 1.0e-8)
    if real.size < 2:
        raise RuntimeError("Perron/parity real modes were not resolved")
    perron = int(real[np.argmin(np.abs(values_r[real] - 1.0))])
    parity = int(real[np.argmin(values_r[real].real)])
    projectors: list[PeripheralProjector] = []
    for index in (perron, parity):
        eigenvalue = float(values_r[index].real)
        left_index = int(np.argmin(np.abs(values_l - eigenvalue)))
        right = np.asarray(vectors_r[:, index].real, dtype=np.float64)
        left = np.asarray(vectors_l[:, left_index].real, dtype=np.float64)
        pairing = float(np.dot(left, right))
        if abs(pairing) < 1.0e-12:
            raise RuntimeError("left/right peripheral pairing is singular")
        left /= pairing
        right_residual = float(
            np.linalg.norm(matrix @ right - eigenvalue * right)
            / np.linalg.norm(right)
        )
        left_residual = float(
            np.linalg.norm(matrix.T @ left - eigenvalue * left)
            / np.linalg.norm(left)
        )
        projectors.append(
            PeripheralProjector(
                eigenvalue, right, left, right_residual, left_residual
            )
        )
    return projectors[0], projectors[1]


def apply_deflated(
    matrix,
    projectors: tuple[PeripheralProjector, ...],
    vector: np.ndarray,
) -> np.ndarray:
    """Apply ``K - sum(lambda_i P_i)`` without forming dense projectors."""

    source = np.asarray(vector, dtype=np.float64)
    result = np.asarray(matrix @ source, dtype=np.float64)
    for projector in projectors:
        result -= (
            projector.eigenvalue
            * projector.right
            * float(np.dot(projector.left, source))
        )
    return result
