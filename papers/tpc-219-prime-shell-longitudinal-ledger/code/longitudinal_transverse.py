#!/usr/bin/env python3
"""Exact q-space longitudinal/transverse energy ledger for TPC-219."""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable

Vector = tuple[Fraction, ...]


class LedgerFailure(RuntimeError):
    """Raised when an exact finite ledger is malformed."""


def _same_dimension(vectors: Iterable[Vector]) -> tuple[Vector, ...]:
    data = tuple(vectors)
    if not data:
        raise LedgerFailure("the q-label set must be nonempty")
    dimension = len(data[0])
    if dimension == 0 or any(len(vector) != dimension for vector in data):
        raise LedgerFailure("vectors must have one common positive dimension")
    return data


def add(left: Vector, right: Vector) -> Vector:
    if len(left) != len(right):
        raise LedgerFailure("dimension mismatch")
    return tuple(a + b for a, b in zip(left, right))


def scale(value: Fraction, vector: Vector) -> Vector:
    return tuple(value * coordinate for coordinate in vector)


def mean(vectors: Iterable[Vector]) -> Vector:
    data = _same_dimension(vectors)
    total = tuple(Fraction(0) for _ in data[0])
    for vector in data:
        total = add(total, vector)
    return scale(Fraction(1, len(data)), total)


def squared_norm(vector: Vector) -> Fraction:
    return sum((coordinate * coordinate for coordinate in vector), Fraction(0))


def ledger(vectors: Iterable[Vector]) -> dict[str, object]:
    data = _same_dimension(vectors)
    count = len(data)
    average = mean(data)
    residuals = tuple(add(vector, scale(Fraction(-1), average)) for vector in data)
    diagonal = sum((squared_norm(vector) for vector in data), Fraction(0))
    transverse = sum((squared_norm(vector) for vector in residuals), Fraction(0))
    shell_vector = tuple(
        sum((vector[index] for vector in data), Fraction(0))
        for index in range(len(data[0]))
    )
    shell = squared_norm(shell_vector)
    expected = Fraction(count) * (diagonal - transverse)
    if shell != expected:
        raise LedgerFailure("longitudinal/transverse identity failed")
    if not (Fraction(0) <= transverse <= diagonal):
        raise LedgerFailure("transverse energy is outside its Pythagorean range")
    return {
        "P": count,
        "dimension": len(data[0]),
        "mean": [str(value) for value in average],
        "diagonal": str(diagonal),
        "transverse": str(transverse),
        "shell": str(shell),
        "p_times_diagonal": str(Fraction(count) * diagonal),
        "p_times_transverse": str(Fraction(count) * transverse),
        "identity_residual": str(shell - expected),
    }


def fixtures() -> dict[str, tuple[Vector, ...]]:
    return {
        "aligned": tuple((Fraction(1), Fraction(2)) for _ in range(4)),
        "balanced": (
            (Fraction(1), Fraction(0)),
            (Fraction(-1), Fraction(0)),
            (Fraction(1), Fraction(0)),
            (Fraction(-1), Fraction(0)),
        ),
        "orthogonal": (
            (Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(1)),
            (Fraction(-1), Fraction(0)),
            (Fraction(0), Fraction(-1)),
        ),
        "mixed": (
            (Fraction(2), Fraction(1)),
            (Fraction(0), Fraction(-1)),
            (Fraction(-1), Fraction(2)),
            (Fraction(1), Fraction(0)),
        ),
    }


def build_certificate() -> dict[str, object]:
    records = {name: ledger(vectors) for name, vectors in fixtures().items()}
    aligned = records["aligned"]
    balanced = records["balanced"]
    return {
        "schema": "tpc219-longitudinal-transverse-certificate-v1",
        "status": "PASS",
        "claim_level": "PROVED_STRUCTURAL_L1",
        "records": records,
        "checks": {
            "identity_all_fixtures": all(
                record["identity_residual"] == "0" for record in records.values()
            ),
            "aligned_transverse_zero": aligned["transverse"] == "0",
            "aligned_ratio_is_P": aligned["shell"] == aligned["p_times_diagonal"],
            "balanced_shell_zero": balanced["shell"] == "0",
            "balanced_transverse_equals_diagonal": (
                balanced["transverse"] == balanced["diagonal"]
            ),
        },
        "firewall": {
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b": "OPEN",
            "strict_1_over_400": "UNPAID",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_certificate(), indent=2, sort_keys=True))
