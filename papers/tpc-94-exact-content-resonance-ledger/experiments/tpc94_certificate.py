#!/usr/bin/env python3
"""Deterministic finite regression certificate for TPC-94.

The checks below exercise exact integer identities only.  They are not
asymptotic evidence and do not independently re-run the upstream TPC-93
source--child inverse and multiplicity certificate imported by this paper.
"""

from __future__ import annotations

import json
from math import gcd


def mobius(n: int) -> int:
    if n <= 0:
        raise ValueError("mobius is used only on positive integers")
    value = n
    sign = 1
    prime = 2
    while prime * prime <= value:
        if value % prime == 0:
            value //= prime
            sign = -sign
            if value % prime == 0:
                return 0
            while value % prime == 0:
                value //= prime
        prime += 1
    if value > 1:
        sign = -sign
    return sign


def signed_lift(residue: int, prime: int) -> int:
    if prime <= 2 or prime % 2 == 0:
        raise ValueError("the certificate uses an odd prime modulus")
    lift = residue % prime
    if lift > prime // 2:
        lift -= prime
    return lift


def resolved_length(left: int, right: int, tau: int, step: int) -> int:
    return sum(1 for t in range(left, right + 1) if (t - tau) % step == 0)


def floor_div(numerator: int, denominator: int) -> int:
    return numerator // denominator


