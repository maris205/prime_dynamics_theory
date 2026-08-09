#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V38 canonical packet emitter."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_CANONICAL_FOURIER_KLOOSTERMAN_BALANCED_BLOCK_SVD_EMITTER_PLUS_"
    "OPEN_PHYSICAL_SCHATTEN_AGGREGATE_AND_SOURCE_BACKED_BP_CELL_ENGINE"
)


CONTRACT_ITEMS = (
    ("schema_version", "V38_CANONICAL_PACKET_SCHATTEN_V1"),
    ("artifact_name", "bridge_b_canonical_packet_schatten_emitter.md"),
    ("baseline_commit", "c89d3a0fc5201cba2ef27e37cf388ad763c4d59b"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("route_position", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_K_LANE_CANONICAL_EMITTER_BUILT_ATOMIC_PIER_OPEN"),
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
    ("matrix_normalization", "q^(-2)"),
    ("zero_axis_factor", "(q^2-q+1)/q^2"),
    ("balanced_block_length", "asymptotic_sqrt(q)"),
    ("cell_trivial_scale", "q^2/lambda_q*singular_value"),
    ("canonical_atomic_gate", "sum_q A_q<=x^(5/3+o(1))*Q^omega"),
    ("packet_overhead", "omega<19/800"),
    ("bp_cell_gain", "Q^(-1/32)"),
    ("conditional_output", "x^(53/32+omega/3+o(1))"),
    ("sample_omega", "1/100"),
    ("generic_atomic_l2", "q^(7/4)*||d_q||_2"),
    ("aggregate_energy_factor", "Q^(9/4)"),
    ("energy_overpay", "x^(7/96)"),
    ("fixture_q", 5),
    ("fixture_sum_d", 7),
    ("first_fatal", "NO_LITERAL_THEOREM_BOUNDS_THE_CANONICAL_PHYSICAL_BLOCK_SCHATTEN_AGGREGATE_WITH_OMEGA_LESS_THAN_19_OVER_800"),
)


REGISTRY_ITEMS = (
    ("V38_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V38_ROUTE_ADVANCE", "YES"),
    ("V38_CONDITIONAL_BRIDGE_ADVANCE", "YES"),
    ("V38_ARITHMETIC_ADVANCE", "NO"),
    ("V38_FIXED_ATOM_CREDIT", "0"),
    ("V38_STRICT_1_OVER_400", "UNPAID"),
    ("V38_L2", "NONE"),
    ("V38_TPC_207_TRIGGER", "false"),
    ("V38_NUMBERED_RELEASE", "NO"),
    ("V38_DERIVATION_STATUS", "COHERENT_AFTER_EXACT_SCALAR_RECOLLAPSE_DOUBLE_ORTHOGONALITY_ZERO_AXIS_REMOVAL_AND_BLOCK_SVD"),
    ("V38_ASSUMPTION_POLICY", "ONLY_CANONICAL_PHYSICAL_SCHATTEN_AGGREGATE_IS_OPEN_AND_NEVER_PROMOTED"),
    ("V38_SELECTED_RESEARCH_ROUTE", "K_CANONICAL_SCHATTEN_AGGREGATE_FIRST__E_SECOND__X_THIRD__A_TERMINAL_AFTER_B__C_RESERVE"),
    ("V38_V37_CENTERED_PACKET", "RETAINED_EXACT_WITH_FULL_BACKGROUND_AND_DELETED_DIAGONAL"),
    ("V38_PHYSICAL_RESIDUE_VECTOR", "PROVED_EXACT_FINAL_SCALAR_REGROUPING"),
    ("V38_CANONICAL_FOURIER_KLOOSTERMAN_MATRIX", "PROVED_EXACT_DOUBLE_ADDITIVE_ORTHOGONALITY"),
    ("V38_ZERO_AXIS_SELF_RETURN", "PROVED_EXACT_LAMBDA_Q_FACTOR"),
    ("V38_ZERO_AXIS_FACTOR", "LAMBDA_Q_EQUALS_Q_SQUARED_MINUS_Q_PLUS_ONE_OVER_Q_SQUARED"),
    ("V38_PRIME_COPRIMALITY_AFTER_ZERO_REMOVAL", "PROVED_EXACT_ONLY_ZERO_ZERO_EXCLUDED"),
    ("V38_BALANCED_FREQUENCY_PARTITION", "PROVED_EXACT_CONSECUTIVE_BLOCKS_OF_LENGTH_ASYMPTOTIC_SQRT_Q"),
    ("V38_BLOCK_SVD", "PROVED_EXACT_RANK_ONE_BP_ARRAY_DECOMPOSITION"),
    ("V38_CANONICAL_SCALAR_EMITTER", "PROVED_EXACT_ZERO_REMAINDER"),
    ("V38_EXACTLY_ONCE_POLICY", "FINAL_PHYSICAL_SCALAR_AND_EVERY_MATRIX_ENTRY_EXACTLY_ONCE"),
    ("V38_TEMPLATE_LABEL_RELAXATION", "VALID_ONLY_AFTER_V35_V36_FINAL_SCALAR_RECOLLAPSE_NOT_FOR_LOCAL_CARRIER"),
    ("V38_CELL_TRIVIAL_SCALE", "Q_SQUARED_OVER_LAMBDA_Q_TIMES_SINGULAR_VALUE"),
    ("V38_CANONICAL_ATOMIC_BUDGET", "Q_SQUARED_OVER_LAMBDA_Q_TIMES_SUM_BLOCK_SCHATTEN_ONE"),
    ("V38_CANONICAL_SCHATTEN_GATE", "OPEN_CONJECTURE_AGGREGATE_X_POWER_5_OVER_3_TIMES_Q_POWER_OMEGA"),
    ("V38_PACKET_OVERHEAD_THRESHOLD", "OMEGA_STRICTLY_LESS_THAN_19_OVER_800"),
    ("V38_BLOMER_PASCADI_CELL_ENGINE", "SOURCE_BACKED_Q_POWER_MINUS_1_OVER_32_AFTER_EXACT_EMISSION"),
    ("V38_CONDITIONAL_OUTPUT", "X_POWER_53_OVER_32_PLUS_OMEGA_OVER_3"),
    ("V38_CONDITIONAL_ENDPOINT_MARGIN", "19_OVER_2400_MINUS_OMEGA_OVER_3"),
    ("V38_SAMPLE_OMEGA", "1_OVER_100"),
    ("V38_SAMPLE_OUTPUT", "3983_OVER_2400"),
    ("V38_SAMPLE_ENDPOINT_MARGIN", "11_OVER_2400"),
    ("V38_FULL_MATRIX_SINGULAR_VALUES", "PROVED_EXACT_ABS_D_R_OVER_Q"),
    ("V38_FULL_MATRIX_FROBENIUS", "PROVED_EXACT_Q_INVERSE_TIMES_D_L2"),
    ("V38_GENERIC_BLOCK_SCHATTEN_BASELINE", "Q_POWER_MINUS_1_OVER_4_TIMES_D_L2"),
    ("V38_GENERIC_ATOMIC_L2_BASELINE", "Q_POWER_7_OVER_4_TIMES_D_L2"),
    ("V38_GENERIC_ATOMIC_L1_BASELINE", "Q_POWER_3_OVER_2_TIMES_D_L1"),
    ("V38_PACKET_ENERGY_TO_ATOMIC", "PROVED_Q_POWER_9_OVER_4_TIMES_ENERGY_SQUARE_ROOT"),
    ("V38_PACKET_ENERGY_REQUIRED_BY_GENERIC_ATOMIC_ROUTE", "X_POWER_11_OVER_6_PLUS_2_OMEGA_OVER_3"),
    ("V38_SAMPLE_PACKET_ENERGY_EXPONENT", "46_OVER_25"),
    ("V38_DIRECT_PACKET_ENERGY_CAUCHY", "PROVED_Q_SQUARED_TIMES_ENERGY_SQUARE_ROOT"),
    ("V38_DIRECT_PACKET_ENERGY_OUTPUT", "X_POWER_19_OVER_12_PLUS_OMEGA_OVER_3"),
    ("V38_PACKET_ENERGY_VIA_BP", "STOP_SCOPED_GENERIC_BLOCK_LOSS_Q_1_OVER_4_EXCEEDS_BP_GAIN_Q_1_OVER_32"),
    ("V38_PACKET_ENERGY_BP_OVERPAY", "X_POWER_7_OVER_96"),
    ("V38_HARPER_GENERAL_BDH_DIRECT_ATTACHMENT", "STOP_SCOPED_ONE_Q_INDEPENDENT_SEQUENCE_Q_RANGE_AND_DISTRIBUTION_HYPOTHESES_MISMATCH"),
    ("V38_LEWKO_VARIATIONAL_BDH_DIRECT_ATTACHMENT", "STOP_SCOPED_PRIME_COUNTING_ONE_SEQUENCE_WRONG_PACKET_AND_NORM"),
    ("V38_HIEU_SHORT_INTERVAL_BDH_DIRECT_ATTACHMENT", "STOP_SCOPED_SINGLE_LAMBDA_SEQUENCE_NO_BETA_CENTERED_INVERSE_BLOCK"),
    ("V38_DIRECT_PRIMARY_SOURCE_FOR_CANONICAL_SCHATTEN_GATE", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09"),
    ("V38_ROUTE_E", "RETAINED_OPEN_WHOLE_RESIDUAL_SIGMA_LT_13_OVER_4800"),
    ("V38_ROUTE_X", "RETAINED_OPEN_JOINT_CHARACTER_KAPPA_GT_403_OVER_1200"),
    ("V38_TERMINAL_A", "OPEN_TERMINAL_EQUIVALENT_SIGNED_QLOCAL_COVARIANCE_AFTER_B"),
    ("V38_DYNAMICS_C", "RESERVE_DISTINGUISHED_SEED_ATTACHMENT_STILL_OPEN"),
    ("V38_NEXT_THEOREM", "DIRECT_LITERAL_CANONICAL_BLOCK_SCHATTEN_AGGREGATE_WITH_OMEGA_1_OVER_100_BENCHMARK"),
    ("V38_FIRST_FATAL", "NO_LITERAL_THEOREM_BOUNDS_THE_CANONICAL_PHYSICAL_BLOCK_SCHATTEN_AGGREGATE_WITH_OMEGA_LESS_THAN_19_OVER_800"),
    ("V38_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_K_LANE_CANONICAL_EMITTER_BUILT_ATOMIC_PIER_OPEN"),
    ("V38_SOURCE_LOCK_POLICY", "PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED"),
    ("V38_ROUTE_MAP_REFERENCE", "TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B"),
)


EXPECTED_REGISTRY_SHA256 = "44bc40fc8971dc4a0b3d941719feb89cc3ce3580178a2c4ad1c5bdab9a59c574"


SOURCE_ITEMS = (
    ("BLOMER_PASCADI_CRITICAL_CELL", "arXiv:2607.24311v1_Theorem_1.1"),
    ("HARPER_GENERAL_BDH", "arXiv:2412.19644v1_Theorems_1_2"),
    ("LEWKO_VARIATIONAL_BDH", "arXiv:1111.6190v2_Theorems_1_4"),
    ("HIEU_SHORT_INTERVAL_BDH", "arXiv:2509.04883v2_Appendix_A"),
)


DEPENDENCIES = (
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
    max_fn=max,
    sorted_fn=sorted,
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
    if dict_type(literal_registry).get("V38_MAXIMUM_CLAIM") != literal_maximum_claim:
        raise failure_type("maximum claim registry seed changed")
    if registry_digest(literal_registry) != literal_registry_digest:
        raise failure_type("registry literal digest changed")

    def compute_base() -> tuple[tuple[str, object], ...]:
        q = 5
        units = tuple_type(range_fn(1, q))
        d = (3, -2, 5, 1)
        sum_d = sum_fn(d, 0)
        d_l1 = sum_fn((abs_fn(value) for value in d), 0)
        d_l2_sq = sum_fn((value * value for value in d), 0)
        if (units, sum_d, d_l1, d_l2_sq) != ((1, 2, 3, 4), 7, 11, 39):
            raise failure_type("physical residue fixture changed")

        def inverse(value: int) -> int:
            for candidate in range_fn(1, q):
                if (value * candidate) % q == 1:
                    return candidate
            raise failure_type("inverse missing")

        full_numerator = 0
        wrong_inverse_numerator = 0
        for r_index, r in enumerate_fn(units):
            for x in units:
                m_sum = q if x == r else 0
                n_sum = q if inverse(x) == inverse(r) else 0
                wrong_n_sum = q if inverse(x) == r else 0
                full_numerator += d[r_index] * m_sum * n_sum
                wrong_inverse_numerator += d[r_index] * m_sum * wrong_n_sum
        full_emission = fraction_type(full_numerator, q * q)
        wrong_normalization = fraction_type(full_numerator, q)
        wrong_inverse = fraction_type(wrong_inverse_numerator, q * q)
        if (full_emission, wrong_normalization, wrong_inverse) != (
            fraction_type(7),
            fraction_type(35),
            fraction_type(4),
        ):
            raise failure_type("double orthogonality fixture changed")

        matrix_zero = fraction_type(sum_d, q * q)
        kloosterman_zero = q - 1
        zero_contribution = matrix_zero * kloosterman_zero
        lambda_q = fraction_type(q * q - q + 1, q * q)
        off_axis = full_emission - zero_contribution
        recovered = off_axis / lambda_q
        if (
            matrix_zero,
            zero_contribution,
            lambda_q,
            off_axis,
            recovered,
        ) != (
            fraction_type(7, 25),
            fraction_type(28, 25),
            fraction_type(21, 25),
            fraction_type(147, 25),
            fraction_type(7),
        ):
            raise failure_type("zero-axis fixture changed")

        block_count = 2
        quotient, remainder = divmod(q, block_count)
        block_sizes = tuple_type(
            quotient + int_type(index < remainder) for index in range_fn(block_count)
        )
        starts = []
        cursor = 0
        for size in block_sizes:
            starts.append(tuple_type(range_fn(cursor, cursor + size)))
            cursor += size
        blocks = tuple_type(starts)
        flattened = tuple_type(value for block in blocks for value in block)
        matrix_entries = tuple_type((m, n) for m in range_fn(q) for n in range_fn(q))
        block_entries = tuple_type(
            (m, n) for left in blocks for right in blocks for m in left for n in right
        )
        admissible_entries = tuple_type(pair for pair in matrix_entries if pair != (0, 0))
        if (
            block_sizes,
            flattened,
            tuple_type(sorted_fn(block_entries)),
            len_fn(set_type(block_entries)),
            len_fn(admissible_entries),
        ) != (
            (3, 2),
            (0, 1, 2, 3, 4),
            matrix_entries,
            25,
            24,
        ):
            raise failure_type("balanced block partition changed")

        frobenius_sq = fraction_type(d_l2_sq, q * q)
        if frobenius_sq != fraction_type(39, 25):
            raise failure_type("Frobenius fixture changed")

        sqrt_rank_exponent = fraction_type(1, 4)
        block_pair_count_exponent = fraction_type(1)
        block_cauchy_exponent = block_pair_count_exponent / 2
        matrix_frobenius_exponent = fraction_type(-1)
        block_schatten_exponent = (
            sqrt_rank_exponent + block_cauchy_exponent + matrix_frobenius_exponent
        )
        atomic_l2_exponent = block_schatten_exponent + 2
        aggregate_energy_exponent = (
            2 * atomic_l2_exponent + 1
        ) / 2
        atomic_l1_exponent = fraction_type(3, 2)
        if (
            block_schatten_exponent,
            atomic_l2_exponent,
            aggregate_energy_exponent,
            atomic_l1_exponent,
        ) != (
            fraction_type(-1, 4),
            fraction_type(7, 4),
            fraction_type(9, 4),
            fraction_type(3, 2),
        ):
            raise failure_type("Schatten exponent ledger changed")

        endpoint = fraction_type(5, 3) - fraction_type(1, 400)
        omega_ceiling = fraction_type(19, 800)
        sample_omega = fraction_type(1, 100)
        bp_gain_q = fraction_type(1, 32)
        bp_gain_x = bp_gain_q / 3
        conditional_output = fraction_type(5, 3) + sample_omega / 3 - bp_gain_x
        conditional_margin = endpoint - conditional_output
        equality_margin = endpoint - (
            fraction_type(5, 3) + omega_ceiling / 3 - bp_gain_x
        )

        energy_required = fraction_type(11, 6) + 2 * sample_omega / 3
        energy_required_ceiling = fraction_type(11, 6) + 2 * omega_ceiling / 3
        direct_energy_output = fraction_type(2, 3) + energy_required / 2
        direct_energy_margin = endpoint - direct_energy_output
        bp_overpay = conditional_output - direct_energy_output
        if (
            conditional_output,
            conditional_margin,
            equality_margin,
            energy_required,
            energy_required_ceiling,
            direct_energy_output,
            direct_energy_margin,
            bp_overpay,
        ) != (
            fraction_type(3983, 2400),
            fraction_type(11, 2400),
            fraction_type(0),
            fraction_type(46, 25),
            fraction_type(2219, 1200),
            fraction_type(119, 75),
            fraction_type(31, 400),
            fraction_type(7, 96),
        ):
            raise failure_type("endpoint/energy firewall changed")

        compiler_truth = tuple_type(
            (emitter, atomic, cell, emitter and atomic and cell)
            for emitter in (False, True)
            for atomic in (False, True)
            for cell in (False, True)
        )
        if sum_fn((int_type(row[-1]) for row in compiler_truth), 0) != 1:
            raise failure_type("conditional compiler logic changed")

        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("conditional_bridge_advance", "YES"),
            ("fixture_q", q),
            ("fixture_d", d),
            ("sum_d", sum_d),
            ("d_l1", d_l1),
            ("d_l2_sq", d_l2_sq),
            ("full_emission", str_type(full_emission)),
            ("wrong_normalization", str_type(wrong_normalization)),
            ("wrong_inverse", str_type(wrong_inverse)),
            ("matrix_zero", str_type(matrix_zero)),
            ("zero_contribution", str_type(zero_contribution)),
            ("lambda_q", str_type(lambda_q)),
            ("off_axis", str_type(off_axis)),
            ("recovered", str_type(recovered)),
            ("block_sizes", block_sizes),
            ("block_entries", len_fn(block_entries)),
            ("admissible_entries", len_fn(admissible_entries)),
            ("frobenius_sq", str_type(frobenius_sq)),
            ("block_schatten_exponent", str_type(block_schatten_exponent)),
            ("atomic_l2_exponent", str_type(atomic_l2_exponent)),
            ("aggregate_energy_exponent", str_type(aggregate_energy_exponent)),
            ("atomic_l1_exponent", str_type(atomic_l1_exponent)),
            ("sample_omega", str_type(sample_omega)),
            ("omega_ceiling", str_type(omega_ceiling)),
            ("conditional_output", str_type(conditional_output)),
            ("conditional_margin", str_type(conditional_margin)),
            ("equality_margin", str_type(equality_margin)),
            ("energy_required", str_type(energy_required)),
            ("energy_required_ceiling", str_type(energy_required_ceiling)),
            ("direct_energy_output", str_type(direct_energy_output)),
            ("direct_energy_margin", str_type(direct_energy_margin)),
            ("bp_overpay", str_type(bp_overpay)),
            ("compiler_truth", compiler_truth),
            ("selected_route", "K_CANONICAL_SCHATTEN_AGGREGATE_FIRST__E_SECOND__X_THIRD__A_TERMINAL_AFTER_B__C_RESERVE"),
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
