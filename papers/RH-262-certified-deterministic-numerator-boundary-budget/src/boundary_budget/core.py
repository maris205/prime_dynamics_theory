"""Arb bounds for the Hardy-scaled deterministic numerator logarithm."""

from __future__ import annotations

from dataclasses import dataclass

from flint import arb


@dataclass(frozen=True)
class BoundaryBudget:
    """Certified scalar bounds on one fixed Hardy-scaled circle."""

    scaled_circle: arb
    numerator_circle: arb
    squared_circle: arb
    radius_ratio: arb
    nuclear_norm: arb
    operator_norm: arb
    operator_square_norm: arb
    cube_contraction: arb
    cube_geometric_ratio: arb
    fredholm_log: arb
    astar_log: arb
    bfactor_log: arb
    linear_c_log: arb
    total_log: arb


def _up(value: arb) -> arb:
    return value.upper()


def certify_boundary_budget(
    reduced_bounds: object,
    *,
    scaled_circle: arb | None = None,
    hardy_radius: arb | None = None,
) -> BoundaryBudget:
    """Convert the RH-13 reduced-sector certificate into a log budget.

    ``reduced_bounds`` is the ``CertifiedBounds`` object returned by
    RH-13's ``certify_reduced_gap``.  The calculation is kept here as a
    scalar interface so every inequality can be tested independently.
    """

    one = arb(1)
    circle = arb(7) / 5 if scaled_circle is None else arb(scaled_circle)
    hardy = arb(17) / 20 if hardy_radius is None else arb(hardy_radius)
    if not (circle > 0 and hardy > 0):
        raise ValueError("the circle and Hardy radius must be positive")

    numerator_circle = _up(circle / hardy)
    lam = reduced_bounds.lam
    if not numerator_circle < lam:
        raise ValueError("the numerator circle must lie inside |u|<lambda")
    squared_circle = _up(numerator_circle**2)
    radius_ratio = _up(numerator_circle / lam)

    weight_norm = reduced_bounds.beta_one_weight_norm
    tau = reduced_bounds.tau
    disk_radius = reduced_bounds.disk_radius
    fixed_point_radius = reduced_bounds.r
    nuclear_norm = _up(
        2
        * weight_norm
        * (
            tau / (one - tau)
            + one / (one - (fixed_point_radius / disk_radius) ** 2).sqrt()
            - one
        )
    )

    epsilon = reduced_bounds.beta_one_truncation_error
    matrix_norm = reduced_bounds.beta_one_matrix_norm
    matrix_square_norm = reduced_bounds.beta_one_matrix_square_norm
    operator_norm = _up(matrix_norm + epsilon)
    operator_square_norm = _up(
        matrix_square_norm + 2 * matrix_norm * epsilon + epsilon**2
    )
    cube_contraction = _up(reduced_bounds.beta_one_cube_bound)
    cube_geometric_ratio = _up(cube_contraction * squared_circle**3)
    if not cube_geometric_ratio < one:
        raise RuntimeError("the grouped Fredholm series is not contractive")

    nuclear_square = _up(operator_norm * nuclear_norm)
    nuclear_cube = _up(operator_square_norm * nuclear_norm)
    fredholm_log = _up(
        (
            nuclear_norm * squared_circle
            + nuclear_square * squared_circle**2 / 2
            + nuclear_cube * squared_circle**3 / 3
        )
        / (one - cube_geometric_ratio)
    )
    astar_log = _up(-arb.log(one - radius_ratio**2))
    bfactor_log = _up(
        -arb.log(one - radius_ratio**2)
        / (2 * (one - lam ** -2))
    )
    linear_c_log = _up(arb.atanh(radius_ratio) - radius_ratio)
    total_log = _up(fredholm_log + astar_log + bfactor_log + linear_c_log)

    return BoundaryBudget(
        scaled_circle=circle,
        numerator_circle=numerator_circle,
        squared_circle=squared_circle,
        radius_ratio=radius_ratio,
        nuclear_norm=nuclear_norm,
        operator_norm=operator_norm,
        operator_square_norm=operator_square_norm,
        cube_contraction=cube_contraction,
        cube_geometric_ratio=cube_geometric_ratio,
        fredholm_log=fredholm_log,
        astar_log=astar_log,
        bfactor_log=bfactor_log,
        linear_c_log=linear_c_log,
        total_log=total_log,
    )


def cauchy_tail_factor(
    *,
    inner_radius: arb,
    outer_radius: arb,
    first_omitted_order: int,
) -> arb:
    """Return an outward Arb bound for the geometric Cauchy factor."""

    inner = arb(inner_radius)
    outer = arb(outer_radius)
    order = int(first_omitted_order)
    if not (inner >= 0 and outer > inner and order >= 1):
        raise ValueError("require 0 <= inner < outer and positive order")
    ratio = inner / outer
    return _up(ratio**order / (1 - ratio))


def certified_tail_budget(
    *,
    boundary_supremum: arb,
    inner_radius: arb,
    outer_radius: arb,
    first_omitted_order: int,
) -> tuple[arb, arb, arb]:
    """Return factor, additive log tail, and multiplicative error."""

    supremum = arb(boundary_supremum)
    if not supremum >= 0:
        raise ValueError("the boundary supremum must be nonnegative")
    factor = cauchy_tail_factor(
        inner_radius=inner_radius,
        outer_radius=outer_radius,
        first_omitted_order=first_omitted_order,
    )
    additive = _up(supremum * factor)
    multiplicative = _up(arb.exp(additive) - 1)
    return factor, additive, multiplicative
