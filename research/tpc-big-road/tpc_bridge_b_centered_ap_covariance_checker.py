#!/usr/bin/env python3
"""Fail-closed finite checker for the V47 centered AP covariance atlas."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever a frozen V47 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "EXACT_ADDITIVE_ZERO_MODE_EXCISION_STRICTLY_REDUCES_V46_ALL_RESIDUE_"
    "AP_BDH_TO_ONE_CENTERED_SIGNED_PRIME_HYBRID_COVARIANCE_GATE_AND_"
    "RANKS_TWO_EXPLICIT_FALLBACK_LANES"
)


REGISTRY = (
    "V47_MAXIMUM_CLAIM = EXACT_ADDITIVE_ZERO_MODE_EXCISION_STRICTLY_REDUCES_V46_ALL_RESIDUE_AP_BDH_TO_ONE_CENTERED_SIGNED_PRIME_HYBRID_COVARIANCE_GATE_AND_RANKS_TWO_EXPLICIT_FALLBACK_LANES",
    "V47_ROUTE_ADVANCE = YES",
    "V47_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V47_ARITHMETIC_ADVANCE = NO",
    "V47_FIXED_ATOM_CREDIT = 0",
    "V47_STRICT_1_OVER_400 = UNPAID",
    "V47_L2 = NONE",
    "V47_TPC_207_TRIGGER = false",
    "V47_NUMBERED_RELEASE = NO",
    "V47_DERIVATION_STATUS = COHERENT_AFTER_EXACT_ADDITIVE_ZERO_MODE_EXCISION_CENTERED_PARSEVAL_AND_PRIME_HYBRID_LOCAL_ERROR_SPLIT",
    "V47_ASSUMPTION_POLICY = CENTERED_SIGNED_COVARIANCE_IS_OPEN_AND_NATURAL_SCALE_RHO_ZERO_IS_EXPLICITLY_CONJECTURAL",
    "V47_SELECTED_RESEARCH_ROUTE = CENTERED_SIGNED_PRIME_HYBRID_COVARIANCE_FIRST__SEPARATE_MARGINALS_SECOND__V45_CONDUCTOR_ATLAS_INDEPENDENT_FALLBACK__LONG_MOBIUS_NEXT__V42_GATE_B_PARALLEL__V43_A_B_JOIN__C_RESERVE",
    "V47_V46_LOCAL_EULER_PAYMENT = RETAINED_SOURCE_BACKED_NORMALIZED_X_POWER_1891_OVER_1920",
    "V47_V46_LOCAL_ENDPOINT_MARGIN = RETAINED_121_OVER_9600",
    "V47_V46_RECIPROCAL_OCCUPANCY_ENERGY = RETAINED_PROVED_P_SQUARED_X_O1",
    "V47_ADDITIVE_ZERO_MODE_SUPPORT = PROVED_EXACT_A_D_ZERO_EQUALS_ZERO",
    "V47_ADDITIVE_ZERO_MODE_REASON = PROVED_ZERO_LT_ABS_M_LT_D_AND_Q_INVERTIBLE_MOD_D",
    "V47_NONZERO_FREQUENCY_PAIRING = PROVED_EXACT_BEFORE_OUTER_ABSOLUTE",
    "V47_CENTERED_RESIDUAL = DEFINED_R_D_CIRCLE_EQUALS_R_D_MINUS_RESIDUE_AVERAGE",
    "V47_CENTERED_PARSEVAL = PROVED_EXACT_NONZERO_FOURIER_ENERGY_EQUALS_D_TIMES_CENTERED_RESIDUE_ENERGY",
    "V47_CONSTANT_RESIDUE_SHIFT_INVARIANCE = PROVED_EXACT_FOR_PHYSICAL_PAIRING",
    "V47_ZERO_MODE_SCOPE_FIREWALL = ADDITIVE_CONSTANT_ONLY_DOES_NOT_DELETE_MULTIPLICATIVE_PRINCIPAL_LOW_CONDUCTOR_EXCEPTIONAL_OR_NONUNIT_MODES",
    "V47_CENTERED_GATE_STRENGTH = STRICTLY_WEAKER_THAN_V46_FULL_ENERGY_IN_AMBIENT_SPACE_AND_SUFFICIENT_FOR_THE_LITERAL_PAIRING",
    "V47_LITERAL_FAMILY_STRICTNESS = NOT_CLAIMED_BY_FINITE_AMBIENT_FIXTURE",
    "V47_SHIFTED_PRIME_LOCAL_ERROR = DEFINED_LAMBDA_U_PLUS_2_MINUS_P_D_A_OVER_LOG_U",
    "V47_HYBRID_LOCAL_ERROR = DEFINED_B_Z_U_MINUS_B_D_Z_A_OVER_LOG_U",
    "V47_SIGNED_LOCAL_ERROR_SPLIT = PROVED_EXACT_R_D_EQUALS_P_D_ERROR_MINUS_H_D_ERROR",
    "V47_CENTERED_SIGNED_SPLIT = PROVED_EXACT_R_D_CIRCLE_EQUALS_P_D_CIRCLE_MINUS_H_D_CIRCLE",
    "V47_PRIME_HYBRID_COVARIANCE_IDENTITY = PROVED_EXACT_E_R_EQUALS_E_P_PLUS_E_H_MINUS_TWO_REAL_COVARIANCE",
    "V47_CENTERED_COVARIANCE_ENERGY = DEFINED_SUM_D_D_SUM_A_ABS_R_D_CIRCLE_SQUARED",
    "V47_CENTERED_COVARIANCE_NATURAL_SCALE = X_TIMES_U_SQUARED_EQUALS_X_POWER_333_OVER_200",
    "V47_CENTERED_COVARIANCE_GATE = OPEN_X_U_SQUARED_X_POWER_RHO_WITH_ZERO_LE_RHO_LT_33_OVER_100",
    "V47_CENTERED_COVARIANCE_BENCHMARK = CONJECTURAL_RHO_EQUALS_ZERO",
    "V47_CENTERED_RESIDUAL_NUMERATOR_OUTPUT = CONDITIONAL_X_POWER_1799_OVER_1200_PLUS_RHO_OVER_2_PLUS_O1",
    "V47_CENTERED_RESIDUAL_NORMALIZED_OUTPUT = CONDITIONAL_X_POWER_333_OVER_400_PLUS_RHO_OVER_2_PLUS_O1",
    "V47_CENTERED_RESIDUAL_MARGIN = 33_OVER_200_MINUS_RHO_OVER_2",
    "V47_TRANSITION_CONDITIONAL_COMPILER = PROVED_CENTERED_COVARIANCE_GATE_PAYS_FULL_TRANSITION_WITH_V46_LOCAL_AND_V44_CORRECTIONS",
    "V47_TRANSITION_CONDITIONAL_MARGIN = MIN_121_OVER_9600_33_OVER_200_MINUS_RHO_OVER_2_13_OVER_4800_817_OVER_4800",
    "V47_SEPARATE_PRIME_VARIANCE = OPEN_HEURISTIC_HOOLEY_PROFILE_WRONG_LITERAL_SOURCE_INTERFACE",
    "V47_SEPARATE_HYBRID_VARIANCE = OPEN_NEW_SIEVE_AP_VARIANCE_THEOREM",
    "V47_SEPARATE_MARGINAL_COMPILER = PROVED_SUFFICIENT_BY_CENTERED_L2_TRIANGLE",
    "V47_SEPARATE_MARGINAL_STRENGTH = STRICTLY_STRONGER_IN_FINITE_AMBIENT_SPACE_NOT_CLAIMED_FOR_LITERAL_FAMILY",
    "V47_CLASSICAL_MAIN_MESH = OPTIONAL_PROVED_U_CUBED_X_O1",
    "V47_CLASSICAL_MAIN_MESH_EXPONENT = 399_OVER_400",
    "V47_EXACT_LOCAL_PROFILE_PREFERENCE = SELECTED_NO_MESH_AND_NO_LOG_DENOMINATOR_REPLACEMENT",
    "V47_V45_HIGH_CONDUCTOR_PAYMENT = RETAINED_INDEPENDENT_SOURCE_BACKED_X_POWER_213_OVER_128",
    "V47_V45_TO_CENTERED_SPLICE = OPEN_EXACT_PROJECTION_COMPILER_NO_DOUBLE_COUNTING",
    "V47_LONG_BALANCED_WINDOW = OPEN_D_GT_U_AND_K_GT_U",
    "V47_LONG_REVERSE_TYPE_I_WINDOW = OPEN_D_GT_U_AND_K_LE_U",
    "V47_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE",
    "V47_FIORILLI_HOOLEY_VARIANCE = HEURISTIC_SUPPORT_ONLY_NO_UNIFORM_LITERAL_THEOREM_BELOW_SQUARE_ROOT",
    "V47_BAKER_FREIBERG_DIRECT_ATTACHMENT = STOP_SCOPED_SPARSE_MODULUS_SEQUENCE_NOT_COMPLETE_SQUAREFREE_TRANSITION_FAMILY",
    "V47_KOUKOULOPOULOS_DIRECT_ATTACHMENT = STOP_SCOPED_MOST_MODULI_AND_INTERVAL_ORIGINS_NOT_ONE_FIXED_COMPLETE_LITERAL_FAMILY",
    "V47_SIFTED_RESTRICTION_DIRECT_ATTACHMENT = STOP_SCOPED_WRONG_NORM_AND_NO_LITERAL_B_Z_CENTERED_AP_COVARIANCE",
    "V47_CLASSICAL_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_RANGE_AND_MODULUS_DEPENDENT_PROFILE_MISMATCH_RETAINED_FROM_V46",
    "V47_DIRECT_PRIMARY_SOURCE_FOR_CENTERED_COVARIANCE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11",
    "V47_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_NATURAL_SCALE_CENTERED_SIGNED_PRIME_HYBRID_AP_COVARIANCE_UNIFORMLY_FOR_X_POWER_31_OVER_96_LT_D_LE_X_POWER_133_OVER_400",
    "V47_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_LOCAL_EULER_PAID_ADDITIVE_ZERO_MODE_DELETED_CENTERED_PRIME_HYBRID_COVARIANCE_OPEN_LONG_MOBIUS_SPAN_OPEN",
    "V47_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED",
    "V47_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B",
)


REGISTRY_SHA256 = "88582aea629c50b0b935f99a9a8784e8fb946b3002a3d72be69217792744562b"


SOURCE_LOCKS = (
    ("1301.5663", "Daniel Fiorilli", "Hooley variance below square root is heuristic or conditional, not the literal V47 theorem"),
    ("1706.07319", "Roger Baker; Tristan Freiberg", "variance over sparse moduli [F(n)], not the complete transition family"),
    ("1405.6592", "Dimitris Koukoulopoulos", "most moduli and most interval origins, not one fixed complete family"),
    ("2512.21640", "Tanmoy Bera; G. K. Viswanadham", "restriction norm for sifted integers, not centered AP covariance"),
    ("1111.6190", "Mark Lewko; Allison Lewko", "variational BDH in the classical large-modulus regime"),
    ("2412.19644", "Adam J. Harper", "general-sequence BDH requires Q greater than sqrt(2x)"),
    ("1909.12280", "Oleksiy Klurman; Alexander P. Mangerel; Joni Teravainen", "bounded multiplicative almost-all-modulus interface"),
)


DEPENDENCIES = (
    ("research/tpc-big-road/bridge_b_centered_ap_covariance_and_prime_hybrid_atlas.md", "5501dffe68adbefc8d53021ca2539cd2a8934128f08205a97cea973597682d7f"),
    ("research/tpc-big-road/bridge_b_transition_native_euler_bdh_compiler.md", "f834c13f689b8283c40bd962b0ec4fa5cdcaaee061eca1914a6356a1cfd96011"),
    ("research/tpc-big-road/tpc_bridge_b_transition_native_euler_bdh_checker.py", "e679064886b4cc7ada2e63f75605bbcff7b5ade6eb6af7f1af8b6c46a64ddcc8"),
    ("research/tpc-big-road/bridge_b_conductor_stratified_transition_spectrum.md", "0a797eb4e3791319624fb5dd7a597d6d6bb217b46759739a51854312df6f4ec9"),
    ("research/tpc-big-road/bridge_b_transition_reciprocal_variance_and_ramanujan_mean.md", "053ae6a18740a2e81d754c4ecce7af1a00ecfe331f7d5d4991945889f14c9920"),
    ("research/tpc-big-road/bridge_b_euler_zero_axis_and_kernel_carrier.md", "922d5601b088a8a3a8dd52d3e9d186c85e7fea00ca670f3c6f324c1d433da464"),
    ("research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md", "fd02eaf5504b7a7c2182a8a045b9ec03488ef72ef7b88e750ba781163c10525a"),
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
    file_seed=__file__,
):
    literal_maximum_claim = (
        "EXACT_ADDITIVE_ZERO_MODE_EXCISION_STRICTLY_REDUCES_V46_ALL_RESIDUE_"
        "AP_BDH_TO_ONE_CENTERED_SIGNED_PRIME_HYBRID_COVARIANCE_GATE_AND_"
        "RANKS_TWO_EXPLICIT_FALLBACK_LANES"
    )
    literal_registry_digest = "88582aea629c50b0b935f99a9a8784e8fb946b3002a3d72be69217792744562b"
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
        payload = ("\n".join(rows) + "\n").encode("utf-8")
        return sha256_fn(payload).hexdigest()

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
        data = path_read_bytes(path).replace(b"\r\n", b"\n")
        return sha256_fn(data).hexdigest()

    def validate_dependencies(candidate):
        if not same_exact(candidate, literal_dependencies):
            raise CheckFailure("dependency lock changed")
        for relative, expected_hash in candidate:
            if canonical_file_hash(repo_root / relative) != expected_hash:
                raise CheckFailure("dependency hash changed: " + relative)

    def dft4(values):
        roots = ((1, 0), (0, 1), (-1, 0), (0, -1))
        output = []
        for r in range_fn(4):
            real = 0
            imag = 0
            for a, value in enumerate_fn(values):
                rr, ii = roots[(r * a) % 4]
                real += value * rr
                imag += value * ii
            output.append((real, imag))
        return tuple_type(output)

    def finite_fixtures():
        d = 5
        occupancy = [0] * d
        for q in (7, 11):
            inverse_q = pow_fn(q, -1, d)
            for m in (-2, -1, 1, 2):
                occupancy[(m * inverse_q) % d] += 1
        occupancy = tuple_type(occupancy)

        raw = (7, 3, 5, 1)
        mean = sum_fn(raw) // 4
        centered = tuple_type(value - mean for value in raw)
        raw_dft = dft4(raw)
        centered_dft = dft4(centered)
        centered_energy = sum_fn(re * re + im * im for re, im in centered_dft[1:])
        centered_physical_energy = 4 * sum_fn(value * value for value in centered)
        shifted_dft = dft4(tuple_type(value + 137 for value in raw))

        prime = (10, -10, 10, -10)
        hybrid = (9, -9, 9, -9)
        residual = tuple_type(p - h for p, h in zip_fn(prime, hybrid))
        prime_energy = 4 * sum_fn(v * v for v in prime)
        hybrid_energy = 4 * sum_fn(v * v for v in hybrid)
        covariance = 4 * sum_fn(p * h for p, h in zip_fn(prime, hybrid))
        signed_energy = 4 * sum_fn(v * v for v in residual)

        p = 5
        delta5 = []
        for a in range_fn(p):
            f = fraction_type(0, 1) if a == p - 2 else fraction_type(p, p - 1)
            g = fraction_type(p, p - 1) if a == 0 else fraction_type(p * (p - 2), (p - 1) ** 2)
            delta5.append(f - g)
        delta5 = tuple_type(delta5)

        exponents = dict_type((
            ("H", fraction_type(21, 32)),
            ("Q", fraction_type(1, 3)),
            ("U", fraction_type(133, 400)),
            ("Y0", fraction_type(31, 96)),
            ("P", fraction_type(1, 96)),
            ("L_pr", fraction_type(2, 3)),
        ))
        natural = 1 + 2 * exponents["U"]
        coefficient = 2 * exponents["P"]
        numerator = exponents["H"] + exponents["P"] + natural / 2
        normalized = numerator - exponents["L_pr"]
        margin = fraction_type(1997, 1200) - numerator
        local_numerator = fraction_type(1057, 640)
        local_margin = fraction_type(1997, 1200) - local_numerator
        mesh = 3 * exponents["U"]

        return dict_type((
            ("occupancy", occupancy),
            ("raw_dft", raw_dft),
            ("mean", mean),
            ("centered", centered),
            ("centered_dft", centered_dft),
            ("centered_energy", centered_energy),
            ("centered_physical_energy", centered_physical_energy),
            ("constant_shift_nonzero_invariant", shifted_dft[1:] == raw_dft[1:]),
            ("prime_energy", prime_energy),
            ("hybrid_energy", hybrid_energy),
            ("covariance", covariance),
            ("signed_energy", signed_energy),
            ("covariance_identity", signed_energy == prime_energy + hybrid_energy - 2 * covariance),
            ("delta5", delta5),
            ("delta5_sum", sum_fn(delta5, fraction_type(0, 1))),
            ("exponents", exponents),
            ("natural", natural),
            ("coefficient", coefficient),
            ("numerator", numerator),
            ("normalized", normalized),
            ("margin", margin),
            ("local_numerator", local_numerator),
            ("local_margin", local_margin),
            ("mesh", mesh),
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
        ("source_locks", 7),
        ("dependency_locks", 7),
        ("H", "21/32"),
        ("Q", "1/3"),
        ("U", "133/400"),
        ("Y0", "31/96"),
        ("P", "1/96"),
        ("L_pr", "2/3"),
        ("natural_energy", "333/200"),
        ("occupancy_energy", "1/48"),
        ("residual_numerator", "1799/1200"),
        ("residual_normalized", "333/400"),
        ("residual_margin", "33/200"),
        ("rho_cutoff", "33/100"),
        ("local_numerator", "1057/640"),
        ("local_margin", "121/9600"),
        ("mesh_exponent", "399/400"),
        ("occupancy", (0, 2, 2, 2, 2)),
        ("centered_mean", 4),
        ("centered_vector", (3, -1, 1, -3)),
        ("centered_dft", ((2, 2), (8, 0), (2, -2))),
        ("centered_energy", 80),
        ("prime_energy", 1600),
        ("hybrid_energy", 1296),
        ("covariance", 1440),
        ("signed_energy", 16),
        ("delta5", ("0", "5/16", "5/16", "-15/16", "5/16")),
        ("source_attachment", False),
        ("first_fatal", "NO_LITERAL_THEOREM_PROVES_NATURAL_SCALE_CENTERED_SIGNED_PRIME_HYBRID_AP_COVARIANCE"),
        ("route_position", "BRIDGE_A_CENTERED_PRIME_HYBRID_COVARIANCE_OPEN"),
    )
    expected_contract = dict_type(contract_items)

    def validate_contract(candidate):
        if not same_exact(candidate, expected_contract):
            raise CheckFailure("contract changed")

    def fraction_text(value):
        return str_type(value.numerator) if value.denominator == 1 else str_type(value.numerator) + "/" + str_type(value.denominator)

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
            ("additive_zero_mode", fixture["occupancy"][0] == 0),
            ("occupancy", fixture["occupancy"]),
            ("centered_parseval", fixture["centered_energy"] == fixture["centered_physical_energy"]),
            ("constant_shift_invariant", fixture["constant_shift_nonzero_invariant"]),
            ("centered_vector", fixture["centered"]),
            ("centered_dft", fixture["centered_dft"][1:]),
            ("centered_energy", fixture["centered_energy"]),
            ("prime_energy", fixture["prime_energy"]),
            ("hybrid_energy", fixture["hybrid_energy"]),
            ("covariance", fixture["covariance"]),
            ("signed_energy", fixture["signed_energy"]),
            ("covariance_identity", fixture["covariance_identity"]),
            ("delta5", tuple_type(fraction_text(v) for v in fixture["delta5"])),
            ("delta5_zero_mean", fixture["delta5_sum"] == 0),
            ("natural_energy", fraction_text(fixture["natural"])),
            ("occupancy_energy", fraction_text(fixture["coefficient"])),
            ("residual_numerator", fraction_text(fixture["numerator"])),
            ("residual_normalized", fraction_text(fixture["normalized"])),
            ("residual_margin", fraction_text(fixture["margin"])),
            ("rho_cutoff", "33/100"),
            ("local_numerator", fraction_text(fixture["local_numerator"])),
            ("local_margin", fraction_text(fixture["local_margin"])),
            ("mesh_exponent", fraction_text(fixture["mesh"])),
            ("preferred_lane", "SIGNED_CENTERED_PRIME_HYBRID_COVARIANCE"),
            ("separate_marginals", "SUFFICIENT_BUT_STRONGER"),
            ("v45_lane", "INDEPENDENT_FALLBACK_REQUIRES_SPLICE_COMPILER"),
            ("source_attachment", False),
            ("first_fatal", "NO_LITERAL_THEOREM_PROVES_NATURAL_SCALE_CENTERED_SIGNED_PRIME_HYBRID_AP_COVARIANCE"),
            ("route_position", "BRIDGE_A_CENTERED_PRIME_HYBRID_COVARIANCE_OPEN"),
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
                return hash("maximum_claim")

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

    if fixture["occupancy"] != (0, 2, 2, 2, 2):
        raise CheckFailure("occupancy fixture changed")
    if fixture["raw_dft"] != ((16, 0), (2, 2), (8, 0), (2, -2)):
        raise CheckFailure("raw DFT changed")
    if fixture["centered"] != (3, -1, 1, -3):
        raise CheckFailure("centering changed")
    if fixture["centered_dft"] != ((0, 0), (2, 2), (8, 0), (2, -2)):
        raise CheckFailure("centered DFT changed")
    if fixture["centered_energy"] != 80 or fixture["centered_physical_energy"] != 80:
        raise CheckFailure("centered Parseval changed")
    if not fixture["constant_shift_nonzero_invariant"]:
        raise CheckFailure("constant shift entered nonzero frequencies")
    if not fixture["covariance_identity"] or fixture["signed_energy"] != 16:
        raise CheckFailure("covariance identity changed")
    if fixture["delta5"] != (
        fraction_type(0), fraction_type(5, 16), fraction_type(5, 16),
        fraction_type(-15, 16), fraction_type(5, 16),
    ):
        raise CheckFailure("delta5 changed")
    expected_fractions = (
        (fixture["natural"], fraction_type(333, 200)),
        (fixture["coefficient"], fraction_type(1, 48)),
        (fixture["numerator"], fraction_type(1799, 1200)),
        (fixture["normalized"], fraction_type(333, 400)),
        (fixture["margin"], fraction_type(33, 200)),
        (fixture["local_numerator"], fraction_type(1057, 640)),
        (fixture["local_margin"], fraction_type(121, 9600)),
        (fixture["mesh"], fraction_type(399, 400)),
    )
    if not all_fn(got == want for got, want in expected_fractions):
        raise CheckFailure("exponent ledger changed")

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

    expected_counts = (131, 124, 17, 17, 151, 440)
    actual_counts = (
        contract_mutations, registry_mutations, source_mutations,
        dependency_mutations, semantic_mutations, mutation_actions,
    )
    if actual_counts != expected_counts:
        raise CheckFailure("mutation counts changed")
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
    dict_type=dict,
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
