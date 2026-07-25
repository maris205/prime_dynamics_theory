#!/usr/bin/env python3
"""Deterministic exact checks for TPC-111 Abel duality."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


def prefixes(values: tuple[int, ...]) -> list[Fraction]:
    out: list[Fraction] = []
    total = Fraction(0)
    for value in values:
        total += value
        out.append(total)
    return out


def certificate() -> dict:
    checks = 0
    sequences = 0
    for n in range(1, 7):
        for sigma in itertools.product((-1, 0, 1), repeat=n):
            sequences += 1
            w = [Fraction((i + 2) * (-1) ** i, n + 3) for i in range(n)]
            s = prefixes(sigma)
            direct = sum(Fraction(sigma[i]) * w[i] for i in range(n))
            abel = s[-1] * w[-1]
            abel += sum(s[k] * (w[k] - w[k + 1]) for k in range(n - 1))
            assert direct == abel
            checks += 1

            k_star = max(range(n), key=lambda k: abs(s[k]))
            d = [Fraction(0) for _ in range(n)]
            d[k_star] = Fraction(1 if s[k_star] >= 0 else -1)
            dual_value = abs(sum(s[k] * d[k] for k in range(n)))
            assert dual_value == max(abs(value) for value in s)
            checks += 1
            assert sum(abs(value) for value in d) == 1
            checks += 1

    atoms = [Fraction(3), Fraction(-2), Fraction(5), Fraction(-7), Fraction(11)]
    partitions = [
        [[0, 1, 2, 3, 4]],
        [[0, 1], [2, 3, 4]],
        [[0], [1], [2], [3], [4]],
    ]
    total = sum(atoms)
    for partition in partitions:
        coarsened = sum(sum(atoms[i] for i in block) for block in partition)
        assert coarsened == total
        checks += 1

    return {
        "schema": "tpc111-zero-mode-prefix-audit-v1",
        "status": "PASS",
        "sign_sequences_tested": sequences,
        "partitions_tested": len(partitions),
        "assertions_checked": checks,
        "claim_boundary": {
            "coarsening_invariance": True,
            "sharp_prefix_duality": True,
            "literal_growing_prefix_bound": False,
            "positive_eta_Z": False,
            "fixed_h0_L2_progress": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = certificate()
    target = Path(__file__).with_suffix(".json")
    if args.write:
        target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.check:
        expected = json.loads(target.read_text(encoding="utf-8"))
        if result != expected:
            raise SystemExit("certificate mismatch")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
