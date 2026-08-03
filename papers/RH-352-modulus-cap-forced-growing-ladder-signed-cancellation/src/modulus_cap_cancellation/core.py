"""Exact finite formula checks for the RH-352 theorem.

The finite fixtures below reproduce the source-bound algebra.  They are not
observations of physical traces or evidence for an asymptotic statement.
"""

from __future__ import annotations

from fractions import Fraction
import math
from typing import Iterable


R_H = Fraction(17, 20)
Q = Fraction(1, 2)
R = Fraction(7, 5)
LAMBDA_LOWER = Fraction(28, 17)
LAMBDA_UPPER = Fraction(17, 10)
FIXTURE_LAMBDA = Fraction(5, 3)


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
    if isinstance(value, tuple):
        return [_fraction_text(item) for item in value]
    if isinstance(value, list):
        return [_fraction_text(item) for item in value]
    if isinstance(value, dict):
        return {key: _fraction_text(item) for key, item in value.items()}
    return value


def _log_fraction(value: Fraction) -> float:
    if value <= 0:
        raise ValueError("logarithm requires a positive fraction")
    return math.log(value.numerator) - math.log(value.denominator)


def _scientific(value: Fraction, digits: int = 12) -> str:
    if value == 0:
        return "0"
    log_value = _log_fraction(abs(value))
    exponent = math.floor(log_value / math.log(10))
    mantissa = math.exp(log_value - exponent * math.log(10))
    sign = "-" if value < 0 else ""
    return f"{sign}{mantissa:.{digits}f}e{exponent:+d}"


def _root(value: Fraction, degree: int) -> float:
    if degree <= 0:
        raise ValueError("degree must be positive")
    if value < 0:
        raise ValueError("root input must be nonnegative")
    if value == 0:
        return 0.0
    return math.exp(_log_fraction(value) / degree)


def rate_certificate(lambda_value: int | Fraction = FIXTURE_LAMBDA) -> dict[str, object]:
    """Return exact rates and strict rational certificates."""

    lam = _lambda(lambda_value)
    x_value = R**2 / (R_H**2 * lam)
    b_noisy = Q**2 * R_H**2 * lam
    rho_noisy = R_H**2 * lam**3 * Q**2
    rho_target = 1 / lam
    raw_noisy = lam**2 * (Q * R) ** 2
    raw_target = (R / (R_H * lam)) ** 2
    rho_noisy_upper = Fraction(1_419_857, 1_600_000)
    raw_noisy_lower = Fraction(9_604, 7_225)
    return {
        "lambda": lam,
        "x": x_value,
        "x_lambda": x_value * lam,
        "b_noisy": b_noisy,
        "rho_noisy": rho_noisy,
        "rho_target": rho_target,
        "rho_max": max(rho_noisy, rho_target),
        "rho_noisy_upper": rho_noisy_upper,
        "rho_target_upper": Fraction(17, 28),
        "raw_noisy_root": raw_noisy,
        "raw_noisy_lower": raw_noisy_lower,
        "raw_target_root": raw_target,
        "normalized_rates_subunit": max(rho_noisy, rho_target) < 1,
        "certified_noisy_upper_subunit": rho_noisy_upper < 1,
        "raw_noisy_lower_superunit": raw_noisy_lower > 1,
        "scale_conversion_exact": x_value * rho_noisy == raw_noisy,
    }


def coordinate_caps(
    k: int,
    j: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, object]:
    """Reproduce exact eta=0 source majorants at one selected coordinate."""

    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be an integer")
    if isinstance(j, bool) or not isinstance(j, int):
        raise TypeError("j must be an integer")
    if k < 5:
        raise ValueError("k must be at least five")
    if not 2 <= j < k:
        raise ValueError("j must satisfy 2<=j<k")
    lam = _lambda(lambda_value)
    m = k - j
    certificate = rate_certificate(lam)
    x_value = certificate["x"]
    b_noisy = certificate["b_noisy"]
    normalized_noisy = Fraction(2, m) * lam ** (2 * k) * b_noisy**m
    normalized_target = Fraction(24, m) * lam ** (-m)
    normalized_direct = normalized_noisy + normalized_target
    raw_noisy = Fraction(2, m) * lam ** (2 * k) * (Q * R) ** (2 * m)
    q_star_r = R / (R_H * lam)
    raw_target = Fraction(24, m) * q_star_r ** (2 * m)
    return {
        "k": k,
        "j": j,
        "m": m,
        "lambda": lam,
        "normalized_noisy_cap": normalized_noisy,
        "normalized_target_cap": normalized_target,
        "normalized_direct_cap": normalized_direct,
        "raw_noisy_cap": raw_noisy,
        "raw_target_cap": raw_target,
        "noisy_scale_conversion_exact": normalized_noisy * x_value**m == raw_noisy,
        "target_scale_conversion_exact": normalized_target * x_value**m == raw_target,
        "finite_fixture_only": True,
    }


