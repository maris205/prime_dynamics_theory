#!/usr/bin/env python3
"""Fail-closed exact checker for the unnumbered V33 marginal compiler."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_ROOT_ONE_MASTER_MARGINAL_COLLAPSE_TO_TRUNCATED_MOBIUS_"
    "SIEVE_REMAINDER_PLUS_BAZIN_MARGINAL_INTERFACE_AND_LOCAL_CARRIER_FIREWALL"
)


CONTRACT_ITEMS = (
    ("schema_version", "V33_MASTER_MARGINAL_COLLAPSE_V1"),
    ("artifact_name", "bridge_b_master_marginal_collapse_and_joint_residual_firewall.md"),
    ("baseline_commit", "55e333b5dce3564b7786aa35db83b9b3dfec9e11"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("selected_route", "B_JOINT_RESIDUAL_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK"),
    ("route_position", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B"),
    ("route_advance", "YES"),
    ("arithmetic_advance", False),
    ("fixed_atom_credit", 0),
    ("strict_1_over_400", "UNPAID"),
    ("L2", "NONE"),
    ("TPC_207_TRIGGER", False),
    ("numbered_release", "NO"),
    ("root_scope", "ROOT_ONE_MASTER_MARGINAL_ONLY"),
    ("shell", "X_OVER_2_LT_T_LE_X_WITH_X_GE_8"),
    ("J", "133/400"),
    ("cutoff", "d^400<=x^133"),
    ("source_slots", "ORDERED_E_THEN_F_UNITS_RETAINED"),
    ("source_outer_coefficients", (2, -1)),
    ("routing", "FIRST_LARGE_THEN_FIRST_ADMISSIBLE_ORIGINAL_BITMASK"),
    ("full_root_one_numerator", "Lambda(t)"),
    ("master_identity", "Lambda(t)/log(t)-sum_cutoff_d_divides_t_mu(d)"),
    ("prime_master_value", 0),
    ("root_ge_2", "SEPARATE_PREVIOUSLY_PAID_PERFECT_POWER_REMAINDER"),
    ("finite_x_range", (8, 320)),
    ("finite_shell_cases", 25744),
    ("finite_master_occurrences", 422101),
    ("finite_h2_occurrences", 257830),
    ("wrong_sign_witness", (8, 6)),
    ("wrong_cutoff_witness", (127, 65)),
    ("local_collision", (121, 77, 5, 7, 11)),
    ("bazin_Q", "x^(21/64)"),
    ("bazin_theta", "x^(-21/32)"),
    ("bazin_tube_exponent", "149/128"),
    ("bazin_endpoint_deficit", "1549/9600"),
    ("first_fatal", "NO_JOINT_POWER_MEAN_SQUARE_WITH_OCCURRENCE_NATIVE_LOCAL_CARRIER"),
)


REGISTRY_ITEMS = (
    ("V33_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V33_ROUTE_ADVANCE", "YES"),
    ("V33_ARITHMETIC_ADVANCE", "NO"),
    ("V33_FIXED_ATOM_CREDIT", "0"),
    ("V33_STRICT_1_OVER_400", "UNPAID"),
    ("V33_L2", "NONE"),
    ("V33_TPC_207_TRIGGER", "false"),
    ("V33_NUMBERED_RELEASE", "NO"),
    ("V33_SELECTED_RESEARCH_ROUTE", "B_JOINT_RESIDUAL_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK"),
    ("V33_ROOT_ONE_SCOPE", "EXACT_MASTER_MARGINAL_ONLY"),
    ("V33_PHYSICAL_SHELL", "X_OVER_2_LT_T_LE_X_WITH_X_GE_8"),
    ("V33_EXACT_CUTOFF", "D_POWER_400_LE_X_POWER_133"),
    ("V33_CUTOFF_BELOW_SQRT_T", "PROVED_EXACT_FROM_67_OVER_400_AND_X_GE_8"),
    ("V33_HB2_FULL_ROOT_ONE_NUMERATOR", "RETAINED_SOURCE_LOCKED_LAMBDA_T"),
    ("V33_H2_J1_BRANCH", "PROVED_EXACT_2_MU_D_LOG_T_OVER_D"),
    ("V33_H2_J2_LARGE_F1_BRANCH", "PROVED_EXACT_MINUS_MU_D_LOG_T_OVER_D"),
    ("V33_H2_J2_LARGE_F2_BRANCH", "PROVED_EXACT_PLUS_MU_D_LOG_D"),
    ("V33_MU_MU_ONE_IDENTITY", "PROVED_EXACT_MU"),
    ("V33_MU_MU_LOG_IDENTITY", "PROVED_EXACT_MINUS_MU_LOG"),
    ("V33_TWO_J2_H2_BRANCHES", "PROVED_DISJOINT_ON_X_GE_8"),
    ("V33_MASTER_MARGINAL_IDENTITY", "PROVED_EXACT_LAMBDA_OVER_LOG_MINUS_TRUNCATED_MU_CONV_ONE"),
    ("V33_PRIME_MASTER_MARGINAL", "PROVED_EXACT_ZERO"),
    ("V33_ROOT_ONE_PRIME_POWER_TERM", "RETAINED_EXACT_LAMBDA_OVER_LOG"),
    ("V33_ROOT_GE_2_PERFECT_POWER_REMAINDER", "RETAINED_SEPARATE_X_1_OVER_2_PLUS_O1"),
    ("V33_FINITE_ROUTING_RECOMPUTATION", "PROVED_25744_SHELL_CASES_422101_MASTER_257830_H2"),
    ("V33_WRONG_J2_SIGN", "STOP_SCOPED_X8_T6_FORMAL_LOG_VECTOR"),
    ("V33_WRONG_CUTOFF_132", "STOP_SCOPED_X127_T65_FORMAL_LOG_VECTOR"),
    ("V33_OCCURRENCE_LOCAL_COLLISION", "PROVED_EXACT_X121_T77_Z5_GROUPS_7_AND_11"),
    ("V33_MARGINAL_TO_OCCURRENCE_LOCAL_CARRIER", "STOP_SCOPED_SELECTED_GROUP_DATA_NOT_ACCEPTED_BY_MARGINAL_THEOREM"),
    ("V33_BAZIN_BETA_MARGINAL", "SOURCE_BACKED_TYPE_I_II_XI_ATTACHMENT"),
    ("V33_BAZIN_BASE_CELL_Q", "X_POWER_21_OVER_64"),
    ("V33_BAZIN_BASE_CELL_THETA", "X_POWER_MINUS_21_OVER_32"),
    ("V33_BAZIN_XI_DOMINANT_EXPONENT", "85_OVER_64"),
    ("V33_BAZIN_ADDITIVE_TUBE_EXPONENT", "149_OVER_128"),
    ("V33_BAZIN_ENDPOINT_DEFICIT", "1549_OVER_9600"),
    ("V33_BAZIN_TO_V32_QOSC", "STOP_SCOPED_MARGINAL_WRONG_NORM_AND_H_QUARTER_LOSS"),
    ("V33_EVANS_PRIME_E2_TO_LITERAL_RESIDUAL", "STOP_SCOPED_FIXED_E2_LOG_SAVING_AND_NO_LOCAL_CARRIER"),
    ("V33_MRSTT_ALMOST_ALL_SHIFT_TO_LITERAL_RESIDUAL_L2", "STOP_SCOPED_QUALITATIVE_DENSITY_ONE_WRONG_NORM"),
    ("V33_DIRECT_PRIMARY_SOURCE_ATTACHMENT_TO_QOSC", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08"),
    ("V33_NEXT_THEOREM", "POWER_MEAN_SQUARE_FOR_COLLAPSED_SIEVE_REMAINDER_TIMES_PHYSICAL_HYBRID_WITH_OCCURRENCE_NATIVE_LOCAL_CARRIER"),
    ("V33_FIRST_FATAL", "NO_JOINT_POWER_MEAN_SQUARE_FOR_COLLAPSED_SIEVE_REMAINDER_TIMES_PHYSICAL_HYBRID_WITH_OCCURRENCE_NATIVE_LOCAL_CARRIER"),
    ("V33_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B"),
    ("V33_SOURCE_LOCK_POLICY", "PRIMARY_SOURCES_ONLY_FAIL_CLOSED"),
)


EXPECTED_REGISTRY_SHA256 = "b53790e71a636abd4b91866d46e80904ced1286b1b98c3fec1d67b0db54b74bb"


SOURCE_ITEMS = (
    ("FORD_MAYNARD_HB2", "Ford_Maynard_Lemma_5.2_printed_page_19"),
    ("BAZIN_TYPE_I_II", "arXiv:2607.15137v1_Theorem_8"),
    ("MRT_PRODUCT_ENERGY", "arXiv:1707.01315v3_Proposition_3.1_equations_52_54"),
    ("EVANS_PRIME_E2", "arXiv:2102.12297v3_Theorem_1.4"),
    ("MRSTT_ALMOST_ALL", "arXiv:2411.05770v2_Theorem_1.5"),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_shbd2_innovation.md",
        "95c4ba99be6927b38adb4b5fdda19191413720eaf3cc621e6f0d0309211e111e",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py",
        "e572bd9157ce4e733dc411ed8eb29df90d34be0ecf17023186f1648389ded519",
    ),
    (
        "research/tpc-big-road/bridge_b_base_scale_residual_oscillation_compiler.md",
        "13ec946f776008f4eadaf9a2576fa105f8500661075fe8993e04f25d3c0e6148",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_residual_oscillation_checker.py",
        "963b7ff835735252ffebfd2c9e05635c62738ab88ac59db859c31ac9f3202893",
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
    isqrt_fn=math.isqrt,
    prod_fn=math.prod,
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
    any_fn=any,
    enumerate_fn=enumerate,
):
    literal_maximum_claim = maximum_claim_seed
    literal_contract = tuple_type(contract_seed)
    literal_registry = tuple_type(registry_seed)
    literal_registry_digest = registry_digest_seed
    literal_sources = tuple_type(source_seed)
    literal_dependencies = tuple_type(dependency_seed)
    repo_root = path_type(root_seed)

    if dict_type(literal_contract).get("maximum_claim") != literal_maximum_claim:
        raise failure_type("maximum claim contract seed changed")
    if dict_type(literal_registry).get("V33_MAXIMUM_CLAIM") != literal_maximum_claim:
        raise failure_type("maximum claim registry seed changed")

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

    factor_cache: dict[int, tuple[tuple[int, int], ...]] = {}
    divisor_cache: dict[int, tuple[int, ...]] = {}
    mobius_cache: dict[int, int] = {}

    def factorization(n: int) -> tuple[tuple[int, int], ...]:
        if n in factor_cache:
            return factor_cache[n]
        value = n
        prime = 2
        factors = list_type()
        while prime * prime <= value:
            exponent = 0
            while value % prime == 0:
                value //= prime
                exponent += 1
            if exponent:
                factors.append((prime, exponent))
            prime += 1
        if value > 1:
            factors.append((value, 1))
        answer = tuple_type(factors)
        factor_cache[n] = answer
        return answer

    def divisors(n: int) -> tuple[int, ...]:
        if n in divisor_cache:
            return divisor_cache[n]
        values = [1]
        for prime, exponent in factorization(n):
            values = [
                old * prime**power
                for old in values
                for power in range_fn(exponent + 1)
            ]
        answer = tuple_type(sorted(values))
        divisor_cache[n] = answer
        return answer

    def mobius(n: int) -> int:
        if n in mobius_cache:
            return mobius_cache[n]
        factors = factorization(n)
        value = 0 if any_fn(exponent > 1 for _, exponent in factors) else (
            -1 if len_fn(factors) % 2 else 1
        )
        mobius_cache[n] = value
        return value

    def add_log_vector(target: dict[int, int], n: int, scale: int) -> None:
        for prime, exponent in factorization(n):
            target[prime] = target.get(prime, 0) + scale * exponent
            if target[prime] == 0:
                del target[prime]

    def scaled_log_vector(n: int, scale: int) -> dict[int, int]:
        answer: dict[int, int] = {}
        add_log_vector(answer, n, scale)
        return answer

    def vector_add(target: dict[int, int], source: dict[int, int]) -> None:
        for prime, value in source.items():
            target[prime] = target.get(prime, 0) + value
            if target[prime] == 0:
                del target[prime]

    def mangoldt_vector(n: int) -> dict[int, int]:
        factors = factorization(n)
        if len_fn(factors) != 1:
            return {}
        return {factors[0][0]: 1}

    def cutoff(complement: int, analytic_x: int, numerator: int = 133) -> bool:
        return complement**400 <= analytic_x**numerator

    def master_window(group: int, analytic_x: int) -> bool:
        physical_floor = analytic_x // 2
        return group**400 > physical_floor**133 and group * group <= analytic_x

    def route_occurrence(
        product: int,
        analytic_x: int,
        slots: tuple[int, ...],
        kinds: tuple[str, ...],
    ) -> tuple[str, int, int]:
        if prod_fn(slots) != product or len_fn(slots) != len_fn(kinds):
            raise failure_type("occurrence shape changed")
        active = tuple_type(i for i, value in enumerate_fn(slots) if value > 1)
        if not active:
            raise failure_type("empty active occurrence")
        large = tuple_type(i for i in active if slots[i] ** 2 >= product)
        if large:
            first = large[0]
            complement = product // slots[first]
            if kinds[first] == "F" and cutoff(complement, analytic_x):
                return ("H2", complement, first)
            group = complement if kinds[first] == "F" else slots[first]
            if not master_window(group, analytic_x):
                raise failure_type("large MASTER window changed")
            return ("MASTER", group, first)
        full_mask = sum_fn((1 << i for i in active), 0)
        for mask in range_fn(1, 1 << len_fn(slots)):
            if mask & ~full_mask or mask == full_mask:
                continue
            group = prod_fn(
                slots[i] for i in active if mask & (1 << i)
            )
            if group**400 >= product**133 and group * group <= product:
                if not master_window(group, analytic_x):
                    raise failure_type("subset MASTER window changed")
                return ("MASTER", group, -1)
        raise failure_type("no admissible MASTER subset")

    def active_occurrences(
        product: int,
        analytic_x: int,
        mutate_j2_sign: bool = False,
    ):
        e_cutoff = isqrt_fn(analytic_x)
        for e1 in divisors(product):
            if e1 > e_cutoff:
                continue
            f1 = product // e1
            coefficient = 2 * mobius(e1)
            if coefficient and f1 > 1:
                yield coefficient, (e1, f1), ("E", "F")
        for e1 in divisors(product):
            if e1 > e_cutoff:
                continue
            remainder1 = product // e1
            for e2 in divisors(remainder1):
                if e2 > e_cutoff:
                    continue
                remainder = remainder1 // e2
                coefficient = -mobius(e1) * mobius(e2)
                if mutate_j2_sign:
                    coefficient = -coefficient
                if not coefficient:
                    continue
                for f1 in divisors(remainder):
                    if f1 == 1:
                        continue
                    f2 = remainder // f1
                    yield coefficient, (e1, e2, f1, f2), (
                        "E", "E", "F", "F"
                    )

    def enumerate_rows(
        product: int,
        analytic_x: int,
        mutate_j2_sign: bool = False,
    ):
        master: dict[int, int] = {}
        h2: dict[int, int] = {}
        branches: dict[tuple[str, int], dict[int, int]] = {}
        master_count = 0
        h2_count = 0
        rows = list_type()
        for coefficient, slots, kinds in active_occurrences(
            product, analytic_x, mutate_j2_sign
        ):
            route, group, first = route_occurrence(
                product, analytic_x, slots, kinds
            )
            f1 = slots[1] if len_fn(slots) == 2 else slots[2]
            target = h2 if route == "H2" else master
            add_log_vector(target, f1, coefficient)
            if route == "H2":
                h2_count += 1
                branch = "J1" if len_fn(slots) == 2 else (
                    "J2_F1" if first == 2 else "J2_F2"
                )
                key = (branch, group)
                if key not in branches:
                    branches[key] = {}
                add_log_vector(branches[key], f1, coefficient)
            else:
                master_count += 1
            rows.append((route, group, first, coefficient, slots, kinds))
        return master, h2, branches, master_count, h2_count, tuple_type(rows)

    def expected_cutoff_sum(product: int, analytic_x: int, power: int = 133) -> int:
        return sum_fn(
            (
                mobius(d)
                for d in divisors(product)
                if d**400 <= analytic_x**power
            ),
            0,
        )

    def expected_master(product: int, analytic_x: int, power: int = 133):
        answer = mangoldt_vector(product)
        vector_add(
            answer,
            scaled_log_vector(
                product, -expected_cutoff_sum(product, analytic_x, power)
            ),
        )
        return answer

    def verify_branches(product: int, analytic_x: int, branches) -> None:
        for d in divisors(product):
            if not cutoff(d, analytic_x):
                continue
            mu = mobius(d)
            expected = (
                ("J1", scaled_log_vector(product // d, 2 * mu)),
                ("J2_F1", scaled_log_vector(product // d, -mu)),
                ("J2_F2", scaled_log_vector(d, mu)),
            )
            for label, vector in expected:
                if branches.get((label, d), {}) != vector:
                    raise failure_type(
                        "H2 branch identity changed at "
                        + str_type((analytic_x, product, label, d))
                    )
        for label, d in branches:
            if not cutoff(d, analytic_x):
                raise failure_type("H2 branch escaped exact cutoff")

    shell_cases = 0
    master_occurrences = 0
    h2_occurrences = 0
    first_sign_witness = None
    first_cutoff_witness = None
    for analytic_x in range_fn(8, 321):
        for product in range_fn(analytic_x // 2 + 1, analytic_x + 1):
            master, h2, branches, m_count, h_count, _ = enumerate_rows(
                product, analytic_x
            )
            if not cutoff(1, analytic_x):
                raise failure_type("unit cutoff changed")
            if not analytic_x**67 > 2**200:
                raise failure_type("cutoff/square-root exponent chain changed")
            expected = expected_master(product, analytic_x)
            if master != expected:
                raise failure_type(
                    "MASTER marginal identity changed at "
                    + str_type((analytic_x, product, master, expected))
                )
            cutoff_sum = expected_cutoff_sum(product, analytic_x)
            if h2 != scaled_log_vector(product, cutoff_sum):
                raise failure_type("H2 aggregate identity changed")
            verify_branches(product, analytic_x, branches)
            mutated, _, _, _, _, _ = enumerate_rows(
                product, analytic_x, True
            )
            if first_sign_witness is None and mutated != master:
                first_sign_witness = (
                    analytic_x,
                    product,
                    tuple_type(sorted(master.items())),
                    tuple_type(sorted(mutated.items())),
                )
            wrong_cutoff = expected_master(product, analytic_x, 132)
            if first_cutoff_witness is None and wrong_cutoff != master:
                first_cutoff_witness = (
                    analytic_x,
                    product,
                    tuple_type(sorted(master.items())),
                    tuple_type(sorted(wrong_cutoff.items())),
                )
            shell_cases += 1
            master_occurrences += m_count
            h2_occurrences += h_count

    if (
        shell_cases,
        master_occurrences,
        h2_occurrences,
    ) != (25744, 422101, 257830):
        raise failure_type("finite routing totals changed")
    if first_sign_witness != (
        8, 6, ((2, -1), (3, -1)), ((2, 1), (3, -3))
    ):
        raise failure_type("first wrong-sign witness changed")
    if first_cutoff_witness != (
        127, 65, (), ((5, -1), (13, -1))
    ):
        raise failure_type("first wrong-cutoff witness changed")

    example_items = tuple_type()
    examples = list_type()
    for analytic_x, product in ((100, 84), (100, 64), (100, 100)):
        master, _, _, _, _, _ = enumerate_rows(product, analytic_x)
        examples.append((analytic_x, product, tuple_type(sorted(master.items()))))
    example_items = tuple_type(examples)
    if example_items != (
        (100, 84, ((2, 2), (3, 1), (7, 1))),
        (100, 64, ((2, 1),)),
        (100, 100, ()),
    ):
        raise failure_type("published examples changed")

    collision_master, _, _, _, _, collision_rows = enumerate_rows(77, 121)
    collision_a = None
    collision_b = None
    for row in collision_rows:
        route, group, _, coefficient, slots, _ = row
        if route == "MASTER" and slots == (1, 1, 7, 11):
            collision_a = (coefficient, group)
        if route == "MASTER" and slots == (1, 11, 7, 1):
            collision_b = (coefficient, group)
    if collision_a != (-1, 7) or collision_b != (1, 11):
        raise failure_type("occurrence-local collision routing changed")

    def delta_prime(prime: int, z: int, h: int) -> Fraction:
        residue = h % prime
        f_value = (
            fraction_type(0)
            if residue == (-2) % prime
            else fraction_type(prime, prime - 1)
        )
        if prime <= z:
            g_value = f_value
        elif residue == 0:
            g_value = fraction_type(prime, prime - 1)
        else:
            g_value = fraction_type(prime * (prime - 2), (prime - 1) ** 2)
        return f_value - g_value

    delta7 = delta_prime(7, 5, 5)
    delta11 = delta_prime(11, 5, 5)
    local_collision = -delta7 + delta11
    if (
        tuple_type(sorted(collision_master.items())),
        delta7,
        delta11,
        local_collision,
    ) != (
        ((7, -1), (11, -1)),
        fraction_type(-35, 36),
        fraction_type(11, 100),
        fraction_type(487, 450),
    ):
        raise failure_type("occurrence-local collision value changed")

    bazin_terms = (
        fraction_type(1, 2) + 2 * fraction_type(21, 64),
        fraction_type(5, 6) + fraction_type(21, 64),
        fraction_type(1),
        fraction_type(1) + 2 * fraction_type(21, 64)
        - fraction_type(21, 64),
    )
    tube_exponent = bazin_terms[3] - fraction_type(21, 128)
    endpoint_deficit = fraction_type(21, 128) - fraction_type(13, 4800)
    if bazin_terms != (
        fraction_type(37, 32),
        fraction_type(223, 192),
        fraction_type(1),
        fraction_type(85, 64),
    ):
        raise failure_type("Bazin Xi exponent ledger changed")
    if (
        tube_exponent,
        endpoint_deficit,
    ) != (
        fraction_type(149, 128),
        fraction_type(1549, 9600),
    ):
        raise failure_type("Bazin tube loss changed")

    def vector_text(vector) -> str:
        if not vector:
            return "0"
        return ",".join(
            "p" + str_type(prime) + ":" + str_type(coefficient)
            for prime, coefficient in vector
        )

    def fraction_text(value: Fraction) -> str:
        return str_type(value.numerator) + "/" + str_type(value.denominator)

    literal_base = (
        ("check", True),
        ("maximum_claim", literal_maximum_claim),
        ("route_advance", "YES"),
        ("shell_cases", shell_cases),
        ("master_occurrences", master_occurrences),
        ("h2_occurrences", h2_occurrences),
        ("first_wrong_sign_x", first_sign_witness[0]),
        ("first_wrong_sign_t", first_sign_witness[1]),
        ("correct_x8_t6", vector_text(first_sign_witness[2])),
        ("mutated_x8_t6", vector_text(first_sign_witness[3])),
        ("first_wrong_cutoff_x", first_cutoff_witness[0]),
        ("first_wrong_cutoff_t", first_cutoff_witness[1]),
        ("correct_x127_t65", vector_text(first_cutoff_witness[2])),
        ("mutated_x127_t65", vector_text(first_cutoff_witness[3])),
        ("example_x100_t84", vector_text(example_items[0][2])),
        ("example_x100_t64", vector_text(example_items[1][2])),
        ("example_x100_t100", vector_text(example_items[2][2])),
        ("collision_x", 121),
        ("collision_t", 77),
        ("collision_z", 5),
        ("collision_groups", (7, 11)),
        ("collision_marginal", vector_text(tuple_type(sorted(collision_master.items())))),
        ("delta_7_5_at_5", fraction_text(delta7)),
        ("delta_11_5_at_5", fraction_text(delta11)),
        ("collision_local_log7", fraction_text(local_collision)),
        ("bazin_Xi_exponents", tuple_type(fraction_text(v) for v in bazin_terms)),
        ("bazin_tube_exponent", fraction_text(tube_exponent)),
        ("bazin_endpoint_deficit", fraction_text(endpoint_deficit)),
        ("selected_route", "B_THEN_A_THEN_C"),
        ("arithmetic_advance", False),
        ("fixed_atom_credit", 0),
        ("strict_1_over_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", False),
        ("numbered_release", "NO"),
    )

    factor_cache.clear()
    divisor_cache.clear()
    mobius_cache.clear()

    mutation_labels: list[str] = []

    def must_reject(label: str, action) -> None:
        try:
            action()
        except failure_type:
            mutation_labels.append(label)
            return
        raise failure_type("mutation accepted: " + label)

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

    def mapping_mutations(expected: tuple, validator, prefix: str, types: bool) -> int:
        for index, (key, value) in enumerate_fn(expected):
            changed = dict_type(expected)
            changed[key] = mutated(value)
            must_reject(
                prefix + "_value_" + str_type(index),
                lambda c=changed: validator(c),
            )
            rows = list_type(expected)
            rows[index] = (key + "_MUTATED", value)
            must_reject(
                prefix + "_key_" + str_type(index),
                lambda c=dict_type(rows): validator(c),
            )
            if types:
                changed_type = dict_type(expected)
                changed_type[key] = wrong_type(value)
                must_reject(
                    prefix + "_type_" + str_type(index),
                    lambda c=changed_type: validator(c),
                )
        must_reject(prefix + "_outer", lambda: validator(list_type(expected)))

        class StringImpostor(str_type):
            pass

        impostor = dict_type(expected)
        first_key, first_value = expected[0]
        del impostor[first_key]
        impostor[StringImpostor(first_key)] = first_value
        must_reject(prefix + "_key_subclass", lambda: validator(impostor))
        return (3 if types else 2) * len_fn(expected) + 2

    def pair_mutations(expected: tuple, validator, prefix: str, digest_mode: bool) -> int:
        for index, (key, value) in enumerate_fn(expected):
            rows = list_type(expected)
            rows[index] = (key, value + "_MUTATED")
            candidate = tuple_type(rows)
            if digest_mode:
                must_reject(
                    prefix + "_value_" + str_type(index),
                    lambda c=candidate: validator(c, registry_digest(c)),
                )
            else:
                must_reject(
                    prefix + "_value_" + str_type(index),
                    lambda c=candidate: validator(c),
                )
            rows = list_type(expected)
            rows[index] = (key + "_MUTATED", value)
            candidate = tuple_type(rows)
            if digest_mode:
                must_reject(
                    prefix + "_key_" + str_type(index),
                    lambda c=candidate: validator(c, registry_digest(c)),
                )
            else:
                must_reject(
                    prefix + "_key_" + str_type(index),
                    lambda c=candidate: validator(c),
                )
        if digest_mode:
            must_reject(
                prefix + "_outer",
                lambda: validator(list_type(expected), literal_registry_digest),
            )
            must_reject(
                prefix + "_digest",
                lambda: validator(expected, "0" * 64),
            )
        else:
            must_reject(prefix + "_outer", lambda: validator(list_type(expected)))

        class StringImpostor(str_type):
            pass

        rows = list_type(expected)
        rows[0] = (StringImpostor(rows[0][0]), rows[0][1])
        if digest_mode:
            must_reject(
                prefix + "_subclass",
                lambda: validator(tuple_type(rows), literal_registry_digest),
            )
            return 2 * len_fn(expected) + 3
        must_reject(
            prefix + "_subclass",
            lambda: validator(tuple_type(rows)),
        )
        return 2 * len_fn(expected) + 2

    def run() -> dict[str, object]:
        mutation_labels.clear()
        validate_contract(dict_type(literal_contract))
        validate_registry(literal_registry, literal_registry_digest)
        validate_sources(literal_sources)
        validate_dependencies(literal_dependencies)
        require_mapping(dict_type(literal_base), literal_base, "result")
        contract_count = mapping_mutations(
            literal_contract, validate_contract, "contract", False
        )
        registry_count = pair_mutations(
            literal_registry, validate_registry, "registry", True
        )
        source_count = pair_mutations(
            literal_sources, validate_sources, "source", False
        )
        dependency_count = pair_mutations(
            literal_dependencies, validate_dependencies, "dependency", False
        )
        result_count = mapping_mutations(
            literal_base,
            lambda candidate: require_mapping(candidate, literal_base, "result"),
            "result",
            True,
        )
        actions = (
            contract_count
            + registry_count
            + source_count
            + dependency_count
            + result_count
        )
        if (
            len_fn(mutation_labels) != actions
            or len_fn(set_type(mutation_labels)) != actions
        ):
            raise failure_type("mutation ledger changed")
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
        if (
            len_fn(argv) != 1
            or type_fn(argv[0]) is not str_type
            or argv != ("--check",)
        ):
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
_FROZEN_STDOUT = json.dumps(
    _BASELINE_RESULT, sort_keys=True, separators=(",", ":")
)
main = _make_main(
    _TRUSTED_RUN, tuple(_BASELINE_RESULT.items()), _FROZEN_STDOUT
)
del _BASELINE_RESULT


if __name__ == "__main__":
    try:
        raise SystemExit(main(tuple(sys.argv[1:])))
    except CheckFailure as exc:
        sys.stderr.write("CheckFailure: " + str(exc) + "\n")
        raise SystemExit(1)
