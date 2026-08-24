#!/usr/bin/env python3
"""Independent reconstruction of TPC-233 finite mass fixtures."""

from __future__ import annotations

import hashlib
import json
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prime_small(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, int(value**0.5) + 1))


def prime_below_threshold(value: int) -> bool:
    """Independent deterministic MR basis set below 3,825,123,056,546,413,051."""

    if not 0 <= value < 3_825_123_056_546_413_051:
        raise AssertionError("independent fixture outside certified range")
    if value < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17):
        if value % prime == 0:
            return value == prime
    odd = value - 1
    power = 0
    while odd % 2 == 0:
        odd //= 2
        power += 1
    for base in (2, 3, 5, 7, 11, 13, 17, 19, 23):
        residue = pow(base, odd, value)
        if residue in (1, value - 1):
            continue
        for _ in range(power - 1):
            residue = residue * residue % value
            if residue == value - 1:
                break
        else:
            return False
    return True


def first_prime(left: int, right: int) -> int:
    candidate = left + 1
    if candidate % 2 == 0:
        candidate += 1
    while candidate < right:
        if prime_below_threshold(candidate):
            return candidate
        candidate += 2
    raise AssertionError("empty independent prime window")


def main() -> None:
    payload = json.loads((ROOT / "results" / "certificate.json").read_text(encoding="utf-8"))
    records = payload["finite_reproduction"]["records"]
    rebuilt = []
    for expected in records:
        L = expected["L"]
        Q = expected["Q"]
        low = first_prime(Q, Q + Q // (2 * L))
        high = first_prime(2 * Q - Q // (2 * L), 2 * Q)
        clock = 4 * L * Q
        low_cutoff = L * low // Q
        high_cutoff = L * high // Q
        low_positive = sum(gcd(m, clock) == 1 for m in range(1, low_cutoff + 1))
        high_positive = sum(gcd(m, clock) == 1 for m in range(1, high_cutoff + 1))
        prime_interval = sum(prime_small(m) for m in range(L + 1, 2 * L))
        rebuilt.append({
            "L": L,
            "two_power": expected["two_power"],
            "primorial": expected["primorial"],
            "Q": Q,
            "clock": clock,
            "low_prime": low,
            "high_prime": high,
            "low_cutoff": low_cutoff,
            "high_cutoff": high_cutoff,
            "low_atoms": 2 * low_positive,
            "high_atoms": 2 * high_positive,
            "row_mass_ratio": high_positive,
            "prime_interval_count": prime_interval,
            "universal_kappa_cap": 2 * L - 1,
        })
    if rebuilt != records:
        raise SystemExit("TPC233 independent reconstruction mismatch")
    digest = hashlib.sha256(
        json.dumps(rebuilt, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if digest != payload["finite_reproduction"]["records_sha256"]:
        raise SystemExit("TPC233 digest mismatch")
    print("TPC233_INDEPENDENT_CHECK=PASS")
    print(f"fixtures={len(rebuilt)}")
    print(f"largest_exact_ratio={max(row['row_mass_ratio'] for row in rebuilt)}")


if __name__ == "__main__":
    main()
