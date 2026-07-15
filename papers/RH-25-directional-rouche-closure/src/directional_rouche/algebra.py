"""Directional Feshbach corrections and contour-majorant utilities."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class DirectionalCorrection:
    """Exact correction of one approximate external block solve."""

    residual: np.ndarray
    correction_solution: np.ndarray
    approximate_feshbach: np.ndarray
    corrected_feshbach: np.ndarray
    feshbach_perturbation: np.ndarray
    rouche_ratio: float
    identity_residual: float


@dataclass(frozen=True)
class TailMajorant:
    """Conditional geometric majorant inferred from two increments."""

    first_increment: float
    second_increment: float
    contraction_ratio: float
    total_from_base: float
    future_after_second: float
    admissible: bool


def matrix_rouche_ratio(base: np.ndarray, perturbation: np.ndarray) -> float:
    r"""Return ``||base^{-1} perturbation||_2``."""

    first = np.asarray(base, dtype=np.complex128)
    delta = np.asarray(perturbation, dtype=np.complex128)
    if first.ndim != 2 or first.shape[0] != first.shape[1]:
        raise ValueError("base must be square")
    if delta.shape != first.shape:
        raise ValueError("perturbation and base must have the same shape")
    return float(np.linalg.norm(np.linalg.solve(first, delta), ord=2))


def exact_directional_correction(
    external_matrix: np.ndarray,
    reduced: np.ndarray,
    forcing: np.ndarray,
    observation: np.ndarray,
    approximate_solution: np.ndarray,
    spectral_parameter: complex,
) -> DirectionalCorrection:
    r"""Correct ``(zI-B)X=C`` and verify ``F-F_J=-E(zI-B)^{-1}R``.

    The residual convention is ``R=C-(zI-B)X``.  Consequently the exact
    external solution is ``X+(zI-B)^{-1}R`` and the exact Feshbach matrix is
    the approximate matrix minus ``E(zI-B)^{-1}R``.
    """

    external = np.asarray(external_matrix, dtype=np.complex128)
    direct = np.asarray(reduced, dtype=np.complex128)
    source = np.asarray(forcing, dtype=np.complex128)
    observed = np.asarray(observation, dtype=np.complex128)
    approximate = np.asarray(approximate_solution, dtype=np.complex128)
    if external.ndim != 2 or external.shape[0] != external.shape[1]:
        raise ValueError("external_matrix must be square")
    ambient = external.shape[0]
    rank = direct.shape[0]
    if direct.shape != (rank, rank):
        raise ValueError("reduced must be square")
    if source.shape != (ambient, rank) or approximate.shape != source.shape:
        raise ValueError("forcing and approximate solution have incompatible shapes")
    if observed.shape != (rank, ambient):
        raise ValueError("observation has incompatible shape")
    zeta = complex(spectral_parameter)
    shifted = zeta * np.eye(ambient, dtype=np.complex128) - external
    residual = source - shifted @ approximate
    correction_solution = np.linalg.solve(shifted, residual)
    approximate_feshbach = (
        zeta * np.eye(rank, dtype=np.complex128)
        - direct
        - observed @ approximate
    )
    perturbation = -observed @ correction_solution
    corrected = approximate_feshbach + perturbation
    exact_solution = np.linalg.solve(shifted, source)
    direct_exact = zeta * np.eye(rank) - direct - observed @ exact_solution
    scale = max(
        np.linalg.norm(direct_exact),
        np.linalg.norm(corrected),
        np.finfo(float).tiny,
    )
    return DirectionalCorrection(
        residual=residual,
        correction_solution=correction_solution,
        approximate_feshbach=approximate_feshbach,
        corrected_feshbach=corrected,
        feshbach_perturbation=perturbation,
        rouche_ratio=matrix_rouche_ratio(approximate_feshbach, perturbation),
        identity_residual=float(np.linalg.norm(corrected - direct_exact) / scale),
    )


def global_scalar_majorant(
    inverse_feshbach_norm: float,
    observation_norm: float,
    external_resolvent_norm: float,
    residual_norm: float,
) -> float:
    r"""Return the scalar majorant for a directional Rouch\'e perturbation."""

    values = np.asarray(
        (
            inverse_feshbach_norm,
            observation_norm,
            external_resolvent_norm,
            residual_norm,
        ),
        dtype=np.float64,
    )
    if np.any(values < 0.0) or not np.all(np.isfinite(values)):
        raise ValueError("all majorant factors must be finite and nonnegative")
    return float(np.prod(values))


