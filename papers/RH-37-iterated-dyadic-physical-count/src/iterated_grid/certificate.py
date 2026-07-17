"""Outward-rounded resolvent propagation through one dyadic Schur split."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


@dataclass(frozen=True)
class PropagatedResolventBound:
    """Leafwise bounds for the first refinement and the next Rouch\'e gate."""

    coarse_resolvent_upper: float
    first_effective_product_upper: float
    first_effective_resolvent_upper: float
    column_factor_upper: float
    row_factor_upper: float
    fine_resolvent_upper: float
    second_effective_perturbation_upper: float | None
    second_continuation_product_upper: float | None
    first_gate_closed: bool
    second_gate_closed: bool | None


def _up(value: float) -> float:
    return float(np.nextafter(float(value), np.inf))


def _down(value: float) -> float:
    return float(np.nextafter(float(value), -np.inf))


def _up_add(left: float, right: float) -> float:
    return _up(float(left) + float(right))


def _up_mul(left: float, right: float) -> float:
    return _up(float(left) * float(right))


def _up_sqrt(value: float) -> float:
    return _up(math.sqrt(float(value)))


def _graph_factor(detail_resolvent: float, coupling: float) -> float:
    product = _up_mul(detail_resolvent, coupling)
    square = _up_mul(product, product)
    return _up_sqrt(_up_add(1.0, square))


def propagate_resolvent_bound(
    coarse_resolvent_upper: float,
    *,
    first_effective_perturbation_upper: float,
    first_detail_resolvent_upper: float,
    first_coarse_to_detail_upper: float,
    first_detail_to_coarse_upper: float,
    second_effective_perturbation_upper: float | None = None,
) -> PropagatedResolventBound:
    """Propagate a coarse inverse bound through the exact Schur inverse.

    If ``M = ||(z-A_c)^{-1}||`` and ``M epsilon < 1``, the effective
    inverse is bounded by ``M/(1-M epsilon)``.  The full block inverse is
    then bounded using the exact graph-factorization

    ``[I; R_D C] F^{-1} [I, B R_D] + diag(0, R_D)``.
    """

    coarse = float(coarse_resolvent_upper)
    epsilon = float(first_effective_perturbation_upper)
    product = _up_mul(coarse, epsilon)
    first_closed = bool(product < 1.0)
    column = _graph_factor(
        float(first_detail_resolvent_upper),
        float(first_coarse_to_detail_upper),
    )
    row = _graph_factor(
        float(first_detail_resolvent_upper),
        float(first_detail_to_coarse_upper),
    )
    if first_closed:
        denominator = _down(1.0 - product)
        effective_inverse = _up(coarse / denominator)
        fine = _up_add(
            float(first_detail_resolvent_upper),
            _up_mul(_up_mul(column, row), effective_inverse),
        )
    else:
        effective_inverse = float("inf")
        fine = float("inf")

    if second_effective_perturbation_upper is None:
        second_epsilon = None
        second_product = None
        second_closed = None
    else:
        second_epsilon = float(second_effective_perturbation_upper)
        second_product = _up_mul(fine, second_epsilon)
        second_closed = bool(second_product < 1.0)

    return PropagatedResolventBound(
        coarse_resolvent_upper=coarse,
        first_effective_product_upper=product,
        first_effective_resolvent_upper=effective_inverse,
        column_factor_upper=column,
        row_factor_upper=row,
        fine_resolvent_upper=fine,
        second_effective_perturbation_upper=second_epsilon,
        second_continuation_product_upper=second_product,
        first_gate_closed=first_closed,
        second_gate_closed=second_closed,
    )
