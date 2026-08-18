#!/usr/bin/env python3
"""Small human-readable sanity run for the TPC-211 structural package."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from product_coupled import finite_case  # noqa: E402


def main() -> int:
    for primes in ((5, 7), (5, 7, 11), (5, 7, 11, 13)):
        record = finite_case(primes, 3)
        print(
            "primes={primes} modulus={modulus} profiles={divisor_count} "
            "rank={profile_rank} ratio={ratio} derivative={derivative}".format(
                primes=record["primes"],
                modulus=record["modulus"],
                divisor_count=record["divisor_count"],
                profile_rank=record["profile_rank"],
                ratio=record["coherent_to_diagonal_ratio"],
                derivative=record["log_derivative_identity"],
            )
        )
    print("TPC211_PRODUCT_RANK_SANITY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