def ceil_div(numerator: int, denominator: int) -> int:
    return -((-numerator) // denominator)


def formula_length(left: int, right: int, tau: int, step: int) -> int:
    return max(
        0,
        floor_div(right - tau, step)
        - ceil_div(left - tau, step)
        + 1,
    )


def sector(
    *,
    structurally_null: bool,
    occupancy: int,
    conductor: int,
    short_threshold: int,
    conductor_threshold: int,
    resonant: bool,
) -> str:
    if structurally_null:
        return "null"
    if occupancy <= short_threshold:
        return "short"
    if conductor == 1:
        return "constant"
    if 2 <= conductor <= conductor_threshold:
        return "low_resonant" if resonant else "low_generic"
    return "high_resonant" if resonant else "high_generic"


def check_normalization_and_mobius() -> int:
    checks = 0
    for sigma in range(1, 10):
        for slope in range(1, 10):
            if gcd(sigma, slope) != 1:
                continue
            for d in range(1, 11):
                if gcd(d, sigma) != 1:
                    continue
                for u in range(1, 11):
                    if gcd(u, slope) != 1:
                        continue
                    h0 = sigma * u - slope * d
                    if h0 == 0:
                        continue
                    for b in range(1, 21):
                        step = b // gcd(b, sigma)
                        soluble = gcd(slope, step) == 1
                        solutions = [
                            t
                            for t in range(step)
                            if (u + slope * t) % step == 0
                        ]
                        assert len(solutions) == (1 if soluble else 0)
                        if not soluble:
                            continue
                        tau = solutions[0]
                        d0 = d + sigma * tau
                        v0 = (u + slope * tau) // step
                        content = gcd(d0, sigma * step)
                        assert content == gcd(step, abs(h0))
                        assert (sigma * step) * v0 - slope * d0 == h0
                        assert gcd(d0 // content, (sigma * step) // content) == 1
                        assert gcd(v0, slope) == 1
                        for z in range(5):
                            first = d0 + sigma * step * z
                            second_reduced = v0 + slope * z
                            second_raw = step * second_reduced
                            lhs = mobius(first) * mobius(second_raw)
                            rhs = (
                                mobius(content)
                                * mobius(step)
                                * mobius(first // content)
                                * mobius(second_reduced)
                                * int(gcd(content, first // content) == 1)
                                * int(gcd(step, second_reduced) == 1)
                            )
                            assert lhs == rhs
                            checks += 1
    return checks


def check_orientation() -> int:
    checks = 0
    for prime in (5, 7, 11):
        for c in range(1, prime):
            modulus = c * prime
            for residue in range(1, prime):
                lift = signed_lift(residue, prime)
                for epsilon in (-1, 1):
                    for moving_origin in range(-5, 6):
                        for opposite_row in range(-3, 4):
                            for omega in range(-8, 9):
                                for z in range(-2, 3):
                                    whole = (
                                        -epsilon
                                        * lift
                                        * (moving_origin + omega * z - opposite_row)
                                    ) % modulus
                                    split = (
                                        -epsilon
                                        * lift
                                        * (moving_origin - opposite_row)
                                        - epsilon * lift * omega * z
                                    ) % modulus
                                    assert whole == split
                                    checks += 1
    return checks


def check_signed_lift_and_conductor() -> tuple[int, dict[str, int]]:
    checks = 0
    for prime in (3, 5, 7, 11, 13):
        for residue in range(1, prime):
            lift = signed_lift(residue, prime)
            assert lift % prime == residue
            assert 0 < abs(lift) < prime / 2
            for c in range(1, prime):
                for omega in range(1, 3 * c * prime + 1):
                    conductor = c * prime // gcd(c * prime, lift * omega)
                    if omega % prime == 0:
                        assert conductor <= c
                    else:
                        assert conductor >= prime
                    if omega % c == 0:
                        literal_omega = omega // c
                        expected = 1 if literal_omega % prime == 0 else prime
                        assert conductor == expected
                        shifted = c * prime // gcd(
                            c * prime, (lift + prime) * omega
                        )
                        assert shifted == conductor
                    checks += 1

    ambiguity = {
        "prime": 3,
        "content": 2,
        "omega": 1,
        "representative_0_to_q_minus_1": 2,
        "signed_representative": -1,
    }
    q = ambiguity["prime"]
    c = ambiguity["content"]
    omega = ambiguity["omega"]
    ambiguity["conductor_0_to_q_minus_1"] = c * q // gcd(c * q, 2 * omega)
    ambiguity["conductor_signed"] = c * q // gcd(c * q, -omega)
    assert ambiguity["conductor_0_to_q_minus_1"] != ambiguity["conductor_signed"]
    return checks, ambiguity


def check_progression_and_partition_boundaries() -> tuple[int, int]:
    length_checks = 0
    for left in range(-4, 5):
        for native_length in range(1, 21):
            right = left + native_length - 1
            for step in range(1, 16):
                for tau in range(step):
                    actual = resolved_length(left, right, tau, step)
                    formula = formula_length(left, right, tau, step)
                    assert actual == formula
                    assert actual <= (native_length + step - 1) // step
                    for integer_threshold in range(1, 11):
                        if step * integer_threshold >= native_length:
                            assert actual <= integer_threshold
                    length_checks += 1

    partition_checks = 0
    labels = {
        "null",
        "short",
        "constant",
        "low_resonant",
        "low_generic",
        "high_resonant",
        "high_generic",
    }
    for structurally_null in (False, True):
        for occupancy in (0, 1, 3, 4, 8):
            for conductor in (1, 2, 5, 6, 11):
                for resonant in (False, True):
                    label = sector(
                        structurally_null=structurally_null,
                        occupancy=occupancy,
                        conductor=conductor,
                        short_threshold=3,
                        conductor_threshold=5,
                        resonant=resonant,
                    )
                    assert label in labels
                    if structurally_null:
                        assert label == "null"
                    elif occupancy <= 3:
                        assert label == "short"
                    elif conductor == 1:
                        assert label == "constant"
                    elif conductor <= 5:
                        assert label.startswith("low_")
                    else:
                        assert label.startswith("high_")
                    partition_checks += 1

    # The outer content-inversion coefficient is structurally null here
    # even though B can be squarefree.
    assert mobius(4) == 0
    assert gcd(4, 4) == 4
    assert 4 // gcd(4, 4) == 1

    return length_checks, partition_checks


def main() -> None:
    normalization_checks = check_normalization_and_mobius()
    orientation_checks = check_orientation()
    conductor_checks, ambiguity = check_signed_lift_and_conductor()
    length_checks, partition_checks = check_progression_and_partition_boundaries()
    result = {
        "schema": "tpc94-certificate-v1",
        "checks": {
            "normalization_and_mobius": normalization_checks,
            "orientation": orientation_checks,
            "signed_lift_and_conductor": conductor_checks,
            "progression_length": length_checks,
            "partition_boundaries": partition_checks,
            "total": (
                normalization_checks
                + orientation_checks
                + conductor_checks
                + length_checks
                + partition_checks
            ),
        },
        "abstract_lift_ambiguity_witness": ambiguity,
        "scope": {
            "exact_integer_regression_only": True,
            "asymptotic_cancellation_tested": False,
            "tpc93_lossless_provenance_recertified_by_this_script": False,
            "l2_or_prime_pair_claim": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
