#!/usr/bin/env python3
"""Finite sanity check for the compact-support bump interpolation geometry."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from profile_realization import (  # noqa: E402
    aligned_mobius_profiles,
    isolated_profile_geometry,
    nonzero_mobius_divisors,
    profile_nodes,
    realize_profile,
)


def main() -> int:
    moduli = (3, 5, 7, 11, 13)
    max_error = Fraction(0, 1)
    support_rows = 0
    for q in moduli:
        divisors = nonzero_mobius_divisors(q)
        _, profiles = aligned_mobius_profiles(q, divisors)
        nodes = profile_nodes(q)
        geometry = isolated_profile_geometry(q)
        for profile in profiles:
            recovered = realize_profile(q, profile)
            max_error = max(
                max_error,
                max(
                    abs(left - right)
                    for left, right in zip(profile, recovered)
                )
                if profile
                else Fraction(0, 1),
            )
            support_rows += len(nodes)
        if geometry["strict_isolation"] is not True:
            raise AssertionError(f"support isolation failed for q={q}")
    if max_error != 0:
        raise AssertionError(f"profile interpolation error={max_error}")
    print("TPC210_PROFILE_INTERPOLATION_SANITY=PASS")
    print(f"moduli={len(moduli)}")
    print(f"support_rows={support_rows}")
    print("max_exact_profile_error=0")
    print("interpretation=finite_bump_geometry_only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
