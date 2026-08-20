#!/usr/bin/env python3
"""Independent reconstruction of the TPC-215 finite certificate."""

from __future__ import annotations

import argparse
import hashlib
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
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def factors(value: int) -> tuple[int, ...]:
    result: list[int] = []
    remainder = value
    candidate = 2
    while candidate * candidate <= remainder:
        if remainder % candidate == 0:
            result.append(candidate)
            remainder //= candidate
            if remainder % candidate == 0:
                raise ValueError("not squarefree")
        candidate += 1
    if remainder > 1:
        result.append(remainder)
    return tuple(result)


def squarefree(value: int) -> bool:
    try:
        factors(value)
    except ValueError:
        return False
    return True


def mu(value: int) -> int:
    return -1 if len(factors(value)) % 2 else 1


def divisors(value: int) -> tuple[int, ...]:
    return tuple(item for item in range(1, value + 1) if value % item == 0)


def psi(value: Fraction) -> Fraction:
    return Fraction(1, 1) / (1 + value * value) ** 2


def row(modulus: int) -> tuple[Fraction, ...]:
    result = [Fraction(0, 1) for _ in range(modulus)]
    for q in Q_VALUES:
        require(gcd(q, modulus) == 1, "unit inverse")
        cutoff = modulus * q // HEIGHT
        for m in range(-cutoff, cutoff + 1):
            if m:
                result[(m * pow(q, -1, modulus)) % modulus] += psi(
                    Fraction(HEIGHT * m, modulus * q)
                )
    return tuple(result)


def row_hash(values: tuple[Fraction, ...]) -> str:
    return hashlib.sha256("|".join(str(value) for value in values).encode("ascii")).hexdigest()


def fraction_hash(value: Fraction) -> str:
    return hashlib.sha256(str(value).encode("ascii")).hexdigest()


def norm(values: tuple[Fraction, ...]) -> Fraction:
    return sum((value * value for value in values), Fraction(0, 1))


def primitive_norm(values: tuple[Fraction, ...]) -> Fraction:
    modulus = len(values)
    return sum(
        (values[residue] ** 2 for residue in range(modulus) if gcd(residue, modulus) == 1),
        Fraction(0, 1),
    )


def coefficient_poly(value: int) -> dict[str, Fraction]:
    scale = Fraction(mu(value), value)
    return {f"log({prime})": scale for prime in factors(value)}


def add_poly(left: dict[str, Fraction], right: dict[str, Fraction]) -> dict[str, Fraction]:
    result = dict(left)
    for variable, coefficient in right.items():
        result[variable] = result.get(variable, Fraction(0, 1)) + coefficient
        if result[variable] == 0:
            del result[variable]
    return result


def tail_poly(family: tuple[int, ...], denominator: int) -> dict[str, Fraction]:
    result: dict[str, Fraction] = {}
    for value in family:
        if value % denominator == 0:
            result = add_poly(result, coefficient_poly(value))
    return result


def evaluate(poly: dict[str, Fraction]) -> float:
    return sum(
        float(coefficient) * math.log(int(variable[4:-1]))
        for variable, coefficient in poly.items()
    )


def harmonic(number: int) -> Fraction:
    return sum((Fraction(1, value) for value in range(1, number + 1)), Fraction(0, 1))


def expected_firewall() -> dict[str, object]:
    return {
        "route_advance": "YES",
        "structural_threshold_a": "PASS",
        "activation_floor": "PROVED_EXACT",
        "active_denominator_in_full_band": "PROVED_EXACT",
        "short_quotient_normal_form": "PROVED_EXACT",
        "quotient_length_exponent": "PROVED_23_OVER_2400",
        "row_norm_divisor_decomposition": "PROVED_EXACT",
        "cluster_to_direct_majorant": "PROVED_O_LOG_X_SQUARED",
        "fixed_power_cluster_amplification": "EXCLUDED",
        "top_shell_ratio_one": "PROVED_EXACT",
        "uniform_rowwise_power_saving": "REFUTED_SCOPED",
        "finite_ratios": "NUMERICAL_OBSERVATION",
        "direct_sum_arithmetic_energy_bound": "OPEN",
        "finite_window_off_frequency_gram": "OPEN",
        "prime_shell_reassembly": "OPEN",
        "arithmetic_advance": "NO",
        "fixed_atom_credit": 0,
        "l2": "NONE",
        "full_gate_b_strict_1_over_400": "UNPAID",
    }


