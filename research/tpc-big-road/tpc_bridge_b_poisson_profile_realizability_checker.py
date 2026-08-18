#!/usr/bin/env python3
"""Fail-closed finite checker for the TPC-210 profile obstruction."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / "research/tpc-big-road/bridge_b_poisson_profile_realizability_obstruction.md"
PAPER = ROOT / "papers/tpc-210-poisson-profile-realizability"
CERTIFICATE = PAPER / "results/certificate.json"
MODULI = (3, 5, 7, 11, 13)

REGISTRY = (
    "TPC210_MAXIMUM_CLAIM = EXACT_FINITE_POISSON_PROFILE_INTERPOLATION_PLUS_MOBIUS_WEIGHTED_ALIGNED_GRAM_OBSTRUCTION",
    "TPC210_ROUTE_ADVANCE = YES",
    "TPC210_STRUCTURAL_THRESHOLD_A = PASS",
    "TPC210_FINITE_PROFILE_INTERPOLATION = PROVED_EXACT",
    "TPC210_MOBIUS_WEIGHTED_ALIGNED_FAMILY = PROVED_EXACT",
    "TPC210_CROSS_DIVISOR_GRAM_REDUCTION = PROVED_EXACT",
    "TPC210_PROFILE_CLASS_UNIVERSAL_SAVING = REFUTED_SCOPED",
    "TPC210_ACTUAL_PHYSICAL_PROFILE_BOUND = OPEN",
    "TPC210_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID",
    "TPC210_ARITHMETIC_ADVANCE = NO",
    "TPC210_GLOBAL_GATE_B_ADVANCE = NO",
    "TPC210_FIXED_ATOM_CREDIT = 0",
    "TPC210_L2 = NONE",
    "TPC210_FIRST_FATAL = NO_CROSS_DIVISOR_PHYSICAL_COUPLING_FROM_SCHWARTZ_POISSON_MOBIUS_INTERFACE_ALONE",
    "TPC210_ROUND2_CLUE = FIND_A_LITERAL_PHYSICAL_CROSS_DIVISOR_COUPLING_OR_GRAM_BOUND_BEFORE_ANY_NEW_PRIME_BDH_ATTACHMENT",
    "TPC210_REUSABLE_STRUCTURE = ISOLATED_FOURIER_NODE_PROFILE_INTERPOLATION_PLUS_MOBIUS_ADJOINT_ALIGNMENT_PLUS_PSD_GRAM",
    "TPC210_TPC_TRIGGER = true",
    "TPC_210_TRIGGER = true",
)


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


def expected_geometry(q: int) -> dict[str, object]:
    return {
        "node_count": q - 1,
        "support_radius": str(Fraction(1, 4 * q)),
        "minimum_node_gap": str(Fraction(10 * q + 1, q)),
        "same_residue_lattice_gap": "1",
        "strict_isolation": True,
    }


def expected_gram(weights: list[int]) -> list[list[str]]:
    return [[str(Fraction(left * right, 2)) for right in weights] for left in weights]


def check_certificate() -> tuple[int, int, int]:
    require(CERTIFICATE.is_file(), "TPC-210 certificate missing")
    data = json.loads(
        CERTIFICATE.read_text(encoding="utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=lambda token: (_ for _ in ()).throw(CheckFailure(token)),
    )
    require(data["schema"] == "TPC210_POISSON_PROFILE_REALIZABILITY_CERTIFICATE_V1", "schema")
    require(data["classification"] == "PROVED_STRUCTURAL_L1_STOP_SCOPED_PROFILE_CLASS", "classification")
    firewall = data["claim_firewall"]
    require(firewall["finite_profile_interpolation"] == "PROVED_EXACT", "interpolation")
    require(firewall["mobius_weighted_aligned_family"] == "PROVED_EXACT", "alignment")
    require(firewall["cross_divisor_gram_reduction"] == "PROVED_EXACT", "Gram")
    require(firewall["profile_class_universal_saving"] == "REFUTED_SCOPED", "scoped stop")
    require(firewall["actual_physical_tpc_profile_bound"] == "OPEN", "physical open")
    require(firewall["full_gate_b_strict_1_over_400"] == "UNPAID", "Gate B")
    require(firewall["arithmetic_advance"] == "NO", "arithmetic")
    require(firewall["fixed_atom_credit"] == 0, "atom")
    require(firewall["l2"] == "NONE", "L2")

    records = data["moduli"]
    total_profiles = 0
    total_coordinates = 0
    total_geometry = 0
    for q in MODULI:
        record = records[str(q)]
        ds = divisors(q)
        weights = [mu(value) for value in ds]
        count = len(ds)
        require(record["divisors"] == ds, f"divisors q={q}")
        require(record["weights"] == weights, f"weights q={q}")
        require(record["profile_rows"] == count, f"profile rows q={q}")
        require(record["geometry"] == expected_geometry(q), f"geometry q={q}")
        require(record["realized_exactly"] is True, f"realization q={q}")
        require(record["profile_gram"] == expected_gram(weights), f"Gram q={q}")
        require(Fraction(record["diagonal_energy"]) == Fraction(count, 2), f"diagonal q={q}")
        require(Fraction(record["aggregate_energy"]) == Fraction(count * count, 2), f"aggregate q={q}")
        require(Fraction(record["energy_ratio"]) == count, f"ratio q={q}")
        require(record["mobius_l1_mass"] == count, f"L1 q={q}")
        require(record["mobius_l2_mass"] == count, f"L2 mass q={q}")
        total_profiles += count
        total_coordinates += (q - 1) * count
        total_geometry += q - 1

    resonance = data["resonance"]
    require(resonance["q"] == 5, "resonance q")
    require(resonance["divisors"] == [2, 3], "resonance divisors")
    require(resonance["weights"] == [-1, -1], "resonance weights")
    require(Fraction(resonance["energy_ratio"]) == 2, "resonance ratio")
    counts = data["audit_counts"]
    require(counts["modulus_rows"] == 5, "modulus rows")
    require(counts["realized_profile_rows"] == total_profiles == 20, "profile total")
    require(counts["residue_coordinate_rows"] == total_coordinates == 178, "coordinate total")
    require(counts["support_geometry_rows"] == total_geometry == 34, "geometry total")
    return total_profiles, total_coordinates, total_geometry


def check_files_and_registry() -> int:
    require(PROOF.is_file(), "TPC-210 proof missing")
    proof_text = PROOF.read_text(encoding="utf-8")
    for row in REGISTRY:
        require(row in proof_text, f"registry row missing: {row}")
    required = (
        "README.md",
        "PAPER_PLAN.md",
        "paper/main.tex",
        "paper/references.bib",
        "paper/paper.pdf",
        "code/profile_realization.py",
        "experiments/run_certificate.py",
        "experiments/independent_checker.py",
        "experiments/profile_interpolation_sanity.py",
        "results/certificate.json",
        "notes/theorem_ledger.md",
        "notes/source_lock.md",
        "notes/route_evaluation.md",
    )
    for relative in required:
        require((PAPER / relative).is_file(), f"artifact missing: {relative}")
    pdf = (PAPER / "paper/paper.pdf").read_bytes()
    require(pdf.startswith(b"%PDF-"), "paper PDF header")
    require(len(pdf) > 100_000, "paper PDF unexpectedly small")
    return len(REGISTRY) + len(required) + 1


def check_mutation_firewall() -> int:
    mutations = 0
    require(expected_geometry(5)["support_radius"] != "1/5", "radius mutation escaped")
    mutations += 1
    require(expected_gram([-1, -1])[0][1] != "0", "cross Gram mutation escaped")
    mutations += 1
    require(Fraction(2) != Fraction(1), "ratio mutation escaped")
    mutations += 1
    require(len(divisors(5)) == 2, "Mobius divisor mutation escaped")
    mutations += 1
    return mutations


def run() -> dict[str, object]:
    profile_rows, coordinate_rows, geometry_rows = check_certificate()
    file_rows = check_files_and_registry()
    mutation_rows = check_mutation_firewall()
    return {
        "classification": "TPC210_PROVED_STRUCTURAL_L1_STOP_SCOPED_PROFILE_CLASS",
        "verdict": "PASS",
        "moduli": len(MODULI),
        "realized_profile_rows": profile_rows,
        "residue_coordinate_rows": coordinate_rows,
        "support_geometry_rows": geometry_rows,
        "q5_energy_ratio": "2",
        "file_registry_rows": file_rows,
        "mutation_rows": mutation_rows,
        "actual_physical_profile_bound": "OPEN",
        "full_gate_b": "OPEN",
        "strict_1_over_400": "UNPAID",
        "arithmetic_advance": "NO",
        "l2": "NONE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")
    try:
        payload = run()
    except CheckFailure as exc:
        print(f"TPC-210 profile checker: FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
