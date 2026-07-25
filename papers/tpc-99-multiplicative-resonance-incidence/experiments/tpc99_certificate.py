#!/usr/bin/env python3
"""Finite regression for the TPC-99 resonance incidence operator."""

from __future__ import annotations

import cmath
import json
import math
from collections import Counter


PRIMES = (7, 11, 13, 17, 19, 23, 29, 31)
TOL = 2e-8


def factors(n: int) -> list[int]:
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def primitive_root(q: int) -> int:
    for g in range(2, q):
        if all(pow(g, (q - 1) // p, q) != 1 for p in factors(q - 1)):
            return g
    raise AssertionError("no primitive root")


def signed(x: int, q: int) -> int:
    x %= q
    return x if x <= q // 2 else x - q


def run() -> dict[str, object]:
    counts: Counter[str] = Counter()
    max_fourier_error = 0.0

    for q in PRIMES:
        n = q - 1
        g = primitive_root(q)
        powers = [pow(g, j, q) for j in range(n)]
        logs = {x: j for j, x in enumerate(powers)}

        for h in range(1, n // 2 + 1):
            e_set = {x for x in range(1, q) if abs(signed(x, q)) <= h}
            assert len(e_set) == 2 * h

            for r in range(1, q):
                degree = sum(1 for w in range(1, q) if (r * w) % q in e_set)
                assert degree == 2 * h
                counts["biregular_degrees"] += 1

            for length in range(1, q + 1):
                width = min(n // 2, q // length)
                for x in range(1, q):
                    lhs = length * abs(signed(x, q)) <= q
                    rhs = abs(signed(x, q)) <= width
                    assert lhs == rhs
                    counts["resonance_equivalence"] += 1

            eigenvalues = []
            for k in range(n):
                chi_minus_one = cmath.exp(
                    2j * math.pi * k * logs[q - 1] / n
                )
                direct = sum(
                    cmath.exp(-2j * math.pi * k * logs[x] / n)
                    for x in e_set
                )
                half = sum(
                    cmath.exp(-2j * math.pi * k * logs[x] / n)
                    for x in range(1, h + 1)
                )
                factored = (1 + chi_minus_one.conjugate()) * half
                max_fourier_error = max(
                    max_fourier_error, abs(direct - factored)
                )
                assert abs(direct - factored) < TOL
                if abs(chi_minus_one + 1) < TOL:
                    assert abs(direct) < TOL
                    counts["odd_null_modes"] += 1
                eigenvalues.append(direct)

            assert abs(eigenvalues[0] - 2 * h) < TOL
            hs_nonprincipal = sum(abs(z) ** 2 for z in eigenvalues[1:])
            assert abs(hs_nonprincipal - 2 * h * (n - 2 * h)) < TOL
            counts["hilbert_schmidt"] += 1

            a = {
                x: complex((3 * x + h) % 7 - 3, (x * x + q) % 5 - 2)
                for x in range(1, q)
            }
            b = {
                x: complex((2 * x + q) % 5 - 2, (x + h) % 3 - 1)
                for x in range(1, q)
            }
            direct_form = sum(
                a[w] * b[r]
                for w in range(1, q)
                for r in range(1, q)
                if (r * w) % q in e_set
            )
            spectral = 0j
            for k, ehat in enumerate(eigenvalues):
                asum = sum(
                    a[x] * cmath.exp(2j * math.pi * k * logs[x] / n)
                    for x in range(1, q)
                )
                bsum = sum(
                    b[x] * cmath.exp(2j * math.pi * k * logs[x] / n)
                    for x in range(1, q)
                )
                spectral += ehat * asum * bsum / n
            assert abs(direct_form - spectral) < 2e-7
            counts["bilinear_fourier_identity"] += 1

            delta_value = sum(
                1 for r in range(1, min(h, 4) + 1)
                if r in e_set
            )
            assert delta_value == min(h, 4)
            counts["delta_obstruction"] += 1

    return {
        "all_checks_passed": True,
        "description": (
            "Finite resonance-window, biregularity, multiplicative "
            "spectrum, parity-nullspace, Hilbert-Schmidt, and bilinear "
            "regression; not an asymptotic theorem"
        ),
        "counts": dict(sorted(counts.items())),
        "maximum_fourier_roundoff": max_fourier_error,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
