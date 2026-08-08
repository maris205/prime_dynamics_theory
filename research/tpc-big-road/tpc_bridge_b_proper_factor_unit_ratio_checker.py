#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V35 proper-factor ratio compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_ENDPOINT_FREE_PROPER_FACTOR_AND_PAID_NONUNIT_PRINCIPAL_"
    "REDUCTION_TO_ZERO_DELETED_COPRIME_FIXED_SHIFT_TWO_TERNARY_RATIO_CORE"
)


CONTRACT_ITEMS = (
    ("schema_version", "V35_PROPER_FACTOR_UNIT_RATIO_V1"),
    ("artifact_name", "bridge_b_proper_factor_unit_ratio_reduction.md"),
    ("baseline_commit", "469202a4cb84dc7bf12301ca5f10be8b283d620d"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("selected_route", "B_COPRIME_FIXED_SHIFT_RATIO_CORE_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK"),
    ("route_position", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B"),
    ("route_advance", "YES"),
    ("arithmetic_advance", False),
    ("fixed_atom_credit", 0),
    ("strict_1_over_400", "UNPAID"),
    ("L2", "NONE"),
    ("TPC_207_TRIGGER", False),
    ("numbered_release", "NO"),
    ("shell", "X_OVER_2_LT_T_LE_X_WITH_X_GE_8"),
    ("H", "x^(21/32)"),
    ("Q", "x^(1/3)"),
    ("L_pr", "x^(2/3+o(1))"),
    ("proper_factor_support", "d>=2_and_k>=2"),
    ("proper_factor_weight_bound", "abs(omega)<=1"),
    ("unit_kernel", "q*u1(u*inverse(dk))+1/(q-1)"),
    ("exact_partition", "D=core+principal+nonunit"),
    ("paid_remainders", "x^(53/32+o(1))"),
    ("core_target", "x^(5/3-delta+o(1))"),
    ("required_delta", "delta>1/400"),
    ("finite_x_range", (8, 320)),
    ("finite_shell_cases", 25744),
    ("finite_prime_rows", 4945),
    ("finite_nonzero_beta_rows", 7449),
    ("finite_proper_weight_terms", 72237),
    ("ratio_fixture_primes", (5, 7)),
    ("ratio_fixture_L_pr", 10),
    ("first_fatal", "NO_BINARY_SOURCE_PARAMETERIZATION_PRESERVES_Q_INDEPENDENT_COEFFICIENTS_PRIME_ONLY_ZERO_DELETION_AND_PHYSICAL_THIRD_ARRAY"),
)


REGISTRY_ITEMS = (
    ("V35_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V35_ROUTE_ADVANCE", "YES"),
    ("V35_ARITHMETIC_ADVANCE", "NO"),
    ("V35_FIXED_ATOM_CREDIT", "0"),
    ("V35_STRICT_1_OVER_400", "UNPAID"),
    ("V35_L2", "NONE"),
    ("V35_TPC_207_TRIGGER", "false"),
    ("V35_NUMBERED_RELEASE", "NO"),
    ("V35_SELECTED_RESEARCH_ROUTE", "B_COPRIME_FIXED_SHIFT_RATIO_CORE_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK"),
    ("V35_V34_COMPENSATED_FRAME", "RETAINED_EXACT_ZERO_DELETED_ONE_OUTER_SIGNED_SCALAR"),
    ("V35_PROPER_FACTOR_IDENTITY", "PROVED_EXACT_BETA_EQUALS_SUM_MU_TIMES_OMEGA"),
    ("V35_D_EQ_1_ENDPOINT", "PROVED_EXACT_ZERO_COEFFICIENT"),
    ("V35_K_EQ_1_ENDPOINT", "PROVED_EXACT_ZERO_COEFFICIENT"),
    ("V35_PROPER_FACTOR_SUPPORT", "PROVED_EXACT_D_AND_K_AT_LEAST_2"),
    ("V35_PROPER_FACTOR_WEIGHT", "PROVED_EXACT_PIECEWISE_NEG_LOG_D_OR_POS_LOG_K_OVER_LOG_DK"),
    ("V35_PROPER_FACTOR_WEIGHT_BOUND", "PROVED_EXACT_ABSOLUTE_VALUE_AT_MOST_1"),
    ("V35_PRIME_ROWS", "PROVED_EXACT_EMPTY"),
    ("V35_UNIT_RATIO_VECTOR", "PROVED_EXACT_Q_U1_PLUS_ONE_OVER_Q_MINUS_1"),
    ("V35_UNIT_CHARACTER_EXPANSION", "PROVED_EXACT_NONPRINCIPAL_CHARACTER_AVERAGE"),
    ("V35_EXACT_DECOMPOSITION", "PROVED_EXACT_D_EQUALS_CORE_PLUS_PRINCIPAL_PLUS_NONUNIT"),
    ("V35_NONUNIT_PAYMENT", "PROVED_ABSOLUTE_X_POWER_53_OVER_32_PLUS_O1"),
    ("V35_UNIT_PRINCIPAL_PAYMENT", "PROVED_ABSOLUTE_X_POWER_53_OVER_32_PLUS_O1"),
    ("V35_PAID_REMAINDER_E_EXPONENT", "X_POWER_95_OVER_96_PLUS_O1"),
    ("V35_PAID_REMAINDER_NUMERATOR_SAVING", "1_OVER_96"),
    ("V35_PAID_REMAINDER_ENDPOINT_MARGIN", "19_OVER_2400"),
    ("V35_COPRIME_CORE", "PROVED_EXACT_PRIME_ONLY_ZERO_DELETED_THREE_ARRAY_RATIO_FRAME"),
    ("V35_FIXED_SHIFT_TWO_FORM", "PROVED_EXACT_N_CONGRUENT_DK_PLUS_2"),
    ("V35_CORE_NUMERATOR_TARGET", "X_POWER_5_OVER_3_MINUS_DELTA_PLUS_O1"),
    ("V35_REQUIRED_DELTA", "STRICTLY_GREATER_THAN_1_OVER_400"),
    ("V35_CORE_E_EXPONENT", "X_POWER_1_MINUS_DELTA_PLUS_O1"),
    ("V35_LOCAL_CARRIER_PAYMENT", "RETAINED_SOURCE_BACKED_X_1891_OVER_1920_PLUS_O1"),
    ("V35_LOCAL_CARRIER_ENDPOINT_MARGIN", "121_OVER_9600"),
    ("V35_COMBINED_B_MARGIN", "MIN_DELTA_MINUS_1_OVER_400_AND_19_OVER_2400_AND_121_OVER_9600"),
    ("V35_FULL_DIAGONAL_REINSERTION", "STOP_SCOPED_CIRCULAR_L_PR_TIMES_PHYSICAL_SCALAR"),
    ("V35_CORE_DIAGONAL_CORRECTION", "STOP_SCOPED_ABSOLUTE_X_POWER_5_OVER_3"),
    ("V35_RAW_POSITIVE_COMPENSATION_TRIANGLE", "STOP_SCOPED_X_POWER_191_OVER_96"),
    ("V35_DRAPPEAU_UNIT_KERNEL", "MATCHES_U1_ONLY_AT_R_EQUALS_1_ON_PRIME_UNITS"),
    ("V35_DRAPPEAU_DIRECT_ATTACHMENT", "STOP_SCOPED_BINARY_FIXED_PRODUCT_ALL_MODULI_NO_THIRD_PHYSICAL_ARRAY_OR_ZERO_DELETION"),
    ("V35_FOUVRY_RADZIWILL_DIRECT_ATTACHMENT", "STOP_SCOPED_BINARY_FIXED_RESIDUE_WRONG_OBJECT_AND_SUBPOWER_OUTPUT"),
    ("V35_WRIGHT_DIRECT_ATTACHMENT", "STOP_SCOPED_FIXED_RESIDUE_SIEGEL_WALFISZ_ARRAY_NO_MOVING_RATIO"),
    ("V35_BETTIN_CHANDEE_DIRECT_ATTACHMENT", "STOP_SCOPED_FIXED_DETERMINANT_NO_COLLECTIVE_Q_ELL_REASSEMBLY"),
    ("V35_BETTIN_CHANDEE_PER_SHIFT_TRIANGLE_EXPONENT", "943_OVER_480"),
    ("V35_BETTIN_CHANDEE_PER_SHIFT_TRIANGLE_DEFICIT", "721_OVER_2400"),
    ("V35_BAZIN_DIRECT_ATTACHMENT", "STOP_SCOPED_ONE_MARGINAL_NO_PHYSICAL_PRODUCT"),
    ("V35_DIRECT_PRIMARY_SOURCE_ATTACHMENT", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09"),
    ("V35_NEXT_THEOREM", "DELTA_GT_1_OVER_400_POWER_SAVING_FOR_PRIME_ONLY_ZERO_DELETED_THREE_ARRAY_FIXED_SHIFT_TWO_RATIO_CORE"),
    ("V35_FIRST_FATAL", "NO_BINARY_SOURCE_PARAMETERIZATION_PRESERVES_Q_INDEPENDENT_COEFFICIENTS_PRIME_ONLY_ZERO_DELETION_AND_PHYSICAL_THIRD_ARRAY"),
    ("V35_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B"),
    ("V35_SOURCE_LOCK_POLICY", "PRIMARY_SOURCES_ONLY_FAIL_CLOSED"),
)


EXPECTED_REGISTRY_SHA256 = "cf8d7df24621b5b10d7004bf7b3d0cdd51ffb572037c4d553f8102ee94115a63"


SOURCE_ITEMS = (
    ("DRAPPEAU_BINARY_DISPERSION", "arXiv:1504.05549v4_Theorem_5.1_equations_5.1_5.3_5.7"),
    ("FOUVRY_RADZIWILL_FIXED_RESIDUE", "arXiv:1811.08672_Theorems_1.1_1.2"),
    ("WRIGHT_FIXED_RESIDUE", "arXiv:2604.25177v1_Theorem_2.1_Corollary_2.2"),
    ("BETTIN_CHANDEE_DETERMINANT", "arXiv:1502.00769v1_Theorem_1_Corollary_1"),
    ("BAZIN_ONE_MARGINAL", "arXiv:2607.15137v1_Theorem_8"),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_paid_local_carrier_and_compensated_prime_frame.md",
        "e1816cdac10715bd982ef14960346f17968ac1ea96a3cdbf0b740d3f473ebca8",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_paid_local_carrier_prime_frame_checker.py",
        "d1ac9b35ac3c164cdf5931f5b01fa4021db233263c537c0602c73796632a151a",
    ),
    (
        "research/tpc-big-road/bridge_b_master_marginal_collapse_and_joint_residual_firewall.md",
        "6785eab0d05ec1b564c99d6d155788950bc7383b0fdfa10e2458dab71956b167",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_master_marginal_collapse_checker.py",
        "c70e30b1437350fefbd9236eb29fab5d94356ec5ff0040a90358b470f02e0a13",
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
    any_fn=any,
    enumerate_fn=enumerate,
    pow_fn=pow,
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
    if dict_type(literal_registry).get("V35_MAXIMUM_CLAIM") != literal_maximum_claim:
        raise failure_type("maximum claim registry seed changed")
    if registry_digest(literal_registry) != literal_registry_digest:
        raise failure_type("registry literal digest changed")

    def compute_base() -> tuple[tuple[str, object], ...]:
        factor_cache: dict[int, tuple[tuple[int, int], ...]] = {}
        divisor_cache: dict[int, tuple[int, ...]] = {}
        mobius_cache: dict[int, int] = {}

        def factorization(n: int) -> tuple[tuple[int, int], ...]:
            if n in factor_cache:
                return factor_cache[n]
            original = n
            rows = []
            p = 2
            while p * p <= n:
                if n % p == 0:
                    exponent = 0
                    while n % p == 0:
                        n //= p
                        exponent += 1
                    rows.append((p, exponent))
                p += 1
            if n > 1:
                rows.append((n, 1))
            value = tuple_type(rows)
            factor_cache[original] = value
            return value

        def divisors(n: int) -> tuple[int, ...]:
            if n in divisor_cache:
                return divisor_cache[n]
            values = [1]
            for p, exponent in factorization(n):
                values = [d * p**e for d in values for e in range_fn(exponent + 1)]
            result = tuple_type(sorted_fn(values))
            divisor_cache[n] = result
            return result

        def mobius(n: int) -> int:
            if n in mobius_cache:
                return mobius_cache[n]
            factors = factorization(n)
            value = 0 if any_fn(exponent > 1 for _, exponent in factors) else (
                -1 if len_fn(factors) % 2 else 1
            )
            mobius_cache[n] = value
            return value

        def below_cutoff(d: int, analytic_x: int) -> bool:
            return d**400 <= analytic_x**133

        def is_prime(n: int) -> bool:
            factors = factorization(n)
            return len_fn(factors) == 1 and factors[0][1] == 1

        def lambda_over_log(n: int) -> Fraction:
            factors = factorization(n)
            if len_fn(factors) != 1:
                return fraction_type(0)
            return fraction_type(1, factors[0][1])

        def beta_fraction(analytic_x: int, t: int) -> Fraction:
            return lambda_over_log(t) - sum_fn(
                (mobius(d) for d in divisors(t) if below_cutoff(d, analytic_x)),
                0,
            )

        def add_vector(
            left: dict[int, int], right: dict[int, int], scale: int = 1
        ) -> dict[int, int]:
            result = dict_type(left)
            for prime, coefficient in right.items():
                result[prime] = result.get(prime, 0) + scale * coefficient
                if result[prime] == 0:
                    del result[prime]
            return result

        def log_vector(n: int) -> dict[int, int]:
            return dict_type(factorization(n))

        def beta_log_vector(analytic_x: int, t: int) -> dict[int, int]:
            logarithm = log_vector(t)
            cutoff_sum = sum_fn(
                (mobius(d) for d in divisors(t) if below_cutoff(d, analytic_x)),
                0,
            )
            result = dict_type(
                (prime, -cutoff_sum * exponent)
                for prime, exponent in logarithm.items()
                if cutoff_sum * exponent
            )
            factors = factorization(t)
            if len_fn(factors) == 1:
                prime = factors[0][0]
                result[prime] = result.get(prime, 0) + 1
                if result[prime] == 0:
                    del result[prime]
            return result

        def proper_log_vector(
            analytic_x: int, t: int
        ) -> tuple[dict[int, int], int]:
            logarithm = log_vector(t)
            total: dict[int, int] = {}
            active_terms = 0
            for d in divisors(t):
                k = t // d
                mu = mobius(d)
                if d < 2 or k < 2 or mu == 0:
                    continue
                contribution = (
                    dict_type(logarithm)
                    if not below_cutoff(d, analytic_x)
                    else {}
                )
                contribution = add_vector(contribution, log_vector(d), -1)
                contribution = dict_type(
                    (prime, mu * coefficient)
                    for prime, coefficient in contribution.items()
                    if mu * coefficient
                )
                if contribution:
                    active_terms += 1
                total = add_vector(total, contribution)
            return total, active_terms

        shell_cases = 0
        prime_rows = 0
        nonzero_beta_rows = 0
        proper_weight_terms = 0
        for analytic_x in range_fn(8, 321):
            for t in range_fn(analytic_x // 2 + 1, analytic_x + 1):
                if not t**400 > analytic_x**133:
                    raise failure_type("shell endpoint escaped upper cutoff")
                left = beta_log_vector(analytic_x, t)
                right, active_terms = proper_log_vector(analytic_x, t)
                if left != right:
                    raise failure_type(
                        "proper-factor prime-log identity changed at "
                        + str_type((analytic_x, t))
                    )
                if is_prime(t):
                    prime_rows += 1
                    if left or beta_fraction(analytic_x, t) != 0:
                        raise failure_type("prime row stopped being empty")
                if left:
                    nonzero_beta_rows += 1
                proper_weight_terms += active_terms
                shell_cases += 1

        if (
            shell_cases,
            prime_rows,
            nonzero_beta_rows,
            proper_weight_terms,
        ) != (25744, 4945, 7449, 72237):
            raise failure_type("proper-factor finite census changed")

        example_points = (
            (8, 5),
            (8, 6),
            (8, 8),
            (100, 84),
            (100, 64),
            (100, 100),
            (100, 70),
        )
        beta_examples = tuple_type(
            (
                "x" + str_type(x) + "_t" + str_type(t),
                str_type(beta_fraction(x, t)),
            )
            for x, t in example_points
        )
        if beta_examples != (
            ("x8_t5", "0"),
            ("x8_t6", "-1"),
            ("x8_t8", "-2/3"),
            ("x100_t84", "1"),
            ("x100_t64", "1/6"),
            ("x100_t100", "0"),
            ("x100_t70", "0"),
        ):
            raise failure_type("proper-factor examples changed")

        beta_fixture = (1, -1, 2, 0, -2, 1, 0, 1, -1, 2)
        physical_fixture = (2, 0, -1, 1, 3, -2, 1, 0, 2, -1)
        primes = (5, 7)
        size = len_fn(beta_fixture)

        def smooth_weight(h: int) -> Fraction:
            return fraction_type(0) if h == 0 else fraction_type(1, abs_fn(h) + 1)

        def unit_center(q: int, residue: int) -> Fraction:
            return fraction_type(int_type(residue % q == 1), 1) - fraction_type(1, q - 1)

        per_q = []
        original_total = fraction_type(0)
        nonunit_total = fraction_type(0)
        core_total = fraction_type(0)
        principal_total = fraction_type(0)
        for q in primes:
            original = fraction_type(0)
            nonunit = fraction_type(0)
            core = fraction_type(0)
            principal = fraction_type(0)
            for t in range_fn(size):
                for u in range_fn(size):
                    if t == u:
                        continue
                    amplitude = (
                        beta_fixture[t]
                        * physical_fixture[u]
                        * smooth_weight(u - t)
                    )
                    kernel = q * int_type(u % q == t % q) - 1
                    original += amplitude * kernel
                    if (t * u) % q == 0:
                        nonunit += amplitude * kernel
                    else:
                        ratio = (u * pow_fn(t, -1, q)) % q
                        core += amplitude * q * unit_center(q, ratio)
                        principal += amplitude * fraction_type(1, q - 1)
            if original != nonunit + core + principal:
                raise failure_type("unit-ratio decomposition changed")
            per_q.append(
                tuple_type(
                    str_type(value)
                    for value in (original, nonunit, core, principal)
                )
            )
            original_total += original
            nonunit_total += nonunit
            core_total += core
            principal_total += principal

        ratio_totals = tuple_type(
            str_type(value)
            for value in (
                original_total,
                nonunit_total,
                core_total,
                principal_total,
            )
        )
        if tuple_type(per_q) != (
            ("-1823/315", "-299/84", "-551/144", "1151/720"),
            ("-4238/315", "-29/105", "-15659/1080", "1427/1080"),
        ) or ratio_totals != (
            "-6061/315",
            "-537/140",
            "-39583/2160",
            "6307/2160",
        ):
            raise failure_type("unit-ratio fixture changed")

        diagonal_scalar = sum_fn(
            (beta_fixture[t] * physical_fixture[t] for t in range_fn(size)), 0
        )
        l_pr_fixture = sum_fn((q - 1 for q in primes), 0)
        full_diagonal = l_pr_fixture * diagonal_scalar
        core_diagonal = sum_fn(
            (
                fraction_type(q * (q - 2), q - 1)
                * sum_fn(
                    (
                        beta_fixture[t] * physical_fixture[t]
                        for t in range_fn(size)
                        if t % q != 0
                    ),
                    0,
                )
                for q in primes
            ),
            fraction_type(0),
        )
        if (
            diagonal_scalar,
            l_pr_fixture,
            full_diagonal,
            core_diagonal,
        ) != (-12, 10, -120, fraction_type(-380, 3)):
            raise failure_type("diagonal firewall fixture changed")

        paid_exponent = fraction_type(53, 32)
        numerator_saving = fraction_type(5, 3) - paid_exponent
        paid_endpoint_margin = (
            fraction_type(5, 3) - fraction_type(1, 400) - paid_exponent
        )
        paid_e_exponent = paid_exponent - fraction_type(2, 3)
        local_margin = fraction_type(399, 400) - fraction_type(1891, 1920)
        sample_delta = fraction_type(1, 300)
        combined_margin = min_fn(
            sample_delta - fraction_type(1, 400),
            paid_endpoint_margin,
            local_margin,
        )
        bc_triangle = fraction_type(39, 40) + fraction_type(95, 96)
        bc_deficit = bc_triangle - (
            fraction_type(5, 3) - fraction_type(1, 400)
        )
        raw_triangle = fraction_type(191, 96)
        if (
            paid_exponent,
            numerator_saving,
            paid_endpoint_margin,
            paid_e_exponent,
            local_margin,
            combined_margin,
            bc_triangle,
            bc_deficit,
            raw_triangle,
        ) != (
            fraction_type(53, 32),
            fraction_type(1, 96),
            fraction_type(19, 2400),
            fraction_type(95, 96),
            fraction_type(121, 9600),
            fraction_type(1, 1200),
            fraction_type(943, 480),
            fraction_type(721, 2400),
            fraction_type(191, 96),
        ):
            raise failure_type("V35 exponent ledger changed")

        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("shell_cases", shell_cases),
            ("prime_rows", prime_rows),
            ("nonzero_beta_rows", nonzero_beta_rows),
            ("proper_weight_terms", proper_weight_terms),
            ("beta_examples", beta_examples),
            ("ratio_per_q", tuple_type(per_q)),
            ("ratio_totals", ratio_totals),
            ("ratio_identity", original_total == nonunit_total + core_total + principal_total),
            ("diagonal_scalar", diagonal_scalar),
            ("full_diagonal", full_diagonal),
            ("core_diagonal", str_type(core_diagonal)),
            ("paid_numerator_exponent", str_type(paid_exponent)),
            ("paid_numerator_saving", str_type(numerator_saving)),
            ("paid_endpoint_margin", str_type(paid_endpoint_margin)),
            ("paid_E_exponent", str_type(paid_e_exponent)),
            ("local_carrier_margin", str_type(local_margin)),
            ("sample_delta", str_type(sample_delta)),
            ("sample_combined_margin", str_type(combined_margin)),
            ("raw_triangle_exponent", str_type(raw_triangle)),
            ("bc_triangle_exponent", str_type(bc_triangle)),
            ("bc_triangle_deficit", str_type(bc_deficit)),
            ("selected_route", "B_THEN_A_THEN_C"),
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
