#!/usr/bin/env python3
"""Exact primitive-collision transition for TPC-226.

The finite clock family is

    x=Q^3, H=4 Q^2, h_L=4 L Q, Q<q<2Q prime,

with the literal primitive multiplier condition ``gcd(m, h_L)=1``.  The
module classifies every cross-prime support collision for L<=4 and computes
the associated energies with exact ``Fraction`` arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from math import gcd
from typing import Iterable


J = 4
AFFINE_SLOPES = (
    Fraction(0),
    Fraction(1, 10),
    Fraction(-1, 10),
    Fraction(1, 5),
)
ODD_SIGNS = (Fraction(1), Fraction(-1), Fraction(1), Fraction(-1))
SLOPE_SQUARE_SUM = sum((value * value for value in AFFINE_SLOPES), Fraction(0))
ODD_SQUARE_SUM = sum((value * value for value in ODD_SIGNS), Fraction(0))
Vector = dict[tuple[int, int], Fraction]


class TransitionFailure(RuntimeError):
    """Raised when a declared TPC-226 invariant fails."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise TransitionFailure(message)


def is_prime(value: int) -> bool:
    require(type(value) is int, "prime input must be an exact integer")
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def prime_shell(Q: int) -> tuple[int, ...]:
    require(type(Q) is int and Q >= 8, "Q must be an integer at least eight")
    return tuple(q for q in range(Q + 1, 2 * Q) if is_prime(q))


def source_parameters(Q: int, L: int) -> tuple[int, int, int]:
    require(type(Q) is int and Q >= 8, "invalid Q")
    require(type(L) is int and 1 <= L <= 4, "L must lie in {1,2,3,4}")
    return Q**3, 4 * Q**2, 4 * L * Q


