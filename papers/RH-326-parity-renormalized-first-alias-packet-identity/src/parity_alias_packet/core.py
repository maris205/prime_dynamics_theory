"""Exact parity and counterloop packet algebra for RH-326."""

from __future__ import annotations

import math


U_C = 1.5436890126920764
R_FIXED = U_C - 1.0
LAMBDA = 2.0 * U_C * R_FIXED
HARDY_RADIUS = 0.85
TRACE_RADIUS = 1.4
C_STAR = 0.105258535936908
MULTIPLIER_CONSTANT = 1.9463429052009677
CLEARANCE_CONSTANT = 0.4608051492
COUNTERLOOP_BETA_LIMIT = 1.0 / (HARDY_RADIUS * math.sqrt(LAMBDA))
ALPHA = 2.0 * U_C
KAPPA_AFF = ALPHA * LAMBDA
AFFINE_NOISE_BETA = math.sqrt(1.0 + LAMBDA**2)
MATCHING_EXPONENT = math.log(TRACE_RADIUS) / math.log(LAMBDA)
ALIAS_GROWTH_EXPONENT = (
    math.log(COUNTERLOOP_BETA_LIMIT * TRACE_RADIUS) / math.log(LAMBDA)
)
SCALAR_BALANCE_PHASE = -math.log(C_STAR * MULTIPLIER_CONSTANT) / math.log(
    LAMBDA
)
SCALAR_BALANCE_CLEARANCE = CLEARANCE_CONSTANT * (
    C_STAR * MULTIPLIER_CONSTANT
) ** 2


