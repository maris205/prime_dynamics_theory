#!/usr/bin/env python3
"""Exact read-only checker for the TPC Bridge-B physical-dual rank barrier.

The checker verifies finite integer/rational linear algebra only.  It neither
constructs a Logistic/Henon carrier nor supplies an arithmetic saving.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction


REGISTRY = {
    "BRIDGE_B_ACTUAL_INTERVAL_PLUS_MEAN_RANK": "PROVED_EXACT_GROWING_BANDCOUNT_K_PLUS_1",
    "BRIDGE_B_ACTUAL_STAGE_BAND_INTERVAL_RANK": "PROVED_EXACT_GROWING_BANDCOUNT_K",
    "BRIDGE_B_ALL_TRANSLATIONS_CURRENT_GATE": "NO",
    "BRIDGE_B_ALL_TRANSLATIONS_FIXED_RANK_RETURN": "STOP_SCOPED_NEAR_PRIMORIAL_RANK",
    "BRIDGE_B_APPROXIMATE_LOW_RANK_RETURN": "OPEN_REQUIRES_WIDTH_AND_PHYSICAL_NORM",
    "BRIDGE_B_ARITHMETIC_ADVANCE": "NO",
    "BRIDGE_B_BRATTELI_FIXED_VERTEX_RANK": "NOT_STOPPED_WITHOUT_LEVEL_STATE_FACTORIZATION",
    "BRIDGE_B_COMMON_STAGE_FIXED_RANK_EXACT_RETURN": "STOP_SCOPED_STAGE_BAND_RANK_GROWTH",
    "BRIDGE_B_COMMON_STAGE_GROWING_SPARSE_CARRIER": "SELECTED_OPEN_NEW_THEOREM",
    "BRIDGE_B_HENON_FIXED_FINITE_DICTIONARY_EXACT_RETURN": "STOP_SCOPED_IF_COMMON_STAGE_RETURN",
    "BRIDGE_B_HENON_GROWING_OBSERVABLE_FAMILY": "OPTIONAL_OPEN_EXACT_FACTOR_REQUIRED",
    "BRIDGE_B_INTERVAL_DIFFERENCE_BASIS": "PROVED_EXACT_THREE_SPARSE",
    "BRIDGE_B_LOGISTIC_FIXED_FINITE_DICTIONARY_EXACT_RETURN": "STOP_SCOPED_IF_COMMON_STAGE_RETURN",
    "BRIDGE_B_LOGISTIC_GROWING_FUNCTION_SPACE": "OPEN_REQUIRES_FORCING_AND_LOSS_LEDGER",
    "BRIDGE_B_STAGE_BAND_CARDINALITY": "PROVED_EXACT_BANDCOUNT_K",
    "BRIDGE_B_STAGE_BAND_NO_WRAP_K_GE_4": "PROVED_EXACT",
    "BRIDGE_B_S_ADIC_FIXED_ALPHABET": "NOT_STOPPED_WITHOUT_LEVEL_STATE_FACTORIZATION",
    "BRIDGE_B_TRANSLATED_INTERVAL_CIRCULANT_RANK": "PROVED_EXACT_P_MINUS_GCD_PLUS_1",
    "BRIDGE_B_X_SPECIFIC_ONE_SCALE_FIT": "STOP_SCOPED_NO_COMMON_COCYCLE",
    "BRIDGE_B_X_SPECIFIC_UNIFORM_TRIANGULAR_FAMILY": "OPEN_RESERVE_REQUIRES_UNIFORM_LEDGER",
    "FIXED_ATOM_CREDIT": "0",
    "L2": "NONE",
    "STRICT_1_OVER_400": "UNPAID",
    "TPC_207_TRIGGER": "false",
}

EXPECTED_REGISTRY_SHA256 = "8edf44c0af0146acfe9f0cb7e9c1a72f53bc2a05dc852cac11e547db478f2aac"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_registry_bytes(registry: dict[str, str]) -> bytes:
    return "".join(
        f"{key}\t{registry[key]}\n" for key in sorted(registry)
    ).encode("utf-8")


def registry_sha256(registry: dict[str, str]) -> str:
    return hashlib.sha256(canonical_registry_bytes(registry)).hexdigest()


def exact_rank(matrix: list[list[int | Fraction]]) -> int:
    if not matrix:
        return 0
    width = len(matrix[0])
    require(width > 0, "empty matrix width")
    require(all(len(row) == width for row in matrix), "ragged matrix")
    work = [[Fraction(value) for value in row] for row in matrix]
    height = len(work)
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, height) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def stage_band(physical_prime: int, next_prime: int) -> tuple[int, int, int]:
    require(physical_prime > 2 and physical_prime % 2 == 1, "p must be odd")
    require(next_prime > physical_prime and next_prime % 2 == 1, "q must be odd")
    lower = (physical_prime * physical_prime - 1) // 2
    upper = (next_prime * next_prime - 3) // 2
    count = upper - lower + 1
    require(
        count == (next_prime * next_prime - physical_prime * physical_prime) // 2,
        "stage-band cardinality identity failed",
    )
    return lower, upper, count


def interval_coefficient(modulus: int, scale: int, residue: int) -> int:
    """Coefficient of f(residue) in sum_(scale<n<=2*scale) f(n mod modulus)."""
    require(modulus > 0 and 0 <= residue < modulus, "invalid residue")
    return (2 * scale - residue) // modulus - (scale - residue) // modulus


def interval_row(modulus: int, scale: int) -> list[int]:
    return [interval_coefficient(modulus, scale, residue) for residue in range(modulus)]


def sparse_interval_row(modulus: int, scale: int) -> dict[int, int]:
    result: dict[int, int] = {}
    for integer in range(scale + 1, 2 * scale + 1):
        residue = integer % modulus
        result[residue] = result.get(residue, 0) + 1
    return {residue: value for residue, value in result.items() if value}


def sparse_difference(
    left: dict[int, int], right: dict[int, int]
) -> dict[int, int]:
    keys = set(left) | set(right)
    return {
        key: left.get(key, 0) - right.get(key, 0)
        for key in keys
        if left.get(key, 0) != right.get(key, 0)
    }


def no_wrap_stage_fixture(
    stage: int, physical_prime: int, next_prime: int, primorial: int
) -> dict[str, int | str]:
    lower, upper, count = stage_band(physical_prime, next_prime)
    require(stage >= 4, "no-wrap theorem fixture must have k>=4")
    require(2 * upper < primorial, "stage band wraps modulo the primorial")
    for scale in range(lower, upper + 1):
        value = 2 * scale + 2
        require(
            physical_prime * physical_prime <= value < next_prime * next_prime,
            "scale assigned to wrong prime stage",
        )

    scales = list(range(lower, upper + 1))
    endpoint_minor = [
        [interval_coefficient(primorial, scale, 2 * witness) for witness in scales]
        for scale in scales
    ]
    for row in range(count):
        require(endpoint_minor[row][row] == 1, "endpoint minor lost unit diagonal")
        for column in range(row + 1, count):
            require(endpoint_minor[row][column] == 0, "endpoint minor not triangular")
    require(exact_rank(endpoint_minor) == count, "actual interval rank failed")

    augmented = [
        row + [interval_coefficient(primorial, scale, 0)]
        for row, scale in zip(endpoint_minor, scales)
    ]
    augmented.append([1] * (count + 1))
    require(exact_rank(augmented) == count + 1, "Haar-mean augmentation failed")

    for scale in range(lower + 1, upper + 1):
        current = sparse_interval_row(primorial, scale)
        previous = sparse_interval_row(primorial, scale - 1)
        difference = sparse_difference(current, previous)
        expected = {scale: -1, 2 * scale - 1: 1, 2 * scale: 1}
        require(difference == expected, "three-sparse interval difference failed")

    return {
        "stage": stage,
        "physical_prime": physical_prime,
        "next_prime": next_prime,
        "primorial": primorial,
        "lower_scale": lower,
        "upper_scale": upper,
        "band_count": count,
        "interval_rank": count,
        "mean_augmented_rank": count + 1,
        "difference_sparsity": 3,
    }


def wrap_control(
    stage: int, physical_prime: int, next_prime: int, primorial: int
) -> dict[str, int | bool]:
    lower, upper, count = stage_band(physical_prime, next_prime)
    rows = [interval_row(primorial, scale) for scale in range(lower, upper + 1)]
    return {
        "stage": stage,
        "primorial": primorial,
        "band_count": count,
        "exact_rank": exact_rank(rows),
        "whole_band_no_wrap": 2 * upper < primorial,
    }


def translated_interval_matrix(modulus: int, length: int) -> list[list[int]]:
    require(modulus >= 1 and length >= 1, "positive modulus and length required")
    matrix: list[list[int]] = []
    for translate in range(modulus):
        row = [0] * modulus
        for step in range(1, length + 1):
            row[(translate + step) % modulus] += 1
        matrix.append(row)
    return matrix


def translated_interval_rank_formula(modulus: int, length: int) -> int:
    require(modulus >= 1 and length >= 1, "positive modulus and length required")
    return modulus - math.gcd(modulus, length) + 1


def run_check() -> dict[str, object]:
    digest = registry_sha256(REGISTRY)
    require(digest == EXPECTED_REGISTRY_SHA256, "canonical V17 registry hash mismatch")

    stage_fixtures = [
        no_wrap_stage_fixture(4, 7, 11, 210),
        no_wrap_stage_fixture(5, 11, 13, 2310),
        no_wrap_stage_fixture(6, 13, 17, 30030),
    ]
    wrap_controls = [
        wrap_control(2, 3, 5, 6),
        wrap_control(3, 5, 7, 30),
    ]
    require(wrap_controls[0]["exact_rank"] == 5, "k=2 wrap-control rank changed")
    require(wrap_controls[1]["exact_rank"] == 12, "k=3 wrap-control rank changed")

    enumerated = 0
    for modulus in range(1, 17):
        for length in range(1, 2 * modulus + 3):
            matrix_rank = exact_rank(translated_interval_matrix(modulus, length))
            formula_rank = translated_interval_rank_formula(modulus, length)
            require(matrix_rank == formula_rank, "translated-interval rank formula failed")
            enumerated += 1
    require(enumerated == 304, "translated-rank enumeration count changed")

    large_circulant_fixtures = []
    for modulus, length, expected in (
        (6, 4, 5),
        (30, 10, 21),
        (30, 9, 28),
        (210, 24, 205),
        (2310, 60, 2281),
        (2310, 77, 2234),
        (30030, 84, 29989),
        (30, 1, 30),
        (30, 30, 1),
    ):
        actual = translated_interval_rank_formula(modulus, length)
        require(actual == expected, "large circulant fixture changed")
        large_circulant_fixtures.append(
            {"modulus": modulus, "length": length, "rank": actual}
        )

    lower, upper, count = stage_band(7, 11)
    require(interval_coefficient(210, lower, lower) == 0, "open-left anchor failed")
    closed_left_mutation = interval_coefficient(210, lower, lower) + 1
    require(closed_left_mutation != 0, "closed-left mutation escaped")
    scales = list(range(lower, upper + 1))
    correct_minor = [
        [interval_coefficient(210, scale, 2 * witness) for witness in scales]
        for scale in scales
    ]
    require(exact_rank(correct_minor[:-1]) == count - 1, "drop-scale mutation escaped")
    wrong_upper = upper + 1
    require(
        not (7 * 7 <= 2 * wrong_upper + 2 < 11 * 11),
        "stage upper-endpoint mutation escaped",
    )
    shifted_minor = [
        [interval_coefficient(210, scale, 2 * witness + 1) for witness in scales]
        for scale in scales
    ]
    require(exact_rank(shifted_minor) == count - 1, "wrong witness mutation escaped")
    correct_difference = sparse_difference(
        sparse_interval_row(210, lower + 1), sparse_interval_row(210, lower)
    )
    missing_negative_atom = {
        key: value for key, value in correct_difference.items() if value > 0
    }
    require(
        missing_negative_atom != correct_difference,
        "missing-negative-atom mutation escaped",
    )
    require(
        translated_interval_rank_formula(30, 10) != 30 - math.gcd(30, 10),
        "constant Fourier mode mutation escaped",
    )
    require(
        translated_interval_rank_formula(30, 10)
        != translated_interval_rank_formula(30, 11),
        "length-plus-one mutation escaped",
    )
    require(
        1 < translated_interval_rank_formula(30, 10),
        "single-translation mutation escaped",
    )

    return {
        "status": "PASS",
        "claim_level": "EXACT_PHYSICAL_DUAL_RANK_GEOMETRY_NO_ARITHMETIC_ADVANCE",
        "stage_fixtures": stage_fixtures,
        "wrap_controls": wrap_controls,
        "translated_rank_cases_enumerated": enumerated,
        "large_circulant_fixtures": large_circulant_fixtures,
        "mutation_tests": {
            "closed_left_interval": "DETECTED",
            "drop_one_stage_scale": "DETECTED",
            "include_upper_scale_plus_one": "DETECTED",
            "shift_witness_columns": "DETECTED",
            "difference_missing_negative_atom": "DETECTED",
            "circulant_forget_constant_mode": "DETECTED",
            "circulant_length_plus_one": "DETECTED",
            "single_translation_claimed_all_translations": "DETECTED",
        },
        "registry_rows": len(REGISTRY),
        "registry_sha256": digest,
        "arithmetic_advance": False,
        "tpc_207_trigger": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run exact read-only checks")
    parser.add_argument(
        "--registry-hash", action="store_true", help="print the canonical registry hash"
    )
    args = parser.parse_args()
    if args.registry_hash:
        print(registry_sha256(REGISTRY))
        return 0
    if not args.check:
        parser.error("use --check")
    print(json.dumps(run_check(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
