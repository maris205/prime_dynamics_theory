"""Exact signed-ledger tools for the RH-330 full-trace transfer criterion."""

from __future__ import annotations

from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from typing import Iterable, Mapping, Sequence


OBSERVABLE_FIELDS = ("boundary", "shell", "remainder", "parity", "alias")
SPLIT_FIELDS = (
    "boundary",
    "exchange",
    "observation",
    "remainder",
    "parity",
    "alias",
)
OBSERVABLE_SIGNS = {
    "boundary": 1,
    "shell": 1,
    "remainder": 1,
    "parity": 1,
    "alias": -1,
}
SPLIT_SIGNS = {
    "boundary": 1,
    "exchange": 1,
    "observation": 1,
    "remainder": 1,
    "parity": 1,
    "alias": -1,
}


def _positive_integer(value: int, *, name: str = "k") -> int:
    if isinstance(value, bool) or int(value) != value or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return int(value)


def _as_fraction(value: Fraction | int | str) -> Fraction:
    return Fraction(value)


def _slot_map(
    values: Mapping[str, Fraction | int | str],
    *,
    fields: Sequence[str],
    name: str,
) -> dict[str, Fraction]:
    if set(values) != set(fields):
        raise ValueError(f"{name} must contain exactly {tuple(fields)}")
    return {field: _as_fraction(values[field]) for field in fields}


def _nonnegative_map(
    values: Mapping[str, Fraction | int | str],
    *,
    fields: Sequence[str],
    name: str,
) -> dict[str, Fraction]:
    result = _slot_map(values, fields=fields, name=name)
    if any(value < 0 for value in result.values()):
        raise ValueError(f"{name} values must be nonnegative")
    return result


def fraction_string(value: Fraction | int | str) -> str:
    """Return a canonical rational string."""

    value = _as_fraction(value)
    return f"{value.numerator}/{value.denominator}"


def outward_decimal_interval(
    value: Fraction | int | str, digits: int = 18
) -> list[str]:
    """Return directed decimal endpoints enclosing an exact rational."""

    value = _as_fraction(value)
    digits = _positive_integer(digits, name="digits")
    numerator = Decimal(value.numerator)
    denominator = Decimal(value.denominator)
    with localcontext() as context:
        context.prec = digits
        context.rounding = ROUND_FLOOR
        lower = numerator / denominator
    with localcontext() as context:
        context.prec = digits
        context.rounding = ROUND_CEILING
        upper = numerator / denominator
    return [format(lower, "e"), format(upper, "e")]


def critical_weighted_contribution(
    residual: Fraction | int | str, target: Fraction | int | str
) -> Fraction:
    """Return |e_(2k)| R^(2k)/(2k) = |e_(2k)|/(2 H_k)."""

    residual = _as_fraction(residual)
    target = _as_fraction(target)
    if target <= 0:
        raise ValueError("target must be positive")
    return abs(residual) / (2 * target)


def weighted_prefix_decomposition(
    off_alias_budget: Fraction | int | str,
    critical_residual: Fraction | int | str,
    target: Fraction | int | str,
) -> dict[str, Fraction]:
    """Split a one-alias weighted prefix into off-alias and critical terms."""

    off_alias_budget = _as_fraction(off_alias_budget)
    if off_alias_budget < 0:
        raise ValueError("off-alias budget must be nonnegative")
    critical = critical_weighted_contribution(critical_residual, target)
    return {
        "off_alias_budget": off_alias_budget,
        "critical_contribution": critical,
        "total_weighted_prefix": off_alias_budget + critical,
    }


def observable_residual(
    slots: Mapping[str, Fraction | int | str],
) -> Fraction:
    """Evaluate B + S + R + P - A on the observable five-slot ledger."""

    slots = _slot_map(slots, fields=OBSERVABLE_FIELDS, name="slots")
    return sum(OBSERVABLE_SIGNS[field] * slots[field] for field in OBSERVABLE_FIELDS)


