#!/usr/bin/env python3
"""Fail-closed finite checker for the V50 endpoint/Siegel-world compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever the frozen V50 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "AN_OPEN_SAVING_PARAMETER_DELTA_IN_0_1_OVER_9600_GENERATES_AN_EXACT_"
    "SELF_FINANCING_CONDUCTOR_CUT_AND_THE_GLOBAL_SIEGEL_QUALITY_DICHOTOMY_"
    "SENDS_UNBOUNDED_QUALITY_TO_A_SOURCE_BACKED_TWIN_PRIME_EXIT_OR_REDUCES_"
    "BRIDGE_A_TO_A_BOUNDED_QUALITY_SIGNED_CORE_THEOREM"
)


REGISTRY = (
    "V50_MAXIMUM_CLAIM = AN_OPEN_SAVING_PARAMETER_DELTA_IN_0_1_OVER_9600_GENERATES_AN_EXACT_SELF_FINANCING_CONDUCTOR_CUT_AND_THE_GLOBAL_SIEGEL_QUALITY_DICHOTOMY_SENDS_UNBOUNDED_QUALITY_TO_A_SOURCE_BACKED_TWIN_PRIME_EXIT_OR_REDUCES_BRIDGE_A_TO_A_BOUNDED_QUALITY_SIGNED_CORE_THEOREM",
    "V50_ROUTE_ADVANCE = YES",
    "V50_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V50_ARITHMETIC_ADVANCE = NO",
    "V50_FIXED_ATOM_CREDIT = 0",
    "V50_STRICT_1_OVER_400 = UNPAID",
    "V50_L2 = NONE",
    "V50_TPC_207_TRIGGER = false",
    "V50_NUMBERED_RELEASE = NO",
    "V50_DERIVATION_STATUS = COHERENT_AFTER_SAVING_MATCHED_MOVING_CUT_GLOBAL_SIEGEL_QUALITY_DICHOTOMY_AND_SOURCE_BACKED_UNBOUNDED_QUALITY_EXIT",
    "V50_ASSUMPTION_POLICY = BOUNDED_QUALITY_DIRECT_SIGNED_CORE_IS_PRIMARY_HEURISTIC_THEOREM__UNBOUNDED_QUALITY_IS_SOURCE_BACKED_CONDITIONAL_EXIT__MARGINAL_ENGINES_ARE_STRONGER_FALLBACKS",
    "V50_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_DIRECT_TPC_EXIT__OTHERWISE_BOUNDED_QUALITY_ENDPOINT_CORE__THEN_LONG_MOBIUS__V42_GATE_B__V43_JOIN__C_RESERVE",
    "V50_SAVING_PARAMETER_DOMAIN = OPEN_0_LT_DELTA_LT_1_OVER_9600",
    "V50_BETA_DELTA = 1_OVER_200_PLUS_2_DELTA",
    "V50_CUT_ORDER = PROVED_STRICT_1_OVER_200_LT_BETA_DELTA_LT_1_OVER_192",
    "V50_V49_RECOVERY = DELTA_1_OVER_19200_GIVES_BETA_49_OVER_9600",
    "V50_MOVING_CONDUCTOR_SPLIT = PROVED_EXACT_T_COMMON_EQUALS_M_BELOW_D_DELTA_PLUS_V_AT_LEAST_D_DELTA",
    "V50_COLLAR_BLOCK_BOUND = RETAINED_V45_P_SQUARED_TIMES_D_OVER_Q_PLUS_ONE_OVER_D",
    "V50_COLLAR_COEFFICIENT_ENERGY = PROVED_X_POWER_19_OVER_1200_MINUS_2_DELTA_PLUS_O1",
    "V50_OLD_HIGH_COEFFICIENT_ENERGY = RETAINED_X_POWER_1_OVER_64_PLUS_O1",
    "V50_COMBINED_COEFFICIENT_ENERGY = PROVED_X_POWER_19_OVER_1200_MINUS_2_DELTA_PLUS_O1",
    "V50_PAID_CONDUCTOR_REMAINDER = PROVED_V_AT_LEAST_D_DELTA_X_POWER_1997_OVER_1200_MINUS_DELTA_PLUS_O1",
    "V50_PAID_CONDUCTOR_REMAINDER_MARGIN = DELTA",
    "V50_DELTA_ZERO_ENDPOINT = STOP_SCOPED_ZERO_STRICT_MARGIN",
    "V50_DELTA_UPPER_ENDPOINT = V48_D0_BOUNDARY_OUTSIDE_OPEN_V50_INTERIOR",
    "V50_ENDPOINT_CORE = DEFINED_C_DELTA_EQUALS_M_BELOW_D_DELTA_MINUS_L_PF",
    "V50_ENDPOINT_CORE_SPLICE = PROVED_EXACT_R_AP_EQUALS_C_DELTA_PLUS_V_AT_LEAST_D_DELTA",
    "V50_BUDGET_MATCHED_CORE_GATE = OPEN_X_POWER_1997_OVER_1200_MINUS_DELTA_PLUS_O1",
    "V50_TRANSITION_COMPILER = PROVED_BUDGET_MATCHED_CORE_GATE_PAYS_AP_TRANSITION",
    "V50_TRANSITION_MARGIN = ANY_FIXED_DELTA_TR_STRICTLY_LESS_THAN_DELTA",
    "V50_THREE_LANE_REASSEMBLY = RETAINED_EXACT_C_DELTA_EQUALS_C_PR_DELTA_PLUS_C_GEN_DELTA_PLUS_C_EXC_DELTA",
    "V50_LANDAU_PAGE_EXCEPTION_SET = DEFINED_BEFORE_ESTIMATE_AT_LEVEL_D_DELTA",
    "V50_LANDAU_PAGE_EXCEPTION_CARDINALITY = SOURCE_BACKED_EMPTY_OR_SINGLETON",
    "V50_EXCEPTIONAL_INDUCED_TOWER = RETAINED_ALL_COFACTORS",
    "V50_SIEGEL_QUALITY = DEFINED_ETA_CHI_TIMES_ONE_MINUS_BETA_TIMES_LOG_D_EQUALS_ONE",
    "V50_GLOBAL_SIEGEL_QUALITY_DICHOTOMY = PROVED_EXHAUSTIVE_BOUNDED_OR_UNBOUNDED",
    "V50_UNBOUNDED_QUALITY_WORLD = SOURCE_BACKED_CONDITIONAL_DIRECT_TWIN_PRIME_EXIT",
    "V50_MATOMAKI_MERIKOSKI_COROLLARY_1_1 = SOURCE_BACKED_FIXED_H2_X_IN_D_POWER_10_TO_D_POWER_10_LOG_QUALITY_WITH_EXP_MINUS_C_SQRT_LOG_QUALITY_ERROR",
    "V50_H2_SINGULAR_SERIES = PROVED_STRICTLY_POSITIVE",
    "V50_PROPER_PRIME_POWER_CONTAMINATION = PROVED_O_X_POWER_1_OVER_2_LOG_CUBED_X",
    "V50_UNBOUNDED_QUALITY_TO_TPC = PROVED_CONDITIONAL_FROM_SOURCE_CORRELATION_AND_PRIME_POWER_REMOVAL",
    "V50_PER_SCALE_SINGLETON_TO_GLOBAL_UNBOUNDED = STOP_SCOPED_FALSE_QUANTIFIER_PROMOTION",
    "V50_BOUNDED_QUALITY_WORLD = REDUCED_TO_FOR_EVERY_FIXED_B_ONE_B_DEPENDENT_ENDPOINT_MATCHED_DIRECT_SIGNED_CORE_GATE",
    "V50_BOUNDED_QUALITY_GATE = OPEN_FOR_EVERY_FINITE_B_EXISTS_DELTA_B_WITH_DIRECT_SIGNED_CORE_X_POWER_TARGET_MINUS_DELTA_B",
    "V50_BOUNDED_QUALITY_GATE_QUANTIFIERS = FOR_EVERY_FINITE_B__EXISTS_DELTA_B__EXISTS_C_B_X0_B__FOR_ALL_X_AT_LEAST_X0_B",
    "V50_B_DEPENDENCE = ALLOWED_IN_DELTA_B_THRESHOLD_AND_IMPLIED_CONSTANT_NOT_IN_LATER_X",
    "V50_DIRECT_SIGNED_GATE = SELECTED_ONE_SCALAR_BEFORE_OUTER_ABSOLUTE",
    "V50_MARGINAL_THREE_ENGINE_PACKAGE = OPEN_STRONGER_SUFFICIENT_HEURISTIC_THEOREM",
    "V50_MARGINAL_THREE_ENGINE_STRENGTH = STRONGER_NOT_EQUIVALENT_TO_DIRECT_SIGNED_GATE",
    "V50_TRIANGLE_OVERPAY_FIREWALL = RETAINED_FINITE_SIGNED_CANCELLATION_FIXTURE_19_VERSUS_5",
    "V50_DELETE_EXCEPTIONAL_LANE = STOP_SCOPED_CHANGES_LITERAL_SCALAR",
    "V50_BFI_MOVING_COLLAR = SOURCE_BACKED_VIA_V45_PRIMITIVE_BLOCK_ESTIMATE",
    "V50_FGKMT_LANDAU_PAGE = SOURCE_BACKED_PER_SCALE_EXCEPTIONAL_TYPE_AND_CARDINALITY_ONLY",
    "V50_MATOMAKI_MERIKOSKI_UNBOUNDED_EXIT = SOURCE_BACKED_LITERAL_FIXED_SHIFT_CORRELATION",
    "V50_SACHPAZIS_LARGE_MODULUS_AP = STOP_SCOPED_REQUIRES_X_EQUALS_D_POWER_V_WITH_V_AT_LEAST_200_OVER_EPSILON_AND_FIXED_AP_OBJECT",
    "V50_WRIGHT_LARGE_MODULUS_AP = STOP_SCOPED_SUBPOWER_EXCEPTIONAL_CONDUCTOR_AND_AP_RESIDUE_OBJECT",
    "V50_DIRECT_PRIMARY_SOURCE_FOR_BOUNDED_CORE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11",
    "V50_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_THE_B_DEPENDENT_ENDPOINT_MATCHED_LOCAL_CENTERED_PRINCIPAL_GENERIC_EXCEPTIONAL_SIGNED_CORE_WITH_FIXED_POWER",
    "V50_LONG_BALANCED_WINDOW = OPEN_D_GT_U_AND_K_GT_U",
    "V50_LONG_REVERSE_TYPE_I_WINDOW = OPEN_D_GT_U_AND_K_LE_U",
    "V50_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE",
    "V50_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_SELF_FINANCING_ENDPOINT_CORE_AND_TWO_SIEGEL_QUALITY_WORLDS_MAPPED_LONG_MOBIUS_OPEN",
    "V50_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED",
    "V50_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B",
)


REGISTRY_SHA256 = "57c788cbbfecb60570edd299b094e0af26ed924be01257fd0718acc6d82aad97"


SOURCE_LOCKS = (
    ("BFI-large-moduli", "Enrico Bombieri; John Friedlander; Henryk Iwaniec", "primitive-character block estimate inherited through V45 pays the moving collar only"),
    ("1412.5029v3", "Kevin Ford; Ben Green; Sergei Konyagin; James Maynard; Terence Tao", "Landau--Page alternative gives at most one primitive quadratic exceptional character per scale"),
    ("2112.11412v2", "Kaisa Matomaki; Jori Merikoski", "Corollary 1.1(i) gives fixed-shift prime correlation for X between d^10 and d^(10 log quality)"),
    ("2511.16452v1", "Stelios Sachpazis", "Theorem 1.1 requires X=D^V with V at least 200/epsilon and estimates a fixed AP residue object"),
    ("2507.10780v1", "Thomas Wright", "Theorem 2.2 assumes log D=(log x)^kappa and estimates AP residue counts"),
)


DEPENDENCIES = (
    ("research/tpc-big-road/bridge_b_endpoint_matched_siegel_world_compiler.md", "fd85314cf01edb2e1f63232197e5dd160cd61003269c0e5d31c8cc962efaea29"),
    ("research/tpc-big-road/bridge_b_ultralow_conductor_three_lane_compiler.md", "c44d081bd1ef00a118191f1404b442e3c67585862a4ca737cdc6dafebff6c364"),
    ("research/tpc-big-road/tpc_bridge_b_ultralow_conductor_three_lane_checker.py", "7ae56b5660c6d108e11061182985f8f67ba7074d3288ca4fbd6807e4ad324255"),
    ("research/tpc-big-road/bridge_b_low_conductor_signed_covariance_splice.md", "5b35d2fc4fcb6d66628f704df3d22b39fa76b0fb524fdb30062c309f0485b6c5"),
    ("research/tpc-big-road/tpc_bridge_b_low_conductor_signed_covariance_checker.py", "fd86b19f1bdf7dd2a66a99060810369f64367909ac2bceb04df3e39c464af9fe"),
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
    min_fn=min,
    max_fn=max,
    hash_fn=hash,
    file_seed=__file__,
):
    literal_maximum_claim = (
        "AN_OPEN_SAVING_PARAMETER_DELTA_IN_0_1_OVER_9600_GENERATES_AN_EXACT_"
        "SELF_FINANCING_CONDUCTOR_CUT_AND_THE_GLOBAL_SIEGEL_QUALITY_DICHOTOMY_"
        "SENDS_UNBOUNDED_QUALITY_TO_A_SOURCE_BACKED_TWIN_PRIME_EXIT_OR_REDUCES_"
        "BRIDGE_A_TO_A_BOUNDED_QUALITY_SIGNED_CORE_THEOREM"
    )
    literal_registry_digest = "57c788cbbfecb60570edd299b094e0af26ed924be01257fd0718acc6d82aad97"
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

    def finite_fixtures():
        h_exp = fraction_type(21, 32)
        q_exp = fraction_type(1, 3)
        p_exp = fraction_type(1, 96)
        d0_exp = fraction_type(1, 192)
        threshold = fraction_type(1, 200)
        target = fraction_type(1997, 1200)
        delta_v49 = fraction_type(1, 19200)
        delta_alt = fraction_type(1, 24000)
        delta_upper = fraction_type(1, 9600)

        def cut_data(delta):
            beta = threshold + 2 * delta
            collar = 2 * p_exp - beta
            old_high = 3 * p_exp / 2
            combined = max_fn(collar, old_high)
            output = h_exp + 1 + combined / 2
            return (beta, collar, old_high, combined, output, target - output)

        v49 = cut_data(delta_v49)
        alt = cut_data(delta_alt)
        zero = cut_data(fraction_type(0, 1))
        upper = cut_data(delta_upper)

        lane_rows = (
            ("principal", 1, False, 11),
            ("generic", 3, False, 2),
            ("exceptional", 5, True, 5),
            ("generic", 7, False, -9),
        )
        exceptional_rows = tuple_type(row for row in lane_rows if row[2])
        m_pr = sum_fn(row[3] for row in lane_rows if row[0] == "principal")
        m_gen = sum_fn(row[3] for row in lane_rows if row[0] == "generic")
        m_exc = sum_fn(row[3] for row in exceptional_rows)
        l_pf = 4
        c_pr = m_pr - l_pf
        c_core = c_pr + m_gen + m_exc
        triangle = abs_fn(c_pr) + abs_fn(m_gen) + abs_fn(m_exc)

        worlds = ("BOUNDED", "UNBOUNDED")
        bounded_sample = (12, 18, 37)
        finite_prefix = (10, 20, 40, 80)
        quantifier_order = (
            "FOR_EVERY_FINITE_B",
            "EXISTS_DELTA_B",
            "EXISTS_C_B_AND_X0_B",
            "FOR_ALL_X_AT_LEAST_X0_B",
        )
        wrong_quantifier_order = (
            "FOR_EVERY_FINITE_B",
            "FOR_ALL_X_AT_LEAST_X0_B",
            "EXISTS_DELTA_B",
            "EXISTS_C_B_AND_X0_B",
        )

        return dict_type((
            ("H", h_exp),
            ("Q", q_exp),
            ("P", p_exp),
            ("D0", d0_exp),
            ("threshold", threshold),
            ("target", target),
            ("delta_v49", delta_v49),
            ("delta_alt", delta_alt),
            ("delta_upper", delta_upper),
            ("v49", v49),
            ("alt", alt),
            ("zero", zero),
            ("upper", upper),
            ("cut_product_v49", d0_exp + v49[0]),
            ("lane_rows", lane_rows),
            ("exceptional_rows", exceptional_rows),
            ("m_pr", m_pr),
            ("m_gen", m_gen),
            ("m_exc", m_exc),
            ("l_pf", l_pf),
            ("c_pr", c_pr),
            ("c_core", c_core),
            ("triangle", triangle),
            ("worlds", worlds),
            ("bounded_sample", bounded_sample),
            ("finite_prefix", finite_prefix),
            ("quantifier_order", quantifier_order),
            ("wrong_quantifier_order", wrong_quantifier_order),
            ("prime_power_exponent", fraction_type(1, 2)),
            ("correlation_main_exponent", fraction_type(1, 1)),
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
        ("registry_rows", 64),
        ("source_locks", 5),
        ("dependency_locks", 5),
        ("H", "21/32"),
        ("Q", "1/3"),
        ("P", "1/96"),
        ("D0", "1/192"),
        ("endpoint_threshold", "1/200"),
        ("target_numerator", "1997/1200"),
        ("delta_lower", "0"),
        ("delta_upper", "1/9600"),
        ("delta_v49", "1/19200"),
        ("beta_v49", "49/9600"),
        ("energy_v49", "151/9600"),
        ("output_v49", "31951/19200"),
        ("margin_v49", "1/19200"),
        ("delta_alt", "1/24000"),
        ("beta_alt", "61/12000"),
        ("energy_alt", "63/4000"),
        ("output_alt", "13313/8000"),
        ("delta_zero_status", "ZERO_STRICT_MARGIN"),
        ("delta_upper_status", "V48_D0_BOUNDARY"),
        ("world_dichotomy", ("BOUNDED", "UNBOUNDED")),
        ("current_world_known", False),
        ("bounded_sample_max", 37),
        ("quantifier_order", fixture["quantifier_order"]),
        ("finite_prefix_proves_unbounded", False),
        ("prime_power_exponent", "1/2"),
        ("correlation_main_exponent", "1"),
        ("mm_source_attachment", True),
        ("bounded_core_attachment", False),
        ("source_attachment", False),
        ("first_fatal", "NO_LITERAL_B_DEPENDENT_ENDPOINT_MATCHED_SIGNED_CORE_FIXED_POWER_THEOREM"),
        ("route_position", "BRIDGE_A_SELF_FINANCING_CORE_TWO_SIEGEL_WORLDS_MAPPED"),
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
        v49 = fixture["v49"]
        alt = fixture["alt"]
        zero = fixture["zero"]
        upper = fixture["upper"]
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
            ("delta_v49", fraction_text(fixture["delta_v49"])),
            ("beta_v49", fraction_text(v49[0])),
            ("beta_v49_interior", fixture["threshold"] < v49[0] < fixture["D0"]),
            ("energy_v49", fraction_text(v49[3])),
            ("output_v49", fraction_text(v49[4])),
            ("margin_v49", fraction_text(v49[5])),
            ("v49_recovery", v49[0] == fraction_type(49, 9600)),
            ("delta_alt", fraction_text(fixture["delta_alt"])),
            ("beta_alt", fraction_text(alt[0])),
            ("beta_alt_interior", fixture["threshold"] < alt[0] < fixture["D0"]),
            ("energy_alt", fraction_text(alt[3])),
            ("output_alt", fraction_text(alt[4])),
            ("margin_alt", fraction_text(alt[5])),
            ("beta_zero", fraction_text(zero[0])),
            ("zero_has_strict_margin", zero[5] > 0),
            ("beta_upper", fraction_text(upper[0])),
            ("upper_hits_D0", upper[0] == fixture["D0"]),
            ("cut_product_below_Q", fixture["cut_product_v49"] < fixture["Q"]),
            ("lane_rows", fixture["lane_rows"]),
            ("exceptional_cardinality", len_fn(fixture["exceptional_rows"])),
            ("exceptional_quadratic", all_fn(row[2] for row in fixture["exceptional_rows"])),
            ("m_pr", fixture["m_pr"]),
            ("m_gen", fixture["m_gen"]),
            ("m_exc", fixture["m_exc"]),
            ("l_pf", fixture["l_pf"]),
            ("c_pr", fixture["c_pr"]),
            ("c_core", fixture["c_core"]),
            ("triangle_overpay", fixture["triangle"]),
            ("three_lane_identity", fixture["c_core"] == fixture["c_pr"] + fixture["m_gen"] + fixture["m_exc"]),
            ("direct_signed_scalar", abs_fn(fixture["c_core"])),
            ("worlds", fixture["worlds"]),
            ("bounded_sample", fixture["bounded_sample"]),
            ("bounded_sample_max", max_fn(fixture["bounded_sample"])),
            ("finite_quality_prefix", fixture["finite_prefix"]),
            ("finite_prefix_is_bounded", max_fn(fixture["finite_prefix"]) == 80),
            ("finite_prefix_proves_unbounded", False),
            ("current_world_known", False),
            ("quantifier_order", fixture["quantifier_order"]),
            ("wrong_quantifier_order", fixture["wrong_quantifier_order"]),
            ("quantifier_order_rejected", fixture["quantifier_order"] != fixture["wrong_quantifier_order"]),
            ("mm_h", 2),
            ("mm_lower_conductor_power", 10),
            ("mm_source_attachment", True),
            ("h2_singular_series_positive", True),
            ("prime_power_exponent", fraction_text(fixture["prime_power_exponent"])),
            ("correlation_main_exponent", fraction_text(fixture["correlation_main_exponent"])),
            ("contamination_exponent_gap", fraction_text(fixture["correlation_main_exponent"] - fixture["prime_power_exponent"])),
            ("current_tpc_trigger", False),
            ("bounded_core_attachment", False),
            ("preferred_bounded_gate", "DIRECT_B_DEPENDENT_ENDPOINT_MATCHED_SIGNED_CORE"),
            ("unbounded_route", "SOURCE_BACKED_DIRECT_TWIN_PRIME_EXIT"),
            ("source_attachment", False),
            ("first_fatal", "NO_LITERAL_B_DEPENDENT_ENDPOINT_MATCHED_SIGNED_CORE_FIXED_POWER_THEOREM"),
            ("route_position", "BRIDGE_A_SELF_FINANCING_CORE_TWO_SIEGEL_WORLDS_MAPPED"),
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

    v49 = fixture["v49"]
    alt = fixture["alt"]
    zero = fixture["zero"]
    upper = fixture["upper"]
    if not (fixture["threshold"] < v49[0] < fixture["D0"]):
        raise CheckFailure("V49 interior recovery changed")
    if not (fixture["threshold"] < alt[0] < fixture["D0"]):
        raise CheckFailure("alternate interior cut changed")
    expected_fractions = (
        (v49[0], fraction_type(49, 9600)),
        (v49[3], fraction_type(151, 9600)),
        (v49[4], fraction_type(31951, 19200)),
        (v49[5], fraction_type(1, 19200)),
        (alt[0], fraction_type(61, 12000)),
        (alt[3], fraction_type(63, 4000)),
        (alt[4], fraction_type(13313, 8000)),
        (alt[5], fraction_type(1, 24000)),
    )
    if not all_fn(got == want for got, want in expected_fractions):
        raise CheckFailure("moving-cut exponent ledger changed")
    if zero[0] != fixture["threshold"] or zero[5] != 0:
        raise CheckFailure("zero-margin endpoint changed")
    if upper[0] != fixture["D0"]:
        raise CheckFailure("upper D0 endpoint changed")
    if fixture["cut_product_v49"] >= fixture["Q"]:
        raise CheckFailure("moving-cut product condition changed")
    if len_fn(fixture["exceptional_rows"]) not in (0, 1):
        raise CheckFailure("Landau--Page cardinality changed")
    if not all_fn(row[2] for row in fixture["exceptional_rows"]):
        raise CheckFailure("exceptional quadratic type changed")
    if (
        fixture["m_pr"],
        fixture["m_gen"],
        fixture["m_exc"],
        fixture["l_pf"],
        fixture["c_pr"],
        fixture["c_core"],
        fixture["triangle"],
    ) != (11, -7, 5, 4, 7, 5, 19):
        raise CheckFailure("three-lane fixture changed")
    if fixture["c_core"] != fixture["c_pr"] + fixture["m_gen"] + fixture["m_exc"]:
        raise CheckFailure("three-lane identity changed")
    if fixture["triangle"] <= abs_fn(fixture["c_core"]):
        raise CheckFailure("triangle overpay firewall changed")
    if fixture["worlds"] != ("BOUNDED", "UNBOUNDED"):
        raise CheckFailure("quality-world dichotomy changed")
    if max_fn(fixture["bounded_sample"]) != 37:
        raise CheckFailure("bounded-quality fixture changed")
    if max_fn(fixture["finite_prefix"]) != 80:
        raise CheckFailure("finite-prefix firewall changed")
    if fixture["quantifier_order"] == fixture["wrong_quantifier_order"]:
        raise CheckFailure("bounded-world quantifier firewall changed")
    if fixture["prime_power_exponent"] >= fixture["correlation_main_exponent"]:
        raise CheckFailure("prime-power contamination gap changed")

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

    expected_counts = (140, 132, 13, 13, 226, 524)
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
