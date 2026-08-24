#!/usr/bin/env python3
"""Independent exact replay for TPC-226.

This checker intentionally does not import the producer module.
"""

from __future__ import annotations

import json
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/certificate.json"
J = 4
SLOPES = (Fraction(0), Fraction(1, 10), Fraction(-1, 10), Fraction(1, 5))
SIGNS = (Fraction(1), Fraction(-1), Fraction(1), Fraction(-1))


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise CheckFailure(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def prime(n: int) -> bool:
    if type(n) is not int or n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return n == divisor
        divisor += 1
    return True


def shell(Q: int) -> tuple[int, ...]:
    return tuple(q for q in range(Q + 1, 2 * Q) if prime(q))


def multipliers(Q: int, L: int, q: int) -> tuple[int, ...]:
    h = 4 * L * Q
    cutoff = L * q // Q
    return tuple(m for m in range(-cutoff, cutoff + 1) if m and gcd(abs(m), h) == 1)


def supports(Q: int, L: int) -> dict[int, dict[int, int]]:
    h = 4 * L * Q
    result: dict[int, dict[int, int]] = {}
    for q in shell(Q):
        need(gcd(q, h) == 1, "nonunit prime")
        inverse = pow(q, -1, h)
        row: dict[int, int] = {}
        for m in multipliers(Q, L, q):
            residue = m * inverse % h
            need(residue not in row, "internal folding")
            row[residue] = m
        result[q] = row
    return result


def collisions(Q: int, L: int) -> dict[tuple[int, int], set[tuple[int, int, int]]]:
    rows = supports(Q, L)
    qs = sorted(rows)
    found: dict[tuple[int, int], set[tuple[int, int, int]]] = {}
    for index, q1 in enumerate(qs):
        for q2 in qs[index + 1 :]:
            for residue in set(rows[q1]).intersection(rows[q2]):
                found.setdefault((q1, q2), set()).add(
                    (rows[q1][residue], rows[q2][residue], residue)
                )
    return found


def resonances(Q: int) -> tuple[tuple[int, int], ...]:
    h = 16 * Q
    qs = set(shell(Q))
    result = []
    for p in sorted(qs):
        numerator = 16 * Q - 7 * p
        if numerator <= 0 or numerator % 3:
            continue
        r = numerator // 3
        if r in qs and p < r and gcd(21, h) == 1:
            if 3 in multipliers(Q, 4, p) and 7 in multipliers(Q, 4, r):
                result.append((p, r))
    return tuple(result)


def check_geometry(Q: int, L: int) -> int:
    found = collisions(Q, L)
    if L <= 3:
        need(not found, f"low-dilation collision Q={Q}, L={L}")
        return 0
    expected = resonances(Q)
    need(set(found) == set(expected), f"resonance pair mismatch Q={Q}")
    h = 16 * Q
    for p, r in expected:
        ip = pow(p, -1, h)
        ir = pow(r, -1, h)
        target = {
            (3, -7, 3 * ip % h),
            (-3, 7, -3 * ip % h),
        }
        need(found[p, r] == target, f"resonance multiplier mismatch Q={Q}")
        need(-7 * ir % h == 3 * ip % h, "positive residue mismatch")
        need(7 * ir % h == -3 * ip % h, "negative residue mismatch")
    return len(expected)


def profile(mode: str, j: int, t: Fraction) -> Fraction:
    if mode == "aligned":
        return Fraction(1)
    if mode == "affine":
        return Fraction(1) + SLOPES[j] * t
    if mode == "balanced_sign":
        need(t != 0, "sign profile sampled at zero")
        return SIGNS[j] if t > 0 else -SIGNS[j]
    raise CheckFailure("unknown profile")


def add(target: dict[int, Fraction], source: dict[int, Fraction]) -> None:
    for residue, value in source.items():
        target[residue] = target.get(residue, Fraction(0)) + value
        if target[residue] == 0:
            del target[residue]


def norm(row: dict[int, Fraction]) -> Fraction:
    return sum((value * value for value in row.values()), Fraction(0))


def energy_values(Q: int, mode: str) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    L = 4
    h = 16 * Q
    rows: dict[tuple[int, int], dict[int, Fraction]] = {}
    for q in shell(Q):
        inverse = pow(q, -1, h)
        for j in range(J):
            row: dict[int, Fraction] = {}
            for m in multipliers(Q, L, q):
                t = Fraction(m * Q, L * q)
                need(abs(t) <= 1, "profile interval")
                residue = m * inverse % h
                row[residue] = profile(mode, j, t) / h
            rows[q, j] = row
    diagonal = sum((norm(row) for row in rows.values()), Fraction(0))
    ap = Fraction(0)
    for j in range(J):
        combined: dict[int, Fraction] = {}
        for q in shell(Q):
            add(combined, rows[q, j])
        ap += norm(combined)
    polarized = Fraction(0)
    for q in shell(Q):
        combined = {}
        for j in range(J):
            add(combined, rows[q, j])
        polarized += norm(combined)
    total: dict[int, Fraction] = {}
    for row in rows.values():
        add(total, row)
    return diagonal, ap, polarized, norm(total)


def text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def ratio(a: Fraction, b: Fraction) -> str:
    return "UNDEFINED" if b == 0 else text(a / b)


def scan() -> dict[str, object]:
    lines = []
    scales = total = maximum = 0
    first = maximum_Q = None
    for Q in range(8, 513):
        for L in (1, 2, 3):
            need(check_geometry(Q, L) == 0, "unexpected low collision")
        pairs = resonances(Q)
        need(check_geometry(Q, 4) == len(pairs), "L4 count")
        encoded = ",".join(f"{p}:{r}" for p, r in pairs) or "-"
        lines.append(f"{Q}|0|0|0|{encoded}")
        if pairs:
            scales += 1
            total += len(pairs)
            if first is None:
                first = Q
            if len(pairs) > maximum:
                maximum = len(pairs)
                maximum_Q = Q
    return {
        "Q_min": 8,
        "Q_max": 512,
        "scales_checked": 505,
        "L1_collision_scales": 0,
        "L2_collision_scales": 0,
        "L3_collision_scales": 0,
        "L4_collision_scales": scales,
        "L4_total_resonances": total,
        "L4_first_collision_Q": first,
        "L4_maximum_resonances": maximum,
        "L4_maximum_Q": maximum_Q,
        "classification_sha256": sha256(("\n".join(lines) + "\n").encode()).hexdigest(),
    }


def check_record(row: dict[str, object]) -> None:
    Q = row["Q"]
    mode = row["mode"]
    need(type(Q) is int and Q >= 8, "record Q type")
    need(type(mode) is str, "record mode type")
    D, A, P, F = energy_values(Q, mode)
    need(row["collision_pairs"] == len(resonances(Q)), "record collision count")
    need(row["shared_coordinates"] == 2 * len(resonances(Q)), "record coordinate count")
    need(row["resonances"] == [[p, r] for p, r in resonances(Q)], "record resonances")
    need(row["E_diag"] == text(D), "record diagonal")
    need(row["E_AP"] == text(A), "record AP")
    need(row["E_pol"] == text(P), "record polarized")
    need(row["E_all"] == text(F), "record full")
    need(row["AP_minus_diag"] == text(A - D), "record correction")
    need(row["AP_over_diag"] == ratio(A, D), "record AP ratio")
    need(row["all_over_pol"] == ratio(F, P), "record full ratio")
    if mode in ("aligned", "affine"):
        need(A > D, "amplification sign")
    else:
        need(A < D and P == 0 and F == 0, "odd sign/cancellation")


def main() -> int:
    try:
        data = json.loads(CERTIFICATE.read_text(), object_pairs_hook=no_duplicates)
        need(data.get("schema") == "tpc226-first-primitive-collision-transition-v1", "schema")
        need(data.get("status") == "PASS", "status")
        need(data.get("claim_level") == "PROVED_STRUCTURAL_L1", "claim level")
        need(data.get("date") == "2026-08-24", "date")
        need(data.get("author") == "Liang Wang", "author")
        need(data.get("affiliation") == "Huazhong University of Science and Technology", "affiliation")
        need(data.get("boundary_scan") == scan(), "boundary scan")
        records = data.get("records")
        need(type(records) is dict and set(records) == {"aligned", "affine", "balanced_sign"}, "record modes")
        need(all(type(rows) is list and len(rows) == 10 for rows in records.values()), "record counts")
        for rows in records.values():
            for row in rows:
                need(type(row) is dict, "record type")
                check_record(row)
        q25 = data.get("Q25_exact")
        need(q25.get("aligned_AP_over_diag") == "15/13", "Q25 aligned")
        need(
            q25.get("affine_AP_over_diag")
            == "14610396266802411880605/12679409642889136447511",
            "Q25 affine",
        )
        need(q25.get("balanced_sign_AP_over_diag") == "11/13", "Q25 sign")
        need(q25.get("balanced_sign_E_pol") == "0", "Q25 polarized")
        need(q25.get("balanced_sign_E_all") == "0", "Q25 full")
        firewall = data.get("firewall")
        need(firewall.get("dilated_clock_family") == "MODELING_CHOICE", "clock firewall")
        need(firewall.get("V46_profile_transfer") == "OPEN", "transfer firewall")
        need(firewall.get("arithmetic_advance") == "NO", "arithmetic firewall")
        need(type(firewall.get("fixed_atom_credit")) is int and firewall.get("fixed_atom_credit") == 0, "atom firewall")
        need(firewall.get("L2") == "NONE", "L2 firewall")
        need(firewall.get("full_gate_b") == "OPEN", "Gate B firewall")
        need(firewall.get("strict_1_over_400") == "UNPAID", "strict firewall")
        flags = data.get("checks")
        need(type(flags) is dict and flags and all(type(v) is bool and v for v in flags.values()), "check flags")
    except (CheckFailure, OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"TPC226_INDEPENDENT_CHECK=FAIL: {error}")
        return 1
    print("TPC226_INDEPENDENT_CHECK=PASS")
    print("classification_scales=505")
    print("profile_records=30")
    print("first_collision_Q=25")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
