"""Exact residue deflation and stable-rank transfer inequalities."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def _nonnegative(value: float, name: str) -> float:
    result = float(value)
    if not np.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def rank_one_projection(
    right: np.ndarray, left: np.ndarray
) -> np.ndarray:
    """Return ``r l*`` after enforcing the normalization ``l* r = 1``."""

    r = np.asarray(right, dtype=np.complex128).reshape(-1)
    ell = np.asarray(left, dtype=np.complex128).reshape(-1)
    if r.shape != ell.shape:
        raise ValueError("left and right eigenvectors must have equal size")
    pairing = np.vdot(ell, r)
    if abs(pairing) <= np.finfo(float).tiny:
        raise ValueError("left and right eigenvectors have zero pairing")
    return np.outer(r, np.conjugate(ell / np.conjugate(pairing)))


def deflated_shift_dense(
    matrix: np.ndarray,
    z: complex,
    eigenvalue: complex,
    right: np.ndarray,
    left: np.ndarray,
) -> np.ndarray:
    """Return ``zI - T + lambda P`` for the normalized rank-one projector."""

    operator = np.asarray(matrix, dtype=np.complex128)
    if operator.ndim != 2 or operator.shape[0] != operator.shape[1]:
        raise ValueError("matrix must be square")
    projection = rank_one_projection(right, left)
    if projection.shape != operator.shape:
        raise ValueError("eigenvectors have incompatible dimension")
    return complex(z) * np.eye(operator.shape[0]) - operator + complex(
        eigenvalue
    ) * projection


def reduced_resolvent_dense(
    matrix: np.ndarray,
    z: complex,
    eigenvalue: complex,
    right: np.ndarray,
    left: np.ndarray,
) -> np.ndarray:
    r"""Evaluate ``(z-(T-lambda P))^{-1}(I-P)`` exactly in dense algebra."""

    operator = np.asarray(matrix, dtype=np.complex128)
    projection = rank_one_projection(right, left)
    complement = np.eye(operator.shape[0]) - projection
    shifted = deflated_shift_dense(
        operator, z, eigenvalue, right, left
    )
    return np.linalg.solve(shifted, complement)


@dataclass(frozen=True)
class StableRankTransfer:
    """Upper ledger transferring two Hilbert--Schmidt gains to a mixed gain."""

    left_hilbert_schmidt_gain: float
    right_hilbert_schmidt_gain: float
    b_sqrt_stable_rank_upper: float
    c_sqrt_stable_rank_upper: float
    selected_sqrt_stable_rank_upper: float
    mixed_gain_upper: float


def mixed_gain_from_hilbert_schmidt(
    left_hilbert_schmidt_gain: float,
    right_hilbert_schmidt_gain: float,
    *,
    b_hilbert_schmidt_upper: float,
    b_operator_lower: float,
    c_hilbert_schmidt_upper: float,
    c_operator_lower: float,
) -> StableRankTransfer:
    r"""Bound the RH-48 mixed placement by stable-rank factors.

    If ``a_2`` and ``c_2`` are the normalized Hilbert--Schmidt directional
    gains, then

    ``min(a_2 c_inf, a_inf c_2)``

    is at most

    ``a_2 c_2 min(||B||_HS/||B||, ||C||_HS/||C||)``.

    Certified Hilbert--Schmidt uppers and operator-norm lowers may be supplied
    in place of exact norms.
    """

    left_gain = _nonnegative(
        left_hilbert_schmidt_gain, "left_hilbert_schmidt_gain"
    )
    right_gain = _nonnegative(
        right_hilbert_schmidt_gain, "right_hilbert_schmidt_gain"
    )
    b_hs = _nonnegative(b_hilbert_schmidt_upper, "b_hilbert_schmidt_upper")
    c_hs = _nonnegative(c_hilbert_schmidt_upper, "c_hilbert_schmidt_upper")
    b_op = _nonnegative(b_operator_lower, "b_operator_lower")
    c_op = _nonnegative(c_operator_lower, "c_operator_lower")
    if b_op == 0.0 or c_op == 0.0:
        raise ValueError("operator lower bounds must be positive")
    b_rank = b_hs / b_op
    c_rank = c_hs / c_op
    selected = min(b_rank, c_rank)
    return StableRankTransfer(
        left_hilbert_schmidt_gain=left_gain,
        right_hilbert_schmidt_gain=right_gain,
        b_sqrt_stable_rank_upper=b_rank,
        c_sqrt_stable_rank_upper=c_rank,
        selected_sqrt_stable_rank_upper=selected,
        mixed_gain_upper=left_gain * right_gain * selected,
    )


@dataclass(frozen=True)
class DirectionalResidualUpper:
    """One residual-certified normalized directional Hilbert--Schmidt upper."""

    approximation_norm_upper: float
    residual_norm_upper: float
    reduced_inverse_norm_upper: float
    denominator_norm_lower: float
    absolute_action_upper: float
    normalized_gain_upper: float


def directional_residual_upper(
    approximation_norm_upper: float,
    residual_norm_upper: float,
    reduced_inverse_norm_upper: float,
    denominator_norm_lower: float,
) -> DirectionalResidualUpper:
    r"""Apply ``||R E|| <= ||X|| + ||R|| ||E-A X||`` with norm bounds."""

    approximation = _nonnegative(
        approximation_norm_upper, "approximation_norm_upper"
    )
    residual = _nonnegative(residual_norm_upper, "residual_norm_upper")
    inverse = _nonnegative(
        reduced_inverse_norm_upper, "reduced_inverse_norm_upper"
    )
    denominator = _nonnegative(
        denominator_norm_lower, "denominator_norm_lower"
    )
    if denominator == 0.0:
        raise ValueError("denominator norm lower bound must be positive")
    absolute = approximation + inverse * residual
    return DirectionalResidualUpper(
        approximation_norm_upper=approximation,
        residual_norm_upper=residual,
        reduced_inverse_norm_upper=inverse,
        denominator_norm_lower=denominator,
        absolute_action_upper=absolute,
        normalized_gain_upper=absolute / denominator,
    )
