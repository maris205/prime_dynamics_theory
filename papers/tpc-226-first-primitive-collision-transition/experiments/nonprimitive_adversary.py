#!/usr/bin/env python3
"""Adversarial checks for the primitive-support and sign firewalls."""

from __future__ import annotations

import sys
from fractions import Fraction
from math import gcd
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from primitive_collision_transition import (  # noqa: E402
    energies,
    pair_collisions,
    prime_shell,
    resonance_pairs,
    source_parameters,
)


class AdversaryFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise AdversaryFailure(message)


def nonprimitive_collisions(Q: int, L: int) -> list[tuple[int, int, int, int, int]]:
    _, _, h = source_parameters(Q, L)
    rows = {}
    for q in prime_shell(Q):
        inverse = pow(q, -1, h)
        cutoff = L * q // Q
        rows[q] = {
            m * inverse % h: m
            for m in range(-cutoff, cutoff + 1)
            if m
        }
    found = []
    qs = sorted(rows)
    for index, q1 in enumerate(qs):
        for q2 in qs[index + 1 :]:
            for residue in set(rows[q1]).intersection(rows[q2]):
                found.append((q1, q2, rows[q1][residue], rows[q2][residue], residue))
    return sorted(found)


def main() -> int:
    try:
        fake = nonprimitive_collisions(8, 3)
        need(fake == [(11, 13, -4, 4, 52), (11, 13, 4, -4, 44)], "fake L3 fixture")
        need(all(gcd(abs(row[2]), 96) > 1 for row in fake), "fake multiplier should be nonprimitive")
        need(pair_collisions(8, 3) == (), "primitive L3 support must be disjoint")

        need(resonance_pairs(25) == ((37, 47),), "Q25 resonance")
        real = pair_collisions(25, 4)
        need(len(real) == 2, "Q25 coordinate multiplicity")
        need({row["residue"] for row in real} == {119, 281}, "Q25 residues")
        need({(row["m1"], row["m2"]) for row in real} == {(3, -7), (-3, 7)}, "Q25 multipliers")

        aligned = energies(25, 4, "aligned")
        affine = energies(25, 4, "affine")
        signed = energies(25, 4, "balanced_sign")
        need(aligned["E_AP"] / aligned["E_diag"] == Fraction(15, 13), "aligned ratio")
        need(
            affine["E_AP"] / affine["E_diag"]
            == Fraction(14610396266802411880605, 12679409642889136447511),
            "affine ratio",
        )
        need(signed["E_AP"] / signed["E_diag"] == Fraction(11, 13), "sign ratio")
        need(signed["E_pol"] == 0 and signed["E_all"] == 0, "sign packet cancellation")
        need(aligned["E_AP"] > aligned["E_diag"], "aligned must amplify")
        need(affine["E_AP"] > affine["E_diag"], "affine must amplify")
        need(signed["E_AP"] < signed["E_diag"], "sign profile must save")
    except (AdversaryFailure, OSError, ValueError) as error:
        print(f"TPC226_NONPRIMITIVE_ADVERSARY=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC226_NONPRIMITIVE_ADVERSARY=PASS")
    print("fake_L3_coordinates=2")
    print("real_L4_coordinates=2")
    print("profile_sign_trichotomy=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
