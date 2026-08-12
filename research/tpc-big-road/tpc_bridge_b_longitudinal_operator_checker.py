#!/usr/bin/env python3
"""Fail-closed finite checker for the V55 longitudinal operator compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever the frozen V55 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "EXACT_POINTWISE_REPLICATION_OF_THE_PHYSICAL_SCALAR_ACROSS_EVERY_PRIME_"
    "MODULUS_PLUS_MINIMAX_LINEAR_EXTRACTOR_AND_MODULUS_OPERATOR_TTSTAR_"
    "DICHOTOMY_WITH_MAXIMAL_GATE_A_TRANSFER_INTERFACE"
)


REGISTRY = (
    "V55_MAXIMUM_CLAIM = EXACT_POINTWISE_REPLICATION_OF_THE_PHYSICAL_SCALAR_ACROSS_EVERY_PRIME_MODULUS_PLUS_MINIMAX_LINEAR_EXTRACTOR_AND_MODULUS_OPERATOR_TTSTAR_DICHOTOMY_WITH_MAXIMAL_GATE_A_TRANSFER_INTERFACE",
    "V55_ROUTE_ADVANCE = YES",
    "V55_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V55_ARITHMETIC_ADVANCE = NO",
    "V55_FIXED_ATOM_CREDIT = 0",
    "V55_STRICT_1_OVER_400 = UNPAID",
    "V55_L2 = NONE",
    "V55_TPC_207_TRIGGER = false",
    "V55_NUMBERED_RELEASE = NO",
    "V55_DERIVATION_STATUS = COHERENT_AFTER_POINTWISE_ERROR_PAYMENT_OPERATOR_DICHOTOMY_MINIMAX_EXTRACTION_TTSTAR_FIREWALL_AND_MAXIMAL_ABEL_TRANSFER",
    "V55_ASSUMPTION_POLICY = MAXIMAL_PARTIAL_SHELL_AND_PRE_Q_PACKET_SAVINGS_REMAIN_CONJECTURAL__EXACT_OPERATOR_RESULTS_RECEIVE_NO_ARITHMETIC_CREDIT",
    "V55_SELECTED_RESEARCH_ROUTE = STOP_LONGITUDINAL_QSPACE_PRELIMINARY_ENGINEERING__PIVOT_TO_V51_MAXIMAL_FOLD_FIRST_OR_V52_PAD_FOR_GATE_A_AND_V42_COMMON_TRANSVERSE_FOR_GATE_B__RETAIN_V55_LONGITUDINAL_READOUT_AS_TERMINAL_ONLY",
    "V55_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO",
    "V55_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400",
    "V55_INHERITED_PAIRED_DIFFERENCE = RETAINED_EXACT_D_Q_EQUALS_KAPPA_Q_S_PHYSICAL_MINUS_E_Q",
    "V55_INHERITED_DIFFERENCE_ERROR_ENERGY = RETAINED_PROVED_X_95_OVER_48_PLUS_O1",
    "V55_POINTWISE_UNIT_OMISSION = PROVED_X_2_OVER_3_PLUS_O1_EACH_Q",
    "V55_POINTWISE_SQUARE_COMPLETION = PROVED_X_79_OVER_96_PLUS_O1_EACH_Q",
    "V55_POINTWISE_DIFFERENCE_ERROR = PROVED_X_79_OVER_96_PLUS_O1_EACH_Q",
    "V55_SINGLE_MODULUS_REPLICA = PROVED_EXACT_S_Q_REP_EQUALS_D_Q_OVER_KAPPA_Q_EQUALS_S_PHYSICAL_MINUS_E_Q_OVER_KAPPA_Q",
    "V55_SINGLE_MODULUS_REPLICA_ERROR = PROVED_X_79_OVER_96_PLUS_O1",
    "V55_PAIRWISE_REPLICA_CONSISTENCY = PROVED_X_79_OVER_96_PLUS_O1",
    "V55_SINGLE_Q_DIFFERENCE_THEOREM = RETYPED_TERMINAL_EQUIVALENT_TO_PHYSICAL_ENDPOINT_UP_TO_PAID_ERROR",
    "V55_GENERAL_MODULUS_OPERATOR_IDENTITY = PROVED_EXACT_TD_EQUALS_S_TKAPPA_MINUS_TE",
    "V55_TRANSVERSE_OPERATOR_CASE = PROVED_TKAPPA_ZERO_IMPLIES_TD_EQUALS_MINUS_TE",
    "V55_LONGITUDINAL_OPERATOR_CASE = PROVED_NONZERO_TKAPPA_GIVES_EXACT_PHYSICAL_ESTIMATOR",
    "V55_OPERATOR_ESTIMATOR_ERROR = PROVED_NORM_T_OVER_NORM_TKAPPA_TIMES_NORM_E",
    "V55_OPERATOR_CONDITION_LOWER_BOUND = PROVED_NORM_T_OVER_NORM_TKAPPA_AT_LEAST_ONE_OVER_NORM_KAPPA",
    "V55_LINEAR_UNBIASED_CLASS = DEFINED_INNER_A_KAPPA_EQUALS_ONE",
    "V55_MINIMAX_LINEAR_EXTRACTOR = PROVED_UNIQUE_A_STAR_EQUALS_KAPPA_OVER_N_KAPPA",
    "V55_MINIMAX_WORST_CASE_ERROR = PROVED_NORM_E_OVER_SQRT_N_KAPPA",
    "V55_MINIMAX_EXTRACTION_EXPONENT = PROVED_X_79_OVER_96_PLUS_O1",
    "V55_PSD_TTSTAR_IDENTITY = PROVED_EXACT_QUADRATIC_EXPANSION",
    "V55_PSD_TRANSVERSE_CASE = PROVED_AKAPPA_ZERO_DELETES_PHYSICAL_MODE",
    "V55_PSD_LONGITUDINAL_CASE = PROVED_POSITIVE_KAPPA_ENERGY_IS_TERMINAL_EQUIVALENT",
    "V55_CENTERED_MODULUS_BDH = NO_GO_POST_Q_PRELIMINARY_DELETES_KAPPA_MODE",
    "V55_POST_Q_TTSTAR_SHORTCUT = NO_GO_EITHER_TRANSVERSE_OR_TERMINAL_NO_THIRD_CASE",
    "V55_CHARACTER_FIXED_Q_PACKET = RETAINED_EXACT_NONPRINCIPAL_PRODUCT_PACKET",
    "V55_TTSTAR_EXACT_RATIO_RAY = RETAINED_EXACT_PHYSICAL_U_EQUALS_T_MODE",
    "V55_PRE_Q_COMPRESSION_REQUIREMENT = OPEN_SIGNED_DIAGONAL_PLUS_OFFDIAGONAL_LITERAL_PACKET_THEOREM",
    "V55_MAXIMAL_GATE_A_PARTIAL_SUM = DEFINED_F_OF_Y_EQUALS_SUM_Q_LE_Y_Q_P_Q",
    "V55_MAXIMAL_GATE_A_ABEL_IDENTITY = PROVED_EXACT_LONGITUDINAL_WEIGHT_TRANSFER",
    "V55_MAXIMAL_GATE_A_TRANSFER = PROVED_CONDITIONAL_SUP_F_X_1997_OVER_1200_IMPLIES_L_A_X_1597_OVER_1200",
    "V55_FULL_SHELL_GATE_A_SCALAR = NO_GO_DOES_NOT_CONTROL_LONGITUDINAL_WEIGHTED_SUM",
    "V55_FULL_SHELL_COUNTEREXAMPLE = PROVED_EXACT_ZERO_Q_WEIGHTED_SUM_WITH_NONZERO_KAPPA_WEIGHTED_SUM",
    "V55_MAXIMAL_GATE_A_THEOREM = OPEN_NEW_WHOLE_OBJECT_THEOREM",
    "V55_LONGITUDINAL_PACKET_NATURAL_SCALE = X_4_OVER_3_PLUS_O1",
    "V55_LONGITUDINAL_PACKET_TARGET_SCALE = X_1597_OVER_1200_MINUS_ETA_PLUS_O1",
    "V55_LONGITUDINAL_PACKET_GAP = 1_OVER_400",
    "V55_LONGITUDINAL_ANGULAR_SAVING_LAW = DELTA_B_PLUS_DELTA_W_OVER_2_PLUS_RHO_STRICTLY_GREATER_THAN_1_OVER_400",
    "V55_NARROW_PRIME_SHELL = NO_FREE_EXPONENT_CREDIT_SIGNAL_PACKET_AND_TARGET_SCALE_TOGETHER",
    "V55_MILICEVIC_QIN_WU_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_POST_EMITTER_KLOOSTERMAN_CELL_ONLY",
    "V55_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_POST_EMITTER_KLOOSTERMAN_CELL_ONLY",
    "V55_KERR_SHPARLINSKI_WU_XI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_POST_EMITTER_KLOOSTERMAN_CELL_ONLY",
    "V55_HARPER_GENERAL_BDH = NO_GO_DIRECT_CENTERED_VARIANCE_AND_LONGITUDINAL_MODE_MISMATCH",
    "V55_RUNBO_LI_LARGE_MODULI = NO_GO_DIRECT_PRIME_AP_FIRST_MOMENT_AND_PAIRED_PACKET_MISMATCH",
    "V55_ZHENG_SIMULTANEOUS_AP = NO_GO_DIRECT_SOURCE_SPECIFIC_PROGRESSIONS_AND_COMPENSATED_PACKET_MISMATCH",
    "V55_DONG_ROBLES_ZEINDLER = EXCLUDED_WITHDRAWN_MISSING_L2_FACTOR_NO_THEOREM_CREDIT",
    "V55_DIRECT_PRIMARY_SOURCE_FOR_LONGITUDINAL_PACKET = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_12",
    "V55_Q5_Q7_REPLICA_FIXTURE = PROVED_EXACT_POINTWISE_REPLICATION_AND_PAIRWISE_DIFFERENCE",
    "V55_OPERATOR_DICHOTOMY_FIXTURE = PROVED_EXACT_TRANSVERSE_AND_DIAGONAL_KEEP_CASES",
    "V55_MINIMAX_FIXTURE = PROVED_EXACT_A_STAR_NORM_BEATS_COORDINATE_ESTIMATOR",
    "V55_PSD_TERMINAL_DELETION_FIXTURE = PROVED_EXACT_ARBITRARY_LONGITUDINAL_ZERO_ENERGY",
    "V55_MAXIMAL_ABEL_FIXTURE = PROVED_EXACT_PARTIAL_SUM_IDENTITY_AND_FULL_SHELL_NO_GO",
    "V55_FIRST_FATAL = NO_PRIMARY_THEOREM_CONTROLS_THE_LITERAL_PRE_Q_PROJECTION_SIGNED_DIAGONAL_OFFDIAGONAL_PACKET_OR_THE_V51_MAXIMAL_PARTIAL_PRIME_SHELL__ANY_POST_Q_OPERATOR_RETAINING_KAPPA_IS_TERMINAL_EQUIVALENT_AND_THE_COMMON_TRANSVERSE_THEOREM_REMAINS_OPEN",
    "V55_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_REPLICATION_MINIMAX_OPERATOR_DICHOTOMY_AND_MAXIMAL_SHELL_INTERFACE",
    "V55_SMALL_PAPER_STATUS = STRUCTURAL_LEMMA_PACKAGE_READY_NO_STANDALONE_ASYMPTOTIC_THEOREM",
    "V55_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_LONGITUDINAL_CABLE_RECLASSIFIED_AS_TERMINAL_READOUT__PRE_Q_GATE_A_AND_COMMON_TRANSVERSE_PIERS_OPEN",
    "V55_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED_WITH_WITHDRAWN_SOURCES_EXCLUDED",
    "V55_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_PRE_Q_PIERS_AND_TERMINAL_READOUT",
)


REGISTRY_SHA256 = "fafcbfe7188ca0733c21ade0cc4bae2395444768667a99e07c895c40e87ae97d"


SOURCE_LOCKS = (
    (
        "2511.07550v1",
        "Djordje Milicevic; Xinhua Qin; Xiaosheng Wu",
        "Theorem 1.1 is a fixed-modulus separable bilinear Kloosterman-sum bound, not the literal signed paired packet or maximal prime shell",
    ),
    (
        "2607.24311v1",
        "Valentin Blomer; Alexandru Pascadi",
        "Theorem 1.1 is a fixed-modulus post-emitter Kloosterman-cell engine only",
    ),
    (
        "2204.05038v5",
        "Bryce Kerr; Igor E. Shparlinski; Xiaosheng Wu; Ping Xi",
        "Fixed-modulus Type-II Kloosterman arrays do not include the paired-row longitudinal completion",
    ),
    (
        "2412.19644v1",
        "Adam J. Harper",
        "Centered BDH variance for a fixed regular sequence deletes the V55 longitudinal mode",
    ),
    (
        "2602.20917v6",
        "Runbo Li",
        "Prime arithmetic-progression first moments and Harman-sieve arrays are not the literal paired prime-hybrid covariance",
    ),
    (
        "2512.22798v1",
        "Zongkun Zheng",
        "Two simultaneous prime progressions use source-specific arrays rather than the compensated moving pair packet",
    ),
    (
        "2601.00292v2",
        "Anji Dong; Nicolas Robles; Dirk Zeindler",
        "Withdrawn after a missing L squared factor in equation 2.53; no claimed improved bound receives theorem credit",
    ),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_longitudinal_replication_and_modulus_operator_dichotomy.md",
        "e0e5d02ec2cddfafa8377a714215632732560e36a3afbab0c0a60547a533311a",
    ),
    (
        "research/tpc-big-road/bridge_b_paired_row_longitudinal_mode_and_terminal_equivalence.md",
        "9c6646e45ab5de506c07e185efc67a6c2af541f9d8435838a3b913692df2b52f",
    ),
    (
        "research/tpc-big-road/bridge_b_fold_first_long_mobius_compiler.md",
        "56a3959ca2f7867e370b9ec11d1ad601824297f1b27a713503ac34df13234c73",
    ),
    (
        "research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md",
        "b45ef249175c84758f6052a647f54f74c227351d317034766c5988c7c98f7c5e",
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
    zip_fn=zip,
    set_type=set,
    range_fn=range,
    enumerate_fn=enumerate,
    sum_fn=sum,
    failure_type=CheckFailure,
    file_seed=__file__,
):
    literal_maximum_claim = (
        "EXACT_POINTWISE_REPLICATION_OF_THE_PHYSICAL_SCALAR_ACROSS_EVERY_PRIME_"
        "MODULUS_PLUS_MINIMAX_LINEAR_EXTRACTOR_AND_MODULUS_OPERATOR_TTSTAR_"
        "DICHOTOMY_WITH_MAXIMAL_GATE_A_TRANSFER_INTERFACE"
    )
    literal_registry_digest = (
        "fafcbfe7188ca0733c21ade0cc4bae2395444768667a99e07c895c40e87ae97d"
    )
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
        point_unit = 1 - q_exp
        point_square = fraction_type(1, 2) + h_exp - q_exp
        error_energy = fraction_type(95, 48)
        extraction = error_energy / 2 - q_exp / 2
        target_longitudinal = target + q_exp
        natural_longitudinal = fraction_type(4, 3)
        packet_gap = natural_longitudinal - target_longitudinal
        selected_longitudinal = fraction_type(127, 96)
        selected_gap = natural_longitudinal - selected_longitudinal

        kappa = (fraction_type(3, 4), fraction_type(5, 6))
        difference = (fraction_type(-17, 4), fraction_type(-1))
        error = (fraction_type(-17, 8), fraction_type(-73, 12))
        physical = fraction_type(-17, 2)
        if difference != tuple_type(
            physical * kappa[i] - error[i] for i in range_fn(2)
        ):
            raise failure_type("paired difference fixture failed")

        replicas = tuple_type(difference[i] / kappa[i] for i in range_fn(2))
        replica_rhs = tuple_type(
            physical - error[i] / kappa[i] for i in range_fn(2)
        )
        if replicas != replica_rhs or replicas != (
            fraction_type(-17, 3),
            fraction_type(-6, 5),
        ):
            raise failure_type("replication fixture failed")
        replica_difference = replicas[0] - replicas[1]

        kappa_norm = dot(kappa, kappa)
        a_star = tuple_type(value / kappa_norm for value in kappa)
        a_star_norm = dot(a_star, a_star)
        coordinate = (fraction_type(4, 3), fraction_type(0))
        coordinate_norm = dot(coordinate, coordinate)
        if dot(a_star, kappa) != 1 or dot(coordinate, kappa) != 1:
            raise failure_type("unbiased-estimator fixture failed")
        if a_star_norm != 1 / kappa_norm or not a_star_norm < coordinate_norm:
            raise failure_type("minimax fixture failed")

        transverse = (kappa[1], -kappa[0])
        if dot(transverse, kappa) != 0:
            raise failure_type("transverse operator fixture failed")
        terminal_amplitude = fraction_type(37)
        terminal_row = tuple_type(terminal_amplitude * value for value in kappa)
        terminal_energy = dot(transverse, terminal_row) ** 2
        if terminal_energy != 0:
            raise failure_type("PSD deletion fixture failed")

        t_difference = (2 * difference[0], difference[1])
        t_kappa = (2 * kappa[0], kappa[1])
        t_error = (2 * error[0], error[1])
        t_kappa_norm = dot(t_kappa, t_kappa)
        t_estimator = dot(t_difference, t_kappa) / t_kappa_norm
        t_error_projection = dot(t_error, t_kappa) / t_kappa_norm
        condition_ratio_squared = fraction_type(4) / t_kappa_norm
        if t_estimator != physical - t_error_projection:
            raise failure_type("kept operator fixture failed")
        if not condition_ratio_squared > 1 / kappa_norm:
            raise failure_type("operator condition fixture failed")

        qs = (5, 7, 11)
        p_rows = (fraction_type(2), fraction_type(-1), fraction_type(3))
        kappas = tuple_type(fraction_type(q - 2, q - 1) for q in qs)
        weights = tuple_type(kappas[i] / qs[i] for i in range_fn(3))
        cumulative = []
        current = fraction_type(0)
        for q, row in zip_fn(qs, p_rows):
            current += q * row
            cumulative.append(current)
        direct_abel = dot(kappas, p_rows)
        abel = weights[-1] * cumulative[-1] + sum_fn(
            (weights[i] - weights[i + 1]) * cumulative[i]
            for i in range_fn(2)
        )
        if direct_abel != abel:
            raise failure_type("Abel fixture failed")

        full_shell_rows = (fraction_type(7), fraction_type(-5))
        full_shell = 5 * full_shell_rows[0] + 7 * full_shell_rows[1]
        longitudinal_shell = (
            fraction_type(3, 4) * full_shell_rows[0]
            + fraction_type(5, 6) * full_shell_rows[1]
        )
        if full_shell != 0 or longitudinal_shell == 0:
            raise failure_type("full-shell no-go fixture failed")

        return dict_type(
            (
                ("target", target),
                ("H", h_exp),
                ("Q", q_exp),
                ("point_unit", point_unit),
                ("point_square", point_square),
                ("error_energy", error_energy),
                ("extraction", extraction),
                ("target_longitudinal", target_longitudinal),
                ("natural_longitudinal", natural_longitudinal),
                ("packet_gap", packet_gap),
                ("selected_longitudinal", selected_longitudinal),
                ("selected_gap", selected_gap),
                ("physical", physical),
                ("kappa", kappa),
                ("difference", difference),
                ("error", error),
                ("replicas", replicas),
                ("replica_difference", replica_difference),
                ("kappa_norm", kappa_norm),
                ("a_star", a_star),
                ("a_star_norm", a_star_norm),
                ("coordinate_norm", coordinate_norm),
                ("transverse", transverse),
                ("terminal_energy", terminal_energy),
                ("t_kappa_norm", t_kappa_norm),
                ("t_estimator", t_estimator),
                ("condition_ratio_squared", condition_ratio_squared),
                ("abel_cumulative", tuple_type(cumulative)),
                ("abel_direct", direct_abel),
                ("abel_value", abel),
                ("full_shell", full_shell),
                ("longitudinal_shell", longitudinal_shell),
            )
        )

    fixture = finite_fixtures()
    first_fatal = (
        "NO_PRIMARY_THEOREM_CONTROLS_THE_LITERAL_PRE_Q_PROJECTION_SIGNED_DIAGONAL_"
        "OFFDIAGONAL_PACKET_OR_THE_V51_MAXIMAL_PARTIAL_PRIME_SHELL__ANY_POST_Q_"
        "OPERATOR_RETAINING_KAPPA_IS_TERMINAL_EQUIVALENT_AND_THE_COMMON_TRANSVERSE_"
        "THEOREM_REMAINS_OPEN"
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
        ("registry_rows", 70),
        ("source_locks", 7),
        ("dependency_locks", 4),
        ("pointwise_error", "79/96"),
        ("packet_gap", "1/400"),
        ("operator_status", "TRANSVERSE_OR_TERMINAL"),
        ("minimax_status", "KAPPA_OVER_N_KAPPA"),
        ("maximal_gate_a", "OPEN_NEW_WHOLE_OBJECT_THEOREM"),
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
            ("H", fraction_text(fixture["H"])),
            ("Q", fraction_text(fixture["Q"])),
            ("point_unit", fraction_text(fixture["point_unit"])),
            ("point_square", fraction_text(fixture["point_square"])),
            ("error_energy", fraction_text(fixture["error_energy"])),
            ("extraction", fraction_text(fixture["extraction"])),
            (
                "target_longitudinal",
                fraction_text(fixture["target_longitudinal"]),
            ),
            (
                "natural_longitudinal",
                fraction_text(fixture["natural_longitudinal"]),
            ),
            ("packet_gap", fraction_text(fixture["packet_gap"])),
            (
                "selected_longitudinal",
                fraction_text(fixture["selected_longitudinal"]),
            ),
            ("selected_gap", fraction_text(fixture["selected_gap"])),
            ("fixture_physical", fraction_text(fixture["physical"])),
            ("fixture_kappa", fraction_tuple(fixture["kappa"])),
            ("fixture_difference", fraction_tuple(fixture["difference"])),
            ("fixture_error", fraction_tuple(fixture["error"])),
            ("fixture_replicas", fraction_tuple(fixture["replicas"])),
            (
                "fixture_replica_difference",
                fraction_text(fixture["replica_difference"]),
            ),
            ("fixture_kappa_norm", fraction_text(fixture["kappa_norm"])),
            ("fixture_a_star", fraction_tuple(fixture["a_star"])),
            ("fixture_a_star_norm", fraction_text(fixture["a_star_norm"])),
            (
                "fixture_coordinate_norm",
                fraction_text(fixture["coordinate_norm"]),
            ),
            ("fixture_transverse", fraction_tuple(fixture["transverse"])),
            (
                "fixture_terminal_energy",
                fraction_text(fixture["terminal_energy"]),
            ),
            (
                "fixture_t_kappa_norm",
                fraction_text(fixture["t_kappa_norm"]),
            ),
            ("fixture_t_estimator", fraction_text(fixture["t_estimator"])),
            (
                "fixture_condition_ratio_squared",
                fraction_text(fixture["condition_ratio_squared"]),
            ),
            (
                "fixture_abel_cumulative",
                fraction_tuple(fixture["abel_cumulative"]),
            ),
            ("fixture_abel_direct", fraction_text(fixture["abel_direct"])),
            ("fixture_abel_value", fraction_text(fixture["abel_value"])),
            ("fixture_full_shell", fraction_text(fixture["full_shell"])),
            (
                "fixture_longitudinal_shell",
                fraction_text(fixture["longitudinal_shell"]),
            ),
            ("operator_status", "TRANSVERSE_OR_TERMINAL"),
            ("minimax_status", "KAPPA_OVER_N_KAPPA"),
            ("maximal_gate_a", "OPEN_NEW_WHOLE_OBJECT_THEOREM"),
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
            "registry-outer-type",
            lambda: validate_registry(list_type(literal_registry)),
        )
        typed = list_type(literal_registry)
        typed[0] = 1
        must_reject(
            "registry-row-type",
            lambda: validate_registry(tuple_type(typed)),
        )

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
        must_reject(
            "source-outer-type",
            lambda: validate_sources(list_type(literal_sources)),
        )
        must_reject(
            "source-row-shape",
            lambda: validate_sources((("bad", "row"),)),
        )

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
        must_reject(
            "dependency-row-shape",
            lambda: validate_dependencies((("bad",),)),
        )

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
