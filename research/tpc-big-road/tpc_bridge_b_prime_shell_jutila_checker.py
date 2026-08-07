#!/usr/bin/env python3
"""Read-only exact checker for the TPC Bridge-B V23 route atlas."""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
from fractions import Fraction
from pathlib import Path
from typing import Callable, Iterable


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


V19_PATH = Path("research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py")
V19_CANONICAL_SHA256 = "e572bd9157ce4e733dc411ed8eb29df90d34be0ecf17023186f1648389ded519"
V21_PATH = Path("research/tpc-big-road/tpc_bridge_b_mesoscopic_covariance_checker.py")
V21_CANONICAL_SHA256 = "b6350ce0f7ed38dd7671f5076a0c26bf82bb57850ec35505c4cfec3239ad336e"
V22_PATH = Path("research/tpc-big-road/tpc_bridge_b_centered_projector_checker.py")
V22_CANONICAL_SHA256 = "013aea5a5975c65c3dda9be0df335dd672fec7776096f4edff13b1d7946637a2"


CONTRACT = {
    "route_version": "BOLD_CHANNEL_V23",
    "claim_ceiling": "EXACT_L0_PRIME_SHELL_JUTILA_EXPONENT_INTERFACE_AND_FINITE_TRANSPORT_FALSIFIERS",
    "physical_h0": 2,
    "analytic_physical_binding": "x=2X",
    "raw_row": "V19_COMBINED_RAW_MASTER_PLUS2_MINUS1",
    "residual": "LAMBDA_SHIFT2_MINUS_TENSOR_LOCAL_B",
    "prime_shell": "PRIME_QMES_LT_q_LE_2QMES_WITH_QSRC_EQUALS_2QMES",
    "prime_ensemble_normalization": "L=SUM_q_MINUS_1",
    "fiber_normalization": "ACTUAL_RAGGED_COUNTS",
    "outer_absolute_value": "ONCE_OUTSIDE_COMPLETE_REASSEMBLY",
    "jutila_source": "BLOMER_LI_2511_03294V1_SECTION_2_1_LEMMA_1_PSI_RANGE_0_1_SUPPORT_MINUS1_1_INTEGRAL1",
    "jutila_omega": "PRIME_SHELL_INDICATOR_SUPPORTED_ON_q_LE_QSRC_EQUALS_2QMES",
    "jutila_L": "SUM_PHI_q_EQUALS_SUM_q_MINUS_1",
    "jutila_delta": "QMES_POWER_MINUS_2_PLUS_ETA",
    "jutila_eta": "1/32",
    "jutila_dual_exponent": "17/32",
    "bp_q_saving": "11/512",
    "bp_x_saving": "11/1536",
    "strict_local_margin": "179/38400",
    "original_bp_margin": "19/2400",
    "arc_width_loss": "5/1536",
    "eta_window": "3/200_LT_ETA_LT_173/2400",
    "pure_energy_theta_threshold": "13/4800",
    "pure_energy_trivial_theta": "1/2_STOP_SCOPED",
    "dft_scope": "FINITE_COMPLEXITY_DIAGNOSTIC_ONLY",
    "stable_cell_scope": "FINITE_SCHEDULING_DIAGNOSTIC_ONLY",
    "survivor_token": "V23_PRIME_SHELL_JUTILA_KLOOSTERMAN_INTERTWINED_PHYSICAL_COMPILER_GATE",
    "survivor_status": "OPEN_CONDITIONAL",
    "arithmetic_advance": False,
    "fixed_atom_credit": 0,
    "strict_1_over_400": "UNPAID",
    "L2": "NONE",
    "TPC_207_TRIGGER": False,
}


