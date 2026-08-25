#!/usr/bin/env python3
"""Exact exhaustive stress test for the TPC-245 covariance identities."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction


Gaussian = tuple[Fraction, Fraction]
Vector = tuple[Gaussian, ...]
STATUS = "PROVED_STRUCTURAL_L1_SHARP_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISKS"


class StressFailure(RuntimeError):
    """Fail-closed stress error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise StressFailure(message)


def z(real: int = 0, imag: int = 0) -> Gaussian:
    return (Fraction(real), Fraction(imag))


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def abs_sq(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def inner(first: Vector, second: Vector) -> Gaussian:
    require(len(first) == len(second), "dimension")
    total = z()
    for left, right in zip(first, second):
        total = add(total, mul(conj(left), right))
    return total


def norm_sq(value: Vector) -> Fraction:
    answer = inner(value, value)
    require(answer[1] == 0 and answer[0] >= 0, "norm")
    return answer[0]


def audit_dimension(vectors: tuple[Vector, ...], transverse_dimension: int) -> dict[str, int]:
    ordered_pairs = 0
    decomposition_checks = 0
    cauchy_checks = 0
    equality_cases = 0
    zero_radius_cases = 0
    for b_vector, w_vector in itertools.product(vectors, repeat=2):
        ordered_pairs += 1
        b = b_vector[0]
        w = w_vector[0]
        bp = b_vector[1:]
        wp = w_vector[1:]
        center = mul(conj(w), b)
        transverse = inner(wp, bp)
        covariance = inner(w_vector, b_vector)
        require(covariance == add(center, transverse), "decomposition")
        decomposition_checks += 1
        eb = norm_sq(bp)
        ew = norm_sq(wp)
        require(abs_sq(transverse) <= eb * ew, "Cauchy")
        cauchy_checks += 1
        if abs_sq(transverse) == eb * ew:
            equality_cases += 1
        if eb * ew == 0:
            require(transverse == z(), "zero radius")
            zero_radius_cases += 1
        if transverse_dimension == 1 and eb * ew > 0:
            require(abs_sq(transverse) == eb * ew, "one-dimensional circle")
    return {
        "cauchy_checks": cauchy_checks,
        "decomposition_checks": decomposition_checks,
        "equality_cases": equality_cases,
        "ordered_pairs": ordered_pairs,
        "zero_radius_cases": zero_radius_cases,
    }


def run() -> dict[str, object]:
    alphabet = (z(), z(1), z(-1), z(0, 1), z(0, -1))
    dim_two_vectors = tuple(itertools.product(alphabet, repeat=3))
    dim_one_vectors = tuple(itertools.product(alphabet, repeat=2))
    result_two = audit_dimension(dim_two_vectors, 2)
    result_one = audit_dimension(dim_one_vectors, 1)
    require(result_two["ordered_pairs"] == len(dim_two_vectors) ** 2,
            "dimension-two census")
    require(result_one["ordered_pairs"] == len(dim_one_vectors) ** 2,
            "dimension-one census")
    return {
        "alphabet_size": len(alphabet),
        "classification": "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
        "dimension_one": result_one,
        "dimension_one_vectors": len(dim_one_vectors),
        "dimension_two": result_two,
        "dimension_two_vectors": len(dim_two_vectors),
        "status": "PASS",
        "theorem_status": STATUS,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC245_COVARIANCE_DISK_STRESS=FAIL: use --check")
    try:
        record = run()
        print("TPC245_COVARIANCE_DISK_STRESS=PASS")
        print(json.dumps(record, sort_keys=True, separators=(",", ":")))
    except (StressFailure, TypeError, ValueError) as error:
        raise SystemExit("TPC245_COVARIANCE_DISK_STRESS=FAIL: " + str(error))


if __name__ == "__main__":
    main()
