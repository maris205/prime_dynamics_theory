"""Exact-arithmetic audit for the RH-329 isolated graded exchange model.

Every verdict is obtained with :class:`fractions.Fraction`.  Floating-point
values are presentation-only and never decide reachability or failure.
"""

from __future__ import annotations

import math
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from functools import lru_cache


HARDY_RADIUS = Fraction(17, 20)
TARGET_RADIUS = Fraction(7, 5)
EXPANSION = Fraction("1.6785735104283224")
MULTIPLIER_CONSTANT = Fraction("1.9463429052009678")
PARITY_CONSTANT = Fraction("0.105258535936908")
CLEARANCE_CONSTANT = Fraction("0.4608051492")
MODEL_CONTRAST = Fraction(4, 5)
REFERENCE_CONTRAST = Fraction(3, 5)
BOUNDARY_CONTRAST = Fraction(1, 2)
PHASE = Fraction(0, 1)


def _positive_integer(value: int, *, name: str = "k") -> int:
    if isinstance(value, bool) or int(value) != value or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return int(value)


def _unit_fraction(value: Fraction | int | str, *, name: str) -> Fraction:
    value = Fraction(value)
    if not Fraction(0) <= value <= Fraction(1):
        raise ValueError(f"{name} must lie in [0, 1]")
    return value


def fraction_string(value: Fraction) -> str:
    """Return a canonical exact rational string."""

    value = Fraction(value)
    return f"{value.numerator}/{value.denominator}"


def outward_decimal_interval(value: Fraction, digits: int = 18) -> list[str]:
    """Return directed decimal endpoints enclosing an exact fraction."""

    value = Fraction(value)
    digits = _positive_integer(digits, name="digits")
    numerator = Decimal(value.numerator)
    denominator = Decimal(value.denominator)
    with localcontext() as ctx:
        ctx.prec = digits
        ctx.rounding = ROUND_FLOOR
        lower = numerator / denominator
    with localcontext() as ctx:
        ctx.prec = digits
        ctx.rounding = ROUND_CEILING
        upper = numerator / denominator
    return [format(lower, "e"), format(upper, "e")]


