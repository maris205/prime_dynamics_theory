"""Exact exchange-channel and signed-budget formulas for RH-327."""

from __future__ import annotations

import math
from typing import Iterable


TRACE_RADIUS = 1.4
HARDY_RADIUS = 0.85


def _positive_integer(value: int, *, name: str) -> int:
    value = int(value)
    if value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _even_order(value: int) -> int:
    value = _positive_integer(value, name="order")
    if value % 2:
        raise ValueError("the first-alias exchange budget requires even order")
    return value


def _contrast(value: float, *, name: str = "contrast") -> float:
    value = float(value)
    if not -1.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [-1, 1]")
    return value


def _positive(value: float, *, name: str) -> float:
    value = float(value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")
    return value


def exchange_matrix(contrast: float) -> tuple[tuple[float, float], ...]:
    """Return the exchange-symmetric two-branch Markov matrix ``K_c``."""

    contrast = _contrast(contrast)
    return (
        ((1.0 + contrast) / 2.0, (1.0 - contrast) / 2.0),
        ((1.0 - contrast) / 2.0, (1.0 + contrast) / 2.0),
    )


def exchange_power(
    contrast: float, order: int
) -> tuple[tuple[float, float], ...]:
    """Return ``K_c**order = K_(c**order)`` in closed form."""

    contrast = _contrast(contrast)
    order = _positive_integer(order, name="order")
    return exchange_matrix(contrast**order)


def symmetric_compression(contrast: float, order: int) -> float:
    """Return the branch-blind symmetric compression of ``K_c**order``."""

    _contrast(contrast)
    _positive_integer(order, name="order")
    return 1.0


def trace_power(contrast: float, order: int) -> float:
    """Return ``Tr(K_c**order) = 1 + c**order``."""

    contrast = _contrast(contrast)
    order = _positive_integer(order, name="order")
    return 1.0 + contrast**order


def localized_branch_trace(contrast: float, order: int) -> float:
    """Return either diagonal branch trace of ``K_c**order``."""

    return trace_power(contrast, order) / 2.0


def reset_completion_trace(contrast: float, order: int) -> float:
    """Return the trace power of the synthetic reset completion ``G_d x K_c``."""

    return trace_power(contrast, order)


def exchange_shell_defect(
    contrast: float,
    reference_contrast: float,
    order: int,
    *,
    scale: float = 1.0,
) -> float:
    """Return the signed noisy-minus-reference even-order shell defect."""

    contrast = _contrast(contrast)
    reference_contrast = _contrast(
        reference_contrast, name="reference_contrast"
    )
    order = _even_order(order)
    scale = _positive(scale, name="scale")
    return scale * (contrast**order - reference_contrast**order)


def fixed_reference_interval(
    reference_contrast: float,
    order: int,
    *,
    scale: float = 1.0,
) -> tuple[float, float]:
    """Return the exact defect interval when the reference is fixed."""

    reference_contrast = _contrast(
        reference_contrast, name="reference_contrast"
    )
    order = _even_order(order)
    scale = _positive(scale, name="scale")
    anchor = abs(reference_contrast) ** order
    return (-scale * anchor, scale * (1.0 - anchor))


def interval_distance(value: float, lower: float, upper: float) -> float:
    """Return the Euclidean distance from a scalar to a closed interval."""

    value = float(value)
    lower = float(lower)
    upper = float(upper)
    if lower > upper:
        raise ValueError("lower endpoint must not exceed upper endpoint")
    if value < lower:
        return lower - value
    if value > upper:
        return value - upper
    return 0.0


def best_fixed_reference_shell(
    demand: float,
    reference_contrast: float,
    order: int,
    *,
    scale: float = 1.0,
) -> dict[str, float | bool]:
    """Return the sharp fixed-reference shell and residual for a demand."""

    demand = float(demand)
    lower, upper = fixed_reference_interval(
        reference_contrast, order, scale=scale
    )
    shell = min(upper, max(lower, demand))
    return {
        "demand": demand,
        "interval_lower": lower,
        "interval_upper": upper,
        "best_shell": shell,
        "signed_residual": shell - demand,
        "absolute_residual": abs(shell - demand),
        "reachable": lower <= demand <= upper,
    }


def realize_fixed_reference_shell(
    demand: float,
    reference_contrast: float,
    order: int,
    *,
    scale: float = 1.0,
) -> float:
    """Return a nonnegative noisy contrast realizing a reachable demand."""

    demand = float(demand)
    reference_contrast = _contrast(
        reference_contrast, name="reference_contrast"
    )
    order = _even_order(order)
    scale = _positive(scale, name="scale")
    anchor = abs(reference_contrast) ** order
    powered = demand / scale + anchor
    tolerance = 32.0 * math.ulp(1.0)
    if powered < -tolerance or powered > 1.0 + tolerance:
        raise ValueError("demand lies outside the fixed-reference interval")
    powered = min(1.0, max(0.0, powered))
    return powered ** (1.0 / order)


def free_pair_interval(*, scale: float = 1.0) -> tuple[float, float]:
    """Return the union of defect values when both contrasts are free."""

    scale = _positive(scale, name="scale")
    return (-scale, scale)


def free_pair_distance(demand: float, *, scale: float = 1.0) -> float:
    """Return the sharp free-pair residual ``(|D|-L)_+``."""

    scale = _positive(scale, name="scale")
    return max(abs(float(demand)) - scale, 0.0)


def realize_free_pair_fraction(
    fraction: float, order: int
) -> tuple[float, float]:
    """Realize a normalized defect in ``[-1, 1]`` with two contrasts."""

    fraction = float(fraction)
    order = _even_order(order)
    if not -1.0 <= fraction <= 1.0:
        raise ValueError("fraction must lie in [-1, 1]")
    radius = abs(fraction) ** (1.0 / order)
    if fraction >= 0.0:
        return radius, 0.0
    return 0.0, radius


def minimum_pair_contrast_radius(fraction: float, order: int) -> float:
    """Return the minimum max contrast realizing a normalized defect."""

    fraction = float(fraction)
    order = _even_order(order)
    if not -1.0 <= fraction <= 1.0:
        raise ValueError("fraction must lie in [-1, 1]")
    return abs(fraction) ** (1.0 / order)


def scaled_edge_gap(fraction: float, k: int) -> float:
    """Return ``2k(1-|fraction|**(1/(2k)))`` for a nonzero fraction."""

    fraction = abs(float(fraction))
    k = _positive_integer(k, name="k")
    if not 0.0 < fraction <= 1.0:
        raise ValueError("absolute fraction must lie in (0, 1]")
    return 2.0 * k * (1.0 - fraction ** (1.0 / (2 * k)))


def first_alias_target(k: int, *, radius: float = TRACE_RADIUS) -> float:
    """Return the required first-alias error scale ``k R**(-2k)``."""

    k = _positive_integer(k, name="k")
    radius = _positive(radius, name="radius")
    return k * radius ** (-2 * k)


def localized_raw_packets(
    noisy_traces: Iterable[float],
    deterministic_traces: Iterable[float],
    order: int,
    *,
    hardy_radius: float = HARDY_RADIUS,
) -> tuple[float, float, float]:
    """Return the three Hardy-scaled localized raw-trace packets."""

    order = _positive_integer(order, name="order")
    hardy_radius = _positive(hardy_radius, name="hardy_radius")
    noisy = tuple(float(value) for value in noisy_traces)
    deterministic = tuple(float(value) for value in deterministic_traces)
    if len(noisy) != 3 or len(deterministic) != 3:
        raise ValueError("exactly three boundary/shell/far slots are required")
    factor = hardy_radius ** (-order)
    return tuple(
        factor * (noisy_value - deterministic_value)
        for noisy_value, deterministic_value in zip(noisy, deterministic)
    )


def raw_packet_from_totals(
    noisy_traces: Iterable[float],
    deterministic_traces: Iterable[float],
    order: int,
    *,
    hardy_radius: float = HARDY_RADIUS,
) -> float:
    """Return the total raw packet obtained by summing the localized slots."""

    return sum(
        localized_raw_packets(
            noisy_traces,
            deterministic_traces,
            order,
            hardy_radius=hardy_radius,
        )
    )


def required_shell_demand(
    alias_defect: float, parity_packet: float, boundary_packet: float
) -> float:
    """Return ``A-P-B``, the shell demand before the trace remainder."""

    return float(alias_defect) - float(parity_packet) - float(boundary_packet)


def first_alias_residual(
    boundary_packet: float,
    shell_packet: float,
    trace_remainder: float,
    parity_packet: float,
    alias_defect: float,
) -> float:
    """Return the exact RH-326 signed packet ledger."""

    return (
        float(boundary_packet)
        + float(shell_packet)
        + float(trace_remainder)
        + float(parity_packet)
        - float(alias_defect)
    )


def contrast_row(contrast: float, order: int) -> dict[str, float | int]:
    """Return one exact exchange-channel diagnostic row."""

    contrast = _contrast(contrast)
    order = _positive_integer(order, name="order")
    return {
        "contrast": contrast,
        "order": order,
        "symmetric_compression": symmetric_compression(contrast, order),
        "trace_power": trace_power(contrast, order),
        "left_localized_trace": localized_branch_trace(contrast, order),
        "right_localized_trace": localized_branch_trace(contrast, order),
    }


def fixed_budget_row(
    demand_fraction: float, reference_contrast: float, order: int
) -> dict[str, float | int | bool | None]:
    """Return one unit-scale fixed-reference budget row."""

    row = best_fixed_reference_shell(
        demand_fraction, reference_contrast, order, scale=1.0
    )
    noisy_contrast = None
    if bool(row["reachable"]):
        noisy_contrast = realize_fixed_reference_shell(
            demand_fraction, reference_contrast, order, scale=1.0
        )
    return {
        "order": int(order),
        "reference_contrast": float(reference_contrast),
        "demand_fraction": float(demand_fraction),
        "interval_lower": float(row["interval_lower"]),
        "interval_upper": float(row["interval_upper"]),
        "reachable": bool(row["reachable"]),
        "best_shell_fraction": float(row["best_shell"]),
        "absolute_residual_fraction": float(row["absolute_residual"]),
        "realizing_noisy_contrast": noisy_contrast,
    }


def rh328_interface() -> dict[str, object]:
    """Return the typed RH-327 to RH-328 handoff schema."""

    return {
        "schema": "rh327_to_rh328_v1",
        "phase_mode": "fixed_eta_subsequence",
        "phase_definition": "eta=k-log(1/sigma)/(2*log(lambda))",
        "clearance_model": "d=C_b*lambda**(-2*eta)",
        "period": "2*k",
        "target_scale": "k*R**(-2*k)",
        "trace_normalization": "r_H**(-2*k)",
        "retained_coordinates": ["V", "U", "W"],
        "coordinate_orientation": ["positive", "negative", "positive"],
        "output_center_shift": "kappa_aff*d",
        "branch_labels": ["boundary", "neighboring_shell", "far_remainder"],
        "raw_packet_identity": "T=B+S+R",
        "joint_residual_identity": "e=B+S+R+P-A",
        "joint_signs": {
            "boundary_packet": 1,
            "neighboring_shell_packet": 1,
            "trace_remainder": 1,
            "parity_packet": 1,
            "counterloop_alias_defect": -1,
        },
        "exchange_model_demand": "D=A-P-B",
        "fixed_reference_reachability_screen": (
            "dist(D,[-L*|c0|^(2k),L*(1-|c0|^(2k))])"
        ),
        "physical_fixed_contrast_mismatch": "open",
        "required_remainder_scale": "o(k*R**(-2*k))",
        "actual_localized_trace_slots": "defined_exactly",
        "local_probability_to_trace_identification": "open",
        "trace_observation_norm_bound": "open",
        "duhamel_prefix_suffix_bound": "open",
        "little_o_remainder": "open",
    }
