"""Outward composition of RH-31, RH-29, and RH-28 certificates."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Mapping

from flint import acb, arb, ctx

from .counts import exact_acb, exact_arb, lower_float, upper_float


@dataclass(frozen=True)
class ComposedBound:
    """One selected-center and selected-arc bound composition."""

    lifted_inverse_upper: float
    denominator_lower: float
    center_inverse_upper: float
    selected_arc_inverse_upper: float
    selected_arc_budget_lower: float
    selected_arc_closed: bool


@dataclass(frozen=True)
class ArcTransportRecord:
    """Outcome of transporting one center bound to one RH-28 arc disc."""

    sigma: float
    arc: int
    selected: bool
    center_distance_upper: float
    disc_distance_upper: float
    neumann_product_lower: float
    neumann_product_upper: float
    transported_inverse_upper: float | None
    arc_budget_lower: float
    status: str


def compose_lifted_bound(
    *,
    threshold: float,
    singular_scalar: float,
    right_residual_upper: float,
    left_residual_upper: float,
    lift: float,
    selected_arc_radius_upper: float,
    selected_arc_budget_lower: float,
    precision: int = 256,
) -> tuple[ComposedBound, arb]:
    """Compose the RH-31 threshold with the exact RH-29 formula.

    All arguments are archived binary64 scalars.  Bounds carrying ``upper``
    or ``lower`` in their names already have the indicated direction in the
    upstream certificate and are embedded as exact dyadic values here.
    """

    previous_precision = ctx.prec
    try:
        ctx.prec = int(precision)
        alpha = exact_arb(threshold)
        singular = exact_arb(singular_scalar)
        right = exact_arb(right_residual_upper)
        left = exact_arb(left_residual_upper)
        tau = exact_arb(lift)
        if not alpha > 0 or not singular > 0 or not tau > 0:
            raise ValueError("threshold, singular scalar, and lift must be positive")
        lifted_inverse = (1 / alpha).upper()
        coefficient = abs(tau - singular).upper()
        denominator = singular - coefficient * lifted_inverse * right
        if not denominator.lower() > 0:
            raise ValueError("the RH-29 Sherman--Morrison denominator is not positive")
        center_bound = (
            lifted_inverse
            + coefficient
            * (1 + lifted_inverse * right)
            * (1 + lifted_inverse * left)
            / (tau * denominator)
        ).upper()
        radius = exact_arb(selected_arc_radius_upper)
        arc_denominator = 1 - radius * center_bound
        if not arc_denominator.lower() > 0:
            raise ValueError("the selected-arc Neumann denominator is not positive")
        arc_bound = (center_bound / arc_denominator).upper()
        budget = exact_arb(selected_arc_budget_lower)
        closed = bool(arc_bound < budget)
        result = ComposedBound(
            lifted_inverse_upper=upper_float(lifted_inverse),
            denominator_lower=lower_float(denominator),
            center_inverse_upper=upper_float(center_bound),
            selected_arc_inverse_upper=upper_float(arc_bound),
            selected_arc_budget_lower=lower_float(budget),
            selected_arc_closed=closed,
        )
        return result, center_bound
    finally:
        ctx.prec = previous_precision


def transport_arc_cover(
    *,
    sigma: float,
    source_center: complex,
    center_inverse_upper: arb,
    arcs: Iterable[Mapping[str, str]],
    selected_arc: int,
    precision: int = 256,
) -> list[ArcTransportRecord]:
    """Audit the exact one-center Neumann transport over all stored arcs."""

    previous_precision = ctx.prec
    records: list[ArcTransportRecord] = []
    try:
        ctx.prec = int(precision)
        source = exact_acb(source_center)
        bound = center_inverse_upper.upper()
        for row in arcs:
            target = acb(
                exact_arb(float(row["center_real"])),
                exact_arb(float(row["center_imag"])),
            )
            center_distance = abs(target - source)
            disc_distance = center_distance + exact_arb(float(row["disc_radius"]))
            product = disc_distance * bound
            product_lower = lower_float(product)
            product_upper = upper_float(product)
            transported: float | None = None
            if product.upper() < 1:
                denominator = 1 - product
                transported_ball = (bound / denominator).upper()
                transported = upper_float(transported_ball)
                budget = exact_arb(float(row["resolvent_budget_lower"]))
                status = (
                    "closed"
                    if transported_ball < budget
                    else "budget_failure"
                )
            elif product.lower() > 1:
                status = "neumann_failure"
            else:
                status = "ambiguous_neumann_boundary"
            records.append(
                ArcTransportRecord(
                    sigma=float(sigma),
                    arc=int(row["arc"]),
                    selected=int(row["arc"]) == int(selected_arc),
                    center_distance_upper=upper_float(center_distance),
                    disc_distance_upper=upper_float(disc_distance),
                    neumann_product_lower=product_lower,
                    neumann_product_upper=product_upper,
                    transported_inverse_upper=transported,
                    arc_budget_lower=math.nextafter(
                        float(row["resolvent_budget_lower"]), -math.inf
                    ),
                    status=status,
                )
            )
    finally:
        ctx.prec = previous_precision
    return records
