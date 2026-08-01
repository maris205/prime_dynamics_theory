"""Exact RH-337 clock and frozen-comparator certificates.

The rational constants below reproduce the RH-329 graded comparator.  They
are model definitions, not interval enclosures for the physical constants.
The physical expansion rate remains the positive algebraic root of
``x^3 + 4 x^2 - 16``.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction


F = Fraction

R_H = F(17, 20)
R_TRACE = F(7, 5)
LAMBDA_HAT = F(2098216888035403, 1250000000000000)
C_M_HAT = F(9731714526004839, 5000000000000000)
C_STAR_HAT = F(26314633984227, 250000000000000)


def lambda_polynomial(value: Fraction) -> Fraction:
    """Evaluate ``x^3+4x^2-16`` exactly."""

    return value**3 + 4 * value**2 - 16


def exact_clock_certificate() -> dict[str, object]:
    """Return the exact certificate that ``LAMBDA_HAT > lambda``."""

    residual = lambda_polynomial(LAMBDA_HAT)
    radius_ratio_squared = (R_TRACE / R_H) ** 2
    return {
        "physical_polynomial": "lambda^3+4*lambda^2-16=0",
        "positive_axis_derivative": "3*lambda^2+8*lambda>0",
        "physical_root_bracket": (F(1), F(2)),
        "polynomial_at_one": lambda_polynomial(F(1)),
        "polynomial_at_two": lambda_polynomial(F(2)),
        "Lambda_hat": LAMBDA_HAT,
        "polynomial_at_Lambda_hat": residual,
        "Lambda_hat_greater_than_lambda": residual > 0,
        "R_over_r_H_squared": radius_ratio_squared,
        "R_over_r_H_squared_greater_than_two": radius_ratio_squared > 2,
        "beta_R_greater_than_one_from_lambda_less_than_two": (
            radius_ratio_squared > 2
        ),
    }


def model_beta_squared() -> Fraction:
    """Return the exact RH-329 model value ``beta_hat^2``."""

    return F(1) / (R_H**2 * LAMBDA_HAT)


def model_alias_packet(k: int) -> Fraction:
    """Return the exact RH-329 hatted alias packet."""

    if k < 2:
        raise ValueError("the RH-329 audit domain is k>=2")
    coefficient = F(2 * k - 2, 1) / C_M_HAT + 2
    return coefficient * model_beta_squared() ** k


def model_parity_packet(k: int) -> Fraction:
    """Return the exact RH-329 hatted parity packet."""

    if k < 2:
        raise ValueError("the RH-329 audit domain is k>=2")
    delta = C_STAR_HAT * LAMBDA_HAT ** (-k)
    return R_H ** (-2 * k) * (1 - (1 - delta) ** (2 * k))


def model_packet_scale(k: int) -> Fraction:
    """Return ``k r_H^(-2k) Lambda_hat^(-k)``."""

    if k < 2:
        raise ValueError("the RH-329 audit domain is k>=2")
    return k * R_H ** (-2 * k) * LAMBDA_HAT ** (-k)


def parity_binomial_bounds(k: int) -> tuple[Fraction, Fraction]:
    """Return exact second-order lower and first-order upper parity bounds."""

    if k < 2:
        raise ValueError("the RH-329 audit domain is k>=2")
    x = C_STAR_HAT * LAMBDA_HAT ** (-k)
    n = 2 * k
    lower = R_H ** (-2 * k) * (n * x - F(n * (n - 1), 2) * x**2)
    upper = R_H ** (-2 * k) * n * x
    return lower, upper


def model_packet_audit(k: int) -> dict[str, Fraction | int]:
    """Return exact finite reproductions of the hatted packet scales."""

    parity = model_parity_packet(k)
    alias = model_alias_packet(k)
    scale = model_packet_scale(k)
    lower, upper = parity_binomial_bounds(k)
    return {
        "k": k,
        "parity": parity,
        "alias": alias,
        "common_model_scale": scale,
        "parity_over_scale": parity / scale,
        "alias_over_scale": alias / scale,
        "parity_lower_bound": lower,
        "parity_upper_bound": upper,
    }


def physical_lambda_decimal(precision: int = 80) -> Decimal:
    """Evaluate the positive algebraic root for diagnostics only."""

    if precision < 30:
        raise ValueError("precision must be at least 30 digits")
    with localcontext() as context:
        context.prec = precision
        value = Decimal("1.678573510428322")
        for _ in range(24):
            polynomial = value**3 + Decimal(4) * value**2 - Decimal(16)
            derivative = Decimal(3) * value**2 + Decimal(8) * value
            value -= polynomial / derivative
        return +value


def clock_diagnostics(precision: int = 80) -> dict[str, Decimal]:
    """Return high-precision diagnostics for the strict clock drift."""

    with localcontext() as context:
        context.prec = precision
        physical = physical_lambda_decimal(precision)
        hatted = Decimal(LAMBDA_HAT.numerator) / Decimal(LAMBDA_HAT.denominator)
        phase_slope = Decimal(1) - hatted.ln() / physical.ln()
        return {
            "lambda": +physical,
            "Lambda_hat": +hatted,
            "Lambda_hat_minus_lambda": +(hatted - physical),
            "physical_phase_slope": +phase_slope,
            "one_phase_unit_k": +(-Decimal(1) / phase_slope),
            "log_lambda_over_Lambda_hat": +(physical / hatted).ln(),
        }


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"
