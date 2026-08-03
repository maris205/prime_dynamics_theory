"""Exact and high-precision diagnostics for RH-356.

Finite rows reproduce the graded-counterloop formulas.  They are not noisy
head observations and do not supply the open ``D_(4k)(R) -> 0`` theorem.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_FLOOR, localcontext
from fractions import Fraction


R_H = Fraction(17, 20)
R = Fraction(7, 5)
LAMBDA_LOWER = Fraction(28, 17)
LAMBDA_UPPER = Fraction(17, 10)
FIXTURE_LAMBDA = Fraction(5, 3)
PHYSICAL_LAMBDA_DIAGNOSTIC = (
    "1.678573510428322265103705129306573200848357492195184493557517278808406444163932851476870838856614026"
)
C_M_DIAGNOSTIC = "1.9463429052009677158"


def _integer(value: int, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer")
    return value


def _fraction(value: int | Fraction, name: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    return Fraction(value)


def _lambda(value: int | Fraction) -> Fraction:
    lam = _fraction(value, "lambda_value")
    if not LAMBDA_LOWER < lam < LAMBDA_UPPER:
        raise ValueError("lambda_value must lie strictly between 28/17 and 17/10")
    return lam


def _fraction_text(value: object) -> object:
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {key: _fraction_text(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_fraction_text(item) for item in value]
    return value


def _decimal_text(value: Decimal) -> str:
    return format(+value, ".50E")


def exact_constants(
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, Fraction | bool]:
    """Return the exact rational reproduction constants."""

    lam = _lambda(lambda_value)
    x_value = R**2 / (R_H**2 * lam)
    return {
        "r_H": R_H,
        "R": R,
        "lambda": lam,
        "x": x_value,
        "x_identity": x_value == (R / R_H) ** 2 / lam,
        "x_is_superunit": x_value > 1,
    }


def exact_alias_budget(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> Fraction:
    """Return the first-alias weighted impulse for the ``C_M=1`` fixture."""

    order = _integer(k, "k")
    if order < 2:
        raise ValueError("k must be at least two")
    x_value = exact_constants(lambda_value)["x"]
    return Fraction(order - 1, order) * x_value**order


def exact_post_budget(
    k: int,
    depth: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> Fraction:
    """Return the exact post-first-alias budget through depth ``L``."""

    order = _integer(k, "k")
    level = _integer(depth, "depth")
    if order < 2:
        raise ValueError("k must be at least two")
    if not 1 <= level <= order - 1:
        raise ValueError("depth must satisfy 1 <= L <= k-1")
    x_value = exact_constants(lambda_value)["x"]
    return sum(
        (x_value ** (order + j) / (order + j) for j in range(1, level + 1)),
        Fraction(0),
    )


def exact_ratio_certificate(
    k: int,
    depth: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool]:
    """Return the exact ratio and its uniform geometric proxy."""

    order = _integer(k, "k")
    level = _integer(depth, "depth")
    alias = exact_alias_budget(order, lambda_value)
    post = exact_post_budget(order, level, lambda_value)
    x_value = exact_constants(lambda_value)["x"]
    exact_sum = Fraction(order, order - 1) * sum(
        (x_value**j / (order + j) for j in range(1, level + 1)),
        Fraction(0),
    )
    proxy = x_value * (x_value**level - 1) / (order * (x_value - 1))
    return {
        "k": order,
        "L": level,
        "alias_budget": alias,
        "post_budget": post,
        "ratio": post / alias,
        "ratio_identity": post / alias == exact_sum,
        "uniform_proxy": proxy,
        "ratio_over_proxy": (post / alias) / proxy,
        "finite_formula_only": True,
    }


def phase_diagnostic(
    k: int,
    c_text: str = "0",
    lambda_text: str = PHYSICAL_LAMBDA_DIAGNOSTIC,
    c_m_text: str = C_M_DIAGNOSTIC,
) -> dict[str, int | str | bool]:
    """Evaluate the synthetic finite-radius floor-phase law."""

    order = _integer(k, "k")
    if order < 3:
        raise ValueError("k must be at least three")
    if any(type(value) is not str for value in (c_text, lambda_text, c_m_text)):
        raise TypeError("decimal inputs must be strings")
    with localcontext() as context:
        context.prec = 90
        lam = Decimal(lambda_text)
        c_m = Decimal(c_m_text)
        shift = Decimal(c_text)
        lower = Decimal(28) / Decimal(17)
        upper = Decimal(17) / Decimal(10)
        if not lower < lam < upper:
            raise ValueError("lambda diagnostic must lie in the physical interval")
        if not c_m > 0:
            raise ValueError("C_M diagnostic must be positive")
        radius = Decimal(7) / Decimal(5)
        r_h = Decimal(17) / Decimal(20)
        x_value = radius**2 / (r_h**2 * lam)
        y_value = x_value * (-c_m.ln() / Decimal(order)).exp()
        log_x_k = Decimal(order).ln() / x_value.ln()
        floor_argument = log_x_k + shift
        level = int(floor_argument.to_integral_value(rounding=ROUND_FLOOR))
        if not 1 <= level <= order - 1:
            raise ValueError("floor depth must lie in 1 <= L <= k-1")
        phase = floor_argument - Decimal(level)
        alias = (Decimal(1) - Decimal(1) / Decimal(order)) * y_value**order
        post = sum(
            (
                y_value ** (order + j) / Decimal(order + j)
                for j in range(1, level + 1)
            ),
            Decimal(0),
        )
        ratio = post / alias
        phase_law = x_value / (x_value - 1) * x_value ** (shift - phase)
        lower_cluster = x_value**shift / (x_value - 1)
        upper_cluster = x_value ** (shift + 1) / (x_value - 1)
        return {
            "k": order,
            "L": level,
            "x": _decimal_text(x_value),
            "y_k": _decimal_text(y_value),
            "log_x_k": _decimal_text(log_x_k),
            "integer_phase": _decimal_text(phase),
            "ratio": _decimal_text(ratio),
            "phase_law": _decimal_text(phase_law),
            "ratio_over_phase_law": _decimal_text(ratio / phase_law),
            "cluster_lower": _decimal_text(lower_cluster),
            "cluster_upper": _decimal_text(upper_cluster),
            "phase_law_inside_closed_cluster": (
                lower_cluster <= phase_law <= upper_cluster
            ),
            "finite_formula_only": True,
            "synthetic_multiplier_law": True,
        }


def result_status() -> dict[str, object]:
    """Return the strict machine-readable RH-356 theorem ledger."""

    constants = exact_constants()
    exact_rows = [
        exact_ratio_certificate(k, depth)
        for k, depth in ((16, 2), (32, 4), (64, 7), (128, 11))
    ]
    phase_rows = [phase_diagnostic(k, "0") for k in (64, 128, 256, 512)]
    gates = {
        "A_canonical_intrinsic_determinant": False,
        "B_time_oriented_unitary_completion": False,
        "C_self_adjoint_generator_T_log_T": False,
        "D_von_mangoldt_prime_power_trace": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "counterloop_is_actual_noisy_head": False,
        "D_4k_transport_proved": False,
        "fixed_floor_offset_has_single_limit": False,
        "one_minus_y_k_to_minus_L_dropped_at_fixed_depth": False,
        "C_M_survives_in_mesoscopic_ratio": False,
        "mesoscopic_formula_extended_to_linear_depth": False,
        "direct_p_or_full_E_off_closed": False,
        "rh241_moving_noisy_envelope_closed": False,
        "rh288_activated": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
    }
    return {
        "status": "RH-356_sharp_post_first_alias_mesoscopic_crossover",
        "verdict": "GO_SCOPED",
        "constants": _fraction_text(constants),
        "diagnostic_constants": {
            "lambda": PHYSICAL_LAMBDA_DIAGNOSTIC,
            "C_M": C_M_DIAGNOSTIC,
            "not_interval_certificates": True,
        },
        "exact_ledger": {
            "alias": "A_k=(1-1/k)*y_k^k",
            "post_band": "B_(k,L)=sum_(j=1)^L y_k^(k+j)/(k+j)",
            "ratio": "B/A=(k/(k-1))*sum_(j=1)^L y_k^j/(k+j)",
        },
        "uniform_law": {
            "domain": "1<=L<=ell_k_with_ell_k=o(k)",
            "formula": "B/A=x*(x^L-1)/(k*(x-1))*(1+o(1))_uniformly",
            "fixed_depth": "for_fixed_L,_k*B/A->x*(x^L-1)/(x-1)",
            "growing_depth_only": "L->infinity_and_L=o(k)",
            "finite_radius_factor": "1-y_k^(-L)_must_be_retained_at_bounded_depth",
            "master_after_deleting_1-y_k^(-L)": "B/A=[x/(x-1)]*x^(L-log_x(k))*(1+o(1))",
            "C_M_cancels": True,
        },
        "crossover": {
            "delta": "L-log_x(k)",
            "subcritical": "delta->-infinity_implies_ratio->0",
            "finite": "delta->c_implies_ratio->[x/(x-1)]*x^c",
            "supercritical": "delta->infinity_implies_ratio->infinity",
            "balance_offset": "log_x((x-1)/x)",
            "physical_depth": "n-2k=(2/log(x))*log(log(1/sigma))+O(1)",
        },
        "integer_phase": {
            "depth": "floor(log_x(k)+c)",
            "law": "ratio=[x/(x-1)]*x^(c-{log_x(k)+c})*(1+o(1))",
            "phase_limit_set": "[0,1]",
            "liminf": "x^c/(x-1)",
            "limsup": "x^(c+1)/(x-1)",
            "single_limit": False,
        },
        "conditional_actual_head": {
            "hypothesis": "original_same_clock_unnormalized_D_(4k)(R)->0",
            "hypothesis_proved_here": False,
            "partial_budget_transfer": True,
            "odd_post_budget_tends_to_zero": True,
            "inherits_mesoscopic_ratio_only_conditionally": True,
            "root_or_rank_transfer": False,
        },
        "exact_fixture_rows": _fraction_text(exact_rows),
        "phase_diagnostic_rows": phase_rows,
        "finite_rows_are_formula_reproduction_only": True,
        "gates": gates,
        "false_claims": false_claims,
        "scope": [
            "unconditional_graded_counterloop_crossover",
            "1-y_k^(-L)_removed_only_when_L_tends_to_infinity",
            "integer_floor_phase_retained",
            "actual_head_transfer_conditional_on_unnormalized_D_4k_only",
            "no_linear_depth_extension",
            "no_RH_conclusion",
        ],
    }