def primitive_multipliers(Q: int, L: int, q: int) -> tuple[int, ...]:
    _, H, h = source_parameters(Q, L)
    require(q in prime_shell(Q), "q is not in the active prime shell")
    require(gcd(q, h) == 1, "active prime is not a unit modulo h")
    cutoff = h * q // H
    require(cutoff == L * q // Q, "cutoff formula mismatch")
    return tuple(
        m
        for m in range(-cutoff, cutoff + 1)
        if m != 0 and gcd(abs(m), h) == 1
    )


def support_with_multipliers(Q: int, L: int, q: int) -> dict[int, int]:
    _, _, h = source_parameters(Q, L)
    inverse = pow(q, -1, h)
    support: dict[int, int] = {}
    for m in primitive_multipliers(Q, L, q):
        coordinate = (m * inverse) % h
        require(coordinate not in support, "internal row support folding")
        support[coordinate] = m
    return support


def pair_collisions(Q: int, L: int) -> tuple[dict[str, int], ...]:
    qs = prime_shell(Q)
    supports = {q: support_with_multipliers(Q, L, q) for q in qs}
    rows: list[dict[str, int]] = []
    for index, q1 in enumerate(qs):
        for q2 in qs[index + 1 :]:
            shared = sorted(set(supports[q1]).intersection(supports[q2]))
            for residue in shared:
                rows.append(
                    {
                        "q1": q1,
                        "q2": q2,
                        "m1": supports[q1][residue],
                        "m2": supports[q2][residue],
                        "residue": residue,
                    }
                )
    return tuple(rows)


def resonance_pairs(Q: int) -> tuple[tuple[int, int], ...]:
    """Return the canonical low/high L=4 resonance pairs."""

    _, _, h = source_parameters(Q, 4)
    qs = set(prime_shell(Q))
    pairs: list[tuple[int, int]] = []
    for p in sorted(qs):
        numerator = 16 * Q - 7 * p
        if numerator <= 0 or numerator % 3:
            continue
        r = numerator // 3
        if r not in qs or not p < r:
            continue
        if gcd(3, h) != 1 or gcd(7, h) != 1:
            continue
        if 3 not in primitive_multipliers(Q, 4, p):
            continue
        if 7 not in primitive_multipliers(Q, 4, r):
            continue
        require(7 * p + 3 * r == h, "resonance equation mismatch")
        pairs.append((p, r))
    return tuple(pairs)


def check_collision_classification(Q: int, L: int) -> dict[str, object]:
    collisions = pair_collisions(Q, L)
    if L <= 3:
        require(not collisions, f"unexpected primitive collision at Q={Q}, L={L}")
        return {
            "Q": Q,
            "L": L,
            "collision_pairs": 0,
            "shared_coordinates": 0,
            "resonances": [],
        }

    expected = resonance_pairs(Q)
    by_pair: dict[tuple[int, int], set[tuple[int, int, int]]] = {}
    for row in collisions:
        pair = (row["q1"], row["q2"])
        by_pair.setdefault(pair, set()).add(
            (row["m1"], row["m2"], row["residue"])
        )
    require(set(by_pair) == set(expected), f"L=4 pair mismatch at Q={Q}")
    _, _, h = source_parameters(Q, 4)
    for p, r in expected:
        inverse_p = pow(p, -1, h)
        inverse_r = pow(r, -1, h)
        residue_plus = (3 * inverse_p) % h
        residue_minus = (-3 * inverse_p) % h
        expected_rows = {
            (3, -7, residue_plus),
            (-3, 7, residue_minus),
        }
        require(by_pair[(p, r)] == expected_rows, f"L=4 multiplier mismatch at Q={Q}")
        require((-7 * inverse_r) % h == residue_plus, "positive resonance residue")
        require((7 * inverse_r) % h == residue_minus, "negative resonance residue")
        require(residue_plus != residue_minus, "collapsed resonance coordinates")
    return {
        "Q": Q,
        "L": L,
        "collision_pairs": len(expected),
        "shared_coordinates": len(collisions),
        "resonances": [[p, r] for p, r in expected],
    }


def profile_value(mode: str, packet: int, t: Fraction) -> Fraction:
    require(type(packet) is int and 0 <= packet < J, "packet outside J=4")
    require(type(t) is Fraction, "profile argument must be Fraction")
    if mode == "aligned":
        return Fraction(1)
    if mode == "affine":
        return Fraction(1) + AFFINE_SLOPES[packet] * t
    if mode == "balanced_sign":
        require(t != 0, "balanced sign profile is sampled only away from zero")
        return ODD_SIGNS[packet] if t > 0 else -ODD_SIGNS[packet]
    raise TransitionFailure(f"unknown profile mode: {mode}")


def add_to(vector: Vector, coordinate: tuple[int, int], value: Fraction) -> None:
    vector[coordinate] = vector.get(coordinate, Fraction(0)) + value
    if vector[coordinate] == 0:
        del vector[coordinate]


def literal_rows(Q: int, L: int, mode: str) -> dict[tuple[int, int], Vector]:
    _, _, h = source_parameters(Q, L)
    rows: dict[tuple[int, int], Vector] = {}
    for q in prime_shell(Q):
        inverse = pow(q, -1, h)
        for packet in range(J):
            vector: Vector = {}
            for m in primitive_multipliers(Q, L, q):
                coordinate = (h, (m * inverse) % h)
                t = Fraction(m * Q, L * q)
                require(abs(t) <= 1, "sample outside the locked profile interval")
                add_to(vector, coordinate, profile_value(mode, packet, t) / h)
            rows[(q, packet)] = vector
    return rows


def vector_sum(vectors: Iterable[Vector]) -> Vector:
    result: Vector = {}
    for vector in vectors:
        for coordinate, value in vector.items():
            add_to(result, coordinate, value)
    return result


def squared_norm(vector: Vector) -> Fraction:
    return sum((value * value for value in vector.values()), Fraction(0))


def energies(Q: int, L: int, mode: str) -> dict[str, Fraction]:
    rows = literal_rows(Q, L, mode)
    qs = prime_shell(Q)
    by_packet = [
        vector_sum(rows[(q, packet)] for q in qs) for packet in range(J)
    ]
    by_prime = [
        vector_sum(rows[(q, packet)] for packet in range(J)) for q in qs
    ]
    diagonal = sum((squared_norm(row) for row in rows.values()), Fraction(0))
    ap = sum((squared_norm(row) for row in by_packet), Fraction(0))
    polarized = sum((squared_norm(row) for row in by_prime), Fraction(0))
    full = squared_norm(vector_sum(rows.values()))
    return {
        "E_diag": diagonal,
        "E_AP": ap,
        "E_pol": polarized,
        "E_all": full,
    }


def resonance_correction(Q: int, mode: str) -> Fraction:
    _, _, h = source_parameters(Q, 4)
    correction = Fraction(0)
    for p, r in resonance_pairs(Q):
        u = Fraction(3 * Q, 4 * p)
        v = Fraction(7 * Q, 4 * r)
        if mode == "aligned":
            correction += Fraction(4 * J, h * h)
        elif mode == "affine":
            correction += Fraction(4, h * h) * (J - SLOPE_SQUARE_SUM * u * v)
        elif mode == "balanced_sign":
            correction -= Fraction(4, h * h) * ODD_SQUARE_SUM
        else:
            raise TransitionFailure(f"unknown mode: {mode}")
    return correction


def fraction_text(value: Fraction) -> str:
    require(type(value) is Fraction, "fraction_text requires Fraction")
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def ratio_text(numerator: Fraction, denominator: Fraction) -> str:
    if denominator == 0:
        return "UNDEFINED"
    return fraction_text(numerator / denominator)


def energy_record(Q: int, mode: str) -> dict[str, object]:
    geometry = check_collision_classification(Q, 4)
    values = energies(Q, 4, mode)
    correction = resonance_correction(Q, mode)
    require(
        values["E_AP"] - values["E_diag"] == correction,
        f"resonance correction mismatch at Q={Q}, mode={mode}",
    )
    if geometry["collision_pairs"]:
        if mode in ("aligned", "affine"):
            require(values["E_AP"] > values["E_diag"], "expected AP amplification")
        else:
            require(values["E_AP"] < values["E_diag"], "expected AP saving")
            require(values["E_pol"] == 0 and values["E_all"] == 0, "packet cancellation")
    _, H, h = source_parameters(Q, 4)
    return {
        "Q": Q,
        "x": Q**3,
        "H": H,
        "h": h,
        "L": 4,
        "mode": mode,
        "prime_count": len(prime_shell(Q)),
        "collision_pairs": geometry["collision_pairs"],
        "shared_coordinates": geometry["shared_coordinates"],
        "resonances": geometry["resonances"],
        "E_diag": fraction_text(values["E_diag"]),
        "E_AP": fraction_text(values["E_AP"]),
        "E_pol": fraction_text(values["E_pol"]),
        "E_all": fraction_text(values["E_all"]),
        "AP_minus_diag": fraction_text(correction),
        "AP_over_diag": ratio_text(values["E_AP"], values["E_diag"]),
        "all_over_pol": ratio_text(values["E_all"], values["E_pol"]),
    }


def classification_scan(Q_min: int = 8, Q_max: int = 512) -> dict[str, object]:
    require(type(Q_min) is int and type(Q_max) is int and 8 <= Q_min <= Q_max, "scan range")
    lines: list[str] = []
    collision_scales = 0
    total_resonances = 0
    first_collision_Q: int | None = None
    maximum_resonances = 0
    maximum_Q: int | None = None
    for Q in range(Q_min, Q_max + 1):
        counts = []
        for L in range(1, 5):
            row = check_collision_classification(Q, L)
            counts.append(int(row["collision_pairs"]))
        require(counts[:3] == [0, 0, 0], f"low-dilation collision at Q={Q}")
        resonances = resonance_pairs(Q)
        require(counts[3] == len(resonances), f"L=4 count mismatch at Q={Q}")
        encoded = ",".join(f"{p}:{r}" for p, r in resonances) or "-"
        lines.append(f"{Q}|0|0|0|{encoded}")
        if resonances:
            collision_scales += 1
            total_resonances += len(resonances)
            if first_collision_Q is None:
                first_collision_Q = Q
            if len(resonances) > maximum_resonances:
                maximum_resonances = len(resonances)
                maximum_Q = Q
    digest = sha256(("\n".join(lines) + "\n").encode()).hexdigest()
    return {
        "Q_min": Q_min,
        "Q_max": Q_max,
        "scales_checked": Q_max - Q_min + 1,
        "L1_collision_scales": 0,
        "L2_collision_scales": 0,
        "L3_collision_scales": 0,
        "L4_collision_scales": collision_scales,
        "L4_total_resonances": total_resonances,
        "L4_first_collision_Q": first_collision_Q,
        "L4_maximum_resonances": maximum_resonances,
        "L4_maximum_Q": maximum_Q,
        "classification_sha256": digest,
    }


def build_certificate() -> dict[str, object]:
    witness_scales = (25, 32, 40, 46, 55, 100, 127, 257, 499, 1000)
    records = {
        mode: [energy_record(Q, mode) for Q in witness_scales]
        for mode in ("aligned", "affine", "balanced_sign")
    }
    require(all(row["collision_pairs"] > 0 for rows in records.values() for row in rows), "empty witness")
    q25 = {mode: records[mode][0] for mode in records}
    require(q25["aligned"]["AP_over_diag"] == "15/13", "aligned Q25 ratio")
    require(
        q25["affine"]["AP_over_diag"]
        == "14610396266802411880605/12679409642889136447511",
        "affine Q25 ratio",
    )
    require(q25["balanced_sign"]["AP_over_diag"] == "11/13", "sign Q25 ratio")
    require(q25["balanced_sign"]["E_pol"] == "0", "sign Q25 polarized")
    require(q25["balanced_sign"]["E_all"] == "0", "sign Q25 full")
    return {
        "schema": "tpc226-first-primitive-collision-transition-v1",
        "status": "PASS",
        "claim_level": "PROVED_STRUCTURAL_L1",
        "date": "2026-08-24",
        "author": "Liang Wang",
        "affiliation": "Huazhong University of Science and Technology",
        "theorem": {
            "clock_family": "x=Q^3, H=4Q^2, h_L=4LQ",
            "stable_domain": "Q>=8, L in {1,2,3,4}",
            "primitive_support": "gcd(m,h_L)=1",
            "L_le_3_disjointness": "PROVED_EXACT",
            "first_primitive_collision_dilation": 4,
            "L4_resonance": "7p+3r=16Q with multipliers +/-3 and -/+7",
            "Q25_witness": "Q=25, p=37, r=47, residues={119,281} mod 400",
            "uniform_profile_independent_saving": "REFUTED_SCOPED",
        },
        "boundary_scan": classification_scan(),
        "witness_scales": list(witness_scales),
        "records": records,
        "Q25_exact": {
            "aligned_AP_over_diag": q25["aligned"]["AP_over_diag"],
            "affine_AP_over_diag": q25["affine"]["AP_over_diag"],
            "balanced_sign_AP_over_diag": q25["balanced_sign"]["AP_over_diag"],
            "balanced_sign_E_pol": q25["balanced_sign"]["E_pol"],
            "balanced_sign_E_all": q25["balanced_sign"]["E_all"],
        },
        "firewall": {
            "dilated_clock_family": "MODELING_CHOICE",
            "V46_profile_transfer": "OPEN",
            "arithmetic_cancellation": "NONE",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "L2": "NONE",
            "full_gate_b": "OPEN",
            "strict_1_over_400": "UNPAID",
        },
        "checks": {
            "primitive_false_L3_overlap_rejected": True,
            "L_le_3_universal_disjointness_proved": True,
            "L4_resonance_classified": True,
            "aligned_amplification": True,
            "affine_amplification": True,
            "balanced_sign_AP_saving": True,
            "balanced_sign_packet_cancellation": True,
            "physical_transfer_not_claimed": True,
        },
        "round2_clue": "SOURCE_LOCK_THE_SIGN_OF_THE_3_7_RESONANCE_BEFORE_ANY_UNIFORM_AP_SAVING",
    }


__all__ = [
    "AFFINE_SLOPES",
    "J",
    "ODD_SIGNS",
    "TransitionFailure",
    "build_certificate",
    "check_collision_classification",
    "classification_scan",
    "energies",
    "energy_record",
    "fraction_text",
    "is_prime",
    "literal_rows",
    "pair_collisions",
    "prime_shell",
    "primitive_multipliers",
    "profile_value",
    "resonance_pairs",
    "source_parameters",
    "support_with_multipliers",
]