def split_residual(slots: Mapping[str, Fraction | int | str]) -> Fraction:
    """Evaluate B + X + E_obs + R + P - A on a frozen split ledger."""

    slots = _slot_map(slots, fields=SPLIT_FIELDS, name="slots")
    return sum(SPLIT_SIGNS[field] * slots[field] for field in SPLIT_FIELDS)


def collapse_shell(
    slots: Mapping[str, Fraction | int | str],
) -> dict[str, Fraction]:
    """Collapse a frozen exchange/observation split to the observable shell."""

    slots = _slot_map(slots, fields=SPLIT_FIELDS, name="slots")
    return {
        "boundary": slots["boundary"],
        "shell": slots["exchange"] + slots["observation"],
        "remainder": slots["remainder"],
        "parity": slots["parity"],
        "alias": slots["alias"],
    }


def gauge_shift(
    slots: Mapping[str, Fraction | int | str],
    shift: Fraction | int | str,
) -> dict[str, Fraction]:
    """Apply X -> X+t and E_obs -> E_obs-t to a frozen split ledger."""

    result = _slot_map(slots, fields=SPLIT_FIELDS, name="slots")
    shift = _as_fraction(shift)
    result["exchange"] += shift
    result["observation"] -= shift
    return result


def replacement_defects(
    actual: Mapping[str, Fraction | int | str],
    model: Mapping[str, Fraction | int | str],
) -> dict[str, Fraction]:
    """Return actual-minus-model defects in every observable slot."""

    actual = _slot_map(actual, fields=OBSERVABLE_FIELDS, name="actual")
    model = _slot_map(model, fields=OBSERVABLE_FIELDS, name="model")
    return {field: actual[field] - model[field] for field in OBSERVABLE_FIELDS}


def joint_replacement_defect(
    defects: Mapping[str, Fraction | int | str],
) -> Fraction:
    """Return the signed joint defect Delta_B+Delta_S+Delta_R+Delta_P-Delta_A."""

    return observable_residual(defects)


def transfer_identity(
    actual: Mapping[str, Fraction | int | str],
    model: Mapping[str, Fraction | int | str],
) -> dict[str, Fraction]:
    """Return the exact full-trace replacement identity."""

    model_residual = observable_residual(model)
    actual_residual = observable_residual(actual)
    joint = joint_replacement_defect(replacement_defects(actual, model))
    return {
        "model_residual": model_residual,
        "joint_replacement_defect": joint,
        "actual_residual": actual_residual,
        "identity_error": actual_residual - model_residual - joint,
    }


def zero_observable_slots() -> dict[str, Fraction]:
    """Return a zero-filled observable ledger."""

    return {field: Fraction(0) for field in OBSERVABLE_FIELDS}


def add_observable_slots(
    left: Mapping[str, Fraction | int | str],
    right: Mapping[str, Fraction | int | str],
) -> dict[str, Fraction]:
    """Add two observable ledgers componentwise."""

    left = _slot_map(left, fields=OBSERVABLE_FIELDS, name="left")
    right = _slot_map(right, fields=OBSERVABLE_FIELDS, name="right")
    return {field: left[field] + right[field] for field in OBSERVABLE_FIELDS}


def symmetric_packet_interval(
    model_residual: Fraction | int | str,
    centers: Mapping[str, Fraction | int | str],
    radii: Mapping[str, Fraction | int | str],
) -> dict[str, Fraction]:
    """Return the sharp interval from independent centered slot enclosures."""

    model_residual = _as_fraction(model_residual)
    centers = _slot_map(centers, fields=OBSERVABLE_FIELDS, name="centers")
    radii = _nonnegative_map(radii, fields=OBSERVABLE_FIELDS, name="radii")
    center = model_residual + joint_replacement_defect(centers)
    radius = sum(radii.values(), Fraction(0))
    lower = center - radius
    upper = center + radius
    best = Fraction(0) if lower <= 0 <= upper else min(abs(lower), abs(upper))
    return {
        "center": center,
        "radius": radius,
        "lower": lower,
        "upper": upper,
        "best_absolute_residual": best,
        "worst_absolute_residual": max(abs(lower), abs(upper)),
    }


