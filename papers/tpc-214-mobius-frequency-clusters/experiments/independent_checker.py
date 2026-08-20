"""Independent checker for the TPC-214 finite cluster certificate."""

from __future__ import annotations

import argparse
import json
import math
import sys
from fractions import Fraction
from math import gcd, lcm
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results/certificate.json"
Q_VALUES = (11, 13, 17)
HEIGHT = 40
FAMILIES = ((5, 7, 35), (3, 5, 7, 105))


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
            require(remainder % candidate != 0, "non-squarefree fixture")
        candidate += 1
    if remainder > 1:
        result.append(remainder)
    return tuple(result)


def mobius(value: int) -> int:
    result = 1
    for prime in factors(value):
        result = -result
    return result


def divisors(value: int) -> tuple[int, ...]:
    return tuple(d for d in range(1, value + 1) if value % d == 0)


def psi(value: Fraction) -> Fraction:
    return Fraction(1, 1) / (1 + value * value) ** 2


def row(modulus: int) -> tuple[Fraction, ...]:
    result = [Fraction(0, 1) for _ in range(modulus)]
    for q in Q_VALUES:
        require(gcd(q, modulus) == 1, "q is not a unit")
        limit = modulus * q // HEIGHT
        for m in range(-limit, limit + 1):
            if m:
                residue = (m * pow(q, -1, modulus)) % modulus
                result[residue] += psi(Fraction(HEIGHT * m, modulus * q))
    return tuple(result)


def row_hash(values: tuple[Fraction, ...]) -> str:
    import hashlib

    return hashlib.sha256("|".join(str(value) for value in values).encode("ascii")).hexdigest()


def row_norm(values: tuple[Fraction, ...], primitive_only: bool) -> Fraction:
    modulus = len(values)
    return sum(
        (values[index] * values[index] for index in range(modulus) if not primitive_only or gcd(index, modulus) == 1),
        Fraction(0, 1),
    )


def gram(left: int, right: int, period: int) -> Fraction:
    left_row = row(left)
    right_row = row(right)
    require(period % lcm(left, right) == 0, "common period")
    return period * sum(
        (
            left_row[a] * right_row[b]
            for a in range(left)
            for b in range(right)
            if Fraction(a, left) == Fraction(b, right)
        ),
        Fraction(0, 1),
    )


def linear_coefficient(value: int) -> dict[tuple[str, ...], Fraction]:
    scale = Fraction(mobius(value), value)
    return {(f"log({prime})",): scale for prime in factors(value)}


def poly_add(left: dict[tuple[str, ...], Fraction], right: dict[tuple[str, ...], Fraction]) -> dict[tuple[str, ...], Fraction]:
    result = dict(left)
    for key, value in right.items():
        result[key] = result.get(key, Fraction(0)) + value
        if not result[key]:
            del result[key]
    return result


def poly_mul(left: dict[tuple[str, ...], Fraction], right: dict[tuple[str, ...], Fraction]) -> dict[tuple[str, ...], Fraction]:
    result: dict[tuple[str, ...], Fraction] = {}
    for left_key, left_value in left.items():
        for right_key, right_value in right.items():
            key = tuple(sorted(left_key + right_key))
            result[key] = result.get(key, Fraction(0)) + left_value * right_value
    return {key: value for key, value in result.items() if value}


def poly_scale(poly: dict[tuple[str, ...], Fraction], scalar: Fraction) -> dict[tuple[str, ...], Fraction]:
    return {key: scalar * value for key, value in poly.items() if scalar * value}


def cluster_coefficient(family: tuple[int, ...], denominator: int) -> dict[tuple[str, ...], Fraction]:
    result: dict[tuple[str, ...], Fraction] = {}
    for divisor in family:
        if divisor % denominator == 0:
            result = poly_add(result, linear_coefficient(divisor))
    return result


def evaluate(poly: dict[tuple[str, ...], Fraction]) -> float:
    result = 0.0
    for monomial, value in poly.items():
        term = float(value)
        for variable in monomial:
            term *= math.log(int(variable[4:-1]))
        result += term
    return result


