"""All-order Cauchy tails for the Hardy-scaled deterministic numerator."""

from __future__ import annotations

import math


def scaled_zero_free_radius(hardy_radius: float, numerator_radius: float) -> float:
    """Return the zero-free radius of ``G(z / r_H)``."""

    hardy = float(hardy_radius)
    radius = float(numerator_radius)
    if not 0.0 < hardy < 1.0 or radius <= 1.0:
        raise ValueError("the Hardy radius must lie in (0,1) and the numerator radius exceed one")
    return hardy * radius


def cauchy_tail_factor(
    disk_radius: float,
    cauchy_radius: float,
    first_omitted_order: int,
) -> float:
    """Return the factor multiplying ``sup_|z|=S |log G_H(z)|``.

    If ``log G_H(z)=-sum a_n z^n/n`` is holomorphic on ``|z|<S`` and
    ``R<S``, then the logarithmic target tail from order ``N`` is at most
    ``M_S * cauchy_tail_factor(R, S, N)``.
    """

    inner = float(disk_radius)
    outer = float(cauchy_radius)
    order = int(first_omitted_order)
    if inner < 0.0 or outer <= 0.0 or inner >= outer or order < 1:
        raise ValueError("require 0 <= R < S and a positive first omitted order")
    ratio = inner / outer
    return float(ratio**order / (1.0 - ratio))


def logarithmic_target_tail_bound(
    log_boundary_supremum: float,
    disk_radius: float,
    cauchy_radius: float,
    first_omitted_order: int,
) -> float:
    """Bound ``sum_{n>=N} |a_n| R^n/n`` by Cauchy's estimate."""

    supremum = float(log_boundary_supremum)
    if supremum < 0.0 or not math.isfinite(supremum):
        raise ValueError("the logarithmic boundary supremum must be finite and nonnegative")
    return supremum * cauchy_tail_factor(
        disk_radius, cauchy_radius, first_omitted_order
    )


def multiplicative_tail_error(logarithmic_tail: float) -> float:
    """Convert a logarithmic tail to the relative exponential error."""

    value = float(logarithmic_tail)
    if value < 0.0 or not math.isfinite(value):
        raise ValueError("the logarithmic tail must be finite and nonnegative")
    return float(math.expm1(value))
