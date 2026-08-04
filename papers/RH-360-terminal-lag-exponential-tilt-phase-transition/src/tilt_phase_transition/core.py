"""Exact and high-precision diagnostics for RH-360.

The rows reproduce finite deterministic budget transforms.  They are not
observations of an actual noisy head and do not prove any limiting theorem.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction


R_H = Fraction(17, 20)
R = Fraction(7, 5)
LAMBDA_LOWER = Fraction(28, 17)
LAMBDA_UPPER = Fraction(17, 10)
FIXTURE_LAMBDA = Fraction(5, 3)


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


def _as_decimal(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def exact_constants(
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, Fraction | bool]:
    """Return exact rational fixture constants."""

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


def exact_terminal_distribution(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> list[Fraction]:
    """Return the exact fixture terminal-lag distribution."""

    weights = _exact_weights(k, lambda_value)
    total = sum(weights, Fraction(0))
    return [weight / total for weight in weights]


def exact_generating_function(
    k: int,
    z: int | Fraction,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> Fraction:
    """Return ``G_k(z)`` exactly for a rational nonnegative tilt."""

    order = _validate_k(k)
    tilt = _fraction(z, "z")
    if tilt < 0:
        raise ValueError("z must be nonnegative")
    probabilities = exact_terminal_distribution(order, lambda_value)
    return sum(
        (tilt**r * probability for r, probability in enumerate(probabilities)),
        Fraction(0),
    )


def transform_certificate(
    k: int,
    z_ratio: int | Fraction,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool | str]:
    """Return an exact transform row for ``z=z_ratio*x``."""

    order = _validate_k(k)
    ratio = _fraction(z_ratio, "z_ratio")
    if ratio < 0:
        raise ValueError("z_ratio must be nonnegative")
    x_value = exact_constants(lambda_value)["x"]
    tilt = ratio * x_value
    observed = exact_generating_function(order, tilt, lambda_value)
    if ratio < 1:
        target = (1 - x_value**-1) / (1 - ratio)
        regime = "subcritical"
        scaled = observed / target
    elif ratio == 1:
        target = None
        regime = "critical"
        scaled = observed / order
    else:
        target = (
            2
            * (1 - x_value**-1)
            / (1 - ratio**-1)
            * ratio ** (order - 2)
        )
        regime = "supercritical"
        scaled = observed / target
    return {
        "k": order,
        "z_ratio": ratio,
        "z": tilt,
        "regime": regime,
        "generating_function": observed,
        "asymptotic_target": target,
        "observed_over_target_or_k": scaled,
        "finite_formula_only": True,
    }


def _l1_with_geometric(
    probabilities: list[Fraction],
    ratio: Fraction,
) -> Fraction:
    target = [(1 - ratio) * ratio**r for r in range(len(probabilities))]
    tail = ratio ** len(probabilities)
    return sum(
        (abs(observed - expected) for observed, expected in zip(probabilities, target)),
        tail,
    )


def subcritical_metrics(
    k: int,
    z_ratio: int | Fraction = Fraction(1, 2),
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool]:
    """Compare the subcritical tilted law with geometric ratio ``z/x``."""

    order = _validate_k(k)
    ratio = _fraction(z_ratio, "z_ratio")
    if not 0 <= ratio < 1:
        raise ValueError("subcritical z_ratio must satisfy 0 <= z_ratio < 1")
    x_value = exact_constants(lambda_value)["x"]
    base = exact_terminal_distribution(order, lambda_value)
    unnormalized = [(ratio * x_value) ** r * p for r, p in enumerate(base)]
    total = sum(unnormalized, Fraction(0))
    tilted = [weight / total for weight in unnormalized]
    return {
        "k": order,
        "z_ratio": ratio,
        "probability_sum": sum(tilted, Fraction(0)),
        "l1_to_geometric": _l1_with_geometric(tilted, ratio),
        "total_variation_to_geometric": _l1_with_geometric(tilted, ratio) / 2,
        "finite_formula_only": True,
    }


def supercritical_metrics(
    k: int,
    z_ratio: int | Fraction = 2,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool]:
    """Compare opposite-endpoint distance with geometric ratio ``x/z``."""

    order = _validate_k(k)
    ratio = _fraction(z_ratio, "z_ratio")
    if not ratio > 1:
        raise ValueError("supercritical z_ratio must exceed one")
    x_value = exact_constants(lambda_value)["x"]
    base = exact_terminal_distribution(order, lambda_value)
    unnormalized = [(ratio * x_value) ** r * p for r, p in enumerate(base)]
    total = sum(unnormalized, Fraction(0))
    tilted_r = [weight / total for weight in unnormalized]
    tilted_ell = list(reversed(tilted_r))
    target_ratio = 1 / ratio
    return {
        "k": order,
        "z_ratio": ratio,
        "ell_probability_sum": sum(tilted_ell, Fraction(0)),
        "l1_to_geometric": _l1_with_geometric(tilted_ell, target_ratio),
        "total_variation_to_geometric": _l1_with_geometric(
            tilted_ell, target_ratio
        )
        / 2,
        "finite_formula_only": True,
    }


def critical_metrics(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | str | bool]:
    """Check the ``C_M=1, tau=0`` critical transform and scaled mean."""

    order = _validate_k(k)
    x_value = exact_constants(lambda_value)["x"]
    observed = exact_generating_function(order, x_value, lambda_value)
    base = exact_terminal_distribution(order, lambda_value)
    unnormalized = [x_value**r * p for r, p in enumerate(base)]
    total = sum(unnormalized, Fraction(0))
    tilted = [weight / total for weight in unnormalized]
    scaled_mean = sum(
        (Fraction(r, order) * p for r, p in enumerate(tilted)), Fraction(0)
    )
    with localcontext() as context:
        context.prec = 100
        x_decimal = _as_decimal(x_value)
        log_two = Decimal(2).ln()
        transform_target = Decimal(2) * (Decimal(1) - Decimal(1) / x_decimal) * log_two
        mean_target = Decimal(2) - Decimal(1) / log_two
        observed_scaled = _as_decimal(observed) / Decimal(order)
        mean_decimal = _as_decimal(scaled_mean)
        return {
            "k": order,
            "critical_z": _decimal_text(x_decimal),
            "generating_over_k": _decimal_text(observed_scaled),
            "transform_target": _decimal_text(transform_target),
            "transform_ratio": _decimal_text(observed_scaled / transform_target),
            "scaled_lag_mean": _decimal_text(mean_decimal),
            "scaled_lag_mean_target": _decimal_text(mean_target),
            "absolute_mean_error": _decimal_text(abs(mean_decimal - mean_target)),
            "finite_formula_only": True,
        }


def result_status() -> dict[str, object]:
    """Return the strict machine-readable RH-360 theorem ledger."""

    constants = exact_constants()
    sub_transform_rows = [
        transform_certificate(k, Fraction(1, 2)) for k in (16, 32, 64, 128)
    ]
    critical_rows = [critical_metrics(k) for k in (16, 32, 64, 128)]
    super_transform_rows = [
        transform_certificate(k, 2) for k in (16, 32, 64, 128)
    ]
    sub_tilt_rows = [subcritical_metrics(k) for k in (16, 32, 64, 128)]
    super_tilt_rows = [supercritical_metrics(k) for k in (16, 32, 64, 128)]
    gates = {
        "A_canonical_intrinsic_determinant": False,
        "B_time_oriented_unitary_completion": False,
        "C_self_adjoint_generator_T_log_T": False,
        "D_von_mangoldt_prime_power_trace": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "tv_limit_controls_all_exponential_tilts": False,
        "critical_constant_forgets_C_M": False,
        "tilted_budget_is_eigenvalue_distribution": False,
        "tilted_budget_is_root_counting_measure": False,
        "tilted_budget_is_noisy_stochastic_law": False,
        "counterloop_is_actual_noisy_head": False,
        "D_4k_transport_proved": False,
        "actual_roots_rank_or_spectrum_identified": False,
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
        "status": "RH-360_terminal_lag_exponential_tilt_phase_transition",
        "verdict": "GO_SCOPED",
        "constants": _fraction_text(constants),
        "generating_function": {
            "definition": "G_k(z)=sum_(r=0)^(k-2)z^r*pi_k(r)",
            "subcritical": "G_k(z)->(1-x^(-1))/(1-z/x)_for_0<=z<x",
            "critical": "G_k(x*exp(tau/k))/k->2*(1-x^(-1))*integral_0^1 exp((tau+log(C_M))*s)/(2-s) ds",
            "supercritical": "G_k(z)~2*C_M*(1-x^(-1))*(z/x)^(k-2)/(1-x/z)_for_z>x",
            "free_energy": "log(G_k(z))/k->max(0,log(z/x))",
        },
        "tilted_phase_diagram": {
            "subcritical": "terminal_lag_geometric_ratio_z/x",
            "critical": "scaled_lag_density_proportional_to_exp((tau+log(C_M))*s)/(2-s)",
            "supercritical": "opposite_endpoint_distance_geometric_ratio_x/z",
            "spectral_probability_interpretation": False,
        },
        "conditional_actual_head": {
            "hypothesis": "original_same_clock_unnormalized_D_(4k)(R)->0",
            "hypothesis_proved_here": False,
            "all_nonnegative_tilt_sequences_inherited": True,
            "root_rank_spectrum_or_determinant_transfer": False,
        },
        "next_paper": {
            "paper": "RH-361",
            "route": "ten_layer_signed_completion_and_upper_counterloop_review",
            "status": "review_trigger_not_proved_here",
        },
        "subcritical_transform_rows": _fraction_text(sub_transform_rows),
        "critical_rows": critical_rows,
        "supercritical_transform_rows": _fraction_text(super_transform_rows),
        "subcritical_tilt_rows": _fraction_text(sub_tilt_rows),
        "supercritical_tilt_rows": _fraction_text(super_tilt_rows),
        "finite_rows_are_formula_reproduction_only": True,
        "gates": gates,
        "false_claims": false_claims,
        "scope": [
            "unconditional_deterministic_terminal_lag_transform_phase_transition",
            "three_tilted_budget_distribution_limits",
            "conditional_actual_head_inheritance_on_unnormalized_D_4k_only",
            "no_root_rank_determinant_or_RH_conclusion",
        ],
    }
