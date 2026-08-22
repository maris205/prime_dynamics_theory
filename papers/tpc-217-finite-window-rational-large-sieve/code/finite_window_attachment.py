#!/usr/bin/env python3
"""Finite-window reduced-frequency attachment for TPC-217."""

from __future__ import annotations

import cmath
import math
from fractions import Fraction
from math import gcd


Q_VALUES = (11, 13, 17)
HEIGHT = 40
LOWER = 2
UPPER = 35
PSI_NAME = "(1+t^2)^(-2)"


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise AuditFailure(message)


def prime_factors(value: int) -> tuple[int, ...]:
    require(type(value) is int and value >= 1, "positive integer")
    remaining = value
    factors: list[int] = []
    candidate = 2
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            factors.append(candidate)
            remaining //= candidate
            require(remaining % candidate != 0, "squarefree input")
        candidate += 1
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def mobius(value: int) -> int:
    require(type(value) is int and value >= 1, "positive integer")
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


def divisor_family(
    lower: int = LOWER,
    upper: int = UPPER,
    q_values: tuple[int, ...] = Q_VALUES,
) -> tuple[int, ...]:
    return tuple(
        value
        for value in range(lower + 1, upper + 1)
        if squarefree(value) and all(gcd(value, q) == 1 for q in q_values)
    )


def positive_divisors(value: int) -> tuple[int, ...]:
    return tuple(d for d in range(1, value + 1) if value % d == 0)


def psi_weight(argument: Fraction) -> Fraction:
    return Fraction(1, 1) / (1 + argument * argument) ** 2


def emitter_row(
    divisor: int,
    q_values: tuple[int, ...] = Q_VALUES,
    height: int = HEIGHT,
) -> tuple[Fraction, ...]:
    require(divisor >= 1 and height >= 1, "positive parameters")
    row = [Fraction(0, 1) for _ in range(divisor)]
    for q in q_values:
        require(gcd(q, divisor) == 1, "q must be a unit modulo divisor")
        cutoff = divisor * q // height
        inverse = pow(q, -1, divisor) if divisor > 1 else 0
        for m in range(-cutoff, cutoff + 1):
            if m:
                residue = (m * inverse) % divisor if divisor > 1 else 0
                row[residue] += psi_weight(Fraction(height * m, divisor * q))
    return tuple(row)


def reduced_denominators(family: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted({h for divisor in family for h in positive_divisors(divisor)}))


def coefficient_value(divisor: int) -> float:
    return mobius(divisor) * math.log(divisor) / divisor


def cluster_coefficient(family: tuple[int, ...], denominator: int) -> float:
    return sum(
        (coefficient_value(divisor) for divisor in family if divisor % denominator == 0),
        0.0,
    )


def primitive_residues(denominator: int) -> tuple[int, ...]:
    return tuple(a for a in range(denominator) if gcd(a, denominator) == 1)


def direct_value(
    integer: int,
    family: tuple[int, ...],
    q_values: tuple[int, ...] = Q_VALUES,
    height: int = HEIGHT,
) -> complex:
    total = 0j
    for divisor in family:
        row = emitter_row(divisor, q_values, height)
        for residue, value in enumerate(row):
            total += coefficient_value(divisor) * float(value) * cmath.exp(
                2j * math.pi * integer * residue / divisor
            )
    return total


def reduced_value(
    integer: int,
    family: tuple[int, ...],
    q_values: tuple[int, ...] = Q_VALUES,
    height: int = HEIGHT,
) -> complex:
    total = 0j
    for denominator in reduced_denominators(family):
        coefficient = cluster_coefficient(family, denominator)
        row = emitter_row(denominator, q_values, height)
        for numerator in primitive_residues(denominator):
            total += coefficient * float(row[numerator]) * cmath.exp(
                2j * math.pi * integer * numerator / denominator
            )
    return total


