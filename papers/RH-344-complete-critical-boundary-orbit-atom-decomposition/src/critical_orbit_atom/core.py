"""RH-344 complete critical boundary-orbit diagnostics.

The paper's conclusions are analytic.  The finite rows produced here reproduce
the exact orbit counts, ledger identities, and scale formulas only; they are
not used as asymptotic evidence.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction


F = Fraction
R_H = F(17, 20)
R_TRACE = F(7, 5)


def physical_constants(precision: int = 100) -> dict[str, Decimal]:
    """Return the archived physical constants at high precision."""

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


def boundary_point(k: int, precision: int = 100) -> Decimal:
    """Solve the RH-17 inverse-word fixed-point equation by bisection."""

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
    """Return the signed primitive orbit of physical length ``2k``."""

    if k < 2:
        raise ValueError("the RH-344 first-alias domain is k>=2")
    with localcontext() as context:
        context.prec = precision
        u = physical_constants(precision)["u_c"]
        point = boundary_point(k, precision)
        orbit: list[Decimal] = []
        for _ in range(2 * k):
            orbit.append(+point)
            point = Decimal(1) - u * point**2
        return tuple(orbit)


def complete_orbit_row(
    k: int,
    precision: int = 100,
    window_A: Decimal | int = Decimal("0.25"),
    phase_eta: int = 0,
) -> dict[str, object]:
    """Reproduce the complete-orbit split on an exact integer phase fixture."""

    if k < 2:
        raise ValueError("the RH-344 first-alias domain is k>=2")
    if window_A <= 0:
        raise ValueError("window_A must be positive")
    if not isinstance(phase_eta, int):
        raise TypeError("phase_eta must be an integer diagnostic phase")

    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        u = constants["u_c"]
        lam = constants["lambda"]
        b = constants["b"]
        beta = constants["beta"]
        orbit = boundary_orbit(k, precision)
        folded = tuple(abs(value) for value in orbit)
        critical_index = 2 * k - 2
        critical_point = folded[critical_index]
        sqrt_sigma = lam ** (phase_eta - k)
        width = Decimal(window_A) * sqrt_sigma

        def in_left(value: Decimal) -> bool:
            return b - width <= value < b

        def in_right(value: Decimal) -> bool:
            return b <= value <= b + width

        left_count = sum(in_left(value) for value in folded)
        right_count = sum(in_right(value) for value in folded)
        far_count = 2 * k - left_count - right_count
        epsilon = int(in_left(critical_point))

        multiplier = Decimal(1)
        for value in orbit:
            multiplier *= -2 * u * value
        absolute_multiplier = abs(multiplier)

        r_h = Decimal(R_H.numerator) / R_H.denominator
        radius = Decimal(R_TRACE.numerator) / R_TRACE.denominator
        hardy = r_h ** (-2 * k)
        point_weight = hardy / (1 + absolute_multiplier)
        far_atom = Decimal(2 * k - 1) * point_weight
        full_atom = Decimal(2 * k) * point_weight
        beta_k_power = hardy / absolute_multiplier
        alias = Decimal(2 * k - 2) * beta_k_power + 2 * beta ** (2 * k)
        target = Decimal(k) * radius ** (-2 * k)
        next_point = Decimal(1) - u * orbit[-1] ** 2

        return {
            "k": k,
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
            "orbit_closure_error": abs(next_point - orbit[0]),
            "multiplier": multiplier,
            "point_weight": point_weight,
            "far_atom": far_atom,
            "full_atom": full_atom,
            "alias_packet": alias,
            "target": target,
            "full_over_far": full_atom / far_atom,
            "full_over_alias": full_atom / alias,
            "sum_over_alias": (alias + full_atom) / alias,
            "point_over_target": point_weight / target,
            "full_over_target": full_atom / target,
            "exact_full_over_far": f"{2 * k}/{2 * k - 1}",
        }


def ledger_fixture(
    *,
    raw_rest: Fraction,
    parity: Fraction,
    alias: Fraction,
    full_atom: Fraction,
    head_defect: Fraction,
) -> dict[str, Fraction]:
    """Return the exact typed critical-order ledger over rational fixtures."""

    q_value = raw_rest + parity - alias - full_atom
    p_value = q_value - head_defect
    compensation_residual = raw_rest + parity - head_defect - alias - full_atom
    return {
        "q": q_value,
        "p": p_value,
        "compensation_residual": compensation_residual,
        "raw_identity_residual": q_value - (raw_rest + parity - alias - full_atom),
        "direct_identity_residual": p_value - (q_value - head_defect),
    }


def decimal_text(value: Decimal) -> str:
    return format(value, "f")
