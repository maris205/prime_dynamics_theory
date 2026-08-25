#!/usr/bin/env python3
"""Produce the TPC-250 exact rational sharpness certificate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "TPC250_CERTIFICATE_V1"
CLAIM = "PROVED_STRUCTURAL_L1_COHERENCE_CONTROLLED_GRAM_QUADRATIC_SHARPNESS"
HANDOFF_SHA256 = "75fe9219197b41a54271df2ce4d1f15d20cd5fccd500c0a4cf4527f43c8f7357"
FIREWALL = {
    "TPC250_ACTUAL_V59_COHERENCE_ASYMPTOTIC": "OPEN",
    "TPC250_ARITHMETIC_ADVANCE": "NO",
    "TPC250_FIXED_ATOM_CREDIT": "0",
    "TPC250_L2": "NONE",
    "TPC250_FULL_GATE_B": "OPEN",
    "TPC250_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC250_TWIN_PRIME_RESULT": "NONE",
}


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def _digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical(payload)).hexdigest()


def _f(value: int | str | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def _s(value: Fraction) -> str:
    return str(value)


def _determinant(matrix: list[list[Fraction]]) -> Fraction:
    size = len(matrix)
    if size == 0:
        return Fraction(1)
    total = Fraction(0)
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            1
            for left in range(size)
            for right in range(left + 1, size)
            if permutation[left] > permutation[right]
        )
        term = Fraction(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        total += term
    return total


def _is_psd(matrix: list[list[Fraction]]) -> bool:
    size = len(matrix)
    for count in range(1, size + 1):
        for indices in itertools.combinations(range(size), count):
            principal = [[matrix[i][j] for j in indices] for i in indices]
            if _determinant(principal) < 0:
                return False
    return True


def _fixture(
    name: str,
    purpose: str,
    gram_values: list[list[int | str | Fraction]],
    weight_values: list[int | str | Fraction],
    equality: str,
    marginal_profile: str | None = None,
) -> dict[str, Any]:
    gram = [[_f(entry) for entry in row] for row in gram_values]
    weights = [_f(weight) for weight in weight_values]
    size = len(weights)
    if len(gram) != size or any(len(row) != size for row in gram):
        raise ValueError(f"{name}: matrix dimension mismatch")
    if any(gram[i][j] != gram[j][i] for i in range(size) for j in range(size)):
        raise ValueError(f"{name}: Gram matrix is not symmetric")
    if any(gram[i][i] != 1 for i in range(size)):
        raise ValueError(f"{name}: certificate fixtures must use unit vectors")
    if not _is_psd(gram):
        raise ValueError(f"{name}: Gram matrix is not positive semidefinite")

    active = [index for index, weight in enumerate(weights) if weight != 0]
    mu = Fraction(0)
    if len(active) >= 2:
        mu = max(abs(gram[i][j]) for i in active for j in active if i != j)
    diagonal = sum(weight * weight for weight in weights)
    ell_one = sum(abs(weight) for weight in weights)
    off_mass = ell_one * ell_one - diagonal
    quadratic = sum(weights[i] * gram[i][j] * weights[j] for i in range(size) for j in range(size))
    signed_lower = diagonal - mu * off_mass
    floor_lower = max(signed_lower, Fraction(0))
    upper = diagonal + mu * off_mass
    kappa = None if diagonal == 0 else ell_one * ell_one / diagonal

    if quadratic < floor_lower or quadratic > upper:
        raise ValueError(f"{name}: theorem envelope failed during production")
    if abs(quadratic - diagonal) > mu * off_mass:
        raise ValueError(f"{name}: deviation estimate failed during production")

    record: dict[str, Any] = {
        "name": name,
        "purpose": purpose,
        "gram": [[_s(entry) for entry in row] for row in gram],
        "weights": [_s(weight) for weight in weights],
        "unit_norms": True,
        "expected": {
            "active_size": len(active),
            "mu": _s(mu),
            "D": _s(diagonal),
            "L": _s(ell_one),
            "L2_minus_D": _s(off_mass),
            "quadratic": _s(quadratic),
            "signed_lower": _s(signed_lower),
            "floor_lower": _s(floor_lower),
            "upper": _s(upper),
            "kappa": None if kappa is None else _s(kappa),
        },
        "equality": equality,
    }
    if marginal_profile is not None:
        record["marginal_profile"] = marginal_profile
    return record


def build_document() -> dict[str, Any]:
    fixtures = [
        _fixture(
            "upper_equicorrelated_mu_1_over_3",
            "upper coefficient one",
            [[1, "1/3", "1/3"], ["1/3", 1, "1/3"], ["1/3", "1/3", 1]],
            [1, 1, 1],
            "quadratic=upper",
        ),
        _fixture(
            "signed_lower_mu_2_over_5",
            "signed lower coefficient one",
            [[1, "-2/5"], ["-2/5", 1]],
            [1, 1],
            "quadratic=signed_lower=floor_lower",
        ),
        _fixture(
            "floor_regular_simplex_three",
            "exact zero at the signed lower endpoint",
            [[1, "-1/2", "-1/2"], ["-1/2", 1, "-1/2"], ["-1/2", "-1/2", 1]],
            [1, 1, 1],
            "quadratic=signed_lower=floor_lower=0",
        ),
        _fixture(
            "floor_rational_collinear_negative_raw",
            "necessary nonnegative floor with negative raw lower value",
            [[1, 1, -1], [1, 1, -1], [-1, -1, 1]],
            [1, 1, 2],
            "quadratic=floor_lower=0 and signed_lower<0",
        ),
        _fixture(
            "same_marginals_aligned",
            "marginal data attain the L squared upper endpoint",
            [[1, 1], [1, 1]],
            [1, 1],
            "quadratic=L^2=4",
            "unit_pair_weights_1_1",
        ),
        _fixture(
            "same_marginals_antialigned",
            "the same marginal data permit exact cancellation",
            [[1, -1], [-1, 1]],
            [1, 1],
            "quadratic=0",
            "unit_pair_weights_1_1",
        ),
        _fixture(
            "zero_data_empty_pair",
            "D=0 has mu=0 and no kappa",
            [[1, 0], [0, 1]],
            [0, 0],
            "quadratic=D=L=0 and kappa=null",
        ),
        _fixture(
            "singleton_active_empty_pair",
            "one active index has mu=0 without an empty maximum",
            [[1, "3/5"], ["3/5", 1]],
            ["2/3", 0],
            "quadratic=D and kappa=1",
        ),
    ]
    payload = {
        "claim": CLAIM,
        "evidence_label": "EXACT_FINITE_CERTIFICATE",
        "source_lock": {
            "handoff_sha256": HANDOFF_SHA256,
            "imported_identity": "g_c=sum_b lambda_cb v_cb; ||g_c||^2=lambda_c^* G_c lambda_c",
            "actual_v59_asymptotic": "OPEN",
        },
        "definitions": {
            "mu_empty_pair_rule": "mu=0 when active_size<=1",
            "kappa_domain": "kappa=L^2/D only when D>0",
            "inner_product_orientation": "conjugate-linear first",
        },
        "firewall": FIREWALL,
        "fixtures": fixtures,
        "universal_sharpness_scope": "constants and nonnegative floor; not every arbitrary parameter tuple",
    }
    return {"schema": SCHEMA, "payload": payload, "digest": _digest(payload)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare generated certificate with the release file")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "results" / "tpc250_certificate.json")
    args = parser.parse_args()
    document = build_document()
    if args.check:
        if not args.output.is_file():
            print(f"FAIL missing certificate: {args.output}")
            return 1
        try:
            existing = json.loads(args.output.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            print(f"FAIL unreadable certificate: {error}")
            return 1
        if existing != document:
            print("FAIL release certificate differs from exact regenerated document")
            return 1
        print(f"PASS {SCHEMA} digest={document['digest']} fixtures={len(document['payload']['fixtures'])}")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE {args.output} digest={document['digest']} fixtures={len(document['payload']['fixtures'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