def grouped_signed_interval(
    model_residual: Fraction | int | str,
    group_centers: Iterable[Fraction | int | str],
    group_radii: Iterable[Fraction | int | str],
) -> dict[str, Fraction]:
    """Return the sharp interval after coupled signed terms are grouped."""

    model_residual = _as_fraction(model_residual)
    centers = [_as_fraction(value) for value in group_centers]
    radii = [_as_fraction(value) for value in group_radii]
    if len(centers) != len(radii):
        raise ValueError("group centers and radii must have equal lengths")
    if any(radius < 0 for radius in radii):
        raise ValueError("group radii must be nonnegative")
    center = model_residual + sum(centers, Fraction(0))
    radius = sum(radii, Fraction(0))
    lower = center - radius
    upper = center + radius
    best = Fraction(0) if lower <= 0 <= upper else min(abs(lower), abs(upper))
    return {
        "center": center,
        "radius": radius,
        "lower": lower,
        "upper": upper,
        "best_absolute_residual": best,
        "worst_absolute_residual": max(abs(lower), abs(upper)),
    }


def weighted_signed_ledger(
    orientations: Sequence[int],
    weights: Sequence[Fraction | int | str],
    defects: Sequence[Fraction | int | str],
) -> dict[str, Fraction | int]:
    """Retain every signed Duhamel term and its unsigned majorant."""

    if not (len(orientations) == len(weights) == len(defects)):
        raise ValueError("orientations, weights, and defects must have equal lengths")
    if any(orientation not in (-1, 1) for orientation in orientations):
        raise ValueError("orientations must be +1 or -1")
    exact_weights = [_as_fraction(value) for value in weights]
    exact_defects = [_as_fraction(value) for value in defects]
    if any(weight < 0 for weight in exact_weights):
        raise ValueError("weights must be nonnegative")
    terms = [
        orientation * weight * defect
        for orientation, weight, defect in zip(
            orientations, exact_weights, exact_defects, strict=True
        )
    ]
    return {
        "term_count": len(terms),
        "signed_sum": sum(terms, Fraction(0)),
        "absolute_majorant": sum((abs(term) for term in terms), Fraction(0)),
    }


def balanced_replacement(scale: Fraction | int | str) -> dict[str, Fraction]:
    """Return large boundary/shell defects with exact signed cancellation."""

    scale = _as_fraction(scale)
    result = zero_observable_slots()
    result["boundary"] = scale
    result["shell"] = -scale
    return result


def unpaired_subalias_replacement(
    alias_scale: Fraction | int | str, k: int
) -> dict[str, Fraction]:
    """Return an o(A_k) defect A_k/k that can dominate H_k."""

    alias_scale = _as_fraction(alias_scale)
    k = _positive_integer(k)
    result = zero_observable_slots()
    result["boundary"] = alias_scale / k
    return result


def repairing_replacement(
    model_residual: Fraction | int | str,
    target: Fraction | int | str,
    k: int,
) -> dict[str, Fraction]:
    """Return Delta=-e_hat+H/k, which repairs the residual to H/k."""

    model_residual = _as_fraction(model_residual)
    target = _as_fraction(target)
    k = _positive_integer(k)
    result = zero_observable_slots()
    result["boundary"] = -model_residual + target / k
    return result


