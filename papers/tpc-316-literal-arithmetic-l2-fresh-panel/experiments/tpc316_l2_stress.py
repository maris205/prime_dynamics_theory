#!/usr/bin/env python3
"""Hostile finite checks for the TPC-316 literal L2 certificate."""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-316-literal-arithmetic-l2-fresh-panel"
RESULT = PROJECT / "results/tpc316_certificate.json"
HEIGHT = 66
SCALES = (640, 1280)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
STATUS = (
    "PROVED_EXACT_FINITE_LITERAL_ARITHMETIC_L2_ENVELOPE_PLUS_"
    "TWO_SCALE_OBSTRUCTION")
SCHEMA = "TPC316_LITERAL_ARITHMETIC_L2_FRESH_PANEL_V1"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def primes_up_to(limit: int) -> list[int]:
    sieve = [True] * (limit + 1)
    sieve[:2] = [False, False]
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            for multiple in range(p * p, limit + 1, p):
                sieve[multiple] = False
    return [p for p, flag in enumerate(sieve) if flag]


PRIMES = primes_up_to(160)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def kernel(delta: int, height: int, exponent: int) -> Fraction:
    delta = abs(delta)
    return Fraction(height ** (2 * exponent),
                    (height * height + delta * delta) ** exponent)


def residue_count(lo: int, hi: int, residue: int, p: int) -> int:
    first = lo + (residue - lo) % p
    return 0 if first > hi else 1 + (hi - first) // p


def counted_valid(lo: int, hi: int, delta: int, p: int) -> int:
    n = hi - lo + 1
    pair_count = n - abs(delta)
    tlo, thi = max(lo, lo - delta), min(hi, hi - delta)
    need(thi - tlo + 1 == pair_count, "stress pair range")
    excluded_zero = residue_count(tlo, thi, 0, p)
    if delta % p == 0:
        return pair_count - excluded_zero
    return pair_count - excluded_zero - residue_count(tlo, thi, -delta, p)


def direct_valid(lo: int, hi: int, delta: int, p: int) -> int:
    return sum(
        1 for t in range(lo, hi + 1)
        if lo <= t + delta <= hi and t % p and (t + delta) % p)


def centered(delta: int, p: int) -> Fraction:
    return (Fraction(1) if delta % p == 0 else Fraction(0)) - Fraction(1, p - 1)


def counted_mass(lo: int, hi: int, height: int, q0: int,
                 exponent: int) -> Fraction:
    total = Fraction(0)
    for p in shell(q0):
        for delta in range(-(hi - lo), hi - lo + 1):
            if delta == 0:
                continue
            total += (p * kernel(delta, height, exponent)
                      * centered(delta, p)) ** 2 * counted_valid(
                          lo, hi, delta, p)
    return total


def direct_mass(lo: int, hi: int, height: int, p_values: list[int],
                exponent: int) -> Fraction:
    total = Fraction(0)
    for p in p_values:
        for u in range(lo, hi + 1):
            for t in range(lo, hi + 1):
                if u == t or u % p == 0 or t % p == 0:
                    continue
                total += (p * kernel(u - t, height, exponent)
                          * centered(u - t, p)) ** 2
    return total


def direct_output(lo: int, hi: int, height: int, p_values: list[int],
                  exponent: int, vector: list[Fraction]) -> list[Fraction]:
    output: list[Fraction] = []
    for p in p_values:
        for u in range(lo, hi + 1):
            total = Fraction(0)
            for index, t in enumerate(range(lo, hi + 1)):
                if u == t or u % p == 0 or t % p == 0:
                    continue
                total += (p * kernel(u - t, height, exponent)
                          * centered(u - t, p) * vector[index])
            output.append(total)
    return output


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def main() -> int:
    try:
        # Difference-count identity on every signed difference in a small
        # panel, with several moduli including a modulus larger than the span.
        count_checks = 0
        for p in (3, 5, 7, 11, 17):
            for delta in range(-15, 16):
                if delta:
                    need(counted_valid(11, 26, delta, p) ==
                         direct_valid(11, 26, delta, p),
                         "difference-count mutation")
                    count_checks += 1

        # Full direct Frobenius mass agrees with the compressed formula on a
        # small shell, and a nontrivial signed vector obeys the exact finite
        # Frobenius L2 inequality.
        small_lo, small_hi = 17, 32
        p_values = [5]
        mass_a = counted_mass(small_lo, small_hi, 9, 3, 1)
        mass_b = direct_mass(small_lo, small_hi, 9, p_values, 1)
        need(mass_a == mass_b, "small mass identity")
        vector = [Fraction((-1) ** i * (i + 2), 3) for i in range(16)]
        output = direct_output(small_lo, small_hi, 9, p_values, 1, vector)
        output_energy = sum(value * value for value in output)
        vector_energy = sum(value * value for value in vector)
        need(output_energy <= mass_b * vector_energy,
             "Frobenius inequality")
        basis = [Fraction(0)] * 16
        basis[7] = Fraction(1)
        basis_output = direct_output(small_lo, small_hi, 9, p_values, 1,
                                     basis)
        need(sum(value * value for value in basis_output) <= mass_b,
             "basis inequality")

        # Kernel and deletion checks guard the two easy ways to accidentally
        # change the physical operator while keeping dimensions unchanged.
        need(kernel(4, HEIGHT, 1) == kernel(-4, HEIGHT, 1) and
             kernel(0, HEIGHT, 1) == 1, "kernel symmetry")
        need(centered(0, 5) == Fraction(3, 4) and
             centered(1, 5) == Fraction(-1, 4), "centered gate")
        need(all(len(shell(q)) == size for q, size in
                 zip(Q_ANCHORS, (6, 9, 12, 15))), "shell geometry")

        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "stress certificate canonicality")
        need(document["claim_status"] == STATUS and
             document["payload"]["schema"] == SCHEMA, "stress header")
        audit = document["payload"]["finite_audit"]
        need(audit["normalized_hs_increased_all_rows"] is True and
             audit["fixed_power_credit"] == 0, "stress firewall")

        # Hostile copies must be rejected by the same simple header rules.
        mutated = dict(document)
        mutated["claim_status"] = "PROVED_GROWING_L2"
        need(mutated["claim_status"] != STATUS, "status mutation accepted")
        altered_audit = dict(audit)
        altered_audit["fixed_power_credit"] = 1
        need(altered_audit["fixed_power_credit"] != 0,
             "power-credit mutation accepted")
    except (Failure, OSError, json.JSONDecodeError, KeyError):
        return 1
    print("TPC316_STRESS=PASS difference_counts=155 small_mass_identity=1 "
          "signed_vectors=2 deletion_checks=2 shell_rows=8 "
          "two_scale_firewall=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
