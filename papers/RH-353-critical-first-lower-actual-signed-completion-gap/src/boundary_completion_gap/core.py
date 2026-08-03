"""Exact finite formula checks for the RH-353 boundary gap theorem.

The fixtures reproduce algebraic identities and strict rational bounds.
They are not observations of physical traces or asymptotic evidence.
"""

from __future__ import annotations

from fractions import Fraction
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


def _positive(value: int | Fraction, name: str) -> Fraction:
    result = _fraction(value, name)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


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


def rate_certificate(lambda_value: int | Fraction = FIXTURE_LAMBDA) -> dict[str, object]:
    """Return the two-order natural-scale rate and global certificates."""

    lam = _lambda(lambda_value)
    x_value = R**2 / (R_H**2 * lam)
    rho_noisy = R_H**2 * lam**3 / 4
    rho_target = 1 / lam
    return {
        "lambda": lam,
        "x": x_value,
        "rho_noisy": rho_noisy,
        "rho_target": rho_target,
        "rho_max": max(rho_noisy, rho_target),
        "rho_noisy_upper": Fraction(1_419_857, 1_600_000),
        "rho_target_upper": Fraction(17, 28),
        "normalized_rates_subunit": max(rho_noisy, rho_target) < 1,
    }


def boundary_completion(
    gamma: int | Fraction,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, object]:
    """Return the exact leading critical and first-lower completion vector."""

    lam = _lambda(lambda_value)
    phase = _positive(gamma, "gamma")
    critical = 2 - phase
    first_lower = 1 - phase / lam
    gap = critical - lam * first_lower
    return {
        "lambda": lam,
        "gamma": phase,
        "critical_Z": critical,
        "first_lower_Z": first_lower,
        "phase_free_gap": gap,
        "gap_identity_exact": gap == 2 - lam,
        "max_abs_Z": max(abs(critical), abs(first_lower)),
        "finite_formula_only": True,
    }


def minimax_certificate(
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, object]:
    """Return the exact minimax optimizer and strict global lower certificate."""

    lam = _lambda(lambda_value)
    optimizer = 3 * lam / (1 + lam)
    value = (2 - lam) / (1 + lam)
    witness = boundary_completion(optimizer, lam)
    return {
        "lambda": lam,
        "optimizer_gamma": optimizer,
        "minimax_value": value,
        "critical_at_optimizer": witness["critical_Z"],
        "first_lower_at_optimizer": witness["first_lower_Z"],
        "opposite_equal_errors": (
            witness["critical_Z"] == value
            and witness["first_lower_Z"] == -value
        ),
        "global_lower_certificate": Fraction(1, 9),
        "strictly_above_global_certificate": value > Fraction(1, 9),
        "gap_lower_certificate": Fraction(3, 10),
        "strict_gap_certificate": 2 - lam > Fraction(3, 10),
    }


def weighted_supply_bound(
    critical_Z: int | Fraction,
    first_lower_Z: int | Fraction,
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> dict[str, object]:
    """Check the triangle/minimax bound induced by the affine gap."""

    lam = _lambda(lambda_value)
    z0 = _fraction(critical_Z, "critical_Z")
    zm = _fraction(first_lower_Z, "first_lower_Z")
    gap = z0 - lam * zm
    max_abs = max(abs(z0), abs(zm))
    return {
        "lambda": lam,
        "critical_Z": z0,
        "first_lower_Z": zm,
        "gap": gap,
        "max_abs_Z": max_abs,
        "triangle_bound_exact": (1 + lam) * max_abs >= abs(gap),
        "implied_lower_bound": abs(gap) / (1 + lam),
    }


def finite_rows(
    gammas: Iterable[int | Fraction],
    lambda_value: int | Fraction = FIXTURE_LAMBDA,
) -> list[dict[str, object]]:
    """Evaluate exact finite phase fixtures."""

    lam = _lambda(lambda_value)
    values = tuple(_positive(gamma, "gamma") for gamma in gammas)
    if not values:
        raise ValueError("gammas must be nonempty")
    return [boundary_completion(gamma, lam) for gamma in values]


def result_status() -> dict[str, object]:
    """Return the strict machine-readable RH-353 theorem ledger."""

    rates = rate_certificate()
    minimax = minimax_certificate()
    rows = finite_rows(
        (
            Fraction(1),
            FIXTURE_LAMBDA,
            minimax["optimizer_gamma"],
            Fraction(2),
        )
    )
    gates = {
        "A_canonical_intrinsic_determinant": False,
        "B_time_oriented_unitary_completion": False,
        "C_self_adjoint_generator_T_log_T": False,
        "D_von_mangoldt_prime_power_trace": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "critical_direct_o_H_proved": False,
        "first_lower_direct_o_H_proved": False,
        "full_E_off_decided": False,
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
    return {
        "status": "actual_critical_first_lower_phase_free_completion_gap_proved",
        "verdict": "GO_STRICT_SCOPED_THEOREM",
        "clock": "one_bounded_phase_physical_clock_with_m=k-1",
        "source_types": {
            "direct": "p=tau-a=q-d_at_orders_2k_and_2k-2",
            "critical": "p_k^0=Y_k^0+P_k^0-S_k^0",
            "first_lower": "p_k^-=Y_k^-+P_k^--S_k^-",
        },
        "rate_theorem": {
            "two_order_cap": "max(|p_k^0|/(2H_k*x^k),|p_k^-|/(2H_m*x^m))",
            "root_ceiling": "max(r_H^2*lambda^3/4,1/lambda)<1",
            "rho_noisy_upper": "1419857/1600000",
            "rho_target_upper": "17/28",
        },
        "actual_completion_laws": {
            "critical": "C_M*Y_k^0/(2H_k*x^k)=2-gamma_k+o(1)",
            "first_lower": "C_M*Y_k^-/(2H_m*x^m)=1-gamma_k/lambda+o(1)",
            "gamma_k": "C_*C_M*lambda^(eta_k)",
        },
        "phase_free_theorem": {
            "affine_gap": "Z_k^0-lambda*Z_k^-=2-lambda+o(1)",
            "gap_lower": "2-lambda>3/10",
            "minimax_liminf": "liminf_max(|Z_k^0|,|Z_k^-|)>1/9",
            "actual_Y_supply": "two_coordinate_max_unnormalized_Y_weight_diverges_on_x^(k-1)_scale",
        },
        "constants": _fraction_text(
            {
                "r_H": R_H,
                "q": Q,
                "R": R,
                "lambda_lower": LAMBDA_LOWER,
                "lambda_upper": LAMBDA_UPPER,
                "fixture_lambda": FIXTURE_LAMBDA,
                "fixture_x": rates["x"],
                "global_minimax_certificate": Fraction(1, 9),
                "global_gap_certificate": Fraction(3, 10),
            }
        ),
        "finite_rows": _fraction_text(rows),
        "finite_minimax_witness": _fraction_text(minimax),
        "finite_rows_are_formula_reproduction_only": True,
        "source_anchors": {
            "RH-262": "28/17<lambda",
            "RH-267": "all_order_deterministic_target_cap",
            "RH-282": "actual_modulus_complement_trace_cap",
            "RH-344": "complete_critical_direct_decomposition_and_demand_scale",
            "RH-345": "critical_parity_phase_law",
            "RH-346": "complete_first_lower_direct_decomposition_and_demand_scale",
            "RH-347": "first_lower_parity_phase_law",
            "RH-352": "natural_scale_actual_direct_cap_method",
        },
        "gates": gates,
        "false_claims": false_claims,
        "scope": "actual_critical_and_first_lower_Y_at_leading_natural_scale_only",
    }
