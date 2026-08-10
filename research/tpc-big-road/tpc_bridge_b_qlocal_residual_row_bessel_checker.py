#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V41 q-local residual-row bridge."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_QLOCAL_ROW_SPLIT_AND_ELEMENTARY_MODEL_ENERGY_PAYMENT_REDUCE_GATE_"
    "B_TO_RESIDUAL_ROW_BESSEL_WITH_ZERO_AXIS_FIREWALL"
)


SELECTED_ROUTE = (
    "QLR_RESIDUAL_Q_ROW_ENERGY_FIRST__RBR_RESTRICTED_RESIDUAL_ROW_BESSEL_"
    "IMPLEMENTATION__DUAL_AND_CHARACTER_FORMS_SECOND__P2_K_E_X_RESERVES__"
    "A_TERMINAL__C_RESERVE"
)


FIRST_FATAL = (
    "NO_LITERAL_THEOREM_BOUNDS_SUM_Q_ABS_RHO_Q_SQUARED_AT_X_POWER_7_OVER_"
    "3_MINUS_KAPPA_FOR_KAPPA_GREATER_THAN_1_OVER_200"
)


CONTRACT_ITEMS = (
    ("schema_version", "V41_QLOCAL_RESIDUAL_ROW_BESSEL_V1"),
    ("artifact_name", "bridge_b_qlocal_residual_row_bessel_compiler.md"),
    ("baseline_commit", "fa68a37a73fe543983fb9c369498e53321bff080"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("route_position", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_QLOCAL_MODEL_PIER_PAID_RESIDUAL_ROW_BESSEL_SPAN_OPEN"),
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
    ("row_split", "s_q=m_q+rho_q"),
    ("model_row_pointwise", "x^(1+o(1))*H/q^2"),
    ("model_row_point_exponent", "95/96"),
    ("model_energy", "x^(37/16+o(1))"),
    ("model_output", "x^(53/32+o(1))"),
    ("model_margin", "19/2400"),
    ("residual_energy", "sum_q|rho_q|^2"),
    ("residual_gate", "x^(7/3-kappa+o(1))"),
    ("kappa_threshold", "1/200"),
    ("residual_diagonal", "x^(95/48+o(1))"),
    ("residual_bessel_tau_threshold", "419/1200"),
    ("sample_tau", "1/3"),
    ("sample_energy", "37/16"),
    ("sample_output", "53/32"),
    ("sample_margin", "19/2400"),
    ("q_squared_over_H", "x^(1/96)"),
    ("selected_route", SELECTED_ROUTE),
    ("source_boundary", "NO_LITERAL_QLOCAL_RESIDUAL_ROW_ENERGY_THEOREM"),
    ("fixture_q", 5),
    ("fixture_gamma", ("0", "5/16", "5/16", "-15/16", "5/16")),
    ("fixture_gamma_sum", "0"),
    ("fixture_full_convolution", ("5/16", "5/16", "-15/16", "5/16")),
    ("fixture_off_convolution", ("5/64", "5/64", "-15/64", "5/64")),
    ("fixture_s", "-11717/5040"),
    ("fixture_m", "307/1792"),
    ("fixture_rho", "-201287/80640"),
    ("zero_axis_row_energy", "0"),
    ("zero_axis_atom", "37"),
    ("first_fatal", FIRST_FATAL),
)


REGISTRY_ITEMS = (
    ("V41_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V41_ROUTE_ADVANCE", "YES"),
    ("V41_CONDITIONAL_BRIDGE_ADVANCE", "YES"),
    ("V41_ARITHMETIC_ADVANCE", "NO"),
    ("V41_FIXED_ATOM_CREDIT", "0"),
    ("V41_STRICT_1_OVER_400", "UNPAID"),
    ("V41_L2", "NONE"),
    ("V41_TPC_207_TRIGGER", "false"),
    ("V41_NUMBERED_RELEASE", "NO"),
    ("V41_DERIVATION_STATUS", "COHERENT_AFTER_EXACT_QLOCAL_SPLIT_THREE_RESIDUE_MODEL_PAYMENT_RESIDUAL_ENDPOINT_AND_ZERO_AXIS_FIREWALL"),
    ("V41_ASSUMPTION_POLICY", "RESIDUAL_ROW_ENERGY_OR_RESTRICTED_RESIDUAL_ROW_BESSEL_REMAINS_EXPLICIT_OPEN_THEOREM"),
    ("V41_SELECTED_RESEARCH_ROUTE", SELECTED_ROUTE),
    ("V41_V40_CONSTANT_RESIDUE_SCALAR", "RETAINED_EXACT_ZERO_REMAINDER"),
    ("V41_QLOCAL_PROFILE", "GAMMA_Q_THREE_RESIDUE_FORM_REUSED_FROM_V30"),
    ("V41_QLOCAL_PROFILE_MEAN", "PROVED_EXACT_ZERO_MOD_Q"),
    ("V41_EXACT_ROW_SPLIT", "S_Q_EQUALS_M_Q_PLUS_RHO_Q"),
    ("V41_MODEL_ROW_POINTWISE", "PROVED_X_POWER_1_TIMES_H_OVER_Q_SQUARED"),
    ("V41_MODEL_EXCEPTIONAL_RESIDUE", "T_CONGRUENT_MINUS_2_COUNT_X_OVER_Q"),
    ("V41_MODEL_ROW_ENERGY", "PROVED_X_POWER_37_OVER_16"),
    ("V41_MODEL_SCALAR_OUTPUT", "PROVED_X_POWER_53_OVER_32"),
    ("V41_MODEL_ENDPOINT_MARGIN", "19_OVER_2400"),
    ("V41_V40_LOCAL_CARRIER_ROWWISE_STATUS", "PAID_AT_ROW_BENCHMARK"),
    ("V41_RESIDUAL_ROW_ENERGY", "SUM_Q_ABS_RHO_Q_SQUARED"),
    ("V41_RESIDUAL_ROW_ENERGY_GATE", "OPEN_CONJECTURE_X_POWER_7_OVER_3_MINUS_KAPPA"),
    ("V41_RESIDUAL_KAPPA_THRESHOLD", "KAPPA_STRICTLY_GREATER_THAN_1_OVER_200"),
    ("V41_RESIDUAL_CONDITIONAL_OUTPUT", "MAX_OF_X_POWER_53_OVER_32_AND_X_POWER_5_OVER_3_MINUS_KAPPA_OVER_2"),
    ("V41_RESIDUAL_ENDPOINT_MARGIN", "MIN_OF_19_OVER_2400_AND_KAPPA_OVER_2_MINUS_1_OVER_400"),
    ("V41_FULL_ROW_FROM_RESIDUAL", "PROVED_TRIANGLE_WITH_PAID_MODEL"),
    ("V41_RESIDUAL_ROW_DIAGONAL", "PROVED_X_POWER_95_OVER_48"),
    ("V41_RESTRICTED_RESIDUAL_ROW_BESSEL_GATE", "OPEN_CONJECTURE_E_RES_LE_X_POWER_TAU_TIMES_D_RES"),
    ("V41_RESTRICTED_RESIDUAL_ROW_BESSEL_TAU_THRESHOLD", "TAU_STRICTLY_LESS_THAN_419_OVER_1200"),
    ("V41_SAMPLE_RESIDUAL_TAU", "1_OVER_3"),
    ("V41_SAMPLE_RESIDUAL_ENERGY", "X_POWER_37_OVER_16"),
    ("V41_SAMPLE_RESIDUAL_OUTPUT", "X_POWER_53_OVER_32"),
    ("V41_SAMPLE_RESIDUAL_MARGIN", "19_OVER_2400"),
    ("V41_RESIDUAL_L2_DUAL", "PROVED_ONE_OUTER_ABSOLUTE_MODULUS_FAMILY"),
    ("V41_RESIDUAL_CHARACTER_ROW", "PROVED_EXACT_CENTERED_BW_RES_MINUS_Z_RES"),
    ("V41_SEPARATE_MARGINAL_LARGE_SIEVE", "STOP_SCOPED_DOES_NOT_CONTROL_SAME_INDEX_RESIDUAL_PRODUCT"),
    ("V41_OFFZERO_RESIDUAL_TO_ZERO_AXIS", "STOP_SCOPED_DELTA_ZERO_FIXTURE"),
    ("V41_AUGMENTED_ROW_WITH_ZERO_AXIS", "TERMINAL_EQUIVALENT_NOT_PRELIMINARY"),
    ("V41_TERMINAL_QLOCAL_GATE_A", "OPEN_INDEPENDENT_SIGNED_COVARIANCE"),
    ("V41_MRT_DIRECT_ATTACHMENT", "STOP_SCOPED_SOURCE_COEFFICIENTS_LOG_SAVING_AND_Q_DEPENDENT_RESIDUAL_MISMATCH"),
    ("V41_MERIKOSKI_DIRECT_ATTACHMENT", "STOP_SCOPED_UNWEIGHTED_FIRST_SHIFT_AVERAGE_NOT_CENTERED_ROW_SQUARE"),
    ("V41_LICHTMAN_TERAVAINEN_DIRECT_ATTACHMENT", "STOP_SCOPED_QUALITATIVE_EXCEPTIONAL_SET_CAN_CONTAIN_SPARSE_QK_SUPPORT_AND_COEFFICIENTS_MISMATCH"),
    ("V41_EVANS_DIRECT_ATTACHMENT", "STOP_SCOPED_E2_FACTOR_WINDOWS_AND_ALMOST_ALL_SHIFT_OUTPUT_MISMATCH"),
    ("V41_KOUKOULOPOULOS_SHORT_AP_ATTACHMENT", "STOP_SCOPED_Q_SQUARED_EXCEEDS_H_AND_ONE_SEQUENCE_MARGINAL"),
    ("V41_HARPER_GENERAL_BDH_ATTACHMENT", "STOP_SCOPED_FIXED_SEQUENCE_LARGE_MODULUS_AND_DISTRIBUTION_HYPOTHESES_MISMATCH"),
    ("V41_BAZIN_BETA_MARGINAL_TO_RESIDUAL_ROW", "STOP_SCOPED_ONE_SIDED_MARGINAL_AND_H_QUARTER_LOSS"),
    ("V41_DIRECT_PRIMARY_SOURCE_FOR_RESIDUAL_ROW_GATE", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10"),
    ("V41_FIRST_FATAL", FIRST_FATAL),
    ("V41_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_QLOCAL_MODEL_PIER_PAID_RESIDUAL_ROW_BESSEL_SPAN_OPEN"),
    ("V41_SOURCE_LOCK_POLICY", "PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED"),
    ("V41_ROUTE_MAP_REFERENCE", "TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B"),
)


EXPECTED_REGISTRY_SHA256 = "4a2d9f9f8f243deaea18dce16e0af0c7de69b0f4befedb37356b4b80dc62156e"


SOURCE_ITEMS = (
    ("MRT_LONG_SHIFT", "arXiv:1707.01315v3_Theorem_1.3_and_Proposition_3.1"),
    ("MERIKOSKI_AVERAGED_HL", "arXiv:1605.04757v1_Main_Theorem_1_and_Corollary_1"),
    ("LICHTMAN_TERAVAINEN_HLC", "arXiv:2111.08912v3_Theorem_1.1"),
    ("EVANS_ALMOST_PRIMES", "arXiv:2102.12297v3_Theorems_1.1_and_1.4"),
    ("KOUKOULOPOULOS_SHORT_AP", "arXiv:1405.6592v2_Theorems_1.1_1.2_1.3"),
    ("HARPER_GENERAL_BDH", "arXiv:2412.19644v1_Theorems_1_2"),
    ("BAZIN_TYPE_I_II", "arXiv:2607.15137v1_Theorem_8"),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_row_energy_and_packet_route_atlas.md",
        "1f7ae86094a2ff908ba41be6eaefd36bf6959b7e2618e909c59daa44df828ca4",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_row_energy_route_atlas_checker.py",
        "0385c32f52d80d8cd50e529603440c02e7cc4f581c8b9e8bbd3743fe619b13c4",
    ),
    (
        "research/tpc-big-road/bridge_b_terminal_major_cross_flatness_and_equivariant_quotient.md",
        "5c3d59e3b324a8c67109566c5e54dd3d3fc381b295b2c6cce15c49762ea4bbf6",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_terminal_major_cross_flatness_checker.py",
        "662dbe9259f8a6176894711d692470608115b9df89f255e6c53dbd493e11cfcf",
    ),
)


def _make_trusted_runner(
    maximum_claim_seed=MAXIMUM_CLAIM,
    selected_route_seed=SELECTED_ROUTE,
    first_fatal_seed=FIRST_FATAL,
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
    literal_first_fatal = first_fatal_seed
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
    if registry_map.get("V41_MAXIMUM_CLAIM") != literal_maximum_claim:
        raise failure_type("maximum claim registry seed changed")
    if contract_map.get("selected_route") != literal_selected_route:
        raise failure_type("selected route contract seed changed")
    if registry_map.get("V41_SELECTED_RESEARCH_ROUTE") != literal_selected_route:
        raise failure_type("selected route registry seed changed")
    if contract_map.get("first_fatal") != literal_first_fatal:
        raise failure_type("first fatal contract seed changed")
    if registry_map.get("V41_FIRST_FATAL") != literal_first_fatal:
        raise failure_type("first fatal registry seed changed")
    if registry_digest(literal_registry) != literal_registry_digest:
        raise failure_type("registry literal digest changed")

    def gamma(q: int, residue: int) -> Fraction:
        reduced = residue % q
        if reduced == (-2) % q:
            return -fraction_type(q * (q - 2), (q - 1) ** 2)
        if reduced == 0:
            return fraction_type(0)
        return fraction_type(q, (q - 1) ** 2)

    def centered_multiplier(q: int, h: int) -> Fraction:
        return fraction_type(int_type(h % q == 0)) - fraction_type(1, q - 1)

    def compute_base() -> tuple[tuple[str, object], ...]:
        q = 5
        gamma_vector = tuple_type(gamma(q, residue) for residue in range_fn(q))
        gamma_sum = sum_fn(gamma_vector, fraction_type(0))
        if gamma_vector != (
            fraction_type(0),
            fraction_type(5, 16),
            fraction_type(5, 16),
            -fraction_type(15, 16),
            fraction_type(5, 16),
        ) or gamma_sum != 0:
            raise failure_type("q-local profile fixture changed")

        full_convolution = tuple_type(
            sum_fn(
                (
                    gamma(q, u) * centered_multiplier(q, u - t)
                    for u in range_fn(q)
                ),
                fraction_type(0),
            )
            for t in range_fn(1, q)
        )
        off_convolution = tuple_type(
            sum_fn(
                (
                    gamma(q, u) * centered_multiplier(q, u - t)
                    for u in range_fn(q)
                    if u != t
                ),
                fraction_type(0),
            )
            for t in range_fn(1, q)
        )
        if full_convolution != tuple_type(gamma_vector[t] for t in range_fn(1, q)):
            raise failure_type("full q-local convolution changed")
        if off_convolution != tuple_type(gamma_vector[t] / (q - 1) for t in range_fn(1, q)):
            raise failure_type("off-diagonal q-local convolution changed")

        toy_interval = (1, 2, 3, 4, 6, 7, 8, 9)

        def beta(t: int) -> Fraction:
            return fraction_type((t % 7) - 3)

        def physical_w(u: int) -> Fraction:
            return fraction_type(((2 * u + 1) % 9) - 4)

        def kernel(h: int) -> Fraction:
            return fraction_type(1, 1 + abs_fn(h))

        physical_row = fraction_type(0)
        model_row = fraction_type(0)
        residual_row = fraction_type(0)
        for t in toy_interval:
            for u in toy_interval:
                if t == u:
                    continue
                common = beta(t) * kernel(u - t) * centered_multiplier(q, u - t)
                physical_row += common * physical_w(u)
                model_row += common * gamma(q, u)
                residual_row += common * (physical_w(u) - gamma(q, u))
        if (
            physical_row,
            model_row,
            residual_row,
            model_row + residual_row,
        ) != (
            -fraction_type(11717, 5040),
            fraction_type(307, 1792),
            -fraction_type(201287, 80640),
            physical_row,
        ):
            raise failure_type("exact row split fixture changed")

        H = fraction_type(21, 32)
        Q = fraction_type(1, 3)
        endpoint = fraction_type(1997, 1200)
        model_row_point = fraction_type(1) + H - 2 * Q
        model_energy = fraction_type(2) + 2 * H - 3 * Q
        model_output = 3 * Q / 2 + model_energy / 2
        model_margin = endpoint - model_output
        row_gate = fraction_type(7, 3)
        model_kappa = row_gate - model_energy
        kappa_threshold = fraction_type(1, 200)
        residual_diagonal = fraction_type(1) + 2 * H - Q
        tau_threshold = row_gate - kappa_threshold - residual_diagonal
        sample_tau = fraction_type(1, 3)
        sample_energy = residual_diagonal + sample_tau
        q_squared_gap = 2 * Q - H
        if (
            model_row_point,
            model_energy,
            model_output,
            model_margin,
            model_kappa,
            residual_diagonal,
            tau_threshold,
            sample_energy,
            q_squared_gap,
        ) != (
            fraction_type(95, 96),
            fraction_type(37, 16),
            fraction_type(53, 32),
            fraction_type(19, 2400),
            fraction_type(1, 48),
            fraction_type(95, 48),
            fraction_type(419, 1200),
            fraction_type(37, 16),
            fraction_type(1, 96),
        ):
            raise failure_type("V41 exponent ledger changed")
        if not (
            model_kappa > kappa_threshold
            and sample_tau < tau_threshold
            and model_output < endpoint
        ):
            raise failure_type("strict endpoint relation changed")

        zero_axis_atom = 37
        zero_axis_rows = tuple_type(0 for _ in (5, 7, 11))
        zero_axis_energy = sum_fn((value * value for value in zero_axis_rows), 0)
        if (zero_axis_energy, zero_axis_atom) != (0, 37):
            raise failure_type("zero-axis firewall fixture changed")

        route_truth = tuple_type(
            (model_paid, residual_paid, terminal_paid, model_paid and residual_paid and terminal_paid)
            for model_paid in (False, True)
            for residual_paid in (False, True)
            for terminal_paid in (False, True)
        )
        if sum_fn((int_type(row[-1]) for row in route_truth), 0) != 1:
            raise failure_type("conditional route logic changed")

        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("conditional_bridge_advance", "YES"),
            ("fixture_q", q),
            ("gamma_vector", tuple_type(str_type(value) for value in gamma_vector)),
            ("gamma_sum", str_type(gamma_sum)),
            ("full_convolution", tuple_type(str_type(value) for value in full_convolution)),
            ("off_convolution", tuple_type(str_type(value) for value in off_convolution)),
            ("toy_interval", toy_interval),
            ("physical_row", str_type(physical_row)),
            ("model_row", str_type(model_row)),
            ("residual_row", str_type(residual_row)),
            ("row_split_exact", physical_row == model_row + residual_row),
            ("model_row_point_exponent", str_type(model_row_point)),
            ("model_energy_exponent", str_type(model_energy)),
            ("model_output_exponent", str_type(model_output)),
            ("model_margin", str_type(model_margin)),
            ("model_kappa", str_type(model_kappa)),
            ("kappa_threshold", str_type(kappa_threshold)),
            ("residual_diagonal_exponent", str_type(residual_diagonal)),
            ("tau_threshold", str_type(tau_threshold)),
            ("sample_tau", str_type(sample_tau)),
            ("sample_energy", str_type(sample_energy)),
            ("q_squared_over_H_gap", str_type(q_squared_gap)),
            ("zero_axis_rows", zero_axis_rows),
            ("zero_axis_row_energy", zero_axis_energy),
            ("zero_axis_atom", zero_axis_atom),
            ("route_truth", route_truth),
            ("selected_route", literal_selected_route),
            ("first_fatal", literal_first_fatal),
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