def check_fixture(fixture: dict[str, object]) -> None:
    family = tuple(
        value
        for value in range(LOWER + 1, UPPER + 1)
        if squarefree(value) and all(gcd(value, q) == 1 for q in Q_VALUES)
    )
    reduced = tuple(sorted({h for value in family for h in divisors(value)}))
    active = tuple(h for h in reduced if any(row(h)))
    activation_floor = (HEIGHT + max(Q_VALUES) - 1) // max(Q_VALUES)
    quotient_bound = UPPER * max(Q_VALUES) // HEIGHT

    require(fixture["q_values"] == list(Q_VALUES), "q values")
    require(fixture["H"] == HEIGHT, "height")
    require(fixture["Y0"] == LOWER, "lower cutoff")
    require(fixture["U"] == UPPER, "upper cutoff")
    require(fixture["psi"] == "(1+t^2)^(-2)", "psi")
    require(fixture["divisors"] == list(family), "divisor family")
    require(fixture["reduced_denominators"] == list(reduced), "reduced denominators")
    require(fixture["active_denominators"] == list(active), "active denominators")
    require(fixture["activation_floor"] == activation_floor, "activation floor")
    require(fixture["uniform_quotient_bound"] == quotient_bound, "quotient bound")
    require(all(h >= activation_floor and h in family for h in active), "activation band")
    require(row(1)[0] == 0, "zero axis")

    dilation_count = 0
    decomposition_rows: list[str] = []
    for value in family:
        large = row(value)
        for h in divisors(value):
            small = row(h)
            scale = value // h
            for residue, entry in enumerate(small):
                require(large[scale * residue] == entry, "dilation covariance")
                dilation_count += 1
        lhs = norm(large)
        rhs = sum((primitive_norm(row(h)) for h in divisors(value)), Fraction(0, 1))
        require(lhs == rhs, "row decomposition")
        decomposition_rows.append(f"{value}:{lhs}:{rhs}")
    require(fixture["dilation_checks"] == dilation_count, "dilation count")
    expected_decomposition_hash = hashlib.sha256(
        "|".join(decomposition_rows).encode("ascii")
    ).hexdigest()
    require(fixture["row_decomposition_hash"] == expected_decomposition_hash, "decomposition hash")

    records = fixture["tail_rows"]
    require(type(records) is list and len(records) == len(active), "tail row count")
    cluster_energy = 0.0
    actual_max = 1
    expected_top: list[int] = []
    for h, record in zip(active, records):
        require(type(record) is dict, "tail row object")
        multiples = tuple(value for value in family if value % h == 0)
        quotients = tuple(value // h for value in multiples)
        actual_max = max(actual_max, *quotients)
        poly = tail_poly(family, h)
        value = evaluate(poly)
        direct_mass = sum((mu(d) * math.log(d) / d) ** 2 for d in multiples)
        ratio = value * value / direct_mass
        harmonic_index = UPPER // h
        majorant = (math.log(UPPER) / math.log(h)) ** 2 * float(harmonic(harmonic_index)) ** 2
        is_top = 2 * h > UPPER
        if is_top:
            expected_top.append(h)
            require(multiples == (h,), "top-shell multiple")
            require(poly == coefficient_poly(h), "top-shell coefficient")
            require(abs(ratio - 1.0) <= 1e-14, "top-shell ratio")
        require(record == {
            "denominator": h,
            "multiples": list(multiples),
            "quotients": list(quotients),
            "tail_polynomial": {key: str(poly[key]) for key in sorted(poly)},
            "tail_value": format(value, ".17g"),
            "direct_coefficient_mass": format(direct_mass, ".17g"),
            "tail_to_direct_ratio": format(ratio, ".17g"),
            "harmonic_index": harmonic_index,
            "harmonic_majorant": format(majorant, ".17g"),
            "top_shell": is_top,
            "row_hash": row_hash(row(h)),
            "primitive_norm_hash": fraction_hash(primitive_norm(row(h))),
        }, f"tail row {h}")
        require(ratio <= majorant * (1 + 1e-13), "majorant")
        cluster_energy += float(primitive_norm(row(h))) * value * value

    direct_energy = sum(
        (mu(d) * math.log(d) / d) ** 2 * float(norm(row(d))) for d in family
    )
    global_ratio = cluster_energy / direct_energy
    require(fixture["actual_max_quotient"] == actual_max, "actual quotient")
    require(actual_max <= quotient_bound, "actual quotient bound")
    require(fixture["top_shell_denominators"] == expected_top, "top-shell list")
    require(fixture["cluster_energy"] == format(cluster_energy, ".17g"), "cluster energy")
    require(fixture["direct_sum_energy"] == format(direct_energy, ".17g"), "direct energy")
    require(fixture["cluster_to_direct_ratio"] == format(global_ratio, ".17g"), "global ratio")
    require(fixture["numeric_classification"] == "NUMERICAL_OBSERVATION", "numeric class")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        require(CERTIFICATE.is_file(), "certificate missing")
        data = json.loads(CERTIFICATE.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        require(data["schema"] == "TPC215_SHORT_QUOTIENT_MOBIUS_MAJORANT_CERTIFICATE_V1", "schema")
        require(data["classification"] == "PROVED_STRUCTURAL_L1_SHORT_QUOTIENT_CLUSTER_MAJORANT", "class")
        require(data["source_exponents"] == {
            "H": "21/32",
            "Q": "1/3",
            "U": "133/400",
            "Y0": "31/96",
            "UQ_over_H": "23/2400",
        }, "source exponents")
        require(data["source_relations"] == {
            "Y0": "H/(4Q)",
            "q_shell": "Q<q<=2Q",
            "activation": "h>=H/q_max>=H/(2Q)=2Y0",
            "quotient": "k<=Uq_max/H<=2UQ/H=2x^(23/2400+o(1))",
            "majorant": "A_x=O((log x)^2)=x^(o(1))",
        }, "source relations")
        require(data["claim_firewall"] == expected_firewall(), "claim firewall")
        check_fixture(data["finite_fixture"])
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, ZeroDivisionError) as error:
        print(f"TPC215_INDEPENDENT_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    fixture = data["finite_fixture"]
    print("TPC215_INDEPENDENT_CHECK=PASS")
    print("active_denominators=", len(fixture["active_denominators"]))
    print("top_shell_rows=", len(fixture["top_shell_denominators"]))
    print("global_ratio=", fixture["cluster_to_direct_ratio"])
    print("claim_level=PROVED_STRUCTURAL_L1_SHORT_QUOTIENT_CLUSTER_MAJORANT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
