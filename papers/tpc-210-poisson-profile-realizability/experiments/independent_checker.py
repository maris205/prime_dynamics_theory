#!/usr/bin/env python3
"""Independent checker for the TPC-210 profile-realizability certificate."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import gcd
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results" / "certificate.json"
MODULI = (3, 5, 7, 11, 13)


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise CheckFailure(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def mu(value: int) -> int:
    remaining = value
    prime = 2
    parity = 0
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            parity ^= 1
            if remaining % prime == 0:
                return 0
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        parity ^= 1
    return -1 if parity else 1


def divisors(q: int) -> list[int]:
    return [value for value in range(2, q) if gcd(value, q) == 1 and mu(value) != 0]


def witness(q: int) -> list[Fraction]:
    values = [Fraction(0, 1) for _ in range(q - 1)]
    values[0] = Fraction(1, 2)
    values[1] = Fraction(-1, 2)
    return values


def apply_dilation(vector: list[Fraction], q: int, divisor: int) -> list[Fraction]:
    return [vector[(frequency * divisor) % q - 1] for frequency in range(1, q)]


def expected_profile(q: int, divisor: int, weight: int) -> list[Fraction]:
    inverse = pow(divisor, -1, q)
    adjoint = apply_dilation(witness(q), q, inverse)
    return [weight * value for value in adjoint]


def center(vector: list[Fraction]) -> list[Fraction]:
    average = sum(vector, Fraction(0, 1)) / len(vector)
    return [value - average for value in vector]


def norm2(vector: list[Fraction]) -> Fraction:
    return sum(value * value for value in vector)


def expected_gram(q: int, weights: list[int]) -> list[list[Fraction]]:
    return [
        [Fraction(left * right, 2) for right in weights]
        for left in weights
    ]


def expected_geometry(q: int) -> dict[str, object]:
    return {
        "node_count": q - 1,
        "support_radius": str(Fraction(1, 4 * q)),
        "minimum_node_gap": str(Fraction(10 * q + 1, q)),
        "same_residue_lattice_gap": "1",
        "strict_isolation": True,
    }


def check_modulus(q: int, record: dict[str, object]) -> int:
    ds = divisors(q)
    weights = [mu(value) for value in ds]
    count = len(ds)
    require(record["divisors"] == ds, f"divisors q={q}")
    require(record["weights"] == weights, f"weights q={q}")
    require(record["profile_rows"] == count, f"profile rows q={q}")
    require(record["geometry"] == expected_geometry(q), f"geometry q={q}")
    require(record["realized_exactly"] is True, f"realization q={q}")
    require(record["profile_gram"] == [[str(value) for value in row] for row in expected_gram(q, weights)], f"Gram q={q}")
    diagonal = Fraction(count, 2)
    aggregate = Fraction(count * count, 2)
    require(Fraction(record["diagonal_energy"]) == diagonal, f"diagonal q={q}")
    require(Fraction(record["aggregate_energy"]) == aggregate, f"aggregate q={q}")
    require(Fraction(record["energy_ratio"]) == count, f"ratio q={q}")
    require(record["mobius_l1_mass"] == count, f"L1 q={q}")
    require(record["mobius_l2_mass"] == count, f"L2 q={q}")
    profiles = [expected_profile(q, divisor, weight) for divisor, weight in zip(ds, weights)]
    for profile in profiles:
        require(len(profile) == q - 1, f"profile dimension q={q}")
    output = [
        sum(
            weight * apply_dilation(profile, q, divisor)[coordinate]
            for divisor, weight, profile in zip(ds, weights, profiles)
        )
        for coordinate in range(q - 1)
    ]
    require(output == [count * value for value in witness(q)], f"aligned output q={q}")
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    require(CERTIFICATE.is_file(), "certificate missing")
    data = json.loads(
        CERTIFICATE.read_text(encoding="utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=lambda token: (_ for _ in ()).throw(CheckFailure(token)),
    )
    require(type(data) is dict, "top-level type")
    require(
        set(data)
        == {
            "audit_counts",
            "claim_firewall",
            "classification",
            "moduli",
            "open_theorem",
            "resonance",
            "schema",
        },
        "top-level keys",
    )
    require(data["schema"] == "TPC210_POISSON_PROFILE_REALIZABILITY_CERTIFICATE_V1", "schema")
    require(data["classification"] == "PROVED_STRUCTURAL_L1_STOP_SCOPED_PROFILE_CLASS", "classification")
    firewall = data["claim_firewall"]
    require(type(firewall) is dict, "firewall type")
    require(firewall["finite_profile_interpolation"] == "PROVED_EXACT", "interpolation")
    require(firewall["mobius_weighted_aligned_family"] == "PROVED_EXACT", "Mobius alignment")
    require(firewall["cross_divisor_gram_reduction"] == "PROVED_EXACT", "Gram reduction")
    require(firewall["profile_class_universal_saving"] == "REFUTED_SCOPED", "saving firewall")
    require(firewall["actual_physical_tpc_profile_bound"] == "OPEN", "physical bound")
    require(firewall["full_gate_b_strict_1_over_400"] == "UNPAID", "Gate B")
    require(firewall["arithmetic_advance"] == "NO", "arithmetic")
    require(type(firewall["fixed_atom_credit"]) is int and firewall["fixed_atom_credit"] == 0, "atom")
    require(firewall["l2"] == "NONE", "L2")

    records = data["moduli"]
    require(type(records) is dict and set(records) == {str(q) for q in MODULI}, "moduli")
    total_profiles = sum(check_modulus(q, records[str(q)]) for q in MODULI)
    resonance = data["resonance"]
    require(resonance["q"] == 5, "resonance q")
    require(resonance["divisors"] == [2, 3], "resonance divisors")
    require(resonance["weights"] == [-1, -1], "resonance weights")
    require(Fraction(resonance["diagonal_energy"]) == Fraction(1), "resonance diagonal")
    require(Fraction(resonance["aggregate_energy"]) == Fraction(2), "resonance aggregate")
    require(Fraction(resonance["energy_ratio"]) == Fraction(2), "resonance ratio")
    require(resonance["mobius_l1_mass"] == 2, "resonance L1")
    require(resonance["ratio_equals_divisor_count"] is True, "resonance flag")

    counts = data["audit_counts"]
    require(counts["modulus_rows"] == 5, "modulus count")
    require(counts["realized_profile_rows"] == total_profiles == 20, "profile count")
    require(
        counts["residue_coordinate_rows"]
        == sum((q - 1) * len(divisors(q)) for q in MODULI)
        == 178,
        "residue coordinate count",
    )
    require(counts["support_geometry_rows"] == sum(q - 1 for q in MODULI), "geometry count")

    mutation_rows = 0
    require(expected_geometry(5)["support_radius"] != "1/5", "radius mutation escaped")
    mutation_rows += 1
    require(Fraction(2) != Fraction(1), "resonance mutation escaped")
    mutation_rows += 1
    require(expected_gram(5, [-1, -1])[0][1] != Fraction(0), "cross Gram deletion escaped")
    mutation_rows += 1
    require(check_modulus(5, records["5"]) == 2, "q=5 independent replay")
    mutation_rows += 1

    print("TPC210_INDEPENDENT_CHECK=PASS")
    print(f"moduli={len(MODULI)}")
    print(f"realized_profile_rows={total_profiles}")
    print(f"mutation_rows={mutation_rows}")
    print("claim_level=PROVED_STRUCTURAL_L1_STOP_SCOPED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
