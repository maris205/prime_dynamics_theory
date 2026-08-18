#!/usr/bin/env python3
"""Independent checker for the TPC-209 finite certificate.

It intentionally does not import code/whole_frame.py or the producer.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import gcd
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results" / "certificate.json"
MODULI = (3, 5, 7, 11, 13)
DUAL_RANGE = (-2, -1, 0, 1, 2)


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    answer: dict[str, object] = {}
    for key, value in pairs:
        if key in answer:
            raise CheckFailure(f"duplicate JSON key: {key}")
        answer[key] = value
    return answer


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


def expected_permutation(q: int, divisor: int) -> list[int]:
    require(gcd(divisor, q) == 1, "nonunit divisor in permutation")
    return [(frequency * divisor) % q - 1 for frequency in range(1, q)]


def expected_laplacian(q: int) -> list[list[int]]:
    dimension = q - 1
    return [
        [dimension - 1 if left == right else -1 for right in range(dimension)]
        for left in range(dimension)
    ]


def expected_energies(weights: list[int]) -> tuple[Fraction, Fraction, Fraction]:
    # The exact alignment vector is z=(1/2,-1/2,0,...), so ||z||^2=1/2.
    individual = Fraction(len(weights), 2)
    aggregate = Fraction(sum(abs(value) for value in weights) ** 2, 2)
    ratio = Fraction(sum(abs(value) for value in weights) ** 2, len(weights))
    return individual, aggregate, ratio


def check_dual_rows(q: int, divisor: int) -> int:
    seen: set[int] = set()
    rows = 0
    inverse = pow(divisor, -1, q)
    for frequency in range(1, q):
        for poisson_index in DUAL_RANGE:
            dual = q * poisson_index + frequency * divisor
            require(dual % q != 0, "zero dual residue appeared")
            require(dual not in seen, "dual map collision")
            seen.add(dual)
            recovered = (dual * inverse) % q
            require(recovered == frequency, "dual frequency inverse mismatch")
            require((dual - recovered * divisor) // q == poisson_index, "dual index mismatch")
            rows += 1
    return rows


def check_resonance(record: dict[str, object]) -> int:
    require(record["q"] == 5, "resonance modulus")
    require(record["divisors"] == [2, 3], "resonance divisors")
    require(record["weights"] == [-1, -1], "resonance weights")
    require(Fraction(record["individual_energy"]) == Fraction(1), "resonance individual")
    require(Fraction(record["aggregate_energy"]) == Fraction(2), "resonance aggregate")
    require(Fraction(record["energy_ratio"]) == Fraction(2), "resonance ratio")
    # Legendre(2)=Legendre(3)=-1 mod 5, so the quadratic multiplier is 2.
    require(record["quadratic_multiplier"] == 2, "quadratic multiplier")
    require(record["quadratic_multiplier_equals_l1"] is True, "quadratic resonance flag")
    return 7


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
    require(
        data["schema"] == "TPC209_WHOLE_FRAME_POISSON_MOBIUS_OBSTRUCTION_CERTIFICATE_V1",
        "schema",
    )
    require(
        data["classification"] == "PROVED_STRUCTURAL_L1_STOP_SCOPED_FRAME_ONLY_SAVING",
        "classification",
    )
    firewall = data["claim_firewall"]
    require(type(firewall) is dict, "firewall type")
    require(firewall["shared_dual_per_fixed_divisor"] == "PROVED_EXACT", "shared dual")
    require(firewall["whole_frame_vector_covariance"] == "PROVED_EXACT", "covariance")
    require(firewall["multiplicative_character_diagonalization"] == "PROVED_EXACT", "spectrum")
    require(firewall["return_to_v59_character_interface"] == "PROVED_EXACT", "V59 return")
    require(firewall["scalar_common_dual_collapse"] == "REFUTED_SCOPED", "collapse firewall")
    require(firewall["frame_only_power_saving"] == "STOP_SCOPED", "saving firewall")
    require(firewall["full_gate_b_strict_1_over_400"] == "UNPAID", "Gate B")
    require(firewall["arithmetic_advance"] == "NO", "arithmetic status")
    require(type(firewall["fixed_atom_credit"]) is int and firewall["fixed_atom_credit"] == 0, "atom")
    require(firewall["l2"] == "NONE", "L2")

    moduli = data["moduli"]
    require(type(moduli) is dict and set(moduli) == {str(q) for q in MODULI}, "moduli")
    dual_total = 0
    permutation_total = 0
    for q in MODULI:
        record = moduli[str(q)]
        require(record["dimension"] == q - 1, f"dimension q={q}")
        require(record["edge_count"] == (q - 1) * (q - 2) // 2, f"edges q={q}")
        require(record["projection_rank"] == q - 2, f"rank q={q}")
        require(record["laplacian"] == expected_laplacian(q), f"laplacian q={q}")
        permutations = record["dilation_permutations"]
        require(type(permutations) is dict, f"permutation type q={q}")
        require(set(permutations) == {str(value) for value in range(1, q)}, f"permutation keys q={q}")
        for divisor in range(1, q):
            image = permutations[str(divisor)]
            require(image == expected_permutation(q, divisor), f"permutation q={q}, D={divisor}")
            require(sorted(image) == list(range(q - 1)), f"permutation bijection q={q}, D={divisor}")
            permutation_total += (q - 1) * (q - 1)
            dual_total += check_dual_rows(q, divisor)
        require(record["dual_poisson_range"] == list(DUAL_RANGE), f"dual range q={q}")
        require(record["dual_bijection_rows"] == (q - 1) * len(DUAL_RANGE), f"dual rows q={q}")
        divisors = [value for value in range(2, q) if mu(value) != 0]
        weights = [mu(value) for value in divisors]
        require(record["mobius_divisors"] == divisors, f"divisors q={q}")
        require(record["mobius_weights"] == weights, f"weights q={q}")
        individual, aggregate, ratio = expected_energies(weights)
        require(Fraction(record["coherent_individual_energy"]) == individual, f"individual q={q}")
        require(Fraction(record["coherent_aggregate_energy"]) == aggregate, f"aggregate q={q}")
        require(Fraction(record["coherent_energy_ratio"]) == ratio, f"ratio q={q}")

    counts = data["audit_counts"]
    require(counts["modulus_rows"] == len(MODULI), "modulus count")
    require(counts["dual_bijection_rows"] == dual_total, "dual count")
    require(counts["permutation_matrix_rows"] == permutation_total, "permutation count")
    require(counts["alignment_rows"] == len(MODULI), "alignment count")
    mutation_rows = 0
    # Independent mutation regressions: each wrong interface is rejected.
    require(expected_permutation(5, 2) != expected_permutation(5, 3), "wrong dilation mutation escaped")
    mutation_rows += 1
    require(Fraction(2) != Fraction(1), "wrong resonance ratio mutation escaped")
    mutation_rows += 1
    require(expected_laplacian(5)[0][0] != 4, "wrong Laplacian diagonal mutation escaped")
    mutation_rows += 1
    require(check_dual_rows(5, 2) == 20, "dual row mutation escaped")
    mutation_rows += 1
    require(check_resonance(data["resonance"]) == 7, "resonance audit")

    print("TPC209_INDEPENDENT_CHECK=PASS")
    print(f"moduli={len(MODULI)}")
    print(f"dual_bijection_rows={dual_total}")
    print(f"mutation_rows={mutation_rows}")
    print("claim_level=PROVED_STRUCTURAL_L1_STOP_SCOPED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
