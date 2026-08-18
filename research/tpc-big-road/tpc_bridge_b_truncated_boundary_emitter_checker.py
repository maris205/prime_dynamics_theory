#!/usr/bin/env python3
"""Independent release checker for the TPC-212 boundary/emitter bridge."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / "research/tpc-big-road/bridge_b_truncated_boundary_emitter.md"
PAPER = ROOT / "papers/tpc-212-truncated-boundary-emitter"
CERTIFICATE = PAPER / "results/certificate.json"

REGISTRY = (
    "TPC212_MAXIMUM_CLAIM = EXACT_TRUNCATED_BOOLEAN_BOUNDARY_AND_RECIPROCAL_EMITTER_GRAM_OBSTRUCTION",
    "TPC212_ROUTE_ADVANCE = YES",
    "TPC212_STRUCTURAL_THRESHOLD_A = PASS",
    "TPC212_CUT_ENDPOINT_LEAKAGE = PROVED_EXACT",
    "TPC212_BOUNDARY_DECOMPOSITION = PROVED_EXACT",
    "TPC212_RECIPROCAL_COLLISION = PROVED_EXACT_FINITE",
    "TPC212_EMITTER_GRAM = PROVED_EXACT_BLOCK_DIAGONAL",
    "TPC212_EMITTER_ONLY_UNIVERSAL_SAVING = REFUTED_SCOPED",
    "TPC212_LITERAL_PHYSICAL_BOUNDARY_BOUND = OPEN",
    "TPC212_PHYSICAL_CROSS_DIVISOR_GRAM_BOUND = OPEN",
    "TPC212_ARITHMETIC_ADVANCE = NO",
    "TPC212_FIXED_ATOM_CREDIT = 0",
    "TPC212_L2 = NONE",
    "TPC212_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID",
    "TPC212_TPC_TRIGGER = true",
)

REQUIRED = (
    "README.md",
    "PAPER_PLAN.md",
    "paper/main.tex",
    "paper/references.bib",
    "paper/paper.pdf",
    "code/boundary_emitter.py",
    "experiments/run_certificate.py",
    "experiments/independent_checker.py",
    "experiments/boundary_sanity.py",
    "results/certificate.json",
    "notes/theorem_ledger.md",
    "notes/source_lock.md",
    "notes/route_evaluation.md",
)


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def check_layout() -> int:
    require(PROOF.is_file(), "bridge proof missing")
    proof = PROOF.read_text(encoding="utf-8")
    for row in REGISTRY:
        require(row in proof, f"registry row missing: {row}")
    require("signed Boolean endpoint incidence" in proof, "incidence theorem missing")
    require("collision identity" in proof, "collision theorem missing")
    for relative in REQUIRED:
        require((PAPER / relative).is_file(), f"artifact missing: {relative}")
    pdf = (PAPER / "paper/paper.pdf").read_bytes()
    require(pdf.startswith(b"%PDF-"), "PDF header")
    require(len(pdf) > 100_000, "PDF unexpectedly small")
    return len(REGISTRY) + len(REQUIRED) + 3


def check_certificate() -> tuple[int, int, int]:
    require(CERTIFICATE.is_file(), "certificate missing")
    data = json.loads(
        CERTIFICATE.read_text(encoding="utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=lambda token: (_ for _ in ()).throw(CheckFailure(token)),
    )
    require(data["schema"] == "TPC212_TRUNCATED_BOUNDARY_EMITTER_CERTIFICATE_V1", "schema")
    require(data["classification"] == "PROVED_STRUCTURAL_L1_STOP_SCOPED_BOUNDARY_EMITTER", "classification")
    require(data["modeling_choice"] == "UNIT_RECIPROCAL_WEIGHTS_PSI_EQUALS_ONE_FINITE_FIXTURE", "fixture")
    firewall = data["claim_firewall"]
    expected_firewall = {
        "route_advance": "YES",
        "structural_threshold_a": "PASS",
        "cut_endpoint_leakage": "PROVED_EXACT",
        "boundary_decomposition": "PROVED_EXACT",
        "reciprocal_collision": "PROVED_EXACT_FINITE",
        "emitter_gram": "PROVED_EXACT_BLOCK_DIAGONAL",
        "emitter_only_universal_saving": "REFUTED_SCOPED",
        "literal_physical_boundary_bound": "OPEN",
        "physical_cross_divisor_gram_bound": "OPEN",
        "arithmetic_advance": "NO",
        "fixed_atom_credit": 0,
        "l2": "NONE",
        "full_gate_b_strict_1_over_400": "UNPAID",
    }
    require(firewall == expected_firewall, "claim firewall")
    boundaries = data["boundary_cases"]
    require(len(boundaries) == 4, "boundary case count")
    first = boundaries[0]
    require(first["primes"] == [5, 7], "first boundary primes")
    require(first["lower"] == 5 and first["upper"] == 35, "first boundary cut")
    require(first["active_divisors"] == [7, 35], "first active divisors")
    require(first["active_endpoint_incidence"] == [1, 0], "first leakage")
    require(all(record["boundary_identity"] is True for record in boundaries), "boundary flags")
    boundary_coordinates = sum(int(record["profile_coordinate_count"]) for record in boundaries)
    require(boundary_coordinates == 5810, "boundary coordinate count")

    emitters = data["emitter_cases"]
    require(len(emitters) == 3, "emitter case count")
    require(all(record["unit_weight_alignment"] is True for record in emitters), "fixture alignment flags")
    require(all(record["direct_sum_gram_rank"] == len(record["divisors"]) for record in emitters), "Gram ranks")
    ratios = [record["coherent_to_diagonal_ratio"] for record in emitters]
    require(ratios == ["2", "4", "3"], "alignment ratios")
    divisor_rows = sum(len(record["divisors"]) for record in emitters)
    require(divisor_rows == 9, "emitter divisor count")
    counts = data["audit_counts"]
    require(counts == {
        "boundary_cases": 4,
        "boundary_profile_coordinate_rows": 5810,
        "emitter_cases": 3,
        "emitter_divisor_rows": 9,
    }, "audit counts")
    contract = data["theorem_contract"]
    require(contract["literal_physical_boundary_bound"] == "OPEN", "physical boundary contract")
    require(contract["prime_shell_reassembly"] == "OPEN", "prime shell contract")
    return len(boundaries), boundary_coordinates, divisor_rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")
    try:
        layout_rows = check_layout()
        boundary_cases, boundary_coordinates, divisor_rows = check_certificate()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError) as error:
        print(f"TPC212 BRIDGE CHECK=FAIL {error}", file=sys.stderr)
        return 1
    print("TPC212_BRIDGE_CHECK=PASS")
    print(f"layout_registry_rows={layout_rows}")
    print(f"boundary_cases={boundary_cases}")
    print(f"boundary_profile_coordinate_rows={boundary_coordinates}")
    print(f"emitter_divisor_rows={divisor_rows}")
    print("route_advance=YES")
    print("literal_physical_boundary_bound=OPEN")
    print("arithmetic_advance=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
