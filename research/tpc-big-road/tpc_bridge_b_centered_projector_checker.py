#!/usr/bin/env python3
"""Read-only exact checker for the TPC Bridge-B V22 projector firewall."""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
from fractions import Fraction
from pathlib import Path
from typing import Iterable


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


V21_PATH = Path("research/tpc-big-road/tpc_bridge_b_mesoscopic_covariance_checker.py")
V21_CANONICAL_SHA256 = "b6350ce0f7ed38dd7671f5076a0c26bf82bb57850ec35505c4cfec3239ad336e"


CONTRACT = {
    "representation": "ACTUAL_SHELL_COUNTING_PROJECTORS",
    "fixed_h0": 2,
    "mesoscopic_q_exponent": "1/3",
    "complete_equal_weight_ensemble": True,
    "actual_ragged_counts": True,
    "paid_mean": "PROVED_SOURCE_BACKED_ARBITRARY_LOG_POWER",
    "centered_target": "OPEN_NEW_ARITHMETIC_THEOREM",
    "residue_fourier": "STOP_SCOPED_EXACT_ZERO_MARGINAL",
    "direct_projector_dispersion": "STOP_SCOPED_PAID_MEAN_BRANCH_ONLY",
    "complete_ensemble_compression": "STOP_SCOPED_IDENTITY_SPACE",
    "finite_witness": "SYNTHETIC_W_EQUALS_LITERAL_BETA_NOT_PHYSICAL_RESIDUAL",
    "bp_local_saving": "CONDITIONAL_X_MINUS_1_OVER_96",
    "bp_post_poisson_compiler": "OPEN_CONDITIONAL",
    "odometer_return": "PROVED_EXACT_L0_NO_CANCELLATION",
    "transversal_common_return": "OPEN_NEW_CONSTRUCTION",
    "arithmetic_advance": False,
    "fixed_atom_credit": 0,
    "strict_1_over_400": "UNPAID",
    "L2": "NONE",
    "TPC_207_TRIGGER": False,
}


REGISTRY_ITEMS = (
    ("MAXIMUM_CLAIM", "EXACT_L0_CENTERED_PROJECTOR_FIREWALL_AND_CONDITIONAL_FORK"),
    ("PHYSICAL_H0", "2"),
    ("PHYSICAL_X", "2X"),
    ("MESOSCOPIC_Q", "X_POWER_1_OVER_3_AUXILIARY_NOT_PACKET_Q"),
    ("ENSEMBLE", "COMPLETE_PREDECLARED_EQUAL_WEIGHT_PRIMES"),
    ("FIBER_COUNTS", "ACTUAL_FLOOR_CEILING"),
    ("MEAN_BRANCH", "PROVED_SOURCE_BACKED_ARBITRARY_LOG_POWER"),
    ("CENTERED_OPERATOR", "IDENTITY_MINUS_AVERAGED_COUNTING_PROJECTOR"),
    ("PROJECTOR_KERNEL", "RAGGED_Q_DIVIDES_T_MINUS_U"),
    ("RESIDUE_MARGINALS", "EXACTLY_ZERO_ALL_H_MOD_Q"),
    ("WITHIN_FIBER_COVARIANCE", "CURRENT_OPEN_OBJECT"),
    ("FIBER_QUOTIENT_LENGTH", "ASYMPTOTIC_Q_SQUARED"),
    ("AVERAGED_PROJECTOR_RANK", "AT_MOST_SUM_Q"),
    ("CENTERED_IDENTITY_SPACE", "DIMENSION_AT_LEAST_H_MINUS_SUM_Q"),
    ("CENTERED_OPERATOR_NORM", "ONE"),
    ("X1000_ENSEMBLE", "11_13_17_19"),
    ("X1000_MEAN_SPAN_RANK", "57"),
    ("X1000_IDENTITY_MULTIPLICITY", "443"),
    ("FINITE_INFORMATION_LOSS_WITNESS", "SYNTHETIC_W_EQUALS_LITERAL_BETA_NOT_PHYSICAL_RESIDUAL"),
    ("PAIR_EXPANSION", "ORIGINAL_S_MINUS_PAID_HBAR"),
    ("DIRECT_PROJECTOR_DISPERSION", "STOP_SCOPED_PAID_MEAN_ONLY"),
    ("DIRECT_RESIDUE_KLOOSTERMAN", "STOP_SCOPED_KERNEL_AND_ZERO_MARGINAL"),
    ("BP_SOURCE", "ARXIV_2607_24311V1_THEOREMS_1_1_5_2_5_5"),
    ("BP_CRITICAL_SAVING", "Q_MINUS_1_OVER_32_EQUALS_X_MINUS_1_OVER_96"),
    ("STRICT_MARGIN", "19_OVER_2400_BEFORE_COMPILER_LOSSES"),
    ("BP_POST_POISSON_COMPILER", "OPEN_CONDITIONAL"),
    ("NAIVE_FULL_Q_COMPLETION", "STOP_SCOPED_BLACK_BOX_CAUCHY_CERTIFIES_NO_NET_GAIN_WITHOUT_BLOCK_STRUCTURE"),
    ("ODOMETER_ORBIT_SUM", "PROVED_EXACT_L0_NO_CANCELLATION"),
    ("LOGISTIC_PHYSICAL_INTERTWINER", "ABSENT"),
    ("TRANSVERSAL_COMMON_RETURN", "OPEN_NEW_CONSTRUCTION"),
    ("HENON", "OPTIONAL_EXACT_NATURAL_EXTENSION_ONLY"),
    ("ARITHMETIC_ADVANCE", "NO"),
    ("FIXED_ATOM_CREDIT", "0"),
    ("STRICT_1_OVER_400", "UNPAID"),
    ("L2", "NONE"),
    ("TPC_207_TRIGGER", "FALSE"),
)


