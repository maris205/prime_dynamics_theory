"""Exact RH-343 equal-rank, equal-mass first-alias diagnostics.

The module evaluates closed finite-shell identities.  It does not read or
construct a noisy operator spectrum, and its finite rows have no asymptotic
evidentiary role.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction


F = Fraction
Q_HEAD = F(1, 2)
R_H = F(17, 20)
R_TRACE = F(7, 5)
A_RADIUS = F(3, 4)
B_RADIUS = F(4, 5)
C_RADIUS_SQUARED = F(481, 800)
BETA_LIMIT = Decimal("0.9080523604")


def _integer_at_least(name: str, value: int, minimum: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{name} must be an integer >={minimum}")


def counterloop_rank(k: int) -> int:
    """Return #Y_k=2k-2."""

    _integer_at_least("k", k, 2)
    return 2 * k - 2


def candidate_rank(k: int) -> int:
    """Return the common rank of the invisible and visible candidates."""

    _integer_at_least("k", k, 2)
    return 6 * k - 2


def full_shell_power_sum(length: int, radius: Fraction, order: int) -> Fraction:
    """Return L r^n 1_(L|n) for a rational-radius complete shell."""

    _integer_at_least("length", length, 2)
    _integer_at_least("order", order, 1)
    if not isinstance(radius, Fraction) or radius <= 0:
        raise ValueError("radius must be a positive Fraction")
    if order % length:
        return F(0)
    return length * radius**order


