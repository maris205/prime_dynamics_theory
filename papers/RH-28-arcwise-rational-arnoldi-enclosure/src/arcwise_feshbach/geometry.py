"""Arb-backed circular arc covers."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from flint import acb, arb, ctx


@dataclass(frozen=True)
class ArcDisc:
    index: int
    angle: float
    center: complex
    radius: float
    start_numerator: int = 0
    end_numerator: int = 1
    turn_denominator: int = 1
    refinement_level: int = 0


def fractional_circular_arc_disc(
    contour_center: complex,
    contour_radius: float,
    start_numerator: int,
    end_numerator: int,
    turn_denominator: int,
    *,
    index: int = 0,
    refinement_level: int = 0,
    decimal_digits: int = 80,
) -> ArcDisc:
    """Cover one rational-turn circular subarc by a rigorous complex disc."""

    start = int(start_numerator)
    end = int(end_numerator)
    denominator = int(turn_denominator)
    if denominator < 1 or start < 0 or end <= start or end > denominator:
        raise ValueError("invalid rational-turn arc")
    radius = float(contour_radius)
    if radius <= 0.0:
        raise ValueError("contour radius must be positive")
    ctx.dps = int(decimal_digits)
    pi = arb.pi()
    c_real = arb(float(complex(contour_center).real))
    c_imag = arb(float(complex(contour_center).imag))
    r_ball = arb(radius)
    theta = arb(start + end) * pi / arb(denominator)
    half_chord = (
        arb(2.0)
        * r_ball
        * (arb(end - start) * pi / arb(2 * denominator)).sin()
    )
    real_ball = c_real + r_ball * theta.cos()
    imag_ball = c_imag + r_ball * theta.sin()
    center = complex(float(real_ball.mid()), float(imag_ball.mid()))
    center_error = abs(
        acb(real_ball, imag_ball) - acb(arb(center.real), arb(center.imag))
    )
    cover_radius = float((half_chord + center_error).upper())
    cover_radius = float(np.nextafter(cover_radius, np.inf))
    return ArcDisc(
        index=int(index),
        angle=float((start + end) * np.pi / denominator),
        center=center,
        radius=cover_radius,
        start_numerator=start,
        end_numerator=end,
        turn_denominator=denominator,
        refinement_level=int(refinement_level),
    )


def bisect_circular_arc_disc(
    arc: ArcDisc,
    contour_center: complex,
    contour_radius: float,
    *,
    first_index: int = 0,
    decimal_digits: int = 80,
) -> tuple[ArcDisc, ArcDisc]:
    """Return two exact dyadic children whose subarcs partition ``arc``."""

    start = int(arc.start_numerator)
    end = int(arc.end_numerator)
    denominator = int(arc.turn_denominator)
    doubled = 2 * denominator
    middle = start + end
    level = int(arc.refinement_level) + 1
    left = fractional_circular_arc_disc(
        contour_center,
        contour_radius,
        2 * start,
        middle,
        doubled,
        index=int(first_index),
        refinement_level=level,
        decimal_digits=decimal_digits,
    )
    right = fractional_circular_arc_disc(
        contour_center,
        contour_radius,
        middle,
        2 * end,
        doubled,
        index=int(first_index) + 1,
        refinement_level=level,
        decimal_digits=decimal_digits,
    )
    return left, right


def circular_arc_discs(
    contour_center: complex,
    contour_radius: float,
    count: int,
    *,
    decimal_digits: int = 80,
) -> list[ArcDisc]:
    """Cover a mathematical circle by discs centred at subarc midpoints."""

    total = int(count)
    if total < 8:
        raise ValueError("at least eight subarcs are required")
    radius = float(contour_radius)
    if radius <= 0.0:
        raise ValueError("contour radius must be positive")
    discs: list[ArcDisc] = []
    for index in range(total):
        discs.append(
            fractional_circular_arc_disc(
                contour_center,
                radius,
                index,
                index + 1,
                total,
                index=index,
                decimal_digits=decimal_digits,
            )
        )
    return discs
