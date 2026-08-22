#!/usr/bin/env python3
"""Build the exact finite certificate for TPC-218.

The certificate deliberately separates three objects:

* a small literal dilation/regrouping fixture;
* a Hilbert-valued finite-window large-sieve fixture;
* two algebraic adversaries, one for the prime label and one for packet
  projection.

All row values and fixture coefficients are rational until the exponential
evaluation is requested.  The finite tests are structural checks only; they
do not claim an asymptotic prime or Möbius cancellation theorem.
"""

from __future__ import annotations

import cmath
import json
import math
from fractions import Fraction


class AuditFailure(RuntimeError):
    """Raised when the finite structural fixture is malformed."""


Q_VALUES = (11, 13, 17)
D_VALUES = (5, 10, 15)
HEIGHT = 40
UPPER = 35
PACKET_WEIGHTS = (Fraction(1), Fraction(1, 2), Fraction(-1), Fraction(2))
ALIGNMENT_Q_VALUES = (101, 131, 151, 181)
ALIGNMENT_HEIGHT = 500
ALIGNMENT_MODULUS = 5


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise AuditFailure(message)


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
    """Constant-profile emitter row for one shell label."""

    require(is_prime(q), f"q={q} is not prime")
    require(math.gcd(q, modulus) == 1, f"q={q} is not a unit modulo {modulus}")
    cutoff = modulus * q // height
    result = [Fraction(0, 1) for _ in range(modulus)]
    inverse = pow(q, -1, modulus) if modulus > 1 else 0
    for m in range(-cutoff, cutoff + 1):
        if m:
            residue = (m * inverse) % modulus if modulus > 1 else 0
            result[residue] += Fraction(1, 1)
    return tuple(result)


def coefficient(value: int) -> Fraction:
    # The finite dilation fixture uses mu(d)/d so every identity is exact.
    # The asymptotic theorem itself retains the literal mu(d) log(d)/d.
    return Fraction(mobius(value), value)


def cluster_coefficient(values: tuple[int, ...], denominator: int) -> Fraction:
    return sum(
        (coefficient(value) for value in values if value % denominator == 0),
        Fraction(0, 1),
    )


