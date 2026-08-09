#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V36 multiroute bridge atlas."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_PROPER_FACTOR_RECOLLAPSE_TO_BINARY_OFF_DIAGONAL_HYBRID_"
    "CHARACTER_COVARIANCE_PLUS_ONE_OF_THREE_CONDITIONAL_GATE_B_COMPILER_"
    "AND_EXPLICIT_HEURISTIC_CHARTER"
)


CONTRACT_ITEMS = (
    ("schema_version", "V36_MULTIROUTE_RATIO_CORE_V1"),
    ("artifact_name", "bridge_b_multiroute_ratio_core_atlas.md"),
    ("baseline_commit", "cb5467a3bef6137b8969d44b380e37352aee30f4"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("route_position", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_THREE_CONDITIONAL_LANES_MARKED"),
    ("route_advance", "YES"),
    ("conditional_bridge_advance", "YES"),
    ("arithmetic_advance", False),
    ("fixed_atom_credit", 0),
    ("strict_1_over_400", "UNPAID"),
    ("L2", "NONE"),
    ("TPC_207_TRIGGER", False),
    ("numbered_release", "NO"),
    ("H", "x^(21/32)"),
    ("Q", "x^(1/3)"),
    ("L_pr", "x^(2/3+o(1))"),
    ("paid_remainder", "x^(53/32+o(1))"),
    ("core_target", "x^(5/3-delta+o(1))"),
    ("required_delta", "delta>1/400"),
    ("route_E", "weighted_residual_energy_sigma<13/4800"),
    ("route_K0", "collective_Q^(-31/32)_compiler_conjecture"),
    ("route_K1", "source_backed_Q^(-1/32)_cell_gain"),
    ("route_X", "joint_character_kappa>403/1200"),
    ("route_logic", "E_OR_K_OR_X"),
    ("fixture_primes", (5, 7)),
    ("fixture_core", "-2257/432"),
    ("heuristic_exponent", "223/192"),
    ("first_fatal", "NO_LITERAL_THEOREM_SUPPLIES_ANY_ONE_OF_THE_THREE_CONJECTURAL_BRIDGE_INPUTS"),
)


REGISTRY_ITEMS = (
    ("V36_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V36_ROUTE_ADVANCE", "YES"),
    ("V36_CONDITIONAL_BRIDGE_ADVANCE", "YES"),
    ("V36_ARITHMETIC_ADVANCE", "NO"),
    ("V36_FIXED_ATOM_CREDIT", "0"),
    ("V36_STRICT_1_OVER_400", "UNPAID"),
    ("V36_L2", "NONE"),
    ("V36_TPC_207_TRIGGER", "false"),
    ("V36_NUMBERED_RELEASE", "NO"),
    ("V36_DERIVATION_STATUS", "COHERENT_AFTER_REFRAMING_AND_EXPLICIT_EXTRA_ASSUMPTIONS"),
    ("V36_ASSUMPTION_POLICY", "CONJECTURES_EXPLICIT_AND_NEVER_PROMOTED_TO_THEOREMS"),
    ("V36_SELECTED_RESEARCH_ROUTE", "K_COLLECTIVE_COMPILER_FIRST__E_ENERGY_SECOND__X_CHARACTER_THIRD__A_TERMINAL_AFTER_B__C_DYNAMICS_RESERVE"),
    ("V36_V35_CORE", "RETAINED_EXACT_PRIME_ONLY_ZERO_DELETED_COPRIME_RATIO_CORE"),
    ("V36_PROPER_FACTOR_RECOLLAPSE", "PROVED_EXACT_SUM_OCCURRENCES_BACK_TO_BETA_OF_T"),
    ("V36_BINARY_RATIO_CORE", "PROVED_EXACT_TWO_ARRAY_OFF_DIAGONAL_FORM"),
    ("V36_HYBRID_CHARACTER_INVERSION", "PROVED_EXACT_FOURIER_CHARACTER_NORMAL_FORM"),
    ("V36_CHARACTER_DIAGONAL_SUBTRACTION", "PROVED_EXACT_Z_Q_REQUIRED"),
    ("V36_ONE_OF_THREE_COMPILER", "PROVED_EXACT_CONDITIONAL_OR_GATE"),
    ("V36_ROUTE_E_STATUS", "OPEN_CONJECTURE_WHOLE_OBJECT_WEIGHTED_RESIDUAL_ENERGY"),
    ("V36_ROUTE_E_INPUT", "N_E_LE_X_POWER_1_PLUS_SIGMA_WITH_SIGMA_LT_13_OVER_4800"),
    ("V36_ROUTE_E_DELTA", "1_OVER_192_MINUS_SIGMA"),
    ("V36_ROUTE_E_ENDPOINT_MARGIN", "13_OVER_4800_MINUS_SIGMA"),
    ("V36_ROUTE_K0_STATUS", "OPEN_CONJECTURE_COLLECTIVE_Q_ELL_EMITTER_AND_REASSEMBLY"),
    ("V36_ROUTE_K0_STRUCTURAL_GAIN", "Q_POWER_MINUS_31_OVER_32"),
    ("V36_ROUTE_K1_STATUS", "SOURCE_BACKED_FIXED_MODULUS_CELL_ENGINE_AFTER_EXACT_EMISSION"),
    ("V36_ROUTE_K1_CELL_GAIN", "Q_POWER_MINUS_1_OVER_32"),
    ("V36_ROUTE_K_TOTAL_GAIN", "Q_POWER_MINUS_1_EQUALS_X_POWER_MINUS_1_OVER_3"),
    ("V36_ROUTE_K_DELTA", "1_OVER_96"),
    ("V36_ROUTE_K_ENDPOINT_MARGIN", "19_OVER_2400"),
    ("V36_ROUTE_X_STATUS", "OPEN_CONJECTURE_JOINT_HYBRID_CHARACTER_DECOUPLING"),
    ("V36_ROUTE_X_BASELINE", "X_POWER_2_PLUS_O1_FROM_SEPARATE_LARGE_SIEVE_CAUCHY"),
    ("V36_ROUTE_X_REQUIRED_KAPPA", "STRICTLY_GREATER_THAN_403_OVER_1200"),
    ("V36_ROUTE_X_DELTA", "KAPPA_MINUS_1_OVER_3"),
    ("V36_ROUTE_X_ENDPOINT_MARGIN", "KAPPA_MINUS_403_OVER_1200"),
    ("V36_RANDOM_PHASE_BENCHMARK", "HEURISTIC_ONLY_X_POWER_223_OVER_192"),
    ("V36_RANDOM_PHASE_GAP_TO_X_5_OVER_3", "97_OVER_192"),
    ("V36_SEPARATE_MARGINAL_LARGE_SIEVE", "STOP_SCOPED_X_POWER_2_DEFICIT_403_OVER_1200"),
    ("V36_FIXED_Q_TRIANGLE", "STOP_SCOPED_REQUIRES_Q_POWER_MINUS_31_OVER_32_MINUS_3_DELTA_BEFORE_MODULUS_SUM"),
    ("V36_BLOMER_PASCADI_CELL_ENGINE", "SOURCE_BACKED_Q_POWER_MINUS_1_OVER_32_AT_CRITICAL_FIXED_MODULUS_RANGE"),
    ("V36_BLOMER_PASCADI_DIRECT_ATTACHMENT", "STOP_SCOPED_NO_COLLECTIVE_Q_ELL_EMITTER_COEFFICIENT_COMPILER_OR_REASSEMBLY"),
    ("V36_FOUVRY_SHPARLINSKI_XI_DIRECT_ATTACHMENT", "STOP_SCOPED_FIXED_PRIME_SHORT_VARIABLES_WRONG_CROSS_WEIGHT_AND_NO_MODULUS_REASSEMBLY"),
    ("V36_DONG_ROBLES_ZEINDLER_DIRECT_ATTACHMENT", "STOP_SCOPED_FIXED_BILINEAR_FRACTION_NO_PHYSICAL_JOINT_COVARIANCE"),
    ("V36_RUNBO_LI_DIRECT_ATTACHMENT", "STOP_SCOPED_SPECIAL_HARMAN_MAJORANTS_AND_MODULUS_FORMS_WRONG_SIGNED_OBJECT"),
    ("V36_TERMINAL_A", "OPEN_TERMINAL_EQUIVALENT_SIGNED_QLOCAL_COVARIANCE_AFTER_B"),
    ("V36_DYNAMICS_C", "RESERVE_DISTINGUISHED_SEED_ATTACHMENT_STILL_OPEN"),
    ("V36_HEURISTIC_DOES_NOT_IMPLY_ARITHMETIC_ADVANCE", "PROVED_STATUS_FIREWALL"),
    ("V36_DIRECT_PRIMARY_SOURCE_ATTACHMENT", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09"),
    ("V36_NEXT_THEOREM", "COLLECTIVE_Q_POWER_MINUS_31_OVER_32_DETERMINANT_EMITTER_OR_WHOLE_RESIDUAL_SIGMA_LT_13_OVER_4800_OR_JOINT_CHARACTER_KAPPA_GT_403_OVER_1200"),
    ("V36_FIRST_FATAL", "NO_LITERAL_THEOREM_SUPPLIES_ANY_ONE_OF_THE_THREE_CONJECTURAL_BRIDGE_INPUTS"),
    ("V36_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_THREE_CONDITIONAL_LANES_MARKED"),
    ("V36_SOURCE_LOCK_POLICY", "PRIMARY_SOURCES_ONLY_FAIL_CLOSED"),
)


EXPECTED_REGISTRY_SHA256 = "6cf2ae8722d14ec0966e1461748f426b171654c6076ef5f0e56111aaa3c6bf48"


SOURCE_ITEMS = (
    ("MRT_ABSTRACT_ENERGY_REDUCTION", "arXiv:1707.01315v3_Proposition_3.1_equations_52_54"),
    ("BLOMER_PASCADI_KLOOSTERMAN_CELL", "arXiv:2607.24311v1_Theorem_1.1_Theorem_5.5"),
    ("FOUVRY_SHPARLINSKI_XI_CHARACTER_FORMS", "arXiv:2404.09295v4_Theorems_2.5_2.7"),
    ("DONG_ROBLES_ZEINDLER_FRACTIONS", "arXiv:2601.00292v1_main_bilinear_fraction_bounds"),
    ("RUNBO_LI_HARMAN_AP", "arXiv:2602.20917_Theorem_1.1"),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_proper_factor_unit_ratio_reduction.md",
        "705b0dfd4d94d70bad798ca6cccf7e0f37f049683d30373ea895d97a6db93da1",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_proper_factor_unit_ratio_checker.py",
        "8c5e3dcc03b6ac132baae8a0c0c1949fddc24a6f114fd61de416cf4a7b02bd51",
    ),
    (
        "research/tpc-big-road/bridge_b_base_scale_residual_oscillation_compiler.md",
        "13ec946f776008f4eadaf9a2576fa105f8500661075fe8993e04f25d3c0e6148",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_residual_oscillation_checker.py",
        "963b7ff835735252ffebfd2c9e05635c62738ab88ac59db859c31ac9f3202893",
    ),
    (
        "research/tpc-big-road/bridge_b_ramanujan_energy_and_pointed_block_gate.md",
        "90f8cd26b9dd6b99a4f5083e80cdf13fc6ec2498081e269455f9b12726e66c5c",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_ramanujan_energy_checker.py",
        "61bba5c8f860617e5e938b29a77d2ca85adddd4ce79f1b3e33811c31ab1d4580",
    ),
)


def _make_trusted_runner(
    maximum_claim_seed=MAXIMUM_CLAIM,
    contract_seed=CONTRACT_ITEMS,
    registry_seed=REGISTRY_ITEMS,
    registry_digest_seed=EXPECTED_REGISTRY_SHA256,
    source_seed=SOURCE_ITEMS,
    dependency_seed=DEPENDENCIES,
    root_seed=str(Path(__file__).resolve().parents[2]),
    failure_type=CheckFailure,
    fraction_type=Fraction,
    path_type=Path,
    path_is_file=Path.is_file,
    path_read_bytes=Path.read_bytes,
    sha256_fn=hashlib.sha256,
    dict_type=dict,
    list_type=list,
    tuple_type=tuple,
    set_type=set,
    str_type=str,
    int_type=int,
    bool_type=bool,
    type_fn=type,
    len_fn=len,
    range_fn=range,
    sum_fn=sum,
    abs_fn=abs,
    min_fn=min,
    sorted_fn=sorted,
    zip_fn=zip,
    pow_fn=pow,
    all_fn=all,
    enumerate_fn=enumerate,
):
    literal_maximum_claim = maximum_claim_seed
    literal_contract = tuple_type(contract_seed)
    literal_registry = tuple_type(registry_seed)
    literal_registry_digest = registry_digest_seed
    literal_sources = tuple_type(source_seed)
    literal_dependencies = tuple_type(dependency_seed)
    repo_root = path_type(root_seed)

    def exact_str(value: object) -> bool:
        return type_fn(value) is str_type

    def exact_int(value: object) -> bool:
        return type_fn(value) is int_type

    def exact_bool(value: object) -> bool:
        return type_fn(value) is bool_type

    def canonical_bytes(raw: bytes) -> bytes:
        return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

    def digest_bytes(raw: bytes) -> str:
        return sha256_fn(raw).hexdigest()

    def registry_bytes(candidate: tuple[tuple[str, str], ...]) -> bytes:
        return b"".join(
            (key + "=" + value + "\n").encode("utf-8") for key, value in candidate
        )

    def registry_digest(candidate: tuple[tuple[str, str], ...]) -> str:
        return digest_bytes(registry_bytes(candidate))

    def require_pairs(candidate: object, expected: tuple, label: str) -> None:
        if type_fn(candidate) is not tuple_type or len_fn(candidate) != len_fn(expected):
            raise failure_type(label + " shape changed")
        for row in candidate:
            if type_fn(row) is not tuple_type or len_fn(row) != 2:
                raise failure_type(label + " row shape changed")
            if not exact_str(row[0]) or not exact_str(row[1]):
                raise failure_type(label + " row type changed")
        if len_fn(set_type(key for key, _ in candidate)) != len_fn(candidate):
            raise failure_type(label + " keys not unique")
        if candidate != expected:
            raise failure_type(label + " semantic promotion")

    def require_mapping(candidate: object, expected: tuple, label: str) -> None:
        if type_fn(candidate) is not dict_type:
            raise failure_type(label + " outer type changed")
        if not all_fn(type_fn(key) is str_type for key in candidate):
            raise failure_type(label + " key type changed")
        expected_map = dict_type(expected)
        if set_type(candidate) != set_type(expected_map):
            raise failure_type(label + " key set changed")
        for key, value in expected:
            if type_fn(candidate[key]) is not type_fn(value) or candidate[key] != value:
                raise failure_type(label + " value changed at " + key)

    def validate_contract(candidate: object) -> None:
        require_mapping(candidate, literal_contract, "contract")

    def validate_registry(candidate: object, claimed_digest: object) -> None:
        require_pairs(candidate, literal_registry, "registry")
        if not exact_str(claimed_digest) or claimed_digest != literal_registry_digest:
            raise failure_type("registry digest changed")
        if registry_digest(candidate) != literal_registry_digest:
            raise failure_type("registry content digest changed")

    def validate_sources(candidate: object) -> None:
        require_pairs(candidate, literal_sources, "source")

    def validate_dependencies(candidate: object) -> None:
        require_pairs(candidate, literal_dependencies, "dependency")
        for relative, expected_hash in candidate:
            path = repo_root / relative
            if not path_is_file(path):
                raise failure_type("dependency missing: " + relative)
            actual = digest_bytes(canonical_bytes(path_read_bytes(path)))
            if actual != expected_hash:
                raise failure_type("dependency hash changed: " + relative)

    if dict_type(literal_contract).get("maximum_claim") != literal_maximum_claim:
        raise failure_type("maximum claim contract seed changed")
    if dict_type(literal_registry).get("V36_MAXIMUM_CLAIM") != literal_maximum_claim:
        raise failure_type("maximum claim registry seed changed")
    if registry_digest(literal_registry) != literal_registry_digest:
        raise failure_type("registry literal digest changed")

    def compute_base() -> tuple[tuple[str, object], ...]:
        occurrences = (
            (2, 3, fraction_type(1)),
            (3, 2, fraction_type(-1, 2)),
            (2, 4, fraction_type(-1)),
            (4, 2, fraction_type(2, 3)),
            (3, 3, fraction_type(2)),
            (2, 5, fraction_type(1, 3)),
        )
        physical = {
            5: fraction_type(2),
            6: fraction_type(-1),
            7: fraction_type(3),
            8: fraction_type(1, 2),
            9: fraction_type(-2),
            10: fraction_type(1),
            11: fraction_type(-1, 3),
        }
        primes = (5, 7)

        def kernel(h: int) -> Fraction:
            return fraction_type(1, abs_fn(h) + 1)

        def unit_center(q: int, ratio: int) -> Fraction:
            return fraction_type(int_type(ratio % q == 1)) - fraction_type(1, q - 1)

        beta: dict[int, Fraction] = {}
        for d, k, coefficient in occurrences:
            beta[d * k] = beta.get(d * k, fraction_type(0)) + coefficient
        beta_rows = tuple_type((t, str_type(beta[t])) for t in sorted_fn(beta))
        if beta_rows != ((6, "1/2"), (8, "-1/3"), (9, "2"), (10, "1/3")):
            raise failure_type("proper-factor re-collapse fixture changed")

        occurrence_core = fraction_type(0)
        for q in primes:
            for d, k, coefficient in occurrences:
                t = d * k
                for u, physical_value in physical.items():
                    if u == t or (t * u) % q == 0:
                        continue
                    ratio = (u * pow_fn(t, -1, q)) % q
                    occurrence_core += (
                        q
                        * coefficient
                        * physical_value
                        * kernel(u - t)
                        * unit_center(q, ratio)
                    )

        binary_core = fraction_type(0)
        spectral_full = fraction_type(0)
        spectral_diagonal = fraction_type(0)
        character_rows = []
        for q in primes:
            for t, beta_value in beta.items():
                for u, physical_value in physical.items():
                    if (t * u) % q == 0:
                        continue
                    character_sum = q - 2 if u % q == t % q else -1
                    character_rows.append((q, t % q, u % q, character_sum))
                    spectral_full += (
                        fraction_type(q, q - 1)
                        * beta_value
                        * physical_value
                        * kernel(u - t)
                        * character_sum
                    )
                    if u != t:
                        ratio = (u * pow_fn(t, -1, q)) % q
                        binary_core += (
                            q
                            * beta_value
                            * physical_value
                            * kernel(u - t)
                            * unit_center(q, ratio)
                        )
            z_q = sum_fn(
                (
                    beta_value * physical.get(t, fraction_type(0))
                    for t, beta_value in beta.items()
                    if t % q != 0
                ),
                fraction_type(0),
            )
            spectral_diagonal += fraction_type(q * (q - 2), q - 1) * z_q

        character_core = spectral_full - spectral_diagonal
        if not (
            occurrence_core
            == binary_core
            == character_core
            == fraction_type(-2257, 432)
        ):
            raise failure_type("occurrence/binary/character identity changed")
        if len_fn(character_rows) != 39:
            raise failure_type("character orthogonality census changed")

        aligned_left = (2, -1, 3, 1)
        aligned_right = (2, -1, 3, 1)
        dot = sum_fn((a * b for a, b in zip_fn(aligned_left, aligned_right)), 0)
        norm_left_sq = sum_fn((a * a for a in aligned_left), 0)
        norm_right_sq = sum_fn((b * b for b in aligned_right), 0)
        cauchy_saturated = dot * dot == norm_left_sq * norm_right_sq
        if not cauchy_saturated or (dot, norm_left_sq, norm_right_sq) != (15, 15, 15):
            raise failure_type("marginal Cauchy saturation witness changed")

        sample_sigma = fraction_type(1, 9600)
        additive_coefficient = fraction_type(127, 192)
        additive_output = additive_coefficient + 1 + sample_sigma
        additive_delta = fraction_type(1, 192) - sample_sigma
        additive_margin = additive_delta - fraction_type(1, 400)
        if (
            additive_output,
            additive_delta,
            additive_margin,
        ) != (
            fraction_type(319, 192) + sample_sigma,
            fraction_type(49, 9600),
            fraction_type(1, 384),
        ):
            raise failure_type("additive route ledger changed")

        structural_q_gain = fraction_type(31, 32)
        cell_q_gain = fraction_type(1, 32)
        total_q_gain = structural_q_gain + cell_q_gain
        determinant_delta = fraction_type(1, 96)
        determinant_output = fraction_type(191, 96) - fraction_type(1, 3)
        determinant_margin = determinant_delta - fraction_type(1, 400)
        if (
            total_q_gain,
            determinant_output,
            determinant_delta,
            determinant_margin,
        ) != (
            fraction_type(1),
            fraction_type(53, 32),
            fraction_type(1, 96),
            fraction_type(19, 2400),
        ):
            raise failure_type("determinant 31+1 ledger changed")

        required_kappa = fraction_type(1, 3) + fraction_type(1, 400)
        sample_kappa = fraction_type(17, 48)
        character_delta = sample_kappa - fraction_type(1, 3)
        character_margin = character_delta - fraction_type(1, 400)
        marginal_deficit = 2 - (fraction_type(5, 3) - fraction_type(1, 400))
        if (
            required_kappa,
            character_delta,
            character_margin,
            marginal_deficit,
        ) != (
            fraction_type(403, 1200),
            fraction_type(1, 48),
            fraction_type(11, 600),
            fraction_type(403, 1200),
        ):
            raise failure_type("character route ledger changed")

        random_exponent = fraction_type(1, 3) + fraction_type(53, 64)
        random_gap = fraction_type(5, 3) - random_exponent
        random_kappa = 2 - random_exponent
        fixed_q_endpoint_requirement = fraction_type(31, 32) + 3 * fraction_type(1, 400)
        if (
            random_exponent,
            random_gap,
            random_kappa,
            fixed_q_endpoint_requirement,
        ) != (
            fraction_type(223, 192),
            fraction_type(97, 192),
            fraction_type(161, 192),
            fraction_type(781, 800),
        ):
            raise failure_type("heuristic or fixed-q ledger changed")

        or_truth = tuple_type(
            (e, k, x_route, e or k or x_route)
            for e in (False, True)
            for k in (False, True)
            for x_route in (False, True)
        )
        if len_fn(or_truth) != 8 or sum_fn(int_type(row[3]) for row in or_truth) != 7:
            raise failure_type("one-of-three logical compiler changed")

        combined_det_margin = min_fn(
            determinant_margin,
            fraction_type(19, 2400),
            fraction_type(121, 9600),
        )
        if combined_det_margin != fraction_type(19, 2400):
            raise failure_type("combined determinant margin changed")

        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("conditional_bridge_advance", "YES"),
            ("beta_rows", beta_rows),
            ("occurrence_core", str_type(occurrence_core)),
            ("binary_core", str_type(binary_core)),
            ("character_core", str_type(character_core)),
            ("spectral_diagonal", str_type(spectral_diagonal)),
            ("character_rows", len_fn(character_rows)),
            ("cauchy_saturated", cauchy_saturated),
            ("cauchy_dot", dot),
            ("sample_sigma", str_type(sample_sigma)),
            ("additive_coefficient_exponent", str_type(additive_coefficient)),
            ("additive_output_exponent", str_type(additive_output)),
            ("additive_delta", str_type(additive_delta)),
            ("additive_endpoint_margin", str_type(additive_margin)),
            ("structural_q_gain", str_type(structural_q_gain)),
            ("cell_q_gain", str_type(cell_q_gain)),
            ("total_q_gain", str_type(total_q_gain)),
            ("determinant_output_exponent", str_type(determinant_output)),
            ("determinant_delta", str_type(determinant_delta)),
            ("determinant_endpoint_margin", str_type(determinant_margin)),
            ("combined_det_margin", str_type(combined_det_margin)),
            ("required_character_kappa", str_type(required_kappa)),
            ("sample_character_kappa", str_type(sample_kappa)),
            ("sample_character_delta", str_type(character_delta)),
            ("sample_character_margin", str_type(character_margin)),
            ("marginal_large_sieve_deficit", str_type(marginal_deficit)),
            ("random_phase_exponent", str_type(random_exponent)),
            ("random_phase_gap", str_type(random_gap)),
            ("random_phase_kappa", str_type(random_kappa)),
            ("fixed_q_endpoint_requirement", str_type(fixed_q_endpoint_requirement)),
            ("or_truth", or_truth),
            ("selected_route", "K_THEN_E_THEN_X__A_AFTER_B__C_RESERVE"),
            ("arithmetic_advance", False),
            ("fixed_atom_credit", 0),
            ("strict_1_over_400", "UNPAID"),
            ("L2", "NONE"),
            ("TPC_207_TRIGGER", False),
            ("numbered_release", "NO"),
        )

    literal_base = compute_base()

    def mutated(value: object) -> object:
        if exact_bool(value):
            return not value
        if exact_int(value):
            return value + 1
        if exact_str(value):
            return value + "_MUTATED"
        if type_fn(value) is tuple_type:
            return value + ("MUTATED",)
        raise failure_type("unsupported mutation value")

    def wrong_type(value: object) -> object:
        if exact_bool(value):
            return 1 if value else 0
        if exact_int(value):
            return str_type(value)
        if exact_str(value):
            return (value,)
        if type_fn(value) is tuple_type:
            return list_type(value)
        raise failure_type("unsupported mutation type")

    def run() -> dict[str, object]:
        fresh_base = compute_base()
        require_mapping(dict_type(fresh_base), literal_base, "computed result")
        validate_contract(dict_type(literal_contract))
        validate_registry(literal_registry, literal_registry_digest)
        validate_sources(literal_sources)
        validate_dependencies(literal_dependencies)

        mutation_labels: list[str] = []

        def must_reject(label: str, action) -> None:
            try:
                action()
            except failure_type:
                mutation_labels.append(label)
                return
            raise failure_type("mutation accepted: " + label)

        def mapping_mutations(expected: tuple, validator, prefix: str) -> int:
            for index, (key, value) in enumerate_fn(expected):
                changed = dict_type(expected)
                changed[key] = mutated(value)
                must_reject(prefix + "_value_" + str_type(index), lambda c=changed: validator(c))
                rows = list_type(expected)
                rows[index] = (key + "_MUTATED", value)
                must_reject(prefix + "_key_" + str_type(index), lambda c=dict_type(rows): validator(c))
                changed_type = dict_type(expected)
                changed_type[key] = wrong_type(value)
                must_reject(prefix + "_type_" + str_type(index), lambda c=changed_type: validator(c))
            must_reject(prefix + "_outer", lambda: validator(list_type(expected)))

            class StringImpostor(str_type):
                pass

            impostor = dict_type(expected)
            first_key, first_value = expected[0]
            del impostor[first_key]
            impostor[StringImpostor(first_key)] = first_value
            must_reject(prefix + "_key_subclass", lambda: validator(impostor))
            return 3 * len_fn(expected) + 2

        def pair_mutations(expected: tuple, validator, prefix: str, digest_mode: bool) -> int:
            for index, (key, value) in enumerate_fn(expected):
                rows = list_type(expected)
                rows[index] = (key, value + "_MUTATED")
                candidate = tuple_type(rows)
                if digest_mode:
                    must_reject(prefix + "_value_" + str_type(index), lambda c=candidate: validator(c, registry_digest(c)))
                else:
                    must_reject(prefix + "_value_" + str_type(index), lambda c=candidate: validator(c))
                rows = list_type(expected)
                rows[index] = (key + "_MUTATED", value)
                candidate = tuple_type(rows)
                if digest_mode:
                    must_reject(prefix + "_key_" + str_type(index), lambda c=candidate: validator(c, registry_digest(c)))
                else:
                    must_reject(prefix + "_key_" + str_type(index), lambda c=candidate: validator(c))
            if digest_mode:
                must_reject(prefix + "_outer", lambda: validator(list_type(expected), literal_registry_digest))
                must_reject(prefix + "_digest", lambda: validator(expected, "0" * 64))
            else:
                must_reject(prefix + "_outer", lambda: validator(list_type(expected)))

            class StringImpostor(str_type):
                pass

            rows = list_type(expected)
            rows[0] = (StringImpostor(rows[0][0]), rows[0][1])
            if digest_mode:
                must_reject(prefix + "_subclass", lambda: validator(tuple_type(rows), literal_registry_digest))
                return 2 * len_fn(expected) + 3
            must_reject(prefix + "_subclass", lambda: validator(tuple_type(rows)))
            return 2 * len_fn(expected) + 2

        contract_count = 3 * len_fn(literal_contract) + 2
        registry_count = 2 * len_fn(literal_registry) + 3
        source_count = 2 * len_fn(literal_sources) + 2
        dependency_count = 2 * len_fn(literal_dependencies) + 2
        metadata_fields = 11
        result_count = 3 * (len_fn(literal_base) + metadata_fields) + 2
        actions = contract_count + registry_count + source_count + dependency_count + result_count
        full = literal_base + (
            ("contract_fields", len_fn(literal_contract)),
            ("registry_rows", len_fn(literal_registry)),
            ("source_locks", len_fn(literal_sources)),
            ("dependency_locks", len_fn(literal_dependencies)),
            ("registry_sha256", literal_registry_digest),
            ("contract_mutations", contract_count),
            ("registry_mutations", registry_count),
            ("source_mutations", source_count),
            ("dependency_mutations", dependency_count),
            ("result_mutations", result_count),
            ("mutation_actions", actions),
        )
        require_mapping(dict_type(full), full, "full result")

        observed = (
            mapping_mutations(literal_contract, validate_contract, "contract"),
            pair_mutations(literal_registry, validate_registry, "registry", True),
            pair_mutations(literal_sources, validate_sources, "source", False),
            pair_mutations(literal_dependencies, validate_dependencies, "dependency", False),
            mapping_mutations(full, lambda candidate: require_mapping(candidate, full, "full result"), "result"),
        )
        if observed != (
            contract_count,
            registry_count,
            source_count,
            dependency_count,
            result_count,
        ):
            raise failure_type("mutation count formula changed")
        if len_fn(mutation_labels) != actions or len_fn(set_type(mutation_labels)) != actions:
            raise failure_type("mutation ledger changed")
        return dict_type(full)

    return run


def _make_main(
    runner,
    baseline_items,
    frozen_stdout,
    writer=sys.stdout.write,
    tuple_type=tuple,
    str_type=str,
    type_fn=type,
    len_fn=len,
    failure_type=CheckFailure,
):
    literal_baseline = tuple_type(baseline_items)
    literal_stdout = frozen_stdout

    def sealed(*argv_objects) -> int:
        if len_fn(argv_objects) != 1:
            raise failure_type("explicit --check is required")
        argv = argv_objects[0]
        if type_fn(argv) is not tuple_type:
            raise failure_type("explicit --check is required")
        if len_fn(argv) != 1 or type_fn(argv[0]) is not str_type or argv != ("--check",):
            raise failure_type("explicit --check is required")
        result = runner()
        if tuple_type(result.items()) != literal_baseline:
            raise failure_type("sealed result changed")
        writer(literal_stdout + "\n")
        return 0

    return sealed


_TRUSTED_RUN = _make_trusted_runner()
run_check = _TRUSTED_RUN
_BASELINE_RESULT = _TRUSTED_RUN()
_FROZEN_STDOUT = json.dumps(_BASELINE_RESULT, sort_keys=True, separators=(",", ":"))
main = _make_main(_TRUSTED_RUN, tuple(_BASELINE_RESULT.items()), _FROZEN_STDOUT)
del _BASELINE_RESULT


if __name__ == "__main__":
    try:
        raise SystemExit(main(tuple(sys.argv[1:])))
    except CheckFailure as exc:
        sys.stderr.write("CheckFailure: " + str(exc) + "\n")
        raise SystemExit(1)
