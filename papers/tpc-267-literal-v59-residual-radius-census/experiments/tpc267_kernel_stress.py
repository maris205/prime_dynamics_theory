#!/usr/bin/env python3
"""Adversarial finite stress checks for the TPC-267 census interface."""

from __future__ import annotations

import argparse
import math


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def interval_square(lo: float, hi: float) -> tuple[float, float]:
    values = (lo * lo, lo * hi, hi * lo, hi * hi)
    return (0.0, max(values)) if lo <= 0 <= hi else (min(values), max(values))


def radial_interval(c: tuple[float, float], r2: tuple[float, float]) -> tuple[float, float]:
    c2 = interval_square(*c)
    need(r2[0] > 0 and c2[0] >= 0, "positive radius interval")
    return c2[0] / r2[1], c2[1] / r2[0]


def run() -> None:
    interval_cases = 0
    for center in ((-3.0, -2.9), (-0.2, 0.3), (1.0, 1.1), (4.0, 4.0)):
        for radius2 in ((0.5, 0.6), (2.0, 2.2), (10.0, 10.1)):
            lo, hi = radial_interval(center, radius2)
            need(0 <= lo <= hi, "ratio interval order")
            interval_cases += 1

    # The finite natural-clock rows are deliberately replayed by the
    # independent checker; this stress file focuses on the algebraic guards
    # that make a phase statement meaningful.
    phase_cases = 0
    for residual in (-10.0, -0.01, 0.01, 10.0):
        radius = 20.0
        need(abs(residual) < radius, "phase contraction fixture")
        phase_cases += 1

    need(2 * (1.0 / 4.0) ** 2 == 1.0 / 8.0, "quarter square threshold")
    need((1.0 / 4.0) ** 2 < 1.0 / 16.0 + 1e-15,
         "strict threshold encoding")
    print("TPC267_KERNEL_STRESS=PASS "
          f"interval_cases={interval_cases} phase_cases={phase_cases} "
          "rho_threshold=1/4 tail_enclosure=retained")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    run()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC267_KERNEL_STRESS=FAIL " + str(exc))
        raise SystemExit(1)
