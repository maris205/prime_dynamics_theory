#!/usr/bin/env python3
"""Independent reconstruction of the TPC-237 theorem ledger and fixture."""

from __future__ import annotations

import json
from fractions import Fraction
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise SystemExit("TPC237_INDEPENDENT_CHECK=FAIL: " + message)


def prime(n: int) -> bool:
    require(type(n) is int, "prime input type")
    return n >= 2 and all(n % p for p in range(2, int(n**0.5) + 1))


def mu(n: int) -> int:
    require(type(n) is int and n >= 1, "Mobius input")
    answer = 1
    remaining = n
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            remaining //= divisor
            answer = -answer
            if remaining % divisor == 0:
                return 0
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    return -answer if remaining > 1 else answer


def reconstruct_row(Q: int, H: int, h: int, q: int, signed: bool) -> dict[int, int]:
    require(type(signed) is bool and prime(q) and Q < q <= 2 * Q and gcd(q, h) == 1,
            "row source lock")
    inverse = pow(q, -1, h)
    cutoff = h * q // H
    row: dict[int, int] = {}
    for m in range(-cutoff, cutoff + 1):
        if m:
            a = m * inverse % h
            require(a not in row, "internal injectivity")
            row[a] = (1 if m > 0 else -1) if signed else 1
    return row


def main() -> None:
    stored = json.loads((ROOT / "results" / "certificate.json").read_text(encoding="utf-8"))
    require(type(stored) is dict and stored["status"] == "PASS", "stored status")

    q_exp = Fraction(1, 3)
    h_exp = Fraction(21, 32)
    u_exp = Fraction(133, 400)
    ledger = {
        "Q2_over_H": 2 * q_exp - h_exp,
        "UQ_over_H": u_exp + q_exp - h_exp,
        "main_product": 2 * (2 * q_exp - h_exp),
        "secondary_product": 3 * q_exp + u_exp - 2 * h_exp,
        "window_U2_over_x": 2 * u_exp - 1,
        "unnormalized_main": 1 + 2 * (2 * q_exp - h_exp),
    }
    expected_ledger = {
        "Q2_over_H": Fraction(1, 96),
        "UQ_over_H": Fraction(23, 2400),
        "main_product": Fraction(1, 48),
        "secondary_product": Fraction(1, 50),
        "window_U2_over_x": Fraction(-67, 200),
        "unnormalized_main": Fraction(49, 48),
    }
    require(ledger == expected_ledger, "independent exponent ledger")

    Q, H, U, h = 101, 8830, 99, 82
    selected = (109, 137, 191)
    require(H**32 <= Q**63 < (H + 1) ** 32, "H floor")
    require(U**400 <= Q**399 < (U + 1) ** 400, "U floor")
    require(mu(h) == 1 and all(prime(q) for q in selected), "squarefree source and shell")
    band_terms = [(d, mu(d)) for d in range(1, U + 1) if 4 * Q * d > H and mu(d) and d % h == 0]
    C_h = sum((Fraction(sign, d) for d, sign in band_terms), Fraction(0, 1))
    require(band_terms == [(82, 1)] and C_h == Fraction(1, 82), "rational cluster reproduction")

    direct = Fraction(0, 1)
    collapsed: dict[tuple[bool, int], Fraction] = {}
    row_dump: dict[str, dict[str, dict[str, int]]] = {"constant": {}, "signed_multiplier": {}}
    for signed in (False, True):
        packet = "signed_multiplier" if signed else "constant"
        for q in selected:
            row = reconstruct_row(Q, H, h, q, signed)
            require(set(row) == {3, 79} and all(gcd(a, h) == 1 for a in row), "primitive aligned row")
            row_dump[packet][str(q)] = {str(a): value for a, value in sorted(row.items())}
            for a, value in row.items():
                coefficient = C_h * value
                direct += coefficient * coefficient
                key = (signed, a)
                collapsed[key] = collapsed.get(key, Fraction(0, 1)) + coefficient
    coherent = sum((value * value for value in collapsed.values()), Fraction(0, 1))
    require(direct == Fraction(3, 1681), "direct energy")
    require(coherent == Fraction(5, 1681), "coherent packet trace")
    require(coherent / direct == Fraction(5, 3), "trace collision ratio")
    require(h * coherent == Fraction(10, 41), "complete-period energy")

    R_star = Fraction(4 * Q * Q, H) + Fraction(4 * U * Q, H)
    factor = h - 1 + U * U
    require(h * coherent <= factor * coherent <= factor * R_star * direct, "composed inequality")

    fixture = stored["finite_reproduction"]["records"]["physical_window_fixture"]
    require(fixture["rows"] == row_dump, "stored row reconstruction")
    require(fixture["rational_C_h"] == str(C_h), "stored C_h")
    require(fixture["direct_packet_energy"] == str(direct), "stored direct energy")
    require(fixture["collapsed_packet_trace"] == str(coherent), "stored collapsed energy")
    require(stored["normalization_loss_ledger"]["hidden_P_factor"] == "NONE", "hidden P mutation")
    require(stored["normalization_loss_ledger"]["frequency_representatives"] == "PRIMITIVE_ONLY",
            "primitive interface")
    print("TPC237_INDEPENDENT_CHECK=PASS")
    print("normalized_exponents=1/48+1/50")
    print("source_active_h82_trace_ratio=5/3")


if __name__ == "__main__":
    main()
