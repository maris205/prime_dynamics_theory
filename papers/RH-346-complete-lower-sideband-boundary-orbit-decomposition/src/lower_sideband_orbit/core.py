"""RH-346 complete lower-sideband orbit diagnostics."""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction


F = Fraction
R_H = F(17, 20)
R_TRACE = F(7, 5)
C_STAR_DIAGNOSTIC = Decimal("0.105258535936908")


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
        r_h = Decimal(R_H.numerator) / R_H.denominator
        beta = Decimal(1) / (r_h * lam.sqrt())
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


def _boundary_point(period_parameter: int, precision: int) -> Decimal:
    if period_parameter < 1:
        raise ValueError("period parameter must be positive")
    constants = physical_constants(precision)
    u = constants["u_c"]
    left = constants["b"]
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


def _orbit(period_parameter: int, precision: int) -> tuple[Decimal, ...]:
    with localcontext() as context:
        context.prec = precision
        u = physical_constants(precision)["u_c"]
        point = _boundary_point(period_parameter, precision)
        orbit = []
        for _ in range(2 * period_parameter):
            orbit.append(+point)
            point = Decimal(1) - u * point**2
        return tuple(orbit)


def _multiplier(period_parameter: int, precision: int) -> Decimal:
    with localcontext() as context:
        context.prec = precision
        u = physical_constants(precision)["u_c"]
        orbit = _orbit(period_parameter, precision)
        value = Decimal(1)
        for point in orbit:
            value *= -2 * u * point
        return +value


def sideband_row(
    k: int,
    precision: int = 100,
    window_A: Decimal | int = Decimal("0.25"),
    phase_eta: int = 0,
) -> dict[str, object]:
    """Reproduce the complete period-2(k-1) sideband decomposition."""

    if k < 3:
        raise ValueError("the complete lower-sideband diagnostic domain is k>=3")
    if window_A <= 0:
        raise ValueError("window_A must be positive")
    if not isinstance(phase_eta, int):
        raise TypeError("phase_eta must be an integer diagnostic phase")

    with localcontext() as context:
        context.prec = precision
        m = k - 1
        constants = physical_constants(precision)
        lam = constants["lambda"]
        beta = constants["beta"]
        b = constants["b"]
        u = constants["u_c"]
        r_h = Decimal(R_H.numerator) / R_H.denominator
        radius = Decimal(R_TRACE.numerator) / R_TRACE.denominator

        orbit_m = _orbit(m, precision)
        folded = tuple(abs(value) for value in orbit_m)
        critical_index = 2 * m - 2
        critical_point = folded[critical_index]
        sqrt_sigma = lam ** (phase_eta - k)
        width = Decimal(window_A) * sqrt_sigma

        def in_left(value: Decimal) -> bool:
            return b - width <= value < b

        def in_right(value: Decimal) -> bool:
            return b <= value <= b + width

        left_count = sum(in_left(value) for value in folded)
        right_count = sum(in_right(value) for value in folded)
        far_count = 2 * m - left_count - right_count
        epsilon = int(in_left(critical_point))

        multiplier_m = abs(_multiplier(m, precision))
        multiplier_k = abs(_multiplier(k, precision))
        hardy_m = r_h ** (-2 * m)
        point_weight = hardy_m / (Decimal(1) + multiplier_m)
        partial_atom = Decimal(2 * m - 1) * point_weight
        full_atom = Decimal(2 * m) * point_weight
        beta_k = (-multiplier_k.ln() / Decimal(2 * k)).exp() / r_h
        radial_sideband = 2 * (beta ** (2 * m) - beta_k ** (2 * m))
        combined_demand = full_atom + radial_sideband
        target = Decimal(m) * radius ** (-2 * m)
        next_point = Decimal(1) - u * orbit_m[-1] ** 2

        parity_leading = (
            Decimal(2 * m)
            * C_STAR_DIAGNOSTIC
            * sqrt_sigma
            * hardy_m
        )
        return {
            "k": k,
            "m": m,
            "sideband_order": 2 * m,
            "phase_eta": phase_eta,
            "critical_index": critical_index,
            "complete_count": len(folded),
            "distinct_folded_count": len(set(folded)),
            "left_count": left_count,
            "right_count": right_count,
            "far_count": far_count,
            "epsilon": epsilon,
            "cell_count_identity": left_count + right_count + far_count,
            "critical_q_b": (b - critical_point) / sqrt_sigma,
            "window_A": Decimal(window_A),
            "orbit_closure_error": abs(next_point - orbit_m[0]),
            "multiplier_m": multiplier_m,
            "multiplier_k": multiplier_k,
            "point_weight": point_weight,
            "partial_atom": partial_atom,
            "full_atom": full_atom,
            "radial_sideband": radial_sideband,
            "combined_demand": combined_demand,
            "target": target,
            "full_over_partial": full_atom / partial_atom,
            "point_over_target": point_weight / target,
            "full_over_target": full_atom / target,
            "radial_over_full": radial_sideband / full_atom,
            "combined_over_full": combined_demand / full_atom,
            "parity_leading_over_full": parity_leading / full_atom,
            "exact_full_over_partial": f"{2 * m}/{2 * m - 1}",
        }


def typed_ledger_fixture(
    *,
    raw_rest: Fraction,
    parity: Fraction,
    radial_sideband: Fraction,
    full_atom: Fraction,
    head_defect: Fraction,
) -> dict[str, Fraction]:
    q_value = raw_rest + parity - radial_sideband - full_atom
    p_value = q_value - head_defect
    return {
        "q": q_value,
        "p": p_value,
        "raw_residual": q_value
        - (raw_rest + parity - radial_sideband - full_atom),
        "direct_residual": p_value - (q_value - head_defect),
        "compensation_residual": raw_rest
        + parity
        - head_defect
        - radial_sideband
        - full_atom,
    }


def decimal_text(value: Decimal) -> str:
    return format(value, "f")
