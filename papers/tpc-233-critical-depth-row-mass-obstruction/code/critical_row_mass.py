#!/usr/bin/env python3
"""Exact finite critical-row mass certificates for TPC-233."""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from math import gcd


class MassFailure(RuntimeError):
    """Raised when a declared TPC-233 invariant fails."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise MassFailure(message)


@lru_cache(maxsize=None)
def primes_up_to(limit: int) -> tuple[int, ...]:
    require(type(limit) is int and limit >= 2, "invalid prime limit")
    out: list[int] = []
    for value in range(2, limit + 1):
        if all(value % divisor for divisor in range(2, int(value**0.5) + 1)):
            out.append(value)
    return tuple(out)


def primorial(limit: int) -> int:
    value = 1
    for prime in primes_up_to(limit):
        value *= prime
    return value


def is_prime_64(value: int) -> bool:
    """Deterministic Miller--Rabin for unsigned 64-bit integers."""

    require(type(value) is int and 0 <= value < 2**64, "primality domain")
    if value < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small:
        if value % prime == 0:
            return value == prime
    odd = value - 1
    power = 0
    while odd % 2 == 0:
        power += 1
        odd //= 2
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % value == 0:
            continue
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


def first_prime_strictly_between(left: int, right: int) -> int:
    require(type(left) is int and type(right) is int and 2 <= left < right < 2**64, "prime interval")
    candidate = left + 1
    if candidate % 2 == 0:
        candidate += 1
    while candidate < right:
        if is_prime_64(candidate):
            return candidate
        candidate += 2
    raise MassFailure("finite fixture prime window is empty")


def positive_primitive_count(clock: int, cutoff: int) -> int:
    require(type(clock) is int and clock > 0, "invalid clock")
    require(type(cutoff) is int and cutoff >= 1, "invalid cutoff")
    return sum(1 for multiplier in range(1, cutoff + 1) if gcd(multiplier, clock) == 1)


def interval_prime_count(L: int) -> int:
    return sum(1 for prime in primes_up_to(2 * L - 1) if prime > L)


FIXTURES = (
    (5, 7),
    (7, 12),
    (11, 27),
    (13, 33),
)


def fixture_record(L: int, two_power: int) -> dict[str, int]:
    require(type(L) is int and L >= 3, "invalid L")
    require(type(two_power) is int and two_power >= 0, "invalid two-adic exponent")
    P = primorial(L)
    Q = P * 2**two_power
    require(Q < 2**63, "fixture must stay in signed 64-bit range")
    low_right = Q + Q // (2 * L)
    high_left = 2 * Q - Q // (2 * L)
    low_prime = first_prime_strictly_between(Q, low_right)
    high_prime = first_prime_strictly_between(high_left, 2 * Q)
    low_cutoff = L * low_prime // Q
    high_cutoff = L * high_prime // Q
    require(low_cutoff == L, "low cutoff is not L")
    require(high_cutoff == 2 * L - 1, "high cutoff is not 2L-1")
    clock = 4 * L * Q
    low_positive = positive_primitive_count(clock, low_cutoff)
    high_positive = positive_primitive_count(clock, high_cutoff)
    interval_count = interval_prime_count(L)
    require(low_positive == 1, "primorial low row must contain only multiplier one")
    require(high_positive == 1 + interval_count, "high row exact prime-interval identity")
    require(all(Q % prime == 0 for prime in primes_up_to(L)), "Q lacks a primorial factor")
    return {
        "L": L,
        "two_power": two_power,
        "primorial": P,
        "Q": Q,
        "clock": clock,
        "low_prime": low_prime,
        "high_prime": high_prime,
        "low_cutoff": low_cutoff,
        "high_cutoff": high_cutoff,
        "low_atoms": 2 * low_positive,
        "high_atoms": 2 * high_positive,
        "row_mass_ratio": high_positive,
        "prime_interval_count": interval_count,
        "universal_kappa_cap": 2 * L - 1,
    }


def build_certificate() -> dict[str, object]:
    records = [fixture_record(L, two_power) for L, two_power in FIXTURES]
    digest = hashlib.sha256(
        json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "schema": "tpc233-critical-depth-row-mass-obstruction-v1",
        "status": "PASS",
        "claim_level": "PROVED_ARITHMETIC_OBSTRUCTION_L1",
        "theorem": {
            "critical_clock": "Q_L=2^j product_{prime ell<=L} ell with log Q_L=L log L+O(1)",
            "critical_relation": "L~log Q_L/loglog Q_L",
            "low_atoms": "2",
            "high_atoms": "2(1+pi(2L-1)-pi(L))",
            "divergence": "kappa_raw >= (1+o(1))L/log L -> infinity",
            "universal_cap": "kappa_raw <= 2L-1",
        },
        "finite_reproduction": {
            "records": records,
            "record_count": len(records),
            "records_sha256": digest,
            "interpretation": "exact finite reproduction only; shrinking-window existence is proved analytically",
        },
        "checks": {
            "primorial_saturation": True,
            "low_cutoff_exact": True,
            "high_cutoff_exact": True,
            "low_atom_identity": True,
            "high_atom_identity": True,
            "universal_comparability_cap": True,
        },
        "firewall": {
            "fixed_comparability_from_geometry": "REFUTED_SCOPED",
            "row_normalization_repair": "OPEN",
            "actual_v59_row_weights": "OPEN",
            "arithmetic_advance": "NO",
            "arithmetic_cancellation": "NONE",
            "fixed_atom_credit": 0,
            "L2": "NONE",
            "full_gate_b": "OPEN",
        },
    }
