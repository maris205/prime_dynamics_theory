#!/usr/bin/env python3
"""Independent exact reconstruction of the TPC-216 adversarial fixture."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results/certificate.json"
Q_SCALE = 100
HEIGHT = 500
MODULUS = 5
Q_VALUES = (101, 131, 151, 181)


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


def fraction_string(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def parse_fraction(value: object, label: str) -> Fraction:
    require(type(value) is str, f"{label} is not a string")
    return Fraction(value)


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
    require(q % MODULUS == 1, f"q={q} congruence")
    cutoff = MODULUS * q // HEIGHT
    result = [Fraction(0, 1) for _ in range(MODULUS)]
    inverse = pow(q, -1, MODULUS)
    for m in range(-cutoff, cutoff + 1):
        if m:
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


def expected_row_record(q: int) -> dict[str, object]:
    row = row_for_q(q)
    return {
        "q": q,
        "cutoff": MODULUS * q // HEIGHT,
        "inverse_mod_d": pow(q, -1, MODULUS),
        "support": support(row),
        "row": [fraction_string(value) for value in row],
        "norm": fraction_string(norm(row)),
    }


def check_certificate(data: dict[str, object]) -> None:
    require(data["schema"] == "TPC216_DIRECT_SUM_ROW_ENERGY_ENVELOPE_CERTIFICATE_V1", "schema")
    require(
        data["classification"] == "PROVED_STRUCTURAL_L1_DIRECT_SUM_ROW_ENERGY_ENVELOPE",
        "classification",
    )
    require(
        data["source_exponents"] == {
            "H": "21/32",
            "Q": "1/3",
            "U": "133/400",
            "Y0": "31/96",
            "Q3_over_H": "11/32",
        },
        "source exponents",
    )
    require(
        data["source_relations"] == {
            "Y0": "H/(4Q)",
            "shell": "Q<q<=2Q",
            "collision_condition": "4Q<H for sufficiently large x",
            "direct_energy": "E_direct=L*sum_d |c_d|^2*||B_d||_2^2",
            "envelope": "L^(-1)E_direct <= C_psi*(Q^3/H)*(log U)^3",
        },
        "source relations",
    )
    require(
        data["theorem"] == {
            "profile_assumption": "M_psi=sup_t |psi(t)|<infinity",
            "fixed_q_row_norm": "||B_(d,q)||_2^2 <= 2*M_psi^2*d*q/H",
            "shell_cauchy": "||B_d||_2^2 <= 4*M_psi^2*P^2*d*Q/H",
            "prime_shell_cardinality": "P<=2Q",
            "prime_count_used": False,
            "normalized_exponent": "11/32",
            "log_power": 3,
            "status": "PROVED_STRUCTURAL_L1",
        },
        "theorem metadata",
    )
    firewall = data["claim_firewall"]
    require(
        firewall == {
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
        "claim firewall",
    )

    fixture = data["finite_adversary"]
    require(fixture["Q_scale"] == Q_SCALE, "Q scale")
    require(fixture["H"] == HEIGHT, "H")
    require(fixture["d"] == MODULUS, "d")
    require(fixture["q_values"] == list(Q_VALUES), "q values")
    require(fixture["profile"] == "(1+t^2)^(-2)", "profile")
    require(fixture["all_q_congruent_to_one_mod_d"] is True, "congruence flag")
    require(fixture["all_cutoffs"] == 1, "cutoff flag")
    require(fixture["aligned_support"] == [1, MODULUS - 1], "support flag")
    require(fixture["classification"] == "FINITE_STRUCTURAL_ADVERSARY", "finite class")

    rows = {q: row_for_q(q) for q in Q_VALUES}
    records = fixture["individual_rows"]
    require(type(records) is list and len(records) == len(Q_VALUES), "row record count")
    for q, record in zip(Q_VALUES, records):
        require(record == expected_row_record(q), f"row record q={q}")
        require(record["cutoff"] == 1, f"cutoff q={q}")
        require(record["support"] == [1, MODULUS - 1], f"support q={q}")

    combined = row_total(Q_VALUES)
    diagonal_sum = sum((norm(rows[q]) for q in Q_VALUES), Fraction(0, 1))
    combined_norm = norm(combined)
    ratio = combined_norm / diagonal_sum
    cauchy_upper_bound = len(Q_VALUES) * diagonal_sum
    require(
        fixture["combined_row"] == [fraction_string(value) for value in combined],
        "combined row",
    )
    require(fixture["individual_norm_sum"] == fraction_string(diagonal_sum), "diagonal sum")
    require(fixture["combined_norm"] == fraction_string(combined_norm), "combined norm")
    require(
        fixture["cauchy_upper_bound"] == fraction_string(cauchy_upper_bound),
        "Cauchy bound",
    )
    require(fixture["coherence_ratio"] == fraction_string(ratio), "coherence ratio")
    require(combined_norm > diagonal_sum, "aligned rows did not create positive cross energy")
    require(combined_norm <= cauchy_upper_bound, "Cauchy inequality")
    require(ratio > 1 and ratio < len(Q_VALUES), "coherence ratio range")

    for q in Q_VALUES:
        require(MODULUS * q // HEIGHT == 1, f"finite cutoff q={q}")
        require(norm(rows[q]) <= Fraction(2 * MODULUS * q, HEIGHT), f"fixed q bound q={q}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        require(CERTIFICATE.is_file(), "certificate missing")
        data = json.loads(CERTIFICATE.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        require(type(data) is dict, "certificate object")
        check_certificate(data)
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"TPC216_INDEPENDENT_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    fixture = data["finite_adversary"]
    print("TPC216_INDEPENDENT_CHECK=PASS")
    print("q_count=", len(fixture["q_values"]))
    print("aligned_support=", fixture["aligned_support"])
    print("coherence_ratio=", fixture["coherence_ratio"])
    print("normalized_exponent=11/32")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
