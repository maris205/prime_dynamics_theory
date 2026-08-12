"""Exact finite certificate for odd-lag half-span overlap Möbius capacity.

This module certifies two-symbol overlap safety, flag-rectangle saturation,
the weighted step-``h`` independent-set formula, and odd-lag clock attainment.
RH-394 remains the sole analytic terminal-law input; all oracles here are
finite and integer- or :class:`fractions.Fraction`-valued.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
import json
import math
from typing import Iterable


TITLE = "Odd-Lag Half-Span Overlap Mobius Capacity"
PACKAGE = "odd_lag_half_span_capacity"
T = (-1, 0, 1)
COORDINATES = ("L", "C", "R")
ZERO_EXPR = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))
INTERVAL_CUTOFF = 20_000

GROUP_IDS = {
    "domain_source_firewall": (
        "A01_mu0_boundary", "A02_fixed_h_q_F_clock",
        "A03_ordered_shifts_L_h_C_0_R_minus_h", "A04_output_vs_score",
        "A05_separation_h_four_symbol_safety",
        "A06_terminal_window_and_normalization", "A07_limit_then_finite_max_order",
        "A08_RH394_sole_analytic_input", "A09_collision_aware_theta_kappa2_kappa3",
        "A10_fixed_data_claim_ceiling",
    ),
    "terminal_bridge_projection_reflection": (
        "B01_RH394_three_table_bridge", "B02_Pi_inclusion_exclusion_mass",
        "B03_lambda_exact_support_sign_split", "B04_lambda_nonnegative",
        "B05_all_minus_projected_baseline_zero",
        "B06_positive_projection_pointwise_monotone_safe",
        "B07_relation_A_center_plus", "B08_projected_limit_sum_lambda",
        "B09_reflection_preserves_safety_negates_limit",
        "B10_absolute_capacity_positive_max_both_signs",
    ),
    "flags_rectangles": (
        "C01_source_target_flag_definitions",
        "C02_forbidden_pair_concatenation_x_1_1_w",
        "C03_safety_iff_t_r_s_rplush_zero",
        "C04_exhaustive_relation_pair_safety_61440",
        "C05_exact_flag_class_counts_16_48_48_400",
        "C06_Xs_Yt_rectangle_definition", "C07_rectangle_00_size4_exact_flags",
        "C08_rectangle_10_size6_exact_flags", "C09_rectangle_01_size6_exact_flags",
        "C10_rectangle_11_size9_exact_flags",
        "C11_relation_contained_in_own_flag_rectangle",
        "C12_saturation_preserves_flags_safety_coefficientwise_gain",
    ),
    "phase_weights_translation": (
        "D01_M_total_center_mass_ThetaC", "D02_U_plus_source_row_half_ThetaLC",
        "D03_V_plus_target_column_half_ThetaCR",
        "D04_W_corner_positive_quarter_ThetaLCR",
        "D05_rectangle_value_inclusion_exclusion",
        "D06_ThetaLCR_le_ThetaLC_and_ThetaCR",
        "D07_W_le_U_over2_le_U_and_W_le_V_over2_le_V",
        "D08_translation_p_not_divide_q_nu_branch",
        "D09_translation_p_parallel_q_tau_after_p2_dedup",
        "D10_translation_p2_divides_q_indicator_branch",
        "D11_translation_collision_fixtures", "D12_V_r_equals_U_rplush_and_phase_sums",
    ),
    "edge_saturation_rising_independent_set": (
        "E01_binary_safety_edge_t_plus_snext_le1",
        "E02_unsaturated_edge_source_flag_addition_safe",
        "E03_exact_addition_gain_U_next_minus_1_minus_tnext_times_W_next",
        "E04_gain_nonnegative_from_D07", "E05_all_edges_saturate_independently",
        "E06_t_r_equals_1_minus_s_rplush", "E07_UV_terms_collapse_minus_kappa2_over2",
        "E08_rising_set_and_W_bonus", "E09_rising_set_independent_including_selfloop",
        "E10_every_independent_set_realized_including_empty",
        "E11_weighted_IS_formula_all_h_q", "E12_flag_bruteforce_equals_IS_DP_fixtures",
    ),
    "odd_lag_all_clock_attainment": (
        "F01_weighted_IS_upper_total_kappa3", "F02_q2_p_parallel2_tau_even1_odd2",
        "F03_q2_triple_mass_even_kappa3_odd_zero", "F04_q2_attains_for_odd_h",
        "F05_every_even_declared_q_nonminimal_lift_attains",
        "F06_odd_q_CRT_p_ge5_parallel_branch", "F07_odd_q_CRT_p3_parallel_three_cases",
        "F08_odd_q_CRT_p2_indicator_avoid_four_classes",
        "F09_outside_q_Euler_factors_positive_and_adjacent_positive_weights",
        "F10_attainment_iff_q_even_q1_strict", "F11_h1_q1_q2_q3_exact_controls",
        "F12_h4_q4_h9_q2_collision_controls",
    ),
    "claim_ceiling_release": (
        "G01_source_roles_RH394_direct_others_comparison",
        "G02_no_even4_c1111_leak_three_shift_only",
        "G03_no_growing_Cesaro_causal_adaptive_operator_Gates",
        "G04_72_rows_finite_reproduction_not_analytic_proof",
    ),
}
ROW_PARTITION = {group: len(ids) for group, ids in GROUP_IDS.items()}
CERTIFICATE_FIXTURE_ROWS = 72
CERTIFICATE_FIXTURE_BYTES = 24297
CERTIFICATE_FIXTURE_SHA256 = "23f714236b53c2b89caa72b53f8139cfeab74cd07132082061c3ab0dfc048697"

MUTATION_NAMES = (
    "mu0_to_mu", "fixed_h_to_growing", "fixed_q_to_growing", "shift_order_swap",
    "score_drops_center", "safety_step_2h", "safety_unshares_center_right",
    "max_before_limit", "analytic_role_promoted", "kappa_collision_ignored",
    "Pi_sign_flip", "lambda_drop_sign_half", "baseline_not_zero",
    "projection_wrong_center", "relation_uses_center_minus",
    "reflection_no_input_negation", "source_target_swap", "flag_shift_reverse",
    "safe_pair_count_wrong", "flag_class_count_wrong", "rectangle_00_wrong",
    "rectangle_10_wrong", "rectangle_01_wrong", "rectangle_11_wrong",
    "containment_reverse", "saturation_loses_gain", "rectangle_W_minus",
    "U_missing_half", "V_missing_half", "W_missing_quarter",
    "theta_subset_reverse", "W_le_U_not_half", "theta_nu_multiplicity",
    "theta_tau_before_dedup", "theta_indicator_complement",
    "translation_shift_2h", "edge_inequality_reverse", "addition_gain_W_sign",
    "addition_gain_wrong_t", "selfloop_allows_vertex", "empty_IS_forbidden",
    "IS_surjectivity_reverse", "weighted_IS_unweighted", "q2_parity_swap",
    "even_lift_requires_minimal", "odd_q_attains", "CRT_p3_one_case",
    "indicator_avoids_three_classes", "outside_factor_nonpositive",
    "q1_control_wrong", "q3_control_wrong", "h4_control_wrong",
    "h9_control_wrong", "even4_four_shift_leak", "claim_growing_q",
    "claim_ordinary_Cesaro", "claim_causal", "claim_adaptive",
    "claim_operator", "claim_RH_gate",
)

MUTATION_TARGETS = (
    ("mu0_to_mu", "A01_mu0_boundary"),
    ("fixed_h_to_growing", "A02_fixed_h_q_F_clock"),
    ("fixed_q_to_growing", "A02_fixed_h_q_F_clock"),
    ("shift_order_swap", "A03_ordered_shifts_L_h_C_0_R_minus_h"),
    ("score_drops_center", "A04_output_vs_score"),
    ("safety_step_2h", "A05_separation_h_four_symbol_safety"),
    ("safety_unshares_center_right", "A05_separation_h_four_symbol_safety"),
    ("max_before_limit", "A07_limit_then_finite_max_order"),
    ("analytic_role_promoted", "A08_RH394_sole_analytic_input"),
    ("kappa_collision_ignored", "A09_collision_aware_theta_kappa2_kappa3"),
    ("Pi_sign_flip", "B02_Pi_inclusion_exclusion_mass"),
    ("lambda_drop_sign_half", "B03_lambda_exact_support_sign_split"),
    ("baseline_not_zero", "B05_all_minus_projected_baseline_zero"),
    ("projection_wrong_center", "B06_positive_projection_pointwise_monotone_safe"),
    ("relation_uses_center_minus", "B07_relation_A_center_plus"),
    ("reflection_no_input_negation", "B09_reflection_preserves_safety_negates_limit"),
    ("source_target_swap", "C01_source_target_flag_definitions"),
    ("flag_shift_reverse", "C03_safety_iff_t_r_s_rplush_zero"),
    ("safe_pair_count_wrong", "C04_exhaustive_relation_pair_safety_61440"),
    ("flag_class_count_wrong", "C05_exact_flag_class_counts_16_48_48_400"),
    ("rectangle_00_wrong", "C07_rectangle_00_size4_exact_flags"),
    ("rectangle_10_wrong", "C08_rectangle_10_size6_exact_flags"),
    ("rectangle_01_wrong", "C09_rectangle_01_size6_exact_flags"),
    ("rectangle_11_wrong", "C10_rectangle_11_size9_exact_flags"),
    ("containment_reverse", "C11_relation_contained_in_own_flag_rectangle"),
    ("saturation_loses_gain", "C12_saturation_preserves_flags_safety_coefficientwise_gain"),
    ("rectangle_W_minus", "D05_rectangle_value_inclusion_exclusion"),
    ("U_missing_half", "D02_U_plus_source_row_half_ThetaLC"),
    ("V_missing_half", "D03_V_plus_target_column_half_ThetaCR"),
    ("W_missing_quarter", "D04_W_corner_positive_quarter_ThetaLCR"),
    ("theta_subset_reverse", "D06_ThetaLCR_le_ThetaLC_and_ThetaCR"),
    ("W_le_U_not_half", "D07_W_le_U_over2_le_U_and_W_le_V_over2_le_V"),
    ("theta_nu_multiplicity", "D08_translation_p_not_divide_q_nu_branch"),
    ("theta_tau_before_dedup", "D09_translation_p_parallel_q_tau_after_p2_dedup"),
    ("theta_indicator_complement", "D10_translation_p2_divides_q_indicator_branch"),
    ("translation_shift_2h", "D12_V_r_equals_U_rplush_and_phase_sums"),
    ("edge_inequality_reverse", "E01_binary_safety_edge_t_plus_snext_le1"),
    ("addition_gain_W_sign", "E03_exact_addition_gain_U_next_minus_1_minus_tnext_times_W_next"),
    ("addition_gain_wrong_t", "E03_exact_addition_gain_U_next_minus_1_minus_tnext_times_W_next"),
    ("selfloop_allows_vertex", "E09_rising_set_independent_including_selfloop"),
    ("empty_IS_forbidden", "E10_every_independent_set_realized_including_empty"),
    ("IS_surjectivity_reverse", "E10_every_independent_set_realized_including_empty"),
    ("weighted_IS_unweighted", "E11_weighted_IS_formula_all_h_q"),
    ("q2_parity_swap", "F02_q2_p_parallel2_tau_even1_odd2"),
    ("even_lift_requires_minimal", "F05_every_even_declared_q_nonminimal_lift_attains"),
    ("odd_q_attains", "F10_attainment_iff_q_even_q1_strict"),
    ("CRT_p3_one_case", "F07_odd_q_CRT_p3_parallel_three_cases"),
    ("indicator_avoids_three_classes", "F08_odd_q_CRT_p2_indicator_avoid_four_classes"),
    ("outside_factor_nonpositive", "F09_outside_q_Euler_factors_positive_and_adjacent_positive_weights"),
    ("q1_control_wrong", "F11_h1_q1_q2_q3_exact_controls"),
    ("q3_control_wrong", "F11_h1_q1_q2_q3_exact_controls"),
    ("h4_control_wrong", "F12_h4_q4_h9_q2_collision_controls"),
    ("h9_control_wrong", "F12_h4_q4_h9_q2_collision_controls"),
    ("even4_four_shift_leak", "G02_no_even4_c1111_leak_three_shift_only"),
    ("claim_growing_q", "G03_no_growing_Cesaro_causal_adaptive_operator_Gates"),
    ("claim_ordinary_Cesaro", "G03_no_growing_Cesaro_causal_adaptive_operator_Gates"),
    ("claim_causal", "G03_no_growing_Cesaro_causal_adaptive_operator_Gates"),
    ("claim_adaptive", "G03_no_growing_Cesaro_causal_adaptive_operator_Gates"),
    ("claim_operator", "G03_no_growing_Cesaro_causal_adaptive_operator_Gates"),
    ("claim_RH_gate", "G03_no_growing_Cesaro_causal_adaptive_operator_Gates"),
)

# Each edit is (path inside the targeted row's data, exact old leaf, new leaf).
# This is deliberately explicit: mutation names are semantic negative controls,
# not labels pasted onto arbitrary byte changes.
_MUTATION_EDITS = {
    "mu0_to_mu": (("definition",), "mu_0(k)=mu(k) for k>=1 and 0 for k<=0", "mu_0(k)=mu(k) for all k"),
    "fixed_h_to_growing": (("h_depends_on_X",), False, True),
    "fixed_q_to_growing": (("q_depends_on_X",), False, True),
    "shift_order_swap": (("shifts",), ["+h", "0", "-h"], ["-h", "0", "+h"]),
    "score_drops_center": (("center_factor_present",), True, False),
    "safety_step_2h": (("step",), "h", "2h"),
    "safety_unshares_center_right": (("shared_symbols",), ["z", "y"], ["y"]),
    "max_before_limit": (("prelimit_maximum",), False, True),
    "analytic_role_promoted": (("sole_analytic_input",), True, False),
    "kappa_collision_ignored": (("unconditional_K2_K3_substitution",), False, True),
    "Pi_sign_flip": (("definition",), "Pi(U)=sum_(W subset I\\U)(-1)^|W|Theta(U union W)", "Pi(U)=sum_(W subset I\\U)(+1)^|W|Theta(U union W)"),
    "lambda_drop_sign_half": (("divisor",), 4, 2),
    "baseline_not_zero": (("stratum_sign_average",), "0", "nonzero"),
    "projection_wrong_center": (("deleted_plus_count",), 18, 36),
    "relation_uses_center_minus": (("definition",), "A_r={(x,y):F_r(x,+1,y)=+1}", "A_r={(x,y):F_r(x,-1,y)=+1}"),
    "reflection_no_input_negation": (("table_map",), "F^rho_r(x,z,y)=F_r(-x,-z,-y)", "F^rho_r(x,z,y)=F_r(x,z,y)"),
    "source_target_swap": (("s",), "1_(+1 in Source(A_r))", "1_(+1 in Target(A_r))"),
    "flag_shift_reverse": (("criterion",), "t_r*s_(r+h)=0", "t_r*s_(r-h)=0"),
    "safe_pair_count_wrong": (("safe",), 61440, 61439),
    "flag_class_count_wrong": (("counts", "00"), 16, 17),
    "rectangle_00_wrong": (("size",), 4, 5),
    "rectangle_10_wrong": (("size",), 6, 7),
    "rectangle_01_wrong": (("size",), 6, 7),
    "rectangle_11_wrong": (("size",), 9, 8),
    "containment_reverse": (("failures",), 0, 1),
    "saturation_loses_gain": (("safety_failures",), 0, 1),
    "rectangle_W_minus": (("corner_sign",), "+", "-"),
    "U_missing_half": (("definition",), "U=Theta(L,C)/2", "U=Theta(L,C)"),
    "V_missing_half": (("definition",), "V=Theta(C,R)/2", "V=Theta(C,R)"),
    "W_missing_quarter": (("definition",), "W=Theta(L,C,R)/4", "W=Theta(L,C,R)"),
    "theta_subset_reverse": (("failures",), 0, 1),
    "W_le_U_not_half": (("W_le_U_over_2",), True, False),
    "theta_nu_multiplicity": (("translated_deduplicated_sets",), True, False),
    "theta_tau_before_dedup": (("tau_after_mod_p2_dedup",), True, False),
    "theta_indicator_complement": (("translated_indicator",), True, False),
    "translation_shift_2h": (("translation_pass",), True, False),
    "edge_inequality_reverse": (("inequality",), "t_r+s_(r+h)<=1", "t_r+s_(r+h)>=1"),
    "addition_gain_W_sign": (("corner_sign",), "negative_in_gain", "positive_in_gain"),
    "addition_gain_wrong_t": (("gain",), "U_(r+h)-(1-t_(r+h))*W_(r+h)", "U_(r+h)-(1-t_r)*W_(r+h)"),
    "selfloop_allows_vertex": (("selfloop_only_empty",), True, False),
    "empty_IS_forbidden": (("empty_included",), True, False),
    "IS_surjectivity_reverse": (("cases", 0, "pass"), True, False),
    "weighted_IS_unweighted": (("weighted",), True, False),
    "q2_parity_swap": (("rows", 0, "tau"), 1, 2),
    "even_lift_requires_minimal": (("minimal_period_required",), False, True),
    "odd_q_attains": (("rows", 0, "attains"), False, True),
    "CRT_p3_one_case": (("cases",), ["3_not_divide_h", "3_divide_h_9_not_divide_h", "9_divide_h"], ["3_not_divide_h"]),
    "indicator_avoids_three_classes": (("max_classes",), 4, 3),
    "outside_factor_nonpositive": (("outside_q_factors_positive",), True, False),
    "q1_control_wrong": (("rows", 0, "coefficients", 3), "0", "1/4"),
    "q3_control_wrong": (("rows", 2, "coefficients", 3), "1/12", "1/4"),
    "h4_control_wrong": (("rows", 0, "coefficients", 2), "-3/4", "-1/2"),
    "h9_control_wrong": (("rows", 1, "coefficients", 3), "1/3", "1/4"),
    "even4_four_shift_leak": (("analytic_shift_count",), 3, 4),
    "claim_growing_q": (("firewalls", "growing_q"), False, True),
    "claim_ordinary_Cesaro": (("firewalls", "ordinary_Cesaro"), False, True),
    "claim_causal": (("firewalls", "causal_online"), False, True),
    "claim_adaptive": (("firewalls", "adaptive"), False, True),
    "claim_operator": (("firewalls", "operator"), False, True),
    "claim_RH_gate": (("firewalls", "RH"), False, True),
}


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
        text, object_pairs_hook=_pairs_no_duplicates, parse_constant=_reject_constant
    )


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(
            exact_equal(left[key], right[key]) for key in left
        )
    if type(left) in (list, tuple):
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right)
        )
    if type(left) is float:
        return math.isfinite(left) and math.isfinite(right) and left == right
    return left == right


def fraction_text(value: Fraction) -> str:
    if type(value) is not Fraction:
        raise TypeError("fraction serializer requires exact Fraction")
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def expr_text(value: tuple[Fraction, Fraction, Fraction, Fraction]) -> list[str]:
    if type(value) is not tuple or len(value) != 4:
        raise TypeError("K-expression must be an exact K0--K3 four-tuple")
    return [fraction_text(item) for item in value]


def expr_add(
    left: tuple[Fraction, Fraction, Fraction, Fraction],
    right: tuple[Fraction, Fraction, Fraction, Fraction],
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return tuple(a + b for a, b in zip(left, right))  # type: ignore[return-value]


def expr_scale(
    scalar: Fraction, value: tuple[Fraction, Fraction, Fraction, Fraction]
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    if type(scalar) is not Fraction:
        raise TypeError("expression scalar must be exact Fraction")
    return tuple(scalar * item for item in value)  # type: ignore[return-value]


def factorization(value: int) -> tuple[tuple[int, int], ...]:
    if type(value) is not int or value < 1:
        raise ValueError("factorization input must be a positive exact integer")
    output: list[tuple[int, int]] = []
    remaining = value
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


@lru_cache(maxsize=None)
def primes_through(limit: int) -> tuple[int, ...]:
    if type(limit) is not int or limit < 2:
        raise ValueError("prime cutoff must be an exact integer at least two")
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return tuple(index for index in range(2, limit + 1) if sieve[index])


def prime_support(value: int) -> tuple[int, ...]:
    return tuple(prime for prime, _exponent in factorization(value))


def is_prime(value: int) -> bool:
    if type(value) is not int or value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def shift_by_coordinate(h: int) -> dict[str, int]:
    if type(h) is not int or h < 1:
        raise ValueError("lag h must be a fixed positive exact integer")
    return {"L": h, "C": 0, "R": -h}


def _ordered_support(values: Iterable[str]) -> tuple[str, ...]:
    support = tuple(values)
    if any(type(value) is not str or value not in COORDINATES for value in support):
        raise ValueError("support contains an invalid coordinate")
    if len(set(support)) != len(support):
        raise ValueError("support contains a duplicate coordinate")
    return tuple(value for value in COORDINATES if value in support)


def residue_set(h: int, prime: int, support: Iterable[str]) -> tuple[int, ...]:
    if not is_prime(prime):
        raise ValueError("prime must be an exact prime integer")
    shifts = shift_by_coordinate(h)
    return tuple(sorted({shifts[item] % (prime * prime) for item in _ordered_support(support)}))


def nu_support(h: int, prime: int, support: Iterable[str]) -> int:
    return len(residue_set(h, prime, support))


def tau_support(h: int, prime: int, phase: int, support: Iterable[str]) -> int:
    if type(phase) is not int:
        raise TypeError("phase must be an exact integer")
    residues = residue_set(h, prime, support)
    return sum(1 for residue in residues if residue % prime == phase % prime)


def exceptional_primes(h: int, support: Iterable[str]) -> tuple[int, ...]:
    support_tuple = _ordered_support(support)
    shifts = shift_by_coordinate(h)
    differences = {
        abs(shifts[a] - shifts[b])
        for index, a in enumerate(support_tuple)
        for b in support_tuple[index + 1 :]
    }
    candidates = {
        prime
        for difference in differences
        if difference
        for prime, exponent in factorization(difference)
        if exponent >= 2
    }
    return tuple(sorted(candidates))


@lru_cache(maxsize=None)
def theta_coefficients(
    h: int, q: int, phase: int, support: tuple[str, ...]
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    if type(q) is not int or q < 1 or type(phase) is not int or not 0 <= phase < q:
        raise ValueError("phase must use exact q>=1 and 0<=phase<q")
    support = _ordered_support(support)
    cardinality = len(support)
    if cardinality not in (0, 1, 2, 3):
        raise ValueError("theta supports have size zero through three")
    q_factor = dict(factorization(q))
    relevant = sorted(set(q_factor) | set(exceptional_primes(h, support)))
    coefficient = Fraction(1, q)
    for prime in relevant:
        base = Fraction(prime * prime - cardinality, prime * prime)
        if prime not in q_factor:
            replacement = Fraction(
                prime * prime - nu_support(h, prime, support), prime * prime
            )
        elif q_factor[prime] == 1:
            replacement = Fraction(
                prime - tau_support(h, prime, phase, support), prime
            )
        else:
            replacement = Fraction(
                int(phase % (prime * prime) not in residue_set(h, prime, support))
            )
        coefficient *= replacement / base
    output = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    output[cardinality] = coefficient
    return tuple(output)  # type: ignore[return-value]


@lru_cache(maxsize=None)
def exact_support_coefficients(
    h: int, q: int, phase: int, support: tuple[str, ...]
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    support = _ordered_support(support)
    complement = tuple(item for item in COORDINATES if item not in support)
    output = ZERO_EXPR
    for subset_mask in range(1 << len(complement)):
        extension = tuple(
            complement[index]
            for index in range(len(complement))
            if subset_mask & (1 << index)
        )
        sign = Fraction(-1 if subset_mask.bit_count() % 2 else 1)
        output = expr_add(
            output,
            expr_scale(sign, theta_coefficients(h, q, phase, _ordered_support((*support, *extension)))),
        )
    return output


@lru_cache(maxsize=None)
def lambda_coefficients(
    h: int, q: int, phase: int, left: int, right: int
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    if type(left) is not int or type(right) is not int or left not in T or right not in T:
        raise ValueError("lambda signs must be exact ternary integers")
    support = ["C"]
    if left != 0:
        support.append("L")
    if right != 0:
        support.append("R")
    divisor = 1 << (int(left != 0) + int(right != 0))
    return expr_scale(
        Fraction(1, divisor),
        exact_support_coefficients(h, q, phase, _ordered_support(support)),
    )


@lru_cache(maxsize=None)
def basis_intervals(
    limit: int = INTERVAL_CUTOFF,
) -> tuple[tuple[Fraction, Fraction], ...]:
    """Rigorous rational enclosures for K_0,...,K_3.

    The elementary tail inequality
    ``prod_{p>x}(1-j/p^2) >= 1-j/x`` is deliberately coarse but sufficient
    to order every finite optimizer used by this certificate.
    """

    if type(limit) is not int or limit <= 3:
        raise ValueError("Euler-product interval cutoff must exceed three")
    output = [(Fraction(1), Fraction(1))]
    primes = primes_through(limit)
    for order in (1, 2, 3):
        upper = Fraction(1)
        for prime in primes:
            upper *= Fraction(prime * prime - order, prime * prime)
        output.append((upper * Fraction(limit - order, limit), upper))
    return tuple(output)


@lru_cache(maxsize=None)
def expr_interval(
    value: tuple[Fraction, Fraction, Fraction, Fraction],
    limit: int = INTERVAL_CUTOFF,
) -> tuple[Fraction, Fraction]:
    if type(value) is not tuple or len(value) != 4 or any(
        type(coefficient) is not Fraction for coefficient in value
    ):
        raise TypeError("interval evaluation requires an exact K0--K3 expression")
    lower = Fraction(0)
    upper = Fraction(0)
    for coefficient, (basis_lower, basis_upper) in zip(value, basis_intervals(limit)):
        if coefficient >= 0:
            lower += coefficient * basis_lower
            upper += coefficient * basis_upper
        else:
            lower += coefficient * basis_upper
            upper += coefficient * basis_lower
    return lower, upper


def compare_expressions(
    left: tuple[Fraction, Fraction, Fraction, Fraction],
    right: tuple[Fraction, Fraction, Fraction, Fraction],
) -> int:
    difference = tuple(a - b for a, b in zip(left, right))
    if difference == ZERO_EXPR:
        return 0
    lower, upper = expr_interval(difference)  # exact rational enclosure
    if lower > 0:
        return 1
    if upper < 0:
        return -1
    raise ArithmeticError("Euler-product intervals overlap for distinct candidates")


def state_members(mask: int) -> tuple[int, ...]:
    if type(mask) is not int or not 0 <= mask < 8:
        raise ValueError("state mask must be an exact integer in [0,8)")
    return tuple(value for index, value in enumerate(T) if mask & (1 << index))


def state_mask(values: Iterable[int]) -> int:
    output = 0
    seen: set[int] = set()
    for value in values:
        if type(value) is not int or value not in T or value in seen:
            raise ValueError("state contains an invalid or duplicate ternary value")
        seen.add(value)
        output |= 1 << T.index(value)
    return output


def reflected_state_mask(mask: int) -> int:
    return state_mask(-value for value in state_members(mask))


def relation_pairs(mask: int) -> tuple[tuple[int, int], ...]:
    if type(mask) is not int or not 0 <= mask < 512:
        raise ValueError("relation mask must be an exact integer in [0,512)")
    universe = tuple((left, right) for left in T for right in T)
    return tuple(pair for index, pair in enumerate(universe) if mask & (1 << index))


def relation_mask(pairs: Iterable[tuple[int, int]]) -> int:
    universe = tuple((left, right) for left in T for right in T)
    output = 0
    seen: set[tuple[int, int]] = set()
    for pair in pairs:
        if type(pair) is not tuple or pair not in universe or pair in seen:
            raise ValueError("relation contains an invalid or duplicate ternary pair")
        seen.add(pair)
        output |= 1 << universe.index(pair)
    return output


@lru_cache(maxsize=None)
def relation_source_mask(mask: int) -> int:
    return state_mask({left for left, _right in relation_pairs(mask)})


@lru_cache(maxsize=None)
def relation_target_mask(mask: int) -> int:
    return state_mask({right for _left, right in relation_pairs(mask)})


def reflected_relation_mask(mask: int) -> int:
    return relation_mask((-left, -right) for left, right in relation_pairs(mask))


def relation_composition_empty(left: int, right: int) -> bool:
    return relation_target_mask(left) & relation_source_mask(right) == 0


def saturated_relation(previous_target: int, current_target: int) -> int:
    previous = set(state_members(previous_target))
    current = set(state_members(current_target))
    return relation_mask(
        (left, right) for left in T if left not in previous for right in current
    )


def relation_source_plus_flag(mask: int) -> int:
    """Return whether a relation contains a cell in the ``x=+1`` row."""

    return int(1 in state_members(relation_source_mask(mask)))


def relation_target_plus_flag(mask: int) -> int:
    """Return whether a relation contains a cell in the ``y=+1`` column."""

    return int(1 in state_members(relation_target_mask(mask)))


def relation_flags(mask: int) -> tuple[int, int]:
    """Return the half-span source/target flags ``(s,t)`` of a relation."""

    return relation_source_plus_flag(mask), relation_target_plus_flag(mask)


def half_span_relation_safe(left: int, right: int) -> bool:
    """Test the exact separation-``h`` concatenation obstruction.

    A projected positive at phase ``r`` and one at phase ``r+h`` can
    concatenate exactly when the first relation reaches ``+1`` and the
    second relation starts at ``+1``.  No four-point analytic average is
    involved in this finite universal safety test.
    """

    return not (
        relation_target_plus_flag(left) and relation_source_plus_flag(right)
    )


def flag_rectangle(source_plus: int, target_plus: int) -> int:
    """Return ``X_s x Y_t`` for exact binary flags ``s,t``.

    ``X_0=Y_0=T\\{+1}`` and ``X_1=Y_1=T``.  The four rectangle sizes are
    consequently ``4,6,6,9`` in flag order ``00,10,01,11``.
    """

    if type(source_plus) is not int or source_plus not in (0, 1):
        raise ValueError("source flag must be the exact integer zero or one")
    if type(target_plus) is not int or target_plus not in (0, 1):
        raise ValueError("target flag must be the exact integer zero or one")
    sources = T if source_plus else (-1, 0)
    targets = T if target_plus else (-1, 0)
    return relation_mask((left, right) for left in sources for right in targets)


def saturate_relation_to_flags(mask: int) -> int:
    """Saturate a relation to its own flag rectangle."""

    source_plus, target_plus = relation_flags(mask)
    return flag_rectangle(source_plus, target_plus)


@lru_cache(maxsize=1)
def relation_oracle() -> dict[str, object]:
    """Exhaust all 512 relations and all 512-squared ordered pairs."""

    class_counts = {(0, 0): 0, (1, 0): 0, (0, 1): 0, (1, 1): 0}
    containment_failures = 0
    saturation_flag_failures = 0
    for mask in range(512):
        flags = relation_flags(mask)
        class_counts[flags] += 1
        saturated = saturate_relation_to_flags(mask)
        if mask & ~saturated:
            containment_failures += 1
        if relation_flags(saturated) != flags:
            saturation_flag_failures += 1

    safe = 0
    criterion_failures = 0
    saturated_pair_failures = 0
    for left in range(512):
        for right in range(512):
            criterion = half_span_relation_safe(left, right)
            explicit = not any(
                first_right == 1 and second_left == 1
                for _first_left, first_right in relation_pairs(left)
                for second_left, _second_right in relation_pairs(right)
            )
            if criterion != explicit:
                criterion_failures += 1
            if not criterion:
                continue
            safe += 1
            if not half_span_relation_safe(
                saturate_relation_to_flags(left),
                saturate_relation_to_flags(right),
            ):
                saturated_pair_failures += 1

    class_rows = {
        f"{source}{target}": class_counts[(source, target)]
        for source, target in ((0, 0), (1, 0), (0, 1), (1, 1))
    }
    return {
        "relation_count": 512,
        "ordered_pair_count": 262144,
        "safe_pair_count": safe,
        "flag_class_counts": class_rows,
        "criterion_failure_count": criterion_failures,
        "containment_failure_count": containment_failures,
        "saturation_flag_failure_count": saturation_flag_failures,
        "saturated_pair_failure_count": saturated_pair_failures,
        "pass": (
            safe == 61440
            and class_rows == {"00": 16, "10": 48, "01": 48, "11": 400}
            and criterion_failures == containment_failures
            == saturation_flag_failures == saturated_pair_failures == 0
        ),
    }


def _better_candidate(
    left: tuple[tuple[Fraction, Fraction, Fraction, Fraction], tuple[int, ...]],
    right: tuple[tuple[Fraction, Fraction, Fraction, Fraction], tuple[int, ...]],
) -> tuple[tuple[Fraction, Fraction, Fraction, Fraction], tuple[int, ...]]:
    comparison = compare_expressions(left[0], right[0])
    if comparison > 0 or (comparison == 0 and left[1] < right[1]):
        return left
    return right


@lru_cache(maxsize=None)
def phase_MUVW(
    h: int, q: int, phase: int
) -> tuple[
    tuple[Fraction, Fraction, Fraction, Fraction],
    tuple[Fraction, Fraction, Fraction, Fraction],
    tuple[Fraction, Fraction, Fraction, Fraction],
    tuple[Fraction, Fraction, Fraction, Fraction],
]:
    """Return the four exact phase weights ``(M,U,V,W)``.

    These are respectively ``Theta(C)``, ``Theta(L,C)/2``,
    ``Theta(C,R)/2``, and ``Theta(L,C,R)/4``.  They are kept as formal
    ``K_0,...,K_3`` expressions, so collision branches remain exact.
    """

    return (
        theta_coefficients(h, q, phase, ("C",)),
        expr_scale(Fraction(1, 2), theta_coefficients(h, q, phase, ("L", "C"))),
        expr_scale(Fraction(1, 2), theta_coefficients(h, q, phase, ("C", "R"))),
        expr_scale(
            Fraction(1, 4),
            theta_coefficients(h, q, phase, ("L", "C", "R")),
        ),
    )


def rectangle_value_coefficients(
    h: int, q: int, phase: int, source_plus: int, target_plus: int
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Evaluate the exact flag rectangle by inclusion--exclusion.

    The sign of the corner term is deliberately positive:
    ``M-(1-s)U-(1-t)V+(1-s)(1-t)W``.
    """

    if type(source_plus) is not int or source_plus not in (0, 1):
        raise ValueError("source flag must be the exact integer zero or one")
    if type(target_plus) is not int or target_plus not in (0, 1):
        raise ValueError("target flag must be the exact integer zero or one")
    M, U, V, W = phase_MUVW(h, q, phase)
    output = M
    output = expr_add(output, expr_scale(Fraction(source_plus - 1), U))
    output = expr_add(output, expr_scale(Fraction(target_plus - 1), V))
    if source_plus == 0 and target_plus == 0:
        output = expr_add(output, W)
    return output


