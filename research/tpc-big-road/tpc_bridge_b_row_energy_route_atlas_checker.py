#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V40 q-row energy route atlas."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_CONSTANT_RESIDUE_COMPRESSION_DIAGONAL_PACKET_PAYMENT_AND_ROW_"
    "BESSEL_THRESHOLD_SELECT_Q_ROW_ENERGY_AS_WEAKER_PRIMARY_BRIDGE"
)


SELECTED_ROUTE = (
    "R2_Q_ROW_ENERGY_FIRST__RB_RESTRICTED_ROW_BESSEL_IMPLEMENTATION__SHIFT_"
    "AND_CHARACTER_NORMAL_FORMS_SECOND__P2_PACKET_ENERGY_K_SCHATTEN_E_"
    "RESIDUAL_X_CHARACTER_RESERVES__A_TERMINAL__C_RESERVE"
)


CONTRACT_ITEMS = (
    ("schema_version", "V40_Q_ROW_ENERGY_ROUTE_ATLAS_V1"),
    ("artifact_name", "bridge_b_row_energy_and_packet_route_atlas.md"),
    ("baseline_commit", "d6566e42ef1f5717de4dea5e80a0d4293fb3c712"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("route_position", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_CONSTANT_RESIDUE_DIRECTION_SELECTED_ROW_BESSEL_PIER_OPEN"),
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
    ("row_scalar", "s_q=sum_r d_q(r)"),
    ("row_energy", "sum_q|s_q|^2"),
    ("direct_row_factor", "Q^(3/2)"),
    ("row_gate_exponent", "7/3-kappa"),
    ("kappa_threshold", "1/200"),
    ("row_diagonal_exponent", "95/48"),
    ("row_bessel_tau_threshold", "419/1200"),
    ("sample_tau", "1/3"),
    ("sample_row_energy", "37/16"),
    ("sample_kappa", "1/48"),
    ("sample_output", "53/32"),
    ("sample_margin", "19/2400"),
    ("unit_deletion_energy", "37/16"),
    ("shift_support_gap", "1/96"),
    ("shift_sigma_threshold", "13/4800"),
    ("selected_route", SELECTED_ROUTE),
    ("source_boundary", "NO_LITERAL_Q_ROW_ENERGY_OR_RESTRICTED_ROW_BESSEL_THEOREM"),
    ("fixture_q", 5),
    ("fixture_row_sum", 7),
    ("fixture_packet_energy", 39),
    ("fixture_alternating_row", 0),
    ("fixture_alternating_packet", 4),
    ("fixture_negative_offdiagonal", -18),
    ("first_fatal", "NO_LITERAL_THEOREM_BOUNDS_SUM_Q_ABS_SUM_T_BETA_T_G_Q_T_SQUARED_AT_X_POWER_7_OVER_3_MINUS_KAPPA_FOR_KAPPA_GREATER_THAN_1_OVER_200"),
)


REGISTRY_ITEMS = (
    ("V40_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V40_ROUTE_ADVANCE", "YES"),
    ("V40_CONDITIONAL_BRIDGE_ADVANCE", "YES"),
    ("V40_ARITHMETIC_ADVANCE", "NO"),
    ("V40_FIXED_ATOM_CREDIT", "0"),
    ("V40_STRICT_1_OVER_400", "UNPAID"),
    ("V40_L2", "NONE"),
    ("V40_TPC_207_TRIGGER", "false"),
    ("V40_NUMBERED_RELEASE", "NO"),
    ("V40_DERIVATION_STATUS", "COHERENT_AFTER_CONSTANT_RESIDUE_COMPRESSION_COLLISION_EXPANSION_DIAGONAL_PAYMENT_AND_THREE_NORMAL_FORMS"),
    ("V40_ASSUMPTION_POLICY", "ROW_ENERGY_ROW_BESSEL_FULL_SHIFT_AND_JOINT_CHARACTER_BOUNDS_REMAIN_EXPLICIT_OPEN_THEOREMS"),
    ("V40_SELECTED_RESEARCH_ROUTE", SELECTED_ROUTE),
    ("V40_V39_PACKET_SCALAR", "RETAINED_EXACT_ZERO_REMAINDER"),
    ("V40_CONSTANT_RESIDUE_ROW_SCALAR", "S_Q_EQUALS_SUM_R_D_Q_R"),
    ("V40_ROW_ENERGY", "SUM_Q_ABS_S_Q_SQUARED"),
    ("V40_DIRECT_ROW_ENERGY_CAUCHY", "PROVED_Q_POWER_3_OVER_2_TIMES_ROW_ENERGY_SQUARE_ROOT"),
    ("V40_ROW_ENERGY_GATE", "OPEN_CONJECTURE_X_POWER_7_OVER_3_MINUS_KAPPA"),
    ("V40_ROW_ENERGY_KAPPA_THRESHOLD", "KAPPA_STRICTLY_GREATER_THAN_1_OVER_200"),
    ("V40_ROW_ENERGY_CONDITIONAL_OUTPUT", "X_POWER_5_OVER_3_MINUS_KAPPA_OVER_2"),
    ("V40_ROW_ENERGY_ENDPOINT_MARGIN", "KAPPA_OVER_2_MINUS_1_OVER_400"),
    ("V40_PACKET_ENERGY_IMPLIES_ROW_ENERGY", "PROVED_CAUCHY_WITH_ONE_Q_FACTOR"),
    ("V40_ROW_ENERGY_IMPLIES_PACKET_ENERGY", "STOP_SCOPED_Q5_ALTERNATING_TRANSVERSE_PACKET"),
    ("V40_V39_PACKET_P2_STATUS", "RETAINED_STRONGER_RESERVE_NOT_PRIMARY_NORM"),
    ("V40_PHYSICAL_ROW_COEFFICIENT", "A_Q_T_EQUALS_BETA_T_TIMES_G_Q_T"),
    ("V40_ROW_COLLISION_IDENTITY", "PROVED_EXACT_DIAGONAL_PLUS_SIGNED_OFFDIAGONAL"),
    ("V40_ROW_OFFDIAGONAL_POSITIVITY", "STOP_SCOPED_SIGN_INDEFINITE_FINITE_FIXTURE"),
    ("V40_CENTERED_PACKET_POINTWISE_ENVELOPE", "PROVED_H_OVER_Q_TIMES_X_O1"),
    ("V40_ROW_DIAGONAL_PAYMENT", "PROVED_X_POWER_95_OVER_48"),
    ("V40_RESTRICTED_ROW_BESSEL_GATE", "OPEN_CONJECTURE_E_ROW_LE_X_POWER_TAU_TIMES_D_ROW"),
    ("V40_RESTRICTED_ROW_BESSEL_TAU_THRESHOLD", "TAU_STRICTLY_LESS_THAN_419_OVER_1200"),
    ("V40_SAMPLE_ROW_BESSEL_TAU", "1_OVER_3"),
    ("V40_SAMPLE_ROW_ENERGY", "X_POWER_37_OVER_16"),
    ("V40_SAMPLE_ROW_KAPPA", "1_OVER_48"),
    ("V40_SAMPLE_ROW_OUTPUT", "X_POWER_53_OVER_32"),
    ("V40_SAMPLE_ROW_ENDPOINT_MARGIN", "19_OVER_2400"),
    ("V40_UNIT_FREE_SHIFT_ROW", "PROVED_EXACT_CENTERED_DIVISIBILITY_MULTIPLIER"),
    ("V40_UNIT_DELETION_POINTWISE", "PROVED_X_POWER_1_TIMES_H_OVER_Q_SQUARED"),
    ("V40_UNIT_DELETION_ENERGY", "PROVED_X_POWER_37_OVER_16"),
    ("V40_EFFECTIVE_SHIFT_BELOW_Q_SQUARED", "PROVED_SCHWARTZ_WITH_EXPONENT_GAP_1_OVER_96"),
    ("V40_UNIQUE_PRIME_DIVISOR_SUPPORT", "PROVED_FOR_NONZERO_ABS_H_STRICTLY_BELOW_Q_SQUARED"),
    ("V40_SHIFT_ENERGY_COMPILER", "PROVED_H_OVER_Q_TIMES_FULL_SHIFT_WEIGHTED_ENERGY_PLUS_UNIT_PAYMENT"),
    ("V40_FULL_SHIFT_ENERGY_GATE", "OPEN_STRONGER_CONJECTURE_X_POWER_2_PLUS_2_SIGMA"),
    ("V40_FULL_SHIFT_SIGMA_THRESHOLD", "SIGMA_STRICTLY_LESS_THAN_13_OVER_4800"),
    ("V40_V36_RESIDUAL_TO_FULL_SHIFT_ATTACHMENT", "STOP_SCOPED_LOCAL_CARRIER_ROWWISE_REASSEMBLY_UNPAID"),
    ("V40_JOINT_CHARACTER_ROW_IDENTITY", "PROVED_EXACT_CENTERED_BW_MINUS_Z"),
    ("V40_JOINT_CHARACTER_FOURTH_MOMENT", "OPEN_STRONGER_THEOREM_INTERFACE"),
    ("V40_SEPARATE_MARGINAL_CHARACTER_LARGE_SIEVE", "STOP_SCOPED_DOES_NOT_CONTROL_SAME_INDEX_PRODUCT_COVARIANCE"),
    ("V40_HARPER_GENERAL_BDH_DIRECT_ATTACHMENT", "STOP_SCOPED_FIXED_SEQUENCE_LARGE_MODULUS_AND_DISTRIBUTION_HYPOTHESES_MISMATCH"),
    ("V40_ZHENG_SIMULTANEOUS_AP_DIRECT_ATTACHMENT", "STOP_SCOPED_SOURCE_ARRAYS_MODULUS_RANGE_AND_LITERAL_ROW_MISMATCH"),
    ("V40_PASCADI_SMOOTH_AP_DIRECT_ATTACHMENT", "STOP_SCOPED_SMOOTH_TRIPLE_CONVOLUTION_NOT_ORDERED_MASTER_HYBRID_ROW"),
    ("V40_BFKMM_SHIFTED_CONVOLUTION_DIRECT_ATTACHMENT", "STOP_SCOPED_AUTOMORPHIC_COEFFICIENT_AND_SHIFT_FAMILY_MISMATCH"),
    ("V40_BLOMER_PASCADI_DIRECT_ATTACHMENT", "STOP_SCOPED_POST_EMITTER_SEPARABLE_FIXED_MODULUS_ENGINE_NOT_ROW_ENERGY"),
    ("V40_DIRECT_PRIMARY_SOURCE_FOR_ROW_GATE", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09"),
    ("V40_FIRST_FATAL", "NO_LITERAL_THEOREM_BOUNDS_SUM_Q_ABS_SUM_T_BETA_T_G_Q_T_SQUARED_AT_X_POWER_7_OVER_3_MINUS_KAPPA_FOR_KAPPA_GREATER_THAN_1_OVER_200"),
    ("V40_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_CONSTANT_RESIDUE_DIRECTION_SELECTED_ROW_BESSEL_PIER_OPEN"),
    ("V40_SOURCE_LOCK_POLICY", "PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED"),
    ("V40_ROUTE_MAP_REFERENCE", "TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B"),
)


EXPECTED_REGISTRY_SHA256 = "e16a6a7108795ed1cd02927eaf6f509dc35932bc9a7cb2fbaa96f5c14e3f292e"


SOURCE_ITEMS = (
    ("HARPER_GENERAL_BDH", "arXiv:2412.19644v1_Theorems_1_2"),
    ("ZHENG_SIMULTANEOUS_AP", "arXiv:2512.22798v1_Theorems_1.1_1.2"),
    ("PASCADI_SMOOTH_AP", "arXiv:2304.11696v3_Main_Theorem"),
    ("BFKMM_TWISTED_L_MOMENTS", "arXiv:1411.4467v3_Shifted_Convolution_and_Bilinear_Kloosterman_Architecture"),
    ("BLOMER_PASCADI_OPERATOR_CELL", "arXiv:2607.24311v1_Theorem_1.1"),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_schatten_duality_and_packet_energy_pivot.md",
        "eac9c6975d23e8d2ba35d8884a0fc8b75ab6e73022d29cdcde18e38f4dbfa280",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_schatten_packet_energy_checker.py",
        "cb943b1fc6d3b411ea7748f39f8495dcf446a35b95b9ed28a8515b18877cfa62",
    ),
    (
        "research/tpc-big-road/bridge_b_loss_budgeted_shift_packet_compiler.md",
        "07226c6af1c8145982f5cb71fbfe3159cb11f27e6ecd7eba4014431a0d024545",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_loss_budgeted_shift_packet_checker.py",
        "cc0427402fa7f4df85bffb927e06ed5bdf3a9cc14a19bdf76dd832b87cfd4ee4",
    ),
    (
        "research/tpc-big-road/bridge_b_multiroute_ratio_core_atlas.md",
        "97c725b3fd086825125aa5d9ea302bdb874243bddc2708e5603a1c1d591b0a98",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_multiroute_ratio_core_checker.py",
        "b4f383bccd05194af28665b9a6b98fe98756d89a12d37609ef65fbd92869f8ce",
    ),
)


def _make_trusted_runner(
    maximum_claim_seed=MAXIMUM_CLAIM,
    selected_route_seed=SELECTED_ROUTE,
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
    all_fn=all,
    enumerate_fn=enumerate,
):
    literal_maximum_claim = maximum_claim_seed
    literal_selected_route = selected_route_seed
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
            (key + "=" + value + "\n").encode("utf-8")
            for key, value in candidate
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

    contract_map = dict_type(literal_contract)
    registry_map = dict_type(literal_registry)
    if contract_map.get("maximum_claim") != literal_maximum_claim:
        raise failure_type("maximum claim contract seed changed")
    if registry_map.get("V40_MAXIMUM_CLAIM") != literal_maximum_claim:
        raise failure_type("maximum claim registry seed changed")
    if contract_map.get("selected_route") != literal_selected_route:
        raise failure_type("selected route contract seed changed")
    if registry_map.get("V40_SELECTED_RESEARCH_ROUTE") != literal_selected_route:
        raise failure_type("selected route registry seed changed")
    if registry_digest(literal_registry) != literal_registry_digest:
        raise failure_type("registry literal digest changed")

    def compute_base() -> tuple[tuple[str, object], ...]:
        q = 5
        d = (3, -2, 5, 1)
        row_sum = sum_fn(d, 0)
        packet_energy = sum_fn((value * value for value in d), 0)
        row_energy = row_sum * row_sum
        packet_cauchy_rhs = (q - 1) * packet_energy
        if (row_sum, packet_energy, row_energy, packet_cauchy_rhs) != (7, 39, 49, 156):
            raise failure_type("row versus packet fixture changed")
        if row_energy > packet_cauchy_rhs:
            raise failure_type("packet-to-row Cauchy changed")

        alternating = (1, -1, 1, -1)
        alternating_row = sum_fn(alternating, 0)
        alternating_packet = sum_fn((value * value for value in alternating), 0)
        if (alternating_row, alternating_packet) != (0, 4):
            raise failure_type("transverse packet fixture changed")

        positive = (2, -1, 3)
        positive_sum = sum_fn(positive, 0)
        positive_energy = positive_sum * positive_sum
        positive_diagonal = sum_fn((value * value for value in positive), 0)
        positive_offdiagonal = positive_energy - positive_diagonal
        if (positive_sum, positive_energy, positive_diagonal, positive_offdiagonal) != (4, 16, 14, 2):
            raise failure_type("positive collision fixture changed")

        negative = (1, -2, 4, -1)
        negative_sum = sum_fn(negative, 0)
        negative_energy = negative_sum * negative_sum
        negative_diagonal = sum_fn((value * value for value in negative), 0)
        negative_offdiagonal = negative_energy - negative_diagonal
        if (negative_sum, negative_energy, negative_diagonal, negative_offdiagonal) != (2, 4, 22, -18):
            raise failure_type("negative collision fixture changed")

        endpoint = fraction_type(1997, 1200)
        row_gate = fraction_type(7, 3)
        kappa_threshold = fraction_type(1, 200)
        diagonal_exponent = fraction_type(95, 48)
        tau_threshold = row_gate - kappa_threshold - diagonal_exponent
        sample_tau = fraction_type(1, 3)
        sample_energy = diagonal_exponent + sample_tau
        sample_kappa = row_gate - sample_energy
        sample_output = fraction_type(1, 2) + sample_energy / 2
        sample_margin = endpoint - sample_output
        unit_deletion = fraction_type(2) + 2 * fraction_type(21, 32) - 3 * fraction_type(1, 3)
        shift_gap = 2 * fraction_type(1, 3) - fraction_type(21, 32)
        shift_base = fraction_type(2) + fraction_type(21, 32) - fraction_type(1, 3)
        shift_output = fraction_type(1, 2) + shift_base / 2
        shift_sigma_threshold = endpoint - shift_output
        if (
            tau_threshold,
            sample_energy,
            sample_kappa,
            sample_output,
            sample_margin,
            unit_deletion,
            shift_gap,
            shift_base,
            shift_output,
            shift_sigma_threshold,
        ) != (
            fraction_type(419, 1200),
            fraction_type(37, 16),
            fraction_type(1, 48),
            fraction_type(53, 32),
            fraction_type(19, 2400),
            fraction_type(37, 16),
            fraction_type(1, 96),
            fraction_type(223, 96),
            fraction_type(319, 192),
            fraction_type(13, 4800),
        ):
            raise failure_type("row endpoint ledger changed")
        if not (sample_tau < tau_threshold and sample_kappa > kappa_threshold):
            raise failure_type("strict row endpoint changed")

        toy_primes = (5, 7)
        unique_divisor = all_fn(
            sum_fn((int_type(h % prime == 0) for prime in toy_primes), 0) <= 1
            for h in range_fn(1, 35)
        )
        boundary_divisors = sum_fn((int_type(35 % prime == 0) for prime in toy_primes), 0)
        if (unique_divisor, boundary_divisors) != (True, 2):
            raise failure_type("unique prime divisor fixture changed")

        route_truth = tuple_type(
            (emitter, row_gate_ok, terminal, emitter and row_gate_ok and terminal)
            for emitter in (False, True)
            for row_gate_ok in (False, True)
            for terminal in (False, True)
        )
        if sum_fn((int_type(row[-1]) for row in route_truth), 0) != 1:
            raise failure_type("conditional route logic changed")

        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("conditional_bridge_advance", "YES"),
            ("fixture_q", q),
            ("fixture_d", d),
            ("row_sum", row_sum),
            ("packet_energy", packet_energy),
            ("row_energy", row_energy),
            ("packet_cauchy_rhs", packet_cauchy_rhs),
            ("alternating_d", alternating),
            ("alternating_row", alternating_row),
            ("alternating_packet", alternating_packet),
            ("positive_collision", positive),
            ("positive_energy", positive_energy),
            ("positive_diagonal", positive_diagonal),
            ("positive_offdiagonal", positive_offdiagonal),
            ("negative_collision", negative),
            ("negative_energy", negative_energy),
            ("negative_diagonal", negative_diagonal),
            ("negative_offdiagonal", negative_offdiagonal),
            ("row_gate_exponent", str_type(row_gate)),
            ("kappa_threshold", str_type(kappa_threshold)),
            ("diagonal_exponent", str_type(diagonal_exponent)),
            ("tau_threshold", str_type(tau_threshold)),
            ("sample_tau", str_type(sample_tau)),
            ("sample_energy", str_type(sample_energy)),
            ("sample_kappa", str_type(sample_kappa)),
            ("sample_output", str_type(sample_output)),
            ("sample_margin", str_type(sample_margin)),
            ("unit_deletion_exponent", str_type(unit_deletion)),
            ("shift_support_gap", str_type(shift_gap)),
            ("shift_base_exponent", str_type(shift_base)),
            ("shift_output", str_type(shift_output)),
            ("shift_sigma_threshold", str_type(shift_sigma_threshold)),
            ("unique_divisor_below_boundary", unique_divisor),
            ("boundary_divisors_at_35", boundary_divisors),
            ("route_truth", route_truth),
            ("selected_route", literal_selected_route),
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
del _make_trusted_runner
run_check = _TRUSTED_RUN
_BASELINE_RESULT = _TRUSTED_RUN()
_FROZEN_STDOUT = json.dumps(_BASELINE_RESULT, sort_keys=True, separators=(",", ":"))
main = _make_main(_TRUSTED_RUN, tuple(_BASELINE_RESULT.items()), _FROZEN_STDOUT)
del _make_main
del _BASELINE_RESULT


if __name__ == "__main__":
    try:
        raise SystemExit(main(tuple(sys.argv[1:])))
    except CheckFailure as exc:
        sys.stderr.write("CheckFailure: " + str(exc) + "\n")
        raise SystemExit(1)
