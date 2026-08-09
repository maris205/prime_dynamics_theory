#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V39 packet-energy pivot."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_BLOCK_PROJECTIVE_DUALITY_ABSOLUTE_MASS_LOWER_BARRIER_AND_GENERIC_"
    "SCHATTEN_CONTINUUM_SELECT_DIRECT_PACKET_ENERGY_AS_PRIMARY_OPEN_BRIDGE"
)


CONTRACT_ITEMS = (
    ("schema_version", "V39_SCHATTEN_DUAL_PACKET_ENERGY_V1"),
    ("artifact_name", "bridge_b_schatten_duality_and_packet_energy_pivot.md"),
    ("baseline_commit", "44a681ae29f1c13064fd672073eb7a7cd28694fd"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("route_position", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_CANONICAL_EMITTER_BUILT_PACKET_ENERGY_PIER_SELECTED_SCHATTEN_TOLL_EXPOSED"),
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
    ("zero_axis_factor", "(q^2-q+1)/q^2"),
    ("block_dual_class", "product_of_block_operator_unit_balls"),
    ("mass_lower_barrier", "lambda_q^(-1)*(q*||d_q||_1-|sum_r d_q(r)|)"),
    ("certified_schatten_alpha", "71/32-7/(16p)"),
    ("certified_p2_energy_ceiling", "399/200"),
    ("optimistic_p4_energy_ceiling", "773/400"),
    ("packet_energy", "sum_q_r|d_q(r)|^2"),
    ("direct_energy_factor", "Q^2"),
    ("kappa_threshold", "1/200"),
    ("sample_kappa", "1/100"),
    ("sample_output", "997/600"),
    ("selected_route", "P2_DIRECT_PACKET_ENERGY_FIRST__K_SPECIALIZED_SCHATTEN_SECOND__E_THIRD__X_FOURTH__A_TERMINAL_AFTER_B__C_RESERVE"),
    ("source_boundary", "NO_LITERAL_Q_DEPENDENT_PACKET_ENERGY_THEOREM"),
    ("fixture_q", 5),
    ("fixture_dual_value", 8),
    ("fixture_mass_lower", "500/21"),
    ("first_fatal", "NO_LITERAL_THEOREM_BOUNDS_SUM_Q_R_ABS_D_Q_R_SQUARED_BY_X_POWER_2_MINUS_KAPPA_FOR_KAPPA_GREATER_THAN_1_OVER_200"),
)


REGISTRY_ITEMS = (
    ("V39_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V39_ROUTE_ADVANCE", "YES"),
    ("V39_CONDITIONAL_BRIDGE_ADVANCE", "YES"),
    ("V39_ARITHMETIC_ADVANCE", "NO"),
    ("V39_FIXED_ATOM_CREDIT", "0"),
    ("V39_STRICT_1_OVER_400", "UNPAID"),
    ("V39_L2", "NONE"),
    ("V39_TPC_207_TRIGGER", "false"),
    ("V39_NUMBERED_RELEASE", "NO"),
    ("V39_DERIVATION_STATUS", "COHERENT_AFTER_BLOCK_NUCLEAR_DUALITY_MASS_BARRIER_CERTIFIED_AND_OPTIMISTIC_SCHATTEN_COMPARISON"),
    ("V39_ASSUMPTION_POLICY", "PACKET_ENERGY_AND_SPECIALIZED_SCHATTEN_COMPRESSION_REMAIN_EXPLICIT_OPEN_THEOREMS"),
    ("V39_SELECTED_RESEARCH_ROUTE", "P2_DIRECT_PACKET_ENERGY_FIRST__K_SPECIALIZED_SCHATTEN_SECOND__E_THIRD__X_FOURTH__A_TERMINAL_AFTER_B__C_RESERVE"),
    ("V39_V38_CANONICAL_EMITTER", "RETAINED_EXACT_ZERO_REMAINDER"),
    ("V39_BLOCK_PROJECTIVE_DUALITY", "PROVED_EXACT_PRODUCT_OF_BLOCK_OPERATOR_BALLS"),
    ("V39_BLOCK_DUAL_CURVE_TEST", "PROVED_EXACT_PHI_Q_T_ON_R_AND_R_INVERSE"),
    ("V39_PHYSICAL_DUAL_EXPANSION", "PROVED_EXACT_BETA_TIMES_CENTERED_G_TIMES_PHI"),
    ("V39_ATOMIC_ABSOLUTE_MASS_LOWER_BARRIER", "PROVED_LAMBDA_INVERSE_TIMES_Q_D_L1_MINUS_ABS_SUM_D"),
    ("V39_SCALAR_ZERO_ATOMIC_ZERO_IMPLICATION", "STOP_SCOPED_Q5_ALTERNATING_PACKET_COUNTEREXAMPLE"),
    ("V39_CANONICAL_SCHATTEN_GATE", "RETAINED_OPEN_SPECIALIZED_NON_GENERIC_COMPRESSION_LANE"),
    ("V39_BLOMER_PASCADI_FORMAL_INTERFACE", "SOURCE_BACKED_SEPARABLE_BILINEAR_OPERATOR_NORM_Q_MINUS_1_OVER_32"),
    ("V39_BLOMER_PASCADI_FOURTH_MOMENT", "PROOF_ARCHITECTURE_NOT_STANDALONE_ALL_BLOCK_S4_THEOREM"),
    ("V39_OPTIMISTIC_S4_POLICY", "COUNTERFACTUAL_GRANT_FOR_ROUTE_STRESS_TEST_NO_THEOREM_CREDIT"),
    ("V39_CERTIFIED_SCHATTEN_ALPHA", "71_OVER_32_MINUS_7_OVER_16P"),
    ("V39_CERTIFIED_SCHATTEN_ENERGY_CEILING", "2219_OVER_1200_PLUS_7_OVER_24P"),
    ("V39_CERTIFIED_P2_ENERGY_CEILING", "399_OVER_200"),
    ("V39_CERTIFIED_P4_ENERGY_CEILING", "4613_OVER_2400"),
    ("V39_CERTIFIED_PINFINITY_ENERGY_CEILING", "2219_OVER_1200"),
    ("V39_OPTIMISTIC_S4_P4_ENERGY_CEILING", "773_OVER_400"),
    ("V39_GENERIC_SCHATTEN_OPTIMUM", "PROVED_P_EQUALS_2_EVEN_AFTER_OPTIMISTIC_S4_GRANT"),
    ("V39_PACKET_ENERGY", "SUM_Q_SUM_R_ABS_D_Q_R_SQUARED"),
    ("V39_DIRECT_PACKET_ENERGY_CAUCHY", "PROVED_Q_SQUARED_TIMES_PACKET_ENERGY_SQUARE_ROOT"),
    ("V39_PACKET_ENERGY_GATE", "OPEN_CONJECTURE_X_POWER_2_MINUS_KAPPA"),
    ("V39_PACKET_ENERGY_KAPPA_THRESHOLD", "KAPPA_STRICTLY_GREATER_THAN_1_OVER_200"),
    ("V39_PACKET_ENERGY_CONDITIONAL_OUTPUT", "X_POWER_5_OVER_3_MINUS_KAPPA_OVER_2"),
    ("V39_PACKET_ENERGY_ENDPOINT_MARGIN", "KAPPA_OVER_2_MINUS_1_OVER_400"),
    ("V39_SAMPLE_KAPPA", "1_OVER_100"),
    ("V39_SAMPLE_OUTPUT", "997_OVER_600"),
    ("V39_SAMPLE_ENDPOINT_MARGIN", "1_OVER_400"),
    ("V39_KERR_SHPARLINSKI_WU_XI_DIRECT_ATTACHMENT", "STOP_SCOPED_SEPARABLE_BILINEAR_ARRAYS_NO_LITERAL_Q_DEPENDENT_PACKET_ENERGY"),
    ("V39_KOWALSKI_MICHEL_SAWIN_DIRECT_ATTACHMENT", "STOP_SCOPED_SEPARABLE_HYPER_KLOOSTERMAN_BILINEAR_WRONG_MATRIX_AND_PACKET_NORM"),
    ("V39_HARPER_GENERAL_BDH_DIRECT_ATTACHMENT", "STOP_SCOPED_ONE_Q_INDEPENDENT_SEQUENCE_MODULUS_RANGE_AND_DISTRIBUTION_HYPOTHESES_MISMATCH"),
    ("V39_DIRECT_PRIMARY_SOURCE_FOR_PACKET_ENERGY_GATE", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09"),
    ("V39_ROUTE_E", "RETAINED_OPEN_WHOLE_RESIDUAL_SIGMA_LT_13_OVER_4800"),
    ("V39_ROUTE_X", "RETAINED_OPEN_JOINT_CHARACTER_KAPPA_GT_403_OVER_1200"),
    ("V39_TERMINAL_A", "OPEN_TERMINAL_EQUIVALENT_SIGNED_QLOCAL_COVARIANCE_AFTER_B"),
    ("V39_DYNAMICS_C", "RESERVE_DISTINGUISHED_SEED_ATTACHMENT_STILL_OPEN"),
    ("V39_NEXT_THEOREM", "DIRECT_LITERAL_Q_DEPENDENT_CENTERED_PACKET_ENERGY_WITH_KAPPA_1_OVER_100_BENCHMARK"),
    ("V39_FIRST_FATAL", "NO_LITERAL_THEOREM_BOUNDS_SUM_Q_R_ABS_D_Q_R_SQUARED_BY_X_POWER_2_MINUS_KAPPA_FOR_KAPPA_GREATER_THAN_1_OVER_200"),
    ("V39_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_CANONICAL_EMITTER_BUILT_PACKET_ENERGY_PIER_SELECTED_SCHATTEN_TOLL_EXPOSED"),
    ("V39_SOURCE_LOCK_POLICY", "PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED"),
    ("V39_ROUTE_MAP_REFERENCE", "TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B"),
)


EXPECTED_REGISTRY_SHA256 = "4596392ed36f38b087677624005a45ffd1d9f57e1dbbe19dc361d8fb385dc1f7"


SOURCE_ITEMS = (
    ("BLOMER_PASCADI_OPERATOR_CELL", "arXiv:2607.24311v1_Theorem_1.1_Sections_1.4_1.5"),
    ("KERR_SHPARLINSKI_WU_XI_BILINEAR", "arXiv:2204.05038v5_Theorems_2.5_2.8"),
    ("KOWALSKI_MICHEL_SAWIN_BILINEAR", "arXiv:1511.01636v5_Theorem_1.1"),
    ("HARPER_GENERAL_BDH", "arXiv:2412.19644v1_Theorems_1_2"),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_canonical_packet_schatten_emitter.md",
        "3ba663dd409fd12a901d12799d0ee0ca851751d047eeaa09a605c867dc1495e1",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_canonical_packet_schatten_checker.py",
        "b0d986384bb0cf023505df63d5f07d3e7de1427194711d963b2d6e7757031cec",
    ),
    (
        "research/tpc-big-road/bridge_b_loss_budgeted_shift_packet_compiler.md",
        "07226c6af1c8145982f5cb71fbfe3159cb11f27e6ecd7eba4014431a0d024545",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_loss_budgeted_shift_packet_checker.py",
        "cc0427402fa7f4df85bffb927e06ed5bdf3a9cc14a19bdf76dd832b87cfd4ee4",
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

    if dict_type(literal_contract).get("maximum_claim") != literal_maximum_claim:
        raise failure_type("maximum claim contract seed changed")
    if dict_type(literal_registry).get("V39_MAXIMUM_CLAIM") != literal_maximum_claim:
        raise failure_type("maximum claim registry seed changed")
    if registry_digest(literal_registry) != literal_registry_digest:
        raise failure_type("registry literal digest changed")

    def compute_base() -> tuple[tuple[str, object], ...]:
        q = 5
        units = tuple_type(range_fn(1, q))
        d = (3, -2, 5, 1)

        def inverse(value: int) -> int:
            for candidate in range_fn(1, q):
                if (value * candidate) % q == 1:
                    return candidate
            raise failure_type("inverse missing")

        phi = tuple_type(
            q - 1 if (r + inverse(r)) % q == 0 else -1 for r in units
        )
        dual_value = sum_fn((d[index] * phi[index] for index in range_fn(q - 1)), 0)
        if (units, phi, dual_value) != ((1, 2, 3, 4), (-1, 4, 4, -1), 8):
            raise failure_type("physical dual fixture changed")

        block_sizes = (3, 2)
        blocks = (tuple_type(range_fn(0, 3)), tuple_type(range_fn(3, 5)))
        identity_block_checks = []
        for left in blocks:
            for right in blocks:
                row_counts = tuple_type(
                    sum_fn((int_type(m == n) for n in right), 0) for m in left
                )
                col_counts = tuple_type(
                    sum_fn((int_type(m == n) for m in left), 0) for n in right
                )
                identity_block_checks.append(
                    all_fn(value <= 1 for value in row_counts + col_counts)
                )
        if block_sizes != tuple_type(len_fn(block) for block in blocks):
            raise failure_type("balanced blocks changed")
        if not all_fn(identity_block_checks):
            raise failure_type("identity block contraction changed")

        alternating = (1, -1, 1, -1)
        alternating_sum = sum_fn(alternating, 0)
        alternating_l1 = sum_fn((abs_fn(value) for value in alternating), 0)
        lambda_q = fraction_type(q * q - q + 1, q * q)
        full_nuclear = fraction_type(alternating_l1, q)
        mass_lower = fraction_type(q * alternating_l1 - abs_fn(alternating_sum), 1) / lambda_q
        if (
            alternating_sum,
            alternating_l1,
            lambda_q,
            full_nuclear,
            mass_lower,
        ) != (
            0,
            4,
            fraction_type(21, 25),
            fraction_type(4, 5),
            fraction_type(500, 21),
        ):
            raise failure_type("absolute mass barrier changed")

        synthetic_nuclear = 5 + 4
        synthetic_dual = 3 + 2 + 4
        synthetic_operator_norms = (1, 1)
        if (synthetic_nuclear, synthetic_dual, synthetic_operator_norms) != (9, 9, (1, 1)):
            raise failure_type("projective dual fixture changed")

        endpoint = fraction_type(1997, 1200)

        def certified_alpha(p: int) -> Fraction:
            return fraction_type(71, 32) - fraction_type(7, 16 * p)

        def energy_ceiling(alpha: Fraction) -> Fraction:
            return 2 * (endpoint - alpha / 3)

        cert_alpha_2 = certified_alpha(2)
        cert_alpha_4 = certified_alpha(4)
        cert_alpha_inf = fraction_type(71, 32)
        cert_eta_2 = energy_ceiling(cert_alpha_2)
        cert_eta_4 = energy_ceiling(cert_alpha_4)
        cert_eta_inf = energy_ceiling(cert_alpha_inf)
        if (
            cert_alpha_2,
            cert_alpha_4,
            cert_alpha_inf,
            cert_eta_2,
            cert_eta_4,
            cert_eta_inf,
        ) != (
            fraction_type(2),
            fraction_type(135, 64),
            fraction_type(71, 32),
            fraction_type(399, 200),
            fraction_type(4613, 2400),
            fraction_type(2219, 1200),
        ):
            raise failure_type("certified Schatten continuum changed")
        if not (cert_eta_2 > cert_eta_4 > cert_eta_inf):
            raise failure_type("certified route ordering changed")

        opt_alpha_2 = fraction_type(2)
        opt_alpha_4 = fraction_type(67, 32)
        opt_alpha_inf = fraction_type(71, 32)
        opt_eta_2 = energy_ceiling(opt_alpha_2)
        opt_eta_4 = energy_ceiling(opt_alpha_4)
        opt_eta_inf = energy_ceiling(opt_alpha_inf)
        if (
            opt_eta_2,
            opt_eta_4,
            opt_eta_inf,
        ) != (
            fraction_type(399, 200),
            fraction_type(773, 400),
            fraction_type(2219, 1200),
        ):
            raise failure_type("optimistic S4 route changed")
        if not (opt_eta_2 > opt_eta_4 > opt_eta_inf):
            raise failure_type("optimistic route ordering changed")

        kappa_threshold = fraction_type(2) - cert_eta_2
        sample_kappa = fraction_type(1, 100)
        sample_output = fraction_type(5, 3) - sample_kappa / 2
        sample_margin = endpoint - sample_output
        if (
            kappa_threshold,
            sample_output,
            sample_margin,
        ) != (
            fraction_type(1, 200),
            fraction_type(997, 600),
            fraction_type(1, 400),
        ):
            raise failure_type("packet energy endpoint changed")

        route_truth = tuple_type(
            (emitter, energy, terminal, emitter and energy and terminal)
            for emitter in (False, True)
            for energy in (False, True)
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
            ("phi_identity", phi),
            ("dual_value", dual_value),
            ("block_sizes", block_sizes),
            ("identity_block_contractions", tuple_type(identity_block_checks)),
            ("alternating_d", alternating),
            ("alternating_sum", alternating_sum),
            ("alternating_l1", alternating_l1),
            ("lambda_q", str_type(lambda_q)),
            ("full_nuclear", str_type(full_nuclear)),
            ("mass_lower", str_type(mass_lower)),
            ("synthetic_nuclear", synthetic_nuclear),
            ("synthetic_dual", synthetic_dual),
            ("cert_alpha_p2", str_type(cert_alpha_2)),
            ("cert_alpha_p4", str_type(cert_alpha_4)),
            ("cert_alpha_pinf", str_type(cert_alpha_inf)),
            ("cert_eta_p2", str_type(cert_eta_2)),
            ("cert_eta_p4", str_type(cert_eta_4)),
            ("cert_eta_pinf", str_type(cert_eta_inf)),
            ("opt_eta_p2", str_type(opt_eta_2)),
            ("opt_eta_p4", str_type(opt_eta_4)),
            ("opt_eta_pinf", str_type(opt_eta_inf)),
            ("kappa_threshold", str_type(kappa_threshold)),
            ("sample_kappa", str_type(sample_kappa)),
            ("sample_output", str_type(sample_output)),
            ("sample_margin", str_type(sample_margin)),
            ("route_truth", route_truth),
            ("selected_route", "P2_DIRECT_PACKET_ENERGY_FIRST__K_SPECIALIZED_SCHATTEN_SECOND__E_THIRD__X_FOURTH__A_TERMINAL_AFTER_B__C_RESERVE"),
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
