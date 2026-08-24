#!/usr/bin/env python3
"""Boundary and hypothesis attacks for TPC-233."""

from __future__ import annotations

import sys
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from critical_row_mass import FIXTURES, fixture_record, positive_primitive_count  # noqa: E402


def main() -> None:
    removed_primes = (3, 5, 7, 11)
    for (L, exponent), removed in zip(FIXTURES, removed_primes, strict=True):
        row = fixture_record(L, exponent)
        Q = row["Q"]
        assert Q % removed == 0 and L % removed != 0
        damaged_Q = Q // removed
        damaged_clock = 4 * L * damaged_Q
        assert gcd(removed, damaged_clock) == 1
        assert positive_primitive_count(damaged_clock, L) >= 2
        assert row["low_cutoff"] == L
        assert row["high_cutoff"] == 2 * L - 1
        assert row["row_mass_ratio"] <= row["universal_kappa_cap"]
    print("TPC233_MASS_ADVERSARY=PASS")
    print("primorial_factor_removals=4")
    print("boundary_cutoffs=EXACT")


if __name__ == "__main__":
    main()
