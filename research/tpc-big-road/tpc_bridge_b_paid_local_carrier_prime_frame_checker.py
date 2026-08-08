#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V34 compensated-frame compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_PAID_LOCAL_CARRIER_ELIMINATION_TO_COLLAPSED_COMPENSATED_"
    "PRIME_FRAME_COVARIANCE_WITH_STRICT_DELTA_GT_1_OVER_400_GATE"
)


CONTRACT_ITEMS = (
    ("schema_version", "V34_PAID_LOCAL_CARRIER_PRIME_FRAME_V1"),
    ("artifact_name", "bridge_b_paid_local_carrier_and_compensated_prime_frame.md"),
    ("baseline_commit", "b73cb6928d5ea3d3b58b87c0a1e5154d0d9c8f92"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("selected_route", "B_DIRECT_COLLAPSED_PRIME_FRAME_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK"),
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
    ("beta", "Lambda/log+sum_d_above_cutoff_mu(d)"),
    ("rho", "Lambda/log+mu_with_rho_prime_zero"),
    ("proper_tail", "sum_dk=t_k_ge_2_d_above_cutoff_mu(d)"),
    ("local_carrier_payment", "x^(1891/1920+o(1))"),
    ("direct_scalar", "E(e)=E(r)-E(Mloc)"),
    ("prime_frame", "sum_q_sum_h_Phi(h)*(q*1_q_divides_h-1)"),
    ("numerator_target", "x^(5/3-delta+o(1))"),
    ("required_delta", "delta>1/400"),
    ("finite_x_range", (8, 320)),
    ("finite_shell_cases", 25744),
    ("finite_prime_rows", 4945),
    ("finite_nonzero_proper_tail_rows", 13824),
    ("finite_nonzero_proper_tail_terms", 44205),
    ("frame_fixture", (5, 7, 10)),
    ("first_fatal", "NO_POWER_SAVING_BEYOND_X_5_OVER_3_FOR_COLLAPSED_PHYSICAL_COMPENSATED_PRIME_FRAME"),
)


REGISTRY_ITEMS = (
    ("V34_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V34_ROUTE_ADVANCE", "YES"),
    ("V34_ARITHMETIC_ADVANCE", "NO"),
    ("V34_FIXED_ATOM_CREDIT", "0"),
    ("V34_STRICT_1_OVER_400", "UNPAID"),
    ("V34_L2", "NONE"),
    ("V34_TPC_207_TRIGGER", "false"),
    ("V34_NUMBERED_RELEASE", "NO"),
    ("V34_SELECTED_RESEARCH_ROUTE", "B_DIRECT_COLLAPSED_PRIME_FRAME_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK"),
    ("V34_BETA_MASTER_MARGINAL", "RETAINED_EXACT_V33_LAMBDA_OVER_LOG_MINUS_TRUNCATED_MU_CONV_ONE"),
    ("V34_BETA_LARGE_DIVISOR_TAIL", "PROVED_EXACT_LAMBDA_OVER_LOG_PLUS_MU_ABOVE_CUTOFF"),
    ("V34_PRIME_DELETED_ENDPOINT", "PROVED_EXACT_RHO_EQUALS_LAMBDA_OVER_LOG_PLUS_MU_AND_RHO_P_EQUALS_ZERO"),
    ("V34_GENUINE_BILINEAR_TAIL", "PROVED_EXACT_K_GE_2_D_ABOVE_CUTOFF"),
    ("V34_LOCAL_CARRIER_E_PAYMENT", "RETAINED_SOURCE_BACKED_X_1891_OVER_1920_PLUS_O1"),
    ("V34_LOCAL_CARRIER_J_PAYMENT", "RETAINED_SOURCE_BACKED_X_1891_OVER_1920_PLUS_O1"),
    ("V34_DIRECT_SCALAR_ELIMINATION", "PROVED_EXACT_E_OF_E_EQUALS_E_OF_R_MINUS_E_OF_MLOC"),
    ("V34_OCCURRENCE_LABEL_IN_NEW_B_THEOREM", "REMOVED_BY_SEPARATELY_PAID_SCALAR_LOCAL_CARRIER"),
    ("V34_QOSC_P_REPLACEMENT", "STOP_SCOPED_REINTRODUCES_LARGE_OFFZERO_LOCAL_MAIN"),
    ("V34_V32_QOSC_P_MINUS_L", "RETAINED_VALID_STRONGER_ALTERNATIVE"),
    ("V34_RAMANUJAN_PRIME_VECTOR", "PROVED_EXACT_C_Q_EQUALS_Q_DIVISIBILITY_MINUS_ONE"),
    ("V34_ZERO_DELETED_SMOOTH_CORRELATION", "PROVED_EXACT_PHI_H"),
    ("V34_COMPENSATED_DILATION_FORM", "PROVED_EXACT_QK_MINUS_ALL_H"),
    ("V34_COMPENSATED_PAIR_FORM", "PROVED_EXACT_ONE_OUTER_SIGNED_SCALAR"),
    ("V34_L_PR_NORMALIZATION", "X_POWER_2_OVER_3_PLUS_O1"),
    ("V34_DIRECT_NUMERATOR_TARGET", "X_POWER_5_OVER_3_MINUS_DELTA_PLUS_O1"),
    ("V34_REQUIRED_DELTA", "STRICTLY_GREATER_THAN_1_OVER_400"),
    ("V34_DIRECT_E_R_EXPONENT", "X_POWER_1_MINUS_DELTA_PLUS_O1"),
    ("V34_DIRECT_ENDPOINT_MARGIN", "DELTA_MINUS_1_OVER_400"),
    ("V34_LOCAL_CARRIER_ENDPOINT_MARGIN", "121_OVER_9600"),
    ("V34_COMBINED_B_MARGIN", "MIN_DELTA_MINUS_1_OVER_400_AND_121_OVER_9600"),
    ("V34_BAZIN_ACTUAL_FRAME_Q", "X_POWER_1_OVER_3"),
    ("V34_BAZIN_ACTUAL_FRAME_THETA", "X_POWER_MINUS_21_OVER_32"),
    ("V34_BAZIN_ACTUAL_FRAME_XI_EXPONENT", "257_OVER_192"),
    ("V34_BAZIN_ACTUAL_FRAME_ADDITIVE_EXPONENT", "75_OVER_64"),
    ("V34_BAZIN_TO_DIRECT_COVARIANCE", "STOP_SCOPED_ONE_MARGINAL_NO_PHYSICAL_PRODUCT"),
    ("V34_MRT_TO_DIRECT_COVARIANCE", "STOP_SCOPED_LOGARITHMIC_SHIFT_ENERGY_WRONG_COEFFICIENT_AND_FRAME"),
    ("V34_EVANS_TO_DIRECT_COVARIANCE", "STOP_SCOPED_FIXED_E2_ALMOST_ALL_SHIFTS_WRONG_COEFFICIENT"),
    ("V34_MRSTT_TO_DIRECT_COVARIANCE", "STOP_SCOPED_DENSITY_ONE_NO_QUANTITATIVE_FRAME_POWER"),
    ("V34_DIRECT_PRIMARY_SOURCE_ATTACHMENT", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08"),
    ("V34_NEXT_THEOREM", "DELTA_GT_1_OVER_400_POWER_SAVING_FOR_COLLAPSED_SIEVE_REMAINDER_TIMES_PHYSICAL_HYBRID_IN_COMPENSATED_PRIME_FRAME"),
    ("V34_FIRST_FATAL", "NO_POWER_SAVING_BEYOND_X_5_OVER_3_FOR_COLLAPSED_PHYSICAL_COMPENSATED_PRIME_FRAME"),
    ("V34_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B"),
    ("V34_SOURCE_LOCK_POLICY", "PRIMARY_SOURCES_ONLY_FAIL_CLOSED"),
)


EXPECTED_REGISTRY_SHA256 = "8a6caddc05238b6706034e7e2b6cf9fb5bf8d70ff714c85d0c897a4f5e36ce3c"


SOURCE_ITEMS = (
    ("BETTIN_CHANDEE_LOCAL_CARRIER", "arXiv:1502.00769v1_Theorem_1"),
    ("BAZIN_TYPE_I_II", "arXiv:2607.15137v1_Theorem_8"),
    ("MRT_PRODUCT_ENERGY", "arXiv:1707.01315v3_Proposition_3.1_equations_52_54"),
    ("EVANS_PRIME_E2", "arXiv:2102.12297v3_Theorem_1.4"),
    ("MRSTT_ALMOST_ALL", "arXiv:2411.05770v2_Theorem_1.5"),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_joint_major_minor_and_low_christoffel.md",
        "c4b61b790911d2cfcb3d7a0139d368a35d0d0fdab2984637f3f2fe30638543ab",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_joint_major_minor_checker.py",
        "a016840f1ce41b4ed7ee2e315e7848922da1247828f68dfaf3b62e46fac8fa8c",
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
    if dict_type(literal_registry).get("V34_MAXIMUM_CLAIM") != literal_maximum_claim:
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
            answer = tuple_type(sorted_fn(values))
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

        def lambda_over_log(n: int) -> Fraction:
            factors = factorization(n)
            if len_fn(factors) != 1:
                return fraction_type(0)
            return fraction_type(1, factors[0][1])

        def is_prime(n: int) -> bool:
            factors = factorization(n)
            return len_fn(factors) == 1 and factors[0][1] == 1

        def below_cutoff(d: int, analytic_x: int) -> bool:
            return d**400 <= analytic_x**133

        def beta(analytic_x: int, t: int) -> Fraction:
            return lambda_over_log(t) - sum_fn(
                (mobius(d) for d in divisors(t) if below_cutoff(d, analytic_x)),
                0,
            )

        def upper_tail(analytic_x: int, t: int) -> Fraction:
            return lambda_over_log(t) + sum_fn(
                (mobius(d) for d in divisors(t) if not below_cutoff(d, analytic_x)),
                0,
            )

        def rho(t: int) -> Fraction:
            return lambda_over_log(t) + mobius(t)

        def proper_tail(analytic_x: int, t: int) -> int:
            return sum_fn(
                (
                    mobius(d)
                    for d in divisors(t)
                    if t // d >= 2 and not below_cutoff(d, analytic_x)
                ),
                0,
            )

        shell_cases = 0
        prime_rows = 0
        nonzero_proper_rows = 0
        nonzero_proper_terms = 0
        for analytic_x in range_fn(8, 321):
            for t in range_fn(analytic_x // 2 + 1, analytic_x + 1):
                if not t**400 > analytic_x**133:
                    raise failure_type("shell endpoint escaped upper cutoff")
                if sum_fn((mobius(d) for d in divisors(t)), 0) != 0:
                    raise failure_type("complete Mobius divisor sum changed")
                beta_value = beta(analytic_x, t)
                upper_value = upper_tail(analytic_x, t)
                proper_value = proper_tail(analytic_x, t)
                if beta_value != upper_value or beta_value != rho(t) + proper_value:
                    raise failure_type(
                        "large-divisor tail identity changed at "
                        + str_type((analytic_x, t))
                    )
                if is_prime(t):
                    prime_rows += 1
                    if rho(t) != 0 or beta_value != 0:
                        raise failure_type("prime-deleted endpoint changed")
                if proper_value:
                    nonzero_proper_rows += 1
                nonzero_proper_terms += sum_fn(
                    (
                        1
                        for d in divisors(t)
                        if t // d >= 2
                        and not below_cutoff(d, analytic_x)
                        and mobius(d) != 0
                    ),
                    0,
                )
                shell_cases += 1

        if (
            shell_cases,
            prime_rows,
            nonzero_proper_rows,
            nonzero_proper_terms,
        ) != (25744, 4945, 13824, 44205):
            raise failure_type("large-divisor finite census changed")

        def fraction_text(value: Fraction) -> str:
            return str_type(value)

        example_points = (
            (8, 5),
            (8, 6),
            (100, 84),
            (100, 64),
            (100, 100),
            (100, 70),
        )
        tail_examples = tuple_type(
            (
                "x" + str_type(x) + "_t" + str_type(t),
                fraction_text(beta(x, t)),
                fraction_text(rho(t)),
                str_type(proper_tail(x, t)),
            )
            for x, t in example_points
        )
        if tail_examples != (
            ("x8_t5", "0", "0", "0"),
            ("x8_t6", "-1", "1", "-2"),
            ("x100_t84", "1", "0", "1"),
            ("x100_t64", "1/6", "1/6", "0"),
            ("x100_t100", "0", "0", "0"),
            ("x100_t70", "0", "-1", "1"),
        ):
            raise failure_type("large-divisor examples changed")

        def ramanujan_prime(q: int, h: int) -> int:
            if h % q == 0:
                return q - 1
            residues = tuple_type(sorted_fn((a * h) % q for a in range_fn(1, q)))
            if residues != tuple_type(range_fn(1, q)):
                raise failure_type("prime root-of-unity permutation changed")
            return -1

        c5_vector = tuple_type(ramanujan_prime(5, h) for h in range_fn(5))
        if c5_vector != (4, -1, -1, -1, -1):
            raise failure_type("prime Ramanujan vector changed")

        beta_fixture = (1, -1, 2, 0, -2, 1, 0, 1, -1, 2)
        physical_fixture = (2, 0, -1, 1, 3, -2, 1, 0, 2, -1)
        primes = (5, 7)
        domain_size = len_fn(beta_fixture)

        def smooth_weight(h: int) -> Fraction:
            return fraction_type(0) if h == 0 else fraction_type(1, abs_fn(h) + 1)

        def correlation(h: int) -> int:
            return sum_fn(
                (
                    beta_fixture[t] * physical_fixture[t + h]
                    for t in range_fn(domain_size)
                    if 0 <= t + h < domain_size
                ),
                0,
            )

        phi = dict_type(
            (
                h,
                smooth_weight(h) * correlation(h),
            )
            for h in range_fn(-domain_size + 1, domain_size)
            if h != 0
        )
        h_form = sum_fn(
            (
                sum_fn((ramanujan_prime(q, h) for q in primes), 0) * value
                for h, value in phi.items()
            ),
            fraction_type(0),
        )
        dilation_positive = sum_fn(
            (
                q
                * sum_fn(
                    (
                        phi[q * k]
                        for k in range_fn(-domain_size, domain_size + 1)
                        if k != 0 and q * k in phi
                    ),
                    fraction_type(0),
                )
                for q in primes
            ),
            fraction_type(0),
        )
        dilation_compensation = len_fn(primes) * sum_fn(
            phi.values(), fraction_type(0)
        )
        dilation_form = dilation_positive - dilation_compensation
        pair_form = sum_fn(
            (
                beta_fixture[t]
                * physical_fixture[u]
                * smooth_weight(u - t)
                * ramanujan_prime(q, u - t)
                for q in primes
                for t in range_fn(domain_size)
                for u in range_fn(domain_size)
                if t != u
            ),
            fraction_type(0),
        )
        if (
            h_form,
            dilation_positive,
            dilation_compensation,
            dilation_form,
            pair_form,
        ) != (
            fraction_type(-6061, 315),
            fraction_type(2, 3),
            fraction_type(6271, 315),
            fraction_type(-6061, 315),
            fraction_type(-6061, 315),
        ):
            raise failure_type("compensated frame normal forms changed")
        l_pr_fixture = sum_fn((q - 1 for q in primes), 0)
        e_r_fixture = -h_form / l_pr_fixture
        if l_pr_fixture != 10 or e_r_fixture != fraction_type(6061, 3150):
            raise failure_type("prime-frame normalization changed")

        local_carrier = {1: fraction_type(3), 2: fraction_type(-3)}
        local_e = -sum_fn(
            (
                fraction_type(ramanujan_prime(5, h), 4) * value
                for h, value in local_carrier.items()
            ),
            fraction_type(0),
        )
        local_energy = sum_fn(
            (value * value for value in local_carrier.values()),
            fraction_type(0),
        )
        if local_e != 0 or local_energy != 18:
            raise failure_type("paid-scalar versus energy firewall changed")

        delta = fraction_type(1, 300)
        direct_margin = delta - fraction_type(1, 400)
        local_margin = fraction_type(399, 400) - fraction_type(1891, 1920)
        combined_margin = min_fn(direct_margin, local_margin)
        if (
            direct_margin,
            local_margin,
            combined_margin,
        ) != (
            fraction_type(1, 1200),
            fraction_type(121, 9600),
            fraction_type(1, 1200),
        ):
            raise failure_type("strict endpoint ledger changed")

        q_exponent = fraction_type(1, 3)
        theta_exponent = fraction_type(-21, 32)
        bazin_terms = (
            fraction_type(1, 2) + 2 * q_exponent,
            fraction_type(5, 6) + q_exponent,
            fraction_type(1),
            fraction_type(1) + 2 * q_exponent + theta_exponent / 2,
        )
        bazin_xi = max_fn(bazin_terms)
        bazin_additive = bazin_xi - q_exponent / 2
        if bazin_terms != (
            fraction_type(7, 6),
            fraction_type(7, 6),
            fraction_type(1),
            fraction_type(257, 192),
        ) or bazin_additive != fraction_type(75, 64):
            raise failure_type("Bazin actual-frame exponent ledger changed")

        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("shell_cases", shell_cases),
            ("prime_rows", prime_rows),
            ("nonzero_proper_tail_rows", nonzero_proper_rows),
            ("nonzero_proper_tail_terms", nonzero_proper_terms),
            ("tail_examples", tail_examples),
            ("ramanujan_c5", c5_vector),
            ("frame_h_form", fraction_text(h_form)),
            ("frame_dilation_positive", fraction_text(dilation_positive)),
            ("frame_dilation_compensation", fraction_text(dilation_compensation)),
            ("frame_dilation_form", fraction_text(dilation_form)),
            ("frame_pair_form", fraction_text(pair_form)),
            ("frame_L_pr", l_pr_fixture),
            ("frame_E_r", fraction_text(e_r_fixture)),
            ("local_carrier_E", fraction_text(local_e)),
            ("local_carrier_offzero_energy", fraction_text(local_energy)),
            ("sample_delta", fraction_text(delta)),
            ("sample_direct_margin", fraction_text(direct_margin)),
            ("local_carrier_margin", fraction_text(local_margin)),
            ("sample_combined_margin", fraction_text(combined_margin)),
            ("bazin_Xi_exponents", tuple_type(fraction_text(v) for v in bazin_terms)),
            ("bazin_dominant_exponent", fraction_text(bazin_xi)),
            ("bazin_additive_exponent", fraction_text(bazin_additive)),
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
            return 3 * len_fn(expected) + 2

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
            must_reject(prefix + "_subclass", lambda: validator(tuple_type(rows)))
            return 2 * len_fn(expected) + 2

        contract_count = 3 * len_fn(literal_contract) + 2
        registry_count = 2 * len_fn(literal_registry) + 3
        source_count = 2 * len_fn(literal_sources) + 2
        dependency_count = 2 * len_fn(literal_dependencies) + 2
        metadata_fields = 11
        result_count = 3 * (len_fn(literal_base) + metadata_fields) + 2
        actions = (
            contract_count
            + registry_count
            + source_count
            + dependency_count
            + result_count
        )
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

        observed_contract = mapping_mutations(
            literal_contract, validate_contract, "contract"
        )
        observed_registry = pair_mutations(
            literal_registry, validate_registry, "registry", True
        )
        observed_source = pair_mutations(
            literal_sources, validate_sources, "source", False
        )
        observed_dependency = pair_mutations(
            literal_dependencies, validate_dependencies, "dependency", False
        )
        observed_result = mapping_mutations(
            full,
            lambda candidate: require_mapping(candidate, full, "full result"),
            "result",
        )
        if (
            observed_contract,
            observed_registry,
            observed_source,
            observed_dependency,
            observed_result,
        ) != (
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
