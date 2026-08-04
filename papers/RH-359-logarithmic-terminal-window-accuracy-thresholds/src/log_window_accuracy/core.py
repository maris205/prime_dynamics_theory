"""Exact and high-precision diagnostics for RH-359.

Finite rows reproduce deterministic terminal-tail formulas.  They do not
prove the phase-density theorem and are not observations of an actual noisy
head.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_FLOOR, localcontext
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


def _validate_q(k: int, q: int) -> tuple[int, int]:
    order = _validate_k(k)
    width = _integer(q, "q")
    if not 0 <= width <= order - 2:
        raise ValueError("q must satisfy 0 <= q <= k-2")
    return order, width


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


def exact_full_budget(
    k: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> Fraction:
    """Return the complete deterministic strict upper budget."""

    return sum(_exact_weights(k, lambda_value), Fraction(0))


def exact_tail_ratio(
    k: int,
    q: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> Fraction:
    """Return the exact relative tail ``E_k(q)``."""

    order, width = _validate_q(k, q)
    weights = _exact_weights(order, lambda_value)
    return sum(weights[width:], Fraction(0)) / sum(weights, Fraction(0))


def exact_minimal_width(
    k: int,
    accuracy_power: int,
    x_shift: int = 0,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> int:
    """Return the exact minimum q with E_k(q) <= x^(-c) k^(-a).

    Integer ``accuracy_power`` and ``x_shift`` keep the target rational.
    """

    order = _validate_k(k)
    power = _integer(accuracy_power, "accuracy_power")
    shift = _integer(x_shift, "x_shift")
    if power <= 0:
        raise ValueError("accuracy_power must be positive")
    x_value = exact_constants(lambda_value)["x"]
    target = x_value ** (-shift) / order**power
    for width in range(order - 1):
        if exact_tail_ratio(order, width, lambda_value) <= target:
            return width
    raise RuntimeError("no admissible terminal width met the target")


def exact_window_certificate(
    k: int,
    accuracy_power: int,
    x_shift: int = 0,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, int | Fraction | bool]:
    """Return an exact minimal-width threshold certificate."""

    order = _validate_k(k)
    power = _integer(accuracy_power, "accuracy_power")
    shift = _integer(x_shift, "x_shift")
    if power <= 0:
        raise ValueError("accuracy_power must be positive")
    x_value = exact_constants(lambda_value)["x"]
    target = x_value ** (-shift) / order**power
    width = exact_minimal_width(order, power, shift, lambda_value)
    ratio = exact_tail_ratio(order, width, lambda_value)
    previous = exact_tail_ratio(order, width - 1, lambda_value) if width else None
    return {
        "k": order,
        "accuracy_power": power,
        "x_shift": shift,
        "target": target,
        "minimal_width": width,
        "tail_at_width": ratio,
        "tail_meets_target": ratio <= target,
        "previous_tail": previous,
        "previous_fails_target": previous is None or previous > target,
        "strict_tail_monotonicity": all(
            exact_tail_ratio(order, q + 1, lambda_value)
            < exact_tail_ratio(order, q, lambda_value)
            for q in range(order - 2)
        ),
        "finite_formula_only": True,
    }


def logarithmic_window_diagnostic(
    k: int,
    a_text: str = "2",
    c_text: str = "0.25",
    lambda_text: str = "1.6666666666666666666666666666666666666666666666666666666666667",
) -> dict[str, int | str | bool]:
    """Evaluate the finite phase law with high-precision decimal arithmetic."""

    order = _validate_k(k)
    if any(type(value) is not str for value in (a_text, c_text, lambda_text)):
        raise TypeError("decimal inputs must be strings")
    with localcontext() as context:
        context.prec = 120
        a_value = Decimal(a_text)
        shift = Decimal(c_text)
        lam = Decimal(lambda_text)
        lower = Decimal(28) / Decimal(17)
        upper = Decimal(17) / Decimal(10)
        if not a_value > 0:
            raise ValueError("a must be positive")
        if not lower < lam < upper:
            raise ValueError("lambda must lie in the physical interval")
        radius = Decimal(7) / Decimal(5)
        r_h = Decimal(17) / Decimal(20)
        x_value = radius**2 / (r_h**2 * lam)
        continuous = a_value * Decimal(order).ln() / x_value.ln() + shift
        width = int(continuous.to_integral_value(rounding=ROUND_FLOOR))
        if not 0 <= width <= order - 2:
            raise ValueError("logarithmic width must be admissible")
        phase = continuous - Decimal(width)
        weights = [
            x_value ** (2 * order - 1 - r) / Decimal(2 * order - 1 - r)
            for r in range(order - 1)
        ]
        full = sum(weights, Decimal(0))
        tail = sum(weights[width:], Decimal(0)) / full
        normalized = Decimal(order) ** a_value * tail
        phase_law = _decimal_power(x_value, phase - shift)
        target = _decimal_power(x_value, -shift) * Decimal(order) ** (-a_value)
        exact_minimum = next(
            q
            for q in range(order - 1)
            if sum(weights[q:], Decimal(0)) / full <= target
        )
        correction = Decimal(exact_minimum) - continuous
        return {
            "k": order,
            "a": _decimal_text(a_value),
            "c": _decimal_text(shift),
            "x": _decimal_text(x_value),
            "continuous_width": _decimal_text(continuous),
            "floor_width": width,
            "phase": _decimal_text(phase),
            "tail_ratio": _decimal_text(tail),
            "normalized_tail": _decimal_text(normalized),
            "phase_law": _decimal_text(phase_law),
            "normalized_over_phase_law": _decimal_text(normalized / phase_law),
            "target": _decimal_text(target),
            "minimal_width": exact_minimum,
            "minimal_width_correction": _decimal_text(correction),
            "correction_in_coarse_interval": Decimal(-1) < correction < Decimal(2),
            "finite_formula_only": True,
        }


def phase_cover_diagnostic(
    start_k: int,
    stop_k: int,
    bins: int = 10,
    a_text: str = "2",
    c_text: str = "0.25",
) -> dict[str, object]:
    """Report finite phase-bin coverage without treating it as a proof."""

    start = _validate_k(start_k)
    stop = _validate_k(stop_k)
    count = _integer(bins, "bins")
    if stop <= start:
        raise ValueError("stop_k must exceed start_k")
    if count < 2:
        raise ValueError("bins must be at least two")
    if type(a_text) is not str or type(c_text) is not str:
        raise TypeError("phase inputs must be strings")
    with localcontext() as context:
        context.prec = 90
        a_value = Decimal(a_text)
        shift = Decimal(c_text)
        if not a_value > 0:
            raise ValueError("a must be positive")
        x_value = Decimal(2352) / Decimal(1445)
        occupied: set[int] = set()
        phase_min = Decimal(1)
        phase_max = Decimal(0)
        for order in range(start, stop + 1):
            value = a_value * Decimal(order).ln() / x_value.ln() + shift
            phase = value - value.to_integral_value(rounding=ROUND_FLOOR)
            occupied.add(min(count - 1, int(phase * count)))
            phase_min = min(phase_min, phase)
            phase_max = max(phase_max, phase)
        return {
            "start_k": start,
            "stop_k": stop,
            "bins": count,
            "occupied_bins": sorted(occupied),
            "occupied_count": len(occupied),
            "phase_min": _decimal_text(phase_min),
            "phase_max": _decimal_text(phase_max),
            "finite_coverage_is_not_density_proof": True,
        }


def result_status() -> dict[str, object]:
    """Return the strict machine-readable RH-359 theorem ledger."""

    constants = exact_constants()
    exact_rows = [
        exact_window_certificate(k, 2, 0) for k in (16, 32, 64, 128)
    ]
    phase_rows = [
        logarithmic_window_diagnostic(k) for k in (32, 64, 128, 256)
    ]
    cover_rows = [
        phase_cover_diagnostic(10, stop, 10) for stop in (100, 1000, 10000)
    ]
    gates = {
        "A_canonical_intrinsic_determinant": False,
        "B_time_oriented_unitary_completion": False,
        "C_self_adjoint_generator_T_log_T": False,
        "D_von_mangoldt_prime_power_trace": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "finite_phase_rows_prove_density": False,
        "floor_phase_has_unique_constant": False,
        "minimal_width_has_universal_exact_integer_formula": False,
        "counterloop_is_actual_noisy_head": False,
        "D_4k_transport_proved": False,
        "actual_roots_rank_or_spectrum_identified": False,
        "terminal_window_q_closes_open_direct_trace_q": False,
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
        "status": "RH-359_logarithmic_terminal_window_accuracy_thresholds",
        "verdict": "GO_SCOPED",
        "constants": _fraction_text(constants),
        "tail_ledger": {
            "relative_error": "E_k(q)=P_k(q)/C_k",
            "domain": "0<=q<=k-2",
            "log_window_uniformity": "sup_(q<=A*log(k))|x^q*E_k(q)-1|->0",
            "finite_tail_factor_deleted_on_full_range": False,
        },
        "polynomial_phase": {
            "continuous_width": "t_k=a*log(k)/log(x)+c",
            "integer_width": "q_k=floor(t_k)",
            "phase": "theta_k={t_k}",
            "law": "k^a*E_k(q_k)=x^(theta_k-c)*(1+o(1))",
            "phase_limit_set": "[0,1]",
            "normalized_error_limit_set": "[x^(-c),x^(1-c)]",
            "unique_constant": False,
        },
        "minimal_window": {
            "definition": "Q_k=min{q:E_k(q)<=x^(-c)*k^(-a)}",
            "first_order": "Q_k=a*log(k)/log(x)+c+O(1)",
            "correction_limit_set": "[0,1]",
            "generic_phase_selection": "Q_k=ceil(t_k)_away_from_phase_endpoints",
            "universal_exact_integer_selection": False,
        },
        "accuracy_exponents": {
            "law": "log(E_k(q_k))/log(k)->-a_if_q_k*log(x)/log(k)->a",
            "superlog_sublinear_is_superpolynomial": True,
            "vanishing_error_iff_q_to_infinity": True,
        },
        "conditional_actual_head": {
            "hypothesis": "original_same_clock_unnormalized_D_(4k)(R)->0",
            "hypothesis_proved_here": False,
            "phase_exponent_and_minimal_width_inherited": True,
            "root_rank_spectrum_or_determinant_transfer": False,
        },
        "next_candidate": {
            "paper": "RH-360",
            "route": "terminal_lag_exponential_tilt_phase_transition",
            "status": "read_only_candidate_not_proved_here",
        },
        "exact_minimal_width_rows": _fraction_text(exact_rows),
        "phase_diagnostic_rows": phase_rows,
        "finite_phase_cover_rows": cover_rows,
        "finite_rows_are_formula_reproduction_only": True,
        "gates": gates,
        "false_claims": false_claims,
        "scope": [
            "unconditional_deterministic_logarithmic_accuracy_thresholds",
            "complete_floor_phase_and_minimal_width_limit_sets",
            "conditional_actual_head_inheritance_on_unnormalized_D_4k_only",
            "no_root_rank_determinant_or_RH_conclusion",
        ],
    }
