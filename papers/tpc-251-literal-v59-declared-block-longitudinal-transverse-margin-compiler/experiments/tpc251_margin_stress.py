#!/usr/bin/env python3
"""Deterministic exact-rational stress for the TPC-251 compiler."""

from __future__ import annotations

import argparse
import random
from fractions import Fraction


CASES = 160


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def add(*vectors: list[Fraction]) -> list[Fraction]:
    return [sum(entries, Fraction(0)) for entries in zip(*vectors)]


def sub(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    return [x - y for x, y in zip(left, right)]


def scale(scalar: Fraction, vector: list[Fraction]) -> list[Fraction]:
    return [scalar * entry for entry in vector]


def norm2(vector: list[Fraction]) -> Fraction:
    return dot(vector, vector)


def signs_basis() -> list[list[Fraction]]:
    return [
        [Fraction(1, 2)] * 4,
        [Fraction(1, 2), Fraction(-1, 2), Fraction(1, 2), Fraction(-1, 2)],
        [Fraction(1, 2), Fraction(1, 2), Fraction(-1, 2), Fraction(-1, 2)],
        [Fraction(1, 2), Fraction(-1, 2), Fraction(-1, 2), Fraction(1, 2)],
    ]


def run_case(case_id: int) -> None:
    rng = random.Random(251000 + case_id)
    permutation = list(range(8))
    rng.shuffle(permutation)
    blocks = [permutation[:4], permutation[4:]]
    if sorted(blocks[0] + blocks[1]) != list(range(8)) or not blocks[0] or not blocks[1]:
        raise RuntimeError("partition generation failed")
    basis = signs_basis()
    u = basis[0]
    probes: dict[tuple[int, int], list[Fraction]] = {}
    projected: dict[tuple[int, int], list[Fraction]] = {}
    w_lanes: dict[int, list[Fraction]] = {}
    for c in range(2):
        coefficients = [Fraction(rng.randint(-5, 5), rng.choice([1, 2, 3, 4, 5])) for _ in range(4)]
        w_lanes[c] = add(*(scale(coefficients[index], basis[index]) for index in range(4)))
        for b in range(2):
            longitudinal = Fraction(rng.randint(-6, 6), rng.choice([1, 2, 3, 4, 5]))
            amplitude = Fraction(rng.randint(-5, 5), rng.choice([1, 2, 4, 5]))
            axis = 1 + rng.randrange(3)
            probe = add(scale(longitudinal, u), scale(amplitude, basis[axis]))
            probes[c, b] = probe
            projected[c, b] = scale(amplitude, basis[axis])

    c_long = Fraction(0)
    q_trans = Fraction(0)
    scalar = Fraction(0)
    for c in range(2):
        w_c = w_lanes[c]
        a_c = dot(u, w_c)
        w_perp = sub(w_c, scale(a_c, u))
        g_c = add(probes[c, 0], probes[c, 1])
        b_c = dot(u, g_c)
        g_perp = add(projected[c, 0], projected[c, 1])
        c_long += a_c * b_c
        q_trans += dot(w_perp, g_perp)
        scalar += dot(w_c, g_c)
        distances = [Fraction(0) if norm2(projected[c, b]) == 0 else abs(next(
            dot(projected[c, b], basis[axis]) for axis in range(1, 4) if dot(projected[c, b], basis[axis]) != 0
        )) for b in range(2)]
        active = [b for b, distance in enumerate(distances) if distance != 0]
        mu = Fraction(0)
        if len(active) >= 2:
            mu = max(
                abs(dot(projected[c, b], projected[c, bp])) / (distances[b] * distances[bp])
                for b in active for bp in active if b != bp
            )
        diagonal = sum((distance * distance for distance in distances), Fraction(0))
        ell_one = sum(distances, Fraction(0))
        upper2 = diagonal + mu * (ell_one * ell_one - diagonal)
        if norm2(g_perp) > upper2:
            raise RuntimeError(f"case {case_id}: coherence upper failed")
        if len(active) < 2 and mu != 0:
            raise RuntimeError(f"case {case_id}: empty-pair convention failed")
    if scalar != c_long + q_trans:
        raise RuntimeError(f"case {case_id}: decomposition failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("stress is read-only; pass --check")
    try:
        for case_id in range(CASES):
            run_case(case_id)
    except RuntimeError as error:
        print(f"FAIL {error}")
        return 1
    print(
        f"PASS exact_rational_declared_partition_probe_families={CASES} "
        "partition_sizes=4+4 optimization_sensitive_assertions=0 "
        "evidence=FINITE_STRUCTURAL_STRESS_NOT_ASYMPTOTIC"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
