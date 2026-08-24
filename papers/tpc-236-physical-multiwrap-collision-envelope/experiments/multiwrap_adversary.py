#!/usr/bin/env python3
"""Adversarial controls for physical multiplicity and gcd reduction."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from physical_multiwrap import gcd_adversary_fixture, triple_collision_fixture  # noqa: E402


def main() -> None:
    triple = triple_collision_fixture()
    gcd_case = gcd_adversary_fixture()
    if triple["bessel_ratio"] != "3":
        raise SystemExit("TPC236_MULTIWRAP_ADVERSARY=FAIL: multiplicity-two survived")
    if not gcd_case["naive_modulus_h_bound"] < gcd_case["actual_multiplicity"] <= gcd_case["gcd_reduced_bound"]:
        raise SystemExit("TPC236_MULTIWRAP_ADVERSARY=FAIL: gcd reduction not separated")
    print("TPC236_MULTIWRAP_ADVERSARY=PASS")
    print("physical_multiplicity_two=REFUTED_BY_RATIO_3")
    print("gcd_reduced_modulus=REQUIRED")


if __name__ == "__main__":
    main()