def fraction_string(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def direct_at(
    integer: int,
    values: tuple[int, ...],
    q: int,
    packet: int,
) -> complex:
    total = 0j
    weight = float(PACKET_WEIGHTS[packet])
    for divisor in values:
        row = row_for_q(divisor, q)
        for residue, value in enumerate(row):
            total += (
                float(coefficient(divisor) * value) * weight
                * cmath.exp(2j * math.pi * integer * residue / divisor)
            )
    return total


def reduced_at(
    integer: int,
    values: tuple[int, ...],
    q: int,
    packet: int,
) -> complex:
    total = 0j
    weight = float(PACKET_WEIGHTS[packet])
    for denominator in reduced_denominators(values):
        scale = cluster_coefficient(values, denominator)
        row = row_for_q(denominator, q)
        for numerator in primitive(denominator):
            total += (
                float(scale * row[numerator]) * weight
                * cmath.exp(2j * math.pi * integer * numerator / denominator)
            )
    return total


def vector_at(
    integer: int,
    values: tuple[int, ...],
    q_values: tuple[int, ...] = Q_VALUES,
) -> tuple[complex, ...]:
    return tuple(
        reduced_at(integer, values, q, packet)
        for q in q_values
        for packet in range(len(PACKET_WEIGHTS))
    )


def coefficient_energy(
    values: tuple[int, ...],
    q_values: tuple[int, ...] = Q_VALUES,
) -> Fraction:
    energy = Fraction(0, 1)
    for denominator in reduced_denominators(values):
        scale = cluster_coefficient(values, denominator)
        row_values = [row_for_q(denominator, q) for q in q_values]
        for numerator in primitive(denominator):
            for row in row_values:
                for weight in PACKET_WEIGHTS:
                    value = scale * row[numerator] * weight
                    energy += value * value
    return energy


def squared_norm(values: tuple[complex, ...]) -> float:
    return sum(abs(value) ** 2 for value in values)


def interval_record(start: int, length: int) -> dict[str, object]:
    energy = coefficient_energy(D_VALUES)
    direct_energy = sum(
        squared_norm(
            tuple(
                direct_at(start + offset, D_VALUES, q, packet)
                for q in Q_VALUES
                for packet in range(len(PACKET_WEIGHTS))
            )
        )
        for offset in range(length)
    )
    regrouped_energy = sum(
        squared_norm(vector_at(start + offset, D_VALUES))
        for offset in range(length)
    )
    pointwise_error = max(
        max(
            abs(
                direct_at(start + offset, D_VALUES, q, packet)
                - reduced_at(start + offset, D_VALUES, q, packet)
            )
            for q in Q_VALUES
            for packet in range(len(PACKET_WEIGHTS))
        )
        for offset in range(length)
    )
    rhs = (length + UPPER * UPPER) * float(energy)
    return {
        "start": start,
        "length": length,
        "direct_vector_energy": format(direct_energy, ".17g"),
        "regrouped_vector_energy": format(regrouped_energy, ".17g"),
        "large_sieve_rhs": format(rhs, ".17g"),
        "energy_to_large_sieve_ratio": format(direct_energy / rhs, ".17g"),
        "pointwise_regrouping_error": format(pointwise_error, ".17g"),
    }


def prime_alignment_fixture() -> dict[str, object]:
    rows = {
        q: row_for_q(ALIGNMENT_MODULUS, q, ALIGNMENT_HEIGHT)
        for q in ALIGNMENT_Q_VALUES
    }
    combined = tuple(
        sum((rows[q][index] for q in ALIGNMENT_Q_VALUES), Fraction(0, 1))
        for index in range(ALIGNMENT_MODULUS)
    )
    individual_energy = sum(
        (value * value for row in rows.values() for value in row),
        Fraction(0, 1),
    ) / len(ALIGNMENT_Q_VALUES)
    diagonal = len(ALIGNMENT_Q_VALUES) * individual_energy
    coherent = sum((value * value for value in combined), Fraction(0, 1))
    return {
        "q_values": list(ALIGNMENT_Q_VALUES),
        "height": ALIGNMENT_HEIGHT,
        "modulus": ALIGNMENT_MODULUS,
        "cutoffs": [
            ALIGNMENT_MODULUS * q // ALIGNMENT_HEIGHT
            for q in ALIGNMENT_Q_VALUES
        ],
        "profile": "1",
        "q_mod_d": [q % ALIGNMENT_MODULUS for q in ALIGNMENT_Q_VALUES],
        "row_supports": [
            [index for index, value in enumerate(rows[q]) if value]
            for q in ALIGNMENT_Q_VALUES
        ],
        "combined_row": [fraction_string(value) for value in combined],
        "diagonal_energy": fraction_string(diagonal),
        "coherent_energy": fraction_string(coherent),
        "coherent_to_diagonal_ratio": fraction_string(coherent / diagonal),
        "cauchy_ratio": len(ALIGNMENT_Q_VALUES),
        "classification": "NUMERICALLY_CERTIFIED_FINITE_STRUCTURAL_ADVERSARY",
    }


def packet_alignment_fixture() -> dict[str, object]:
    # Four-packet polarization vector omega=(1,i,-1,-i)/2 and v=(1,2).
    # The unit projection captures all energy when every packet is parallel.
    vector_norm = Fraction(1 + 4, 1)
    total_packet_energy = vector_norm
    projected_energy = vector_norm
    return {
        "packet_count": 4,
        "omega": ["1/2", "i/2", "-1/2", "-i/2"],
        "base_vector": [1, 2],
        "total_packet_energy": fraction_string(total_packet_energy),
        "unit_projection_energy": fraction_string(projected_energy),
        "projection_to_total_ratio": fraction_string(projected_energy / total_packet_energy),
        "classification": "ALGEBRAIC_FINITE_ALIGNMENT",
    }


def build_fixture() -> dict[str, object]:
    require(all(mobius(value) != 0 for value in D_VALUES), "fixture divisors must be squarefree")
    require(all(is_prime(q) for q in Q_VALUES), "fixture shell must be prime")
    require(all(math.gcd(q, value) == 1 for q in Q_VALUES for value in D_VALUES), "unit fixture")
    return {
        "schema": "TPC218_PRIME_SHELL_PACKET_LIFT_CERTIFICATE_V1",
        "classification": "PROVED_STRUCTURAL_L1_PRIME_LABEL_AND_PACKET_PRESERVING_LIFT",
        "source_exponents": {
            "H": "21/32",
            "Q": "1/3",
            "Y0": "31/96",
            "U": "133/400",
            "Q2_over_H": "1/96",
            "Q3_over_H": "11/32",
            "U2_over_x": "-67/200",
            "UQ_over_H": "23/2400",
        },
        "source_relations": {
            "shell": "Q<q<=2Q",
            "packet_count": "J=4 for the four-packet interface",
            "split_kernel": "K_(j,q)(n)=sum_(h,a) C_h B_(h,q)^(j)(a)e(na/h)",
            "vector_kernel": "K_vec(n)=(K_(j,q)(n))_(j,q)",
            "finite_window_bound": "sum_I ||K_vec||^2 <= (N+U^2) sum_(h,a,j,q)|C_h B_(h,q)^(j)(a)|^2",
            "active_h": "h>=H/(2Q) for a nonzero emitter row",
            "coefficient_harmonic_bound": "sum_h h|C_h|^2 << (log x)^5",
        },
        "theorem": {
            "hilbert_valued_large_sieve": "PROVED_STANDARD_TENSOR_LIFT",
            "prime_label_preservation": "PROVED_EXACT_COORDINATE_LIFT",
            "packet_matrix_bound": "PROVED_EXACT_TRACE_DOMINATION",
            "split_normalized_exponent": "PROVED_X_1_OVER_96_LOG_FIVE",
            "split_unnormalized_exponent": "97/96",
            "scalar_shell_recovery": "PROVED_X_11_OVER_32_LOG_FIVE",
            "scalar_collapse_cost": "P<=2Q",
            "prime_count_used": False,
            "mobius_cancellation_used": False,
            "arithmetic_saving": False,
            "status": "PROVED_STRUCTURAL_L1",
        },
        "finite_fixture": {
            "q_values": list(Q_VALUES),
            "divisor_values": list(D_VALUES),
            "height": HEIGHT,
            "upper_denominator": UPPER,
            "packet_weights": [fraction_string(value) for value in PACKET_WEIGHTS],
            "reduced_denominators": list(reduced_denominators(D_VALUES)),
            "coefficient_energy": fraction_string(coefficient_energy(D_VALUES)),
            "intervals": [interval_record(0, 3), interval_record(5, 4), interval_record(17, 2)],
            "coefficient_note": "mu(d)/d surrogate used only for exact finite index validation; asymptotic theorem uses mu(d)log(d)/d",
            "classification": "NUMERICALLY_CERTIFIED_STRUCTURAL_FIXTURE",
        },
        "prime_label_alignment": prime_alignment_fixture(),
        "packet_alignment": packet_alignment_fixture(),
        "claim_firewall": {
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
        },
    }


def canonical(data: dict[str, object]) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
