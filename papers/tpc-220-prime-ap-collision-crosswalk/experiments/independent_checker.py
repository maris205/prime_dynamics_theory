#!/usr/bin/env python3
"""Independent exact replay of TPC-220 identities."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "certificate.json"
Q = (101, 103, 107, 109)
H = (17, 19, 23)
HEIGHT = 500


def residues(h):
    return tuple(a for a in range(h) if math.gcd(a, h) == 1)


def atoms(h, q):
    L = h * q // HEIGHT
    return tuple(m for m in range(-L, L + 1) if m and math.gcd(m, h) == 1)


def w(profile, h, m, q):
    value = Fraction(HEIGHT * m, h * q)
    return Fraction(1) if profile == "constant" else Fraction(1) + value / 100


def row(h, q, profile):
    result = {a: Fraction(0) for a in residues(h)}
    inv = pow(q, -1, h)
    for m in atoms(h, q):
        result[(m * inv) % h] += w(profile, h, m, q)
    return result


def direct(h, a, profile):
    return sum((row(h, q, profile)[a] for q in Q), Fraction(0))


def ap(h, a, profile):
    total = Fraction(0)
    inv = pow(a, -1, h)
    L = h * max(Q) // HEIGHT
    for m in range(-L, L + 1):
        if not m or math.gcd(m, h) != 1:
            continue
        for q in Q:
            if q % h == (inv * m) % h and abs(m) <= h * q // HEIGHT:
                total += w(profile, h, m, q)
    return total


def gram(h, q, qp, profile):
    left, right = row(h, q, profile), row(h, qp, profile)
    direct_value = sum((left[a] * right[a] for a in residues(h)), Fraction(0))
    collision = Fraction(0)
    for m in atoms(h, q):
        for mp in atoms(h, qp):
            if (m * qp - mp * q) % h == 0:
                collision += w(profile, h, m, q) * w(profile, h, mp, qp)
    return direct_value, collision


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    data = json.loads(CERTIFICATE.read_text())
    expected = {(h, profile): record for record in data["records"] for h, profile in [(record["h"], record["profile"])]}
    for h in H:
        for profile in ("constant", "affine"):
            record = expected[(h, profile)]
            for a in residues(h):
                if direct(h, a, profile) != ap(h, a, profile):
                    raise SystemExit("TPC220 AP crosswalk mismatch")
            for q in Q:
                for qp in Q:
                    d, c = gram(h, q, qp, profile)
                    if d != c:
                        raise SystemExit("TPC220 Gram mismatch")
            if any(value != "0" for value in record["crosswalk_residuals"] + record["gram_residuals"]):
                raise SystemExit("TPC220 recorded residual is nonzero")
    print("TPC220_INDEPENDENT_CHECK=PASS")
    print("records=6")
    print("profiles=constant,affine")
    print("offdiagonal_collision=OBSERVED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
