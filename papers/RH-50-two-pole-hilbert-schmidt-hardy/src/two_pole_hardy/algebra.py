"""Exact finite-dimensional algebra behind two-pole Hardy certificates."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy.linalg import solve_discrete_lyapunov


def _positive(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def two_pole_projector(
    right: np.ndarray, left: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Return the biorthogonal rank-two projector and corrected left modes."""

    r = np.asarray(right, dtype=np.complex128)
    ell = np.asarray(left, dtype=np.complex128)
    if r.ndim != 2 or ell.shape != r.shape or r.shape[1] != 2:
        raise ValueError("right and left must be equally sized two-column arrays")
    gram = ell.conjugate().T @ r
    corrected_left = ell @ np.linalg.inv(gram).conjugate().T
    projection = r @ corrected_left.conjugate().T
    return projection, corrected_left


def two_pole_bulk_matrix(
    matrix: np.ndarray,
    right: np.ndarray,
    left: np.ndarray,
    eigenvalues: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Remove two biorthogonal eigenvalue channels from a dense matrix."""

    operator = np.asarray(matrix, dtype=np.complex128)
    values = np.asarray(eigenvalues, dtype=np.complex128).reshape(-1)
    if operator.ndim != 2 or operator.shape[0] != operator.shape[1]:
        raise ValueError("matrix must be square")
    if values.shape != (2,):
        raise ValueError("exactly two eigenvalues are required")
    projection, corrected_left = two_pole_projector(right, left)
    r = np.asarray(right, dtype=np.complex128)
    bulk = operator - r @ np.diag(values) @ corrected_left.conjugate().T
    return bulk, projection, corrected_left


def hardy_energy(sequence, radius: float) -> float:
    r"""Return ``(sum r^(-2m) ||X_m||^2)^(1/2)`` from norm data."""

    value = _positive(radius, "radius")
    terms = np.asarray(sequence, dtype=np.float64)
    if terms.ndim != 1 or np.any(~np.isfinite(terms)) or np.any(terms < 0.0):
        raise ValueError("sequence must contain finite nonnegative norms")
    powers = value ** (-2.0 * np.arange(terms.size, dtype=np.float64))
    return float(np.sqrt(np.dot(powers, terms * terms)))


@dataclass(frozen=True)
class HardyResolventUpper:
    """Cauchy--Schwarz upper obtained from one directional Hardy energy."""

    energy: float
    energy_radius: float
    contour_modulus_lower: float
    cauchy_factor: float
    resolvent_action_upper: float


def hardy_resolvent_upper(
    energy: float, radius: float, contour_modulus_lower: float
) -> HardyResolventUpper:
    r"""Bound a Laurent range action by its weighted square-sum energy."""

    norm = _positive(energy, "energy")
    r = _positive(radius, "radius")
    modulus = _positive(contour_modulus_lower, "contour_modulus_lower")
    if r >= modulus:
        raise ValueError("Hardy radius must be below the contour modulus")
    factor = 1.0 / math.sqrt(modulus * modulus - r * r)
    return HardyResolventUpper(
        energy=norm,
        energy_radius=r,
        contour_modulus_lower=modulus,
        cauchy_factor=factor,
        resolvent_action_upper=factor * norm,
    )


def controllability_gramian(
    bulk: np.ndarray, source: np.ndarray, radius: float
) -> np.ndarray:
    r"""Solve ``G=(N/r)G(N/r)^*+EE^*`` for a stable scaled bulk."""

    operator = np.asarray(bulk, dtype=np.complex128)
    forcing = np.asarray(source, dtype=np.complex128)
    r = _positive(radius, "radius")
    return solve_discrete_lyapunov(
        operator / r, forcing @ forcing.conjugate().T
    )


def observability_gramian(
    bulk: np.ndarray, observation: np.ndarray, radius: float
) -> np.ndarray:
    r"""Solve ``O=(N/r)^*O(N/r)+C^*C`` for a stable scaled bulk."""

    operator = np.asarray(bulk, dtype=np.complex128)
    observed = np.asarray(observation, dtype=np.complex128)
    r = _positive(radius, "radius")
    return solve_discrete_lyapunov(
        operator.conjugate().T / r,
        observed.conjugate().T @ observed,
    )


@dataclass(frozen=True)
class LyapunovCertificate:
    """Positive supersolution certificate for one controllability Gramian."""

    admissible: bool
    residual_minimum_eigenvalue: float
    trace_upper: float


def lyapunov_supersolution_certificate(
    bulk: np.ndarray,
    source: np.ndarray,
    candidate: np.ndarray,
    radius: float,
    *,
    tolerance: float = 1.0e-12,
) -> LyapunovCertificate:
    r"""Check ``H-(N/r)H(N/r)^* >= EE^*`` and return ``tr(H)``."""

    operator = np.asarray(bulk, dtype=np.complex128)
    forcing = np.asarray(source, dtype=np.complex128)
    trial = np.asarray(candidate, dtype=np.complex128)
    r = _positive(radius, "radius")
    if trial.shape != operator.shape:
        raise ValueError("candidate has incompatible shape")
    hermitian_defect = np.linalg.norm(trial - trial.conjugate().T, 2)
    if hermitian_defect > float(tolerance):
        raise ValueError("candidate must be Hermitian")
    scaled = operator / r
    residual = (
        trial
        - scaled @ trial @ scaled.conjugate().T
        - forcing @ forcing.conjugate().T
    )
    residual = 0.5 * (residual + residual.conjugate().T)
    minimum = float(np.min(np.linalg.eigvalsh(residual)).real)
    trace = float(np.trace(trial).real)
    return LyapunovCertificate(
        admissible=(minimum >= -float(tolerance) and trace >= 0.0),
        residual_minimum_eigenvalue=minimum,
        trace_upper=trace,
    )
