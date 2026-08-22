#!/usr/bin/env python3
"""Independent exact replay of the TPC-221 Schur and saturation certificate."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "certificate.json"
Q_VALUES = (101, 103, 107, 109)
H_VALUES = (17, 19, 23)
HEIGHT = 500
SATURATION_H = 5
SATURATION_Q = (101, 151, 181, 191)


def residues(h):
    return tuple(a for a in range(h) if math.gcd(a, h) == 1)


def atoms(h, q, height=HEIGHT):
    length = h * q // height
    return tuple(m for m in range(-length, length + 1) if m and math.gcd(m, h) == 1)


def weight(profile, h, m, q, height=HEIGHT):
    if profile == "constant":
        return Fraction(1)
    if profile == "affine":
        return Fraction(1) + Fraction(height * m, h * q) / 100
    raise ValueError(profile)


def row(h, q, profile, height=HEIGHT):
    values = {a: Fraction(0) for a in residues(h)}
    inverse = pow(q, -1, h)
    for m in atoms(h, q, height):
        values[(m * inverse) % h] += weight(profile, h, m, q, height)
    return values


def direct_gram(h, q, qp, profile, height=HEIGHT):
    left = row(h, q, profile, height)
    right = row(h, qp, profile, height)
    return sum((left[a] * right[a] for a in residues(h)), Fraction(0))


def collision_gram(h, q, qp, profile, height=HEIGHT):
    total = Fraction(0)
    for m in atoms(h, q, height):
        for mp in atoms(h, qp, height):
            if (m * qp - mp * q) % h == 0:
                total += weight(profile, h, m, q, height) * weight(profile, h, mp, qp, height)
    return total


def matrix(q_values, h, profile, height=HEIGHT):
    return [[collision_gram(h, q, qp, profile, height) for qp in q_values] for q in q_values]


def energy(g, values):
    return sum((values[i] * g[i][j] * values[j]
                for i in range(len(values)) for j in range(len(values))), Fraction(0))


def row_sum(line):
    return sum((abs(value) for value in line), Fraction(0))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    data = json.loads(CERTIFICATE.read_text())
    if data.get("schema") != "tpc221-collision-graph-schur-envelope-v1":
        raise SystemExit("schema mismatch")
    if data.get("status") != "PASS" or data.get("claim_level") != "PROVED_STRUCTURAL_L1":
        raise SystemExit("status mismatch")
    records = {(item["h"], item["profile"]): item for item in data["records"]}
    for h in H_VALUES:
        for profile in ("constant", "affine"):
            item = records[(h, profile)]
            g = matrix(Q_VALUES, h, profile)
            for i, q in enumerate(Q_VALUES):
                for j, qp in enumerate(Q_VALUES):
                    if direct_gram(h, q, qp, profile) != g[i][j]:
                        raise SystemExit("Gram crosswalk mismatch")
            if any(value != "0" for value in item["gram_residuals"] + item["diagonal_residuals"]):
                raise SystemExit("recorded residual mismatch")
            rho = max((row_sum(line) for line in g), default=Fraction(0))
            if str(rho) != item["schur_radius"]:
                raise SystemExit("Schur radius mismatch")
            values = [Fraction(1), Fraction(-2), Fraction(3), Fraction(-1)]
            if rho * sum((v * v for v in values), Fraction(0)) < energy(g, values):
                raise SystemExit("Schur inequality failed")
    sat = data["saturation"]
    g = matrix(SATURATION_Q, SATURATION_H, "constant")
    rows = [row(SATURATION_H, q, "constant") for q in SATURATION_Q]
    if not all(candidate == rows[0] for candidate in rows[1:]):
        raise SystemExit("literal rows are not aligned")
    if any(value != 2 for line in g for value in line):
        raise SystemExit("saturation Gram is not 2J")
    values = [Fraction(1)] * len(SATURATION_Q)
    coherent = energy(g, values)
    diagonal_total = sum((g[i][i] for i in range(len(g))), Fraction(0))
    if coherent / diagonal_total != len(SATURATION_Q):
        raise SystemExit("saturation ratio mismatch")
    if sat["coherent_to_diagonal_ratio"] != str(len(SATURATION_Q)):
        raise SystemExit("certificate saturation mismatch")
    print("TPC221_INDEPENDENT_CHECK=PASS")
    print("generic_records=6")
    print("saturation_ratio=4")
    print("schur_status=EXACT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
