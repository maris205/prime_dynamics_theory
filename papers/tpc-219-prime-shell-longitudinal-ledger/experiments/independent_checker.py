#!/usr/bin/env python3
"""Independent replay of the TPC-219 certificate without importing its producer."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "certificate.json"


def norm(vector):
    return sum((value * value for value in vector), Fraction(0))


def replay(vectors):
    p = len(vectors)
    mean = tuple(
        sum((vector[index] for vector in vectors), Fraction(0)) / p
        for index in range(len(vectors[0]))
    )
    residuals = tuple(
        tuple(vector[index] - mean[index] for index in range(len(mean)))
        for vector in vectors
    )
    diagonal = sum((norm(vector) for vector in vectors), Fraction(0))
    transverse = sum((norm(vector) for vector in residuals), Fraction(0))
    shell_vector = tuple(
        sum((vector[index] for vector in vectors), Fraction(0))
        for index in range(len(vectors[0]))
    )
    shell = norm(shell_vector)
    return {
        "P": p,
        "dimension": len(vectors[0]),
        "mean": [str(value) for value in mean],
        "diagonal": str(diagonal),
        "transverse": str(transverse),
        "shell": str(shell),
        "p_times_diagonal": str(p * diagonal),
        "p_times_transverse": str(p * transverse),
        "identity_residual": str(shell - p * (diagonal - transverse)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    observed = json.loads(CERTIFICATE.read_text())
    fixtures = {
        "aligned": tuple((Fraction(1), Fraction(2)) for _ in range(4)),
        "balanced": ((Fraction(1), Fraction(0)), (Fraction(-1), Fraction(0)),
                     (Fraction(1), Fraction(0)), (Fraction(-1), Fraction(0))),
        "orthogonal": ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)),
                        (Fraction(-1), Fraction(0)), (Fraction(0), Fraction(-1))),
        "mixed": ((Fraction(2), Fraction(1)), (Fraction(0), Fraction(-1)),
                  (Fraction(-1), Fraction(2)), (Fraction(1), Fraction(0))),
    }
    for name, vectors in fixtures.items():
        if observed["records"][name] != replay(vectors):
            raise SystemExit(f"TPC219 independent mismatch: {name}")
    checks = observed["checks"]
    if not all(type(value) is bool and value for value in checks.values()):
        raise SystemExit("TPC219 certificate check flags are not exact true booleans")
    print("TPC219_INDEPENDENT_CHECK=PASS")
    print("fixtures=4")
    print("aligned_ratio=P")
    print("balanced_shell=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
