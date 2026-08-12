#!/usr/bin/env python3
"""Fail-closed finite checker for the V56 pruned dyadic maximal compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever the frozen V56 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "EXACT_PRUNED_DYADIC_TREE_COMPILER_REDUCES_THE_V51_MAXIMAL_FOLD_FIRST_"
    "PARTIAL_PRIME_SHELL_TO_ONE_UNIFORM_CANONICAL_BLOCK_THEOREM_WITH_TRIVIAL_"
    "LEAF_MARGIN_AND_NO_POWER_LOSS"
)


REGISTRY = (
    "V56_MAXIMUM_CLAIM = EXACT_PRUNED_DYADIC_TREE_COMPILER_REDUCES_THE_V51_MAXIMAL_FOLD_FIRST_PARTIAL_PRIME_SHELL_TO_ONE_UNIFORM_CANONICAL_BLOCK_THEOREM_WITH_TRIVIAL_LEAF_MARGIN_AND_NO_POWER_LOSS",
    "V56_ROUTE_ADVANCE = YES",
    "V56_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V56_ARITHMETIC_ADVANCE = NO",
    "V56_FIXED_ATOM_CREDIT = 0",
    "V56_STRICT_1_OVER_400 = UNPAID",
    "V56_L2 = NONE",
    "V56_TPC_207_TRIGGER = false",
    "V56_NUMBERED_RELEASE = NO",
    "V56_DERIVATION_STATUS = COHERENT_AFTER_LITERAL_ROW_FREEZE_SINGLE_Q_PAYMENT_PRUNED_DYADIC_TREE_MAXIMALIZATION_REVERSE_INTERVAL_BOUND_TWO_WORLD_COMPILER_AND_SOURCE_FIREWALL",
    "V56_ASSUMPTION_POLICY = CANONICAL_BLOCK_THEOREM_AND_COMMON_TRANSVERSE_GATE_REMAIN_CONJECTURAL__MAXIMALIZATION_AND_LEAF_PAYMENT_RECEIVE_ONLY_L0_ROUTE_CREDIT",
    "V56_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_SOURCE_BACKED_CONDITIONAL_EXIT__OTHERWISE_PRUNED_DYADIC_FOLD_FIRST_GATE_A_PLUS_V42_COMMON_TRANSVERSE_GATE_B__V52_PAD_PARALLEL_FALLBACK",
    "V56_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_ARCHITECTURE__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO",
    "V56_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__T_NUM_1997_OVER_1200",
    "V56_INHERITED_FOLD_FIRST_ROW = RETAINED_EXACT_P_Q_EQUALS_SUM_BETA_CIRCLE_TIMES_COMPENSATED_R_Q",
    "V56_LITERAL_DATA_RETENTION = PROVED_SAME_PAIR_FOLD_PHYSICAL_W_DIAGONAL_COMPENSATION_UNIT_MASK_HARD_SHELL_AND_ONE_BLOCK_SIGN",
    "V56_SINGLE_MODULUS_ABSOLUTE_ROW = PROVED_Q_ABS_P_Q_LE_X_H_X_O1",
    "V56_SINGLE_MODULUS_EXPONENT = 53_OVER_32",
    "V56_SINGLE_MODULUS_MARGIN_TO_GATE_A = 19_OVER_2400",
    "V56_PRUNE_EXPONENT_RANGE = ZERO_LT_LAMBDA_LT_19_OVER_2400",
    "V56_CANONICAL_PRUNE_BENCHMARK = LAMBDA_19_OVER_4800",
    "V56_ORDERED_PRIME_SHELL = PREDECLARED_BEFORE_ROW_VALUES",
    "V56_LEAF_PARTITION = PROVED_CONSECUTIVE_AT_MOST_X_LAMBDA_PRIMES",
    "V56_DYADIC_NODE_FAMILY = DEFINED_ALIGNED_UNIONS_OF_POWER_OF_TWO_LEAVES",
    "V56_BLOCK_FUNCTIONAL = DEFINED_T_X_B_EQUALS_SUM_Q_IN_B_Q_P_Q",
    "V56_PREFIX_BINARY_DECOMPOSITION = PROVED_EXACT_DISJOINT_CANONICAL_NODES_PLUS_ONE_PARTIAL_LEAF",
    "V56_PREFIX_NODE_COUNT = PROVED_O_LOG_Q",
    "V56_PREFIX_SINGLETON_COUNT = PROVED_AT_MOST_ONE_FULL_LEAF_PLUS_ONE_PARTIAL_LEAF",
    "V56_TRIVIAL_LEAF_BOUND = PROVED_X_T_NUM_MINUS_19_OVER_2400_PLUS_LAMBDA_PLUS_O1",
    "V56_TRIVIAL_LEAF_MARGIN = PROVED_19_OVER_2400_MINUS_LAMBDA",
    "V56_CANONICAL_BLOCK_THEOREM = CONJECTURAL_H_TREE_LAMBDA_ETA_D",
    "V56_CANONICAL_BLOCK_UNIFORMITY = REQUIRED_ONE_CONSTANT_THRESHOLD_AND_O1_OVER_ALL_PREDECLARED_NODES",
    "V56_TREE_TO_MAXIMAL = PROVED_CONDITIONAL_WITH_ONLY_LOG_Q_LOSS",
    "V56_MAXIMAL_SAVING_LAW = ETA_M_LT_MIN_ETA_D_AND_19_OVER_2400_MINUS_LAMBDA",
    "V56_MAXIMAL_TO_INTERVAL = PROVED_FACTOR_TWO_DIFFERENCE_OF_PREFIXES",
    "V56_TREE_MAXIMAL_POWER_EQUIVALENCE = PROVED_AFTER_SHORT_LEAF_PAYMENT",
    "V56_FULL_SHELL_ONLY = NO_GO_DOES_NOT_CONTROL_MAXIMAL_PREFIX_OR_LONGITUDINAL_ABEL_WEIGHT",
    "V56_FULL_SHELL_COUNTEREXAMPLE = PROVED_Q5_Q7_ZERO_FINAL_WITH_PREFIX_35_AND_NONZERO_KAPPA_SUM",
    "V56_INTERVAL_FACTOR_TWO_FIXTURE = PROVED_SEQUENCE_1_MINUS2_1_SHARP",
    "V56_DYADIC_PREFIX_FIXTURE = PROVED_13_TERM_LEAF3_PREFIX11_EXACT",
    "V56_COEFFICIENT_UNIFORM_SHORTCUT = NO_GO_COMMON_SIGN_REACHES_X_191_OVER_96_PLUS_O1",
    "V56_FOLD_BEFORE_TREE_TRIANGLE = PROVED_REQUIRED_EACH_NODE_RETAINS_COMPLETE_FOLDED_COMPENSATED_ROW",
    "V56_BLOCK_LEVEL_TRIANGLE = PROVED_LEGAL_O_LOG_Q_AFTER_WHOLE_NODE_ESTIMATES",
    "V56_SMOOTH_MODULUS_WEIGHT_TRANSFER = OPEN_REQUIRES_BOUNDARY_STRIP_AND_DERIVATIVE_NORM_PAYMENT",
    "V56_TREE_IMPLIES_V51_GATE_A = PROVED_CONDITIONAL_FULL_SHELL_SPECIALIZATION",
    "V56_SQUARE_ROW_PAYMENT = RETAINED_X_143_OVER_96_PLUS_O1",
    "V56_GATE_A_SAVING_LAW = ETA_A_LT_MIN_ETA_D_19_OVER_2400_MINUS_LAMBDA_419_OVER_2400_11_OVER_600_MINUS_EPSILON",
    "V56_V42_COMMON_TRANSVERSE_GATE_B = RETAINED_INDEPENDENT_OPEN_THEOREM",
    "V56_TWO_GATE_ENDPOINT_LAW = PROVED_CONDITIONAL_MIN_INCLUDES_ETA_B_AND_19_OVER_2400",
    "V56_MAXIMAL_ABEL_TRANSFER = RETAINED_PROVED_TO_LONGITUDINAL_X_1597_OVER_1200_MINUS_ETA_M",
    "V56_LONGITUDINAL_READOUT = RETYPED_TERMINAL_INTERFACE_NOT_GATE_B",
    "V56_UNBOUNDED_SIEGEL_QUALITY_WORLD = RETAINED_SOURCE_BACKED_CONDITIONAL_DIRECT_TPC_EXIT",
    "V56_BOUNDED_SIEGEL_QUALITY_TREE_FAMILY = CONJECTURAL_FORALL_B_EXISTS_ETA_D_B_UNIFORM_ALL_NODES_ALL_LARGE_X",
    "V56_TWO_WORLD_COMPILER = PROVED_CONDITIONAL_UNBOUNDED_EXIT_OR_BOUNDED_TREE_PLUS_GATE_B",
    "V56_V52_PAD_GATE_A = RETAINED_PARALLEL_CONJECTURAL_FALLBACK_NO_CREDIT_SPLICING",
    "V56_LEWKO_LEWKO_VARIATIONAL_LARGE_SIEVE = SOURCE_BACKED_ARCHITECTURE_DYADIC_ENDPOINT_COMPILER_ON_INNER_INDEX",
    "V56_LEWKO_LEWKO_DIRECT_ATTACHMENT = NO_GO_WRONG_MAXIMAL_AXIS_AND_WRONG_LITERAL_COEFFICIENT",
    "V56_RAMARE_SPECTRAL_LARGE_SIEVE = SOURCE_BACKED_ARCHITECTURE_SMOOTH_NONNEGATIVE_Q_AVERAGE_AND_INNER_MAXIMALITY",
    "V56_RAMARE_DIRECT_ATTACHMENT = NO_GO_SIGNED_OUTER_Q_FOLD_FIRST_PACKET_MISSING",
    "V56_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_POST_EMITTER_KLOOSTERMAN_CELL_ONLY",
    "V56_MQW_KSWX_FIXED_MODULUS = NO_GO_DIRECT_NO_CANONICAL_Q_BLOCK_REASSEMBLY",
    "V56_RUNBO_LI_LARGE_MODULI = NO_GO_DIRECT_HARMAN_PRIME_ARRAY_AND_FOLDED_PAIR_PACKET_MISMATCH",
    "V56_BAZIN_PRODUCT_OF_K_PRIMES = NO_GO_DIRECT_WRONG_ENDPOINT_COEFFICIENT_AND_DIRECTION",
    "V56_DIRECT_PRIMARY_SOURCE_FOR_H_TREE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_12",
    "V56_FIRST_FATAL = NO_PRIMARY_THEOREM_PROVES_THE_UNIFORM_CANONICAL_DYADIC_BLOCK_BOUND_FOR_THE_LITERAL_V51_FOLD_FIRST_DIAGONAL_COMPLETED_COMPENSATED_PAIR_PRIME_HYBRID_ROW__AND_V42_COMMON_TRANSVERSE_GATE_B_REMAINS_OPEN",
    "V56_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_PRUNED_DYADIC_MAXIMALIZATION_LEAF_MARGIN_AND_POWER_EQUIVALENCE",
    "V56_SMALL_PAPER_STATUS = STRUCTURAL_LEMMA_PACKAGE_READY_BUT_ELEMENTARY_MAXIMALIZATION_IS_NOT_A_STANDALONE_ASYMPTOTIC_MAIN_THEOREM",
    "V56_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_MAXIMAL_GATE_A_ENDPOINT_MOTION_COMPILED__CANONICAL_LARGE_BLOCK_CANCELLATION_AND_COMMON_TRANSVERSE_PIER_OPEN",
    "V56_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED_NO_ARCHITECTURE_TO_ATTACHMENT_PROMOTION",
    "V56_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_PRUNED_DYADIC_GATE_A_AND_COMMON_TRANSVERSE_GATE_B",
)


REGISTRY_SHA256 = "b90ceeb741eb5887af83398ac754edeef61f78f44b34beb245fb56e1cf28e494"


SOURCE_LOCKS = (
    (
        "1111.6190v2",
        "Allison Lewko; Mark Lewko",
        "Lemmas 16 and 23-24 give dyadic and variational maximal large-sieve architecture on the inner coefficient index, not the outer q-folded row",
    ),
    (
        "2303.04409v2",
        "Olivier Ramare",
        "Lemmas 3.1-3.2 and the smoothed quadratic q-average have inner maximality and nonnegative large-sieve data, not the signed outer-q packet",
    ),
    (
        "2607.24311v1",
        "Valentin Blomer; Alexandru Pascadi",
        "Theorem 1.1 is a fixed-modulus post-emitter Kloosterman-cell engine only",
    ),
    (
        "2511.07550v1",
        "Djordje Milicevic; Xinhua Qin; Xiaosheng Wu",
        "Theorem 1.1 is fixed-modulus and does not reassemble canonical q blocks of the literal folded packet",
    ),
    (
        "2204.05038v5",
        "Bryce Kerr; Igor E. Shparlinski; Xiaosheng Wu; Ping Xi",
        "Fixed-modulus Kloosterman arrays do not include the compensated fold-first q-block family",
    ),
    (
        "2602.20917v6",
        "Runbo Li",
        "Large-modulus prime AP mean values use Harman-sieve arrays rather than the pair-prime hybrid covariance",
    ),
    (
        "2607.15137v1",
        "Pierre-Alexandre Bazin",
        "The product-of-k-primes exponential-sum endpoint has the wrong coefficient family, maximal axis, and estimate direction",
    ),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_pruned_dyadic_maximal_fold_first_compiler.md",
        "1c88a216d402afddf463826aaf44aafc0e38dd46cef3c18e119890cc83adbd4a",
    ),
    (
        "research/tpc-big-road/bridge_b_longitudinal_replication_and_modulus_operator_dichotomy.md",
        "e0e5d02ec2cddfafa8377a714215632732560e36a3afbab0c0a60547a533311a",
    ),
    (
        "research/tpc-big-road/bridge_b_fold_first_long_mobius_compiler.md",
        "56a3959ca2f7867e370b9ec11d1ad601824297f1b27a713503ac34df13234c73",
    ),
    (
        "research/tpc-big-road/bridge_b_endpoint_matched_siegel_world_compiler.md",
        "fd85314cf01edb2e1f63232197e5dd160cd61003269c0e5d31c8cc962efaea29",
    ),
    (
        "research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md",
        "b45ef249175c84758f6052a647f54f74c227351d317034766c5988c7c98f7c5e",
    ),
    (
        "research/tpc-big-road/bridge_b_mobius_directional_dispersion_compiler.md",
        "7888146d36445289520b7f20b9fc99f5ccf39c41d9ed5aec7da47b9e25cb859f",
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
    min_fn=min,
    abs_fn=abs,
    divmod_fn=divmod,
    failure_type=CheckFailure,
    file_seed=__file__,
):
    literal_maximum_claim = (
        "EXACT_PRUNED_DYADIC_TREE_COMPILER_REDUCES_THE_V51_MAXIMAL_FOLD_FIRST_"
        "PARTIAL_PRIME_SHELL_TO_ONE_UNIFORM_CANONICAL_BLOCK_THEOREM_WITH_TRIVIAL_"
        "LEAF_MARGIN_AND_NO_POWER_LOSS"
    )
    literal_registry_digest = (
        "b90ceeb741eb5887af83398ac754edeef61f78f44b34beb245fb56e1cf28e494"
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

    def binary_prefix_parts(n, leaf_size):
        complete, remainder = divmod_fn(n, leaf_size)
        parts = []
        leaf_start = 0
        bit = complete.bit_length() - 1
        while bit >= 0:
            size = 1 << bit
            if complete & size:
                start = leaf_start * leaf_size
                end = (leaf_start + size) * leaf_size
                kind = "NODE" if size >= 2 else "LEAF"
                if leaf_start % size != 0:
                    raise failure_type("dyadic alignment failed")
                parts.append((start, end, kind))
                leaf_start += size
            bit -= 1
        if remainder:
            parts.append((complete * leaf_size, n, "PARTIAL"))
        return tuple_type(parts)

    def finite_fixtures():
        target = fraction_type(1997, 1200)
        h_exp = fraction_type(21, 32)
        q_exp = fraction_type(1, 3)
        one_row = 1 + h_exp
        row_gap = target - one_row
        prune = fraction_type(19, 4800)
        leaf_margin = row_gap - prune
        eta_d = fraction_type(1, 300)
        eta_m = fraction_type(1, 400)
        if row_gap != fraction_type(19, 2400):
            raise failure_type("single-row margin failed")
        if leaf_margin != fraction_type(19, 4800):
            raise failure_type("leaf margin failed")
        if not (eta_m < eta_d and eta_m < leaf_margin):
            raise failure_type("strict maximal saving failed")

        values = (3, -1, 4, 1, 5, -9, 2, 6, -5, 3, 5, -8, 9)
        parts = binary_prefix_parts(11, 3)
        expected_parts = ((0, 6, "NODE"), (6, 9, "LEAF"), (9, 11, "PARTIAL"))
        if parts != expected_parts:
            raise failure_type("binary prefix parts changed")
        part_sums = tuple_type(sum_fn(values[a:b]) for a, b, _ in parts)
        prefix_sum = sum_fn(values[:11])
        if part_sums != (3, 3, 8) or prefix_sum != 14:
            raise failure_type("dyadic prefix fixture failed")
        if sum_fn(part_sums) != prefix_sum:
            raise failure_type("dyadic reconstruction failed")

        sharp = (1, -2, 1)
        sharp_prefix = []
        current = 0
        for value in sharp:
            current += value
            sharp_prefix.append(current)
        prefix_norm = max_fn(abs_fn(value) for value in sharp_prefix)
        interval_norm = abs_fn(sharp[1])
        if prefix_norm != 1 or interval_norm != 2 * prefix_norm:
            raise failure_type("factor-two interval fixture failed")

        qs = (5, 7)
        rows = (fraction_type(7), fraction_type(-5))
        weighted = tuple_type(q * row for q, row in zip_fn(qs, rows))
        weighted_prefix = (weighted[0], sum_fn(weighted))
        kappas = tuple_type(fraction_type(q - 2, q - 1) for q in qs)
        longitudinal = sum_fn(k * row for k, row in zip_fn(kappas, rows))
        if weighted_prefix != (fraction_type(35), fraction_type(0)):
            raise failure_type("full-shell maximal fixture failed")
        if longitudinal != fraction_type(13, 12):
            raise failure_type("longitudinal fixture failed")

        abel_qs = (5, 7, 11)
        abel_rows = (fraction_type(2), fraction_type(-1), fraction_type(3))
        abel_kappa = tuple_type(
            fraction_type(q - 2, q - 1) for q in abel_qs
        )
        abel_weights = tuple_type(
            abel_kappa[i] / abel_qs[i] for i in range_fn(3)
        )
        cumulative = []
        current_f = fraction_type(0)
        for q, row in zip_fn(abel_qs, abel_rows):
            current_f += q * row
            cumulative.append(current_f)
        direct_abel = sum_fn(
            abel_kappa[i] * abel_rows[i] for i in range_fn(3)
        )
        abel_value = abel_weights[-1] * cumulative[-1] + sum_fn(
            (abel_weights[i] - abel_weights[i + 1]) * cumulative[i]
            for i in range_fn(2)
        )
        if direct_abel != abel_value:
            raise failure_type("Abel fixture failed")

        same_sign = (5, 5, 5, 5)
        if sum_fn(same_sign) != 20:
            raise failure_type("same-sign fixture failed")

        return dict_type(
            (
                ("target", target),
                ("H", h_exp),
                ("Q", q_exp),
                ("one_row", one_row),
                ("row_gap", row_gap),
                ("prune", prune),
                ("leaf_margin", leaf_margin),
                ("eta_d", eta_d),
                ("eta_m", eta_m),
                ("maximal_exp", target - eta_m),
                ("longitudinal_exp", fraction_type(1597, 1200) - eta_m),
                ("parts", parts),
                ("part_sums", part_sums),
                ("prefix_sum", prefix_sum),
                ("sharp_prefix", tuple_type(sharp_prefix)),
                ("prefix_norm", prefix_norm),
                ("interval_norm", interval_norm),
                ("weighted_prefix", weighted_prefix),
                ("longitudinal", longitudinal),
                ("abel_cumulative", tuple_type(cumulative)),
                ("abel_direct", direct_abel),
                ("abel_value", abel_value),
                ("same_sign_total", sum_fn(same_sign)),
            )
        )

    fixture = finite_fixtures()
    first_fatal = (
        "NO_PRIMARY_THEOREM_PROVES_THE_UNIFORM_CANONICAL_DYADIC_BLOCK_BOUND_FOR_"
        "THE_LITERAL_V51_FOLD_FIRST_DIAGONAL_COMPLETED_COMPENSATED_PAIR_PRIME_"
        "HYBRID_ROW__AND_V42_COMMON_TRANSVERSE_GATE_B_REMAINS_OPEN"
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
        ("dependency_locks", 6),
        ("single_row_exp", "53/32"),
        ("single_row_margin", "19/2400"),
        ("canonical_prune", "19/4800"),
        ("tree_status", "CONJECTURAL_H_TREE"),
        ("maximalization", "PROVED_NO_POWER_LOSS"),
        ("gate_b", "OPEN_INDEPENDENT"),
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
            ("single_row_exp", fraction_text(fixture["one_row"])),
            ("single_row_margin", fraction_text(fixture["row_gap"])),
            ("canonical_prune", fraction_text(fixture["prune"])),
            ("leaf_margin", fraction_text(fixture["leaf_margin"])),
            ("fixture_eta_d", fraction_text(fixture["eta_d"])),
            ("fixture_eta_m", fraction_text(fixture["eta_m"])),
            ("fixture_maximal_exp", fraction_text(fixture["maximal_exp"])),
            (
                "fixture_longitudinal_exp",
                fraction_text(fixture["longitudinal_exp"]),
            ),
            ("fixture_parts", fixture["parts"]),
            ("fixture_part_sums", fixture["part_sums"]),
            ("fixture_prefix_sum", fixture["prefix_sum"]),
            ("fixture_sharp_prefix", fixture["sharp_prefix"]),
            ("fixture_prefix_norm", fixture["prefix_norm"]),
            ("fixture_interval_norm", fixture["interval_norm"]),
            ("fixture_weighted_prefix", fraction_tuple(fixture["weighted_prefix"])),
            ("fixture_longitudinal", fraction_text(fixture["longitudinal"])),
            (
                "fixture_abel_cumulative",
                fraction_tuple(fixture["abel_cumulative"]),
            ),
            ("fixture_abel_direct", fraction_text(fixture["abel_direct"])),
            ("fixture_abel_value", fraction_text(fixture["abel_value"])),
            ("fixture_same_sign_total", fixture["same_sign_total"]),
            ("tree_status", "CONJECTURAL_H_TREE"),
            ("maximalization", "PROVED_NO_POWER_LOSS"),
            ("gate_b", "OPEN_INDEPENDENT"),
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
            "source-outer-type", lambda: validate_sources(list_type(literal_sources))
        )
        must_reject(
            "source-row-shape", lambda: validate_sources((("bad", "row"),))
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
            "dependency-row-shape", lambda: validate_dependencies((("bad",),))
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