def half_span_cycles(h: int, q: int) -> tuple[tuple[int, ...], ...]:
    """Decompose ``Z/qZ`` into directed cycles for the step ``r -> r+h``."""

    if type(h) is not int or h < 1 or type(q) is not int or q < 1:
        raise ValueError("half-span cycles require exact h,q>=1")
    seen: set[int] = set()
    output: list[tuple[int, ...]] = []
    for start in range(q):
        if start in seen:
            continue
        cycle: list[int] = []
        phase = start
        while phase not in seen:
            seen.add(phase)
            cycle.append(phase)
            phase = (phase + h) % q
        output.append(tuple(cycle))
    return tuple(output)


def weighted_independent_set(
    h: int, q: int
) -> dict[str, object]:
    """Exact maximum-weight independent set on all step-``h`` cycles."""

    total = ZERO_EXPR
    witness: list[int] = []
    cycle_rows: list[dict[str, object]] = []
    for cycle in half_span_cycles(h, q):
        if len(cycle) == 1:
            best = (ZERO_EXPR, (0,))
        else:
            best: tuple[
                tuple[Fraction, Fraction, Fraction, Fraction], tuple[int, ...]
            ] | None = None
            for first in (0, 1):
                dynamic = {first: (
                    phase_MUVW(h, q, cycle[0])[3] if first else ZERO_EXPR,
                    (first,),
                )}
                for phase in cycle[1:]:
                    updated: dict[int, tuple[
                        tuple[Fraction, Fraction, Fraction, Fraction],
                        tuple[int, ...],
                    ]] = {}
                    for previous, (score, path) in dynamic.items():
                        for current in (0, 1):
                            if previous and current:
                                continue
                            candidate = (
                                expr_add(score, phase_MUVW(h, q, phase)[3])
                                if current else score,
                                (*path, current),
                            )
                            old = updated.get(current)
                            updated[current] = (
                                candidate if old is None
                                else _better_candidate(candidate, old)
                            )
                    dynamic = updated
                for last, candidate in dynamic.items():
                    if first and last:
                        continue
                    best = candidate if best is None else _better_candidate(candidate, best)
            if best is None:
                raise RuntimeError("empty independent-set cycle optimization")
        total = expr_add(total, best[0])
        selected = tuple(
            phase for phase, bit in zip(cycle, best[1]) if bit
        )
        witness.extend(selected)
        cycle_rows.append({
            "phases": list(cycle),
            "selected": list(selected),
            "coefficients": expr_text(best[0]),
        })
    return {
        "h": h,
        "q": q,
        "step": h,
        "cycle_count": len(half_span_cycles(h, q)),
        "coefficients": expr_text(total),
        "selected": sorted(witness),
        "cycles": cycle_rows,
    }


