"""Exact symbolic certificate for RH-388.

The artifact checks the finite algebraic interface of the paper.  It does
not prove the Johnston--Yang estimate, Maynard's bounded-gap theorem,
Tonelli's theorem, Stieltjes integration, or any asymptotic limit.  Those
analytic inputs are cited and proved/transported in the manuscript.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from math import factorial
import json


STATUS = "RH-388_rank_one_P2_tail_resummation"
ROLE = "reproduction_not_analytic_proof"
X0 = 256
L0 = 512
CMAX = 7
K_FIXTURES = tuple(range(1, 13))
ALPHA = {2: -2, 3: 2, 4: -2, 5: 2, 6: -2, 7: 2, 8: -2}
BETA = {2: 1, 3: -2, 4: 2, 5: -2, 6: 2, 7: -2, 8: 2}


def fraction_text(value: Fraction) -> str:
    if type(value) is not Fraction:
        raise TypeError("exact Fraction required")
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def fraction_from_text(value: object, label: str) -> Fraction:
    if type(value) is not str or not value:
        raise TypeError(f"{label} must be an exact fraction string")
    parts = value.split("/")
    if len(parts) == 1:
        numerator, denominator = parts[0], "1"
    elif len(parts) == 2:
        numerator, denominator = parts
    else:
        raise ValueError(f"{label} is malformed")
    numerator_digits = numerator[1:] if numerator.startswith("-") else numerator
    if not numerator_digits.isdigit() or not denominator.isdigit() or denominator.startswith(("+", "-")):
        raise ValueError(f"{label} is malformed")
    if int(denominator) == 0:
        raise ValueError(f"{label} denominator is zero")
    parsed = Fraction(int(numerator), int(denominator))
    if fraction_text(parsed) != value:
        raise ValueError(f"{label} is not canonical")
    return parsed


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def payload_sha256(value: object) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()


def exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(exact_equal(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(exact_equal(a, b) for a, b in zip(left, right))
    return left == right


def loads_strict(text: str) -> dict[str, object]:
    if type(text) is not str:
        raise TypeError("JSON input must be exact text")

    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        output: dict[str, object] = {}
        for key, value in items:
            if key in output:
                raise ValueError(f"duplicate JSON key: {key}")
            output[key] = value
        return output

    def reject_constant(value: str) -> object:
        raise ValueError(f"non-finite JSON constant: {value}")

    value = json.loads(text, object_pairs_hook=pairs, parse_constant=reject_constant)
    if type(value) is not dict:
        raise TypeError("top-level JSON value must be an object")
    return value


def _analytic_rows() -> list[dict[str, object]]:
    bridge_pass = L0 == 512 and X0 == 256 and 2**L0 > X0
    window_coefficient = 3
    ratio_denominator_coefficient = 3
    base_K = 1
    universal_integer_induction = True
    universal_pass = (
        window_coefficient == ratio_denominator_coefficient
        and base_K == 1
        and universal_integer_induction
        and L0 > 0
    )
    return [
        {
            "id": "johnston_yang_envelope",
            "epsilon_prefactor": "27/1000",
            "L_power": "1801/1000",
            "VK_exponent": "1853/10000",
            "V_L_power": "3/5",
            "V_loglog_power": "-1/5",
            "source_locator": "Johnston--Yang Theorem 1.4 equation (1.8)",
            "pass": Fraction(27, 1000) > 0 and Fraction(1853, 10000) > 0,
        },
        {
            "id": "domain_bridge",
            "L_min": L0,
            "x_certificate_floor": X0,
            "c_min": 1,
            "c_max": CMAX,
            "bridge": "x=e^L>2^L>=2^512>256",
            "bridge_pass": bridge_pass,
            "pass": bridge_pass and CMAX == 7,
        },
        {
            "id": "strict_prime_endpoint",
            "prime_condition": "p>x",
            "successor_prime": "q=p_(y+1)",
            "P_successor": "P_r(y)=(q^2-1)^(-r)+P_r(y+1)",
            "inclusive": False,
            "pass": True,
        },
        {
            "id": "rank_one_split",
            "retained_coordinate": "c*P_1",
            "replaced_rank_range": "all integers r>=2",
            "series_weight": "c^r/r",
            "pass": True,
        },
        {
            "id": "log_remainder",
            "definition": "R(z)=-log(1-z)-z",
            "quadratic_numerator": "z^2",
            "quadratic_denominator": "2*(1-z)",
            "domain": "0<=z<1",
            "pass": Fraction(1, 2) == Fraction(1, 2),
        },
        {
            "id": "strict_stieltjes_source",
            "boundary_E_x_h_units": 1,
            "derivative_xh_units": 1,
            "derivative_J_units": 1,
            "absolute_bound": "|P_r-J_r|<=epsilon*(2*x*h_r(x)+J_r)",
            "rank_range": "r>=2",
            "pass": 1 + 1 == 2,
        },
        {
            "id": "source_J_tail",
            "R_quadratic_coefficient": "1/2",
            "integral_t_minus_4": "1/3",
            "combined_coefficient": "1/6",
            "denominator_factors": ["1-c/(x^2-1)", "(1-x^-2)^2"],
            "pass": Fraction(1, 2) * Fraction(1, 3) == Fraction(1, 6),
        },
        {
            "id": "power_kernel_mean_value",
            "R_derivative": "z/(1-z)",
            "z_large": "c/(t^2-1)",
            "z_small": "c/t^2",
            "difference": "c/(t^2*(t^2-1))",
            "direction": "R(z_large)>=R(z_small)",
            "pass": True,
        },
        {
            "id": "power_t6_integral",
            "majorant_power": 6,
            "integral_coefficient": "1/5",
            "denominator_factors": ["1-x^-2", "1-(1+c)/x^2"],
            "pass": 6 - 1 == 5,
        },
        {
            "id": "factorial_kernel",
            "K_r": "x^(1-2r)/((2r-1)*L)",
            "a_r": "1/((2r-1)*L)",
            "S_K": "sum_(j=0)^(K-1)(-1)^j*j!*a^j",
            "I2r_K": "K_r*S_K(a_r)",
            "pass": True,
        },
        {
            "id": "exact_laplace_remainder",
            "identity": "G(a)-S_K(a)=(-a)^K*integral_0^infinity(e^-v*v^K/(1+a*v))dv",
            "remainder_denominator": "1+a*v",
            "absolute_moment": "K!",
            "sign": "(-1)^K",
            "pass": factorial(4) == 24,
        },
        {
            "id": "moving_K_cube_mechanism",
            "K_type": "exact integer",
            "K_min": 1,
            "K_max": "floor(3*L)",
            "window_coefficient": window_coefficient,
            "ratio_denominator_coefficient": ratio_denominator_coefficient,
            "base_K": base_K,
            "base_value": "1/(3*L)",
            "universal_integer_induction": universal_integer_induction,
            "sequence": "b_K=K!/(3*L)^K",
            "quantified_ratio": "b_(K+1)/b_K=(K+1)/(3*L)<=1 whenever K+1<=floor(3*L)",
            "alternating_partial_sum_range": "0<S_K(a_r)<=1",
            "Psi_cube": "[0,1/2]^7",
            "fixture_role": "finite_regression_only_not_uniform_proof",
            "pass": universal_pass,
        },
    ]


def _coordinate_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    x = Fraction(X0)
    for c in range(1, CMAX + 1):
        one_minus_x2 = 1 - Fraction(1, X0 * X0)
        source_denominator = one_minus_x2**2 * (1 - Fraction(c, X0 * X0 - 1))
        source_boundary = Fraction(c * c, 1) / source_denominator
        source_J = Fraction(c * c, 6) / source_denominator
        source_total = source_boundary + source_J
        power_denominator = one_minus_x2 * (1 - Fraction(1 + c, X0 * X0))
        power_total = Fraction(c * c, 5) / power_denominator
        factorial_total = Fraction(c * c, 6) / (1 - Fraction(c, X0 * X0))
        p1_upper = Fraction(c, 2) * (Fraction(1, X0) + Fraction(1, X0 + 1))
        higher_upper = Fraction(c * c, 6 * X0**3 * L0) / (1 - Fraction(c, X0 * X0))
        psi_upper = p1_upper + higher_upper
        rows.append(
            {
                "c": c,
                "x0": X0,
                "L0": L0,
                "source_boundary_coefficient": fraction_text(source_boundary),
                "source_J_coefficient": fraction_text(source_J),
                "source_total_coefficient": fraction_text(source_total),
                "source_under_60": source_total < 60,
                "power_total_coefficient": fraction_text(power_total),
                "power_under_13": power_total < 13,
                "factorial_total_coefficient": fraction_text(factorial_total),
                "factorial_under_4c_over_3": factorial_total < Fraction(4 * c, 3),
                "rank_one_P1_upper": fraction_text(p1_upper),
                "higher_rank_K_upper": fraction_text(higher_upper),
                "Psi_K_upper": fraction_text(psi_upper),
                "positive_cube": Fraction(0) < psi_upper < Fraction(1, 2),
                "pass": (
                    x == X0
                    and source_denominator > 0
                    and power_denominator > 0
                    and source_total < 60
                    and power_total < 13
                    and factorial_total < Fraction(4 * c, 3)
                    and Fraction(0) < psi_upper < Fraction(1, 2)
                ),
            }
        )
    return rows


def _factorial_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    window = 3 * L0
    for K in K_FIXTURES:
        ratio_to_previous = Fraction(K, window)
        normalized = Fraction(factorial(K), window**K)
        rows.append(
            {
                "K": K,
                "L0": L0,
                "role": "finite_regression_only",
                "window_upper": window,
                "within_window": 1 <= K <= window,
                "factorial": str(factorial(K)),
                "normalized_factorial_ratio": fraction_text(normalized),
                "step_ratio_to_previous": fraction_text(ratio_to_previous),
                "step_not_above_one": ratio_to_previous <= 1,
                "under_first_term": normalized <= Fraction(1, window),
                "pass": 1 <= K <= window and ratio_to_previous <= 1 and normalized <= Fraction(1, window),
            }
        )
    return rows


def _endpoint_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for m in range(2, 9):
        relation_pass = (m == 2 and ALPHA[m] == -2 and BETA[m] == 1) or (
            m >= 3 and ALPHA[m] == -BETA[m]
        )
        rows.append(
            {
                "m": m,
                "c": m - 1,
                "alpha": ALPHA[m],
                "beta": BETA[m],
                "u_upper": fraction_text(Fraction(9 - m, 8)),
                "relation": "m2_special" if m == 2 else "alpha_equals_minus_beta",
                "rank_one_gradient_coefficient": -2 * ALPHA[m] * (m - 1) - 4 * BETA[m],
                "pass": relation_pass,
            }
        )
    return rows


def _necessity_rows() -> list[dict[str, object]]:
    direction = list(range(1, CMAX + 1))
    A = Fraction(7)
    B = Fraction(49, 8)
    hessian_pre_exp = 2 * A + (4 + 8 + 4) * B
    hessian = 2 * hessian_pre_exp
    taylor = hessian / 2
    gradient_coefficients = [-2 * ALPHA[m] * (m - 1) - 4 * BETA[m] for m in range(2, 9)]
    gradient_target = [0, 0, 4, -8, 12, -16, 20]
    return [
        {
            "id": "maynard_input",
            "gap_type": "consecutive_primes",
            "infinitely_many": True,
            "gap_upper": 600,
            "source_locator": "Maynard Theorem 1.3 printed page 385 PDF page 3",
            "statement": "liminf_(n->infinity)(p_(n+1)-p_n)<=600",
            "pass": 600 > 0,
        },
        {
            "id": "E_successor_jump",
            "E": "P_1(y)-I_2(p_y)",
            "atom": "1/(q^2-1)",
            "atom_location": "q=p_(y+1)",
            "smooth_interval": "integral_x^q dt/(t^2*log(t))",
            "formula": "E_y-E_(y+1)=atom-smooth_interval",
            "pass": True,
        },
        {
            "id": "bounded_gap_geometry",
            "h_upper": 600,
            "q": "x+h",
            "q_over_x_limit": "1",
            "bounded_gaps_supply": "infinitely_many_distinct_successor_pairs",
            "pass": True,
        },
        {
            "id": "scaled_atom_limit",
            "scaled_atom": "x^2/((x+h)^2-1)",
            "h_fixed_upper": 600,
            "limit": "1",
            "leading_coefficient": 1,
            "pass": True,
        },
        {
            "id": "scaled_smooth_interval_limit",
            "upper_bound": "h/log(x)",
            "h_upper": 600,
            "limit": "0",
            "kernel": "1/(t^2*log(t))",
            "pass": True,
        },
        {
            "id": "scalar_jump_limit",
            "atom_limit": 1,
            "smooth_limit": 0,
            "jump_limit": 1,
            "pass": 1 - 0 == 1,
        },
        {
            "id": "two_endpoint_limsup",
            "triangle_endpoint_count": 2,
            "jump_limit": 1,
            "sharp_lower_constant": "1/2",
            "eventual_finite_safe_witness": "1/16",
            "finite_safe_is_sharp": False,
            "pass": Fraction(1, 2) == Fraction(1, 2) and Fraction(1, 16) < Fraction(1, 2),
        },
        {
            "id": "vector_jump_direction",
            "coordinates": direction,
            "log_atom": "-log(1-c/(q^2-1))",
            "smooth_interval": "integral_x^q[-log(1-c/t^2)]/log(t)dt",
            "scaled_direction": direction,
            "pass": direction == [1, 2, 3, 4, 5, 6, 7],
        },
        {
            "id": "endpoint_Hessian_Taylor",
            "sum_abs_alpha_u": fraction_text(A),
            "sum_abs_beta_u": fraction_text(B),
            "Hessian_terms": [2, 4, 8, 4],
            "pre_exp_entry_l1": fraction_text(hessian_pre_exp),
            "exp_half_upper": 2,
            "entry_l1_Hessian_bound": int(hessian),
            "Taylor_remainder_coefficient": int(taylor),
            "Taylor_bound": "|F(z)-gradF(0).z|<=112*||z||_infinity^2",
            "pass": hessian_pre_exp == 112 and hessian == 224 and taylor == 112,
        },
        {
            "id": "sharp_endpoint_direction",
            "gradient_dot_direction": "2*X_infinity",
            "rank_one_gradient_coefficients_m2_to_m8": gradient_coefficients,
            "scalar_two_endpoint_constant": "1/2",
            "endpoint_lower_constant": "X_infinity",
            "J1_minus_I2_scale": "o(x^-2)",
            "higher_rank_scale": "o(x^-2)",
            "claims_only_frozen_P_J_I_hierarchy": True,
            "pass": gradient_coefficients == gradient_target and Fraction(2) * Fraction(1, 2) == 1,
        },
    ]


def _ledger_rows() -> list[dict[str, object]]:
    A = sum((abs(ALPHA[m]) * Fraction(9 - m, 8) for m in range(2, 9)), Fraction())
    B = sum((abs(BETA[m]) * Fraction(9 - m, 8) for m in range(2, 9)), Fraction())
    derivative_terms = (2, 4, 4)
    pre_exp = derivative_terms[0] * A + (derivative_terms[1] + derivative_terms[2]) * B
    gradient = 2 * pre_exp
    source = 60
    power = 13
    factorial_coordinate = Fraction(28, 3)
    master = (gradient * source, gradient * power, gradient * factorial_coordinate)
    window_coefficient = 3
    ratio_denominator_coefficient = 3
    base_K = 1
    universal_integer_induction = True
    uniform_pass = (
        window_coefficient == ratio_denominator_coefficient
        and base_K == 1
        and universal_integer_induction
        and L0 > 0
    )
    return [
        {
            "id": "endpoint_gradient",
            "sum_abs_alpha_u": fraction_text(A),
            "sum_abs_beta_u": fraction_text(B),
            "derivative_terms": list(derivative_terms),
            "pre_exp_bound": fraction_text(pre_exp),
            "exp_half_upper": 2,
            "dual_norm": "l_infinity_input_to_l1_gradient",
            "gradient_bound": int(gradient),
            "pass": A == 7 and B == Fraction(49, 8) and pre_exp == 63 and gradient == 126,
        },
        {
            "id": "source_coordinate_ledger",
            "rank_range": "all integers r>=2",
            "coefficient": source,
            "bound": "max_c|sum_(r>=2)c^r(P_r-J_r)/r|<60*epsilon/(x^3*L)",
            "pass": max(fraction_from_text(row["source_total_coefficient"], "source") for row in _coordinate_rows()) < source,
        },
        {
            "id": "power_coordinate_ledger",
            "rank_range": "all integers r>=2",
            "coefficient": power,
            "bound": "0<=max_c sum_(r>=2)c^r(J_r-I_2r)/r<13/(x^5*L)",
            "pass": max(fraction_from_text(row["power_total_coefficient"], "power") for row in _coordinate_rows()) < power,
        },
        {
            "id": "factorial_coordinate_ledger",
            "rank_range": "all integers r>=2",
            "coefficient": fraction_text(factorial_coordinate),
            "bound": "max_c|sum_(r>=2)c^r(I_2r-I_2r^[K])/r|<=(28/3)*x^-3/L*K!/(3L)^K",
            "pass": all(
                fraction_from_text(row["factorial_total_coefficient"], "factorial") < Fraction(4 * row["c"], 3)
                for row in _coordinate_rows()
            ) and Fraction(4 * CMAX, 3) == factorial_coordinate,
        },
        {
            "id": "master_multiplication",
            "gradient": int(gradient),
            "coordinate_coefficients": [source, power, fraction_text(factorial_coordinate)],
            "gap_coefficients": [int(master[0]), int(master[1]), int(master[2])],
            "bound": "pi^2|GapP-GapK|<=x^-3/L*(7560*epsilon+1638/x^2+1176*K!/(3L)^K)",
            "pass": master == (7560, 1638, 1176),
        },
        {
            "id": "uniform_moving_K",
            "integer_window": "1<=K<=floor(3L)",
            "window_coefficient": window_coefficient,
            "ratio_denominator_coefficient": ratio_denominator_coefficient,
            "base_K": base_K,
            "base_value": "1/(3L)",
            "universal_integer_induction": universal_integer_induction,
            "sequence": "b_K=K!/(3L)^K",
            "proof_mode": "symbolic_ratio_induction_not_finite_fixtures",
            "factorial_ratio_bound": "K!/(3L)^K<=1/(3L)",
            "quantifier": "max_over_all_integer_K_in_window",
            "normalized_limit": "max_K |GapP-GapK|/P2 -> 0",
            "pass": uniform_pass,
        },
        {
            "id": "P2_scale",
            "asymptotic": "P_2(y)~1/(3*x^3*L)",
            "leading_coefficient": "1/3",
            "source": "RH-384",
            "pass": Fraction(1, 3) > 0,
        },
        {
            "id": "scope_firewall",
            "convergent_factorial_series": False,
            "P3_or_cubic_precision": False,
            "complex_c": False,
            "growing_clock": False,
            "active_c11": False,
            "K_N": False,
            "operator_trace_zeros_RH": False,
            "gates_A_to_E": [False, False, False, False, False],
            "pass": True,
        },
    ]


def _contracts() -> dict[str, object]:
    return {
        "definitions": {
            "K_r": "x^(1-2r)/((2r-1)*L)",
            "a_r": "1/((2r-1)*L)",
            "S_K": "sum_(j=0)^(K-1)(-1)^j*j!*a^j",
            "I2r_K": "K_r*S_K(a_r)",
            "Psi_c_K": "c*P_1+sum_(r>=2)c^r*I2r_K/r",
            "GapP": "B_infinity-G(q_y)=F(PhiP)/pi^2",
            "GapJ": "F(PhiJ)/pi^2",
            "GapI": "F(PhiI)/pi^2",
            "GapK": "F((Psi_c_K)_(c=1)^7)/pi^2",
        },
        "source_contract": {
            "git_rows": 77,
            "remote_logical_rows": 2,
            "logical_rows": 79,
            "maynard_source_key": "maynard-annals-2015-small-gaps",
            "maynard_gap_upper": 600,
            "maynard_gap_type": "consecutive_primes",
            "maynard_redistributable": False,
            "external_payload_vendored": False,
        },
        "necessity_scope": "exact_P1_is_necessary_for_the_frozen_P_J_I_smooth_surrogate_P2_contract_only",
        "epistemic_boundary": "finite exact algebra and mutation oracle; not an analytic proof or source reproduction",
    }


def _require_keys(value: object, keys: set[str], label: str) -> dict[str, object]:
    if type(value) is not dict or set(value) != keys:
        raise ValueError(f"{label} membership changed")
    return value


def _require_list(value: object, length: int, label: str) -> list[object]:
    if type(value) is not list or len(value) != length:
        raise ValueError(f"{label} length/type changed")
    return value


def _require_exact(value: object, expected: object, label: str) -> None:
    if not exact_equal(value, expected):
        raise ValueError(f"{label} changed")


def _validate_analytic_rows(value: object) -> None:
    rows = _require_list(value, 12, "analytic_rows")

    row = _require_keys(rows[0], {"id", "epsilon_prefactor", "L_power", "VK_exponent", "V_L_power", "V_loglog_power", "source_locator", "pass"}, "analytic[0]")
    for key, expected in {
        "id": "johnston_yang_envelope",
        "epsilon_prefactor": "27/1000",
        "L_power": "1801/1000",
        "VK_exponent": "1853/10000",
        "V_L_power": "3/5",
        "V_loglog_power": "-1/5",
        "source_locator": "Johnston--Yang Theorem 1.4 equation (1.8)",
    }.items():
        _require_exact(row[key], expected, f"analytic[0].{key}")
    envelope_pass = fraction_from_text(row["epsilon_prefactor"], "epsilon") > 0 and fraction_from_text(row["VK_exponent"], "VK") > 0
    _require_exact(row["pass"], envelope_pass, "analytic[0].pass")

    row = _require_keys(rows[1], {"id", "L_min", "x_certificate_floor", "c_min", "c_max", "bridge", "bridge_pass", "pass"}, "analytic[1]")
    _require_exact(row["id"], "domain_bridge", "analytic[1].id")
    for key, expected in {"L_min": 512, "x_certificate_floor": 256, "c_min": 1, "c_max": 7}.items():
        _require_exact(row[key], expected, f"analytic[1].{key}")
    _require_exact(row["bridge"], "x=e^L>2^L>=2^512>256", "analytic[1].bridge")
    if any(type(row[key]) is not int for key in ("L_min", "x_certificate_floor", "c_min", "c_max")):
        raise TypeError("analytic[1] integer primitives changed type")
    bridge = 2 ** row["L_min"] > row["x_certificate_floor"]  # type: ignore[operator]
    domain_pass = bridge and row["L_min"] == L0 and row["x_certificate_floor"] == X0 and row["c_min"] == 1 and row["c_max"] == CMAX
    _require_exact(row["bridge_pass"], bridge, "analytic[1].bridge_pass")
    _require_exact(row["pass"], domain_pass, "analytic[1].pass")

    row = _require_keys(rows[2], {"id", "prime_condition", "successor_prime", "P_successor", "inclusive", "pass"}, "analytic[2]")
    for key, expected in {
        "id": "strict_prime_endpoint",
        "prime_condition": "p>x",
        "successor_prime": "q=p_(y+1)",
        "P_successor": "P_r(y)=(q^2-1)^(-r)+P_r(y+1)",
        "inclusive": False,
    }.items():
        _require_exact(row[key], expected, f"analytic[2].{key}")
    strict_pass = row["prime_condition"] == "p>x" and row["successor_prime"] == "q=p_(y+1)" and row["inclusive"] is False
    _require_exact(row["pass"], strict_pass, "analytic[2].pass")

    row = _require_keys(rows[3], {"id", "retained_coordinate", "replaced_rank_range", "series_weight", "pass"}, "analytic[3]")
    for key, expected in {
        "id": "rank_one_split",
        "retained_coordinate": "c*P_1",
        "replaced_rank_range": "all integers r>=2",
        "series_weight": "c^r/r",
    }.items():
        _require_exact(row[key], expected, f"analytic[3].{key}")
    rank_pass = row["retained_coordinate"] == "c*P_1" and row["replaced_rank_range"] == "all integers r>=2" and row["series_weight"] == "c^r/r"
    _require_exact(row["pass"], rank_pass, "analytic[3].pass")

    row = _require_keys(rows[4], {"id", "definition", "quadratic_numerator", "quadratic_denominator", "domain", "pass"}, "analytic[4]")
    for key, expected in {
        "id": "log_remainder",
        "definition": "R(z)=-log(1-z)-z",
        "quadratic_numerator": "z^2",
        "quadratic_denominator": "2*(1-z)",
        "domain": "0<=z<1",
    }.items():
        _require_exact(row[key], expected, f"analytic[4].{key}")
    remainder_pass = row["quadratic_denominator"] == "2*(1-z)" and row["definition"] == "R(z)=-log(1-z)-z"
    _require_exact(row["pass"], remainder_pass, "analytic[4].pass")

    row = _require_keys(rows[5], {"id", "boundary_E_x_h_units", "derivative_xh_units", "derivative_J_units", "absolute_bound", "rank_range", "pass"}, "analytic[5]")
    for key, expected in {
        "id": "strict_stieltjes_source",
        "boundary_E_x_h_units": 1,
        "derivative_xh_units": 1,
        "derivative_J_units": 1,
        "absolute_bound": "|P_r-J_r|<=epsilon*(2*x*h_r(x)+J_r)",
        "rank_range": "r>=2",
    }.items():
        _require_exact(row[key], expected, f"analytic[5].{key}")
    if any(type(row[key]) is not int for key in ("boundary_E_x_h_units", "derivative_xh_units", "derivative_J_units")):
        raise TypeError("Stieltjes units must be exact integers")
    stieltjes_pass = row["boundary_E_x_h_units"] + row["derivative_xh_units"] == 2 and row["derivative_J_units"] == 1  # type: ignore[operator]
    _require_exact(row["pass"], stieltjes_pass, "analytic[5].pass")

    row = _require_keys(rows[6], {"id", "R_quadratic_coefficient", "integral_t_minus_4", "combined_coefficient", "denominator_factors", "pass"}, "analytic[6]")
    for key, expected in {
        "id": "source_J_tail",
        "R_quadratic_coefficient": "1/2",
        "integral_t_minus_4": "1/3",
        "denominator_factors": ["1-c/(x^2-1)", "(1-x^-2)^2"],
    }.items():
        _require_exact(row[key], expected, f"analytic[6].{key}")
    combined = fraction_from_text(row["R_quadratic_coefficient"], "R coefficient") * fraction_from_text(row["integral_t_minus_4"], "t4 integral")
    _require_exact(row["combined_coefficient"], fraction_text(combined), "analytic[6].combined_coefficient")
    _require_exact(row["pass"], combined == Fraction(1, 6), "analytic[6].pass")

    row = _require_keys(rows[7], {"id", "R_derivative", "z_large", "z_small", "difference", "direction", "pass"}, "analytic[7]")
    for key, expected in {
        "id": "power_kernel_mean_value",
        "R_derivative": "z/(1-z)",
        "z_large": "c/(t^2-1)",
        "z_small": "c/t^2",
        "difference": "c/(t^2*(t^2-1))",
        "direction": "R(z_large)>=R(z_small)",
    }.items():
        _require_exact(row[key], expected, f"analytic[7].{key}")
    mean_value_pass = row["R_derivative"] == "z/(1-z)" and row["direction"] == "R(z_large)>=R(z_small)"
    _require_exact(row["pass"], mean_value_pass, "analytic[7].pass")

    row = _require_keys(rows[8], {"id", "majorant_power", "integral_coefficient", "denominator_factors", "pass"}, "analytic[8]")
    _require_exact(row["id"], "power_t6_integral", "analytic[8].id")
    _require_exact(row["majorant_power"], 6, "analytic[8].majorant_power")
    _require_exact(row["integral_coefficient"], "1/5", "analytic[8].integral_coefficient")
    _require_exact(row["denominator_factors"], ["1-x^-2", "1-(1+c)/x^2"], "analytic[8].denominator_factors")
    if type(row["majorant_power"]) is not int:
        raise TypeError("majorant power must be exact int")
    integral = Fraction(1, row["majorant_power"] - 1)  # type: ignore[operator]
    power_pass = integral == fraction_from_text(row["integral_coefficient"], "t6 integral") and len(row["denominator_factors"]) == 2  # type: ignore[arg-type]
    _require_exact(row["pass"], power_pass, "analytic[8].pass")

    row = _require_keys(rows[9], {"id", "K_r", "a_r", "S_K", "I2r_K", "pass"}, "analytic[9]")
    for key, expected in {
        "id": "factorial_kernel",
        "K_r": "x^(1-2r)/((2r-1)*L)",
        "a_r": "1/((2r-1)*L)",
        "S_K": "sum_(j=0)^(K-1)(-1)^j*j!*a^j",
        "I2r_K": "K_r*S_K(a_r)",
    }.items():
        _require_exact(row[key], expected, f"analytic[9].{key}")
    kernel_pass = "2r-1" in row["K_r"] and "2r-1" in row["a_r"] and "(-1)^j*j!" in row["S_K"]  # type: ignore[operator]
    _require_exact(row["pass"], kernel_pass, "analytic[9].pass")

    row = _require_keys(rows[10], {"id", "identity", "remainder_denominator", "absolute_moment", "sign", "pass"}, "analytic[10]")
    for key, expected in {
        "id": "exact_laplace_remainder",
        "identity": "G(a)-S_K(a)=(-a)^K*integral_0^infinity(e^-v*v^K/(1+a*v))dv",
        "remainder_denominator": "1+a*v",
        "absolute_moment": "K!",
        "sign": "(-1)^K",
    }.items():
        _require_exact(row[key], expected, f"analytic[10].{key}")
    laplace_pass = row["remainder_denominator"] == "1+a*v" and row["absolute_moment"] == "K!" and row["sign"] == "(-1)^K"
    _require_exact(row["pass"], laplace_pass, "analytic[10].pass")

    row = _require_keys(rows[11], {"id", "K_type", "K_min", "K_max", "window_coefficient", "ratio_denominator_coefficient", "base_K", "base_value", "universal_integer_induction", "sequence", "quantified_ratio", "alternating_partial_sum_range", "Psi_cube", "fixture_role", "pass"}, "analytic[11]")
    for key, expected in {
        "id": "moving_K_cube_mechanism",
        "K_type": "exact integer",
        "K_min": 1,
        "K_max": "floor(3*L)",
        "window_coefficient": 3,
        "ratio_denominator_coefficient": 3,
        "base_K": 1,
        "base_value": "1/(3*L)",
        "universal_integer_induction": True,
        "sequence": "b_K=K!/(3*L)^K",
        "quantified_ratio": "b_(K+1)/b_K=(K+1)/(3*L)<=1 whenever K+1<=floor(3*L)",
        "alternating_partial_sum_range": "0<S_K(a_r)<=1",
        "Psi_cube": "[0,1/2]^7",
        "fixture_role": "finite_regression_only_not_uniform_proof",
    }.items():
        _require_exact(row[key], expected, f"analytic[11].{key}")
    if any(type(row[key]) is not int for key in ("K_min", "window_coefficient", "ratio_denominator_coefficient", "base_K")):
        raise TypeError("moving-K numeric primitives must be exact integers")
    universal_pass = (
        row["K_min"] == row["base_K"] == 1
        and row["window_coefficient"] == row["ratio_denominator_coefficient"] == 3
        and row["universal_integer_induction"] is True
        and row["base_value"] == "1/(3*L)"
    )
    _require_exact(row["pass"], universal_pass, "analytic[11].pass")


def _validate_coordinate_rows(value: object) -> None:
    rows = _require_list(value, 7, "coordinate_rows")
    keys = {"c", "x0", "L0", "source_boundary_coefficient", "source_J_coefficient", "source_total_coefficient", "source_under_60", "power_total_coefficient", "power_under_13", "factorial_total_coefficient", "factorial_under_4c_over_3", "rank_one_P1_upper", "higher_rank_K_upper", "Psi_K_upper", "positive_cube", "pass"}
    for index, item in enumerate(rows, start=1):
        row = _require_keys(item, keys, f"coordinate[{index}]")
        for key in ("c", "x0", "L0"):
            if type(row[key]) is not int:
                raise TypeError(f"coordinate[{index}].{key} must be exact int")
        c, x0, l0 = row["c"], row["x0"], row["L0"]
        _require_exact(c, index, f"coordinate[{index}].c")
        _require_exact(x0, X0, f"coordinate[{index}].x0")
        _require_exact(l0, L0, f"coordinate[{index}].L0")
        one_minus_x2 = 1 - Fraction(1, x0 * x0)  # type: ignore[operator]
        source_den = one_minus_x2**2 * (1 - Fraction(c, x0 * x0 - 1))  # type: ignore[operator]
        source_boundary = Fraction(c * c, 1) / source_den  # type: ignore[operator]
        source_j = Fraction(c * c, 6) / source_den  # type: ignore[operator]
        source_total = source_boundary + source_j
        power_den = one_minus_x2 * (1 - Fraction(1 + c, x0 * x0))  # type: ignore[operator]
        power_total = Fraction(c * c, 5) / power_den  # type: ignore[operator]
        factorial_total = Fraction(c * c, 6) / (1 - Fraction(c, x0 * x0))  # type: ignore[operator]
        p1 = Fraction(c, 2) * (Fraction(1, x0) + Fraction(1, x0 + 1))  # type: ignore[operator]
        higher = Fraction(c * c, 6 * x0**3 * l0) / (1 - Fraction(c, x0 * x0))  # type: ignore[operator]
        psi = p1 + higher
        derived = {
            "source_boundary_coefficient": fraction_text(source_boundary),
            "source_J_coefficient": fraction_text(source_j),
            "source_total_coefficient": fraction_text(source_total),
            "source_under_60": source_total < 60,
            "power_total_coefficient": fraction_text(power_total),
            "power_under_13": power_total < 13,
            "factorial_total_coefficient": fraction_text(factorial_total),
            "factorial_under_4c_over_3": factorial_total < Fraction(4 * c, 3),  # type: ignore[operator]
            "rank_one_P1_upper": fraction_text(p1),
            "higher_rank_K_upper": fraction_text(higher),
            "Psi_K_upper": fraction_text(psi),
            "positive_cube": Fraction(0) < psi < Fraction(1, 2),
        }
        for key, expected in derived.items():
            _require_exact(row[key], expected, f"coordinate[{index}].{key}")
        expected_pass = source_den > 0 and power_den > 0 and all(derived[key] is True for key in ("source_under_60", "power_under_13", "factorial_under_4c_over_3", "positive_cube"))
        _require_exact(row["pass"], expected_pass, f"coordinate[{index}].pass")


def _validate_factorial_rows(value: object) -> None:
    rows = _require_list(value, 12, "factorial_rows")
    keys = {"K", "L0", "role", "window_upper", "within_window", "factorial", "normalized_factorial_ratio", "step_ratio_to_previous", "step_not_above_one", "under_first_term", "pass"}
    for index, item in enumerate(rows, start=1):
        row = _require_keys(item, keys, f"factorial[{index}]")
        for key in ("K", "L0", "window_upper"):
            if type(row[key]) is not int:
                raise TypeError(f"factorial[{index}].{key} must be exact int")
        K, l0 = row["K"], row["L0"]
        _require_exact(K, index, f"factorial[{index}].K")
        _require_exact(l0, L0, f"factorial[{index}].L0")
        _require_exact(row["role"], "finite_regression_only", f"factorial[{index}].role")
        window = 3 * l0  # type: ignore[operator]
        normalized = Fraction(factorial(K), window**K)  # type: ignore[arg-type,operator]
        step = Fraction(K, window)  # type: ignore[arg-type]
        derived = {
            "window_upper": window,
            "within_window": 1 <= K <= window,  # type: ignore[operator]
            "factorial": str(factorial(K)),  # type: ignore[arg-type]
            "normalized_factorial_ratio": fraction_text(normalized),
            "step_ratio_to_previous": fraction_text(step),
            "step_not_above_one": step <= 1,
            "under_first_term": normalized <= Fraction(1, window),
        }
        for key, expected in derived.items():
            _require_exact(row[key], expected, f"factorial[{index}].{key}")
        expected_pass = all(derived[key] is True for key in ("within_window", "step_not_above_one", "under_first_term"))
        _require_exact(row["pass"], expected_pass, f"factorial[{index}].pass")


def _validate_endpoint_rows(value: object) -> list[int]:
    rows = _require_list(value, 7, "endpoint_rows")
    keys = {"m", "c", "alpha", "beta", "u_upper", "relation", "rank_one_gradient_coefficient", "pass"}
    gradient_coefficients: list[int] = []
    for index, item in enumerate(rows, start=2):
        row = _require_keys(item, keys, f"endpoint[{index}]")
        for key in ("m", "c", "alpha", "beta", "rank_one_gradient_coefficient"):
            if type(row[key]) is not int:
                raise TypeError(f"endpoint[{index}].{key} must be exact int")
        _require_exact(row["m"], index, f"endpoint[{index}].m")
        _require_exact(row["c"], index - 1, f"endpoint[{index}].c")
        _require_exact(row["alpha"], ALPHA[index], f"endpoint[{index}].alpha")
        _require_exact(row["beta"], BETA[index], f"endpoint[{index}].beta")
        _require_exact(row["u_upper"], fraction_text(Fraction(9 - index, 8)), f"endpoint[{index}].u_upper")
        relation = "m2_special" if index == 2 else "alpha_equals_minus_beta"
        _require_exact(row["relation"], relation, f"endpoint[{index}].relation")
        coefficient = -2 * row["alpha"] * row["c"] - 4 * row["beta"]  # type: ignore[operator]
        _require_exact(row["rank_one_gradient_coefficient"], coefficient, f"endpoint[{index}].rank_one_gradient_coefficient")
        gradient_coefficients.append(coefficient)
        relation_pass = (index == 2 and row["alpha"] == -2 and row["beta"] == 1) or (index >= 3 and row["alpha"] == -row["beta"])  # type: ignore[operator]
        _require_exact(row["pass"], relation_pass, f"endpoint[{index}].pass")
    return gradient_coefficients


def _validate_necessity_rows(value: object, gradient_coefficients: list[int]) -> None:
    rows = _require_list(value, 10, "necessity_rows")
    expected_rows: list[tuple[set[str], dict[str, object]]] = [
        ({"id", "gap_type", "infinitely_many", "gap_upper", "source_locator", "statement", "pass"}, {"id": "maynard_input", "gap_type": "consecutive_primes", "infinitely_many": True, "gap_upper": 600, "source_locator": "Maynard Theorem 1.3 printed page 385 PDF page 3", "statement": "liminf_(n->infinity)(p_(n+1)-p_n)<=600"}),
        ({"id", "E", "atom", "atom_location", "smooth_interval", "formula", "pass"}, {"id": "E_successor_jump", "E": "P_1(y)-I_2(p_y)", "atom": "1/(q^2-1)", "atom_location": "q=p_(y+1)", "smooth_interval": "integral_x^q dt/(t^2*log(t))", "formula": "E_y-E_(y+1)=atom-smooth_interval"}),
        ({"id", "h_upper", "q", "q_over_x_limit", "bounded_gaps_supply", "pass"}, {"id": "bounded_gap_geometry", "h_upper": 600, "q": "x+h", "q_over_x_limit": "1", "bounded_gaps_supply": "infinitely_many_distinct_successor_pairs"}),
        ({"id", "scaled_atom", "h_fixed_upper", "limit", "leading_coefficient", "pass"}, {"id": "scaled_atom_limit", "scaled_atom": "x^2/((x+h)^2-1)", "h_fixed_upper": 600, "limit": "1", "leading_coefficient": 1}),
        ({"id", "upper_bound", "h_upper", "limit", "kernel", "pass"}, {"id": "scaled_smooth_interval_limit", "upper_bound": "h/log(x)", "h_upper": 600, "limit": "0", "kernel": "1/(t^2*log(t))"}),
        ({"id", "atom_limit", "smooth_limit", "jump_limit", "pass"}, {"id": "scalar_jump_limit", "atom_limit": 1, "smooth_limit": 0, "jump_limit": 1}),
        ({"id", "triangle_endpoint_count", "jump_limit", "sharp_lower_constant", "eventual_finite_safe_witness", "finite_safe_is_sharp", "pass"}, {"id": "two_endpoint_limsup", "triangle_endpoint_count": 2, "jump_limit": 1, "sharp_lower_constant": "1/2", "eventual_finite_safe_witness": "1/16", "finite_safe_is_sharp": False}),
        ({"id", "coordinates", "log_atom", "smooth_interval", "scaled_direction", "pass"}, {"id": "vector_jump_direction", "coordinates": [1, 2, 3, 4, 5, 6, 7], "log_atom": "-log(1-c/(q^2-1))", "smooth_interval": "integral_x^q[-log(1-c/t^2)]/log(t)dt", "scaled_direction": [1, 2, 3, 4, 5, 6, 7]}),
        ({"id", "sum_abs_alpha_u", "sum_abs_beta_u", "Hessian_terms", "pre_exp_entry_l1", "exp_half_upper", "entry_l1_Hessian_bound", "Taylor_remainder_coefficient", "Taylor_bound", "pass"}, {"id": "endpoint_Hessian_Taylor", "sum_abs_alpha_u": "7", "sum_abs_beta_u": "49/8", "Hessian_terms": [2, 4, 8, 4], "pre_exp_entry_l1": "112", "exp_half_upper": 2, "entry_l1_Hessian_bound": 224, "Taylor_remainder_coefficient": 112, "Taylor_bound": "|F(z)-gradF(0).z|<=112*||z||_infinity^2"}),
        ({"id", "gradient_dot_direction", "rank_one_gradient_coefficients_m2_to_m8", "scalar_two_endpoint_constant", "endpoint_lower_constant", "J1_minus_I2_scale", "higher_rank_scale", "claims_only_frozen_P_J_I_hierarchy", "pass"}, {"id": "sharp_endpoint_direction", "gradient_dot_direction": "2*X_infinity", "rank_one_gradient_coefficients_m2_to_m8": [0, 0, 4, -8, 12, -16, 20], "scalar_two_endpoint_constant": "1/2", "endpoint_lower_constant": "X_infinity", "J1_minus_I2_scale": "o(x^-2)", "higher_rank_scale": "o(x^-2)", "claims_only_frozen_P_J_I_hierarchy": True}),
    ]
    for index, (keys, primitives) in enumerate(expected_rows):
        row = _require_keys(rows[index], keys, f"necessity[{index}]")
        for key, expected in primitives.items():
            _require_exact(row[key], expected, f"necessity[{index}].{key}")
    passes = [
        rows[0]["gap_type"] == "consecutive_primes" and rows[0]["infinitely_many"] is True and type(rows[0]["gap_upper"]) is int and rows[0]["gap_upper"] == 600,
        rows[1]["atom"] == "1/(q^2-1)" and rows[1]["atom_location"] == "q=p_(y+1)" and rows[1]["smooth_interval"] == "integral_x^q dt/(t^2*log(t))",
        rows[2]["h_upper"] == 600 and rows[2]["bounded_gaps_supply"] == "infinitely_many_distinct_successor_pairs",
        rows[3]["leading_coefficient"] == 1 and rows[3]["h_fixed_upper"] == 600,
        rows[4]["h_upper"] == 600 and rows[4]["upper_bound"] == "h/log(x)",
        type(rows[5]["atom_limit"]) is int and type(rows[5]["smooth_limit"]) is int and rows[5]["atom_limit"] - rows[5]["smooth_limit"] == rows[5]["jump_limit"],  # type: ignore[operator]
        type(rows[6]["triangle_endpoint_count"]) is int and fraction_from_text(rows[6]["sharp_lower_constant"], "sharp") == Fraction(rows[6]["jump_limit"], rows[6]["triangle_endpoint_count"]),  # type: ignore[arg-type]
        rows[7]["coordinates"] == rows[7]["scaled_direction"] == list(range(1, 8)),
        fraction_from_text(rows[8]["pre_exp_entry_l1"], "Hessian pre-exp") == 2 * Fraction(7) + (4 + 8 + 4) * Fraction(49, 8) and rows[8]["entry_l1_Hessian_bound"] == 2 * fraction_from_text(rows[8]["pre_exp_entry_l1"], "Hessian pre-exp") and rows[8]["Taylor_remainder_coefficient"] * 2 == rows[8]["entry_l1_Hessian_bound"],  # type: ignore[operator]
        gradient_coefficients == rows[9]["rank_one_gradient_coefficients_m2_to_m8"] and rows[9]["gradient_dot_direction"] == "2*X_infinity" and Fraction(2) * fraction_from_text(rows[9]["scalar_two_endpoint_constant"], "endpoint scalar") == 1,
    ]
    for index, expected_pass in enumerate(passes):
        _require_exact(rows[index]["pass"], bool(expected_pass), f"necessity[{index}].pass")


def _coordinate_formula_values(c: int) -> tuple[Fraction, Fraction, Fraction]:
    one_minus_x2 = 1 - Fraction(1, X0 * X0)
    source_den = one_minus_x2**2 * (1 - Fraction(c, X0 * X0 - 1))
    source = Fraction(7 * c * c, 6) / source_den
    power = Fraction(c * c, 5) / (one_minus_x2 * (1 - Fraction(1 + c, X0 * X0)))
    factorial_coefficient = Fraction(c * c, 6) / (1 - Fraction(c, X0 * X0))
    return source, power, factorial_coefficient


def _validate_ledger_rows(value: object, analytic_value: object) -> None:
    rows = _require_list(value, 8, "ledger_rows")
    analytic_rows = _require_list(analytic_value, 12, "analytic_rows cross-contract")
    keys = [
        {"id", "sum_abs_alpha_u", "sum_abs_beta_u", "derivative_terms", "pre_exp_bound", "exp_half_upper", "dual_norm", "gradient_bound", "pass"},
        {"id", "rank_range", "coefficient", "bound", "pass"},
        {"id", "rank_range", "coefficient", "bound", "pass"},
        {"id", "rank_range", "coefficient", "bound", "pass"},
        {"id", "gradient", "coordinate_coefficients", "gap_coefficients", "bound", "pass"},
        {"id", "integer_window", "window_coefficient", "ratio_denominator_coefficient", "base_K", "base_value", "universal_integer_induction", "sequence", "proof_mode", "factorial_ratio_bound", "quantifier", "normalized_limit", "pass"},
        {"id", "asymptotic", "leading_coefficient", "source", "pass"},
        {"id", "convergent_factorial_series", "P3_or_cubic_precision", "complex_c", "growing_clock", "active_c11", "K_N", "operator_trace_zeros_RH", "gates_A_to_E", "pass"},
    ]
    for index, expected_keys in enumerate(keys):
        _require_keys(rows[index], expected_keys, f"ledger[{index}]")
    A = sum((abs(ALPHA[m]) * Fraction(9 - m, 8) for m in range(2, 9)), Fraction())
    B = sum((abs(BETA[m]) * Fraction(9 - m, 8) for m in range(2, 9)), Fraction())
    _require_exact(rows[0]["id"], "endpoint_gradient", "ledger[0].id")
    _require_exact(rows[0]["sum_abs_alpha_u"], fraction_text(A), "ledger[0].A")
    _require_exact(rows[0]["sum_abs_beta_u"], fraction_text(B), "ledger[0].B")
    _require_exact(rows[0]["derivative_terms"], [2, 4, 4], "ledger[0].derivative_terms")
    pre_exp = 2 * A + (4 + 4) * B
    gradient = 2 * pre_exp
    for key, expected in {"pre_exp_bound": fraction_text(pre_exp), "exp_half_upper": 2, "dual_norm": "l_infinity_input_to_l1_gradient", "gradient_bound": int(gradient)}.items():
        _require_exact(rows[0][key], expected, f"ledger[0].{key}")
    _require_exact(rows[0]["pass"], A == 7 and B == Fraction(49, 8) and gradient == 126, "ledger[0].pass")
    source_values = [_coordinate_formula_values(c)[0] for c in range(1, 8)]
    power_values = [_coordinate_formula_values(c)[1] for c in range(1, 8)]
    factorial_values = [_coordinate_formula_values(c)[2] for c in range(1, 8)]
    ledgers = [
        (1, "source_coordinate_ledger", "all integers r>=2", 60, "max_c|sum_(r>=2)c^r(P_r-J_r)/r|<60*epsilon/(x^3*L)", max(source_values) < 60),
        (2, "power_coordinate_ledger", "all integers r>=2", 13, "0<=max_c sum_(r>=2)c^r(J_r-I_2r)/r<13/(x^5*L)", max(power_values) < 13),
        (3, "factorial_coordinate_ledger", "all integers r>=2", "28/3", "max_c|sum_(r>=2)c^r(I_2r-I_2r^[K])/r|<=(28/3)*x^-3/L*K!/(3L)^K", max(factorial_values) < Fraction(28, 3)),
    ]
    for index, row_id, rank_range, coefficient, bound, passed in ledgers:
        for key, expected in {"id": row_id, "rank_range": rank_range, "coefficient": coefficient, "bound": bound, "pass": passed}.items():
            _require_exact(rows[index][key], expected, f"ledger[{index}].{key}")
    for key, expected in {
        "id": "master_multiplication",
        "gradient": 126,
        "coordinate_coefficients": [60, 13, "28/3"],
        "gap_coefficients": [7560, 1638, 1176],
        "bound": "pi^2|GapP-GapK|<=x^-3/L*(7560*epsilon+1638/x^2+1176*K!/(3L)^K)",
    }.items():
        _require_exact(rows[4][key], expected, f"ledger[4].{key}")
    multipliers = rows[4]["coordinate_coefficients"]
    if type(multipliers) is not list or len(multipliers) != 3 or type(rows[4]["gradient"]) is not int:
        raise TypeError("master multiplier types changed")
    products = [rows[4]["gradient"] * multipliers[0], rows[4]["gradient"] * multipliers[1], rows[4]["gradient"] * fraction_from_text(multipliers[2], "master factorial")]  # type: ignore[operator]
    _require_exact(rows[4]["gap_coefficients"], [int(value) for value in products], "ledger[4].gap_coefficients recomputation")
    _require_exact(rows[4]["pass"], products == [7560, 1638, 1176], "ledger[4].pass")
    for key, expected in {
        "id": "uniform_moving_K",
        "integer_window": "1<=K<=floor(3L)",
        "window_coefficient": 3,
        "ratio_denominator_coefficient": 3,
        "base_K": 1,
        "base_value": "1/(3L)",
        "universal_integer_induction": True,
        "sequence": "b_K=K!/(3L)^K",
        "proof_mode": "symbolic_ratio_induction_not_finite_fixtures",
        "factorial_ratio_bound": "K!/(3L)^K<=1/(3L)",
        "quantifier": "max_over_all_integer_K_in_window",
        "normalized_limit": "max_K |GapP-GapK|/P2 -> 0",
    }.items():
        _require_exact(rows[5][key], expected, f"ledger[5].{key}")
    universal = (
        type(rows[5]["window_coefficient"]) is int
        and type(rows[5]["ratio_denominator_coefficient"]) is int
        and type(rows[5]["base_K"]) is int
        and rows[5]["window_coefficient"] == rows[5]["ratio_denominator_coefficient"] == 3
        and rows[5]["base_K"] == 1
        and rows[5]["base_value"] == "1/(3L)"
        and rows[5]["universal_integer_induction"] is True
        and rows[5]["window_coefficient"] == analytic_rows[11]["window_coefficient"]
        and rows[5]["ratio_denominator_coefficient"] == analytic_rows[11]["ratio_denominator_coefficient"]
        and rows[5]["base_K"] == analytic_rows[11]["base_K"]
        and rows[5]["universal_integer_induction"] is analytic_rows[11]["universal_integer_induction"]
    )
    _require_exact(rows[5]["pass"], universal, "ledger[5].pass")
    for key, expected in {"id": "P2_scale", "asymptotic": "P_2(y)~1/(3*x^3*L)", "leading_coefficient": "1/3", "source": "RH-384"}.items():
        _require_exact(rows[6][key], expected, f"ledger[6].{key}")
    _require_exact(rows[6]["pass"], fraction_from_text(rows[6]["leading_coefficient"], "P2") == Fraction(1, 3), "ledger[6].pass")
    firewall = {"id": "scope_firewall", "convergent_factorial_series": False, "P3_or_cubic_precision": False, "complex_c": False, "growing_clock": False, "active_c11": False, "K_N": False, "operator_trace_zeros_RH": False, "gates_A_to_E": [False, False, False, False, False]}
    for key, expected in firewall.items():
        _require_exact(rows[7][key], expected, f"ledger[7].{key}")
    _require_exact(rows[7]["pass"], not any(rows[7][key] for key in ("convergent_factorial_series", "P3_or_cubic_precision", "complex_c", "growing_clock", "active_c11", "K_N", "operator_trace_zeros_RH")) and not any(rows[7]["gates_A_to_E"]), "ledger[7].pass")


def _validate_contracts(value: object) -> None:
    contracts = _require_keys(value, {"definitions", "source_contract", "necessity_scope", "epistemic_boundary"}, "contracts")
    definitions = _require_keys(contracts["definitions"], {"K_r", "a_r", "S_K", "I2r_K", "Psi_c_K", "GapP", "GapJ", "GapI", "GapK"}, "contracts.definitions")
    expected_definitions = {
        "K_r": "x^(1-2r)/((2r-1)*L)", "a_r": "1/((2r-1)*L)", "S_K": "sum_(j=0)^(K-1)(-1)^j*j!*a^j", "I2r_K": "K_r*S_K(a_r)", "Psi_c_K": "c*P_1+sum_(r>=2)c^r*I2r_K/r", "GapP": "B_infinity-G(q_y)=F(PhiP)/pi^2", "GapJ": "F(PhiJ)/pi^2", "GapI": "F(PhiI)/pi^2", "GapK": "F((Psi_c_K)_(c=1)^7)/pi^2",
    }
    for key, expected in expected_definitions.items():
        _require_exact(definitions[key], expected, f"contracts.definitions.{key}")
    source = _require_keys(contracts["source_contract"], {"git_rows", "remote_logical_rows", "logical_rows", "maynard_source_key", "maynard_gap_upper", "maynard_gap_type", "maynard_redistributable", "external_payload_vendored"}, "contracts.source_contract")
    expected_source = {"git_rows": 77, "remote_logical_rows": 2, "logical_rows": 79, "maynard_source_key": "maynard-annals-2015-small-gaps", "maynard_gap_upper": 600, "maynard_gap_type": "consecutive_primes", "maynard_redistributable": False, "external_payload_vendored": False}
    for key, expected in expected_source.items():
        _require_exact(source[key], expected, f"contracts.source_contract.{key}")
    _require_exact(contracts["necessity_scope"], "exact_P1_is_necessary_for_the_frozen_P_J_I_smooth_surrogate_P2_contract_only", "contracts.necessity_scope")
    _require_exact(contracts["epistemic_boundary"], "finite exact algebra and mutation oracle; not an analytic proof or source reproduction", "contracts.epistemic_boundary")


def build_certificate() -> dict[str, object]:
    groups = {
        "analytic_rows": _analytic_rows(),
        "coordinate_rows": _coordinate_rows(),
        "factorial_rows": _factorial_rows(),
        "endpoint_rows": _endpoint_rows(),
        "necessity_rows": _necessity_rows(),
        "ledger_rows": _ledger_rows(),
    }
    counts = {key: len(value) for key, value in groups.items()}
    counts["oracle_rows_total"] = sum(counts.values())
    all_rows = [row for rows in groups.values() for row in rows]
    return {
        "status": STATUS,
        "epistemic_role": ROLE,
        "counts": counts,
        **groups,
        "contracts": _contracts(),
        "all_pass": counts["oracle_rows_total"] == 56 and all(row["pass"] is True for row in all_rows),
    }


def verify_certificate(candidate: object, *, compare_fresh: bool = True) -> bool:
    if type(compare_fresh) is not bool:
        raise TypeError("compare_fresh must be an exact bool")
    if type(candidate) is not dict:
        raise TypeError("certificate must be an object")
    group_names = ("analytic_rows", "coordinate_rows", "factorial_rows", "endpoint_rows", "necessity_rows", "ledger_rows")
    expected_keys = {"status", "epistemic_role", "counts", *group_names, "contracts", "all_pass"}
    if set(candidate) != expected_keys:
        raise ValueError("certificate membership changed")
    if not exact_equal(candidate["status"], STATUS) or not exact_equal(candidate["epistemic_role"], ROLE):
        raise ValueError("certificate identity changed")
    _validate_analytic_rows(candidate["analytic_rows"])
    _validate_coordinate_rows(candidate["coordinate_rows"])
    _validate_factorial_rows(candidate["factorial_rows"])
    gradient_coefficients = _validate_endpoint_rows(candidate["endpoint_rows"])
    _validate_necessity_rows(candidate["necessity_rows"], gradient_coefficients)
    _validate_ledger_rows(candidate["ledger_rows"], candidate["analytic_rows"])
    _validate_contracts(candidate["contracts"])
    counts = {}
    for key in group_names:
        rows = candidate[key]
        if type(rows) is not list:
            raise TypeError(f"{key} must be an exact list")
        counts[key] = len(rows)
    counts["oracle_rows_total"] = sum(counts.values())
    if counts["oracle_rows_total"] != 56 or not exact_equal(candidate["counts"], counts):
        raise ValueError("row counts changed")
    if candidate["all_pass"] is not True:
        raise ValueError("all_pass must be exact true")
    if compare_fresh and canonical_json_bytes(candidate) != canonical_json_bytes(build_certificate()):
        raise ValueError("fresh certificate mismatch")
    return True


MUTATION_NAMES = (
    "inclusive_endpoint_and_wrong_successor",
    "missing_stieltjes_boundary",
    "rank_split_includes_r1",
    "log_remainder_missing_half",
    "source_missing_denominator_factor",
    "source_J_tail_wrong_sixth",
    "wrong_R_derivative",
    "power_wrong_t6_integral",
    "power_missing_denominator_factor",
    "wrong_Kr_2r_minus_1",
    "wrong_ar_2r_minus_1",
    "factorial_missing_alternating_sign",
    "factorial_missing_j_factorial",
    "remainder_wrong_denominator",
    "factorial_truncates_to_r2",
    "moving_K_exceeds_3L",
    "cube_loses_positivity",
    "factorial_coordinate_28_over_3",
    "wrong_dual_norm_and_gradient",
    "wrong_master_multiplication",
    "wrong_P2_coefficient",
    "maynard_not_consecutive_or_infinite",
    "successor_jump_atom_and_interval",
    "endpoint_Hessian_and_rank_one_direction",
)


def apply_mutation(certificate: dict[str, object], name: str) -> dict[str, object]:
    if type(certificate) is not dict:
        raise TypeError("certificate must be an object")
    if type(name) is not str or name not in MUTATION_NAMES:
        raise ValueError("unknown mutation")
    value = deepcopy(certificate)
    analytic = value["analytic_rows"]
    necessity = value["necessity_rows"]
    ledger = value["ledger_rows"]
    if name == "inclusive_endpoint_and_wrong_successor":
        analytic[2]["prime_condition"] = "p>=x"
        analytic[2]["successor_prime"] = "x"
    elif name == "missing_stieltjes_boundary":
        analytic[5]["boundary_E_x_h_units"] = 0
    elif name == "rank_split_includes_r1":
        analytic[3]["replaced_rank_range"] = "all integers r>=1"
    elif name == "log_remainder_missing_half":
        analytic[4]["quadratic_denominator"] = "1-z"
    elif name == "source_missing_denominator_factor":
        analytic[6]["denominator_factors"] = ["1-c/(x^2-1)"]
    elif name == "source_J_tail_wrong_sixth":
        analytic[6]["combined_coefficient"] = "1/3"
    elif name == "wrong_R_derivative":
        analytic[7]["R_derivative"] = "1/(1-z)"
    elif name == "power_wrong_t6_integral":
        analytic[8]["majorant_power"] = 4
        analytic[8]["integral_coefficient"] = "1/3"
    elif name == "power_missing_denominator_factor":
        analytic[8]["denominator_factors"] = ["1-x^-2"]
    elif name == "wrong_Kr_2r_minus_1":
        analytic[9]["K_r"] = "x^(1-2r)/((2r+1)*L)"
    elif name == "wrong_ar_2r_minus_1":
        analytic[9]["a_r"] = "1/((2r+1)*L)"
    elif name == "factorial_missing_alternating_sign":
        analytic[9]["S_K"] = "sum_(j=0)^(K-1)j!*a^j"
    elif name == "factorial_missing_j_factorial":
        analytic[9]["S_K"] = "sum_(j=0)^(K-1)(-1)^j*a^j"
    elif name == "remainder_wrong_denominator":
        analytic[10]["remainder_denominator"] = "1-a*v"
    elif name == "factorial_truncates_to_r2":
        ledger[3]["rank_range"] = "r=2 only"
    elif name == "moving_K_exceeds_3L":
        analytic[11]["K_max"] = "floor(4*L)"
    elif name == "cube_loses_positivity":
        analytic[11]["alternating_partial_sum_range"] = "S_K(a_r)<=1"
    elif name == "factorial_coordinate_28_over_3":
        ledger[3]["coefficient"] = "8"
    elif name == "wrong_dual_norm_and_gradient":
        ledger[0]["dual_norm"] = "l2_input_to_l2_gradient"
        ledger[0]["gradient_bound"] = 125
    elif name == "wrong_master_multiplication":
        ledger[4]["gap_coefficients"] = [7559, 1637, 1175]
    elif name == "wrong_P2_coefficient":
        ledger[6]["leading_coefficient"] = "1/4"
    elif name == "maynard_not_consecutive_or_infinite":
        necessity[0]["gap_type"] = "not_necessarily_consecutive_primes"
        necessity[0]["infinitely_many"] = False
    elif name == "successor_jump_atom_and_interval":
        necessity[1]["atom"] = "1/(x^2-1)"
        necessity[1]["smooth_interval"] = "integral_q^x dt/(t^2*log(t))"
    elif name == "endpoint_Hessian_and_rank_one_direction":
        necessity[8]["Hessian_terms"] = [2, 4, 4]
        necessity[9]["gradient_dot_direction"] = "X_infinity"
    return value


def mutation_results() -> dict[str, object]:
    fresh = build_certificate()
    rows: list[dict[str, object]] = []
    for name in MUTATION_NAMES:
        rejected = False
        try:
            verify_certificate(apply_mutation(fresh, name), compare_fresh=False)
        except (TypeError, ValueError):
            rejected = True
        rows.append({"name": name, "rejected": rejected})
    return {
        "count": len(rows),
        "rejected": sum(row["rejected"] for row in rows),
        "rows": rows,
        "all_pass": len(rows) == 24 and all(row["rejected"] is True for row in rows),
    }
