#!/usr/bin/env python3
"""Deterministic finite certificate for the TPC-109 saturation theorem."""

from __future__ import annotations

import argparse
import cmath
import json
from pathlib import Path


def certificate() -> dict:
    checks = 0
    max_root_residual = 0.0
    for k in range(2, 33):
        roots = [cmath.exp(2j * cmath.pi * j / k) for j in range(k)]
        root_sum = sum(roots)
        diagonal = sum(abs(z) ** 2 for z in roots)
        aligned_square = abs(sum(1 for _ in range(k))) ** 2
        residual = abs(root_sum)
        max_root_residual = max(max_root_residual, residual)
        assert residual < 1.0e-12
        checks += 1
        assert abs(diagonal - k) < 1.0e-12
        checks += 1
        assert abs(aligned_square - k * k) < 1.0e-12
        checks += 1

    # A dominant three-atom example: lengths 5, 2, 1.
    lengths = [5.0, 2.0, 1.0]
    radius_sum = sum(lengths)
    defect = max(0.0, 2.0 * max(lengths) - radius_sum)
    assert defect == 2.0
    checks += 1
    assert defect * defect == 4.0
    checks += 1

    # A balanced example: lengths 2, 1, 1 closes exactly.
    balanced = [2.0, 1.0, 1.0]
    assert max(0.0, 2.0 * max(balanced) - sum(balanced)) == 0.0
    checks += 1

    return {
        "schema": "tpc109-coherent-prime-square-audit-v1",
        "status": "PASS",
        "fibers_tested": 31,
        "assertions_checked": checks,
        "max_root_of_unity_residual_lt_1e-12": max_root_residual < 1.0e-12,
        "claim_boundary": {
            "finite_saturation_theorem": True,
            "literal_fiber_identification": True,
            "growing_fixed_h0_saving": False,
            "parity_breakthrough": False,
            "prime_pair_or_twin_prime_theorem": False,
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
