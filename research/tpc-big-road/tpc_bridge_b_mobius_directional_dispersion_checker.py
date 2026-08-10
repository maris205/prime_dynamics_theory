#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V42 directional-dispersion bridge."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_QLOCAL_POSITIVE_GRAM_GATE_PROPER_FACTOR_LIFT_PAID_OCCURRENCE_"
    "DIAGONAL_DYADIC_DIRECTIONAL_COMPILER_AND_OPERATOR_ONLY_CERTIFICATE_NO_GO"
)


SELECTED_ROUTE = (
    "PROPER_FACTOR_DIRECTIONAL_DISPERSION_FIRST__SOURCE_NATIVE_TYPE_I_II_"
    "TRANSFORM_SECOND__GENERIC_OPERATOR_AND_MARGINAL_ROADS_STOP__A_"
    "TERMINAL__C_RESERVE"
)


FIRST_FATAL = (
    "NO_LITERAL_THEOREM_BOUNDS_POSITIVE_PHYSICAL_OFFDIAGONAL_GRAM_COLLISION_"
    "AT_X_POWER_37_OVER_16_WHILE_RETAINING_CENTERED_SPIKE_BACKGROUND_CROSS_TERM"
)


CONTRACT_ITEMS = (
    ("schema_version", "V42_MOBIUS_DIRECTIONAL_DISPERSION_V1"),
    ("artifact_name", "bridge_b_mobius_directional_dispersion_compiler.md"),
    ("baseline_commit", "48b7bca985f35ccd4295b9ce44b55177488eef32"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("route_position", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_QLOCAL_MODEL_PIER_PAID_PROPER_FACTOR_DIRECTIONAL_SPAN_OPEN"),
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
    ("proper_factor_identity", "beta(t)=sum_(dk=t,d,k>=2)mu(d)omega_x(d,k)"),
    ("proper_factor_diagonal", "x^(95/48+o(1))"),
    ("cell_gate", "E_j<=Q*x^o*D_j"),
    ("conditional_residual_energy", "x^(37/16+o(1))"),
    ("conditional_dual_norm", "x^(37/32+o(1))"),
    ("conditional_output", "x^(53/32+o(1))"),
    ("conditional_margin", "19/2400"),
    ("operator_certificate_floor", "N_active/x^(1/3+o(1))"),
    ("operator_support_ceiling", "x^(273/400-o(1))"),
    ("operator_full_active_floor", "x^(2/3+o(1))"),
    ("operator_endpoint_excess", "127/400"),
    ("matrix_fixture_shape", "2x8"),
    ("matrix_fixture_hs", 16),
    ("matrix_fixture_energy", 64),
    ("matrix_fixture_ratio", "4"),
    ("matrix_fixture_stable_rank", "2"),
    ("q5_fixture_M", 3),
    ("q5_fixture_row", "45/4"),
    ("q5_fixture_diagonal", "189/16"),
    ("q5_fixture_energy", "2025/16"),
    ("q5_fixture_ratio", "75/7"),
    ("q5_fixture_offdiagonal", "459/4"),
    ("projector_spike", "8"),
    ("projector_background", "2"),
    ("projector_cross_term", "-32"),
    ("projector_energy", "36"),
    ("proper_factor_test_x", 100),
    ("proper_factor_test_cases", 50),
    ("proper_factor_prime_rows", 10),
    ("beta84_log_vector", ((2, 2), (3, 1), (7, 1))),
    ("zero_axis_row_energy", 0),
    ("zero_axis_atom", 37),
    ("selected_route", SELECTED_ROUTE),
    ("source_boundary", "NO_LITERAL_MOBIUS_PRIME_DIRECTIONAL_DISPERSION_THEOREM"),
    ("first_fatal", FIRST_FATAL),
)


REGISTRY_ITEMS = (
    ("V42_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V42_ROUTE_ADVANCE", "YES"),
    ("V42_CONDITIONAL_BRIDGE_ADVANCE", "YES"),
    ("V42_ARITHMETIC_ADVANCE", "NO"),
    ("V42_FIXED_ATOM_CREDIT", "0"),
    ("V42_STRICT_1_OVER_400", "UNPAID"),
    ("V42_L2", "NONE"),
    ("V42_TPC_207_TRIGGER", "false"),
    ("V42_NUMBERED_RELEASE", "NO"),
    ("V42_DERIVATION_STATUS", "COHERENT_AFTER_EXACT_PROPER_FACTOR_LIFT_OCCURRENCE_DIAGONAL_DYADIC_REASSEMBLY_DIRECTIONAL_AND_ZERO_AXIS_FIREWALLS"),
    ("V42_ASSUMPTION_POLICY", "CELLWISE_PHYSICAL_MOBIUS_PRIME_DIRECTIONAL_DISPERSION_REMAINS_EXPLICIT_OPEN_THEOREM"),
    ("V42_SELECTED_RESEARCH_ROUTE", SELECTED_ROUTE),
    ("V42_V41_QLOCAL_SPLIT", "RETAINED_EXACT_MODEL_PAID_RESIDUAL_OPEN"),
    ("V42_V35_PROPER_FACTOR_IDENTITY", "RETAINED_EXACT_BETA_EQUALS_SUM_MU_TIMES_OMEGA"),
    ("V42_PROPER_FACTOR_SUPPORT", "PROVED_EXACT_D_AND_K_AT_LEAST_2"),
    ("V42_PRIME_ROW_CANCELLATION", "PROVED_EXACT_EMPTY_PROPER_FACTOR_SUM"),
    ("V42_RESIDUAL_PROPER_FACTOR_LIFT", "PROVED_EXACT_BEFORE_ANY_OUTER_ABSOLUTE"),
    ("V42_PROPER_FACTOR_OCCURRENCE_DIAGONAL", "PROVED_X_POWER_95_OVER_48"),
    ("V42_COLLAPSED_TO_OCCURRENCE_DIAGONAL", "PROVED_WITH_DIVISOR_X_O1_LOSS"),
    ("V42_RESIDUAL_GRAM_IDENTITY", "PROVED_EXACT_E_RES_EQUALS_D_RES_PLUS_REAL_SIGNED_O_RES"),
    ("V42_PRIMARY_POSITIVE_GRAM_GATE", "OPEN_CONJECTURE_POSITIVE_O_RES_LE_X_POWER_37_OVER_16"),
    ("V42_SPIKE_BACKGROUND_ENERGY", "PROVED_EXACT_WITH_SIGNED_CROSS_TERM_RETAINED"),
    ("V42_DYADIC_D_CELLS", "PROVED_EXACT_DISJOINT_O_LOG_X_PARTITION"),
    ("V42_DYADIC_RESIDUAL_REASSEMBLY", "PROVED_EXACT_RHO_EQUALS_SUM_J_RHO_J"),
    ("V42_CELLWISE_MOBIUS_PRIME_DIRECTIONAL_GATE", "OPEN_CONJECTURE_E_J_LE_Q_X_O1_D_J"),
    ("V42_CELLWISE_DIRECTIONAL_LOSS", "Q_EQUALS_X_POWER_1_OVER_3"),
    ("V42_CELLWISE_TO_GLOBAL_COMPILER", "PROVED_BY_L2_TRIANGLE_AND_CELL_CAUCHY"),
    ("V42_CONDITIONAL_RESIDUAL_ENERGY", "X_POWER_37_OVER_16"),
    ("V42_CONDITIONAL_RESIDUAL_DUAL_NORM", "X_POWER_37_OVER_32"),
    ("V42_CONDITIONAL_SCALAR_OUTPUT", "X_POWER_53_OVER_32"),
    ("V42_CONDITIONAL_ENDPOINT_MARGIN", "19_OVER_2400"),
    ("V42_CONDITIONAL_KAPPA", "1_OVER_48"),
    ("V42_CELLWISE_L2_DUAL", "PROVED_ONE_OUTER_ABSOLUTE_MODULUS_FAMILY"),
    ("V42_OMEGA_TWO_BRANCH_FORM", "PROVED_EXACT_MU_LOG_D_OR_MU_LOG_K_OVER_LOG_DK"),
    ("V42_LOG_DENOMINATOR_ABEL_COMPILER", "PROVED_EXACT_UNIFORM_PRODUCT_CUTOFF_INTERFACE"),
    ("V42_OPERATOR_MATRIX_IDENTITY", "PROVED_E_RES_EQUALS_NORM_A_ONE_ACTIVE_SQUARED_AND_D_RES_EQUALS_HS_SQUARED"),
    ("V42_STABLE_RANK_CEILING", "PROVED_AT_MOST_NUMBER_OF_Q_ROWS_X_POWER_1_OVER_3"),
    ("V42_OPERATOR_ONLY_CERTIFICATE_LOSS_FLOOR", "N_ACTIVE_OVER_X_POWER_1_OVER_3"),
    ("V42_OPERATOR_ONLY_THRESHOLD_SUPPORT_CEILING", "X_POWER_273_OVER_400"),
    ("V42_OPERATOR_ONLY_FULL_ACTIVE_LOSS", "X_POWER_2_OVER_3"),
    ("V42_OPERATOR_ONLY_ENDPOINT_EXCESS", "127_OVER_400"),
    ("V42_MAXIMAL_STABLE_RANK_FIXTURE", "PROVED_2_BY_8_HADAMARD_ROWS_RATIO_4"),
    ("V42_GENERIC_CENTERED_KERNEL_Q_LOSS", "STOP_SCOPED_Q5_M3_COUNTEREXAMPLE_RATIO_75_OVER_7"),
    ("V42_COEFFICIENT_BLIND_ROW_BESSEL", "STOP_SCOPED_PHYSICAL_DIRECTION_REQUIRED"),
    ("V42_SPLIT_BETA_CHANNELS_BEFORE_OUTER_ABSOLUTE", "STOP_SCOPED_PRIME_ROW_EXACT_CANCELLATION_DESTROYED"),
    ("V42_OFFZERO_DIRECTIONAL_GATE_TO_ZERO_AXIS", "STOP_SCOPED_DELTA_ZERO_FIREWALL_RETAINED"),
    ("V42_TERMINAL_QLOCAL_GATE_A", "OPEN_INDEPENDENT_SIGNED_COVARIANCE"),
    ("V42_MRT_DIRECT_ATTACHMENT", "STOP_SCOPED_SOURCE_COEFFICIENTS_AND_Q_DEPENDENT_RESIDUAL_MISMATCH"),
    ("V42_HARPER_BDH_DIRECT_ATTACHMENT", "STOP_SCOPED_ONE_FIXED_SEQUENCE_AND_MODULUS_HYPOTHESES_MISMATCH"),
    ("V42_BAZIN_DIRECT_ATTACHMENT", "STOP_SCOPED_ONE_SIDED_BETA_MARGINAL_NOT_JOINT_ROW_SQUARE"),
    ("V42_RUNBO_LI_DIRECT_ATTACHMENT", "STOP_SCOPED_FACTORED_MODULUS_PRIME_DISTRIBUTION_NOT_PROPER_FACTOR_RESIDUAL_DIRECTION"),
    ("V42_BLOMER_PASCADI_BALANCED_CELL", "SOURCE_BACKED_LOCAL_ENGINE_Q_MINUS_1_OVER_32_AFTER_V38_EXACT_EMITTER"),
    ("V42_LOCAL_KLOOSTERMAN_ENGINE_TO_MPD", "STOP_SCOPED_BLOCK_ATOMIC_BUDGET_AND_Q_L2_REASSEMBLY_UNPAID"),
    ("V42_MILICEVIC_QIN_WU_DIRECT_ATTACHMENT", "STOP_SCOPED_POST_TRANSFORM_FIXED_MODULUS_KLOOSTERMAN_ARRAYS_ONLY"),
    ("V42_DIRECT_PRIMARY_SOURCE_FOR_MPD_CELL_GATE", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10"),
    ("V42_FIRST_FATAL", FIRST_FATAL),
    ("V42_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_QLOCAL_MODEL_PIER_PAID_PROPER_FACTOR_DIRECTIONAL_SPAN_OPEN"),
    ("V42_SOURCE_LOCK_POLICY", "PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED"),
    ("V42_ROUTE_MAP_REFERENCE", "TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B"),
)


EXPECTED_REGISTRY_SHA256 = "d1d3ec9094a2df4d96dc315fa332b45b6a955ce464e860bc40485efa9d66d4d7"


SOURCE_ITEMS = (
    ("MRT_SHIFT_ENERGY", "arXiv:1707.01315v3_Theorem_1.3_and_Proposition_3.1"),
    ("HARPER_GENERAL_BDH", "arXiv:2412.19644v1_Theorems_1_2"),
    ("BAZIN_TYPE_I_II", "arXiv:2607.15137v1_Theorem_8"),
    ("RUNBO_LI_FACTORED_MODULI", "arXiv:2602.20917v6_Theorem_1.1"),
    ("BLOMER_PASCADI_BALANCED_CELL", "arXiv:2607.24311v1_Theorem_1.1"),
    ("MILICEVIC_QIN_WU_KLOOSTERMAN", "arXiv:2511.07550v1_Theorem_1.1"),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_qlocal_residual_row_bessel_compiler.md",
        "43a1a49be7faea2ef5220c3f4b797f35e155b594a68dfd5166c66f5367096934",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_qlocal_residual_row_bessel_checker.py",
        "af1aa709d6aaef6d0b8c8d686e75267833c95c917d599b6d5f88830e05e9a193",
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
    sorted_fn=sorted,
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
    if registry_map.get("V42_MAXIMUM_CLAIM") != literal_maximum_claim:
        raise failure_type("maximum claim registry seed changed")
    if contract_map.get("selected_route") != literal_selected_route:
        raise failure_type("selected route contract seed changed")
    if registry_map.get("V42_SELECTED_RESEARCH_ROUTE") != literal_selected_route:
        raise failure_type("selected route registry seed changed")
    if contract_map.get("first_fatal") != literal_first_fatal:
        raise failure_type("first fatal contract seed changed")
    if registry_map.get("V42_FIRST_FATAL") != literal_first_fatal:
        raise failure_type("first fatal registry seed changed")
    if registry_digest(literal_registry) != literal_registry_digest:
        raise failure_type("registry literal digest changed")

    def factorization(n: int) -> tuple[tuple[int, int], ...]:
        rows = []
        p = 2
        remaining = n
        while p * p <= remaining:
            if remaining % p == 0:
                exponent = 0
                while remaining % p == 0:
                    remaining //= p
                    exponent += 1
                rows.append((p, exponent))
            p += 1
        if remaining > 1:
            rows.append((remaining, 1))
        return tuple_type(rows)

    def divisors(n: int) -> tuple[int, ...]:
        values = [1]
        for p, exponent in factorization(n):
            old = tuple_type(values)
            power = 1
            for _ in range_fn(exponent):
                power *= p
                values.extend(value * power for value in old)
        return tuple_type(sorted_fn(values))

    def mobius(n: int) -> int:
        factors = factorization(n)
        if not all_fn(exponent == 1 for _, exponent in factors):
            return 0
        return -1 if len_fn(factors) % 2 else 1

    def log_vector(n: int) -> tuple[tuple[int, int], ...]:
        return factorization(n)

    def vector_add(
        left: tuple[tuple[int, int], ...],
        right: tuple[tuple[int, int], ...],
    ) -> tuple[tuple[int, int], ...]:
        result = dict_type(left)
        for prime, coefficient in right:
            result[prime] = result.get(prime, 0) + coefficient
            if result[prime] == 0:
                del result[prime]
        return tuple_type(sorted_fn(result.items()))

    def vector_scale(
        vector: tuple[tuple[int, int], ...], scalar: int
    ) -> tuple[tuple[int, int], ...]:
        return tuple_type((prime, scalar * coefficient) for prime, coefficient in vector if scalar * coefficient)

    def lambda_vector(n: int) -> tuple[tuple[int, int], ...]:
        factors = factorization(n)
        if len_fn(factors) == 1:
            return ((factors[0][0], 1),)
        return ()

    def beta_numerator(x: int, t: int) -> tuple[tuple[int, int], ...]:
        cutoff_mu = sum_fn(
            (
                mobius(d)
                for d in divisors(t)
                if d ** 400 <= x ** 133
            ),
            0,
        )
        return vector_add(lambda_vector(t), vector_scale(log_vector(t), -cutoff_mu))

    def proper_terms(
        x: int, t: int
    ) -> tuple[tuple[int, tuple[tuple[int, int], ...]], ...]:
        rows = []
        for d in divisors(t):
            k = t // d
            mu = mobius(d)
            if d < 2 or k < 2 or mu == 0:
                continue
            numerator = (
                vector_scale(log_vector(d), -mu)
                if d ** 400 <= x ** 133
                else vector_scale(log_vector(k), mu)
            )
            rows.append((d, numerator))
        return tuple_type(rows)

    def proper_numerator(x: int, t: int) -> tuple[tuple[int, int], ...]:
        total: tuple[tuple[int, int], ...] = ()
        for _, numerator in proper_terms(x, t):
            total = vector_add(total, numerator)
        return total

    def compute_base() -> tuple[tuple[str, object], ...]:
        x = 100
        shell = tuple_type(range_fn(51, 101))
        identity_cases = 0
        prime_rows = 0
        occurrence_count = 0
        dyadic_reassembly_cases = 0
        for t in shell:
            beta_vector = beta_numerator(x, t)
            proper_vector = proper_numerator(x, t)
            if beta_vector != proper_vector:
                raise failure_type("proper-factor identity changed at " + str_type(t))
            identity_cases += 1
            terms = proper_terms(x, t)
            occurrence_count += len_fn(terms)
            cell_totals: dict[int, tuple[tuple[int, int], ...]] = {}
            for d, numerator in terms:
                cell = d.bit_length() - 1
                cell_totals[cell] = vector_add(cell_totals.get(cell, ()), numerator)
            reassembled: tuple[tuple[int, int], ...] = ()
            for cell in sorted_fn(cell_totals):
                reassembled = vector_add(reassembled, cell_totals[cell])
            if reassembled != proper_vector:
                raise failure_type("dyadic cell reassembly changed at " + str_type(t))
            dyadic_reassembly_cases += 1
            factors = factorization(t)
            if len_fn(factors) == 1 and factors[0][1] == 1:
                prime_rows += 1
                if beta_vector != () or terms != ():
                    raise failure_type("prime cancellation changed")
        beta84 = beta_numerator(x, 84)
        if (identity_cases, prime_rows, beta84) != (
            50,
            10,
            ((2, 2), (3, 1), (7, 1)),
        ):
            raise failure_type("proper-factor finite ledger changed")

        matrix_rows = (
            (1, 1, 1, 1, 1, 1, 1, 1),
            (1, -1, 1, -1, 1, -1, 1, -1),
        )
        matrix_hs = sum_fn((value * value for row in matrix_rows for value in row), 0)
        matrix_energy = sum_fn((sum_fn(row, 0) ** 2 for row in matrix_rows), 0)
        matrix_inner = sum_fn((matrix_rows[0][i] * matrix_rows[1][i] for i in range_fn(8)), 0)
        matrix_op_squared = 8
        matrix_stable_rank = fraction_type(matrix_hs, matrix_op_squared)
        matrix_ratio = fraction_type(matrix_energy, matrix_hs)
        if (
            matrix_hs,
            matrix_energy,
            matrix_inner,
            matrix_stable_rank,
            matrix_ratio,
        ) != (16, 64, 0, fraction_type(2), fraction_type(4)):
            raise failure_type("maximal stable-rank fixture changed")

        q = 5
        copies = 3
        g_values = {
            1: fraction_type(3 * (copies - 1), 4),
            2: -fraction_type(copies, 4),
            3: -fraction_type(copies, 4),
            4: -fraction_type(copies, 4),
        }
        q5_row = sum_fn((copies * abs_fn(value) for value in g_values.values()), fraction_type(0))
        q5_diagonal = sum_fn((copies * value * value for value in g_values.values()), fraction_type(0))
        q5_energy = q5_row * q5_row
        q5_ratio = q5_energy / q5_diagonal
        q5_offdiagonal = q5_energy - q5_diagonal
        if (q5_row, q5_diagonal, q5_energy, q5_ratio, q5_offdiagonal) != (
            fraction_type(45, 4),
            fraction_type(189, 16),
            fraction_type(2025, 16),
            fraction_type(75, 7),
            fraction_type(459, 4),
        ) or not q5_energy > q * q5_diagonal:
            raise failure_type("generic centered-kernel counterexample changed")

        projector_columns = 6
        projector_residual = fraction_type(4, 3)
        projector_spike = projector_columns * projector_residual
        projector_background = projector_spike / (q - 1)
        projector_rho = projector_spike - projector_background
        projector_diagonal = projector_columns
        projector_cross = -2 * projector_spike * projector_background
        projector_energy = (
            projector_spike * projector_spike
            + projector_background * projector_background
            + projector_cross
        )
        if (
            projector_spike,
            projector_background,
            projector_rho,
            projector_diagonal,
            projector_cross,
            projector_energy,
        ) != (
            fraction_type(8),
            fraction_type(2),
            fraction_type(6),
            fraction_type(6),
            fraction_type(-32),
            fraction_type(36),
        ):
            raise failure_type("spike-background cross-term fixture changed")

        H = fraction_type(21, 32)
        Q = fraction_type(1, 3)
        endpoint = fraction_type(1997, 1200)
        occurrence_diagonal = fraction_type(1) + 2 * H - Q
        conditional_energy = occurrence_diagonal + Q
        conditional_dual = conditional_energy / 2
        conditional_output = 3 * Q / 2 + conditional_dual
        endpoint_margin = endpoint - conditional_output
        conditional_kappa = fraction_type(7, 3) - conditional_energy
        tau_threshold = fraction_type(419, 1200)
        operator_floor = fraction_type(1) - Q
        operator_support_ceiling = Q + tau_threshold
        operator_excess = operator_floor - tau_threshold
        if (
            occurrence_diagonal,
            conditional_energy,
            conditional_dual,
            conditional_output,
            endpoint_margin,
            conditional_kappa,
            operator_floor,
            operator_support_ceiling,
            operator_excess,
        ) != (
            fraction_type(95, 48),
            fraction_type(37, 16),
            fraction_type(37, 32),
            fraction_type(53, 32),
            fraction_type(19, 2400),
            fraction_type(1, 48),
            fraction_type(2, 3),
            fraction_type(273, 400),
            fraction_type(127, 400),
        ):
            raise failure_type("V42 exponent ledger changed")
        if not (Q < tau_threshold < operator_floor and conditional_output < endpoint):
            raise failure_type("strict endpoint ordering changed")

        zero_axis_atom = 37
        zero_axis_rows = tuple_type(0 for _ in (5, 7, 11))
        zero_axis_energy = sum_fn((value * value for value in zero_axis_rows), 0)
        if (zero_axis_energy, zero_axis_atom) != (0, 37):
            raise failure_type("zero-axis firewall changed")

        route_truth = tuple_type(
            (model_paid, mpd_paid, terminal_paid, model_paid and mpd_paid and terminal_paid)
            for model_paid in (False, True)
            for mpd_paid in (False, True)
            for terminal_paid in (False, True)
        )
        if sum_fn((int_type(row[-1]) for row in route_truth), 0) != 1:
            raise failure_type("conditional route truth table changed")

        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("conditional_bridge_advance", "YES"),
            ("proper_factor_test_x", x),
            ("proper_factor_test_cases", identity_cases),
            ("proper_factor_prime_rows", prime_rows),
            ("proper_factor_occurrences", occurrence_count),
            ("dyadic_reassembly_cases", dyadic_reassembly_cases),
            ("beta84_log_vector", beta84),
            ("matrix_shape", (2, 8)),
            ("matrix_hs", matrix_hs),
            ("matrix_energy", matrix_energy),
            ("matrix_stable_rank", str_type(matrix_stable_rank)),
            ("matrix_ratio", str_type(matrix_ratio)),
            ("q5_M", copies),
            ("q5_row", str_type(q5_row)),
            ("q5_diagonal", str_type(q5_diagonal)),
            ("q5_energy", str_type(q5_energy)),
            ("q5_ratio", str_type(q5_ratio)),
            ("q5_offdiagonal", str_type(q5_offdiagonal)),
            ("projector_spike", str_type(projector_spike)),
            ("projector_background", str_type(projector_background)),
            ("projector_rho", str_type(projector_rho)),
            ("projector_diagonal", str_type(projector_diagonal)),
            ("projector_cross_term", str_type(projector_cross)),
            ("projector_energy", str_type(projector_energy)),
            ("occurrence_diagonal_exponent", str_type(occurrence_diagonal)),
            ("conditional_energy_exponent", str_type(conditional_energy)),
            ("conditional_dual_exponent", str_type(conditional_dual)),
            ("conditional_output_exponent", str_type(conditional_output)),
            ("conditional_endpoint_margin", str_type(endpoint_margin)),
            ("conditional_kappa", str_type(conditional_kappa)),
            ("tau_threshold", str_type(tau_threshold)),
            ("operator_full_active_floor", str_type(operator_floor)),
            ("operator_support_ceiling", str_type(operator_support_ceiling)),
            ("operator_endpoint_excess", str_type(operator_excess)),
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
                must_reject(prefix + "_subclass", lambda: validator(tuple_type(rows), literal_registry_digest)
                )
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
