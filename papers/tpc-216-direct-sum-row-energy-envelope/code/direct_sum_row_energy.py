#!/usr/bin/env python3
"""Materialize the exact finite certificate for TPC-216."""

from __future__ import annotations

from fractions import Fraction


Q_SCALE = 100
HEIGHT = 500
MODULUS = 5
Q_VALUES = (101, 131, 151, 181)


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise AuditFailure(message)


def fraction_string(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return value == divisor
        divisor += 1
    return True


def psi(value: Fraction) -> Fraction:
    return Fraction(1, 1) / (1 + value * value) ** 2


def row_for_q(q: int) -> tuple[Fraction, ...]:
    require(is_prime(q), f"q={q} is not prime")
    require(q % MODULUS == 1, f"q={q} is not 1 modulo {MODULUS}")
    cutoff = MODULUS * q // HEIGHT
    result = [Fraction(0, 1) for _ in range(MODULUS)]
    inverse = pow(q, -1, MODULUS)
    for m in range(-cutoff, cutoff + 1):
        if m != 0:
            result[(m * inverse) % MODULUS] += psi(
                Fraction(HEIGHT * m, MODULUS * q)
            )
    return tuple(result)


def row_total(q_values: tuple[int, ...]) -> tuple[Fraction, ...]:
    result = [Fraction(0, 1) for _ in range(MODULUS)]
    for q in q_values:
        for residue, value in enumerate(row_for_q(q)):
            result[residue] += value
    return tuple(result)


def norm(row: tuple[Fraction, ...]) -> Fraction:
    return sum((value * value for value in row), Fraction(0, 1))


def support(row: tuple[Fraction, ...]) -> list[int]:
    return [index for index, value in enumerate(row) if value != 0]


def build_certificate() -> dict[str, object]:
    rows = {q: row_for_q(q) for q in Q_VALUES}
    individual_norms = {q: norm(rows[q]) for q in Q_VALUES}
    combined = row_total(Q_VALUES)
    combined_norm = norm(combined)
    diagonal_sum = sum(individual_norms.values(), Fraction(0, 1))
    ratio = combined_norm / diagonal_sum
    cauchy_rhs = len(Q_VALUES) * diagonal_sum

    row_records = []
    for q in Q_VALUES:
        row = rows[q]
        row_records.append(
            {
                "q": q,
                "cutoff": MODULUS * q // HEIGHT,
                "inverse_mod_d": pow(q, -1, MODULUS),
                "support": support(row),
                "row": [fraction_string(value) for value in row],
                "norm": fraction_string(individual_norms[q]),
            }
        )

    return {
        "schema": "TPC216_DIRECT_SUM_ROW_ENERGY_ENVELOPE_CERTIFICATE_V1",
        "classification": "PROVED_STRUCTURAL_L1_DIRECT_SUM_ROW_ENERGY_ENVELOPE",
        "source_exponents": {
            "H": "21/32",
            "Q": "1/3",
            "U": "133/400",
            "Y0": "31/96",
            "Q3_over_H": "11/32",
        },
        "source_relations": {
            "Y0": "H/(4Q)",
            "shell": "Q<q<=2Q",
            "collision_condition": "4Q<H for sufficiently large x",
            "direct_energy": "E_direct=L*sum_d |c_d|^2*||B_d||_2^2",
            "envelope": "L^(-1)E_direct <= C_psi*(Q^3/H)*(log U)^3",
        },
        "theorem": {
            "profile_assumption": "M_psi=sup_t |psi(t)|<infinity",
            "fixed_q_row_norm": "||B_(d,q)||_2^2 <= 2*M_psi^2*d*q/H",
            "shell_cauchy": "||B_d||_2^2 <= 4*M_psi^2*P^2*d*Q/H",
            "prime_shell_cardinality": "P<=2Q",
            "prime_count_used": False,
            "normalized_exponent": "11/32",
            "log_power": 3,
            "status": "PROVED_STRUCTURAL_L1",
        },
        "finite_adversary": {
            "Q_scale": Q_SCALE,
            "H": HEIGHT,
            "d": MODULUS,
            "q_values": list(Q_VALUES),
            "profile": "(1+t^2)^(-2)",
            "all_q_congruent_to_one_mod_d": True,
            "all_cutoffs": 1,
            "aligned_support": [1, MODULUS - 1],
            "individual_rows": row_records,
            "combined_row": [fraction_string(value) for value in combined],
            "individual_norm_sum": fraction_string(diagonal_sum),
            "combined_norm": fraction_string(combined_norm),
            "cauchy_upper_bound": fraction_string(cauchy_rhs),
            "coherence_ratio": fraction_string(ratio),
            "classification": "FINITE_STRUCTURAL_ADVERSARY",
        },
        "claim_firewall": {
            "route_a": "NOT_APPLICABLE",
            "route_b_structural_threshold_a": "PASS",
            "fixed_q_no_collision": "PROVED_EXACT",
            "shell_cauchy_envelope": "PROVED_EXACT",
            "direct_sum_row_energy_envelope": "PROVED_X_11_OVER_32_LOG_CUBED",
            "normalized_exponent": "PROVED_11_OVER_32",
            "arithmetic_cancellation": "NONE",
            "finite_window_off_frequency_gram": "OPEN",
            "prime_shell_reassembly": "OPEN",
            "full_gate_b": "OPEN",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b_strict_1_over_400": "UNPAID",
            "cauchy_bottleneck": "EXHIBITED_BY_ALIGNED_FINITE_FIXTURE",
        },
    }
