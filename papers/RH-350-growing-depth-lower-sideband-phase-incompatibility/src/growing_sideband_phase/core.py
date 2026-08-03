"""RH-350 growing-depth lower-sideband diagnostics.

The analytic theorems are symbolic.  Finite decimal rows evaluate exact
boundary multipliers and scalar formulas under the fixtures ``a_k=1`` and
``Y=0``.  They are not interval certificates or noisy-operator data.
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
            "x_lambda": +(x * lam),
        }


def _h(value: Decimal, u: Decimal) -> Decimal:
    return ((Decimal(1) - ((Decimal(1) - value) / u).sqrt()) / u).sqrt()


def _q(value: Decimal, u: Decimal) -> Decimal:
    return ((Decimal(1) + ((Decimal(1) - value) / u).sqrt()) / u).sqrt()


@lru_cache(maxsize=None)
def _boundary_point(period_parameter: int, precision: int) -> Decimal:
    if period_parameter < 1:
        raise ValueError("period parameter must be positive")
    u = physical_constants(precision)["u_c"]
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


def balance_phase(precision: int = 100) -> Decimal:
    """Solve diagnostically C_* C_M lambda^(eta-2)=1."""

    with localcontext() as context:
        context.prec = precision
        lam = physical_constants(precision)["lambda"]
        return +(
            Decimal(2)
            - (C_STAR_DIAGNOSTIC * C_M_DIAGNOSTIC).ln() / lam.ln()
        )


def relative_objective(a: Decimal, lam: Decimal, depth: int) -> Decimal:
    if a <= 0 or lam <= 1 or depth < 3:
        raise ValueError("require a>0, lambda>1, and depth>=3")
    return max(
        abs(a * lam ** (2 - j) - 1)
        for j in range(2, depth + 1)
    )


def relative_minimax(depth: int, precision: int = 100) -> dict[str, object]:
    if depth < 3:
        raise ValueError("depth must be at least 3")
    with localcontext() as context:
        context.prec = precision
        lam = physical_constants(precision)["lambda"]
        power = lam ** (depth - 2)
        optimizer = 2 * power / (power + 1)
        minimum = (power - 1) / (power + 1)
        return {
            "depth": depth,
            "optimizer": +optimizer,
            "minimum": +minimum,
            "objective_at_optimizer": +relative_objective(
                optimizer, lam, depth
            ),
        }


def weighted_objective(a: Decimal, lam: Decimal, x: Decimal, n: int) -> Decimal:
    if a <= 0 or lam <= 1 or x <= 1 or n < 1:
        raise ValueError("require a>0, lambda>1, x>1, and n>=1")
    return sum(
        (x ** (-r) * abs(a * lam ** (-r) - 1) for r in range(n + 1)),
        Decimal(0),
    )


def weighted_minimax(n: int, precision: int = 100) -> dict[str, object]:
    if n < 1:
        raise ValueError("n must be at least 1")
    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        lam = constants["lambda"]
        x = constants["x"]
        minimum = (
            (1 - x ** (-n)) / (x - 1)
            - (1 - (x * lam) ** (-n)) / (x * lam - 1)
        )
        limit = 1 / (x - 1) - 1 / (x * lam - 1)
        return {
            "n": n,
            "depth": n + 2,
            "optimizer": Decimal(1),
            "minimum": +minimum,
            "objective_at_optimizer": +weighted_objective(
                Decimal(1), lam, x, n
            ),
            "limit": +limit,
            "gap_to_limit": +(limit - minimum),
        }


def sideband_entry(
    k: int,
    j: int,
    precision: int = 100,
) -> dict[str, Decimal | int]:
    """Evaluate one scalar-fixture lower-sideband row at a_k=1, Y=0."""

    if k < 7 or j < 2 or j > k - 2:
        raise ValueError("require k>=7 and 2<=j<=k-2")
    m = k - j
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

        eta = balance_phase(precision)
        sqrt_sigma = ((eta - Decimal(k)) * lam.ln()).exp()
        delta = C_STAR_DIAGNOSTIC * sqrt_sigma
        parity = hardy * (1 - (1 - delta) ** (2 * m))

        target = Decimal(m) * radius ** (-2 * m)
        direct_fixture = parity - demand
        weighted_residual = abs(direct_fixture) / (2 * target)
        demand_normalized = C_M_DIAGNOSTIC * demand / (
            2 * target * x**m
        )
        parity_normalized = C_M_DIAGNOSTIC * parity / (
            2 * target * x**m
        )
        phase_target = lam ** (2 - j)
        contribution = weighted_residual / x ** (k - 2)
        contribution_reference = (
            x ** (2 - j) * abs(phase_target - 1) / C_M_DIAGNOSTIC
        )
        return {
            "k": k,
            "j": j,
            "m": m,
            "order": 2 * m,
            "eta_balance": eta,
            "sqrt_sigma": sqrt_sigma,
            "delta_leading_model": delta,
            "multiplier_m": multiplier_m,
            "multiplier_k": multiplier_k,
            "full_atom": full_atom,
            "radial": radial,
            "demand": demand,
            "parity": parity,
            "target_H_m": target,
            "direct_fixture_Y_zero": direct_fixture,
            "demand_normalized": demand_normalized,
            "parity_normalized": parity_normalized,
            "phase_target": phase_target,
            "weighted_residual_W": weighted_residual,
            "top_normalized_contribution": contribution,
            "top_normalized_reference": contribution_reference,
        }


def growing_row(
    k: int,
    depth: int,
    precision: int = 100,
) -> dict[str, object]:
    if depth < 3 or depth > k - 2:
        raise ValueError("require 3<=depth<=k-2")
    with localcontext() as context:
        context.prec = precision
        entries = [sideband_entry(k, j, precision) for j in range(2, depth + 1)]
        normalized_sum = sum(
            (entry["top_normalized_contribution"] for entry in entries),
            Decimal(0),
        )
        reference = weighted_minimax(depth - 2, precision)
        normalized_reference = reference["minimum"] / C_M_DIAGNOSTIC
        demand_error = max(
            abs(entry["demand_normalized"] - 1) for entry in entries
        )
        parity_error = max(
            abs(entry["parity_normalized"] - entry["phase_target"])
            for entry in entries
        )
        return {
            "k": k,
            "depth_J": depth,
            "N": depth - 2,
            "fixture": "a_k=1_and_Y_kj=0_formula_reproduction_only",
            "entries": entries,
            "normalized_weighted_sum": normalized_sum,
            "normalized_minimax_reference": normalized_reference,
            "normalized_absolute_error": abs(
                normalized_sum - normalized_reference
            ),
            "max_demand_uniform_error": demand_error,
            "max_parity_uniform_error": parity_error,
        }


def decimal_text(value: Decimal) -> str:
    return format(value, "f")
