"""Expanding-circle lift and equivariant flat traces."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq

from .periodic import LAMBDA_FIXED, R_FIXED, U_CRITICAL, quadratic_component_map


TWO_PI = 2.0 * np.pi


def lift_map(theta: np.ndarray | float, *, unwrapped: bool = False) -> np.ndarray:
    """Degree-two circle lift F satisfying pi(F(theta))=T(pi(theta)).

    Here pi(theta)=-r*cos(theta).  If unwrapped is true, the returned real lift
    satisfies F(theta+2*pi)=F(theta)+4*pi.
    """

    angle = np.asarray(theta, dtype=np.float64)
    turns = np.floor(angle / TWO_PI)
    reduced = angle - turns * TWO_PI
    x = -float(R_FIXED) * np.cos(reduced)
    image = quadratic_component_map(x, dtype=np.float64)
    cosine = np.clip(-image / float(R_FIXED), -1.0, 1.0)
    endpoint_tolerance = 64.0 * np.finfo(np.float64).eps
    cosine = np.where(np.abs(cosine - 1.0) <= endpoint_tolerance, 1.0, cosine)
    cosine = np.where(np.abs(cosine + 1.0) <= endpoint_tolerance, -1.0, cosine)
    alpha = np.arccos(cosine)
    quadrant = np.floor(2.0 * reduced / np.pi).astype(np.int64)
    quadrant = np.minimum(quadrant, 3)
    base = np.where(
        quadrant % 2 == 0,
        (quadrant + 2) * np.pi - alpha,
        (quadrant + 1) * np.pi + alpha,
    )
    lifted = base + 2.0 * TWO_PI * turns
    if unwrapped:
        return lifted
    return np.mod(lifted, TWO_PI)


def lift_derivative(theta: np.ndarray | float) -> np.ndarray:
    """Positive derivative of the desingularized circle map."""

    angle = np.asarray(theta, dtype=np.float64)
    x = -float(R_FIXED) * np.cos(angle)
    t = x**2
    u = float(U_CRITICAL)
    squared = (
        16.0
        * (1.0 - u * t) ** 2
        / (u * (2.0 - u * t) * (1.0 - t))
    )
    return np.sqrt(squared)


def iterate_lift(theta: float, length: int) -> tuple[float, float]:
    value = float(theta)
    derivative = 1.0
    for _ in range(length):
        derivative *= float(lift_derivative(value))
        value = float(lift_map(value, unwrapped=True))
    return value, derivative


def _monotone_roots(length: int, twisted: bool) -> list[tuple[float, float]]:
    left = 0.0
    right = TWO_PI

    def value_and_derivative(theta: float) -> tuple[float, float]:
        image, derivative = iterate_lift(theta, length)
        if twisted:
            return image + theta, derivative
        return image - theta, derivative

    left_value, _ = value_and_derivative(left)
    right_value, _ = value_and_derivative(right)
    first = int(np.ceil(left_value / TWO_PI - 1.0e-12))
    last = int(np.floor(right_value / TWO_PI + 1.0e-12))
    roots: list[tuple[float, float]] = []
    for integer in range(first, last + 1):
        target = integer * TWO_PI
        left_residual = left_value - target
        right_residual = right_value - target
        if abs(left_residual) < 2.0e-12:
            root = left
        elif abs(right_residual) < 2.0e-12:
            root = right
        elif left_residual * right_residual < 0.0:
            root = float(
                brentq(
                    lambda point: value_and_derivative(point)[0] - target,
                    left,
                    right,
                    xtol=2.0e-14,
                    rtol=2.0e-14,
                )
            )
        else:
            continue
        if root >= right - 2.0e-12:
            continue
        _, derivative = iterate_lift(root, length)
        roots.append((root, derivative))
    return roots


@dataclass(frozen=True)
class LiftTraceAudit:
    two_step_length: int
    fixed_count: int
    twisted_fixed_count: int
    even_beta_one_trace: float
    odd_beta_two_trace: float
    reconstructed_component_trace: float


def lift_trace_audit(two_step_length: int) -> LiftTraceAudit:
    """Equivariant trace reconstruction of the interval periodic weight."""

    if two_step_length < 1:
        raise ValueError("two_step_length must be positive")
    fixed = _monotone_roots(two_step_length, twisted=False)
    twisted = _monotone_roots(two_step_length, twisted=True)

    def trace(roots: list[tuple[float, float]], beta: int, sign: int) -> float:
        return float(
            sum(
                derivative ** (-beta) / (1.0 - sign / derivative)
                for _, derivative in roots
            )
        )

    a_one = trace(fixed, beta=1, sign=1)
    b_one = trace(twisted, beta=1, sign=-1)
    a_two = trace(fixed, beta=2, sign=1)
    b_two = trace(twisted, beta=2, sign=-1)
    even_one = 0.5 * (a_one + b_one)
    odd_two = 0.5 * (a_two - b_two)
    length = two_step_length
    reconstructed = (
        even_one
        - odd_two
        - float(LAMBDA_FIXED) ** (-length)
        + float(LAMBDA_FIXED) ** (-2 * length)
    )
    return LiftTraceAudit(
        two_step_length=length,
        fixed_count=len(fixed),
        twisted_fixed_count=len(twisted),
        even_beta_one_trace=even_one,
        odd_beta_two_trace=odd_two,
        reconstructed_component_trace=reconstructed,
    )
