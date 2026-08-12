#!/usr/bin/env python3
"""Fail-closed finite checker for the V57 longitudinal-anchor compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever the frozen V57 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "EXACT_LONGITUDINAL_ROOT_ANCHOR_CANCELS_THE_PHYSICAL_MODE_FROM_EVERY_"
    "GATE_A_PREFIX_AND_TRANSFERS_ALL_ENDPOINT_MOTION_TO_ONE_GATE_B_ROW_"
    "BESSEL_THEOREM_PLUS_PAID_ERROR"
)


REGISTRY = (
    "V57_MAXIMUM_CLAIM = EXACT_LONGITUDINAL_ROOT_ANCHOR_CANCELS_THE_PHYSICAL_MODE_FROM_EVERY_GATE_A_PREFIX_AND_TRANSFERS_ALL_ENDPOINT_MOTION_TO_ONE_GATE_B_ROW_BESSEL_THEOREM_PLUS_PAID_ERROR",
    "V57_ROUTE_ADVANCE = YES",
    "V57_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V57_ARITHMETIC_ADVANCE = NO",
    "V57_FIXED_ATOM_CREDIT = 0",
    "V57_STRICT_1_OVER_400 = UNPAID",
    "V57_L2 = NONE",
    "V57_TPC_207_TRIGGER = false",
    "V57_NUMBERED_RELEASE = NO",
    "V57_DERIVATION_STATUS = COHERENT_AFTER_PAIRED_ROW_PREFIX_SUM_LONGITUDINAL_ROOT_ANCHOR_PREFIX_ERROR_PAYMENT_GATE_B_ROW_BESSEL_MAXIMALIZATION_AND_DIRECT_PHYSICAL_READOUT",
    "V57_ASSUMPTION_POLICY = H_FOLD_AND_H_B_RB_REMAIN_CONJECTURAL__EXACT_TRANSFER_RECEIVES_ONLY_L0_ROUTE_CREDIT",
    "V57_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_CONDITIONAL_EXIT__OTHERWISE_V51_FULL_SHELL_ROOT_PLUS_V53_GATE_B_ROW_BESSEL__V56_TREE_AND_V52_PAD_PARALLEL_FALLBACKS",
    "V57_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_ARCHITECTURE__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO",
    "V57_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__T_NUM_1997_OVER_1200",
    "V57_PAIR_ROW = RETAINED_EXACT_V54_NONSQUARE_DIAGONAL_COMPLETED_P_Q",
    "V57_PHYSICAL_ROW = RETAINED_EXACT_V54_FULL_BETA_DIAGONAL_DELETED_C_Q",
    "V57_PAIRED_ROW_DIFFERENCE = RETAINED_EXACT_P_Q_MINUS_C_Q_EQUALS_KAPPA_Q_S_PHYSICAL_MINUS_E_Q",
    "V57_WEIGHTED_PREFIXES = DEFINED_A_Y_C_Y_E_Y_K_Y_WITH_COMMON_Q_WEIGHT",
    "V57_PREFIX_LONGITUDINAL_IDENTITY = PROVED_EXACT_A_Y_MINUS_C_Y_EQUALS_K_Y_S_PHYSICAL_MINUS_E_Y",
    "V57_ROOT_RATIO = DEFINED_R_Y_EQUALS_K_Y_OVER_K_STAR_IN_ZERO_ONE",
    "V57_LONGITUDINAL_ROOT_ANCHOR = PROVED_EXACT_A_Y_MINUS_R_Y_A_STAR_EQUALS_C_Y_MINUS_R_Y_C_STAR_MINUS_E_Y_PLUS_R_Y_E_STAR",
    "V57_PHYSICAL_PREFIX_MODE = PROVED_CANCELS_IDENTICALLY_AFTER_ROOT_ANCHOR",
    "V57_MAXIMAL_TRANSFER_BOUND = PROVED_SUP_A_LE_ABS_A_STAR_PLUS_TWO_SUP_C_PLUS_TWO_SUP_E",
    "V57_CONSECUTIVE_BLOCK_TRANSFER = PROVED_BY_DIFFERENCE_OF_ANCHORED_PREFIXES",
    "V57_WRONG_COUNT_RATIO = NO_GO_DOES_NOT_CANCEL_KAPPA_LONGITUDINAL_MODE",
    "V57_UNIT_OMISSION_PREFIX = PROVED_X_4_OVER_3_PLUS_O1",
    "V57_SQUARE_ROW_PREFIX = PROVED_X_143_OVER_96_PLUS_O1",
    "V57_PREFIX_ERROR_MAXIMUM = PROVED_X_143_OVER_96_PLUS_O1",
    "V57_PREFIX_ERROR_MARGIN = 419_OVER_2400",
    "V57_GATE_B_COLLISION_DIAGONAL = RETAINED_PROVED_X_95_OVER_48_PLUS_O1",
    "V57_GATE_B_ROW_BESSEL = CONJECTURAL_H_B_RB_TAU_B_ON_LITERAL_FULL_BETA_DIAGONAL_DELETED_ROW",
    "V57_GATE_B_PREFIX_CAUCHY = PROVED_UNIFORM_OVER_ALL_ENDPOINTS",
    "V57_GATE_B_MAXIMAL_EXPONENT = 143_OVER_96_PLUS_TAU_B_OVER_2",
    "V57_GATE_B_STRICT_ROW_LOSS = TAU_B_STRICTLY_LESS_THAN_419_OVER_1200",
    "V57_GATE_B_SAVING = ETA_C_LT_419_OVER_2400_MINUS_TAU_B_OVER_2",
    "V57_SELECTED_GATE_B_LOSS = TAU_B_EQUALS_1_OVER_3",
    "V57_SELECTED_GATE_B_MAXIMUM = X_53_OVER_32_PLUS_O1",
    "V57_SELECTED_GATE_B_MARGIN = 19_OVER_2400",
    "V57_EQUALITY_ROW_LOSS = NO_GO_ZERO_FIXED_POWER_MARGIN",
    "V57_GATE_A_ROOT_THEOREM = CONJECTURAL_V51_H_FOLD_ETA_L_ON_MIXED_PLUS_BALANCED_NONSQUARE_ROW",
    "V57_ROOT_PLUS_TRANSVERSE_COMPILER = PROVED_CONDITIONAL_H_FOLD_PLUS_H_B_RB_IMPLIES_ALL_GATE_A_PREFIXES",
    "V57_MAXIMAL_GATE_A_SAVING = ETA_M_LT_MIN_ETA_L_AND_419_OVER_2400_MINUS_TAU_B_OVER_2",
    "V57_FULL_SHELL_KAPPA_MASS = PROVED_X_2_OVER_3_PLUS_O1",
    "V57_DIRECT_PHYSICAL_READOUT = PROVED_EXACT_S_EQUALS_A_STAR_MINUS_C_STAR_PLUS_E_STAR_OVER_K_STAR",
    "V57_GENERAL_PHYSICAL_SAVING = ETA_LT_MIN_ETA_L_AND_419_OVER_2400_MINUS_TAU_B_OVER_2",
    "V57_SELECTED_PHYSICAL_OUTPUT = X_95_OVER_96_PLUS_O1",
    "V57_SELECTED_PHYSICAL_MARGIN = 19_OVER_2400",
    "V57_GATE_B_USAGE = PROVED_EXACTLY_ONCE_ROW_ENERGY_PAYS_BOTH_FULL_SHELL_AND_PREFIX_C",
    "V57_V43_BOUNDARY = BYPASSED_IN_THIS_COMPILER_BY_EXACT_V54_PAIRED_ROW_IDENTITY",
    "V57_V56_TREE = RETAINED_VALID_STRONGER_GATE_A_FALLBACK_NOT_REQUIRED_ON_SELECTED_ROOT_PLUS_ROW_ROUTE",
    "V57_V53_SYMMETRIC_TWO_ROW_BESSEL = RETYPED_STRONGER_THAN_NEEDED_ON_GATE_A_AXIS",
    "V57_V52_PAD = RETAINED_PARALLEL_CONJECTURAL_GATE_A_FALLBACK_NO_CREDIT_SPLICING",
    "V57_PACKAGE_COMPARISON = NONCOMPARABLE_GLOBALLY__WEAKER_GATE_A_ROOT_BUT_STRONGER_GATE_B_ROW_THAN_SCALAR_ONLY",
    "V57_FULL_SHELL_A_ALONE = NO_GO_PREFIXES_AND_PHYSICAL_ENDPOINT_REQUIRE_INDEPENDENT_GATE_B_CONTROL",
    "V57_TRANSVERSE_PROJECTION_ALONE = NO_GO_ANNIHILATES_ARBITRARILY_LARGE_KAPPA_PHYSICAL_MODE",
    "V57_PREFIX_FIXTURE = PROVED_Q_5_7_11_EXACT_TWO_NONTRIVIAL_ENDPOINTS_AND_S_RECOVERY_13",
    "V57_HARPER_BDH = SOURCE_BACKED_ARCHITECTURE_FIXED_SEQUENCE_WRONG_Q_RANGE_AND_Q_DEPENDENT_ROW",
    "V57_LEWKO_LEWKO_VARIATIONAL_BDH = SOURCE_BACKED_ARCHITECTURE_WRONG_INNER_VARIATION_AXIS_AND_LITERAL_ROW",
    "V57_RAMARE_SPECTRAL_LARGE_SIEVE = SOURCE_BACKED_ARCHITECTURE_NONNEGATIVE_QUADRATIC_FORM_WRONG_SIGNED_PACKET",
    "V57_PASCADI_TRIPLY_FACTORABLE_AP = NO_GO_DIRECT_FIXED_PROGRESSION_ARRAYS_NOT_LITERAL_ROW",
    "V57_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_POST_EMITTER_KLOOSTERMAN_CELL_ONLY",
    "V57_DIRECT_PRIMARY_SOURCE_FOR_H_FOLD_OR_H_B_RB = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_12",
    "V57_FIRST_FATAL = NO_PRIMARY_THEOREM_PROVES_EITHER_THE_LITERAL_V51_FULL_SHELL_MIXED_PLUS_BALANCED_FOLD_OR_THE_V53_GATE_B_RESTRICTED_ROW_BESSEL_ENERGY__THE_EXACT_LONGITUDINAL_ANCHOR_DOES_NOT_ESTIMATE_EITHER_PREMISE",
    "V57_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_LONGITUDINAL_ANCHOR_MAXIMAL_TRANSFER_AND_ROOT_PLUS_TRANSVERSE_TWO_PIER_COMPILER",
    "V57_SMALL_PAPER_STATUS = STRUCTURAL_LEMMA_PACKAGE_MATERIALLY_STRENGTHENED__MAIN_SIGNED_ROOT_AND_TRANSVERSE_ROW_THEOREMS_OPEN",
    "V57_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_ROOT_ANCHOR_INSTALLED__FULL_SHELL_FOLD_AND_TRANSVERSE_GATE_B_ROW_BESSEL_ARE_THE_TWO_OPEN_PIERS",
    "V57_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED_NO_ARCHITECTURE_TO_ATTACHMENT_PROMOTION",
    "V57_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_LONGITUDINAL_ROOT_ANCHOR_AND_TRANSVERSE_ROW",
)


REGISTRY_SHA256 = "01d46556527433f0c45680d558bc07c9e8355d610d555eb196984dd8c4e8f87d"


SOURCE_LOCKS = (
    (
        "2412.19644v1",
        "Adam J. Harper",
        "BDH asymptotics concern one fixed sequence in a different modulus range, not the q-dependent literal Gate-B row",
    ),
    (
        "1111.6190v2",
        "Allison Lewko; Mark Lewko",
        "Variational BDH and large-sieve bounds vary an inner coefficient index, not the outer prime-modulus row",
    ),
    (
        "2303.04409v2",
        "Olivier Ramare",
        "The spectral large-sieve form is nonnegative and lacks the signed compensated pair-prime packet",
    ),
    (
        "2505.00653v2",
        "Alexandru Pascadi",
        "Triply well-factorable progression arrays do not equal the occurrence-native q-dependent row",
    ),
    (
        "2607.24311v1",
        "Valentin Blomer; Alexandru Pascadi",
        "The fixed-modulus post-emitter Kloosterman-cell engine proves neither H_fold nor the q-family row energy",
    ),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_longitudinal_anchor_transverse_maximal_transfer.md",
        "85faea9c98ae44c3b04319fc5eef26d3a70a60993782a13a2a2c54a3ef5832b5",
    ),
    (
        "research/tpc-big-road/bridge_b_fold_first_long_mobius_compiler.md",
        "56a3959ca2f7867e370b9ec11d1ad601824297f1b27a713503ac34df13234c73",
    ),
    (
        "research/tpc-big-road/bridge_b_pair_row_bessel_and_symmetric_two_gate_compiler.md",
        "2c3f7e1c661c68104bec3b88c33e223165ff26d328e0b7d6885d4258d2686698",
    ),
    (
        "research/tpc-big-road/bridge_b_paired_row_longitudinal_mode_and_terminal_equivalence.md",
        "9c6646e45ab5de506c07e185efc67a6c2af541f9d8435838a3b913692df2b52f",
    ),
    (
        "research/tpc-big-road/bridge_b_pruned_dyadic_maximal_fold_first_compiler.md",
        "1c88a216d402afddf463826aaf44aafc0e38dd46cef3c18e119890cc83adbd4a",
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
    any_fn=any,
    set_type=set,
    range_fn=range,
    enumerate_fn=enumerate,
    zip_fn=zip,
    sum_fn=sum,
    max_fn=max,
    abs_fn=abs,
    failure_type=CheckFailure,
    file_seed=__file__,
):
    literal_maximum_claim = (
        "EXACT_LONGITUDINAL_ROOT_ANCHOR_CANCELS_THE_PHYSICAL_MODE_FROM_EVERY_"
        "GATE_A_PREFIX_AND_TRANSFERS_ALL_ENDPOINT_MOTION_TO_ONE_GATE_B_ROW_"
        "BESSEL_THEOREM_PLUS_PAID_ERROR"
    )
    literal_registry_digest = (
        "01d46556527433f0c45680d558bc07c9e8355d610d555eb196984dd8c4e8f87d"
    )
    literal_registry = tuple_type(registry_seed)
    literal_sources = tuple_type(source_seed)
    literal_dependencies = tuple_type(dependency_seed)
    repo_root = path_type(file_seed).resolve().parents[2]
    path_is_file = path_type.is_file
    path_read_bytes = path_type.read_bytes
    literal_dependency_paths = tuple_type(
        (relative, repo_root / relative, expected_hash)
        for relative, expected_hash in literal_dependencies
    )
    mutation_labels = []

    if maximum_claim_seed != literal_maximum_claim:
        raise failure_type("maximum-claim seed changed")
    if registry_digest_seed != literal_registry_digest:
        raise failure_type("registry-digest seed changed")

    def canonical_digest(rows):
        return sha256_fn(("\n".join(rows) + "\n").encode("utf-8")).hexdigest()

    def same_exact(got, want):
        if type_fn(got) is not type_fn(want):
            return False
        if type_fn(want) is tuple_type:
            return len_fn(got) == len_fn(want) and all_fn(
                same_exact(g, w) for g, w in zip_fn(got, want)
            )
        if type_fn(want) is dict_type:
            if not all_fn(type_fn(key) is str_type for key in got):
                return False
            if set_type(got) != set_type(want):
                return False
            return all_fn(same_exact(got[key], want[key]) for key in want)
        return got == want

    def validate_registry(candidate):
        if type_fn(candidate) is not tuple_type:
            raise failure_type("registry type changed")
        if not all_fn(type_fn(row) is str_type for row in candidate):
            raise failure_type("registry row type changed")
        if candidate != literal_registry:
            raise failure_type("registry changed")
        if len_fn(candidate) != len_fn(set_type(candidate)):
            raise failure_type("registry rows not unique")
        if canonical_digest(candidate) != literal_registry_digest:
            raise failure_type("registry digest changed")

    def validate_sources(candidate):
        if type_fn(candidate) is not tuple_type:
            raise failure_type("source type changed")
        for row in candidate:
            if type_fn(row) is not tuple_type or len_fn(row) != 3:
                raise failure_type("source row shape changed")
            if not all_fn(type_fn(item) is str_type for item in row):
                raise failure_type("source row type changed")
        if candidate != literal_sources:
            raise failure_type("source locks changed")

    def canonical_file_hash(path):
        return sha256_fn(path_read_bytes(path).replace(b"\r\n", b"\n")).hexdigest()

    def validate_dependencies(candidate):
        if type_fn(candidate) is not tuple_type:
            raise failure_type("dependency type changed")
        for row in candidate:
            if type_fn(row) is not tuple_type or len_fn(row) != 2:
                raise failure_type("dependency row shape changed")
            if not all_fn(type_fn(item) is str_type for item in row):
                raise failure_type("dependency row type changed")
        if candidate != literal_dependencies:
            raise failure_type("dependencies changed")
        for relative, path, expected_hash in literal_dependency_paths:
            if not path_is_file(path):
                raise failure_type("dependency missing: " + relative)
            if canonical_file_hash(path) != expected_hash:
                raise failure_type("dependency hash changed: " + relative)

    def fraction_text(value):
        if value.denominator == 1:
            return str_type(value.numerator)
        return str_type(value.numerator) + "/" + str_type(value.denominator)

    def fraction_tuple(values):
        return tuple_type(fraction_text(value) for value in values)

    def finite_fixtures():
        target = fraction_type(1997, 1200)
        row_diagonal = fraction_type(95, 48)
        base_maximal = fraction_type(1, 2) + row_diagonal / 2
        row_loss_threshold = 2 * (target - base_maximal)
        selected_tau = fraction_type(1, 3)
        selected_maximal = base_maximal + selected_tau / 2
        selected_saving = target - selected_maximal
        physical = selected_maximal - fraction_type(2, 3)
        physical_margin = fraction_type(399, 400) - physical
        error_prefix = fraction_type(143, 96)
        error_margin = target - error_prefix

        if row_loss_threshold != fraction_type(419, 1200):
            raise failure_type("row-loss threshold failed")
        if selected_maximal != fraction_type(53, 32):
            raise failure_type("selected maximal exponent failed")
        if selected_saving != fraction_type(19, 2400):
            raise failure_type("selected saving failed")
        if physical != fraction_type(95, 96):
            raise failure_type("physical exponent failed")
        if physical_margin != fraction_type(19, 2400):
            raise failure_type("physical margin failed")
        if error_margin != fraction_type(419, 2400):
            raise failure_type("prefix-error margin failed")

        qs = (5, 7, 11)
        kappas = tuple_type(fraction_type(q - 2, q - 1) for q in qs)
        scalar = fraction_type(13)
        errors = (fraction_type(2), fraction_type(-1), fraction_type(3))
        c_rows = (fraction_type(4), fraction_type(-5), fraction_type(6))
        p_rows = tuple_type(
            c_rows[i] + kappas[i] * scalar - errors[i] for i in range_fn(3)
        )
        if p_rows != (
            fraction_type(47, 4),
            fraction_type(41, 6),
            fraction_type(147, 10),
        ):
            raise failure_type("paired rows failed")

        def weighted_prefix(rows):
            out = []
            running = fraction_type(0)
            for q, value in zip_fn(qs, rows):
                running += q * value
                out.append(running)
            return tuple_type(out)

        a_pref = weighted_prefix(p_rows)
        c_pref = weighted_prefix(c_rows)
        e_pref = weighted_prefix(errors)
        k_pref = weighted_prefix(kappas)
        if a_pref != (
            fraction_type(235, 4),
            fraction_type(1279, 12),
            fraction_type(16097, 60),
        ):
            raise failure_type("A prefixes failed")
        if c_pref != (fraction_type(20), fraction_type(-15), fraction_type(51)):
            raise failure_type("C prefixes failed")
        if e_pref != (fraction_type(10), fraction_type(3), fraction_type(36)):
            raise failure_type("E prefixes failed")
        if k_pref != (
            fraction_type(15, 4),
            fraction_type(115, 12),
            fraction_type(1169, 60),
        ):
            raise failure_type("K prefixes failed")

        anchored = []
        for i in range_fn(3):
            ratio = k_pref[i] / k_pref[-1]
            lhs = a_pref[i] - ratio * a_pref[-1]
            rhs = (
                c_pref[i]
                - ratio * c_pref[-1]
                - e_pref[i]
                + ratio * e_pref[-1]
            )
            if lhs != rhs:
                raise failure_type("anchor identity failed")
            anchored.append(lhs)
        if tuple_type(anchored) != (
            fraction_type(8315, 1169),
            fraction_type(-29667, 1169),
            fraction_type(0),
        ):
            raise failure_type("anchored values failed")

        recovered = (a_pref[-1] - c_pref[-1] + e_pref[-1]) / k_pref[-1]
        if recovered != scalar:
            raise failure_type("physical recovery failed")

        wrong_ratio = fraction_type(1, 3)
        wrong_lhs = a_pref[0] - wrong_ratio * a_pref[-1]
        wrong_rhs = (
            c_pref[0]
            - wrong_ratio * c_pref[-1]
            - e_pref[0]
            + wrong_ratio * e_pref[-1]
        )
        if wrong_lhs == wrong_rhs:
            raise failure_type("wrong count ratio was accepted")

        return dict_type(
            (
                ("target", target),
                ("row_diagonal", row_diagonal),
                ("base_maximal", base_maximal),
                ("row_loss_threshold", row_loss_threshold),
                ("selected_tau", selected_tau),
                ("selected_maximal", selected_maximal),
                ("selected_saving", selected_saving),
                ("physical", physical),
                ("physical_margin", physical_margin),
                ("error_prefix", error_prefix),
                ("error_margin", error_margin),
                ("kappas", kappas),
                ("p_rows", p_rows),
                ("a_pref", a_pref),
                ("c_pref", c_pref),
                ("e_pref", e_pref),
                ("k_pref", k_pref),
                ("anchored", tuple_type(anchored)),
                ("recovered", recovered),
                ("wrong_ratio_gap", wrong_lhs - wrong_rhs),
            )
        )

    fixture = finite_fixtures()
    first_fatal = (
        "NO_PRIMARY_THEOREM_PROVES_EITHER_THE_LITERAL_V51_FULL_SHELL_MIXED_"
        "PLUS_BALANCED_FOLD_OR_THE_V53_GATE_B_RESTRICTED_ROW_BESSEL_ENERGY__"
        "THE_EXACT_LONGITUDINAL_ANCHOR_DOES_NOT_ESTIMATE_EITHER_PREMISE"
    )
    contract_items = (
        ("maximum_claim", literal_maximum_claim),
        ("route_advance", True),
        ("conditional_bridge_advance", True),
        ("arithmetic_advance", False),
        ("fixed_atom_credit", 0),
        ("strict_1_over_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", False),
        ("numbered_release", "NO"),
        ("registry_rows", 68),
        ("source_locks", 5),
        ("dependency_locks", 5),
        ("anchor_identity", "PROVED_EXACT"),
        ("prefix_error", "143/96"),
        ("row_loss_threshold", "419/1200"),
        ("selected_tau", "1/3"),
        ("selected_maximal", "53/32"),
        ("selected_physical", "95/96"),
        ("selected_margin", "19/2400"),
        ("gate_a_root", "CONJECTURAL_H_FOLD"),
        ("gate_b_row", "CONJECTURAL_H_B_RB"),
        ("direct_source", "NONE"),
        ("first_fatal", first_fatal),
        ("mutation_policy", "ALL_ADVERTISED_EXECUTED"),
    )

    def validate_contract(candidate):
        if not same_exact(candidate, dict_type(contract_items)):
            raise failure_type("contract changed")

    def result_items_base():
        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", True),
            ("conditional_bridge_advance", True),
            ("arithmetic_advance", False),
            ("fixed_atom_credit", 0),
            ("strict_1_over_400", "UNPAID"),
            ("L2", "NONE"),
            ("TPC_207_TRIGGER", False),
            ("numbered_release", "NO"),
            ("registry_rows", len_fn(literal_registry)),
            ("registry_digest", canonical_digest(literal_registry)),
            ("source_locks", len_fn(literal_sources)),
            ("dependency_locks", len_fn(literal_dependencies)),
            ("target", fraction_text(fixture["target"])),
            ("row_diagonal", fraction_text(fixture["row_diagonal"])),
            ("base_maximal", fraction_text(fixture["base_maximal"])),
            ("row_loss_threshold", fraction_text(fixture["row_loss_threshold"])),
            ("selected_tau", fraction_text(fixture["selected_tau"])),
            ("selected_maximal", fraction_text(fixture["selected_maximal"])),
            ("selected_saving", fraction_text(fixture["selected_saving"])),
            ("selected_physical", fraction_text(fixture["physical"])),
            ("physical_margin", fraction_text(fixture["physical_margin"])),
            ("prefix_error", fraction_text(fixture["error_prefix"])),
            ("prefix_error_margin", fraction_text(fixture["error_margin"])),
            ("fixture_kappas", fraction_tuple(fixture["kappas"])),
            ("fixture_p_rows", fraction_tuple(fixture["p_rows"])),
            ("fixture_A_prefix", fraction_tuple(fixture["a_pref"])),
            ("fixture_C_prefix", fraction_tuple(fixture["c_pref"])),
            ("fixture_E_prefix", fraction_tuple(fixture["e_pref"])),
            ("fixture_K_prefix", fraction_tuple(fixture["k_pref"])),
            ("fixture_anchored", fraction_tuple(fixture["anchored"])),
            ("fixture_recovered", fraction_text(fixture["recovered"])),
            ("fixture_wrong_ratio_gap", fraction_text(fixture["wrong_ratio_gap"])),
            ("anchor_identity", "PROVED_EXACT"),
            ("maximalization", "PROVED_CONDITIONAL_ROOT_PLUS_TRANSVERSE"),
            ("gate_a_root", "CONJECTURAL_H_FOLD"),
            ("gate_b_row", "CONJECTURAL_H_B_RB"),
            ("v56_tree", "RETAINED_FALLBACK"),
            ("direct_source", "NONE"),
            ("first_fatal", first_fatal),
        )

    base_items = result_items_base()
    contract_mutations = 3 * len_fn(contract_items) + 1
    registry_mutations = 2 * len_fn(literal_registry) + 2
    source_mutations = 2 * len_fn(literal_sources) + 2
    dependency_mutations = 2 * len_fn(literal_dependencies) + 2
    full_field_count = len_fn(base_items) + 6
    semantic_mutations = 2 * full_field_count + 1
    mutation_actions = (
        contract_mutations
        + registry_mutations
        + source_mutations
        + dependency_mutations
        + semantic_mutations
    )
    count_items = (
        ("contract_mutations", contract_mutations),
        ("registry_mutations", registry_mutations),
        ("source_mutations", source_mutations),
        ("dependency_mutations", dependency_mutations),
        ("semantic_mutations", semantic_mutations),
        ("mutation_actions", mutation_actions),
    )
    expected_items = base_items + count_items

    def validate_result(candidate):
        if not same_exact(candidate, dict_type(expected_items)):
            raise failure_type("result changed")

    def wrong_same_type(value):
        if type_fn(value) is bool_type:
            return not value
        if type_fn(value) is int_type:
            return value + 1
        if type_fn(value) is str_type:
            return value + "__MUTATED"
        if type_fn(value) is tuple_type:
            return value + ("__MUTATED",)
        raise failure_type("unsupported mutation value")

    def wrong_type(value):
        if type_fn(value) is bool_type:
            return int_type(value)
        if type_fn(value) is int_type:
            return str_type(value)
        if type_fn(value) is str_type:
            return (value,)
        if type_fn(value) is tuple_type:
            return list_type(value)
        raise failure_type("unsupported mutation type")

    def must_reject(label, action):
        mutation_labels.append(label)
        try:
            action()
        except failure_type:
            return
        raise failure_type("mutation accepted: " + label)

    def run_contract_mutations():
        for key, value in contract_items:
            missing = dict_type(contract_items)
            del missing[key]
            must_reject(
                "contract-missing-" + key,
                lambda candidate=missing: validate_contract(candidate),
            )
            changed = dict_type(contract_items)
            changed[key] = wrong_same_type(value)
            must_reject(
                "contract-value-" + key,
                lambda candidate=changed: validate_contract(candidate),
            )
            typed = dict_type(contract_items)
            typed[key] = wrong_type(value)
            must_reject(
                "contract-type-" + key,
                lambda candidate=typed: validate_contract(candidate),
            )
        extra = dict_type(contract_items)
        extra["__extra__"] = 1
        must_reject("contract-extra", lambda: validate_contract(extra))

    def run_registry_mutations():
        for index, row in enumerate_fn(literal_registry):
            changed = list_type(literal_registry)
            changed[index] = row + "__MUTATED"
            must_reject(
                "registry-value-" + str_type(index),
                lambda candidate=tuple_type(changed): validate_registry(candidate),
            )
            removed = literal_registry[:index] + literal_registry[index + 1 :]
            must_reject(
                "registry-missing-" + str_type(index),
                lambda candidate=removed: validate_registry(candidate),
            )
        must_reject(
            "registry-outer-type", lambda: validate_registry(list_type(literal_registry))
        )
        typed = list_type(literal_registry)
        typed[0] = 1
        must_reject("registry-row-type", lambda: validate_registry(tuple_type(typed)))

    def run_source_mutations():
        for index, row in enumerate_fn(literal_sources):
            changed = list_type(literal_sources)
            changed[index] = (row[0], row[1], row[2] + "__MUTATED")
            must_reject(
                "source-value-" + str_type(index),
                lambda candidate=tuple_type(changed): validate_sources(candidate),
            )
            typed = list_type(literal_sources)
            typed[index] = (row[0], row[1], 1)
            must_reject(
                "source-type-" + str_type(index),
                lambda candidate=tuple_type(typed): validate_sources(candidate),
            )
        must_reject("source-outer-type", lambda: validate_sources(list_type(literal_sources)))
        must_reject("source-row-shape", lambda: validate_sources((("bad", "row"),)))

    def run_dependency_mutations():
        for index, row in enumerate_fn(literal_dependencies):
            changed = list_type(literal_dependencies)
            changed[index] = (row[0], "0" * 64)
            must_reject(
                "dependency-value-" + str_type(index),
                lambda candidate=tuple_type(changed): validate_dependencies(candidate),
            )
            typed = list_type(literal_dependencies)
            typed[index] = (row[0], 1)
            must_reject(
                "dependency-type-" + str_type(index),
                lambda candidate=tuple_type(typed): validate_dependencies(candidate),
            )
        must_reject(
            "dependency-outer-type",
            lambda: validate_dependencies(list_type(literal_dependencies)),
        )
        must_reject("dependency-row-shape", lambda: validate_dependencies((("bad",),)))

    def run_semantic_mutations():
        for key, value in expected_items:
            changed = dict_type(expected_items)
            changed[key] = wrong_same_type(value)
            must_reject(
                "result-value-" + key,
                lambda candidate=changed: validate_result(candidate),
            )
            typed = dict_type(expected_items)
            typed[key] = wrong_type(value)
            must_reject(
                "result-type-" + key,
                lambda candidate=typed: validate_result(candidate),
            )
        extra = dict_type(expected_items)
        extra["__extra__"] = 1
        must_reject("result-extra", lambda: validate_result(extra))

    def run_check_sealed():
        mutation_labels.clear()
        validate_registry(literal_registry)
        validate_sources(literal_sources)
        validate_dependencies(literal_dependencies)
        validate_contract(dict_type(contract_items))
        run_contract_mutations()
        run_registry_mutations()
        run_source_mutations()
        run_dependency_mutations()
        run_semantic_mutations()
        if len_fn(mutation_labels) != mutation_actions:
            raise failure_type("mutation count changed")
        if len_fn(set_type(mutation_labels)) != mutation_actions:
            raise failure_type("mutation labels not unique")
        if any_fn(type_fn(label) is not str_type for label in mutation_labels):
            raise failure_type("mutation label type changed")
        result = dict_type(expected_items)
        validate_result(result)
        return dict_type(result)

    return run_check_sealed


_TRUSTED_RUN = _make_trusted_runner()
run_check = _TRUSTED_RUN
_FROZEN_RESULT = _TRUSTED_RUN()
_FROZEN_STDOUT = json.dumps(
    _FROZEN_RESULT, sort_keys=True, separators=(",", ":"), ensure_ascii=False
)


def _make_main(
    *,
    trusted_run=_TRUSTED_RUN,
    frozen_stdout=_FROZEN_STDOUT,
    tuple_type=tuple,
    str_type=str,
    type_fn=type,
    len_fn=len,
    all_fn=all,
    print_fn=print,
    failure_type=CheckFailure,
):
    def sealed(*argv_objects):
        if len_fn(argv_objects) != 1:
            raise failure_type("explicit --check is required")
        args = argv_objects[0]
        if type_fn(args) is not tuple_type:
            raise failure_type("explicit --check is required")
        if not all_fn(type_fn(item) is str_type for item in args):
            raise failure_type("explicit --check is required")
        if args != ("--check",):
            raise failure_type("explicit --check is required")
        trusted_run()
        print_fn(frozen_stdout)
        return 0

    return sealed


main = _make_main()


if __name__ == "__main__":
    try:
        raise SystemExit(main(tuple(sys.argv[1:])))
    except CheckFailure as exc:
        print("CheckFailure: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
