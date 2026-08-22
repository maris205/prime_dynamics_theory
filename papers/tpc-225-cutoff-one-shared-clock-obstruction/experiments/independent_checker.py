#!/usr/bin/env python3
"""Independent replay of the TPC-225 cutoff-one identities.

This file deliberately does not import the producer.  It rebuilds the prime
shell, inverse-residue rows, profile fixtures, and all four energies from
scratch using exact rational arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
import json
from math import gcd
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results" / "certificate.json"
J = 4
SLOPES = (Fraction(0), Fraction(1, 10), Fraction(-1, 10), Fraction(1, 5))


class IndependentFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise IndependentFailure(message)


def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise IndependentFailure(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return n == d
        d += 1
    return True


def shell(Q: int) -> tuple[int, ...]:
    return tuple(q for q in range(Q + 1, 2 * Q + 1) if is_prime(q))


def add(v: dict[tuple[int, int], Fraction], key: tuple[int, int], value: Fraction) -> None:
    v[key] = v.get(key, Fraction(0)) + value
    if v[key] == 0:
        del v[key]


def sum_vectors(vectors: list[dict[tuple[int, int], Fraction]]) -> dict[tuple[int, int], Fraction]:
    result: dict[tuple[int, int], Fraction] = {}
    for vector in vectors:
        for key, value in vector.items():
            add(result, key, value)
    return result


def norm(v: dict[tuple[int, int], Fraction]) -> Fraction:
    return sum((x * x for x in v.values()), Fraction(0))


def values(Q: int, q: int, packet: int, mode: str) -> tuple[Fraction, Fraction]:
    if mode == "affine":
        t = Fraction(Q, q)
        return 1 + SLOPES[packet] * t, 1 - SLOPES[packet] * t
    if mode == "aligned":
        return Fraction(1), Fraction(1)
    if mode == "balanced":
        return (
            (Fraction(1), Fraction(-1), Fraction(0), Fraction(0))[packet],
            (Fraction(0), Fraction(0), Fraction(1), Fraction(-1))[packet],
        )
    raise IndependentFailure("unknown mode")


def audit(Q: int, mode: str) -> tuple[Fraction, Fraction, Fraction, Fraction, set[int], int]:
    H = 4 * Q * Q
    h = 4 * Q
    qs = shell(Q)
    rows: dict[tuple[int, int], dict[tuple[int, int], Fraction]] = {}
    for q in qs:
        require(gcd(q, h) == 1, "non-unit prime")
        inverse = pow(q, -1, h)
        require(h * q // H == 1, "cutoff-one failure")
        for packet in range(J):
            plus, minus = values(Q, q, packet, mode)
            row: dict[tuple[int, int], Fraction] = {}
            add(row, (h, inverse), plus / h)
            add(row, (h, (-inverse) % h), minus / h)
            rows[q, packet] = row
    supports = {
        q: {
            key[1]
            for packet in range(J)
            for key in rows[q, packet]
        }
        for q in qs
    }
    for index, q1 in enumerate(qs):
        for q2 in qs[index + 1 :]:
            require(supports[q1].isdisjoint(supports[q2]), "support collision")
    by_packet = [sum_vectors([rows[q, packet] for q in qs]) for packet in range(J)]
    by_prime = [sum_vectors([rows[q, packet] for packet in range(J)]) for q in qs]
    diagonal = sum((norm(row) for row in rows.values()), Fraction(0))
    ap = sum((norm(row) for row in by_packet), Fraction(0))
    polarized = sum((norm(row) for row in by_prime), Fraction(0))
    full = norm(sum_vectors(list(rows.values())))
    return diagonal, ap, polarized, full, set().union(*supports.values()), len(qs)


def main() -> int:
    try:
        data = json.loads(CERTIFICATE.read_text(), object_pairs_hook=no_duplicates)
        require(data["schema"] == "tpc225-cutoff-one-shared-clock-obstruction-v1", "schema")
        require(data["status"] == "PASS", "certificate status")
        require(data["claim_level"] == "PROVED_STRUCTURAL_L1", "claim level")
        require(data["author"] == "Liang Wang", "author")
        require(data["affiliation"] == "Huazhong University of Science and Technology", "affiliation")
        theorem = data["theorem"]
        require(theorem["cutoff"] == "floor(hq/H)=1", "cutoff theorem")
        require(theorem["support_disjointness"] == "PROVED_EXACT", "support theorem")
        require(theorem["ap_equals_diagonal"] == "PROVED_EXACT", "AP theorem")
        require(theorem["all_equals_polarized"] == "PROVED_EXACT", "full theorem")
        require(theorem["positive_ap_saving_on_clock"] == "REFUTED_SCOPED", "AP obstruction")
        checks = data["checks"]
        require(all(type(value) is bool and value for value in checks.values()), "check flags")
        affine = data["affine_clock"]["records"]
        aligned = data["boundary_profiles"]["aligned_records"]
        balanced = data["boundary_profiles"]["balanced_records"]
        require(len(affine) == 9 and len(aligned) == 7 and len(balanced) == 7, "record counts")
        for record in affine + aligned + balanced:
            Q = record["Q"]
            mode = record["mode"]
            diagonal, ap, polarized, full, support, count = audit(Q, mode)
            require(str(diagonal) == record["E_diag"], f"diagonal replay Q={Q}")
            require(str(ap) == record["E_AP"], f"AP replay Q={Q}")
            require(str(polarized) == record["E_pol"], f"polar replay Q={Q}")
            require(str(full) == record["E_all"], f"full replay Q={Q}")
            require(ap == diagonal and full == polarized, f"identity Q={Q}")
            require(count == record["prime_count"], f"prime count Q={Q}")
            require(len(support) == 2 * count, f"support count Q={Q}")
        for Q in range(3, 100):
            diagonal, ap, polarized, full, _, _ = audit(Q, "affine")
            require(ap == diagonal and full == polarized, f"boundary identity Q={Q}")
        for record in balanced:
            require(record["E_pol"] == "0", "balanced cancellation replay")
            require(record["E_diag"] != "0", "balanced diagonal replay")
        print("TPC225_INDEPENDENT_CHECK=PASS")
        print("affine_scales=9")
        print("boundary_profile_scales=14")
        print("boundary_Q_range=3..99")
        print("ap_identity=E_AP_EQUALS_E_DIAG")
        print("full_identity=E_ALL_EQUALS_E_POL")
        print("arithmetic_advance=NO")
        return 0
    except (IndependentFailure, OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"TPC225_INDEPENDENT_CHECK=FAIL: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