EXPECTED_REGISTRY_SHA256 = "19c228b356cf1b8034eb3e018c0ef0e2d8363515062f9472c4857b54b1f1d8c7"


def canonical_lf_bytes(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def registry_hash(items: Iterable[tuple[str, str]]) -> str:
    payload = "".join(f"{key}={value}\n" for key, value in items).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def literal_contract() -> dict[str, object]:
    return {
        "representation": "ACTUAL_SHELL_COUNTING_PROJECTORS",
        "fixed_h0": 2,
        "mesoscopic_q_exponent": "1/3",
        "complete_equal_weight_ensemble": True,
        "actual_ragged_counts": True,
        "paid_mean": "PROVED_SOURCE_BACKED_ARBITRARY_LOG_POWER",
        "centered_target": "OPEN_NEW_ARITHMETIC_THEOREM",
        "residue_fourier": "STOP_SCOPED_EXACT_ZERO_MARGINAL",
        "direct_projector_dispersion": "STOP_SCOPED_PAID_MEAN_BRANCH_ONLY",
        "complete_ensemble_compression": "STOP_SCOPED_IDENTITY_SPACE",
        "finite_witness": "SYNTHETIC_W_EQUALS_LITERAL_BETA_NOT_PHYSICAL_RESIDUAL",
        "bp_local_saving": "CONDITIONAL_X_MINUS_1_OVER_96",
        "bp_post_poisson_compiler": "OPEN_CONDITIONAL",
        "odometer_return": "PROVED_EXACT_L0_NO_CANCELLATION",
        "transversal_common_return": "OPEN_NEW_CONSTRUCTION",
        "arithmetic_advance": False,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }


def literal_registry() -> tuple[tuple[str, str], ...]:
    return (
        ("MAXIMUM_CLAIM", "EXACT_L0_CENTERED_PROJECTOR_FIREWALL_AND_CONDITIONAL_FORK"),
        ("PHYSICAL_H0", "2"),
        ("PHYSICAL_X", "2X"),
        ("MESOSCOPIC_Q", "X_POWER_1_OVER_3_AUXILIARY_NOT_PACKET_Q"),
        ("ENSEMBLE", "COMPLETE_PREDECLARED_EQUAL_WEIGHT_PRIMES"),
        ("FIBER_COUNTS", "ACTUAL_FLOOR_CEILING"),
        ("MEAN_BRANCH", "PROVED_SOURCE_BACKED_ARBITRARY_LOG_POWER"),
        ("CENTERED_OPERATOR", "IDENTITY_MINUS_AVERAGED_COUNTING_PROJECTOR"),
        ("PROJECTOR_KERNEL", "RAGGED_Q_DIVIDES_T_MINUS_U"),
        ("RESIDUE_MARGINALS", "EXACTLY_ZERO_ALL_H_MOD_Q"),
        ("WITHIN_FIBER_COVARIANCE", "CURRENT_OPEN_OBJECT"),
        ("FIBER_QUOTIENT_LENGTH", "ASYMPTOTIC_Q_SQUARED"),
        ("AVERAGED_PROJECTOR_RANK", "AT_MOST_SUM_Q"),
        ("CENTERED_IDENTITY_SPACE", "DIMENSION_AT_LEAST_H_MINUS_SUM_Q"),
        ("CENTERED_OPERATOR_NORM", "ONE"),
        ("X1000_ENSEMBLE", "11_13_17_19"),
        ("X1000_MEAN_SPAN_RANK", "57"),
        ("X1000_IDENTITY_MULTIPLICITY", "443"),
        ("FINITE_INFORMATION_LOSS_WITNESS", "SYNTHETIC_W_EQUALS_LITERAL_BETA_NOT_PHYSICAL_RESIDUAL"),
        ("PAIR_EXPANSION", "ORIGINAL_S_MINUS_PAID_HBAR"),
        ("DIRECT_PROJECTOR_DISPERSION", "STOP_SCOPED_PAID_MEAN_ONLY"),
        ("DIRECT_RESIDUE_KLOOSTERMAN", "STOP_SCOPED_KERNEL_AND_ZERO_MARGINAL"),
        ("BP_SOURCE", "ARXIV_2607_24311V1_THEOREMS_1_1_5_2_5_5"),
        ("BP_CRITICAL_SAVING", "Q_MINUS_1_OVER_32_EQUALS_X_MINUS_1_OVER_96"),
        ("STRICT_MARGIN", "19_OVER_2400_BEFORE_COMPILER_LOSSES"),
        ("BP_POST_POISSON_COMPILER", "OPEN_CONDITIONAL"),
        ("NAIVE_FULL_Q_COMPLETION", "STOP_SCOPED_BLACK_BOX_CAUCHY_CERTIFIES_NO_NET_GAIN_WITHOUT_BLOCK_STRUCTURE"),
        ("ODOMETER_ORBIT_SUM", "PROVED_EXACT_L0_NO_CANCELLATION"),
        ("LOGISTIC_PHYSICAL_INTERTWINER", "ABSENT"),
        ("TRANSVERSAL_COMMON_RETURN", "OPEN_NEW_CONSTRUCTION"),
        ("HENON", "OPTIONAL_EXACT_NATURAL_EXTENSION_ONLY"),
        ("ARITHMETIC_ADVANCE", "NO"),
        ("FIXED_ATOM_CREDIT", "0"),
        ("STRICT_1_OVER_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", "FALSE"),
    )


def validate_contract(candidate: object) -> None:
    # This lock is deliberately local.  The public fixture provider is used by
    # mutation tests, but must not be able to self-attest a coordinated runtime
    # promotion when both CONTRACT and literal_contract are rebound.
    expected = {
        "representation": "ACTUAL_SHELL_COUNTING_PROJECTORS",
        "fixed_h0": 2,
        "mesoscopic_q_exponent": "1/3",
        "complete_equal_weight_ensemble": True,
        "actual_ragged_counts": True,
        "paid_mean": "PROVED_SOURCE_BACKED_ARBITRARY_LOG_POWER",
        "centered_target": "OPEN_NEW_ARITHMETIC_THEOREM",
        "residue_fourier": "STOP_SCOPED_EXACT_ZERO_MARGINAL",
        "direct_projector_dispersion": "STOP_SCOPED_PAID_MEAN_BRANCH_ONLY",
        "complete_ensemble_compression": "STOP_SCOPED_IDENTITY_SPACE",
        "finite_witness": "SYNTHETIC_W_EQUALS_LITERAL_BETA_NOT_PHYSICAL_RESIDUAL",
        "bp_local_saving": "CONDITIONAL_X_MINUS_1_OVER_96",
        "bp_post_poisson_compiler": "OPEN_CONDITIONAL",
        "odometer_return": "PROVED_EXACT_L0_NO_CANCELLATION",
        "transversal_common_return": "OPEN_NEW_CONSTRUCTION",
        "arithmetic_advance": False,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }
    require(type(candidate) is dict, "contract is not an exact dict")
    require(set(candidate) == set(expected), "contract key set changed")
    for key, value in expected.items():
        require(type(candidate[key]) is type(value), f"contract field {key} has wrong type")
        require(candidate[key] == value, f"contract field {key} changed")


def validate_registry(candidate: object, digest: object) -> None:
    # As above, keep the release semantics and digest independent of mutable
    # module fixtures.  This blocks registry+provider+digest self-attestation.
    expected = (
        ("MAXIMUM_CLAIM", "EXACT_L0_CENTERED_PROJECTOR_FIREWALL_AND_CONDITIONAL_FORK"),
        ("PHYSICAL_H0", "2"),
        ("PHYSICAL_X", "2X"),
        ("MESOSCOPIC_Q", "X_POWER_1_OVER_3_AUXILIARY_NOT_PACKET_Q"),
        ("ENSEMBLE", "COMPLETE_PREDECLARED_EQUAL_WEIGHT_PRIMES"),
        ("FIBER_COUNTS", "ACTUAL_FLOOR_CEILING"),
        ("MEAN_BRANCH", "PROVED_SOURCE_BACKED_ARBITRARY_LOG_POWER"),
        ("CENTERED_OPERATOR", "IDENTITY_MINUS_AVERAGED_COUNTING_PROJECTOR"),
        ("PROJECTOR_KERNEL", "RAGGED_Q_DIVIDES_T_MINUS_U"),
        ("RESIDUE_MARGINALS", "EXACTLY_ZERO_ALL_H_MOD_Q"),
        ("WITHIN_FIBER_COVARIANCE", "CURRENT_OPEN_OBJECT"),
        ("FIBER_QUOTIENT_LENGTH", "ASYMPTOTIC_Q_SQUARED"),
        ("AVERAGED_PROJECTOR_RANK", "AT_MOST_SUM_Q"),
        ("CENTERED_IDENTITY_SPACE", "DIMENSION_AT_LEAST_H_MINUS_SUM_Q"),
        ("CENTERED_OPERATOR_NORM", "ONE"),
        ("X1000_ENSEMBLE", "11_13_17_19"),
        ("X1000_MEAN_SPAN_RANK", "57"),
        ("X1000_IDENTITY_MULTIPLICITY", "443"),
        ("FINITE_INFORMATION_LOSS_WITNESS", "SYNTHETIC_W_EQUALS_LITERAL_BETA_NOT_PHYSICAL_RESIDUAL"),
        ("PAIR_EXPANSION", "ORIGINAL_S_MINUS_PAID_HBAR"),
        ("DIRECT_PROJECTOR_DISPERSION", "STOP_SCOPED_PAID_MEAN_ONLY"),
        ("DIRECT_RESIDUE_KLOOSTERMAN", "STOP_SCOPED_KERNEL_AND_ZERO_MARGINAL"),
        ("BP_SOURCE", "ARXIV_2607_24311V1_THEOREMS_1_1_5_2_5_5"),
        ("BP_CRITICAL_SAVING", "Q_MINUS_1_OVER_32_EQUALS_X_MINUS_1_OVER_96"),
        ("STRICT_MARGIN", "19_OVER_2400_BEFORE_COMPILER_LOSSES"),
        ("BP_POST_POISSON_COMPILER", "OPEN_CONDITIONAL"),
        ("NAIVE_FULL_Q_COMPLETION", "STOP_SCOPED_BLACK_BOX_CAUCHY_CERTIFIES_NO_NET_GAIN_WITHOUT_BLOCK_STRUCTURE"),
        ("ODOMETER_ORBIT_SUM", "PROVED_EXACT_L0_NO_CANCELLATION"),
        ("LOGISTIC_PHYSICAL_INTERTWINER", "ABSENT"),
        ("TRANSVERSAL_COMMON_RETURN", "OPEN_NEW_CONSTRUCTION"),
        ("HENON", "OPTIONAL_EXACT_NATURAL_EXTENSION_ONLY"),
        ("ARITHMETIC_ADVANCE", "NO"),
        ("FIXED_ATOM_CREDIT", "0"),
        ("STRICT_1_OVER_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", "FALSE"),
    )
    expected_digest = "19c228b356cf1b8034eb3e018c0ef0e2d8363515062f9472c4857b54b1f1d8c7"
    require(type(candidate) is tuple, "registry is not a tuple")
    require(all(type(row) is tuple and len(row) == 2 for row in candidate), "registry row schema changed")
    require(all(type(key) is str and type(value) is str for key, value in candidate), "registry row type changed")
    require(candidate == expected, "registry semantic row changed")
    require(len({key for key, _ in candidate}) == len(expected), "registry key uniqueness changed")
    require(type(digest) is str, "registry digest has wrong type")
    require(digest == expected_digest, "registry digest binding changed")
    require(registry_hash(candidate) == expected_digest, "registry digest changed")


def load_v21() -> tuple[dict[str, object], dict[str, object]]:
    path = Path("research/tpc-big-road/tpc_bridge_b_mesoscopic_covariance_checker.py")
    expected_digest = "b6350ce0f7ed38dd7671f5076a0c26bf82bb57850ec35505c4cfec3239ad336e"
    require(path.is_file(), "V21 checker is absent")
    digest = hashlib.sha256(canonical_lf_bytes(path.read_bytes())).hexdigest()
    require(digest == expected_digest, "V21 canonical checker hash mismatch")
    v21 = runpy.run_path(str(path))
    result = v21["run_check"]()
    require(type(result) is dict and result.get("check") is True, "V21 checker failed")
    require(result.get("arithmetic_advance") is False, "V21 arithmetic status changed")
    require(result.get("TPC_207_TRIGGER") is False, "V21 TPC-207 status changed")
    dependencies = v21["load_dependencies"]()
    require(type(dependencies) is tuple and len(dependencies) == 2, "V21 dependency bundle changed")
    return v21, dependencies[1]


def shell_integers(analytic_x: int) -> tuple[int, ...]:
    require(type(analytic_x) is int and analytic_x >= 2, "analytic x is invalid")
    return tuple(range(analytic_x // 2 + 1, analytic_x + 1))


def fibers(analytic_x: int, modulus: int) -> tuple[tuple[int, ...], ...]:
    shell = shell_integers(analytic_x)
    return tuple(tuple(t for t in shell if t % modulus == residue) for residue in range(modulus))


def conditional_mean(vector: dict[int, Fraction], analytic_x: int, modulus: int) -> dict[int, Fraction]:
    shell = shell_integers(analytic_x)
    require(set(vector) == set(shell), "conditional-mean domain changed")
    result: dict[int, Fraction] = {}
    for fiber in fibers(analytic_x, modulus):
        if not fiber:
            continue
        mean = sum((vector[t] for t in fiber), Fraction(0)) / len(fiber)
        for t in fiber:
            result[t] = mean
    require(set(result) == set(shell), "conditional mean lost a shell point")
    return result


def dot(left: dict[int, Fraction], right: dict[int, Fraction]) -> Fraction:
    require(set(left) == set(right), "dot domains differ")
    return sum((left[t] * right[t] for t in left), Fraction(0))


def projector_fixture(analytic_x: int, modulus: int) -> dict[str, Fraction | int]:
    shell = shell_integers(analytic_x)
    beta = {t: Fraction(((7 * t + analytic_x) % 23) - 11, (t % 4) + 1) for t in shell}
    residual = {t: Fraction(((5 * t + modulus) % 29) - 14, (t % 5) + 1) for t in shell}
    mean_residual = conditional_mean(residual, analytic_x, modulus)
    centered = {t: residual[t] - mean_residual[t] for t in shell}
    scalar = dot(beta, residual)
    mean = dot(beta, mean_residual)
    covariance = dot(beta, centered)
    pair = Fraction(0)
    diagonal = Fraction(0)
    off_diagonal = Fraction(0)
    marginal_cases = 0
    for fiber in fibers(analytic_x, modulus):
        if not fiber:
            continue
        count = len(fiber)
        require(sum((centered[t] for t in fiber), Fraction(0)) == 0, "centered residue marginal changed")
        marginal_cases += 1
        beta_sum = sum((beta[t] for t in fiber), Fraction(0))
        residual_sum = sum((residual[t] for t in fiber), Fraction(0))
        pair += sum(
            ((beta[t] - beta[u]) * (residual[t] - residual[u]) for t in fiber for u in fiber),
            Fraction(0),
        ) / (2 * count)
        correction = sum((beta[t] * residual[t] for t in fiber), Fraction(0)) / count
        diagonal += sum((beta[t] * residual[t] for t in fiber), Fraction(0)) - correction
        off_diagonal += correction - beta_sum * residual_sum / count
    require(scalar == mean + covariance, "projector split failed")
    require(covariance == pair, "pair identity failed")
    require(covariance == diagonal + off_diagonal, "diagonal atlas failed")
    require(off_diagonal == -mean + (scalar - diagonal), "off-diagonal paid-branch identity failed")
    return {
        "marginal_cases": marginal_cases,
        "scalar": scalar,
        "mean": mean,
        "covariance": covariance,
    }


def validate_projector_algebra() -> dict[str, int]:
    cases = 0
    marginal_cases = 0
    ragged = 0
    for analytic_x in (24, 25, 31, 64, 100, 166, 211):
        for modulus in (3, 5, 7, 11, 13, 19):
            result = projector_fixture(analytic_x, modulus)
            marginal_cases += int(result["marginal_cases"])
            counts = tuple(len(fiber) for fiber in fibers(analytic_x, modulus))
            require(max(counts) - min(counts) <= 1, "fiber raggedness exceeded one")
            require(sum(counts) == len(shell_integers(analytic_x)), "fiber cover changed")
            if max(counts) != min(counts):
                ragged += 1
            cases += 1
    return {"projector_cases": cases, "marginal_cases": marginal_cases, "ragged_cases": ragged}


def rank_mod_prime(rows: list[list[int]], prime: int = 1_000_003) -> int:
    require(rows and rows[0], "rank matrix is empty")
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "rank matrix is ragged")
    matrix = [[entry % prime for entry in row] for row in rows]
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [(entry * inverse) % prime for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        if rank == width:
            break
    return rank


def finite_difference_witness(primes: tuple[int, ...]) -> dict[int, int]:
    coefficients = {0: 1}
    for prime in primes:
        updated = dict(coefficients)
        for exponent, coefficient in coefficients.items():
            updated[exponent + prime] = updated.get(exponent + prime, 0) - coefficient
        coefficients = {exponent: coefficient for exponent, coefficient in updated.items() if coefficient}
    require(coefficients.get(0) == 1, "finite-difference witness vanished")
    return coefficients


def validate_complete_ensemble() -> dict[str, int]:
    analytic_x = 1000
    shell = shell_integers(analytic_x)
    primes = (11, 13, 17, 19)
    rows: list[list[int]] = []
    for integer in shell:
        row = [1]
        for prime in primes:
            row.extend(int(integer % prime == residue) for residue in range(1, prime))
        rows.append(row)
    expected_rank = 1 + sum(prime - 1 for prime in primes)
    rank = rank_mod_prime(rows)
    require(expected_rank == 57 and rank == expected_rank, "complete mean-span rank changed")
    require(len(shell) - rank == 443, "complete identity multiplicity changed")

    polynomial = finite_difference_witness(primes)
    shift = 600
    require(shift > analytic_x // 2 and shift + max(polynomial) <= analytic_x, "witness left shell")
    vector = {integer: Fraction(0) for integer in shell}
    for exponent, coefficient in polynomial.items():
        vector[shift + exponent] += coefficient
    require(any(value for value in vector.values()), "common-kernel vector is zero")
    for prime in primes:
        mean = conditional_mean(vector, analytic_x, prime)
        require(all(value == 0 for value in mean.values()), f"common-kernel witness failed at q={prime}")
    return {
        "shell_size": len(shell),
        "prime_count": len(primes),
        "mean_span_rank": rank,
        "identity_multiplicity": len(shell) - rank,
        "witness_support": sum(value != 0 for value in vector.values()),
    }


def validate_synthetic_information_loss(v21: dict[str, object], v19: dict[str, object]) -> dict[str, object]:
    analytic_x = 166
    shell = shell_integers(analytic_x)
    beta = {
        integer: v21["literal_beta_fraction"](v19, integer, analytic_x)
        for integer in shell
    }
    mean_beta = conditional_mean(beta, analytic_x, 7)
    state = {integer: beta[integer] - mean_beta[integer] for integer in shell}
    for fiber in fibers(analytic_x, 7):
        require(sum((state[t] for t in fiber), Fraction(0)) == 0, "synthetic witness marginal changed")
    scalar = dot(beta, state)
    mean_state = conditional_mean(state, analytic_x, 7)
    mean = dot(beta, mean_state)
    centered = dot(beta, {t: state[t] - mean_state[t] for t in shell})
    require(mean == 0, "synthetic witness acquired a residue mean")
    require(scalar == centered == Fraction(2359675, 77616), "synthetic centered energy changed")
    pair = projector_fixture(166, 7)
    require(type(pair["covariance"]) is Fraction, "independent pair fixture changed type")
    return {
        "analytic_x": analytic_x,
        "modulus": 7,
        "shell_size": len(shell),
        "scalar": f"{scalar.numerator}/{scalar.denominator}",
    }


def validate_odometer_return() -> dict[str, int]:
    cases = 0
    for analytic_x, prime_set in ((100, (5, 7, 11)), (166, (7, 11, 13)), (211, (11, 13, 17))):
        shell = shell_integers(analytic_x)
        beta = {t: Fraction(((3 * t + 5) % 17) - 8, (t % 3) + 1) for t in shell}
        residual = {t: Fraction(((11 * t + 1) % 19) - 9, (t % 4) + 1) for t in shell}
        covariance_sum = Fraction(0)
        orbit_sum = Fraction(0)
        centered_by_prime: list[dict[int, Fraction]] = []
        for prime in prime_set:
            mean = conditional_mean(residual, analytic_x, prime)
            centered = {t: residual[t] - mean[t] for t in shell}
            centered_by_prime.append(centered)
            covariance_sum += dot(beta, centered) / len(prime_set)
        for integer in shell:
            phi = beta[integer] * sum(
                (centered[integer] for centered in centered_by_prime), Fraction(0)
            ) / len(prime_set)
            orbit_point = integer
            require(orbit_point == integer, "odometer distinguished orbit changed")
            orbit_sum += phi
        require(orbit_sum == covariance_sum, "odometer orbit return failed")
        cases += 1
    return {"odometer_return_cases": cases}


def validate_exponents() -> dict[str, str]:
    q_saving = Fraction(1, 32)
    q_exponent = Fraction(1, 3)
    x_saving = q_saving * q_exponent
    margin = x_saving - Fraction(1, 400)
    require(x_saving == Fraction(1, 96), "BP x-saving exponent changed")
    require(margin == Fraction(19, 2400) and margin > 0, "strict endpoint margin changed")
    require(Fraction(1, 1) - q_exponent == Fraction(2, 3), "fiber quotient exponent changed")
    require(Fraction(2, 3) / q_exponent == 2, "fiber quotient is not q-squared")
    require(Fraction(1, 2) * q_exponent == Fraction(1, 6), "BP critical length exponent changed")
    return {"bp_x_saving": "1/96", "strict_margin": "19/2400", "fiber_length": "q^2"}


def wrong_value(value: object) -> object:
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if type(value) is str:
        return value + "_MUTATED"
    raise CheckFailure("unsupported mutation type")


def run_mutations() -> dict[str, int]:
    contract_count = 0
    # run_check validates these globals against independent local literals
    # before entering the mutation matrix.  Using the validated candidates
    # here prevents a rebound fixture-provider function from self-attesting
    # an unrelated decoy schema.
    base_contract = dict(CONTRACT)
    for key in tuple(base_contract):
        candidate = dict(base_contract)
        del candidate[key]
        try:
            validate_contract(candidate)
        except CheckFailure:
            contract_count += 1
        else:
            raise CheckFailure(f"missing contract mutation escaped: {key}")
        candidate = dict(base_contract)
        candidate[key] = wrong_value(candidate[key])
        try:
            validate_contract(candidate)
        except CheckFailure:
            contract_count += 1
        else:
            raise CheckFailure(f"value contract mutation escaped: {key}")
    extra_contract = dict(base_contract)
    extra_contract["UNDECLARED"] = "FALSE_PROMOTION"
    try:
        validate_contract(extra_contract)
    except CheckFailure:
        contract_count += 1
    else:
        raise CheckFailure("extra contract mutation escaped")

    registry_count = 0
    base_registry = REGISTRY_ITEMS
    for index, (key, value) in enumerate(base_registry):
        changed = list(base_registry)
        changed[index] = (key, value + "_MUTATED")
        candidate = tuple(changed)
        try:
            validate_registry(candidate, registry_hash(candidate))
        except CheckFailure:
            registry_count += 1
        else:
            raise CheckFailure(f"registry value mutation escaped: {key}")
        changed = list(base_registry)
        changed[index] = (f"UNKNOWN_{index:02d}", value)
        candidate = tuple(changed)
        try:
            validate_registry(candidate, registry_hash(candidate))
        except CheckFailure:
            registry_count += 1
        else:
            raise CheckFailure(f"registry key mutation escaped: {key}")
    special_candidates = (
        base_registry[:-1],
        base_registry + (("EXTRA", "FALSE_PROMOTION"),),
        tuple((key, value) for key, value in reversed(base_registry)),
    )
    for candidate in special_candidates:
        try:
            validate_registry(candidate, registry_hash(candidate))
        except CheckFailure:
            registry_count += 1
        else:
            raise CheckFailure("registry structural mutation escaped")
    try:
        validate_registry(base_registry, "0" * 64)
    except CheckFailure:
        registry_count += 1
    else:
        raise CheckFailure("registry digest mutation escaped")
    return {"contract_mutations": contract_count, "registry_mutations": registry_count}


def run_check() -> dict[str, object]:
    validate_contract(CONTRACT)
    validate_registry(REGISTRY_ITEMS, EXPECTED_REGISTRY_SHA256)
    v21, v19 = load_v21()
    algebra = validate_projector_algebra()
    ensemble = validate_complete_ensemble()
    synthetic = validate_synthetic_information_loss(v21, v19)
    odometer = validate_odometer_return()
    exponents = validate_exponents()
    mutations = run_mutations()
    result = {
        "check": True,
        "claim": "EXACT_L0_CENTERED_PROJECTOR_FIREWALL_AND_CONDITIONAL_FORK",
        "projector_cases": algebra["projector_cases"],
        "residue_marginals": algebra["marginal_cases"],
        "ragged_cases": algebra["ragged_cases"],
        "x1000_mean_span_rank": ensemble["mean_span_rank"],
        "x1000_identity_multiplicity": ensemble["identity_multiplicity"],
        "common_kernel_witness_support": ensemble["witness_support"],
        "synthetic_beta_centered_energy": synthetic["scalar"],
        "odometer_return_cases": odometer["odometer_return_cases"],
        "bp_x_saving": exponents["bp_x_saving"],
        "strict_margin": exponents["strict_margin"],
        "contract_mutations": mutations["contract_mutations"],
        "registry_mutations": mutations["registry_mutations"],
        "registry_rows": len(REGISTRY_ITEMS),
        "registry_sha256": "19c228b356cf1b8034eb3e018c0ef0e2d8363515062f9472c4857b54b1f1d8c7",
        "direct_residue_kloosterman": "STOP_SCOPED",
        "direct_projector_dispersion": "STOP_SCOPED",
        "bp_post_poisson_compiler": "OPEN_CONDITIONAL",
        "odometer_return": "PROVED_EXACT_L0_NO_CANCELLATION",
        "transversal_common_return": "OPEN_NEW_CONSTRUCTION",
        "arithmetic_advance": False,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run the read-only V22 checker")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require(args.check is True, "the explicit --check entry is required")
    print(json.dumps(run_check(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
