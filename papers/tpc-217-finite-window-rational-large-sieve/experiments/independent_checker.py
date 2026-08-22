#!/usr/bin/env python3
"""Independent finite-window and regrouping checker for TPC-217."""

from __future__ import annotations

import argparse
import cmath
import json
import math
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results/certificate.json"
Q_VALUES = (11, 13, 17)
HEIGHT = 40
LOWER = 2
UPPER = 35


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate key: {key}")
        result[key] = value
    return result


def mobius(value: int) -> int:
    remaining = value
    parity = 0
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            if remaining % prime == 0:
                return 0
            parity += 1
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        parity += 1
    return -1 if parity % 2 else 1


def squarefree(value: int) -> bool:
    return mobius(value) != 0


def family() -> tuple[int, ...]:
    return tuple(
        value
        for value in range(LOWER + 1, UPPER + 1)
        if squarefree(value) and all(gcd(value, q) == 1 for q in Q_VALUES)
    )


def divisors(value: int) -> tuple[int, ...]:
    return tuple(d for d in range(1, value + 1) if value % d == 0)


def psi(argument: Fraction) -> Fraction:
    return Fraction(1, 1) / (1 + argument * argument) ** 2


def row(divisor: int, q_values: tuple[int, ...] = Q_VALUES, height: int = HEIGHT) -> tuple[Fraction, ...]:
    values = [Fraction(0, 1) for _ in range(divisor)]
    for q in q_values:
        require(gcd(q, divisor) == 1, "unit condition")
        cutoff = divisor * q // height
        inverse = pow(q, -1, divisor) if divisor > 1 else 0
        for m in range(-cutoff, cutoff + 1):
            if m:
                residue = (m * inverse) % divisor if divisor > 1 else 0
                values[residue] += psi(Fraction(height * m, divisor * q))
    return tuple(values)


def reduced(family_values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted({h for d in family_values for h in divisors(d)}))


def coefficient(value: int) -> float:
    return mobius(value) * math.log(value) / value


def cluster_coeff(family_values: tuple[int, ...], denominator: int) -> float:
    return sum(coefficient(d) for d in family_values if d % denominator == 0)


def primitive(denominator: int) -> tuple[int, ...]:
    return tuple(a for a in range(denominator) if gcd(a, denominator) == 1)


def direct_at(integer: int, family_values: tuple[int, ...]) -> complex:
    total = 0j
    for d in family_values:
        values = row(d)
        for r, value in enumerate(values):
            total += coefficient(d) * float(value) * cmath.exp(2j * math.pi * integer * r / d)
    return total


def reduced_at(integer: int, family_values: tuple[int, ...]) -> complex:
    total = 0j
    for h in reduced(family_values):
        values = row(h)
        scale = cluster_coeff(family_values, h)
        for a in primitive(h):
            total += scale * float(values[a]) * cmath.exp(2j * math.pi * integer * a / h)
    return total


def norm_energy(family_values: tuple[int, ...]) -> float:
    return sum(
        (cluster_coeff(family_values, h) * float(row(h)[a])) ** 2
        for h in reduced(family_values)
        for a in primitive(h)
    )