def exchange_matrix(
    contrast: Fraction | int | str,
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    """Return K_c = Pi_s + c Pi_a with exact rational entries."""

    contrast = _unit_fraction(contrast, name="contrast")
    return (
        ((1 + contrast) / 2, (1 - contrast) / 2),
        ((1 - contrast) / 2, (1 + contrast) / 2),
    )


def matrix_multiply(
    left: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
    right: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    """Multiply two exact 2 by 2 matrices."""

    return tuple(
        tuple(sum(left[i][m] * right[m][j] for m in range(2)) for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def matrix_power(
    matrix: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
    order: int,
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    """Raise an exact 2 by 2 matrix to a nonnegative integer power."""

    if isinstance(order, bool) or int(order) != order or order < 0:
        raise ValueError("order must be a nonnegative integer")
    order = int(order)
    result = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    base = matrix
    while order:
        if order & 1:
            result = matrix_multiply(result, base)
        base = matrix_multiply(base, base)
        order //= 2
    return result


def matrix_trace(
    matrix: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
) -> Fraction:
    """Return the exact matrix trace."""

    return matrix[0][0] + matrix[1][1]


def exchange_trace_power(contrast: Fraction | int | str, order: int) -> Fraction:
    """Return Tr K_c^order = 1 + c^order."""

    contrast = _unit_fraction(contrast, name="contrast")
    order = _positive_integer(order, name="order")
    return 1 + contrast**order


def beta_squared() -> Fraction:
    """Return beta^2 = 1/(r_H^2 Lambda), an exact rational."""

    return 1 / (HARDY_RADIUS**2 * EXPANSION)


def alias_coefficient(k: int) -> Fraction:
    """Return a_k = (2k-2)/C_M + 2."""

    k = _positive_integer(k)
    return Fraction(2 * k - 2, 1) / MULTIPLIER_CONSTANT + 2


def alias_packet(k: int) -> Fraction:
    """Return the exact counterloop block trace A_k = a_k beta^(2k)."""

    k = _positive_integer(k)
    return _alias_packet_cached(k)


@lru_cache(maxsize=None)
def _alias_packet_cached(k: int) -> Fraction:
    return alias_coefficient(k) * beta_squared() ** k


def noise_scale(k: int) -> Fraction:
    """Return the fixed-phase isolated clock sigma_k = Lambda^(-2k)."""

    k = _positive_integer(k)
    return EXPANSION ** (-2 * k)


def parity_gap(k: int) -> Fraction:
    """Return delta_k = C_* Lambda^(-k) exactly."""

    k = _positive_integer(k)
    return PARITY_CONSTANT * EXPANSION ** (-k)


def parity_packet(k: int) -> Fraction:
    """Return r_H^(-2k)[1-(1-delta_k)^(2k)] exactly."""

    k = _positive_integer(k)
    return _parity_packet_cached(k)


@lru_cache(maxsize=None)
def _parity_packet_cached(k: int) -> Fraction:
    delta = parity_gap(k)
    return HARDY_RADIUS ** (-2 * k) * (1 - (1 - delta) ** (2 * k))


def boundary_packet(k: int) -> Fraction:
    """Return the identical-block boundary observation, exactly zero."""

    _positive_integer(k)
    return BOUNDARY_CONTRAST ** (2 * k) - BOUNDARY_CONTRAST ** (2 * k)


def shell_packet(k: int) -> Fraction:
    """Return Tr(Q_c^(2k)-Q_c0^(2k)) with scale L_k=A_k."""

    k = _positive_integer(k)
    return alias_packet(k) * (
        MODEL_CONTRAST ** (2 * k) - REFERENCE_CONTRAST ** (2 * k)
    )


def far_remainder(k: int) -> Fraction:
    """The isolated model has no omitted block."""

    _positive_integer(k)
    return Fraction(0)


def observation_error(k: int) -> Fraction:
    """The exchange representation is the exact model trace difference."""

    _positive_integer(k)
    return Fraction(0)


def target(k: int) -> Fraction:
    """Return H_k = k R^(-2k) exactly."""

    k = _positive_integer(k)
    return k * TARGET_RADIUS ** (-2 * k)


def demand(k: int) -> Fraction:
    """Return D_k = A_k-P_k-B_k."""

    k = _positive_integer(k)
    return alias_packet(k) - parity_packet(k) - boundary_packet(k)


def required_power(k: int) -> Fraction:
    """Return y_k = c0^(2k)+D_k/L_k with L_k=A_k."""

    k = _positive_integer(k)
    return REFERENCE_CONTRAST ** (2 * k) + demand(k) / alias_packet(k)


def power_mismatch(k: int) -> Fraction:
    """Return c_iso^(2k)-y_k exactly."""

    k = _positive_integer(k)
    return MODEL_CONTRAST ** (2 * k) - required_power(k)


def residual(k: int) -> Fraction:
    """Return e_k=B_k+S_k+R_k+P_k-A_k exactly."""

    k = _positive_integer(k)
    return (
        boundary_packet(k)
        + shell_packet(k)
        + far_remainder(k)
        + parity_packet(k)
        - alias_packet(k)
    )


def parity_to_alias(k: int) -> Fraction:
    """Return the exact ratio P_k/A_k."""

    k = _positive_integer(k)
    return parity_packet(k) / alias_packet(k)


def alias_to_target(k: int) -> Fraction:
    """Return A_k/H_k exactly."""

    k = _positive_integer(k)
    return alias_packet(k) / target(k)


def residual_to_target(k: int) -> Fraction:
    """Return e_k/H_k exactly."""

    k = _positive_integer(k)
    return residual(k) / target(k)


def reachability_screen_zero(k: int) -> bool:
    """Return whether y_k lies in [0,1], decided exactly."""

    y = required_power(k)
    return Fraction(0) <= y <= Fraction(1)


def common_duhamel_weight(k: int) -> float:
    """Return 2 s_k^(2k-1), common to all exact shell-product legs."""

    k = _positive_integer(k)
    scale = float(alias_packet(k)) ** (1.0 / (2 * k))
    return 2.0 * scale ** (2 * k - 1)


def duhamel_ledger(k: int) -> dict[str, int | float | str | bool]:
    """Return the compressed all-leg Duhamel ledger for both shell channels."""

    k = _positive_integer(k)
    weight = common_duhamel_weight(k)
    return {
        "channel_count": 2,
        "legs_per_channel": 2 * k,
        "total_prefix_suffix_weight_count": 4 * k,
        "trace_observation_norm": 2,
        "common_weight_presentation": weight,
        "common_weight_formula": "2*A_k**((2k-1)/(2k))",
        "common_weight_status": "floating_presentation_of_exact_formula",
        "all_weights_equal": True,
        "all_leg_defects_exact": "0/1",
        "duhamel_majorant_exact": "0/1",
    }


def frozen_certificates() -> dict[str, Fraction | bool]:
    """Return the exact rational inequalities driving the route verdict."""

    phase_ratio = PARITY_CONSTANT * MULTIPLIER_CONSTANT
    growth_base = TARGET_RADIUS**2 / (HARDY_RADIUS**2 * EXPANSION)
    return {
        "phase_ratio": phase_ratio,
        "phase_ratio_margin": 1 - phase_ratio,
        "phase_ratio_strictly_between_zero_and_one": 0 < phase_ratio < 1,
        "growth_base": growth_base,
        "growth_base_margin": growth_base - 1,
        "growth_base_greater_than_one": growth_base > 1,
        "model_contrast_subunit": MODEL_CONTRAST < 1,
        "reference_contrast_subunit": REFERENCE_CONTRAST < 1,
    }


def target_contrast_radius(k: int) -> float | None:
    """Return y_k^(1/(2k)) for reachable rows, for presentation only."""

    k = _positive_integer(k)
    if not reachability_screen_zero(k):
        return None
    return float(required_power(k)) ** (1.0 / (2 * k))


def audit_row(k: int) -> dict[str, object]:
    """Return one exact-verdict isolated-model audit row."""

    k = _positive_integer(k)
    if k < 2:
        raise ValueError("the RH-329 audit domain is k >= 2")
    alias = alias_packet(k)
    parity = parity_packet(k)
    shell = shell_packet(k)
    power = required_power(k)
    mismatch = power_mismatch(k)
    error = residual(k)
    normalized = residual_to_target(k)
    radius = target_contrast_radius(k)
    return {
        "k": k,
        "period": 2 * k,
        "sigma_interval": outward_decimal_interval(noise_scale(k)),
        "target_interval": outward_decimal_interval(target(k)),
        "alias_packet_interval": outward_decimal_interval(alias),
        "shell_scale_interval": outward_decimal_interval(alias),
        "shell_scale_identity": "L_k=A_k",
        "parity_packet_interval": outward_decimal_interval(parity),
        "boundary_packet_exact": "0/1",
        "shell_packet_interval": outward_decimal_interval(shell),
        "observation_error_exact": "0/1",
        "far_remainder_exact": "0/1",
        "parity_to_alias_interval": outward_decimal_interval(parity / alias),
        "required_power_interval": outward_decimal_interval(power),
        "reachability_screen_zero_exact": reachability_screen_zero(k),
        "model_power_interval": outward_decimal_interval(MODEL_CONTRAST ** (2 * k)),
        "reference_power_interval": outward_decimal_interval(
            REFERENCE_CONTRAST ** (2 * k)
        ),
        "power_mismatch_interval": outward_decimal_interval(mismatch),
        "target_contrast_radius_presentation": radius,
        "contrast_radius_gap_presentation": (
            None if radius is None else radius - float(MODEL_CONTRAST)
        ),
        "root_presentation_status": "floating_presentation_only",
        "residual_interval": outward_decimal_interval(error),
        "alias_to_target_interval": outward_decimal_interval(alias_to_target(k)),
        "target_to_alias_power_tolerance_interval": outward_decimal_interval(
            target(k) / alias
        ),
        "target_over_k_alias_radius_tolerance_interval": outward_decimal_interval(
            target(k) / (k * alias)
        ),
        "residual_to_target_interval": outward_decimal_interval(normalized),
        "absolute_residual_to_target_interval": outward_decimal_interval(
            abs(normalized)
        ),
        "best_case_absolute_residual_to_target_interval": outward_decimal_interval(
            abs(normalized)
        ),
        "worst_case_absolute_residual_to_target_interval": outward_decimal_interval(
            abs(normalized)
        ),
        "observation_duhamel_majorant_to_target_exact": "0/1",
        "far_remainder_bound_to_target_exact": "0/1",
        "residual_negative_exact": error < 0,
        "within_one_target_unit_exact": abs(error) <= target(k),
        "within_one_target_unit_status": (
            "finite_reproduction_check_not_a_little_o_verdict"
        ),
        "duhamel": duhamel_ledger(k),
        "verdict_source": "exact_fraction_arithmetic",
    }


def isolated_interface() -> dict[str, object]:
    """Return the RH-329 to RH-330 typed handoff."""

    return {
        "model_type": "graded_finite_dimensional_isolated_trace_model",
        "alias_block": "diag(beta_k repeated 2k-2, beta repeated 2)",
        "parity_block": "one_dimensional_reference_minus_noisy_even_power",
        "boundary_block": "identical_scaled_two_state_exchange_blocks",
        "shell_blocks": "Q_c=A_k**(1/(2k))*K_c and Q_c0=A_k**(1/(2k))*K_c0",
        "model_contrast": fraction_string(MODEL_CONTRAST),
        "reference_contrast": fraction_string(REFERENCE_CONTRAST),
        "shell_scale": "L_k=A_k",
        "phase": "eta=0",
        "audit_domain": "integer k>=2",
        "clearance": fraction_string(CLEARANCE_CONSTANT),
        "orientation": ["positive", "negative", "positive"],
        "observation_error": "0/1",
        "duhamel_majorant": "0/1",
        "far_remainder": "0/1",
        "isolated_model_joint_matching": "fails",
        "actual_noisy_operator_identified": False,
        "full_trace_transfer_proved": False,
    }
