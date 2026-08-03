"""RH-349 two-lower-sideband phase diagnostics.

The theorems in RH-349 are symbolic and conditional on two named actual
remainder hypotheses.  Decimal rows reproduce the finite scalar formulas
with the fixture ``Y_2=Y_3=0``.  They are not interval certificates,
operator computations, or evidence for those hypotheses.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache


F = Fraction
R_H = F(17, 20)
R_TRACE = F(7, 5)
C_STAR_DIAGNOSTIC = Decimal("0.105258535936908")
C_M_DIAGNOSTIC = Decimal("1.946342905200968")


def physical_constants(precision: int = 100) -> dict[str, Decimal]:
    """Return the archived physical constants at diagnostic precision."""

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
        x = (beta * radius) ** 2
        return {
            "u_c": +u,
            "r": +r,
            "lambda": +lam,
            "beta": +beta,
            "x": +x,
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
def boundary_multiplier(period_parameter: int, precision: int = 100) -> Decimal:
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


def balance_phase_j2(precision: int = 100) -> Decimal:
    """Solve diagnostically C_* C_M lambda^(eta-2)=1."""

    with localcontext() as context:
        context.prec = precision
        lam = physical_constants(precision)["lambda"]
        return +(
            Decimal(2)
            - (C_STAR_DIAGNOSTIC * C_M_DIAGNOSTIC).ln() / lam.ln()
        )


def relative_objective(a: Decimal, lam: Decimal) -> Decimal:
    """The unweighted two-coordinate minimax objective."""

    if a <= 0 or lam <= 1:
        raise ValueError("the minimax domain is a>0 and lambda>1")
    return max(abs(a - 1), abs(a / lam - 1))


def weighted_objective(a: Decimal, lam: Decimal, x: Decimal) -> Decimal:
    """The physical prefix-weighted two-coordinate objective."""

    if a <= 0 or lam <= 1 or x <= 1:
        raise ValueError("the weighted domain is a>0, lambda>1, x>1")
    return x * abs(a - 1) + abs(a / lam - 1)


def minimax_ledger(precision: int = 100) -> dict[str, Decimal]:
    """Return the exact analytic optimizers evaluated diagnostically."""

    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        lam = constants["lambda"]
        x = constants["x"]
        relative_optimizer = 2 * lam / (lam + 1)
        relative_minimum = (lam - 1) / (lam + 1)
        weighted_optimizer = Decimal(1)
        weighted_minimum = 1 - 1 / lam
        return {
            "relative_optimizer": +relative_optimizer,
            "relative_minimum": +relative_minimum,
            "relative_objective_at_optimizer": +relative_objective(
                relative_optimizer, lam
            ),
            "weighted_optimizer": +weighted_optimizer,
            "weighted_minimum": +weighted_minimum,
            "weighted_objective_at_optimizer": +weighted_objective(
                weighted_optimizer, lam, x
            ),
        }


def sideband_entry(
    k: int,
    j: int,
    precision: int = 100,
) -> dict[str, Decimal | int]:
    """Reconstruct one fixed lower-sideband diagnostic at a=gamma_2=1."""

    if j not in (2, 3):
        raise ValueError("RH-349 uses exactly j=2 and j=3")
    m = k - j
    if m < 2:
        raise ValueError("the boundary period parameter must be at least 2")
    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        lam = constants["lambda"]
        beta = constants["beta"]
        x = constants["x"]
        r_h = Decimal(R_H.numerator) / R_H.denominator
        radius = Decimal(R_TRACE.numerator) / R_TRACE.denominator

        multiplier_m = boundary_multiplier(m, precision)
        multiplier_k = boundary_multiplier(k, precision)
        hardy = r_h ** (-2 * m)
        point_weight = hardy / (1 + multiplier_m)
        full_atom = Decimal(2 * m) * point_weight
        beta_k = (-multiplier_k.ln() / Decimal(2 * k)).exp() / r_h
        radial = Decimal(2) * (beta ** (2 * m) - beta_k ** (2 * m))
        demand = full_atom + radial

        eta = balance_phase_j2(precision)
        sqrt_sigma = ((eta - Decimal(k)) * lam.ln()).exp()
        delta = C_STAR_DIAGNOSTIC * sqrt_sigma
        parity = hardy * (1 - (1 - delta) ** (2 * m))

        target = Decimal(m) * radius ** (-2 * m)
        direct_fixture = parity - demand
        weighted_residual = abs(direct_fixture) / (2 * target)
        gamma_limit = (
            C_STAR_DIAGNOSTIC
            * C_M_DIAGNOSTIC
            * ((eta - Decimal(j)) * lam.ln()).exp()
        )
        demand_reference = (
            Decimal(2 * m) / C_M_DIAGNOSTIC * beta ** (2 * m)
        )
        weighted_reference = abs(gamma_limit - 1) / C_M_DIAGNOSTIC * x**m
        return {
            "k": k,
            "j": j,
            "m": m,
            "order": 2 * m,
            "eta_j2_balance": eta,
            "sqrt_sigma": sqrt_sigma,
            "delta_leading_model": delta,
            "multiplier_m": multiplier_m,
            "multiplier_k": multiplier_k,
            "point_weight": point_weight,
            "full_atom": full_atom,
            "radial": radial,
            "demand": demand,
            "demand_reference": demand_reference,
            "demand_over_reference": demand / demand_reference,
            "parity": parity,
            "parity_over_demand": parity / demand,
            "gamma_limit": gamma_limit,
            "target_H_m": target,
            "direct_fixture_Y_zero": direct_fixture,
            "weighted_residual_W_j": weighted_residual,
            "weighted_residual_over_x_m": weighted_residual / x**m,
            "weighted_asymptotic_reference": weighted_reference,
        }


def two_sideband_row(k: int, precision: int = 100) -> dict[str, object]:
    """Build the j=2,3 row at the physically weighted optimum a=1."""

    if k < 6:
        raise ValueError("k must be at least 6")
    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        lam = constants["lambda"]
        x = constants["x"]
        entries = [sideband_entry(k, j, precision) for j in (2, 3)]
        weighted_sum = sum(
            (entry["weighted_residual_W_j"] for entry in entries),
            Decimal(0),
        )
        normalized = weighted_sum / x ** (k - 3)
        scaled_normalized = C_M_DIAGNOSTIC * normalized
        weighted_minimum = 1 - 1 / lam
        raw_limit = weighted_minimum / C_M_DIAGNOSTIC
        return {
            "k": k,
            "phase_choice": "a=gamma_2=1",
            "fixture": "Y_2=Y_3=0_formula_reproduction_only",
            "entries": entries,
            "weighted_residual_sum": weighted_sum,
            "normalization": "x^(k-3)",
            "normalized_weighted_sum": normalized,
            "raw_limit": raw_limit,
            "raw_limit_absolute_error": abs(normalized - raw_limit),
            "C_M_scaled_normalized_sum": scaled_normalized,
            "C_M_scaled_limit": weighted_minimum,
            "C_M_scaled_absolute_error": abs(
                scaled_normalized - weighted_minimum
            ),
        }


def decimal_text(value: Decimal) -> str:
    return format(value, "f")
