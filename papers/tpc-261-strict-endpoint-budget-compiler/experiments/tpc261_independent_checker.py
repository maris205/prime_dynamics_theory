#!/usr/bin/env python3
"""Independent exact checker for the TPC-261 endpoint-budget certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE = "7837a9186f489684152645ab6c89bf78560250c5"
ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc261_certificate.json"
CLAIM = "PROVED_STRUCTURAL_ENDPOINT_BUDGET_OBSTRUCTION_FOR_LITERAL_V59_REASSEMBLY"
REQUIRED = Fraction(1, 400)

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


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def frozen(relative: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE + ":" + relative],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"",
         "frozen source: " + relative)
    return result.stdout


def source_audit() -> None:
    for relative, expected in SOURCE_HASHES.items():
        need(hashlib.sha256(frozen(relative)).hexdigest() == expected,
             "source hash: " + relative)


def fraction_text(value: Fraction) -> str:
    return str(value)


def lane_records() -> list[dict[str, str]]:
    raw = [
        ("conditional_benchmark", Fraction(1, 100), Fraction(1, 1200),
         "CONDITIONAL_COMPARISON", "STRICT"),
        ("exact_threshold", Fraction(1, 400), Fraction(0),
         "THRESHOLD_REFERENCE", "BORDERLINE"),
        ("loss_below_threshold", Fraction(1, 400), Fraction(1, 1200),
         "FAILURE_TEST", "INSUFFICIENT"),
        ("local_boundary_gap", Fraction(1, 48), Fraction(0),
         "LOCAL_ONLY", "STRICT"),
        ("null_log_lane", Fraction(0), Fraction(0),
         "LOG_ONLY_NO_POWER", "NO_FIXED_POWER"),
    ]
    output = []
    for name, delta, loss, scope, classification in raw:
        effective = delta - loss
        output.append({
            "classification": classification,
            "delta": fraction_text(delta),
            "effective": fraction_text(effective),
            "loss": fraction_text(loss),
            "margin_over_required": fraction_text(effective - REQUIRED),
            "name": name,
            "scope": scope,
        })
    return output


def budget_record() -> dict[str, Any]:
    return {
        "baseline_exponent": "5/3",
        "lanes": lane_records(),
        "required_strict_saving": "1/400",
        "target_exponent": "1997/1200",
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


def firewall() -> dict[str, Any]:
    return {
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
        "TPC261_STATUS": CLAIM,
        "TPC261_STRICT_THRESHOLD": "PROVED_EXACT_ONE_OVER_400",
        "TPC261_TWIN_PRIME_RESULT": "NONE",
    }


def expected_witness() -> dict[str, Any]:
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


def semantic(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        return (
            data["schema"] == "TPC261_CERTIFICATE_V1"
            and data["claim"] == CLAIM
            and data["baseline"] == {"head": BASELINE,
                                      "source_count": len(SOURCE_HASHES)}
            and data["source_hashes"] == SOURCE_HASHES
            and data["budget_audit"] == budget_record()
            and data["lane_audit"] == lane_audit()
            and data["firewall"] == firewall()
            and data["scaled_witness"] == expected_witness()
            and data["log_power_audit"] == {
                "delta": "0",
                "fixed_log_power_credit": "NONE",
                "limit": "x^delta/(log x)^M -> infinity for every fixed delta>0 and M",
                "reason": "fixed logarithmic suppression cannot pay a positive power gap",
            }
            and data["round2_clue"] ==
            "PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE_WITH_EFFECTIVE_SAVING_GREATER_THAN_1_OVER_400"
            and data["epistemic_status"] == {
                "arithmetic_l2": "NONE",
                "budget_compiler": "PROVED_EXACT",
                "literal_mode_zero": "OPEN",
                "log_power_firewall": "PROVED_EXACT",
                "scaled_witness": "NUMERICALLY_CERTIFIED_STRUCTURAL",
            }
        )
    except (KeyError, TypeError):
        return False


def mutation_audit(data: dict[str, Any]) -> int:
    candidates: list[dict[str, Any]] = []

    def mutate(path: tuple[object, ...], value: Any) -> None:
        item = deepcopy(data)
        cursor: Any = item
        for key in path[:-1]:
            cursor = cursor[int(key)] if isinstance(cursor, list) else cursor[key]
        last = path[-1]
        if isinstance(cursor, list):
            cursor[int(last)] = value
        else:
            cursor[last] = value
        candidates.append(item)

    mutate(("schema",), "TPC261_CERTIFICATE_V0")
    mutate(("claim",), "PROVED")
    mutate(("baseline", "head"), "0" * 40)
    mutate(("source_hashes",), {})
    mutate(("budget_audit", "required_strict_saving"), "0")
    mutate(("budget_audit", "target_exponent"), "5/3")
    mutate(("budget_audit", "lanes", "0", "effective"), "0")
    mutate(("budget_audit", "lanes", "1", "classification"), "STRICT")
    mutate(("budget_audit", "lanes", "3", "scope"), "GLOBAL")
    mutate(("log_power_audit", "fixed_log_power_credit"), "1/400")
    mutate(("scaled_witness", "plus_energy_coefficient"), "0")
    mutate(("scaled_witness", "same_null_projection"), False)
    mutate(("firewall", "TPC261_ARITHMETIC_ADVANCE"), "YES")
    mutate(("firewall", "TPC261_FULL_GATE_B"), "PAID")
    mutate(("firewall", "TPC261_FIXED_ATOM_CREDIT"), 1)
    mutate(("round2_clue",), "OTHER")
    need(all(not semantic(candidate) for candidate in candidates),
         "mutation accepted")
    return len(candidates)


def run() -> None:
    source_audit()
    need(CERTIFICATE.is_file(), "certificate missing")
    raw = CERTIFICATE.read_text(encoding="utf-8")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonical")
    need(semantic(data), "certificate semantics")
    rejected = mutation_audit(data)
    print("TPC261_INDEPENDENT_CHECK=PASS "
          f"sources={len(SOURCE_HASHES)} lanes={len(data['budget_audit']['lanes'])} "
          f"mutations_rejected={rejected} producer_imported=NO")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    run()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC261_INDEPENDENT_CHECK=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
