"""Primal-dual residual identities for goal-oriented Feshbach corrections."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class PrimalDualCorrection:
    """Computed correction and coefficients multiplying a resolvent bound."""

    primal_residual: np.ndarray
    dual_residual: np.ndarray
    primal_correction: np.ndarray
    dual_weighted_correction: np.ndarray
    computed_correction: np.ndarray
    primal_rouche_ratio: float
    dual_weighted_rouche_ratio: float
    computed_rouche_ratio: float
    one_sided_resolvent_coefficient: float
    primal_dual_resolvent_coefficient: float
    one_sided_resolvent_budget: float
    primal_dual_resolvent_budget: float


def _matrix_rouche_ratio(base: np.ndarray, perturbation: np.ndarray) -> float:
    return float(np.linalg.norm(np.linalg.solve(base, perturbation), ord=2))


def resolvent_budget(computed_ratio: float, coefficient: float) -> float:
    r"""Return ``(1-computed_ratio)/coefficient`` with exact edge handling."""

    ratio = float(computed_ratio)
    factor = float(coefficient)
    if ratio < 0.0 or factor < 0.0:
        raise ValueError("ratio and coefficient must be nonnegative")
    if ratio >= 1.0:
        return 0.0
    if factor == 0.0:
        return float("inf")
    return float((1.0 - ratio) / factor)


def primal_dual_correction(
    shifted: np.ndarray,
    observation: np.ndarray,
    base_feshbach: np.ndarray,
    primary_rhs: np.ndarray,
    primal_approximation: np.ndarray,
    dual_approximation: np.ndarray,
) -> PrimalDualCorrection:
    r"""Evaluate the exact primal-dual decomposition data.

    Let ``A=shifted``, ``E=observation``, and let the desired Feshbach
    perturbation be ``-E A^{-1} R``.  For approximate primal and dual solves
    ``Y`` and ``Z``, define

    ``r = R-A Y`` and ``s = E^*-A^* Z``.

    Then

    ``-E A^{-1}R = -E Y-Z^*r-s^*A^{-1}r``.

    The returned coefficients multiply any upper bound for ``||A^{-1}||``.
    The primal-dual coefficient keeps the computable alignment
    ``||F_J^{-1}s^*||`` instead of splitting it into two global factors.
    """

    operator = np.asarray(shifted, dtype=np.complex128)
    observed = np.asarray(observation, dtype=np.complex128)
    base = np.asarray(base_feshbach, dtype=np.complex128)
    right_hand_side = np.asarray(primary_rhs, dtype=np.complex128)
    primal = np.asarray(primal_approximation, dtype=np.complex128)
    dual = np.asarray(dual_approximation, dtype=np.complex128)
    if operator.ndim != 2 or operator.shape[0] != operator.shape[1]:
        raise ValueError("shifted must be square")
    ambient = operator.shape[0]
    if base.ndim != 2 or base.shape[0] != base.shape[1]:
        raise ValueError("base_feshbach must be square")
    rank = base.shape[0]
    if observed.shape != (rank, ambient):
        raise ValueError("observation has incompatible shape")
    expected = (ambient, rank)
    if any(array.shape != expected for array in (right_hand_side, primal, dual)):
        raise ValueError("right-hand side and approximations have incompatible shape")

    primal_residual = right_hand_side - operator @ primal
    dual_residual = observed.conj().T - operator.conj().T @ dual
    return primal_dual_correction_from_residuals(
        observed,
        base,
        primal,
        primal_residual,
        dual,
        dual_residual,
    )


def primal_dual_correction_from_residuals(
    observation: np.ndarray,
    base_feshbach: np.ndarray,
    primal_approximation: np.ndarray,
    primal_residual: np.ndarray,
    dual_approximation: np.ndarray,
    dual_residual: np.ndarray,
) -> PrimalDualCorrection:
    """Evaluate the correction from explicitly checked primal/dual residuals.

    This matrix-free entry point is algebraically identical to
    :func:`primal_dual_correction`; it avoids forming the ambient shifted
    operator when the two residual blocks were evaluated by operator calls.
    """

    observed = np.asarray(observation, dtype=np.complex128)
    base = np.asarray(base_feshbach, dtype=np.complex128)
    primal = np.asarray(primal_approximation, dtype=np.complex128)
    residual = np.asarray(primal_residual, dtype=np.complex128)
    dual = np.asarray(dual_approximation, dtype=np.complex128)
    dual_defect = np.asarray(dual_residual, dtype=np.complex128)
    if base.ndim != 2 or base.shape[0] != base.shape[1]:
        raise ValueError("base_feshbach must be square")
    rank = base.shape[0]
    if observed.ndim != 2 or observed.shape[0] != rank:
        raise ValueError("observation has incompatible shape")
    ambient = observed.shape[1]
    expected = (ambient, rank)
    if any(
        array.shape != expected
        for array in (primal, residual, dual, dual_defect)
    ):
        raise ValueError("approximations and residuals have incompatible shape")

    primal_correction = -observed @ primal
    dual_weighted_correction = -dual.conj().T @ residual
    computed = primal_correction + dual_weighted_correction
    primal_ratio = _matrix_rouche_ratio(base, primal_correction)
    dual_ratio = _matrix_rouche_ratio(base, dual_weighted_correction)
    computed_ratio = _matrix_rouche_ratio(base, computed)
    residual_norm = float(np.linalg.norm(residual, 2))
    one_sided = float(
        np.linalg.norm(np.linalg.solve(base, observed), 2) * residual_norm
    )
    dual_factor = np.linalg.solve(base, dual_defect.conj().T)
    primal_dual = float(np.linalg.norm(dual_factor, 2) * residual_norm)
    return PrimalDualCorrection(
        primal_residual=residual,
        dual_residual=dual_defect,
        primal_correction=primal_correction,
        dual_weighted_correction=dual_weighted_correction,
        computed_correction=computed,
        primal_rouche_ratio=primal_ratio,
        dual_weighted_rouche_ratio=dual_ratio,
        computed_rouche_ratio=computed_ratio,
        one_sided_resolvent_coefficient=one_sided,
        primal_dual_resolvent_coefficient=primal_dual,
        one_sided_resolvent_budget=resolvent_budget(primal_ratio, one_sided),
        primal_dual_resolvent_budget=resolvent_budget(
            computed_ratio, primal_dual
        ),
    )


def exact_identity_residual(
    shifted: np.ndarray,
    observation: np.ndarray,
    primary_rhs: np.ndarray,
    result: PrimalDualCorrection,
) -> float:
    """Return the relative residual in the exact primal-dual identity."""

    operator = np.asarray(shifted, dtype=np.complex128)
    observed = np.asarray(observation, dtype=np.complex128)
    right_hand_side = np.asarray(primary_rhs, dtype=np.complex128)
    exact = -observed @ np.linalg.solve(operator, right_hand_side)
    remainder = -result.dual_residual.conj().T @ np.linalg.solve(
        operator, result.primal_residual
    )
    reconstructed = result.computed_correction + remainder
    scale = max(
        np.linalg.norm(exact, 2),
        np.linalg.norm(reconstructed, 2),
        np.finfo(float).tiny,
    )
    return float(np.linalg.norm(exact - reconstructed, 2) / scale)