def geometric_tail_majorant(
    first_increment: float,
    second_increment: float,
) -> TailMajorant:
    r"""Return a conditional geometric tail bound from consecutive increments.

    If all increments after the second contract by at most
    ``q=second/first<1``, then the total perturbation from the base is at
    most ``first + second/(1-q)``.  The function does not infer that the
    observed ratio persists; it only evaluates the stated conditional bound.
    """

    first = float(first_increment)
    second = float(second_increment)
    if first < 0.0 or second < 0.0:
        raise ValueError("increments must be nonnegative")
    if first == 0.0:
        admissible = second == 0.0
        ratio = 0.0 if admissible else float("inf")
        total = 0.0 if admissible else float("inf")
        future = 0.0 if admissible else float("inf")
    else:
        ratio = second / first
        admissible = ratio < 1.0
        if admissible:
            future = second * ratio / (1.0 - ratio)
            total = first + second / (1.0 - ratio)
        else:
            future = float("inf")
            total = float("inf")
    return TailMajorant(
        first_increment=first,
        second_increment=second,
        contraction_ratio=float(ratio),
        total_from_base=float(total),
        future_after_second=float(future),
        admissible=bool(admissible),
    )


def circular_lipschitz_lower_bound(
    singular_value_lower_samples: np.ndarray,
    radius: float,
) -> float:
    r"""Extend nodal lower bounds for ``s_min(zI-B)`` over a circle.

    Singular values are one-Lipschitz in the spectral parameter.  For
    equally spaced samples, every point of an arc is at chord distance at
    most ``2 r sin(pi/(2N))`` from one endpoint.  The returned value is thus
    a rigorous full-circle lower bound whenever the supplied nodal values
    are themselves rigorous lower bounds.
    """

    samples = np.asarray(singular_value_lower_samples, dtype=np.float64)
    if samples.ndim != 1 or samples.size < 4:
        raise ValueError("at least four singular-value samples are required")
    if np.any(samples < 0.0) or float(radius) <= 0.0:
        raise ValueError("samples must be nonnegative and radius positive")
    half_chord = 2.0 * float(radius) * np.sin(np.pi / (2.0 * samples.size))
    interval_minima = np.minimum(samples, np.roll(samples, -1)) - half_chord
    return float(max(0.0, np.min(interval_minima)))


def determinant_winding(phases: np.ndarray) -> tuple[float, int, float]:
    """Return floating winding, nearest integer, and maximum phase step."""

    values = np.asarray(phases, dtype=np.float64)
    if values.ndim != 1 or values.size < 4:
        raise ValueError("at least four determinant phases are required")
    increments = np.angle(np.exp(1.0j * (np.roll(values, -1) - values)))
    floating = float(np.sum(increments) / (2.0 * np.pi))
    return floating, int(np.rint(floating)), float(np.max(np.abs(increments)))


def fom_external_solution(model, spectral_parameter: complex, *, depth: int) -> np.ndarray:
    """Reconstruct all FOM external solution columns from retained bases."""

    if model.retained_bases is None:
        raise ValueError("the Arnoldi model does not retain ambient bases")
    selected = int(depth)
    if selected < 1 or selected > model.maximum_depth:
        raise ValueError("depth is outside the retained Arnoldi range")
    zeta = complex(spectral_parameter)
    columns = []
    for column in range(model.packet_rank):
        hessenberg = np.asarray(model.hessenbergs[column])[:selected, :selected]
        right_hand_side = np.zeros(selected, dtype=np.complex128)
        right_hand_side[0] = float(model.forcing_norms[column])
        coordinates = np.linalg.solve(
            zeta * np.eye(selected, dtype=np.complex128) - hessenberg,
            right_hand_side,
        )
        basis = np.asarray(model.retained_bases[column])[:, :selected]
        columns.append(basis @ coordinates)
    return np.column_stack(columns)
