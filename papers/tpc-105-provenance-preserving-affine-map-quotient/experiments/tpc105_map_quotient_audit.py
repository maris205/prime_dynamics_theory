#!/usr/bin/env python3
"""Exact finite regression for the TPC-105 canonical map quotient."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
import json


PRIMES = (5, 7, 11, 13, 17, 19)


@dataclass(frozen=True)
class Atom:
    label: str
    q: int
    h: int
    A: int
    m: int
    j: int
    weight: int

    @property
    def affine_map(self) -> tuple[int, int]:
        return ((self.A * self.m) % self.q, (self.A * self.h) % self.q)

    @property
    def omega(self) -> int:
        s, t = self.affine_map
        return (s * self.j + t) % self.q


def census_direct(atoms: list[Atom]) -> dict[int, int]:
    out: dict[int, int] = defaultdict(int)
    for atom in atoms:
        out[atom.omega] += atom.weight
    return dict(out)


def profiles(atoms: list[Atom]) -> dict[tuple[int, int], dict[int, int]]:
    out: dict[tuple[int, int], dict[int, int]] = {}
    for atom in atoms:
        profile = out.setdefault(atom.affine_map, {})
        profile[atom.j] = profile.get(atom.j, 0) + atom.weight
    return out


def census_quotient(
    q: int, data: dict[tuple[int, int], dict[int, int]]
) -> dict[int, int]:
    out: dict[int, int] = defaultdict(int)
    for (s, t), profile in data.items():
        for j, weight in profile.items():
            out[(s * j + t) % q] += weight
    return dict(out)


def centered_kernel(equal: bool, q: int) -> Fraction:
    return Fraction(int(equal), 1) - Fraction(1, q - 1)


def direct_cross(atoms: list[Atom]) -> Fraction:
    total = Fraction(0)
    for i, left in enumerate(atoms):
        for k, right in enumerate(atoms):
            if i == k:
                continue
            total += (
                left.weight
                * right.weight
                * centered_kernel(left.omega == right.omega, left.q)
            )
    return total


def split_cross(atoms: list[Atom]) -> tuple[Fraction, Fraction]:
    identical = Fraction(0)
    distinct = Fraction(0)
    for i, left in enumerate(atoms):
        for k, right in enumerate(atoms):
            if i == k:
                continue
            term = (
                left.weight
                * right.weight
                * centered_kernel(left.omega == right.omega, left.q)
            )
            if left.affine_map == right.affine_map:
                identical += term
            else:
                distinct += term
    return identical, distinct


def identical_profile_formula(atoms: list[Atom]) -> Fraction:
    q = atoms[0].q
    by_map: dict[tuple[int, int], list[Atom]] = defaultdict(list)
    for atom in atoms:
        by_map[atom.affine_map].append(atom)
    collision = 0
    baseline_pairs = 0
    for members in by_map.values():
        by_input: dict[int, list[Atom]] = defaultdict(list)
        for atom in members:
            by_input[atom.j].append(atom)
        for group in by_input.values():
            mass = sum(atom.weight for atom in group)
            squares = sum(atom.weight**2 for atom in group)
            collision += mass**2 - squares
        mass = sum(atom.weight for atom in members)
        squares = sum(atom.weight**2 for atom in members)
        baseline_pairs += mass**2 - squares
    return Fraction(collision, 1) - Fraction(baseline_pairs, q - 1)


def distinct_profile_formula(atoms: list[Atom]) -> Fraction:
    q = atoms[0].q
    data = profiles(atoms)
    total = Fraction(0)
    for left_map, left_profile in data.items():
        for right_map, right_profile in data.items():
            if left_map == right_map:
                continue
            left_s, left_t = left_map
            right_s, right_t = right_map
            for left_j, left_weight in left_profile.items():
                left_omega = (left_s * left_j + left_t) % q
                for right_j, right_weight in right_profile.items():
                    right_omega = (right_s * right_j + right_t) % q
                    total += (
                        left_weight
                        * right_weight
                        * centered_kernel(left_omega == right_omega, q)
                    )
    return total


def main() -> None:
    census_checks = 0
    split_checks = 0
    classification_checks = 0
    concentration_checks = 0

    for q in PRIMES:
        for h in (1, 2):
            if h >= q:
                continue
            atoms: list[Atom] = []
            for index in range(1, 4 * q + 1):
                A = 1 + ((3 * index + h) % (q - 1))
                m = 1 + ((5 * index + 2 * h) % (q - 1))
                j = (7 * index + h) % q
                weight = 1 + ((11 * index + q) % 9)
                candidate = Atom(f"p{index}", q, h, A, m, j, weight)
                if candidate.omega != 0:
                    atoms.append(candidate)

            if not atoms or any(atom.omega == 0 for atom in atoms):
                raise AssertionError(("physical-support", q, h))

            data = profiles(atoms)
            if census_direct(atoms) != census_quotient(q, data):
                raise AssertionError(("census", q, h))
            census_checks += 1

            for left in atoms:
                for right in atoms:
                    same_map = left.affine_map == right.affine_map
                    classified = (
                        left.A % q == right.A % q
                        and left.m % q == right.m % q
                    )
                    if same_map != classified:
                        raise AssertionError(("classification", left, right))
                    if same_map:
                        same_output = left.omega == right.omega
                        if same_output != (left.j % q == right.j % q):
                            raise AssertionError(("same-map-output", left, right))
                    classification_checks += 1

            direct = direct_cross(atoms)
            identical, distinct = split_cross(atoms)
            if direct != identical + distinct:
                raise AssertionError(("split", q, h))
            if identical != identical_profile_formula(atoms):
                raise AssertionError(("identical-profile-formula", q, h))
            if distinct != distinct_profile_formula(atoms):
                raise AssertionError(("distinct-profile-formula", q, h))
            split_checks += 3

            by_map: dict[tuple[int, int], list[Atom]] = defaultdict(list)
            for atom in atoms:
                by_map[atom.affine_map].append(atom)
            masses = [sum(atom.weight for atom in values) for values in by_map.values()]
            upper = max(masses) * sum(atom.weight for atom in atoms)
            pair_mass = sum(
                sum(atom.weight for atom in values) ** 2
                - sum(atom.weight**2 for atom in values)
                for values in by_map.values()
            )
            if abs(identical) > pair_mass or pair_mass > upper:
                raise AssertionError(("concentration-chain", q, h))
            concentration_checks += 2

    # Same map and same total mass, but different input profiles/censuses.
    left = [Atom("left", 5, 1, 1, 1, 0, 1)]
    right = [Atom("right", 5, 1, 1, 1, 1, 1)]
    if left[0].affine_map != right[0].affine_map:
        raise AssertionError("mass-only witness maps differ")
    if sum(a.weight for a in left) != sum(a.weight for a in right):
        raise AssertionError("mass-only witness totals differ")
    if census_direct(left) == census_direct(right):
        raise AssertionError("mass-only witness did not change census")

    # Unit atom cap with arbitrary map-class mass.
    atom_cap_witness_checks = 0
    for size in (1, 2, 5, 11, 23):
        witness = [
            Atom(f"w{k}", 29, 1, 1, 1, k % 29, 1)
            for k in range(size)
        ]
        map_mass = sum(atom.weight for atom in witness)
        atom_cap = max(atom.weight for atom in witness)
        if (atom_cap, map_mass) != (1, size):
            raise AssertionError(("atom-map witness", size))
        atom_cap_witness_checks += 1

    result = {
        "schema": "tpc-105-map-quotient-audit-v1",
        "status": "PASS",
        "checks": {
            "direct_vs_quotient_censuses": census_checks,
            "map_classification_pairs": classification_checks,
            "cross_split_and_profile_identities": split_checks,
            "identical_map_concentration_bounds": concentration_checks,
            "mass_only_counterexample": 1,
            "atom_cap_vs_map_mass_counterexamples": atom_cap_witness_checks,
        },
        "claim_boundary": {
            "finite_exact_certificate": True,
            "lossless_literal_quotient_proved_in_paper": True,
            "actual_map_class_cap_proved": False,
            "actual_distinct_map_incidence_proved": False,
            "new_L2_fixed_shift_estimate": False,
            "parity_breakthrough": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
