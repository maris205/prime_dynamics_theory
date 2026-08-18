#!/usr/bin/env python3
"""Numerical sanity checks for the continuous Poisson reindexing formula.

This is deliberately not used as theorem evidence.  It checks three rapidly
decaying Gaussian examples with independently written direct and dual sums.
"""

from __future__ import annotations

import cmath
import math


CASES = (
    (5, 2, 1, 1.7, 0.13),
    (7, 3, 2, 1.35, -0.21),
    (11, 4, 5, 2.1, 0.07),
)


def error(q: int, divisor: int, frequency: int, scale: float, modulation: float) -> float:
    def function(x: float) -> complex:
        return cmath.exp(-math.pi * (x / scale) ** 2 + 2j * math.pi * modulation * x)

    def transform(xi: float) -> complex:
        return scale * cmath.exp(-math.pi * scale**2 * (xi - modulation) ** 2)

    direct = sum(
        function(m) * cmath.exp(-2j * math.pi * frequency * divisor * m / q)
        for m in range(-40, 41)
    )
    dual = sum(
        transform(r + frequency * divisor / q) for r in range(-40, 41)
    )
    return abs(direct - dual)


def main() -> int:
    errors = [error(*case) for case in CASES]
    maximum = max(errors)
    print("TPC209_GAUSSIAN_POISSON_SANITY=PASS" if maximum < 1e-12 else "TPC209_GAUSSIAN_POISSON_SANITY=FAIL")
    print(f"cases={len(CASES)}")
    print(f"max_error={maximum:.3e}")
    return 0 if maximum < 1e-12 else 1


if __name__ == "__main__":
    raise SystemExit(main())
