"""RH-339 first-lower-sideband physical orbit-atom diagnostics."""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction


F = Fraction
R_H = F(17, 20)
R_TRACE = F(7, 5)


def sideband_order(k: int) -> int:
    if k < 3:
        raise ValueError("the diagnostic sideband domain is k>=3")
    return 2 * k - 2


def sideband_component_index(k: int) -> int:
    return sideband_order(k) // 2


def sideband_in_one_alias_cut(k: int, cut: int) -> bool:
    if not (2 * k < cut <= 4 * k):
        raise ValueError("the one-alias cut must satisfy 2k<h<=4k")
    order = sideband_order(k)
    return 2 <= order < cut and order != 2 * k


def physical_constants(precision: int = 100) -> dict[str, Decimal]:
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
        beta = Decimal(1) / (
            (Decimal(R_H.numerator) / R_H.denominator) * lam.sqrt()
        )
        return {"u_c": +u, "r": +r, "lambda": +lam, "b": +b, "beta": +beta}


def _h(value: Decimal, u: Decimal) -> Decimal:
    return ((Decimal(1) - ((Decimal(1) - value) / u).sqrt()) / u).sqrt()


def _q(value: Decimal, u: Decimal) -> Decimal:
    return ((Decimal(1) + ((Decimal(1) - value) / u).sqrt()) / u).sqrt()


def boundary_point(component_index: int, precision: int = 100) -> Decimal:
    if component_index < 1:
        raise ValueError("component_index must be positive")
    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        u = constants["u_c"]
        left = constants["b"]
        right = Decimal(1)

        def residual(value: Decimal) -> Decimal:
            image = value
            for _ in range(component_index - 1):
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


def boundary_orbit(component_index: int, precision: int = 100) -> tuple[Decimal, ...]:
    with localcontext() as context:
        context.prec = precision
        u = physical_constants(precision)["u_c"]
        point = boundary_point(component_index, precision)
        orbit: list[Decimal] = []
        for _ in range(2 * component_index):
            orbit.append(+point)
            point = Decimal(1) - u * point**2
        return tuple(orbit)


def sideband_diagnostic(
    k: int,
    precision: int = 100,
    window_A: Decimal | int = Decimal("0.25"),
) -> dict[str, object]:
    """Reproduce the period-2(k-1) orbit atom inside the k-clock far set."""

    if window_A <= 0:
        raise ValueError("window_A must be positive")
    m = sideband_component_index(k)
    n = 2 * m
    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        u = constants["u_c"]
        lam = constants["lambda"]
        b = constants["b"]
        beta = constants["beta"]
        orbit = boundary_orbit(m, precision)
        folded = tuple(abs(value) for value in orbit)
        excluded_index = n - 2
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
        hardy = r_h ** (-n)
        atom_mass = hardy * Decimal(n - 1) / (1 + absolute_multiplier)
        target = Decimal(m) * radius ** (-2 * m)
        weighted_absolute_atom = atom_mass * radius**n / Decimal(n)
        return {
            "k": k,
            "component_index": m,
            "sideband_order": n,
            "excluded_index": excluded_index,
            "certified_subset_count": len(omega),
            "certified_subset_far_count": sum(in_far(value) for value in omega),
            "orbit_closure_error": abs((Decimal(1) - u * orbit[-1] ** 2) - orbit[0]),
            "window_half_width_on_k_clock": width,
            "multiplier": multiplier,
            "atom_mass": atom_mass,
            "sideband_target": target,
            "atom_over_sideband_target": atom_mass / target,
            "absolute_weighted_atom": weighted_absolute_atom,
            "weighted_identity_error": abs(weighted_absolute_atom - atom_mass / (2 * target)),
            "beta_R_power": (beta * radius) ** (2 * m),
        }


def decimal_text(value: Decimal) -> str:
    return format(value, "f")
