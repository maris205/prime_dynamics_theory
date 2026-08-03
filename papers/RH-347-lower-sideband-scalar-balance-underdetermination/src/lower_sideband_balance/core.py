"""RH-347 lower-sideband scalar balance diagnostics.

The analytic results are symbolic.  Decimal constants and finite rows only
reproduce the exact scalar formulas and target-scale separation.
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


def _multiplier(period_parameter: int, precision: int) -> Decimal:
    with localcontext() as context:
        context.prec = precision
        u = physical_constants(precision)["u_c"]
        point = _boundary_point(period_parameter, precision)
        value = Decimal(1)
        for _ in range(2 * period_parameter):
            value *= -2 * u * point
            point = Decimal(1) - u * point**2
        return +value


def balance_phase(precision: int = 100) -> Decimal:
    """Diagnostic solution of C_* C_M lambda^(eta-1) = 1."""

    with localcontext() as context:
        context.prec = precision
        lam = physical_constants(precision)["lambda"]
        return +(
            Decimal(1)
            - (C_STAR_DIAGNOSTIC * C_M_DIAGNOSTIC).ln() / lam.ln()
        )


def _parity_delta(packet: Decimal, m: int, r_h: Decimal) -> Decimal:
    scaled = packet * r_h ** (2 * m)
    if not (Decimal(0) < scaled < Decimal(1)):
        raise ValueError("desired parity packet must lie in (0,r_H^(-2m))")
    root = ((Decimal(1) - scaled).ln() / Decimal(2 * m)).exp()
    return Decimal(1) - root


def completion_row(
    m: int,
    precision: int = 100,
) -> dict[str, Decimal | int]:
    """Reproduce the two balance-phase lower scalar completions."""

    if m < 2:
        raise ValueError("the RH-347 lower-sideband diagnostic domain is m>=2")
    with localcontext() as context:
        context.prec = precision
        k = m + 1
        constants = physical_constants(precision)
        lam = constants["lambda"]
        beta = constants["beta"]
        r_h = Decimal(R_H.numerator) / R_H.denominator
        radius = Decimal(R_TRACE.numerator) / R_TRACE.denominator

        multiplier_m = abs(_multiplier(m, precision))
        multiplier_k = abs(_multiplier(k, precision))
        hardy_m = r_h ** (-2 * m)
        point_weight = hardy_m / (Decimal(1) + multiplier_m)
        full_atom = Decimal(2 * m) * point_weight
        beta_k = (-multiplier_k.ln() / Decimal(2 * k)).exp() / r_h
        radial_sideband = 2 * (beta ** (2 * m) - beta_k ** (2 * m))
        demand = full_atom + radial_sideband
        target = Decimal(m) * radius ** (-2 * m)

        eta_minus = balance_phase(precision)
        sqrt_sigma = ((eta_minus - Decimal(k)) * lam.ln()).exp()
        expected_delta = C_STAR_DIAGNOSTIC * sqrt_sigma

        close_packet = demand
        far_packet = demand + full_atom / Decimal(m)
        close_delta = _parity_delta(close_packet, m, r_h)
        far_delta = _parity_delta(far_packet, m, r_h)

        def recovered(delta: Decimal) -> Decimal:
            return hardy_m * (
                Decimal(1) - (Decimal(1) - delta) ** (2 * m)
            )

        far_residual = full_atom / Decimal(m)
        weighted_far = far_residual / (Decimal(2) * target)
        point_over_target = point_weight / target
        return {
            "m": m,
            "k": k,
            "sideband_order": 2 * m,
            "root_exponent_denominator": 2 * m,
            "eta_minus": eta_minus,
            "phase_ratio": C_STAR_DIAGNOSTIC
            * C_M_DIAGNOSTIC
            * ((eta_minus - Decimal(1)) * lam.ln()).exp(),
            "multiplier_m": multiplier_m,
            "multiplier_k": multiplier_k,
            "point_weight": point_weight,
            "full_atom": full_atom,
            "radial_sideband": radial_sideband,
            "demand": demand,
            "target": target,
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
            "two_point_weights": Decimal(2) * point_weight,
            "far_weighted_lower": weighted_far,
            "point_over_target": point_over_target,
            "far_weighted_identity_error": abs(
                weighted_far - point_over_target
            ),
            "scaled_close_packet": close_packet * r_h ** (2 * m),
            "scaled_far_packet": far_packet * r_h ** (2 * m),
            "full_over_target": full_atom / target,
            "demand_over_full": demand / full_atom,
        }


def decimal_text(value: Decimal) -> str:
    return format(value, "f")
