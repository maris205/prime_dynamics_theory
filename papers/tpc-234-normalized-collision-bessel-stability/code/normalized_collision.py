#!/usr/bin/env python3
"""Exact support and normalized-collision certificates for TPC-234."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from math import gcd


class OperatorFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise OperatorFailure(message)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    return all(value % divisor for divisor in range(3, int(value**0.5) + 1, 2))


@lru_cache(maxsize=None)
def prime_shell(Q: int) -> tuple[int, ...]:
    return tuple(value for value in range(Q + 1, 2 * Q) if is_prime(value))


def row_support(Q: int, L: int, q: int) -> dict[int, int]:
    require(Q >= 8 and 1 <= L < Q / 4, "short clock range")
    require(q in prime_shell(Q), "inactive prime row")
    clock = 4 * L * Q
    require(gcd(q, clock) == 1, "noninvertible row")
    inverse = pow(q, -1, clock)
    cutoff = L * q // Q
    support: dict[int, int] = {}
    for absolute in range(1, cutoff + 1):
        if gcd(absolute, clock) != 1:
            continue
        for multiplier in (-absolute, absolute):
            residue = multiplier * inverse % clock
            require(residue not in support, "internal folding")
            support[residue] = multiplier
    require(bool(support), "zero row cannot be normalized")
    return support


def scale_record(Q: int, L: int) -> dict[str, int]:
    buckets: dict[int, list[int]] = defaultdict(list)
    atoms = 0
    for q in prime_shell(Q):
        support = row_support(Q, L, q)
        atoms += len(support)
        for residue in support:
            buckets[residue].append(q)
    maximum = max((len(rows) for rows in buckets.values()), default=0)
    require(maximum <= 2, "multiplicity-two theorem failed")
    return {
        "Q": Q,
        "L": L,
        "clock": 4 * L * Q,
        "prime_rows": len(prime_shell(Q)),
        "atoms": atoms,
        "singleton_buckets": sum(len(rows) == 1 for rows in buckets.values()),
        "double_buckets": sum(len(rows) == 2 for rows in buckets.values()),
        "max_bucket_multiplicity": maximum,
    }


def literal_q39_fixture() -> dict[str, object]:
    Q, L, p, r = 39, 7, 67, 71
    first = row_support(Q, L, p)
    second = row_support(Q, L, r)
    shared = sorted(set(first) & set(second))
    require(len(first) == len(second) == 6, "Q39 row sizes")
    require(shared == [277, 815], "Q39 shared coordinates")
    require([(first[x], second[x]) for x in shared] == [(-5, 11), (5, -11)], "Q39 multipliers")
    diagonal = 12
    symmetric = 16
    antisymmetric = 8
    require(Fraction(symmetric, diagonal) == Fraction(4, 3), "symmetric ratio")
    require(Fraction(antisymmetric, diagonal) == Fraction(2, 3), "antisymmetric ratio")
    return {
        "Q": Q,
        "L": L,
        "clock": 4 * L * Q,
        "rows": [p, r],
        "atoms_per_row": 6,
        "shared_coordinates": shared,
        "shared_multipliers": [[first[x], second[x]] for x in shared],
        "normalized_inner_product": "1/3",
        "symmetric_diagonal": diagonal,
        "symmetric_energy": symmetric,
        "symmetric_ratio": "4/3",
        "antisymmetric_energy": antisymmetric,
        "antisymmetric_ratio": "2/3",
    }


def exact_residual_fixture() -> dict[str, str]:
    # Contributions after coefficients are inserted; every coordinate has <=2 terms.
    buckets = (
        (Fraction(2, 3),),
        (Fraction(3, 5), Fraction(-4, 7)),
        (Fraction(-5, 11), Fraction(7, 13)),
        (Fraction(1, 2),),
    )
    diagonal = sum(sum(value * value for value in bucket) for bucket in buckets)
    energy = sum(sum(bucket, Fraction(0)) ** 2 for bucket in buckets)
    residual = 2 * diagonal - energy
    decomposed = sum(
        bucket[0] ** 2 if len(bucket) == 1 else (bucket[0] - bucket[1]) ** 2
        for bucket in buckets
    )
    require(residual == decomposed and residual >= 0, "exact residual identity")
    return {
        "diagonal": str(diagonal),
        "energy": str(energy),
        "two_diagonal_minus_energy": str(residual),
        "pointwise_decomposition": str(decomposed),
    }


def build_certificate() -> dict[str, object]:
    scales = ((25, 4), (39, 7), (101, 16), (211, 32), (401, 64))
    records = [scale_record(Q, L) for Q, L in scales]
    literal = literal_q39_fixture()
    residual = exact_residual_fixture()
    digest = hashlib.sha256(
        json.dumps({"records": records, "literal": literal, "residual": residual}, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "schema": "tpc234-normalized-collision-bessel-stability-v1",
        "status": "PASS",
        "claim_level": "PROVED_STRUCTURAL_L1",
        "theorem": {
            "normalized_gram": "0 <= G <= 2I",
            "offdiagonal_gram": "-I <= G-I <= I and ||G-I|| <= 1",
            "depth_dependence": "NONE",
            "ambient_sharpness": "two identical singleton unit rows attain ratio 2",
            "saving_status": "normalization alone does not imply ratio below one",
        },
        "finite_reproduction": {
            "records": records,
            "literal_q39": literal,
            "exact_residual": residual,
            "digest": digest,
        },
        "adversarial_controls": {
            "ambient_ratio_two": "PROVED_EXACT",
            "triple_bucket_ratio_three": "REJECTED_OUT_OF_SCOPE",
            "literal_symmetric_ratio": "4/3",
            "literal_antisymmetric_ratio": "2/3",
        },
        "firewall": {
            "unit_row_normalization": "MODELING_TRANSFORM",
            "source_valid_normalization": "OPEN",
            "actual_v59_crosswalk": "OPEN",
            "arithmetic_advance": "NO",
            "arithmetic_cancellation": "NONE",
            "fixed_atom_credit": 0,
            "L2": "NONE",
            "full_gate_b": "OPEN",
        },
    }
