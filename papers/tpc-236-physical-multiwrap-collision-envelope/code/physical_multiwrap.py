#!/usr/bin/env python3
"""Exact physical-row collision counting and certificates for TPC-236."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from math import gcd


class MultiwrapFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise MultiwrapFailure(message)


def ceil_div(a: int, b: int) -> int:
    require(type(a) is int and type(b) is int and a >= 0 and b > 0, "ceil-div inputs")
    return (a + b - 1) // b


def primes_in_shell(Q: int) -> tuple[int, ...]:
    require(type(Q) is int and Q >= 2, "shell scale")
    sieve = bytearray(b"\x01") * (2 * Q + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int((2 * Q) ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p : 2 * Q + 1 : p] = b"\x00" * (((2 * Q - p * p) // p) + 1)
    return tuple(q for q in range(Q + 1, 2 * Q + 1) if sieve[q])


def row_atoms(Q: int, H: int, h: int, q: int) -> tuple[tuple[int, int], ...]:
    require(all(type(v) is int and v > 0 for v in (Q, H, h, q)), "positive row scales")
    require(h <= Q < q <= 2 * Q, "physical shell ordering")
    require(gcd(q, h) == 1, "shell prime must be invertible")
    cutoff = h * q // H
    q_inverse = pow(q, -1, h)
    return tuple((m * q_inverse % h, m) for m in range(-cutoff, cutoff + 1) if m)


def row_support(Q: int, H: int, h: int, q: int) -> tuple[int, ...]:
    atoms = row_atoms(Q, H, h, q)
    support = tuple(sorted(a for a, _ in atoms))
    require(len(support) == len(set(support)), "internal row collision")
    return support


def bucket_rows(Q: int, H: int, h: int) -> dict[int, dict[int, tuple[int, ...]]]:
    buckets: dict[int, dict[int, list[int]]] = {}
    for q in primes_in_shell(Q):
        for a, m in row_atoms(Q, H, h, q):
            buckets.setdefault(a, {}).setdefault(q, []).append(m)
    frozen: dict[int, dict[int, tuple[int, ...]]] = {}
    for a, rows in buckets.items():
        frozen[a] = {q: tuple(ms) for q, ms in rows.items()}
    return frozen


def gcd_fiber_bound(Q: int, H: int, h: int, a: int) -> dict[str, int]:
    require(0 <= a < h <= Q, "residue and denominator range")
    g = gcd(a, h)
    global_cutoff = 2 * h * Q // H
    possible_multipliers = 2 * (global_cutoff // g)
    reduced_modulus = h // g
    shell_class_capacity = ceil_div(Q, reduced_modulus)
    return {
        "g": g,
        "global_cutoff": global_cutoff,
        "possible_multipliers": possible_multipliers,
        "reduced_modulus": reduced_modulus,
        "shell_class_capacity": shell_class_capacity,
        "exact_upper_bound": possible_multipliers * shell_class_capacity,
    }


def audit_scale(Q: int, H: int) -> dict[str, object]:
    require(4 * Q < H < Q * Q, "multi-wrap physical regime")
    shell = primes_in_shell(Q)
    minimum_h = ceil_div(H, 2 * Q)
    maximum_multiplicity = 0
    maximum_exact_bound = 0
    witness: dict[str, object] | None = None
    bucket_count = 0
    for h in range(minimum_h, Q + 1):
        buckets = bucket_rows(Q, H, h)
        for a, rows in buckets.items():
            bucket_count += 1
            require(all(len(ms) == 1 for ms in rows.values()), "row injectivity")
            multiplicity = len(rows)
            bound = gcd_fiber_bound(Q, H, h, a)
            require(multiplicity <= bound["exact_upper_bound"], "gcd-fiber bound")
            two_term_bound = Fraction(4 * Q * Q, H) + Fraction(4 * h * Q, bound["g"] * H)
            require(Fraction(bound["exact_upper_bound"], 1) <= two_term_bound, "two-term envelope")
            require(Fraction(bound["exact_upper_bound"], 1) <= Fraction(8 * Q * Q, H), "global envelope")
            maximum_exact_bound = max(maximum_exact_bound, bound["exact_upper_bound"])
            if multiplicity > maximum_multiplicity:
                maximum_multiplicity = multiplicity
                witness = {
                    "h": h,
                    "a": a,
                    "g": bound["g"],
                    "rows": [[q, list(ms)] for q, ms in sorted(rows.items())],
                }
    return {
        "Q": Q,
        "H": H,
        "shell_primes": len(shell),
        "active_h_min": minimum_h,
        "active_h_max": Q,
        "bucket_count": bucket_count,
        "maximum_multiplicity": maximum_multiplicity,
        "maximum_exact_bound": maximum_exact_bound,
        "global_bound": str(Fraction(8 * Q * Q, H)),
        "witness": witness,
    }


def triple_collision_fixture() -> dict[str, object]:
    Q, H, U, h = 101, 8830, 99, 80
    require(H**32 <= Q**63 < (H + 1) ** 32, "V59-shaped H floor")
    require(U**400 <= Q**399 < (U + 1) ** 400 and h <= U, "V59-shaped U floor")
    selected = (113, 127, 193)
    supports = {q: row_support(Q, H, h, q) for q in selected}
    require(all(support == (17, 63) for support in supports.values()), "triple support")
    buckets = bucket_rows(Q, H, h)
    require(set(selected).issubset(buckets[63]), "triple bucket")
    diagonal_energy = sum(len(supports[q]) for q in selected)
    combined: dict[int, int] = {}
    for q in selected:
        for a in supports[q]:
            combined[a] = combined.get(a, 0) + 1
    combined_energy = sum(value * value for value in combined.values())
    ratio = Fraction(combined_energy, diagonal_energy)
    require((diagonal_energy, combined_energy, ratio) == (6, 18, 3), "triple Bessel ratio")
    return {
        "Q": Q,
        "H": H,
        "U": U,
        "h": h,
        "Q2_over_H": str(Fraction(Q * Q, H)),
        "selected_rows": list(selected),
        "supports": {str(q): list(supports[q]) for q in selected},
        "bucket_63": [[q, list(buckets[63][q])] for q in selected],
        "diagonal_energy": diagonal_energy,
        "combined_energy": combined_energy,
        "bessel_ratio": str(ratio),
    }


def gcd_adversary_fixture() -> dict[str, object]:
    Q, H, h, a = 16, 65, 8, 6
    rows = bucket_rows(Q, H, h)[a]
    correct = gcd_fiber_bound(Q, H, h, a)
    naive_period_h = 2 * (correct["global_cutoff"] // correct["g"]) * ceil_div(Q, h)
    require(len(rows) == 5, "nonprimitive bucket multiplicity")
    require(naive_period_h == 4 < len(rows) <= correct["exact_upper_bound"] == 8, "gcd reduction necessity")
    return {
        "Q": Q,
        "H": H,
        "h": h,
        "a": a,
        "g": correct["g"],
        "rows": [[q, list(ms)] for q, ms in sorted(rows.items())],
        "actual_multiplicity": len(rows),
        "naive_modulus_h_bound": naive_period_h,
        "gcd_reduced_bound": correct["exact_upper_bound"],
    }


def exponent_ledger() -> dict[str, str]:
    q = Fraction(1, 3)
    height = Fraction(21, 32)
    upper_h = Fraction(133, 400)
    ledger = {
        "Q": q,
        "H": height,
        "U": upper_h,
        "Q2_over_H": 2 * q - height,
        "H_over_Q": height - q,
        "U_below_Q": q - upper_h,
        "maximum_depth": upper_h + q - height,
    }
    require(ledger["Q2_over_H"] == Fraction(1, 96), "multiplicity exponent")
    require(ledger["H_over_Q"] == Fraction(31, 96), "height ratio")
    require(ledger["U_below_Q"] == Fraction(1, 1200), "h below Q")
    require(ledger["maximum_depth"] == Fraction(23, 2400), "depth range")
    return {key: str(value) for key, value in ledger.items()}


def build_certificate() -> dict[str, object]:
    scales = [audit_scale(Q, H) for Q, H in ((11, 45), (17, 70), (25, 104), (53, 220), (101, 8830))]
    records = {
        "exponents": exponent_ledger(),
        "triple_collision": triple_collision_fixture(),
        "gcd_adversary": gcd_adversary_fixture(),
        "census": scales,
    }
    digest = hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return {
        "schema": "tpc236-physical-multiwrap-collision-envelope-v1",
        "status": "PASS",
        "claim_level": "PROVED_STRUCTURAL_L1",
        "theorem": {
            "exact_bucket_bound": "2 floor(floor(2hQ/H)/g) ceil(Qg/h), g=gcd(a,h)",
            "global_bucket_bound": "8Q^2/H",
            "v59_refined_bound": "4x^(1/96)+4x^(23/2400)",
            "fixed_h_bessel": "unnormalized source-valid weighted envelope",
            "v59_toll": "(4+o(1))x^(1/96)",
            "multiplicity_two": "REFUTED_SCOPED_BY_EXACT_TRIPLE_COLLISION",
        },
        "finite_reproduction": {"records": records, "digest": digest},
        "source_lock": {
            "divisor_weight_C_h": "PRESERVED_EXPLICITLY",
            "full_h_direct_sum": "PRESERVED_PRE_REASSEMBLY",
            "common_packet_transform": "PRESERVED_WITH_OPERATOR_NORM",
            "row_unit_normalization": "NOT_USED",
        },
        "firewall": {
            "cross_h_rational_frequency_reassembly": "OPEN",
            "C_h_weighted_cancellation": "OPEN",
            "benchmark_margin": "ZERO_ONLY_IF_MULTIPLICATIVE_AT_ENERGY_LEVEL",
            "arithmetic_advance": "NO",
            "arithmetic_cancellation": "NONE",
            "fixed_atom_credit": 0,
            "L2": "NONE",
            "full_gate_b": "OPEN",
        },
    }
