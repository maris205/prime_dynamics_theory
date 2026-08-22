#!/usr/bin/env python3
from __future__ import annotations

from fractions import Fraction
import math


def residues(h):
    return tuple(a for a in range(h) if math.gcd(a, h) == 1)


def row(h, q, height=500):
    length = h * q // height
    values = {a: Fraction(0) for a in residues(h)}
    inv = pow(q, -1, h)
    for m in range(-length, length + 1):
        if m and math.gcd(m, h) == 1:
            values[(m * inv) % h] += 1
    return values


def main():
    h = 5
    q_values = (101, 151, 181, 191)
    rows = [row(h, q) for q in q_values]
    if not all(candidate == rows[0] for candidate in rows[1:]):
        raise SystemExit("alignment adversary failed")
    diagonal = sum(rows[0].values())
    coherent = sum(
        (sum(rows[i][a] for i in range(len(rows))) ** 2 for a in rows[0]),
        Fraction(0),
    )
    # Each of the two occupied residues has amplitude 4, hence energy 32.
    if coherent != 32 or diagonal * len(q_values) != 8:
        raise SystemExit("unexpected saturation values")
    ratio = Fraction(coherent, diagonal * len(q_values))
    if ratio != len(q_values):
        raise SystemExit("P saturation not reached")
    print("TPC221_SCHUR_SATURATION_ADVERSARY=PASS")
    print(f"h={h} q_count={len(q_values)} diagonal_total={diagonal * len(q_values)}")
    print(f"schur_top={2 * len(q_values)} coherent_energy={coherent} ratio={ratio}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
