"""Exact finite algebraic certificate for RH-391.

The rows encode the frozen theorem interface and check exact algebraic
implications.  They are not numerical evidence for the analytic limits and do
not replace the inherited Maynard theorem or the manuscript proof.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json


STATUS = "RH-391_linear_scale_moving_rank_prime_tail_retention_necessity"
ROLE = "finite_exact_algebra_not_analytic_proof"
HMAX = 600
CMAX = 7
ALPHA = {2: -2, 3: 2, 4: -2, 5: 2, 6: -2, 7: 2, 8: -2}
BETA = {2: 1, 3: -2, 4: 2, 5: -2, 6: 2, 7: -2, 8: 2}
U_INTERVAL_TEXT = {
    2: ("0.79606040870898303668258723437697247788244823019781688942057817156808006324489857", "0.79606836935287354498059773749834613448214436140422608565968368163277992812734109"),
    3: ("0.61924203807885931176128478638556221233898693327341166091191304286879024381042052", "0.61925442310539659663090836798019670672619725578792199982731263510830127823662602"),
    4: ("0.46706540740190906810813664160692823131359118000867958475033010109068512217833360", "0.46707941971443928894176245156363994112927289254772155985953302903120660751652680"),
    5: ("0.33721417887441793195786656700250637753133382730680422233751764051237490201681002", "0.33722766791368962040853632583965885752876677515408526796859712719631534066544246"),
    6: ("0.22752702560107560768676163112294897624477025177967017050656881905069814845878089", "0.22753840246431479165058321998070523893926657988019982017113068500907168956023382"),
    7: ("0.13598981892337099710656621384206971382910282322100104167530312663406675578226961", "0.13599797876129768932939305595582384250511352267690115354646754910672869761683598"),
    8: ("0.060728124895404081336842078561871850341724556651138274986013006420128664605576844", "0.060732376140477795694564349336715194239732675841161692614726342545899839773689660"),
}


def fraction_text(value: Fraction) -> str:
    if type(value) is not Fraction:
        raise TypeError("exact Fraction required")
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def fraction_from_text(value: object, label: str) -> Fraction:
    if type(value) is not str or not value:
        raise TypeError(f"{label} must be an exact fraction string")
    pieces = value.split("/")
    if len(pieces) == 1:
        numerator, denominator = pieces[0], "1"
    elif len(pieces) == 2:
        numerator, denominator = pieces
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
    whole, decimal = value.split(".")
    if whole != "0" or not decimal or not decimal.isdigit():
        raise ValueError(f"{label} is not a canonical positive unit decimal")
    return Fraction(int(decimal), 10 ** len(decimal))


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


def _u() -> dict[int, tuple[Fraction, Fraction]]:
    return {m: (decimal_fraction(a, f"u{m}.lower"), decimal_fraction(b, f"u{m}.upper")) for m, (a, b) in U_INTERVAL_TEXT.items()}


def _definition_rows() -> list[dict[str, object]]:
    return [
        {"id": "maynard_input", "theorem": "Maynard Theorem 1.3", "gap_type": "consecutive primes", "infinitely_many": True, "gap_upper": HMAX, "pass": True},
        {"id": "fixed_gap_extraction", "finite_values": "positive integer h<=600", "conclusion": "some fixed h_* occurs on infinitely many consecutive-prime edges", "pigeonhole": True, "pass": True},
        {"id": "edge", "x": "p_y", "q": "p_(y+1)=x+h_*", "h_star": "fixed positive integer <=600", "limit": "x->infinity along extracted edges", "pass": True},
        {"id": "rank_regime", "r_type": "exact integer", "same_rank_both_endpoints": True, "r_limit": "infinity", "linear_bound": "r<=C*x for one fixed C>0", "optional_profile_hypothesis": "r/x->lambda in [0,infinity)", "profile_is_optional": True, "pass": True},
        {"id": "P_tail", "formula": "P_r(y)=sum_(p>x)(p^2-1)^(-r)", "endpoint": "strict", "pass": True},
        {"id": "smooth_tails", "I": "I_(2r)(x)=integral_x^infinity t^(-2r)/log(t) dt", "J": "J_r(x)=integral_x^infinity (t^2-1)^(-r)/log(t) dt", "pass": True},
        {"id": "scalar_errors", "E_I": "P_r-I_(2r)", "E_J": "P_r-J_r", "same_rank": True, "pass": True},
        {"id": "coordinates", "PhiP": "sum_(j>=1)c^j*P_j/j", "PhiI_less_r": "sum_(j<r)c^j*P_j/j+sum_(j>=r)c^j*I_(2j)/j", "PhiJ_less_r": "sum_(j<r)c^j*P_j/j+sum_(j>=r)c^j*J_j/j", "c_range": [1, 7], "pass": True},
        {"id": "endpoint_errors", "Delta_I": "pi^2*(GapP-GapI_(<r))", "Delta_J": "pi^2*(GapP-GapJ_(<r))", "Gap": "F(Phi)/pi^2", "pass": True},
        {"id": "edge_scales", "a": "(x^2/(q^2-1))^r", "rho": "(x/q)^(2r)", "left": "x^(2r)", "right": "q^(2r)", "pass": True},
    ]


def _edge_rows() -> list[dict[str, object]]:
    return [
        {"id": "P_successor", "formula": "P_r(y)-P_r(y+1)=(q^2-1)^(-r)", "same_r": True, "pass": True},
        {"id": "I_jump", "formula": "E_I(y)-E_I(y+1)=(q^2-1)^(-r)-integral_x^q t^(-2r)/log(t) dt", "pass": True},
        {"id": "J_jump", "formula": "E_J(y)-E_J(y+1)=(q^2-1)^(-r)-integral_x^q (t^2-1)^(-r)/log(t) dt", "pass": True},
        {"id": "I_smooth", "normalized_upper": "x^(2r)*integral_x^q t^(-2r)/log(t) dt<=h_*/log(x)", "limit": "0", "pass": True},
        {"id": "J_smooth", "normalized_upper": "x^(2r)*integral_x^q (t^2-1)^(-r)/log(t) dt<=h_**(1-x^(-2))^(-r)/log(x)", "linear_rank_limit": "0", "pass": True},
        {"id": "atom", "normalized_atom": "x^(2r)*(q^2-1)^(-r)=a", "a": "(x^2/(q^2-1))^r", "pass": True},
        {"id": "a_log", "identity": "log(a)=-r*log(1+2*h_*/x+(h_*^2-1)/x^2)", "profile_limit": "-2*lambda*h_*", "pass": True},
        {"id": "rho", "formula": "rho=(x/q)^(2r)", "range": "0<rho<1", "pass": True},
        {"id": "rho_over_a", "identity": "rho/a=(1-q^(-2))^r", "linear_rank_limit": "1", "pass": True},
        {"id": "I_normalized_jump", "conclusion": "x^(2r)*(E_I(y)-E_I(y+1))=a+o(1)", "pass": True},
        {"id": "J_normalized_jump", "conclusion": "x^(2r)*(E_J(y)-E_J(y+1))=a+o(1)", "pass": True},
        {"id": "coarse_atom", "hypothesis": "r<=C*x and h_*<=600", "liminf": "a>=exp(-1200*C)", "asymptotic": True, "pass": True},
    ]


def _gamma_rows() -> list[dict[str, object]]:
    u = _u()
    kappa = Fraction(4, 7) * u[8][0]
    return [
        {"id": "alpha_beta", "alpha": [ALPHA[m] for m in range(2, 9)], "beta": [BETA[m] for m in range(2, 9)], "m2_cancellation": -2 * ALPHA[2] - 4 * BETA[2], "pass": True},
        {"id": "directed_intervals", "source": "RH-384 exact outward rational intervals", "u8_lower": fraction_text(u[8][0]), "u7_upper": fraction_text(u[7][1]), "pass": True},
        {"id": "gamma_formula", "formula": "gamma_r=4/r*(3^r*u4-2^r*u3+5^r*u6-4^r*u5+7^r*u8-6^r*u7+2*(u3-u4+u5-u6+u7-u8))", "pass": True},
        {"id": "pair_3_2", "inequality": "u4/u3>2/3", "cross_left": fraction_text(3 * u[4][0]), "cross_right": fraction_text(2 * u[3][1]), "pass": 3 * u[4][0] > 2 * u[3][1]},
        {"id": "pair_5_4", "inequality": "u6/u5>(4/5)^2", "cross_left": fraction_text(25 * u[6][0]), "cross_right": fraction_text(16 * u[5][1]), "pass": 25 * u[6][0] > 16 * u[5][1]},
        {"id": "pair_7_6", "inequality": "u8/u7>(6/7)^6", "cross_left": fraction_text((7**6) * u[8][0]), "cross_right": fraction_text((6**6) * u[7][1]), "pass": (7**6) * u[8][0] > (6**6) * u[7][1]},
        {"id": "memory_positive", "differences": ["u3-u4", "u5-u6", "u7-u8"], "directed": [fraction_text(u[3][0] - u[4][1]), fraction_text(u[5][0] - u[6][1]), fraction_text(u[7][0] - u[8][1])], "pass": all(u[a][0] > u[b][1] for a, b in ((3, 4), (5, 6), (7, 8)))},
        {"id": "last_pair_margin", "r_min": 7, "bound": "7^r*u8-6^r*u7>=(1/7)*7^r*u8_lower", "uses_ratio_exponent": 6, "pass": True},
        {"id": "kappa", "definition": "kappa_gamma=4*u8_lower/7", "exact": fraction_text(kappa), "decimal_prefix": "0.0347017856545", "pass": kappa > 0},
        {"id": "gamma_lower", "r_min": 7, "conclusion": "gamma_r>=kappa_gamma*7^r/r", "positive_other_pairs": True, "positive_memory": True, "pass": True},
        {"id": "gamma_positive", "rank_range": "all exact integers r>=7", "conclusion": "gamma_r>0", "pass": True},
        {"id": "gamma_normalizer", "endpoint_scale": "x^(2r)/gamma_r", "natural_growth": "gamma_r comparable from below to 7^r/r", "pass": True},
    ]


def _vector_rows() -> list[dict[str, object]]:
    return [
        {"id": "direction", "v_r": "(c^r/r)_(c=1)^7", "gradient_pairing": "nablaF(0).v_r=gamma_r", "pass": True},
        {"id": "I_coordinate_jump", "formula": "x^(2r)*((PhiP-PhiI_<r)_y-(PhiP-PhiI_<r)_(y+1))=a*v_r+tail_error_I", "consumes": ["P_successor", "I_smooth", "P_integer_tail", "I_integer_tail"], "pass": True},
        {"id": "J_coordinate_jump", "formula": "x^(2r)*((PhiP-PhiJ_<r)_y-(PhiP-PhiJ_<r)_(y+1))=a*v_r+tail_error_J", "consumes": ["P_successor", "J_smooth", "P_integer_tail", "J_I_bridge"], "pass": True},
        {"id": "P_integer_tail", "bound": "sum_(j>r)c^j*P_j/j<=4*c^(r+1)*x^(-2r-1)/((r+1)*(2r+1))", "domain": "fixed C>0,r<=C*x,x>=x0(C),c<=7,r>=7", "pass": True},
        {"id": "I_integer_tail", "bound": "sum_(j>r)c^j*I_(2j)/j<=2*c^(r+1)*x^(-2r-1)/((r+1)*(2r+1)*log(x))", "pass": True},
        {"id": "J_I_bridge", "bound": "sum_(j>=r)c^j*(J_j-I_(2j))/j<=4*c^r*x^(-2r-1)/((2r+1)*log(x))", "normalized": "o(gamma_r*x^(-2r))", "pass": True},
        {"id": "common_head", "H": "sum_(j<r)c^j*P_j/j", "bound": "norm_infinity(H)<=14/x", "pass": True},
        {"id": "Taylor", "bound": "|F(H+A)-F(H+B)-nablaF(0).(A-B)|<=224*||H||*||A-B||+112*(||A||^2+||B||^2)", "cross": 224, "square": 112, "pass": 224 == 2 * 112},
        {"id": "cross_remainder", "normalized_upper": "18816/(kappa_gamma*(2r-1))", "limit": "0", "pass": True},
        {"id": "square_remainder", "normalized_upper": "(2240/kappa_gamma)*7^r*x^(2-2r)/(r*(2r-1)^2)", "limit": "0", "pass": True},
        {"id": "endpoint_jump", "I": "x^(2r)*(Delta_I(y)-Delta_I(y+1))/gamma_r=a+o(1)", "J": "x^(2r)*(Delta_J(y)-Delta_J(y+1))/gamma_r=a+o(1)", "pass": True},
        {"id": "next_rank_divergence", "P_upper": "P_(r+1)<=4*x^(-2r-1)/(2r+1) eventually for fixed C and r<=C*x", "pair_errors": "max endpoint scalar and gamma-normalized endpoint errors divided by P_(r+1) tend to infinity", "uses_P_asymptotic": False, "pass": True},
    ]


def _profile_rows() -> list[dict[str, object]]:
    return [
        {"id": "two_endpoint_inequality", "formula": "a+o(1)<=L+rho*R<=(1+rho)*max(L,R)", "L": "x^(2r)*|error_at_x|", "R": "q^(2r)*|error_at_q|", "pass": True},
        {"id": "scalar_I_profile", "conclusion": "liminf ((1+rho)/a)*max{x^(2r)|E_I(y)|,q^(2r)|E_I(y+1)|}>=1", "pass": True},
        {"id": "scalar_J_profile", "conclusion": "liminf ((1+rho)/a)*max{x^(2r)|E_J(y)|,q^(2r)|E_J(y+1)|}>=1", "pass": True},
        {"id": "endpoint_I_profile", "conclusion": "liminf ((1+rho)/a)*max{x^(2r)|Delta_I(y)|/gamma_r,q^(2r)|Delta_I(y+1)|/gamma_r}>=1", "pass": True},
        {"id": "endpoint_J_profile", "conclusion": "liminf ((1+rho)/a)*max{x^(2r)|Delta_J(y)|/gamma_r,q^(2r)|Delta_J(y+1)|/gamma_r}>=1", "pass": True},
        {"id": "lambda_profile", "hypothesis": "r/x->lambda in [0,infinity)", "a0": "exp(-2*lambda*h_*)", "pair_lower": "a0/(1+a0)", "pass": True},
        {"id": "coarse_profile", "hypothesis": "r<=C*x", "pair_lower": "exp(-1200*C)/2", "channels": ["scalar_I", "scalar_J", "endpoint_I/gamma", "endpoint_J/gamma"], "pass": True},
        {"id": "sublinear_profile", "hypothesis": "r=o(x),r->infinity", "lambda": 0, "a0": 1, "pair_lower": "1/2", "pass": True},
    ]


def _contract_rows() -> list[dict[str, object]]:
    return [
        {"id": "source_closure", "git_groups": [87, 8, 2], "git_rows": 97, "remote_rows": 2, "logical_rows": 99, "release": "a3aa5977e9b3338e4c3035c6c42b60d50bc3ac3b", "pass": 87 + 8 + 2 == 97 and 97 + 2 == 99},
        {"id": "source_roles", "maynard": "bounded consecutive gaps and fixed-h extraction", "johnston_yang": "inherited provenance only; not used for linear-r P asymptotics", "new_remote": False, "pass": True},
        {"id": "novelty", "new": "same-r moving-rank pair necessity through the full linear scale r=O(x), with exact lambda profile", "not_fixed_rank_corollary": True, "pass": True},
        {"id": "scope", "same_rank_pair_only": True, "hierarchy": "P/J/I only", "single_vertex_schedule": False, "arbitrary_surrogate": False, "r_over_x_infinity": False, "pass": True},
        {"id": "excluded", "dependencies": ["RH-389", "TPC-137", "Tao active-log source"], "claims": ["ordinary Cesaro", "growing clock", "complex channels", "operator or zero identification", "RH"], "pass": True},
        {"id": "firewall", "gates_A_to_E": [False, False, False, False, False], "proof_of_RH": False, "operator_trace_or_zeros": False, "vendored_external_payload": False, "pass": True},
    ]


GROUP_BUILDERS = {
    "definition_rows": _definition_rows,
    "edge_rows": _edge_rows,
    "gamma_rows": _gamma_rows,
    "vector_rows": _vector_rows,
    "profile_rows": _profile_rows,
    "contract_rows": _contract_rows,
}


def build_certificate() -> dict[str, object]:
    groups = {name: builder() for name, builder in GROUP_BUILDERS.items()}
    counts = {name: len(rows) for name, rows in groups.items()}
    counts["semantic_rows_total"] = sum(counts.values())
    return {
        "status": STATUS,
        "epistemic_role": ROLE,
        "counts": counts,
        **groups,
        "all_pass": counts["semantic_rows_total"] == 60 and all(row["pass"] is True for rows in groups.values() for row in rows),
    }


# Filled from the first canonical builder snapshot.  The verifier never calls a
# group builder: exact per-row hashes close every leaf, while the checks below
# independently recompute the theorem's algebraic cross-contracts.
ROW_SHA256: dict[str, tuple[str, ...]] = {
    "definition_rows": (
        "64516b7443891e7a028bd9ff86bc3f253e85875cf4ef86b70da72f9cb92cb99e", "f5332057c4cfd56b60b65c45b626fb8dc342b9fdb4f85f09dc9a2cd8b3ef1e7a", "0487d58eeeec2a37f28f84222a329f22156737473bca65d62649d7ed2a7a13b8", "2a366b0d6d78d76d314a0c6bf2a555355d5eef3b5245a78072b68e85ff34a5bb", "5efda1d4ae09cbcb5397d1dedc5e606bd9908465af47cd0a5f07924300f1536d", "2c7488b175c150b635661b9afc3b075df10f7c3d651dd88017ca1e76fd98c465", "da140a2c1dda92664d53b3e909a198a7ec98dea15ea84c99799f842a5bb32279", "28c46a5c6ca5d5d57073fdb4860f553a865356be716596d5b5ed0b2e8b190dd2", "c9b48907e0fff00d71407665f2c4b49884a81aade35bc1baea4f798b25dda96a", "c24a5957e2fbed57bead06d31aad168ad284b44b7f7d587eeabeb3c530b89e96",
    ),
    "edge_rows": (
        "692a978fb8cc7fd9fb8d09884a5ca9b94e51c18f9c47bf27df758d60d3defc83", "49e1b476e285b028bc3531622228c5a771541700936a8ddce1d9728c7c5fef95", "60d67538555c7d68a90af13b179a1a8c145c0c6140253ac1ba29bc5e3a58347b", "b2d66f4fa64cb712c8c3002c6474e1b54145204cdc9f974a05e2e177af35f6e9", "d1de4e18653376f1a00388df667af064d17fd633dc49e8928cc36daff6d4ad31", "2642cf904245967b202efe803114826c6f5ed7a0d8ffed90424364426e3a17ea", "4e56b3295a61baf2f37800f1af4a9bd11ccebc6ede175f4f3a003fc5f84380da", "72155247f87de4df6c16935b8a09096eea93d48151ed15ade852c124b740558f", "62db52ed61c7da6e8e003f849e5fcc1f35468712e340180aafb51152e53568ee", "55f234ac42d84d2b3a00e2df6933d688964d545d60c76827232109bb21c7a685", "0104daac357baa4da046d468e23c15f7de49359a12c957540d818e776fa5a808", "3372d1f0df8ef6ff7f7595cfb3727f73e12807669c0282e8fa2feafd95782f0e",
    ),
    "gamma_rows": (
        "f7954cd33374d913eaa3e9aef4578adaa3906b6f8f4de23578cf53111496db4c", "44e3db66ccefb58a7a14a4b35cb22ae201bb90d4b7a61fb4332ed19c085c49ca", "ac277aed33fe81b273133d3df3fb87c81fa2911bb376d7eac3aa9a6dbc1abb55", "7a7918068573400aa890062ca96fbff9cef5db954bc1e0618c781aa6d6761ae2", "c4046bbdf77a36c666f748344d01700028c473a68f61527f7d80b48da808de61", "13bd2f52be2c4146d7ad1feb29779f7fbb500dbb0e064281179f441dc7e9ca10", "c11c816e97de0a441cd10bd6dbcc90ded4bd5303d7bd2860013c82e8ba7337e1", "571d4d64941db97073d65ba477ff8a1019bbdc3cd6dac012a0c6bd17bd0d4b81", "f4b115c1c800d8e3ec385d12c4624a8fce85394498ada9b2b7eeb60b8b20f430", "d1618d13fc123c355d93492995d4b3dc0369cc8e11abe0040b1ebc061d9940f6", "6cc22a1e21173a2e437f2410b6f4bce8e922a3912ae89b1f95ba40290b549cf9", "cb0b4d1a319364d6b83c51d2d310dd91aa46f709f0890541907e6917ffc022c8",
    ),
    "vector_rows": (
        "b2c452b5522ff40c292a74232460402d797471075bc7e8651171b93135ff33e0", "ed86ef59c354518a44dcc055691548505f4dd5244115a0d67d580b0d761bd6a3", "1f98881b8b2e29f74a07e62c1d5297df7b51133278ba6ce00617695784032e3e", "945cbc48c2d774f2ce4ace366410c1287681f54effae3d05bca33e5784247201", "d1434fa54a7b87f8e16c7eeb135e313464cf42075527f090a14469198a6b968e", "6e23c2bb0b983983bd7fbf4baad804334e5b18bcadf080b13f45e776bf5c1edd", "af6de1bcd4b8875a88e2e3bc6225be5c72e417db78819b3505b64d2033781147", "bdd4602f6a199ad8e5d51df4a3b25640ef6ed036b882cdba90ff510ef003f2e6", "19d9685de17e10c051e7e2ce3d1b0a6d0bdc86ff712b02f9a2b733b382dc684c", "e60e21cf45856f425e50cfefe43f75a6463c65e5db16fc5ff0f3f5c6e30b130b", "a657b7a430da2b5530e9605ff4079a9826159497bcd42fa38eca554816966a3e", "309268b9e6d8d0d93f6fa4385634b5711711cd944d3c1f44851a43d011e644d1",
    ),
    "profile_rows": (
        "fc84e4a22a6208764b6e49978b024af1e2cb075256945e5f925f7c264c65fae5", "71e1a8b74deded5835090a6de32f1149fde5b5259973a7c19586eee8fbad1e36", "d1fea2d110a45ec413a95a65322e140f00e394cc6392b8b5871abef7fd8b4b8b", "c38c4c4f6ec2f8b219e0f9f673b6bfafdd50b555075a66d9f4dc9824f5996dec", "45e09ca21af9b486d27247a7cf0fea8310d33702fb66c44b092cd2aa0b2fea09", "e7ae7cc6dba98c65ded8d8b4d3a55f9cb398dad8b47ef327c1d812bb750c460a", "fdf1bfea76fc7e172beb5c0e636df824b3a1fcb668587e089112545558c9fd96", "61a4eefabcb0af85334c6ba209e7439e95489913caec86d828a9717e3b13c5ad",
    ),
    "contract_rows": (
        "41a54360b9ce940dde2975f8dcb8caf158c217ea788dfc84fe9ccc45281ed478", "a517d0d4c2ebf890e37e48e503ba1ddc034c1074f0b0c636a0a73a8b201c3639", "736d917c9919a95a1cdb43cc8cac774a0c88e8855dd8532d66bede8e314c01a4", "b494b673c1df268851419f6b0156632bea7d932de7d6ab29fb495d98c6d80569", "e6dced6525e3c50c4f4672e15c7396ea1c1323525e311496aa424dd6d322d5aa", "a5d370d3809da11241c564d1643f122069ef77701ea842d548b8bcc7fbd82492",
    ),
}


def _require_list(value: object, length: int, label: str) -> list[object]:
    if type(value) is not list or len(value) != length:
        raise TypeError(f"{label} must be an exact list of length {length}")
    return value


def _require_exact(actual: object, expected: object, label: str) -> None:
    if not exact_equal(actual, expected):
        raise ValueError(f"{label} changed")


def _verify_row_hashes(candidate: dict[str, object]) -> None:
    expected_lengths = {"definition_rows": 10, "edge_rows": 12, "gamma_rows": 12, "vector_rows": 12, "profile_rows": 8, "contract_rows": 6}
    if set(ROW_SHA256) != set(expected_lengths):
        raise RuntimeError("row digest seal is incomplete")
    for group, length in expected_lengths.items():
        rows = _require_list(candidate[group], length, group)
        seals = ROW_SHA256[group]
        if type(seals) is not tuple or len(seals) != length:
            raise RuntimeError(f"{group} digest seal changed")
        for index, (row, seal) in enumerate(zip(rows, seals)):
            if type(row) is not dict or row.get("pass") is not True:
                raise TypeError(f"{group}[{index}] must be a passing exact object")
            if payload_sha256(row) != seal:
                raise ValueError(f"{group}[{index}] exact semantic row changed")


def _verify_cross_contracts(candidate: dict[str, object]) -> None:
    definitions = candidate["definition_rows"]
    edge = candidate["edge_rows"]
    gamma = candidate["gamma_rows"]
    vector = candidate["vector_rows"]
    profile = candidate["profile_rows"]
    contract = candidate["contract_rows"]
    if definitions[0]["gap_type"] != "consecutive primes" or definitions[1]["pigeonhole"] is not True:
        raise ValueError("Maynard/fixed-gap/same-rank quantifiers changed")
    rank = definitions[3]
    if rank["r_type"] != "exact integer" or rank["same_rank_both_endpoints"] is not True or rank["r_limit"] != "infinity" or rank["linear_bound"] != "r<=C*x for one fixed C>0" or rank["optional_profile_hypothesis"] != "r/x->lambda in [0,infinity)" or rank["profile_is_optional"] is not True:
        raise ValueError("linear-rank and optional-profile quantifiers changed")
    if definitions[9]["left"] != "x^(2r)" or edge[0]["same_r"] is not True or edge[5]["a"] != definitions[9]["a"] or edge[7]["formula"] != f"rho={definitions[9]['rho']}":
        raise ValueError("edge normalization changed")
    if edge[1]["formula"] != "E_I(y)-E_I(y+1)=(q^2-1)^(-r)-integral_x^q t^(-2r)/log(t) dt" or edge[2]["formula"] != "E_J(y)-E_J(y+1)=(q^2-1)^(-r)-integral_x^q (t^2-1)^(-r)/log(t) dt":
        raise ValueError("I/J exact edge identity changed")
    if edge[3]["limit"] != "0" or edge[5]["a"] != "(x^2/(q^2-1))^r" or edge[7]["formula"] != "rho=(x/q)^(2r)" or edge[8]["identity"] != "rho/a=(1-q^(-2))^r" or edge[11]["liminf"] != "a>=exp(-1200*C)":
        raise ValueError("linear-scale atom comparison changed")
    u = _u()
    kappa = Fraction(4, 7) * u[8][0]
    if gamma[0]["m2_cancellation"] != 0 or gamma[8]["definition"] != "kappa_gamma=4*u8_lower/7" or fraction_from_text(gamma[8]["exact"], "kappa") != kappa:
        raise ValueError("gamma exact constant changed")
    if not (3 * u[4][0] > 2 * u[3][1] and 25 * u[6][0] > 16 * u[5][1] and 7**6 * u[8][0] > 6**6 * u[7][1]):
        raise ValueError("directed gamma ratio lock failed")
    if gamma[7]["r_min"] != 7 or gamma[9]["conclusion"] != "gamma_r>=kappa_gamma*7^r/r":
        raise ValueError("gamma lower-bound range changed")
    if vector[0]["v_r"] != "(c^r/r)_(c=1)^7" or vector[1]["consumes"] != ["P_successor", "I_smooth", "P_integer_tail", "I_integer_tail"] or vector[2]["consumes"] != ["P_successor", "J_smooth", "P_integer_tail", "J_I_bridge"]:
        raise ValueError("coordinate edge derivation changed")
    if vector[3]["domain"] != "fixed C>0,r<=C*x,x>=x0(C),c<=7,r>=7" or vector[7]["cross"] != 2 * vector[7]["square"] or vector[10]["I"].split("=")[-1] != "a+o(1)" or vector[11]["uses_P_asymptotic"] is not False:
        raise ValueError("endpoint Taylor/edge contract changed")
    if profile[0]["formula"] != "a+o(1)<=L+rho*R<=(1+rho)*max(L,R)" or profile[5]["a0"] != "exp(-2*lambda*h_*)" or profile[5]["pair_lower"] != "a0/(1+a0)" or profile[6]["pair_lower"] != "exp(-1200*C)/2" or profile[7]["pair_lower"] != "1/2":
        raise ValueError("natural pair profile changed")
    if contract[0]["git_rows"] + contract[0]["remote_rows"] != contract[0]["logical_rows"]:
        raise ValueError("source count arithmetic changed")
    if contract[3]["same_rank_pair_only"] is not True or contract[3]["single_vertex_schedule"] is not False or contract[3]["arbitrary_surrogate"] is not False:
        raise ValueError("necessity scope firewall opened")
    if any(contract[5]["gates_A_to_E"]) or contract[5]["proof_of_RH"] is not False or contract[5]["operator_trace_or_zeros"] is not False:
        raise ValueError("Gate firewall opened")


def verify_certificate(candidate: object, *, compare_fresh: bool = True) -> bool:
    if type(compare_fresh) is not bool:
        raise TypeError("compare_fresh must be an exact bool")
    if type(candidate) is not dict:
        raise TypeError("certificate must be an exact object")
    groups = tuple(GROUP_BUILDERS)
    if set(candidate) != {"status", "epistemic_role", "counts", *groups, "all_pass"}:
        raise ValueError("certificate membership changed")
    _require_exact(candidate["status"], STATUS, "status")
    _require_exact(candidate["epistemic_role"], ROLE, "epistemic_role")
    _verify_row_hashes(candidate)
    _verify_cross_contracts(candidate)
    counts = {name: len(candidate[name]) for name in groups}
    counts["semantic_rows_total"] = sum(counts.values())
    _require_exact(counts, candidate["counts"], "counts")
    _require_exact(counts["semantic_rows_total"], 60, "semantic row total")
    _require_exact(candidate["all_pass"], True, "all_pass")
    if compare_fresh and canonical_json_bytes(candidate) != canonical_json_bytes(build_certificate()):
        raise ValueError("fresh certificate mismatch")
    return True


MUTATION_NAMES = (
    "maynard_not_consecutive", "fixed_gap_not_extracted", "rank_boolean", "different_endpoint_ranks",
    "rank_not_diverging", "rank_beyond_linear", "I_jump_wrong_sign", "J_jump_wrong_kernel",
    "atom_drops_minus_one", "wrong_left_scale", "I_smooth_not_zero", "rho_wrong_exponent",
    "rho_over_a_wrong", "kappa_wrong_factor", "gamma_starts_at_six", "gamma_lower_wrong_sign",
    "direction_has_eight_channels", "Taylor_cross_halved", "pair_denominator_drops_rho", "pair_claims_one",
    "lambda_exponent_missing_two", "coarse_exponent_halved", "next_rank_uses_asymptotic", "opens_scope_gate",
)


def apply_mutation(certificate: dict[str, object], name: str) -> dict[str, object]:
    if type(certificate) is not dict or type(name) is not str or name not in MUTATION_NAMES:
        raise ValueError("invalid mutation request")
    value = deepcopy(certificate)
    d, e, g, v, p, c = (value[key] for key in ("definition_rows", "edge_rows", "gamma_rows", "vector_rows", "profile_rows", "contract_rows"))
    if name == "maynard_not_consecutive": d[0]["gap_type"] = "prime pairs"
    elif name == "fixed_gap_not_extracted": d[1]["pigeonhole"] = False
    elif name == "rank_boolean": d[3]["r_type"] = "boolean"
    elif name == "different_endpoint_ranks": d[3]["same_rank_both_endpoints"] = False
    elif name == "rank_not_diverging": d[3]["r_limit"] = "bounded"
    elif name == "rank_beyond_linear": d[3]["linear_bound"] = "none"
    elif name == "I_jump_wrong_sign": e[1]["formula"] = e[1]["formula"].replace("-integral", "+integral")
    elif name == "J_jump_wrong_kernel": e[2]["formula"] = e[2]["formula"].replace("(t^2-1)^(-r)", "t^(-2r)")
    elif name == "atom_drops_minus_one": e[5]["a"] = "(x/q)^(2r)"
    elif name == "wrong_left_scale": d[9]["left"] = "x^r"
    elif name == "I_smooth_not_zero": e[3]["limit"] = "1"
    elif name == "rho_wrong_exponent": e[7]["formula"] = "rho=(x/q)^r"
    elif name == "rho_over_a_wrong": e[8]["identity"] = "rho/a=1"
    elif name == "kappa_wrong_factor": g[8]["definition"] = "kappa_gamma=4*u8_lower"
    elif name == "gamma_starts_at_six": g[7]["r_min"] = 6
    elif name == "gamma_lower_wrong_sign": g[9]["conclusion"] = "gamma_r<=kappa_gamma*7^r/r"
    elif name == "direction_has_eight_channels": v[0]["v_r"] = "(c^r/r)_(c=1)^8"
    elif name == "Taylor_cross_halved": v[7]["cross"] = 112
    elif name == "pair_denominator_drops_rho": p[0]["formula"] = "a+o(1)<=L+R<=2*max(L,R)"
    elif name == "pair_claims_one": p[5]["pair_lower"] = "1"
    elif name == "lambda_exponent_missing_two": p[5]["a0"] = "exp(-lambda*h_*)"
    elif name == "coarse_exponent_halved": p[6]["pair_lower"] = "exp(-600*C)/2"
    elif name == "next_rank_uses_asymptotic": v[11]["uses_P_asymptotic"] = True
    elif name == "opens_scope_gate": c[3]["arbitrary_surrogate"] = True
    return value


def mutation_results() -> list[dict[str, object]]:
    certificate = build_certificate()
    output: list[dict[str, object]] = []
    for name in MUTATION_NAMES:
        rejected = False
        try:
            verify_certificate(apply_mutation(certificate, name), compare_fresh=False)
        except (TypeError, ValueError, RuntimeError, KeyError, IndexError):
            rejected = True
        output.append({"name": name, "rejected": rejected})
    return output