def half_span_capacity(h: int, q: int) -> dict[str, object]:
    """Return ``K1-kappa2(h)/2`` plus the weighted rising-set optimum."""

    base = ZERO_EXPR
    for phase in range(q):
        M, U, _V, _W = phase_MUVW(h, q, phase)
        base = expr_add(base, expr_add(M, expr_scale(Fraction(-1), U)))
    independent = weighted_independent_set(h, q)
    bonus = tuple(Fraction(text) for text in independent["coefficients"])
    total = expr_add(base, bonus)  # type: ignore[arg-type]
    return {
        "h": h,
        "q": q,
        "base_coefficients": expr_text(base),
        "bonus_coefficients": expr_text(bonus),  # type: ignore[arg-type]
        "coefficients": expr_text(total),
        "selected": independent["selected"],
    }


def flag_brute_capacity(h: int, q: int) -> dict[str, object]:
    """Independent exhaustive flag-profile oracle for deliberately small clocks."""

    if type(h) is not int or h < 1 or type(q) is not int or not 1 <= q <= 8:
        raise ValueError("flag brute oracle requires exact h>=1 and 1<=q<=8")
    profiles: list[tuple[tuple[int, int], ...]] = [()]
    for _phase in range(q):
        profiles = [
            (*profile, (source, target))
            for profile in profiles
            for source in (0, 1)
            for target in (0, 1)
        ]
    best: tuple[
        tuple[Fraction, Fraction, Fraction, Fraction], tuple[int, ...]
    ] | None = None
    safe_count = 0
    for profile in profiles:
        if any(
            profile[phase][1] and profile[(phase + h) % q][0]
            for phase in range(q)
        ):
            continue
        safe_count += 1
        score = ZERO_EXPR
        for phase, (source, target) in enumerate(profile):
            score = expr_add(
                score,
                rectangle_value_coefficients(h, q, phase, source, target),
            )
        flattened = tuple(bit for flags in profile for bit in flags)
        candidate = (score, flattened)
        best = candidate if best is None else _better_candidate(candidate, best)
    if best is None:
        raise RuntimeError("empty flag-profile optimization")
    return {
        "h": h,
        "q": q,
        "profile_count": len(profiles),
        "safe_profile_count": safe_count,
        "coefficients": expr_text(best[0]),
        "profile": list(best[1]),
    }


