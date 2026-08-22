#!/usr/bin/env python3
"""Boundary and adversarial checks for the TPC-225 obstruction."""

from __future__ import annotations

from fractions import Fraction
from math import gcd


def prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return n == d
        d += 1
    return True


def shell(Q: int) -> list[int]:
    return [q for q in range(Q + 1, 2 * Q + 1) if prime(q)]


def supports(Q: int) -> list[set[int]]:
    h = 4 * Q
    return [
        {pow(q, -1, h), (-pow(q, -1, h)) % h}
        for q in shell(Q)
    ]


def profile_energy(values: list[tuple[Fraction, Fraction]]) -> tuple[Fraction, Fraction]:
    diagonal = sum((u * u + v * v for u, v in values), Fraction(0))
    polarized = sum(
        (
            sum(u for u, _ in values) ** 2,
            sum(v for _, v in values) ** 2,
        ),
        Fraction(0),
    )
    return diagonal, polarized


def main() -> int:
    for Q in range(3, 100):
        qs = shell(Q)
        if not qs:
            raise SystemExit(f"empty shell at Q={Q}")
        h = 4 * Q
        for q in qs:
            if gcd(q, h) != 1 or h * q // (4 * Q * Q) != 1:
                raise SystemExit(f"clock boundary failed at Q={Q}, q={q}")
        sets = supports(Q)
        for index, left in enumerate(sets):
            for right in sets[index + 1 :]:
                if left & right:
                    raise SystemExit(f"support collision at Q={Q}")

    aligned = [(Fraction(1), Fraction(1)) for _ in range(4)]
    balanced = [
        (Fraction(1), Fraction(0)),
        (Fraction(-1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(0), Fraction(-1)),
    ]
    aligned_d, aligned_p = profile_energy(aligned)
    balanced_d, balanced_p = profile_energy(balanced)
    if aligned_d != 8 or aligned_p != 32:
        raise SystemExit("aligned profile boundary changed")
    if balanced_d != 4 or balanced_p != 0:
        raise SystemExit("balanced profile boundary changed")
    if not aligned_d > 0 or not balanced_d > 0:
        raise SystemExit("nonzero diagonal boundary lost")
    print("TPC225_BOUNDARY_ADVERSARY=PASS")
    print("Q_range=3..99")
    print("support_collisions=0")
    print("aligned_profile=E_pol_over_E_diag=4")
    print("balanced_profile=E_pol_over_E_diag=0")
    print("strict_ap_saving=REFUTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
