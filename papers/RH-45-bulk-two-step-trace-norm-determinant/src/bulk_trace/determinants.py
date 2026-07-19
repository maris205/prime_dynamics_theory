"""Floating sparse determinants for stored rank-two-deflated matrices.

The routines in this module are diagnostics, not interval certificates.  A
rank-two matrix determinant lemma keeps the stored 2048--8192 computations
sparse even though the intrinsic peripheral subtraction is dense.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math

import numpy as np
from scipy.sparse import csc_matrix, eye
from scipy.sparse.linalg import splu


def permutation_sign(permutation: np.ndarray) -> int:
    """Return the sign of a permutation in one-line notation."""

    values = np.asarray(permutation, dtype=np.int64)
    size = int(values.size)
    if np.unique(values).size != size or np.any(values < 0) or np.any(values >= size):
        raise ValueError("input is not a permutation")
    visited = np.zeros(size, dtype=bool)
    cycles = 0
    for start in range(size):
        if visited[start]:
            continue
        cycles += 1
        index = start
        while not visited[index]:
            visited[index] = True
            index = int(values[index])
    return -1 if (size - cycles) % 2 else 1


@dataclass(frozen=True)
class SignedLogDeterminant:
    sign: float
    log_absolute_value: float

    @property
    def value(self) -> float:
        return float(self.sign * math.exp(self.log_absolute_value))


@dataclass(frozen=True)
class BulkDeterminantEvaluation:
    square_parameter: float
    one_step_parameter: float
    negative_shift_determinant: float
    positive_shift_determinant: float
    square_determinant: float
    bulk_trace: float
    symmetric_det2_product: float
    symmetric_det2_identity_error: float
    negative_shift_log_absolute_value: float
    positive_shift_log_absolute_value: float

    def as_dict(self) -> dict[str, float]:
        return asdict(self)


def _sparse_lu_signed_logdet(factor) -> SignedLogDeterminant:
    diagonal = np.asarray(factor.U.diagonal(), dtype=np.float64)
    if np.any(diagonal == 0.0):
        return SignedLogDeterminant(sign=0.0, log_absolute_value=-math.inf)
    sign = float(
        permutation_sign(factor.perm_r)
        * permutation_sign(factor.perm_c)
        * np.prod(np.sign(diagonal))
    )
    log_absolute = float(np.sum(np.log(np.abs(diagonal))))
    return SignedLogDeterminant(sign=sign, log_absolute_value=log_absolute)


def low_rank_bulk_log_determinant(
    matrix,
    right_modes: np.ndarray,
    left_modes: np.ndarray,
    peripheral_values: np.ndarray,
    parameter: float,
) -> SignedLogDeterminant:
    r"""Evaluate ``det(I-parameter*(P-R Lambda L^T))``.

    If ``A=I-sP`` and ``U=R Lambda``, then

    ``det(I-sB)=det(A) det(I+s L^T A^{-1} U)``.
    """

    sparse = csc_matrix(matrix)
    dimension = int(sparse.shape[0])
    if sparse.shape[1] != dimension:
        raise ValueError("matrix must be square")
    right = np.asarray(right_modes, dtype=np.float64)
    left = np.asarray(left_modes, dtype=np.float64)
    values = np.asarray(peripheral_values, dtype=np.float64)
    if right.shape != left.shape or right.shape[0] != dimension:
        raise ValueError("left and right factors have incompatible shapes")
    if values.shape != (right.shape[1],):
        raise ValueError("peripheral eigenvalue vector has incompatible shape")

    shift = float(parameter)
    base = eye(dimension, format="csc", dtype=np.float64) - shift * sparse
    factor = splu(base, permc_spec="COLAMD")
    base_det = _sparse_lu_signed_logdet(factor)
    weighted_right = right * values[None, :]
    solved = factor.solve(weighted_right)
    correction = np.eye(values.size) + shift * (left.T @ solved)
    correction_sign, correction_logabs = np.linalg.slogdet(correction)
    if correction_sign == 0.0:
        return SignedLogDeterminant(sign=0.0, log_absolute_value=-math.inf)
    return SignedLogDeterminant(
        sign=float(base_det.sign * correction_sign),
        log_absolute_value=float(
            base_det.log_absolute_value + correction_logabs
        ),
    )


def bulk_square_determinant(
    matrix,
    right_modes: np.ndarray,
    left_modes: np.ndarray,
    peripheral_values: np.ndarray,
    square_parameter: float,
) -> BulkDeterminantEvaluation:
    r"""Evaluate ``det(I-w B^2)`` through the symmetric one-step product."""

    parameter = float(square_parameter)
    if parameter < 0.0:
        raise ValueError("the stored real pilot requires a nonnegative w")
    z = math.sqrt(parameter)
    if z == 0.0:
        negative = SignedLogDeterminant(1.0, 0.0)
        positive = SignedLogDeterminant(1.0, 0.0)
    else:
        negative = low_rank_bulk_log_determinant(
            matrix,
            right_modes,
            left_modes,
            peripheral_values,
            z,
        )
        positive = low_rank_bulk_log_determinant(
            matrix,
            right_modes,
            left_modes,
            peripheral_values,
            -z,
        )
    square_value = float(
        negative.sign
        * positive.sign
        * math.exp(
            negative.log_absolute_value + positive.log_absolute_value
        )
    )
    matrix_trace = float(np.asarray(matrix.diagonal()).sum())
    weighted_trace = float(
        np.trace(
            np.asarray(left_modes).T
            @ (np.asarray(right_modes) * np.asarray(peripheral_values)[None, :])
        )
    )
    bulk_trace = matrix_trace - weighted_trace
    det2_negative = negative.value * math.exp(z * bulk_trace)
    det2_positive = positive.value * math.exp(-z * bulk_trace)
    symmetric_product = float(det2_negative * det2_positive)
    return BulkDeterminantEvaluation(
        square_parameter=parameter,
        one_step_parameter=z,
        negative_shift_determinant=negative.value,
        positive_shift_determinant=positive.value,
        square_determinant=square_value,
        bulk_trace=bulk_trace,
        symmetric_det2_product=symmetric_product,
        symmetric_det2_identity_error=abs(
            symmetric_product - square_value
        ),
        negative_shift_log_absolute_value=negative.log_absolute_value,
        positive_shift_log_absolute_value=positive.log_absolute_value,
    )
