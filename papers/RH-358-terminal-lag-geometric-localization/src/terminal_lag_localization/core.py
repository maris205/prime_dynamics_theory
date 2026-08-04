"""Exact and high-precision diagnostics for RH-358.

Finite rows reproduce deterministic graded-counterloop formulas.  They are
not observations of an actual noisy head and do not prove the open same-clock
hypothesis ``D_(4k)(R) -> 0``.
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


def _validate_k(k: int) -> int:
    order = _integer(k, "k")
    if order < 2:
        raise ValueError("k must be at least two")
    return order


def _validate_lag(k: int, q: int) -> tuple[int, int]:
    order = _validate_k(k)
    lag = _integer(q, "q")
    if not 0 <= lag <= order - 2:
        raise ValueError("q must satisfy 0 <= q <= k-2")
    return order, lag


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


def _decimal_power(base: Decimal, exponent: Decimal) -> Decimal:
    return (exponent * base.ln()).exp()


def exact_constants(
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, Fraction | bool]:
    """Return exact rational reproduction constants."""

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


def _exact_weights(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> list[Fraction]:
    order = _validate_k(k)
    x_value = exact_constants(lambda_value)["x"]
    return [
        x_value ** (2 * order - 1 - r) / (2 * order - 1 - r)
        for r in range(order - 1)
    ]


def exact_full_budget(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> Fraction:
    """Return ``C_k=B_k(k-1)`` for the exact ``C_M=1`` fixture."""

    return sum(_exact_weights(k, lambda_value), Fraction(0))


def exact_partial_budget(
    k: int,
    q: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> Fraction:
    """Return ``P_k(q)=B_k(k-1-q)`` for the exact fixture."""

    order, lag = _validate_lag(k, q)
    weights = _exact_weights(order, lambda_value)
    return sum(weights[lag:], Fraction(0))


def exact_terminal_distribution(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> list[Fraction]:
    """Return the exact finite terminal-lag probability vector."""

    weights = _exact_weights(k, lambda_value)
    total = sum(weights, Fraction(0))
    return [weight / total for weight in weights]


def exact_profile_proxy(
    k: int,
    q: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> Fraction:
    """Return the finite-radius uniform profile without its ``1+O(1/k)``."""

    order, lag = _validate_lag(k, q)
    x_value = exact_constants(lambda_value)["x"]
    return (
        x_value ** (-lag)
        * Fraction(2 * order - 1, 2 * order - 1 - lag)
        * (1 - x_value ** (-(order - 1 - lag)))
        / (1 - x_value ** (-(order - 1)))
    )


def exact_profile_certificate(
    k: int,
    q: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool]:
    """Check the exact tail identity and the finite uniform proxy."""

    order, lag = _validate_lag(k, q)
    full = exact_full_budget(order, lambda_value)
    partial = exact_partial_budget(order, lag, lambda_value)
    distribution = exact_terminal_distribution(order, lambda_value)
    ratio = partial / full
    tail_mass = sum(distribution[lag:], Fraction(0))
    proxy = exact_profile_proxy(order, lag, lambda_value)
    return {
        "k": order,
        "q": lag,
        "residual_depth": order - 1 - lag,
        "full_budget": full,
        "partial_budget": partial,
        "tail_ratio": ratio,
        "tail_identity": ratio == tail_mass,
        "probability_normalization": sum(distribution, Fraction(0)) == 1,
        "profile_proxy": proxy,
        "tail_over_profile_proxy": ratio / proxy,
        "retained_terminal_mass": 1 - ratio,
        "finite_formula_only": True,
    }


def uniform_profile_error_envelope(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool]:
    """Return the exact worst relative profile error over all terminal lags."""

    order = _validate_k(k)
    rows = [
        exact_profile_certificate(order, lag, lambda_value)
        for lag in range(order - 1)
    ]
    errors = [abs(row["tail_over_profile_proxy"] - 1) for row in rows]
    maximum = max(errors)
    return {
        "k": order,
        "lag_count": order - 1,
        "max_relative_error": maximum,
        "max_error_lag": errors.index(maximum),
        "k_times_max_relative_error": order * maximum,
        "finite_formula_only": True,
    }


def distribution_metrics(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool]:
    """Compare the finite terminal law with the limiting geometric law."""

    order = _validate_k(k)
    x_value = exact_constants(lambda_value)["x"]
    probabilities = exact_terminal_distribution(order, lambda_value)
    geometric = [
        (1 - x_value**-1) * x_value**(-r) for r in range(order - 1)
    ]
    geometric_tail = x_value ** (-(order - 1))
    l1_error = sum(
        (abs(observed - target) for observed, target in zip(probabilities, geometric)),
        geometric_tail,
    )
    mean = sum(
        (Fraction(r) * probability for r, probability in enumerate(probabilities)),
        Fraction(0),
    )
    second = sum(
        (
            Fraction(r * r) * probability
            for r, probability in enumerate(probabilities)
        ),
        Fraction(0),
    )
    variance = second - mean * mean
    mean_target = 1 / (x_value - 1)
    variance_target = x_value / (x_value - 1) ** 2
    return {
        "k": order,
        "support_size": order - 1,
        "probability_sum": sum(probabilities, Fraction(0)),
        "l1_to_geometric": l1_error,
        "total_variation_to_geometric": l1_error / 2,
        "mean": mean,
        "mean_target": mean_target,
        "absolute_mean_error": abs(mean - mean_target),
        "variance": variance,
        "variance_target": variance_target,
        "absolute_variance_error": abs(variance - variance_target),
        "finite_formula_only": True,
    }


def synthetic_profile_diagnostic(
    k: int,
    q: int,
    lambda_text: str = PHYSICAL_LAMBDA_DIAGNOSTIC,
    c_m_text: str = C_M_DIAGNOSTIC,
) -> dict[str, int | str | bool]:
    """Evaluate one high-precision synthetic source-locked profile row."""

    order, lag = _validate_lag(k, q)
    if type(lambda_text) is not str or type(c_m_text) is not str:
        raise TypeError("decimal inputs must be strings")
    with localcontext() as context:
        context.prec = 110
        lam = Decimal(lambda_text)
        c_m = Decimal(c_m_text)
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
        weights = [
            y_value ** (2 * order - 1 - r) / Decimal(2 * order - 1 - r)
            for r in range(order - 1)
        ]
        full = sum(weights, Decimal(0))
        partial = sum(weights[lag:], Decimal(0))
        ratio = partial / full
        finite_y_proxy = (
            y_value ** (-lag)
            * Decimal(2 * order - 1)
            / Decimal(2 * order - 1 - lag)
            * (Decimal(1) - y_value ** (-(order - 1 - lag)))
            / (Decimal(1) - y_value ** (-(order - 1)))
        )
        lag_fraction = Decimal(lag) / Decimal(order)
        source_proxy = (
            x_value ** (-lag)
            * _decimal_power(c_m, lag_fraction)
            * Decimal(2 * order - 1)
            / Decimal(2 * order - 1 - lag)
            * (Decimal(1) - x_value ** (-(order - 1 - lag)))
            / (Decimal(1) - x_value ** (-(order - 1)))
        )
        theta_law = (
            x_value ** (-lag)
            * _decimal_power(c_m, lag_fraction)
            * Decimal(2)
            / (Decimal(2) - lag_fraction)
        )
        residual_depth = order - 1 - lag
        residual_law = (
            Decimal(2)
            * c_m
            * x_value ** (-lag)
            * (Decimal(1) - x_value ** (-residual_depth))
        )
        return {
            "k": order,
            "q": lag,
            "residual_depth": residual_depth,
            "q_over_k": _decimal_text(lag_fraction),
            "x": _decimal_text(x_value),
            "y_k": _decimal_text(y_value),
            "tail_ratio": _decimal_text(ratio),
            "finite_y_proxy": _decimal_text(finite_y_proxy),
            "tail_over_finite_y_proxy": _decimal_text(ratio / finite_y_proxy),
            "source_proxy": _decimal_text(source_proxy),
            "tail_over_source_proxy": _decimal_text(ratio / source_proxy),
            "linear_theta_law": _decimal_text(theta_law),
            "tail_over_linear_theta_law": _decimal_text(ratio / theta_law),
            "fixed_residual_depth_law": _decimal_text(residual_law),
            "tail_over_fixed_residual_depth_law": _decimal_text(
                ratio / residual_law
            ),
            "finite_formula_only": True,
            "synthetic_multiplier_law": True,
        }


def result_status() -> dict[str, object]:
    """Return the strict machine-readable RH-358 theorem ledger."""

    constants = exact_constants()
    exact_rows = [
        exact_profile_certificate(k, lag)
        for k, lag in ((12, 0), (24, 3), (40, 10), (64, 62))
    ]
    envelope_rows = [uniform_profile_error_envelope(k) for k in (8, 16, 32, 64)]
    metric_rows = [distribution_metrics(k) for k in (16, 32, 64, 128)]
    linear_rows = [
        synthetic_profile_diagnostic(k, k // 4) for k in (32, 64, 128, 256)
    ]
    residual_rows = [
        synthetic_profile_diagnostic(k, k - 4) for k in (32, 64, 128, 256)
    ]
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
        "actual_head_roots_rank_or_spectrum_identified": False,
        "x_minus_q_is_uniform_on_full_lag_range": False,
        "fixed_terminal_window_captures_all_mass": False,
        "terminal_lag_q_closes_open_direct_trace_q": False,
        "direct_p_q_or_full_E_off_closed": False,
        "rh241_moving_noisy_envelope_closed": False,
        "rh288_activated": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
    }
    return {
        "status": "RH-358_terminal_lag_geometric_localization",
        "verdict": "GO_SCOPED",
        "constants": _fraction_text(constants),
        "diagnostic_constants": {
            "lambda": PHYSICAL_LAMBDA_DIAGNOSTIC,
            "C_M": C_M_DIAGNOSTIC,
            "not_interval_certificates": True,
        },
        "exact_ledger": {
            "complete_budget": "C_k=B_k(k-1)",
            "partial_budget": "P_k(q)=B_k(k-1-q)",
            "domain": "0<=q<=k-2",
            "lag_probability": "pi_k(r)=[y_k^(2k-1-r)/(2k-1-r)]/C_k",
            "tail_identity": "P_k(q)/C_k=sum_(r=q)^(k-2)_pi_k(r)",
        },
        "uniform_terminal_profile": {
            "finite_radius": "P/C=y_k^(-q)*(2k-1)/(2k-1-q)*(1-y_k^(-(k-1-q)))/(1-y_k^(-(k-1)))*(1+O(1/k))",
            "source_locked": "P/C=x^(-q)*C_M^(q/k)*(2k-1)/(2k-1-q)*(1-x^(-(k-1-q)))/(1-x^(-(k-1)))*(1+o(1))",
            "relative_errors_uniform": True,
            "x_minus_q_alone_uniform": False,
        },
        "lag_regimes": {
            "sublinear": "q=o(k)_implies_P/C=x^(-q)*(1+o(1))",
            "linear": "q/k->theta<1_implies_P/C~[2*C_M^theta/(2-theta)]*x^(-q)",
            "fixed_residual_depth": "q=k-1-ell_fixed_implies_P/C~2*C_M*x^(-q)*(1-x^(-ell))",
        },
        "geometric_localization": {
            "limit": "pi(r)=(1-x^(-1))*x^(-r)",
            "ell1_convergence": True,
            "total_variation_convergence": True,
            "mean_limit": "1/(x-1)",
            "variance_limit": "x/(x-1)^2",
            "fixed_window_retained_mass": "1-x^(-q)",
            "vanishing_truncation_iff": "q->infinity",
        },
        "conditional_actual_head": {
            "hypothesis": "original_same_clock_unnormalized_D_(4k)(R)->0",
            "hypothesis_proved_here": False,
            "uniform_even_tail_profile_inherited": True,
            "uniform_coordinatewise_lag_ratio_inherited": True,
            "lag_total_variation_limit_inherited": True,
            "first_two_lag_moments_inherited": True,
            "moment_transfer_uses_tv_alone": False,
            "root_rank_spectrum_or_determinant_transfer": False,
        },
        "next_candidate": {
            "paper": "RH-359",
            "route": "logarithmic_terminal_window_accuracy_thresholds",
            "status": "read_only_candidate_not_proved_here",
        },
        "exact_profile_rows": _fraction_text(exact_rows),
        "uniform_error_envelope_rows": _fraction_text(envelope_rows),
        "distribution_metric_rows": _fraction_text(metric_rows),
        "linear_diagnostic_rows": linear_rows,
        "fixed_residual_diagnostic_rows": residual_rows,
        "finite_rows_are_formula_reproduction_only": True,
        "gates": gates,
        "false_claims": false_claims,
        "scope": [
            "unconditional_deterministic_graded_counterloop_tail_profile",
            "uniform_full_lag_finite_tail_asymptotic",
            "geometric_ell1_total_variation_and_moment_localization",
            "conditional_actual_head_inheritance_on_unnormalized_D_4k_only",
            "no_root_rank_determinant_or_RH_conclusion",
        ],
    }
