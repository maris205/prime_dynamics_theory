#!/usr/bin/env python3
"""Fail-closed finite checker for the V53 pair-row Bessel compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever the frozen V53 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "EXACT_PAIR_ROW_COMPRESSION_PAID_COLLISION_DIAGONAL_AND_SYMMETRIC_TWO_GATE_"
    "ROW_BESSEL_COMPILER_REDUCE_BRIDGE_A_TO_ONE_Q_LOSS_FOR_TWO_LITERAL_ROW_SPECIES"
)


REGISTRY = (
    "V53_MAXIMUM_CLAIM = EXACT_PAIR_ROW_COMPRESSION_PAID_COLLISION_DIAGONAL_AND_SYMMETRIC_TWO_GATE_ROW_BESSEL_COMPILER_REDUCE_BRIDGE_A_TO_ONE_Q_LOSS_FOR_TWO_LITERAL_ROW_SPECIES",
    "V53_ROUTE_ADVANCE = YES",
    "V53_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V53_ARITHMETIC_ADVANCE = NO",
    "V53_FIXED_ATOM_CREDIT = 0",
    "V53_STRICT_1_OVER_400 = UNPAID",
    "V53_L2 = NONE",
    "V53_TPC_207_TRIGGER = false",
    "V53_NUMBERED_RELEASE = NO",
    "V53_DERIVATION_STATUS = COHERENT_AFTER_PAIR_ROW_COMPRESSION_COLLISION_DIAGONAL_ENDPOINT_LAW_AND_TWO_GATE_CROSSWALK",
    "V53_ASSUMPTION_POLICY = ROW_BESSEL_AND_CHARACTER_FOURTH_MOMENT_REMAIN_CONJECTURAL__PAID_DIAGONALS_AND_FINITE_FIXTURES_RECEIVE_NO_ASYMPTOTIC_CREDIT",
    "V53_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_CONDITIONAL_EXIT__OTHERWISE_SYMMETRIC_TWO_SPECIES_ROW_BESSEL__PAD_AND_MPD_FALLBACKS__V43_JOIN__DYNAMICS_RESERVE",
    "V53_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO",
    "V53_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__DILATION_31_OVER_96",
    "V53_FROZEN_GATE_A_OBJECT = RETAINED_EXACT_V52_COMPENSATED_PAIR_DILATION",
    "V53_PAIR_ROW_SCALAR = PROVED_EXACT_A_Q_CIRCLE_SUMS_BETA_CIRCLE_TIMES_R_Q",
    "V53_PAIR_ROW_SHELL_IDENTITY = PROVED_EXACT_F_CIRCLE_EQUALS_SUM_Q_Q_A_Q_CIRCLE",
    "V53_Q_SHELL_CAUCHY = PROVED_EXACT_SUM_Q_SQUARED_FACTOR_X_1_PLUS_O1",
    "V53_PAIR_ROW_ENERGY = DEFINED_EXACT_SUM_Q_ABS_A_Q_CIRCLE_SQUARED",
    "V53_PAIR_COLLISION_EXPANSION = PROVED_EXACT_DIAGONAL_PLUS_SIGNED_OFFDIAGONAL",
    "V53_PAIR_COLLISION_OFFDIAGONAL = SIGNED_NOT_POSITIVE_AND_MUST_REMAIN_INSIDE_ROW_ENERGY",
    "V53_PAIR_ROW_POINTWISE_KERNEL = PROVED_H_OVER_Q_TIMES_X_O1_WITH_BOTH_COMPENSATED_LINES_INCLUDED",
    "V53_PAIR_ROW_DIAGONAL = PROVED_X_95_OVER_48_PLUS_O1",
    "V53_PAIR_ROW_BESSEL_HYPOTHESIS = CONJECTURAL_H_A_RB_TAU_A",
    "V53_PAIR_ROW_BESSEL_ENDPOINT = TAU_A_STRICTLY_LESS_THAN_419_OVER_1200",
    "V53_PAIR_ROW_OUTPUT_LAW = X_143_OVER_96_PLUS_TAU_A_OVER_2_PLUS_O1",
    "V53_SELECTED_ONE_Q_LOSS = TAU_A_EQUALS_1_OVER_3",
    "V53_SELECTED_PAIR_ROW_ENERGY = X_37_OVER_16_PLUS_O1",
    "V53_SELECTED_PAIR_ROW_OUTPUT = X_53_OVER_32_PLUS_O1",
    "V53_SELECTED_PAIR_ROW_MARGIN = 19_OVER_2400",
    "V53_TRIVIAL_FULL_X_ROW_LOSS = TAU_A_EQUALS_1",
    "V53_TRIVIAL_ROW_OUTPUT = X_191_OVER_96_PLUS_O1",
    "V53_TRIVIAL_ROW_DEFICIT = 781_OVER_2400",
    "V53_PHYSICAL_DIAGONAL_TOGGLE = PROVED_EXACT_R_Q_EQUALS_G_Q_PLUS_C_PRIME_Q_ZERO_W",
    "V53_PHYSICAL_DIAGONAL_POLICY = RETAINED_INSIDE_A_Q_BEFORE_SQUARE_AND_OUTER_ABSOLUTE",
    "V53_POLARIZED_GENERIC_BDH = NO_GO_RETURNS_THE_UNKNOWN_PHYSICAL_CROSS_DIAGONAL_AS_MAIN",
    "V53_Q5_DIAGONAL_FIXTURE = PROVED_EXACT_35_OVER_2_MINUS_15_OVER_2_EQUALS_10",
    "V53_PAIR_CHARACTER_ROW = PROVED_EXACT_ONE_OVER_Q_MINUS_1_NONPRINCIPAL_PRODUCT_AVERAGE",
    "V53_PAIR_CHARACTER_FOURTH_MOMENT = CONJECTURAL_STRONGER_SUFFICIENT_INTERFACE_AT_X_37_OVER_16",
    "V53_SEPARATE_CHARACTER_SECOND_MOMENTS = NO_GO_DO_NOT_PROVE_THE_JOINT_PRODUCT_FOURTH_MOMENT",
    "V53_GATE_B_ROW = RETAINED_EXACT_V40_DIAGONAL_DELETED_COMPENSATED_ROW",
    "V53_GATE_B_COLLISION_DIAGONAL = RETAINED_PROVED_X_95_OVER_48_PLUS_O1",
    "V53_TWO_SPECIES_ROW_BESSEL = CONJECTURAL_H_2RB_TAU_A_TAU_B_FOR_TWO_LITERAL_ROWS_ONLY",
    "V53_TWO_SPECIES_ENDPOINT = PROVED_CONDITIONAL_IF_MAX_TAU_STRICTLY_LESS_THAN_419_OVER_1200",
    "V53_SYMMETRIC_ONE_Q_BENCHMARK = TAU_A_EQUALS_TAU_B_EQUALS_1_OVER_3",
    "V53_SYMMETRIC_TWO_GATE_OUTPUTS = BOTH_X_53_OVER_32_PLUS_O1",
    "V53_SYMMETRIC_PHYSICAL_ENDPOINT_MARGIN = ANY_ETA_STRICTLY_BETWEEN_0_AND_19_OVER_2400_AFTER_V43",
    "V53_SQUARE_ROW = RETAINED_PAID_X_143_OVER_96_PLUS_O1",
    "V53_HARD_SHELL_BOUNDARY = RETAINED_PAID_WITH_11_OVER_600_MINUS_EPSILON_MARGIN",
    "V53_ROW_BESSEL_VERSUS_DIRECT_SCALAR = STRICTLY_STRONGER_SUFFICIENT_INTERFACE_CROSS_Q_CANCELLATION_DISCARDED",
    "V53_CROSS_Q_FIXTURE = PROVED_FORMAL_5_TIMES_7_PLUS_7_TIMES_MINUS_5_EQUALS_0_WITH_ROW_ENERGY_74",
    "V53_SIGNED_COLLISION_FIXTURE = PROVED_FORMAL_ROW_ENERGY_4_DIAGONAL_22_OFFDIAGONAL_MINUS_18",
    "V53_ALIGNED_ROW_FIXTURE = PROVED_FORMAL_ROW_ENERGY_16_DIAGONAL_4",
    "V53_V52_PAD_ROUTE = RETAINED_INDEPENDENT_CONJECTURAL_ALTERNATIVE",
    "V53_V42_MPD_ROUTE = RETAINED_INDEPENDENT_CONJECTURAL_GATE_B_ALTERNATIVE",
    "V53_V50_BOUNDED_CORE = RETAINED_SEQUENTIAL_CONJECTURAL_ALTERNATIVE",
    "V53_HARPER_GENERAL_BDH = NO_GO_DIRECT_FIXED_SEQUENCE_Q_ABOVE_SQRT_2X_AND_DILATION_HYPOTHESIS_MISMATCH",
    "V53_RUNBO_LI_LARGE_MODULI = NO_GO_DIRECT_FIXED_RESIDUE_FIRST_MOMENT_AND_FACTORIZABLE_MODULUS_WEIGHT_MISMATCH",
    "V53_PASCADI_TRIPLY_FACTORABLE = NO_GO_DIRECT_FIXED_RESIDUE_PRIME_AP_AND_MODULUS_WEIGHT_MISMATCH",
    "V53_ZHENG_SIMULTANEOUS_AP = NO_GO_DIRECT_FIXED_RESIDUE_AND_MOVING_PRODUCT_ROW_MISMATCH",
    "V53_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_LOCAL_CELL_ONLY",
    "V53_DIRECT_PRIMARY_SOURCE_FOR_H_A_RB = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11",
    "V53_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_THE_ONE_Q_RESTRICTED_ROW_BESSEL_BOUND_FOR_THE_DIAGONAL_COMPLETED_FOLDED_PAIR_ROW__AND_THE_MATCHING_GATE_B_ROW_BOUND_REMAINS_INDEPENDENTLY_OPEN",
    "V53_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_PAIR_ROW_DIAGONAL_ONE_Q_ENDPOINT_AND_SYMMETRIC_TWO_GATE_SCHEMA",
    "V53_SMALL_PAPER_STATUS = UNNUMBERED_OUTLINE_ONLY_NO_STANDALONE_ASYMPTOTIC_THEOREM",
    "V53_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_SYMMETRIC_PAIR_AND_PHYSICAL_ROW_BESSEL_PIERS_OPEN",
    "V53_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED",
    "V53_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B",
)


REGISTRY_SHA256 = "7cee07d0b822d6fda36d7b2e7ef4303aa9bd75e668a93703bf9cfb639c74edd7"


SOURCE_LOCKS = (
    (
        "2412.19644v1",
        "Adam J. Harper",
        "Theorem 1 treats one fixed sequence for sqrt(2x)<Q<=x under progression, non-concentration, and hereditary-sparsity hypotheses",
    ),
    (
        "2602.20917v6",
        "Runbo Li",
        "Theorem 1.1 is a fixed-residue first moment with bilinear factorable modulus weights and explicit size conditions",
    ),
    (
        "2505.00653v2",
        "Alexandru Pascadi",
        "Theorem 1.3 uses a fixed residue and triply-well-factorable or linear-sieve modulus weights for prime progression distribution",
    ),
    (
        "2512.22798v1",
        "Zongkun Zheng",
        "Theorems 1.1--1.2 have fixed simultaneous or product residues and do not accept the moving folded pair row",
    ),
    (
        "2607.24311v1",
        "Valentin Blomer; Alexandru Pascadi",
        "Theorem 1.1 is a fixed-modulus critical bilinear Kloosterman cell after a legal emitter and norm are supplied",
    ),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_pair_row_bessel_and_symmetric_two_gate_compiler.md",
        "2c3f7e1c661c68104bec3b88c33e223165ff26d328e0b7d6885d4258d2686698",
    ),
    (
        "research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md",
        "b45ef249175c84758f6052a647f54f74c227351d317034766c5988c7c98f7c5e",
    ),
    (
        "research/tpc-big-road/bridge_b_row_energy_and_packet_route_atlas.md",
        "1f7ae86094a2ff908ba41be6eaefd36bf6959b7e2618e909c59daa44df828ca4",
    ),
    (
        "research/tpc-big-road/bridge_b_fold_first_long_mobius_compiler.md",
        "56a3959ca2f7867e370b9ec11d1ad601824297f1b27a713503ac34df13234c73",
    ),
    (
        "research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md",
        "fd02eaf5504b7a7c2182a8a045b9ec03488ef72ef7b88e750ba781163c10525a",
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
    hash_fn=hash,
    failure_type=CheckFailure,
    file_seed=__file__,
):
    literal_maximum_claim = (
        "EXACT_PAIR_ROW_COMPRESSION_PAID_COLLISION_DIAGONAL_AND_SYMMETRIC_TWO_GATE_"
        "ROW_BESSEL_COMPILER_REDUCE_BRIDGE_A_TO_ONE_Q_LOSS_FOR_TWO_LITERAL_ROW_SPECIES"
    )
    literal_registry_digest = "7cee07d0b822d6fda36d7b2e7ef4303aa9bd75e668a93703bf9cfb639c74edd7"
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

    def dot(left, right):
        return sum_fn(a * b for a, b in zip_fn(left, right))

    def finite_fixtures():
        target = fraction_type(1997, 1200)
        h_exp = fraction_type(21, 32)
        q_exp = fraction_type(1, 3)
        dilation = h_exp - q_exp
        diagonal = 1 + 2 * h_exp - q_exp
        base_output = fraction_type(1, 2) + diagonal / 2
        tau_endpoint = 2 * (target - base_output)
        tau_selected = q_exp
        row_energy = diagonal + tau_selected
        row_output = fraction_type(1, 2) + row_energy / 2
        row_margin = target - row_output
        trivial_output = base_output + fraction_type(1, 2)
        trivial_deficit = trivial_output - target
        square_margin = target - fraction_type(143, 96)
        shell_margin = target - fraction_type(79, 48)

        q = 5
        t = 6
        beta_t = 2
        endpoint = ((4, 2), (6, -1), (11, 3))
        same_sum = sum_fn(weight for u, weight in endpoint if (u - t) % q == 0)
        all_sum = sum_fn(weight for _, weight in endpoint)
        r_value = fraction_type(same_sum, 1) - fraction_type(all_sum, q - 1)
        c_zero = fraction_type(q - 2, q - 1)
        w_t = -1
        diagonal_piece = c_zero * w_t
        g_value = r_value - diagonal_piece
        q5_offdiag = q * beta_t * g_value
        q5_diagonal = q * beta_t * diagonal_piece
        q5_total = q * beta_t * r_value

        collision = (1, -2, 4, -1)
        collision_energy = abs_fn(sum_fn(collision)) ** 2
        collision_diagonal = sum_fn(value * value for value in collision)
        collision_offdiagonal = collision_energy - collision_diagonal
        aligned = (1, 1, 1, 1)
        aligned_values = (abs_fn(sum_fn(aligned)) ** 2, sum_fn(v * v for v in aligned))

        cross_q = ((5, 7), (7, -5))
        cross_scalar = dot(cross_q[0], cross_q[1])
        cross_energy = dot(cross_q[1], cross_q[1])
        cauchy_q = (5, 7)
        cauchy_rows = (3, -2)
        cauchy_scalar = dot(cauchy_q, cauchy_rows)
        cauchy_bound = dot(cauchy_q, cauchy_q) * dot(cauchy_rows, cauchy_rows)

        q5_logs = {1: 0, 2: 1, 4: 2, 3: 3}
        roots = (1, 1j, -1, -1j)
        projector_equal = sum_fn(
            roots[(j * (q5_logs[2] - q5_logs[2])) % 4] for j in range_fn(1, 4)
        )
        projector_unequal = sum_fn(
            roots[(j * (q5_logs[2] - q5_logs[3])) % 4] for j in range_fn(1, 4)
        )

        return dict_type(
            (
                ("target", target),
                ("h_exp", h_exp),
                ("q_exp", q_exp),
                ("dilation", dilation),
                ("diagonal", diagonal),
                ("base_output", base_output),
                ("tau_endpoint", tau_endpoint),
                ("tau_selected", tau_selected),
                ("row_energy", row_energy),
                ("row_output", row_output),
                ("row_margin", row_margin),
                ("trivial_output", trivial_output),
                ("trivial_deficit", trivial_deficit),
                ("square_margin", square_margin),
                ("shell_margin", shell_margin),
                ("boundary_at_one_over_96", shell_margin - fraction_type(1, 96)),
                ("q5_r", r_value),
                ("q5_g", g_value),
                ("q5_offdiag", q5_offdiag),
                ("q5_diagonal", q5_diagonal),
                ("q5_total", q5_total),
                ("collision", (collision_energy, collision_diagonal, collision_offdiagonal)),
                ("aligned", aligned_values),
                ("cross_q", (cross_scalar, cross_energy)),
                ("cauchy", (cauchy_scalar * cauchy_scalar, cauchy_bound)),
                ("projector", (projector_equal, projector_unequal)),
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
        ("registry_rows", 68),
        ("source_locks", 5),
        ("dependency_locks", 5),
        ("selected_tau", "1/3"),
        ("tau_endpoint", "419/1200"),
        ("row_energy", "37/16"),
        ("row_output", "53/32"),
        ("row_margin", "19/2400"),
        ("trivial_output", "191/96"),
        ("trivial_deficit", "781/2400"),
        ("pair_row_gate", "CONJECTURAL"),
        ("two_species_gate", "CONJECTURAL"),
        (
            "first_fatal",
            "NO_LITERAL_THEOREM_PROVES_THE_ONE_Q_RESTRICTED_ROW_BESSEL_BOUND_FOR_THE_DIAGONAL_COMPLETED_FOLDED_PAIR_ROW__AND_THE_MATCHING_GATE_B_ROW_BOUND_REMAINS_INDEPENDENTLY_OPEN",
        ),
        ("direct_source", "NONE"),
        ("mutation_policy", "ALL_ADVERTISED_EXECUTED"),
    )
    expected_contract = dict_type(contract_items)

    def validate_contract(candidate):
        if not same_exact(candidate, expected_contract):
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
            ("H", fraction_text(fixture["h_exp"])),
            ("Q", fraction_text(fixture["q_exp"])),
            ("dilation", fraction_text(fixture["dilation"])),
            ("diagonal", fraction_text(fixture["diagonal"])),
            ("base_output", fraction_text(fixture["base_output"])),
            ("tau_endpoint", fraction_text(fixture["tau_endpoint"])),
            ("tau_selected", fraction_text(fixture["tau_selected"])),
            ("row_energy", fraction_text(fixture["row_energy"])),
            ("row_output", fraction_text(fixture["row_output"])),
            ("row_margin", fraction_text(fixture["row_margin"])),
            ("trivial_output", fraction_text(fixture["trivial_output"])),
            ("trivial_deficit", fraction_text(fixture["trivial_deficit"])),
            ("square_margin", fraction_text(fixture["square_margin"])),
            ("shell_margin", fraction_text(fixture["shell_margin"])),
            ("q5_R", fraction_text(fixture["q5_r"])),
            ("q5_G", fraction_text(fixture["q5_g"])),
            ("q5_offdiag", fraction_text(fixture["q5_offdiag"])),
            ("q5_diagonal", fraction_text(fixture["q5_diagonal"])),
            ("q5_total", fraction_text(fixture["q5_total"])),
            ("collision", fixture["collision"]),
            ("aligned", fixture["aligned"]),
            ("cross_q", fixture["cross_q"]),
            ("cauchy", fixture["cauchy"]),
            ("character_projector", (3, -1)),
            ("pair_row_gate", "CONJECTURAL"),
            ("two_species_gate", "CONJECTURAL"),
            (
                "first_fatal",
                "NO_LITERAL_THEOREM_PROVES_THE_ONE_Q_RESTRICTED_ROW_BESSEL_BOUND_FOR_THE_DIAGONAL_COMPLETED_FOLDED_PAIR_ROW__AND_THE_MATCHING_GATE_B_ROW_BOUND_REMAINS_INDEPENDENTLY_OPEN",
            ),
            ("direct_source", "NONE"),
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
        except failure_type:
            return
        raise failure_type("mutation accepted: " + label)

    def run_contract_mutations():
        start = len_fn(mutation_labels)
        for key, value in tuple_type(expected_contract.items()):
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
        impostor[KeyImpostor()] = impostor.pop("maximum_claim")
        must_reject("contract_key_impostor", validate_contract, impostor)
        return len_fn(mutation_labels) - start

    def run_registry_mutations():
        start = len_fn(mutation_labels)
        for index, row in enumerate_fn(literal_registry):
            changed = list_type(literal_registry)
            changed[index] = row + "_MUT"
            must_reject("registry_value_" + str_type(index), validate_registry, tuple_type(changed))

            class StringSubclass(str_type):
                pass

            changed = list_type(literal_registry)
            changed[index] = StringSubclass(row)
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
            changed[index] = (row[0] + "_MUT", row[1], row[2])
            must_reject("source_value_" + str_type(index), validate_sources, tuple_type(changed))
            changed = list_type(literal_sources)
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
            changed = list_type(literal_dependencies)
            changed[index] = list_type(row)
            must_reject("dependency_type_" + str_type(index), validate_dependencies, tuple_type(changed))
        must_reject("dependency_missing", validate_dependencies, literal_dependencies[:-1])
        must_reject("dependency_extra", validate_dependencies, literal_dependencies + (("x", "0" * 64),))
        must_reject("dependency_list", validate_dependencies, list_type(literal_dependencies))
        return len_fn(mutation_labels) - start

    def validate_result(candidate, expected):
        if not same_exact(candidate, expected):
            raise failure_type("result changed")

    validate_registry(literal_registry)
    validate_sources(literal_sources)
    validate_dependencies(literal_dependencies)
    validate_contract(expected_contract)

    expected_fractions = (
        ("dilation", fraction_type(31, 96)),
        ("diagonal", fraction_type(95, 48)),
        ("base_output", fraction_type(143, 96)),
        ("tau_endpoint", fraction_type(419, 1200)),
        ("row_energy", fraction_type(37, 16)),
        ("row_output", fraction_type(53, 32)),
        ("row_margin", fraction_type(19, 2400)),
        ("trivial_output", fraction_type(191, 96)),
        ("trivial_deficit", fraction_type(781, 2400)),
        ("square_margin", fraction_type(419, 2400)),
        ("shell_margin", fraction_type(11, 600)),
        ("boundary_at_one_over_96", fraction_type(19, 2400)),
    )
    for key, expected in expected_fractions:
        if fixture[key] != expected:
            raise failure_type(key + " changed")
    if (
        fixture["q5_r"],
        fixture["q5_g"],
        fixture["q5_offdiag"],
        fixture["q5_diagonal"],
        fixture["q5_total"],
    ) != (
        fraction_type(1, 1),
        fraction_type(7, 4),
        fraction_type(35, 2),
        fraction_type(-15, 2),
        fraction_type(10, 1),
    ):
        raise failure_type("q5 diagonal fixture changed")
    if fixture["collision"] != (4, 22, -18):
        raise failure_type("signed collision fixture changed")
    if fixture["aligned"] != (16, 4):
        raise failure_type("aligned fixture changed")
    if fixture["cross_q"] != (0, 74):
        raise failure_type("cross-q fixture changed")
    if fixture["cauchy"] != (1, 962):
        raise failure_type("q-shell Cauchy fixture changed")
    if tuple_type(int(round(value.real)) for value in fixture["projector"]) != (3, -1):
        raise failure_type("character projector changed")
    if any(abs_fn(value.imag) > 0 for value in fixture["projector"]):
        raise failure_type("character projector imaginary part changed")

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

    expected_counts = (74, 140, 13, 13, 148, 388)
    actual_counts = (
        contract_mutations,
        registry_mutations,
        source_mutations,
        dependency_mutations,
        semantic_mutations,
        mutation_actions,
    )
    if actual_counts != expected_counts:
        raise failure_type("mutation counts changed: " + str_type(actual_counts))
    if len_fn(tuple_type(mutation_labels)) != len_fn(set_type(mutation_labels)):
        raise failure_type("mutation labels not unique")

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
    hash_fn = hash
    failure_type = CheckFailure
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
            hash_fn=hash_fn,
            failure_type=failure_type,
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
    failure_type=CheckFailure,
):
    baseline = trusted_runner()
    baseline_items = tuple_type(baseline.items())
    frozen_stdout = json_dumps(baseline, sort_keys=True, separators=(",", ":")) + "\n"

    def sealed(*argv_objects):
        if len_fn(argv_objects) != 1:
            raise failure_type("explicit --check is required")
        argv = argv_objects[0]
        if type_fn(argv) is not tuple_type:
            raise failure_type("explicit --check is required")
        if len_fn(argv) != 1 or type_fn(argv[0]) is not str_type or argv[0] != "--check":
            raise failure_type("explicit --check is required")
        result = trusted_runner()
        if tuple_type(result.items()) != baseline_items:
            raise failure_type("sealed result changed")
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
