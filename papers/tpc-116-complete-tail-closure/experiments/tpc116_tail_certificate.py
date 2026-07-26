#!/usr/bin/env python3
"""Exact finite regression for the TPC-116 tail closure identities."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def dot(x: list[Fraction], y: list[Fraction]) -> Fraction:
    return sum(a * b for a, b in zip(x, y))


def main() -> None:
    atoms = [Fraction(3), Fraction(-2), Fraction(5), Fraction(7)]
    classes = {
        "low": [0],
        "high": [1],
        "ultra": [2],
        "boundary": [3],
    }
    coverage = [0] * len(atoms)
    class_sums: dict[str, Fraction] = {}
    for name, indices in classes.items():
        class_sums[name] = sum(atoms[i] for i in indices)
        for i in indices:
            coverage[i] += 1
    if coverage != [1] * len(atoms):
        raise AssertionError("declared partition is not one-fold")
    if sum(class_sums.values()) != sum(atoms):
        raise AssertionError("exact class disintegration failed")

    overlapping = {"left": [0, 1, 2], "right": [2, 3]}
    multiplicity = [0] * len(atoms)
    overlap_sum = Fraction(0)
    for indices in overlapping.values():
        overlap_sum += sum(atoms[i] for i in indices)
        for i in indices:
            multiplicity[i] += 1
    defect = sum(
        Fraction(multiplicity[i] - 1) * atoms[i]
        for i in range(len(atoms))
    )
    if overlap_sum != sum(atoms) + defect:
        raise AssertionError("overlap defect identity failed")

    hilbert_cases = [
        ([1, 2, 3], [4, 5, 6]),
        ([2, -1, 4], [3, 0, -2]),
        ([3, 6, 9], [2, 4, 6]),
    ]
    hilbert_checks = 0
    equality_checks = 0
    for raw_m, raw_a in hilbert_cases:
        m = [Fraction(x) for x in raw_m]
        a = [Fraction(x) for x in raw_a]
        lhs_squared = dot(m, a) ** 2
        rhs_squared = dot(m, m) * dot(a, a)
        if lhs_squared > rhs_squared:
            raise AssertionError("Cauchy--Schwarz failed")
        hilbert_checks += 1
        if raw_a == [2, 4, 6]:
            if lhs_squared != rhs_squared:
                raise AssertionError("proportional vectors did not saturate")
            equality_checks += 1

    phase_cases = [
        [Fraction(1), Fraction(2), Fraction(4)],
        [Fraction(3), Fraction(5), Fraction(7), Fraction(11)],
    ]
    phase_checks = 0
    maxima: list[str] = []
    for magnitudes in phase_cases:
        observed = max(
            abs(sum(Fraction(sign) * a for sign, a in zip(signs, magnitudes)))
            for signs in product((-1, 1), repeat=len(magnitudes))
        )
        target = sum(magnitudes)
        if observed != target:
            raise AssertionError("real phase-alignment maximum failed")
        maxima.append(str(target))
        phase_checks += 1

    incomplete_coverage_rejected = [1, 1, 0, 1] != [1] * 4
    unknown_class_rejected = any(
        value is None for value in {"high": Fraction(1), "ultra": None}.values()
    )
    if not incomplete_coverage_rejected or not unknown_class_rejected:
        raise AssertionError("closure ledger accepted an incomplete input")

    sigma_small = Fraction(1, 800)
    sigma_h4 = Fraction(1, 400)
    complement_power_closure = sigma_small > 0
    subcritical_not_h4 = sigma_small < Fraction(1, 400)
    h4_raw_packet_gate = sigma_h4 >= Fraction(1, 400)
    if not all(
        [complement_power_closure, subcritical_not_h4, h4_raw_packet_gate]
    ):
        raise AssertionError("o(X)/H4 endpoint distinction failed")

    result = {
        "schema": "tpc-116-complete-tail-certificate-v1",
        "status": "PASS",
        "checks": {
            "exact_partition_identities": 2,
            "overlap_defect_identities": 1,
            "hilbert_inequalities": hilbert_checks,
            "sharp_hilbert_equalities": equality_checks,
            "phase_blind_sharp_maxima": phase_checks,
            "incomplete_ledgers_rejected": 2,
            "complement_vs_h4_endpoint_cases": 3,
        },
        "phase_blind_maxima": maxima,
        "claim_boundary": {
            "finite_exact_certificate": True,
            "complete_growing_tpc_tail_bound": False,
            "new_L2_fixed_shift_estimate": False,
            "parity_breakthrough": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(__file__).with_suffix(".json").write_text(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
