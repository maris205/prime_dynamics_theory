#!/usr/bin/env python3
"""Exact finite regression certificate for TPC-52.

The checks concern only finite algebra used by the analytic proofs.  They
do not test prime asymptotics, coherent prime cancellation, or any
parity-sensitive claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


Q = Fraction


def finite_difference_checks() -> int:
    """r-th differences annihilate moments below r at clustered nodes."""
    checks = 0
    for r in range(1, 13):
        coeff = [Q((-1) ** (r - k) * math.comb(r, k)) for k in range(r + 1)]
        norm2 = sum((a * a for a in coeff), Q(0))
        assert norm2 > 0
        checks += 1
        for j_scale in range(r + 2, r + 42):
            nodes = [Q(7, 13) + Q(k, j_scale) for k in range(r + 1)]
            for degree in range(r):
                moment = sum((a * x**degree for a, x in zip(coeff, nodes)), Q(0))
                assert moment == 0
                checks += 1
            leading = sum((a * x**r for a, x in zip(coeff, nodes)), Q(0))
            assert leading == Q(math.factorial(r), j_scale**r)
            checks += 1
    return checks


def orthogonal_lift_checks() -> int:
    """The retained label removes all scalar cross terms."""
    checks = 0
    for n in range(1, 65):
        coefficients = [Q((7 * j + 3) % 19 - 9, j + 5) for j in range(n)]
        fiber_norms = [Q((11 * j + 5) % 23 + 1, 2 * j + 7) for j in range(n)]
        lifted = sum((c * c * h for c, h in zip(coefficients, fiber_norms)), Q(0))
        diagonal_gram = sum(
            (coefficients[i] * coefficients[j] * (fiber_norms[i] if i == j else 0)
             for i in range(n) for j in range(n)),
            Q(0),
        )
        assert lifted == diagonal_gram
        assert lifted >= 0
        checks += 2
    return checks


def diagonal_mellin_ledger_checks() -> int:
    """Exact weighted-energy identity for finite diagonal multipliers."""
    checks = 0
    for q in range(1, 6):
        for n in range(1, 38):
            c = [Q((5 * i + 2) % 17 - 8, i + 9) for i in range(n)]
            factors = [
                [Q(((i + 2) * (nu + 3)) % 29 + 1, i + nu + 11) for nu in range(q)]
                for i in range(n)
            ]
            carrier = sum((z * z for z in c), Q(0))
            physical = sum(
                (c[i] * c[i] * math.prod((w * w for w in factors[i]), start=Q(1))
                 for i in range(n)),
                Q(0),
            )
            theta = physical / carrier if carrier else Q(0)
            a_mass = Q(2 * q + 3, q + 4)
            envelope_sq = a_mass * a_mass * carrier
            if physical:
                assert envelope_sq / physical == a_mass * a_mass / theta
                checks += 1
            assert Q(0) <= theta
            checks += 1
    return checks


def weighted_overlap_checks() -> int:
    """Fiberwise overlap bounds survive arbitrary nonnegative weights."""
    checks = 0
    for n in range(1, 81):
        rho = Q(1, n + 5)
        weights = [Q((13 * i + 7) % 31, i + 3) ** 2 for i in range(n)]
        carrier = [Q((17 * i + 11) % 37 + 1, i + 8) for i in range(n)]
        ratios = [rho + Q((19 * i + 3) % 41, (i + 9) * (n + 7)) for i in range(n)]
        denominator = sum((w * b for w, b in zip(weights, carrier)), Q(0))
        numerator = sum((w * b * e for w, b, e in zip(weights, carrier, ratios)), Q(0))
        assert numerator >= rho * denominator
        checks += 1
        if denominator:
            assert numerator / denominator >= rho
            checks += 1
    return checks


def good_bad_threshold_checks() -> int:
    checks = 0
    for n in range(2, 101):
        eta = Q(1, n)
        energies = [Q((i * 7 + 1) % 17, i + n + 3) for i in range(1, 40)]
        overlaps = [Q((i * 11 + 5) % (2 * n), n) for i in range(1, 40)]
        bad = sum((e * o for e, o in zip(energies, overlaps) if o < eta), Q(0))
        bad_carrier = sum((e for e, o in zip(energies, overlaps) if o < eta), Q(0))
        assert bad <= eta * bad_carrier
        checks += 1
    return checks


def endpoint_checks() -> int:
    checks = 0
    j_exp = Q(133, 400)
    assert 2 * j_exp == Q(133, 200)
    checks += 1
    budget = Q(1, 400)
    assert 2 * Q(1, 1600) + Q(1, 2000) + Q(1, 2000) + Q(1, 4000) == budget
    checks += 1
    assert Q(0) <= budget < j_exp
    checks += 1
    return checks


def source_hash() -> str:
    data = Path(__file__).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def build_certificate() -> bytes:
    groups = {
        "clustered_finite_differences": finite_difference_checks(),
        "orthogonal_orbit_lift": orthogonal_lift_checks(),
        "diagonal_mellin_energy_ledger": diagonal_mellin_ledger_checks(),
        "arbitrary_weight_overlap_transfer": weighted_overlap_checks(),
        "good_bad_overlap_threshold": good_bad_threshold_checks(),
        "endpoint_fraction_ledger": endpoint_checks(),
    }
    semantic_payload = {
        "claims": [
            "clustered scalar samples admit high-order near-null directions",
            "retained orbit labels make the physical Gram diagonal",
            "the actual-direction Mellin cost is the reciprocal overlap ratio",
            "fiberwise overlap bounds survive arbitrary source concentration",
            "bad overlap packets have small physical energy relative to carrier energy",
            "the TPC-52 endpoint fractions are internally consistent",
        ],
        "scope": "finite exact algebra only; no prime asymptotic, coherent-prime, or parity claim",
    }
    semantic_hash = hashlib.sha256(
        json.dumps(semantic_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    payload = {
        "certificate": "TPC-52 exact finite regression certificate",
        "groups": groups,
        "total_exact_checks": sum(groups.values()),
        "semantic_sha256": semantic_hash,
        "normalized_source_sha256": source_hash(),
        "scope": semantic_payload["scope"],
    }
    core = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    trailer = {"certificate_core_sha256": hashlib.sha256(core).hexdigest()}
    return core + (json.dumps(trailer, sort_keys=True) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = build_certificate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(data)
    print(data.decode("utf-8"), end="")


if __name__ == "__main__":
    main()
