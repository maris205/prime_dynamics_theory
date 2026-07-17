"""Outward one-center transport to archived RH-28 arc discs."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping

from flint import acb, arb, ctx


@dataclass(frozen=True)
class ArcCoverage:
    arc: int
    distance_upper: float
    neumann_product_upper: float
    transported_inverse_upper: float | None
    budget_lower: float
    closed: bool


def _exact_arb(value: float) -> arb:
    return arb(float(value))


def _exact_acb(value: complex) -> acb:
    point = complex(value)
    return acb(_exact_arb(point.real), _exact_arb(point.imag))


def _upper_float(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def _lower_float(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def certify_arc_coverage(
    source_center: complex,
    center_inverse_upper: float,
    row: Mapping[str, str],
    *,
    precision: int = 256,
) -> ArcCoverage:
    previous_precision = ctx.prec
    try:
        ctx.prec = int(precision)
        source = _exact_acb(source_center)
        target = acb(
            _exact_arb(float(row["center_real"])),
            _exact_arb(float(row["center_imag"])),
        )
        center_distance = abs(target - source)
        distance = center_distance + _exact_arb(float(row["disc_radius"]))
        bound = _exact_arb(float(center_inverse_upper)).upper()
        product = distance * bound
        budget = _exact_arb(float(row["resolvent_budget_lower"]))
        transported = None
        closed = False
        if product.upper() < 1:
            denominator = 1 - product
            transported_ball = (bound / denominator).upper()
            transported = _upper_float(transported_ball)
            closed = bool(transported_ball < budget)
        return ArcCoverage(
            arc=int(row["arc"]),
            distance_upper=_upper_float(distance),
            neumann_product_upper=_upper_float(product),
            transported_inverse_upper=transported,
            budget_lower=_lower_float(budget),
            closed=closed,
        )
    finally:
        ctx.prec = previous_precision