def window_caps(
    k: int,
    depth: int,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, object]:
    """Return finite-window cap summaries without promoting them to evidence."""

    if isinstance(depth, bool) or not isinstance(depth, int):
        raise TypeError("depth must be an integer")
    if depth < 3:
        raise ValueError("depth must be at least three")
    if depth >= k:
        raise ValueError("depth must be smaller than k")
    lam = _lambda(lambda_value)
    rows = [coordinate_caps(k, j, lam) for j in range(2, depth + 1)]
    max_row = max(rows, key=lambda row: row["normalized_direct_cap"])
    raw_row = max(rows, key=lambda row: row["raw_noisy_cap"])
    x_value = rate_certificate(lam)["x"]
    geometric_weight = sum(
        (x_value ** (2 - j) for j in range(2, depth + 1)), Fraction(0)
    )
    normalized_u_cap = max_row["normalized_direct_cap"]
    normalized_l_cap = normalized_u_cap * geometric_weight
    return {
        "k": k,
        "depth": depth,
        "coordinate_count": depth - 1,
        "lambda": lam,
        "max_normalized_coordinate_j": max_row["j"],
        "max_raw_noisy_coordinate_j": raw_row["j"],
        "normalized_u_cap": normalized_u_cap,
        "normalized_l_cap": normalized_l_cap,
        "raw_noisy_window_cap": raw_row["raw_noisy_cap"],
        "geometric_weight": geometric_weight,
        "all_scale_conversions_exact": all(
            row["noisy_scale_conversion_exact"]
            and row["target_scale_conversion_exact"]
            for row in rows
        ),
        "finite_fixture_only": True,
    }


def _values(values: Iterable[int | Fraction], name: str) -> tuple[Fraction, ...]:
    converted = tuple(_fraction(value, name) for value in values)
    if not converted:
        raise ValueError(f"{name} must be nonempty")
    return converted


def finite_identity_witness(
    demand: Iterable[int | Fraction],
    parity: Iterable[int | Fraction],
    direct: Iterable[int | Fraction],
) -> dict[str, object]:
    """Check Y=S-P+p exactly on finite rational coefficient ledgers."""

    demand_values = _values(demand, "demand")
    parity_values = _values(parity, "parity")
    direct_values = _values(direct, "direct")
    if len({len(demand_values), len(parity_values), len(direct_values)}) != 1:
        raise ValueError("demand, parity, and direct must have equal lengths")
    remainder = tuple(
        source - packet + residual
        for source, packet, residual in zip(
            demand_values, parity_values, direct_values
        )
    )
    recovered = tuple(
        value + packet - source
        for value, packet, source in zip(
            remainder, parity_values, demand_values
        )
    )
    tracking_error = tuple(
        value - (source - packet)
        for value, source, packet in zip(
            remainder, demand_values, parity_values
        )
    )
    return {
        "demand": demand_values,
        "parity": parity_values,
        "direct": direct_values,
        "actual_Y_formula": remainder,
        "recovered_direct": recovered,
        "tracking_error": tracking_error,
        "direct_identity_exact": recovered == direct_values,
        "tracking_error_equals_direct_exact": tracking_error == direct_values,
        "physical_trace_observation": False,
    }


def _window_summary(k: int) -> dict[str, object]:
    depth = math.isqrt(k)
    data = window_caps(k, depth, FIXTURE_LAMBDA)
    return {
        "k": k,
        "depth": depth,
        "coordinate_count": data["coordinate_count"],
        "lambda_fixture": "5/3",
        "normalized_u_cap_decimal": _scientific(data["normalized_u_cap"]),
        "normalized_u_cap_kth_root": f"{_root(data['normalized_u_cap'], k):.12f}",
        "normalized_l_cap_decimal": _scientific(data["normalized_l_cap"]),
        "normalized_l_cap_kth_root": f"{_root(data['normalized_l_cap'], k):.12f}",
        "raw_noisy_majorant_decimal": _scientific(data["raw_noisy_window_cap"]),
        "raw_noisy_majorant_kth_root": f"{_root(data['raw_noisy_window_cap'], k):.12f}",
        "max_normalized_coordinate_j": data["max_normalized_coordinate_j"],
        "max_raw_noisy_coordinate_j": data["max_raw_noisy_coordinate_j"],
        "all_scale_conversions_exact": data["all_scale_conversions_exact"],
        "finite_formula_reproduction_only": True,
    }


