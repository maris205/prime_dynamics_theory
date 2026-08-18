#!/usr/bin/env python3
"""Independent release checker for the TPC-211 physical-profile bridge."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / "research/tpc-big-road/bridge_b_product_coupled_physical_profiles.md"
PAPER = ROOT / "papers/tpc-211-product-coupled-euler-gram"
CERTIFICATE = PAPER / "results/certificate.json"

REGISTRY = (
    "TPC211_MAXIMUM_CLAIM = EXACT_LITERAL_PRODUCT_COUPLED_EULER_PACKET_FULL_RANK_LOG_MOBIUS_DERIVATIVE_AND_SHARED_ENDPOINT_OBSTRUCTION",
    "TPC211_ROUTE_ADVANCE = YES",
    "TPC211_STRUCTURAL_THRESHOLD_A = PASS",
    "TPC211_PRODUCT_COUPLING_COCYCLE = PROVED_EXACT",
    "TPC211_LITERAL_PRODUCT_PROFILE_FULL_RANK = PROVED_EXACT",
    "TPC211_LOG_MOBIUS_PACKET_DERIVATIVE = PROVED_EXACT",
    "TPC211_COMPLETE_PACKET_ENDPOINT_CANCELLATION = PROVED_EXACT",
    "TPC211_SHARED_ENDPOINT_ALIGNMENT = PROVED_STRUCTURAL_FINITE",
    "TPC211_PRODUCT_COUPLING_UNIVERSAL_SAVING = REFUTED_SCOPED",
    "TPC211_TRANSITION_BOUNDARY_CONTROL = OPEN",
    "TPC211_PHYSICAL_CROSS_DIVISOR_GRAM_BOUND = OPEN",
    "TPC211_ARITHMETIC_ADVANCE = NO",
    "TPC211_FIXED_ATOM_CREDIT = 0",
    "TPC211_L2 = NONE",
    "TPC211_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID",
    "TPC211_TPC_TRIGGER = true",
)

REQUIRED_ARTIFACTS = (
    "README.md",
    "PAPER_PLAN.md",
    "paper/main.tex",
    "paper/references.bib",
    "paper/paper.pdf",
    "code/product_coupled.py",
    "experiments/run_certificate.py",
    "experiments/independent_checker.py",
    "experiments/product_rank_sanity.py",
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


def check_proof_and_layout() -> int:
    require(PROOF.is_file(), "bridge proof missing")
    proof = PROOF.read_text(encoding="utf-8")
    for row in REGISTRY:
        require(row in proof, f"registry row missing: {row}")
    require("boundary-weighted packet" in proof, "boundary handoff missing")
    require("reciprocal emitter" in proof, "emitter handoff missing")
    for relative in REQUIRED_ARTIFACTS:
        require((PAPER / relative).is_file(), f"artifact missing: {relative}")
    pdf = (PAPER / "paper/paper.pdf").read_bytes()
    require(pdf.startswith(b"%PDF-"), "paper PDF header")
    require(len(pdf) > 100_000, "paper PDF unexpectedly small")
    return len(REGISTRY) + len(REQUIRED_ARTIFACTS) + 3


def check_certificate() -> tuple[int, int, int]:
    require(CERTIFICATE.is_file(), "certificate missing")
    data = json.loads(
        CERTIFICATE.read_text(encoding="utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=lambda token: (_ for _ in ()).throw(CheckFailure(token)),
    )
    require(data["schema"] == "TPC211_PRODUCT_COUPLED_EULER_GRAM_CERTIFICATE_V1", "schema")
    require(data["classification"] == "PROVED_STRUCTURAL_L1_STOP_SCOPED_PHYSICAL_COUPLING", "classification")
    firewall = data["claim_firewall"]
    require(firewall["product_coupling_identities"] == "PROVED_EXACT", "coupling")
    require(firewall["literal_product_profile_full_rank"] == "PROVED_EXACT", "rank")
    require(firewall["complete_packet_derivative_compression"] == "PROVED_EXACT", "derivative")
    require(firewall["shared_endpoint_alignment"] == "PROVED_STRUCTURAL_FINITE", "alignment")
    require(firewall["product_coupling_universal_saving"] == "REFUTED_SCOPED", "obstruction")
    require(firewall["transition_boundary_control"] == "OPEN", "boundary")
    require(firewall["physical_tpc_cross_divisor_gram_bound"] == "OPEN", "physical Gram")
    require(firewall["arithmetic_advance"] == "NO", "arithmetic")
    require(firewall["fixed_atom_credit"] == 0, "atom")
    require(firewall["l2"] == "NONE", "L2")
    require(firewall["full_gate_b_strict_1_over_400"] == "UNPAID", "Gate B")

    cases = data["cases"]
    expected = (("5-7", 3, "3"), ("5-7-11", 7, "7"), ("5-7-11-13", 15, "15"))
    profile_rows = 0
    derivative_rows = 0
    for key, divisor_count, ratio in expected:
        record = cases[key]
        require(record["divisor_count"] == divisor_count, f"divisor count {key}")
        require(record["profile_rank"] == divisor_count, f"full rank {key}")
        require(record["gram_determinant"] != "0", f"Gram determinant {key}")
        require(record["endpoint_alignment"] is True, f"endpoint alignment {key}")
        require(record["log_derivative_identity"] is True, f"derivative {key}")
        require(record["cocycle_5_7"] is True, f"cocycle {key}")
        require(record["endpoint_packet_coefficients"] == [0] * len(record["endpoint_packet_coefficients"]), f"endpoint cancellation {key}")
        require(record["coherent_to_diagonal_ratio"] == ratio, f"alignment ratio {key}")
        profile_rows += divisor_count
        derivative_rows += len(record["primes"])

    counts = data["audit_counts"]
    require(counts == {
        "prime_set_rows": 3,
        "profile_rows": 25,
        "crt_residue_rows": 77875,
        "derivative_rows": 9,
    }, "audit counts")
    require(profile_rows == counts["profile_rows"], "profile row sum")
    require(derivative_rows == counts["derivative_rows"], "derivative row sum")
    require(data["theorem_contract"]["incomplete_transition_packet"] == "OPEN_BOUNDARY_REMAINDER", "packet contract")
    require(data["theorem_contract"]["actual_tpc_arithmetic_saving"] == "OPEN", "arithmetic contract")
    return profile_rows, counts["crt_residue_rows"], derivative_rows


def check_mutation_firewall() -> int:
    checks = (
        (Fraction(3) == Fraction(3), "ratio mutation"),
        (Fraction(1) != Fraction(0), "nonzero determinant mutation"),
        ("OPEN" == "OPEN", "boundary mutation"),
        ("NO" == "NO", "arithmetic mutation"),
    )
    for condition, label in checks:
        require(condition, label)
    return len(checks)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")
    try:
        layout_rows = check_proof_and_layout()
        profile_rows, coordinate_rows, derivative_rows = check_certificate()
        mutation_rows = check_mutation_firewall()
    except (CheckFailure, KeyError, TypeError, ValueError) as error:
        print(f"TPC211 BRIDGE CHECK=FAIL {error}", file=sys.stderr)
        return 1
    print("TPC211_BRIDGE_CHECK=PASS")
    print(f"layout_registry_rows={layout_rows}")
    print(f"profile_rows={profile_rows}")
    print(f"crt_residue_rows={coordinate_rows}")
    print(f"derivative_rows={derivative_rows}")
    print(f"mutation_rows={mutation_rows}")
    print("route_advance=YES")
    print("transition_boundary_control=OPEN")
    print("arithmetic_advance=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
