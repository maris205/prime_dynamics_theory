"""Exact and high-precision formula checks for RH-355.

The rational fixture uses ``C_M=1`` and ``lambda=5/3`` so every finite
counterloop sum is exact.  The decimal rows evaluate the synthetic exact law
``|M_k|=C_M*lambda**k`` at repository diagnostics.  Neither family is an
observation of the actual noisy head or evidence for a transport theorem.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
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
    """Return exact physical constants for the rational reproduction fixture."""

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


def strict_upper_weighted_term(
    k: int,
    n: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> Fraction:
    """Return ``|s_(k,n)| R^n/n`` on ``2k<n<4k`` for the C_M=1 fixture."""

    order = _integer(k, "k")
    moment = _integer(n, "n")
    if order < 2:
        raise ValueError("k must be at least two")
    if not 2 * order < moment < 4 * order:
        raise ValueError("n must lie in the strict upper-alias band")
    if moment % 2:
        return Fraction(0)
    x_value = exact_constants(lambda_value)["x"]
    m = moment // 2
    return x_value**m / m


def exact_upper_budget(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool]:
    """Return the exact strict upper-band budget for ``C_M=1``."""

    order = _integer(k, "k")
    if order < 2:
        raise ValueError("k must be at least two")
    x_value = exact_constants(lambda_value)["x"]
    raw = sum((x_value**m / m for m in range(order + 1, 2 * order)), Fraction(0))
    normalized = raw / x_value**order
    asymptotic_ratio = normalized * 2 * order * (x_value - 1) / x_value**order
    return {
        "k": order,
        "even_term_count": order - 1,
        "raw_budget": raw,
        "normalized_budget": normalized,
        "normalized_asymptotic_ratio": asymptotic_ratio,
        "finite_formula_only": True,
    }


def exact_terminal_term(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool]:
    """Return the exact ``n=4k-2`` contribution for ``C_M=1``."""

    order = _integer(k, "k")
    if order < 2:
        raise ValueError("k must be at least two")
    x_value = exact_constants(lambda_value)["x"]
    raw = x_value ** (2 * order - 1) / (2 * order - 1)
    normalized = raw / x_value**order
    asymptotic_ratio = normalized * 2 * order / x_value ** (order - 1)
    budget_ratio = raw / exact_upper_budget(order, lambda_value)["raw_budget"]
    return {
        "k": order,
        "n": 4 * order - 2,
        "raw_term": raw,
        "normalized_term": normalized,
        "normalized_asymptotic_ratio": asymptotic_ratio,
        "terminal_over_budget": budget_ratio,
        "finite_formula_only": True,
    }


def counterexample_certificate(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool | str]:
    """Return the exact complete-shell counterexample ledger for ``C_M=1``."""

    order = _integer(k, "k")
    if order < 2:
        raise ValueError("k must be at least two")
    x_value = exact_constants(lambda_value)["x"]
    shell_order = 2 * order + 2
    raw_defect = x_value ** (order + 1) / (order + 1)
    normalized_defect = raw_defect / x_value**order
    return {
        "k": order,
        "N": shell_order,
        "N_in_strict_upper_band": 2 * order < shell_order < 4 * order,
        "only_one_shell_multiple_in_band": 2 * shell_order >= 4 * order,
        "relative_error_at_N": Fraction(1),
        "raw_defect": raw_defect,
        "normalized_defect": normalized_defect,
        "normalized_identity": normalized_defect == x_value / (order + 1),
        "shell_type": "complete_Nth_root_conjugation_closed_finite_normal_information_class",
        "finite_formula_only": True,
    }


def synthetic_asymptotic_row(
    k: int,
    lambda_text: str = PHYSICAL_LAMBDA_DIAGNOSTIC,
    c_m_text: str = C_M_DIAGNOSTIC,
) -> dict[str, int | str | bool]:
    """Evaluate the exact synthetic multiplier law with high precision."""

    order = _integer(k, "k")
    if order < 2:
        raise ValueError("k must be at least two")
    if type(lambda_text) is not str or type(c_m_text) is not str:
        raise TypeError("lambda_text and c_m_text must be decimal strings")
    with localcontext() as context:
        context.prec = 90
        lam = Decimal(lambda_text)
        c_m = Decimal(c_m_text)
        lower = Decimal(28) / Decimal(17)
        upper = Decimal(17) / Decimal(10)
        if not lower < lam < upper:
            raise ValueError("lambda diagnostic must lie in the physical interval")
        if not c_m > 0:
            raise ValueError("C_M diagnostic must be positive")
        r_h = Decimal(17) / Decimal(20)
        radius = Decimal(7) / Decimal(5)
        x_value = radius**2 / (r_h**2 * lam)
        y_value = x_value * (-c_m.ln() / Decimal(order)).exp()
        raw = sum(
            (y_value**m / Decimal(m) for m in range(order + 1, 2 * order)),
            Decimal(0),
        )
        normalized = raw / x_value**order
        budget_ratio = (
            normalized
            * Decimal(2)
            * c_m**2
            * Decimal(order)
            * (x_value - 1)
            / x_value**order
        )
        normalized_root = (normalized.ln() / Decimal(order)).exp()
        terminal = y_value ** (2 * order - 1) / Decimal(2 * order - 1)
        normalized_terminal = terminal / x_value**order
        terminal_ratio = (
            normalized_terminal
            * Decimal(2)
            * c_m**2
            * Decimal(order)
            / x_value ** (order - 1)
        )
        terminal_share = terminal / raw
        normalized_shell_defect = (
            y_value ** (order + 1) / Decimal(order + 1) / x_value**order
        )
        shell_ratio = (
            normalized_shell_defect * c_m * Decimal(order) / x_value
        )
        return {
            "k": order,
            "x": _decimal_text(x_value),
            "y_k": _decimal_text(y_value),
            "normalized_budget": _decimal_text(normalized),
            "normalized_budget_root": _decimal_text(normalized_root),
            "budget_asymptotic_ratio": _decimal_text(budget_ratio),
            "terminal_asymptotic_ratio": _decimal_text(terminal_ratio),
            "terminal_share": _decimal_text(terminal_share),
            "counterexample_normalized_defect": _decimal_text(normalized_shell_defect),
            "counterexample_scaled_ratio": _decimal_text(shell_ratio),
            "finite_formula_only": True,
            "synthetic_multiplier_law": True,
        }


def result_status() -> dict[str, object]:
    """Return the strict machine-readable RH-355 theorem ledger."""

    constants = exact_constants()
    exact_rows = [exact_upper_budget(k) for k in (8, 16, 32, 64)]
    terminal_rows = [exact_terminal_term(k) for k in (8, 16, 32, 64)]
    shell_rows = [counterexample_certificate(k) for k in (8, 16, 32, 64)]
    diagnostic_rows = [synthetic_asymptotic_row(k) for k in (8, 16, 32, 64)]
    gates = {
        "A_canonical_intrinsic_determinant": False,
        "B_time_oriented_unitary_completion": False,
        "C_self_adjoint_generator_T_log_T": False,
        "D_von_mangoldt_prime_power_trace": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "D_4k_transport_proved": False,
        "normalized_defect_implies_uniform_relative_matching": False,
        "counterexample_is_actual_noisy_operator": False,
        "actual_head_rank_identified": False,
        "counterloop_is_actual_spectral_submultiset": False,
        "direct_p_budget_transferred_to_q": False,
        "full_E_off_closed": False,
        "rh241_moving_noisy_envelope_closed": False,
        "rh288_activated": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
    }
    return {
        "status": "RH-355_upper_alias_counterloop_burden_and_head_transfer_precision",
        "verdict": "GO_SCOPED",
        "constants": _fraction_text(constants),
        "diagnostic_constants": {
            "lambda": PHYSICAL_LAMBDA_DIAGNOSTIC,
            "C_M": C_M_DIAGNOSTIC,
            "not_interval_certificates": True,
        },
        "source_types": {
            "actual_head": "h_(sigma,n)=sum_(mu_in_H_sigma)mu^n",
            "counterloop": "s_(k,n)=beta_k^n(2k*1_(2k|n)-1-(-1)^n)",
            "head_defect": "d_(sigma,k,n)=h_(sigma,n)-s_(k,n)",
            "direct_coefficient": "p_(sigma,k,n)=tau_(sigma,n)-a_n=q_(sigma,k,n)-d_(sigma,k,n)",
        },
        "source_anchors": {
            "RH-17": "M_k=-C_M*lambda^k*(1+o(1)), C_M>0",
            "RH-288": "unnormalized_weighted_head_defect_leaf",
            "RH-297": "alias_impulse_ledger_only",
            "RH-336": "physical_constants_and_x>1",
            "RH-340": "D_u(R)_same_clock_prefix_synchronization",
            "RH-342": "actual_modulus_complete_head_and_exact_counterloop_moments",
            "RH-354": "direct_p_distinct_from_q_and_head_defect",
        },
        "counterloop_theorem": {
            "raw_upper_budget": "C_up=sum_(m=k+1)^(2k-1)y_k^m/m",
            "raw_asymptotic": "C_up~x^(2k)/(2*C_M^2*k*(x-1))",
            "normalized_asymptotic": "x^(-k)C_up~x^k/(2*C_M^2*k*(x-1))",
            "normalized_kth_root": "x>1",
            "terminal_normalized": "x^(-k)|s_(k,4k-2)|R^(4k-2)/(4k-2)~x^(k-1)/(2*C_M^2*k)",
            "terminal_share": "(x-1)/x",
        },
        "conditional_transport": {
            "hypothesis": "original_unnormalized_D_(4k)(R)->0_on_one_physical_clock",
            "hypothesis_is_proved_here": False,
            "actual_upper_budget": "same_as_counterloop_budget",
            "odd_upper_weighted_head_budget": "tends_to_zero",
            "uniform_even_relative_precision": "o(k*x^(-k))",
            "terminal_relative_precision": "o(k*x^(-2k))",
        },
        "normalized_weak_condition": {
            "hypothesis": "Delta_up=x^(-k)*sum_upper|h-s|R^n/n->0",
            "aggregate_normalized_budget_transfer": True,
            "terminal_relative_precision": "o(k*x^(-k))",
            "uniform_bandwise_relative_matching": False,
            "does_not_imply_unnormalized_D_4k": True,
        },
        "counterexample": {
            "shell": "N=2k+2_complete_root_shell_at_a_k=beta_k*(2/N)^(1/N)",
            "relative_error_at_N": "1",
            "normalized_defect": "~x/(C_M*k)->0",
            "unnormalized_defect": "~x^(k+1)/(C_M*k)->infinity",
            "scope": "finite_conjugation_closed_normal_information_class_only",
        },
        "exact_fixture_rows": _fraction_text(exact_rows),
        "terminal_fixture_rows": _fraction_text(terminal_rows),
        "counterexample_fixture_rows": _fraction_text(shell_rows),
        "diagnostic_rows": diagnostic_rows,
        "finite_rows_are_formula_reproduction_only": True,
        "gates": gates,
        "false_claims": false_claims,
        "scope": [
            "unconditional_graded_counterloop_asymptotic",
            "actual_head_conclusions_are_conditional_only",
            "weak_normalized_defect_has_a_rigorous_information_class_obstruction",
            "no_direct_p_q_or_E_off_transfer",
            "no_RH_conclusion",
        ],
    }