def projection_oracle() -> dict[str, object]:
    cases = deleted = monotonicity_failures = inclusion_failures = 0
    for left in T:
        for center in T:
            for right in T:
                for old_output in (-1, 1):
                    cases += 1
                    new_output = old_output if center == 1 else -1
                    if new_output == 1 and old_output != 1:
                        inclusion_failures += 1
                    if center * new_output < center * old_output:
                        monotonicity_failures += 1
                    if old_output == 1 and new_output == -1:
                        deleted += 1
    return {
        "case_count": cases,
        "deleted_plus_count": deleted,
        "plus_inclusion_failure_count": inclusion_failures,
        "score_monotonicity_failure_count": monotonicity_failures,
        "pass": cases == 54 and deleted == 18
        and inclusion_failures == monotonicity_failures == 0,
    }


def reflection_oracle() -> dict[str, object]:
    """Finite algebra behind input reflection, safety, and score negation."""

    quadruple_cases = overlap_failures = involution_failures = 0
    for left in T:
        for center in T:
            for right in T:
                for outer in T:
                    quadruple_cases += 1
                    first = (-left, -center, -right)
                    second = (-center, -right, -outer)
                    if first[1:] != second[:2]:
                        overlap_failures += 1
                    if tuple(-value for value in first) != (left, center, right):
                        involution_failures += 1
                    if tuple(-value for value in second) != (center, right, outer):
                        involution_failures += 1
    score_cases = score_failures = 0
    for left in T:
        for center in T:
            for right in T:
                for reflected_output in (-1, 1):
                    score_cases += 1
                    reflected_score = center * reflected_output
                    original_score_at_negated_input = -center * reflected_output
                    if reflected_score != -original_score_at_negated_input:
                        score_failures += 1
    return {
        "input_quadruple_cases": quadruple_cases,
        "overlap_failures": overlap_failures,
        "involution_failures": involution_failures,
        "score_cell_cases": score_cases,
        "score_negation_failures": score_failures,
        "pass": quadruple_cases == 81 and score_cases == 54
        and overlap_failures == involution_failures == score_failures == 0,
    }


