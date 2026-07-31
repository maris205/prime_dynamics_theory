"""Exact scalar ledgers for the RH-328 joint matching interface.

The routines in this module evaluate proved algebraic formulas.  They do not
identify a physical shell contrast or certify any asymptotic noisy trace law.
"""

from __future__ import annotations

import math
from collections.abc import Iterable


U_C = 1.5436890126920764
LAMBDA = 1.6785735104283224
HARDY_RADIUS = 0.85
TARGET_RADIUS = 1.4
BETA = 1.0 / (HARDY_RADIUS * math.sqrt(LAMBDA))
MULTIPLIER_CONSTANT = 1.9463429052009678
PARITY_CONSTANT = 0.105258535936908
CLEARANCE_CONSTANT = 0.4608051492
ALPHA = 2.0 * U_C
KAPPA_AFF = ALPHA * LAMBDA


def _finite(value: float, *, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive(value: float, *, name: str) -> float:
    value = _finite(value, name=name)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")
    return value


def _nonnegative(value: float, *, name: str) -> float:
    value = _finite(value, name=name)
    if value < 0.0:
        raise ValueError(f"{name} must be nonnegative")
    return value


def _positive_integer(value: int, *, name: str) -> int:
    if isinstance(value, bool) or int(value) != value or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return int(value)


def _contrast(value: float, *, name: str) -> float:
    value = _finite(value, name=name)
    if abs(value) > 1.0:
        raise ValueError(f"{name} must lie in [-1, 1]")
    return value


def hardy_target(k: int, *, radius: float = TARGET_RADIUS) -> float:
    """Return the first-alias target H_k = k R^(-2k)."""

    k = _positive_integer(k, name="k")
    radius = _positive(radius, name="radius")
    return k * radius ** (-2 * k)


def leading_alias_model(
    k: int,
    *,
    beta: float = BETA,
    multiplier_constant: float = MULTIPLIER_CONSTANT,
) -> float:
    """Evaluate the leading RH-326 alias model (2k/C_M) beta^(2k)."""

    k = _positive_integer(k, name="k")
    beta = _positive(beta, name="beta")
    multiplier_constant = _positive(
        multiplier_constant, name="multiplier_constant"
    )
    return (2.0 * k / multiplier_constant) * beta ** (2 * k)


def leading_parity_ratio(
    phase: float,
    *,
    parity_constant: float = PARITY_CONSTANT,
    multiplier_constant: float = MULTIPLIER_CONSTANT,
    expansion: float = LAMBDA,
) -> float:
    """Evaluate C_* C_M lambda^eta (diagnostic, not interval certified)."""

    phase = _finite(phase, name="phase")
    parity_constant = _positive(parity_constant, name="parity_constant")
    multiplier_constant = _positive(
        multiplier_constant, name="multiplier_constant"
    )
    expansion = _positive(expansion, name="expansion")
    return parity_constant * multiplier_constant * expansion**phase


def leading_clearance_ratio(
    phase: float,
    *,
    clearance_constant: float = CLEARANCE_CONSTANT,
    expansion: float = LAMBDA,
) -> float:
    """Evaluate C_b lambda^(-2 eta) on a fixed clock phase."""

    phase = _finite(phase, name="phase")
    clearance_constant = _positive(
        clearance_constant, name="clearance_constant"
    )
    expansion = _positive(expansion, name="expansion")
    return clearance_constant * expansion ** (-2.0 * phase)


def joint_demand(
    alias_defect: float,
    parity_packet: float,
    boundary_packet: float,
) -> float:
    """Return D = A - P - B with the RH-326/RH-327 sign convention."""

    return (
        _finite(alias_defect, name="alias_defect")
        - _finite(parity_packet, name="parity_packet")
        - _finite(boundary_packet, name="boundary_packet")
    )


def exchange_shell(
    k: int,
    scale: float,
    contrast: float,
    reference_contrast: float,
) -> float:
    """Return L(c^(2k)-c0^(2k)) for a fixed reference contrast."""

    k = _positive_integer(k, name="k")
    scale = _positive(scale, name="scale")
    contrast = _contrast(contrast, name="contrast")
    reference_contrast = _contrast(
        reference_contrast, name="reference_contrast"
    )
    return scale * (
        contrast ** (2 * k) - reference_contrast ** (2 * k)
    )


def matching_power(
    k: int,
    demand: float,
    scale: float,
    reference_contrast: float,
) -> float:
    """Return the exact required even power y = c0^(2k) + D/L."""

    k = _positive_integer(k, name="k")
    demand = _finite(demand, name="demand")
    scale = _positive(scale, name="scale")
    reference_contrast = _contrast(
        reference_contrast, name="reference_contrast"
    )
    return reference_contrast ** (2 * k) + demand / scale


def distance_to_unit_interval(value: float) -> float:
    """Distance from a scalar to [0, 1]."""

    value = _finite(value, name="value")
    if value < 0.0:
        return -value
    if value > 1.0:
        return value - 1.0
    return 0.0


def fixed_reference_reachability(
    k: int,
    demand: float,
    scale: float,
    reference_contrast: float,
) -> dict[str, float | bool | None]:
    """Return the exact best-case fixed-reference reachability data."""

    scale = _positive(scale, name="scale")
    y = matching_power(k, demand, scale, reference_contrast)
    reachable = 0.0 <= y <= 1.0
    radius = y ** (1.0 / (2 * int(k))) if reachable else None
    return {
        "required_power": y,
        "reachable": reachable,
        "target_contrast_radius": radius,
        "best_absolute_residual": scale * distance_to_unit_interval(y),
    }


def joint_residual(
    boundary_packet: float,
    shell_packet: float,
    remainder: float,
    parity_packet: float,
    alias_defect: float,
) -> float:
    """Return e = B + S + R + P - A."""

    return (
        _finite(boundary_packet, name="boundary_packet")
        + _finite(shell_packet, name="shell_packet")
        + _finite(remainder, name="remainder")
        + _finite(parity_packet, name="parity_packet")
        - _finite(alias_defect, name="alias_defect")
    )


def joint_matching_decomposition(
    *,
    k: int,
    alias_defect: float,
    parity_packet: float,
    boundary_packet: float,
    scale: float,
    contrast: float,
    reference_contrast: float,
    observation_error: float = 0.0,
    remainder: float = 0.0,
) -> dict[str, float]:
    """Evaluate the exact RH-328 decomposition.

    The conditional shell representation is
    S = L(c^(2k)-c0^(2k)) + observation_error.
    """

    demand = joint_demand(alias_defect, parity_packet, boundary_packet)
    y = matching_power(k, demand, scale, reference_contrast)
    shell_model = exchange_shell(k, scale, contrast, reference_contrast)
    observation_error = _finite(
        observation_error, name="observation_error"
    )
    remainder = _finite(remainder, name="remainder")
    shell_packet = shell_model + observation_error
    model_mismatch = scale * (abs(float(contrast)) ** (2 * int(k)) - y)
    residual = joint_residual(
        boundary_packet,
        shell_packet,
        remainder,
        parity_packet,
        alias_defect,
    )
    decomposed = model_mismatch + observation_error + remainder
    return {
        "demand": demand,
        "required_power": y,
        "shell_model": shell_model,
        "shell_packet": shell_packet,
        "model_mismatch": model_mismatch,
        "observation_error": observation_error,
        "remainder": remainder,
        "residual": residual,
        "decomposed_residual": decomposed,
        "identity_error": residual - decomposed,
    }


def normalized_required_power(
    *,
    parity_to_alias: float,
    boundary_to_alias: float,
    shell_to_alias: float,
    reference_power: float,
) -> float:
    """Return z0 + (1-q-b)/ell in alias-normalized variables."""

    parity_to_alias = _finite(parity_to_alias, name="parity_to_alias")
    boundary_to_alias = _finite(
        boundary_to_alias, name="boundary_to_alias"
    )
    shell_to_alias = _positive(shell_to_alias, name="shell_to_alias")
    reference_power = _nonnegative(reference_power, name="reference_power")
    if reference_power > 1.0:
        raise ValueError("reference_power must lie in [0, 1]")
    return reference_power + (
        1.0 - parity_to_alias - boundary_to_alias
    ) / shell_to_alias


def target_contrast_radius(k: int, required_power: float) -> float:
    """Return y^(1/(2k)) for y in [0, 1]."""

    k = _positive_integer(k, name="k")
    required_power = _finite(required_power, name="required_power")
    if not 0.0 <= required_power <= 1.0:
        raise ValueError("required_power must lie in [0, 1]")
    return required_power ** (1.0 / (2 * k))


def power_radius_comparison(
    k: int,
    required_power: float,
    contrast: float,
) -> dict[str, float]:
    """Return exact mean-value bounds comparing power and radius mismatch."""

    k = _positive_integer(k, name="k")
    required_power = _finite(required_power, name="required_power")
    if not 0.0 < required_power <= 1.0:
        raise ValueError("required_power must lie in (0, 1]")
    contrast = abs(_contrast(contrast, name="contrast"))
    target = target_contrast_radius(k, required_power)
    radius_mismatch = abs(contrast - target)
    power_mismatch = abs(contrast ** (2 * k) - required_power)
    lo = min(contrast, target)
    hi = max(contrast, target)
    lower_bound = 2.0 * k * lo ** (2 * k - 1) * radius_mismatch
    upper_bound = 2.0 * k * hi ** (2 * k - 1) * radius_mismatch
    return {
        "target_radius": target,
        "radius_mismatch": radius_mismatch,
        "power_mismatch": power_mismatch,
        "mean_value_lower_bound": lower_bound,
        "mean_value_upper_bound": upper_bound,
    }


def duhamel_majorant(
    weights: Iterable[float], defects: Iterable[float]
) -> float:
    """Return sum_j W_j delta_j for nonnegative weights and defects."""

    weights = list(weights)
    defects = list(defects)
    if len(weights) != len(defects):
        raise ValueError("weights and defects must have equal length")
    return sum(
        _nonnegative(w, name="weight") * _nonnegative(d, name="defect")
        for w, d in zip(weights, defects, strict=True)
    )


def uncertainty_interval(
    model_mismatch: float,
    observation_bound: float,
    remainder_bound: float,
) -> dict[str, float]:
    """Return the sharp residual interval under symmetric error bounds."""

    model_mismatch = _finite(model_mismatch, name="model_mismatch")
    observation_bound = _nonnegative(
        observation_bound, name="observation_bound"
    )
    remainder_bound = _nonnegative(
        remainder_bound, name="remainder_bound"
    )
    radius = observation_bound + remainder_bound
    return {
        "lower": model_mismatch - radius,
        "upper": model_mismatch + radius,
        "best_absolute_residual": max(abs(model_mismatch) - radius, 0.0),
        "worst_absolute_residual": abs(model_mismatch) + radius,
    }


def reachability_false_positive(
    *, theta: float, scale: float, target: float
) -> dict[str, float]:
    """Return the c0=0, D=theta L, c_phys=0 false-positive ledger."""

    theta = _finite(theta, name="theta")
    if not 0.0 < theta < 1.0:
        raise ValueError("theta must lie in (0, 1)")
    scale = _positive(scale, name="scale")
    target = _positive(target, name="target")
    demand = theta * scale
    return {
        "demand": demand,
        "best_case_reachability_residual": 0.0,
        "physical_model_mismatch": -demand,
        "absolute_mismatch_to_target": demand / target,
    }


def typed_interface() -> dict[str, object]:
    """Return the retained RH-328 interface and open physical fields."""

    return {
        "period": "2k",
        "target": "H_k=k*R^(-2k)",
        "clock": "k=log(1/sigma)/(2*log(lambda))+O(1)",
        "phase": "eta_sigma -> eta on a fixed-phase subsequence",
        "clearance": "d=C_b*lambda^(-2*eta)",
        "coordinates": ["V", "U", "W"],
        "orientation": ["positive", "negative", "positive"],
        "output_shift": "kappa_aff*d",
        "joint_ledger": "e=B+S+R+P-A",
        "demand": "D=A-P-B",
        "fixed_reference_power": "y=c0^(2k)+D/L",
        "conditional_shell_representation": "S=L*(c_phys^(2k)-c0^(2k))+E_obs",
        "exact_matching_equation": "e=L*(c_phys^(2k)-y)+E_obs+R",
        "duhamel_observation_bound": "U=sum_j W_j*delta_j",
        "physical_trace_observation_identified": False,
        "physical_shell_scale_identified": False,
        "physical_contrast_identified": False,
        "far_remainder_little_o_proved": False,
    }
