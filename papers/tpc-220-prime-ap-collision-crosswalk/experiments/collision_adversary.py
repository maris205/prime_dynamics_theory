#!/usr/bin/env python3
"""Show an exact off-diagonal collision in the TPC-220 incidence graph."""

from fractions import Fraction
import math


def main() -> int:
    h = 17
    q, qp = 101, 103
    L, Lp = h * q // 500, h * qp // 500
    collisions = []
    for m in range(-L, L + 1):
        if not m or math.gcd(m, h) != 1:
            continue
        for mp in range(-Lp, Lp + 1):
            if not mp or math.gcd(mp, h) != 1:
                continue
            if (m * qp - mp * q) % h == 0:
                collisions.append((m, mp))
    if not collisions:
        raise SystemExit("expected off-diagonal collision is absent")
    print("TPC220_COLLISION_ADVERSARY=PASS")
    print(f"h={h} q={q} qp={qp} collision_count={len(collisions)}")
    print(f"first_collision={collisions[0]}")
    print(f"exact_weight={Fraction(1)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