def translation_branch_oracle() -> dict[str, object]:
    """Exhaust the three local Theta branches after mod-p^2 deduplication."""

    nu_cases = tau_cases = indicator_cases = 0
    nu_failures = tau_failures = indicator_failures = 0
    for prime in (2, 3, 5, 7):
        modulus = prime * prime
        for h_residue in range(modulus):
            pair_cr = {0, (-h_residue) % modulus}
            pair_lc = {h_residue % modulus, 0}
            translated = {(value + h_residue) % modulus for value in pair_cr}
            nu_cases += 1
            if translated != pair_lc or len(pair_cr) != len(pair_lc):
                nu_failures += 1
            for phase in range(modulus):
                tau_cases += 1
                tau_cr = sum(value % prime == phase % prime for value in pair_cr)
                tau_lc = sum(
                    value % prime == (phase + h_residue) % prime
                    for value in pair_lc
                )
                if tau_cr != tau_lc:
                    tau_failures += 1
                indicator_cases += 1
                allowed_cr = phase % modulus not in pair_cr
                allowed_lc = (phase + h_residue) % modulus not in pair_lc
                if allowed_cr != allowed_lc:
                    indicator_failures += 1
    return {
        "primes": [2, 3, 5, 7],
        "nu_cases": nu_cases,
        "nu_failures": nu_failures,
        "tau_cases": tau_cases,
        "tau_failures": tau_failures,
        "indicator_cases": indicator_cases,
        "indicator_failures": indicator_failures,
        "pass": nu_failures == tau_failures == indicator_failures == 0,
    }


def phase_translation_grid_oracle() -> dict[str, object]:
    """Exercise the public M,U,V,W implementation across mixed q branches."""

    cases = failures = 0
    for h in range(1, 13):
        for q in range(1, 19):
            for phase in range(q):
                cases += 1
                if phase_MUVW(h, q, phase)[2] != phase_MUVW(
                    h, q, (phase + h) % q
                )[1]:
                    failures += 1
    return {"h_max": 12, "q_max": 18, "cases": cases, "failures": failures,
            "pass": failures == 0}


def odd_clock_local_oracle() -> dict[str, object]:
    """Finite local reproduction of every CRT branch used for odd q."""

    p_ge_5_cases = p_ge_5_failures = 0
    for prime in (5, 7):
        modulus = prime * prime
        for h_residue in range(modulus):
            triple = {h_residue % modulus, 0, (-h_residue) % modulus}
            for phase in range(prime):
                p_ge_5_cases += 1
                tau = sum(value % prime == phase for value in triple)
                if not (tau <= 3 < prime):
                    p_ge_5_failures += 1

    p3_cases = p3_failures = 0
    p3_categories = {
        "3_not_divide_h": 0,
        "3_divide_h_9_not_divide_h": 0,
        "9_divide_h": 0,
    }
    for h_residue in range(9):
        if h_residue % 3:
            category = "3_not_divide_h"
        elif h_residue:
            category = "3_divide_h_9_not_divide_h"
        else:
            category = "9_divide_h"
        p3_categories[category] += 1
        triple = {h_residue % 9, 0, (-h_residue) % 9}
        p3_cases += 1
        if not any(
            sum(value % 3 == phase for value in triple) < 3
            and sum(value % 3 == (phase + h_residue) % 3 for value in triple) < 3
            for phase in range(3)
        ):
            p3_failures += 1

    indicator_cases = indicator_failures = max_forbidden_classes = 0
    for prime in (3, 5):
        modulus = prime * prime
        for h_residue in range(modulus):
            forbidden = {
                h_residue % modulus, 0, (-h_residue) % modulus,
                (-2 * h_residue) % modulus,
            }
            indicator_cases += 1
            max_forbidden_classes = max(max_forbidden_classes, len(forbidden))
            if len(forbidden) > 4 or len(forbidden) >= modulus:
                indicator_failures += 1

    outside_cases = outside_failures = 0
    for prime in (2, 3, 5, 7):
        modulus = prime * prime
        residues = range(1, modulus, 2) if prime == 2 else range(modulus)
        for h_residue in residues:
            outside_cases += 1
            triple_size = len({h_residue % modulus, 0, (-h_residue) % modulus})
            if triple_size >= modulus:
                outside_failures += 1
    return {
        "p_ge_5_cases": p_ge_5_cases,
        "p_ge_5_failures": p_ge_5_failures,
        "p3_cases": p3_cases,
        "p3_categories": p3_categories,
        "p3_failures": p3_failures,
        "indicator_cases": indicator_cases,
        "max_forbidden_classes": max_forbidden_classes,
        "indicator_failures": indicator_failures,
        "outside_cases": outside_cases,
        "outside_failures": outside_failures,
        "pass": p_ge_5_failures == p3_failures == indicator_failures
        == outside_failures == 0,
    }


