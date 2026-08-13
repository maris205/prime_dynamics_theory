#!/usr/bin/env python3
"""Fail-closed finite checker for the V58 terminal scalar-root split."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever the frozen V58 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "EXACT_V35_V57_CROSSWALK_IDENTIFIES_THE_GATE_B_FULL_SHELL_WITH_THE_"
    "PROPER_FACTOR_RATIO_CORE_AND_SPLITS_THE_CONSUMED_ROW_ENERGY_INTO_A_"
    "TERMINAL_SCALAR_ROOT_PLUS_OPTIONAL_Q_TRANSVERSE_VARIANCE"
)


REGISTRY = (
    "V58_MAXIMUM_CLAIM = EXACT_V35_V57_CROSSWALK_IDENTIFIES_THE_GATE_B_FULL_SHELL_WITH_THE_PROPER_FACTOR_RATIO_CORE_AND_SPLITS_THE_CONSUMED_ROW_ENERGY_INTO_A_TERMINAL_SCALAR_ROOT_PLUS_OPTIONAL_Q_TRANSVERSE_VARIANCE",
    "V58_ROUTE_ADVANCE = YES",
    "V58_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V58_ARITHMETIC_ADVANCE = NO",
    "V58_FIXED_ATOM_CREDIT = 0",
    "V58_STRICT_1_OVER_400 = UNPAID",
    "V58_L2 = NONE",
    "V58_TPC_207_TRIGGER = false",
    "V58_NUMBERED_RELEASE = NO",
    "V58_DERIVATION_STATUS = COHERENT_AFTER_LITERAL_ROW_FREEZE_EXACT_V35_V57_CROSSWALK_Q_WEIGHT_ORTHOGONAL_SPLIT_EXPONENT_TRANSLATION_TWO_SCALAR_ENDPOINT_COMPILER_AND_OPTIONAL_PREFIX_VARIANCE",
    "V58_ASSUMPTION_POLICY = V51_GATE_A_ROOT_AND_V35_GATE_B_SCALAR_CORE_REMAIN_CONJECTURAL__TRANSVERSE_ROW_IS_OPTIONAL_FOR_MAXIMAL_PREFIXES_ONLY",
    "V58_SELECTED_RESEARCH_ROUTE = V51_FULL_SHELL_GATE_A_ROOT_PLUS_V35_PROPER_FACTOR_GATE_B_SCALAR_CORE__ADD_Q_TRANSVERSE_VARIANCE_ONLY_FOR_MAXIMAL_GATE_A_PREFIXES",
    "V58_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_ARCHITECTURE__CONJECTURAL__NO_GO",
    "V58_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__T_NUM_1997_OVER_1200",
    "V58_PAIR_ROW = RETAINED_EXACT_V54_NONSQUARE_DIAGONAL_COMPLETED_P_Q",
    "V58_PHYSICAL_ROW = RETAINED_EXACT_V54_FULL_BETA_DIAGONAL_DELETED_C_Q",
    "V58_PAIRED_ROW_DIFFERENCE = RETAINED_EXACT_P_Q_MINUS_C_Q_EQUALS_KAPPA_Q_S_PHYSICAL_MINUS_E_Q",
    "V58_FULL_SHELL_SCALARS = DEFINED_A_STAR_C_STAR_E_STAR_K_STAR_WITH_COMMON_Q_WEIGHT",
    "V58_DIRECT_PHYSICAL_READOUT = RETAINED_EXACT_S_EQUALS_A_STAR_MINUS_C_STAR_PLUS_E_STAR_OVER_K_STAR",
    "V58_DIAGONAL_DELETED_KERNEL = PROVED_EXACT_G_Q_SUMS_UNIT_OFFDIAGONAL_W_K_H_C_PRIME_Q",
    "V58_PROPER_FACTOR_IDENTITY = RETAINED_EXACT_BETA_EQUALS_SUM_DK_MU_D_OMEGA_DK_WITH_D_K_AT_LEAST_TWO",
    "V58_V35_V57_SCALAR_CROSSWALK = PROVED_EXACT_C_STAR_EQUALS_MATHFRAK_C_V35_TERM_BY_TERM",
    "V58_CROSSWALK_REMAINDER_POLICY = V35_PRINCIPAL_AND_NONUNIT_TERMS_BELONG_TO_LARGER_D_NOT_TO_ALREADY_CENTERED_C_STAR",
    "V58_GATE_B_WEIGHT_VECTOR = DEFINED_V_Q_EQUALS_Q_AND_V_STAR_EQUALS_SUM_Q_SQUARED",
    "V58_GATE_B_WEIGHT_NORM = PROVED_V_STAR_EQUALS_X_1_PLUS_O1",
    "V58_Q_TRANSVERSE_ROW = DEFINED_C_PERP_EQUALS_C_MINUS_C_STAR_OVER_V_STAR_TIMES_V",
    "V58_Q_TRANSVERSE_ORTHOGONALITY = PROVED_EXACT_INNER_C_PERP_V_EQUALS_ZERO",
    "V58_GATE_B_PYTHAGORAS = PROVED_EXACT_SUM_ABS_C_Q_SQUARED_EQUALS_ABS_C_STAR_SQUARED_OVER_V_STAR_PLUS_NORM_C_PERP_SQUARED",
    "V58_V53_RELATIVE_ROW_BESSEL = RETAINED_STRONGER_THAN_THE_ABSOLUTE_POWER_ENVELOPE_CONSUMED_BY_V57",
    "V58_ABSOLUTE_ROW_DIRECT_SUM = PROVED_POWER_EQUIVALENT_TO_LONGITUDINAL_PLUS_TRANSVERSE_COMPONENT_BOUNDS_WITH_NO_EXPONENT_LOSS",
    "V58_RELATIVE_CONVERSE = NOT_CLAIMED_WITHOUT_A_LOWER_BOUND_FOR_THE_COLLISION_DIAGONAL",
    "V58_LONGITUDINAL_ENERGY = DEFINED_ABS_C_STAR_SQUARED_OVER_V_STAR",
    "V58_LONGITUDINAL_DELTA_TO_TAU = PROVED_TAU_PARALLEL_EQUALS_17_OVER_48_MINUS_TWO_DELTA",
    "V58_STRICT_THRESHOLD_EQUIVALENCE = PROVED_DELTA_GREATER_THAN_1_OVER_400_IFF_TAU_PARALLEL_LESS_THAN_419_OVER_1200",
    "V58_BENCHMARK_TRANSLATION = PROVED_DELTA_1_OVER_96_EQUALS_TAU_PARALLEL_1_OVER_3",
    "V58_GATE_A_ROOT_THEOREM = CONJECTURAL_V51_H_FOLD_ETA_A_ON_FULL_SHELL_NONSQUARE_ROW",
    "V58_GATE_B_SCALAR_ROOT_THEOREM = CONJECTURAL_V35_MATHFRAK_C_X_5_OVER_3_MINUS_DELTA_WITH_DELTA_GREATER_THAN_1_OVER_400",
    "V58_PREFIX_ERROR = RETAINED_PROVED_E_STAR_X_143_OVER_96_PLUS_O1",
    "V58_FULL_SHELL_KAPPA_MASS = RETAINED_PROVED_K_STAR_X_2_OVER_3_PLUS_O1",
    "V58_TWO_SCALAR_ENDPOINT_COMPILER = PROVED_CONDITIONAL_H_A_STAR_PLUS_V35_SCALAR_ROOT_IMPLIES_STRICT_PHYSICAL_ENDPOINT",
    "V58_ENDPOINT_SAVING = ETA_LESS_THAN_MIN_ETA_A_AND_DELTA_MINUS_1_OVER_400_AND_419_OVER_2400",
    "V58_SELECTED_GATE_B_DELTA = 1_OVER_96",
    "V58_SELECTED_GATE_B_NUMERATOR = X_53_OVER_32_PLUS_O1",
    "V58_SELECTED_PHYSICAL_OUTPUT = X_95_OVER_96_PLUS_O1",
    "V58_SELECTED_PHYSICAL_MARGIN = 19_OVER_2400",
    "V58_PREFIX_PROJECTION = PROVED_EXACT_C_Y_MINUS_S_Y_C_STAR_EQUALS_INNER_C_PERP_V_Y",
    "V58_PREFIX_PROJECTED_NORM = PROVED_V_Y_NORM_SQUARED_EQUALS_V_OF_Y_TIMES_ONE_MINUS_V_OF_Y_OVER_V_STAR_LE_V_STAR_OVER_FOUR",
    "V58_OPTIONAL_TRANSVERSE_MAXIMALIZATION = PROVED_TRANSVERSE_ENERGY_CONTROLS_ALL_CENTERED_GATE_B_PREFIXES",
    "V58_ROOT_RATIO_CONVERSION = PROVED_EXACT_C_Y_MINUS_R_Y_C_STAR_EQUALS_C_Y_MINUS_S_Y_C_STAR_PLUS_S_Y_MINUS_R_Y_TIMES_C_STAR",
    "V58_TERMINAL_GATE_B_TRANSVERSE_REQUIREMENT = NONE",
    "V58_MAXIMAL_GATE_A_TRANSVERSE_REQUIREMENT = OPEN_OPTIONAL_Q_TRANSVERSE_VARIANCE_THEOREM",
    "V58_V57_ROW_BESSEL = RETYPED_VALID_STRONGER_PACKAGE_BUNDLING_TERMINAL_SCALAR_AND_PREFIX_VARIANCE",
    "V58_SCALAR_ROOT_ALONE = NO_GO_FOR_UNIFORM_MOVING_PREFIXES_WITHOUT_TRANSVERSE_CONTROL",
    "V58_DIRECT_A_MINUS_C_THEOREM = NO_GO_AS_PRELIMINARY_BECAUSE_TERMINAL_EQUIVALENT_TO_PHYSICAL_S_UP_TO_PAID_ERROR",
    "V58_FINITE_ORTHOGONAL_FIXTURE = PROVED_Q_5_7_11_ENERGY_77_EQUALS_867_OVER_65_PLUS_4138_OVER_65",
    "V58_FINITE_PREFIX_FIXTURE = PROVED_CENTERED_PREFIXES_175_OVER_13_AND_MINUS_2233_OVER_65",
    "V58_FINITE_RATIO_KERNEL_FIXTURE = PROVED_Q5_UNIT_CONGRUENT_3_OVER_4_AND_NONCONGRUENT_MINUS_1_OVER_4",
    "V58_WRIGHT_UNBALANCED_CONVOLUTION = SOURCE_BACKED_ARCHITECTURE_TWO_Q_INDEPENDENT_ARRAYS_FIXED_RESIDUE_AND_SIEGEL_WALFISZ_WRONG_LITERAL_CORE",
    "V58_DRAPPEAU_DISPERSION = SOURCE_BACKED_ARCHITECTURE_CONVOLUTION_KLOOSTERMAN_FRAME_WITHOUT_LITERAL_THREE_ARRAY_OCCURRENCE_CORE",
    "V58_FOUVRY_RADZIWILL = SOURCE_BACKED_ARCHITECTURE_UNBALANCED_TWO_SEQUENCE_CONVOLUTION_WITH_TINY_SIEGEL_WALFISZ_FACTOR",
    "V58_BLOMER_PASCADI = SOURCE_BACKED_CONDITIONAL_FIXED_MODULUS_POST_EMITTER_BILINEAR_KLOOSTERMAN_ENGINE",
    "V58_HARPER_BDH = SOURCE_BACKED_ARCHITECTURE_ONE_FIXED_SEQUENCE_WRONG_MODULUS_AND_MOVING_RATIO",
    "V58_DIRECT_PRIMARY_SOURCE_FOR_H_A_STAR_OR_V35_SCALAR_CORE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_13",
    "V58_FIRST_FATAL = NO_PRIMARY_THEOREM_PROVES_EITHER_THE_LITERAL_V51_FULL_SHELL_SIGNED_FOLD_OR_THE_IDENTICAL_V35_V57_PROPER_FACTOR_CENTERED_GATE_B_SCALAR_CORE",
    "V58_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_EXACT_SCALAR_CROSSWALK_DIRECT_SUM_AND_TWO_SCALAR_ENDPOINT_COMPILER",
    "V58_SMALL_PAPER_STATUS = STRUCTURAL_LEMMA_PACKAGE_STRENGTHENED__TWO_SIGNED_SCALAR_ROOT_THEOREMS_REMAIN_OPEN",
    "V58_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_TERMINAL_ROUTE_NOW_TWO_SCALAR_PIERS__Q_TRANSVERSE_ROW_MOVED_TO_OPTIONAL_MAXIMAL_RAILING",
    "V58_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED_NO_ARCHITECTURE_TO_ATTACHMENT_PROMOTION",
    "V58_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_TWO_SCALAR_PIERS_AND_OPTIONAL_TRANSVERSE_RAILING",
)


REGISTRY_SHA256 = "83cb073c38a757132773eef5f5fd8cfcedfc5cdbf1abc6e5998c52a10892b19f"


SOURCE_LOCKS = (
    (
        "2604.25177v2",
        "Thomas Wright",
        "Corollary 2.2 has two q-independent divisor-bounded arrays, a fixed residue, an outer L1 modulus average, and a Siegel-Walfisz input",
    ),
    (
        "1504.05549",
        "Sary Drappeau",
        "The dispersion and Kloosterman architecture does not contain the literal three-array moving-ratio occurrence scalar",
    ),
    (
        "1811.08672",
        "Etienne Fouvry; Maksym Radziwill",
        "The theorem treats an unbalanced two-sequence convolution with one tiny Siegel-Walfisz factor",
    ),
    (
        "2607.24311v1",
        "Valentin Blomer; Alexandru Pascadi",
        "The fixed-modulus post-emitter bilinear Kloosterman engine does not prove the whole prime-shell scalar",
    ),
    (
        "2412.19644v1",
        "Adam J. Harper",
        "The general-sequence BDH theorem has one fixed sequence and does not accept the moving-ratio Gate-B core",
    ),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_terminal_scalar_root_and_q_transverse_split.md",
        "358170955e74a1ae227941fcc643d85194e3b273b2189524e2698fddc4a67f51",
    ),
    (
        "research/tpc-big-road/bridge_b_proper_factor_unit_ratio_reduction.md",
        "705b0dfd4d94d70bad798ca6cccf7e0f37f049683d30373ea895d97a6db93da1",
    ),
    (
        "research/tpc-big-road/bridge_b_paired_row_longitudinal_mode_and_terminal_equivalence.md",
        "9c6646e45ab5de506c07e185efc67a6c2af541f9d8435838a3b913692df2b52f",
    ),
    (
        "research/tpc-big-road/bridge_b_longitudinal_anchor_transverse_maximal_transfer.md",
        "85faea9c98ae44c3b04319fc5eef26d3a70a60993782a13a2a2c54a3ef5832b5",
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
        "EXACT_V35_V57_CROSSWALK_IDENTIFIES_THE_GATE_B_FULL_SHELL_WITH_THE_"
        "PROPER_FACTOR_RATIO_CORE_AND_SPLITS_THE_CONSUMED_ROW_ENERGY_INTO_A_"
        "TERMINAL_SCALAR_ROOT_PLUS_OPTIONAL_Q_TRANSVERSE_VARIANCE"
    )
    literal_registry_digest = (
        "83cb073c38a757132773eef5f5fd8cfcedfc5cdbf1abc6e5998c52a10892b19f"
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
        target_num = fraction_type(1997, 1200)
        target_phys = fraction_type(399, 400)
        row_diagonal = fraction_type(95, 48)
        delta_threshold = fraction_type(1, 400)
        delta_selected = fraction_type(1, 96)
        tau_threshold = fraction_type(17, 48) - 2 * delta_threshold
        tau_selected = fraction_type(17, 48) - 2 * delta_selected
        scalar_num = fraction_type(5, 3) - delta_selected
        scalar_phys = scalar_num - fraction_type(2, 3)
        scalar_margin = target_phys - scalar_phys
        error_num = fraction_type(143, 96)
        error_phys = error_num - fraction_type(2, 3)
        error_margin = target_phys - error_phys

        if tau_threshold != fraction_type(419, 1200):
            raise failure_type("tau threshold failed")
        if tau_selected != fraction_type(1, 3):
            raise failure_type("selected tau failed")
        if scalar_num != fraction_type(53, 32):
            raise failure_type("selected numerator failed")
        if scalar_phys != fraction_type(95, 96):
            raise failure_type("selected physical exponent failed")
        if scalar_margin != fraction_type(19, 2400):
            raise failure_type("selected margin failed")
        if error_phys != fraction_type(79, 96):
            raise failure_type("error physical exponent failed")
        if error_margin != fraction_type(419, 2400):
            raise failure_type("error margin failed")

        qs = (5, 7, 11)
        c_rows = tuple_type(fraction_type(v) for v in (4, -5, 6))
        weight_norm = sum_fn(fraction_type(q * q) for q in qs)
        c_star = sum_fn(fraction_type(q) * c for q, c in zip_fn(qs, c_rows))
        projection = c_star / weight_norm
        c_perp = tuple_type(
            c - projection * q for q, c in zip_fn(qs, c_rows)
        )
        orthogonality = sum_fn(
            fraction_type(q) * value for q, value in zip_fn(qs, c_perp)
        )
        full_energy = sum_fn(value * value for value in c_rows)
        longitudinal = c_star * c_star / weight_norm
        transverse = sum_fn(value * value for value in c_perp)

        if weight_norm != fraction_type(195):
            raise failure_type("weight norm failed")
        if c_star != fraction_type(51):
            raise failure_type("C star failed")
        if projection != fraction_type(17, 65):
            raise failure_type("projection coefficient failed")
        if c_perp != (
            fraction_type(35, 13),
            fraction_type(-444, 65),
            fraction_type(203, 65),
        ):
            raise failure_type("transverse vector failed")
        if orthogonality != 0:
            raise failure_type("orthogonality failed")
        if full_energy != fraction_type(77):
            raise failure_type("full energy failed")
        if longitudinal != fraction_type(867, 65):
            raise failure_type("longitudinal energy failed")
        if transverse != fraction_type(4138, 65):
            raise failure_type("transverse energy failed")
        if full_energy != longitudinal + transverse:
            raise failure_type("Pythagoras failed")

        prefix_c = []
        prefix_v = []
        prefix_centered = []
        prefix_transverse = []
        prefix_projected_norm = []
        running_c = fraction_type(0)
        running_v = fraction_type(0)
        for index, (q, value) in enumerate_fn(zip_fn(qs, c_rows)):
            running_c += q * value
            running_v += q * q
            scale = running_v / weight_norm
            centered = running_c - scale * c_star
            transverse_read = sum_fn(
                fraction_type(qs[j]) * c_perp[j] for j in range_fn(index + 1)
            )
            projected_norm = running_v * (1 - running_v / weight_norm)
            if centered != transverse_read:
                raise failure_type("prefix projection failed")
            if projected_norm > weight_norm / 4:
                raise failure_type("prefix projected norm failed")
            prefix_c.append(running_c)
            prefix_v.append(running_v)
            prefix_centered.append(centered)
            prefix_transverse.append(transverse_read)
            prefix_projected_norm.append(projected_norm)

        if tuple_type(prefix_centered) != (
            fraction_type(175, 13),
            fraction_type(-2233, 65),
            fraction_type(0),
        ):
            raise failure_type("centered prefix values failed")

        ratio_rows = []
        for q, t, u, expected in (
            (5, 6, 11, fraction_type(3, 4)),
            (5, 6, 8, fraction_type(-1, 4)),
            (7, 10, 17, fraction_type(5, 6)),
            (7, 10, 12, fraction_type(-1, 6)),
        ):
            inverse = next(
                candidate
                for candidate in range_fn(1, q)
                if (candidate * t) % q == 1
            )
            c_prime = fraction_type(1 if (u - t) % q == 0 else 0) - fraction_type(
                1, q - 1
            )
            unit_ratio = fraction_type(1 if (u * inverse) % q == 1 else 0) - fraction_type(
                1, q - 1
            )
            if c_prime != expected or unit_ratio != expected:
                raise failure_type("unit-ratio crosswalk failed")
            ratio_rows.append((q, t, u, expected))

        return dict_type(
            (
                ("target_num", target_num),
                ("target_phys", target_phys),
                ("row_diagonal", row_diagonal),
                ("delta_threshold", delta_threshold),
                ("delta_selected", delta_selected),
                ("tau_threshold", tau_threshold),
                ("tau_selected", tau_selected),
                ("scalar_num", scalar_num),
                ("scalar_phys", scalar_phys),
                ("scalar_margin", scalar_margin),
                ("error_num", error_num),
                ("error_phys", error_phys),
                ("error_margin", error_margin),
                ("qs", qs),
                ("c_rows", c_rows),
                ("weight_norm", weight_norm),
                ("c_star", c_star),
                ("projection", projection),
                ("c_perp", c_perp),
                ("full_energy", full_energy),
                ("longitudinal", longitudinal),
                ("transverse", transverse),
                ("prefix_c", tuple_type(prefix_c)),
                ("prefix_v", tuple_type(prefix_v)),
                ("prefix_centered", tuple_type(prefix_centered)),
                ("prefix_transverse", tuple_type(prefix_transverse)),
                ("prefix_projected_norm", tuple_type(prefix_projected_norm)),
                ("ratio_rows", tuple_type(ratio_rows)),
            )
        )

    fixture = finite_fixtures()
    first_fatal = (
        "NO_PRIMARY_THEOREM_PROVES_EITHER_THE_LITERAL_V51_FULL_SHELL_SIGNED_"
        "FOLD_OR_THE_IDENTICAL_V35_V57_PROPER_FACTOR_CENTERED_GATE_B_SCALAR_CORE"
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
        ("registry_rows", 69),
        ("source_locks", 5),
        ("dependency_locks", 5),
        ("scalar_crosswalk", "PROVED_EXACT"),
        ("orthogonal_split", "PROVED_EXACT"),
        ("delta_to_tau", "17/48-2*delta"),
        ("strict_tau_threshold", "419/1200"),
        ("selected_delta", "1/96"),
        ("selected_tau", "1/3"),
        ("selected_numerator", "53/32"),
        ("selected_physical", "95/96"),
        ("selected_margin", "19/2400"),
        ("terminal_transverse", "NONE"),
        ("maximal_transverse", "OPEN_OPTIONAL"),
        ("direct_source", "NONE"),
        ("first_fatal", first_fatal),
        ("mutation_policy", "ALL_ADVERTISED_EXECUTED"),
    )

    def validate_contract(candidate):
        if not same_exact(candidate, dict_type(contract_items)):
            raise failure_type("contract changed")

    def result_items_base():
        ratio_values = tuple_type(
            (q, t, u, fraction_text(value)) for q, t, u, value in fixture["ratio_rows"]
        )
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
            ("target_numerator", fraction_text(fixture["target_num"])),
            ("target_physical", fraction_text(fixture["target_phys"])),
            ("row_diagonal", fraction_text(fixture["row_diagonal"])),
            ("delta_threshold", fraction_text(fixture["delta_threshold"])),
            ("selected_delta", fraction_text(fixture["delta_selected"])),
            ("tau_threshold", fraction_text(fixture["tau_threshold"])),
            ("selected_tau", fraction_text(fixture["tau_selected"])),
            ("selected_numerator", fraction_text(fixture["scalar_num"])),
            ("selected_physical", fraction_text(fixture["scalar_phys"])),
            ("selected_margin", fraction_text(fixture["scalar_margin"])),
            ("error_numerator", fraction_text(fixture["error_num"])),
            ("error_physical", fraction_text(fixture["error_phys"])),
            ("error_margin", fraction_text(fixture["error_margin"])),
            ("fixture_qs", fixture["qs"]),
            ("fixture_C_rows", fraction_tuple(fixture["c_rows"])),
            ("fixture_weight_norm", fraction_text(fixture["weight_norm"])),
            ("fixture_C_star", fraction_text(fixture["c_star"])),
            ("fixture_projection", fraction_text(fixture["projection"])),
            ("fixture_C_perp", fraction_tuple(fixture["c_perp"])),
            ("fixture_full_energy", fraction_text(fixture["full_energy"])),
            ("fixture_longitudinal", fraction_text(fixture["longitudinal"])),
            ("fixture_transverse", fraction_text(fixture["transverse"])),
            ("fixture_prefix_C", fraction_tuple(fixture["prefix_c"])),
            ("fixture_prefix_V", fraction_tuple(fixture["prefix_v"])),
            ("fixture_prefix_centered", fraction_tuple(fixture["prefix_centered"])),
            ("fixture_prefix_transverse", fraction_tuple(fixture["prefix_transverse"])),
            ("fixture_prefix_projected_norm", fraction_tuple(fixture["prefix_projected_norm"])),
            ("fixture_ratio_rows", ratio_values),
            ("scalar_crosswalk", "PROVED_EXACT_C_STAR_EQUALS_V35_CORE"),
            ("orthogonal_split", "PROVED_EXACT"),
            ("endpoint_compiler", "PROVED_CONDITIONAL_TWO_SCALAR"),
            ("terminal_transverse", "NONE"),
            ("maximal_transverse", "OPEN_OPTIONAL"),
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
