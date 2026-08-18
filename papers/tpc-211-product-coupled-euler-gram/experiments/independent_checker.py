#!/usr/bin/env python3
"""Independent exact checker for the TPC-211 certificate.

This file intentionally reimplements the finite algebra instead of importing
the producer module.  It checks the structural identities, rank, determinant,
and shared-endpoint alignment from the serialized certificate.
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from math import prod
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results" / "certificate.json"
CASES = ((5, 7), (5, 7, 11), (5, 7, 11, 13))
CUTOFF = 3


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise CheckFailure(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def masks(primes: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(range(1, 1 << len(primes)))


def local_f(prime: int, residue: int) -> Fraction:
    return Fraction(0, 1) if (residue + 2) % prime == 0 else Fraction(prime, prime - 1)


def local_g(prime: int, residue: int) -> Fraction:
    return (
        Fraction(prime, prime - 1)
        if residue % prime == 0
        else Fraction(prime * (prime - 2), (prime - 1) ** 2)
    )


def profile_rows(primes: tuple[int, ...]) -> dict[int, tuple[Fraction, ...]]:
    modulus = prod(primes)
    result: dict[int, tuple[Fraction, ...]] = {}
    for mask in masks(primes):
        values: list[Fraction] = []
        for residue in range(modulus):
            p_value = Fraction(1, 1)
            b_value = Fraction(1, 1)
            for index, prime in enumerate(primes):
                if (mask >> index) & 1:
                    p_value *= local_f(prime, residue)
                    b_value *= local_g(prime, residue)
            values.append(p_value - b_value)
        result[mask] = tuple(values)
    return result


def inner(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0, 1))


def gram(rows: dict[int, tuple[Fraction, ...]]) -> list[list[Fraction]]:
    vectors = [rows[mask] for mask in rows]
    return [[inner(left, right) for right in vectors] for left in vectors]


def rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (index for index in range(pivot_row, row_count) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for index in range(row_count):
            if index == pivot_row or not work[index][column]:
                continue
            factor = work[index][column]
            work[index] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[index], work[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    work = [row[:] for row in matrix]
    value = Fraction(1, 1)
    for column in range(len(work)):
        pivot = next(
            (index for index in range(column, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            return Fraction(0, 1)
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
            value = -value
        diagonal = work[column][column]
        value *= diagonal
        work[column] = [entry / diagonal for entry in work[column]]
        for index in range(column + 1, len(work)):
            if not work[index][column]:
                continue
            factor = work[index][column]
            work[index] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[index], work[column])
            ]
    return value


def solve(matrix: list[list[Fraction]], target: list[Fraction]) -> list[Fraction]:
    size = len(matrix)
    augmented = [row[:] + [target[index]] for index, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(
            (index for index in range(column, size) if augmented[index][column]),
            None,
        )
        require(pivot is not None, "Gram matrix unexpectedly singular")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for index in range(size):
            if index == column or not augmented[index][column]:
                continue
            factor = augmented[index][column]
            augmented[index] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(augmented[index], augmented[column])
            ]
    return [row[-1] for row in augmented]


def mask_mu(mask: int) -> int:
    return -1 if mask.bit_count() % 2 else 1


def endpoint_coefficients(primes: tuple[int, ...]) -> list[int]:
    return [
        sum(mask_mu(mask) for mask in masks(primes) if (mask >> index) & 1)
        for index in range(len(primes))
    ]


def derivative_identity(primes: tuple[int, ...], rows: dict[int, tuple[Fraction, ...]]) -> bool:
    modulus = prod(primes)
    for marked, prime in enumerate(primes):
        coefficient = [Fraction(0, 1) for _ in range(modulus)]
        for mask, vector in rows.items():
            if (mask >> marked) & 1:
                sign = mask_mu(mask)
                coefficient = [
                    old + sign * value for old, value in zip(coefficient, vector)
                ]
        derivative: list[Fraction] = []
        for residue in range(modulus):
            p_term = Fraction(1, 1)
            b_term = Fraction(1, 1)
            for index, other in enumerate(primes):
                if index == marked:
                    p_term *= local_f(other, residue)
                    b_term *= local_g(other, residue)
                else:
                    p_term *= 1 - local_f(other, residue)
                    b_term *= 1 - local_g(other, residue)
            derivative.append(p_term - b_term)
        require(
            all(old + new == 0 for old, new in zip(coefficient, derivative)),
            f"log derivative identity p={prime}",
        )
    return True


def check_cocycle(primes: tuple[int, ...], rows: dict[int, tuple[Fraction, ...]]) -> None:
    modulus = prod(primes)
    left_mask, right_mask = 1, 2
    union = left_mask | right_mask
    for residue in range(modulus):
        p_left = b_right = Fraction(1, 1)
        for index, prime in enumerate(primes):
            if (left_mask >> index) & 1:
                p_left *= local_f(prime, residue)
            if (right_mask >> index) & 1:
                b_right *= local_g(prime, residue)
        expected = p_left * rows[right_mask][residue] + b_right * rows[left_mask][residue]
        require(rows[union][residue] == expected, "cocycle identity")


def check_case(primes: tuple[int, ...], record: dict[str, object]) -> None:
    rows = profile_rows(primes)
    ordered_masks = list(rows)
    matrix = gram(rows)
    expected_count = len(ordered_masks)
    require(record["primes"] == list(primes), f"primes {primes}")
    require(record["cutoff"] == CUTOFF, f"cutoff {primes}")
    require(record["modulus"] == prod(primes), f"modulus {primes}")
    require(record["divisor_masks"] == ordered_masks, f"masks {primes}")
    require(record["divisor_count"] == expected_count, f"count {primes}")
    require(record["profile_rank"] == rank([list(row) for row in rows.values()]), f"rank {primes}")
    require(record["profile_rank"] == expected_count, f"full rank {primes}")
    require(Fraction(record["gram_determinant"]) == determinant(matrix), f"determinant {primes}")
    require(record["endpoint_alignment"] is True, f"alignment flag {primes}")
    target = [Fraction(mask_mu(mask), 1) for mask in ordered_masks]
    coefficients = solve(matrix, target)
    endpoint = [
        sum((coefficients[j] * rows[mask][index] for j, mask in enumerate(ordered_masks)), Fraction(0, 1))
        for index in range(prod(primes))
    ]
    correlations = [inner(tuple(endpoint), rows[mask]) for mask in ordered_masks]
    require(correlations == target, f"shared endpoint target {primes}")
    require(record["mobius_correlations"] == [str(value) for value in correlations], f"correlations {primes}")
    coherent = sum((correlations[i] * target[i] for i in range(expected_count)), Fraction(0, 1))
    diagonal = sum((value * value for value in correlations), Fraction(0, 1))
    require(Fraction(record["coherent_energy"]) == coherent * coherent, f"coherent energy {primes}")
    require(Fraction(record["diagonal_energy"]) == diagonal, f"diagonal energy {primes}")
    require(Fraction(record["coherent_to_diagonal_ratio"]) == expected_count, f"ratio {primes}")
    require(record["log_derivative_identity"] is derivative_identity(primes, rows), f"derivative flag {primes}")
    require(record["endpoint_packet_coefficients"] == endpoint_coefficients(primes), f"endpoint coefficients {primes}")
    require(record["endpoint_packet_coefficients"] == [0] * len(primes), f"endpoint cancellation {primes}")
    check_cocycle(primes, rows)
    require(record["cocycle_5_7"] is True, f"cocycle flag {primes}")
    endpoint_norm = inner(tuple(endpoint), tuple(endpoint))
    require(Fraction(record["endpoint_vector_norm_squared"]) == endpoint_norm, f"endpoint norm {primes}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")
    if not CERTIFICATE.is_file():
        print("TPC211_INDEPENDENT_CHECK=FAIL missing certificate", file=sys.stderr)
        return 1
    try:
        raw = CERTIFICATE.read_text(encoding="utf-8")
        data = json.loads(raw, object_pairs_hook=unique_object)
        require(data["schema"] == "TPC211_PRODUCT_COUPLED_EULER_GRAM_CERTIFICATE_V1", "schema")
        require(data["classification"] == "PROVED_STRUCTURAL_L1_STOP_SCOPED_PHYSICAL_COUPLING", "classification")
        require(data["cutoff"] == CUTOFF, "global cutoff")
        cases = data["cases"]
        require(type(cases) is dict and list(cases) == ["5-7", "5-7-11", "5-7-11-13"], "case order")
        for primes in CASES:
            key = "-".join(str(prime) for prime in primes)
            check_case(primes, cases[key])
        counts = data["audit_counts"]
        require(counts == {
            "prime_set_rows": 3,
            "profile_rows": 25,
            "crt_residue_rows": 77875,
            "derivative_rows": 9,
        }, "audit counts")
        print("TPC211_INDEPENDENT_CHECK=PASS")
        print("full_rank_cases=3")
        print("shared_endpoint_alignment=3/3")
        print("log_derivative_cases=3/3")
        print("claim_level=PROVED_STRUCTURAL_L1_STOP_SCOPED_PHYSICAL_COUPLING")
        return 0
    except (CheckFailure, KeyError, TypeError, ValueError) as error:
        print(f"TPC211_INDEPENDENT_CHECK=FAIL {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