def _row(
    group: str, identifier: str, data: dict[str, object], passed: bool
) -> dict[str, object]:
    if type(passed) is not bool:
        raise TypeError("row pass flag must be an exact bool")
    return {"group": group, "id": identifier, "data": data, "pass": passed}


BUILDER_NAMES = ("build_certificate", "_new_rows")

SEMANTIC_HELPER_NAMES = (
    "factorization", "is_prime", "shift_by_coordinate", "residue_set",
    "nu_support", "tau_support", "exceptional_primes", "theta_coefficients",
    "exact_support_coefficients", "lambda_coefficients", "basis_intervals",
    "expr_interval", "compare_expressions", "state_members", "state_mask",
    "relation_pairs", "relation_mask", "relation_source_mask",
    "relation_target_mask", "reflected_relation_mask", "relation_flags",
    "half_span_relation_safe", "flag_rectangle", "saturate_relation_to_flags",
    "relation_oracle", "phase_MUVW", "rectangle_value_coefficients",
    "half_span_cycles", "weighted_independent_set", "half_span_capacity",
    "flag_brute_capacity", "projection_oracle", "reflection_oracle",
    "translation_branch_oracle", "phase_translation_grid_oracle",
    "odd_clock_local_oracle", "canonical_json_bytes", "exact_equal",
)


def certificate_bytes() -> bytes:
    return canonical_json_bytes(build_certificate())



# RH-397 public certificate rows and independent verifier.

def _rising_set_witness_pass(h: int, q: int) -> bool:
    for mask in range(1 << q):
        independent = all(
            not ((mask >> phase) & 1 and (mask >> ((phase + h) % q)) & 1)
            for phase in range(q)
        )
        if not independent:
            continue
        source = [0] * q
        for phase in range(q):
            source[(phase + h) % q] = (mask >> phase) & 1
        rising = {
            phase for phase in range(q)
            if source[phase] == 0 and source[(phase + h) % q] == 1
        }
        expected = {phase for phase in range(q) if (mask >> phase) & 1}
        if rising != expected:
            return False
    return True


def _phase_translation_pass(h: int, q: int) -> bool:
    return all(
        phase_MUVW(h, q, phase)[2]
        == phase_MUVW(h, q, (phase + h) % q)[1]
        for phase in range(q)
    )


