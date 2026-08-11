#!/usr/bin/env python3
"""Fail-closed finite checker for the V49 ultra-low three-lane compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever the frozen V49 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "V45_SECOND_MOMENT_PAYS_THE_CRITICAL_CONDUCTOR_COLLAR_TO_D1_AND_THE_"
    "REMAINING_LOCAL_CENTERED_ULTRALOW_SCALAR_SPLITS_EXACTLY_INTO_"
    "PRINCIPAL_GENERIC_AND_UNIQUE_POSSIBLE_EXCEPTIONAL_LANES_BEFORE_OUTER_ABSOLUTE"
)


REGISTRY = (
    "V49_MAXIMUM_CLAIM = V45_SECOND_MOMENT_PAYS_THE_CRITICAL_CONDUCTOR_COLLAR_TO_D1_AND_THE_REMAINING_LOCAL_CENTERED_ULTRALOW_SCALAR_SPLITS_EXACTLY_INTO_PRINCIPAL_GENERIC_AND_UNIQUE_POSSIBLE_EXCEPTIONAL_LANES_BEFORE_OUTER_ABSOLUTE",
    "V49_ROUTE_ADVANCE = YES",
    "V49_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V49_ARITHMETIC_ADVANCE = NO",
    "V49_FIXED_ATOM_CREDIT = 0",
    "V49_STRICT_1_OVER_400 = UNPAID",
    "V49_L2 = NONE",
    "V49_TPC_207_TRIGGER = false",
    "V49_NUMBERED_RELEASE = NO",
    "V49_DERIVATION_STATUS = COHERENT_AFTER_CRITICAL_COLLAR_PAYMENT_LOCAL_CENTERING_AND_EXCEPTIONAL_AWARE_THREE_LANE_SPLIT",
    "V49_ASSUMPTION_POLICY = DIRECT_THREE_LANE_SIGNED_SCALAR_IS_PRIMARY_HEURISTIC_THEOREM_AND_SEPARATE_PRINCIPAL_GENERIC_EXCEPTIONAL_BOUNDS_ARE_STRONGER_FALLBACKS",
    "V49_SELECTED_RESEARCH_ROUTE = PAY_CRITICAL_CONDUCTOR_COLLAR__ATTACK_DIRECT_LOCAL_CENTERED_ULTRALOW_THREE_LANE_SCALAR__THEN_LONG_MOBIUS__V42_GATE_B_PARALLEL__V43_A_B_JOIN__C_RESERVE",
    "V49_V48_COMMON_TRANSITION = RETAINED_EXACT_BEFORE_FIRST_OUTER_ABSOLUTE",
    "V49_D1_DEFINITION = X_POWER_49_OVER_9600",
    "V49_D1_THRESHOLD_ORDER = PROVED_STRICT_1_OVER_200_LT_49_OVER_9600_LT_1_OVER_192",
    "V49_MOVING_CONDUCTOR_SPLIT = PROVED_EXACT_T_COMMON_EQUALS_M_BELOW_D1_PLUS_V_AT_LEAST_D1",
    "V49_COLLAR_BLOCK_BOUND = RETAINED_V45_P_SQUARED_TIMES_D_OVER_Q_PLUS_ONE_OVER_D",
    "V49_COLLAR_COEFFICIENT_ENERGY = PROVED_X_POWER_151_OVER_9600_PLUS_O1",
    "V49_OLD_HIGH_COEFFICIENT_ENERGY = RETAINED_X_POWER_150_OVER_9600_PLUS_O1",
    "V49_COMBINED_COEFFICIENT_ENERGY = PROVED_X_POWER_151_OVER_9600_PLUS_O1",
    "V49_PAID_CONDUCTOR_REMAINDER = PROVED_V_AT_LEAST_D1_X_POWER_31951_OVER_19200_PLUS_O1",
    "V49_PAID_CONDUCTOR_REMAINDER_MARGIN = 1_OVER_19200",
    "V49_ULTRALOW_CENTERED_SCALAR = DEFINED_C_UL_EQUALS_M_BELOW_D1_MINUS_L_PF",
    "V49_CENTERED_SCALAR_SPLICE = PROVED_EXACT_R_AP_EQUALS_C_UL_PLUS_V_AT_LEAST_D1",
    "V49_LOCAL_EULER_LOCATION = RETAINED_INSIDE_SELECTED_ULTRALOW_SCALAR",
    "V49_LOCAL_EULER_DOUBLE_COUNTING = STOP_SCOPED_DO_NOT_CHARGE_L_PF_BOTH_INSIDE_C_UL_AND_AS_EXTERNAL_ERROR",
    "V49_DIRECT_ULTRALOW_GATE = OPEN_X_POWER_1997_OVER_1200_MINUS_ETA_UL_WITH_ETA_UL_POSITIVE",
    "V49_ULTRALOW_TO_AP_RESIDUAL = PROVED_TERMINAL_EQUIVALENT_MODULO_PAID_CONDUCTOR_REMAINDER",
    "V49_TRANSITION_CONDITIONAL_COMPILER = PROVED_DIRECT_ULTRALOW_GATE_PAYS_TRANSITION_WITH_CORRECTIONS",
    "V49_TRANSITION_CONDITIONAL_MARGIN = MIN_ETA_UL_1_OVER_19200_13_OVER_4800_817_OVER_4800",
    "V49_PRINCIPAL_LANE = PROVED_EXACT_CONDUCTOR_ONE_COMPONENT_MINUS_LOCAL_EULER_SCALAR",
    "V49_GENERIC_LANE = PROVED_EXACT_ALL_NONPRINCIPAL_NONEXCEPTIONAL_PRIMITIVE_CONDUCTORS_BELOW_D1",
    "V49_LANDAU_PAGE_EXCEPTION_SET = DEFINED_BEFORE_ESTIMATE_AT_LEVEL_D1",
    "V49_LANDAU_PAGE_EXCEPTION_CARDINALITY = SOURCE_BACKED_EMPTY_OR_SINGLETON",
    "V49_LANDAU_PAGE_EXCEPTION_TYPE = SOURCE_BACKED_UNIQUE_PRIMITIVE_QUADRATIC_CHARACTER_IF_PRESENT",
    "V49_EXCEPTIONAL_LANE = PROVED_EXACT_POSSIBLE_EXCEPTIONAL_PRIMITIVE_ROW_WITH_ALL_INDUCED_COFACTORS",
    "V49_THREE_LANE_REASSEMBLY = PROVED_EXACT_C_UL_EQUALS_C_PR_PLUS_C_GEN_PLUS_C_EXC",
    "V49_DIRECT_THREE_LANE_GATE = SELECTED_ONE_SIGNED_SCALAR_BEFORE_OUTER_ABSOLUTE",
    "V49_MARGINAL_THREE_ENGINE_PACKAGE = OPEN_STRONGER_SUFFICIENT_HEURISTIC_THEOREM",
    "V49_MARGINAL_THREE_ENGINE_STRENGTH = STRONGER_NOT_EQUIVALENT_TO_DIRECT_SIGNED_GATE",
    "V49_TRIANGLE_OVERPAY_FIREWALL = PROVED_FINITE_SIGNED_CANCELLATION_FIXTURE_19_VERSUS_5",
    "V49_PRINCIPAL_LOCAL_RELATION = RETAINED_SCALAR_SUBTRACTION_ONLY",
    "V49_PRINCIPAL_LOCAL_TERMWISE_PROJECTION = STOP_SCOPED_FALSE_EQUAL_SUM_DIFFERENT_VECTOR_FIXTURE",
    "V49_EXCEPTIONAL_PRIMITIVE_RANK = AT_MOST_ONE_PRIMITIVE_CHARACTER_TYPE",
    "V49_EXCEPTIONAL_INDUCED_TOWER = RETAINED_ALL_E_COFACTORS_NOT_ONE_SUMMAND",
    "V49_DELETE_EXCEPTIONAL_PRIME_AFTER_FREEZE = STOP_SCOPED_CHANGES_COMMON_ENSEMBLE",
    "V49_GENERIC_ZERO_FREE_REGION_TO_LITERAL_POWER = STOP_SCOPED_WRONG_NORM_AND_NO_SIGNED_RAMANUJAN_ATTACHMENT",
    "V49_BFI_CRITICAL_COLLAR = SOURCE_BACKED_VIA_V45_PRIMITIVE_BLOCK_ESTIMATE",
    "V49_FGKMT_LANDAU_PAGE = SOURCE_BACKED_EXCEPTIONAL_TYPE_AND_CARDINALITY_ONLY",
    "V49_DRAPPEAU_FIORILLI_EXCEPTIONAL_BIAS = SOURCE_BACKED_WARNING_WRONG_FIXED_RESIDUE_FIRST_MOMENT_OBJECT",
    "V49_BAKER_FEW_EXCEPTIONAL_MODULI = STOP_SCOPED_PAIRWISE_COPRIME_AND_DISCARDABLE_EXCEPTION_SET_WRONG_OBJECT",
    "V49_PRODUCTS_OF_PRIMES_DENSE_MODEL = STOP_SCOPED_TERNARY_PRODUCT_AND_QUADRATIC_OBSTRUCTION_WRONG_OBJECT",
    "V49_DIRECT_PRIMARY_SOURCE_FOR_ULTRALOW_SIGNED_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11",
    "V49_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_THE_LOCAL_CENTERED_ULTRALOW_PRINCIPAL_GENERIC_EXCEPTIONAL_SIGNED_SCALAR_WITH_FIXED_POWER",
    "V49_LONG_BALANCED_WINDOW = OPEN_D_GT_U_AND_K_GT_U",
    "V49_LONG_REVERSE_TYPE_I_WINDOW = OPEN_D_GT_U_AND_K_LE_U",
    "V49_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE",
    "V49_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_CRITICAL_CONDUCTOR_COLLAR_PAID_ULTRALOW_THREE_LANE_SCALAR_OPEN_LONG_MOBIUS_OPEN",
    "V49_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED",
    "V49_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B",
)


REGISTRY_SHA256 = "854e5b552eaf972e5d9e8b38a8dc5a69bcfcd7f582edda464c2f7f275ad81c6e"


SOURCE_LOCKS = (
    ("BFI-large-moduli", "Enrico Bombieri; John Friedlander; Henryk Iwaniec", "primitive-character large-sieve block estimate inherited through the exact V45 compiler"),
    ("1412.5029v3", "Kevin Ford; Ben Green; Sergei Konyagin; James Maynard; Terence Tao", "Landau--Page exceptional alternative is empty or one primitive quadratic character"),
    ("2003.02201v1", "Sary Drappeau; Daniel Fiorilli", "possible exceptional secondary bias is retained in a fixed-residue first moment, not the V49 scalar"),
    ("1905.12488v1", "Roger Baker", "few exceptional pairwise-coprime moduli, not the induced-cofactor tower"),
    ("2301.07679v3", "Kaisa Matomaki; Joni Teravainen", "ternary prime-product dense model with possible quadratic obstruction, not the signed V49 object"),
)


DEPENDENCIES = (
    ("research/tpc-big-road/bridge_b_ultralow_conductor_three_lane_compiler.md", "c44d081bd1ef00a118191f1404b442e3c67585862a4ca737cdc6dafebff6c364"),
    ("research/tpc-big-road/bridge_b_low_conductor_signed_covariance_splice.md", "5b35d2fc4fcb6d66628f704df3d22b39fa76b0fb524fdb30062c309f0485b6c5"),
    ("research/tpc-big-road/tpc_bridge_b_low_conductor_signed_covariance_checker.py", "fd86b19f1bdf7dd2a66a99060810369f64367909ac2bceb04df3e39c464af9fe"),
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
        "V45_SECOND_MOMENT_PAYS_THE_CRITICAL_CONDUCTOR_COLLAR_TO_D1_AND_THE_"
        "REMAINING_LOCAL_CENTERED_ULTRALOW_SCALAR_SPLITS_EXACTLY_INTO_"
        "PRINCIPAL_GENERIC_AND_UNIQUE_POSSIBLE_EXCEPTIONAL_LANES_BEFORE_OUTER_ABSOLUTE"
    )
    literal_registry_digest = "854e5b552eaf972e5d9e8b38a8dc5a69bcfcd7f582edda464c2f7f275ad81c6e"
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
        exponents = dict_type((
            ("H", fraction_type(21, 32)),
            ("Q", fraction_type(1, 3)),
            ("P", fraction_type(1, 96)),
            ("D0", fraction_type(1, 192)),
            ("D1", fraction_type(49, 9600)),
            ("threshold", fraction_type(1, 200)),
            ("target", fraction_type(1997, 1200)),
        ))
        collar_energy = 2 * exponents["P"] - exponents["D1"]
        old_high_energy = 3 * exponents["P"] / 2
        combined_energy = max_fn(collar_energy, old_high_energy)
        paid_output = exponents["H"] + 1 + combined_energy / 2
        paid_margin = exponents["target"] - paid_output
        cut_product_exponent = exponents["D0"] + exponents["D1"]

        lane_rows = (
            ("principal", 1, False, 11),
            ("generic", 3, False, 2),
            ("exceptional", 5, True, 5),
            ("generic", 7, False, -9),
        )
        exceptional_rows = tuple_type(row for row in lane_rows if row[2])
        generic_rows = tuple_type(row for row in lane_rows if row[0] == "generic")
        principal_rows = tuple_type(row for row in lane_rows if row[0] == "principal")
        two_exceptional_rows = exceptional_rows + (("exceptional", 11, True, -2),)

        m_pr = sum_fn(row[3] for row in principal_rows)
        m_gen = sum_fn(row[3] for row in generic_rows)
        m_exc = sum_fn(row[3] for row in exceptional_rows)
        l_pf = 4
        v_paid = 3
        m_low = m_pr + m_gen + m_exc
        c_pr = m_pr - l_pf
        c_ul = c_pr + m_gen + m_exc
        r_ap = c_ul + v_paid
        triangle = abs_fn(c_pr) + abs_fn(m_gen) + abs_fn(m_exc)

        induced_weights = (2, -1, 4)
        principal_vector = (3, 1)
        local_vector = (2, 2)

        return dict_type((
            ("H", exponents["H"]),
            ("Q", exponents["Q"]),
            ("P", exponents["P"]),
            ("D0", exponents["D0"]),
            ("D1", exponents["D1"]),
            ("threshold", exponents["threshold"]),
            ("target", exponents["target"]),
            ("collar_energy", collar_energy),
            ("old_high_energy", old_high_energy),
            ("combined_energy", combined_energy),
            ("paid_output", paid_output),
            ("paid_margin", paid_margin),
            ("cut_product_exponent", cut_product_exponent),
            ("lane_rows", lane_rows),
            ("exceptional_rows", exceptional_rows),
            ("two_exceptional_rows", two_exceptional_rows),
            ("m_pr", m_pr),
            ("m_gen", m_gen),
            ("m_exc", m_exc),
            ("l_pf", l_pf),
            ("v_paid", v_paid),
            ("m_low", m_low),
            ("c_pr", c_pr),
            ("c_ul", c_ul),
            ("r_ap", r_ap),
            ("triangle", triangle),
            ("induced_weights", induced_weights),
            ("induced_sum", sum_fn(induced_weights)),
            ("principal_vector", principal_vector),
            ("local_vector", local_vector),
            ("principal_local_scalar_equal", sum_fn(principal_vector) == sum_fn(local_vector)),
            ("principal_local_termwise_equal", principal_vector == local_vector),
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
        ("registry_rows", 60),
        ("source_locks", 5),
        ("dependency_locks", 7),
        ("H", "21/32"),
        ("Q", "1/3"),
        ("P", "1/96"),
        ("D0", "1/192"),
        ("D1", "49/9600"),
        ("endpoint_threshold", "1/200"),
        ("target_numerator", "1997/1200"),
        ("collar_coefficient_energy", "151/9600"),
        ("old_high_coefficient_energy", "150/9600"),
        ("combined_coefficient_energy", "151/9600"),
        ("paid_conductor_output", "31951/19200"),
        ("paid_conductor_margin", "1/19200"),
        ("cut_product_exponent", "33/3200"),
        ("m_pr", 11),
        ("m_gen", -7),
        ("m_exc", 5),
        ("l_pf", 4),
        ("v_paid", 3),
        ("m_low", 9),
        ("c_pr", 7),
        ("c_ul", 5),
        ("r_ap", 8),
        ("triangle_overpay", 19),
        ("exceptional_cardinality", 1),
        ("exceptional_quadratic", True),
        ("induced_cofactors", 3),
        ("induced_sum", 5),
        ("source_attachment", False),
        ("first_fatal", "NO_LITERAL_LOCAL_CENTERED_ULTRALOW_THREE_LANE_FIXED_POWER_THEOREM"),
        ("route_position", "BRIDGE_A_CRITICAL_COLLAR_PAID_ULTRALOW_THREE_LANE_OPEN"),
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
            ("D1", fraction_text(fixture["D1"])),
            ("threshold_order", fixture["threshold"] < fixture["D1"] < fixture["D0"]),
            ("collar_coefficient_energy", fraction_text(fixture["collar_energy"])),
            ("old_high_coefficient_energy", "150/9600"),
            ("combined_coefficient_energy", fraction_text(fixture["combined_energy"])),
            ("paid_conductor_output", fraction_text(fixture["paid_output"])),
            ("paid_conductor_margin", fraction_text(fixture["paid_margin"])),
            ("cut_product_exponent", fraction_text(fixture["cut_product_exponent"])),
            ("cut_product_below_Q", fixture["cut_product_exponent"] < fixture["Q"]),
            ("lane_rows", fixture["lane_rows"]),
            ("exceptional_cardinality", len_fn(fixture["exceptional_rows"])),
            ("exceptional_quadratic", all_fn(row[2] for row in fixture["exceptional_rows"])),
            ("two_exceptional_rejected", len_fn(fixture["two_exceptional_rows"]) > 1),
            ("m_pr", fixture["m_pr"]),
            ("m_gen", fixture["m_gen"]),
            ("m_exc", fixture["m_exc"]),
            ("l_pf", fixture["l_pf"]),
            ("v_paid", fixture["v_paid"]),
            ("m_low", fixture["m_low"]),
            ("c_pr", fixture["c_pr"]),
            ("c_ul", fixture["c_ul"]),
            ("r_ap", fixture["r_ap"]),
            ("splice_identity", fixture["r_ap"] == fixture["c_ul"] + fixture["v_paid"]),
            ("three_lane_identity", fixture["c_ul"] == fixture["c_pr"] + fixture["m_gen"] + fixture["m_exc"]),
            ("triangle_overpay", fixture["triangle"]),
            ("direct_signed_scalar", abs_fn(fixture["c_ul"])),
            ("induced_weights", fixture["induced_weights"]),
            ("induced_cofactors", len_fn(fixture["induced_weights"])),
            ("induced_sum", fixture["induced_sum"]),
            ("principal_local_scalar_equal", fixture["principal_local_scalar_equal"]),
            ("principal_local_termwise_equal", fixture["principal_local_termwise_equal"]),
            ("preferred_gate", "DIRECT_LOCAL_CENTERED_ULTRALOW_THREE_LANE_SCALAR"),
            ("fallback_gate", "SEPARATE_PRINCIPAL_GENERIC_EXCEPTIONAL_MARGINALS_STRONGER"),
            ("source_attachment", False),
            ("first_fatal", "NO_LITERAL_LOCAL_CENTERED_ULTRALOW_THREE_LANE_FIXED_POWER_THEOREM"),
            ("route_position", "BRIDGE_A_CRITICAL_COLLAR_PAID_ULTRALOW_THREE_LANE_OPEN"),
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

    if not (fixture["threshold"] < fixture["D1"] < fixture["D0"]):
        raise CheckFailure("D1 threshold order changed")
    expected_fractions = (
        (fixture["collar_energy"], fraction_type(151, 9600)),
        (fixture["old_high_energy"], fraction_type(150, 9600)),
        (fixture["combined_energy"], fraction_type(151, 9600)),
        (fixture["paid_output"], fraction_type(31951, 19200)),
        (fixture["target"], fraction_type(31952, 19200)),
        (fixture["paid_margin"], fraction_type(1, 19200)),
        (fixture["cut_product_exponent"], fraction_type(33, 3200)),
    )
    if not all_fn(got == want for got, want in expected_fractions):
        raise CheckFailure("critical collar exponent ledger changed")
    if fixture["cut_product_exponent"] >= fixture["Q"]:
        raise CheckFailure("D0 D1 below Q condition changed")
    if len_fn(fixture["exceptional_rows"]) not in (0, 1):
        raise CheckFailure("Landau--Page cardinality changed")
    if not all_fn(row[2] for row in fixture["exceptional_rows"]):
        raise CheckFailure("exceptional quadratic type changed")
    if len_fn(fixture["two_exceptional_rows"]) <= 1:
        raise CheckFailure("two-exception falsifier changed")
    if (
        fixture["m_pr"],
        fixture["m_gen"],
        fixture["m_exc"],
        fixture["l_pf"],
        fixture["v_paid"],
        fixture["m_low"],
        fixture["c_pr"],
        fixture["c_ul"],
        fixture["r_ap"],
        fixture["triangle"],
    ) != (11, -7, 5, 4, 3, 9, 7, 5, 8, 19):
        raise CheckFailure("three-lane scalar fixture changed")
    if fixture["c_ul"] != fixture["c_pr"] + fixture["m_gen"] + fixture["m_exc"]:
        raise CheckFailure("three-lane reassembly changed")
    if fixture["r_ap"] != fixture["c_ul"] + fixture["v_paid"]:
        raise CheckFailure("paid-splice sign changed")
    if fixture["triangle"] <= abs_fn(fixture["c_ul"]):
        raise CheckFailure("triangle overpay falsifier changed")
    if fixture["induced_weights"] != (2, -1, 4) or fixture["induced_sum"] != 5:
        raise CheckFailure("induced-cofactor tower changed")
    if not fixture["principal_local_scalar_equal"] or fixture["principal_local_termwise_equal"]:
        raise CheckFailure("principal/local projection falsifier changed")

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

    expected_counts = (137, 124, 13, 17, 172, 463)
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