REGISTRY_ITEMS = (
    ("MAXIMUM_CLAIM", "EXACT_L0_PRIME_SHELL_JUTILA_EXPONENT_INTERFACE_AND_FINITE_TRANSPORT_FALSIFIERS"),
    ("PHYSICAL_H0", "2"),
    ("PHYSICAL_X", "x_EQUALS_2X"),
    ("PHYSICAL_SHELL", "STRICT_x_OVER_2_LT_t_LE_x"),
    ("PHYSICAL_RAW_ROW", "V19_COMBINED_RAW_MASTER_PLUS2_MINUS1"),
    ("PHYSICAL_RESIDUAL", "LAMBDA_SHIFT2_MINUS_TENSOR_LOCAL_B"),
    ("OUTER_ABSOLUTE", "ONCE_OUTSIDE_COMPLETE_REASSEMBLY"),
    ("CIRCLE_MODULUS", "EXTERNAL_PRIME_SHELL_QMES_LT_q_LE_2QMES_WITH_QSRC_EQUALS_2QMES"),
    ("DETERMINANT_DIVISOR", "DISTINCT_FROM_CIRCLE_MODULUS_UNLESS_EXPLICIT_LOCAL_SLICE"),
    ("JUTILA_SOURCE", "BLOMER_LI_2511_03294V1_SECTION_2_1_LEMMA_1_PSI_RANGE_0_1_SUPPORT_MINUS1_1_INTEGRAL1"),
    ("JUTILA_WEIGHT", "PRIME_SHELL_INDICATOR_SUPPORTED_ON_q_LE_QSRC_EQUALS_2QMES"),
    ("JUTILA_L", "SUM_PHI_q_EQUALS_SUM_q_MINUS_1"),
    ("JUTILA_DELTA", "QMES_POWER_MINUS_2_PLUS_ETA"),
    ("JUTILA_ETA", "1_OVER_32"),
    ("JUTILA_L2_APPROXIMATION", "SOURCE_BACKED_Q_POWER_MINUS_ETA_SQUARED_NORM"),
    ("JUTILA_SCALAR_SPLIT", "EXACT_MAIN_PLUS_EXPLICIT_ERROR"),
    ("PHYSICAL_G_TRIVIAL_NORM", "X_POWER_3_OVER_2_POLYLOG"),
    ("PHYSICAL_ENERGY_GATE", "OPEN_THETA_LT_13_OVER_4800"),
    ("BP_SOURCE", "BLOMER_PASCADI_2607_24311V1_THEOREMS_1_1_5_2_5_5"),
    ("BP_DUAL_SUPPORT", "Q_POWER_17_OVER_32_AT_ETA_1_OVER_32"),
    ("BP_Q_SAVING", "11_OVER_512"),
    ("BP_X_SAVING", "11_OVER_1536"),
    ("STRICT_LOCAL_MARGIN", "179_OVER_38400_BEFORE_COMPILER_LOSSES"),
    ("ETA_WINDOW", "3_OVER_200_LT_ETA_LT_173_OVER_2400"),
    ("PRIME_SHELL_ATTACHMENT", "SOURCE_BACKED_RESTRICTED_MODULUS_L2_APPROXIMATION"),
    ("INTERTWINED_COMPILER_GATE", "OPEN_CONDITIONAL"),
    ("NAIVE_CONGRUENCE", "STOP_SCOPED_OFFDIAGONAL_L_NOT_REASSEMBLED"),
    ("EXACT_FAREY_PRIME_SHELL", "STOP_SCOPED_ALL_C_LE_C_GEOMETRY_REQUIRED"),
    ("STANDARD_DELTA_PRIME_SHELL", "STOP_SCOPED_NO_SOURCE_BACKED_PRIME_ONLY_WEIGHT_AND_REASSEMBLY"),
    ("SINGLE_Q_FINITE_FOURIER", "STOP_SCOPED_DIVISIBILITY_ONLY"),
    ("MINIMAL_HB2_B3", "STOP_SCOPED_NO_SECOND_SMOOTH_VARIABLE_AND_QUADRATIC_CRT_ZERO_MODE"),
    ("D_EQ_Q_DOUBLE_POISSON", "EXACT_LOCAL_FORMULA_AFTER_SEPARATED_ATOM"),
    ("D_EQ_Q_FIXED_UNIT_BP", "SOURCE_ATTACHED_LOCAL_ONLY"),
    ("D_EQ_Q_OUTER_TRIANGLE", "STOP_SCOPED_Q_15_OVER_32_DEFICIT"),
    ("MOVING_UNIT_VECTOR_LIFT", "STOP_SCOPED_FALSE_CHARACTER_EIGENMODE"),
    ("SOURCE_STABLE_CELL", "PROVED_EXACT_FINITE"),
    ("CARRIER_STABLE_CELL", "PROVED_EXACT_FINITE"),
    ("X166_STAGE_FIXTURE", "H83_Q7_RANK_P7_RANK_C76"),
    ("X166_BETA_GAMMA_FIXTURE", "BETA_SUPPORT30_GAMMA_SUPPORT79_GAMMA_ENERGY2359675_OVER_77616"),
    ("X166_DFT_FIXTURE", "BETA83_GAMMA82_ONLY_GAMMA_ZERO_FREQUENCY"),
    ("X168_STAGE_FIXTURE", "H84_Q7_11_RANK_P17_RANK_C83_DEFECT16"),
    ("X168_BETA_GAMMA_FIXTURE", "BETA_SUPPORT30_GAMMA_SUPPORT84_GAMMA_ENERGY71460239_OVER_2370816"),
    ("X168_DFT_FIXTURE", "BETA84_GAMMA83_ONLY_GAMMA_ZERO_FREQUENCY"),
    ("X166_X168_OPERATOR_RANKS", "OVERLAP_P17_STACKED_C82_UNION_DELTA19_Q11_BIRTH16"),
    ("X166_X168_BETA_GAMMA_UPDATE", "BETA_MINUS_E84_PLUS_E168_GAMMA_SUPPORT81_Q11_NONZERO_DFT10"),
    ("STABLE_PAIR_FIXTURES", "170_172__172_174__180_182__200_202_NOT_BOUNDARY_SUPPORTED"),
    ("WALL_CENSUS_100_400", "150_PAIRS_BETA_STABLE147_Q_STABLE146_JOINT143_FINITE_ONLY"),
    ("RELEASE_BOUNDARY", "ARITHMETIC_NO_FIXED_ATOM0_STRICT_UNPAID_L2_NONE_TPC207_FALSE"),
)


EXPECTED_REGISTRY_SHA256 = "15e40e8c20050549c3e244be59747019f115ebb8ccb9356f95fd449250073b07"


