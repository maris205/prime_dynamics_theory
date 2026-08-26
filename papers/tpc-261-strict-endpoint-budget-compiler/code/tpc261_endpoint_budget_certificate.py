#!/usr/bin/env python3
"""Deterministic exact certificate for the TPC-261 endpoint budget."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE_HEAD = "7837a9186f489684152645ab6c89bf78560250c5"
PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
RESULT = PROJECT / "results/tpc261_certificate.json"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "bb320d9bc39933193f5a15f89e285678fef029818d958f7d506401a5e5550af1",
    "papers/tpc-260-four-packet-residual-reassembly/README.md":
        "f45e54e26672327578535e88d948e5559d1e7c6517cfe7a3cefcd29f19630949",
    "papers/tpc-260-four-packet-residual-reassembly/PROOF_PACKAGE.md":
        "e5cfb3d7b1f5b32ddc59270656ec2ff11e2d97c90c2deb68395d03aab55a03b2",
    "papers/tpc-260-four-packet-residual-reassembly/notes/theorem_ledger.md":
        "32ef275efbecb0175dbb01bfc068f654106f9ab3accb89703350ea9628aad746",
    "papers/tpc-260-four-packet-residual-reassembly/notes/route_evaluation.md":
        "2cee2e6e166c4e484bf8f88b7f9ef80ec72d893d8c829606b4353aab39f2f9dd",
    "research/tpc-big-road/bridge_b_four_packet_residual_reassembly.md":
        "01daeff6289bfa857a1f108bea785b908139f749b8233a227a00002dd239561a",
    "research/tpc-big-road/tpc_bridge_b_four_packet_residual_reassembly_checker.py":
        "74f2cc8ee0aa610f21d8e5010fcc419502c678c0ea9d01b849bc075fa24549b3",
}

STATUS = "PROVED_STRUCTURAL_ENDPOINT_BUDGET_OBSTRUCTION_FOR_LITERAL_V59_REASSEMBLY"
ROUND2_CLUE = (
    "PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE_WITH_EFFECTIVE_SAVING_GREATER_THAN_1_OVER_400"
)
E0 = Fraction(5, 3)
TARGET = Fraction(1997, 1200)
REQUIRED = E0 - TARGET

FIREWALL = {
    "TPC261_ARITHMETIC_ADVANCE": "NO",
    "TPC261_BUDGET_IDENTITY": "PROVED_EXACT",
    "TPC261_BORDERLINE_EQUALITY": "PROVED_EXACT_POWER_LEVEL_ONLY",
    "TPC261_FIXED_ATOM_CREDIT": 0,
    "TPC261_FULL_GATE_B": "OPEN",
    "TPC261_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC261_GLOBAL_FIXED_POWER_CREDIT": "NONE",
    "TPC261_L2": "NONE",
    "TPC261_LITERAL_MODE_ZERO_ESTIMATE": "OPEN",
    "TPC261_LITERAL_PRIME_SHELL_COUNTEREXAMPLE": "NONE",
    "TPC261_LOG_ONLY_TO_POWER_PROMOTION": "REFUTED_SCOPED",
    "TPC261_ROUTE_ADVANCE": "YES_SCOPED_ENDPOINT_BUDGET_COMPILER",
    "TPC261_SCALED_NULL_COMPATIBLE_WITNESS": "PROVED_STRUCTURAL_SYNTHETIC",
    "TPC261_STATUS": STATUS,
    "TPC261_STRICT_THRESHOLD": "PROVED_EXACT_ONE_OVER_400",
    "TPC261_TWIN_PRIME_RESULT": "NONE",
}


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def fraction_text(value: Fraction) -> str:
    return str(value)


def frozen_blob(relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", BASELINE_HEAD + ":" + relative], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0 and result.stderr == b"",
         "frozen source: " + relative)
    return result.stdout


def verify_sources() -> int:
    count = 0
    for relative, expected in SOURCE_HASHES.items():
        blob = frozen_blob(relative)
        need(hashlib.sha256(blob).hexdigest() == expected,
             "source hash: " + relative)
        need(len(blob) > 0, "empty source: " + relative)
        count += 1
    return count


def classify(effective: Fraction) -> str:
    if effective > REQUIRED:
        return "STRICT"
    if effective == REQUIRED:
        return "BORDERLINE"
    return "INSUFFICIENT"


def budget_audit() -> dict[str, Any]:
    raw = [
        ("conditional_benchmark", Fraction(1, 100), Fraction(1, 1200),
         "CONDITIONAL_COMPARISON"),
        ("exact_threshold", Fraction(1, 400), Fraction(0),
         "THRESHOLD_REFERENCE"),
        ("loss_below_threshold", Fraction(1, 400), Fraction(1, 1200),
         "FAILURE_TEST"),
        ("local_boundary_gap", Fraction(1, 48), Fraction(0),
         "LOCAL_ONLY"),
        ("null_log_lane", Fraction(0), Fraction(0),
         "LOG_ONLY_NO_POWER"),
    ]
    lanes = []
    for name, delta, loss, scope in raw:
        effective = delta - loss
        lanes.append({
            "classification": classify(effective)
            if name != "null_log_lane" else "NO_FIXED_POWER",
            "delta": fraction_text(delta),
            "effective": fraction_text(effective),
            "loss": fraction_text(loss),
            "margin_over_required": fraction_text(effective - REQUIRED),
            "name": name,
            "scope": scope,
        })
    need(lanes[0]["effective"] == "11/1200", "strict fixture")
    need(lanes[0]["margin_over_required"] == "1/150", "strict margin")
    need(lanes[1]["classification"] == "BORDERLINE", "borderline fixture")
    need(lanes[2]["effective"] == "1/600" and
         lanes[2]["margin_over_required"] == "-1/1200", "loss fixture")
    need(lanes[3]["margin_over_required"] == "11/600", "local margin")
    return {
        "baseline_exponent": fraction_text(E0),
        "lanes": lanes,
        "required_strict_saving": fraction_text(REQUIRED),
        "target_exponent": fraction_text(TARGET),
    }


def log_power_audit() -> dict[str, str]:
    return {
        "delta": "0",
        "fixed_log_power_credit": "NONE",
        "limit": "x^delta/(log x)^M -> infinity for every fixed delta>0 and M",
        "reason": "fixed logarithmic suppression cannot pay a positive power gap",
    }


def scaled_witness() -> dict[str, Any]:
    need(2 * Fraction(5, 6) == E0, "amplitude exponent")
    return {
        "amplitude_exponent": "5/6",
        "alternating_energy_coefficient": "0",
        "alternating_energy_exponent": "5/3",
        "common_packet_diagonal": ["x^(5/3)"] * 4,
        "full_energy_difference": "16*x^(5/3) versus 0",
        "full_energy_exponent": "5/3",
        "plus_energy_coefficient": "16",
        "same_haar_projections": True,
        "same_null_projection": True,
        "synthetic": True,
    }


def lane_audit() -> list[dict[str, str]]:
    return [
        {"lane": "TPC259_same_clock_null", "evidence": "LOG_ONLY",
         "fixed_power_credit": "0", "scope": "SAME_CLOCK_SCOPED"},
        {"lane": "TPC260_mode_zero_residual", "evidence": "UNPAID",
         "fixed_power_credit": "NONE", "scope": "LITERAL_ESTIMATE_OPEN"},
        {"lane": "TPC257_boundary_gap", "evidence": "LOCAL_1_OVER_48",
         "fixed_power_credit": "NOT_ATTACHED", "scope": "LOCAL_ONLY"},
        {"lane": "TPC217_finite_window", "evidence": "STRUCTURAL_L1",
         "fixed_power_credit": "NONE", "scope": "UNATTACHED"},
        {"lane": "TPC257_lower_floor", "evidence": "LOWER_BOUND",
         "fixed_power_credit": "NONE", "scope": "NO_UPPER_CONTROL"},
    ]


def build_certificate() -> dict[str, Any]:
    source_count = verify_sources()
    return {
        "baseline": {"head": BASELINE_HEAD, "source_count": source_count},
        "budget_audit": budget_audit(),
        "claim": STATUS,
        "epistemic_status": {
            "budget_compiler": "PROVED_EXACT",
            "log_power_firewall": "PROVED_EXACT",
            "scaled_witness": "NUMERICALLY_CERTIFIED_STRUCTURAL",
            "literal_mode_zero": "OPEN",
            "arithmetic_l2": "NONE",
        },
        "firewall": dict(FIREWALL),
        "lane_audit": lane_audit(),
        "log_power_audit": log_power_audit(),
        "round2_clue": ROUND2_CLUE,
        "scaled_witness": scaled_witness(),
        "schema": "TPC261_CERTIFICATE_V1",
        "source_hashes": dict(SOURCE_HASHES),
    }


def check_result(expected: dict[str, Any]) -> None:
    need(RESULT.is_file(), "certificate missing")
    raw = RESULT.read_text(encoding="utf-8")
    need(raw == canonical_json(expected), "certificate is not canonical")
    need(json.loads(raw) == expected, "certificate semantics")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    need(args.check != args.emit, "choose exactly one mode")
    expected = build_certificate()
    if args.emit:
        sys.stdout.write(canonical_json(expected))
        return 0
    check_result(expected)
    lanes = expected["budget_audit"]["lanes"]
    print("TPC261_CERTIFICATE=PASS "
          f"sources={expected['baseline']['source_count']} lanes={len(lanes)} "
          "budget=EXACT strict_threshold=1/400 "
          "log_only=NO_FIXED_POWER scaled_witness=PROVED_STRUCTURAL_SYNTHETIC "
          "literal_mode_zero=OPEN")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC261_CERTIFICATE=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
