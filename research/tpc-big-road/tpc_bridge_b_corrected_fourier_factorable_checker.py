#!/usr/bin/env python3
"""Fail-closed finite checker for the V25 corrected Fourier/factorable gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


class CheckFailure(RuntimeError):
    pass


ROOT = Path(__file__).resolve().parents[2]
V24_PROOF_REL = (
    "research/tpc-big-road/bridge_b_literal_jutila_farey_atom_compiler.md"
)
V24_CHECKER_REL = (
    "research/tpc-big-road/tpc_bridge_b_literal_jutila_farey_atom_checker.py"
)
V24_PROOF_CANONICAL_SHA256 = (
    "d8fb384e8f3dea30ea9c525805ec12878905e8424ad878aab27ab1f3bffc5a69"
)
V24_CHECKER_CANONICAL_SHA256 = (
    "ab499b2b809e446747baf817f48c11c70ca9ac9d8726271df22892e00c5ed54d"
)

SOURCE_URL = "https://arxiv.org/html/2511.03294v1"
SOURCE_VERSION = "arXiv:2511.03294v1"
SOURCE_LOCATOR = "Lemma_1_equations_2_1_and_2_2"

MAXIMUM_CLAIM = (
    "EXACT_L0_CORRECTED_JUTILA_FOURIER_AND_FACTORIZABLE_AUXILIARY_"
    "EMITTER_WITH_SOURCE_TRANSFER_FIREWALLS"
)

FORMAL_STATUSES = (
    (
        "V25_BLOMER_LI_2_2_FIRST_LINE_AS_PRINTED_MISSING_d_PHASE",
        "STOP_SCOPED_LITERAL_q2_FOURIER_COUNTEREXAMPLE",
    ),
    (
        "V25_CORRECTED_JUTILA_DIVISOR_FOURIER_EXPANSION",
        "PROVED_EXACT_L0_REPOSITORY_DERIVATION",
    ),
    (
        "V25_FOURIER_RATIONAL_DUMMY_INDEX_IDENTIFICATION",
        "STOP_SCOPED_POISSON_DUAL_TYPE_ERROR",
    ),
    (
        "V25_FULL_ENSEMBLE_ZERO_MODE_CANCELLATION",
        "PROVED_EXACT_L0",
    ),
    (
        "V25_NONZERO_SHIFT_SIGNED_FAREY_KLOOSTERMAN_EMITTER",
        "PROVED_EXACT_L0",
    ),
    (
        "V25_PRIME_SHELL_GROUPED_RAMANUJAN_KERNEL",
        "PROVED_EXACT_L0",
    ),
    (
        "V25_DIRECT_CELLWISE_BP_FROM_EXACT_EMITTER",
        "STOP_SCOPED_OUTER_NORM_LONG_RANGE_AND_REASSEMBLY_UNPAID",
    ),
    (
        "V25_FIXED_c_z_COPRIME_SHORT_BP_CELL",
        "SOURCE_BACKED_CONDITIONAL_ENGINE",
    ),
    (
        "V25_FIXED_c_z_NONUNIT_PASCADI_CELL",
        "CONDITIONAL_BV_FOURIER_MEASURE_NORM_UNPAID",
    ),
    (
        "V25_FACTORIZABLE_AUXILIARY_JUTILA_SPLIT",
        "PROVED_EXACT_L0",
    ),
    (
        "V25_FACTORIZABLE_AUXILIARY_L2_GAIN",
        "PROVED_SOURCE_BACKED_DERIVED_UPPER_BOUND_X_MINUS_1_OVER_14",
    ),
    (
        "V25_DIRECT_BLOMER_LI_41_OVER_42_TO_LITERAL_TPC_TRANSFER",
        "STOP_SCOPED_COEFFICIENT_VORONOI_AND_REASSEMBLY_MISMATCH",
    ),
    (
        "V25_ATOMWISE_COMMON_GOOD_PRIME_ENSEMBLE",
        "STOP_SCOPED_MOVING_SLOPE_GCD_AND_REASSEMBLY_MISMATCH",
    ),
    (
        "V25_RAMANUJAN_WEIGHTED_NONZERO_SHIFT_PHYSICAL_THEOREM",
        "OPEN_NEW_THEOREM",
    ),
    (
        "V25_FACTORIZABLE_LITERAL_TRANSFORM_COMPILER",
        "OPEN_NEW_CONSTRUCTION",
    ),
)


def canonical_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def exact_type(value: Any, expected: Any) -> bool:
    return type(value) is type(expected)


def literal_contract() -> dict[str, Any]:
    return {
        "schema": "TPC_V25_CORRECTED_FOURIER_FACTORIZABLE_V1",
        "task": "V25_CORRECTED_FOURIER_AND_FACTORIZABLE_AUXILIARY_GATE",
        "fixed_h0": 2,
        "physical_scale": "x=2X",
        "fourier_transform": "hatpsi_plus(xi)=integral_psi(v)e(xi*v)dv",
        "true_frequency_kernel": "K(n)=L^-1_sum_q_omega(q)r_q(n)hatpsi_plus(delta*n)",
        "printed_phase": "e(-alpha*m)",
        "corrected_phase": "e(-alpha*d*m)",
        "rational_congruence": "lambda_rat=bd_mod_c",
        "fourier_frequency": "n=d*m",
        "dummy_index_relation": "m_fourier_NOT_lambda_rat",
        "q2_printed_frequency_one": "-H1+2H2",
        "q2_true_frequency_one": "-H1",
        "zero_mode": "CANCELS_ONLY_AFTER_FULL_q_d_ENSEMBLE",
        "farey_atom": "S(D-n,sigma(z)u;c)e(z(D-n))",
        "finite_error": "E=-sum_D_nonzero_B(D)K(D)",
        "prime_kernel": "hatpsi(delta*n)/L*(-R+sum_q_divides_n(q))",
        "first_unpaid_norm": "norm_of_(1-chi)G_not_norm_of_1-chi",
        "fixed_cell_bp": "CONDITIONAL_ONLY_M_N_LE_c_AND_COPRIME",
        "factor_q1_exponent": "4/21",
        "factor_q2_exponent": "8/21",
        "factor_q_exponent": "4/7",
        "factor_L_exponent": "8/7",
        "factor_delta_exact_split": "-1",
        "factor_l2_squared_upper_bound_exponent": "-1/7",
        "factor_l2_upper_bound_exponent": "-1/14",
        "factor_crude_error_exponent": "10/7",
        "factor_energy_theta_threshold": "193/2800",
        "source_delta_clock": "delta>=x^(-1+epsilon)",
        "source_coefficient_family": "GL3_Hecke_times_divisor",
        "literal_coefficient_family": "V19_raw_times_Lambda_minus_hybrid",
        "factorable_t": "UNRESTRICTED_SMOOTH",
        "factorable_multiplicity": "KEEP_ALL_(p,t)_REPRESENTATIONS",
        "factorable_omega_sup_bound": "<=norm_rho_infinity*tau(q)=x^o(1)",
        "arithmetic_advance": False,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
        "maximum_claim": MAXIMUM_CLAIM,
    }


def validate_contract(
    candidate: Mapping[str, Any], _exact_type: Any = exact_type
) -> None:
    hard = {
        "schema": "TPC_V25_CORRECTED_FOURIER_FACTORIZABLE_V1",
        "task": "V25_CORRECTED_FOURIER_AND_FACTORIZABLE_AUXILIARY_GATE",
        "fixed_h0": 2,
        "physical_scale": "x=2X",
        "fourier_transform": "hatpsi_plus(xi)=integral_psi(v)e(xi*v)dv",
        "true_frequency_kernel": "K(n)=L^-1_sum_q_omega(q)r_q(n)hatpsi_plus(delta*n)",
        "printed_phase": "e(-alpha*m)",
        "corrected_phase": "e(-alpha*d*m)",
        "rational_congruence": "lambda_rat=bd_mod_c",
        "fourier_frequency": "n=d*m",
        "dummy_index_relation": "m_fourier_NOT_lambda_rat",
        "q2_printed_frequency_one": "-H1+2H2",
        "q2_true_frequency_one": "-H1",
        "zero_mode": "CANCELS_ONLY_AFTER_FULL_q_d_ENSEMBLE",
        "farey_atom": "S(D-n,sigma(z)u;c)e(z(D-n))",
        "finite_error": "E=-sum_D_nonzero_B(D)K(D)",
        "prime_kernel": "hatpsi(delta*n)/L*(-R+sum_q_divides_n(q))",
        "first_unpaid_norm": "norm_of_(1-chi)G_not_norm_of_1-chi",
        "fixed_cell_bp": "CONDITIONAL_ONLY_M_N_LE_c_AND_COPRIME",
        "factor_q1_exponent": "4/21",
        "factor_q2_exponent": "8/21",
        "factor_q_exponent": "4/7",
        "factor_L_exponent": "8/7",
        "factor_delta_exact_split": "-1",
        "factor_l2_squared_upper_bound_exponent": "-1/7",
        "factor_l2_upper_bound_exponent": "-1/14",
        "factor_crude_error_exponent": "10/7",
        "factor_energy_theta_threshold": "193/2800",
        "source_delta_clock": "delta>=x^(-1+epsilon)",
        "source_coefficient_family": "GL3_Hecke_times_divisor",
        "literal_coefficient_family": "V19_raw_times_Lambda_minus_hybrid",
        "factorable_t": "UNRESTRICTED_SMOOTH",
        "factorable_multiplicity": "KEEP_ALL_(p,t)_REPRESENTATIONS",
        "factorable_omega_sup_bound": "<=norm_rho_infinity*tau(q)=x^o(1)",
        "arithmetic_advance": False,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
        "maximum_claim": (
            "EXACT_L0_CORRECTED_JUTILA_FOURIER_AND_FACTORIZABLE_AUXILIARY_"
            "EMITTER_WITH_SOURCE_TRANSFER_FIREWALLS"
        ),
    }
    if set(candidate) != set(hard):
        raise CheckFailure("contract key set changed")
    for key, expected in hard.items():
        value = candidate[key]
        if not _exact_type(value, expected):
            raise CheckFailure(f"contract field {key} type changed")
        if value != expected:
            raise CheckFailure(f"contract field {key} changed")


def literal_registry_items() -> tuple[tuple[str, str], ...]:
    return (
        *FORMAL_STATUSES,
        ("BL_V1_2_2_FIRST_LINE", "PRINTED_MISSING_d_PHASE"),
        ("BL_V1_2_2_SECOND_LINE", "CONSISTENT_WITH_CORRECTED_PHASE"),
        ("BL_V1_VERSION_STATUS", "ONLY_V1_FOUND_2026_08_08"),
        ("FOURIER_INDEX", "n=d*m"),
        ("RATIONAL_INDEX", "lambda_rat=bd_mod_c"),
        ("FOURIER_RATIONAL_CROSSWALK", "POISSON_DUAL_NOT_TERMWISE"),
        ("KAPPA_ZERO", "ONE_FULL_ENSEMBLE"),
        ("IDENTITY_MINUS_CHI_ZERO", "CANCELLED_FULL_ENSEMBLE_ONLY"),
        ("PHYSICAL_ERROR", "RAMANUJAN_WEIGHTED_NONZERO_SHIFTS"),
        ("FAREY_EMITTER", "COMPLETE_SIGNED_KLOOSTERMAN_L0"),
        ("FOURIER_TAIL", "ZERO_ONLY_AFTER_COMPLETE_FAREY_REASSEMBLY"),
        ("RATIONAL_ZERO", "LOCAL_NONEMPTY_NOT_FOURIER_ZERO"),
        ("LITERAL_SHIFT_AXIS", "D_MINUS_n_EQUAL_ZERO_SURVIVES"),
        ("U_AXIS", "RAMANUJAN_AXIS_SURVIVES"),
        ("NONUNIT_ROWS", "RETAINED"),
        ("PRIME_SHELL_DIVISOR_BRANCHES", "OVERLAP_NOT_COVER"),
        ("OUTER_M_NORM", "UNPAID"),
        ("OUTER_U_NORM", "EXACT_c_TIMES_INTERVAL_LENGTH"),
        ("BP_TOP_CELL_MARGIN", "101/12800_GROSS_ONLY"),
        ("BP_LONG_RANGE", "UNPAID_SUBDIVISION"),
        ("PASCADI_NONUNIT_CELL", "BV_FOURIER_MEASURE_NORM_UNPAID"),
        ("Q_AUX_LABEL", "DISTINCT_FROM_V23_PRIME_SHELL"),
        ("Q_AUX_CLOCK", "Q1_4_21_Q2_8_21_Q_4_7"),
        ("Q_AUX_NORMALIZER", "x_8_7_PLUS_o1"),
        ("Q_AUX_L2_UPPER_BOUND", "AT_MOST_x_minus_1_14_PLUS_o1"),
        ("Q_AUX_ENERGY_THRESHOLD", "theta_less_193_2800"),
        ("Q_AUX_T", "UNRESTRICTED_SMOOTH"),
        ("Q_AUX_MULTIPLICITY", "NO_DEDUP"),
        ("Q_AUX_OMEGA_SUP_BOUND", "AT_MOST_NORM_RHO_INFINITY_TIMES_TAU_q"),
        ("Q_AUX_COMPOSITE_KERNEL", "GENERAL_RAMANUJAN_NOT_PRIME_TWO_VALUE"),
        ("SOURCE_41_42", "SOURCE_OBJECT_ONLY"),
        ("LITERAL_VORONOI_INTERFACE", "ABSENT"),
        ("ATOMWISE_GOOD_PRIMES", "NO_COMMON_OPENED_ATOM_ENSEMBLE"),
        ("ARITHMETIC_ADVANCE", "NO"),
        ("FIXED_ATOM_CREDIT", "0"),
        ("STRICT_1_OVER_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", "false"),
        ("MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    )


def registry_digest(items: Sequence[tuple[str, str]]) -> str:
    payload = json.dumps(
        list(items), ensure_ascii=True, separators=(",", ":")
    ).encode("ascii")
    return sha256_hex(payload)


EXPECTED_REGISTRY_SHA256 = (
    "3781892c4b9a830f7bb0f7e1a73f97b2283245e42f02f7db4904d45d18391d42"
)


def validate_registry(
    candidate: Sequence[tuple[str, str]],
    supplied_digest: str,
    _registry_digest: Any = registry_digest,
) -> None:
    hard = (
        (
            "V25_BLOMER_LI_2_2_FIRST_LINE_AS_PRINTED_MISSING_d_PHASE",
            "STOP_SCOPED_LITERAL_q2_FOURIER_COUNTEREXAMPLE",
        ),
        (
            "V25_CORRECTED_JUTILA_DIVISOR_FOURIER_EXPANSION",
            "PROVED_EXACT_L0_REPOSITORY_DERIVATION",
        ),
        (
            "V25_FOURIER_RATIONAL_DUMMY_INDEX_IDENTIFICATION",
            "STOP_SCOPED_POISSON_DUAL_TYPE_ERROR",
        ),
        (
            "V25_FULL_ENSEMBLE_ZERO_MODE_CANCELLATION",
            "PROVED_EXACT_L0",
        ),
        (
            "V25_NONZERO_SHIFT_SIGNED_FAREY_KLOOSTERMAN_EMITTER",
            "PROVED_EXACT_L0",
        ),
        (
            "V25_PRIME_SHELL_GROUPED_RAMANUJAN_KERNEL",
            "PROVED_EXACT_L0",
        ),
        (
            "V25_DIRECT_CELLWISE_BP_FROM_EXACT_EMITTER",
            "STOP_SCOPED_OUTER_NORM_LONG_RANGE_AND_REASSEMBLY_UNPAID",
        ),
        (
            "V25_FIXED_c_z_COPRIME_SHORT_BP_CELL",
            "SOURCE_BACKED_CONDITIONAL_ENGINE",
        ),
        (
            "V25_FIXED_c_z_NONUNIT_PASCADI_CELL",
            "CONDITIONAL_BV_FOURIER_MEASURE_NORM_UNPAID",
        ),
        (
            "V25_FACTORIZABLE_AUXILIARY_JUTILA_SPLIT",
            "PROVED_EXACT_L0",
        ),
        (
            "V25_FACTORIZABLE_AUXILIARY_L2_GAIN",
            "PROVED_SOURCE_BACKED_DERIVED_UPPER_BOUND_X_MINUS_1_OVER_14",
        ),
        (
            "V25_DIRECT_BLOMER_LI_41_OVER_42_TO_LITERAL_TPC_TRANSFER",
            "STOP_SCOPED_COEFFICIENT_VORONOI_AND_REASSEMBLY_MISMATCH",
        ),
        (
            "V25_ATOMWISE_COMMON_GOOD_PRIME_ENSEMBLE",
            "STOP_SCOPED_MOVING_SLOPE_GCD_AND_REASSEMBLY_MISMATCH",
        ),
        (
            "V25_RAMANUJAN_WEIGHTED_NONZERO_SHIFT_PHYSICAL_THEOREM",
            "OPEN_NEW_THEOREM",
        ),
        (
            "V25_FACTORIZABLE_LITERAL_TRANSFORM_COMPILER",
            "OPEN_NEW_CONSTRUCTION",
        ),
        ("BL_V1_2_2_FIRST_LINE", "PRINTED_MISSING_d_PHASE"),
        ("BL_V1_2_2_SECOND_LINE", "CONSISTENT_WITH_CORRECTED_PHASE"),
        ("BL_V1_VERSION_STATUS", "ONLY_V1_FOUND_2026_08_08"),
        ("FOURIER_INDEX", "n=d*m"),
        ("RATIONAL_INDEX", "lambda_rat=bd_mod_c"),
        ("FOURIER_RATIONAL_CROSSWALK", "POISSON_DUAL_NOT_TERMWISE"),
        ("KAPPA_ZERO", "ONE_FULL_ENSEMBLE"),
        ("IDENTITY_MINUS_CHI_ZERO", "CANCELLED_FULL_ENSEMBLE_ONLY"),
        ("PHYSICAL_ERROR", "RAMANUJAN_WEIGHTED_NONZERO_SHIFTS"),
        ("FAREY_EMITTER", "COMPLETE_SIGNED_KLOOSTERMAN_L0"),
        ("FOURIER_TAIL", "ZERO_ONLY_AFTER_COMPLETE_FAREY_REASSEMBLY"),
        ("RATIONAL_ZERO", "LOCAL_NONEMPTY_NOT_FOURIER_ZERO"),
        ("LITERAL_SHIFT_AXIS", "D_MINUS_n_EQUAL_ZERO_SURVIVES"),
        ("U_AXIS", "RAMANUJAN_AXIS_SURVIVES"),
        ("NONUNIT_ROWS", "RETAINED"),
        ("PRIME_SHELL_DIVISOR_BRANCHES", "OVERLAP_NOT_COVER"),
        ("OUTER_M_NORM", "UNPAID"),
        ("OUTER_U_NORM", "EXACT_c_TIMES_INTERVAL_LENGTH"),
        ("BP_TOP_CELL_MARGIN", "101/12800_GROSS_ONLY"),
        ("BP_LONG_RANGE", "UNPAID_SUBDIVISION"),
        ("PASCADI_NONUNIT_CELL", "BV_FOURIER_MEASURE_NORM_UNPAID"),
        ("Q_AUX_LABEL", "DISTINCT_FROM_V23_PRIME_SHELL"),
        ("Q_AUX_CLOCK", "Q1_4_21_Q2_8_21_Q_4_7"),
        ("Q_AUX_NORMALIZER", "x_8_7_PLUS_o1"),
        ("Q_AUX_L2_UPPER_BOUND", "AT_MOST_x_minus_1_14_PLUS_o1"),
        ("Q_AUX_ENERGY_THRESHOLD", "theta_less_193_2800"),
        ("Q_AUX_T", "UNRESTRICTED_SMOOTH"),
        ("Q_AUX_MULTIPLICITY", "NO_DEDUP"),
        ("Q_AUX_OMEGA_SUP_BOUND", "AT_MOST_NORM_RHO_INFINITY_TIMES_TAU_q"),
        ("Q_AUX_COMPOSITE_KERNEL", "GENERAL_RAMANUJAN_NOT_PRIME_TWO_VALUE"),
        ("SOURCE_41_42", "SOURCE_OBJECT_ONLY"),
        ("LITERAL_VORONOI_INTERFACE", "ABSENT"),
        ("ATOMWISE_GOOD_PRIMES", "NO_COMMON_OPENED_ATOM_ENSEMBLE"),
        ("ARITHMETIC_ADVANCE", "NO"),
        ("FIXED_ATOM_CREDIT", "0"),
        ("STRICT_1_OVER_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", "false"),
        (
            "MAXIMUM_CLAIM",
            "EXACT_L0_CORRECTED_JUTILA_FOURIER_AND_FACTORIZABLE_AUXILIARY_"
            "EMITTER_WITH_SOURCE_TRANSFER_FIREWALLS",
        ),
    )
    if type(candidate) not in (tuple, list):
        raise CheckFailure("registry container type changed")
    if len(candidate) != len(hard):
        raise CheckFailure("registry row count changed")
    if any(type(row) is not tuple or len(row) != 2 for row in candidate):
        raise CheckFailure("registry row type changed")
    if len({key for key, _ in candidate}) != len(candidate):
        raise CheckFailure("registry keys are not unique")
    if tuple(candidate) != hard:
        raise CheckFailure("registry semantic row changed")
    actual_digest = _registry_digest(candidate)
    hard_digest = (
        "3781892c4b9a830f7bb0f7e1a73f97b2283245e42f02f7db4904d45d18391d42"
    )
    if supplied_digest != hard_digest:
        raise CheckFailure("registry supplied digest changed")
    if actual_digest != hard_digest:
        raise CheckFailure("registry literal digest changed")


def validate_source_candidate(
    candidate: Mapping[str, str],
    _root: Path = ROOT,
    _canonical_bytes: Any = canonical_bytes,
    _sha256_hex: Any = sha256_hex,
) -> None:
    hard = {
        "v24_proof_path": (
            "research/tpc-big-road/bridge_b_literal_jutila_farey_atom_compiler.md"
        ),
        "v24_checker_path": (
            "research/tpc-big-road/tpc_bridge_b_literal_jutila_farey_atom_checker.py"
        ),
        "v24_proof_sha256": (
            "d8fb384e8f3dea30ea9c525805ec12878905e8424ad878aab27ab1f3bffc5a69"
        ),
        "v24_checker_sha256": (
            "ab499b2b809e446747baf817f48c11c70ca9ac9d8726271df22892e00c5ed54d"
        ),
        "source_url": "https://arxiv.org/html/2511.03294v1",
        "source_version": "arXiv:2511.03294v1",
        "source_locator": "Lemma_1_equations_2_1_and_2_2",
    }
    if set(candidate) != set(hard):
        raise CheckFailure("source-lock key set changed")
    for key, expected in hard.items():
        value = candidate[key]
        if type(value) is not str or value != expected:
            raise CheckFailure(f"source lock {key} changed")
    proof = _root / hard["v24_proof_path"]
    checker = _root / hard["v24_checker_path"]
    if not proof.is_file() or not checker.is_file():
        raise CheckFailure("dependency path missing")
    if _sha256_hex(_canonical_bytes(proof)) != hard["v24_proof_sha256"]:
        raise CheckFailure("V24 proof dependency hash changed")
    if _sha256_hex(_canonical_bytes(checker)) != hard["v24_checker_sha256"]:
        raise CheckFailure("V24 checker dependency hash changed")


def source_candidate() -> dict[str, str]:
    return {
        "v24_proof_path": V24_PROOF_REL,
        "v24_checker_path": V24_CHECKER_REL,
        "v24_proof_sha256": V24_PROOF_CANONICAL_SHA256,
        "v24_checker_sha256": V24_CHECKER_CANONICAL_SHA256,
        "source_url": SOURCE_URL,
        "source_version": SOURCE_VERSION,
        "source_locator": SOURCE_LOCATOR,
    }


def divisors(n: int) -> tuple[int, ...]:
    out: list[int] = []
    for d in range(1, math.isqrt(n) + 1):
        if n % d == 0:
            out.append(d)
            if d * d != n:
                out.append(n // d)
    return tuple(sorted(out))


def mobius(n: int) -> int:
    if n == 1:
        return 1
    count = 0
    p = 2
    remaining = n
    while p * p <= remaining:
        if remaining % p == 0:
            remaining //= p
            count += 1
            if remaining % p == 0:
                return 0
            while remaining % p == 0:
                remaining //= p
        p += 1
    if remaining > 1:
        count += 1
    return -1 if count % 2 else 1


def ramanujan(q: int, n: int) -> int:
    return sum(d * mobius(q // d) for d in divisors(q) if n % d == 0)


def inv_mod(a: int, modulus: int) -> int:
    return pow(a, -1, modulus)


def kloosterman_vector(first: int, second: int, modulus: int) -> tuple[int, ...]:
    coeffs = [0] * modulus
    for b in range(modulus):
        if math.gcd(b, modulus) == 1:
            exponent = (first * b + second * inv_mod(b, modulus)) % modulus
            coeffs[exponent] += 1
    return tuple(coeffs)


def finite_fixtures(
    _ramanujan: Any = ramanujan,
    _kloosterman_vector: Any = kloosterman_vector,
    _mobius: Any = mobius,
    _divisors: Any = divisors,
) -> dict[str, Any]:
    printed_frequency_one = {"H1": -1, "H2": 2}
    corrected_frequency_one = {"H1": -1}
    if printed_frequency_one == corrected_frequency_one:
        raise CheckFailure("q=2 printed Fourier counterexample vanished")

    if _ramanujan(2, 1) != -1 or _ramanujan(2, 2) != 1:
        raise CheckFailure("q=2 Ramanujan fixture changed")
    corrected_frequency_two = -1 + 2
    if corrected_frequency_two != _ramanujan(2, 2):
        raise CheckFailure("corrected d-phase does not recover r_2(2)")

    correct_vec = _kloosterman_vector(2, 1, 5)
    printed_vec = _kloosterman_vector(3, 1, 5)
    if correct_vec != (0, 0, 2, 2, 0):
        raise CheckFailure("correct c=5 Kloosterman vector changed")
    if printed_vec != (0, 2, 0, 0, 2):
        raise CheckFailure("printed c=5 Kloosterman vector changed")
    if correct_vec == printed_vec:
        raise CheckFailure("missing d phase became invisible")

    primes = (5, 7, 11)
    weights = (Fraction(2), Fraction(3), Fraction(5))
    normalizer = sum(w * (q - 1) for q, w in zip(primes, weights))
    zero_sum = sum(
        w * sum(d * _mobius(q // d) for d in _divisors(q))
        for q, w in zip(primes, weights)
    )
    if normalizer != zero_sum or normalizer == 0:
        raise CheckFailure("full-ensemble zero coefficient changed")

    for n in range(-30, 31):
        direct = sum(w * _ramanujan(q, n) for q, w in zip(primes, weights))
        grouped = -sum(weights) + sum(
            w * q for q, w in zip(primes, weights) if n % q == 0
        )
        if direct != grouped:
            raise CheckFailure("prime-shell grouped kernel changed")

    if tuple(_ramanujan(6, n) for n in range(4)) != (2, 1, -1, -2):
        raise CheckFailure("composite Ramanujan fixture changed")

    representations_490 = ((5, 98), (7, 70))
    if any(p * t != 490 for p, t in representations_490):
        raise CheckFailure("factorable multiplicity fixture changed")
    if len({p * t for p, t in representations_490}) != 1:
        raise CheckFailure("factorable duplicate-q fixture changed")

    q1 = Fraction(4, 21)
    q2 = Fraction(8, 21)
    q = q1 + q2
    l_exp = 2 * q
    delta = Fraction(-1)
    l2_squared = 2 * q - 2 * l_exp - delta
    l2 = l2_squared / 2
    crude_error = Fraction(3, 2) + l2
    theta = -l2 - Fraction(1, 400)
    if (q, l_exp, l2_squared, l2, crude_error, theta) != (
        Fraction(4, 7),
        Fraction(8, 7),
        Fraction(-1, 7),
        Fraction(-1, 14),
        Fraction(10, 7),
        Fraction(193, 2800),
    ):
        raise CheckFailure("factorable exponent ledger changed")

    c_exp = Fraction(133, 400)
    bp_cell = c_exp / 32
    bp_margin = bp_cell - Fraction(1, 400)
    if bp_cell != Fraction(133, 12800):
        raise CheckFailure("BP top-cell exponent changed")
    if bp_margin != Fraction(101, 12800):
        raise CheckFailure("BP top-cell margin changed")

    source_325 = (
        Fraction(41, 42),
        Fraction(41, 42),
        Fraction(19, 21),
        Fraction(41, 42),
        Fraction(37, 42),
    )
    source_341 = (
        Fraction(41, 42),
        Fraction(20, 21),
        Fraction(41, 42),
    )

    return {
        "q2_printed": "-H1+2H2",
        "q2_corrected": "-H1",
        "kloosterman_correct": list(correct_vec),
        "kloosterman_printed": list(printed_vec),
        "zero_normalizer": str(normalizer),
        "composite_c6": [_ramanujan(6, n) for n in range(4)],
        "factorable_representations_490": [list(pair) for pair in representations_490],
        "factor_q": str(q),
        "factor_L": str(l_exp),
        "factor_l2_squared_upper_bound": str(l2_squared),
        "factor_l2_upper_bound": str(l2),
        "factor_crude_error": str(crude_error),
        "factor_theta": str(theta),
        "bp_top_cell": str(bp_cell),
        "bp_margin": str(bp_margin),
        "source_325": [str(value) for value in source_325],
        "source_341": [str(value) for value in source_341],
    }


def changed_value(value: Any) -> Any:
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if type(value) is str:
        return value + "_MUTATED"
    raise CheckFailure("unsupported mutation type")


def wrong_type(value: Any) -> Any:
    if type(value) is bool:
        return "false" if not value else "true"
    if type(value) is int:
        return str(value)
    if type(value) is str:
        return [value]
    raise CheckFailure("unsupported wrong-type mutation")


def must_reject(
    action: Any, label: str, _check_failure: Any = CheckFailure
) -> None:
    try:
        action()
    except _check_failure:
        return
    raise CheckFailure(f"mutation escaped: {label}")


def run_contract_mutations(
    _literal_contract: Any = literal_contract,
    _validate_contract: Any = validate_contract,
    _wrong_type: Any = wrong_type,
    _changed_value: Any = changed_value,
    _must_reject: Any = must_reject,
) -> int:
    base = _literal_contract()
    labels: list[str] = []
    for key in tuple(base):
        missing = dict(base)
        del missing[key]
        label = f"contract_missing_{key}"
        _must_reject(lambda c=missing: _validate_contract(c), label)
        labels.append(label)

        typed = dict(base)
        typed[key] = _wrong_type(base[key])
        label = f"contract_type_{key}"
        _must_reject(lambda c=typed: _validate_contract(c), label)
        labels.append(label)

        changed = dict(base)
        changed[key] = _changed_value(base[key])
        label = f"contract_value_{key}"
        _must_reject(lambda c=changed: _validate_contract(c), label)
        labels.append(label)

    extra = dict(base)
    extra["UNKNOWN_FALSE_PROMOTION"] = "PROVED"
    _must_reject(lambda: _validate_contract(extra), "contract_extra")
    labels.append("contract_extra")
    if len(labels) != len(set(labels)):
        raise CheckFailure("contract mutation labels duplicated")
    return len(labels)


def run_registry_mutations(
    _literal_registry_items: Any = literal_registry_items,
    _registry_digest: Any = registry_digest,
    _validate_registry: Any = validate_registry,
    _must_reject: Any = must_reject,
) -> int:
    base = _literal_registry_items()
    labels: list[str] = []
    for index, (key, value) in enumerate(base):
        changed = list(base)
        changed[index] = (key, value + "_MUTATED")
        digest = _registry_digest(changed)
        label = f"registry_value_{index + 1:02d}"
        _must_reject(
            lambda c=tuple(changed), d=digest: _validate_registry(c, d), label
        )
        labels.append(label)

        missing = base[:index] + base[index + 1 :]
        digest = _registry_digest(missing)
        label = f"registry_missing_{index + 1:02d}"
        _must_reject(lambda c=missing, d=digest: _validate_registry(c, d), label)
        labels.append(label)

        replacement = list(base)
        replacement[index] = (f"UNKNOWN_KEY_{index + 1:02d}", value)
        digest = _registry_digest(replacement)
        label = f"registry_key_{index + 1:02d}"
        _must_reject(
            lambda c=tuple(replacement), d=digest: _validate_registry(c, d), label
        )
        labels.append(label)

    extra = base + (("FALSE_RELEASE", "TPC_207_TRUE"),)
    _must_reject(
        lambda: _validate_registry(extra, _registry_digest(extra)),
        "registry_extra_false_release",
    )
    labels.append("registry_extra_false_release")

    _must_reject(
        lambda: _validate_registry(base, "0" * 64),
        "registry_wrong_digest",
    )
    labels.append("registry_wrong_digest")

    if len(labels) != len(set(labels)):
        raise CheckFailure("registry mutation labels duplicated")
    return len(labels)


def run_source_mutations(
    _source_candidate: Any = source_candidate,
    _validate_source_candidate: Any = validate_source_candidate,
    _must_reject: Any = must_reject,
) -> int:
    base = _source_candidate()
    labels: list[str] = []
    for key in tuple(base):
        changed = dict(base)
        changed[key] = base[key] + "_MUTATED"
        label = f"source_{key}"
        _must_reject(lambda c=changed: _validate_source_candidate(c), label)
        labels.append(label)
    extra = dict(base)
    extra["unlocked_source"] = "false"
    _must_reject(lambda: _validate_source_candidate(extra), "source_extra")
    labels.append("source_extra")
    if len(labels) != len(set(labels)):
        raise CheckFailure("source mutation labels duplicated")
    return len(labels)


def validate_result_semantics(
    result: Mapping[str, Any], _exact_type: Any = exact_type
) -> None:
    hard = {
        "arithmetic_advance": False,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
        "maximum_claim": (
            "EXACT_L0_CORRECTED_JUTILA_FOURIER_AND_FACTORIZABLE_AUXILIARY_"
            "EMITTER_WITH_SOURCE_TRANSFER_FIREWALLS"
        ),
    }
    if set(result) != set(hard):
        raise CheckFailure("result semantic key set changed")
    for key, expected in hard.items():
        value = result[key]
        if not _exact_type(value, expected) or value != expected:
            raise CheckFailure(f"result semantic {key} changed")


def run_semantic_mutations(
    _validate_result_semantics: Any = validate_result_semantics,
    _changed_value: Any = changed_value,
    _must_reject: Any = must_reject,
) -> int:
    base = {
        "arithmetic_advance": False,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
        "maximum_claim": MAXIMUM_CLAIM,
    }
    labels: list[str] = []
    for key in tuple(base):
        changed = dict(base)
        changed[key] = _changed_value(base[key])
        label = f"semantic_value_{key}"
        _must_reject(lambda c=changed: _validate_result_semantics(c), label)
        labels.append(label)

        missing = dict(base)
        del missing[key]
        label = f"semantic_missing_{key}"
        _must_reject(lambda c=missing: _validate_result_semantics(c), label)
        labels.append(label)

    extra = dict(base)
    extra["numbered_release"] = True
    _must_reject(lambda: _validate_result_semantics(extra), "semantic_extra")
    labels.append("semantic_extra")
    if len(labels) != len(set(labels)):
        raise CheckFailure("semantic mutation labels duplicated")
    return len(labels)


def validate_full_result(result: Mapping[str, Any]) -> None:
    hard = {
        "check": True,
        "contract_fields": 40,
        "contract_mutations": 121,
        "registry_rows": 54,
        "registry_mutations": 164,
        "registry_sha256": (
            "3781892c4b9a830f7bb0f7e1a73f97b2283245e42f02f7db4904d45d18391d42"
        ),
        "source_lock_mutations": 8,
        "semantic_mutations": 13,
        "q2_printed": "-H1+2H2",
        "q2_corrected": "-H1",
        "kloosterman_correct": [0, 0, 2, 2, 0],
        "kloosterman_printed": [0, 2, 0, 0, 2],
        "factor_l2_upper_bound": "-1/14",
        "factor_theta": "193/2800",
        "bp_margin": "101/12800",
        "arithmetic_advance": False,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
        "maximum_claim": (
            "EXACT_L0_CORRECTED_JUTILA_FOURIER_AND_FACTORIZABLE_AUXILIARY_"
            "EMITTER_WITH_SOURCE_TRANSFER_FIREWALLS"
        ),
    }
    if set(result) != set(hard):
        raise CheckFailure("full result key set changed")
    for key, expected in hard.items():
        value = result[key]
        if type(value) is not type(expected) or value != expected:
            raise CheckFailure(f"full result {key} changed")


def run_check(
    _literal_contract: Any = literal_contract,
    _validate_contract: Any = validate_contract,
    _literal_registry_items: Any = literal_registry_items,
    _validate_registry: Any = validate_registry,
    _expected_registry_sha256: str = EXPECTED_REGISTRY_SHA256,
    _source_candidate: Any = source_candidate,
    _validate_source_candidate: Any = validate_source_candidate,
    _finite_fixtures: Any = finite_fixtures,
    _run_contract_mutations: Any = run_contract_mutations,
    _run_registry_mutations: Any = run_registry_mutations,
    _run_source_mutations: Any = run_source_mutations,
    _run_semantic_mutations: Any = run_semantic_mutations,
    _validate_result_semantics: Any = validate_result_semantics,
    _validate_full_result: Any = validate_full_result,
) -> dict[str, Any]:
    contract = _literal_contract()
    _validate_contract(contract)
    registry = _literal_registry_items()
    _validate_registry(registry, _expected_registry_sha256)
    _validate_source_candidate(_source_candidate())
    fixtures = _finite_fixtures()
    contract_mutations = _run_contract_mutations()
    registry_mutations = _run_registry_mutations()
    source_mutations = _run_source_mutations()
    semantic_mutations = _run_semantic_mutations()
    semantics = {
        "arithmetic_advance": False,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
        "maximum_claim": (
            "EXACT_L0_CORRECTED_JUTILA_FOURIER_AND_FACTORIZABLE_AUXILIARY_"
            "EMITTER_WITH_SOURCE_TRANSFER_FIREWALLS"
        ),
    }
    _validate_result_semantics(semantics)
    result = {
        "check": True,
        "contract_fields": len(contract),
        "contract_mutations": contract_mutations,
        "registry_rows": len(registry),
        "registry_mutations": registry_mutations,
        "registry_sha256": _expected_registry_sha256,
        "source_lock_mutations": source_mutations,
        "semantic_mutations": semantic_mutations,
        "q2_printed": fixtures["q2_printed"],
        "q2_corrected": fixtures["q2_corrected"],
        "kloosterman_correct": fixtures["kloosterman_correct"],
        "kloosterman_printed": fixtures["kloosterman_printed"],
        "factor_l2_upper_bound": fixtures["factor_l2_upper_bound"],
        "factor_theta": fixtures["factor_theta"],
        "bp_margin": fixtures["bp_margin"],
        **semantics,
    }
    _validate_full_result(result)
    return result


def _seal_noarg_runner(runner: Any) -> Any:
    def sealed() -> dict[str, Any]:
        return runner()

    return sealed


run_check = _seal_noarg_runner(run_check)
del _seal_noarg_runner


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(
    argv: Iterable[str] | None = None,
    _parse_args: Any = parse_args,
    _run_check: Any = run_check,
) -> int:
    args = _parse_args(argv)
    if not args.check:
        raise CheckFailure("explicit --check is required")
    result = _run_check()
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


def _seal_main(runner: Any) -> Any:
    def sealed(argv: Iterable[str] | None = None) -> int:
        return runner(argv)

    return sealed


main = _seal_main(main)
del _seal_main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CheckFailure as exc:
        print(f"CheckFailure: {exc}", file=__import__("sys").stderr)
        raise SystemExit(1)