def family_check(family: tuple[int, ...], recorded: dict[str, object]) -> None:
    period = lcm(*family)
    reduced = tuple(sorted({h for divisor in family for h in divisors(divisor)}))
    require(recorded["divisors"] == list(family), "family")
    require(recorded["period"] == period, "period")
    require(recorded["reduced_denominators"] == list(reduced), "reduced denominators")
    for denominator in reduced:
        values = row(denominator)
        require(recorded["row_hashes"][str(denominator)] == row_hash(values), f"row hash {denominator}")
        require(recorded["cluster_row_norms"][str(denominator)] == str(row_norm(values, True)), f"row norm {denominator}")
        require(recorded["cluster_scales"][str(denominator)] == str(period * row_norm(values, True)), f"cluster scale {denominator}")
        require(values[0] == 0, f"zero axis {denominator}")
        for divisor in family:
            if divisor % denominator == 0:
                large = row(divisor)
                scale = divisor // denominator
                require(all(large[scale * residue] == values[residue] for residue in range(denominator)), f"dilation {divisor}/{denominator}")
    expected_gram = [[str(gram(left, right, period)) for right in family] for left in family]
    require(recorded["gram_matrix"] == expected_gram, "Gram matrix")
    expected_cross_terms = []
    for left_index, left in enumerate(family):
        for right_index in range(left_index + 1, len(family)):
            right = family[right_index]
            value = gram(left, right, period)
            if value:
                sign = mobius(left) * mobius(right)
                require(value > 0, "cross Gram must be nonnegative")
                expected_cross_terms.append({
                    "left": left,
                    "right": right,
                    "gram": str(value),
                    "coefficient_sign_product": sign,
                    "cross_term_sign": sign,
                })
    require(recorded["cross_terms"] == expected_cross_terms, "cross terms")
    expected_signs = {term["cross_term_sign"] for term in expected_cross_terms}
    require(len(expected_signs) == 1, "cross sign fixture")
    expected_cross_sign = "POSITIVE_EXACT" if next(iter(expected_signs)) > 0 else "NEGATIVE_EXACT"
    require(recorded["cross_energy_sign"] == expected_cross_sign, "cross energy sign")

    gram_poly: dict[tuple[str, ...], Fraction] = {}
    for left_index, left in enumerate(family):
        for right_index, right in enumerate(family):
            gram_poly = poly_add(gram_poly, poly_scale(poly_mul(linear_coefficient(left), linear_coefficient(right)), gram(left, right, period)))

    cluster_poly: dict[tuple[str, ...], Fraction] = {}
    for denominator in reduced:
        scale = period * row_norm(row(denominator), True)
        cluster_poly = poly_add(cluster_poly, poly_scale(poly_mul(cluster_coefficient(family, denominator), cluster_coefficient(family, denominator)), scale))
    require(gram_poly == cluster_poly, "exact cluster factorization")
    require(recorded["cluster_factorization"] is True, "cluster factorization flag")

    direct_poly: dict[tuple[str, ...], Fraction] = {}
    for divisor in family:
        direct_poly = poly_add(direct_poly, poly_scale(poly_mul(linear_coefficient(divisor), linear_coefficient(divisor)), period * row_norm(row(divisor), False)))
    physical = evaluate(cluster_poly)
    direct = evaluate(direct_poly)
    ratio = physical / direct
    require(abs(physical - float(recorded["physical_energy"])) <= 1e-12 * max(1.0, abs(physical)), "physical energy")
    require(abs(direct - float(recorded["direct_sum_energy"])) <= 1e-12 * max(1.0, abs(direct)), "direct energy")
    require(abs(ratio - float(recorded["physical_to_direct_ratio"])) <= 1e-12 * max(1.0, abs(ratio)), "energy ratio")


def check_four_packet() -> None:
    beta = (Fraction(2), Fraction(1))
    weight = (Fraction(1), Fraction(-2))
    powers = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)), (Fraction(-1), Fraction(0)), (Fraction(0), Fraction(-1)))
    total = (Fraction(0), Fraction(0))
    for power in powers:
        real = beta[0] + power[0] * weight[0] - power[1] * weight[1]
        imaginary = beta[1] + power[0] * weight[1] + power[1] * weight[0]
        norm = real * real + imaginary * imaginary
        total = (total[0] + power[0] * norm / 4, total[1] + power[1] * norm / 4)
    expected = (beta[0] * weight[0] + beta[1] * weight[1], beta[1] * weight[0] - beta[0] * weight[1])
    require(total == expected, "four-packet polarization")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        require(CERTIFICATE.is_file(), "certificate missing")
        data = json.loads(CERTIFICATE.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        require(data["schema"] == "TPC214_MOBIUS_FREQUENCY_CLUSTER_CERTIFICATE_V1", "schema")
        require(data["classification"] == "PROVED_STRUCTURAL_L1_MOBIUS_CLUSTER_REDUCTION", "classification")
        require(data["fixture"] == {
            "H": HEIGHT,
            "families": [list(family) for family in FAMILIES],
            "psi": "(1+t^2)^(-2)",
            "q_below_H": True,
            "q_values": list(Q_VALUES),
        }, "fixture")
        require(data["claim_firewall"] == {
            "route_advance": "YES",
            "structural_threshold_a": "PASS",
            "emitter_dilation_covariance": "PROVED_EXACT",
            "reduced_denominator_cluster_factor": "PROVED_EXACT",
            "zero_axis_scope": "PROVED_EXACT",
            "four_packet_polarization": "PROVED_EXACT_LINEAR_EXTENSION",
            "nested_cluster_cancellation": "PROVED_EXACT_FINITE_SIGN",
            "composite_quotient_enhancement": "PROVED_EXACT_FINITE_SIGN",
            "finite_energy_ratios": "NUMERICAL_OBSERVATION",
            "universal_cluster_saving_sign": "REFUTED_SCOPED",
            "literal_v46_asymptotic_cluster_bound": "OPEN",
            "prime_shell_reassembly": "OPEN",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b_strict_1_over_400": "UNPAID",
        }, "claim firewall")
        require(len(data["families"]) == 2, "family count")
        for family, recorded in zip(FAMILIES, data["families"]):
            family_check(family, recorded)
        check_four_packet()
        first_ratio = float(data["families"][0]["physical_to_direct_ratio"])
        second_ratio = float(data["families"][1]["physical_to_direct_ratio"])
        require(first_ratio < 0.60, "cancellation fixture")
        require(second_ratio > 1.20, "enhancement fixture")
    except (CheckFailure, ValueError, KeyError, TypeError) as error:
        print(f"TPC214_INDEPENDENT_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    print("TPC214_INDEPENDENT_CHECK=PASS")
    print("families=2")
    print("cancellation_ratio=", data["families"][0]["physical_to_direct_ratio"])
    print("enhancement_ratio=", data["families"][1]["physical_to_direct_ratio"])
    print("claim_level=PROVED_STRUCTURAL_L1_MOBIUS_CLUSTER_REDUCTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
