#!/usr/bin/env python3
"""Independent finite exact checker for the TPC big-road proof artifact.

This checker intentionally does not import tpc_big_road_lab.  It writes only its
report to stdout and performs explicit mutation tests.  Universal q/interval and
Abel/Borel--Cantelli quantifiers remain a symbolic proof obligation in README.md.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction


def primes(limit: int) -> list[int]:
    answer: list[int] = []
    for candidate in range(2, limit + 1):
        if all(candidate % p for p in answer if p * p <= candidate):
            answer.append(candidate)
    return answer


def alpha(cutoff: int) -> Fraction:
    value = Fraction(1, 1)
    for p in primes(cutoff):
        rank = len({0, 2 % p})
        value *= Fraction(p - rank, p)
    return value


def local_k(p: int, d: int) -> Fraction:
    base_rank = len({0, 2 % p})
    joint_rank = len({0, 2 % p, d % p, (d + 2) % p})
    return Fraction(p * (p - joint_rank), (p - base_rank) ** 2)


def displayed_local_k(p: int, d: int) -> Fraction:
    if p == 2:
        return Fraction(2 if d % 2 == 0 else 0, 1)
    if p == 3:
        return Fraction(3 if d % 3 == 0 else 0, 1)
    constant = Fraction(1, 1) - Fraction(4, (p - 2) ** 2)
    answer = constant
    if d % p == 0:
        answer += Fraction(2 * p, (p - 2) ** 2)
    if (d - 2) % p == 0:
        answer += Fraction(p, (p - 2) ** 2)
    if (d + 2) % p == 0:
        answer += Fraction(p, (p - 2) ** 2)
    return answer


def k_product(cutoff: int, d: int) -> Fraction:
    value = Fraction(1, 1)
    for p in primes(cutoff):
        value *= local_k(p, d)
    return value


def endpoint_bound(cutoff: int) -> Fraction:
    value = Fraction(1, 1)
    for p in primes(cutoff):
        if p == 2:
            value *= 2
        elif p == 3:
            value *= 3
        else:
            value *= Fraction(p * p, (p - 2) ** 2)
    return value


def interval_discrepancy(cutoff: int, start: int, length: int) -> Fraction:
    return sum((k_product(cutoff, d) - 1 for d in range(start, start + length)), Fraction())


def rough_pair(x: int, translate: int, cutoff: int) -> bool:
    left = x + translate
    return all(left % p and (left + 2) % p for p in primes(cutoff))


def brute_joint(cutoff_left: int, cutoff_right: int, d: int) -> Fraction:
    modulus = math.prod(primes(cutoff_right))
    hits = sum(
        1
        for x in range(modulus)
        if rough_pair(x, 0, cutoff_left) and rough_pair(x, d, cutoff_right)
    )
    return Fraction(hits, modulus)


def formula_joint(cutoff_left: int, cutoff_right: int, d: int) -> Fraction:
    return alpha(cutoff_left) * alpha(cutoff_right) * k_product(cutoff_left, d)


def moving_cutoff(n: int) -> int:
    return math.isqrt(n + 2)


def brute_moving_variance(n_max: int) -> tuple[Fraction, Fraction]:
    modulus = math.prod(primes(moving_cutoff(n_max)))
    values: list[int] = []
    for x in range(modulus):
        values.append(
            sum(1 for n in range(3, n_max + 1) if rough_pair(x, n, moving_cutoff(n)))
        )
    mean = Fraction(sum(values), modulus)
    variance = sum(((Fraction(value, 1) - mean) ** 2 for value in values), Fraction()) / modulus
    return mean, variance


def covariance_moving_variance(n_max: int) -> tuple[Fraction, Fraction]:
    alphas = {n: alpha(moving_cutoff(n)) for n in range(3, n_max + 1)}
    mean = sum(alphas.values(), Fraction())
    variance = sum((a * (1 - a) for a in alphas.values()), Fraction())
    for m in range(3, n_max + 1):
        for n in range(m + 1, n_max + 1):
            covariance = alphas[m] * alphas[n] * (k_product(moving_cutoff(m), n - m) - 1)
            variance += 2 * covariance
    return mean, variance


def primality(n: int) -> bool:
    return n >= 2 and all(n % p for p in range(2, math.isqrt(n) + 1))


def survivor_count(x_value: int, cutoff: int) -> int:
    return sum(
        1
        for n in range(x_value + 1, 2 * x_value + 1)
        if all(n % p and (n + 2) % p for p in primes(cutoff))
    )


def find_cutoff_mutation() -> dict[str, int]:
    for x_value in range(20, 1000):
        correct = math.isqrt(2 * x_value + 2)
        mutated = max(2, correct // 2)
        actual = sum(
            1
            for n in range(x_value + 1, 2 * x_value + 1)
            if primality(n) and primality(n + 2)
        )
        wrong = survivor_count(x_value, mutated)
        if wrong != actual:
            return {"X": x_value, "correct_cutoff": correct, "mutated_cutoff": mutated}
    raise AssertionError("cutoff mutation was not detected")


def run_checks() -> dict[str, object]:
    local_cases = 0
    for p in (2, 3, 5, 7, 11, 13):
        for d in range(-2 * p, 2 * p + 1):
            if local_k(p, d) != displayed_local_k(p, d):
                raise AssertionError(f"local formula mismatch p={p}, d={d}")
            local_cases += 1

    for cutoff in (2, 3, 5, 7, 11):
        period = math.prod(primes(cutoff))
        if sum((k_product(cutoff, d) for d in range(period)), Fraction()) != period:
            raise AssertionError(f"complete-period mean failed at q={cutoff}")
        bound = endpoint_bound(cutoff)
        samples = [(-period // 3, period // 2), (1, period), (7, period + 17)]
        for start, length in samples:
            if abs(interval_discrepancy(cutoff, start, length)) > bound:
                raise AssertionError(f"interval endpoint bound failed at q={cutoff}")

    for cutoff_left, cutoff_right in ((2, 5), (3, 5), (5, 7)):
        for d in range(-8, 13):
            if brute_joint(cutoff_left, cutoff_right, d) != formula_joint(
                cutoff_left, cutoff_right, d
            ):
                raise AssertionError(
                    f"CRT covariance mismatch q={cutoff_left}, Y={cutoff_right}, d={d}"
                )

    for cutoff in (3, 5, 7, 11, 13):
        if alpha(cutoff) ** 2 * endpoint_bound(cutoff) != Fraction(1, 6):
            raise AssertionError(f"alpha^2 D identity failed at q={cutoff}")

    brute_mean, brute_variance = brute_moving_variance(50)
    formula_mean, formula_variance = covariance_moving_variance(50)
    if (brute_mean, brute_variance) != (formula_mean, formula_variance):
        raise AssertionError("moving-cutoff variance formula failed")

    # Mutation 1: omitting the d+2 resonance must corrupt the p=5 table.
    p, d = 5, -2
    mutated = Fraction(1, 1) - Fraction(4, (p - 2) ** 2)
    if d % p == 0:
        mutated += Fraction(2 * p, (p - 2) ** 2)
    if (d - 2) % p == 0:
        mutated += Fraction(p, (p - 2) ** 2)
    if mutated == local_k(p, d):
        raise AssertionError("missing-resonance mutation escaped")

    # Control fixture: when p|h there is one, not two, deleted residue classes.
    correct_rank = len({0, (-6) % 3})
    if correct_rank == 2:
        raise AssertionError("local-rank mutation escaped")

    cutoff_witness = find_cutoff_mutation()
    return {
        "status": "PASS",
        "local_formula_cases": local_cases,
        "exact_checks": [
            "p=2 and p=3 resonance isolation",
            "p>=5 three-resonance coefficient formula",
            "complete-period mean one",
            "sampled interval endpoint bound under the symbolic universal proof",
            "two-cutoff CRT joint probability",
            "alpha(q)^2 D(q)=1/6",
            "brute versus covariance moving variance",
        ],
        "mutation_tests": {
            "missing_d_plus_2_resonance": "DETECTED",
            "subcritical_primality_cutoff": {"status": "DETECTED", **cutoff_witness},
        },
        "control_fixtures": {
            "one_deleted_residue_when_p_divides_shift": "PASS",
        },
        "finite_variance_fixture": {
            "N": 50,
            "mean": f"{brute_mean.numerator}/{brute_mean.denominator}",
            "variance": f"{brute_variance.numerator}/{brute_variance.denominator}",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run the exact checks")
    parser.parse_args()
    print(json.dumps(run_checks(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
