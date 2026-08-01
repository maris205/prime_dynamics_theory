"""Deterministic RH-340 clock and two-order compensation diagnostics.

The executable layer checks exact index relations and high-precision
diagnostics only.  It never turns the printed multiplier constant into an
interval certificate and never evaluates a physical signed prefix.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction


F = Fraction
R_H = F(17, 20)
R_TRACE = F(7, 5)
U_RADIUS = R_TRACE / R_H
C_M_PRINTED = Decimal("1.9463429052")


def one_alias_cut(k: int, cut: int) -> bool:
    if not isinstance(k, int) or isinstance(k, bool) or k < 2:
        raise ValueError("k must be an integer >=2")
    if not isinstance(cut, int) or isinstance(cut, bool):
        raise ValueError("the cut must be an integer")
    if not (2 * k < cut <= 4 * k):
        raise ValueError("the one-alias cut must satisfy 2k<u<=4k")
    return True


def sideband_orders(k: int) -> tuple[int, int]:
    if not isinstance(k, int) or isinstance(k, bool) or k < 2:
        raise ValueError("k must be an integer >=2")
    return 2 * k, 2 * k - 2


def physical_constants(precision: int = 100) -> dict[str, Decimal]:
    if precision < 50:
        raise ValueError("precision must be at least 50 digits")
    with localcontext() as context:
        context.prec = precision
        u = Decimal("1.543689012692076")
        for _ in range(32):
            polynomial = u**3 - 2 * u**2 + 2 * u - 2
            derivative = 3 * u**2 - 4 * u + 2
            u -= polynomial / derivative
        r = u - 1
        lam = 2 * u * r
        beta = Decimal(1) / (
            (Decimal(R_H.numerator) / R_H.denominator) * lam.sqrt()
        )
        q_star = Decimal(1) / (
            (Decimal(R_H.numerator) / R_H.denominator) * lam
        )
        return {"u_c": +u, "lambda": +lam, "r": +r, "beta": +beta, "q_star": +q_star}


def tail_exponents(precision: int = 100) -> dict[str, Decimal]:
    with localcontext() as context:
        context.prec = precision
        lam = physical_constants(precision)["lambda"]
        noise = 2 * (Decimal(10) / 7).ln() / lam.ln() - 1
        target = 2 * (Decimal(17) * lam / Decimal(28)).ln() / lam.ln()
        return {"noise": +noise, "target": +target}


def prefix_weight(order: int, precision: int = 100) -> Decimal:
    """Return R^order/order in the Hardy disk normalization."""

    if not isinstance(order, int) or isinstance(order, bool) or order < 2:
        raise ValueError("order must be an integer >=2")
    with localcontext() as context:
        context.prec = precision
        radius = Decimal(R_TRACE.numerator) / R_TRACE.denominator
        return +(radius**order / Decimal(order))


def synchronization_diagnostic(k: int, precision: int = 100) -> dict[str, object]:
    """Produce finite diagnostics for the common cut u=4k."""

    if precision < 50:
        raise ValueError("precision must be at least 50 digits")
    critical, lower = sideband_orders(k)
    one_alias_cut(k, 4 * k)
    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        exponents = tail_exponents(precision)
        beta_r = constants["beta"] * (Decimal(R_TRACE.numerator) / R_TRACE.denominator)
        critical_power = beta_r ** critical
        lower_power = beta_r ** lower
        atom_majorant = (critical_power + lower_power) / C_M_PRINTED
        return {
            "k": k,
            "u": 4 * k,
            "critical_order": critical,
            "lower_sideband_order": lower,
            "one_alias_cut": True,
            "noise_tail_exponent": exponents["noise"],
            "target_tail_exponent": exponents["target"],
            "beta_R": beta_r,
            "critical_beta_R_power": critical_power,
            "lower_beta_R_power": lower_power,
            "separate_absolute_two_atom_majorant_diagnostic": atom_majorant,
            "critical_weight": prefix_weight(critical, precision),
            "lower_weight": prefix_weight(lower, precision),
            "finite_rows_are_diagnostics_only": True,
        }


def decimal_text(value: Decimal) -> str:
    return format(value, "f")
