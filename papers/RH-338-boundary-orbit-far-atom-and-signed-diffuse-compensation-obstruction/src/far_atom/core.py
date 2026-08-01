"""RH-338 physical boundary-orbit far-atom diagnostics.

The theorem is analytic and sourced from RH-17, RH-326, RH-334, and RH-336.
Decimal orbit rows below only reproduce its geometry and scales.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction


F = Fraction
R_H = F(17, 20)
R_TRACE = F(7, 5)


def physical_constants(precision: int = 100) -> dict[str, Decimal]:
    """Return high-precision physical constants for diagnostics."""

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
        b = Decimal(1) / u.sqrt()
        beta = Decimal(1) / (Decimal(R_H.numerator) / R_H.denominator * lam.sqrt())
        return {
            "u_c": +u,
            "r": +r,
            "lambda": +lam,
            "b": +b,
            "beta": +beta,
        }


def _h(value: Decimal, u: Decimal) -> Decimal:
    return ((Decimal(1) - ((Decimal(1) - value) / u).sqrt()) / u).sqrt()


def _q(value: Decimal, u: Decimal) -> Decimal:
    return ((Decimal(1) + ((Decimal(1) - value) / u).sqrt()) / u).sqrt()


def boundary_point(k: int, precision: int = 100) -> Decimal:
    """Solve the RH-17 inverse-word fixed point by Decimal bisection."""

    if k < 1:
        raise ValueError("k must be positive")
    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        u = constants["u_c"]
        left = constants["b"]
        right = Decimal(1)

        def residual(value: Decimal) -> Decimal:
            image = value
            for _ in range(k - 1):
                image = _h(image, u)
            return _q(image, u) - value

        if residual(left) <= 0 or residual(right) >= 0:
            raise ArithmeticError("boundary-point bracket failed")
        for _ in range(4 * precision):
            middle = (left + right) / 2
            if residual(middle) > 0:
                left = middle
            else:
                right = middle
        return +((left + right) / 2)


def boundary_orbit(k: int, precision: int = 100) -> tuple[Decimal, ...]:
    """Return the signed primitive length-2k boundary orbit diagnostically."""

    if k < 2:
        raise ValueError("the first-alias audit domain is k>=2")
    with localcontext() as context:
        context.prec = precision
        u = physical_constants(precision)["u_c"]
        point = boundary_point(k, precision)
        orbit: list[Decimal] = []
        for _ in range(2 * k):
            orbit.append(+point)
            point = Decimal(1) - u * point**2
        return tuple(orbit)


def certified_far_count(k: int) -> int:
    """The analytic RH-338 subset deletes exactly one of 2k marked points."""

    if k < 2:
        raise ValueError("the first-alias audit domain is k>=2")
    return 2 * k - 1


def diagnostic_row(
    k: int,
    precision: int = 100,
    window_A: Decimal | int = Decimal("0.25"),
) -> dict[str, object]:
    """Reproduce the far count and orbit/alias scales for one finite k."""

    if window_A <= 0:
        raise ValueError("window_A must be positive")
    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        u = constants["u_c"]
        lam = constants["lambda"]
        b = constants["b"]
        beta = constants["beta"]
        orbit = boundary_orbit(k, precision)
        folded = tuple(abs(value) for value in orbit)
        excluded_index = 2 * k - 2
        omega = tuple(value for index, value in enumerate(folded) if index != excluded_index)
        width = Decimal(window_A) * lam ** (-k)

        def in_far(value: Decimal) -> bool:
            return value < b - width or value > b + width

        multiplier = Decimal(1)
        for value in orbit:
            multiplier *= -2 * u * value
        absolute_multiplier = abs(multiplier)

        r_h = Decimal(R_H.numerator) / R_H.denominator
        radius = Decimal(R_TRACE.numerator) / R_TRACE.denominator
        hardy = r_h ** (-2 * k)
        atom_mass = hardy * Decimal(2 * k - 1) / (1 + absolute_multiplier)
        beta_k_power = hardy / absolute_multiplier
        alias = Decimal(2 * k - 2) * beta_k_power + 2 * beta ** (2 * k)
        target = Decimal(k) * radius ** (-2 * k)

        return {
            "k": k,
            "excluded_index": excluded_index,
            "certified_subset_count": len(omega),
            "certified_subset_far_count": sum(in_far(value) for value in omega),
            "whole_orbit_far_count": sum(in_far(value) for value in folded),
            "orbit_closure_error": abs(
                (Decimal(1) - u * orbit[-1] ** 2) - orbit[0]
            ),
            "multiplier": multiplier,
            "window_half_width": width,
            "atom_mass": atom_mass,
            "alias_packet": alias,
            "target": target,
            "atom_over_alias": atom_mass / alias,
            "atom_over_target": atom_mass / target,
        }


def fixed_gap_diagnostics(precision: int = 100) -> dict[str, Decimal]:
    """Return the three positive gaps used by the analytic containment proof."""

    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        u = constants["u_c"]
        b = constants["b"]
        r = constants["r"]
        p_one = boundary_point(1, precision)
        return {
            "p_1_minus_b": +(p_one - b),
            "b_minus_h_of_b": +(b - _h(b, u)),
            "b_minus_r": +(b - r),
        }


def decimal_text(value: Decimal) -> str:
    return format(value, "f")