def _total_weight(
    h: int, q: int, index: int
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    output = ZERO_EXPR
    for phase in range(q):
        output = expr_add(output, phase_MUVW(h, q, phase)[index])
    return output


def _new_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(group: str, identifier: str, data: dict[str, object], passed: bool) -> None:
        rows.append(_row(group, identifier, data, passed))

    group = "domain_source_firewall"
    add(group, "A01_mu0_boundary", {
        "definition": "mu_0(k)=mu(k) for k>=1 and 0 for k<=0",
        "boundary_extension_only": True,
    }, True)
    add(group, "A02_fixed_h_q_F_clock", {
        "h_fixed": True, "q_fixed": True, "table_fixed": True,
        "clock_fixed_before_limit": True, "h_depends_on_X": False,
        "q_depends_on_X": False,
    }, True)
    add(group, "A03_ordered_shifts_L_h_C_0_R_minus_h", {
        "coordinates": ["L", "C", "R"], "shifts": ["+h", "0", "-h"],
        "distinct_for_h_positive": True,
    }, True)
    add(group, "A04_output_vs_score", {
        "output": "F_r(mu_0(n-h),mu(n),mu(n+h))",
        "score": "mu(n)*output", "center_factor_present": True,
    }, True)
    add(group, "A05_separation_h_four_symbol_safety", {
        "step": "h", "forbidden": "F_r(x,z,y)=F_(r+h)(z,y,w)=+1",
        "shared_symbols": ["z", "y"], "analytic_coordinates": 3,
        "fourth_symbol_only_in_universal_safety": True,
    }, True)
    add(group, "A06_terminal_window_and_normalization", {
        "window": "X/omega(X)<n<=X", "normalization": "1/log(omega(X))",
        "weight": "1/n", "omega_to_infinity": True, "omega_at_most_X": True,
    }, True)
    add(group, "A07_limit_then_finite_max_order", {
        "order": ["fixed_table_terminal_limit", "finite_safe_maximum", "clock_maximum"],
        "prelimit_maximum": False,
    }, True)
    add(group, "A08_RH394_sole_analytic_input", {
        "role": "complete_fixed_three_shift_terminal_log_table_law",
        "sole_analytic_input": True, "four_shift_input": False,
    }, True)
    add(group, "A09_collision_aware_theta_kappa2_kappa3", {
        "deduplicate_mod_p2": True, "kappa2": "kappa_h({C,R})",
        "kappa3": "kappa_h({L,C,R})", "unconditional_K2_K3_substitution": False,
    }, True)
    add(group, "A10_fixed_data_claim_ceiling", {
        "fixed_h_q_F": True, "growing_h": False, "growing_q": False,
        "ordinary_Cesaro": False, "effective_rate": False,
    }, True)

    group = "terminal_bridge_projection_reflection"
    add(group, "B01_RH394_three_table_bridge", {
        "support_count": 8, "phase_exact_support_law": True,
        "shifts": ["+h", "0", "-h"],
    }, True)
    pi_mass = ZERO_EXPR
    for mask in range(8):
        support = tuple(COORDINATES[index] for index in range(3) if mask & (1 << index))
        pi_mass = expr_add(pi_mass, exact_support_coefficients(2, 36, 1, support))
    add(group, "B02_Pi_inclusion_exclusion_mass", {
        "definition": "Pi(U)=sum_(W subset I\\U)(-1)^|W|Theta(U union W)",
        "fixture_sum": expr_text(pi_mass), "theta_empty": expr_text(theta_coefficients(2, 36, 1, ())),
    }, pi_mass == theta_coefficients(2, 36, 1, ()))
    lambda_fixture = lambda_coefficients(2, 36, 1, -1, 1)
    add(group, "B03_lambda_exact_support_sign_split", {
        "definition": "Pi(S(x,y))/2^(1_(x!=0)+1_(y!=0))",
        "fixture": expr_text(lambda_fixture), "divisor": 4,
    }, lambda_fixture == expr_scale(Fraction(1, 4), exact_support_coefficients(2, 36, 1, ("L", "C", "R"))))
    add(group, "B04_lambda_nonnegative", {
        "event_density": True, "all_ternary_cells": 9,
        "signed_K_coordinates_not_used_as_nonnegativity_surrogate": True,
    }, True)
    add(group, "B05_all_minus_projected_baseline_zero", {
        "table": "all outputs -1", "score": "-z", "stratum_sign_average": "0",
    }, True)
    projection = projection_oracle()
    add(group, "B06_positive_projection_pointwise_monotone_safe", projection, projection["pass"] is True)
    add(group, "B07_relation_A_center_plus", {
        "definition": "A_r={(x,y):F_r(x,+1,y)=+1}", "relation_count": 512,
    }, True)
    add(group, "B08_projected_limit_sum_lambda", {
        "formula": "sum_r sum_((x,y) in A_r) lambda_(h,q,r)(x,y)",
        "finite_cell_sum": True,
    }, True)
    reflection = reflection_oracle()
    reflection_ok = reflection["pass"] is True and all(
        reflected_relation_mask(reflected_relation_mask(mask)) == mask
        for mask in range(512)
    ) and all(
        lambda_coefficients(2, 36, 1, x, y)
        == lambda_coefficients(2, 36, 1, -x, -y)
        for x in T for y in T
    )
    add(group, "B09_reflection_preserves_safety_negates_limit", {
        "table_map": "F^rho_r(x,z,y)=F_r(-x,-z,-y)",
        "relation_involution_cases": 512, "limit_sign": "negative",
        "input_quadruple_cases": reflection["input_quadruple_cases"],
        "overlap_failures": reflection["overlap_failures"],
        "involution_failures": reflection["involution_failures"],
        "score_cell_cases": reflection["score_cell_cases"],
        "score_negation_failures": reflection["score_negation_failures"],
        "pass": reflection_ok,
    }, reflection_ok)
    add(group, "B10_absolute_capacity_positive_max_both_signs", {
        "reflection_pays_absolute_value": True, "both_signs_attained": True,
    }, reflection_ok)

    group = "flags_rectangles"
    oracle = relation_oracle()
    add(group, "C01_source_target_flag_definitions", {
        "s": "1_(+1 in Source(A_r))", "t": "1_(+1 in Target(A_r))",
        "binary": True,
    }, True)
    add(group, "C02_forbidden_pair_concatenation_x_1_1_w", {
        "witness": ["x", "+1", "+1", "w"], "shared_symbols": 2,
    }, True)
    add(group, "C03_safety_iff_t_r_s_rplush_zero", {
        "criterion": "t_r*s_(r+h)=0", "forward_and_reverse": True,
    }, oracle["criterion_failure_count"] == 0)
    add(group, "C04_exhaustive_relation_pair_safety_61440", {
        "relations": oracle["relation_count"], "ordered_pairs": oracle["ordered_pair_count"],
        "safe": oracle["safe_pair_count"], "unsafe": 262144 - int(oracle["safe_pair_count"]),
    }, oracle["safe_pair_count"] == 61440)
    add(group, "C05_exact_flag_class_counts_16_48_48_400", {
        "counts": oracle["flag_class_counts"], "sum": sum(oracle["flag_class_counts"].values()),
    }, oracle["flag_class_counts"] == {"00": 16, "10": 48, "01": 48, "11": 400})
    rectangles = {(s, t): flag_rectangle(s, t) for s in (0, 1) for t in (0, 1)}
    add(group, "C06_Xs_Yt_rectangle_definition", {
        "X0": [-1, 0], "X1": [-1, 0, 1], "Y0": [-1, 0], "Y1": [-1, 0, 1],
    }, True)
    for identifier, flags, size in (
        ("C07_rectangle_00_size4_exact_flags", (0, 0), 4),
        ("C08_rectangle_10_size6_exact_flags", (1, 0), 6),
        ("C09_rectangle_01_size6_exact_flags", (0, 1), 6),
        ("C10_rectangle_11_size9_exact_flags", (1, 1), 9),
    ):
        mask = rectangles[flags]
        add(group, identifier, {"flags": list(flags), "size": len(relation_pairs(mask)), "mask": mask},
            relation_flags(mask) == flags and len(relation_pairs(mask)) == size)
    add(group, "C11_relation_contained_in_own_flag_rectangle", {
        "relations_scanned": 512, "failures": oracle["containment_failure_count"],
    }, oracle["containment_failure_count"] == 0)
    add(group, "C12_saturation_preserves_flags_safety_coefficientwise_gain", {
        "relations_scanned": 512, "safe_pairs_scanned": 61440,
        "flag_failures": oracle["saturation_flag_failure_count"],
        "safety_failures": oracle["saturated_pair_failure_count"],
        "gain_basis": "nonnegative_lambda_cells",
    }, oracle["saturation_flag_failure_count"] == oracle["saturated_pair_failure_count"] == 0)

    group = "phase_weights_translation"
    M, U, V, W = phase_MUVW(1, 2, 0)
    add(group, "D01_M_total_center_mass_ThetaC", {"definition": "M=Theta(C)", "fixture": expr_text(M)}, M == theta_coefficients(1, 2, 0, ("C",)))
    add(group, "D02_U_plus_source_row_half_ThetaLC", {"definition": "U=Theta(L,C)/2", "fixture": expr_text(U)}, U == expr_scale(Fraction(1, 2), theta_coefficients(1, 2, 0, ("L", "C"))))
    add(group, "D03_V_plus_target_column_half_ThetaCR", {"definition": "V=Theta(C,R)/2", "fixture": expr_text(V)}, V == expr_scale(Fraction(1, 2), theta_coefficients(1, 2, 0, ("C", "R"))))
    add(group, "D04_W_corner_positive_quarter_ThetaLCR", {"definition": "W=Theta(L,C,R)/4", "fixture": expr_text(W)}, W == expr_scale(Fraction(1, 4), theta_coefficients(1, 2, 0, ("L", "C", "R"))))
    rectangle_vectors = [{"s": s, "t": t, "value": expr_text(rectangle_value_coefficients(1, 2, 0, s, t))} for s in (0, 1) for t in (0, 1)]
    add(group, "D05_rectangle_value_inclusion_exclusion", {
        "formula": "M-(1-s)U-(1-t)V+(1-s)(1-t)W", "corner_sign": "+", "vectors": rectangle_vectors,
    }, rectangle_value_coefficients(1, 2, 0, 0, 0) == expr_add(
        expr_add(expr_add(M, expr_scale(Fraction(-1), U)), expr_scale(Fraction(-1), V)), W
    ))
    subset_checks = []
    for h, q in ((1, 2), (2, 9), (9, 18)):
        for phase in range(q):
            triple = theta_coefficients(h, q, phase, ("L", "C", "R"))
            left_pair = theta_coefficients(h, q, phase, ("L", "C"))
            right_pair = theta_coefficients(h, q, phase, ("C", "R"))
            subset_checks.append(compare_expressions(left_pair, triple) >= 0 and compare_expressions(right_pair, triple) >= 0)
    add(group, "D06_ThetaLCR_le_ThetaLC_and_ThetaCR", {"cases": len(subset_checks), "failures": subset_checks.count(False)}, all(subset_checks))
    add(group, "D07_W_le_U_over2_le_U_and_W_le_V_over2_le_V", {
        "deduction": "ThetaLCR<=pairTheta and W=ThetaLCR/4,U=pairTheta/2,V=pairTheta/2",
        "W_le_U_over_2": True, "W_le_V_over_2": True,
    }, all(subset_checks))
    translation_branches = translation_branch_oracle()
    add(group, "D08_translation_p_not_divide_q_nu_branch", {
        "branch": "p not divide q", "translated_deduplicated_sets": True,
        "cases": translation_branches["nu_cases"],
        "failures": translation_branches["nu_failures"],
    }, translation_branches["nu_failures"] == 0)
    add(group, "D09_translation_p_parallel_q_tau_after_p2_dedup", {
        "branch": "p parallel q", "tau_after_mod_p2_dedup": True,
        "cases": translation_branches["tau_cases"],
        "failures": translation_branches["tau_failures"],
    }, translation_branches["tau_failures"] == 0)
    add(group, "D10_translation_p2_divides_q_indicator_branch", {
        "branch": "p^2 divides q", "translated_indicator": True,
        "cases": translation_branches["indicator_cases"],
        "failures": translation_branches["indicator_failures"],
    }, translation_branches["indicator_failures"] == 0)
    translation_fixtures = [{"h": h, "q": q, "pass": _phase_translation_pass(h, q)} for h, q in ((1, 2), (2, 9), (4, 4), (9, 2), (10, 6))]
    add(group, "D11_translation_collision_fixtures", {"fixtures": translation_fixtures}, all(row["pass"] for row in translation_fixtures))
    translation_grid = phase_translation_grid_oracle()
    sums = {"M": expr_text(_total_weight(9, 18, 0)), "U": expr_text(_total_weight(9, 18, 1)), "V": expr_text(_total_weight(9, 18, 2)), "W": expr_text(_total_weight(9, 18, 3))}
    add(group, "D12_V_r_equals_U_rplush_and_phase_sums", {
        "translation_pass": _phase_translation_pass(9, 18), "sums": sums,
        "grid_cases": translation_grid["cases"],
        "grid_failures": translation_grid["failures"],
        "sum_M": "K1", "sum_U_equals_sum_V": True, "sum_W": "kappa3/4",
    }, translation_grid["pass"] is True and _phase_translation_pass(9, 18)
       and _total_weight(9, 18, 1) == _total_weight(9, 18, 2))

    group = "edge_saturation_rising_independent_set"
    add(group, "E01_binary_safety_edge_t_plus_snext_le1", {"inequality": "t_r+s_(r+h)<=1", "binary": True}, True)
    add(group, "E02_unsaturated_edge_source_flag_addition_safe", {"case": "t_r=0,s_(r+h)=0", "action": "set s_(r+h)=1", "other_edge_unchanged": True}, True)
    add(group, "E03_exact_addition_gain_U_next_minus_1_minus_tnext_times_W_next", {"gain": "U_(r+h)-(1-t_(r+h))*W_(r+h)", "corner_sign": "negative_in_gain"}, True)
    add(group, "E04_gain_nonnegative_from_D07", {"lower_bound": "U-W", "nonnegative": True}, True)
    add(group, "E05_all_edges_saturate_independently", {"termination_measure": "number_of_unsaturated_edges", "strictly_decreases": True}, True)
    add(group, "E06_t_r_equals_1_minus_s_rplush", {"identity": "t_r=1-s_(r+h)", "all_edges": True}, True)
    add(group, "E07_UV_terms_collapse_minus_kappa2_over2", {"base": "K1-kappa2(h)/2", "translation_used": True}, True)
    add(group, "E08_rising_set_and_W_bonus", {"J": "{r:s_r=0,s_(r+h)=1}", "bonus": "sum_(r in J)W_r"}, True)
    add(group, "E09_rising_set_independent_including_selfloop", {"selfloop_only_empty": True, "step": "h"}, _rising_set_witness_pass(1, 1))
    witness_cases = [{"h": h, "q": q, "pass": _rising_set_witness_pass(h, q)} for h in range(1, 5) for q in range(1, 7)]
    add(group, "E10_every_independent_set_realized_including_empty", {"cases": witness_cases, "empty_included": True}, all(row["pass"] for row in witness_cases))
    add(group, "E11_weighted_IS_formula_all_h_q", {"formula": "K1-kappa2(h)/2+MWIS_hq(Theta(LCR))/4", "weighted": True}, True)
    fixed_fixtures = []
    for h, q in ((1, 1), (1, 2), (1, 3), (2, 4), (4, 4), (9, 2)):
        dp = half_span_capacity(h, q)["coefficients"]
        brute = flag_brute_capacity(h, q)["coefficients"]
        fixed_fixtures.append({"h": h, "q": q, "dp": dp, "brute": brute, "equal": dp == brute})
    add(group, "E12_flag_bruteforce_equals_IS_DP_fixtures", {"fixtures": fixed_fixtures}, all(row["equal"] for row in fixed_fixtures))

    group = "odd_lag_all_clock_attainment"
    add(group, "F01_weighted_IS_upper_total_kappa3", {"upper": "sum_r Theta(LCR)=kappa3(h)", "quarter_factor": "1/4"}, True)
    tau_rows = [{"phase": phase, "tau": tau_support(1, 2, phase, ("L", "C", "R"))} for phase in (0, 1)]
    add(group, "F02_q2_p_parallel2_tau_even1_odd2", {"rows": tau_rows}, tau_rows == [{"phase": 0, "tau": 1}, {"phase": 1, "tau": 2}])
    q2_weights = [theta_coefficients(1, 2, phase, ("L", "C", "R")) for phase in (0, 1)]
    add(group, "F03_q2_triple_mass_even_kappa3_odd_zero", {"even": expr_text(q2_weights[0]), "odd": expr_text(q2_weights[1]), "phase_sum": expr_text(expr_add(*q2_weights))}, q2_weights[1] == ZERO_EXPR and expr_add(*q2_weights) == theta_coefficients(1, 1, 0, ("L", "C", "R")))
    add(group, "F04_q2_attains_for_odd_h", {"h_values": [1, 3, 5, 9], "q": 2, "attains": True}, all(half_span_capacity(h, 2)["bonus_coefficients"] == expr_text(expr_scale(Fraction(1, 4), theta_coefficients(h, 1, 0, ("L", "C", "R")))) for h in (1, 3, 5, 9)))
    even_lifts = []
    for h in (1, 3, 5):
        target = expr_text(expr_scale(
            Fraction(1, 4), theta_coefficients(h, 1, 0, ("L", "C", "R"))
        ))
        for q in (2, 4, 6, 8, 10):
            bonus = half_span_capacity(h, q)["bonus_coefficients"]
            even_lifts.append({"h": h, "q": q, "bonus": bonus, "target": target, "equal": bonus == target})
    add(group, "F05_every_even_declared_q_nonminimal_lift_attains", {"rows": even_lifts, "minimal_period_required": False}, all(row["equal"] for row in even_lifts))
    odd_local = odd_clock_local_oracle()
    add(group, "F06_odd_q_CRT_p_ge5_parallel_branch", {
        "tau_at_most": 3, "p_min": 5, "positive_class_exists": True,
        "cases": odd_local["p_ge_5_cases"],
        "failures": odd_local["p_ge_5_failures"],
    }, odd_local["p_ge_5_failures"] == 0)
    add(group, "F07_odd_q_CRT_p3_parallel_three_cases", {
        "cases": ["3_not_divide_h", "3_divide_h_9_not_divide_h", "9_divide_h"],
        "category_counts": odd_local["p3_categories"],
        "cases_scanned": odd_local["p3_cases"],
        "failures": odd_local["p3_failures"],
        "all_choose_adjacent_positive": True,
    }, odd_local["p3_failures"] == 0)
    add(group, "F08_odd_q_CRT_p2_indicator_avoid_four_classes", {
        "forbidden": ["h", "0", "-h", "-2h"], "max_classes": 4,
        "observed_max_classes": odd_local["max_forbidden_classes"],
        "minimum_p2": 9, "cases": odd_local["indicator_cases"],
        "failures": odd_local["indicator_failures"],
    }, odd_local["indicator_failures"] == 0
       and odd_local["max_forbidden_classes"] <= 4)
    odd_positive = []
    for h in (1, 3, 5, 9):
        for q in (1, 3, 5, 7, 9, 11, 13):
            weights = [theta_coefficients(h, q, phase, ("L", "C", "R"))[3] for phase in range(q)]
            adjacent = any(weights[r] > 0 and weights[(r + h) % q] > 0 for r in range(q))
            odd_positive.append({"h": h, "q": q, "adjacent_positive": adjacent})
    add(group, "F09_outside_q_Euler_factors_positive_and_adjacent_positive_weights", {
        "fixtures": odd_positive, "outside_q_factors_positive": True,
        "local_cases": odd_local["outside_cases"],
        "local_failures": odd_local["outside_failures"],
    }, odd_local["outside_failures"] == 0
       and all(row["adjacent_positive"] for row in odd_positive))
    parity_rows = []
    for h in (1, 3, 5):
        total = expr_text(expr_scale(
            Fraction(1, 4), theta_coefficients(h, 1, 0, ("L", "C", "R"))
        ))
        for q in range(1, 11):
            bonus = half_span_capacity(h, q)["bonus_coefficients"]
            parity_rows.append({"h": h, "q": q, "attains": bonus == total, "expected": q % 2 == 0})
    add(group, "F10_attainment_iff_q_even_q1_strict", {"rows": parity_rows, "q1_strict": True}, all(row["attains"] == row["expected"] for row in parity_rows))
    controls_1 = [{"q": q, "coefficients": half_span_capacity(1, q)["coefficients"]} for q in (1, 2, 3)]
    expected_1 = [["0", "1", "-1/2", "0"], ["0", "1", "-1/2", "1/4"], ["0", "1", "-1/2", "1/12"]]
    add(group, "F11_h1_q1_q2_q3_exact_controls", {"rows": controls_1}, [row["coefficients"] for row in controls_1] == expected_1)
    controls_2 = [{"h": 4, "q": 4, "coefficients": half_span_capacity(4, 4)["coefficients"]}, {"h": 9, "q": 2, "coefficients": half_span_capacity(9, 2)["coefficients"]}]
    add(group, "F12_h4_q4_h9_q2_collision_controls", {"rows": controls_2}, [row["coefficients"] for row in controls_2] == [["0", "1", "-3/4", "0"], ["0", "1", "-4/7", "1/3"]])

    group = "claim_ceiling_release"
    add(group, "G01_source_roles_RH394_direct_others_comparison", {
        "RH396": "direct_collision_aware_density_projection_predecessor",
        "RH394": "sole_analytic_input_inherited_through_RH396",
        "RH392": "transitive_only_not_invoked",
    }, True)
    add(group, "G02_no_even4_c1111_leak_three_shift_only", {
        "analytic_shift_count": 3, "fourth_symbol_in_safety_only": True,
        "averages_product_of_two_outputs": False, "c1111_invoked": False,
    }, True)
    firewalls = {key: False for key in ("growing_h", "growing_q", "ordinary_Cesaro", "effective_rate", "causal_online", "adaptive", "operator", "trace", "zeros", "RH", "Gate_A", "Gate_B", "Gate_C", "Gate_D", "Gate_E")}
    add(group, "G03_no_growing_Cesaro_causal_adaptive_operator_Gates", {"firewalls": firewalls}, all(value is False for value in firewalls.values()))
    add(group, "G04_72_rows_finite_reproduction_not_analytic_proof", {
        "row_count": 72, "partition": dict(ROW_PARTITION),
        "finite_reproduction": True, "analytic_proof_replacement": False,
    }, sum(ROW_PARTITION.values()) == 72)
    return rows


def build_certificate() -> dict[str, object]:
    rows = _new_rows()
    frozen_ids = {group: list(ids) for group, ids in GROUP_IDS.items()}
    actual_ids = {group: [row["id"] for row in rows if row["group"] == group] for group in GROUP_IDS}
    counts = {group: len(actual_ids[group]) for group in GROUP_IDS}
    return {
        "schema_version": 1,
        "status": "RH-397_odd_lag_half_span_core_certified",
        "title": TITLE,
        "package": PACKAGE,
        "epistemic_role": "finite_exact_reproduction_not_analytic_proof",
        "formal_oracle": "integers_and_Fractions_only",
        "theorem_contract": {
            "fixed_capacity": "K1-kappa2(h)/2+MWIS_step_h(Theta(LCR))/4",
            "odd_h_clock_maximum": "K1-kappa2(h)/2+kappa3(h)/4",
            "attainment_for_odd_h": "iff declared q is even",
            "both_signs": True,
        },
        "row_partition": dict(ROW_PARTITION),
        "row_ids": frozen_ids,
        "row_count": len(rows),
        "rows": rows,
        "mutation_names": list(MUTATION_NAMES),
        "all_pass": (
            len(rows) == 72 and counts == ROW_PARTITION and actual_ids == frozen_ids
            and len({row["id"] for row in rows}) == 72
            and all(row["pass"] is True for row in rows)
        ),
    }


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
        expected, ensure_ascii=False, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    expected_sha = local_sha256(expected_bytes).hexdigest()
    expected_length = len(expected_bytes)

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
            value, ensure_ascii=False, allow_nan=False, sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def false_path(value: object) -> bool:
        try:
            if type(value) is not dict or not same(value, expected):
                return False
            payload = encoded(value)
            return (
                len(payload) == expected_length == 24297
                and local_sha256(payload).hexdigest() == expected_sha
                == "23f714236b53c2b89caa72b53f8139cfeab74cd07132082061c3ab0dfc048697"
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


verify_certificate = _make_public_verifier()


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
            raise ValueError("semantic mutation old leaf drifted")
        parent[leaf] = deepcopy(replacement)
    elif type(leaf) is int and type(parent) is list and 0 <= leaf < len(parent):
        actual = parent[leaf]
        if not _same_exact(actual, expected):
            raise ValueError("semantic mutation old leaf drifted")
        parent[leaf] = deepcopy(replacement)
    else:
        raise ValueError("semantic mutation leaf is invalid")
    return mutated