def canonical_lf_bytes(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def registry_hash(items: Iterable[tuple[str, str]]) -> str:
    payload = "".join(f"{key}={value}\n" for key, value in items).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def literal_contract() -> dict[str, object]:
    return dict(CONTRACT)


def literal_registry() -> tuple[tuple[str, str], ...]:
    return tuple(REGISTRY_ITEMS)


def validate_contract(candidate: object) -> None:
    expected = {
        "route_version": "BOLD_CHANNEL_V23",
        "claim_ceiling": "EXACT_L0_PRIME_SHELL_JUTILA_EXPONENT_INTERFACE_AND_FINITE_TRANSPORT_FALSIFIERS",
        "physical_h0": 2,
        "analytic_physical_binding": "x=2X",
        "raw_row": "V19_COMBINED_RAW_MASTER_PLUS2_MINUS1",
        "residual": "LAMBDA_SHIFT2_MINUS_TENSOR_LOCAL_B",
        "prime_shell": "PRIME_QMES_LT_q_LE_2QMES_WITH_QSRC_EQUALS_2QMES",
        "prime_ensemble_normalization": "L=SUM_q_MINUS_1",
        "fiber_normalization": "ACTUAL_RAGGED_COUNTS",
        "outer_absolute_value": "ONCE_OUTSIDE_COMPLETE_REASSEMBLY",
        "jutila_source": "BLOMER_LI_2511_03294V1_SECTION_2_1_LEMMA_1_PSI_RANGE_0_1_SUPPORT_MINUS1_1_INTEGRAL1",
        "jutila_omega": "PRIME_SHELL_INDICATOR_SUPPORTED_ON_q_LE_QSRC_EQUALS_2QMES",
        "jutila_L": "SUM_PHI_q_EQUALS_SUM_q_MINUS_1",
        "jutila_delta": "QMES_POWER_MINUS_2_PLUS_ETA",
        "jutila_eta": "1/32",
        "jutila_dual_exponent": "17/32",
        "bp_q_saving": "11/512",
        "bp_x_saving": "11/1536",
        "strict_local_margin": "179/38400",
        "original_bp_margin": "19/2400",
        "arc_width_loss": "5/1536",
        "eta_window": "3/200_LT_ETA_LT_173/2400",
        "pure_energy_theta_threshold": "13/4800",
        "pure_energy_trivial_theta": "1/2_STOP_SCOPED",
        "dft_scope": "FINITE_COMPLEXITY_DIAGNOSTIC_ONLY",
        "stable_cell_scope": "FINITE_SCHEDULING_DIAGNOSTIC_ONLY",
        "survivor_token": "V23_PRIME_SHELL_JUTILA_KLOOSTERMAN_INTERTWINED_PHYSICAL_COMPILER_GATE",
        "survivor_status": "OPEN_CONDITIONAL",
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
    expected = (
        ("MAXIMUM_CLAIM", "EXACT_L0_PRIME_SHELL_JUTILA_EXPONENT_INTERFACE_AND_FINITE_TRANSPORT_FALSIFIERS"),
        ("PHYSICAL_H0", "2"),
        ("PHYSICAL_X", "x_EQUALS_2X"),
        ("PHYSICAL_SHELL", "STRICT_x_OVER_2_LT_t_LE_x"),
        ("PHYSICAL_RAW_ROW", "V19_COMBINED_RAW_MASTER_PLUS2_MINUS1"),
        ("PHYSICAL_RESIDUAL", "LAMBDA_SHIFT2_MINUS_TENSOR_LOCAL_B"),
        ("OUTER_ABSOLUTE", "ONCE_OUTSIDE_COMPLETE_REASSEMBLY"),
        ("CIRCLE_MODULUS", "EXTERNAL_PRIME_SHELL_QMES_LT_q_LE_2QMES_WITH_QSRC_EQUALS_2QMES"),
        ("DETERMINANT_DIVISOR", "DISTINCT_FROM_CIRCLE_MODULUS_UNLESS_EXPLICIT_LOCAL_SLICE"),
        ("JUTILA_SOURCE", "BLOMER_LI_2511_03294V1_SECTION_2_1_LEMMA_1_PSI_RANGE_0_1_SUPPORT_MINUS1_1_INTEGRAL1"),
        ("JUTILA_WEIGHT", "PRIME_SHELL_INDICATOR_SUPPORTED_ON_q_LE_QSRC_EQUALS_2QMES"),
        ("JUTILA_L", "SUM_PHI_q_EQUALS_SUM_q_MINUS_1"),
        ("JUTILA_DELTA", "QMES_POWER_MINUS_2_PLUS_ETA"),
        ("JUTILA_ETA", "1_OVER_32"),
        ("JUTILA_L2_APPROXIMATION", "SOURCE_BACKED_Q_POWER_MINUS_ETA_SQUARED_NORM"),
        ("JUTILA_SCALAR_SPLIT", "EXACT_MAIN_PLUS_EXPLICIT_ERROR"),
        ("PHYSICAL_G_TRIVIAL_NORM", "X_POWER_3_OVER_2_POLYLOG"),
        ("PHYSICAL_ENERGY_GATE", "OPEN_THETA_LT_13_OVER_4800"),
        ("BP_SOURCE", "BLOMER_PASCADI_2607_24311V1_THEOREMS_1_1_5_2_5_5"),
        ("BP_DUAL_SUPPORT", "Q_POWER_17_OVER_32_AT_ETA_1_OVER_32"),
        ("BP_Q_SAVING", "11_OVER_512"),
        ("BP_X_SAVING", "11_OVER_1536"),
        ("STRICT_LOCAL_MARGIN", "179_OVER_38400_BEFORE_COMPILER_LOSSES"),
        ("ETA_WINDOW", "3_OVER_200_LT_ETA_LT_173_OVER_2400"),
        ("PRIME_SHELL_ATTACHMENT", "SOURCE_BACKED_RESTRICTED_MODULUS_L2_APPROXIMATION"),
        ("INTERTWINED_COMPILER_GATE", "OPEN_CONDITIONAL"),
        ("NAIVE_CONGRUENCE", "STOP_SCOPED_OFFDIAGONAL_L_NOT_REASSEMBLED"),
        ("EXACT_FAREY_PRIME_SHELL", "STOP_SCOPED_ALL_C_LE_C_GEOMETRY_REQUIRED"),
        ("STANDARD_DELTA_PRIME_SHELL", "STOP_SCOPED_NO_SOURCE_BACKED_PRIME_ONLY_WEIGHT_AND_REASSEMBLY"),
        ("SINGLE_Q_FINITE_FOURIER", "STOP_SCOPED_DIVISIBILITY_ONLY"),
        ("MINIMAL_HB2_B3", "STOP_SCOPED_NO_SECOND_SMOOTH_VARIABLE_AND_QUADRATIC_CRT_ZERO_MODE"),
        ("D_EQ_Q_DOUBLE_POISSON", "EXACT_LOCAL_FORMULA_AFTER_SEPARATED_ATOM"),
        ("D_EQ_Q_FIXED_UNIT_BP", "SOURCE_ATTACHED_LOCAL_ONLY"),
        ("D_EQ_Q_OUTER_TRIANGLE", "STOP_SCOPED_Q_15_OVER_32_DEFICIT"),
        ("MOVING_UNIT_VECTOR_LIFT", "STOP_SCOPED_FALSE_CHARACTER_EIGENMODE"),
        ("SOURCE_STABLE_CELL", "PROVED_EXACT_FINITE"),
        ("CARRIER_STABLE_CELL", "PROVED_EXACT_FINITE"),
        ("X166_STAGE_FIXTURE", "H83_Q7_RANK_P7_RANK_C76"),
        ("X166_BETA_GAMMA_FIXTURE", "BETA_SUPPORT30_GAMMA_SUPPORT79_GAMMA_ENERGY2359675_OVER_77616"),
        ("X166_DFT_FIXTURE", "BETA83_GAMMA82_ONLY_GAMMA_ZERO_FREQUENCY"),
        ("X168_STAGE_FIXTURE", "H84_Q7_11_RANK_P17_RANK_C83_DEFECT16"),
        ("X168_BETA_GAMMA_FIXTURE", "BETA_SUPPORT30_GAMMA_SUPPORT84_GAMMA_ENERGY71460239_OVER_2370816"),
        ("X168_DFT_FIXTURE", "BETA84_GAMMA83_ONLY_GAMMA_ZERO_FREQUENCY"),
        ("X166_X168_OPERATOR_RANKS", "OVERLAP_P17_STACKED_C82_UNION_DELTA19_Q11_BIRTH16"),
        ("X166_X168_BETA_GAMMA_UPDATE", "BETA_MINUS_E84_PLUS_E168_GAMMA_SUPPORT81_Q11_NONZERO_DFT10"),
        ("STABLE_PAIR_FIXTURES", "170_172__172_174__180_182__200_202_NOT_BOUNDARY_SUPPORTED"),
        ("WALL_CENSUS_100_400", "150_PAIRS_BETA_STABLE147_Q_STABLE146_JOINT143_FINITE_ONLY"),
        ("RELEASE_BOUNDARY", "ARITHMETIC_NO_FIXED_ATOM0_STRICT_UNPAID_L2_NONE_TPC207_FALSE"),
    )
    expected_digest = "15e40e8c20050549c3e244be59747019f115ebb8ccb9356f95fd449250073b07"
    require(type(candidate) is tuple, "registry is not a tuple")
    require(all(type(row) is tuple and len(row) == 2 for row in candidate), "registry row schema changed")
    require(all(type(key) is str and type(value) is str for key, value in candidate), "registry row type changed")
    require(candidate == expected, "registry semantic row changed")
    require(len(candidate) == 48, "registry row count changed")
    require(len({key for key, _ in candidate}) == 48, "registry key uniqueness changed")
    require(type(digest) is str, "registry digest has wrong type")
    require(digest == expected_digest, "registry digest binding changed")
    require(registry_hash(candidate) == expected_digest, "registry digest changed")


def load_dependencies() -> tuple[dict[str, object], dict[str, object]]:
    locks = (
        (Path("research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py"),
         "e572bd9157ce4e733dc411ed8eb29df90d34be0ecf17023186f1648389ded519"),
        (Path("research/tpc-big-road/tpc_bridge_b_mesoscopic_covariance_checker.py"),
         "b6350ce0f7ed38dd7671f5076a0c26bf82bb57850ec35505c4cfec3239ad336e"),
        (Path("research/tpc-big-road/tpc_bridge_b_centered_projector_checker.py"),
         "013aea5a5975c65c3dda9be0df335dd672fec7776096f4edff13b1d7946637a2"),
    )
    for path, expected in locks:
        require(path.is_file(), f"dependency is absent: {path}")
        actual = hashlib.sha256(canonical_lf_bytes(path.read_bytes())).hexdigest()
        require(actual == expected, f"dependency canonical hash changed: {path}")
    v22 = runpy.run_path(str(locks[2][0]))
    v22_result = v22["run_check"]()
    require(type(v22_result) is dict and v22_result.get("check") is True, "V22 checker failed")
    require(v22_result.get("claim") == "EXACT_L0_CENTERED_PROJECTOR_FIREWALL_AND_CONDITIONAL_FORK", "V22 claim changed")
    require(v22_result.get("arithmetic_advance") is False, "V22 arithmetic status changed")
    require(type(v22_result.get("fixed_atom_credit")) is int and v22_result["fixed_atom_credit"] == 0, "V22 atom status changed")
    require(v22_result.get("strict_1_over_400") == "UNPAID", "V22 strict status changed")
    require(v22_result.get("L2") == "NONE", "V22 L2 status changed")
    require(v22_result.get("TPC_207_TRIGGER") is False, "V22 TPC-207 status changed")
    v19 = runpy.run_path(str(locks[0][0]))
    return v22, v19


def is_prime(integer: int) -> bool:
    if type(integer) is not int or integer < 2:
        return False
    divisor = 2
    while divisor * divisor <= integer:
        if integer % divisor == 0:
            return integer == divisor
        divisor += 1
    return True


def shell_integers(analytic_x: int) -> tuple[int, ...]:
    require(type(analytic_x) is int and analytic_x >= 2 and analytic_x % 2 == 0, "analytic x is invalid")
    return tuple(range(analytic_x // 2 + 1, analytic_x + 1))


def active_prime_shell(analytic_x: int) -> tuple[int, ...]:
    require(type(analytic_x) is int and analytic_x > 0, "prime-shell x is invalid")
    return tuple(q for q in range(2, analytic_x + 2) if is_prime(q) and analytic_x < q**3 <= 8 * analytic_x)


def jutila_prime_shell(scale_q: int) -> tuple[int, ...]:
    require(type(scale_q) is int and scale_q >= 2, "Jutila scale is invalid")
    return tuple(q for q in range(scale_q + 1, 2 * scale_q + 1) if is_prime(q))


def jutila_L(primes: tuple[int, ...]) -> int:
    require(all(is_prime(q) for q in primes), "Jutila ensemble contains a nonprime")
    return sum(q - 1 for q in primes)


def literal_beta(v19: dict[str, object], integer: int, analytic_x: int) -> Fraction:
    numerator_items = v19["raw_master_numerator"](integer, analytic_x)[0]
    if not numerator_items:
        return Fraction(0)
    numerator = dict(numerator_items)
    factors = dict(v19["factorization"](integer))
    require(set(numerator) <= set(factors), "raw numerator has an extraneous prime")
    ratios = {Fraction(numerator.get(prime, 0), exponent) for prime, exponent in factors.items()}
    require(len(ratios) == 1, "literal beta is not rational on the locked fixture")
    return ratios.pop()


def beta_vector(v19: dict[str, object], analytic_x: int) -> dict[int, Fraction]:
    return {t: literal_beta(v19, t, analytic_x) for t in shell_integers(analytic_x)}


def fibers(shell: tuple[int, ...], modulus: int) -> tuple[tuple[int, ...], ...]:
    require(type(modulus) is int and modulus >= 2, "fiber modulus is invalid")
    return tuple(tuple(t for t in shell if t % modulus == residue) for residue in range(modulus))


def conditional_mean(vector: dict[int, Fraction], shell: tuple[int, ...], modulus: int) -> dict[int, Fraction]:
    require(set(vector) == set(shell), "conditional-mean domain changed")
    result: dict[int, Fraction] = {}
    for fiber in fibers(shell, modulus):
        if not fiber:
            continue
        mean = sum((vector[t] for t in fiber), Fraction(0)) / len(fiber)
        for t in fiber:
            result[t] = mean
    require(set(result) == set(shell), "conditional mean lost a shell point")
    return result


def centered_covector(beta: dict[int, Fraction], shell: tuple[int, ...], primes: tuple[int, ...]) -> dict[int, Fraction]:
    require(bool(primes), "centered ensemble is empty")
    means = [conditional_mean(beta, shell, q) for q in primes]
    return {
        t: beta[t] - sum((mean[t] for mean in means), Fraction(0)) / len(primes)
        for t in shell
    }


def fraction_rank(rows: list[list[Fraction]]) -> int:
    if not rows:
        return 0
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "rank matrix is ragged")
    matrix = [list(row) for row in rows]
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(matrix)) if matrix[row][column] != 0), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [entry / pivot_value for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [entry - factor * pivot_entry for entry, pivot_entry in zip(matrix[row], matrix[rank])]
        rank += 1
        if rank == min(len(matrix), width):
            break
    return rank


def zero_matrix(height: int, width: int) -> list[list[Fraction]]:
    return [[Fraction(0) for _ in range(width)] for _ in range(height)]


def identity_matrix(size: int) -> list[list[Fraction]]:
    return [[Fraction(int(i == j)) for j in range(size)] for i in range(size)]


def projector_matrix(shell: tuple[int, ...], modulus: int) -> list[list[Fraction]]:
    index = {t: i for i, t in enumerate(shell)}
    result = zero_matrix(len(shell), len(shell))
    for fiber in fibers(shell, modulus):
        if not fiber:
            continue
        weight = Fraction(1, len(fiber))
        for left in fiber:
            for right in fiber:
                result[index[left]][index[right]] = weight
    return result


def matrix_add(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    require(len(left) == len(right) and all(len(a) == len(b) for a, b in zip(left, right)), "matrix dimensions differ")
    return [[a + b for a, b in zip(left_row, right_row)] for left_row, right_row in zip(left, right)]


def matrix_sub(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    require(len(left) == len(right) and all(len(a) == len(b) for a, b in zip(left, right)), "matrix dimensions differ")
    return [[a - b for a, b in zip(left_row, right_row)] for left_row, right_row in zip(left, right)]


def matrix_scale(matrix: list[list[Fraction]], scalar: Fraction) -> list[list[Fraction]]:
    return [[scalar * entry for entry in row] for row in matrix]


def matrix_multiply(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    require(bool(left) and bool(right) and len(left[0]) == len(right), "matrix product dimensions differ")
    columns = list(zip(*right))
    return [[sum((a * b for a, b in zip(row, column)), Fraction(0)) for column in columns] for row in left]


def average_projector(shell: tuple[int, ...], primes: tuple[int, ...]) -> list[list[Fraction]]:
    require(bool(primes), "average projector ensemble is empty")
    result = zero_matrix(len(shell), len(shell))
    for prime in primes:
        result = matrix_add(result, projector_matrix(shell, prime))
    return matrix_scale(result, Fraction(1, len(primes)))


def centered_matrix(shell: tuple[int, ...], primes: tuple[int, ...]) -> list[list[Fraction]]:
    return matrix_sub(identity_matrix(len(shell)), average_projector(shell, primes))


def submatrix(matrix: list[list[Fraction]], source_shell: tuple[int, ...], target_shell: tuple[int, ...]) -> list[list[Fraction]]:
    positions = {t: i for i, t in enumerate(source_shell)}
    return [[matrix[positions[left]][positions[right]] for right in target_shell] for left in target_shell]


def extend_matrix(matrix: list[list[Fraction]], source_shell: tuple[int, ...], union: tuple[int, ...]) -> list[list[Fraction]]:
    source_index = {t: i for i, t in enumerate(source_shell)}
    result = zero_matrix(len(union), len(union))
    for i, left in enumerate(union):
        if left not in source_index:
            continue
        for j, right in enumerate(union):
            if right in source_index:
                result[i][j] = matrix[source_index[left]][source_index[right]]
    return result


def circulant_rank(vector: tuple[Fraction, ...]) -> int:
    size = len(vector)
    require(size > 0, "circulant vector is empty")
    matrix = [[vector[(column - row) % size] for column in range(size)] for row in range(size)]
    return fraction_rank(matrix)


def l1(vector: dict[int, Fraction]) -> Fraction:
    return sum((abs(value) for value in vector.values()), Fraction(0))


def l2_squared(vector: dict[int, Fraction]) -> Fraction:
    return sum((value * value for value in vector.values()), Fraction(0))


def support(vector: dict[int, Fraction]) -> int:
    return sum(value != 0 for value in vector.values())


def zero_extend(vector: dict[int, Fraction], union: tuple[int, ...]) -> dict[int, Fraction]:
    return {t: vector.get(t, Fraction(0)) for t in union}


def validate_rank_engine() -> int:
    require(fraction_rank([[Fraction(0), Fraction(0)]]) == 0, "zero rank fixture failed")
    require(fraction_rank([[Fraction(1), Fraction(1)], [Fraction(2), Fraction(2)]]) == 1, "rank-one fixture failed")
    require(fraction_rank([[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]]) == 2, "full-rank fixture failed")
    require(circulant_rank((Fraction(0),) * 7) == 0, "zero circulant fixture failed")
    require(circulant_rank((Fraction(1),) * 7) == 1, "constant circulant fixture failed")
    require(circulant_rank((Fraction(1),) + (Fraction(0),) * 6) == 7, "delta circulant fixture failed")
    require(circulant_rank((Fraction(1), Fraction(-1)) + (Fraction(0),) * 5) == 6, "difference circulant fixture failed")
    return 7


def validate_stage_geometry(v19: dict[str, object]) -> dict[str, object]:
    shell166 = shell_integers(166)
    shell168 = shell_integers(168)
    q166 = active_prime_shell(166)
    q168 = active_prime_shell(168)
    require(q166 == (7,), "x=166 prime shell changed")
    require(q168 == (7, 11), "x=168 prime shell changed")
    require(tuple(len(fiber) for fiber in fibers(shell166, 7)) == (12, 12, 12, 12, 12, 12, 11), "x=166 q7 counts changed")
    require(tuple(len(fiber) for fiber in fibers(shell168, 7)) == (12,) * 7, "x=168 q7 counts changed")
    require(tuple(len(fiber) for fiber in fibers(shell168, 11)) == (8, 8, 8, 8, 7, 7, 7, 7, 8, 8, 8), "x=168 q11 counts changed")

    p166 = average_projector(shell166, q166)
    c166 = centered_matrix(shell166, q166)
    p168 = average_projector(shell168, q168)
    c168 = centered_matrix(shell168, q168)
    require(fraction_rank(p166) == 7 and fraction_rank(c166) == 76, "x=166 ranks changed")
    require(fraction_rank(p168) == 17 and fraction_rank(c168) == 83, "x=168 ranks changed")
    require(fraction_rank(matrix_sub(matrix_multiply(p168, p168), p168)) == 16, "x=168 projector defect rank changed")

    beta166 = beta_vector(v19, 166)
    beta168 = beta_vector(v19, 168)
    expected_points = {84: Fraction(1), 90: Fraction(2), 91: Fraction(-1), 114: Fraction(1), 120: Fraction(2), 121: Fraction(-1, 2), 150: Fraction(2)}
    for integer, expected in expected_points.items():
        require(beta166[integer] == expected, f"x=166 beta point {integer} changed")
    require(support(beta166) == 30 and sum(beta166.values(), Fraction(0)) == Fraction(839, 42), "x=166 beta support/sum changed")
    require(l2_squared(beta166) == Fraction(64177, 1764), "x=166 beta energy changed")
    require(support(beta168) == 30 and sum(beta168.values(), Fraction(0)) == Fraction(839, 42), "x=168 beta support/sum changed")
    require(l2_squared(beta168) == Fraction(64177, 1764), "x=168 beta energy changed")
    require(beta168[167] == 0 and beta168[168] == 1, "x=168 endpoint beta changed")

    gamma166 = centered_covector(beta166, shell166, q166)
    gamma168 = centered_covector(beta168, shell168, q168)
    require(support(gamma166) == 79 and l1(gamma166) == Fraction(18191, 462), "x=166 gamma support/l1 changed")
    require(l2_squared(gamma166) == Fraction(2359675, 77616) and sum(gamma166.values(), Fraction(0)) == 0, "x=166 gamma energy/mean changed")
    require(support(gamma168) == 84 and l1(gamma168) == Fraction(276461, 7056), "x=168 gamma support/l1 changed")
    require(l2_squared(gamma168) == Fraction(71460239, 2370816) and sum(gamma168.values(), Fraction(0)) == 0, "x=168 gamma energy/mean changed")

    beta166_dft = circulant_rank(tuple(beta166[t] for t in shell166))
    gamma166_dft = circulant_rank(tuple(gamma166[t] for t in shell166))
    beta168_dft = circulant_rank(tuple(beta168[t] for t in shell168))
    gamma168_dft = circulant_rank(tuple(gamma168[t] for t in shell168))
    require((beta166_dft, gamma166_dft, beta168_dft, gamma168_dft) == (83, 82, 84, 83), "physical DFT support changed")

    overlap = tuple(range(85, 167))
    e166_7 = submatrix(projector_matrix(shell166, 7), shell166, overlap)
    e168_7 = submatrix(projector_matrix(shell168, 7), shell168, overlap)
    commutator = matrix_sub(e166_7, e168_7)
    nonzero = [entry for row in commutator for entry in row if entry]
    require(fraction_rank(commutator) == 1 and len(nonzero) == 121 and set(nonzero) == {Fraction(1, 132)}, "common-q overlap commutator changed")
    p166_overlap = submatrix(p166, shell166, overlap)
    p168_overlap = submatrix(p168, shell168, overlap)
    c166_overlap = submatrix(c166, shell166, overlap)
    c168_overlap = submatrix(c168, shell168, overlap)
    require(fraction_rank(matrix_sub(p168_overlap, p166_overlap)) == 17, "overlap averaged-projector difference rank changed")
    require(fraction_rank(c166_overlap) == 76 and fraction_rank(c168_overlap) == 82, "overlap centered ranks changed")
    require(fraction_rank(c166_overlap + c168_overlap) == 82, "stacked centered carrier rank changed")

    union = tuple(range(84, 169))
    p166_union = extend_matrix(p166, shell166, union)
    p168_union = extend_matrix(p168, shell168, union)
    c166_union = extend_matrix(c166, shell166, union)
    c168_union = extend_matrix(c168, shell168, union)
    require(fraction_rank(matrix_sub(p168_union, p166_union)) == 19, "union projector update rank changed")
    require(fraction_rank(matrix_sub(c168_union, c166_union)) == 19, "union centered update rank changed")
    c168_q7 = centered_matrix(shell168, (7,))
    require(fraction_rank(matrix_sub(c168, c168_q7)) == 16, "q11 carrier-birth rank changed")

    beta166_union = zero_extend(beta166, union)
    beta168_union = zero_extend(beta168, union)
    beta_delta = {t: beta168_union[t] - beta166_union[t] for t in union}
    require({t: value for t, value in beta_delta.items() if value} == {84: Fraction(-1), 168: Fraction(1)}, "raw beta boundary update changed")
    require(all(beta166[t] == beta168[t] for t in overlap), "raw beta overlap is not stable")
    gamma166_union = zero_extend(gamma166, union)
    gamma168_union = zero_extend(gamma168, union)
    gamma_delta = {t: gamma168_union[t] - gamma166_union[t] for t in union}
    require(support(gamma_delta) == 81 and l1(gamma_delta) == Fraction(150427, 19404), "gamma update support/l1 changed")
    require(l2_squared(gamma_delta) == Fraction(63578899, 26078976), "gamma update energy changed")
    require(tuple(t for t, value in gamma_delta.items() if value == 0) == (113, 120, 124, 131), "gamma update zero coordinates changed")

    period166_q7 = tuple(sum((beta166[t] for t in shell166 if t % 7 == residue), Fraction(0)) for residue in range(7))
    require(period166_q7 == (Fraction(0), Fraction(3), Fraction(51, 14), Fraction(2), Fraction(4), Fraction(3), Fraction(13, 3)), "x=166 q7 periodization changed")
    delta_q7 = tuple(sum((value for t, value in beta_delta.items() if t % 7 == residue), Fraction(0)) for residue in range(7))
    delta_q11 = tuple(sum((value for t, value in beta_delta.items() if t % 11 == residue), Fraction(0)) for residue in range(11))
    require(delta_q7 == (Fraction(0),) * 7, "boundary innovation did not vanish mod 7")
    require(circulant_rank(delta_q11) == 10 and sum(delta_q11, Fraction(0)) == 0, "q11 innovation DFT support changed")

    return {
        "x166_beta_dft_support": beta166_dft,
        "x166_gamma_dft_support": gamma166_dft,
        "x168_beta_dft_support": beta168_dft,
        "x168_gamma_dft_support": gamma168_dft,
        "x166_x168_gamma_update_support": support(gamma_delta),
        "q11_innovation_dft_support": circulant_rank(delta_q11),
    }


def validate_stable_pairs(v19: dict[str, object]) -> int:
    expected = {
        (170, 172): (87, 51, Fraction(1759, 1274), Fraction(11647, 61152)),
        (172, 174): (88, 51, Fraction(2105, 936), Fraction(48695, 78624)),
        (180, 182): (92, 45, Fraction(2755, 936), Fraction(439, 312)),
        (200, 202): (102, 62, Fraction(1901, 1260), Fraction(12157, 54432)),
    }
    for (left, right), (union_size, expected_support, expected_l1, expected_l2) in expected.items():
        left_shell = shell_integers(left)
        right_shell = shell_integers(right)
        require(active_prime_shell(left) == active_prime_shell(right) == (7, 11), f"stable-pair prime shell changed at {left}->{right}")
        left_beta = beta_vector(v19, left)
        right_beta = beta_vector(v19, right)
        overlap = tuple(sorted(set(left_shell) & set(right_shell)))
        require(all(left_beta[t] == right_beta[t] for t in overlap), f"stable-pair beta overlap changed at {left}->{right}")
        left_gamma = centered_covector(left_beta, left_shell, (7, 11))
        right_gamma = centered_covector(right_beta, right_shell, (7, 11))
        union = tuple(sorted(set(left_shell) | set(right_shell)))
        delta = {t: zero_extend(right_gamma, union)[t] - zero_extend(left_gamma, union)[t] for t in union}
        require(len(union) == union_size, f"stable-pair union changed at {left}->{right}")
        require(support(delta) == expected_support, f"stable-pair support changed at {left}->{right}")
        require(l1(delta) == expected_l1, f"stable-pair l1 changed at {left}->{right}")
        require(l2_squared(delta) == expected_l2, f"stable-pair l2 changed at {left}->{right}")
    return len(expected)


def validate_wall_census(v19: dict[str, object]) -> dict[str, int]:
    beta_stable = 0
    q_stable = 0
    joint_stable = 0
    beta_changes: dict[tuple[int, int], int] = {}
    q_changes: dict[tuple[int, int], tuple[tuple[int, ...], tuple[int, ...]]] = {}
    for left in range(100, 400, 2):
        right = left + 2
        overlap = tuple(sorted(set(shell_integers(left)) & set(shell_integers(right))))
        changed = sum(v19["raw_master_numerator"](t, left)[0] != v19["raw_master_numerator"](t, right)[0] for t in overlap)
        beta_is_stable = changed == 0
        q_left = active_prime_shell(left)
        q_right = active_prime_shell(right)
        q_is_stable = q_left == q_right
        beta_stable += int(beta_is_stable)
        q_stable += int(q_is_stable)
        joint_stable += int(beta_is_stable and q_is_stable)
        if not beta_is_stable:
            beta_changes[(left, right)] = changed
        if not q_is_stable:
            q_changes[(left, right)] = (q_left, q_right)
    require(beta_changes == {(126, 128): 13, (218, 220): 18, (348, 350): 24}, "finite beta wall census changed")
    require(q_changes == {(124, 126): ((5, 7), (7,)), (166, 168): ((7,), (7, 11)), (274, 276): ((7, 11), (7, 11, 13)), (342, 344): ((7, 11, 13), (11, 13))}, "finite q wall census changed")
    require((beta_stable, q_stable, joint_stable) == (147, 146, 143), "finite stable-pair counts changed")
    require(126**133 < 5**400 <= 128**133, "J=5 wall changed")
    require(218**133 < 6**400 <= 220**133, "J=6 wall changed")
    require(348**133 < 7**400 <= 350**133, "J=7 wall changed")
    return {"wall_pairs": 150, "beta_stable_pairs": beta_stable, "q_stable_pairs": q_stable, "joint_stable_pairs": joint_stable}


def validate_jutila_ledger() -> dict[str, str]:
    finite_shells = {
        5: ((7,), 6),
        10: ((11, 13, 17, 19), 56),
        11: ((13, 17, 19), 46),
    }
    for scale_q_mes, (expected_primes, expected_L) in finite_shells.items():
        source_cutoff_q_src = 2 * scale_q_mes
        primes = jutila_prime_shell(scale_q_mes)
        require(primes == expected_primes and jutila_L(primes) == expected_L, f"Q_mes={scale_q_mes} Jutila shell changed")
        require(all(scale_q_mes < prime <= source_cutoff_q_src for prime in primes), "prime shell left the source cutoff")
    eta = Fraction(1, 32)
    delta_exponent = -2 + eta
    dual_exponent = Fraction(1, 2) + eta
    branch_one = Fraction(1, 32) - 5 * eta / 16
    branch_two = Fraction(1, 18) - 2 * eta / 3
    q_saving = min(branch_one, branch_two)
    x_saving = q_saving / 3
    strict_margin = x_saving - Fraction(1, 400)
    original_margin = Fraction(1, 96) - Fraction(1, 400)
    arc_loss = Fraction(1, 96) - x_saving
    theta_threshold = eta / 6 - Fraction(1, 400)
    require(delta_exponent == Fraction(-63, 32), "Jutila delta exponent changed")
    require(dual_exponent == Fraction(17, 32), "dual support exponent changed")
    require(branch_one == Fraction(11, 512) and branch_two == Fraction(5, 144), "BP branches changed")
    require(q_saving == Fraction(11, 512), "selected BP q-saving changed")
    require(x_saving == Fraction(11, 1536), "BP q-to-x conversion changed")
    require(strict_margin == Fraction(179, 38400) and strict_margin > 0, "strict local margin changed")
    require(original_margin == Fraction(19, 2400), "original BP margin changed")
    require(arc_loss == Fraction(5, 1536), "arc-width BP loss changed")
    require(Fraction(3, 200) < eta < Fraction(173, 2400), "eta left the formal window")
    require(theta_threshold == Fraction(13, 4800), "pure-energy threshold changed")
    require(Fraction(1, 2) >= theta_threshold, "trivial energy was falsely accepted")
    return {
        "jutila_eta": "1/32",
        "jutila_source_cutoff": "Q_src=2Q_mes",
        "jutila_delta_exponent": "-63/32",
        "jutila_dual_exponent": "17/32",
        "bp_q_saving": "11/512",
        "bp_x_saving": "11/1536",
        "strict_local_margin": "179/38400",
        "pure_energy_theta_threshold": "13/4800",
    }


def wrong_type(value: object) -> object:
    if type(value) is bool:
        return 0
    if type(value) is int:
        return str(value)
    if type(value) is str:
        return (value,)
    raise CheckFailure("unsupported contract type")


def wrong_value(value: object) -> object:
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if type(value) is str:
        return value + "_FALSE_PROMOTION"
    raise CheckFailure("unsupported contract value")


def expect_rejected(action: Callable[[], None], label: str, labels: list[str]) -> None:
    try:
        action()
    except CheckFailure:
        labels.append(label)
    else:
        raise CheckFailure(f"mutation escaped: {label}")


def run_mutations() -> dict[str, int]:
    contract_labels: list[str] = []
    base_contract = dict(CONTRACT)
    for key in tuple(base_contract):
        missing = dict(base_contract)
        del missing[key]
        expect_rejected(lambda candidate=missing: validate_contract(candidate), f"missing::{key}", contract_labels)
        typed = dict(base_contract)
        typed[key] = wrong_type(typed[key])
        expect_rejected(lambda candidate=typed: validate_contract(candidate), f"wrong_type::{key}", contract_labels)
        valued = dict(base_contract)
        valued[key] = wrong_value(valued[key])
        expect_rejected(lambda candidate=valued: validate_contract(candidate), f"wrong_value::{key}", contract_labels)
    extra = dict(base_contract)
    extra["UNDECLARED"] = "FALSE_PROMOTION"
    expect_rejected(lambda: validate_contract(extra), "extra_key", contract_labels)
    promoted = dict(base_contract)
    promoted.update({"arithmetic_advance": True, "fixed_atom_credit": 1, "strict_1_over_400": "PAID", "L2": "PROVED", "TPC_207_TRIGGER": True, "survivor_status": "PROVED"})
    expect_rejected(lambda: validate_contract(promoted), "coordinated_false_release", contract_labels)
    decoy = {"decoy": "self_attested"}
    expect_rejected(lambda: validate_contract(decoy), "provider_decoy", contract_labels)
    expected_contract_labels = {f"{kind}::{key}" for key in base_contract for kind in ("missing", "wrong_type", "wrong_value")} | {"extra_key", "coordinated_false_release", "provider_decoy"}
    require(set(contract_labels) == expected_contract_labels and len(contract_labels) == len(set(contract_labels)) == 102, "contract mutation labels changed")

    registry_labels: list[str] = []
    base_registry = tuple(REGISTRY_ITEMS)
    for index, (key, value) in enumerate(base_registry):
        missing = base_registry[:index] + base_registry[index + 1:]
        expect_rejected(lambda candidate=missing: validate_registry(candidate, registry_hash(candidate)), f"missing::{key}", registry_labels)
        replaced_list = list(base_registry)
        replaced_list[index] = (f"UNKNOWN_{index:02d}", value)
        replaced = tuple(replaced_list)
        expect_rejected(lambda candidate=replaced: validate_registry(candidate, registry_hash(candidate)), f"replace_key::{key}", registry_labels)
        mutated_list = list(base_registry)
        mutated_list[index] = (key, value + "_FALSE_PROMOTION")
        mutated = tuple(mutated_list)
        expect_rejected(lambda candidate=mutated: validate_registry(candidate, registry_hash(candidate)), f"mutate_value::{key}", registry_labels)
    extra_registry = base_registry + (("EXTRA", "FALSE_PROMOTION"),)
    expect_rejected(lambda: validate_registry(extra_registry, registry_hash(extra_registry)), "extra_row", registry_labels)
    duplicate_registry = base_registry + (base_registry[0],)
    expect_rejected(lambda: validate_registry(duplicate_registry, registry_hash(duplicate_registry)), "duplicate_key", registry_labels)
    expect_rejected(lambda: validate_registry(list(base_registry), registry_hash(base_registry)), "wrong_container_type", registry_labels)
    expect_rejected(lambda: validate_registry(base_registry, 0), "wrong_digest_type", registry_labels)
    expect_rejected(lambda: validate_registry(base_registry, "0" * 64), "wrong_digest_value", registry_labels)
    swapped_list = list(base_registry)
    swapped_list[0] = (swapped_list[0][0], swapped_list[1][1])
    swapped_list[1] = (swapped_list[1][0], swapped_list[0][1])
    swapped = tuple(swapped_list)
    expect_rejected(lambda: validate_registry(swapped, registry_hash(swapped)), "swap_two_values", registry_labels)
    rehash_list = list(base_registry)
    rehash_list[-1] = ("RELEASE_BOUNDARY", "ARITHMETIC_YES_STRICT_PAID_L2_PROVED_TPC207_TRUE")
    rehashed = tuple(rehash_list)
    expect_rejected(lambda: validate_registry(rehashed, registry_hash(rehashed)), "coordinated_rehash", registry_labels)
    expected_registry_labels = {f"{kind}::{key}" for key, _ in base_registry for kind in ("missing", "replace_key", "mutate_value")} | {"extra_row", "duplicate_key", "wrong_container_type", "wrong_digest_type", "wrong_digest_value", "swap_two_values", "coordinated_rehash"}
    require(set(registry_labels) == expected_registry_labels and len(registry_labels) == len(set(registry_labels)) == 151, "registry mutation labels changed")
    return {"contract_mutations": len(contract_labels), "registry_mutations": len(registry_labels)}


def run_check() -> dict[str, object]:
    validate_contract(CONTRACT)
    validate_registry(REGISTRY_ITEMS, EXPECTED_REGISTRY_SHA256)
    _, v19 = load_dependencies()
    rank_cases = validate_rank_engine()
    stage = validate_stage_geometry(v19)
    stable_pair_cases = validate_stable_pairs(v19)
    walls = validate_wall_census(v19)
    ledger = validate_jutila_ledger()
    mutations = run_mutations()
    require(CONTRACT["arithmetic_advance"] is False and CONTRACT["TPC_207_TRIGGER"] is False, "release bool boundary changed")
    require(type(CONTRACT["fixed_atom_credit"]) is int and CONTRACT["fixed_atom_credit"] == 0, "fixed-atom boundary changed")
    require(CONTRACT["strict_1_over_400"] == "UNPAID" and CONTRACT["L2"] == "NONE", "strict/L2 boundary changed")
    return {
        "check": True,
        "claim": "EXACT_L0_PRIME_SHELL_JUTILA_EXPONENT_INTERFACE_AND_FINITE_TRANSPORT_FALSIFIERS",
        "contract_fields": 33,
        "contract_mutations": mutations["contract_mutations"],
        "registry_rows": 48,
        "registry_mutations": mutations["registry_mutations"],
        "registry_sha256": "15e40e8c20050549c3e244be59747019f115ebb8ccb9356f95fd449250073b07",
        "rank_engine_cases": rank_cases,
        "jutila_eta": ledger["jutila_eta"],
        "jutila_source_cutoff": ledger["jutila_source_cutoff"],
        "jutila_delta_exponent": ledger["jutila_delta_exponent"],
        "jutila_dual_exponent": ledger["jutila_dual_exponent"],
        "bp_q_saving": ledger["bp_q_saving"],
        "bp_x_saving": ledger["bp_x_saving"],
        "strict_local_margin": ledger["strict_local_margin"],
        "pure_energy_theta_threshold": ledger["pure_energy_theta_threshold"],
        "pure_energy_route": "STOP_SCOPED",
        "survivor": "OPEN_CONDITIONAL",
        "stable_pair_fixtures": stable_pair_cases,
        "wall_pairs": walls["wall_pairs"],
        "wall_beta_stable_pairs": walls["beta_stable_pairs"],
        "wall_q_stable_pairs": walls["q_stable_pairs"],
        "wall_joint_stable_pairs": walls["joint_stable_pairs"],
        "x166_beta_dft_support": stage["x166_beta_dft_support"],
        "x166_gamma_dft_support": stage["x166_gamma_dft_support"],
        "x168_beta_dft_support": stage["x168_beta_dft_support"],
        "x168_gamma_dft_support": stage["x168_gamma_dft_support"],
        "x166_x168_gamma_update_support": stage["x166_x168_gamma_update_support"],
        "q11_innovation_dft_support": stage["q11_innovation_dft_support"],
        "arithmetic_advance": False,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run the read-only V23 checker")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require(args.check is True, "the explicit --check entry is required")
    print(json.dumps(run_check(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