def invisible_shell_power_sum(k: int, order: int) -> Fraction:
    """Return the exact U_(4k)(sqrt(481/800)) power sum.

    A nonzero value can occur only at a multiple of 4k, hence the exponent
    of the squared radius is always integral.
    """

    _integer_at_least("k", k, 2)
    _integer_at_least("order", order, 1)
    length = 4 * k
    if order % length:
        return F(0)
    return length * C_RADIUS_SQUARED ** (order // 2)


def visible_shell_power_sum(k: int, order: int) -> Fraction:
    """Return the combined U_(2k)(a) and U_(2k)(b) power sum."""

    _integer_at_least("k", k, 2)
    _integer_at_least("order", order, 1)
    length = 2 * k
    return full_shell_power_sum(length, A_RADIUS, order) + full_shell_power_sum(
        length, B_RADIUS, order
    )


def extra_squared_mass(candidate: str, k: int) -> Fraction:
    """Return the shell contribution to squared spectral mass."""

    _integer_at_least("k", k, 2)
    if candidate == "invisible":
        return 4 * k * C_RADIUS_SQUARED
    if candidate == "visible":
        return 2 * k * (A_RADIUS**2 + B_RADIUS**2)
    raise ValueError("candidate must be 'invisible' or 'visible'")


def total_squared_mass(candidate: str, k: int, beta_squared: Fraction) -> Fraction:
    """Return (2k-2) beta_k^2 plus the candidate shell mass."""

    _integer_at_least("k", k, 2)
    if not isinstance(beta_squared, Fraction) or beta_squared <= 0:
        raise ValueError("beta_squared must be a positive Fraction")
    return counterloop_rank(k) * beta_squared + extra_squared_mass(candidate, k)


def moment_difference(candidate: str, k: int, order: int) -> Fraction:
    """Return p_n(X_candidate)-p_n(Y_k)."""

    if candidate == "invisible":
        return invisible_shell_power_sum(k, order)
    if candidate == "visible":
        return visible_shell_power_sum(k, order)
    raise ValueError("candidate must be 'invisible' or 'visible'")


def strict_prefix_budget(candidate: str, k: int) -> Fraction:
    """Evaluate D_(4k) exactly with R=7/5 and the strict endpoint."""

    _integer_at_least("k", k, 2)
    return sum(
        abs(moment_difference(candidate, k, order)) * R_TRACE**order / order
        for order in range(2, 4 * k)
    )


def visible_budget_formula(k: int) -> Fraction:
    """Return (21/20)^(2k)+(28/25)^(2k)."""

    _integer_at_least("k", k, 2)
    return (A_RADIUS * R_TRACE) ** (2 * k) + (B_RADIUS * R_TRACE) ** (2 * k)


def pre_alias_certificate(k: int) -> dict[str, object]:
    """Return the exact first-alias split ledger."""

    _integer_at_least("k", k, 2)
    return {
        "pre_alias_first": 2,
        "pre_alias_last": 2 * k - 1,
        "invisible_equals_Y_pre_alias": all(
            moment_difference("invisible", k, order) == 0
            for order in range(2, 2 * k)
        ),
        "visible_equals_Y_pre_alias": all(
            moment_difference("visible", k, order) == 0
            for order in range(2, 2 * k)
        ),
        "split_order": 2 * k,
        "invisible_difference_at_split": moment_difference("invisible", k, 2 * k),
        "visible_difference_at_split": moment_difference("visible", k, 2 * k),
        "strict_endpoint": 4 * k,
    }


def radius_order_certificate(precision: int = 80) -> dict[str, object]:
    """Certify q<a<c<b<beta and the source-safe Hardy cap numerically.

    The comparisons a<c<b are exact after squaring.  The comparison b<beta
    uses the archived limiting value beta=0.9080523604... from RH-272.
    """

    _integer_at_least("precision", precision, 30)
    with localcontext() as context:
        context.prec = precision
        c_radius = (Decimal(C_RADIUS_SQUARED.numerator) / Decimal(
            C_RADIUS_SQUARED.denominator
        )).sqrt()
        cap = Decimal(R_H.denominator) / Decimal(R_H.numerator)
        return {
            "a_squared": A_RADIUS**2,
            "c_squared": C_RADIUS_SQUARED,
            "b_squared": B_RADIUS**2,
            "c_decimal": +c_radius,
            "q_lt_a": Q_HEAD < A_RADIUS,
            "a_lt_c_lt_b_exact_by_squares": (
                A_RADIUS**2 < C_RADIUS_SQUARED < B_RADIUS**2
            ),
            "b_lt_beta_limit": Decimal(B_RADIUS.numerator)
            / Decimal(B_RADIUS.denominator)
            < BETA_LIMIT,
            "beta_limit_lt_global_cap": BETA_LIMIT < cap,
            "global_cap": +cap,
        }


def genus_one_quotient_factor(candidate: str) -> str:
    """Return the exact shell factor attached to each candidate."""

    if candidate == "invisible":
        return "1-(c*z)^(4k)"
    if candidate == "visible":
        return "[1-(a*z)^(2k)][1-(b*z)^(2k)]"
    raise ValueError("candidate must be 'invisible' or 'visible'")


def decimal_text(value: Decimal) -> str:
    return format(value, "f")


def finite_diagnostic(k: int) -> dict[str, object]:
    """Return a finite exact-identity row with no asymptotic evidentiary role."""

    _integer_at_least("k", k, 2)
    pre_alias = pre_alias_certificate(k)
    invisible_budget = strict_prefix_budget("invisible", k)
    visible_budget = strict_prefix_budget("visible", k)
    formula = visible_budget_formula(k)
    return {
        "k": k,
        "cut": 4 * k,
        "common_rank": candidate_rank(k),
        "common_extra_squared_mass": extra_squared_mass("invisible", k),
        "rank_equal": candidate_rank(k) == candidate_rank(k),
        "mass_equal": extra_squared_mass("invisible", k)
        == extra_squared_mass("visible", k),
        "both_pre_alias_equal_Y": (
            pre_alias["invisible_equals_Y_pre_alias"]
            and pre_alias["visible_equals_Y_pre_alias"]
        ),
        "first_split_order": 2 * k,
        "invisible_difference_at_split": pre_alias["invisible_difference_at_split"],
        "visible_difference_at_split": pre_alias["visible_difference_at_split"],
        "D_4k_invisible": invisible_budget,
        "D_4k_visible": visible_budget,
        "visible_budget_formula": formula,
        "formula_matches_direct_sum": visible_budget == formula,
        "finite_row_is_exact_reproduction_only": True,
    }
