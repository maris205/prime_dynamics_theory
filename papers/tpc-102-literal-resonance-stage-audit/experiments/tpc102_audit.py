#!/usr/bin/env python3
"""Finite route-ledger checks for TPC-102; not a prime-pair theorem."""

from __future__ import annotations

from fractions import Fraction
import json
import math


PRIMES = (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)
TOL = 1.0e-10


def check_branch_partition() -> int:
    checks = 0
    for q in PRIMES:
        for omega in range(0, q):
            for u in range(1, 2 * q + 1):
                constant = omega == 0
                q_divides_u = (not constant) and u % q == 0
                invertible = (not constant) and u % q != 0
                assert int(constant) + int(q_divides_u) + int(invertible) == 1
                checks += 1
    return checks


def deterministic_cells(q: int, h: int) -> list[list[int]]:
    n = q - 1
    cells: list[list[int]] = []
    for c in range(1, 2 + h % 4):
        size = 1 + ((h + 2 * c) % min(6, n))
        cells.append([1 + ((3 * h + c + 2 * j) % 9) for j in range(size)])
    return cells


def check_master_diagonal_ledger() -> tuple[int, float]:
    checks = 0
    worst_ratio = 0.0
    for q in PRIMES:
        n = q - 1
        principal = 0.0
        diagonal_weighted = 0.0
        active = 0
        max_atom = 0
        for h in range(1, n // 2 + 1):
            cells = deterministic_cells(q, h)
            mass = sum(sum(cell) for cell in cells)
            diagonal = sum(
                sum(w * w for w in cell) - sum(cell) ** 2 / n
                for cell in cells
            )
            assert diagonal >= -TOL
            max_atom = max(max_atom, *(w for cell in cells for w in cell))
            g_sq = Fraction(2 * h * (n - 2 * h), n)
            g = math.sqrt(float(g_sq))
            principal += (2 * h / n) * mass
            diagonal_weighted += g * math.sqrt(max(0.0, diagonal))
            if g > 0 and mass > 0:
                active += 1
            checks += 1 + sum(len(cell) for cell in cells)
        rhs = math.sqrt(max_atom * active * n * principal)
        assert diagonal_weighted <= rhs + TOL
        if rhs > 0:
            worst_ratio = max(worst_ratio, diagonal_weighted / rhs)
        checks += 1
    return checks, worst_ratio


def check_width_and_exponents() -> tuple[int, dict[str, str]]:
    checks = 0
    for q in PRIMES:
        n = q - 1
        for length in range(1, q + 1):
            h = min(n // 2, q // length)
            g = math.sqrt(2 * h * (n - 2 * h) / n)
            if length <= 2:
                assert g == 0.0
            else:
                assert g <= math.sqrt(2 * q / length) + TOL
            checks += 1
    q_exp = Fraction(267, 400)
    j_exp = Fraction(133, 400)
    old_exp = q_exp / 2
    new_exp = (q_exp - j_exp) / 2
    gain_exp = old_exp - new_exp
    assert new_exp == Fraction(67, 400)
    assert gain_exp == Fraction(133, 800)
    checks += 2
    ledger = {
        "q_exponent": str(q_exp),
        "j_exponent": str(j_exp),
        "old_sqrt_q_exponent": str(old_exp),
        "long_fiber_factor_exponent": str(new_exp),
        "gain_exponent": str(gain_exp),
        "strict_endpoint_budget": "1/400",
    }
    return checks, ledger


def main() -> None:
    branch_checks = check_branch_partition()
    diagonal_checks, worst_ratio = check_master_diagonal_ledger()
    width_checks, ledger = check_width_and_exponents()
    report = {
        "all_checks_passed": True,
        "counts": {
            "disjoint_branch_partition": branch_checks,
            "master_diagonal_ledger": diagonal_checks,
            "width_and_exponent_ledger": width_checks,
        },
        "maximum_diagonal_transfer_ratio": worst_ratio,
        "exponent_ledger": ledger,
        "claim_levels": {
            "finite_algebra": "L0",
            "literal_master_crosswalk": "L1",
            "growing_fixed_h0_arithmetic_estimate": "not proved",
        },
        "description": (
            "Finite dependency, branch-partition, diagonal-transfer, "
            "and exponent-ledger audit; not evidence for Mobius "
            "cancellation or a prime-pair theorem"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
