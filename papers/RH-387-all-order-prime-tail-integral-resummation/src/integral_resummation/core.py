"""Exact symbolic certificate for RH-387.

The finite artifact checks algebraic interfaces only.  It does not prove the
Johnston--Yang estimate, Tonelli's theorem, Stieltjes integration, or an
asymptotic limit.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json


STATUS = "RH-387_all_order_prime_tail_integral_resummation"
ROLE = "reproduction_not_analytic_proof"
X0 = 256
L0 = 512
DEGREE = 4
ALPHA = {2: -2, 3: 2, 4: -2, 5: 2, 6: -2, 7: 2, 8: -2}
BETA = {2: 1, 3: -2, 4: 2, 5: -2, 6: 2, 7: -2, 8: 2}
TAILS = {
    "single": (Fraction(1, 24),),
    "triple": (Fraction(1, 24), Fraction(1, 48), Fraction(1, 120)),
}


def fraction_text(value: Fraction) -> str:
    if type(value) is not Fraction:
        raise TypeError("exact Fraction required")
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def fraction_from_text(value: object, label: str) -> Fraction:
    if type(value) is not str or not value:
        raise TypeError(f"{label} must be an exact fraction string")
    if "/" in value:
        parts = value.split("/")
        if len(parts) != 2:
            raise ValueError(f"{label} is malformed")
        numerator, denominator = parts
        if denominator.startswith(("+", "-")) or not denominator.isdigit() or int(denominator) == 0:
            raise ValueError(f"{label} denominator is malformed")
        if numerator.startswith("-"):
            digits = numerator[1:]
        else:
            digits = numerator
        if not digits.isdigit():
            raise ValueError(f"{label} numerator is malformed")
        parsed = Fraction(int(numerator), int(denominator))
    else:
        if value.startswith("-"):
            digits = value[1:]
        else:
            digits = value
        if not digits.isdigit():
            raise ValueError(f"{label} is malformed")
        parsed = Fraction(int(value))
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
        raise TypeError("JSON input must be text")

    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        output: dict[str, object] = {}
        for key, value in items:
            if key in output:
                raise ValueError(f"duplicate JSON key: {key}")
            output[key] = value
        return output

    def bad(value: str) -> object:
        raise ValueError(f"non-finite JSON constant: {value}")

    value = json.loads(text, object_pairs_hook=pairs, parse_constant=bad)
    if type(value) is not dict:
        raise TypeError("top-level JSON value must be an object")
    return value


def _poly_exp(log_coefficients: list[Fraction]) -> list[Fraction]:
    output = [Fraction(1)] + [Fraction(0)] * DEGREE
    for n in range(1, DEGREE + 1):
        output[n] = sum(k * log_coefficients[k] * output[n - k] for k in range(1, n + 1)) / n
    return output


def _direct_product_coefficients(c: int, weights: tuple[Fraction, ...]) -> list[Fraction]:
    output = [Fraction(1)] + [Fraction(0)] * DEGREE
    for weight in weights:
        previous = output
        output = [Fraction(0)] * (DEGREE + 1)
        for n in range(DEGREE + 1):
            output[n] = sum(previous[n - k] * (c * weight) ** k for k in range(n + 1))
    return output


def _analytic_rows() -> list[dict[str, object]]:
    return [
        {"id": "source_envelope", "epsilon_prefactor": "27/1000", "L_power": "1801/1000", "VK_exponent": "1853/10000", "V_L_power": "3/5", "V_loglog_power": "-1/5", "pass": True},
        {"id": "domain", "L_min": L0, "x_certificate_floor": X0, "c_min": 1, "c_max": 7, "c_type": "exact integer", "bridge": "x=e^L>2^L>=2^512>256 because e>2", "bridge_pass": 2**L0 > X0, "pass": L0 == 512 and X0 == 256 and 2**L0 > X0},
        {"id": "strict_endpoint", "prime_condition": "p>x", "successor": "p_(y+1)", "inclusive": False, "pass": True},
        {"id": "PhiP", "formula": "sum_(r>=1)c^r*P_r/r", "series_divisor": "r", "sign": 1, "pass": True},
        {"id": "PhiJ", "formula": "integral_x^infinity[-log(1-c/(t^2-1))]/log(t)dt", "kernel_denominator": "t^2-1", "pass": True},
        {"id": "PhiI", "formula": "integral_x^infinity[-log(1-c/t^2)]/log(t)dt", "kernel_denominator": "t^2", "pass": True},
        {"id": "tonelli", "atom_upper": "7/24", "atom_strictly_below_one": True, "rearrangement": "nonnegative_absolute_majorant", "pass": True},
        {"id": "strict_stieltjes", "boundary_xh_units": 1, "integral_xh_units": 1, "integral_J_units": 1, "combined": "2*x*h+J", "pass": True},
        {"id": "source_coordinate", "per_c_coefficient": 4, "max_c": 7, "sup_coefficient": 28, "bound": "max_c|PhiP-PhiJ|<=28*epsilon/(x*L)", "pass": True},
        {"id": "power_coordinate", "direction": "PhiJ>=PhiI", "per_c_numerator": 2, "per_c_denominator": 3, "max_bound": "14/3", "bound": "max_c(PhiJ-PhiI)<=14/(3*x^3*L)", "pass": True},
        {"id": "path_cube", "dimension": 7, "lower": "0", "upper": "1/2", "integer_tail_identity": "sum_(n>x)1/(n^2-1)=(1/x+1/(x+1))/2", "pass": True},
        {"id": "endpoint_identity", "scaled_quantity": "pi^2*(B_infinity-G(q_y))", "value": "F(PhiP)", "pi_squared_retained": True, "pass": True},
    ]


def _channel_rows() -> list[dict[str, object]]:
    rows = []
    integer_tail = Fraction(1, 2) * (Fraction(1, X0) + Fraction(1, X0 + 1))
    for c in range(1, 8):
        denominator = 1 - Fraction(1 + c, X0 * X0)
        p_bound = Fraction(c, 1) / (1 - Fraction(c, X0 * X0 - 1)) * integer_tail
        j_bound = Fraction(c, X0 * L0) / denominator
        i_bound = Fraction(c, X0 * L0) / (1 - Fraction(c, X0 * X0))
        source_exact = Fraction(3 * c, 1) / denominator
        power_exact = Fraction(c, 3) / denominator
        all_below_half = max(p_bound, j_bound, i_bound) < Fraction(1, 2)
        source_below = denominator > 0 and source_exact < 4 * c
        power_below = denominator > 0 and power_exact < Fraction(2 * c, 3)
        rows.append({
            "c": c,
            "x0": X0,
            "L0": L0,
            "P_coordinate_upper": fraction_text(p_bound),
            "J_coordinate_upper": fraction_text(j_bound),
            "I_coordinate_upper": fraction_text(i_bound),
            "all_below_half": all_below_half,
            "source_exact_coefficient": fraction_text(source_exact),
            "source_below_4c": source_below,
            "power_exact_coefficient": fraction_text(power_exact),
            "power_below_2c_over_3": power_below,
            "pass": denominator > 0 and all_below_half and source_below and power_below,
        })
    return rows


def _endpoint_rows() -> list[dict[str, object]]:
    rows = []
    for m in range(2, 9):
        rows.append({
            "m": m,
            "c": m - 1,
            "alpha": ALPHA[m],
            "beta": BETA[m],
            "u_upper": fraction_text(Fraction(9 - m, 8)),
            "relation": "m2_special" if m == 2 else "alpha_equals_minus_beta",
            "pass": (m == 2 and ALPHA[m] == -2 and BETA[m] == 1) or (m >= 3 and ALPHA[m] == -BETA[m]),
        })
    return rows


def _resummation_rows() -> list[dict[str, object]]:
    rows = []
    for tail_name, weights in TAILS.items():
        for c in range(1, 8):
            power_sums = [Fraction(0)] + [sum((w**r for w in weights), Fraction()) for r in range(1, DEGREE + 1)]
            log_coefficients = [Fraction(0)] + [Fraction(c**r, r) * power_sums[r] for r in range(1, DEGREE + 1)]
            compiled = _poly_exp(log_coefficients)
            direct = _direct_product_coefficients(c, weights)
            rows.append({
                "tail": tail_name,
                "c": c,
                "degree": DEGREE,
                "weights": [fraction_text(w) for w in weights],
                "power_sums": [fraction_text(v) for v in power_sums[1:]],
                "log_coefficients": [fraction_text(v) for v in log_coefficients[1:]],
                "compiled_product_coefficients": [fraction_text(v) for v in compiled],
                "direct_product_coefficients": [fraction_text(v) for v in direct],
                "pass": compiled == direct and max(c * w for w in weights) < 1,
            })
    return rows


def _ledger_rows() -> list[dict[str, object]]:
    alpha_ledger = sum((abs(ALPHA[m]) * Fraction(9 - m, 8) for m in range(2, 9)), Fraction())
    beta_ledger = sum((abs(BETA[m]) * Fraction(9 - m, 8) for m in range(2, 9)), Fraction())
    derivative_terms = (2, 4, 4)
    gradient_before_exp = derivative_terms[0] * alpha_ledger + (derivative_terms[1] + derivative_terms[2]) * beta_ledger
    gradient = 2 * gradient_before_exp
    return [
        {"id": "gradient", "sum_abs_alpha_u": fraction_text(alpha_ledger), "sum_abs_beta_u": fraction_text(beta_ledger), "derivative_terms": list(derivative_terms), "pre_exp_bound": fraction_text(gradient_before_exp), "cube_exp_upper": "exp(1/2)<2", "exp_half_upper": 2, "l1_gradient_bound": int(gradient), "norm_pair": "l_infinity_to_l1", "pass": derivative_terms == (2, 4, 4) and gradient_before_exp == 63 and gradient == 126},
        {"id": "master", "source_coordinate": 28, "power_coordinate": "14/3", "gradient": 126, "source_gap_coefficient": 3528, "power_gap_coefficient": 588, "source_bound": "pi^2*|GapP-GapJ|<=3528*epsilon/(x*L)", "power_bound": "pi^2*|GapJ-GapI|<=588/(x^3*L)", "combined_bound": "pi^2*|GapP-GapI|<=3528*epsilon/(x*L)+588/(x^3*L)", "pass": 126 * 28 == 3528 and Fraction(126) * Fraction(14, 3) == 588},
    ]


def _contracts() -> dict[str, object]:
    return {
        "endpoint_map": "F(z)=2*(C(u)-C(u_m*exp(z_(m-1))))-4*W(u_m*exp(z))*(1-exp(-z_1))",
        "gap_definitions": {"GapP": "B_infinity-G(q_y)=F(PhiP)/pi^2", "GapJ": "F(PhiJ)/pi^2", "GapI": "F(PhiI)/pi^2"},
        "novelty": "r-infinite_and_partition-infinite_source-limit_exchange_plus_endpoint_Lipschitz",
        "route": {"A_all_order_resummation": "GO", "B_second_order_precision": "STOP_SCOPED"},
        "claim_boundary": {
            "second_order_or_P2_precision": False,
            "complex_c": False,
            "active_c11": False,
            "growing_clock": False,
            "operator_trace_zeros_RH": False,
            "gates_A_to_E": [False, False, False, False, False],
        },
    }


def build_certificate() -> dict[str, object]:
    analytic = _analytic_rows()
    channels = _channel_rows()
    endpoint = _endpoint_rows()
    resummation = _resummation_rows()
    ledger = _ledger_rows()
    counts = {
        "analytic_rows": len(analytic),
        "channel_rows": len(channels),
        "endpoint_rows": len(endpoint),
        "resummation_rows": len(resummation),
        "ledger_rows": len(ledger),
        "oracle_rows_total": len(analytic) + len(channels) + len(endpoint) + len(resummation) + len(ledger),
    }
    return {
        "status": STATUS,
        "epistemic_role": ROLE,
        "counts": counts,
        "analytic_rows": analytic,
        "channel_rows": channels,
        "endpoint_rows": endpoint,
        "resummation_rows": resummation,
        "ledger_rows": ledger,
        "contracts": _contracts(),
        "all_pass": counts["oracle_rows_total"] == 42 and all(row["pass"] is True for group in (analytic, channels, endpoint, resummation, ledger) for row in group),
    }


def verify_certificate(candidate: object, *, compare_fresh: bool = True) -> bool:
    if type(compare_fresh) is not bool:
        raise TypeError("compare_fresh must be an exact bool")
    if type(candidate) is not dict:
        raise TypeError("certificate must be an object")
    expected_keys = {"status", "epistemic_role", "counts", "analytic_rows", "channel_rows", "endpoint_rows", "resummation_rows", "ledger_rows", "contracts", "all_pass"}
    if set(candidate) != expected_keys:
        raise ValueError("certificate membership changed")
    expected_groups = {
        "analytic_rows": _analytic_rows(),
        "channel_rows": _channel_rows(),
        "endpoint_rows": _endpoint_rows(),
        "resummation_rows": _resummation_rows(),
        "ledger_rows": _ledger_rows(),
    }
    if not exact_equal(candidate["status"], STATUS) or not exact_equal(candidate["epistemic_role"], ROLE):
        raise ValueError("certificate identity changed")
    for key, expected in expected_groups.items():
        if not exact_equal(candidate[key], expected):
            raise ValueError(f"{key} semantic oracle failed")
    counts = {key: len(value) for key, value in expected_groups.items()}
    counts["oracle_rows_total"] = sum(counts.values())
    if not exact_equal(candidate["counts"], counts) or counts["oracle_rows_total"] != 42:
        raise ValueError("row counts changed")
    if not exact_equal(candidate["contracts"], _contracts()):
        raise ValueError("contracts changed")
    if candidate["all_pass"] is not True:
        raise ValueError("all_pass must be exact true")
    if compare_fresh and canonical_json_bytes(candidate) != canonical_json_bytes(build_certificate()):
        raise ValueError("fresh certificate mismatch")
    return True


MUTATION_NAMES = (
    "epsilon_prefactor", "epsilon_L_power", "VK_exponent", "V_loglog_sign",
    "L_domain", "c_range", "inclusive_endpoint", "missing_series_divisor",
    "log_product_sign", "tonelli_atom", "missing_boundary", "missing_2xh_plus_J",
    "source_per_c", "source_sup", "J_kernel_denominator", "I_kernel_denominator",
    "JI_direction", "JI_coefficient", "alpha_sign", "beta_sign",
    "endpoint_prefactor_2_to_1", "missing_loss_derivative", "wrong_norm_pair", "claim_P2_precision",
)


def apply_mutation(certificate: dict[str, object], name: str) -> dict[str, object]:
    if type(name) is not str or name not in MUTATION_NAMES:
        raise ValueError("unknown mutation")
    value = deepcopy(certificate)
    a = value["analytic_rows"]
    if name == "epsilon_prefactor": a[0]["epsilon_prefactor"] = "26/1000"
    elif name == "epsilon_L_power": a[0]["L_power"] = "1800/1000"
    elif name == "VK_exponent": a[0]["VK_exponent"] = "1852/10000"
    elif name == "V_loglog_sign": a[0]["V_loglog_power"] = "1/5"
    elif name == "L_domain": a[1]["L_min"] = 511
    elif name == "c_range": a[1]["c_max"] = 8
    elif name == "inclusive_endpoint": a[2]["prime_condition"] = "p>=x"
    elif name == "missing_series_divisor": a[3]["series_divisor"] = "1"
    elif name == "log_product_sign": a[3]["sign"] = -1
    elif name == "tonelli_atom": a[6]["atom_upper"] = "6/24"
    elif name == "missing_boundary": a[7]["boundary_xh_units"] = 0
    elif name == "missing_2xh_plus_J": a[7]["combined"] = "x*h+J"
    elif name == "source_per_c": a[8]["per_c_coefficient"] = 3
    elif name == "source_sup": a[8]["sup_coefficient"] = 21
    elif name == "J_kernel_denominator": a[4]["kernel_denominator"] = "t^2"
    elif name == "I_kernel_denominator": a[5]["kernel_denominator"] = "t^2-1"
    elif name == "JI_direction": a[9]["direction"] = "PhiJ<=PhiI"
    elif name == "JI_coefficient": a[9]["per_c_numerator"] = 1
    elif name == "alpha_sign": value["endpoint_rows"][1]["alpha"] *= -1
    elif name == "beta_sign": value["endpoint_rows"][2]["beta"] *= -1
    elif name == "endpoint_prefactor_2_to_1": value["contracts"]["endpoint_map"] = "F(z)=1*(C(u)-C(u_m*exp(z_(m-1))))-4*W(u_m*exp(z))*(1-exp(-z_1))"
    elif name == "missing_loss_derivative": value["ledger_rows"][0]["derivative_terms"] = [2, 4, 0]
    elif name == "wrong_norm_pair": value["ledger_rows"][0]["norm_pair"] = "l2_to_l2"
    elif name == "claim_P2_precision": value["contracts"]["claim_boundary"]["second_order_or_P2_precision"] = True
    return value


def mutation_results() -> dict[str, object]:
    fresh = build_certificate()
    rows = []
    for name in MUTATION_NAMES:
        rejected = False
        try:
            verify_certificate(apply_mutation(fresh, name), compare_fresh=False)
        except (TypeError, ValueError):
            rejected = True
        rows.append({"name": name, "rejected": rejected})
    return {"count": len(rows), "rejected": sum(row["rejected"] for row in rows), "rows": rows, "all_pass": len(rows) == 24 and all(row["rejected"] for row in rows)}
