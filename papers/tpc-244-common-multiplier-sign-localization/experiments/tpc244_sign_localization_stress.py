#!/usr/bin/env python3
"""Exact finite stress census for TPC-244 sign localization."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction


STATUS = "PROVED_STRUCTURAL_L1_COMMON_MULTIPLIER_SIGN_LOCALIZATION"
Gaussian = tuple[Fraction, Fraction]
Vector = tuple[Gaussian, ...]


class StressFailure(RuntimeError):
    """Fail-closed stress-census error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise StressFailure(message)


def z(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    return (Fraction(real), Fraction(imag))


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def scale(value: Gaussian, scalar: int | Fraction) -> Gaussian:
    factor = Fraction(scalar)
    return (factor * value[0], factor * value[1])


def inner(first: Vector, second: Vector) -> Gaussian:
    require(len(first) == len(second), "stress dimension mismatch")
    total = z()
    for left, right in zip(first, second):
        total = add(total, mul(conj(left), right))
    return total


def direct_sum_census() -> tuple[int, int, int]:
    alphabet = (z(), z(1), z(0, 1))
    vectors = list(itertools.product(alphabet, repeat=4))
    patterns = list(itertools.product((-1, 1), repeat=4))
    multipliers = (1, -2, 3, -4)
    covariance_checks = 0
    asymmetric_sensitive = 0
    pair_count = 0
    for w_value in vectors:
        for b_value in vectors:
            pair_count += 1
            baseline_w = tuple(scale(entry, scalar)
                               for entry, scalar in zip(w_value, multipliers))
            baseline_b = tuple(scale(entry, scalar)
                               for entry, scalar in zip(b_value, multipliers))
            baseline = inner(baseline_w, baseline_b)
            asymmetric_values: set[Gaussian] = set()
            for pattern in patterns:
                signed_w = tuple(scale(entry, sign * scalar)
                                 for entry, sign, scalar in zip(w_value, pattern, multipliers))
                signed_b = tuple(scale(entry, sign * scalar)
                                 for entry, sign, scalar in zip(b_value, pattern, multipliers))
                require(inner(signed_w, signed_b) == baseline,
                        "common-sign direct-sum invariance")
                covariance_checks += 1
                asymmetric_values.add(inner(signed_w, baseline_b))
            if len(asymmetric_values) > 1:
                asymmetric_sensitive += 1
    require(asymmetric_sensitive > 0, "asymmetric lane control must be sensitive")
    return len(vectors), pair_count, covariance_checks


def balanced_digits(value: int, width: int) -> tuple[int, ...]:
    digits: list[int] = []
    current = value
    for _ in range(width):
        digits.append((current % 3) - 1)
        current //= 3
    return tuple(digits)


def cut_census() -> tuple[int, int, int]:
    patterns = list(itertools.product((-1, 1), repeat=3))
    multipliers = (2, -3, 5)
    case_count = 0
    pattern_checks = 0
    nonconstant_cases = 0
    for case in range(27):
        digits = balanced_digits(case, 6)
        matrix: list[list[Gaussian]] = [[z() for _ in range(3)] for _ in range(3)]
        cursor = 0
        for h in range(3):
            matrix[h][h] = z(h + 1, digits[h])
        for h in range(3):
            for k in range(h + 1, 3):
                matrix[h][k] = z(digits[cursor], digits[(cursor + 1) % 6])
                matrix[k][h] = z(digits[(cursor + 2) % 6], -digits[cursor])
                cursor += 2
        diagonal = z()
        edges: dict[tuple[int, int], Gaussian] = {}
        for h in range(3):
            diagonal = add(diagonal, scale(matrix[h][h], multipliers[h] ** 2))
            for k in range(h + 1, 3):
                edges[(h, k)] = scale(add(matrix[h][k], matrix[k][h]),
                                      multipliers[h] * multipliers[k])
        baseline = diagonal
        for edge in edges.values():
            baseline = add(baseline, edge)
        values: set[Gaussian] = set()
        for pattern in patterns:
            polynomial = diagonal
            cut_sum = z()
            for (h, k), edge in edges.items():
                polynomial = add(polynomial, scale(edge, pattern[h] * pattern[k]))
                if pattern[h] != pattern[k]:
                    cut_sum = add(cut_sum, edge)
            require(polynomial == add(baseline, scale(cut_sum, -2)),
                    "stress cut identity")
            values.add(polynomial)
            pattern_checks += 1
        all_edges_zero = all(edge == z() for edge in edges.values())
        require((len(values) == 1) == all_edges_zero,
                "stress all-sign iff criterion")
        if len(values) > 1:
            nonconstant_cases += 1
        case_count += 1
    require(nonconstant_cases > 0, "cut census needs nonconstant cases")
    return case_count, pattern_checks, nonconstant_cases


def run() -> None:
    vectors, pairs, direct_checks = direct_sum_census()
    cut_cases, cut_checks, nonconstant = cut_census()
    result = {
        "classification": "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
        "coefficient_alphabet": ["0", "1", "i"],
        "vectors": vectors,
        "ordered_vector_pairs": pairs,
        "common_sign_patterns": 16,
        "direct_covariance_checks": direct_checks,
        "cut_matrix_cases": cut_cases,
        "cut_pattern_checks": cut_checks,
        "cut_nonconstant_cases": nonconstant,
        "asymmetric_lane_control": "SIGN_SENSITIVE",
        "theorem_status": STATUS,
        "status": "PASS",
    }
    print("TPC244_SIGN_LOCALIZATION_STRESS=PASS")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC244_SIGN_LOCALIZATION_STRESS=FAIL: use --check")
    try:
        run()
    except (StressFailure, KeyError, TypeError, ValueError) as error:
        raise SystemExit("TPC244_SIGN_LOCALIZATION_STRESS=FAIL: " + str(error))


if __name__ == "__main__":
    main()
