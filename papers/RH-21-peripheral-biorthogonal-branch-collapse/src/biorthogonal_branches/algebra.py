"""Exact algebra for peripheral biorthogonal packet data."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BiorthogonalPair:
    """Canonical trial/dual pair inside an oblique spectral complement."""

    synthesis: np.ndarray
    analysis: np.ndarray
    gram: np.ndarray
    biorthogonality_residual: float
    right_annihilation_residual: float
    left_annihilation_residual: float


@dataclass(frozen=True)
class MergeMetrics:
    """Conditioning data for two normalized branch histories."""

    overlap_modulus: float
    bright_singular_value: float
    dark_singular_value: float
    synthesis_condition: float
    gram_condition: float
    dual_norm_lower_bound: float


def _as_columns(values: np.ndarray, *, name: str) -> np.ndarray:
    array = np.asarray(values)
    if array.ndim == 1:
        array = array[:, None]
    if array.ndim != 2 or array.shape[0] < 1 or array.shape[1] < 1:
        raise ValueError(f"{name} must be a nonempty vector or matrix")
    dtype = np.complex128 if np.iscomplexobj(array) else np.float64
    return np.asarray(array, dtype=dtype)


def complement_project(
    values: np.ndarray,
    right_modes: np.ndarray,
    left_modes: np.ndarray,
) -> np.ndarray:
    r"""Apply ``Q = I - R L^*`` to one or more columns."""

    source = _as_columns(values, name="values")
    right = _as_columns(right_modes, name="right_modes")
    left = _as_columns(left_modes, name="left_modes")
    if right.shape != left.shape or source.shape[0] != right.shape[0]:
        raise ValueError("values and peripheral modes have incompatible shapes")
    return source - right @ (left.conj().T @ source)


def canonical_biorthogonal_pair(
    trial: np.ndarray,
    right_modes: np.ndarray,
    left_modes: np.ndarray,
    *,
    test: np.ndarray | None = None,
) -> BiorthogonalPair:
    r"""Return the canonical pair ``V=QV0``, ``W*=G^-1 W0*Q``.

    The peripheral modes must satisfy ``L^* R = I``.  The raw Petrov--Galerkin
    Gram matrix is ``G = W0^* Q V0``.
    """

    raw_trial = _as_columns(trial, name="trial")
    raw_test = raw_trial if test is None else _as_columns(test, name="test")
    right = _as_columns(right_modes, name="right_modes")
    left = _as_columns(left_modes, name="left_modes")
    if right.shape != left.shape or raw_trial.shape[0] != right.shape[0]:
        raise ValueError("trial and peripheral modes have incompatible shapes")
    if raw_test.shape != raw_trial.shape:
        raise ValueError("trial and test matrices must have the same shape")

    identity_error = np.linalg.norm(
        left.conj().T @ right - np.eye(right.shape[1])
    )
    if identity_error > 2.0e-8:
        raise ValueError("peripheral left/right modes are not biorthonormal")

    synthesis = complement_project(raw_trial, right, left)
    row_q = raw_test.conj().T - (raw_test.conj().T @ right) @ left.conj().T
    gram = row_q @ raw_trial
    if np.linalg.matrix_rank(gram) < gram.shape[0]:
        raise ValueError("the complement Gram matrix is singular")
    analysis = np.linalg.solve(gram, row_q)

    biorthogonality = np.linalg.norm(
        analysis @ synthesis - np.eye(synthesis.shape[1])
    )
    right_annihilation = np.linalg.norm(analysis @ right)
    left_annihilation = np.linalg.norm(left.conj().T @ synthesis)
    return BiorthogonalPair(
        synthesis=np.real_if_close(synthesis),
        analysis=np.real_if_close(analysis),
        gram=np.real_if_close(gram),
        biorthogonality_residual=float(biorthogonality),
        right_annihilation_residual=float(right_annihilation),
        left_annihilation_residual=float(left_annihilation),
    )


def gauge_transform(
    matrix: np.ndarray,
    gauge: np.ndarray,
) -> np.ndarray:
    r"""Return the similar matrix ``S^-1 M S``."""

    values = np.asarray(matrix)
    transform = np.asarray(gauge)
    if values.ndim != 2 or values.shape[0] != values.shape[1]:
        raise ValueError("matrix must be square")
    if transform.shape != values.shape:
        raise ValueError("gauge and matrix must have the same shape")
    if np.linalg.matrix_rank(transform) < transform.shape[0]:
        raise ValueError("gauge must be invertible")
    return np.linalg.solve(transform, values @ transform)


def bright_projector() -> np.ndarray:
    r"""Return the idempotent projector onto ``span((1,1)^T)``."""

    bright = np.ones(2, dtype=np.float64)
    return np.outer(bright, bright) / float(bright @ bright)


def bright_coordinate_dual(metric: np.ndarray) -> np.ndarray:
    r"""Return the metric dual row to the unnormalized bright vector.

    For an exchange-symmetric metric the result is exactly ``(1/2,1/2)``.
    The row is a coordinate dual: its pairing with ``(1,1)^T`` is one.
    """

    gram = np.asarray(metric)
    if gram.shape != (2, 2):
        raise ValueError("the branch metric must be 2x2")
    bright = np.ones(2, dtype=gram.dtype)
    row = bright.conj() @ gram
    denominator = row @ bright
    if abs(denominator) < 1.0e-14:
        raise ValueError("the bright vector is null in the supplied metric")
    return np.real_if_close(row / denominator)


def merge_metrics(left: np.ndarray, right: np.ndarray) -> MergeMetrics:
    """Return exact singular-value conditioning for two branch histories."""

    first = np.asarray(left).reshape(-1)
    second = np.asarray(right).reshape(-1)
    if first.shape != second.shape or first.size < 1:
        raise ValueError("branch histories must be equal nonzero vectors")
    first_norm = np.linalg.norm(first)
    second_norm = np.linalg.norm(second)
    if first_norm == 0.0 or second_norm == 0.0:
        raise ValueError("branch histories must be nonzero")
    first = first / first_norm
    second = second / second_norm
    pairing = np.vdot(first, second)
    overlap = float(min(abs(pairing), 1.0))
    bright = float(np.sqrt(max(1.0 + overlap, 0.0)))
    dark = float(np.sqrt(max(1.0 - overlap, 0.0)))
    if dark == 0.0:
        condition = np.inf
        gram_condition = np.inf
        dual_lower = np.inf
    else:
        condition = bright / dark
        gram_condition = condition * condition
        dual_lower = 1.0 / dark
    return MergeMetrics(
        overlap_modulus=overlap,
        bright_singular_value=bright,
        dark_singular_value=dark,
        synthesis_condition=float(condition),
        gram_condition=float(gram_condition),
        dual_norm_lower_bound=float(dual_lower),
    )
