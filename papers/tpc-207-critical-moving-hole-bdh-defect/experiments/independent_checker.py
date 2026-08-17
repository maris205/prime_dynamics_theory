#!/usr/bin/env python3
"""Independent exact checker for TPC-207.

This file intentionally imports neither code/moving_hole.py nor
run_certificate.py.  It reconstructs the core formulas with a separate
implementation and validates the canonical certificate's claim firewall.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results" / "certificate.json"


def plus(a, b):
    return (a[0] + b[0], a[1] + b[1])


def minus(a, b):
    return (a[0] - b[0], a[1] - b[1])


def times(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def conjugate(a):
    return (a[0], -a[1])


def scale(c, a):
    return (c * a[0], c * a[1])


def square(a):
    return a[0] * a[0] + a[1] * a[1]


def total(values):
    answer = (F(0), F(0))
    for value in values:
        answer = plus(answer, value)
    return answer


def average(values):
    return scale(F(1, len(values)), total(values))


def variance_without(values, hole):
    kept = [value for index, value in enumerate(values) if index != hole]
    center = average(kept)
    return sum((square(minus(value, center)) for value in kept), F(0))


def all_variance(values):
    center = average(values)
    return sum((square(minus(value, center)) for value in values), F(0))


def row_energy(residue_coefficients):
    return total(residue_coefficients), sum((square(value) for value in residue_coefficients), F(0))


def remainder(residues, hole):
    q = len(residues)
    rows_and_energy = [row_energy(residue) for residue in residues]
    rows = [item[0] for item in rows_and_energy]
    energies = [item[1] for item in rows_and_energy]
    return variance_without(rows, hole) - F(q - 2, q - 1) * sum(
        (energies[index] for index in range(q) if index != hole), F(0)
    )


def packet(beta, omega, phase):
    result = []
    for left, right in zip(beta, omega):
        width = max(len(left), len(right))
        result.append([
            plus(
                left[index] if index < len(left) else (F(0), F(0)),
                times(phase, right[index] if index < len(right) else (F(0), F(0))),
            )
            for index in range(width)
        ])
    return result


def polarized_lhs(beta, omega, hole):
    phases = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))]
    answer = (F(0), F(0))
    for phase in phases:
        residues = packet(beta, omega, phase)
        answer = plus(answer, scale(remainder(residues, hole) - remainder(residues, 0), phase))
    return scale(F(1, 4), answer)


def polarized_rhs(beta, omega, hole):
    q = len(beta)
    beta_rows = [total(row) for row in beta]
    omega_rows = [total(row) for row in omega]
    beta_bar = average(beta_rows)
    omega_bar = average(omega_rows)
    leverage = minus(
        times(minus(beta_rows[0], beta_bar), conjugate(minus(omega_rows[0], omega_bar))),
        times(minus(beta_rows[hole], beta_bar), conjugate(minus(omega_rows[hole], omega_bar))),
    )
    cross = []
    for left, right in zip(beta, omega):
        width = max(len(left), len(right))
        cross.append(total(
            times(
                left[index] if index < len(left) else (F(0), F(0)),
                conjugate(right[index] if index < len(right) else (F(0), F(0))),
            )
            for index in range(width)
        ))
    return plus(
        scale(F(q, q - 1), leverage),
        scale(F(q - 2, q - 1), minus(cross[hole], cross[0])),
    )


def parse_fraction(text):
    return F(text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()

    if not CERTIFICATE.is_file():
        raise SystemExit("TPC207_INDEPENDENT_CHECK=FAIL missing certificate")
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"), parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    if data.get("schema") != "TPC207_MOVING_HOLE_CERTIFICATE_V1":
        raise AssertionError("schema")

    for q in (2, 3, 5, 7):
        values = [(F(r + 1), F(1 if r % 2 == 0 else -1)) for r in range(q)]
        center = average(values)
        for hole in range(q):
            lhs = variance_without(values, hole)
            rhs = all_variance(values) - F(q, q - 1) * square(minus(values[hole], center))
            if lhs != rhs:
                raise AssertionError((q, hole, "moving-hole"))
            recorded = data["moving_hole_identity"][str(q)][hole]
            if parse_fraction(recorded["lhs"]) != lhs or parse_fraction(recorded["rhs"]) != rhs:
                raise AssertionError((q, hole, "record"))
        expected_square = F(q * (q - 2), (q - 1) ** 2)
        if parse_fraction(data["spectrum_square"][str(q)]["nonzero_eigenvalue_square"]) != expected_square:
            raise AssertionError((q, "spectrum"))
        for fixture in data["translation_sign"]["fixtures"][str(q)]:
            if fixture["moving_hole"] != (-fixture["s"]) % q:
                raise AssertionError((q, "translation"))

    g = lambda a, b=0: (F(a), F(b))
    beta_all = [
        [g(1, 1), g(2, -1)], [g(-1, 2)], [g(3), g(0, 1)],
        [g(2, -2)], [g(-2, 1), g(1)], [g(1, -3)], [g(0, 2), g(2, 2)],
    ]
    omega_all = [
        [g(2), g(-1, 1)], [g(1, -2), g(1)], [g(0, 1)],
        [g(-2, -1), g(1, 1)], [g(3, 2)], [g(-1), g(0, -1)], [g(2, -2)],
    ]
    for q in (2, 3, 5, 7):
        beta = beta_all[:q]
        omega = omega_all[:q]
        for hole in range(q):
            if polarized_lhs(beta, omega, hole) != polarized_rhs(beta, omega, hole):
                raise AssertionError((q, hole, "polarization"))

    fixture = [[g(5), g(5)], [g(1)], [], [], []]
    if remainder(fixture, 0) != 0 or remainder(fixture, 1) != F(75, 2):
        raise AssertionError("q5 fixture")
    if F(53, 32) != F(5, 3) - F(1, 96) or not F(1, 400) < F(1, 96):
        raise AssertionError("exponent ledger")

    firewall = data["claim_firewall"]
    expected = {
        "V60_ROUTE_ADVANCE": "YES",
        "V60_TRANSLATION_SUBGATE_DELTA": "1_OVER_96_PROVED",
        "V60_TRANSLATION_SUBGATE_STRICT_1_OVER_400": "PAID",
        "V60_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID",
        "V60_ARITHMETIC_ADVANCE": "NO",
        "V60_FIXED_ATOM_CREDIT": 0,
        "V60_L2": "NONE",
        "TPC_207_TRIGGER": True,
        "twin_prime_theorem": False,
    }
    for key, value in expected.items():
        if firewall.get(key) != value or type(firewall.get(key)) is not type(value):
            raise AssertionError((key, firewall.get(key), value))

    print("TPC207_INDEPENDENT_CHECK=PASS")
    print("implementation=independent_exact_gaussian_rational")
    print("q_rows=2,3,5,7")
    print("claim_firewall=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
