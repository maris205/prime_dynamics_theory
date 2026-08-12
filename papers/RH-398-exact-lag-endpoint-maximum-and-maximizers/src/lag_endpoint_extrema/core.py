"""Exact finite certificate for the RH-396 lag-endpoint extrema.

The module reproduces the local path-deletion algebra, the finite Euler-product
identities, and the equality/strictness bookkeeping used to classify the global
maximum of ``B_infinity(h)``.  It intentionally does not re-run or replace the
fixed-lag analytic terminal theorem of RH-396.  Every formal oracle below is
integer- or :class:`fractions.Fraction`-valued.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
import math
from typing import Iterable, Sequence


TITLE = "Exact Lag Endpoint Maximum and Maximizers"
PACKAGE = "lag_endpoint_extrema"
MAXIMIZER_SMALL_PRIME_PRODUCT = 210
THEOREM_GAP = Fraction(2, 1_334_025)
CYLINDER_GAP = Fraction(1, 36_750)

GROUP_IDS = {
    "loss_formula": (
        "LF01_oddT_oddL", "LF02_oddT_evenL", "LF03_evenT_oddL",
        "LF04_evenT_evenL", "LF05_T1_edge", "LF06_T2_edge",
        "LF07_L1_edge", "LF08_L2_edge", "LF09_preperiod_L_lt_T",
        "LF10_threshold_L_eq_T", "LF11_postthreshold_L_gt_T",
        "LF12_enumerator_grid",
    ),
    "local_order": (
        "LO01_t_exponent_map", "LO02_oddprime_e0_ge_e1",
        "LO03_oddprime_e1_ge_e2", "LO04_oddL_threeway_equal",
        "LO05_evenL_e0_eq_e1_below_p", "LO06_first_e0e1_strict",
        "LO07_evenL_e1e2_strict", "LO08_two_prime_allowed_order",
        "LO09_p2_L2_strict", "LO10_p3_L4_strict",
        "LO11_p5_L6_strict", "LO12_p7_L8_strict",
    ),
    "telescope": (
        "TS01_t_p_gcd_formula", "TS02_A_product", "TS03_p0_definition",
        "TS04_A_cutoff", "TS05_R_second_difference",
        "TS06_R_nonnegative_event", "TS07_alternating_sum_start",
        "TS08_alternating_sum_terminal", "TS09_B_telescope_identity",
        "TS10_odd_forward_run_event", "TS11_finite_CRT_oracle",
        "TS12_collision_exponent_oracle",
    ),
    "strictness": (
        "ST01_square_p2", "ST02_square_p3", "ST03_square_p5",
        "ST04_square_generic", "ST05_single_p3", "ST06_single_p5",
        "ST07_single_p7", "ST08_boundary_CRT_L2",
        "ST09_boundary_CRT_L4", "ST10_boundary_CRT_L6",
        "ST11_boundary_CRT_L8", "ST12_nonmax_partition",
    ),
    "maximizers": (
        "MX01_base_h1", "MX02_largeprime_invisibility",
        "MX03_multiprime_invisibility", "MX04_true_examples",
        "MX05_false_smallprime_examples", "MX06_false_square_examples",
        "MX07_exhaustive_predicate_grid", "MX08_exact_iff",
    ),
    "complement_gap": (
        "CG01_square_sequence", "CG02_sequence_strict",
        "CG03_sequence_upper_bound", "CG04_sequence_limit",
        "CG05_complement_sup", "CG06_complement_unattained",
        "CG07_p0_ge5_reduction", "CG08_uniform_gap_chain",
    ),
    "joint_endpoint": (
        "JE01_fixed_pair_strict", "JE02_h1_cofinal_lower",
        "JE03_joint_supremum", "JE04_joint_nonattainment",
    ),
    "firewalls": (
        "FW01_quantifier_order", "FW02_data_scope", "FW03_source_roles",
        "FW04_claim_ceiling",
    ),
}
ROW_PARTITION = {group: len(ids) for group, ids in GROUP_IDS.items()}
CERTIFICATE_FIXTURE_ROWS = 72
CERTIFICATE_FIXTURE_BYTES = 36_635
CERTIFICATE_FIXTURE_SHA256 = "d47de091a8fe5a134ba4bbf8ac4689f53b54786d45dc3bfc7061c99b46bea741"

MUTATION_NAMES = (
    "loss_ceil_to_floor", "loss_enumerator_omits_residue_zero",
    "oddT_oddL_wrong_branch", "oddT_evenL_drops_max",
    "evenT_oddL_drops_min", "evenT_evenL_nonzero",
    "preperiod_threshold_shift", "loss_grid_hides_failure",
    "t_map_min_to_max", "t_map_omit_gcd", "t_map_all_p2",
    "local_score_denominator_p", "local_order_swap_e0_e1",
    "local_order_swap_e1_e2", "odd_even_equality_promoted",
    "p2_gap_wrong", "p3_gap_wrong", "p5_gap_wrong", "p7_gap_wrong",
    "A_product_min_to_max", "A_cutoff_missing", "R_left_sign_flip",
    "R_right_index_shift", "alternating_start_negative",
    "alternating_terminal_included", "odd_run_to_even_run",
    "CRT_support_drops_7", "collision_exponent_ignored",
    "omit_square_strict", "drop_single_p3", "drop_single_p5",
    "drop_single_p7", "partition_squarefree_only", "partition_gcd_only",
    "maximizer_210_to_30", "maximizer_210_to_42",
    "maximizer_210_to_70", "maximizer_210_to_105",
    "invisible_prime_threshold_7", "exact_iff_or",
    "square_sequence_p2_to_p", "sequence_gap_zero_allowed",
    "sequence_bound_sign_flip", "complement_max_attained",
    "complement_sup_to_max", "p0_reduction_drops_3",
    "cylinder_omit_2", "cylinder_omit_5", "cylinder_omit_7",
    "cylinder_omit_tail", "cylinder_omit_local_loss",
    "gap_constant_wrong", "gap_direction_flip", "finite_pair_attained",
    "joint_sup_to_max", "q_max_before_limit", "claim_growing_h",
    "RH397_promoted_analytic", "claim_monotonic_h",
    "claim_ordinary_Cesaro", "claim_causal", "claim_operator",
    "claim_RH_Gates", "lag_infimum_attained", "lag_infimum_value_wrong",
    "RH396_endpoint_input_omitted",
)

MUTATION_TARGETS = (
    ("loss_ceil_to_floor", "LF01_oddT_oddL"),
    ("loss_enumerator_omits_residue_zero", "LF12_enumerator_grid"),
    ("oddT_oddL_wrong_branch", "LF01_oddT_oddL"),
    ("oddT_evenL_drops_max", "LF02_oddT_evenL"),
    ("evenT_oddL_drops_min", "LF03_evenT_oddL"),
    ("evenT_evenL_nonzero", "LF04_evenT_evenL"),
    ("preperiod_threshold_shift", "LF09_preperiod_L_lt_T"),
    ("loss_grid_hides_failure", "LF12_enumerator_grid"),
    ("t_map_min_to_max", "LO01_t_exponent_map"),
    ("t_map_omit_gcd", "TS01_t_p_gcd_formula"),
    ("t_map_all_p2", "LO01_t_exponent_map"),
    ("local_score_denominator_p", "LO02_oddprime_e0_ge_e1"),
    ("local_order_swap_e0_e1", "LO02_oddprime_e0_ge_e1"),
    ("local_order_swap_e1_e2", "LO03_oddprime_e1_ge_e2"),
    ("odd_even_equality_promoted", "LO04_oddL_threeway_equal"),
    ("p2_gap_wrong", "LO09_p2_L2_strict"),
    ("p3_gap_wrong", "LO10_p3_L4_strict"),
    ("p5_gap_wrong", "LO11_p5_L6_strict"),
    ("p7_gap_wrong", "LO12_p7_L8_strict"),
    ("A_product_min_to_max", "TS02_A_product"),
    ("A_cutoff_missing", "TS04_A_cutoff"),
    ("R_left_sign_flip", "TS05_R_second_difference"),
    ("R_right_index_shift", "TS05_R_second_difference"),
    ("alternating_start_negative", "TS07_alternating_sum_start"),
    ("alternating_terminal_included", "TS08_alternating_sum_terminal"),
    ("odd_run_to_even_run", "TS10_odd_forward_run_event"),
    ("CRT_support_drops_7", "TS11_finite_CRT_oracle"),
    ("collision_exponent_ignored", "TS12_collision_exponent_oracle"),
    ("omit_square_strict", "ST01_square_p2"),
    ("drop_single_p3", "ST05_single_p3"),
    ("drop_single_p5", "ST06_single_p5"),
    ("drop_single_p7", "ST07_single_p7"),
    ("partition_squarefree_only", "ST12_nonmax_partition"),
    ("partition_gcd_only", "ST12_nonmax_partition"),
    ("maximizer_210_to_30", "MX08_exact_iff"),
    ("maximizer_210_to_42", "MX08_exact_iff"),
    ("maximizer_210_to_70", "MX08_exact_iff"),
    ("maximizer_210_to_105", "MX08_exact_iff"),
    ("invisible_prime_threshold_7", "MX02_largeprime_invisibility"),
    ("exact_iff_or", "MX08_exact_iff"),
    ("square_sequence_p2_to_p", "CG01_square_sequence"),
    ("sequence_gap_zero_allowed", "CG02_sequence_strict"),
    ("sequence_bound_sign_flip", "CG03_sequence_upper_bound"),
    ("complement_max_attained", "CG06_complement_unattained"),
    ("complement_sup_to_max", "CG05_complement_sup"),
    ("p0_reduction_drops_3", "CG07_p0_ge5_reduction"),
    ("cylinder_omit_2", "CG08_uniform_gap_chain"),
    ("cylinder_omit_5", "CG08_uniform_gap_chain"),
    ("cylinder_omit_7", "CG08_uniform_gap_chain"),
    ("cylinder_omit_tail", "CG08_uniform_gap_chain"),
    ("cylinder_omit_local_loss", "CG08_uniform_gap_chain"),
    ("gap_constant_wrong", "CG08_uniform_gap_chain"),
    ("gap_direction_flip", "CG08_uniform_gap_chain"),
    ("finite_pair_attained", "JE01_fixed_pair_strict"),
    ("joint_sup_to_max", "JE03_joint_supremum"),
    ("q_max_before_limit", "FW01_quantifier_order"),
    ("claim_growing_h", "FW02_data_scope"),
    ("RH397_promoted_analytic", "FW03_source_roles"),
    ("claim_monotonic_h", "FW04_claim_ceiling"),
    ("claim_ordinary_Cesaro", "FW04_claim_ceiling"),
    ("claim_causal", "FW04_claim_ceiling"),
    ("claim_operator", "FW04_claim_ceiling"),
    ("claim_RH_Gates", "FW04_claim_ceiling"),
    ("lag_infimum_attained", "JE04_joint_nonattainment"),
    ("lag_infimum_value_wrong", "JE04_joint_nonattainment"),
    ("RH396_endpoint_input_omitted", "FW03_source_roles"),
)

# Each semantic mutation changes one named theorem-bearing leaf in one row.
_MUTATION_EDITS: dict[str, tuple[tuple[object, ...], object, object]] = {
    "loss_ceil_to_floor": (("alpha_formula",), "a(L)=(L+1)//2", "a(L)=L//2"),
    "loss_enumerator_omits_residue_zero": (("residue_range",), "0<=r<T", "1<=r<T"),
    "oddT_oddL_wrong_branch": (("formula",), "Lambda_T(L)=a(L)", "Lambda_T(L)=0"),
    "oddT_evenL_drops_max": (("formula",), "Lambda_T(L)=max(0,L/2-(T-1)/2)", "Lambda_T(L)=L/2-(T-1)/2"),
    "evenT_oddL_drops_min": (("formula",), "Lambda_T(L)=min(a(L),T/2)", "Lambda_T(L)=T/2"),
    "evenT_evenL_nonzero": (("formula",), "Lambda_T(L)=0", "Lambda_T(L)=a(L)"),
    "preperiod_threshold_shift": (("condition",), "L<T", "L<=T"),
    "loss_grid_hides_failure": (("failures",), [], [{"period": 1, "length": 1}]),
    "t_map_min_to_max": (("exponent_map",), "t_p=p^(2-min(v_p(d),2))", "t_p=p^(2-max(v_p(d),2))"),
    "t_map_omit_gcd": (("formula",), "t_p(d)=p^2/gcd(d,p^2)", "t_p(d)=p^2/d"),
    "t_map_all_p2": (("values",), ["p^2", "p", "1"], ["p^2", "p^2", "p^2"]),
    "local_score_denominator_p": (("formula",), "V_(p,e)=a-Lambda_(p^(2-e))/p^2", "V_(p,e)=a-Lambda_(p^(2-e))/p"),
    "local_order_swap_e0_e1": (("order",), "V_(p,0)>=V_(p,1)", "V_(p,1)>=V_(p,0)"),
    "local_order_swap_e1_e2": (("order",), "V_(p,1)>=V_(p,2)", "V_(p,2)>=V_(p,1)"),
    "odd_even_equality_promoted": (("odd_L_equal_only",), True, False),
    "p2_gap_wrong": (("gap",), "1/4", "0"),
    "p3_gap_wrong": (("gap_e0_e1",), "1/9", "0"),
    "p5_gap_wrong": (("gap_e0_e1",), "1/25", "0"),
    "p7_gap_wrong": (("gap_e0_e1",), "1/49", "0"),
    "A_product_min_to_max": (("formula",), "A_m=prod_p(1-min(m,t_p)/p^2)", "A_m=prod_p(1-max(m,t_p)/p^2)"),
    "A_cutoff_missing": (("zero_for_m_at_least_p0_squared",), True, False),
    "R_left_sign_flip": (("formula",), "R_l=A_l-2A_(l+1)+A_(l+2)", "R_l=-A_l-2A_(l+1)+A_(l+2)"),
    "R_right_index_shift": (("right_index",), "l+2", "l+1"),
    "alternating_start_negative": (("first_sign",), "+", "-"),
    "alternating_terminal_included": (("last_index",), "p0^2-1", "p0^2"),
    "odd_run_to_even_run": (("event",), "forward_positive_run_length_is_odd", "forward_positive_run_length_is_even"),
    "CRT_support_drops_7": (("prime_support",), [2, 3, 5, 7], [2, 3, 5]),
    "collision_exponent_ignored": (("deduplicate_mod_p2",), True, False),
    "omit_square_strict": (("strict",), True, False),
    "drop_single_p3": (("strict",), True, False),
    "drop_single_p5": (("strict",), True, False),
    "drop_single_p7": (("strict",), True, False),
    "partition_squarefree_only": (("criterion",), "mu^2(h)=1 and gcd(h,210)=1", "mu^2(h)=1"),
    "partition_gcd_only": (("criterion",), "mu^2(h)=1 and gcd(h,210)=1", "gcd(h,210)=1"),
    "maximizer_210_to_30": (("small_prime_product",), 210, 30),
    "maximizer_210_to_42": (("small_prime_product",), 210, 42),
    "maximizer_210_to_70": (("small_prime_product",), 210, 70),
    "maximizer_210_to_105": (("small_prime_product",), 210, 105),
    "invisible_prime_threshold_7": (("prime_at_least",), 11, 7),
    "exact_iff_or": (("logical_connector",), "and", "or"),
    "square_sequence_p2_to_p": (("sequence",), "h=p^2 for prime p>=11", "h=p for prime p>=11"),
    "sequence_gap_zero_allowed": (("strict_lower",), "0<B1-B_(p^2)", "0<=B1-B_(p^2)"),
    "sequence_bound_sign_flip": (("upper",), "B1-B_(p^2)<=1/p^2", "B_(p^2)-B1<=1/p^2"),
    "complement_max_attained": (("attained",), False, True),
    "complement_sup_to_max": (("extremum",), "supremum", "maximum"),
    "p0_reduction_drops_3": (("three_divides_d",), True, False),
    "cylinder_omit_2": (("factors",), ["1/2", "1/25", "1/49", "tail>3/5", "local_loss=1/9"], ["1/25", "1/49", "tail>3/5", "local_loss=1/9"]),
    "cylinder_omit_5": (("factors",), ["1/2", "1/25", "1/49", "tail>3/5", "local_loss=1/9"], ["1/2", "1/49", "tail>3/5", "local_loss=1/9"]),
    "cylinder_omit_7": (("factors",), ["1/2", "1/25", "1/49", "tail>3/5", "local_loss=1/9"], ["1/2", "1/25", "tail>3/5", "local_loss=1/9"]),
    "cylinder_omit_tail": (("tail_lower",), "3/5", "0"),
    "cylinder_omit_local_loss": (("local_loss",), "1/9", "0"),
    "gap_constant_wrong": (("theorem_gap",), "2/1334025", "1/1334025"),
    "gap_direction_flip": (("chain",), "B1-Bh>=B1-B3>1/36750>2/1334025", "Bh-B1>2/1334025"),
    "finite_pair_attained": (("finite_pair_strict",), True, False),
    "joint_sup_to_max": (("extremum",), "supremum", "maximum"),
    "q_max_before_limit": (("prelimit_maximum",), False, True),
    "claim_growing_h": (("growing_h",), False, True),
    "RH397_promoted_analytic": (("RH397_analytic_input",), False, True),
    "claim_monotonic_h": (("monotonicity_in_h",), False, True),
    "claim_ordinary_Cesaro": (("ordinary_Cesaro",), False, True),
    "claim_causal": (("causal_online",), False, True),
    "claim_operator": (("operator",), False, True),
    "claim_RH_Gates": (("RH_or_Gates_A_E",), False, True),
    "lag_infimum_attained": (("infimum_attained",), False, True),
    "lag_infimum_value_wrong": (("retained_infimum",), "inf_h B_infinity(h)=3/pi^2", "inf_h B_infinity(h)=6/pi^2"),
    "RH396_endpoint_input_omitted": (("RH396",), "sole_load_bearing_theorem_and_analytic_endpoint_input_equations_18_21_Theorem_1_3_equation_22_Corollary_1_4_equation_23", "comparison_only"),
}


def _require_positive_int(value: object, name: str) -> int:
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive exact integer")
    return value


def _require_nonnegative_int(value: object, name: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative exact integer")
    return value


def _pairs_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def _reject_constant(token: str) -> object:
    raise ValueError(f"non-finite JSON constant: {token}")


def loads_strict(text: str) -> object:
    if type(text) is not str:
        raise TypeError("strict JSON input must be exact text")
    return json.loads(
        text,
        object_pairs_hook=_pairs_no_duplicates,
        parse_constant=_reject_constant,
    )


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return tuple(left) == tuple(right) and all(
            exact_equal(left[key], right[key]) for key in left
        )
    if type(left) is list:
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right)
        )
    if type(left) is tuple:
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right)
        )
    return left == right


def fraction_text(value: Fraction) -> str:
    if type(value) is not Fraction:
        raise TypeError("fraction serializer requires an exact Fraction")
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def factorization(value: int) -> tuple[tuple[int, int], ...]:
    value = _require_positive_int(value, "factorization input")
    remaining = value
    output: list[tuple[int, int]] = []
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            output.append((prime, exponent))
        prime += 1
    if remaining > 1:
        output.append((remaining, 1))
    return tuple(output)


def is_prime(value: object) -> bool:
    if type(value) is not int or value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


@lru_cache(maxsize=None)
def primes_through(limit: int) -> tuple[int, ...]:
    limit = _require_positive_int(limit, "prime cutoff")
    if limit < 2:
        return ()
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return tuple(index for index in range(2, limit + 1) if sieve[index])


def valuation(value: int, prime: int) -> int:
    value = _require_positive_int(value, "valuation input")
    if not is_prime(prime):
        raise ValueError("valuation base must be prime")
    exponent = 0
    while value % prime == 0:
        value //= prime
        exponent += 1
    return exponent


def squarefree(value: int) -> bool:
    value = _require_positive_int(value, "squarefree input")
    return all(exponent == 1 for _prime, exponent in factorization(value))


def mobius_squared(value: int) -> int:
    return 1 if squarefree(value) else 0


def first_prime_not_dividing(value: int) -> int:
    value = _require_positive_int(value, "nondivisor input")
    candidate = 2
    while True:
        if is_prime(candidate) and value % candidate:
            return candidate
        candidate += 1


def local_level(d: int, prime: int) -> int:
    d = _require_positive_int(d, "step d")
    if not is_prime(prime):
        raise ValueError("local level requires a prime")
    return min(valuation(d, prime), 2)


def local_orbit_length(d: int, prime: int) -> int:
    d = _require_positive_int(d, "step d")
    if not is_prime(prime):
        raise ValueError("orbit length requires a prime")
    prime_square = prime * prime
    return prime_square // math.gcd(d, prime_square)


def local_survival_factor(d: int, prime: int, length: int) -> Fraction:
    d = _require_positive_int(d, "step d")
    length = _require_positive_int(length, "block length")
    if not is_prime(prime):
        raise ValueError("local survival factor requires a prime")
    prime_square = prime * prime
    orbit = local_orbit_length(d, prime)
    return Fraction(prime_square - min(length, orbit), prime_square)


def residue_count(d: int, prime: int, indices: Iterable[int]) -> int:
    d = _require_positive_int(d, "step d")
    if not is_prime(prime):
        raise ValueError("residue count requires a prime")
    values = tuple(indices)
    if any(type(index) is not int for index in values):
        raise TypeError("indices must be exact integers")
    if len(set(values)) != len(values):
        raise ValueError("indices must be distinct")
    modulus = prime * prime
    return len({d * index % modulus for index in values})


def D_finite(d: int, support: Sequence[int], indices: Iterable[int]) -> Fraction:
    d = _require_positive_int(d, "step d")
    primes = tuple(support)
    if len(set(primes)) != len(primes) or any(not is_prime(p) for p in primes):
        raise ValueError("support must contain distinct primes")
    index_tuple = tuple(indices)
    if any(type(index) is not int for index in index_tuple):
        raise TypeError("indices must be exact integers")
    if len(set(index_tuple)) != len(index_tuple):
        raise ValueError("indices must be distinct")
    output = Fraction(1)
    for prime in primes:
        prime_square = prime * prime
        output *= Fraction(
            prime_square - residue_count(d, prime, index_tuple), prime_square
        )
    return output


def A_finite(d: int, support: Sequence[int], length: int) -> Fraction:
    length = _require_positive_int(length, "block length")
    return D_finite(d, support, range(length))


def A_local_product(d: int, support: Sequence[int], length: int) -> Fraction:
    d = _require_positive_int(d, "step d")
    length = _require_positive_int(length, "block length")
    primes = tuple(support)
    if len(set(primes)) != len(primes) or any(not is_prime(p) for p in primes):
        raise ValueError("support must contain distinct primes")
    output = Fraction(1)
    for prime in primes:
        output *= local_survival_factor(d, prime, length)
    return output


def R_finite(d: int, support: Sequence[int], length: int) -> Fraction:
    length = _require_positive_int(length, "run length")
    interior = tuple(range(length))
    return (
        D_finite(d, support, interior)
        - D_finite(d, support, (-1, *interior))
        - D_finite(d, support, (*interior, length))
        + D_finite(d, support, (-1, *interior, length))
    )


def R_second_difference(d: int, support: Sequence[int], length: int) -> Fraction:
    length = _require_positive_int(length, "run length")
    return (
        A_finite(d, support, length)
        - 2 * A_finite(d, support, length + 1)
        + A_finite(d, support, length + 2)
    )


def alternating_endpoint_finite(d: int, support: Sequence[int]) -> Fraction:
    d = _require_positive_int(d, "step d")
    cutoff = first_prime_not_dividing(d) ** 2
    return sum(
        (
            A_finite(d, support, length)
            if length % 2
            else -A_finite(d, support, length)
        )
        for length in range(1, cutoff)
    )


def run_endpoint_finite(d: int, support: Sequence[int]) -> Fraction:
    d = _require_positive_int(d, "step d")
    cutoff = first_prime_not_dividing(d) ** 2
    singleton = A_finite(d, support, 1)
    return singleton / 2 + sum(
        R_finite(d, support, length) / 2
        for length in range(1, cutoff, 2)
    )


def _phase_positive(residue: int, support: Sequence[int]) -> bool:
    if type(residue) is not int:
        raise TypeError("phase must be an exact integer")
    return all(residue % (prime * prime) for prime in support)


def forward_run_length(
    residue: int, d: int, support: Sequence[int], cutoff: int
) -> int:
    if type(residue) is not int:
        raise TypeError("phase must be an exact integer")
    d = _require_positive_int(d, "step d")
    cutoff = _require_positive_int(cutoff, "run cutoff")
    length = 0
    while length < cutoff and _phase_positive(residue + d * length, support):
        length += 1
    return length


def odd_forward_run_probability(d: int, support: Sequence[int]) -> Fraction:
    d = _require_positive_int(d, "step d")
    primes = tuple(support)
    if len(set(primes)) != len(primes) or any(not is_prime(p) for p in primes):
        raise ValueError("support must contain distinct primes")
    p0 = first_prime_not_dividing(d)
    if p0 not in primes:
        raise ValueError("support must contain the reset prime p0")
    modulus = math.prod(prime * prime for prime in primes)
    odd = sum(
        forward_run_length(residue, d, primes, p0 * p0) % 2
        for residue in range(modulus)
    )
    return Fraction(odd, modulus)


def path_mwis(length: int) -> int:
    length = _require_nonnegative_int(length, "path length")
    return (length + 1) // 2


def path_mwis_after_residue_deletion(length: int, period: int, residue: int) -> int:
    length = _require_positive_int(length, "path length")
    period = _require_positive_int(period, "deletion period")
    if type(residue) is not int or not 0 <= residue < period:
        raise ValueError("residue must lie in the exact period")
    total = 0
    component = 0
    for index in range(1, length + 1):
        if index % period == residue:
            total += path_mwis(component)
            component = 0
        else:
            component += 1
    return total + path_mwis(component)


def deletion_loss(length: int, period: int) -> int:
    length = _require_positive_int(length, "path length")
    period = _require_positive_int(period, "deletion period")
    return period * path_mwis(length) - sum(
        path_mwis_after_residue_deletion(length, period, residue)
        for residue in range(period)
    )


def deletion_loss_formula(length: int, period: int) -> int:
    length = _require_positive_int(length, "path length")
    period = _require_positive_int(period, "deletion period")
    alpha = path_mwis(length)
    if period % 2:
        if length % 2:
            return alpha
        return max(0, length // 2 - (period - 1) // 2)
    if length % 2:
        return min(alpha, period // 2)
    return 0


def local_contribution(length: int, prime: int, level: int) -> Fraction:
    length = _require_positive_int(length, "path length")
    if not is_prime(prime):
        raise ValueError("local contribution requires a prime")
    if type(level) is not int or level not in (0, 1, 2):
        raise ValueError("local level must be one of 0,1,2")
    period = (prime * prime, prime, 1)[level]
    alpha = path_mwis(length)
    return Fraction(alpha) - Fraction(
        deletion_loss_formula(length, period), prime * prime
    )


def local_contribution_levels(length: int, prime: int) -> tuple[Fraction, Fraction, Fraction]:
    return tuple(local_contribution(length, prime, level) for level in (0, 1, 2))  # type: ignore[return-value]


def canonical_local_level(prime: int) -> int:
    if not is_prime(prime):
        raise ValueError("canonical level requires a prime")
    return 1 if prime == 2 else 0


def maximizer_lag(h: int) -> bool:
    h = _require_positive_int(h, "lag h")
    return squarefree(h) and math.gcd(h, MAXIMIZER_SMALL_PRIME_PRODUCT) == 1


def strict_witness(h: int) -> dict[str, object] | None:
    h = _require_positive_int(h, "lag h")
    d = 2 * h
    if d % 4 == 0:
        return {"kind": "square_local_level", "prime": 2, "length": 2}
    for prime, exponent in factorization(h):
        if exponent >= 2:
            return {"kind": "square_local_level", "prime": prime, "length": 2}
    for prime, length in ((3, 4), (5, 6), (7, 8)):
        if h % prime == 0:
            return {"kind": "small_single_local_level", "prime": prime, "length": length}
    return None


def maximizer_scan(limit: int) -> dict[str, object]:
    limit = _require_positive_int(limit, "lag scan limit")
    failures: list[dict[str, object]] = []
    maximizers = 0
    nonmaximizers = 0
    for h in range(1, limit + 1):
        expected = maximizer_lag(h)
        witness = strict_witness(h)
        observed = witness is None
        if expected:
            maximizers += 1
        else:
            nonmaximizers += 1
        if observed != expected:
            failures.append({"h": h, "expected": expected, "witness": witness})
    return {
        "h_min": 1,
        "h_max": limit,
        "cases": limit,
        "maximizers": maximizers,
        "nonmaximizers": nonmaximizers,
        "failures": failures,
        "pass": failures == [],
    }


def deletion_formula_grid(max_period: int = 31, max_length: int = 127) -> dict[str, object]:
    max_period = _require_positive_int(max_period, "maximum period")
    max_length = _require_positive_int(max_length, "maximum path length")
    failures: list[dict[str, int]] = []
    branch_counts = {"odd_T_odd_L": 0, "odd_T_even_L": 0, "even_T_odd_L": 0, "even_T_even_L": 0}
    for period in range(1, max_period + 1):
        for length in range(1, max_length + 1):
            key = (
                ("odd_T_" if period % 2 else "even_T_")
                + ("odd_L" if length % 2 else "even_L")
            )
            branch_counts[key] += 1
            actual = deletion_loss(length, period)
            formula = deletion_loss_formula(length, period)
            if actual != formula:
                failures.append(
                    {"period": period, "length": length, "actual": actual, "formula": formula}
                )
    return {
        "period_min": 1,
        "period_max": max_period,
        "length_min": 1,
        "length_max": max_length,
        "cases": max_period * max_length,
        "branch_counts": branch_counts,
        "failures": failures,
        "pass": failures == [],
    }


def local_order_grid(prime_limit: int = 31, max_length: int = 127) -> dict[str, object]:
    prime_limit = _require_positive_int(prime_limit, "prime limit")
    max_length = _require_positive_int(max_length, "maximum path length")
    primes = primes_through(prime_limit)
    failures: list[dict[str, object]] = []
    strict_02 = 0
    strict_01 = 0
    strict_12 = 0
    for prime in primes:
        for length in range(1, max_length + 1):
            level0, level1, level2 = local_contribution_levels(length, prime)
            ordered = level1 >= level2 if prime == 2 else level0 >= level1 >= level2
            if not ordered:
                failures.append(
                    {
                        "prime": prime,
                        "length": length,
                        "levels": [fraction_text(level0), fraction_text(level1), fraction_text(level2)],
                    }
                )
            strict_02 += int(level0 > level2)
            strict_01 += int(level0 > level1)
            strict_12 += int(level1 > level2)
    return {
        "prime_min": 2,
        "prime_max": prime_limit,
        "primes": list(primes),
        "length_min": 1,
        "length_max": max_length,
        "cases": len(primes) * max_length,
        "strict_level0_over_level1": strict_01,
        "strict_level0_over_level2": strict_02,
        "strict_level1_over_level2": strict_12,
        "prime_two_allowed_levels": [1, 2],
        "failures": failures,
        "pass": failures == [],
    }


def invisible_prime_grid(prime_limit: int = 97) -> dict[str, object]:
    prime_limit = _require_positive_int(prime_limit, "prime limit")
    primes = tuple(prime for prime in primes_through(prime_limit) if prime >= 11)
    failures: list[dict[str, object]] = []
    for prime in primes:
        for length in range(1, 9):
            level0, level1, _level2 = local_contribution_levels(length, prime)
            if level0 != level1:
                failures.append(
                    {
                        "prime": prime,
                        "length": length,
                        "level0": fraction_text(level0),
                        "level1": fraction_text(level1),
                    }
                )
    return {
        "prime_min": 11,
        "prime_max": prime_limit,
        "length_min": 1,
        "length_max": 8,
        "cases": len(primes) * 8,
        "failures": failures,
        "pass": failures == [],
    }


def finite_product_identity_grid() -> dict[str, object]:
    fixtures = (
        (2, (2, 3), 8),
        (6, (2, 3, 5), 12),
        (10, (2, 3, 5), 12),
        (14, (2, 3, 5), 12),
        (22, (2, 3, 5, 11), 12),
        (242, (2, 3, 5, 11), 12),
    )
    failures: list[dict[str, object]] = []
    cases = 0
    for d, support, max_length in fixtures:
        for length in range(1, max_length + 1):
            cases += 1
            direct = A_finite(d, support, length)
            local = A_local_product(d, support, length)
            if direct != local:
                failures.append(
                    {
                        "d": d,
                        "support": list(support),
                        "length": length,
                        "direct": fraction_text(direct),
                        "local": fraction_text(local),
                    }
                )
    return {
        "fixtures": [
            {"d": d, "support": list(support), "length_max": max_length}
            for d, support, max_length in fixtures
        ],
        "cases": cases,
        "failures": failures,
        "pass": failures == [],
    }


def telescope_fixture(d: int, support: Sequence[int]) -> dict[str, object]:
    d = _require_positive_int(d, "step d")
    p0 = first_prime_not_dividing(d)
    if p0 not in support:
        raise ValueError("telescope support must contain p0")
    cutoff = p0 * p0
    a_cutoff = A_finite(d, support, cutoff)
    r_failures = [
        length
        for length in range(1, cutoff)
        if R_finite(d, support, length) != R_second_difference(d, support, length)
    ]
    alternating = alternating_endpoint_finite(d, support)
    run_endpoint = run_endpoint_finite(d, support)
    probability = odd_forward_run_probability(d, support)
    return {
        "d": d,
        "support": list(support),
        "p0": p0,
        "cutoff": cutoff,
        "A_cutoff": fraction_text(a_cutoff),
        "R_second_difference_failures": r_failures,
        "alternating": fraction_text(alternating),
        "run_endpoint": fraction_text(run_endpoint),
        "odd_forward_run_probability": fraction_text(probability),
        "pass": a_cutoff == 0 and r_failures == [] and alternating == run_endpoint == probability,
    }


def prime_square_sequence(prime_limit: int = 97) -> list[dict[str, object]]:
    prime_limit = _require_positive_int(prime_limit, "prime limit")
    rows: list[dict[str, object]] = []
    for prime in primes_through(prime_limit):
        if prime < 11:
            continue
        h = prime * prime
        rows.append(
            {
                "prime": prime,
                "h": h,
                "fixed_lag": True,
                "maximizer": maximizer_lag(h),
                "gap_upper": fraction_text(Fraction(1, prime * prime)),
            }
        )
    return rows


def _row(
    group: str, identifier: str, data: dict[str, object], passed: bool
) -> dict[str, object]:
    if type(passed) is not bool:
        raise TypeError("row pass flag must be an exact bool")
    return {"group": group, "id": identifier, "data": data, "pass": passed}


BUILDER_NAMES = ("build_certificate", "_new_rows")
SEMANTIC_HELPER_NAMES = (
    "factorization", "is_prime", "primes_through", "valuation", "squarefree",
    "mobius_squared", "first_prime_not_dividing", "local_level",
    "local_orbit_length", "local_survival_factor", "residue_count", "D_finite",
    "A_finite", "A_local_product", "R_finite", "R_second_difference",
    "alternating_endpoint_finite", "run_endpoint_finite", "forward_run_length",
    "odd_forward_run_probability", "path_mwis",
    "path_mwis_after_residue_deletion", "deletion_loss",
    "deletion_loss_formula", "local_contribution", "local_contribution_levels",
    "canonical_local_level", "maximizer_lag", "strict_witness",
    "maximizer_scan", "deletion_formula_grid", "local_order_grid",
    "invisible_prime_grid", "finite_product_identity_grid", "telescope_fixture",
    "prime_square_sequence", "canonical_json_bytes", "exact_equal",
)


def _loss_fixture(length: int, period: int) -> dict[str, object]:
    actual = deletion_loss(length, period)
    formula = deletion_loss_formula(length, period)
    return {
        "period": period,
        "length": length,
        "enumerated": actual,
        "formula_value": formula,
        "equal": actual == formula,
    }


def _local_fixture(prime: int, length: int) -> dict[str, object]:
    levels = local_contribution_levels(length, prime)
    return {
        "prime": prime,
        "length": length,
        "levels": [fraction_text(value) for value in levels],
        "gap_e0_e1": fraction_text(levels[0] - levels[1]),
        "gap_e1_e2": fraction_text(levels[1] - levels[2]),
        "gap_e0_e2": fraction_text(levels[0] - levels[2]),
    }


def _new_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(group: str, identifier: str, data: dict[str, object], passed: bool) -> None:
        rows.append(_row(group, identifier, data, passed))

    loss_grid = deletion_formula_grid()
    group = "loss_formula"
    odd_odd = _loss_fixture(7, 5)
    add(group, "LF01_oddT_oddL", {
        "alpha_formula": "a(L)=(L+1)//2", "enumerator": "Lambda_T(L)=T*a(L)-sum_(0<=r<T)alpha(P_L minus indices congruent r mod T)",
        "formula": "Lambda_T(L)=a(L)", "fixture": odd_odd,
    }, odd_odd["equal"] is True and odd_odd["formula_value"] == path_mwis(7))
    odd_even = _loss_fixture(10, 5)
    add(group, "LF02_oddT_evenL", {
        "alpha_formula": "a(L)=(L+1)//2", "formula": "Lambda_T(L)=max(0,L/2-(T-1)/2)",
        "fixture": odd_even,
    }, odd_even["equal"] is True and odd_even["formula_value"] == 3)
    even_odd = _loss_fixture(7, 4)
    add(group, "LF03_evenT_oddL", {
        "alpha_formula": "a(L)=(L+1)//2", "formula": "Lambda_T(L)=min(a(L),T/2)",
        "fixture": even_odd,
    }, even_odd["equal"] is True and even_odd["formula_value"] == 2)
    even_even = _loss_fixture(8, 4)
    add(group, "LF04_evenT_evenL", {
        "alpha_formula": "a(L)=(L+1)//2", "formula": "Lambda_T(L)=0", "fixture": even_even,
    }, even_even["equal"] is True and even_even["formula_value"] == 0)
    t1 = [_loss_fixture(length, 1) for length in range(1, 9)]
    add(group, "LF05_T1_edge", {"period": 1, "fixtures": t1}, all(row["equal"] for row in t1))
    t2 = [_loss_fixture(length, 2) for length in range(1, 9)]
    add(group, "LF06_T2_edge", {"period": 2, "fixtures": t2}, all(row["equal"] for row in t2))
    l1 = [_loss_fixture(1, period) for period in range(1, 9)]
    add(group, "LF07_L1_edge", {"length": 1, "fixtures": l1}, all(row["equal"] for row in l1))
    l2 = [_loss_fixture(2, period) for period in range(1, 9)]
    add(group, "LF08_L2_edge", {"length": 2, "fixtures": l2}, all(row["equal"] for row in l2))
    preperiod = [_loss_fixture(period - 1, period) for period in range(2, 10)]
    add(group, "LF09_preperiod_L_lt_T", {"condition": "L<T", "fixtures": preperiod}, all(row["equal"] for row in preperiod))
    threshold = [_loss_fixture(period, period) for period in range(1, 10)]
    add(group, "LF10_threshold_L_eq_T", {"condition": "L=T", "fixtures": threshold}, all(row["equal"] for row in threshold))
    postperiod = [_loss_fixture(period + 1, period) for period in range(1, 10)]
    add(group, "LF11_postthreshold_L_gt_T", {"condition": "L>T", "fixtures": postperiod}, all(row["equal"] for row in postperiod))
    add(group, "LF12_enumerator_grid", {
        "residue_range": "0<=r<T", "period_range": [1, 31], "length_range": [1, 127],
        "cases": loss_grid["cases"], "branch_counts": loss_grid["branch_counts"], "failures": loss_grid["failures"],
    }, loss_grid["pass"] is True and loss_grid["cases"] == 3937)

    order_grid = local_order_grid()
    group = "local_order"
    exponent_rows = [
        {"prime": prime, "exponent": exponent, "t": local_orbit_length(prime ** exponent, prime)}
        for prime in (2, 3, 5) for exponent in (0, 1, 2)
    ]
    add(group, "LO01_t_exponent_map", {
        "exponent_map": "t_p=p^(2-min(v_p(d),2))", "values": ["p^2", "p", "1"], "fixtures": exponent_rows,
    }, all(row["t"] == row["prime"] ** (2 - row["exponent"]) for row in exponent_rows))
    add(group, "LO02_oddprime_e0_ge_e1", {
        "formula": "V_(p,e)=a-Lambda_(p^(2-e))/p^2", "order": "V_(p,0)>=V_(p,1)",
        "grid_cases": order_grid["cases"], "failures": order_grid["failures"],
    }, order_grid["pass"] is True)
    add(group, "LO03_oddprime_e1_ge_e2", {
        "level2_formula": "V_(p,2)=a(L)*(1-p^-2)", "order": "V_(p,1)>=V_(p,2)",
        "denominator_for_e1": "p^2", "grid_cases": order_grid["cases"],
    }, order_grid["pass"] is True)
    odd_equal = []
    for prime in (3, 5, 7, 11):
        for length in range(1, 16, 2):
            levels = local_contribution_levels(length, prime)
            odd_equal.append({
                "prime": prime,
                "length": length,
                "equal": levels[0] == levels[1] == levels[2],
            })
    add(group, "LO04_oddL_threeway_equal", {
        "odd_L_equal_only": True,
        "meaning": "V_(p,0)=V_(p,1)=V_(p,2) for odd path lengths",
        "fixtures": odd_equal,
    }, all(row["equal"] for row in odd_equal))
    below = []
    for prime in (3, 5, 7, 11):
        for length in range(2, prime, 2):
            levels = local_contribution_levels(length, prime)
            below.append({"prime": prime, "length": length, "equal": levels[0] == levels[1]})
    add(group, "LO05_evenL_e0_eq_e1_below_p", {"condition": "even L<p", "fixtures": below}, all(row["equal"] for row in below))
    first_strict = [_local_fixture(prime, prime + 1) for prime in (3, 5, 7, 11)]
    add(group, "LO06_first_e0e1_strict", {"first_even_length": "L=p+1", "fixtures": first_strict}, all(Fraction(row["gap_e0_e1"]) > 0 for row in first_strict))
    e12 = [_local_fixture(prime, 2) for prime in (3, 5, 7, 11)]
    add(group, "LO07_evenL_e1e2_strict", {"condition": "even L", "fixtures": e12}, all(Fraction(row["gap_e1_e2"]) > 0 for row in e12))
    p2 = _local_fixture(2, 2)
    add(group, "LO08_two_prime_allowed_order", {
        "allowed_levels_for_d_equals_2h": [1, 2], "counterfactual_level0_not_used": True, "fixture": p2,
    }, Fraction(p2["gap_e1_e2"]) > 0)
    add(group, "LO09_p2_L2_strict", {"prime": 2, "length": 2, "allowed_transfer": "e1_to_e2", "gap": p2["gap_e1_e2"]}, p2["gap_e1_e2"] == "1/4")
    for identifier, prime, length, gap in (
        ("LO10_p3_L4_strict", 3, 4, "1/9"),
        ("LO11_p5_L6_strict", 5, 6, "1/25"),
        ("LO12_p7_L8_strict", 7, 8, "1/49"),
    ):
        fixture = _local_fixture(prime, length)
        add(group, identifier, {"prime": prime, "length": length, "gap_e0_e1": fixture["gap_e0_e1"], "fixture": fixture}, fixture["gap_e0_e1"] == gap)

    group = "telescope"
    product_grid = finite_product_identity_grid()
    add(group, "TS01_t_p_gcd_formula", {
        "formula": "t_p(d)=p^2/gcd(d,p^2)", "range": ["1", "p", "p^2"], "fixtures": exponent_rows,
    }, all(row["t"] in (1, row["prime"], row["prime"] ** 2) for row in exponent_rows))
    add(group, "TS02_A_product", {
        "formula": "A_m=prod_p(1-min(m,t_p)/p^2)", "finite_grid_cases": product_grid["cases"], "failures": product_grid["failures"],
    }, product_grid["pass"] is True)
    p0_rows = [{"d": d, "p0": first_prime_not_dividing(d)} for d in (2, 6, 10, 14, 30, 210)]
    add(group, "TS03_p0_definition", {"definition": "p0=min prime p with p not dividing d", "fixtures": p0_rows}, all(d["d"] % d["p0"] for d in p0_rows))
    telescopes = [
        telescope_fixture(2, (2, 3, 5, 7)),
        telescope_fixture(6, (2, 3, 5, 7)),
        telescope_fixture(10, (2, 3, 5, 7)),
        telescope_fixture(14, (2, 3, 5, 7)),
    ]
    add(group, "TS04_A_cutoff", {"zero_for_m_at_least_p0_squared": True, "fixtures": [{"d": row["d"], "cutoff": row["cutoff"], "A_cutoff": row["A_cutoff"]} for row in telescopes]}, all(row["A_cutoff"] == "0" for row in telescopes))
    add(group, "TS05_R_second_difference", {
        "formula": "R_l=A_l-2A_(l+1)+A_(l+2)", "right_index": "l+2", "fixtures": [{"d": row["d"], "failures": row["R_second_difference_failures"]} for row in telescopes],
    }, all(row["R_second_difference_failures"] == [] for row in telescopes))
    nonnegative = []
    for d in (2, 6, 10, 14):
        p0 = first_prime_not_dividing(d)
        for length in range(1, p0 * p0):
            value = R_finite(d, (2, 3, 5, 7), length)
            nonnegative.append({"d": d, "length": length, "value": fraction_text(value)})
    add(group, "TS06_R_nonnegative_event", {"event": "exact_bracketed_positive_run", "fixtures": nonnegative}, all(Fraction(row["value"]) >= 0 for row in nonnegative))
    add(group, "TS07_alternating_sum_start", {"first_index": 1, "first_sign": "+", "sign": "(-1)^(m+1)"}, True)
    add(group, "TS08_alternating_sum_terminal", {"last_index": "p0^2-1", "A_at_p0_squared": "0", "p0_is_odd": True}, all(row["p0"] % 2 == 1 for row in telescopes))
    add(group, "TS09_B_telescope_identity", {
        "formula": "B=sum_(m=1)^(p0^2-1)(-1)^(m+1)A_m", "fixtures": [{"d": row["d"], "alternating": row["alternating"], "run_endpoint": row["run_endpoint"]} for row in telescopes],
    }, all(row["alternating"] == row["run_endpoint"] for row in telescopes))
    add(group, "TS10_odd_forward_run_event", {
        "event": "forward_positive_run_length_is_odd", "phase_space": "finite_CRT_square_divisibility_phase_space_not_random_Mobius", "fixtures": [{"d": row["d"], "endpoint": row["alternating"], "probability": row["odd_forward_run_probability"]} for row in telescopes],
    }, all(row["alternating"] == row["odd_forward_run_probability"] for row in telescopes))
    add(group, "TS11_finite_CRT_oracle", {
        "prime_support": [2, 3, 5, 7], "residue_enumeration": "exact_mod_product_p_squared", "fixtures": telescopes,
    }, all(row["pass"] is True for row in telescopes))
    collision_rows = [
        {"d": d, "prime": prime, "level": local_level(d, prime), "orbit": local_orbit_length(d, prime)}
        for d in (2, 4, 6, 18, 50, 98) for prime in (2, 3, 5, 7)
    ]
    add(group, "TS12_collision_exponent_oracle", {"deduplicate_mod_p2": True, "fixtures": collision_rows}, all(row["orbit"] == row["prime"] ** (2 - row["level"]) for row in collision_rows))

    group = "strictness"
    p2_fixture = _local_fixture(2, 2)
    add(group, "ST01_square_p2", {
        "condition": "2 divides h equivalently 4 divides d", "not_called_square_factor_of_h": True, "prime": 2, "length": 2, "strict": True, "gap": p2_fixture["gap_e1_e2"],
    }, p2_fixture["gap_e1_e2"] == "1/4")
    for identifier, prime in (("ST02_square_p3", 3), ("ST03_square_p5", 5)):
        fixture = _local_fixture(prime, 2)
        add(group, identifier, {"condition": f"{prime}^2 divides h", "prime": prime, "length": 2, "strict": True, "gap_e0_e2": fixture["gap_e0_e2"]}, Fraction(fixture["gap_e0_e2"]) > 0)
    square_generic = []
    for prime in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        fixture = _local_fixture(prime, 2)
        square_generic.append({"prime": prime, "length": 2, "gap": fixture["gap_e0_e2"], "strict": Fraction(fixture["gap_e0_e2"]) > 0})
    add(group, "ST04_square_generic", {"odd_square_divisor": True, "fixtures": square_generic}, all(row["strict"] for row in square_generic))
    for identifier, prime, length, gap in (
        ("ST05_single_p3", 3, 4, "1/9"),
        ("ST06_single_p5", 5, 6, "1/25"),
        ("ST07_single_p7", 7, 8, "1/49"),
    ):
        fixture = _local_fixture(prime, length)
        add(group, identifier, {"condition": f"{prime} exactly divides d", "prime": prime, "length": length, "strict": True, "gap_e0_e1": fixture["gap_e0_e1"]}, fixture["gap_e0_e1"] == gap)
    boundary_fixtures = {2: p2_fixture, 4: _local_fixture(3, 4), 6: _local_fixture(5, 6), 8: _local_fixture(7, 8)}
    for identifier, length in (("ST08_boundary_CRT_L2", 2), ("ST09_boundary_CRT_L4", 4), ("ST10_boundary_CRT_L6", 6), ("ST11_boundary_CRT_L8", 8)):
        gap_key = "gap_e1_e2" if length == 2 else "gap_e0_e1"
        add(group, identifier, {
            "length": length, "finite_square_support_first": True, "positive_density_exact_run_cylinder": True,
            "cofinal_union_tail_after_finite_transfer": True,
            "relevant_gap": gap_key,
            "fixture": boundary_fixtures[length],
        }, Fraction(boundary_fixtures[length][gap_key]) > 0)
    scan = maximizer_scan(1000)
    add(group, "ST12_nonmax_partition", {
        "criterion": "mu^2(h)=1 and gcd(h,210)=1", "branches": ["2 divides h", "odd p^2 divides h", "after squarefree reduction one of 3,5,7 divides h"],
        "grid": scan,
    }, scan["pass"] is True)

    group = "maximizers"
    add(group, "MX01_base_h1", {"h": 1, "d": 2, "p0": 3, "cutoff_last_index": 8, "maximizer": maximizer_lag(1)}, maximizer_lag(1))
    invisible = invisible_prime_grid()
    add(group, "MX02_largeprime_invisibility", {
        "prime_at_least": 11, "length_range": [1, 8], "identity": "Lambda_p(L)=Lambda_(p^2)(L)", "cases": invisible["cases"], "failures": invisible["failures"],
    }, invisible["pass"] is True)
    multiprime = []
    for h in (11, 13, 143, 187, 11 * 13 * 17):
        factors = factorization(h)
        multiprime.append({"h": h, "factors": [[p, e] for p, e in factors], "all_invisible": all(p >= 11 and e == 1 for p, e in factors), "maximizer": maximizer_lag(h)})
    add(group, "MX03_multiprime_invisibility", {"fixtures": multiprime}, all(row["all_invisible"] and row["maximizer"] for row in multiprime))
    true_examples = [1, 11, 13, 143, 187]
    add(group, "MX04_true_examples", {"examples": true_examples, "values": [maximizer_lag(h) for h in true_examples]}, all(maximizer_lag(h) for h in true_examples))
    false_small = [2, 3, 5, 7]
    add(group, "MX05_false_smallprime_examples", {"examples": false_small, "values": [maximizer_lag(h) for h in false_small]}, all(not maximizer_lag(h) for h in false_small))
    false_square = [25, 49, 121, 169]
    add(group, "MX06_false_square_examples", {"examples": false_square, "values": [maximizer_lag(h) for h in false_square]}, all(not maximizer_lag(h) for h in false_square))
    add(group, "MX07_exhaustive_predicate_grid", {"h_range": [1, 1000], "grid": scan}, scan["pass"] is True and scan["cases"] == 1000)
    add(group, "MX08_exact_iff", {
        "literal": "mu^2(h)=1 and gcd(h,210)=1", "logical_connector": "and", "small_prime_product": 210,
        "equivalence": "B_infinity(h)=B_infinity(1) iff criterion", "maximizers_infinite": True,
    }, MAXIMIZER_SMALL_PRIME_PRODUCT == 2 * 3 * 5 * 7)

    group = "complement_gap"
    sequence = prime_square_sequence()
    add(group, "CG01_square_sequence", {"sequence": "h=p^2 for prime p>=11", "rows": sequence}, all(row["h"] == row["prime"] ** 2 for row in sequence))
    sequence_local = []
    for row in sequence:
        prime = int(row["prime"])
        odd_gaps = []
        even_scaled_gaps = []
        for length in range(1, 9):
            level0, _level1, level2 = local_contribution_levels(length, prime)
            gap = level0 - level2
            if length % 2:
                odd_gaps.append(fraction_text(gap))
            else:
                even_scaled_gaps.append(
                    fraction_text(gap * prime * prime)
                )
        sequence_local.append({
            "prime": prime,
            "odd_gaps": odd_gaps,
            "even_scaled_gaps": even_scaled_gaps,
            "L2_gap": fraction_text(
                local_contribution(2, prime, 0)
                - local_contribution(2, prime, 2)
            ),
        })
    strict_local = all(
        local["odd_gaps"] == ["0", "0", "0", "0"]
        and Fraction(local["L2_gap"]) > 0
        for local in sequence_local
    )
    add(group, "CG02_sequence_strict", {
        "strict_lower": "0<B1-B_(p^2)",
        "L2_exact_run_cylinder_positive": True,
        "local_facts": sequence_local,
    }, strict_local)
    upper_local = all(
        local["even_scaled_gaps"] == [str(value) for value in (1, 2, 3, 4)]
        for local in sequence_local
    )
    add(group, "CG03_sequence_upper_bound", {
        "upper": "B1-B_(p^2)<=1/p^2",
        "local_facts": sequence_local,
        "run_density_weight_bound": "sum_(even L<=8)rho_L*a(L)<=1",
        "rows": sequence,
    }, upper_local and all(
        row["gap_upper"] == fraction_text(Fraction(1, row["prime"] ** 2))
        for row in sequence
    ))
    add(group, "CG04_sequence_limit", {"fixed_lags_one_at_a_time": True, "prime_tends_to_infinity": True, "upper_bound_tends_to_zero": True, "no_varying_h_terminal_limit": True}, True)
    add(group, "CG05_complement_sup", {"domain": "positive_lags_not_in_maximizer_set", "extremum": "supremum", "value": "B_infinity(1)"}, True)
    add(group, "CG06_complement_unattained", {"attained": False, "reason": "exact equality iff maximizer criterion"}, True)
    add(group, "CG07_p0_ge5_reduction", {"condition": "p0(h)>=5", "three_divides_d": True, "comparison": "B_h<=B_3"}, True)
    cylinder_factors = ["1/2", "1/25", "1/49", "tail>3/5", "local_loss=1/9"]
    add(group, "CG08_uniform_gap_chain", {
        "factors": cylinder_factors, "tail_lower": "3/5", "cylinder_density_lower": "3/12250", "local_loss": "1/9",
        "strong_gap": fraction_text(CYLINDER_GAP), "theorem_gap": fraction_text(THEOREM_GAP),
        "chain": "B1-Bh>=B1-B3>1/36750>2/1334025",
    }, CYLINDER_GAP == Fraction(1, 2 * 25 * 49) * Fraction(3, 5) * Fraction(1, 9) and CYLINDER_GAP > THEOREM_GAP)

    group = "joint_endpoint"
    add(group, "JE01_fixed_pair_strict", {"statement": "C_h(q)<B_infinity(h)<=B_infinity(1)", "finite_pair_strict": True, "h_fixed": True, "q_finite": True}, True)
    add(group, "JE02_h1_cofinal_lower", {"statement": "sup_(q finite)C_1(q)=B_infinity(1)", "finite_q_attains": False, "source": "RH396_Theorem_1_3_equation_22"}, True)
    add(group, "JE03_joint_supremum", {"extremum": "supremum", "domain": "h>=1 and q finite", "value": "B_infinity(1)"}, True)
    add(group, "JE04_joint_nonattainment", {"no_finite_pair_attains": True, "retained_infimum": "inf_h B_infinity(h)=3/pi^2", "infimum_attained": False}, True)

    group = "firewalls"
    add(group, "FW01_quantifier_order", {
        "order": ["fix h,q,F,omega", "X_to_infinity", "finite_safe_maximum", "scalar_supremum_over_finite_q", "scalar_supremum_over_fixed_h"],
        "prelimit_maximum": False,
    }, True)
    data_scope = {key: False for key in ("growing_h", "growing_q", "growing_table", "moving_order", "uniform_rate")}
    add(group, "FW02_data_scope", {**data_scope, "fixed_scalar_endpoint_comparison_only": True}, all(value is False for value in data_scope.values()))
    add(group, "FW03_source_roles", {
        "RH396": "sole_load_bearing_theorem_and_analytic_endpoint_input_equations_18_21_Theorem_1_3_equation_22_Corollary_1_4_equation_23",
        "RH397": "direct_release_and_provenance_predecessor_only", "RH397_analytic_input": False,
        "new_remote_source": False,
    }, True)
    ceiling = {key: False for key in ("ordinary_Cesaro", "causal_online", "four_shift", "generic_graph", "monotonicity_in_h", "operator", "trace", "zeros", "RH_or_Gates_A_E")}
    add(group, "FW04_claim_ceiling", {**ceiling, "finite_certificate_replaces_analytic_proof": False}, all(value is False for value in ceiling.values()))
    return rows


def build_certificate() -> dict[str, object]:
    rows = _new_rows()
    frozen_ids = {group: list(ids) for group, ids in GROUP_IDS.items()}
    actual_ids = {
        group: [row["id"] for row in rows if row["group"] == group]
        for group in GROUP_IDS
    }
    counts = {group: len(actual_ids[group]) for group in GROUP_IDS}
    return {
        "schema_version": 1,
        "status": "RH-398_exact_lag_endpoint_extrema_core_certified",
        "title": TITLE,
        "package": PACKAGE,
        "epistemic_role": "finite_exact_reproduction_not_analytic_proof",
        "formal_oracle": "integers_and_Fractions_only",
        "theorem_contract": {
            "global_maximum": "B_infinity(h)<=B_infinity(1)",
            "exact_maximizers": "mu^2(h)=1 and gcd(h,210)=1",
            "complement_supremum": "B_infinity(1)_unattained",
            "joint_supremum": "sup_(h>=1,q_finite)C_h(q)=B_infinity(1)_unattained",
            "uniform_p0_ge5_gap": "B_infinity(1)-B_infinity(h)>2/1334025",
        },
        "row_partition": dict(ROW_PARTITION),
        "row_ids": frozen_ids,
        "row_count": len(rows),
        "rows": rows,
        "mutation_names": list(MUTATION_NAMES),
        "all_pass": (
            len(rows) == 72
            and counts == ROW_PARTITION
            and actual_ids == frozen_ids
            and len({row["id"] for row in rows}) == 72
            and all(row["pass"] is True for row in rows)
        ),
    }


def certificate_bytes() -> bytes:
    return canonical_json_bytes(build_certificate())


def _same_exact(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return tuple(left) == tuple(right) and all(
            _same_exact(left[key], right[key]) for key in left
        )
    if type(left) is list:
        return len(left) == len(right) and all(
            _same_exact(a, b) for a, b in zip(left, right)
        )
    return left == right


def _make_public_verifier():
    """Capture an exact builder-free false path and return the public gate."""

    from copy import deepcopy as local_deepcopy
    from hashlib import sha256 as local_sha256
    from json import dumps as local_dumps

    expected = local_deepcopy(build_certificate())
    expected_bytes = local_dumps(
        expected,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    expected_sha = local_sha256(expected_bytes).hexdigest()
    expected_length = len(expected_bytes)
    sealed_length = 36_635
    sealed_sha = "d47de091a8fe5a134ba4bbf8ac4689f53b54786d45dc3bfc7061c99b46bea741"

    def same(left: object, right: object) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return tuple(left) == tuple(right) and all(
                same(left[key], right[key]) for key in left
            )
        if type(left) is list:
            return len(left) == len(right) and all(
                same(a, b) for a, b in zip(left, right)
            )
        return left == right

    def encoded(value: object) -> bytes:
        return local_dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def false_path(value: object) -> bool:
        try:
            if type(value) is not dict or not same(value, expected):
                return False
            payload = encoded(value)
            return (
                len(payload) == expected_length == sealed_length
                and local_sha256(payload).hexdigest() == expected_sha
                == sealed_sha
                and value["all_pass"] is True
            )
        except (KeyError, TypeError, ValueError):
            return False

    def public(value: object, *, compare_fresh: bool = False) -> bool:
        if type(compare_fresh) is not bool:
            raise TypeError("compare_fresh must be an exact bool")
        if not false_path(value):
            return False
        return not compare_fresh or same(value, build_certificate())

    return public


def mutate_certificate(value: dict[str, object], name: str) -> dict[str, object]:
    if type(value) is not dict or type(name) is not str or name not in MUTATION_NAMES:
        raise ValueError("unknown semantic mutation")
    mutated = deepcopy(value)
    target_map = dict(MUTATION_TARGETS)
    if tuple(target_map) != MUTATION_NAMES or set(_MUTATION_EDITS) != set(MUTATION_NAMES):
        raise ValueError("semantic mutation contract is incomplete")
    target = target_map[name]
    rows = [row for row in mutated["rows"] if row["id"] == target]
    if len(rows) != 1 or type(rows[0].get("data")) is not dict:
        raise ValueError("semantic mutation target is not unique")
    path, expected, replacement = _MUTATION_EDITS[name]
    parent: object = rows[0]["data"]
    for key in path[:-1]:
        if type(key) is str and type(parent) is dict and key in parent:
            parent = parent[key]
        elif type(key) is int and type(parent) is list and 0 <= key < len(parent):
            parent = parent[key]
        else:
            raise ValueError("semantic mutation path is invalid")
    leaf = path[-1]
    if type(leaf) is str and type(parent) is dict and leaf in parent:
        actual = parent[leaf]
        if not _same_exact(actual, expected):
            raise ValueError(f"semantic mutation old leaf drifted: {name}")
        parent[leaf] = deepcopy(replacement)
    elif type(leaf) is int and type(parent) is list and 0 <= leaf < len(parent):
        actual = parent[leaf]
        if not _same_exact(actual, expected):
            raise ValueError(f"semantic mutation old leaf drifted: {name}")
        parent[leaf] = deepcopy(replacement)
    else:
        raise ValueError("semantic mutation leaf is invalid")
    return mutated


verify_certificate = _make_public_verifier()


__all__ = (
    "TITLE", "PACKAGE", "MAXIMIZER_SMALL_PRIME_PRODUCT", "THEOREM_GAP",
    "CYLINDER_GAP", "GROUP_IDS", "ROW_PARTITION", "CERTIFICATE_FIXTURE_ROWS",
    "CERTIFICATE_FIXTURE_BYTES", "CERTIFICATE_FIXTURE_SHA256", "MUTATION_NAMES",
    "MUTATION_TARGETS", "BUILDER_NAMES", "SEMANTIC_HELPER_NAMES", "loads_strict",
    "canonical_json_bytes", "exact_equal", "fraction_text", "factorization",
    "is_prime", "primes_through", "valuation", "squarefree", "mobius_squared",
    "first_prime_not_dividing", "local_level", "local_orbit_length",
    "local_survival_factor", "residue_count", "D_finite", "A_finite",
    "A_local_product", "R_finite", "R_second_difference",
    "alternating_endpoint_finite", "run_endpoint_finite", "forward_run_length",
    "odd_forward_run_probability", "path_mwis", "path_mwis_after_residue_deletion",
    "deletion_loss", "deletion_loss_formula", "local_contribution",
    "local_contribution_levels", "canonical_local_level", "maximizer_lag",
    "strict_witness", "maximizer_scan", "deletion_formula_grid",
    "local_order_grid", "invisible_prime_grid", "finite_product_identity_grid",
    "telescope_fixture", "prime_square_sequence", "build_certificate",
    "certificate_bytes", "verify_certificate", "mutate_certificate",
)
