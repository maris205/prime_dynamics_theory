#!/usr/bin/env python3
"""Fail-closed finite checker for the V54 paired-row mode compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever the frozen V54 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "EXACT_PAIRED_ROW_DIAGONALIZATION_PAID_TRANSVERSE_DIFFERENCE_AND_TERMINAL_"
    "LONGITUDINAL_EXTRACTION_RETYPE_SYMMETRIC_TWO_ROW_BESSEL_AS_ONE_ROW_PLUS_"
    "PHYSICAL_ENDPOINT"
)


REGISTRY = (
    "V54_MAXIMUM_CLAIM = EXACT_PAIRED_ROW_DIAGONALIZATION_PAID_TRANSVERSE_DIFFERENCE_AND_TERMINAL_LONGITUDINAL_EXTRACTION_RETYPE_SYMMETRIC_TWO_ROW_BESSEL_AS_ONE_ROW_PLUS_PHYSICAL_ENDPOINT",
    "V54_ROUTE_ADVANCE = YES",
    "V54_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V54_ARITHMETIC_ADVANCE = NO",
    "V54_FIXED_ATOM_CREDIT = 0",
    "V54_STRICT_1_OVER_400 = UNPAID",
    "V54_L2 = NONE",
    "V54_TPC_207_TRIGGER = false",
    "V54_NUMBERED_RELEASE = NO",
    "V54_DERIVATION_STATUS = COHERENT_AFTER_FULL_BETA_SPLIT_ROW_DIFFERENCE_ERROR_PAYMENT_KAPPA_PROJECTION_AND_TWO_OUT_OF_THREE_COMPILER",
    "V54_ASSUMPTION_POLICY = TRANSVERSE_ROW_AND_LONGITUDINAL_SCALAR_ESTIMATES_REMAIN_CONJECTURAL__EXACT_DIAGONALIZATION_RECEIVES_NO_ARITHMETIC_CREDIT",
    "V54_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_CONDITIONAL_EXIT__OTHERWISE_DIRECT_SIGNED_LONGITUDINAL_SCALAR_AND_ONE_COMMON_TRANSVERSE_ROW__V51_V52_V42_FALLBACKS__DYNAMICS_RESERVE",
    "V54_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO",
    "V54_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400",
    "V54_FULL_BETA_SPLIT = RETAINED_EXACT_BETA_EQUALS_BETA_CIRCLE_PLUS_BETA_SQUARE",
    "V54_PAIR_ROW = RETAINED_EXACT_V53_DIAGONAL_COMPLETED_P_Q",
    "V54_PHYSICAL_ROW = RETAINED_EXACT_V40_DIAGONAL_DELETED_C_Q",
    "V54_KERNEL_TOGGLE = RETAINED_EXACT_R_Q_EQUALS_G_Q_PLUS_KAPPA_Q_W",
    "V54_SQUARE_COMPLETED_ROW = DEFINED_EXACT_Y_Q_SQUARE",
    "V54_UNIT_OMISSION_ROW = DEFINED_EXACT_U_Q",
    "V54_UNIT_PHYSICAL_DIAGONAL = PROVED_EXACT_Z_Q_EQUALS_S_PHYSICAL_MINUS_U_Q",
    "V54_PAIRED_ROW_DIFFERENCE = PROVED_EXACT_P_Q_MINUS_C_Q_EQUALS_KAPPA_Q_S_PHYSICAL_MINUS_E_Q",
    "V54_DIFFERENCE_ERROR = PROVED_EXACT_E_Q_EQUALS_KAPPA_Q_U_Q_PLUS_Y_Q_SQUARE",
    "V54_UNIT_OMISSION_ENERGY = PROVED_X_5_OVER_3_PLUS_O1",
    "V54_SQUARE_COMPLETED_ROW_ENERGY = PROVED_X_95_OVER_48_PLUS_O1",
    "V54_DIFFERENCE_ERROR_ENERGY = PROVED_X_95_OVER_48_PLUS_O1",
    "V54_KAPPA_VECTOR_NORM = PROVED_X_1_OVER_3_PLUS_O1",
    "V54_LONGITUDINAL_EXTRACTOR = PROVED_EXACT_S_HAT_EQUALS_INNER_P_MINUS_C_KAPPA_OVER_N_KAPPA",
    "V54_LONGITUDINAL_EXTRACTION_ERROR = PROVED_X_79_OVER_96_PLUS_O1",
    "V54_EXTRACTION_ERROR_MARGIN = 419_OVER_2400",
    "V54_TRANSVERSE_ROW_DIFFERENCE = PROVED_EXACT_PI_PERP_P_MINUS_PI_PERP_C_EQUALS_MINUS_PI_PERP_E",
    "V54_TRANSVERSE_DIFFERENCE_ENERGY = PROVED_X_95_OVER_48_PLUS_O1",
    "V54_TWO_OUT_OF_THREE_COMPILER = PROVED_H_A_PLUS_H_B_IMPLIES_H_S__H_S_PLUS_EITHER_ROW_IMPLIES_THE_OTHER",
    "V54_GENERAL_PHYSICAL_OUTPUT = X_79_OVER_96_PLUS_TAU_OVER_2_PLUS_O1",
    "V54_ROW_LOSS_ENDPOINT = TAU_STRICTLY_LESS_THAN_419_OVER_1200",
    "V54_SELECTED_ONE_Q_LOSS = TAU_EQUALS_1_OVER_3",
    "V54_SELECTED_PHYSICAL_OUTPUT = X_95_OVER_96_PLUS_O1",
    "V54_SELECTED_PHYSICAL_MARGIN = 19_OVER_2400",
    "V54_V43_JOIN = BYPASSED_BY_DIRECT_UNWEIGHTED_KAPPA_PROJECTION_FOR_THIS_CONDITIONAL_COMPILER",
    "V54_LONGITUDINAL_SCALARS = DEFINED_L_A_AND_L_B_AS_KAPPA_PROJECTIONS",
    "V54_LONGITUDINAL_DIFFERENCE = PROVED_EXACT_L_A_MINUS_L_B_EQUALS_N_KAPPA_S_PHYSICAL_MINUS_INNER_E_KAPPA",
    "V54_SELECTED_LONGITUDINAL_SCALE = X_127_OVER_96_PLUS_O1",
    "V54_COMMON_TRANSVERSE_THEOREM = OPEN_ONE_LITERAL_Q_ROW_VARIANCE_SPECIES_SUFFICES_FOR_BOTH_ROWS_UP_TO_PAID_ERROR",
    "V54_LONGITUDINAL_THEOREM = OPEN_TERMINAL_SIGNED_SCALAR_EQUIVALENT_TO_PHYSICAL_ENDPOINT_UP_TO_PAID_ERROR",
    "V54_SYMMETRIC_TWO_ROW_BESSEL = RETYPED_VALID_TERMINAL_PACKAGE_NOT_PREFERRED_PRELIMINARY",
    "V54_CENTERED_MODULUS_BDH_ONLY = NO_GO_CONTROLS_TRANSVERSE_VARIANCE_BUT_DELETES_TERMINAL_LONGITUDINAL_MODE",
    "V54_CHARACTER_DIAGONAL_PACKET = PROVED_EXACT_Z_Q_CIRCLE_INDEPENDENT_OF_CHI_AND_V",
    "V54_TTSTAR_DETERMINANT_CONGRUENCE = PROVED_EXACT_U1_T2_CONGRUENT_U2_T1_MOD_Q",
    "V54_TTSTAR_EXACT_RATIO_RAY = RETAINS_PHYSICAL_U_EQUALS_T_MODE",
    "V54_SPECIAL_L_FUNCTION_FOURTH_MOMENTS = NO_GO_DIRECT_COEFFICIENT_AND_DIAGONAL_CANCELLATION_MISMATCH",
    "V54_HARPER_GENERAL_BDH = NO_GO_DIRECT_FIXED_SEQUENCE_AND_LONGITUDINAL_MODE_MISMATCH",
    "V54_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_TRANSVERSE_CELL_ONLY",
    "V54_RUNBO_LI_LARGE_MODULI = NO_GO_DIRECT_FIXED_RESIDUE_FIRST_MOMENT_AND_PAIRED_ROW_MISMATCH",
    "V54_Q5_Q7_ROW_FIXTURE = PROVED_EXACT_PAIRED_DIFFERENCE_PROJECTION_AND_TRANSVERSE_IDENTITY",
    "V54_TERMINAL_MODE_FIXTURE = PROVED_TRANSVERSE_ZERO_WITH_ARBITRARY_LONGITUDINAL_COORDINATE",
    "V54_V51_DIRECT_SCALAR = RETAINED_WEAKER_CONJECTURAL_GATE_A_ALTERNATIVE",
    "V54_V52_PAD_ROUTE = RETAINED_WEAKER_CONJECTURAL_GATE_A_ALTERNATIVE",
    "V54_V42_MPD_ROUTE = RETAINED_INDEPENDENT_CONJECTURAL_GATE_B_ALTERNATIVE",
    "V54_DIRECT_PRIMARY_SOURCE_FOR_LONGITUDINAL_MODE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11",
    "V54_DIRECT_PRIMARY_SOURCE_FOR_TRANSVERSE_REASSEMBLY = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11",
    "V54_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_THE_KAPPA_LONGITUDINAL_PAIRED_ROW_MODE_EQUIVALENT_UP_TO_PAID_ERROR_TO_THE_PHYSICAL_TWIN_PRIME_RESIDUAL__AND_THE_COMMON_TRANSVERSE_ROW_VARIANCE_REMAINS_INDEPENDENTLY_OPEN",
    "V54_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_PAIRED_ROW_MODE_DIAGONALIZATION_AND_TERMINAL_PACKAGE_FIREWALL",
    "V54_SMALL_PAPER_STATUS = UNNUMBERED_OUTLINE_ONLY_NO_STANDALONE_ASYMPTOTIC_THEOREM",
    "V54_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_PAIRED_ROW_TRANSVERSE_DECK_IDENTIFIED_LONGITUDINAL_TERMINAL_CABLE_OPEN",
    "V54_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED",
    "V54_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B",
)


REGISTRY_SHA256 = "e6a9c1b23060a579f855543f6e3300e35888eb8ca0c915cb7afe99f52f73d17c"


SOURCE_LOCKS = (
    (
        "2412.19644v1",
        "Adam J. Harper",
        "BDH variance for one fixed sequence under additional distribution hypotheses does not control the V54 longitudinal mode",
    ),
    (
        "math/0507150v1",
        "K. Soundararajan",
        "Fourth moment of central Dirichlet L-values has special L-function coefficients rather than the folded pair and prime-hybrid packets",
    ),
    (
        "2004.00504v7",
        "Xiaosheng Wu",
        "Fourth moment over primitive characters and critical-line parameter is an architecture analogue only",
    ),
    (
        "2607.24311v1",
        "Valentin Blomer; Alexandru Pascadi",
        "Fixed-modulus bilinear Kloosterman theorem is a conditional transverse cell engine after a legal emitter and norm",
    ),
    (
        "2602.20917v6",
        "Runbo Li",
        "Fixed-residue prime progression first moments with factorable modulus weights do not accept the paired rows",
    ),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_paired_row_longitudinal_mode_and_terminal_equivalence.md",
        "9c6646e45ab5de506c07e185efc67a6c2af541f9d8435838a3b913692df2b52f",
    ),
    (
        "research/tpc-big-road/bridge_b_pair_row_bessel_and_symmetric_two_gate_compiler.md",
        "2c3f7e1c661c68104bec3b88c33e223165ff26d328e0b7d6885d4258d2686698",
    ),
    (
        "research/tpc-big-road/bridge_b_row_energy_and_packet_route_atlas.md",
        "1f7ae86094a2ff908ba41be6eaefd36bf6959b7e2618e909c59daa44df828ca4",
    ),
    (
        "research/tpc-big-road/bridge_b_fold_first_long_mobius_compiler.md",
        "56a3959ca2f7867e370b9ec11d1ad601824297f1b27a713503ac34df13234c73",
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
    failure_type=CheckFailure,
    file_seed=__file__,
):
    literal_maximum_claim = (
        "EXACT_PAIRED_ROW_DIAGONALIZATION_PAID_TRANSVERSE_DIFFERENCE_AND_TERMINAL_"
        "LONGITUDINAL_EXTRACTION_RETYPE_SYMMETRIC_TWO_ROW_BESSEL_AS_ONE_ROW_PLUS_"
        "PHYSICAL_ENDPOINT"
    )
    literal_registry_digest = "e6a9c1b23060a579f855543f6e3300e35888eb8ca0c915cb7afe99f52f73d17c"
    literal_registry = tuple_type(registry_seed)
    literal_sources = tuple_type(source_seed)
    literal_dependencies = tuple_type(dependency_seed)
    repo_root = path_type(file_seed).resolve().parents[2]
    path_is_file = path_type.is_file
    path_read_bytes = path_type.read_bytes
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
        for relative, expected_hash in candidate:
            path = repo_root / relative
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

    def dot(left, right):
        return sum_fn(a * b for a, b in zip_fn(left, right))

    def finite_fixtures():
        target = fraction_type(399, 400)
        h_exp = fraction_type(21, 32)
        q_exp = fraction_type(1, 3)
        diagonal = 1 + 2 * h_exp - q_exp
        unit_energy = 2 - q_exp
        extraction_error = diagonal / 2 - q_exp / 2
        extraction_margin = target - extraction_error
        tau_endpoint = 2 * extraction_margin
        tau_selected = q_exp
        physical_selected = extraction_error + tau_selected / 2
        physical_margin = target - physical_selected
        longitudinal_selected = (
            diagonal / 2 + tau_selected / 2 + q_exp / 2
        )

        qs = (5, 7)
        ts = (6, 9, 10, 14)
        beta_circle = {
            6: fraction_type(2),
            9: fraction_type(1, 3),
            10: fraction_type(-1),
            14: fraction_type(2),
        }
        beta_square = {
            6: fraction_type(0),
            9: fraction_type(-1, 2),
            10: fraction_type(0),
            14: fraction_type(0),
        }
        beta = {t: beta_circle[t] + beta_square[t] for t in ts}
        weights = {
            6: fraction_type(-1),
            9: fraction_type(3),
            10: fraction_type(2),
            14: fraction_type(-2),
        }
        g_rows = {
            5: {6: fraction_type(7, 4), 9: fraction_type(-1), 14: fraction_type(2)},
            7: {6: fraction_type(1, 2), 9: fraction_type(3), 10: fraction_type(-2)},
        }
        physical = sum_fn(beta[t] * weights[t] for t in ts)
        kappas = {q: fraction_type(q - 2, q - 1) for q in qs}
        pair = {}
        physical_row = {}
        square_row = {}
        omission = {}
        for q in qs:
            units = tuple_type(t for t in ts if t % q != 0)
            r_row = {
                t: g_rows[q][t] + kappas[q] * weights[t] for t in units
            }
            pair[q] = sum_fn(beta_circle[t] * r_row[t] for t in units)
            physical_row[q] = sum_fn(beta[t] * g_rows[q][t] for t in units)
            square_row[q] = sum_fn(beta_square[t] * r_row[t] for t in units)
            omission[q] = sum_fn(
                beta[t] * weights[t] for t in ts if t % q == 0
            )
        difference = {q: pair[q] - physical_row[q] for q in qs}
        error = {q: kappas[q] * omission[q] + square_row[q] for q in qs}
        identity_rhs = {q: kappas[q] * physical - error[q] for q in qs}
        kappa_tuple = tuple_type(kappas[q] for q in qs)
        difference_tuple = tuple_type(difference[q] for q in qs)
        error_tuple = tuple_type(error[q] for q in qs)
        kappa_norm = dot(kappa_tuple, kappa_tuple)
        extracted = dot(difference_tuple, kappa_tuple) / kappa_norm
        error_projection = dot(error_tuple, kappa_tuple) / kappa_norm
        transverse_difference = tuple_type(
            difference[q] - extracted * kappas[q] for q in qs
        )
        transverse_error = tuple_type(
            error[q] - error_projection * kappas[q] for q in qs
        )
        transverse_energy = dot(transverse_difference, transverse_difference)
        error_transverse_energy = dot(transverse_error, transverse_error)

        terminal_t = fraction_type(37)
        terminal_difference = tuple_type(terminal_t * k for k in kappa_tuple)
        terminal_extracted = dot(terminal_difference, kappa_tuple) / kappa_norm
        terminal_transverse = tuple_type(
            terminal_difference[i] - terminal_extracted * kappa_tuple[i]
            for i in range_fn(len_fn(qs))
        )

        if tuple_type(identity_rhs[q] for q in qs) != difference_tuple:
            raise failure_type("paired-row identity fixture failed")
        if extracted - physical != -error_projection:
            raise failure_type("longitudinal extraction fixture failed")
        if transverse_difference != tuple_type(-v for v in transverse_error):
            raise failure_type("transverse identity fixture failed")
        if transverse_energy != error_transverse_energy:
            raise failure_type("transverse energy fixture failed")
        if terminal_extracted != terminal_t or any(terminal_transverse):
            raise failure_type("terminal-mode fixture failed")

        return dict_type(
            (
                ("target", target),
                ("H", h_exp),
                ("Q", q_exp),
                ("diagonal", diagonal),
                ("unit_energy", unit_energy),
                ("extraction_error", extraction_error),
                ("extraction_margin", extraction_margin),
                ("tau_endpoint", tau_endpoint),
                ("tau_selected", tau_selected),
                ("physical_selected", physical_selected),
                ("physical_margin", physical_margin),
                ("longitudinal_selected", longitudinal_selected),
                ("physical", physical),
                ("pair", tuple_type(pair[q] for q in qs)),
                ("physical_row", tuple_type(physical_row[q] for q in qs)),
                ("square_row", tuple_type(square_row[q] for q in qs)),
                ("omission", tuple_type(omission[q] for q in qs)),
                ("difference", difference_tuple),
                ("error", error_tuple),
                ("kappa", kappa_tuple),
                ("kappa_norm", kappa_norm),
                ("extracted", extracted),
                ("transverse", transverse_difference),
                ("transverse_energy", transverse_energy),
                ("terminal", (terminal_extracted, terminal_transverse)),
            )
        )

    fixture = finite_fixtures()

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
        ("registry_rows", 66),
        ("source_locks", 5),
        ("dependency_locks", 4),
        ("selected_tau", "1/3"),
        ("tau_endpoint", "419/1200"),
        ("physical_output", "95/96"),
        ("physical_margin", "19/2400"),
        ("extraction_error", "79/96"),
        ("transverse_status", "PAID_DIFFERENCE_ONLY"),
        ("longitudinal_status", "OPEN_TERMINAL"),
        ("two_row_status", "RETYPED_TERMINAL_PACKAGE"),
        (
            "first_fatal",
            "NO_LITERAL_THEOREM_BOUNDS_THE_KAPPA_LONGITUDINAL_PAIRED_ROW_MODE_EQUIVALENT_UP_TO_PAID_ERROR_TO_THE_PHYSICAL_TWIN_PRIME_RESIDUAL__AND_THE_COMMON_TRANSVERSE_ROW_VARIANCE_REMAINS_INDEPENDENTLY_OPEN",
        ),
        ("direct_source", "NONE"),
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
            ("H", fraction_text(fixture["H"])),
            ("Q", fraction_text(fixture["Q"])),
            ("diagonal", fraction_text(fixture["diagonal"])),
            ("unit_energy", fraction_text(fixture["unit_energy"])),
            ("extraction_error", fraction_text(fixture["extraction_error"])),
            ("extraction_margin", fraction_text(fixture["extraction_margin"])),
            ("tau_endpoint", fraction_text(fixture["tau_endpoint"])),
            ("tau_selected", fraction_text(fixture["tau_selected"])),
            ("physical_output", fraction_text(fixture["physical_selected"])),
            ("physical_margin", fraction_text(fixture["physical_margin"])),
            (
                "longitudinal_scale",
                fraction_text(fixture["longitudinal_selected"]),
            ),
            ("fixture_physical", fraction_text(fixture["physical"])),
            ("fixture_pair", fraction_tuple(fixture["pair"])),
            ("fixture_physical_row", fraction_tuple(fixture["physical_row"])),
            ("fixture_square_row", fraction_tuple(fixture["square_row"])),
            ("fixture_omission", fraction_tuple(fixture["omission"])),
            ("fixture_difference", fraction_tuple(fixture["difference"])),
            ("fixture_error", fraction_tuple(fixture["error"])),
            ("fixture_kappa", fraction_tuple(fixture["kappa"])),
            ("fixture_kappa_norm", fraction_text(fixture["kappa_norm"])),
            ("fixture_extracted", fraction_text(fixture["extracted"])),
            ("fixture_transverse", fraction_tuple(fixture["transverse"])),
            (
                "fixture_transverse_energy",
                fraction_text(fixture["transverse_energy"]),
            ),
            ("terminal_extracted", fraction_text(fixture["terminal"][0])),
            ("terminal_transverse", fraction_tuple(fixture["terminal"][1])),
            ("transverse_status", "PAID_DIFFERENCE_ONLY"),
            ("longitudinal_status", "OPEN_TERMINAL"),
            ("two_row_status", "RETYPED_TERMINAL_PACKAGE"),
            ("direct_source", "NONE"),
            (
                "first_fatal",
                "NO_LITERAL_THEOREM_BOUNDS_THE_KAPPA_LONGITUDINAL_PAIRED_ROW_MODE_EQUIVALENT_UP_TO_PAID_ERROR_TO_THE_PHYSICAL_TWIN_PRIME_RESIDUAL__AND_THE_COMMON_TRANSVERSE_ROW_VARIANCE_REMAINS_INDEPENDENTLY_OPEN",
            ),
        )

    base_items = result_items_base()
    base_result = dict_type(base_items)
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
            must_reject("contract-missing-" + key, lambda c=missing: validate_contract(c))
            changed = dict_type(contract_items)
            changed[key] = wrong_same_type(value)
            must_reject("contract-value-" + key, lambda c=changed: validate_contract(c))
            typed = dict_type(contract_items)
            typed[key] = wrong_type(value)
            must_reject("contract-type-" + key, lambda c=typed: validate_contract(c))
        extra = dict_type(contract_items)
        extra["__extra__"] = 1
        must_reject("contract-extra", lambda: validate_contract(extra))

    def run_registry_mutations():
        for index, row in enumerate_fn(literal_registry):
            changed = list_type(literal_registry)
            changed[index] = row + "__MUTATED"
            must_reject(
                "registry-value-" + str_type(index),
                lambda c=tuple_type(changed): validate_registry(c),
            )
            removed = literal_registry[:index] + literal_registry[index + 1 :]
            must_reject(
                "registry-missing-" + str_type(index),
                lambda c=removed: validate_registry(c),
            )
        must_reject("registry-outer-type", lambda: validate_registry(list_type(literal_registry)))
        typed = list_type(literal_registry)
        typed[0] = 1
        must_reject("registry-row-type", lambda: validate_registry(tuple_type(typed)))

    def run_source_mutations():
        for index, row in enumerate_fn(literal_sources):
            changed = list_type(literal_sources)
            changed[index] = (row[0], row[1], row[2] + "__MUTATED")
            must_reject(
                "source-value-" + str_type(index),
                lambda c=tuple_type(changed): validate_sources(c),
            )
            typed = list_type(literal_sources)
            typed[index] = (row[0], row[1], 1)
            must_reject(
                "source-type-" + str_type(index),
                lambda c=tuple_type(typed): validate_sources(c),
            )
        must_reject("source-outer-type", lambda: validate_sources(list_type(literal_sources)))
        must_reject("source-row-shape", lambda: validate_sources((("bad", "row"),)))

    def run_dependency_mutations():
        for index, row in enumerate_fn(literal_dependencies):
            changed = list_type(literal_dependencies)
            changed[index] = (row[0], "0" * 64)
            must_reject(
                "dependency-value-" + str_type(index),
                lambda c=tuple_type(changed): validate_dependencies(c),
            )
            typed = list_type(literal_dependencies)
            typed[index] = (row[0], 1)
            must_reject(
                "dependency-type-" + str_type(index),
                lambda c=tuple_type(typed): validate_dependencies(c),
            )
        must_reject(
            "dependency-outer-type",
            lambda: validate_dependencies(list_type(literal_dependencies)),
        )
        must_reject(
            "dependency-row-shape",
            lambda: validate_dependencies((("bad",),)),
        )

    def run_semantic_mutations():
        for key, value in expected_items:
            changed = dict_type(expected_items)
            changed[key] = wrong_same_type(value)
            must_reject("result-value-" + key, lambda c=changed: validate_result(c))
            typed = dict_type(expected_items)
            typed[key] = wrong_type(value)
            must_reject("result-type-" + key, lambda c=typed: validate_result(c))
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
