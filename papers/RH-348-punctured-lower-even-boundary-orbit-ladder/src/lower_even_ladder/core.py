"""RH-348 punctured lower-even boundary-orbit ladder diagnostics.

The asymptotic statements in RH-348 are analytic.  Decimal rows reproduce
the exact finite formulas and are not interval certificates or asymptotic
evidence.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache


F = Fraction
R_H = F(17, 20)
R_TRACE = F(7, 5)
C_M_DIAGNOSTIC = Decimal("1.946342905200968")


def physical_constants(precision: int = 90) -> dict[str, Decimal]:
    if precision < 50:
        raise ValueError("precision must be at least 50 digits")
    with localcontext() as context:
        context.prec = precision
        u = Decimal("1.543689012692076")
        for _ in range(28):
            polynomial = u**3 - 2 * u**2 + 2 * u - 2
            derivative = 3 * u**2 - 4 * u + 2
            u -= polynomial / derivative
        r = u - 1
        lam = 2 * u * r
        r_h = Decimal(R_H.numerator) / R_H.denominator
        radius = Decimal(R_TRACE.numerator) / R_TRACE.denominator
        beta = Decimal(1) / (r_h * lam.sqrt())
        return {
            "u_c": +u,
            "r": +r,
            "lambda": +lam,
            "beta": +beta,
            "x": +(beta * radius) ** 2,
        }


def _h(value: Decimal, u: Decimal) -> Decimal:
    return ((Decimal(1) - ((Decimal(1) - value) / u).sqrt()) / u).sqrt()


def _q(value: Decimal, u: Decimal) -> Decimal:
    return ((Decimal(1) + ((Decimal(1) - value) / u).sqrt()) / u).sqrt()


@lru_cache(maxsize=None)
def _boundary_point(period_parameter: int, precision: int) -> Decimal:
    if period_parameter < 1:
        raise ValueError("period parameter must be positive")
    constants = physical_constants(precision)
    u = constants["u_c"]
    left = Decimal(1) / u.sqrt()
    right = Decimal(1)

    def residual(value: Decimal) -> Decimal:
        image = value
        for _ in range(period_parameter - 1):
            image = _h(image, u)
        return _q(image, u) - value

    for _ in range(4 * precision):
        middle = (left + right) / 2
        if residual(middle) > 0:
            left = middle
        else:
            right = middle
    return +((left + right) / 2)


@lru_cache(maxsize=None)
def boundary_multiplier(period_parameter: int, precision: int = 90) -> Decimal:
    """Return the absolute multiplier of the period-2m boundary orbit."""

    if period_parameter < 1:
        raise ValueError("period parameter must be positive")
    with localcontext() as context:
        context.prec = precision
        u = physical_constants(precision)["u_c"]
        point = _boundary_point(period_parameter, precision)
        multiplier = Decimal(1)
        for _ in range(2 * period_parameter):
            multiplier *= -2 * u * point
            point = Decimal(1) - u * point**2
        return +abs(multiplier)


def lower_even_entry(
    k: int,
    m: int,
    precision: int = 90,
) -> dict[str, Decimal | int]:
    """Return one exact punctured lower-even ledger row."""

    if k < 5:
        raise ValueError("k must be at least 5")
    if not (2 <= m <= k - 2):
        raise ValueError("the punctured lower-even domain is 2<=m<=k-2")
    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        beta = constants["beta"]
        r_h = Decimal(R_H.numerator) / R_H.denominator
        radius = Decimal(R_TRACE.numerator) / R_TRACE.denominator
        multiplier_m = boundary_multiplier(m, precision)
        multiplier_k = boundary_multiplier(k, precision)
        point_weight = r_h ** (-2 * m) / (Decimal(1) + multiplier_m)
        full_atom = Decimal(2 * m) * point_weight
        beta_k = (-multiplier_k.ln() / Decimal(2 * k)).exp() / r_h
        radial = Decimal(2) * (beta ** (2 * m) - beta_k ** (2 * m))
        demand = full_atom + radial
        prefix_weight = radius ** (2 * m) / Decimal(2 * m)
        orbit_weighted = full_atom * prefix_weight
        radial_weighted = radial * prefix_weight
        demand_weighted = demand * prefix_weight
        return {
            "k": k,
            "m": m,
            "order": 2 * m,
            "multiplier_m": multiplier_m,
            "multiplier_k": multiplier_k,
            "point_weight": point_weight,
            "full_atom": full_atom,
            "radial": radial,
            "demand": demand,
            "prefix_weight": prefix_weight,
            "orbit_weighted": orbit_weighted,
            "orbit_weighted_identity": point_weight * radius ** (2 * m),
            "radial_weighted": radial_weighted,
            "demand_weighted": demand_weighted,
            "absolute_demand_weighted": abs(demand_weighted),
            "radial_over_full": radial / full_atom,
        }


def ladder_row(
    k: int,
    m_start: int = 2,
    precision: int = 90,
) -> dict[str, Decimal | int | list[dict[str, Decimal | int]]]:
    """Build the complete lower-even punctured ladder through m=k-2."""

    if k < m_start + 2:
        raise ValueError("the ladder must contain at least one order")
    if m_start < 2:
        raise ValueError("m_start must be at least 2")
    with localcontext() as context:
        context.prec = precision
        entries = [
            lower_even_entry(k, m, precision)
            for m in range(m_start, k - 1)
        ]
        constants = physical_constants(precision)
        x = constants["x"]
        orbit = sum(
            (entry["orbit_weighted"] for entry in entries), Decimal(0)
        )
        radial = sum(
            (entry["radial_weighted"] for entry in entries), Decimal(0)
        )
        radial_abs = sum(
            (abs(entry["radial_weighted"]) for entry in entries), Decimal(0)
        )
        demand = sum(
            (entry["demand_weighted"] for entry in entries), Decimal(0)
        )
        demand_abs = sum(
            (entry["absolute_demand_weighted"] for entry in entries),
            Decimal(0),
        )
        asymptotic = x ** (k - 1) / (C_M_DIAGNOSTIC * (x - 1))
        exact_geometric = sum(
            (x**m / C_M_DIAGNOSTIC for m in range(m_start, k - 1)),
            Decimal(0),
        )
        identity_error = max(
            abs(entry["orbit_weighted"] - entry["orbit_weighted_identity"])
            for entry in entries
        )
        return {
            "k": k,
            "m_start": m_start,
            "m_end": k - 2,
            "order_count": len(entries),
            "entries": entries,
            "x": x,
            "orbit_weighted_sum": orbit,
            "radial_weighted_sum": radial,
            "absolute_radial_weighted_sum": radial_abs,
            "combined_demand_weighted_sum": demand,
            "absolute_combined_demand_weighted_sum": demand_abs,
            "asymptotic_orbit_reference": asymptotic,
            "exact_geometric_reference": exact_geometric,
            "orbit_over_asymptotic": orbit / asymptotic,
            "orbit_over_exact_geometric": orbit / exact_geometric,
            "absolute_radial_over_orbit": radial_abs / orbit,
            "combined_over_orbit": demand / orbit,
            "absolute_combined_over_orbit": demand_abs / orbit,
            "max_orbit_identity_error": identity_error,
        }


def typed_compensation_fixture(
    demands: tuple[Fraction, ...],
    supplies: tuple[Fraction, ...],
) -> dict[str, Fraction | int]:
    """Check the finite-dimensional weighted reverse-triangle ledger."""

    if not demands or len(demands) != len(supplies):
        raise ValueError("demand and supply vectors must have equal nonzero length")
    residuals = tuple(supply - demand for supply, demand in zip(supplies, demands))
    demand_mass = sum((abs(value) for value in demands), F(0))
    supply_mass = sum((abs(value) for value in supplies), F(0))
    residual_mass = sum((abs(value) for value in residuals), F(0))
    return {
        "dimension": len(demands),
        "demand_mass": demand_mass,
        "supply_mass": supply_mass,
        "residual_mass": residual_mass,
        "reverse_triangle_slack": supply_mass + residual_mass - demand_mass,
    }


def decimal_text(value: Decimal) -> str:
    return format(value, "f")