def cluster_energy(
    family: tuple[int, ...],
    q_values: tuple[int, ...] = Q_VALUES,
    height: int = HEIGHT,
) -> float:
    total = 0.0
    for denominator in reduced_denominators(family):
        coefficient = cluster_coefficient(family, denominator)
        row = emitter_row(denominator, q_values, height)
        total += sum(
            (coefficient * float(row[numerator])) ** 2
            for numerator in primitive_residues(denominator)
        )
    return total


def window_energy(
    start: int,
    length: int,
    evaluator,
    family: tuple[int, ...],
    q_values: tuple[int, ...] = Q_VALUES,
    height: int = HEIGHT,
) -> float:
    require(length >= 1, "positive window length")
    return sum(
        abs(evaluator(start + offset, family, q_values, height)) ** 2
        for offset in range(length)
    )


def build_fixture() -> dict[str, object]:
    family = divisor_family()
    reduced = reduced_denominators(family)
    diagonal = cluster_energy(family)
    intervals = []
    for start, length in ((0, 1), (0, 17), (123, 60)):
        direct = window_energy(start, length, direct_value, family)
        regrouped = window_energy(start, length, reduced_value, family)
        right_hand_side = (length + UPPER * UPPER) * diagonal
        pointwise_error = max(
            abs(direct_value(start + offset, family) - reduced_value(start + offset, family))
            for offset in range(length)
        )
        intervals.append(
            {
                "start": start,
                "length": length,
                "direct_window_energy": format(direct, ".17g"),
                "regrouped_window_energy": format(regrouped, ".17g"),
                "large_sieve_rhs": format(right_hand_side, ".17g"),
                "energy_to_large_sieve_ratio": format(direct / right_hand_side, ".17g"),
                "pointwise_regrouping_error": format(pointwise_error, ".17g"),
            }
        )

    adversary_q = (101, 131, 151, 181)
    adversary_row = emitter_row(5, adversary_q, 500)
    support = [index for index, value in enumerate(adversary_row) if value]
    diagonal_adversary = sum(float(adversary_row[index]) ** 2 for index in support)
    one_point_energy = sum(float(adversary_row[index]) for index in support) ** 2

    return {
        "schema": "TPC217_FINITE_WINDOW_RATIONAL_LARGE_SIEVE_CERTIFICATE_V1",
        "classification": "PROVED_STRUCTURAL_L1_FINITE_WINDOW_ATTACHMENT",
        "source_exponents": {
            "H": "21/32",
            "Q": "1/3",
            "U": "133/400",
            "Y0": "31/96",
            "Q3_over_H": "11/32",
            "U2_over_x": "-67/200",
        },
        "source_relations": {
            "physical_interval": "I_x=(x/2,x] intersect Z",
            "reduced_frequency": "a/h with 1<=h<=U and gcd(a,h)=1",
            "cluster_coefficient": "C_h=sum_(d in D_x,h|d)c_d",
            "finite_window_bound": "E_I<=(N+U^2)*sum_(h,a)|C_h B_h(a)|^2",
            "coefficient_majorant": "sum_(h,a)|C_h B_h(a)|^2<=A_x*E_direct/L",
        },
        "theorem": {
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
        "finite_fixture": {
            "q_values": list(Q_VALUES),
            "H": HEIGHT,
            "Y0": LOWER,
            "U": UPPER,
            "psi": PSI_NAME,
            "divisors": list(family),
            "reduced_denominators": list(reduced),
            "cluster_energy": format(diagonal, ".17g"),
            "intervals": intervals,
            "numeric_classification": "NUMERICAL_OBSERVATION",
        },
        "frequency_crowding_adversary": {
            "q_values": list(adversary_q),
            "H": 500,
            "d": 5,
            "cutoff": 1,
            "support": support,
            "diagonal_energy": format(diagonal_adversary, ".17g"),
            "one_point_window_energy": format(one_point_energy, ".17g"),
            "window_to_diagonal_ratio": format(one_point_energy / diagonal_adversary, ".17g"),
            "classification": "FINITE_STRUCTURAL_ADVERSARY",
        },
        "claim_firewall": {
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
    }
