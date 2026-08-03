"""Exact and high-precision diagnostics for RH-357.

Finite rows reproduce the deterministic graded-counterloop formulas.  They
are not observations of an actual noisy head and do not prove the open
same-clock hypothesis ``D_(4k)(R) -> 0``.
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


def _validate_depth(k: int, depth: int) -> tuple[int, int]:
    order = _integer(k, "k")
    level = _integer(depth, "depth")
    if order < 2:
        raise ValueError("k must be at least two")
    if not 1 <= level <= order - 1:
        raise ValueError("depth must satisfy 1 <= L <= k-1")
    return order, level


def _fractional_part(value: Fraction) -> Fraction:
    return value - value.numerator // value.denominator


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


def exact_alias_budget(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> Fraction:
    """Return ``A_k`` for the exact ``C_M=1`` rational fixture."""

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
    """Return ``B_k(L)`` for the exact rational fixture."""

    order, level = _validate_depth(k, depth)
    x_value = exact_constants(lambda_value)["x"]
    return sum(
        (x_value ** (order + j) / (order + j) for j in range(1, level + 1)),
        Fraction(0),
    )


def exact_endpoint_certificate(
    k: int,
    depth: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool]:
    """Compare the exact budgets with the uniform endpoint proxies."""

    order, level = _validate_depth(k, depth)
    x_value = exact_constants(lambda_value)["x"]
    alias = exact_alias_budget(order, lambda_value)
    post = exact_post_budget(order, level, lambda_value)
    endpoint_proxy = (
        x_value ** (order + 1)
        * (x_value**level - 1)
        / ((order + level) * (x_value - 1))
    )
    ratio = post / alias
    ratio_proxy = (
        x_value * (x_value**level - 1)
        / ((order + level) * (x_value - 1))
    )
    exact_ratio_sum = Fraction(order, order - 1) * sum(
        (x_value**j / (order + j) for j in range(1, level + 1)),
        Fraction(0),
    )
    return {
        "k": order,
        "L": level,
        "alias_budget": alias,
        "post_budget": post,
        "ratio": ratio,
        "ratio_identity": ratio == exact_ratio_sum,
        "endpoint_proxy": endpoint_proxy,
        "post_over_endpoint_proxy": post / endpoint_proxy,
        "ratio_proxy": ratio_proxy,
        "ratio_over_proxy": ratio / ratio_proxy,
        "bounded_depth_factor": 1 - x_value ** (-level),
        "finite_formula_only": True,
    }


def endpoint_error_envelope(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool]:
    """Return the exact worst relative endpoint error over ``1<=L<=k-1``."""

    order = _integer(k, "k")
    if order < 2:
        raise ValueError("k must be at least two")
    rows = [
        exact_endpoint_certificate(order, level, lambda_value)
        for level in range(1, order)
    ]
    post_errors = [abs(row["post_over_endpoint_proxy"] - 1) for row in rows]
    ratio_errors = [abs(row["ratio_over_proxy"] - 1) for row in rows]
    post_max = max(post_errors)
    ratio_max = max(ratio_errors)
    return {
        "k": order,
        "depth_count": order - 1,
        "post_max_relative_error": post_max,
        "post_max_depth": post_errors.index(post_max) + 1,
        "ratio_max_relative_error": ratio_max,
        "ratio_max_depth": ratio_errors.index(ratio_max) + 1,
        "k_times_post_max_relative_error": order * post_max,
        "finite_formula_only": True,
    }


def rational_phase_orbit(
    alpha_numerator: int,
    alpha_denominator: int,
    c_numerator: int = 0,
    c_denominator: int = 1,
) -> dict[str, object]:
    """Return the exact floor-phase orbit for rational ``alpha``."""

    values = [alpha_numerator, alpha_denominator, c_numerator, c_denominator]
    if any(type(value) is not int for value in values):
        raise TypeError("rational phase inputs must be integers")
    if alpha_denominator == 0 or c_denominator == 0:
        raise ValueError("denominators must be nonzero")
    alpha = Fraction(alpha_numerator, alpha_denominator)
    shift = Fraction(c_numerator, c_denominator)
    if not 0 < alpha <= 1:
        raise ValueError("alpha must satisfy 0 < alpha <= 1")
    phases = sorted({_fractional_part(alpha * residue + shift) for residue in range(alpha.denominator)})
    return {
        "alpha": alpha,
        "c": shift,
        "period": alpha.denominator,
        "phases": phases,
        "phase_count": len(phases),
        "single_phase": len(phases) == 1,
        "exact_rational_orbit": True,
    }


def linear_depth_diagnostic(
    k: int,
    alpha_text: str = "0.5",
    c_text: str = "-0.25",
    lambda_text: str = PHYSICAL_LAMBDA_DIAGNOSTIC,
    c_m_text: str = C_M_DIAGNOSTIC,
) -> dict[str, int | str | bool]:
    """Evaluate a synthetic finite-radius linear-depth row."""

    order = _integer(k, "k")
    if order < 3:
        raise ValueError("k must be at least three")
    texts = (alpha_text, c_text, lambda_text, c_m_text)
    if any(type(value) is not str for value in texts):
        raise TypeError("decimal inputs must be strings")
    with localcontext() as context:
        context.prec = 100
        alpha = Decimal(alpha_text)
        shift = Decimal(c_text)
        lam = Decimal(lambda_text)
        c_m = Decimal(c_m_text)
        lower = Decimal(28) / Decimal(17)
        upper = Decimal(17) / Decimal(10)
        if not Decimal(0) < alpha <= Decimal(1):
            raise ValueError("alpha must satisfy 0 < alpha <= 1")
        if not lower < lam < upper:
            raise ValueError("lambda diagnostic must lie in the physical interval")
        if not c_m > 0:
            raise ValueError("C_M diagnostic must be positive")
        radius = Decimal(7) / Decimal(5)
        r_h = Decimal(17) / Decimal(20)
        x_value = radius**2 / (r_h**2 * lam)
        y_value = x_value * (-c_m.ln() / Decimal(order)).exp()
        floor_argument = alpha * Decimal(order) + shift
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
        level_fraction = Decimal(level) / Decimal(order)
        endpoint_proxy = (
            x_value ** (order + level + 1)
            * (Decimal(1) - x_value ** (-level))
            / (
                _decimal_power(c_m, Decimal(1) + level_fraction)
                * Decimal(order + level)
                * (x_value - Decimal(1))
            )
        )
        ratio_proxy = (
            x_value ** (level + 1)
            * (Decimal(1) - x_value ** (-level))
            / (
                _decimal_power(c_m, level_fraction)
                * Decimal(order + level)
                * (x_value - Decimal(1))
            )
        )
        phase_safe_post = (
            Decimal(order)
            * post
            / _decimal_power(
                x_value, (Decimal(1) + alpha) * Decimal(order)
            )
        )
        phase_safe_ratio = (
            Decimal(order)
            * ratio
            / _decimal_power(x_value, alpha * Decimal(order))
        )
        phase_power = _decimal_power(x_value, shift + Decimal(1) - phase)
        post_phase_law = phase_power / (
            _decimal_power(c_m, Decimal(1) + alpha)
            * (Decimal(1) + alpha)
            * (x_value - Decimal(1))
        )
        ratio_phase_law = phase_power / (
            _decimal_power(c_m, alpha)
            * (Decimal(1) + alpha)
            * (x_value - Decimal(1))
        )
        return {
            "k": order,
            "L": level,
            "alpha": _decimal_text(alpha),
            "c": _decimal_text(shift),
            "phase": _decimal_text(phase),
            "x": _decimal_text(x_value),
            "y_k": _decimal_text(y_value),
            "post_budget": _decimal_text(post),
            "post_endpoint_proxy": _decimal_text(endpoint_proxy),
            "post_over_endpoint_proxy": _decimal_text(post / endpoint_proxy),
            "ratio": _decimal_text(ratio),
            "ratio_proxy": _decimal_text(ratio_proxy),
            "ratio_over_proxy": _decimal_text(ratio / ratio_proxy),
            "phase_safe_post": _decimal_text(phase_safe_post),
            "post_phase_law": _decimal_text(post_phase_law),
            "phase_safe_post_over_law": _decimal_text(
                phase_safe_post / post_phase_law
            ),
            "phase_safe_ratio": _decimal_text(phase_safe_ratio),
            "ratio_phase_law": _decimal_text(ratio_phase_law),
            "phase_safe_ratio_over_law": _decimal_text(
                phase_safe_ratio / ratio_phase_law
            ),
            "finite_formula_only": True,
            "synthetic_multiplier_law": True,
        }


def result_status() -> dict[str, object]:
    """Return the strict machine-readable RH-357 theorem ledger."""

    constants = exact_constants()
    exact_rows = [
        exact_endpoint_certificate(k, depth)
        for k, depth in ((12, 1), (24, 7), (48, 23), (64, 63))
    ]
    envelope_rows = [endpoint_error_envelope(k) for k in (8, 16, 32, 64)]
    diagnostic_rows = [
        linear_depth_diagnostic(k, "0.5", "-0.25")
        for k in (32, 64, 128, 256)
    ]
    rational_orbits = [
        rational_phase_orbit(1, 2, 1, 7),
        rational_phase_orbit(2, 3, -1, 5),
        rational_phase_orbit(1, 1, -1, 2),
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
        "actual_head_roots_or_rank_identified": False,
        "bounded_L_factor_deleted": False,
        "alpha_zero_terminal_simplification_without_L_growth": False,
        "rational_and_irrational_floor_phases_collapsed": False,
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
        "status": "RH-357_uniform_linear_depth_upper_counterloop_profile",
        "verdict": "GO_SCOPED",
        "constants": _fraction_text(constants),
        "diagnostic_constants": {
            "lambda": PHYSICAL_LAMBDA_DIAGNOSTIC,
            "C_M": C_M_DIAGNOSTIC,
            "not_interval_certificates": True,
        },
        "exact_ledger": {
            "alias": "A_k=(1-1/k)*y_k^k",
            "post_band": "B_k(L)=sum_(j=1)^L_y_k^(k+j)/(k+j)",
            "domain": "1<=L<=k-1",
        },
        "uniform_endpoint_theorem": {
            "finite_radius": "B=y_k^(k+L+1)*(1-y_k^(-L))/((k+L)*(y_k-1))*(1+O(1/k))_uniformly",
            "source_locked": "B=x^(k+L+1)*(1-x^(-L))/(C_M^(1+L/k)*(k+L)*(x-1))*(1+o(1))_uniformly",
            "ratio": "B/A=x^(L+1)*(1-x^(-L))/(C_M^(L/k)*(k+L)*(x-1))*(1+o(1))_uniformly",
            "relative_errors_uniform": True,
        },
        "linear_depth": {
            "domain": "L/k->alpha_in_(0,1]",
            "post": "B~x^(k+L+1)/(C_M^(1+alpha)*k*(1+alpha)*(x-1))",
            "ratio": "B/A~x^(L+1)/(C_M^alpha*k*(1+alpha)*(x-1))",
            "post_kth_root": "x^(1+alpha)",
            "ratio_kth_root": "x^alpha",
            "physical_post_log_rate": "(1+alpha)*log(x)/(2*log(lambda))",
            "physical_ratio_log_rate": "alpha*log(x)/(2*log(lambda))",
        },
        "integer_phase": {
            "depth": "L=floor(alpha*k+c)",
            "phase": "theta_k={alpha*k+c}",
            "post_normalization": "k*x^(-(1+alpha)k)*B=x^(c+1-theta_k)/(C_M^(1+alpha)*(1+alpha)*(x-1))*(1+o(1))",
            "ratio_normalization": "k*x^(-alpha*k)*B/A=x^(c+1-theta_k)/(C_M^alpha*(1+alpha)*(x-1))*(1+o(1))",
            "rational_alpha": "finite_periodic_phase_orbit",
            "irrational_alpha": "phase_limit_set_[0,1]_and_interval_of_normalized_cluster_values",
            "universal_single_limit": False,
        },
        "boundary_stitching": {
            "bounded_L": "retain_1-x^(-L)",
            "alpha_zero": "delete_1-x^(-L)_only_if_L->infinity_and_L=o(k)",
            "alpha_one": "L=k-1_recovers_RH-355_complete_strict_upper_band",
        },
        "conditional_actual_head": {
            "hypothesis": "original_same_clock_unnormalized_D_(4k)(R)->0",
            "hypothesis_proved_here": False,
            "uniform_budget_transfer": True,
            "odd_upper_band_budget_tends_to_zero": True,
            "root_or_rank_transfer": False,
        },
        "next_candidate": {
            "paper": "RH-358",
            "route": "terminal_lag_geometric_localization",
            "status": "read_only_candidate_not_proved_here",
        },
        "exact_fixture_rows": _fraction_text(exact_rows),
        "uniform_error_envelope_rows": _fraction_text(envelope_rows),
        "linear_diagnostic_rows": diagnostic_rows,
        "rational_phase_orbits": _fraction_text(rational_orbits),
        "finite_rows_are_formula_reproduction_only": True,
        "gates": gates,
        "false_claims": false_claims,
        "scope": [
            "unconditional_deterministic_graded_counterloop_profile",
            "uniform_all_depth_endpoint_asymptotic",
            "linear_depth_multiplier_constant_and_denominator_profile",
            "rational_irrational_floor_phase_retained",
            "actual_head_transfer_conditional_on_unnormalized_D_4k_only",
            "no_RH_conclusion",
        ],
    }
