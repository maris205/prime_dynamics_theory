#!/usr/bin/env python3
"""Fail-closed finite checker for the V51 fold-first pair compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever the frozen V51 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "EXACT_FOLD_FIRST_UNORDERED_PAIR_DIAGONAL_COMPLETED_EMITTER_REPRESENTS_THE_V43_"
    "GATE_A_NUMERATOR_UP_TO_PAID_ERRORS_AND_REDUCES_MIXED_PLUS_BALANCED_LONG_"
    "MOBIUS_TO_ONE_CONJECTURAL_SIGNED_THEOREM"
)


REGISTRY = (
    "V51_MAXIMUM_CLAIM = EXACT_FOLD_FIRST_UNORDERED_PAIR_DIAGONAL_COMPLETED_EMITTER_REPRESENTS_THE_V43_GATE_A_NUMERATOR_UP_TO_PAID_ERRORS_AND_REDUCES_MIXED_PLUS_BALANCED_LONG_MOBIUS_TO_ONE_CONJECTURAL_SIGNED_THEOREM",
    "V51_ROUTE_ADVANCE = YES",
    "V51_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V51_ARITHMETIC_ADVANCE = NO",
    "V51_FIXED_ATOM_CREDIT = 0",
    "V51_STRICT_1_OVER_400 = UNPAID",
    "V51_L2 = NONE",
    "V51_TPC_207_TRIGGER = false",
    "V51_NUMBERED_RELEASE = NO",
    "V51_DERIVATION_STATUS = COHERENT_AFTER_UNORDERED_FOLD_RANK_TWO_NUMERATOR_ABEL_COMPILER_DIAGONAL_COMPLETED_CROSSWALK_AND_CHARACTER_FOURIER_EMITTER",
    "V51_ASSUMPTION_POLICY = FOLD_FIRST_MIXED_PLUS_BALANCED_BOUND_IS_CONJECTURAL__LOCAL_SPECTRAL_RESULTS_ARE_SOURCE_BACKED_CONDITIONAL__ORIENTATION_FIRST_TRIANGLE_IS_NO_GO",
    "V51_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_CONDITIONAL_EXIT__OTHERWISE_FOLD_FIRST_GATE_A_WHOLE_OBJECT__V42_GATE_B__V43_JOIN__DYNAMICS_RESERVE",
    "V51_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO",
    "V51_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__Y0_31_OVER_96",
    "V51_ORDERED_PROPER_FACTOR_IDENTITY = RETAINED_EXACT_FROM_V43",
    "V51_FOLDED_NONSQUARE_IDENTITY = PROVED_EXACT_TWO_ORIENTATION_SUM",
    "V51_FOLDED_SQUARE_IDENTITY = PROVED_EXACT_MU_S_OVER_2",
    "V51_U_SQUARED_SUPPORT = PROVED_X_133_OVER_200_LT_X_OVER_2",
    "V51_MIXED_PAIR_NUMERATOR = PROVED_EXACT_MU_L_MINUS_MU_S_TIMES_LOG_S",
    "V51_BALANCED_PAIR_NUMERATOR = PROVED_EXACT_MU_S_LOG_L_PLUS_MU_L_LOG_S",
    "V51_PAIR_NUMERATOR_SEPARATION_RANK = PROVED_AT_MOST_TWO_BEFORE_PRODUCT_LOG_DENOMINATOR",
    "V51_PRODUCT_LOG_DENOMINATOR = PROVED_EXACT_ONE_DIMENSIONAL_ABEL_COMPILER",
    "V51_PAIR_DIAGONAL_COMPLETED_ROW = DEFINED_WITH_DIAGONAL_AND_LITERAL_PHYSICAL_DATA",
    "V51_PAIR_ROW_CROSSWALK = PROVED_EXACT_F_Q_EQUALS_S_Q_PLUS_C_Q_ZERO_TIMES_S_Q_UNIT",
    "V51_PAIR_SCALAR_CROSSWALK = PROVED_F_EQUALS_C_PLUS_B_Q_S_PHYSICAL_PLUS_UNIT_ERROR",
    "V51_PAIR_TO_V43_GATE_A = PROVED_UP_TO_X_79_OVER_48_PLUS_EPSILON_X_4_OVER_3_AND_X_1_ERRORS",
    "V51_UNIT_OMISSION = RETAINED_PAID_X_4_OVER_3_PLUS_O1",
    "V51_SHELL_FREEZE_ERROR = RETAINED_PAID_X_79_OVER_48_PLUS_EPSILON_PLUS_O1",
    "V51_NONPRINCIPAL_CHARACTER_PROJECTOR = PROVED_EXACT_FOR_UNIT_RESIDUES",
    "V51_FOURIER_KERNEL_SEPARATION = PROVED_EXACT_FROM_PSI_TRANSFORM_CONVENTION",
    "V51_PAIR_CHARACTER_FOURIER_EMITTER = PROVED_EXACT_ONE_OUTER_SIGNED_AGGREGATE",
    "V51_LITERAL_DATA_RETENTION = PROVED_COMMON_Q_SHELL_W_HARD_PRODUCT_SHELL_SIGNS_PHYSICAL_UNIT_RESTRICTIONS_AND_ZERO_AXIS",
    "V51_PAIR_LANE_SPLIT = PROVED_EXACT_MIXED_PLUS_BALANCED_PLUS_SQUARE",
    "V51_SQUARE_SCALAR_PAYMENT = RETAINED_X_143_OVER_96_PLUS_O1",
    "V51_SQUARE_MARGIN_TO_TARGET = 419_OVER_2400",
    "V51_FOLD_FIRST_WHOLE_OBJECT_GATE = CONJECTURAL_H_FOLD_ETA_L",
    "V51_FOLD_FIRST_GATE_IMPLIES_V43_GATE_A = PROVED_CONDITIONAL_WITH_PAID_ERROR_MARGINS",
    "V51_FOLD_FIRST_BYPASS = SELECTED_BROAD_ALTERNATIVE_TO_SEQUENTIAL_BOUNDED_CORE_REVERSE_TYPE_I_AND_BALANCED_TYPE_II",
    "V51_BOUNDED_QUALITY_CORE = RETAINED_V50_CONJECTURAL_ALTERNATIVE",
    "V51_BOUNDED_QUALITY_POINTWISE_POWER = NO_GO_CONSTANT_RELATIVE_DECAY_NOT_X_POWER",
    "V51_SEMIPRIME_FOLD_CANCELLATION = PROVED_EXACT_ZERO_WITH_NONZERO_ORIENTATION_ABSOLUTE_MASS",
    "V51_ORIENTATION_SUPPORT_MISMATCH = PROVED_FINITE_6_10_Q11_H50_LENGTHS_1_AND_2",
    "V51_ORIENTATION_FIRST_POISSON = NO_GO_DESTROYS_EXACT_FOLD_BEFORE_OUTER_ABSOLUTE",
    "V51_POST_TRANSFORM_ORIENTATION_REASSEMBLY = NO_GO_NO_TERMWISE_RECOVERY_OF_FOLDED_ZERO",
    "V51_GENERIC_CHARACTER_LARGE_SIEVE = PROVED_CEILING_X_2_PLUS_O1",
    "V51_GENERIC_CHARACTER_LARGE_SIEVE_DEFICIT = 403_OVER_1200",
    "V51_BLOMER_PASCADI_FIXED_MODULUS_CELL = SOURCE_BACKED_CONDITIONAL_C_MINUS_1_OVER_32_CRITICAL_SAVING",
    "V51_PASCADI_HORIZONTAL_EXCEPTIONAL_SIEVE = SOURCE_BACKED_CONDITIONAL_AFTER_LITERAL_PAIR_EMITTER_AND_NORM",
    "V51_WRIGHT_UNBALANCED_CONVOLUTION = NO_GO_SIEGEL_WALFISZ_SHORT_SEQUENCE_AND_WRONG_JOINT_OBJECT",
    "V51_MILICEVIC_QIN_WU_FIXED_MODULUS = NO_GO_POST_TRANSFORM_CELL_WITHOUT_COMMON_Q_PAIR_EMITTER_OR_REASSEMBLY",
    "V51_DONG_ROBLES_ZEINDLER_2601_00292 = NO_GO_WITHDRAWN_MISSING_L_SQUARED_FACTOR",
    "V51_DIRECT_PRIMARY_SOURCE_FOR_H_FOLD = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11",
    "V51_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_THE_FOLD_FIRST_MIXED_PLUS_BALANCED_PAIR_NATIVE_GATE_A_AGGREGATE_WITH_PHYSICAL_W_AND_ONE_OUTER_SIGN_AT_FIXED_POWER",
    "V51_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE",
    "V51_TWO_GATE_COMPILER = RETAINED_V43_GATE_A_AND_GATE_B",
    "V51_TWO_GATE_MARGIN = MIN_ETA_L_ETA_B_419_OVER_2400_19_OVER_2400_AND_11_OVER_600_MINUS_EPSILON",
    "V51_PAPER_CANDIDATE_LEDGER = CREATED_PARALLEL_PROVED_CONDITIONAL_CONJECTURAL_NO_GO_TRACK",
    "V51_SMALL_PAPER_STATUS = UNNUMBERED_OUTLINE_ONLY_NO_STANDALONE_THEOREM_PACKAGE_YET",
    "V51_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_FOLD_FIRST_PAIR_NATIVE_GATE_A_MAPPED_ARITHMETIC_BOUND_OPEN",
    "V51_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED",
    "V51_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B",
)


REGISTRY_SHA256 = "471b54e18b543252f2e5df5919bf96a859ed849df3e6af2762fe19e6d4adff92"


SOURCE_LOCKS = (
    (
        "2607.24311v1",
        "Valentin Blomer; Alexandru Pascadi",
        "Theorem 1.1 is a fixed-modulus bilinear Kloosterman-sum cell with c^(-1/32+o(1)) saving at critical length",
    ),
    (
        "2404.04239v3",
        "Alexandru Pascadi",
        "exceptional-form large sieves accept sparse-Fourier sequences after a literal emitter and norm are supplied",
    ),
    (
        "2604.25177v2",
        "Thomas Wright",
        "unbalanced convolution theorem requires a Siegel--Walfisz short sequence and does not accept the literal pair-physical aggregate",
    ),
    (
        "2511.07550v1",
        "Djordje Milicevic; Xinhua Qin; Xiaosheng Wu",
        "bilinear Kloosterman theorem is fixed-modulus and post-transform",
    ),
    (
        "2601.00292v2",
        "Anji Dong; Nicolas Robles; Dirk Zeindler",
        "withdrawn after an omitted L^2 factor changed L^5 to L^7 and removed the claimed improvement",
    ),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_fold_first_long_mobius_compiler.md",
        "56a3959ca2f7867e370b9ec11d1ad601824297f1b27a713503ac34df13234c73",
    ),
    (
        "research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md",
        "fd02eaf5504b7a7c2182a8a045b9ec03488ef72ef7b88e750ba781163c10525a",
    ),
    (
        "research/tpc-big-road/bridge_b_endpoint_matched_siegel_world_compiler.md",
        "fd85314cf01edb2e1f63232197e5dd160cd61003269c0e5d31c8cc962efaea29",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_proper_factor_poisson_transference_checker.py",
        "ff48df45275588f6f27572962dd565db1d8e4475daa6d52c2b382ad068d1ab76",
    ),
    (
        "research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md",
        "8ffa832297c7c7f1926f158487ee7b68a71249f95b80b8e2218056c844f2a925",
    ),
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
    sorted_fn=sorted,
    hash_fn=hash,
    file_seed=__file__,
):
    literal_maximum_claim = (
        "EXACT_FOLD_FIRST_UNORDERED_PAIR_DIAGONAL_COMPLETED_EMITTER_REPRESENTS_THE_V43_"
        "GATE_A_NUMERATOR_UP_TO_PAID_ERRORS_AND_REDUCES_MIXED_PLUS_BALANCED_LONG_"
        "MOBIUS_TO_ONE_CONJECTURAL_SIGNED_THEOREM"
    )
    literal_registry_digest = "471b54e18b543252f2e5df5919bf96a859ed849df3e6af2762fe19e6d4adff92"
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

    def mobius(n):
        if type_fn(n) is not int_type or n < 1:
            raise CheckFailure("mobius input changed")
        m = n
        parity = 0
        p = 2
        while p * p <= m:
            if m % p == 0:
                m //= p
                if m % p == 0:
                    return 0
                parity += 1
                while m % p == 0:
                    m //= p
            p += 1
        if m > 1:
            parity += 1
        return -1 if parity % 2 else 1

    def vector(items):
        combined = {}
        for label, coefficient in items:
            combined[label] = combined.get(label, fraction_type(0, 1)) + coefficient
        return tuple_type(
            (label, combined[label])
            for label in sorted_fn(combined)
            if combined[label] != 0
        )

    def mixed_ordered(s, ell):
        return (
            vector((("log_" + str_type(s), -mobius(s)),)),
            vector((("log_" + str_type(s), mobius(ell)),)),
        )

    def folded_numerator(s, ell, cutoff):
        if not (1 < s < ell):
            raise CheckFailure("pair order changed")
        if s <= cutoff:
            return vector((("log_" + str_type(s), mobius(ell) - mobius(s)),))
        return vector(
            (
                ("log_" + str_type(ell), mobius(s)),
                ("log_" + str_type(s), mobius(ell)),
            )
        )

    def add_vectors(left, right):
        return vector(left + right)

    def cprime_q3(u, t):
        if u % 3 == 0 or t % 3 == 0:
            raise CheckFailure("q3 nonunit entered")
        return fraction_type(1, 2) if u % 3 == t % 3 else fraction_type(-1, 2)

    def finite_fixtures():
        target = fraction_type(1997, 1200)
        h_exp = fraction_type(21, 32)
        q_exp = fraction_type(1, 3)
        u_exp = fraction_type(133, 400)
        y0_exp = h_exp - q_exp
        transition_dual = u_exp + q_exp - h_exp
        balanced_dual = fraction_type(1, 2) + q_exp - h_exp
        square_output = fraction_type(143, 96)
        square_margin = target - square_output
        generic_ceiling = fraction_type(2, 1)
        generic_deficit = generic_ceiling - target
        v43_shell_margin = target - fraction_type(79, 48)
        v35_margin = target - fraction_type(53, 32)
        physical_target = target - fraction_type(2, 3)

        pair_23_ordered = mixed_ordered(2, 3)
        pair_23_folded = folded_numerator(2, 3, 4)
        pair_610_ordered = mixed_ordered(6, 10)
        pair_610_folded = folded_numerator(6, 10, 7)
        pair_26 = folded_numerator(2, 6, 4)
        pair_57 = folded_numerator(5, 7, 4)

        beta = ((4, 2), (5, -1))
        weight = ((4, 3), (5, 7))
        offdiag = fraction_type(0, 1)
        diagonal = fraction_type(0, 1)
        for t, beta_t in beta:
            for u, weight_u in weight:
                value = fraction_type(beta_t * weight_u, 1) * cprime_q3(u, t)
                if u == t:
                    diagonal += value
                else:
                    offdiag += value
        full = offdiag + diagonal
        unit_scalar = sum_fn(
            beta_t * dict_type(weight)[t] for t, beta_t in beta
        )

        abel_a = (
            fraction_type(2, 1),
            fraction_type(-3, 1),
            fraction_type(5, 1),
        )
        abel_f = (
            fraction_type(1, 2),
            fraction_type(1, 3),
            fraction_type(1, 5),
        )
        cumulative = (
            abel_a[0],
            abel_a[0] + abel_a[1],
            sum_fn(abel_a),
        )
        abel_lhs = sum_fn(a * f for a, f in zip_fn(abel_a, abel_f))
        abel_rhs = (
            cumulative[2] * abel_f[2]
            + cumulative[0] * (abel_f[0] - abel_f[1])
            + cumulative[1] * (abel_f[1] - abel_f[2])
        )

        quality_exponents = tuple_type(
            fraction_type(1, 10 * n) for n in (10, 100, 1000)
        )

        return dict_type(
            (
                ("target", target),
                ("H", h_exp),
                ("Q", q_exp),
                ("U", u_exp),
                ("Y0", y0_exp),
                ("transition_dual", transition_dual),
                ("balanced_dual", balanced_dual),
                ("square_output", square_output),
                ("square_margin", square_margin),
                ("generic_ceiling", generic_ceiling),
                ("generic_deficit", generic_deficit),
                ("v43_shell_margin", v43_shell_margin),
                ("v35_margin", v35_margin),
                ("physical_target", physical_target),
                ("pair_23_ordered", pair_23_ordered),
                ("pair_23_folded", pair_23_folded),
                ("pair_610_ordered", pair_610_ordered),
                ("pair_610_folded", pair_610_folded),
                ("pair_26", pair_26),
                ("pair_57", pair_57),
                ("square_6", fraction_type(mobius(6), 2)),
                ("support_short", (6 * 11) // 50),
                ("support_long", (10 * 11) // 50),
                ("character_same", cprime_q3(1, 1)),
                ("character_different", cprime_q3(1, 2)),
                ("offdiag", offdiag),
                ("diagonal", diagonal),
                ("full", full),
                ("unit_scalar", unit_scalar),
                ("abel_lhs", abel_lhs),
                ("abel_rhs", abel_rhs),
                ("quality_exponents", quality_exponents),
            )
        )

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
        ("paper_ledger_path", literal_dependencies[4][0]),
        ("registry_sha256", literal_registry_digest),
        ("registry_rows", 61),
        ("source_locks", 5),
        ("dependency_locks", 5),
        ("claim_classes", ("PROVED", "SOURCE_BACKED_CONDITIONAL", "CONJECTURAL", "NO_GO")),
        ("target_numerator", "1997/1200"),
        ("Y0", "31/96"),
        ("transition_dual", "23/2400"),
        ("balanced_dual", "17/96"),
        ("square_output", "143/96"),
        ("square_margin", "419/2400"),
        ("generic_character_ceiling", "2"),
        ("generic_character_deficit", "403/1200"),
        ("pair_emitter_exact", True),
        ("fold_theorem_attachment", False),
        ("bounded_quality_pointwise_power", False),
        ("blomer_pascadi_cell_attachment", True),
        ("drz_claim_usable", False),
        ("gate_b_attachment", False),
        ("first_fatal", "NO_LITERAL_FOLD_FIRST_PAIR_NATIVE_FIXED_POWER_THEOREM"),
        ("route_position", "BRIDGE_A_FOLD_FIRST_PAIR_NATIVE_GATE_A_MAPPED"),
    )
    expected_contract = dict_type(contract_items)

    def validate_contract(candidate):
        if not same_exact(candidate, expected_contract):
            raise CheckFailure("contract changed")

    def fraction_text(value):
        if value.denominator == 1:
            return str_type(value.numerator)
        return str_type(value.numerator) + "/" + str_type(value.denominator)

    def vector_text(value):
        return tuple_type((label, fraction_text(coefficient)) for label, coefficient in value)

    def vector_pair_text(value):
        return tuple_type(vector_text(row) for row in value)

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
            ("claim_classes", expected_contract["claim_classes"]),
            ("target_numerator", fraction_text(fixture["target"])),
            ("H", fraction_text(fixture["H"])),
            ("Q", fraction_text(fixture["Q"])),
            ("U", fraction_text(fixture["U"])),
            ("Y0", fraction_text(fixture["Y0"])),
            ("transition_dual", fraction_text(fixture["transition_dual"])),
            ("balanced_dual", fraction_text(fixture["balanced_dual"])),
            ("square_output", fraction_text(fixture["square_output"])),
            ("square_margin", fraction_text(fixture["square_margin"])),
            ("generic_character_ceiling", fraction_text(fixture["generic_ceiling"])),
            ("generic_character_deficit", fraction_text(fixture["generic_deficit"])),
            ("v43_shell_margin", fraction_text(fixture["v43_shell_margin"])),
            ("v35_margin", fraction_text(fixture["v35_margin"])),
            ("physical_target", fraction_text(fixture["physical_target"])),
            ("pair_23_ordered", vector_pair_text(fixture["pair_23_ordered"])),
            ("pair_23_folded", vector_text(fixture["pair_23_folded"])),
            ("pair_23_orientation_sum", vector_text(add_vectors(*fixture["pair_23_ordered"]))),
            ("pair_610_ordered", vector_pair_text(fixture["pair_610_ordered"])),
            ("pair_610_folded", vector_text(fixture["pair_610_folded"])),
            ("pair_610_orientation_sum", vector_text(add_vectors(*fixture["pair_610_ordered"]))),
            ("pair_26", vector_text(fixture["pair_26"])),
            ("pair_57", vector_text(fixture["pair_57"])),
            ("square_6", fraction_text(fixture["square_6"])),
            ("orientation_support", (fixture["support_short"], fixture["support_long"])),
            ("character_projector", (
                fraction_text(fixture["character_same"]),
                fraction_text(fixture["character_different"]),
            )),
            ("offdiag_row", fraction_text(fixture["offdiag"])),
            ("diagonal_return", fraction_text(fixture["diagonal"])),
            ("diagonal_completed_row", fraction_text(fixture["full"])),
            ("unit_scalar", fixture["unit_scalar"]),
            ("row_crosswalk", fixture["full"] == fixture["offdiag"] + fraction_type(1, 2) * fixture["unit_scalar"]),
            ("abel_lhs", fraction_text(fixture["abel_lhs"])),
            ("abel_rhs", fraction_text(fixture["abel_rhs"])),
            ("abel_identity", fixture["abel_lhs"] == fixture["abel_rhs"]),
            ("quality_exponents", tuple_type(fraction_text(v) for v in fixture["quality_exponents"])),
            ("quality_power_tends_to_zero", fixture["quality_exponents"][0] > fixture["quality_exponents"][1] > fixture["quality_exponents"][2]),
            ("pair_emitter_exact", True),
            ("fold_theorem_attachment", False),
            ("bounded_quality_pointwise_power", False),
            ("blomer_pascadi_cell_attachment", True),
            ("pascadi_horizontal_attachment", False),
            ("wright_direct_attachment", False),
            ("mqw_direct_attachment", False),
            ("drz_withdrawn", True),
            ("drz_claim_usable", False),
            ("gate_b_attachment", False),
            ("paper_candidate_status", "OUTLINE_ONLY"),
            ("source_attachment", False),
            ("first_fatal", "NO_LITERAL_FOLD_FIRST_PAIR_NATIVE_FIXED_POWER_THEOREM"),
            ("route_position", "BRIDGE_A_FOLD_FIRST_PAIR_NATIVE_GATE_A_MAPPED"),
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

    if fixture["Y0"] != fraction_type(31, 96):
        raise CheckFailure("Y0 exponent changed")
    if fixture["transition_dual"] != fraction_type(23, 2400):
        raise CheckFailure("transition dual exponent changed")
    if fixture["balanced_dual"] != fraction_type(17, 96):
        raise CheckFailure("balanced dual exponent changed")
    if fixture["square_margin"] != fraction_type(419, 2400):
        raise CheckFailure("square margin changed")
    if fixture["generic_deficit"] != fraction_type(403, 1200):
        raise CheckFailure("generic character deficit changed")
    if fixture["physical_target"] != fraction_type(399, 400):
        raise CheckFailure("physical endpoint changed")
    if fixture["pair_23_folded"] or add_vectors(*fixture["pair_23_ordered"]):
        raise CheckFailure("2x3 fold cancellation changed")
    if fixture["pair_610_folded"] or add_vectors(*fixture["pair_610_ordered"]):
        raise CheckFailure("6x10 fold cancellation changed")
    if fixture["pair_26"] != (("log_2", fraction_type(2, 1)),):
        raise CheckFailure("2x6 mixed fold changed")
    if fixture["pair_57"] != (
        ("log_5", fraction_type(-1, 1)),
        ("log_7", fraction_type(-1, 1)),
    ):
        raise CheckFailure("5x7 balanced fold changed")
    if fixture["square_6"] != fraction_type(1, 2):
        raise CheckFailure("square coefficient changed")
    if (fixture["support_short"], fixture["support_long"]) != (1, 2):
        raise CheckFailure("orientation support mismatch changed")
    if (fixture["character_same"], fixture["character_different"]) != (
        fraction_type(1, 2),
        fraction_type(-1, 2),
    ):
        raise CheckFailure("q3 character projector changed")
    if (
        fixture["offdiag"],
        fixture["diagonal"],
        fixture["full"],
        fixture["unit_scalar"],
    ) != (
        fraction_type(-11, 2),
        fraction_type(-1, 2),
        fraction_type(-6, 1),
        -1,
    ):
        raise CheckFailure("diagonal-completed row fixture changed")
    if fixture["full"] != fixture["offdiag"] + fraction_type(1, 2) * fixture["unit_scalar"]:
        raise CheckFailure("row crosswalk changed")
    if fixture["abel_lhs"] != fixture["abel_rhs"] or fixture["abel_lhs"] != 1:
        raise CheckFailure("Abel fixture changed")
    if not (
        fixture["quality_exponents"][0]
        > fixture["quality_exponents"][1]
        > fixture["quality_exponents"][2]
        > 0
    ):
        raise CheckFailure("bounded-quality no-power fixture changed")

    contract_mutations = run_contract_mutations()
    registry_mutations = run_registry_mutations()
    source_mutations = run_source_mutations()
    dependency_mutations = run_dependency_mutations()

    result_base = result_items_base()
    provisional = dict_type(
        result_base
        + (
            ("contract_mutations", contract_mutations),
            ("registry_mutations", registry_mutations),
            ("source_mutations", source_mutations),
            ("dependency_mutations", dependency_mutations),
            ("semantic_mutations", 0),
            ("mutation_actions", 0),
        )
    )
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

    final_result = dict_type(
        result_base
        + (
            ("contract_mutations", contract_mutations),
            ("registry_mutations", registry_mutations),
            ("source_mutations", source_mutations),
            ("dependency_mutations", dependency_mutations),
            ("semantic_mutations", semantic_mutations),
            ("mutation_actions", mutation_actions),
        )
    )

    expected_counts = (101, 126, 13, 13, 214, 467)
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
    sorted_fn = sorted
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
            sorted_fn=sorted_fn,
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
