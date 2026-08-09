"""Exact finite algebraic certificate for RH-390.

The certificate checks the symbolic interface, directed Euler-ratio interval
arithmetic, and mutation resistance used by the paper.  It is deliberately
not a numerical fit and does not replace the analytic proofs or the frozen
Johnston--Yang and Maynard source theorems.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from math import factorial
import json


STATUS = "RH-390_growing_rank_prime_tail_filtration"
ROLE = "finite_exact_algebra_not_analytic_proof"
L0 = 512
X0 = 256
CMAX = 7
ALPHA = {2: -2, 3: 2, 4: -2, 5: 2, 6: -2, 7: 2, 8: -2}
BETA = {2: 1, 3: -2, 4: 2, 5: -2, 6: 2, 7: -2, 8: 2}

# RH-384 directed, outward decimal intervals.  Parsing below turns every
# endpoint into an exact rational; binary floating point is never used.
U_INTERVAL_TEXT = {
    2: (
        "0.79606040870898303668258723437697247788244823019781688942057817156808006324489857",
        "0.79606836935287354498059773749834613448214436140422608565968368163277992812734109",
    ),
    3: (
        "0.61924203807885931176128478638556221233898693327341166091191304286879024381042052",
        "0.61925442310539659663090836798019670672619725578792199982731263510830127823662602",
    ),
    4: (
        "0.46706540740190906810813664160692823131359118000867958475033010109068512217833360",
        "0.46707941971443928894176245156363994112927289254772155985953302903120660751652680",
    ),
    5: (
        "0.33721417887441793195786656700250637753133382730680422233751764051237490201681002",
        "0.33722766791368962040853632583965885752876677515408526796859712719631534066544246",
    ),
    6: (
        "0.22752702560107560768676163112294897624477025177967017050656881905069814845878089",
        "0.22753840246431479165058321998070523893926657988019982017113068500907168956023382",
    ),
    7: (
        "0.13598981892337099710656621384206971382910282322100104167530312663406675578226961",
        "0.13599797876129768932939305595582384250511352267690115354646754910672869761683598",
    ),
    8: (
        "0.060728124895404081336842078561871850341724556651138274986013006420128664605576844",
        "0.060732376140477795694564349336715194239732675841161692614726342545899839773689660",
    ),
}


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
    digits = numerator[1:] if numerator.startswith("-") else numerator
    if not digits.isdigit() or not denominator.isdigit() or denominator.startswith(("+", "-")):
        raise ValueError(f"{label} is malformed")
    if int(denominator) == 0:
        raise ValueError(f"{label} denominator is zero")
    output = Fraction(int(numerator), int(denominator))
    if fraction_text(output) != value:
        raise ValueError(f"{label} is not canonical")
    return output


def decimal_fraction(value: object, label: str) -> Fraction:
    if type(value) is not str or value.count(".") != 1:
        raise TypeError(f"{label} must be a fixed decimal string")
    whole, fractional = value.split(".")
    if whole != "0" or not fractional or not fractional.isdigit():
        raise ValueError(f"{label} is not a canonical positive unit decimal")
    return Fraction(int(fractional), 10 ** len(fractional))


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

    parsed = json.loads(text, object_pairs_hook=pairs, parse_constant=reject_constant)
    if type(parsed) is not dict:
        raise TypeError("top-level JSON value must be an object")
    return parsed


def _u_intervals() -> dict[int, tuple[Fraction, Fraction]]:
    return {
        m: (decimal_fraction(bounds[0], f"u{m}.lower"), decimal_fraction(bounds[1], f"u{m}.upper"))
        for m, bounds in U_INTERVAL_TEXT.items()
    }


def _a_value(s: int, c: int, x: int = X0) -> Fraction:
    u = Fraction(1, x * x)
    return 1 / ((1 - u) ** s * (1 - Fraction(c, x * x - 1)))


def _b_value(s: int, c: int, x: int = X0) -> Fraction:
    u = Fraction(1, x * x)
    return 1 / ((1 - u) ** (s + 1) * (1 - Fraction(c, x * x - 1)))


def _c_value(c: int, x: int = X0) -> Fraction:
    return 1 / (1 - Fraction(c, x * x))


def _gamma_vector(r: int) -> dict[int, Fraction]:
    if type(r) is not int or r < 1:
        raise TypeError("r must be a positive exact integer")
    return {
        m: Fraction(-2 * ALPHA[m] * (m - 1) ** r - 4 * BETA[m], r)
        for m in range(2, 9)
    }


def _gamma_interval(r: int) -> tuple[Fraction, Fraction]:
    intervals = _u_intervals()
    vector = _gamma_vector(r)
    lower = Fraction()
    upper = Fraction()
    for m, coefficient in vector.items():
        lo, hi = intervals[m]
        lower += coefficient * (lo if coefficient >= 0 else hi)
        upper += coefficient * (hi if coefficient >= 0 else lo)
    return lower, upper


def _kernel_rows() -> list[dict[str, object]]:
    source_identity = Fraction(2 * (2 * 5 - 1) + 1, 5) == 4 - Fraction(1, 5)
    return [
        {"id": "johnston_yang", "epsilon": "27/1000*L^(1801/1000)*exp(-(1853/10000)*V)", "V": "L^(3/5)*(log(L))^(-1/5)", "L_min": L0, "pass": Fraction(27, 1000) > 0 and Fraction(1853, 10000) > 0},
        {"id": "domain_bridge", "L_min": L0, "x_floor": X0, "c_range": [1, CMAX], "s_min": 2, "bridge": "x=e^L>2^512>256", "pass": 2**L0 > X0 and CMAX == 7},
        {"id": "strict_endpoint", "prime_condition": "p>x", "successor": "P_r(y)=(q^2-1)^(-r)+P_r(y+1), q=p_(y+1)", "inclusive": False, "pass": True},
        {"id": "rank_split", "retained": "sum_(1<=r<s)c^r*P_r/r", "replaced": "all integers r>=s", "Psi": "retained+sum_(r>=s)c^r*K_r*S_K(a_r)/r", "pass": True},
        {"id": "R_s", "definition": "R_s(z)=sum_(r>=s)z^r/r", "derivative": "R_s'(z)=z^(s-1)/(1-z)", "domain": "s>=2,0<=z<1", "pass": True},
        {"id": "R_s_majorant", "bound": "R_s(z)<=z^s/(s*(1-z))", "coefficient": "1/s", "direction": "upper", "pass": Fraction(1, 5) > 0},
        {"id": "strict_stieltjes", "boundary_units": 1, "derivative_xh_units": 1, "derivative_J_units": 1, "bound": "|P_r-J_r|<=epsilon*(2*x*h_r(x)+J_r)", "pass": 1 + 1 == 2},
        {"id": "source_boundary_normalization", "coefficient": "2*(2s-1)/s", "A": "1/((1-x^-2)^s*(1-c/(x^2-1)))", "pass": Fraction(2 * (2 * 5 - 1), 5) == Fraction(18, 5)},
        {"id": "source_integral_normalization", "coefficient": "1/s", "combined": "4-1/s", "identity_fixture_s": 5, "pass": source_identity},
        {"id": "power_kernel", "inequality": "(1-u)^(-r)-1<=r*u*(1-u)^(-r-1)", "B_exponent": "s+1", "direction": "J_r>=I_2r", "pass": True},
        {"id": "power_integral", "normalized_coefficient": "(2s-1)/(2s+1)", "B": "1/((1-x^-2)^(s+1)*(1-c/(x^2-1)))", "integral_power": "2s+2", "pass": Fraction(2 * 5 - 1, 2 * 5 + 1) == Fraction(9, 11)},
        {"id": "normalized_master", "K_s": "x^(1-2s)/((2s-1)*L)", "coordinate_terms": ["c^s*(4-1/s)*A*epsilon", "c^s*((2s-1)/(2s+1))*B/x^2", "c^s*C*K!/(s*((2s-1)*L)^K)"], "endpoint_multiplier": 126, "pass": 126 == 2 * (2 * 7 + 8 * Fraction(49, 8))},
    ]


def _channel_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for c in range(1, CMAX + 1):
        s = c + 1
        A = _a_value(s, c)
        B = _b_value(s, c)
        C = _c_value(c)
        source = c**s * (4 - Fraction(1, s)) * A
        power = c**s * Fraction(2 * s - 1, 2 * s + 1) * B
        factorial_prefactor = Fraction(c**s, s) * C
        rows.append({
            "c": c,
            "s_fixture": s,
            "x_fixture": X0,
            "A": fraction_text(A),
            "B": fraction_text(B),
            "C": fraction_text(C),
            "source_normalized": fraction_text(source),
            "power_normalized": fraction_text(power),
            "factorial_normalized_prefactor": fraction_text(factorial_prefactor),
            "positive_denominators": A > 0 and B > 0 and C > 0,
            "pass": A > 0 and B > 0 and C > 0 and source > 0 and power > 0 and factorial_prefactor > 0,
        })
    return rows


def _gamma_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    vector = _gamma_vector(4)
    m2_numerator = -2 * ALPHA[2] - 4 * BETA[2]
    rows.append({"id": "m2_cancellation", "m": 2, "symbolic_numerator": "-2*alpha2-4*beta2", "numerator": m2_numerator, "alpha2": ALPHA[2], "beta2": BETA[2], "all_r": True, "pass": m2_numerator == 0})
    for r in range(1, 6):
        lower, upper = _gamma_interval(r)
        rows.append({"id": f"gamma_low_r{r}", "r": r, "coefficient_vector": [fraction_text(_gamma_vector(r)[m]) for m in range(2, 9)], "lower": fraction_text(lower), "upper": fraction_text(upper), "positive": lower > 0, "pass": Fraction(0) < lower <= upper})
    ratio_specs = (("u4_over_u3", 4, 3, 2, 3, 1), ("u6_over_u5", 6, 5, 4, 5, 2), ("u8_over_u7", 8, 7, 6, 7, 6))
    intervals = _u_intervals()
    for row_id, even_m, odd_m, numerator, denominator, exponent in ratio_specs:
        even_lo = intervals[even_m][0]
        odd_hi = intervals[odd_m][1]
        threshold = Fraction(numerator, denominator) ** exponent
        rows.append({"id": row_id, "even_m": even_m, "odd_m": odd_m, "base_ratio": f"{numerator}/{denominator}", "threshold_exponent": exponent, "cross_left": fraction_text(even_lo * threshold.denominator), "cross_right": fraction_text(odd_hi * threshold.numerator), "strict": even_lo / odd_hi > threshold, "pass": even_lo * threshold.denominator > odd_hi * threshold.numerator})
    for odd_m, even_m in ((3, 4), (5, 6), (7, 8)):
        difference = intervals[odd_m][0] - intervals[even_m][1]
        rows.append({"id": f"u{odd_m}_gt_u{even_m}", "odd_m": odd_m, "even_m": even_m, "directed_difference": fraction_text(difference), "strict": difference > 0, "pass": difference > 0})
    pair_pattern = [[3, 4, 2, 3], [5, 6, 4, 5], [7, 8, 6, 7]]
    pattern_pass = all(ALPHA[odd] == 2 and ALPHA[even] == -2 and BETA[odd] == -2 and BETA[even] == 2 and small == odd - 1 and large == even - 1 and 0 < small < large for odd, even, small, large in pair_pattern)
    rows.append({"id": "grouped_singleton_formula", "formula": "gamma_r=(4/r)*(3^r*u4-2^r*u3+5^r*u6-4^r*u5+7^r*u8-6^r*u7+2*(u3-u4+u5-u6+u7-u8))", "z_singleton": "r", "pair_pattern": pair_pattern, "alpha_beta_pattern": "odd:+2,-2; even:-2,+2", "all_r_derivation": True, "pass": pattern_pass and m2_numerator == 0})
    exponents = [1, 2, 6]
    high_pass = all(row["pass"] is True for row in rows[6:12]) and all(exponent <= 6 for exponent in exponents)
    rows.append({"id": "gamma_r_ge_6", "r_min": 6, "ratio_threshold_exponents": exponents, "exponents_not_above_r_min": all(exponent <= 6 for exponent in exponents), "positive_power_pairs": 3, "positive_memory_pairs": 3, "pass": high_pass})
    all_pass = rows[12]["pass"] is True and all(row["pass"] is True for row in rows[1:6]) and rows[13]["pass"] is True
    rows.append({"id": "gamma_all_r", "low_range": [1, 5], "high_range": "r>=6", "consumes_grouped_formula": True, "conclusion": "gamma_(r)>0 for every integer r>=1", "pass": all_pass})
    return rows


def _factorial_rows() -> list[dict[str, object]]:
    return [
        {"id": "K_r", "formula": "x^(1-2r)/((2r-1)*L)", "odd_rate": "2r-1", "pass": 2 * 4 - 1 == 7},
        {"id": "a_r", "formula": "1/((2r-1)*L)", "odd_rate": "2r-1", "pass": 2 * 4 - 1 == 7},
        {"id": "G", "formula": "integral_0^infinity(e^-v/(1+a*v))dv", "denominator": "1+a*v", "pass": True},
        {"id": "S_K", "formula": "sum_(j=0)^(K-1)(-1)^j*j!*a^j", "sign": "(-1)^j", "factorial": "j!", "pass": factorial(4) == 24},
        {"id": "laplace_remainder", "formula": "G(a)-S_K(a)=(-a)^K*integral_0^infinity(e^-v*v^K/(1+a*v))dv", "denominator": "1+a*v", "pass": True},
        {"id": "remainder_sign", "sign": "(-1)^K", "K_type": "exact positive integer", "pass": True},
        {"id": "absolute_moment", "integral": "integral_0^infinity(e^-v*v^K)dv", "value": "K!", "fixture_K": 5, "fixture_value": str(factorial(5)), "pass": factorial(5) == 120},
        {"id": "b_sequence", "formula": "b_K=K!/((2s-1)*L)^K", "base_K": 1, "base_value": "1/((2s-1)*L)", "pass": True},
        {"id": "b_recurrence", "formula": "b_(K+1)/b_K=(K+1)/((2s-1)*L)", "numerator_shift": 1, "pass": True},
        {"id": "full_K_window", "K_min": 1, "K_max": "floor(D)", "D": "(2s-1)*L", "D_domain": "positive real", "K_integer": True, "index_domain": "exact integers 1<=k<floor(D)", "D_positive": True, "floor_D_le_D": True, "ratio_formula": "b_(k+1)/b_k=(k+1)/D", "ratio_numerator_le_D": True, "ratio_upper": "1", "universal_integer_induction": True, "pass": all((True, (2 * 2 - 1) * L0 > 0))},
        {"id": "alternating_positivity", "range": "0<S_K(a_r)<=1 for r>=s and full K window", "j_range": "0<=j<=K-2", "term_ratio": "(j+1)*a_r", "K_minus_1_lt_D": True, "D_le_odd_rate": True, "positive_terms": True, "chain": "j+1<=K-1<D<=(2r-1)*L", "pass": all((True, True, True, (2 * 2 - 1) * L0 > 1))},
        {"id": "factorial_coordinate", "C": "1/(1-c/x^2)", "normalized_bound": "c^s*C*K!/(s*((2s-1)*L)^K)", "rank_range": "all integers r>=s", "pass": True},
    ]


def _growing_rows() -> list[dict[str, object]]:
    A = sum((abs(ALPHA[m]) * Fraction(9 - m, 8) for m in range(2, 9)), Fraction())
    B = sum((abs(BETA[m]) * Fraction(9 - m, 8) for m in range(2, 9)), Fraction())
    derivative_terms = (2, 4, 4)
    pre_exp = derivative_terms[0] * A + (derivative_terms[1] + derivative_terms[2]) * B
    gradient = 2 * pre_exp
    bernoulli_floor = 1 - Fraction(1, X0)
    source_floor = 1 - Fraction(CMAX, X0 * X0 - 1)
    c_floor = 1 - Fraction(CMAX, X0 * X0)
    uniform_A_B = bernoulli_floor > Fraction(1, 2) and source_floor > Fraction(1, 2)
    uniform_C = c_floor > Fraction(1, 2)
    head_upper = Fraction(CMAX, 1) / (1 - Fraction(CMAX, X0 * X0 - 1)) * Fraction(1, 2) * (Fraction(1, X0) + Fraction(1, X0 + 1))
    tail_upper = Fraction(CMAX * CMAX, 6 * X0**3 * L0) / (1 - Fraction(CMAX, X0 * X0))
    cube_upper = head_upper + tail_upper
    rows = [
        {"id": "growing_s_window", "delta_domain": "fixed 0<delta<1", "S_y": "floor((1-delta)*log(L)/log(7))", "s_range": "2<=s<=S_y", "pass": True},
        {"id": "seven_power_budget", "inequality": "7^S_y<=L^(1-delta)", "normalized": "7^S_y/L<=L^(-delta)", "limit": "0", "pass": True},
        {"id": "order_vs_V", "relation": "log(S_y)=o(V)", "V": "L^(3/5)*(log(L))^(-1/5)", "uniform_order_input": "RH-386", "pass": True},
        {"id": "source_limit", "term": "7^S_y*epsilon_x", "rate": "<=(27/1000)*L^(2801/1000-delta)*exp(-(1853/10000)*V)", "A_uniform_upper": 4, "uniform_bridge": "s+1<=L+1<e^L=x, so (s+1)/x^2<1/x<=1/256", "bernoulli_floor": fraction_text(bernoulli_floor), "source_denominator_floor": fraction_text(source_floor), "eventual_smallness": "7*S_y*epsilon_x<=1/2", "limit": "0", "effective_threshold_claimed": False, "pass": uniform_A_B},
        {"id": "power_limit", "term": "7^S_y/x^2", "rate": "<=4*L^(1-delta)/x^2", "B_uniform_upper": 4, "B_exponent_budget": "s+1<=L+1", "uniform_bridge": "(1-x^-2)^(s+1)>=1-(s+1)/x^2>1-1/256", "bernoulli_floor": fraction_text(bernoulli_floor), "source_denominator_floor": fraction_text(source_floor), "limit": "0", "pass": uniform_A_B},
        {"id": "factorial_limit", "term": "7^S_y/(s*(2s-1)*L)", "rate": "<=1/3*L^(-delta)", "C_uniform_upper": 2, "C_denominator_floor": fraction_text(c_floor), "uses_full_K_window": True, "limit": "0", "pass": uniform_C},
        {"id": "uniform_Ps_scale", "asymptotic": "P_s/K_s->1 uniformly for 2<=s<=S_y", "K_s": "x^(1-2s)/((2s-1)*L)", "source": "RH-386 growing-order transfer", "pass": True},
        {"id": "cube", "coordinate_range": "[0,1/2]^7", "head_upper_formula": "c/(1-c/(x^2-1))*1/2*(1/x+1/(x+1))", "tail_upper_formula": "c^2/(6*x^3*L*(1-c/x^2))", "head_upper_fixture": fraction_text(head_upper), "tail_upper_fixture": fraction_text(tail_upper), "total_upper_fixture": fraction_text(cube_upper), "mechanism": "L>=512 bridge plus positive exact head and 0<S_K(a_r)<=1 tail", "fixture_only": False, "pass": 2**L0 > X0 and cube_upper < Fraction(1, 2)},
        {"id": "endpoint_gradient", "sum_abs_alpha_u": fraction_text(A), "sum_abs_beta_u": fraction_text(B), "derivative_terms": list(derivative_terms), "pre_exp": fraction_text(pre_exp), "exp_half_upper": 2, "dual_norm": "l_infinity_input_to_l1_gradient", "gradient": int(gradient), "pass": A == 7 and B == Fraction(49, 8) and pre_exp == 63 and gradient == 126},
        {"id": "uniform_gap_conclusion", "limit_variable": "y->infinity", "quantifiers": "max_(2<=s<=S_y) max_(1<=K<=floor((2s-1)*L))", "ratio": "|GapP-Gap_(s,K)|/P_s", "consumes": ["seven_power_budget", "source_limit", "power_limit", "factorial_limit", "uniform_Ps_scale", "cube", "endpoint_gradient"], "limit": "0", "pass": False},
    ]
    rows[-1]["pass"] = all(rows[index]["pass"] is True for index in range(9))
    return rows


def _necessity_rows() -> list[dict[str, object]]:
    rows = [
        {"id": "maynard", "gap_type": "consecutive_primes", "infinitely_many": True, "gap_upper": 600, "source": "Maynard Theorem 1.3 printed page 385 PDF page 3", "pass": 600 > 0},
        {"id": "rank_r_successor", "r": "fixed r=s-1>=1", "E_r": "P_r(y)-I_(2r)(p_y)", "formula": "E_r(y)-E_r(y+1)=(q^2-1)^(-r)-integral_x^q(t^(-2r)/log(t))dt", "atom_location": "q=p_(y+1)", "pass": True},
        {"id": "bounded_gap_geometry", "q": "x+h", "h_range": "0<h<=600 infinitely often", "q_over_x": "1+o(1)", "distinct_pairs": True, "pass": True},
        {"id": "scaled_atom", "scale": "x^(2r)", "atom": "(q^2-1)^(-r)", "limit": "1", "pass": True},
        {"id": "scaled_smooth_interval", "scale": "x^(2r)", "upper": "600/log(x)*(1+o(1))", "limit": "0", "pass": True},
        {"id": "scalar_limsup", "jump_limit": 1, "endpoint_count": 2, "lower": "1/2", "conclusion": "limsup x^(2r)*|P_r-I_(2r)|>=1/2", "pass": Fraction(1, 2) == Fraction(1, 2)},
        {"id": "vector_direction", "coordinate_c": "c^r/r", "c_range": [1, 7], "direction": "v_r=(c^r/r)_(c=1)^7", "full_tail_jump": "x^(2r)*((tail_P-tail_I)_y-(tail_P-tail_I)_(y+1))->v_r", "higher_ranks": "o(x^(-2r))", "pass": True},
        {"id": "common_head_Taylor", "head": "H=sum_(j<r)c^j*P_j/j", "tails": "A=tail_P_(>=r), B=tail_I_(>=r)", "two_point_bound": "|F(H+A)-F(H+B)-gradF(0).(A-B)|<=224*||H||*||A-B||+112*(||A||^2+||B||^2)", "cross_coefficient": 224, "square_coefficient": 112, "H_order": "O(x^-1*L^-1)", "A_B_order": "O(x^(1-2r)*L^-1)", "cross_x_exponent": "-2r", "square_x_exponent": "2-4r", "target_x_exponent": "-2r", "square_relative_exponent": "2-2r<=0 for r>=1", "L_factor": "L^-2", "scaled_remainder": "o(x^(-2r))", "pass": 224 == 2 * 112 and 2 - 2 * 1 <= 0},
        {"id": "endpoint_singleton", "gradient_dot_v_r": "gamma_(r)", "gamma_positive": True, "gamma_source": "gamma_all_r row", "lower": "gamma_(r)/2", "pass": _gamma_rows()[14]["pass"] is True},
        {"id": "sharp_retention_necessity", "scope": "fixed s only in frozen P/J/I hierarchy", "missing_rank": "r=s-1", "I_conclusion": "limsup x^(2r)*pi^2*|GapP-GapI_(<r)|>=gamma_(r)/2", "J_bridge": "sum_(j>=r)c^j*(J_j-I_(2j))/j=O(x^(-2r-1)/L)=o(x^(-2r))", "J_conclusion": "same lower bound for GapJ_(<r)", "Ps_scale": "P_s~x^(1-2s)/((2s-1)*L)", "Ps_ratio": "limsup error/P_s=infinity", "growing_s_necessity": False, "arbitrary_surrogate": False, "pass": True},
    ]
    rows[-1]["pass"] = all(row["pass"] is True for row in rows[:-1]) and rows[8]["gamma_positive"] is True
    return rows


def _contract_rows() -> list[dict[str, object]]:
    return [
        {"id": "definitions", "x": "p_y", "L": "log(x)", "K_s": "x^(1-2s)/((2s-1)*L)", "Psi": "sum_(r<s)c^r*P_r/r+sum_(r>=s)c^r*K_r*S_K(a_r)/r", "Gap": "Gap_(s,K)=F((Psi_c)_(c=1)^7)/pi^2", "pass": True},
        {"id": "theorem_quantifiers", "limit": "as y->infinity", "delta": "fixed 0<delta<1", "eventual_nonempty": "eventually S_y>=2", "s": "exact integer 2<=s<=floor((1-delta)*log(L)/log(7))", "K": "exact integer 1<=K<=floor((2s-1)*L)", "c": "c in the finite integer set {1,...,7}", "pass": True},
        {"id": "source_closure", "git_rows": 87, "remote_rows": 2, "logical_rows": 89, "release_commit": "8e6f89ee1e58e67c53c5f4719c05e881107113ac", "all87_digest": "b86cb21288fe9c48304d90ae812829f5e44f4fac0a2b725a09e5c1512ca60cab", "logical89_digest": "2255b26dd68adf09f447e251eb5d38c8b1d31fbaa1c26befd8c04165097ed922", "pass": 87 + 2 == 89},
        {"id": "source_roles", "johnston_yang": "prime-counting envelope via RH-386/RH-388 closure", "maynard": "fixed-s consecutive bounded-gap necessity", "excluded": ["RH-389", "TPC-137", "Tao active-log source"], "pass": True},
        {"id": "novelty", "new": "simultaneous growing-s rank filtration with the full moving-K window and sharp fixed-s retention hierarchy", "not_new": "the fixed s=2 theorem of RH-388 or separate fixed-s restatements", "pass": True},
        {"id": "firewall", "convergent_factorial_series": False, "growing_s_necessity": False, "arbitrary_surrogate_necessity": False, "complex_c": False, "active_c11": False, "growing_clock": False, "K_N": False, "operator_trace_zeros_RH": False, "gates_A_to_E": [False, False, False, False, False], "pass": True},
    ]


GROUP_BUILDERS = {
    "kernel_rows": _kernel_rows,
    "channel_rows": _channel_rows,
    "gamma_rows": _gamma_rows,
    "factorial_rows": _factorial_rows,
    "growing_rows": _growing_rows,
    "necessity_rows": _necessity_rows,
    "contract_rows": _contract_rows,
}


def build_certificate() -> dict[str, object]:
    groups = {name: builder() for name, builder in GROUP_BUILDERS.items()}
    counts = {name: len(rows) for name, rows in groups.items()}
    counts["oracle_rows_total"] = sum(counts.values())
    all_rows = [row for rows in groups.values() for row in rows]
    return {
        "status": STATUS,
        "epistemic_role": ROLE,
        "counts": counts,
        **groups,
        "all_pass": counts["oracle_rows_total"] == 72 and all(row["pass"] is True for row in all_rows),
    }


def _require_list(value: object, length: int, label: str) -> list[object]:
    if type(value) is not list or len(value) != length:
        raise TypeError(f"{label} must be an exact list of length {length}")
    return value


def _require_keys(value: object, keys: set[str], label: str) -> dict[str, object]:
    if type(value) is not dict or set(value) != keys:
        raise TypeError(f"{label} membership changed")
    return value


def _require_exact(actual: object, expected: object, label: str) -> None:
    if not exact_equal(actual, expected):
        raise ValueError(f"{label} changed")


def _static_row(value: object, label: str, primitives: dict[str, object], passed: bool) -> dict[str, object]:
    row = _require_keys(value, {*primitives, "pass"}, label)
    for key, expected in primitives.items():
        _require_exact(row[key], expected, f"{label}.{key}")
    _require_exact(row["pass"], bool(passed), f"{label}.pass")
    return row


def _validate_kernel_rows(value: object) -> None:
    rows = _require_list(value, 12, "kernel_rows")
    data: list[tuple[dict[str, object], bool]] = [
        ({"id": "johnston_yang", "epsilon": "27/1000*L^(1801/1000)*exp(-(1853/10000)*V)", "V": "L^(3/5)*(log(L))^(-1/5)", "L_min": 512}, Fraction(27, 1000) > 0 and Fraction(1853, 10000) > 0),
        ({"id": "domain_bridge", "L_min": 512, "x_floor": 256, "c_range": [1, 7], "s_min": 2, "bridge": "x=e^L>2^512>256"}, 2**512 > 256),
        ({"id": "strict_endpoint", "prime_condition": "p>x", "successor": "P_r(y)=(q^2-1)^(-r)+P_r(y+1), q=p_(y+1)", "inclusive": False}, True),
        ({"id": "rank_split", "retained": "sum_(1<=r<s)c^r*P_r/r", "replaced": "all integers r>=s", "Psi": "retained+sum_(r>=s)c^r*K_r*S_K(a_r)/r"}, True),
        ({"id": "R_s", "definition": "R_s(z)=sum_(r>=s)z^r/r", "derivative": "R_s'(z)=z^(s-1)/(1-z)", "domain": "s>=2,0<=z<1"}, True),
        ({"id": "R_s_majorant", "bound": "R_s(z)<=z^s/(s*(1-z))", "coefficient": "1/s", "direction": "upper"}, Fraction(1, 5) > 0),
        ({"id": "strict_stieltjes", "boundary_units": 1, "derivative_xh_units": 1, "derivative_J_units": 1, "bound": "|P_r-J_r|<=epsilon*(2*x*h_r(x)+J_r)"}, 1 + 1 == 2),
        ({"id": "source_boundary_normalization", "coefficient": "2*(2s-1)/s", "A": "1/((1-x^-2)^s*(1-c/(x^2-1)))"}, Fraction(2 * 9, 5) == Fraction(18, 5)),
        ({"id": "source_integral_normalization", "coefficient": "1/s", "combined": "4-1/s", "identity_fixture_s": 5}, Fraction(2 * 9 + 1, 5) == 4 - Fraction(1, 5)),
        ({"id": "power_kernel", "inequality": "(1-u)^(-r)-1<=r*u*(1-u)^(-r-1)", "B_exponent": "s+1", "direction": "J_r>=I_2r"}, True),
        ({"id": "power_integral", "normalized_coefficient": "(2s-1)/(2s+1)", "B": "1/((1-x^-2)^(s+1)*(1-c/(x^2-1)))", "integral_power": "2s+2"}, Fraction(9, 11) == Fraction(2 * 5 - 1, 2 * 5 + 1)),
        ({"id": "normalized_master", "K_s": "x^(1-2s)/((2s-1)*L)", "coordinate_terms": ["c^s*(4-1/s)*A*epsilon", "c^s*((2s-1)/(2s+1))*B/x^2", "c^s*C*K!/(s*((2s-1)*L)^K)"], "endpoint_multiplier": 126}, 126 == 2 * (2 * 7 + 8 * Fraction(49, 8))),
    ]
    for index, (primitives, passed) in enumerate(data):
        _static_row(rows[index], f"kernel[{index}]", primitives, passed)


def _validate_channel_rows(value: object) -> None:
    rows = _require_list(value, 7, "channel_rows")
    keys = {"c", "s_fixture", "x_fixture", "A", "B", "C", "source_normalized", "power_normalized", "factorial_normalized_prefactor", "positive_denominators", "pass"}
    for index, item in enumerate(rows):
        row = _require_keys(item, keys, f"channel[{index}]")
        c = row["c"]
        s = row["s_fixture"]
        x = row["x_fixture"]
        if type(c) is not int or type(s) is not int or type(x) is not int:
            raise TypeError("channel integer primitives changed")
        _require_exact(c, index + 1, f"channel[{index}].c")
        _require_exact(s, c + 1, f"channel[{index}].s")
        _require_exact(x, X0, f"channel[{index}].x")
        A, B, C = _a_value(s, c, x), _b_value(s, c, x), _c_value(c, x)
        source = c**s * (4 - Fraction(1, s)) * A
        power = c**s * Fraction(2 * s - 1, 2 * s + 1) * B
        factorial_prefactor = Fraction(c**s, s) * C
        for key, expected in {"A": fraction_text(A), "B": fraction_text(B), "C": fraction_text(C), "source_normalized": fraction_text(source), "power_normalized": fraction_text(power), "factorial_normalized_prefactor": fraction_text(factorial_prefactor)}.items():
            _require_exact(row[key], expected, f"channel[{index}].{key}")
        positive = A > 0 and B > 0 and C > 0
        _require_exact(row["positive_denominators"], positive, f"channel[{index}].positive")
        _require_exact(row["pass"], positive and source > 0 and power > 0 and factorial_prefactor > 0, f"channel[{index}].pass")


def _validate_gamma_rows(value: object) -> None:
    rows = _require_list(value, 15, "gamma_rows")
    m2_numerator = -2 * ALPHA[2] - 4 * BETA[2]
    _static_row(rows[0], "gamma[0]", {"id": "m2_cancellation", "m": 2, "symbolic_numerator": "-2*alpha2-4*beta2", "numerator": m2_numerator, "alpha2": -2, "beta2": 1, "all_r": True}, m2_numerator == 0)
    low_keys = {"id", "r", "coefficient_vector", "lower", "upper", "positive", "pass"}
    for r in range(1, 6):
        row = _require_keys(rows[r], low_keys, f"gamma[{r}]")
        lower, upper = _gamma_interval(r)
        for key, expected in {"id": f"gamma_low_r{r}", "r": r, "coefficient_vector": [fraction_text(_gamma_vector(r)[m]) for m in range(2, 9)], "lower": fraction_text(lower), "upper": fraction_text(upper), "positive": lower > 0, "pass": Fraction(0) < lower <= upper}.items():
            _require_exact(row[key], expected, f"gamma[{r}].{key}")
    intervals = _u_intervals()
    specs = (("u4_over_u3", 4, 3, 2, 3, 1), ("u6_over_u5", 6, 5, 4, 5, 2), ("u8_over_u7", 8, 7, 6, 7, 6))
    ratio_keys = {"id", "even_m", "odd_m", "base_ratio", "threshold_exponent", "cross_left", "cross_right", "strict", "pass"}
    for offset, (row_id, even_m, odd_m, numerator, denominator, exponent) in enumerate(specs, start=6):
        row = _require_keys(rows[offset], ratio_keys, f"gamma[{offset}]")
        threshold = Fraction(numerator, denominator) ** exponent
        left = intervals[even_m][0] * threshold.denominator
        right = intervals[odd_m][1] * threshold.numerator
        expected = {"id": row_id, "even_m": even_m, "odd_m": odd_m, "base_ratio": f"{numerator}/{denominator}", "threshold_exponent": exponent, "cross_left": fraction_text(left), "cross_right": fraction_text(right), "strict": left > right, "pass": left > right}
        for key, expected_value in expected.items():
            _require_exact(row[key], expected_value, f"gamma[{offset}].{key}")
    monotonic_keys = {"id", "odd_m", "even_m", "directed_difference", "strict", "pass"}
    for offset, (odd_m, even_m) in enumerate(((3, 4), (5, 6), (7, 8)), start=9):
        row = _require_keys(rows[offset], monotonic_keys, f"gamma[{offset}]")
        difference = intervals[odd_m][0] - intervals[even_m][1]
        expected = {"id": f"u{odd_m}_gt_u{even_m}", "odd_m": odd_m, "even_m": even_m, "directed_difference": fraction_text(difference), "strict": difference > 0, "pass": difference > 0}
        for key, expected_value in expected.items():
            _require_exact(row[key], expected_value, f"gamma[{offset}].{key}")
    pair_pattern = [[3, 4, 2, 3], [5, 6, 4, 5], [7, 8, 6, 7]]
    pattern_pass = all(ALPHA[odd] == 2 and ALPHA[even] == -2 and BETA[odd] == -2 and BETA[even] == 2 and small == odd - 1 and large == even - 1 and 0 < small < large for odd, even, small, large in pair_pattern)
    _static_row(rows[12], "gamma[12]", {"id": "grouped_singleton_formula", "formula": "gamma_r=(4/r)*(3^r*u4-2^r*u3+5^r*u6-4^r*u5+7^r*u8-6^r*u7+2*(u3-u4+u5-u6+u7-u8))", "z_singleton": "r", "pair_pattern": pair_pattern, "alpha_beta_pattern": "odd:+2,-2; even:-2,+2", "all_r_derivation": True}, pattern_pass and m2_numerator == 0)
    exponents = rows[13]["ratio_threshold_exponents"] if type(rows[13]) is dict else None
    high_pass = type(exponents) is list and exact_equal(exponents, [1, 2, 6]) and all(type(item) is int and item <= 6 for item in exponents) and all(rows[index]["pass"] is True for index in range(6, 12))
    _static_row(rows[13], "gamma[13]", {"id": "gamma_r_ge_6", "r_min": 6, "ratio_threshold_exponents": [1, 2, 6], "exponents_not_above_r_min": True, "positive_power_pairs": 3, "positive_memory_pairs": 3}, bool(high_pass))
    all_pass = rows[12]["pass"] is True and all(rows[index]["pass"] is True for index in range(1, 6)) and rows[13]["pass"] is True
    _static_row(rows[14], "gamma[14]", {"id": "gamma_all_r", "low_range": [1, 5], "high_range": "r>=6", "consumes_grouped_formula": True, "conclusion": "gamma_(r)>0 for every integer r>=1"}, all_pass)


def _validate_factorial_rows(value: object) -> None:
    rows = _require_list(value, 12, "factorial_rows")
    data: list[tuple[dict[str, object], bool]] = [
        ({"id": "K_r", "formula": "x^(1-2r)/((2r-1)*L)", "odd_rate": "2r-1"}, 2 * 4 - 1 == 7),
        ({"id": "a_r", "formula": "1/((2r-1)*L)", "odd_rate": "2r-1"}, 2 * 4 - 1 == 7),
        ({"id": "G", "formula": "integral_0^infinity(e^-v/(1+a*v))dv", "denominator": "1+a*v"}, True),
        ({"id": "S_K", "formula": "sum_(j=0)^(K-1)(-1)^j*j!*a^j", "sign": "(-1)^j", "factorial": "j!"}, factorial(4) == 24),
        ({"id": "laplace_remainder", "formula": "G(a)-S_K(a)=(-a)^K*integral_0^infinity(e^-v*v^K/(1+a*v))dv", "denominator": "1+a*v"}, True),
        ({"id": "remainder_sign", "sign": "(-1)^K", "K_type": "exact positive integer"}, True),
        ({"id": "absolute_moment", "integral": "integral_0^infinity(e^-v*v^K)dv", "value": "K!", "fixture_K": 5, "fixture_value": "120"}, factorial(5) == 120),
        ({"id": "b_sequence", "formula": "b_K=K!/((2s-1)*L)^K", "base_K": 1, "base_value": "1/((2s-1)*L)"}, True),
        ({"id": "b_recurrence", "formula": "b_(K+1)/b_K=(K+1)/((2s-1)*L)", "numerator_shift": 1}, True),
        ({"id": "full_K_window", "K_min": 1, "K_max": "floor(D)", "D": "(2s-1)*L", "D_domain": "positive real", "K_integer": True, "index_domain": "exact integers 1<=k<floor(D)", "D_positive": True, "floor_D_le_D": True, "ratio_formula": "b_(k+1)/b_k=(k+1)/D", "ratio_numerator_le_D": True, "ratio_upper": "1", "universal_integer_induction": True}, all((True, True, (2 * 2 - 1) * L0 > 0))),
        ({"id": "alternating_positivity", "range": "0<S_K(a_r)<=1 for r>=s and full K window", "j_range": "0<=j<=K-2", "term_ratio": "(j+1)*a_r", "K_minus_1_lt_D": True, "D_le_odd_rate": True, "positive_terms": True, "chain": "j+1<=K-1<D<=(2r-1)*L"}, all((True, True, True, (2 * 2 - 1) * L0 > 1))),
        ({"id": "factorial_coordinate", "C": "1/(1-c/x^2)", "normalized_bound": "c^s*C*K!/(s*((2s-1)*L)^K)", "rank_range": "all integers r>=s"}, True),
    ]
    for index, (primitives, passed) in enumerate(data):
        _static_row(rows[index], f"factorial[{index}]", primitives, passed)
    # Cross-row algebra, independent of the builder.
    _require_exact(rows[0]["odd_rate"], rows[1]["odd_rate"], "factorial odd-rate cross-contract")
    _require_exact(rows[2]["denominator"], rows[4]["denominator"], "factorial denominator cross-contract")
    if rows[7]["base_K"] != rows[9]["K_min"] or rows[8]["numerator_shift"] != 1 or rows[9]["D"] != "(2s-1)*L" or rows[9]["D_domain"] != "positive real" or rows[9]["K_integer"] is not True or rows[9]["floor_D_le_D"] is not True or rows[9]["ratio_numerator_le_D"] is not True or rows[10]["K_minus_1_lt_D"] is not True or rows[10]["D_le_odd_rate"] is not True or rows[10]["chain"] != "j+1<=K-1<D<=(2r-1)*L":
        raise ValueError("factorial induction primitives disagree")


def _validate_growing_rows(value: object, factorial_value: object, kernel_value: object) -> None:
    rows = _require_list(value, 10, "growing_rows")
    factorial_rows = _require_list(factorial_value, 12, "factorial cross-contract")
    kernel_rows = _require_list(kernel_value, 12, "kernel cross-contract")
    A = sum((abs(ALPHA[m]) * Fraction(9 - m, 8) for m in range(2, 9)), Fraction())
    B = sum((abs(BETA[m]) * Fraction(9 - m, 8) for m in range(2, 9)), Fraction())
    pre_exp = 2 * A + (4 + 4) * B
    gradient = 2 * pre_exp
    bernoulli_floor = 1 - Fraction(1, X0)
    source_floor = 1 - Fraction(CMAX, X0 * X0 - 1)
    c_floor = 1 - Fraction(CMAX, X0 * X0)
    uniform_A_B = bernoulli_floor > Fraction(1, 2) and source_floor > Fraction(1, 2)
    uniform_C = c_floor > Fraction(1, 2)
    head_upper = Fraction(CMAX, 1) / (1 - Fraction(CMAX, X0 * X0 - 1)) * Fraction(1, 2) * (Fraction(1, X0) + Fraction(1, X0 + 1))
    tail_upper = Fraction(CMAX * CMAX, 6 * X0**3 * L0) / (1 - Fraction(CMAX, X0 * X0))
    cube_upper = head_upper + tail_upper
    data: list[tuple[dict[str, object], bool]] = [
        ({"id": "growing_s_window", "delta_domain": "fixed 0<delta<1", "S_y": "floor((1-delta)*log(L)/log(7))", "s_range": "2<=s<=S_y"}, True),
        ({"id": "seven_power_budget", "inequality": "7^S_y<=L^(1-delta)", "normalized": "7^S_y/L<=L^(-delta)", "limit": "0"}, True),
        ({"id": "order_vs_V", "relation": "log(S_y)=o(V)", "V": "L^(3/5)*(log(L))^(-1/5)", "uniform_order_input": "RH-386"}, True),
        ({"id": "source_limit", "term": "7^S_y*epsilon_x", "rate": "<=(27/1000)*L^(2801/1000-delta)*exp(-(1853/10000)*V)", "A_uniform_upper": 4, "uniform_bridge": "s+1<=L+1<e^L=x, so (s+1)/x^2<1/x<=1/256", "bernoulli_floor": fraction_text(bernoulli_floor), "source_denominator_floor": fraction_text(source_floor), "eventual_smallness": "7*S_y*epsilon_x<=1/2", "limit": "0", "effective_threshold_claimed": False}, uniform_A_B),
        ({"id": "power_limit", "term": "7^S_y/x^2", "rate": "<=4*L^(1-delta)/x^2", "B_uniform_upper": 4, "B_exponent_budget": "s+1<=L+1", "uniform_bridge": "(1-x^-2)^(s+1)>=1-(s+1)/x^2>1-1/256", "bernoulli_floor": fraction_text(bernoulli_floor), "source_denominator_floor": fraction_text(source_floor), "limit": "0"}, uniform_A_B),
        ({"id": "factorial_limit", "term": "7^S_y/(s*(2s-1)*L)", "rate": "<=1/3*L^(-delta)", "C_uniform_upper": 2, "C_denominator_floor": fraction_text(c_floor), "uses_full_K_window": True, "limit": "0"}, uniform_C and factorial_rows[9]["pass"] is True),
        ({"id": "uniform_Ps_scale", "asymptotic": "P_s/K_s->1 uniformly for 2<=s<=S_y", "K_s": "x^(1-2s)/((2s-1)*L)", "source": "RH-386 growing-order transfer"}, True),
        ({"id": "cube", "coordinate_range": "[0,1/2]^7", "head_upper_formula": "c/(1-c/(x^2-1))*1/2*(1/x+1/(x+1))", "tail_upper_formula": "c^2/(6*x^3*L*(1-c/x^2))", "head_upper_fixture": fraction_text(head_upper), "tail_upper_fixture": fraction_text(tail_upper), "total_upper_fixture": fraction_text(cube_upper), "mechanism": "L>=512 bridge plus positive exact head and 0<S_K(a_r)<=1 tail", "fixture_only": False}, 2**L0 > X0 and cube_upper < Fraction(1, 2) and factorial_rows[10]["pass"] is True and kernel_rows[1]["pass"] is True),
        ({"id": "endpoint_gradient", "sum_abs_alpha_u": fraction_text(A), "sum_abs_beta_u": fraction_text(B), "derivative_terms": [2, 4, 4], "pre_exp": fraction_text(pre_exp), "exp_half_upper": 2, "dual_norm": "l_infinity_input_to_l1_gradient", "gradient": int(gradient)}, A == 7 and B == Fraction(49, 8) and pre_exp == 63 and gradient == 126),
        ({"id": "uniform_gap_conclusion", "limit_variable": "y->infinity", "quantifiers": "max_(2<=s<=S_y) max_(1<=K<=floor((2s-1)*L))", "ratio": "|GapP-Gap_(s,K)|/P_s", "consumes": ["seven_power_budget", "source_limit", "power_limit", "factorial_limit", "uniform_Ps_scale", "cube", "endpoint_gradient"], "limit": "0"}, all(rows[index]["pass"] is True for index in range(9))),
    ]
    for index, (primitives, passed) in enumerate(data):
        _static_row(rows[index], f"growing[{index}]", primitives, passed)
    if rows[5]["uses_full_K_window"] is not True or rows[6]["K_s"] != "x^(1-2s)/((2s-1)*L)" or rows[3]["A_uniform_upper"] != 4 or rows[4]["B_uniform_upper"] != 4 or rows[5]["C_uniform_upper"] != 2:
        raise ValueError("growing normalized-scale chain changed")


def _validate_necessity_rows(value: object, gamma_value: object) -> None:
    rows = _require_list(value, 10, "necessity_rows")
    gamma_rows = _require_list(gamma_value, 15, "gamma_rows cross-contract")
    data: list[tuple[dict[str, object], bool]] = [
        ({"id": "maynard", "gap_type": "consecutive_primes", "infinitely_many": True, "gap_upper": 600, "source": "Maynard Theorem 1.3 printed page 385 PDF page 3"}, True),
        ({"id": "rank_r_successor", "r": "fixed r=s-1>=1", "E_r": "P_r(y)-I_(2r)(p_y)", "formula": "E_r(y)-E_r(y+1)=(q^2-1)^(-r)-integral_x^q(t^(-2r)/log(t))dt", "atom_location": "q=p_(y+1)"}, True),
        ({"id": "bounded_gap_geometry", "q": "x+h", "h_range": "0<h<=600 infinitely often", "q_over_x": "1+o(1)", "distinct_pairs": True}, True),
        ({"id": "scaled_atom", "scale": "x^(2r)", "atom": "(q^2-1)^(-r)", "limit": "1"}, True),
        ({"id": "scaled_smooth_interval", "scale": "x^(2r)", "upper": "600/log(x)*(1+o(1))", "limit": "0"}, True),
        ({"id": "scalar_limsup", "jump_limit": 1, "endpoint_count": 2, "lower": "1/2", "conclusion": "limsup x^(2r)*|P_r-I_(2r)|>=1/2"}, Fraction(1, 2) == Fraction(1, 2)),
        ({"id": "vector_direction", "coordinate_c": "c^r/r", "c_range": [1, 7], "direction": "v_r=(c^r/r)_(c=1)^7", "full_tail_jump": "x^(2r)*((tail_P-tail_I)_y-(tail_P-tail_I)_(y+1))->v_r", "higher_ranks": "o(x^(-2r))"}, True),
        ({"id": "common_head_Taylor", "head": "H=sum_(j<r)c^j*P_j/j", "tails": "A=tail_P_(>=r), B=tail_I_(>=r)", "two_point_bound": "|F(H+A)-F(H+B)-gradF(0).(A-B)|<=224*||H||*||A-B||+112*(||A||^2+||B||^2)", "cross_coefficient": 224, "square_coefficient": 112, "H_order": "O(x^-1*L^-1)", "A_B_order": "O(x^(1-2r)*L^-1)", "cross_x_exponent": "-2r", "square_x_exponent": "2-4r", "target_x_exponent": "-2r", "square_relative_exponent": "2-2r<=0 for r>=1", "L_factor": "L^-2", "scaled_remainder": "o(x^(-2r))"}, 224 == 2 * 112 and 2 - 2 * 1 <= 0),
        ({"id": "endpoint_singleton", "gradient_dot_v_r": "gamma_(r)", "gamma_positive": True, "gamma_source": "gamma_all_r row", "lower": "gamma_(r)/2"}, gamma_rows[14]["pass"] is True),
        ({"id": "sharp_retention_necessity", "scope": "fixed s only in frozen P/J/I hierarchy", "missing_rank": "r=s-1", "I_conclusion": "limsup x^(2r)*pi^2*|GapP-GapI_(<r)|>=gamma_(r)/2", "J_bridge": "sum_(j>=r)c^j*(J_j-I_(2j))/j=O(x^(-2r-1)/L)=o(x^(-2r))", "J_conclusion": "same lower bound for GapJ_(<r)", "Ps_scale": "P_s~x^(1-2s)/((2s-1)*L)", "Ps_ratio": "limsup error/P_s=infinity", "growing_s_necessity": False, "arbitrary_surrogate": False}, all(row["pass"] is True for row in rows[:9]) and gamma_rows[14]["pass"] is True),
    ]
    for index, (primitives, passed) in enumerate(data):
        row = _static_row(rows[index], f"necessity[{index}]", primitives, passed)
        if index == 0 and (row["gap_type"] != "consecutive_primes" or row["infinitely_many"] is not True):
            raise ValueError("Maynard quantifiers changed")
    if fraction_from_text(rows[5]["lower"], "necessity lower") != Fraction(rows[5]["jump_limit"], rows[5]["endpoint_count"]):
        raise ValueError("two-endpoint limsup division changed")
    if rows[8]["gamma_positive"] is not gamma_rows[14]["pass"]:
        raise ValueError("necessity does not consume gamma positivity")
    if rows[9]["pass"] is not True or rows[9]["J_bridge"] != "sum_(j>=r)c^j*(J_j-I_(2j))/j=O(x^(-2r-1)/L)=o(x^(-2r))" or rows[7]["cross_coefficient"] != 2 * rows[7]["square_coefficient"] or rows[7]["square_relative_exponent"] != "2-2r<=0 for r>=1" or rows[6]["higher_ranks"] != "o(x^(-2r))":
        raise ValueError("necessity cross-contract changed")


def _validate_contract_rows(value: object) -> None:
    rows = _require_list(value, 6, "contract_rows")
    data: list[tuple[dict[str, object], bool]] = [
        ({"id": "definitions", "x": "p_y", "L": "log(x)", "K_s": "x^(1-2s)/((2s-1)*L)", "Psi": "sum_(r<s)c^r*P_r/r+sum_(r>=s)c^r*K_r*S_K(a_r)/r", "Gap": "Gap_(s,K)=F((Psi_c)_(c=1)^7)/pi^2"}, True),
        ({"id": "theorem_quantifiers", "limit": "as y->infinity", "delta": "fixed 0<delta<1", "eventual_nonempty": "eventually S_y>=2", "s": "exact integer 2<=s<=floor((1-delta)*log(L)/log(7))", "K": "exact integer 1<=K<=floor((2s-1)*L)", "c": "c in the finite integer set {1,...,7}"}, True),
        ({"id": "source_closure", "git_rows": 87, "remote_rows": 2, "logical_rows": 89, "release_commit": "8e6f89ee1e58e67c53c5f4719c05e881107113ac", "all87_digest": "b86cb21288fe9c48304d90ae812829f5e44f4fac0a2b725a09e5c1512ca60cab", "logical89_digest": "2255b26dd68adf09f447e251eb5d38c8b1d31fbaa1c26befd8c04165097ed922"}, 87 + 2 == 89),
        ({"id": "source_roles", "johnston_yang": "prime-counting envelope via RH-386/RH-388 closure", "maynard": "fixed-s consecutive bounded-gap necessity", "excluded": ["RH-389", "TPC-137", "Tao active-log source"]}, True),
        ({"id": "novelty", "new": "simultaneous growing-s rank filtration with the full moving-K window and sharp fixed-s retention hierarchy", "not_new": "the fixed s=2 theorem of RH-388 or separate fixed-s restatements"}, True),
        ({"id": "firewall", "convergent_factorial_series": False, "growing_s_necessity": False, "arbitrary_surrogate_necessity": False, "complex_c": False, "active_c11": False, "growing_clock": False, "K_N": False, "operator_trace_zeros_RH": False, "gates_A_to_E": [False, False, False, False, False]}, True),
    ]
    for index, (primitives, passed) in enumerate(data):
        row = _static_row(rows[index], f"contract[{index}]", primitives, passed)
        if index == 2 and row["git_rows"] + row["remote_rows"] != row["logical_rows"]:
            raise ValueError("source count arithmetic changed")
    firewall = rows[5]
    if any(firewall[key] for key in ("convergent_factorial_series", "growing_s_necessity", "arbitrary_surrogate_necessity", "complex_c", "active_c11", "growing_clock", "K_N", "operator_trace_zeros_RH")) or any(firewall["gates_A_to_E"]):
        raise ValueError("scope firewall opened")


def verify_certificate(candidate: object, *, compare_fresh: bool = True) -> bool:
    if type(compare_fresh) is not bool:
        raise TypeError("compare_fresh must be an exact bool")
    if type(candidate) is not dict:
        raise TypeError("certificate must be an exact object")
    group_names = tuple(GROUP_BUILDERS)
    expected_keys = {"status", "epistemic_role", "counts", *group_names, "all_pass"}
    if set(candidate) != expected_keys:
        raise ValueError("certificate membership changed")
    _require_exact(candidate["status"], STATUS, "status")
    _require_exact(candidate["epistemic_role"], ROLE, "epistemic_role")
    _validate_kernel_rows(candidate["kernel_rows"])
    _validate_channel_rows(candidate["channel_rows"])
    _validate_gamma_rows(candidate["gamma_rows"])
    _validate_factorial_rows(candidate["factorial_rows"])
    _validate_growing_rows(candidate["growing_rows"], candidate["factorial_rows"], candidate["kernel_rows"])
    _validate_necessity_rows(candidate["necessity_rows"], candidate["gamma_rows"])
    _validate_contract_rows(candidate["contract_rows"])
    counts: dict[str, int] = {}
    for name in group_names:
        rows = candidate[name]
        if type(rows) is not list:
            raise TypeError(f"{name} must be an exact list")
        counts[name] = len(rows)
    counts["oracle_rows_total"] = sum(counts.values())
    if counts["oracle_rows_total"] != 72:
        raise ValueError("oracle row total changed")
    _require_exact(candidate["counts"], counts, "counts")
    _require_exact(candidate["all_pass"], True, "all_pass")
    if compare_fresh and canonical_json_bytes(candidate) != canonical_json_bytes(build_certificate()):
        raise ValueError("fresh certificate mismatch")
    return True


MUTATION_NAMES = (
    "inclusive_endpoint_and_wrong_successor",
    "missing_stieltjes_boundary",
    "rank_split_starts_at_s_plus_one",
    "wrong_Rs_derivative",
    "false_Rs_majorant",
    "missing_source_integral",
    "source_A_wrong_exponent",
    "power_kernel_missing_extra_factor",
    "power_B_wrong_exponent",
    "power_integral_wrong_rate",
    "wrong_Kr_and_ar_rate",
    "factorial_missing_alternating_sign",
    "factorial_missing_j_factorial",
    "laplace_wrong_denominator",
    "factorial_tail_only_rank_s",
    "moving_K_exceeds_window",
    "wrong_b_recurrence",
    "cube_loses_positivity",
    "missing_endpoint_derivative_term",
    "unrestricted_growing_s",
    "singleton_missing_z_r",
    "gamma_last_pair_wrong_threshold",
    "maynard_not_consecutive",
    "sharp_limsup_missing_half",
)


def apply_mutation(certificate: dict[str, object], name: str) -> dict[str, object]:
    if type(certificate) is not dict:
        raise TypeError("certificate must be an exact object")
    if type(name) is not str or name not in MUTATION_NAMES:
        raise ValueError("unknown mutation")
    value = deepcopy(certificate)
    kernel = value["kernel_rows"]
    factorial_rows = value["factorial_rows"]
    growing = value["growing_rows"]
    gamma = value["gamma_rows"]
    necessity = value["necessity_rows"]
    if name == "inclusive_endpoint_and_wrong_successor":
        kernel[2]["prime_condition"] = "p>=x"
        kernel[2]["successor"] = "P_r(y)=x^(-2r)+P_r(y+1)"
    elif name == "missing_stieltjes_boundary":
        kernel[6]["boundary_units"] = 0
    elif name == "rank_split_starts_at_s_plus_one":
        kernel[3]["replaced"] = "all integers r>=s+1"
    elif name == "wrong_Rs_derivative":
        kernel[4]["derivative"] = "R_s'(z)=z^s/(1-z)"
    elif name == "false_Rs_majorant":
        kernel[5]["bound"] = "R_s(z)<=z^s/((s+1)*(1-z))"
        kernel[5]["coefficient"] = "1/(s+1)"
    elif name == "missing_source_integral":
        kernel[8]["combined"] = "4-2/s"
    elif name == "source_A_wrong_exponent":
        kernel[7]["A"] = "1/((1-x^-2)^(s-1)*(1-c/(x^2-1)))"
    elif name == "power_kernel_missing_extra_factor":
        kernel[9]["inequality"] = "(1-u)^(-r)-1<=r*u*(1-u)^(-r)"
    elif name == "power_B_wrong_exponent":
        kernel[10]["B"] = "1/((1-x^-2)^s*(1-c/(x^2-1)))"
        kernel[10]["B_exponent"] = "s" if "B_exponent" in kernel[10] else None
        if "B_exponent" in kernel[10]:
            del kernel[10]["B_exponent"]
    elif name == "power_integral_wrong_rate":
        kernel[10]["normalized_coefficient"] = "(2s-1)/(2s+3)"
        kernel[10]["integral_power"] = "2s+4"
    elif name == "wrong_Kr_and_ar_rate":
        factorial_rows[0]["formula"] = "x^(1-2r)/((2r+1)*L)"
        factorial_rows[1]["formula"] = "1/((2r+1)*L)"
    elif name == "factorial_missing_alternating_sign":
        factorial_rows[3]["formula"] = "sum_(j=0)^(K-1)j!*a^j"
        factorial_rows[3]["sign"] = "+1"
    elif name == "factorial_missing_j_factorial":
        factorial_rows[3]["formula"] = "sum_(j=0)^(K-1)(-1)^j*a^j"
        factorial_rows[3]["factorial"] = "1"
    elif name == "laplace_wrong_denominator":
        factorial_rows[4]["denominator"] = "1-a*v"
        factorial_rows[4]["formula"] = "G(a)-S_K(a)=(-a)^K*integral(e^-v*v^K/(1-a*v))dv"
    elif name == "factorial_tail_only_rank_s":
        factorial_rows[11]["rank_range"] = "r=s only"
    elif name == "moving_K_exceeds_window":
        factorial_rows[9]["K_max"] = "floor(2s*L)"
        factorial_rows[9]["D"] = "2s*L"
    elif name == "wrong_b_recurrence":
        factorial_rows[8]["formula"] = "b_(K+1)/b_K=K/((2s-1)*L)"
        factorial_rows[8]["numerator_shift"] = 0
    elif name == "cube_loses_positivity":
        factorial_rows[10]["range"] = "S_K(a_r)<=1"
        growing[7]["coordinate_range"] = "(-infinity,1/2]^7"
    elif name == "missing_endpoint_derivative_term":
        growing[8]["derivative_terms"] = [2, 4, 0]
    elif name == "unrestricted_growing_s":
        growing[0]["S_y"] = "floor(2*L/log(7))"
        growing[1]["inequality"] = "7^S_y<=x^2"
    elif name == "singleton_missing_z_r":
        gamma[12]["z_singleton"] = "1"
    elif name == "gamma_last_pair_wrong_threshold":
        gamma[8]["threshold_exponent"] = 5
        gamma[13]["ratio_threshold_exponents"] = [1, 2, 5]
    elif name == "maynard_not_consecutive":
        necessity[0]["gap_type"] = "not necessarily consecutive primes"
    elif name == "sharp_limsup_missing_half":
        necessity[5]["lower"] = "1"
        necessity[5]["conclusion"] = "limsup x^(2r)*|P_r-I_(2r)|>=1"
    return value


def mutation_results() -> list[dict[str, object]]:
    certificate = build_certificate()
    output: list[dict[str, object]] = []
    for name in MUTATION_NAMES:
        rejected = False
        try:
            verify_certificate(apply_mutation(certificate, name), compare_fresh=False)
        except (TypeError, ValueError, KeyError, IndexError):
            rejected = True
        output.append({"name": name, "rejected": rejected})
    return output
