#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V37 shift-packet compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_CENTERED_RESIDUE_PACKETIZATION_PLUS_LOSS_BUDGETED_K_ROUTE_"
    "THRESHOLD_AND_SOURCE_BACKED_CELL_ENGINE_AFTER_CONJECTURAL_EMISSION"
)


CONTRACT_ITEMS = (
    ("schema_version", "V37_LOSS_BUDGETED_SHIFT_PACKET_V1"),
    ("artifact_name", "bridge_b_loss_budgeted_shift_packet_compiler.md"),
    ("baseline_commit", "2b199a9989f378666e5bc7b9bb8f2952015f75de"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("route_position", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_K_LANE_LOSS_BUDGETED_PIER_MARKED"),
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
    ("shift_occupancy", "Q^(31/32)"),
    ("raw_triangle", "x^(191/96+o(1))"),
    ("packet_pre_cell_budget", "x^(5/3+o(1))*Q^omega"),
    ("packet_overhead", "omega<19/800"),
    ("bp_cell_gain", "Q^(-1/32)"),
    ("conditional_output", "x^(53/32+omega/3+o(1))"),
    ("general_gain_condition", "rho+gamma>781/800"),
    ("with_bp_rho_condition", "rho>189/200"),
    ("ell_cauchy_status", "STOP_SCOPED_X^(349/192)_DEFICIT_737/4800"),
    ("fixture_q", 5),
    ("fixture_t", 2),
    ("fixture_packet", "95/4"),
    ("first_fatal", "NO_LITERAL_THEOREM_PROVES_THE_BP_ADMISSIBLE_PACKET_EMITTER_AND_AGGREGATE_NORM_WITH_OMEGA_LT_19_OVER_800"),
)


REGISTRY_ITEMS = (
    ("V37_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V37_ROUTE_ADVANCE", "YES"),
    ("V37_CONDITIONAL_BRIDGE_ADVANCE", "YES"),
    ("V37_ARITHMETIC_ADVANCE", "NO"),
    ("V37_FIXED_ATOM_CREDIT", "0"),
    ("V37_STRICT_1_OVER_400", "UNPAID"),
    ("V37_L2", "NONE"),
    ("V37_TPC_207_TRIGGER", "false"),
    ("V37_NUMBERED_RELEASE", "NO"),
    ("V37_DERIVATION_STATUS", "COHERENT_AFTER_EXACT_PACKETIZATION_AND_LOSS_BUDGETING"),
    ("V37_ASSUMPTION_POLICY", "PACKET_EMITTER_IS_EXPLICIT_CONJECTURE_AND_NEVER_PROMOTED_TO_THEOREM"),
    ("V37_SELECTED_RESEARCH_ROUTE", "K_LOSS_BUDGETED_PACKET_EMITTER_FIRST__E_SECOND__X_THIRD__A_TERMINAL_AFTER_B__C_RESERVE"),
    ("V37_V36_BINARY_CORE", "RETAINED_EXACT_OFF_DIAGONAL_COPRIME_RATIO_COVARIANCE"),
    ("V37_CENTERED_RESIDUE_PACKET", "PROVED_EXACT_BINARY_CORE_PACKET_IDENTITY"),
    ("V37_UNIT_TO_DIFFERENCE_BIJECTION", "PROVED_EXACT_A_TO_B_EQUALS_A_MINUS_ONE_TIMES_T"),
    ("V37_PACKET_DIAGONAL", "PROVED_EXACT_ONLY_B_ZERO_ELL_ZERO_ROW_DELETED"),
    ("V37_PACKET_BACKGROUND", "PROVED_EXACT_ALL_B_NOT_EQUAL_MINUS_T_REQUIRED"),
    ("V37_CONSTANT_PACKET", "PROVED_EXACT_ANNIHILATED"),
    ("V37_SCHWARTZ_TAIL", "PROVED_NEGLIGIBLE_AFTER_H_X_EPSILON_TRUNCATION"),
    ("V37_SHIFT_OCCUPANCY", "Q_POWER_31_OVER_32"),
    ("V37_RAW_POSITIVE_COMPENSATING_TRIANGLE", "X_POWER_191_OVER_96"),
    ("V37_PACKET_EMITTER_STATUS", "OPEN_CONJECTURE_BP_ADMISSIBLE_EXACTLY_ONCE_JOINT_PACKET"),
    ("V37_PACKET_EXACTLY_ONCE_POLICY", "PHYSICAL_BETA_W_K_PRIME_SHELL_ZERO_DELETION_AND_ALL_TEMPLATE_LABELS_PRESERVED"),
    ("V37_PACKET_PRE_CELL_BUDGET", "X_POWER_5_OVER_3_TIMES_Q_POWER_OMEGA"),
    ("V37_PACKET_EFFECTIVE_GAIN", "Q_POWER_MINUS_31_OVER_32_PLUS_OMEGA"),
    ("V37_PACKET_OVERHEAD_THRESHOLD", "OMEGA_STRICTLY_LESS_THAN_19_OVER_800"),
    ("V37_BLOMER_PASCADI_CELL_ENGINE", "SOURCE_BACKED_Q_POWER_MINUS_1_OVER_32_AT_CRITICAL_SQUARE_ROOT_RANGE"),
    ("V37_CONDITIONAL_OUTPUT", "X_POWER_53_OVER_32_PLUS_OMEGA_OVER_3"),
    ("V37_CONDITIONAL_DELTA", "1_OVER_96_MINUS_OMEGA_OVER_3"),
    ("V37_CONDITIONAL_ENDPOINT_MARGIN", "19_OVER_2400_MINUS_OMEGA_OVER_3"),
    ("V37_GENERAL_GAIN_CONDITION", "RHO_PLUS_GAMMA_STRICTLY_GREATER_THAN_781_OVER_800"),
    ("V37_WITH_BP_RHO_THRESHOLD", "RHO_STRICTLY_GREATER_THAN_189_OVER_200"),
    ("V37_V36_ZERO_LOSS_COMPILER", "SUFFICIENT_SPECIAL_CASE_OMEGA_ZERO_NOT_NECESSARY"),
    ("V37_ELL_CAUCHY", "STOP_SCOPED_EFFECTIVE_RHO_31_OVER_64_INSUFFICIENT"),
    ("V37_ELL_CAUCHY_OUTPUT", "X_POWER_349_OVER_192"),
    ("V37_ELL_CAUCHY_ENDPOINT_DEFICIT", "737_OVER_4800"),
    ("V37_PACKET_COMPILER_NOT_RANDOM_CANCELLATION", "PROVED_STATUS_FIREWALL"),
    ("V37_GLOBAL_RANDOM_PHASE_BENCHMARK", "RETAINED_HEURISTIC_ONLY_X_POWER_223_OVER_192"),
    ("V37_BLOMER_PASCADI_DIRECT_ATTACHMENT", "STOP_SCOPED_REQUIRES_PRIOR_PHYSICAL_PACKET_EMISSION_AND_AGGREGATE_NORM"),
    ("V37_PASCADI_FREQUENCY_CONCENTRATION_DIRECT_ATTACHMENT", "STOP_SCOPED_ASSUMPTION14_AND_SMOOTH_LEVEL_SEQUENCE_NOT_VERIFIED_FOR_LITERAL_PACKET"),
    ("V37_WRIGHT_PARTIALLY_FIXED_MODULUS_DIRECT_ATTACHMENT", "STOP_SCOPED_WRONG_DISPERSION_ARRAYS_AND_NO_CENTERED_PACKET_REASSEMBLY"),
    ("V37_BETTIN_CHANDEE_DIRECT_ATTACHMENT", "STOP_SCOPED_LOCAL_TRILINEAR_FRACTION_NO_PRIME_SHELL_PACKET_NORM"),
    ("V37_BLOMER_RISAGER_SHPARLINSKI_DIRECT_ATTACHMENT", "STOP_SCOPED_SPECIFIED_TRIPLE_MODULAR_INVERSE_FAMILY_WRONG_PHYSICAL_COEFFICIENTS"),
    ("V37_DIRECT_PRIMARY_SOURCE_ATTACHMENT", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09"),
    ("V37_ROUTE_E", "RETAINED_OPEN_WHOLE_RESIDUAL_SIGMA_LT_13_OVER_4800"),
    ("V37_ROUTE_X", "RETAINED_OPEN_JOINT_CHARACTER_KAPPA_GT_403_OVER_1200"),
    ("V37_TERMINAL_A", "OPEN_TERMINAL_EQUIVALENT_SIGNED_QLOCAL_COVARIANCE_AFTER_B"),
    ("V37_DYNAMICS_C", "RESERVE_DISTINGUISHED_SEED_ATTACHMENT_STILL_OPEN"),
    ("V37_NEXT_THEOREM", "EXACTLY_ONCE_BP_ADMISSIBLE_CENTERED_SHIFT_PACKET_EMITTER_WITH_AGGREGATE_OVERHEAD_OMEGA_LT_19_OVER_800"),
    ("V37_FIRST_FATAL", "NO_LITERAL_THEOREM_PROVES_THE_BP_ADMISSIBLE_PACKET_EMITTER_AND_AGGREGATE_NORM_WITH_OMEGA_LT_19_OVER_800"),
    ("V37_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_K_LANE_LOSS_BUDGETED_PIER_MARKED"),
    ("V37_SOURCE_LOCK_POLICY", "PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED"),
    ("V37_ROUTE_MAP_REFERENCE", "TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B"),
)


EXPECTED_REGISTRY_SHA256 = "bf34e1ac32ba6553d653cd78cec39c65ecd67db06ab2dd000424f8ade7b11c4c"


SOURCE_ITEMS = (
    ("BLOMER_PASCADI_CRITICAL_CELL", "arXiv:2607.24311v1_Theorem_1.1_Theorem_5.5"),
    ("PASCADI_FREQUENCY_CONCENTRATION", "arXiv:2404.04239v3_Theorem_13_Assumption_14_Corollaries_17_18"),
    ("WRIGHT_PARTIALLY_FIXED_FRACTION", "arXiv:2604.25177v1_Theorem_2.1"),
    ("BETTIN_CHANDEE_TRILINEAR_FRACTION", "arXiv:1502.00769v1_Theorem_1"),
    ("BLOMER_RISAGER_SHPARLINSKI_TRIPLE_SUM", "arXiv:2411.17823v3_Theorem_1.1"),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_multiroute_ratio_core_atlas.md",
        "97c725b3fd086825125aa5d9ea302bdb874243bddc2708e5603a1c1d591b0a98",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_multiroute_ratio_core_checker.py",
        "b4f383bccd05194af28665b9a6b98fe98756d89a12d37609ef65fbd92869f8ce",
    ),
    (
        "research/tpc-big-road/bridge_b_proper_factor_unit_ratio_reduction.md",
        "705b0dfd4d94d70bad798ca6cccf7e0f37f049683d30373ea895d97a6db93da1",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_proper_factor_unit_ratio_checker.py",
        "8c5e3dcc03b6ac132baae8a0c0c1949fddc24a6f114fd61de416cf4a7b02bd51",
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
    if dict_type(literal_registry).get("V37_MAXIMUM_CLAIM") != literal_maximum_claim:
        raise failure_type("maximum claim registry seed changed")
    if registry_digest(literal_registry) != literal_registry_digest:
        raise failure_type("registry literal digest changed")

    def compute_base() -> tuple[tuple[str, object], ...]:
        q = 5
        t = 2
        inverse_t = pow_fn(t, -1, q)
        rows = (
            (0, 7, fraction_type(7)),
            (1, 3, fraction_type(-2)),
            (2, 4, fraction_type(3)),
            (4, 1, fraction_type(1)),
        )
        allowed_b = tuple_type(sorted_fn(b for b in range_fn(q) if b != (-t) % q))
        unit_to_b = tuple_type(((a - 1) * t) % q for a in range_fn(1, q))
        if allowed_b != (0, 1, 2, 4) or tuple_type(sorted_fn(unit_to_b)) != allowed_b:
            raise failure_type("unit-to-difference bijection changed")

        packet = dict_type((b, weight) for b, _u, weight in rows)
        packet_total = sum_fn(packet.values(), fraction_type(0))
        packet_mean = packet_total / (q - 1)
        centered_packet = q * (packet[0] - packet_mean)
        positive_branch = q * packet[0]
        compensating_background = fraction_type(q, q - 1) * packet_total
        if (
            packet_total,
            packet_mean,
            centered_packet,
            positive_branch,
            compensating_background,
        ) != (
            fraction_type(9),
            fraction_type(9, 4),
            fraction_type(95, 4),
            fraction_type(35),
            fraction_type(45, 4),
        ):
            raise failure_type("centered packet fixture changed")

        direct_ratio = fraction_type(0)
        for b, u, weight in rows:
            if u == t or u % q == 0 or (u - t) % q != b:
                raise failure_type("physical packet row changed")
            ratio = (u * inverse_t) % q
            u1 = fraction_type(int_type(ratio == 1)) - fraction_type(1, q - 1)
            direct_ratio += q * weight * u1
        if direct_ratio != centered_packet:
            raise failure_type("direct ratio/packet identity changed")

        constant_value = fraction_type(37)
        constant_packet = q * (
            constant_value
            - sum_fn((constant_value for _ in allowed_b), fraction_type(0)) / (q - 1)
        )
        if constant_packet != 0:
            raise failure_type("constant packet annihilation changed")

        raw_exponent = fraction_type(191, 96)
        occupancy_x = fraction_type(31, 96)
        occupancy_q = fraction_type(31, 32)
        ideal_pre_cell = raw_exponent - occupancy_x
        bp_gamma = fraction_type(1, 32)
        endpoint = fraction_type(5, 3) - fraction_type(1, 400)
        total_gain_threshold = 3 * (raw_exponent - endpoint)
        rho_threshold = total_gain_threshold - bp_gamma
        omega_ceiling = occupancy_q - rho_threshold
        if (
            occupancy_x,
            occupancy_q,
            ideal_pre_cell,
            total_gain_threshold,
            rho_threshold,
            omega_ceiling,
        ) != (
            fraction_type(31, 96),
            fraction_type(31, 32),
            fraction_type(5, 3),
            fraction_type(781, 800),
            fraction_type(189, 200),
            fraction_type(19, 800),
        ):
            raise failure_type("packet threshold ledger changed")

        ideal_output = raw_exponent - (occupancy_q + bp_gamma) / 3
        ideal_margin = endpoint - ideal_output
        sample_omega = fraction_type(1, 100)
        sample_output = ideal_output + sample_omega / 3
        sample_margin = endpoint - sample_output
        equality_margin = endpoint - (ideal_output + omega_ceiling / 3)
        if (
            ideal_output,
            ideal_margin,
            sample_output,
            sample_margin,
            equality_margin,
        ) != (
            fraction_type(53, 32),
            fraction_type(19, 2400),
            fraction_type(3983, 2400),
            fraction_type(11, 2400),
            fraction_type(0),
        ):
            raise failure_type("strict overhead ledger changed")

        ell_cauchy_rho = occupancy_q / 2
        ell_cauchy_total_gain = ell_cauchy_rho + bp_gamma
        ell_cauchy_output = raw_exponent - ell_cauchy_total_gain / 3
        ell_cauchy_deficit = ell_cauchy_output - endpoint
        gain_deficit_q = total_gain_threshold - ell_cauchy_total_gain
        if (
            ell_cauchy_rho,
            ell_cauchy_total_gain,
            ell_cauchy_output,
            ell_cauchy_deficit,
            gain_deficit_q,
        ) != (
            fraction_type(31, 64),
            fraction_type(33, 64),
            fraction_type(349, 192),
            fraction_type(737, 4800),
            fraction_type(737, 1600),
        ):
            raise failure_type("ell-Cauchy no-go changed")

        packet_vector = (3, -1, -2, 4, -4)
        packet_vector_sum = sum_fn(packet_vector, 0)
        packet_vector_l1 = sum_fn((abs_fn(v) for v in packet_vector), 0)
        packet_vector_l2_sq = sum_fn((v * v for v in packet_vector), 0)
        if (packet_vector_sum, packet_vector_l1, packet_vector_l2_sq) != (0, 14, 46):
            raise failure_type("packet norm witness changed")

        compiler_truth = tuple_type(
            (emitter, cell, emitter and cell)
            for emitter in (False, True)
            for cell in (False, True)
        )
        if compiler_truth != (
            (False, False, False),
            (False, True, False),
            (True, False, False),
            (True, True, True),
        ):
            raise failure_type("conditional compiler logic changed")

        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("conditional_bridge_advance", "YES"),
            ("fixture_q", q),
            ("fixture_t", t),
            ("allowed_b", allowed_b),
            ("unit_to_b", unit_to_b),
            ("packet_total", str_type(packet_total)),
            ("packet_mean", str_type(packet_mean)),
            ("centered_packet", str_type(centered_packet)),
            ("direct_ratio", str_type(direct_ratio)),
            ("positive_branch", str_type(positive_branch)),
            ("compensating_background", str_type(compensating_background)),
            ("constant_packet", str_type(constant_packet)),
            ("raw_exponent", str_type(raw_exponent)),
            ("occupancy_x_exponent", str_type(occupancy_x)),
            ("occupancy_q_exponent", str_type(occupancy_q)),
            ("ideal_pre_cell_exponent", str_type(ideal_pre_cell)),
            ("bp_gamma", str_type(bp_gamma)),
            ("total_gain_threshold", str_type(total_gain_threshold)),
            ("rho_threshold_with_bp", str_type(rho_threshold)),
            ("omega_ceiling", str_type(omega_ceiling)),
            ("ideal_output_exponent", str_type(ideal_output)),
            ("ideal_endpoint_margin", str_type(ideal_margin)),
            ("sample_omega", str_type(sample_omega)),
            ("sample_output_exponent", str_type(sample_output)),
            ("sample_endpoint_margin", str_type(sample_margin)),
            ("equality_endpoint_margin", str_type(equality_margin)),
            ("ell_cauchy_rho", str_type(ell_cauchy_rho)),
            ("ell_cauchy_total_gain", str_type(ell_cauchy_total_gain)),
            ("ell_cauchy_output", str_type(ell_cauchy_output)),
            ("ell_cauchy_deficit", str_type(ell_cauchy_deficit)),
            ("gain_deficit_q", str_type(gain_deficit_q)),
            ("packet_vector_sum", packet_vector_sum),
            ("packet_vector_l1", packet_vector_l1),
            ("packet_vector_l2_sq", packet_vector_l2_sq),
            ("compiler_truth", compiler_truth),
            ("selected_route", "K_LOSS_BUDGETED_PACKET_FIRST__E_SECOND__X_THIRD__A_AFTER_B__C_RESERVE"),
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
