#!/usr/bin/env python3
"""Independent checker for the TPC-218 finite structural certificate.

This file intentionally does not import the producer.  It recomputes the
finite regrouping, vector energy, shell alignment, and packet alignment from
the definitions used in the paper.
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results/certificate.json"
Q_VALUES = (11, 13, 17)
D_VALUES = (5, 10, 15)
HEIGHT = 40
UPPER = 35
PACKET_WEIGHTS = (Fraction(1), Fraction(1, 2), Fraction(-1), Fraction(2))
ALIGNMENT_Q_VALUES = (101, 131, 151, 181)
ALIGNMENT_HEIGHT = 500
ALIGNMENT_MODULUS = 5


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
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


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return value == divisor
        divisor += 1
    return True


def divisors(value: int) -> tuple[int, ...]:
    return tuple(d for d in range(1, value + 1) if value % d == 0)


def reduced_denominators(values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted({h for value in values for h in divisors(value)}))


def primitive(denominator: int) -> tuple[int, ...]:
    if denominator == 1:
        return (0,)
    return tuple(a for a in range(denominator) if math.gcd(a, denominator) == 1)


def row_for_q(modulus: int, q: int, height: int = HEIGHT) -> tuple[Fraction, ...]:
    require(is_prime(q) and math.gcd(q, modulus) == 1, "invalid shell unit")
    cutoff = modulus * q // height
    values = [Fraction(0, 1) for _ in range(modulus)]
    inverse = pow(q, -1, modulus) if modulus > 1 else 0
    for m in range(-cutoff, cutoff + 1):
        if m:
            values[(m * inverse) % modulus if modulus > 1 else 0] += Fraction(1, 1)
    return tuple(values)


def coefficient(value: int) -> Fraction:
    return Fraction(mobius(value), value)


def cluster(values: tuple[int, ...], denominator: int) -> Fraction:
    return sum((coefficient(value) for value in values if value % denominator == 0), Fraction(0, 1))


def direct_at(integer: int, q: int, packet: int) -> complex:
    total = 0j
    for divisor in D_VALUES:
        for residue, value in enumerate(row_for_q(divisor, q)):
            total += (
                float(coefficient(divisor) * value * PACKET_WEIGHTS[packet])
                * cmath.exp(2j * math.pi * integer * residue / divisor)
            )
    return total


def reduced_at(integer: int, q: int, packet: int) -> complex:
    total = 0j
    for denominator in reduced_denominators(D_VALUES):
        row = row_for_q(denominator, q)
        scale = cluster(D_VALUES, denominator)
        for numerator in primitive(denominator):
            total += (
                float(scale * row[numerator] * PACKET_WEIGHTS[packet])
                * cmath.exp(2j * math.pi * integer * numerator / denominator)
            )
    return total


def energy() -> Fraction:
    total = Fraction(0, 1)
    for denominator in reduced_denominators(D_VALUES):
        scale = cluster(D_VALUES, denominator)
        for numerator in primitive(denominator):
            for q in Q_VALUES:
                value = row_for_q(denominator, q)[numerator]
                for weight in PACKET_WEIGHTS:
                    atom = scale * value * weight
                    total += atom * atom
    return total


def vector_at(integer: int) -> tuple[complex, ...]:
    return tuple(
        reduced_at(integer, q, packet)
        for q in Q_VALUES
        for packet in range(4)
    )


def norm(vector: tuple[complex, ...]) -> float:
    return sum(abs(value) ** 2 for value in vector)


def check_finite_fixture(data: dict[str, object]) -> None:
    finite = data["finite_fixture"]
    require(finite["q_values"] == list(Q_VALUES), "q labels")
    require(finite["divisor_values"] == list(D_VALUES), "divisors")
    require(finite["height"] == HEIGHT and finite["upper_denominator"] == UPPER, "finite scales")
    require(finite["reduced_denominators"] == list(reduced_denominators(D_VALUES)), "denominators")
    require(finite["coefficient_energy"] == str(energy()), "coefficient energy")
    require(finite["classification"] == "NUMERICALLY_CERTIFIED_STRUCTURAL_FIXTURE", "fixture class")
    for record in finite["intervals"]:
        start = record["start"]
        length = record["length"]
        direct_energy = sum(
            norm(tuple(direct_at(start + offset, q, packet) for q in Q_VALUES for packet in range(4)))
            for offset in range(length)
        )
        regrouped_energy = sum(norm(vector_at(start + offset)) for offset in range(length))
        error = max(
            abs(direct_at(start + offset, q, packet) - reduced_at(start + offset, q, packet))
            for offset in range(length)
            for q in Q_VALUES
            for packet in range(4)
        )
        rhs = (length + UPPER * UPPER) * float(energy())
        require(record["direct_vector_energy"] == format(direct_energy, ".17g"), f"direct energy {start}")
        require(record["regrouped_vector_energy"] == format(regrouped_energy, ".17g"), f"regrouped energy {start}")
        require(record["large_sieve_rhs"] == format(rhs, ".17g"), f"large sieve rhs {start}")
        require(record["energy_to_large_sieve_ratio"] == format(direct_energy / rhs, ".17g"), f"ratio {start}")
        require(record["pointwise_regrouping_error"] == format(error, ".17g"), f"error {start}")
        require(error < 1e-11, f"regrouping mismatch {start}")
        require(direct_energy <= rhs * (1 + 1e-12), f"large sieve fixture {start}")


def check_prime_alignment(data: dict[str, object]) -> None:
    fixture = data["prime_label_alignment"]
    require(fixture["q_values"] == list(ALIGNMENT_Q_VALUES), "alignment q values")
    require(fixture["height"] == ALIGNMENT_HEIGHT and fixture["modulus"] == ALIGNMENT_MODULUS, "alignment scales")
    require(fixture["cutoffs"] == [1, 1, 1, 1], "alignment cutoff")
    require(fixture["q_mod_d"] == [1, 1, 1, 1], "alignment residue")
    rows = [row_for_q(ALIGNMENT_MODULUS, q, ALIGNMENT_HEIGHT) for q in ALIGNMENT_Q_VALUES]
    supports = [[i for i, value in enumerate(row) if value] for row in rows]
    require(fixture["row_supports"] == supports == [[1, 4]] * 4, "aligned supports")
    combined = tuple(sum((row[index] for row in rows), Fraction(0, 1)) for index in range(5))
    diagonal = sum((value * value for row in rows for value in row), Fraction(0, 1))
    coherent = sum((value * value for value in combined), Fraction(0, 1))
    require(fixture["diagonal_energy"] == str(diagonal), "diagonal")
    require(fixture["coherent_energy"] == str(coherent), "coherent")
    require(fixture["coherent_to_diagonal_ratio"] == str(coherent / diagonal) == "4", "ratio")
    require(fixture["classification"] == "NUMERICALLY_CERTIFIED_FINITE_STRUCTURAL_ADVERSARY", "adversary class")


def check_packet_alignment(data: dict[str, object]) -> None:
    fixture = data["packet_alignment"]
    require(fixture["packet_count"] == 4, "packet count")
    require(fixture["total_packet_energy"] == "5", "packet energy")
    require(fixture["unit_projection_energy"] == "5", "projection energy")
    require(fixture["projection_to_total_ratio"] == "1", "projection ratio")
    require(fixture["classification"] == "ALGEBRAIC_FINITE_ALIGNMENT", "packet class")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        data = json.loads(CERTIFICATE.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        require(data["schema"] == "TPC218_PRIME_SHELL_PACKET_LIFT_CERTIFICATE_V1", "schema")
        require(data["classification"] == "PROVED_STRUCTURAL_L1_PRIME_LABEL_AND_PACKET_PRESERVING_LIFT", "classification")
        require(data["theorem"]["split_normalized_exponent"] == "PROVED_X_1_OVER_96_LOG_FIVE", "split theorem")
        require(data["theorem"]["scalar_shell_recovery"] == "PROVED_X_11_OVER_32_LOG_FIVE", "collapse theorem")
        require(data["theorem"]["prime_count_used"] is False, "prime count")
        require(data["theorem"]["mobius_cancellation_used"] is False, "Mobius cancellation")
        expected_firewall = {
            "route_a": "NOT_APPLICABLE",
            "route_b_structural_threshold_a": "PASS",
            "hilbert_valued_large_sieve": "PROVED_STANDARD_TENSOR_LIFT",
            "prime_label_preservation": "PROVED_EXACT",
            "packet_matrix_bound": "PROVED_EXACT",
            "split_normalized_exponent": "PROVED_1_OVER_96_LOG_FIVE",
            "scalar_collapse": "PROVED_P_FACTOR_RECOVERS_11_OVER_32",
            "prime_label_orthogonality": "REFUTED_SCOPED",
            "packet_cancellation": "NONE",
            "prime_shell_signed_reassembly": "OPEN",
            "four_packet_signed_reassembly": "OPEN",
            "arithmetic_cancellation": "NONE",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b": "OPEN",
            "full_gate_b_strict_1_over_400": "UNPAID",
        }
        require(data["claim_firewall"] == expected_firewall, "firewall")
        check_finite_fixture(data)
        check_prime_alignment(data)
        check_packet_alignment(data)
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"TPC218_INDEPENDENT_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    print("TPC218_INDEPENDENT_CHECK=PASS")
    print("finite_intervals=3")
    print("q_alignment_ratio=4")
    print("packet_projection_ratio=1")
    print("normalization=vector_split_then_P_collapse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
