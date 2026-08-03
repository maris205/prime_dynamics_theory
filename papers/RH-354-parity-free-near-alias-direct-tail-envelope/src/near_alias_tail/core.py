"""Exact formula checks for the RH-354 direct-tail theorem.

Finite rows reproduce source-bound algebra only.  They are not observations
of the noisy operator or asymptotic evidence.
"""

from __future__ import annotations

from fractions import Fraction
import math


R_H = Fraction(17, 20)
Q = Fraction(1, 2)
R = Fraction(7, 5)
LAMBDA_LOWER = Fraction(28, 17)
LAMBDA_UPPER = Fraction(17, 10)
FIXTURE_LAMBDA = Fraction(5, 3)
PHYSICAL_LAMBDA_DIAGNOSTIC = 1.6785735104283222651


def _fraction(value: int | Fraction, name: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    return Fraction(value)


def _integer(value: int, name: str) -> int:
    if isinstance(value, bool) or type(value) is not int:
        raise TypeError(f"{name} must be an integer")
    return value


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


def rate_certificate(
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, object]:
    """Return the exact squared scales and global root certificates."""

    lam = _lambda(lambda_value)
    s = Q * R
    t = R / (R_H * lam)
    x_value = R**2 / (R_H**2 * lam)
    u_squared = s**2 / x_value
    v_squared = t**2 / x_value
    rho_noisy = lam**2 * u_squared
    rho_target = v_squared
    return {
        "lambda": lam,
        "s": s,
        "t": t,
        "x": x_value,
        "u_squared": u_squared,
        "v_squared": v_squared,
        "rho_noisy": rho_noisy,
        "rho_target": rho_target,
        "rho_noisy_identity": rho_noisy == R_H**2 * lam**3 / 4,
        "rho_target_identity": rho_target == 1 / lam,
        "rho_noisy_dominates": rho_noisy > rho_target,
        "rho_noisy_upper": Fraction(1_419_857, 1_600_000),
        "rho_target_upper": Fraction(17, 28),
        "rates_subunit": max(rho_noisy, rho_target) < 1,
    }


def alias_tail_majorant(
    k: int,
    depth: int,
    eta: int = 0,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, object]:
    """Return the exact alias-clock logarithmic-tail source majorant."""

    order = _integer(k, "k")
    lower_depth = _integer(depth, "depth")
    phase = _integer(eta, "eta")
    if order < 2:
        raise ValueError("k must be at least two")
    if not 0 <= lower_depth <= 2 * order - 2:
        raise ValueError("depth must satisfy 0 <= depth <= 2*k-2")
    lam = _lambda(lambda_value)
    data = rate_certificate(lam)
    n_start = 2 * order - lower_depth
    s = data["s"]
    t = data["t"]
    noisy = (
        Q ** (-2)
        * lam ** (-2 * phase)
        * data["rho_noisy"] ** order
        * s ** (-lower_depth)
        / (n_start * (1 - s))
    )
    target = (
        48
        * data["rho_target"] ** order
        * t ** (-lower_depth)
        / (n_start * (1 - t))
    )
    return {
        "k": order,
        "depth": lower_depth,
        "eta": phase,
        "N": n_start,
        "N_parity": "even" if n_start % 2 == 0 else "odd",
        "noisy_majorant": noisy,
        "target_majorant": target,
        "total_majorant": noisy + target,
        "finite_formula_only": True,
    }


def linear_root_diagnostic(
    depth_ratio: int | Fraction,
    normalization: str,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, object]:
    """Evaluate the exact root formulas numerically for one rational depth."""

    ell = _fraction(depth_ratio, "depth_ratio")
    if not 0 <= ell <= 2:
        raise ValueError("depth_ratio must lie in [0,2]")
    data = rate_certificate(lambda_value)
    if normalization == "natural_bottom":
        noisy_base = math.sqrt(float(data["u_squared"]))
        target_base = math.sqrt(float(data["v_squared"]))
    elif normalization == "alias_clock":
        noisy_base = float(data["s"])
        target_base = float(data["t"])
    else:
        raise ValueError("normalization must be natural_bottom or alias_clock")
    noisy_root = float(data["rho_noisy"]) * noisy_base ** (-float(ell))
    target_root = float(data["rho_target"]) * target_base ** (-float(ell))
    return {
        "depth_ratio": ell,
        "normalization": normalization,
        "noisy_root": noisy_root,
        "target_root": target_root,
        "root_ceiling": max(noisy_root, target_root),
        "finite_formula_only": True,
    }


def threshold_diagnostics(lambda_value: float = PHYSICAL_LAMBDA_DIAGNOSTIC) -> dict[str, float]:
    """Evaluate the two exact threshold formulas at an archived decimal."""

    if isinstance(lambda_value, bool) or not isinstance(lambda_value, (int, float)):
        raise TypeError("lambda_value must be a real number")
    lam = float(lambda_value)
    if not float(LAMBDA_LOWER) < lam < float(LAMBDA_UPPER):
        raise ValueError("lambda_value must lie strictly between 28/17 and 17/10")
    x_value = float(R**2) / (float(R_H**2) * lam)
    s = float(Q * R)
    u = s / math.sqrt(x_value)
    rho_noisy = float(R_H**2) * lam**3 / 4
    return {
        "lambda": lam,
        "alpha_natural": math.log(1 / rho_noisy) / math.log(1 / u),
        "alpha_alias": math.log(1 / rho_noisy) / math.log(1 / s),
    }


def raw_method_certificate(
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, object]:
    """Return the exact unnormalized noisy-root method boundary."""

    lam = _lambda(lambda_value)
    raw_noisy_root = lam**2 * (Q * R) ** 2
    lower_certificate = Fraction(9604, 7225)
    return {
        "lambda": lam,
        "raw_noisy_root": raw_noisy_root,
        "strict_global_lower": lower_certificate,
        "global_lower_is_superunit": lower_certificate > 1,
        "fixture_is_superunit": raw_noisy_root > 1,
        "method_boundary_only": True,
    }


def result_status() -> dict[str, object]:
    """Return the strict machine-readable RH-354 theorem ledger."""

    rates = rate_certificate()
    thresholds = threshold_diagnostics()
    rows = [
        alias_tail_majorant(24, 4),
        alias_tail_majorant(24, 5),
        alias_tail_majorant(48, 6),
        alias_tail_majorant(48, 7),
    ]
    gates = {
        "A_canonical_intrinsic_determinant": False,
        "B_time_oriented_unitary_completion": False,
        "C_self_adjoint_generator_T_log_T": False,
        "D_von_mangoldt_prime_power_trace": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "unnormalized_direct_band_closed": False,
        "low_order_direct_prefix_closed": False,
        "full_E_off_decided": False,
        "head_defect_closed": False,
        "all_order_Y_P_S_decomposition_proved": False,
        "rh241_moving_noisy_envelope_closed": False,
        "rh241_coefficient_bridge_closed": False,
        "rh288_activated": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
    }
    return {
        "status": "RH-354_parity_free_near_alias_direct_tail_envelope",
        "verdict": "GO_SCOPED",
        "clock": "one_bounded_phase_physical_clock",
        "constants": _fraction_text(rates),
        "source_types": {
            "noisy": "tau_(sigma,n)=Tr(C_sigma^n)",
            "target": "a_n=deterministic_numerator_anchor",
            "direct": "p_(sigma,k,n)=tau_(sigma,n)-a_n=q_(sigma,k,n)-d_(sigma,k,n)",
        },
        "source_anchors": {
            "RH-262": "strict_28/17<lambda",
            "RH-267": "all_order_|a_n|<48*q_*^n",
            "RH-282": "all_order_|tau_(sigma,n)|<=sigma^-1*q^(n-2)",
            "RH-288": "typed_tau_minus_a_identity",
            "RH-340": "direct_p_equals_tau_minus_a_equals_q_minus_d",
            "RH-352": "natural_scale_rate_certificates",
            "RH-353": "next_parity_free_near_alias_route",
        },
        "tail_theorem": {
            "N_k": "2*k-L_k",
            "bottom_normalized_tail": "x^(-N_k/2)*sum_(n>=N_k)|p_(sigma,k,n)|*R^n",
            "sublinear_root_ceiling": "rho_N=r_H^2*lambda^3/4<1419857/1600000<1",
            "all_orders_included": True,
        },
        "band_corollary": {
            "near_alias_band": "x^(-k)*sum_(N_k<=n<4k)|p_n|*R^n/n",
            "full_log_tail": "x^(-k)*sum_(n>=N_k)|p_n|*R^n/n",
            "sublinear_root_ceiling": "rho_N<1",
        },
        "linear_frontiers": {
            "alpha_natural_exact": "log(1/rho_N)/log(1/u)",
            "alpha_alias_exact": "log(1/rho_N)/log(1/s)",
            "alpha_natural_diagnostic": f"{thresholds['alpha_natural']:.15f}",
            "alpha_alias_diagnostic": f"{thresholds['alpha_alias']:.15f}",
            "diagnostics_are_not_interval_certificates": True,
        },
        "raw_method_boundary": _fraction_text(raw_method_certificate()),
        "finite_rows": _fraction_text(rows),
        "finite_rows_are_formula_reproduction_only": True,
        "gates": gates,
        "false_claims": false_claims,
        "scope": [
            "actual_direct_coefficient_only",
            "odd_even_critical_lower_upper_and_later_orders_above_cut_at_direct_type",
            "normalized_tail_not_unnormalized_prefix",
            "no_transfer_to_full_trace_without_head_defect",
            "no_RH_conclusion",
        ],
    }
