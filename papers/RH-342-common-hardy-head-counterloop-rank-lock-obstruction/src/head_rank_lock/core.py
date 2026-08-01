"""Exact RH-342 rank, moment, and rate diagnostics.

The executable layer evaluates closed formulas and finite consistency rows.
It does not read noisy eigenvalues, infer a physical head rank, or turn the
information-class counterexample into an actual operator statement.
"""

from __future__ import annotations

from decimal import Decimal, getcontext, localcontext
from fractions import Fraction


F = Fraction
Q_HEAD = F(1, 2)
R_H = F(17, 20)
R_TRACE = F(7, 5)
HIDDEN_RADIUS = F(3, 4)


def _integer_at_least(name: str, value: int, minimum: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{name} must be an integer >={minimum}")


def _decimal(value: Decimal | Fraction | int) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, Fraction):
        with localcontext() as context:
            context.prec = max(getcontext().prec, 100)
            return +(Decimal(value.numerator) / Decimal(value.denominator))
    if isinstance(value, int) and not isinstance(value, bool):
        return Decimal(value)
    raise TypeError("expected Decimal, Fraction, or integer")


def physical_constants(precision: int = 100) -> dict[str, Decimal]:
    """Return the repository constants on the Hardy normalization."""

    if not isinstance(precision, int) or isinstance(precision, bool) or precision < 50:
        raise ValueError("precision must be an integer at least 50")
    with localcontext() as context:
        context.prec = precision
        u = Decimal("1.543689012692076")
        for _ in range(32):
            polynomial = u**3 - 2 * u**2 + 2 * u - 2
            derivative = 3 * u**2 - 4 * u + 2
            u -= polynomial / derivative
        lam = 2 * u * (u - 1)
        r_h = _decimal(R_H)
        beta = Decimal(1) / (r_h * lam.sqrt())
        return {"u_c": +u, "lambda": +lam, "beta": +beta}


def common_clock_thresholds(precision: int = 100) -> dict[str, Decimal]:
    """Return the RH-299 rate thresholds for the cut m=4k."""

    with localcontext() as context:
        context.prec = precision
        constants = physical_constants(precision)
        lam = constants["lambda"]
        beta = constants["beta"]
        radius = _decimal(R_TRACE)
        global_cap = Decimal(1) / _decimal(R_H)
        global_threshold = 2 * (global_cap * radius).ln() / lam.ln()
        local_threshold = 2 * (beta * radius).ln() / lam.ln()
        return {
            "clock_slope": +(Decimal(2) / lam.ln()),
            "global_cap": +global_cap,
            "local_shell_cap": +beta,
            "global_threshold": +global_threshold,
            "local_threshold": +local_threshold,
            "threshold_gap": +(global_threshold - local_threshold),
        }


def counterloop_rank(k: int) -> int:
    _integer_at_least("k", k, 2)
    return 2 * k - 2


def hidden_shell_rank(k: int) -> int:
    _integer_at_least("k", k, 2)
    return 4 * k


def strict_prefix_aliases(k: int) -> dict[str, object]:
    """Return the exact alias membership for 2<=n<4k."""

    _integer_at_least("k", k, 2)
    return {
        "lower_order": 2,
        "cut": 4 * k,
        "first_alias": 2 * k,
        "contains_first_alias": 2 <= 2 * k < 4 * k,
        "contains_second_alias": 2 <= 4 * k < 4 * k,
        "strict_upper_endpoint_excluded": True,
    }


def counterloop_power_sum(
    k: int, order: int, beta: Decimal | Fraction
) -> Decimal:
    """Evaluate beta^n(2k 1_{2k|n}-1-(-1)^n)."""

    _integer_at_least("k", k, 2)
    _integer_at_least("order", order, 1)
    beta_decimal = _decimal(beta)
    if beta_decimal <= 0:
        raise ValueError("beta must be positive")
    coefficient = 2 * k * int(order % (2 * k) == 0) - 1 - (-1) ** order
    with localcontext() as context:
        context.prec = max(100, len(beta_decimal.as_tuple().digits) + 20)
        return +(beta_decimal**order * Decimal(coefficient))


def hidden_shell_power_sum(k: int, order: int) -> Fraction:
    """Return the exact power sum of the radius-3/4 full 4k shell."""

    _integer_at_least("k", k, 2)
    _integer_at_least("order", order, 1)
    if order % (4 * k):
        return F(0)
    return 4 * k * HIDDEN_RADIUS**order


