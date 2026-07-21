"""Finite-dimensional Arnoldi identities and directional power bounds."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


def _matrix(value: np.ndarray) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError("operator must be square")
    return result


def _vector(value: np.ndarray, dimension: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128).reshape(-1)
    if result.shape != (dimension,):
        raise ValueError("source must be a vector with matching dimension")
    return result


@dataclass(frozen=True)
class ArnoldiCertificate:
    basis: np.ndarray
    hessenberg: np.ndarray
    residual_vector: np.ndarray
    residual_norm: float
    breakdown: bool

    @property
    def dimension(self) -> int:
        return self.basis.shape[1]


@dataclass(frozen=True)
class KrylovPowerCertificate:
    horizon: int
    krylov_dimension: int
    exact_norm: float
    projected_norm: float
    residual_bound: float
    upper_bound: float
    operator_norm: float
    arnoldi_residual_norm: float
    breakdown: bool


def arnoldi(
    operator: np.ndarray,
    source: np.ndarray,
    dimension: int,
    *,
    tolerance: float = 1.0e-13,
) -> ArnoldiCertificate:
    r"""Build a modified Gram--Schmidt Arnoldi certificate.

    The returned arrays satisfy

    A V = V H + g e_m^*,

    where g is residual_vector and m is the returned Krylov dimension.  A true
    breakdown is recorded when g is numerically zero.
    """

    a = _matrix(operator)
    z = _vector(source, a.shape[0])
    count = int(dimension)
    if count <= 0 or count > a.shape[0]:
        raise ValueError("dimension must lie between 1 and the matrix size")
    threshold = float(tolerance)
    if not math.isfinite(threshold) or threshold <= 0.0:
        raise ValueError("tolerance must be finite and positive")
    source_norm = float(np.linalg.norm(z))
    if source_norm == 0.0:
        raise ValueError("source must be nonzero")

    vectors = [z / source_norm]
    hessenberg = np.zeros((count, count), dtype=np.complex128)
    breakdown = False
    residual_vector = np.zeros(a.shape[0], dtype=np.complex128)
    for column in range(count):
        work = a @ vectors[column]
        for row, vector in enumerate(vectors):
            coefficient = np.vdot(vector, work)
            hessenberg[row, column] = coefficient
            work -= coefficient * vector
        residual_norm = float(np.linalg.norm(work))
        if column == count - 1:
            if residual_norm > threshold:
                residual_vector = work
            else:
                breakdown = True
            break
        if residual_norm <= threshold:
            breakdown = True
            break
        hessenberg[column + 1, column] = residual_norm
        vectors.append(work / residual_norm)

    basis = np.column_stack(vectors)
    reduced = hessenberg[: basis.shape[1], : basis.shape[1]]
    residual_norm = float(np.linalg.norm(residual_vector))
    return ArnoldiCertificate(
        basis=basis,
        hessenberg=reduced,
        residual_vector=residual_vector,
        residual_norm=float(np.linalg.norm(residual_vector)),
        breakdown=breakdown,
    )


def _power(matrix: np.ndarray, exponent: int) -> np.ndarray:
    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    return np.linalg.matrix_power(matrix, exponent)


def krylov_power_certificate(
    operator: np.ndarray,
    source: np.ndarray,
    horizon: int,
    krylov_dimension: int,
    *,
    operator_norm: float | None = None,
    arnoldi_tolerance: float = 1.0e-13,
) -> KrylovPowerCertificate:
    r"""Bound the directional power using a projected power and one residual.

    If A V = V H + g e_m^* and z=V beta, then

    A^L z = V H^L beta +
      sum_j A^(L-1-j) g e_m^* H^j beta.

    The residual term is bounded with the supplied operator norm.  The
    estimate depends on the actual Krylov coefficients rather than only on
    the ordinary norm power.
    """

    a = _matrix(operator)
    z = _vector(source, a.shape[0])
    length = int(horizon)
    if length < 0:
        raise ValueError("horizon must be nonnegative")
    certificate = arnoldi(
        a,
        z,
        krylov_dimension,
        tolerance=arnoldi_tolerance,
    )
    v = certificate.basis
    h = certificate.hessenberg
    beta = np.zeros(v.shape[1], dtype=np.complex128)
    beta[0] = np.linalg.norm(z)
    projected = v @ (_power(h, length) @ beta)
    residual_bound = 0.0
    if certificate.residual_norm > 0.0:
        rho = float(np.linalg.norm(a, 2) if operator_norm is None else operator_norm)
        if not math.isfinite(rho) or rho < 0.0:
            raise ValueError("operator_norm must be finite and nonnegative")
        power_h = np.eye(h.shape[0], dtype=np.complex128)
        last = h.shape[0] - 1
        selector = np.zeros(h.shape[0], dtype=np.complex128)
        selector[last] = 1.0
        for index in range(length):
            coefficient = np.vdot(selector, power_h @ beta)
            residual_bound += (
                rho ** (length - 1 - index)
                * certificate.residual_norm
                * abs(coefficient)
            )
            power_h = h @ power_h
    exact = float(np.linalg.norm(_power(a, length) @ z))
    projected_norm = float(np.linalg.norm(projected))
    return KrylovPowerCertificate(
        horizon=length,
        krylov_dimension=certificate.dimension,
        exact_norm=exact,
        projected_norm=projected_norm,
        residual_bound=float(residual_bound),
        upper_bound=float(projected_norm + residual_bound),
        operator_norm=float(
            np.linalg.norm(a, 2) if operator_norm is None else operator_norm
        ),
        arnoldi_residual_norm=certificate.residual_norm,
        breakdown=certificate.breakdown,
    )


def geometric_power_upper(
    operator_norm: float,
    source: np.ndarray,
    horizon: int,
) -> float:
    """Return the ordinary norm-power upper."""

    rho = float(operator_norm)
    if not math.isfinite(rho) or rho < 0.0:
        raise ValueError("operator_norm must be finite and nonnegative")
    length = int(horizon)
    if length < 0:
        raise ValueError("horizon must be nonnegative")
    return float(rho**length * np.linalg.norm(np.asarray(source)))


def stein_krylov_tail_upper(
    kappa: float,
    certificate: KrylovPowerCertificate,
) -> float:
    """Multiply a directional power certificate by a Stein factor."""

    multiplier = float(kappa)
    if not math.isfinite(multiplier) or multiplier < 0.0:
        raise ValueError("kappa must be finite and nonnegative")
    return math.sqrt(multiplier) * certificate.upper_bound
