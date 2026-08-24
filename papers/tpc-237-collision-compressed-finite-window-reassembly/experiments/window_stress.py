#!/usr/bin/env python3
"""Finite-window stress test for the source-active TPC-237 fixture."""

from __future__ import annotations

import cmath
import math
from fractions import Fraction
from math import gcd


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise SystemExit("TPC237_WINDOW_STRESS=FAIL: " + message)


def row(h: int, H: int, q: int, signed: bool) -> dict[int, int]:
    inverse = pow(q, -1, h)
    cutoff = h * q // H
    output: dict[int, int] = {}
    for m in range(-cutoff, cutoff + 1):
        if m:
            a = m * inverse % h
            require(a not in output, "internal row collision")
            output[a] = (1 if m > 0 else -1) if signed else 1
    return output


def interval_energy(start: int, length: int, coefficients: dict[tuple[bool, int], Fraction], h: int) -> float:
    require(type(start) is int and type(length) is int and length >= 1, "interval parameters")
    total = 0.0
    for n in range(start, start + length):
        packet_values = {False: 0j, True: 0j}
        for (signed, a), coefficient in coefficients.items():
            phase = cmath.exp(2j * math.pi * n * a / h)
            packet_values[signed] += float(coefficient) * phase
        total += sum(abs(value) ** 2 for value in packet_values.values())
    return total


def main() -> None:
    Q, H, U, h = 101, 8830, 99, 82
    selected = (109, 137, 191)
    C_h = Fraction(1, 82)
    coefficients: dict[tuple[bool, int], Fraction] = {}
    for signed in (False, True):
        for q in selected:
            for a, amplitude in row(h, H, q, signed).items():
                require(gcd(a, h) == 1, "nonprimitive frequency")
                key = (signed, a)
                coefficients[key] = coefficients.get(key, Fraction(0, 1)) + C_h * amplitude
    coefficient_energy = sum((value * value for value in coefficients.values()), Fraction(0, 1))
    require(coefficient_energy == Fraction(5, 1681), "coefficient energy")

    cases = [(start, length) for start in (-37, 0, 41) for length in (1, 2, 17, 81, 82, 83, 164)]
    maximum_ratio = 0.0
    for start, length in cases:
        energy = interval_energy(start, length, coefficients, h)
        rhs = float((length - 1 + U * U) * coefficient_energy)
        ratio = energy / rhs
        require(math.isfinite(energy) and energy <= rhs * (1.0 + 1e-12), "large-sieve stress")
        maximum_ratio = max(maximum_ratio, ratio)
        if length % h == 0:
            require(abs(energy / length - float(coefficient_energy)) <= 1e-12,
                    "complete-period normalized energy")

    require(Fraction(4 * Q * Q, H) + Fraction(4 * U * Q, H) >= 3, "physical collision factor")
    print("TPC237_WINDOW_STRESS=PASS")
    print(f"intervals={len(cases)}")
    print(f"max_large_sieve_ratio={maximum_ratio:.12f}")
    print("full_period_normalized_energy=5/1681")


if __name__ == "__main__":
    main()
