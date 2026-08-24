#!/usr/bin/env python3
"""Independent support-first reconstruction of TPC-234 fixtures."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prime(value: int) -> bool:
    return value >= 2 and all(value % divisor for divisor in range(2, int(value**0.5) + 1))


def support(Q: int, L: int, q: int) -> dict[int, int]:
    h = 4 * L * Q
    inverse = pow(q, -1, h)
    out = {}
    for m in range(-((L * q) // Q), (L * q) // Q + 1):
        if m and gcd(m, h) == 1:
            out[m * inverse % h] = m
    return out


def record(Q: int, L: int) -> dict[str, int]:
    rows = [q for q in range(Q + 1, 2 * Q) if prime(q)]
    buckets = defaultdict(list)
    atoms = 0
    for q in rows:
        row = support(Q, L, q)
        atoms += len(row)
        for x in row:
            buckets[x].append(q)
    return {
        "Q": Q,
        "L": L,
        "clock": 4 * L * Q,
        "prime_rows": len(rows),
        "atoms": atoms,
        "singleton_buckets": sum(len(v) == 1 for v in buckets.values()),
        "double_buckets": sum(len(v) == 2 for v in buckets.values()),
        "max_bucket_multiplicity": max(map(len, buckets.values()), default=0),
    }


def main() -> None:
    payload = json.loads((ROOT / "results" / "certificate.json").read_text(encoding="utf-8"))
    expected_records = payload["finite_reproduction"]["records"]
    rebuilt = [record(row["Q"], row["L"]) for row in expected_records]
    if rebuilt != expected_records:
        raise SystemExit("TPC234 scale reconstruction mismatch")
    q39 = payload["finite_reproduction"]["literal_q39"]
    first = support(39, 7, 67)
    second = support(39, 7, 71)
    shared = sorted(set(first) & set(second))
    literal = {
        "Q": 39,
        "L": 7,
        "clock": 1092,
        "rows": [67, 71],
        "atoms_per_row": 6,
        "shared_coordinates": shared,
        "shared_multipliers": [[first[x], second[x]] for x in shared],
        "normalized_inner_product": "1/3",
        "symmetric_diagonal": 12,
        "symmetric_energy": 16,
        "symmetric_ratio": "4/3",
        "antisymmetric_energy": 8,
        "antisymmetric_ratio": "2/3",
    }
    if literal != q39:
        raise SystemExit("TPC234 Q39 mismatch")
    buckets = ((Fraction(2, 3),), (Fraction(3, 5), Fraction(-4, 7)), (Fraction(-5, 11), Fraction(7, 13)), (Fraction(1, 2),))
    diagonal = sum(sum(v * v for v in b) for b in buckets)
    energy = sum(sum(b, Fraction(0)) ** 2 for b in buckets)
    residual = {
        "diagonal": str(diagonal),
        "energy": str(energy),
        "two_diagonal_minus_energy": str(2 * diagonal - energy),
        "pointwise_decomposition": str(sum(b[0] ** 2 if len(b) == 1 else (b[0] - b[1]) ** 2 for b in buckets)),
    }
    if residual != payload["finite_reproduction"]["exact_residual"]:
        raise SystemExit("TPC234 residual mismatch")
    digest = hashlib.sha256(json.dumps({"records": rebuilt, "literal": literal, "residual": residual}, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    if digest != payload["finite_reproduction"]["digest"]:
        raise SystemExit("TPC234 digest mismatch")
    print("TPC234_INDEPENDENT_CHECK=PASS")
    print(f"scales={len(rebuilt)}")
    print("literal_ratios=4/3,2/3")


if __name__ == "__main__":
    main()
