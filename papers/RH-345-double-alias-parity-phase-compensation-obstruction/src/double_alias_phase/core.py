"""RH-345 double-alias parity-phase diagnostics.

The analytic theorem is symbolic.  Archived decimal constants and finite
rows below only reproduce the scalar identities and scale separation.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction


F = Fraction
R_H = F(17, 20)
R_TRACE = F(7, 5)
C_STAR_DIAGNOSTIC = Decimal("0.105258535936908")
C_M_DIAGNOSTIC = Decimal("1.946342905200968")


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


def _boundary_point(k: int, precision: int) -> Decimal:
    constants = physical_constants(precision)
    u = constants["u_c"]
    left = constants["b"]
    right = Decimal(1)

    def residual(value: Decimal) -> Decimal:
        image = value
        for _ in range(k - 1):
            image = _h(image, u)
        return _q(image, u) - value

    for _ in range(4 * precision):
        middle = (left + right) / 2
        if residual(middle) > 0:
            left = middle
        else:
            right = middle
    return +((left + right) / 2)


def _multiplier(k: int, precision: int) -> Decimal:
    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        u = constants["u_c"]
        point = _boundary_point(k, precision)
        multiplier = Decimal(1)
        for _ in range(2 * k):
            multiplier *= -2 * u * point
            point = Decimal(1) - u * point**2
        return +multiplier


def balance_phase(precision: int = 100) -> Decimal:
    """Return the diagnostic solution of C_* C_M lambda^eta = 2."""

    with localcontext() as context:
        context.prec = precision
        lam = physical_constants(precision)["lambda"]
        return +(
            (Decimal(2) / (C_STAR_DIAGNOSTIC * C_M_DIAGNOSTIC)).ln()
            / lam.ln()
        )


def _parity_delta(packet: Decimal, k: int, r_h: Decimal) -> Decimal:
    scaled = packet * r_h ** (2 * k)
    if not (Decimal(0) < scaled < Decimal(1)):
        raise ValueError("desired parity packet must lie in (0,r_H^(-2k))")
    root = ((Decimal(1) - scaled).ln() / Decimal(2 * k)).exp()
    return Decimal(1) - root


def completion_row(k: int, precision: int = 100) -> dict[str, Decimal | int]:
    """Reproduce the two balance-phase scalar parity completions."""

    if k < 2:
        raise ValueError("the RH-345 first-alias domain is k>=2")
    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        lam = constants["lambda"]
        beta = constants["beta"]
        r_h = Decimal(R_H.numerator) / R_H.denominator
        radius = Decimal(R_TRACE.numerator) / R_TRACE.denominator
        multiplier = abs(_multiplier(k, precision))
        hardy = r_h ** (-2 * k)
        beta_k_power = hardy / multiplier
        alias = Decimal(2 * k - 2) * beta_k_power + 2 * beta ** (2 * k)
        full_atom = Decimal(2 * k) * hardy / (Decimal(1) + multiplier)
        demand = alias + full_atom
        target = Decimal(k) * radius ** (-2 * k)

        eta_two = balance_phase(precision)
        sqrt_sigma = (eta_two * lam.ln()).exp() * lam ** (-k)
        expected_delta = C_STAR_DIAGNOSTIC * sqrt_sigma

        close_packet = demand
        far_packet = demand + alias / Decimal(k)
        close_delta = _parity_delta(close_packet, k, r_h)
        far_delta = _parity_delta(far_packet, k, r_h)

        def recovered(delta: Decimal) -> Decimal:
            return hardy * (Decimal(1) - (Decimal(1) - delta) ** (2 * k))

        far_residual = alias / Decimal(k)
        return {
            "k": k,
            "eta_two": eta_two,
            "phase_ratio": C_STAR_DIAGNOSTIC
            * C_M_DIAGNOSTIC
            * (eta_two * lam.ln()).exp(),
            "alias": alias,
            "full_atom": full_atom,
            "demand": demand,
            "target": target,
            "demand_over_alias": demand / alias,
            "close_packet": close_packet,
            "far_packet": far_packet,
            "close_delta": close_delta,
            "far_delta": far_delta,
            "expected_delta": expected_delta,
            "close_delta_ratio": close_delta / expected_delta,
            "far_delta_ratio": far_delta / expected_delta,
            "close_recovery_error": abs(recovered(close_delta) - close_packet),
            "far_recovery_error": abs(recovered(far_delta) - far_packet),
            "close_direct_residual": Decimal(0),
            "far_direct_residual": far_residual,
            "far_weighted_critical": far_residual / (Decimal(2) * target),
            "scaled_close_packet": close_packet * r_h ** (2 * k),
            "scaled_far_packet": far_packet * r_h ** (2 * k),
        }


def decimal_text(value: Decimal) -> str:
    return format(value, "f")