def result_status() -> dict[str, object]:
    """Return the strict RH-352 machine-readable theorem ledger."""

    certificate = rate_certificate(FIXTURE_LAMBDA)
    witness = finite_identity_witness(
        (8, 5, 3),
        (8, 3, 1),
        (Fraction(1, 64), Fraction(-1, 81), Fraction(1, 125)),
    )
    gates = {
        "A_canonical_intrinsic_determinant": False,
        "B_time_oriented_unitary_completion": False,
        "C_self_adjoint_generator_T_log_T": False,
        "D_von_mangoldt_prime_power_trace": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "unnormalized_selected_prefix_vanishing_proved": False,
        "full_E_off_decided": False,
        "critical_order_controlled": False,
        "first_lower_order_controlled": False,
        "odd_orders_controlled": False,
        "upper_alias_orders_controlled": False,
        "head_counterloop_transport_closed": False,
        "rh241_moving_noisy_all_order_envelope_closed": False,
        "rh241_coefficient_bridge_closed": False,
        "rh288_activated": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
    }
    payload = {
        "status": "actual_growing_lower_even_natural_scale_cancellation_proved",
        "verdict": "GO_STRICT_SCOPED_THEOREM",
        "route_coordinate_closed": "actual_growing_lower_even_signed_remainder_open",
        "growing_window": {
            "indices": "m_(k,j)=k-j_for_2<=j<=J_k",
            "depth": "J_k->infinity_and_J_k=o(k)",
            "clock": "eta_k_bounded",
            "normalization": "2H_m*x^m_locally_and_x^(k-2)_aggregately",
        },
        "source_bounds": {
            "actual_noisy_modulus_complement": "tau_(sigma,n)=Tr(C_sigma^n)_and_|tau|<=sigma^(-1)q^(n-2)",
            "deterministic_target": "|a_n|<48q_*^n_for_all_n>=2",
            "direct_coefficient": "p_(sigma,k,n)=tau_(sigma,n)-a_n",
            "lower_ladder_identity": "p_(k,j)=Y_(k,j)+P_(k,j)-S_(k,j)",
        },
        "constants": _fraction_text(
            {
                "r_H": R_H,
                "q": Q,
                "R": R,
                "lambda_lower": LAMBDA_LOWER,
                "lambda_upper": LAMBDA_UPPER,
                "x_lambda": certificate["x_lambda"],
                "rho_noisy_uniform_upper": Fraction(1_419_857, 1_600_000),
                "rho_target_uniform_upper": Fraction(17, 28),
                "raw_noisy_uniform_lower": Fraction(9_604, 7_225),
            }
        ),
        "uniform_rate_theorem": {
            "U_k": "sup_j_|p_(k,j)|/(2H_m*x^m)",
            "root_ceiling": "max(r_H^2*lambda^3/4,1/lambda)<1",
            "actual_direct_coefficient": True,
            "growing_order_uniform": True,
        },
        "actual_consequences": {
            "normalized_direct_budget": "L_k^act->0_exponentially_with_same_root_ceiling",
            "uniform_Y_tracking": "sup_j_|C_M*Y/(2H_m*x^m)-(1-a_k*lambda^(2-j))|->0",
            "aggregate_Y_law": "Yagg_k^act=F_(J_k-2)(a_k)/C_M+o(1)",
            "aggregate_positive_liminf": "liminf_Yagg_k^act>=A_infinity/C_M>0",
            "rh350_small_Y_hypothesis": "false_for_actual_coefficients",
        },
        "unnormalized_barrier": {
            "separate_noisy_majorant_root": "lambda^2*(qR)^2>9604/7225>1",
            "separate_target_majorant_root": "(q_*R)^2<1",
            "actual_unnormalized_verdict": "open",
        },
        "finite_formula_rows": [_window_summary(k) for k in (64, 144, 256)],
        "finite_identity_witness": _fraction_text(witness),
        "finite_rows_are_formula_reproduction_only": True,
        "source_anchors": {
            "RH-262": "strict_28/17<lambda_boundary",
            "RH-267": "all_order_|a_n|<48q_*^n",
            "RH-282": "M_sigma<=sigma^(-1)_and_modulus_complement_trace_cap",
            "RH-288": "tau-a_is_the_direct_complement_to_anchor_coefficient",
            "RH-336": "lambda<17/10",
            "RH-340": "same_clock_p=tau-a=q-d_type_lock",
            "RH-348": "actual_lower_even_p=Y+P-S_identity",
            "RH-350": "growing_window_uniform_S/P_laws_and_F_N_minimax",
            "RH-351": "close_completion_interpretation_only",
        },
        "gates": gates,
        "false_claims": false_claims,
        "scope": "actual_normalized_selected_lower_even_natural_scale_only",
    }
    return payload