def rank_lock_lower_bound(
    actual_rank: int,
    counter_rank: int,
    beta: Decimal | Fraction,
    q: Fraction = Q_HEAD,
) -> Decimal:
    """Evaluate q(r-m)_+ + beta(m-r)_+."""

    _integer_at_least("actual_rank", actual_rank, 0)
    _integer_at_least("counter_rank", counter_rank, 0)
    if not isinstance(q, Fraction) or q <= 0:
        raise ValueError("q must be a positive Fraction")
    beta_decimal = _decimal(beta)
    if beta_decimal <= 0:
        raise ValueError("beta must be positive")
    excess_actual = max(actual_rank - counter_rank, 0)
    excess_counter = max(counter_rank - actual_rank, 0)
    with localcontext() as context:
        context.prec = max(100, len(beta_decimal.as_tuple().digits) + 20)
        return +(
            _decimal(q) * excess_actual + beta_decimal * excess_counter
        )


def shifted_uniqueness_certificate(
    rank_cap: int, rank_x: int, rank_y: int
) -> dict[str, object]:
    """Return the degree/vanishing ledger in the shifted-moment proof."""

    _integer_at_least("rank_cap", rank_cap, 1)
    _integer_at_least("rank_x", rank_x, 1)
    _integer_at_least("rank_y", rank_y, 1)
    if rank_x > rank_cap or rank_y > rank_cap:
        raise ValueError("both ranks must not exceed the declared cap")
    numerator_degree_bound = rank_x + rank_y - 1
    vanishing_order = 2 * rank_cap
    return {
        "rank_cap": rank_cap,
        "rank_x": rank_x,
        "rank_y": rank_y,
        "moment_first": 2,
        "moment_last": 2 * rank_cap + 1,
        "coefficient_count": 2 * rank_cap,
        "denominator_degree_bound": rank_x + rank_y,
        "numerator_degree_bound": numerator_degree_bound,
        "vanishing_order": vanishing_order,
        "degree_forces_zero_numerator": numerator_degree_bound < vanishing_order,
    }


def genus_one_log_coefficient(defect: Fraction, order: int) -> Fraction:
    """Return the coefficient -d_n/n of the factor quotient logarithm."""

    if not isinstance(defect, Fraction):
        raise TypeError("defect must be a Fraction")
    _integer_at_least("order", order, 2)
    return -defect / order


def root_l1_budget_bound(
    distance: Decimal | Fraction,
    cap: Decimal | Fraction,
    cut: int,
    radius: Fraction = R_TRACE,
) -> Decimal:
    """Evaluate d R sum_{j=1}^{m-2}(BR)^j from RH-299."""

    _integer_at_least("cut", cut, 3)
    d = _decimal(distance)
    b = _decimal(cap)
    r = _decimal(radius)
    if d < 0 or b <= 0 or r <= 0:
        raise ValueError("distance must be nonnegative and cap/radius positive")
    with localcontext() as context:
        context.prec = max(
            100,
            len(d.as_tuple().digits) + len(b.as_tuple().digits) + 40,
        )
        ratio = b * r
        return +(d * r * sum((ratio**j for j in range(1, cut - 1)), Decimal(0)))


def finite_diagnostic(k: int, precision: int = 100) -> dict[str, object]:
    """Return finite formula checks; rows have no asymptotic evidentiary role."""

    _integer_at_least("k", k, 2)
    constants = physical_constants(precision)
    beta = constants["beta"]
    model_rank = counterloop_rank(k)
    shell_rank = hidden_shell_rank(k)
    return {
        "k": k,
        "cut": 4 * k,
        "counterloop_rank": model_rank,
        "hidden_shell_rank": shell_rank,
        "enlarged_rank": model_rank + shell_rank,
        "limiting_beta_first_alias_moment_diagnostic": counterloop_power_sum(
            k, 2 * k, beta
        ),
        "hidden_shell_prefix_moment_zero": all(
            hidden_shell_power_sum(k, order) == 0 for order in range(2, 4 * k)
        ),
        "hidden_shell_first_visible_moment": hidden_shell_power_sum(k, 4 * k),
        "padded_distance_lower_bound": rank_lock_lower_bound(
            model_rank + shell_rank, model_rank, beta
        ),
        "strict_prefix": strict_prefix_aliases(k),
        "finite_row_is_reproduction_only": True,
    }


def decimal_text(value: Decimal) -> str:
    return format(value, "f")
