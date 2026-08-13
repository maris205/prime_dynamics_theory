#!/usr/bin/env python3
"""Fail-closed finite checker for the V59 polarized local-BDH compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever the frozen V59 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "EXACT_COMPLEX_POLARIZATION_REPRESENTS_THE_V35_V58_GATE_B_SCALAR_AS_A_"
    "SIGNED_FOUR_PACKET_PRIME_WEIGHTED_KERNEL_LOCALIZED_OFFDIAGONAL_BDH_"
    "REMAINDER_AND_IDENTIFIES_THE_MISSING_COLLECTIVE_POWER_SAVING_COMPILER"
)


REGISTRY = (
    "V59_MAXIMUM_CLAIM = EXACT_COMPLEX_POLARIZATION_REPRESENTS_THE_V35_V58_GATE_B_SCALAR_AS_A_SIGNED_FOUR_PACKET_PRIME_WEIGHTED_KERNEL_LOCALIZED_OFFDIAGONAL_BDH_REMAINDER_AND_IDENTIFIES_THE_MISSING_COLLECTIVE_POWER_SAVING_COMPILER",
    "V59_ROUTE_ADVANCE = YES",
    "V59_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V59_ARITHMETIC_ADVANCE = NO",
    "V59_FIXED_ATOM_CREDIT = 0",
    "V59_STRICT_1_OVER_400 = UNPAID",
    "V59_L2 = NONE",
    "V59_TPC_207_TRIGGER = false",
    "V59_NUMBERED_RELEASE = NO",
    "V59_DERIVATION_STATUS = COHERENT_AFTER_V35_V58_SCALAR_FREEZE_V36_CHARACTER_FORM_EXACT_COMPLEX_POLARIZATION_REDUCED_RESIDUE_BDH_CROSSWALK_BLOCK_SCALE_LEDGER_SOURCE_AUDIT_AND_FINITE_FALSIFIERS",
    "V59_ASSUMPTION_POLICY = NO_BDH_OR_KLOOSTERMAN_POWER_BOUND_IS_ASSUMED__THE_FOUR_PACKET_AND_LOCAL_COLLECTIVE_THEOREMS_REMAIN_OPEN",
    "V59_SELECTED_RESEARCH_ROUTE = FOUR_LITERAL_POLARIZED_PRIME_BDH_PACKETS_THEN_MESOSCOPIC_BLOCK_COMPILER_THEN_BLOMER_PASCADI_CELLS_THEN_COLLECTIVE_SIGNED_REASSEMBLY",
    "V59_CLAIM_CLASS_POLICY = PROVED_EXACT_COMPILER__SOURCE_BACKED_ARCHITECTURE__SOURCE_BACKED_LOCAL_ENGINE__CONJECTURAL__NO_GO",
    "V59_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__TARGET_5_OVER_3_MINUS_DELTA__DELTA_STRICTLY_GREATER_THAN_1_OVER_400",
    "V59_GATE_B_SCALAR = RETAINED_EXACT_C_STAR_EQUALS_MATHFRAK_C_V35",
    "V59_V36_CHARACTER_FORM = RETAINED_EXACT_B_TIMES_W_MINUS_ONE_Z_PER_NONPRINCIPAL_CHARACTER",
    "V59_CONJUGATE_PACKET = PROVED_EXACT_W_Q_CHI_EQUALS_CONJUGATE_D_Q_CHI_FOR_REAL_PHYSICAL_W",
    "V59_COMPLEX_POLARIZATION = PROVED_EXACT_X_CONJUGATE_Y_EQUALS_ONE_QUARTER_SUM_IJ_ABS_X_PLUS_IJ_Y_SQUARED",
    "V59_FOUR_LITERAL_SEQUENCES = DEFINED_A_J_EQUALS_BETA_PLUS_I_POWER_J_W_FOR_J_ZERO_TO_THREE",
    "V59_REDUCED_RESIDUE_VARIANCE = PROVED_EXACT_NONPRINCIPAL_CHARACTER_PARSEVAL_ON_UNIT_CLASSES",
    "V59_DIAGONAL_MULTIPLICITY = PROVED_EXACT_Q_MINUS_2_NONPRINCIPAL_CHARACTERS",
    "V59_OFFDIAGONAL_BDH_REMAINDER = DEFINED_PRIME_WEIGHTED_KERNEL_LOCALIZED_VARIANCE_MINUS_EXACT_DIAGONAL",
    "V59_GLOBAL_FOUR_PACKET_IDENTITY = PROVED_EXACT_MATHFRAK_C_EQUALS_ONE_QUARTER_SUM_IJ_V_CIRCLE_A_J",
    "V59_DIAGONAL_POLARIZATION = PROVED_EXACT_ONE_QUARTER_SUM_IJ_ABS_BETA_PLUS_IJ_W_SQUARED_EQUALS_BETA_W",
    "V59_REMAINDER_SIGN = PROVED_FINITE_FIXTURES_SHOW_BOTH_POSITIVE_AND_NEGATIVE_VALUES",
    "V59_FOUR_ABSOLUTE_BDH_THEOREM = OPEN_STRONGER_SUFFICIENT_H_4BDH_DELTA",
    "V59_FOUR_ABSOLUTE_POLICY = NOT_EQUIVALENT_TO_THE_SIGNED_ENDPOINT_SCALAR_AND_NO_FREE_TRIANGLE_CREDIT",
    "V59_BLOCK_PARTITION = PROVED_EXACT_ORDERED_PAIR_PARTITION_BEFORE_POLARIZATION_AND_ABSOLUTE_VALUES",
    "V59_LOCAL_POLARIZED_PACKETS = DEFINED_A_BC_J_EQUALS_ETA_B_BETA_PLUS_IJ_ETA_C_W",
    "V59_EFFECTIVE_BLOCK_COUNT = PROVED_X_POWER_11_OVER_32_PLUS_O1_AFTER_SCHWARTZ_TAIL",
    "V59_LOCAL_Q_WEIGHTED_BDH_SCALE = PROVED_X_POWER_127_OVER_96",
    "V59_GLOBAL_NATURAL_SCALE = PROVED_X_Q_SQUARED_EQUALS_X_POWER_5_OVER_3",
    "V59_MESOSCOPIC_CONDUCTOR_GAP = PROVED_Q_SQUARED_OVER_H_EQUALS_X_POWER_1_OVER_96",
    "V59_BLOMER_PASCADI_CRITICAL_SAVING = SOURCE_BACKED_Q_POWER_MINUS_1_OVER_32_EQUALS_X_POWER_MINUS_1_OVER_96",
    "V59_BLOMER_PASCADI_ATTACHMENT = SOURCE_BACKED_LOCAL_ENGINE_AFTER_FIXED_Q_BILINEAR_KLOOSTERMAN_CELL_EMISSION_ONLY",
    "V59_SELECTED_LOCAL_COLLECTIVE_THEOREM = OPEN_H_LOC_POL_DELTA_ON_THE_LITERAL_BLOCK_PRIME_PACKET_FAMILY",
    "V59_REQUIRED_DELTA = STRICTLY_GREATER_THAN_1_OVER_400",
    "V59_SELECTED_DELTA = 1_OVER_96",
    "V59_SELECTED_GATE_B_NUMERATOR = X_POWER_53_OVER_32_PLUS_O1",
    "V59_SELECTED_PHYSICAL_OUTPUT = X_POWER_95_OVER_96_PLUS_O1",
    "V59_SELECTED_GATE_B_MARGIN = 19_OVER_2400",
    "V59_TWO_SCALAR_ENDPOINT_COMPILER = RETAINED_V58_GATE_A_ROOT_PLUS_GATE_B_DELTA_IMPLIES_STRICT_PHYSICAL_SAVING",
    "V59_Q_TRANSVERSE_PREFIX_THEOREM = RETAINED_OPTIONAL_ONLY_FOR_MOVING_PREFIXES",
    "V59_HARPER_GENERAL_SEQUENCE_BDH = SOURCE_BACKED_CLOSEST_QUADRATIC_ARCHITECTURE_WITH_GENERAL_COMPLEX_SEQUENCE",
    "V59_HARPER_GLOBAL_RANGE = STOP_SCOPED_UNSHIFTED_LITERAL_AMBIENT_X_HAS_Q_LESS_THAN_SQRT_X",
    "V59_HARPER_BLOCK_NUMERICAL_WINDOW = PROVED_FORMAL_Q_SQUARED_OVER_H_EQUALS_X_POWER_1_OVER_96",
    "V59_HARPER_TRANSLATION_ATTACHMENT = STOP_SCOPED_BLOCK_SHIFT_CHANGES_THE_DISTINGUISHED_ZERO_RESIDUE_IN_GCD_GROUPED_VARIANCE",
    "V59_HARPER_MODULUS_SUBSET = STOP_SCOPED_ALL_DYADIC_MODULI_SIGNED_REMAINDER_DOES_NOT_CONTROL_PRIME_SUBSET",
    "V59_HARPER_INPUT_CONDITIONS = OPEN_UNPROVED_FOR_FOUR_LITERAL_PACKETS_UNIFORMLY_IN_V_AND_BLOCK",
    "V59_KLURMAN_MANGEREL_TERAVAINEN = SOURCE_BACKED_SHORT_PRIME_MODULUS_VARIANCE_FOR_BOUNDED_MULTIPLICATIVE_FUNCTIONS_WRONG_COEFFICIENT_CLASS",
    "V59_PASCADI_EXCEPTIONAL_LARGE_SIEVE = SOURCE_BACKED_POST_EMITTER_SPARSE_FOURIER_KLOOSTERMAN_ENGINE_WRONG_PRE_EMITTER_OBJECT",
    "V59_WRIGHT_CONVOLUTION = SOURCE_BACKED_TWO_Q_INDEPENDENT_FIXED_RESIDUE_ARRAYS_WITH_SIEGEL_WALFISZ_INPUT_WRONG_QUADRATIC_PACKET",
    "V59_DIRECT_PRIMARY_SOURCE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_13",
    "V59_FIRST_FATAL = NO_PRIMARY_THEOREM_PROVES_A_POWER_SAVING_PRIME_MODULUS_KERNEL_LOCALIZED_OFFDIAGONAL_BDH_REMAINDER_FOR_THE_FOUR_LITERAL_POLARIZED_SEQUENCES_OR_COMPILES_THEIR_BLOCKS_COLLECTIVELY_TO_THE_BLOMER_PASCADI_CELLS",
    "V59_FINITE_COMPLEX_POLARIZATION_FIXTURE = PROVED_2_PLUS_3I_AND_MINUS_1_PLUS_2I_GIVE_4_MINUS_7I",
    "V59_FINITE_Q5_CROSS_FIXTURE = PROVED_BETA_1_MINUS2_3_0_AND_W_2_1_MINUS1_4_GIVE_MINUS15",
    "V59_FINITE_Q5_SIGN_FIXTURE = PROVED_EQUAL_PAIR_GIVES_MINUS2_AND_OPPOSITE_PAIR_GIVES_PLUS2",
    "V59_FINITE_Q5_DIAGONAL_FIXTURE = PROVED_CORRECT_MINUS15_WRONG_Q_MINUS1_GIVES_MINUS12_AND_OMITTED_SUBTRACTION_GIVES_MINUS24",
    "V59_FINITE_TRANSLATION_FIXTURE = PROVED_Q5_EXCLUDING_ZERO_GIVES_3_OVER_4_WHILE_EXCLUDING_ONE_GIVES_75",
    "V59_FINITE_PRIME_SUBSET_FIXTURE = PROVED_SIGNED_ROWS_R5_1_R6_MINUS1_HAVE_ALL_SUM_ZERO_AND_PRIME_SUBSET_ONE",
    "V59_GENERIC_SEQUENCE_THEOREM = NO_GO_DIVISOR_ENVELOPES_ALONE_ALLOW_COHERENT_ONE_RESIDUE_NATURAL_SCALE",
    "V59_PER_BLOCK_PRIME_PACKET_TRIANGLE = NO_GO_RETURNS_X_POWER_5_OVER_3_NATURAL_SCALE",
    "V59_DIAGONAL_RESTORATION = NO_GO_RETURNS_UNKNOWN_PHYSICAL_SCALAR_AT_X_POWER_5_OVER_3_SCALE",
    "V59_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED_NO_NUMERICAL_CLOCK_TO_ATTACHMENT_PROMOTION",
    "V59_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_POLARIZED_PRIME_BDH_NORMAL_FORM_MESOSCOPIC_CLOCK_AND_COLLECTIVE_COMPILER",
    "V59_SMALL_PAPER_STATUS = STRUCTURAL_NOTE_CANDIDATE_STRENGTHENED__POWER_REMAINDER_THEOREM_REMAINS_OPEN",
    "V59_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_JOINT_PRODUCT_WALL_REPLACED_BY_FOUR_ONE_SEQUENCE_PRIME_BDH_PACKETS_AND_ONE_COLLECTIVE_COMPILER",
    "V59_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_POLARIZED_PRIME_BDH_CONSTRUCTION_ZONE",
)


REGISTRY_SHA256 = "dd3c34ddeaf69abee656cfd941b17e63e6142615bc3d516aab860034292a8c87"


SOURCE_LOCKS = (
    (
        "2412.19644v1",
        "Adam J. Harper",
        "Theorems 1-2 treat a general complex sequence but require sqrt(2X)<Q and do not prove the literal prime-only localized signed remainder",
    ),
    (
        "2607.24311v1",
        "Valentin Blomer; Alexandru Pascadi",
        "Theorem 1.1 gives fixed-modulus critical bilinear Kloosterman saving q^-1/32 after cell emission",
    ),
    (
        "2404.04239v3",
        "Alexandru Pascadi",
        "Corollaries 17-18 are post-emitter sparse-Fourier multilinear Kloosterman bounds",
    ),
    (
        "1909.12280v5",
        "Oleksiy Klurman; Alexander P. Mangerel; Joni Teravainen",
        "Short prime-modulus variance concerns bounded multiplicative functions and pretentious structure",
    ),
    (
        "2604.25177v2",
        "Thomas Wright",
        "Corollary 2.2 treats two q-independent fixed-residue convolution arrays with a Siegel-Walfisz input",
    ),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md",
        "74e42689e17efad75e9718a9d6ac3d8f3ec9c16239204a4915b0b7bdc17ae218",
    ),
    (
        "research/tpc-big-road/bridge_b_terminal_scalar_root_and_q_transverse_split.md",
        "358170955e74a1ae227941fcc643d85194e3b273b2189524e2698fddc4a67f51",
    ),
    (
        "research/tpc-big-road/bridge_b_multiroute_ratio_core_atlas.md",
        "97c725b3fd086825125aa5d9ea302bdb874243bddc2708e5603a1c1d591b0a98",
    ),
    (
        "research/tpc-big-road/bridge_b_proper_factor_unit_ratio_reduction.md",
        "705b0dfd4d94d70bad798ca6cccf7e0f37f049683d30373ea895d97a6db93da1",
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
    set_type=set,
    str_type=str,
    int_type=int,
    bool_type=bool,
    type_fn=type,
    len_fn=len,
    all_fn=all,
    range_fn=range,
    enumerate_fn=enumerate,
    sum_fn=sum,
    abs_fn=abs,
    failure_type=CheckFailure,
    file_seed=__file__,
):
    literal_maximum_claim = (
        "EXACT_COMPLEX_POLARIZATION_REPRESENTS_THE_V35_V58_GATE_B_SCALAR_AS_A_"
        "SIGNED_FOUR_PACKET_PRIME_WEIGHTED_KERNEL_LOCALIZED_OFFDIAGONAL_BDH_"
        "REMAINDER_AND_IDENTIFIES_THE_MISSING_COLLECTIVE_POWER_SAVING_COMPILER"
    )
    literal_registry_digest = (
        "dd3c34ddeaf69abee656cfd941b17e63e6142615bc3d516aab860034292a8c87"
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
    mutation_labels = list_type()

    if maximum_claim_seed != literal_maximum_claim:
        raise failure_type("maximum-claim seed changed")
    if registry_digest_seed != literal_registry_digest:
        raise failure_type("registry-digest seed changed")

    class FauxStr(str_type):
        pass

    class KeyImpostor:
        def __init__(self, target):
            self.target = target

        def __hash__(self):
            return hash(self.target)

        def __eq__(self, other):
            return other == self.target

    def rows_digest(rows):
        payload = "\n".join(rows) + "\n"
        return sha256_fn(payload.encode("utf-8")).hexdigest()

    def table_digest(rows):
        payload = "\n".join("\t".join(row) for row in rows) + "\n"
        return sha256_fn(payload.encode("utf-8")).hexdigest()

    def exact_mapping(candidate, expected, label):
        if type_fn(candidate) is not dict_type:
            raise failure_type(label + " must be exact dict")
        if not all_fn(type_fn(key) is str_type for key in candidate):
            raise failure_type(label + " keys must be exact str")
        if set_type(candidate) != set_type(expected):
            raise failure_type(label + " key set changed")
        for key, value in expected.items():
            if type_fn(candidate[key]) is not type_fn(value):
                raise failure_type(label + " value type changed: " + key)
            if candidate[key] != value:
                raise failure_type(label + " value changed: " + key)

    def validate_registry(candidate):
        if type_fn(candidate) is not tuple_type:
            raise failure_type("registry must be exact tuple")
        if not all_fn(type_fn(row) is str_type for row in candidate):
            raise failure_type("registry rows must be exact str")
        if candidate != literal_registry:
            raise failure_type("registry literal changed")
        if rows_digest(candidate) != literal_registry_digest:
            raise failure_type("registry digest changed")

    def validate_sources(candidate):
        if type_fn(candidate) is not tuple_type:
            raise failure_type("sources must be exact tuple")
        for row in candidate:
            if type_fn(row) is not tuple_type or len_fn(row) != 3:
                raise failure_type("source row shape changed")
            if not all_fn(type_fn(cell) is str_type for cell in row):
                raise failure_type("source cells must be exact str")
        if candidate != literal_sources:
            raise failure_type("source locks changed")

    def validate_dependencies(candidate):
        if type_fn(candidate) is not tuple_type:
            raise failure_type("dependencies must be exact tuple")
        for row in candidate:
            if type_fn(row) is not tuple_type or len_fn(row) != 2:
                raise failure_type("dependency row shape changed")
            if not all_fn(type_fn(cell) is str_type for cell in row):
                raise failure_type("dependency cells must be exact str")
        if candidate != literal_dependencies:
            raise failure_type("dependency locks changed")
        for relative, path, expected_hash in literal_dependency_paths:
            if not path_is_file(path):
                raise failure_type("dependency missing: " + relative)
            if sha256_fn(path_read_bytes(path)).hexdigest() != expected_hash:
                raise failure_type("dependency hash changed: " + relative)

    def cadd(z, w):
        return (z[0] + w[0], z[1] + w[1])

    def cmul(z, w):
        return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])

    def cconj(z):
        return (z[0], -z[1])

    def cscale(a, z):
        return (a * z[0], a * z[1])

    def cabs2(z):
        return z[0] * z[0] + z[1] * z[1]

    zero = (fraction_type(0), fraction_type(0))
    one = (fraction_type(1), fraction_type(0))
    imag = (fraction_type(0), fraction_type(1))

    def ipow(j):
        value = one
        for _ in range_fn(j):
            value = cmul(value, imag)
        return value

    def polarization(x, y):
        value = zero
        for j in range_fn(4):
            ij = ipow(j)
            z = cadd(x, cmul(ij, y))
            value = cadd(value, cscale(cabs2(z), ij))
        return cscale(fraction_type(1, 4), value)

    def offdiag_energy(values, diagonal_multiplier=1, include_diagonal=True):
        total = zero
        norm = fraction_type(0)
        for value in values:
            total = cadd(total, value)
            norm += cabs2(value)
        character_energy = 4 * norm - cabs2(total)
        if include_diagonal:
            character_energy -= diagonal_multiplier * norm
        return character_energy

    def polarized_q5(beta, physical, diagonal_multiplier=3, include_diagonal=True):
        value = zero
        for j in range_fn(4):
            ij = ipow(j)
            packet = tuple_type(
                cadd((fraction_type(b), fraction_type(0)), cmul(ij, (fraction_type(w), fraction_type(0))))
                for b, w in zip(beta, physical)
            )
            energy = offdiag_energy(packet, diagonal_multiplier, include_diagonal)
            value = cadd(value, cscale(energy, ij))
        return cscale(fraction_type(1, 4), value)

    def variance_excluding(masses, excluded):
        kept = tuple_type(value for index, value in enumerate_fn(masses) if index != excluded)
        mean = sum_fn(kept, fraction_type(0)) / len_fn(kept)
        return sum_fn(((value - mean) ** 2 for value in kept), fraction_type(0))

    expected_contract = dict_type(
        maximum_claim=literal_maximum_claim,
        route_advance="YES",
        conditional_bridge_advance="YES",
        arithmetic_advance=False,
        fixed_atom_credit=0,
        strict_1_over_400="UNPAID",
        l2="NONE",
        tpc_207_trigger=False,
        numbered_release="NO",
        registry_rows=68,
        source_rows=5,
        dependency_rows=5,
        registry_digest=literal_registry_digest,
        source_digest="2ec49064c7ea65b11a455829941c6f05593c578d94d28c7fca61682aba329117",
        dependency_digest="58bb90e2f5284d1139d4fd56feb5b1c8a28f1831969195608121628fc20d2cb0",
        selected_delta="1/96",
        required_delta="STRICTLY_GREATER_THAN_1_OVER_400",
        first_fatal="NO_PRIMARY_POWER_SAVING_POLARIZED_PRIME_BDH_OR_COLLECTIVE_BP_COMPILER",
    )

    base_result = dict_type(
        check=True,
        maximum_claim=literal_maximum_claim,
        route_advance="YES",
        conditional_bridge_advance="YES",
        arithmetic_advance=False,
        fixed_atom_credit=0,
        strict_1_over_400="UNPAID",
        l2="NONE",
        tpc_207_trigger=False,
        numbered_release="NO",
        registry_rows=68,
        source_rows=5,
        dependency_rows=5,
        registry_digest=literal_registry_digest,
        source_digest="2ec49064c7ea65b11a455829941c6f05593c578d94d28c7fca61682aba329117",
        dependency_digest="58bb90e2f5284d1139d4fd56feb5b1c8a28f1831969195608121628fc20d2cb0",
        polarization_real=4,
        polarization_imag=-7,
        q5_cross=-15,
        q5_polarized_real=-15,
        q5_polarized_imag=0,
        q5_positive=2,
        q5_negative=-2,
        q5_wrong_q_minus_1=-12,
        q5_no_diagonal=-24,
        translation_exclude_zero="3/4",
        translation_exclude_one="75",
        all_moduli_signed=0,
        prime_subset_signed=1,
        h_exponent="21/32",
        q_exponent="1/3",
        block_count_exponent="11/32",
        local_qweighted_scale="127/96",
        global_natural_scale="5/3",
        conductor_gap="1/96",
        bp_x_saving="1/96",
        required_delta="STRICTLY_GREATER_THAN_1_OVER_400",
        selected_delta="1/96",
        selected_numerator="53/32",
        selected_physical_output="95/96",
        selected_margin="19/2400",
        direct_primary_source="NONE",
        first_fatal="NO_PRIMARY_POWER_SAVING_POLARIZED_PRIME_BDH_OR_COLLECTIVE_BP_COMPILER",
        route_position="BRIDGE_A_GATE_B_POLARIZED_PRIME_BDH_CONSTRUCTION_ZONE",
    )

    contract_mutations_expected = 3 * len_fn(expected_contract) + 2
    registry_mutations_expected = 2 * len_fn(literal_registry) + 2
    source_mutations_expected = 2 * len_fn(literal_sources) + 2
    dependency_mutations_expected = 2 * len_fn(literal_dependencies) + 2
    full_result_size = len_fn(base_result) + 6
    result_mutations_expected = 3 * full_result_size + 2
    mutation_actions_expected = (
        contract_mutations_expected
        + registry_mutations_expected
        + source_mutations_expected
        + dependency_mutations_expected
        + result_mutations_expected
    )

    expected_result = dict_type(base_result)
    expected_result.update(
        contract_mutations=contract_mutations_expected,
        registry_mutations=registry_mutations_expected,
        source_mutations=source_mutations_expected,
        dependency_mutations=dependency_mutations_expected,
        result_mutations=result_mutations_expected,
        mutation_actions=mutation_actions_expected,
    )

    def wrong_value(value):
        if type_fn(value) is bool_type:
            return not value
        if type_fn(value) is int_type:
            return value + 1
        if type_fn(value) is str_type:
            return value + "__MUT"
        raise failure_type("unsupported mutation value")

    def wrong_type(value):
        if type_fn(value) is bool_type:
            return int_type(value)
        if type_fn(value) is int_type:
            return bool_type(value)
        if type_fn(value) is str_type:
            return FauxStr(value)
        raise failure_type("unsupported mutation type")

    def must_reject(label, function, candidate):
        before = len_fn(mutation_labels)
        try:
            function(candidate)
        except failure_type:
            mutation_labels.append(label)
        else:
            raise failure_type("mutation accepted: " + label)
        if len_fn(mutation_labels) != before + 1:
            raise failure_type("mutation trace failed: " + label)

    def mutate_mapping(prefix, expected, validator):
        start = len_fn(mutation_labels)
        for key, value in expected.items():
            candidate = dict_type(expected)
            candidate[key] = wrong_value(value)
            must_reject(prefix + ":value:" + key, validator, candidate)
            candidate = dict_type(expected)
            candidate[key] = wrong_type(value)
            must_reject(prefix + ":type:" + key, validator, candidate)
            candidate = dict_type(expected)
            del candidate[key]
            must_reject(prefix + ":missing:" + key, validator, candidate)
        candidate = dict_type(expected)
        candidate[prefix + "_extra"] = 0
        must_reject(prefix + ":extra", validator, candidate)
        first_key = next(iter(expected))
        candidate = dict_type(expected)
        value = candidate.pop(first_key)
        candidate[KeyImpostor(first_key)] = value
        must_reject(prefix + ":key_impostor", validator, candidate)
        return len_fn(mutation_labels) - start

    def mutate_rows(prefix, rows, validator):
        start = len_fn(mutation_labels)
        for index, row in enumerate_fn(rows):
            candidate = list_type(rows)
            if type_fn(row) is str_type:
                candidate[index] = row + "__MUT"
            else:
                changed = list_type(row)
                changed[-1] = changed[-1] + "__MUT"
                candidate[index] = tuple_type(changed)
            must_reject(prefix + ":value:" + str_type(index), validator, tuple_type(candidate))
            candidate = list_type(rows)
            candidate[index] = list_type(row) if type_fn(row) is tuple_type else FauxStr(row)
            must_reject(prefix + ":type:" + str_type(index), validator, tuple_type(candidate))
        must_reject(prefix + ":missing", validator, tuple_type(rows[:-1]))
        must_reject(prefix + ":extra", validator, tuple_type(rows) + (rows[-1],))
        return len_fn(mutation_labels) - start

    def run():
        mutation_labels.clear()
        validate_registry(literal_registry)
        validate_sources(literal_sources)
        validate_dependencies(literal_dependencies)
        exact_mapping(expected_contract, expected_contract, "contract")

        if rows_digest(literal_registry) != literal_registry_digest:
            raise failure_type("registry digest mismatch")
        if table_digest(literal_sources) != expected_contract["source_digest"]:
            raise failure_type("source digest mismatch")
        if table_digest(literal_dependencies) != expected_contract["dependency_digest"]:
            raise failure_type("dependency digest mismatch")

        pair_value = polarization(
            (fraction_type(2), fraction_type(3)),
            (fraction_type(-1), fraction_type(2)),
        )
        if pair_value != (fraction_type(4), fraction_type(-7)):
            raise failure_type("complex polarization fixture changed")

        beta = (1, -2, 3, 0)
        physical = (2, 1, -1, 4)
        direct_cross = sum_fn(
            (fraction_type(b * w) for b, w in zip(beta, physical)),
            fraction_type(0),
        ) - sum_fn(beta) * sum_fn(physical)
        polarized = polarized_q5(beta, physical)
        wrong_diagonal = polarized_q5(beta, physical, diagonal_multiplier=4)
        no_diagonal = polarized_q5(beta, physical, include_diagonal=False)
        if direct_cross != -15 or polarized != (fraction_type(-15), fraction_type(0)):
            raise failure_type("q5 cross fixture changed")
        if wrong_diagonal != (fraction_type(-12), fraction_type(0)):
            raise failure_type("q5 diagonal multiplicity firewall changed")
        if no_diagonal != (fraction_type(-24), fraction_type(0)):
            raise failure_type("q5 diagonal omission firewall changed")

        positive = offdiag_energy(
            ((fraction_type(1), fraction_type(0)), (fraction_type(-1), fraction_type(0)), zero, zero),
            3,
            True,
        )
        negative = offdiag_energy(
            ((fraction_type(1), fraction_type(0)), (fraction_type(1), fraction_type(0)), zero, zero),
            3,
            True,
        )
        if positive != 2 or negative != -2:
            raise failure_type("q5 sign fixture changed")

        masses = tuple_type(fraction_type(v) for v in (10, 1, 0, 0, 0))
        if variance_excluding(masses, 0) != fraction_type(3, 4):
            raise failure_type("translation zero fixture changed")
        if variance_excluding(masses, 1) != fraction_type(75):
            raise failure_type("translation one fixture changed")

        h_exp = fraction_type(21, 32)
        q_exp = fraction_type(1, 3)
        if 1 - h_exp != fraction_type(11, 32):
            raise failure_type("block count exponent changed")
        if 2 * q_exp + h_exp != fraction_type(127, 96):
            raise failure_type("local scale exponent changed")
        if (1 - h_exp) + 2 * q_exp + h_exp != fraction_type(5, 3):
            raise failure_type("natural scale exponent changed")
        if 2 * q_exp - h_exp != fraction_type(1, 96):
            raise failure_type("conductor gap changed")
        if q_exp * fraction_type(1, 32) != fraction_type(1, 96):
            raise failure_type("Blomer-Pascadi x saving changed")
        if fraction_type(5, 3) - fraction_type(1, 96) != fraction_type(53, 32):
            raise failure_type("selected numerator changed")
        if fraction_type(53, 32) - fraction_type(2, 3) != fraction_type(95, 96):
            raise failure_type("selected output changed")
        if fraction_type(1, 96) - fraction_type(1, 400) != fraction_type(19, 2400):
            raise failure_type("strict margin changed")

        contract_count = mutate_mapping(
            "contract", expected_contract, lambda value: exact_mapping(value, expected_contract, "contract")
        )
        registry_count = mutate_rows("registry", literal_registry, validate_registry)
        source_count = mutate_rows("source", literal_sources, validate_sources)
        dependency_count = mutate_rows("dependency", literal_dependencies, validate_dependencies)
        result_count = mutate_mapping(
            "result", expected_result, lambda value: exact_mapping(value, expected_result, "result")
        )

        if contract_count != contract_mutations_expected:
            raise failure_type("contract mutation count changed")
        if registry_count != registry_mutations_expected:
            raise failure_type("registry mutation count changed")
        if source_count != source_mutations_expected:
            raise failure_type("source mutation count changed")
        if dependency_count != dependency_mutations_expected:
            raise failure_type("dependency mutation count changed")
        if result_count != result_mutations_expected:
            raise failure_type("result mutation count changed")
        if len_fn(mutation_labels) != mutation_actions_expected:
            raise failure_type("mutation action total changed")
        if len_fn(set_type(mutation_labels)) != mutation_actions_expected:
            raise failure_type("mutation labels not unique")

        result = dict_type(expected_result)
        exact_mapping(result, expected_result, "result")
        return dict_type(result)

    return run


_TRUSTED_RUN = _make_trusted_runner()


def _make_public_runner(*, runner=_TRUSTED_RUN):
    """Seal the public API against later module-global runner rebinding."""

    def sealed():
        return runner()

    return sealed


run_check = _make_public_runner()
_BASELINE_RESULT = run_check()
_BASELINE_ITEMS = tuple(sorted(_BASELINE_RESULT.items()))
_FROZEN_STDOUT = json.dumps(
    _BASELINE_RESULT, sort_keys=True, separators=(",", ":"), ensure_ascii=True
)


def _make_main(
    *,
    runner=_TRUSTED_RUN,
    baseline_items=_BASELINE_ITEMS,
    frozen_stdout=_FROZEN_STDOUT,
    tuple_type=tuple,
    str_type=str,
    type_fn=type,
    len_fn=len,
    sorted_fn=sorted,
    print_fn=print,
    failure_type=CheckFailure,
):
    def sealed(*argv_objects):
        if len_fn(argv_objects) != 1:
            raise failure_type("explicit --check is required")
        candidate = argv_objects[0]
        try:
            args = tuple_type(candidate)
        except Exception as exc:
            raise failure_type("explicit --check is required") from exc
        if len_fn(args) != 1 or type_fn(args[0]) is not str_type or args != ("--check",):
            raise failure_type("explicit --check is required")
        result = runner()
        if tuple_type(sorted_fn(result.items())) != baseline_items:
            raise failure_type("sealed result changed")
        print_fn(frozen_stdout)
        return 0

    return sealed


main = _make_main()


if __name__ == "__main__":
    try:
        raise SystemExit(main(tuple(sys.argv[1:])))
    except CheckFailure as exc:
        print(f"CheckFailure: {exc}", file=sys.stderr)
        raise SystemExit(1)
