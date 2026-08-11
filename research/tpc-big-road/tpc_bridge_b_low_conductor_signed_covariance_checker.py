#!/usr/bin/env python3
"""Fail-closed finite checker for the V48 conductor--Euler scalar splice."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever the frozen V48 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "EXACT_GCD_REDUCTION_IDENTIFIES_V45_AND_V46_AS_TWO_DECOMPOSITIONS_OF_"
    "ONE_TRANSITION_SCALAR_AND_REPLACES_V47_FULL_CENTERED_ENERGY_BY_ONE_"
    "LOW_CONDUCTOR_SIGNED_PRIME_HYBRID_GATE_WITH_PAID_SPLICE"
)


REGISTRY = (
    "V48_MAXIMUM_CLAIM = EXACT_GCD_REDUCTION_IDENTIFIES_V45_AND_V46_AS_TWO_DECOMPOSITIONS_OF_ONE_TRANSITION_SCALAR_AND_REPLACES_V47_FULL_CENTERED_ENERGY_BY_ONE_LOW_CONDUCTOR_SIGNED_PRIME_HYBRID_GATE_WITH_PAID_SPLICE",
    "V48_ROUTE_ADVANCE = YES",
    "V48_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V48_ARITHMETIC_ADVANCE = NO",
    "V48_FIXED_ATOM_CREDIT = 0",
    "V48_STRICT_1_OVER_400 = UNPAID",
    "V48_L2 = NONE",
    "V48_TPC_207_TRIGGER = false",
    "V48_NUMBERED_RELEASE = NO",
    "V48_DERIVATION_STATUS = COHERENT_AFTER_EXACT_GCD_REDUCTION_SCALAR_SPLICE_LOW_PRIMITIVE_BLOCK_AND_GCD_STRATUM_ANOVA",
    "V48_ASSUMPTION_POLICY = DIRECT_LOW_SCALAR_IS_PRIMARY_OPEN_GATE_AND_DELTA_GREATER_THAN_1_OVER_200_SIGNED_CHARACTER_ENERGY_IS_A_STRONGER_EXPLICIT_HEURISTIC_THEOREM",
    "V48_SELECTED_RESEARCH_ROUTE = DIRECT_LOW_CONDUCTOR_SIGNED_SCALAR_FIRST__SIGNED_CHARACTER_ENERGY_SECOND__PRINCIPAL_AND_EXCEPTIONAL_ROWS_RETAINED__LONG_MOBIUS_NEXT__V42_GATE_B_PARALLEL__V43_A_B_JOIN__C_RESERVE",
    "V48_V45_COMMON_TRANSITION = RETAINED_EXACT_BEFORE_FIRST_OUTER_ABSOLUTE",
    "V48_V46_COMMON_TRANSITION = RETAINED_EXACT_BEFORE_FIRST_OUTER_ABSOLUTE",
    "V48_V47_ADDITIVE_ZERO_MODE = RETAINED_PROVED_EXACT_EMPTY",
    "V48_GCD_REDUCTION = PROVED_EXACT_D_EQUALS_G_S_AND_M_EQUALS_G_N",
    "V48_SQUAREFREE_GCD_COPRIMALITY = PROVED_EXACT_G_COPRIME_S_AND_N_COPRIME_S",
    "V48_REDUCED_PHASE = PROVED_EXACT_E_D_M_U_QBAR_EQUALS_E_S_N_U_QBAR",
    "V48_REDUCED_CUTOFF = PROVED_EXACT_H_M_OVER_D_Q_EQUALS_H_N_OVER_S_Q",
    "V48_LAMBDA_AGGREGATION = PROVED_EXACT_NEGATIVE_SUM_OVER_G_OF_MU_GS_LOG_GS_OVER_GS",
    "V48_COMMON_SCALAR_CROSSWALK = PROVED_EXACT_V45_REDUCED_OBJECT_EQUALS_V46_ORIGINAL_PROPER_FACTOR_OBJECT",
    "V48_SCALAR_SPLICE = PROVED_EXACT_R_AP_EQUALS_M_LOW_PLUS_V_HIGH_MINUS_L_PF",
    "V48_PAID_SPLICE_REMAINDER = DEFINED_E_SPLICE_EQUALS_V_HIGH_MINUS_L_PF",
    "V48_V45_HIGH_CONDUCTOR_PAYMENT = RETAINED_SOURCE_BACKED_X_POWER_213_OVER_128",
    "V48_V46_LOCAL_EULER_PAYMENT = RETAINED_SOURCE_BACKED_X_POWER_1057_OVER_640",
    "V48_SPLICE_REMAINDER_BOUND = PROVED_X_POWER_213_OVER_128_PLUS_O1",
    "V48_SPLICE_ENDPOINT_MARGIN = 1_OVER_9600",
    "V48_NO_DOUBLE_COUNTING = PROVED_USE_SIGNED_SCALAR_IDENTITY_BEFORE_OUTER_ABSOLUTE",
    "V48_ENERGY_SUBTRACTION = STOP_SCOPED_GCD_AGGREGATION_AND_SQUARING_DO_NOT_COMMUTE",
    "V48_V45_HIGH_AS_V47_ORTHOGONAL_PROJECTION = STOP_SCOPED_FALSE_TWO_FIBER_CANCELLATION",
    "V48_LOW_PRIMITIVE_BLOCK = PROVED_EXACT_GAUSS_RAMANUJAN_CHARACTER_FORM",
    "V48_LOW_PHYSICAL_BLOCK = PROVED_EXACT_LAMBDA_U_PLUS_2_MINUS_B_Z_TIMES_CHIBAR_U_C_E_U_OVER_LOG_U",
    "V48_SIGNED_PRIME_HYBRID_SPLIT = PROVED_EXACT_W_EQUALS_W_LAMBDA_MINUS_W_B",
    "V48_LOW_PRINCIPAL_ROW = RETAINED_INSIDE_C_EQUALS_1",
    "V48_LOW_INDUCED_ROWS = RETAINED_ALL_1_LT_C_LT_D0",
    "V48_LOW_EXCEPTIONAL_FIREWALL = RETAIN_POSSIBLE_REAL_EXCEPTIONAL_ROW_NO_POWER_BORROWED",
    "V48_LOW_COEFFICIENT_ENERGY = RETAINED_PROVED_P_SQUARED_X_O1",
    "V48_LOW_COEFFICIENT_ENERGY_EXPONENT = 1_OVER_48",
    "V48_LOW_SIGNED_PHYSICAL_ENERGY = DEFINED_CHARACTER_PARSEVAL_TOWER_W_LOW",
    "V48_LOW_SIGNED_PHYSICAL_ENERGY_CEILING = X_POWER_2_PLUS_O1",
    "V48_LOW_TRIVIAL_SCALAR_OUTPUT = X_POWER_5_OVER_3_PLUS_O1",
    "V48_LOW_TRIVIAL_ENDPOINT_DEFICIT = 1_OVER_400",
    "V48_LOW_SIGNED_CHARACTER_ENERGY_GATE = OPEN_X_POWER_2_MINUS_DELTA_WITH_DELTA_GREATER_THAN_1_OVER_200",
    "V48_LOW_SIGNED_CHARACTER_ENERGY_THRESHOLD = DELTA_GREATER_THAN_1_OVER_200_STRICT",
    "V48_LOW_SIGNED_CHARACTER_ENERGY_OUTPUT = CONDITIONAL_X_POWER_5_OVER_3_MINUS_DELTA_OVER_2_PLUS_O1",
    "V48_LOW_SIGNED_CHARACTER_ENERGY_MARGIN = DELTA_OVER_2_MINUS_1_OVER_400",
    "V48_DIRECT_LOW_SCALAR_GATE = OPEN_X_POWER_1997_OVER_1200_MINUS_ETA_LOW_WITH_ETA_LOW_POSITIVE",
    "V48_CHARACTER_ENERGY_COMPILER = PROVED_SUFFICIENT_FOR_DIRECT_LOW_SCALAR_GATE",
    "V48_DIRECT_SCALAR_STRENGTH = SELECTED_WEAKER_THAN_FULL_SIGNED_CHARACTER_ENERGY",
    "V48_V47_CENTERED_GATE_TO_LOW_SCALAR = PROVED_CONDITIONAL_VIA_PAID_SPLICE",
    "V48_LOW_SCALAR_TO_V47_RESIDUAL = PROVED_CONDITIONAL_VIA_PAID_SPLICE",
    "V48_TRANSITION_CONDITIONAL_COMPILER = PROVED_LOW_SCALAR_GATE_PAYS_FULL_TRANSITION_WITH_HIGH_SPECTRUM_AND_CORRECTIONS",
    "V48_TRANSITION_CONDITIONAL_MARGIN = MIN_ETA_LOW_1_OVER_9600_13_OVER_4800_817_OVER_4800",
    "V48_GCD_STRATUM_ANOVA = PROVED_EXACT_WITHIN_NONPRINCIPAL_PLUS_BETWEEN_PRINCIPAL_ENERGY",
    "V48_GLOBAL_CENTERING_CONSTRAINT = PROVED_ONLY_WEIGHTED_SUM_OF_STRATUM_MEANS_EQUALS_ZERO",
    "V48_STRATUM_PRINCIPAL_SURVIVAL = PROVED_EXACT_GLOBAL_CENTERING_DOES_NOT_DELETE_EACH_STRATUM_MEAN",
    "V48_ANOVA_VERSUS_GCD_AGGREGATION = PROVED_DISTINCT_WITHIN_D_AND_CROSS_D_OPERATIONS",
    "V48_LONG_BALANCED_WINDOW = OPEN_D_GT_U_AND_K_GT_U",
    "V48_LONG_REVERSE_TYPE_I_WINDOW = OPEN_D_GT_U_AND_K_LE_U",
    "V48_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE",
    "V48_BFI_HIGH_CONDUCTOR = SOURCE_BACKED_RETAINED",
    "V48_BFI_LOW_CONDUCTOR_TO_FIXED_POWER = STOP_SCOPED_SIEGEL_WALFISZ_LOG_SAVING_DOES_NOT_PAY_1_OVER_400",
    "V48_CIS_ASYMPTOTIC_LARGE_SIEVE = STOP_SCOPED_WRONG_PHYSICAL_SIGNED_COEFFICIENT_CLASS",
    "V48_PRODUCTS_OF_PRIMES_DENSE_MODEL = STOP_SCOPED_TERNARY_PRODUCT_AND_BURGESS_INTERFACE_WRONG_OBJECT",
    "V48_RUNBO_LI_AP_MEAN_VALUE = STOP_SCOPED_SEPARATE_MAJORANT_MINORANT_AND_AVERAGED_RESIDUE_DO_NOT_PROVE_LITERAL_SIGNED_CHARACTER_ENERGY",
    "V48_JOHNSTON_EFFECTIVE_BV = STOP_SCOPED_EFFECTIVITY_DOES_NOT_STRENGTHEN_TO_FIXED_POWER_LITERAL_SIGNED_GATE",
    "V48_DIRECT_PRIMARY_SOURCE_FOR_LOW_SIGNED_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11",
    "V48_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_LOW_CONDUCTOR_SIGNED_PRIME_HYBRID_CHARACTER_RAMANUJAN_ENERGY_WITH_DELTA_GREATER_THAN_1_OVER_200_OR_THE_DIRECT_LOW_SCALAR_FIXED_POWER",
    "V48_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_HIGH_CONDUCTOR_AND_LOCAL_EULER_PAID_EXACT_SCALAR_SPLICE_DONE_LOW_CONDUCTOR_SIGNED_GATE_OPEN_LONG_MOBIUS_SPAN_OPEN",
    "V48_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED",
    "V48_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B",
)


REGISTRY_SHA256 = "718afd7a21374c93246057049d4c81741fa2ed1badd2bfad3b66bb3784c15738"


SOURCE_LOCKS = (
    ("BFI-large-moduli", "Bombieri; Friedlander; Iwaniec", "high-conductor primitive large sieve only; low conductor is logarithmic Siegel--Walfisz"),
    ("1105.1176", "Brian Conrey; Henryk Iwaniec; Kannan Soundararajan", "primitive asymptotic large sieve, not the literal signed physical block"),
    ("2301.07679", "Kaisa Matomaki; Joni Teravainen", "ternary products and dense model with possible quadratic obstruction"),
    ("2602.20917v6", "Runbo Li", "separate prime majorants/minorants and averaged AP distribution, not signed character energy"),
    ("2510.10853v2", "Daniel R. Johnston", "effectivity of classical BV sifting errors, not a stronger fixed-power norm"),
)


DEPENDENCIES = (
    ("research/tpc-big-road/bridge_b_low_conductor_signed_covariance_splice.md", "5b35d2fc4fcb6d66628f704df3d22b39fa76b0fb524fdb30062c309f0485b6c5"),
    ("research/tpc-big-road/bridge_b_centered_ap_covariance_and_prime_hybrid_atlas.md", "5501dffe68adbefc8d53021ca2539cd2a8934128f08205a97cea973597682d7f"),
    ("research/tpc-big-road/tpc_bridge_b_centered_ap_covariance_checker.py", "b47b72fd8fcb7ea1da177ebcb0b915c74ad7d0efbf9b7a21e58bb0dd1ec93543"),
    ("research/tpc-big-road/bridge_b_transition_native_euler_bdh_compiler.md", "f834c13f689b8283c40bd962b0ec4fa5cdcaaee061eca1914a6356a1cfd96011"),
    ("research/tpc-big-road/tpc_bridge_b_transition_native_euler_bdh_checker.py", "e679064886b4cc7ada2e63f75605bbcff7b5ade6eb6af7f1af8b6c46a64ddcc8"),
    ("research/tpc-big-road/bridge_b_conductor_stratified_transition_spectrum.md", "0a797eb4e3791319624fb5dd7a597d6d6bb217b46759739a51854312df6f4ec9"),
    ("research/tpc-big-road/tpc_bridge_b_conductor_stratified_transition_checker.py", "6b726a75674587ce9ec8450f4b462b90d685ac267519f68c732b8794962b51b6"),
)


def _make_trusted_runner(
    *,
    registry_seed=REGISTRY,
    source_seed=SOURCE_LOCKS,
    dependency_seed=DEPENDENCIES,
    registry_digest_seed=REGISTRY_SHA256,
    maximum_claim_seed=MAXIMUM_CLAIM,
    fraction_type=Fraction,
    path_type=Path,
    sha256_fn=hashlib.sha256,
    dict_type=dict,
    tuple_type=tuple,
    list_type=list,
    str_type=str,
    int_type=int,
    bool_type=bool,
    type_fn=type,
    len_fn=len,
    all_fn=all,
    zip_fn=zip,
    set_type=set,
    range_fn=range,
    enumerate_fn=enumerate,
    sum_fn=sum,
    abs_fn=abs,
    pow_fn=pow,
    min_fn=min,
    max_fn=max,
    hash_fn=hash,
    file_seed=__file__,
):
    literal_maximum_claim = (
        "EXACT_GCD_REDUCTION_IDENTIFIES_V45_AND_V46_AS_TWO_DECOMPOSITIONS_OF_"
        "ONE_TRANSITION_SCALAR_AND_REPLACES_V47_FULL_CENTERED_ENERGY_BY_ONE_"
        "LOW_CONDUCTOR_SIGNED_PRIME_HYBRID_GATE_WITH_PAID_SPLICE"
    )
    literal_registry_digest = "718afd7a21374c93246057049d4c81741fa2ed1badd2bfad3b66bb3784c15738"
    literal_registry = tuple_type(registry_seed)
    literal_sources = tuple_type(source_seed)
    literal_dependencies = tuple_type(dependency_seed)
    repo_root = path_type(file_seed).resolve().parents[2]
    path_is_file = path_type.is_file
    path_read_bytes = path_type.read_bytes
    mutation_labels = []

    if maximum_claim_seed != literal_maximum_claim:
        raise CheckFailure("maximum-claim seed changed")
    if registry_digest_seed != literal_registry_digest:
        raise CheckFailure("registry digest seed changed")

    def canonical_digest(rows):
        return sha256_fn(("\n".join(rows) + "\n").encode("utf-8")).hexdigest()

    if canonical_digest(literal_registry) != literal_registry_digest:
        raise CheckFailure("registry literal digest changed")

    def same_exact(got, want):
        if type_fn(got) is not type_fn(want):
            return False
        if type_fn(want) is tuple_type:
            return len_fn(got) == len_fn(want) and all_fn(
                same_exact(g, w) for g, w in zip_fn(got, want)
            )
        if type_fn(want) is dict_type:
            if not all_fn(type_fn(k) is str_type for k in got):
                return False
            if set_type(got) != set_type(want):
                return False
            return all_fn(same_exact(got[k], want[k]) for k in want)
        return got == want

    def validate_registry(candidate):
        if type_fn(candidate) is not tuple_type:
            raise CheckFailure("registry container type changed")
        if not all_fn(type_fn(row) is str_type for row in candidate):
            raise CheckFailure("registry row type changed")
        if candidate != literal_registry:
            raise CheckFailure("registry values changed")
        if canonical_digest(candidate) != literal_registry_digest:
            raise CheckFailure("registry digest changed")

    def validate_sources(candidate):
        if not same_exact(candidate, literal_sources):
            raise CheckFailure("source lock changed")

    def canonical_file_hash(path):
        if not path_is_file(path):
            raise CheckFailure("dependency path missing")
        return sha256_fn(path_read_bytes(path).replace(b"\r\n", b"\n")).hexdigest()

    def validate_dependencies(candidate):
        if not same_exact(candidate, literal_dependencies):
            raise CheckFailure("dependency lock changed")
        for relative, expected_hash in candidate:
            if canonical_file_hash(repo_root / relative) != expected_hash:
                raise CheckFailure("dependency hash changed: " + relative)

    def gcd(a, b):
        a = abs_fn(a)
        b = abs_fn(b)
        while b:
            a, b = b, a % b
        return a

    def finite_fixtures():
        phase_rows = 0
        phase_checks = 0
        for d in (6, 10, 15, 30):
            q = 7
            inverse_d = pow_fn(q, -1, d)
            for m in range_fn(-d + 1, d):
                if m == 0:
                    continue
                g = gcd(m, d)
                s = d // g
                n = m // g
                if gcd(g, s) != 1 or gcd(n, s) != 1:
                    raise CheckFailure("square-free gcd reduction changed")
                if fraction_type(m, d * q) != fraction_type(n, s * q):
                    raise CheckFailure("smooth cutoff reduction changed")
                inverse_s = pow_fn(q, -1, s)
                for u in range_fn(d):
                    lhs = fraction_type(m * u * inverse_d, d)
                    rhs = fraction_type(n * u * inverse_s, s)
                    if (lhs - rhs).denominator != 1:
                        raise CheckFailure("phase reduction changed")
                    phase_checks += 1
                phase_rows += 1

        occupancy = (3, 1)
        total = (5, 2)
        local = (1, 2)
        residual = tuple_type(f - l for f, l in zip_fn(total, local))

        def dft2(values):
            return (values[0] + values[1], values[0] - values[1])

        occupancy_hat = dft2(occupancy)
        total_hat = dft2(total)
        local_hat = dft2(local)
        residual_hat = dft2(residual)

        direct_total = sum_fn(c * f for c, f in zip_fn(occupancy, total))
        total_low = occupancy_hat[0] * total_hat[0] // 2
        total_high = occupancy_hat[1] * total_hat[1] // 2
        direct_local = sum_fn(c * f for c, f in zip_fn(occupancy, local))
        local_low = occupancy_hat[0] * local_hat[0] // 2
        local_high = occupancy_hat[1] * local_hat[1] // 2
        direct_residual = sum_fn(c * f for c, f in zip_fn(occupancy, residual))
        residual_low = occupancy_hat[0] * residual_hat[0] // 2
        residual_high = occupancy_hat[1] * residual_hat[1] // 2

        prime = (8, 3)
        hybrid = (3, 1)
        signed = tuple_type(p - h for p, h in zip_fn(prime, hybrid))

        aggregation_direct_energy = 1 * 1 + (-1) * (-1)
        aggregation_after_energy = (1 - 1) ** 2

        vector = (5, -2, 1, -3, 0, -1)
        strata = {}
        for a, value in enumerate_fn(vector):
            h = gcd(a, 6)
            strata.setdefault(h, []).append(value)
        within = fraction_type(0)
        between = fraction_type(0)
        weighted_mean = fraction_type(0)
        for values in strata.values():
            mean = fraction_type(sum_fn(values), len_fn(values))
            within += sum_fn((fraction_type(v) - mean) ** 2 for v in values)
            between += len_fn(values) * mean * mean
            weighted_mean += len_fn(values) * mean
        total_energy = sum_fn(v * v for v in vector)

        exponents = dict_type((
            ("H", fraction_type(21, 32)),
            ("P", fraction_type(1, 96)),
            ("target", fraction_type(1997, 1200)),
            ("high", fraction_type(213, 128)),
            ("local", fraction_type(1057, 640)),
        ))
        trivial = exponents["H"] + exponents["P"] + 1
        endpoint_deficit = trivial - exponents["target"]
        delta_threshold = 2 * endpoint_deficit
        high_margin = exponents["target"] - exponents["high"]
        local_margin = exponents["target"] - exponents["local"]

        return dict_type((
            ("phase_rows", phase_rows),
            ("phase_checks", phase_checks),
            ("occupancy_hat", occupancy_hat),
            ("total_hat", total_hat),
            ("local_hat", local_hat),
            ("residual_hat", residual_hat),
            ("direct_total", direct_total),
            ("total_low", total_low),
            ("total_high", total_high),
            ("direct_local", direct_local),
            ("local_low", local_low),
            ("local_high", local_high),
            ("direct_residual", direct_residual),
            ("residual_low", residual_low),
            ("residual_high", residual_high),
            ("prime_transform", sum_fn(prime)),
            ("hybrid_transform", sum_fn(hybrid)),
            ("signed_transform", sum_fn(signed)),
            ("aggregation_direct_energy", aggregation_direct_energy),
            ("aggregation_after_energy", aggregation_after_energy),
            ("anova_vector", vector),
            ("anova_total", total_energy),
            ("anova_within", within),
            ("anova_between", between),
            ("anova_weighted_mean", weighted_mean),
            ("trivial", trivial),
            ("endpoint_deficit", endpoint_deficit),
            ("delta_threshold", delta_threshold),
            ("high_margin", high_margin),
            ("local_margin", local_margin),
        ))

    fixture = finite_fixtures()

    contract_items = (
        ("maximum_claim", literal_maximum_claim),
        ("route_advance", "YES"),
        ("conditional_bridge_advance", "YES"),
        ("arithmetic_advance", False),
        ("fixed_atom_credit", 0),
        ("strict_1_over_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", False),
        ("numbered_release", "NO"),
        ("proof_path", literal_dependencies[0][0]),
        ("proof_sha256", literal_dependencies[0][1]),
        ("registry_sha256", literal_registry_digest),
        ("registry_rows", 71),
        ("source_locks", 5),
        ("dependency_locks", 7),
        ("H", "21/32"),
        ("Q", "1/3"),
        ("U", "133/400"),
        ("Y0", "31/96"),
        ("P", "1/96"),
        ("D0", "1/192"),
        ("L_pr", "2/3"),
        ("target_numerator", "1997/1200"),
        ("high_numerator", "213/128"),
        ("local_numerator", "1057/640"),
        ("splice_margin", "1/9600"),
        ("local_margin", "121/9600"),
        ("trivial_low_output", "5/3"),
        ("endpoint_deficit", "1/400"),
        ("delta_threshold", "1/200"),
        ("phase_rows", 114),
        ("scalar_total", 17),
        ("scalar_low", 14),
        ("scalar_high", 3),
        ("scalar_local", 5),
        ("scalar_residual", 12),
        ("aggregation_direct_energy", 2),
        ("aggregation_after_energy", 0),
        ("anova_total", 40),
        ("anova_within", "1"),
        ("anova_between", "39"),
        ("source_attachment", False),
        ("first_fatal", "NO_LITERAL_LOW_CONDUCTOR_SIGNED_PRIME_HYBRID_FIXED_POWER_THEOREM"),
        ("route_position", "BRIDGE_A_LOW_CONDUCTOR_SIGNED_GATE_OPEN"),
    )
    expected_contract = dict_type(contract_items)

    def validate_contract(candidate):
        if not same_exact(candidate, expected_contract):
            raise CheckFailure("contract changed")

    def fraction_text(value):
        if value.denominator == 1:
            return str_type(value.numerator)
        return str_type(value.numerator) + "/" + str_type(value.denominator)

    def result_items_base():
        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("conditional_bridge_advance", "YES"),
            ("arithmetic_advance", False),
            ("fixed_atom_credit", 0),
            ("strict_1_over_400", "UNPAID"),
            ("L2", "NONE"),
            ("TPC_207_TRIGGER", False),
            ("numbered_release", "NO"),
            ("phase_rows", fixture["phase_rows"]),
            ("phase_checks", fixture["phase_checks"]),
            ("scalar_total", fixture["direct_total"]),
            ("scalar_low", fixture["total_low"]),
            ("scalar_high", fixture["total_high"]),
            ("scalar_local", fixture["direct_local"]),
            ("scalar_local_low", fixture["local_low"]),
            ("scalar_local_high", fixture["local_high"]),
            ("scalar_residual", fixture["direct_residual"]),
            ("scalar_residual_low", fixture["residual_low"]),
            ("scalar_residual_high", fixture["residual_high"]),
            ("splice_identity", fixture["direct_residual"] == fixture["total_low"] + fixture["total_high"] - fixture["direct_local"]),
            ("prime_transform", fixture["prime_transform"]),
            ("hybrid_transform", fixture["hybrid_transform"]),
            ("signed_transform", fixture["signed_transform"]),
            ("aggregation_direct_energy", fixture["aggregation_direct_energy"]),
            ("aggregation_after_energy", fixture["aggregation_after_energy"]),
            ("anova_vector", fixture["anova_vector"]),
            ("anova_total", fixture["anova_total"]),
            ("anova_within", fraction_text(fixture["anova_within"])),
            ("anova_between", fraction_text(fixture["anova_between"])),
            ("anova_centered", fixture["anova_weighted_mean"] == 0),
            ("trivial_low_output", fraction_text(fixture["trivial"])),
            ("endpoint_deficit", fraction_text(fixture["endpoint_deficit"])),
            ("delta_threshold", fraction_text(fixture["delta_threshold"])),
            ("high_margin", fraction_text(fixture["high_margin"])),
            ("local_margin", fraction_text(fixture["local_margin"])),
            ("preferred_gate", "DIRECT_LOW_CONDUCTOR_SIGNED_SCALAR"),
            ("energy_gate", "SUFFICIENT_DELTA_GREATER_THAN_1_OVER_200"),
            ("energy_subtraction", "REJECTED_AGGREGATION_DOES_NOT_COMMUTE_WITH_SQUARING"),
            ("source_attachment", False),
            ("first_fatal", "NO_LITERAL_LOW_CONDUCTOR_SIGNED_PRIME_HYBRID_FIXED_POWER_THEOREM"),
            ("route_position", "BRIDGE_A_LOW_CONDUCTOR_SIGNED_GATE_OPEN"),
            ("registry_sha256", literal_registry_digest),
            ("registry_rows", len_fn(literal_registry)),
            ("source_locks", len_fn(literal_sources)),
            ("dependency_locks", len_fn(literal_dependencies)),
            ("contract_fields", len_fn(contract_items)),
        )

    def wrong_type(value):
        if type_fn(value) is bool_type:
            return 1 if value else 0
        if type_fn(value) is int_type:
            return False
        if type_fn(value) is str_type:
            class StringSubclass(str_type):
                pass
            return StringSubclass(value)
        if type_fn(value) is tuple_type:
            return list_type(value)
        return None

    def wrong_value(value):
        if type_fn(value) is bool_type:
            return not value
        if type_fn(value) is int_type:
            return value + 1
        if type_fn(value) is str_type:
            return value + "_MUT"
        if type_fn(value) is tuple_type:
            return value + ("MUT",)
        return "MUT"

    def must_reject(label, validator, candidate):
        mutation_labels.append(label)
        try:
            validator(candidate)
        except CheckFailure:
            return
        raise CheckFailure("mutation accepted: " + label)

    def run_contract_mutations():
        start = len_fn(mutation_labels)
        for key, value in contract_items:
            missing = dict_type(expected_contract)
            del missing[key]
            must_reject("contract_missing_" + key, validate_contract, missing)
            typed = dict_type(expected_contract)
            typed[key] = wrong_type(value)
            must_reject("contract_type_" + key, validate_contract, typed)
            changed = dict_type(expected_contract)
            changed[key] = wrong_value(value)
            must_reject("contract_value_" + key, validate_contract, changed)
        extra = dict_type(expected_contract)
        extra["EXTRA"] = 1
        must_reject("contract_extra", validate_contract, extra)

        class KeyImpostor:
            def __hash__(self):
                return hash_fn("maximum_claim")

            def __eq__(self, other):
                return other == "maximum_claim"

        impostor = dict_type(expected_contract)
        value = impostor.pop("maximum_claim")
        impostor[KeyImpostor()] = value
        must_reject("contract_key_impostor", validate_contract, impostor)
        return len_fn(mutation_labels) - start

    def run_registry_mutations():
        start = len_fn(mutation_labels)
        for index, row in enumerate_fn(literal_registry):
            changed = list_type(literal_registry)
            changed[index] = row + "_MUT"
            must_reject("registry_value_" + str_type(index), validate_registry, tuple_type(changed))
            changed[index] = 7
            must_reject("registry_type_" + str_type(index), validate_registry, tuple_type(changed))
        must_reject("registry_missing", validate_registry, literal_registry[:-1])
        must_reject("registry_extra", validate_registry, literal_registry + ("EXTRA = MUT",))
        must_reject("registry_list", validate_registry, list_type(literal_registry))
        must_reject("registry_duplicate", validate_registry, literal_registry[:-1] + (literal_registry[0],))
        return len_fn(mutation_labels) - start

    def run_source_mutations():
        start = len_fn(mutation_labels)
        for index, row in enumerate_fn(literal_sources):
            changed = list_type(literal_sources)
            changed[index] = row[:-1] + (row[-1] + "_MUT",)
            must_reject("source_value_" + str_type(index), validate_sources, tuple_type(changed))
            changed[index] = list_type(row)
            must_reject("source_type_" + str_type(index), validate_sources, tuple_type(changed))
        must_reject("source_missing", validate_sources, literal_sources[:-1])
        must_reject("source_extra", validate_sources, literal_sources + (("x", "y", "z"),))
        must_reject("source_list", validate_sources, list_type(literal_sources))
        return len_fn(mutation_labels) - start

    def run_dependency_mutations():
        start = len_fn(mutation_labels)
        for index, row in enumerate_fn(literal_dependencies):
            changed = list_type(literal_dependencies)
            changed[index] = (row[0], "0" * 64)
            must_reject("dependency_value_" + str_type(index), validate_dependencies, tuple_type(changed))
            changed[index] = list_type(row)
            must_reject("dependency_type_" + str_type(index), validate_dependencies, tuple_type(changed))
        must_reject("dependency_missing", validate_dependencies, literal_dependencies[:-1])
        must_reject("dependency_extra", validate_dependencies, literal_dependencies + (("x", "0" * 64),))
        must_reject("dependency_list", validate_dependencies, list_type(literal_dependencies))
        return len_fn(mutation_labels) - start

    def validate_result(candidate, expected):
        if not same_exact(candidate, expected):
            raise CheckFailure("result changed")

    validate_registry(literal_registry)
    validate_sources(literal_sources)
    validate_dependencies(literal_dependencies)
    validate_contract(expected_contract)

    if fixture["phase_rows"] != 114 or fixture["phase_checks"] != 2400:
        raise CheckFailure("gcd phase fixture changed")
    if (fixture["direct_total"], fixture["total_low"], fixture["total_high"]) != (17, 14, 3):
        raise CheckFailure("total conductor split changed")
    if (fixture["direct_local"], fixture["local_low"], fixture["local_high"]) != (5, 6, -1):
        raise CheckFailure("local conductor split changed")
    if (fixture["direct_residual"], fixture["residual_low"], fixture["residual_high"]) != (12, 8, 4):
        raise CheckFailure("residual conductor split changed")
    if fixture["direct_residual"] != fixture["total_low"] + fixture["total_high"] - fixture["direct_local"]:
        raise CheckFailure("scalar splice sign changed")
    if (fixture["prime_transform"], fixture["hybrid_transform"], fixture["signed_transform"]) != (11, 4, 7):
        raise CheckFailure("prime-hybrid sign changed")
    if (fixture["aggregation_direct_energy"], fixture["aggregation_after_energy"]) != (2, 0):
        raise CheckFailure("aggregation no-go changed")
    if fixture["anova_total"] != 40 or fixture["anova_within"] != 1 or fixture["anova_between"] != 39:
        raise CheckFailure("gcd-stratum ANOVA changed")
    if fixture["anova_weighted_mean"] != 0 or fixture["anova_within"] + fixture["anova_between"] != fixture["anova_total"]:
        raise CheckFailure("gcd-stratum centering changed")
    expected_fractions = (
        (fixture["trivial"], fraction_type(5, 3)),
        (fixture["endpoint_deficit"], fraction_type(1, 400)),
        (fixture["delta_threshold"], fraction_type(1, 200)),
        (fixture["high_margin"], fraction_type(1, 9600)),
        (fixture["local_margin"], fraction_type(121, 9600)),
    )
    if not all_fn(got == want for got, want in expected_fractions):
        raise CheckFailure("exponent ledger changed")

    contract_mutations = run_contract_mutations()
    registry_mutations = run_registry_mutations()
    source_mutations = run_source_mutations()
    dependency_mutations = run_dependency_mutations()

    result_base = result_items_base()
    provisional = dict_type(result_base + (
        ("contract_mutations", contract_mutations),
        ("registry_mutations", registry_mutations),
        ("source_mutations", source_mutations),
        ("dependency_mutations", dependency_mutations),
        ("semantic_mutations", 0),
        ("mutation_actions", 0),
    ))
    semantic_expected = dict_type(provisional)

    semantic_start = len_fn(mutation_labels)
    for key, value in tuple_type(semantic_expected.items()):
        missing = dict_type(semantic_expected)
        del missing[key]
        must_reject("result_missing_" + key, lambda c: validate_result(c, semantic_expected), missing)
        typed = dict_type(semantic_expected)
        typed[key] = wrong_type(value)
        must_reject("result_type_" + key, lambda c: validate_result(c, semantic_expected), typed)
        changed = dict_type(semantic_expected)
        changed[key] = wrong_value(value)
        must_reject("result_value_" + key, lambda c: validate_result(c, semantic_expected), changed)
    extra = dict_type(semantic_expected)
    extra["EXTRA"] = 1
    must_reject("result_extra", lambda c: validate_result(c, semantic_expected), extra)
    semantic_mutations = len_fn(mutation_labels) - semantic_start
    mutation_actions = len_fn(mutation_labels)

    final_result = dict_type(result_base + (
        ("contract_mutations", contract_mutations),
        ("registry_mutations", registry_mutations),
        ("source_mutations", source_mutations),
        ("dependency_mutations", dependency_mutations),
        ("semantic_mutations", semantic_mutations),
        ("mutation_actions", mutation_actions),
    ))

    expected_counts = (134, 146, 13, 17, 163, 473)
    actual_counts = (
        contract_mutations,
        registry_mutations,
        source_mutations,
        dependency_mutations,
        semantic_mutations,
        mutation_actions,
    )
    if actual_counts != expected_counts:
        raise CheckFailure("mutation counts changed: " + str_type(actual_counts))
    if len_fn(tuple_type(mutation_labels)) != len_fn(set_type(mutation_labels)):
        raise CheckFailure("mutation labels not unique")

    validate_result(final_result, final_result)
    return dict_type(final_result)


def _seal_runner():
    factory = _make_trusted_runner
    registry = tuple(REGISTRY)
    sources = tuple(SOURCE_LOCKS)
    dependencies = tuple(DEPENDENCIES)
    registry_digest = REGISTRY_SHA256
    maximum_claim = MAXIMUM_CLAIM
    fraction_type = Fraction
    path_type = Path
    sha256_fn = hashlib.sha256
    dict_type = dict
    tuple_type = tuple
    list_type = list
    str_type = str
    int_type = int
    bool_type = bool
    type_fn = type
    len_fn = len
    all_fn = all
    zip_fn = zip
    set_type = set
    range_fn = range
    enumerate_fn = enumerate
    sum_fn = sum
    abs_fn = abs
    pow_fn = pow
    min_fn = min
    max_fn = max
    hash_fn = hash
    file_seed = __file__

    def sealed():
        return factory(
            registry_seed=registry,
            source_seed=sources,
            dependency_seed=dependencies,
            registry_digest_seed=registry_digest,
            maximum_claim_seed=maximum_claim,
            fraction_type=fraction_type,
            path_type=path_type,
            sha256_fn=sha256_fn,
            dict_type=dict_type,
            tuple_type=tuple_type,
            list_type=list_type,
            str_type=str_type,
            int_type=int_type,
            bool_type=bool_type,
            type_fn=type_fn,
            len_fn=len_fn,
            all_fn=all_fn,
            zip_fn=zip_fn,
            set_type=set_type,
            range_fn=range_fn,
            enumerate_fn=enumerate_fn,
            sum_fn=sum_fn,
            abs_fn=abs_fn,
            pow_fn=pow_fn,
            min_fn=min_fn,
            max_fn=max_fn,
            hash_fn=hash_fn,
            file_seed=file_seed,
        )

    return sealed


_TRUSTED_RUN = _seal_runner()
run_check = _TRUSTED_RUN


def _make_main(
    trusted_runner,
    *,
    tuple_type=tuple,
    type_fn=type,
    str_type=str,
    len_fn=len,
    json_dumps=json.dumps,
    stdout_write=sys.stdout.write,
):
    baseline = trusted_runner()
    baseline_items = tuple_type(baseline.items())
    frozen_stdout = json_dumps(baseline, sort_keys=True, separators=(",", ":")) + "\n"

    def sealed(*argv_objects):
        if len_fn(argv_objects) != 1:
            raise CheckFailure("explicit --check is required")
        argv = argv_objects[0]
        if type_fn(argv) is not tuple_type:
            raise CheckFailure("explicit --check is required")
        if len_fn(argv) != 1 or type_fn(argv[0]) is not str_type or argv[0] != "--check":
            raise CheckFailure("explicit --check is required")
        result = trusted_runner()
        if tuple_type(result.items()) != baseline_items:
            raise CheckFailure("sealed result changed")
        stdout_write(frozen_stdout)
        return 0

    return sealed


main = _make_main(_TRUSTED_RUN)


if __name__ == "__main__":
    try:
        raise SystemExit(main(tuple(sys.argv[1:])))
    except CheckFailure as exc:
        sys.stderr.write("CheckFailure: " + str(exc) + "\n")
        raise SystemExit(1)