def check_certificate(data: dict[str, object]) -> None:
    require(data["schema"] == "TPC217_FINITE_WINDOW_RATIONAL_LARGE_SIEVE_CERTIFICATE_V1", "schema")
    require(data["classification"] == "PROVED_STRUCTURAL_L1_FINITE_WINDOW_ATTACHMENT", "classification")
    require(
        data["source_exponents"] == {
            "H": "21/32",
            "Q": "1/3",
            "U": "133/400",
            "Y0": "31/96",
            "Q3_over_H": "11/32",
            "U2_over_x": "-67/200",
        },
        "source exponents",
    )
    require(
        data["source_relations"] == {
            "physical_interval": "I_x=(x/2,x] intersect Z",
            "reduced_frequency": "a/h with 1<=h<=U and gcd(a,h)=1",
            "cluster_coefficient": "C_h=sum_(d in D_x,h|d)c_d",
            "finite_window_bound": "E_I<=(N+U^2)*sum_(h,a)|C_h B_h(a)|^2",
            "coefficient_majorant": "sum_(h,a)|C_h B_h(a)|^2<=A_x*E_direct/L",
        },
        "source relations",
    )
    require(
        data["theorem"] == {
            "reduced_frequency_regrouping": "PROVED_EXACT",
            "frequency_spacing": "delta>=1/U^2",
            "additive_large_sieve": "PROVED_STANDARD_FAREY_LARGE_SIEVE",
            "finite_window_attachment": "PROVED_X_11_OVER_32_LOG_FIVE_NORMALIZED",
            "unnormalized_window_exponent": "43/32",
            "window_loss": "1+U^2/N",
            "prime_count_used": False,
            "mobius_cancellation_used": False,
            "status": "PROVED_STRUCTURAL_L1",
        },
        "theorem metadata",
    )
    firewall = data["claim_firewall"]
    require(
        firewall == {
            "route_a": "NOT_APPLICABLE",
            "route_b_structural_threshold_a": "PASS",
            "reduced_frequency_regrouping": "PROVED_EXACT",
            "finite_window_large_sieve": "PROVED_STANDARD",
            "finite_window_attachment": "PROVED_X_11_OVER_32_LOG_FIVE_NORMALIZED",
            "normalized_exponent": "11/32",
            "finite_window_off_frequency_gram": "CONTROLLED_BY_LARGE_SIEVE",
            "prime_shell_reassembly": "OPEN",
            "four_packet_signed_reassembly": "OPEN",
            "arithmetic_cancellation": "NONE",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b": "OPEN",
            "full_gate_b_strict_1_over_400": "UNPAID",
            "finite_window_orthogonality": "REFUTED_SCOPED",
        },
        "claim firewall",
    )

    fixture = data["finite_fixture"]
    values = family()
    reduced_values = reduced(values)
    require(fixture["q_values"] == list(Q_VALUES), "q values")
    require(fixture["H"] == HEIGHT and fixture["Y0"] == LOWER and fixture["U"] == UPPER, "scales")
    require(fixture["divisors"] == list(values), "divisor family")
    require(fixture["reduced_denominators"] == list(reduced_values), "reduced denominators")
    require(fixture["numeric_classification"] == "NUMERICAL_OBSERVATION", "fixture class")
    expected_energy = norm_energy(values)
    require(fixture["cluster_energy"] == format(expected_energy, ".17g"), "cluster energy")

    for record in fixture["intervals"]:
        start = record["start"]
        length = record["length"]
        direct = sum(abs(direct_at(start + j, values)) ** 2 for j in range(length))
        regrouped = sum(abs(reduced_at(start + j, values)) ** 2 for j in range(length))
        rhs = (length + UPPER * UPPER) * expected_energy
        error = max(abs(direct_at(start + j, values) - reduced_at(start + j, values)) for j in range(length))
        require(record["direct_window_energy"] == format(direct, ".17g"), f"direct window {start}")
        require(record["regrouped_window_energy"] == format(regrouped, ".17g"), f"regrouped window {start}")
        require(record["large_sieve_rhs"] == format(rhs, ".17g"), f"large sieve rhs {start}")
        require(record["energy_to_large_sieve_ratio"] == format(direct / rhs, ".17g"), f"ratio {start}")
        require(record["pointwise_regrouping_error"] == format(error, ".17g"), f"pointwise error {start}")
        require(error < 1e-11, f"regrouping error {start}")
        require(direct <= rhs * (1 + 1e-12), f"large sieve fixture {start}")

    adversary = data["frequency_crowding_adversary"]
    require(adversary["q_values"] == [101, 131, 151, 181], "adversary q values")
    require(adversary["H"] == 500 and adversary["d"] == 5 and adversary["cutoff"] == 1, "adversary scales")
    adversary_row = row(5, (101, 131, 151, 181), 500)
    support = [index for index, value in enumerate(adversary_row) if value]
    diagonal = sum(float(adversary_row[index]) ** 2 for index in support)
    one_point = sum(float(adversary_row[index]) for index in support) ** 2
    require(adversary["support"] == support, "adversary support")
    require(adversary["diagonal_energy"] == format(diagonal, ".17g"), "adversary diagonal")
    require(adversary["one_point_window_energy"] == format(one_point, ".17g"), "adversary window")
    require(adversary["window_to_diagonal_ratio"] == format(one_point / diagonal, ".17g"), "adversary ratio")
    require(adversary["classification"] == "FINITE_STRUCTURAL_ADVERSARY", "adversary class")
    require(support == [1, 4] and abs(one_point / diagonal - 2.0) < 1e-14, "crowding not present")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        require(CERTIFICATE.is_file(), "certificate missing")
        data = json.loads(CERTIFICATE.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        require(type(data) is dict, "certificate object")
        check_certificate(data)
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError, ZeroDivisionError) as error:
        print(f"TPC217_INDEPENDENT_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    fixture = data["finite_fixture"]
    adversary = data["frequency_crowding_adversary"]
    print("TPC217_INDEPENDENT_CHECK=PASS")
    print("active_divisors=", len(fixture["divisors"]))
    print("reduced_denominators=", len(fixture["reduced_denominators"]))
    print("intervals=", len(fixture["intervals"]))
    print("crowding_ratio=", adversary["window_to_diagonal_ratio"])
    print("normalized_exponent=11/32")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