def transfer_audit_row(
    k: int,
    *,
    model_residual: Fraction | int | str,
    alias_scale: Fraction | int | str,
    target: Fraction | int | str,
) -> dict[str, object]:
    """Return one exact RH-329-to-RH-330 transfer diagnostic row."""

    k = _positive_integer(k)
    if k < 2:
        raise ValueError("the RH-330 audit domain is k >= 2")
    model_residual = _as_fraction(model_residual)
    alias_scale = _as_fraction(alias_scale)
    target = _as_fraction(target)
    if alias_scale <= 0 or target <= 0:
        raise ValueError("alias scale and target must be positive")

    repair = repairing_replacement(model_residual, target, k)
    repair_joint = joint_replacement_defect(repair)
    repaired_residual = model_residual + repair_joint
    balanced = balanced_replacement(alias_scale)
    balanced_joint = joint_replacement_defect(balanced)
    balanced_absolute = sum((abs(value) for value in balanced.values()), Fraction(0))
    uncancelled = zero_observable_slots()
    uncancelled["boundary"] = alias_scale
    uncancelled["shell"] = alias_scale
    uncancelled_joint = joint_replacement_defect(uncancelled)
    subalias = unpaired_subalias_replacement(alias_scale, k)
    subalias_joint = joint_replacement_defect(subalias)
    duhamel = weighted_signed_ledger(
        [1] * (2 * k) + [-1] * (2 * k),
        [Fraction(1)] * (4 * k),
        [alias_scale] * (4 * k),
    )

    return {
        "k": k,
        "target_interval": outward_decimal_interval(target),
        "alias_scale_interval": outward_decimal_interval(alias_scale),
        "model_residual_to_target_interval": outward_decimal_interval(
            model_residual / target
        ),
        "model_critical_weighted_contribution_interval": outward_decimal_interval(
            critical_weighted_contribution(model_residual, target)
        ),
        "repair_center_to_alias_interval": outward_decimal_interval(
            -model_residual / alias_scale
        ),
        "repair_joint_to_alias_interval": outward_decimal_interval(
            repair_joint / alias_scale
        ),
        "repair_precision_H_over_A_interval": outward_decimal_interval(
            target / alias_scale
        ),
        "repaired_residual_to_target_exact": fraction_string(
            repaired_residual / target
        ),
        "repaired_residual_is_H_over_k_exact": repaired_residual == target / k,
        "balanced_joint_defect_exact": fraction_string(balanced_joint),
        "balanced_absolute_majorant_to_target_interval": outward_decimal_interval(
            balanced_absolute / target
        ),
        "balanced_cancellation_exact": balanced_joint == 0,
        "same_unsigned_bounds_uncancelled_to_target_interval": (
            outward_decimal_interval(uncancelled_joint / target)
        ),
        "same_unsigned_bounds_have_opposite_verdicts_exact": (
            balanced_joint == 0 and uncancelled_joint == 2 * alias_scale
        ),
        "subalias_defect_to_alias_exact": fraction_string(
            subalias_joint / alias_scale
        ),
        "subalias_defect_to_target_interval": outward_decimal_interval(
            subalias_joint / target
        ),
        "subalias_is_smaller_than_alias_exact": abs(subalias_joint) < alias_scale,
        "subalias_exceeds_target_exact": abs(subalias_joint) > target,
        "duhamel_term_count": duhamel["term_count"],
        "duhamel_signed_sum_exact": fraction_string(duhamel["signed_sum"]),
        "duhamel_absolute_majorant_to_target_interval": outward_decimal_interval(
            Fraction(duhamel["absolute_majorant"]) / target
        ),
        "verdict_source": "exact_fraction_arithmetic",
    }


def rh331_interface() -> dict[str, object]:
    """Return the typed RH-330-to-RH-331 handoff."""

    return {
        "observable_ledger": "e=B+S+R+P-A",
        "critical_extraction": "E_prefix=E_off+abs(e_(2k))/(2H_k)",
        "joint_replacement": "Theta=Delta_B+Delta_S+Delta_R+Delta_P-Delta_A",
        "exact_transfer_identity": "e_actual=e_model+Theta",
        "closure_transfer": "e_model=o(H) implies e_actual=o(H) iff Theta=o(H)",
        "split_gauge": "X->X+t and E_obs->E_obs-t leaves S=X+E_obs invariant",
        "duhamel_channels": ["minus_critical", "plus_critical"],
        "duhamel_terms_retained": "4k before grouping",
        "actual_identification_map_proved": False,
        "actual_joint_replacement_little_o_proved": False,
        "actual_full_trace_replacement_proved": False,
    }
