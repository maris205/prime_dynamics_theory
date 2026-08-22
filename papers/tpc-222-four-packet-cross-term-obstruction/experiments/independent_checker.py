#!/usr/bin/env python3
"""Independent exact replay of TPC-222 Gaussian-rational packet identities."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "certificate.json"
G = tuple[Fraction, Fraction]
ZERO: G = (Fraction(0), Fraction(0))
ONE: G = (Fraction(1), Fraction(0))
I: G = (Fraction(0), Fraction(1))


def add(x: G, y: G) -> G:
    return (x[0] + y[0], x[1] + y[1])


def mul(x: G, y: G) -> G:
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def conj(x: G) -> G:
    return (x[0], -x[1])


def neg(x: G) -> G:
    return (-x[0], -x[1])


def sub(x: G, y: G) -> G:
    return add(x, neg(y))


def norm(x: G) -> Fraction:
    return x[0] * x[0] + x[1] * x[1]


def phase(r: int) -> G:
    return (ONE, I, neg(ONE), neg(I))[r % 4]


def inner(x, y):
    total = ZERO
    for a, b in zip(x, y):
        total = add(total, mul(conj(a), b))
    return total


def vadd(x, y):
    return [add(a, b) for a, b in zip(x, y)]


def vscale(c, x):
    return [mul(c, a) for a in x]


def gram(vectors):
    return [[inner(vectors[j], vectors[k]) for k in range(4)] for j in range(4)]


def energy(vectors, coefficients):
    result = [ZERO]
    for vector, coefficient in zip(vectors, coefficients):
        result = vadd(result, vscale(coefficient, vector))
    return norm(result[0])


def polarization(x, y):
    total = ZERO
    for r in range(4):
        mixed = vadd(x, vscale(phase(r), y))
        total = add(total, mul(phase(-r), (norm(mixed[0]), Fraction(0))))
    return (total[0] / 4, total[1] / 4)


def record(signs):
    vectors = [[(Fraction(sign), Fraction(0))] for sign in signs]
    matrix = gram(vectors)
    coeffs = [ONE] * 4
    diagonal = [matrix[i][i] for i in range(4)]
    trace = sum((value[0] for value in diagonal), Fraction(0))
    target = energy(vectors, coeffs)
    residuals = [
        sub(polarization(vectors[j], vectors[k]), matrix[j][k])
        for j in range(4) for k in range(4)
    ]
    return matrix, diagonal, trace, target, residuals


def text(value):
    return str(value[0]) if value[1] == 0 else f"{value[0]}+{value[1]}i"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    data = json.loads(CERTIFICATE.read_text())
    if data.get("schema") != "tpc222-four-packet-cross-term-obstruction-v1":
        raise SystemExit("schema mismatch")
    if data.get("status") != "PASS" or data.get("claim_level") != "PROVED_STRUCTURAL_L1":
        raise SystemExit("status mismatch")
    expected = {
        "plus": record((1, 1, 1, 1)),
        "minus": record((1, -1, 1, -1)),
    }
    by_name = {item["name"]: item for item in data["fixtures"]}
    for name, (matrix, diagonal, trace, target, residuals) in expected.items():
        item = by_name[name]
        if item["trace"] != str(trace) or item["target_energy"] != str(target):
            raise SystemExit("trace or energy mismatch")
        if item["diagonal"] != [text(value) for value in diagonal]:
            raise SystemExit("diagonal mismatch")
        if any(value != "0" for value in item["polarization_residuals"]):
            raise SystemExit("recorded polarization residual")
        if any(value != ZERO for value in residuals):
            raise SystemExit("polarization identity failed")
        if not item["rank_one"]:
            raise SystemExit("rank-one fixture lost")
        if trace * 4 < target:
            raise SystemExit("trace envelope failed")
    if by_name["plus"]["target_energy"] != "16" or by_name["minus"]["target_energy"] != "0":
        raise SystemExit("signed contrast missing")
    if by_name["plus"]["diagonal"] != by_name["minus"]["diagonal"]:
        raise SystemExit("same-diagonal obstruction missing")
    print("TPC222_INDEPENDENT_CHECK=PASS")
    print("fixtures=plus,minus")
    print("trace=4")
    print("signed_energy_pair=16,0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
