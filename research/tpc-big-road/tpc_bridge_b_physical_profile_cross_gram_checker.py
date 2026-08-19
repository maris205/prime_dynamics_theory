#!/usr/bin/env python3
"""Independent release checker for the TPC-213 physical coupling bridge."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from math import gcd, lcm
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / "research/tpc-big-road/bridge_b_physical_profile_cross_gram.md"
PAPER = ROOT / "papers/tpc-213-physical-profile-cross-gram"
CERTIFICATE = PAPER / "results/certificate.json"

REGISTRY = (
    "TPC213_MAXIMUM_CLAIM = EXACT_COMMON_SOURCE_PROFILE_PULLBACK_AND_FINITE_CROSS_DIVISOR_GRAM",
    "TPC213_ROUTE_ADVANCE = YES",
    "TPC213_STRUCTURAL_THRESHOLD_A = PASS",
    "TPC213_PHYSICAL_PROFILE_EMITTER_PULLBACK = PROVED_EXACT",
    "TPC213_RESIDUE_LIFT_GCD_ALIASING = PROVED_EXACT",
    "TPC213_CROSS_DIVISOR_FREQUENCY_GRAM = PROVED_EXACT_FINITE",
    "TPC213_PHYSICAL_DIRECT_SUM_REPLACEMENT = REFUTED_SCOPED",
    "TPC213_LITERAL_V46_ASYMPTOTIC_GRAM_BOUND = OPEN",
    "TPC213_PRIME_SHELL_REASSEMBLY = OPEN",
    "TPC213_ARITHMETIC_ADVANCE = NO",
    "TPC213_FIXED_ATOM_CREDIT = 0",
    "TPC213_L2 = NONE",
    "TPC213_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID",
    "TPC213_TPC_TRIGGER = true",
)

REQUIRED = (
    "README.md",
    "PAPER_PLAN.md",
    "PROOF_PACKAGE.md",
    "paper/main.tex",
    "paper/references.bib",
    "paper/paper.pdf",
    "code/profile_cross_gram.py",
    "experiments/run_certificate.py",
    "experiments/independent_checker.py",
    "experiments/coupling_sanity.py",
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


def occupancy(divisor: int, q_values: tuple[int, ...], H: int) -> tuple[int, ...]:
    result = [0 for _ in range(divisor)]
    for q in q_values:
        require(gcd(q, divisor) == 1, "nonunit q")
        limit = divisor * q // H
        for m in range(-limit, limit + 1):
            if m:
                result[(m * pow(q, -1, divisor)) % divisor] += 1
    return tuple(result)


def intersections(left: int, right: int, a: tuple[int, ...], b: tuple[int, ...]) -> tuple[tuple[int, int, int, int], ...]:
    return tuple(
        (r, s, a[r], b[s])
        for r in range(left)
        for s in range(right)
        if Fraction(r, left) == Fraction(s, right) and a[r] and b[s]
    )


def check_layout() -> int:
    require(PROOF.is_file(), "bridge proof missing")
    proof = PROOF.read_text(encoding="utf-8")
    for row in REGISTRY:
        require(row in proof, f"registry row missing: {row}")
    require("Common-source pullback theorem" in proof, "pullback theorem missing")
    require("frequency-intersection" in proof, "frequency Gram theorem missing")
    require("gcd/lcm" in proof, "CRT theorem missing")
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
    require(data["schema"] == "TPC213_PHYSICAL_PROFILE_CROSS_GRAM_CERTIFICATE_V1", "schema")
    require(data["classification"] == "PROVED_STRUCTURAL_L1_CROSS_DIVISOR_COUPLING", "classification")
    require(data["modeling_choice"] == "UNIT_RECIPROCAL_WEIGHTS_PSI_EQUALS_ONE_NO_LOG_PREFactor", "modeling choice")
    fixture = data["fixture"]
    require(fixture["divisors"] == [5, 7, 35], "divisor fixture")
    require(fixture["support"] == [0, 34, 35], "support fixture")
    require(fixture["q_values"] == [11, 13, 17] and fixture["H"] == 40, "emitter fixture")
    require(data["joint_lift"] == {
        "row_count": 47,
        "column_count": 35,
        "rank": 35,
        "domain_kernel_dimension": 0,
        "codomain_dependency_dimension": 12,
    }, "joint lift")
    firewall = data["claim_firewall"]
    require(firewall == {
        "route_advance": "YES",
        "structural_threshold_a": "PASS",
        "physical_profile_emitter_pullback": "PROVED_EXACT",
        "residue_lift_gcd_aliasing": "PROVED_EXACT",
        "cross_divisor_frequency_gram": "PROVED_EXACT_FINITE",
        "physical_direct_sum_replacement": "REFUTED_SCOPED",
        "literal_v46_asymptotic_gram_bound": "OPEN",
        "prime_shell_reassembly": "OPEN",
        "arithmetic_advance": "NO",
        "fixed_atom_credit": 0,
        "l2": "NONE",
        "full_gate_b_strict_1_over_400": "UNPAID",
    }, "claim firewall")
    cross = data["cross_gram_cases"]
    require(len(cross) == 3, "cross case count")
    require(
        [(row["left"], row["right"], row["cross_gram"]) for row in cross]
        == [(5, 7, 0), (5, 35, 560), (7, 35, 770)],
        "cross Gram values",
    )
    require(sum(row["cross_gram_nonzero"] for row in cross) == 2, "nonzero cross count")
    require(data["audit_counts"] == {
        "delta_profile_rows": 3,
        "delta_profile_coordinates": 47,
        "lift_cases": 3,
        "emitter_cases": 3,
        "cross_gram_cases": 3,
    }, "audit counts")
    return len(data["delta_profiles"]), 35, sum(row["cross_gram_nonzero"] for row in cross)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")
    try:
        layout_rows = check_layout()
        profile_rows, lift_rank, nonzero_cross = check_certificate()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"TPC213_BRIDGE_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    print("TPC213_BRIDGE_CHECK=PASS")
    print(f"layout_registry_rows={layout_rows}")
    print(f"delta_profile_rows={profile_rows}")
    print(f"joint_lift_rank={lift_rank}")
    print(f"nonzero_cross_gram_cases={nonzero_cross}")
    print("route_advance=YES")
    print("literal_v46_asymptotic_gram_bound=OPEN")
    print("arithmetic_advance=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