def _positive_integer(value: int, *, name: str) -> int:
    value = int(value)
    if value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _positive(value: float, *, name: str) -> float:
    value = float(value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")
    return value


def _parity_delta(delta: float) -> float:
    delta = float(delta)
    if delta < 0.0 or delta >= 1.0:
        raise ValueError("the parity gap delta must lie in [0, 1)")
    return delta


def parity_sign(order: int) -> int:
    """Return ``(-1)**order`` as an integer."""

    order = _positive_integer(order, name="order")
    return 1 if order % 2 == 0 else -1


def parity_packet(
    order: int, delta: float, *, hardy_radius: float = HARDY_RADIUS
) -> float:
    """Return the signed Hardy-scaled parity correction.

    If ``lambda_minus = -(1-delta)``, this is
    ``r_H**(-n) * ((-1)**n - lambda_minus**n)``.
    """

    order = _positive_integer(order, name="order")
    delta = _parity_delta(delta)
    hardy_radius = _positive(hardy_radius, name="hardy_radius")
    magnitude = -math.expm1(order * math.log1p(-delta))
    return parity_sign(order) * hardy_radius ** (-order) * magnitude


def parity_linear_term(
    order: int, delta: float, *, hardy_radius: float = HARDY_RADIUS
) -> float:
    """Return the signed first-order parity term."""

    order = _positive_integer(order, name="order")
    delta = _parity_delta(delta)
    hardy_radius = _positive(hardy_radius, name="hardy_radius")
    return parity_sign(order) * order * delta * hardy_radius ** (-order)


def parity_remainder_bound(
    order: int, delta: float, *, hardy_radius: float = HARDY_RADIUS
) -> float:
    """Return the uniform Taylor remainder bound in absolute value."""

    order = _positive_integer(order, name="order")
    delta = _parity_delta(delta)
    hardy_radius = _positive(hardy_radius, name="hardy_radius")
    return (
        0.5
        * order
        * (order - 1)
        * delta**2
        * hardy_radius ** (-order)
    )


def counterloop_moment(k: int, order: int, beta_k: float) -> float:
    """Return the exact finite-radius counterloop moment ``s_(k,n)``."""

    k = _positive_integer(k, name="k")
    order = _positive_integer(order, name="order")
    beta_k = _positive(beta_k, name="beta_k")
    alias_indicator = int(order % (2 * k) == 0)
    return beta_k**order * (
        2 * k * alias_indicator - 1 - parity_sign(order)
    )


def limiting_pole_moment(
    order: int, *, beta: float = COUNTERLOOP_BETA_LIMIT
) -> float:
    """Return the limiting pole moment, renamed to avoid archived conflicts."""

    order = _positive_integer(order, name="order")
    beta = _positive(beta, name="beta")
    return -2.0 * int(order % 2 == 0) * beta**order


def radial_counterloop_correction(
    k: int,
    order: int,
    beta_k: float,
    *,
    beta: float = COUNTERLOOP_BETA_LIMIT,
) -> float:
    """Return the non-alias radial correction in ``s_(k,n)-p_n``."""

    _positive_integer(k, name="k")
    order = _positive_integer(order, name="order")
    beta_k = _positive(beta_k, name="beta_k")
    beta = _positive(beta, name="beta")
    return 2.0 * int(order % 2 == 0) * (beta**order - beta_k**order)


def alias_impulse(k: int, order: int, beta_k: float) -> float:
    """Return the exact roots-of-unity alias impulse."""

    k = _positive_integer(k, name="k")
    order = _positive_integer(order, name="order")
    beta_k = _positive(beta_k, name="beta_k")
    return 2.0 * k * beta_k**order * int(order % (2 * k) == 0)


def counterloop_defect(
    k: int,
    order: int,
    beta_k: float,
    *,
    beta: float = COUNTERLOOP_BETA_LIMIT,
) -> float:
    """Return ``s_(k,n)-p_n`` in the Hardy-scaled ledger."""

    return counterloop_moment(k, order, beta_k) - limiting_pole_moment(
        order, beta=beta
    )


def hardy_bulk_difference(
    raw_trace_defect: float,
    order: int,
    delta: float,
    *,
    hardy_radius: float = HARDY_RADIUS,
) -> float:
    """Return ``c^H_(sigma,n)-c^H_n`` from the raw trace defect."""

    order = _positive_integer(order, name="order")
    hardy_radius = _positive(hardy_radius, name="hardy_radius")
    return float(raw_trace_defect) * hardy_radius ** (-order) + parity_packet(
        order, delta, hardy_radius=hardy_radius
    )


def first_alias_identity(
    raw_trace_defect: float,
    k: int,
    delta: float,
    beta_k: float,
    *,
    hardy_radius: float = HARDY_RADIUS,
    beta: float = COUNTERLOOP_BETA_LIMIT,
) -> dict[str, float | int]:
    """Return every signed component of the exact first-alias residual."""

    k = _positive_integer(k, name="k")
    order = 2 * k
    raw_hardy = float(raw_trace_defect) * hardy_radius ** (-order)
    parity = parity_packet(order, delta, hardy_radius=hardy_radius)
    radial = radial_counterloop_correction(k, order, beta_k, beta=beta)
    impulse = alias_impulse(k, order, beta_k)
    defect = radial + impulse
    return {
        "k": k,
        "order": order,
        "raw_hardy_packet": raw_hardy,
        "parity_packet": parity,
        "radial_counterloop_correction": radial,
        "alias_impulse": impulse,
        "counterloop_defect": defect,
        "residual": raw_hardy + parity - defect,
    }


def asymptotic_beta_k(
    k: int,
    *,
    beta: float = COUNTERLOOP_BETA_LIMIT,
    multiplier_constant: float = MULTIPLIER_CONSTANT,
) -> float:
    """Return the leading archived finite-radius model for ``beta_k``."""

    k = _positive_integer(k, name="k")
    beta = _positive(beta, name="beta")
    multiplier_constant = _positive(
        multiplier_constant, name="multiplier_constant"
    )
    return beta * math.exp(-math.log(multiplier_constant) / (2.0 * k))


def natural_phase(sigma: float, k: int) -> float:
    """Return ``eta = k-log(1/sigma)/(2 log lambda)``."""

    sigma = float(sigma)
    if sigma <= 0.0 or sigma >= 1.0:
        raise ValueError("sigma must lie in (0, 1)")
    k = _positive_integer(k, name="k")
    return k - math.log(1.0 / sigma) / (2.0 * math.log(LAMBDA))


def sigma_from_phase(k: int, phase: float) -> float:
    """Invert the natural-clock phase relation."""

    k = _positive_integer(k, name="k")
    phase = float(phase)
    if k - phase <= 0.0:
        raise ValueError("k-phase must be positive")
    return LAMBDA ** (-2.0 * (k - phase))


def clearance_ratio_from_phase(
    phase: float, *, clearance_constant: float = CLEARANCE_CONSTANT
) -> float:
    """Return the leading boundary clearance-to-noise ratio."""

    clearance_constant = _positive(
        clearance_constant, name="clearance_constant"
    )
    return clearance_constant * LAMBDA ** (-2.0 * float(phase))


def scalar_balance_ratio(phase: float) -> float:
    """Return the leading even parity-packet / alias-defect ratio."""

    return C_STAR * MULTIPLIER_CONSTANT * LAMBDA ** float(phase)


def packet_row(k: int, phase: float) -> dict[str, float | int]:
    """Evaluate the leading archived packet model at a fixed clock phase."""

    k = _positive_integer(k, name="k")
    phase = float(phase)
    sigma = sigma_from_phase(k, phase)
    delta = C_STAR * math.sqrt(sigma)
    beta_k = asymptotic_beta_k(k)
    identity = first_alias_identity(0.0, k, delta, beta_k)
    alias_value = float(identity["counterloop_defect"])
    parity_value = float(identity["parity_packet"])
    target = k * TRACE_RADIUS ** (-2 * k)
    return {
        "k": k,
        "phase": phase,
        "sigma": sigma,
        "parity_gap_model": delta,
        "beta_k_model": beta_k,
        "parity_packet": parity_value,
        "counterloop_defect": alias_value,
        "parity_to_alias_ratio": parity_value / alias_value,
        "leading_ratio": scalar_balance_ratio(phase),
        "scalar_only_residual": parity_value - alias_value,
        "target": target,
        "absolute_residual_to_target": abs(parity_value - alias_value) / target,
    }


def phase_row(phase: float) -> dict[str, float | list[str]]:
    """Return the phase and retained-coordinate interface data for RH-327."""

    phase = float(phase)
    clearance = clearance_ratio_from_phase(phase)
    return {
        "phase": phase,
        "clearance_ratio": clearance,
        "leading_parity_to_alias_ratio": scalar_balance_ratio(phase),
        "retained_coordinates": ["V", "U", "W"],
        "orientation": ["positive", "negative", "positive"],
        "output_center_shift": KAPPA_AFF * clearance,
    }


def sign_rows(k: int, delta: float, beta_k: float) -> list[dict[str, float | int | str]]:
    """Return an exact odd/even/alias sign table."""

    k = _positive_integer(k, name="k")
    rows = []
    for label, order in (
        ("odd_pre_alias", 2 * k - 1),
        ("even_pre_alias", 2 * k - 2),
        ("first_alias", 2 * k),
        ("odd_post_alias", 2 * k + 1),
        ("second_alias", 4 * k),
    ):
        rows.append(
            {
                "label": label,
                "order": order,
                "parity_sign": parity_sign(order),
                "parity_packet": parity_packet(order, delta),
                "radial_correction": radial_counterloop_correction(
                    k, order, beta_k
                ),
                "alias_impulse": alias_impulse(k, order, beta_k),
                "counterloop_defect": counterloop_defect(k, order, beta_k),
            }
        )
    return rows
