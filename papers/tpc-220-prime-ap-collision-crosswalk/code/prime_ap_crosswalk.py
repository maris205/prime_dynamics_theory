#!/usr/bin/env python3
"""Exact prime-AP and multiplicative-collision crosswalk for TPC-220."""

from __future__ import annotations

from fractions import Fraction
import math


class CrosswalkFailure(RuntimeError):
    pass


Q_VALUES = (101, 103, 107, 109)
H_VALUES = (17, 19, 23)
HEIGHT = 500


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CrosswalkFailure(message)


def primitive_residues(h: int) -> tuple[int, ...]:
    return tuple(a for a in range(h) if math.gcd(a, h) == 1)


def atoms(h: int, q: int) -> tuple[int, ...]:
    length = h * q // HEIGHT
    return tuple(m for m in range(-length, length + 1) if m and math.gcd(m, h) == 1)


def profile_value(profile: str, h: int, m: int, q: int) -> Fraction:
    t = Fraction(HEIGHT * m, h * q)
    if profile == "constant":
        return Fraction(1)
    if profile == "affine":
        return Fraction(1) + t / 100
    raise CrosswalkFailure(f"unknown profile: {profile}")


def row(h: int, q: int, profile: str) -> dict[int, Fraction]:
    values = {a: Fraction(0) for a in primitive_residues(h)}
    inverse = pow(q, -1, h)
    for m in atoms(h, q):
        a = (m * inverse) % h
        values[a] += profile_value(profile, h, m, q)
    return values


def ap_crosswalk(h: int, a: int, profile: str) -> Fraction:
    inverse_a = pow(a, -1, h)
    total = Fraction(0)
    max_length = h * max(Q_VALUES) // HEIGHT
    for m in range(-max_length, max_length + 1):
        if not m or math.gcd(m, h) != 1:
            continue
        residue = (inverse_a * m) % h
        for q in Q_VALUES:
            if q % h == residue and abs(m) <= h * q // HEIGHT:
                total += profile_value(profile, h, m, q)
    return total


def direct_reassembled(h: int, a: int, profile: str) -> Fraction:
    return sum((row(h, q, profile)[a] for q in Q_VALUES), Fraction(0))


def gram_direct(h: int, q: int, qp: int, profile: str) -> Fraction:
    left = row(h, q, profile)
    right = row(h, qp, profile)
    return sum((left[a] * right[a] for a in primitive_residues(h)), Fraction(0))


def gram_collision(h: int, q: int, qp: int, profile: str) -> Fraction:
    total = Fraction(0)
    for m in atoms(h, q):
        for mp in atoms(h, qp):
            if (m * qp - mp * q) % h == 0:
                total += profile_value(profile, h, m, q) * profile_value(profile, h, mp, qp)
    return total


def diagonal_formula(h: int, q: int, profile: str) -> Fraction:
    return sum(
        (profile_value(profile, h, m, q) ** 2 for m in atoms(h, q)),
        Fraction(0),
    )


def record(h: int, profile: str) -> dict[str, object]:
    crosswalk_residuals = []
    gram_residuals = []
    diagonal_residuals = []
    offdiag = []
    for a in primitive_residues(h):
        crosswalk_residuals.append(str(direct_reassembled(h, a, profile) - ap_crosswalk(h, a, profile)))
    for q in Q_VALUES:
        for qp in Q_VALUES:
            direct = gram_direct(h, q, qp, profile)
            collision = gram_collision(h, q, qp, profile)
            gram_residuals.append(str(direct - collision))
            if q == qp:
                diagonal_residuals.append(str(direct - diagonal_formula(h, q, profile)))
            elif collision:
                offdiag.append({"q": q, "qp": qp, "collision_gram": str(collision)})
    return {
        "h": h,
        "profile": profile,
        "q_count": len(Q_VALUES),
        "primitive_residues": len(primitive_residues(h)),
        "max_cutoff": max(h * q // HEIGHT for q in Q_VALUES),
        "crosswalk_residuals": crosswalk_residuals,
        "gram_residuals": gram_residuals,
        "diagonal_residuals": diagonal_residuals,
        "offdiag_collision_entries": offdiag,
        "offdiag_entry_count": len(offdiag),
    }


def build_certificate() -> dict[str, object]:
    records = [record(h, profile) for h in H_VALUES for profile in ("constant", "affine")]
    require(all(all(value == "0" for value in r["crosswalk_residuals"]) for r in records), "crosswalk failure")
    require(all(all(value == "0" for value in r["gram_residuals"]) for r in records), "Gram failure")
    require(all(all(value == "0" for value in r["diagonal_residuals"]) for r in records), "diagonal failure")
    require(any(r["offdiag_entry_count"] > 0 for r in records), "no off-diagonal collision observed")
    return {
        "schema": "tpc220-prime-ap-collision-crosswalk-v1",
        "status": "PASS",
        "claim_level": "PROVED_STRUCTURAL_L1",
        "height": HEIGHT,
        "q_values": list(Q_VALUES),
        "h_values": list(H_VALUES),
        "records": records,
        "checks": {
            "weighted_ap_crosswalk_exact": True,
            "multiplicative_gram_exact": True,
            "diagonal_reduction_exact": True,
            "offdiagonal_collision_present": True,
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
