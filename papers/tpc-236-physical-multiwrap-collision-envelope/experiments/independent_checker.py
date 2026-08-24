#!/usr/bin/env python3
"""Independent exact reconstruction of the TPC-236 collision envelope."""

from __future__ import annotations

import json
from fractions import Fraction
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise SystemExit("TPC236_INDEPENDENT_CHECK=FAIL: " + message)


def shell_primes(Q: int) -> list[int]:
    answer = []
    for n in range(Q + 1, 2 * Q + 1):
        prime = n >= 2 and all(n % p for p in range(2, int(n**0.5) + 1))
        if prime:
            answer.append(n)
    return answer


def ceil_div(a: int, b: int) -> int:
    return (a + b - 1) // b


def reconstruct(Q: int, H: int) -> tuple[int, int]:
    maximum = 0
    buckets_seen = 0
    for h in range(ceil_div(H, 2 * Q), Q + 1):
        buckets: dict[int, dict[int, list[int]]] = {}
        for q in shell_primes(Q):
            cutoff = h * q // H
            inverse = pow(q, -1, h)
            residues = []
            for m in range(-cutoff, cutoff + 1):
                if m:
                    a = m * inverse % h
                    residues.append(a)
                    buckets.setdefault(a, {}).setdefault(q, []).append(m)
            require(len(residues) == len(set(residues)), "internal injectivity")
        M = 2 * h * Q // H
        for a, rows in buckets.items():
            buckets_seen += 1
            g = gcd(a, h)
            exact_bound = 2 * (M // g) * ceil_div(Q, h // g)
            require(len(rows) <= exact_bound, "exact gcd-fiber envelope")
            require(Fraction(exact_bound, 1) <= Fraction(8 * Q * Q, H), "global envelope")
            maximum = max(maximum, len(rows))
    return maximum, buckets_seen


def main() -> None:
    stored = json.loads((ROOT / "results" / "certificate.json").read_text(encoding="utf-8"))
    scales = [(11, 45), (17, 70), (25, 104), (53, 220), (101, 8830), (211, 37664)]
    maxima = []
    for Q, H in scales:
        require(4 * Q < H < Q * Q, "physical regime")
        maximum, seen = reconstruct(Q, H)
        require(seen > 0, "active buckets")
        maxima.append(maximum)

    Q, H, U, h = 101, 8830, 99, 80
    require(H**32 <= Q**63 < (H + 1) ** 32, "exact H floor")
    require(U**400 <= Q**399 < (U + 1) ** 400 and h <= U, "exact U floor")
    supports = {}
    for q in (113, 127, 193):
        cutoff = h * q // H
        require(cutoff == 1, "triple cutoff")
        inverse = pow(q, -1, h)
        supports[q] = sorted({m * inverse % h for m in (-1, 1)})
    require(all(value == [17, 63] for value in supports.values()), "triple supports")
    require(stored["finite_reproduction"]["records"]["triple_collision"]["bessel_ratio"] == "3", "stored ratio")
    require(Fraction(2, 3) - Fraction(21, 32) == Fraction(1, 96), "V59 exponent")
    print("TPC236_INDEPENDENT_CHECK=PASS")
    print("maximum_multiplicities=" + ",".join(map(str, maxima)))
    print("q101_triple_ratio=3")


if __name__ == "__main__":
    main()
