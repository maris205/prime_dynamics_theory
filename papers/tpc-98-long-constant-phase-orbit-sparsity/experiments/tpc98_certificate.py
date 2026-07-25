#!/usr/bin/env python3
"""Exact finite checks for the TPC-98 divisibility mechanism.

This script checks only finite identities and counting assertions.  It
does not certify asymptotic divisor estimates or Mobius cancellation.
"""

from __future__ import annotations

import json
import math
from collections import Counter


PRIMES = (11, 13, 17, 19, 23, 29, 31)
SHIFTS = (-7, -3, -1, 1, 2, 5, 9)


def divisors(n: int) -> list[int]:
    n = abs(n)
    return [d for d in range(1, n + 1) if n % d == 0]


def mobius(n: int) -> int:
    if n == 1:
        return 1
    value = n
    count = 0
    p = 2
    while p * p <= value:
        if value % p == 0:
            value //= p
            count += 1
            if value % p == 0:
                return 0
            while value % p == 0:
                value //= p
        p += 1
    if value > 1:
        count += 1
    return -1 if count % 2 else 1


def content_mass(g: int, cutoff: int) -> int:
    return sum(
        abs(mobius(kappa))
        for c in divisors(g)
        if c <= cutoff
        for kappa in divisors(g // c)
    )


def run() -> dict[str, object]:
    checks: Counter[str] = Counter()
    examples = []

    for q in PRIMES:
        for h in SHIFTS:
            # The literal padding is stronger than q > 2 max(row).
            for m in range(1, (q - 1) // 2 + 1):
                if math.gcd(m, q) != 1:
                    continue
                orbit = list(range(1, q))
                roots = [j for j in orbit if (m * j + h) % q == 0]
                assert len(roots) <= 1
                checks["orbit_one_point"] += 1

                for j in orbit:
                    target = m * j + h
                    if target <= 0:
                        continue
                    for u in divisors(target):
                        sigma = target // u
                        for ell in range(1, min(m, q - 1) + 1):
                            if m % ell:
                                continue
                            for v in divisors(m // ell):
                                if v >= q:
                                    continue
                                for n in range(1, (q - 1) // 2 + 1):
                                    if n == m:
                                        continue
                                    other_target = n * j + h
                                    if other_target <= 0:
                                        continue
                                    common = math.gcd(target, other_target)
                                    for b in divisors(common):
                                        if math.gcd(b, j) != 1:
                                            continue
                                        assert (m - n) % b == 0
                                        big_b = b // math.gcd(b, sigma)
                                        assert 1 <= big_b <= b < q
                                        checks["literal_content_step"] += 1
                                        omega = ell * v * sigma * big_b
                                        assert (
                                            omega % q == 0
                                        ) == (sigma % q == 0)
                                        checks["literal_dichotomy"] += 1
                                        if omega % q == 0:
                                            assert target % q == 0
                                            assert roots == [j]
                                            checks["constant_provenance"] += 1
                                            if len(examples) < 5:
                                                examples.append(
                                                    {
                                                        "q": q,
                                                        "h": h,
                                                        "m": m,
                                                        "n": n,
                                                        "j": j,
                                                        "u": u,
                                                        "sigma": sigma,
                                                        "ell": ell,
                                                        "v": v,
                                                        "b": b,
                                                        "B": big_b,
                                                    }
                                                )

            for g in range(1, 4 * q):
                mass = content_mass(g, q)
                tau = len(divisors(g))
                assert mass <= tau * tau
                checks["content_mass"] += 1

    assert checks["constant_provenance"] > 0
    return {
        "all_checks_passed": True,
        "description": (
            "Finite exact regression for orbit sparsity, literal "
            "content-step bounds, constant-phase provenance, and "
            "exact-content absolute multiplicity; not an asymptotic theorem"
        ),
        "checks": dict(sorted(checks.items())),
        "sample_constant_keys": examples,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
