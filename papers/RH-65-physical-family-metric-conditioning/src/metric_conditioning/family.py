"""High-precision Lyapunov metrics for near-peripheral Jordan families."""

from __future__ import annotations

from dataclasses import dataclass
import math

import mpmath as mp


@dataclass(frozen=True)
class MetricLedger:
    """Conditioning data for the canonical discrete Lyapunov metric."""

    dimension: int
    gap: mp.mpf
    coupling: mp.mpf
    lambda_min: mp.mpf
    lambda_max: mp.mpf
    condition_number: mp.mpf
    contraction: mp.mpf
    contraction_gap: mp.mpf
    transfer_factor: mp.mpf


def _positive_mpf(value: object, name: str) -> mp.mpf:
    result = mp.mpf(value)
    if not mp.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def jordan_chain(
    dimension: int,
    gap: object,
    coupling: object,
) -> mp.matrix:
    """Return A=sqrt(1-gap) I + coupling*N with N the upper shift."""

    size = int(dimension)
    if size < 1:
        raise ValueError("dimension must be positive")
    s = _positive_mpf(gap, "gap")
    if s >= 1:
        raise ValueError("gap must be smaller than one")
    c = mp.mpf(coupling)
    if not mp.isfinite(c) or c < 0:
        raise ValueError("coupling must be finite and nonnegative")
    q = mp.sqrt(1 - s)
    operator = mp.matrix(size)
    for index in range(size):
        operator[index, index] = q
        if index + 1 < size:
            operator[index, index + 1] = c
    return operator


def _kronecker(left: mp.matrix, right: mp.matrix) -> mp.matrix:
    result = mp.matrix(
        left.rows * right.rows,
        left.cols * right.cols,
    )
    for i in range(left.rows):
        for j in range(left.cols):
            for k in range(right.rows):
                for ell in range(right.cols):
                    result[i * right.rows + k, j * right.cols + ell] = (
                        left[i, j] * right[k, ell]
                    )
    return result


def lyapunov_metric(operator: mp.matrix) -> mp.matrix:
    """Solve M-A^T M A=I by high-precision vectorization."""

    if operator.rows != operator.cols or operator.rows == 0:
        raise ValueError("operator must be nonempty and square")
    size = operator.rows
    coefficient = mp.eye(size * size) - _kronecker(
        operator.T,
        operator.T,
    )
    identity_vector = mp.matrix(
        [
            1 if row == column else 0
            for column in range(size)
            for row in range(size)
        ]
    )
    solution = mp.lu_solve(coefficient, identity_vector)
    metric = mp.matrix(size)
    for column in range(size):
        for row in range(size):
            metric[row, column] = solution[column * size + row]
    return (metric + metric.T) / 2


def exact_two_step_metric(gap: object, coupling: object) -> mp.matrix:
    """Closed form for the two-dimensional Jordan-chain metric."""

    s = _positive_mpf(gap, "gap")
    if s >= 1:
        raise ValueError("gap must be smaller than one")
    c = mp.mpf(coupling)
    if not mp.isfinite(c) or c < 0:
        raise ValueError("coupling must be finite and nonnegative")
    q = mp.sqrt(1 - s)
    m11 = 1 / s
    m12 = q * c / (s * s)
    m22 = 1 / s + c * c * (1 + q * q) / (s**3)
    return mp.matrix([[m11, m12], [m12, m22]])


def lyapunov_residual(operator: mp.matrix, metric: mp.matrix) -> mp.matrix:
    """Return M-A^T M A-I."""

    if operator.rows != operator.cols or metric.rows != metric.cols:
        raise ValueError("operator and metric must be square")
    if operator.rows != metric.rows:
        raise ValueError("operator and metric dimensions must agree")
    return metric - operator.T * metric * operator - mp.eye(operator.rows)


def max_abs_entry(matrix: mp.matrix) -> mp.mpf:
    """Maximum absolute matrix entry."""

    return max(
        (abs(matrix[row, column]) for row in range(matrix.rows)
         for column in range(matrix.cols)),
        default=mp.mpf("0"),
    )


def metric_ledger(
    dimension: int,
    gap: object,
    coupling: object,
    *,
    dps: int = 120,
) -> MetricLedger:
    """Compute the exact-identity conditioning ledger at high precision."""

    precision = int(dps)
    if precision < 40:
        raise ValueError("dps must be at least 40")
    with mp.workdps(precision):
        s = _positive_mpf(gap, "gap")
        c = mp.mpf(coupling)
        operator = jordan_chain(dimension, s, c)
        metric = lyapunov_metric(operator)
        eigenvalues = mp.eigsy(metric, eigvals_only=True)
        lambda_min = +eigenvalues[0]
        lambda_max = +eigenvalues[-1]
        if lambda_min <= 0:
            raise ArithmeticError("computed metric is not positive")
        inverse_maximum = 1 / lambda_max
        contraction = mp.sqrt(1 - inverse_maximum)
        contraction_gap = inverse_maximum / (1 + contraction)
        return MetricLedger(
            dimension=int(dimension),
            gap=+s,
            coupling=+c,
            lambda_min=lambda_min,
            lambda_max=lambda_max,
            condition_number=lambda_max / lambda_min,
            contraction=contraction,
            contraction_gap=contraction_gap,
            transfer_factor=mp.sqrt(lambda_max / lambda_min),
        )


def contraction_horizon(
    contraction: object,
    tolerance: object,
) -> int:
    """Smallest L with contraction**L <= tolerance."""

    q = mp.mpf(contraction)
    epsilon = mp.mpf(tolerance)
    if not (0 < q < 1):
        raise ValueError("contraction must lie strictly between zero and one")
    if not (0 < epsilon < 1):
        raise ValueError("tolerance must lie strictly between zero and one")
    return int(mp.ceil(mp.log(epsilon) / mp.log(q)))


def theoretical_exponents(dimension: int, coupling_power: float) -> tuple[float, float]:
    """Return the predicted cond and metric-gap exponents for alpha<=1."""

    size = int(dimension)
    alpha = float(coupling_power)
    if size < 1 or not math.isfinite(alpha) or alpha < 0:
        raise ValueError("invalid dimension or coupling power")
    excess = max(0.0, 1.0 - alpha)
    condition_exponent = 2.0 * (size - 1) * excess
    return condition_exponent, 1.0 + condition_exponent
