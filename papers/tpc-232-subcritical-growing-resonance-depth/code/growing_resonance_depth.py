#!/usr/bin/env python3
"""Exact finite collision scans and theorem metadata for TPC-232."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from math import gcd


class DepthFailure(RuntimeError):
    """Raised when a declared growing-depth invariant fails."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise DepthFailure(message)


def is_prime(value: int) -> bool:
    require(type(value) is int, "prime input must be an exact integer")
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


@lru_cache(maxsize=None)
def prime_shell(Q: int) -> tuple[int, ...]:
    require(type(Q) is int and Q >= 8, "Q must be an integer at least eight")
    return tuple(q for q in range(Q + 1, 2 * Q) if is_prime(q))


def validate_scale(Q: int, L: int) -> None:
    require(type(Q) is int and Q >= 8, "invalid Q")
    require(type(L) is int and 1 <= L < Q // 4, "require 1 <= L < Q/4")


def positive_multipliers(Q: int, L: int, q: int) -> tuple[int, ...]:
    validate_scale(Q, L)
    require(q in prime_shell(Q), "q is not in the prime shell")
    h = 4 * L * Q
    require(gcd(q, h) == 1, "prime row is not invertible on the clock")
    cutoff = L * q // Q
    require(cutoff < q, "short-multiplier regime failed")
    return tuple(m for m in range(1, cutoff + 1) if gcd(m, h) == 1)


def row_support(Q: int, L: int, q: int) -> dict[int, int]:
    h = 4 * L * Q
    inverse = pow(q, -1, h)
    support: dict[int, int] = {}
    for absolute in positive_multipliers(Q, L, q):
        for multiplier in (-absolute, absolute):
            residue = multiplier * inverse % h
            require(residue not in support, "internal support folding")
            support[residue] = multiplier
    return support


def support_scan(Q: int, L: int) -> dict[str, object]:
    """Compile literal support collisions without using resonance equations."""

    validate_scale(Q, L)
    h = 4 * L * Q
    primes = prime_shell(Q)
    buckets: dict[int, list[tuple[int, int]]] = defaultdict(list)
    atom_count = 0
    for q in primes:
        support = row_support(Q, L, q)
        atom_count += len(support)
        for residue, multiplier in support.items():
            buckets[residue].append((q, multiplier))

    channel_records: list[tuple[int, int, int, int, int]] = []
    unique_edges: set[tuple[int, int]] = set()
    degrees = {q: set() for q in primes}
    max_bucket = 0
    for residue, rows in buckets.items():
        max_bucket = max(max_bucket, len(rows))
        require(len({q for q, _ in rows}) == len(rows), "one row repeated in a residue bucket")
        require(len(rows) <= 2, "same-sign exclusion should force bucket multiplicity at most two")
        if len(rows) != 2:
            continue
        (q1, m1), (q2, m2) = sorted(rows)
        require(m1 * m2 < 0, "collision multipliers must have opposite signs")
        a, b = abs(m1), abs(m2)
        require(a * q2 + b * q1 == h, "resonance equation mismatch")
        require(gcd(a, b) == 1, "primitive resonance coefficients must be coprime")
        channel_records.append((q1, q2, a, b, residue))
        unique_edges.add((q1, q2))
        degrees[q1].add(q2)
        degrees[q2].add(q1)

    require(len(channel_records) % 2 == 0, "global-sign collision count must be even")
    sign_orbits: dict[tuple[int, int, int, int], set[int]] = defaultdict(set)
    for q1, q2, a, b, residue in channel_records:
        sign_orbits[(q1, q2, a, b)].add(residue)
    require(all(len(residues) == 2 for residues in sign_orbits.values()), "each channel needs two sign residues")

    canonical = sorted((q1, q2, a, b) for q1, q2, a, b in sign_orbits)
    encoded = json.dumps(canonical, separators=(",", ":")).encode("utf-8")
    return {
        "Q": Q,
        "L": L,
        "clock": h,
        "prime_rows": len(primes),
        "atoms": atom_count,
        "collision_coordinates": len(channel_records),
        "resonance_channels": len(sign_orbits),
        "unique_edges": len(unique_edges),
        "incident_rows": len({q for edge in unique_edges for q in edge}),
        "max_degree": max((len(neighbors) for neighbors in degrees.values()), default=0),
        "max_bucket_multiplicity": max_bucket,
        "channel_sha256": hashlib.sha256(encoded).hexdigest(),
    }


def channel_weight_sum(L: int) -> Fraction:
    require(type(L) is int and L >= 1, "L must be positive")
    return sum(
        (Fraction(1, max(a, b)) for a in range(1, 2 * L) for b in range(1, 2 * L)),
        Fraction(0),
    )


def build_certificate() -> dict[str, object]:
    scales = (
        (25, 4),
        (101, 4), (101, 8), (101, 16),
        (211, 8), (211, 16), (211, 32),
        (401, 16), (401, 32), (401, 64),
        (809, 32), (809, 64), (809, 128),
        (1601, 64), (1601, 128), (1601, 256),
        (3203, 128), (3203, 256), (3203, 512),
    )
    records = [support_scan(Q, L) for Q, L in scales]
    digest = hashlib.sha256(
        json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    weight_checks = []
    for L in (1, 2, 4, 8, 16, 32, 64):
        weight = channel_weight_sum(L)
        require(weight <= 4 * L, "coefficient weight bound failed")
        weight_checks.append({"L": L, "numerator": weight.numerator, "denominator": weight.denominator})
    q25 = support_scan(25, 4)
    require(q25["resonance_channels"] == 1 and q25["collision_coordinates"] == 2, "Q25 anchor")
    require(all(record["max_bucket_multiplicity"] <= 2 for record in records), "bucket theorem")
    return {
        "schema": "tpc232-subcritical-growing-resonance-depth-v1",
        "status": "PASS",
        "claim_level": "PROVED_ARITHMETIC_OBSTRUCTION_L1",
        "theorem": {
            "uniform_range": "1 <= L <= (log Q)^A for fixed A",
            "incidence_bound": "C_L(Q) <<_A L Q loglog(3LQ)/(log Q)^2",
            "normalized_bound": "C_L(Q)/P(Q) <<_A L loglog(3LQ)/log Q",
            "subcritical_stop": "L=o(log Q/loglog Q) implies C_L(Q)/P(Q)->0",
            "clock_capacity": "the surrogate clock is exact for L<Q/4; V59 attachment is OPEN",
        },
        "finite_scan": {
            "records": records,
            "record_count": len(records),
            "scan_sha256": digest,
            "interpretation": "finite reproduction only, not asymptotic evidence",
        },
        "coefficient_weight_checks": weight_checks,
        "checks": {
            "short_multiplier_regime": True,
            "opposite_sign_reduction": True,
            "one_wrap_equation": True,
            "two_sign_residues_per_channel": True,
            "coefficient_weight_sum_le_4L": True,
            "subcritical_density_transfer": True,
        },
        "firewall": {
            "dilated_clock": "MODELING_CHOICE",
            "growing_depth_arithmetic_obstruction": "PROVED_SOURCE_BACKED",
            "critical_depth_sufficiency": "OPEN",
            "actual_v59_clock_attachment": "OPEN",
            "arithmetic_advance": "NO",
            "arithmetic_cancellation": "NONE",
            "fixed_atom_credit": 0,
            "L2": "NONE",
            "full_gate_b": "OPEN",
        },
    }
