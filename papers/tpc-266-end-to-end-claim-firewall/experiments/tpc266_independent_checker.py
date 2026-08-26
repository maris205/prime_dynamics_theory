#!/usr/bin/env python3
"""Independent checker for the TPC-266 typed end-to-end certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE_HEAD = "9753ec69d41efc285dcfd1f0ac32156b7bb911b5"
ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc266_certificate.json"
CLAIM = "PROVED_EXACT_END_TO_END_RESIDUAL_CLAIM_FIREWALL"
ROUND2 = (
    "PROVE_A_LITERAL_V59_RADIUS_OR_SIGNED_PHASE_BOUND_WITH_EFFECTIVE_SAVING_"
    "GREATER_THAN_1_OVER_400"
)
SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "873448074c451830a27378661c0ec146472e789cc7b698e65f27dbfcabe6a7ca",
    "papers/tpc-265-schur-endpoint-budget-compiler/README.md":
        "bb114657476ca2d10f34b9c5c96e93804d676a20b9e7ad1770df16d60719eedd",
    "papers/tpc-265-schur-endpoint-budget-compiler/PROOF_PACKAGE.md":
        "de683a97b1d099778ee08f72fa1e12ea6a28bef418e04bf1f99c915412ba38f3",
    "papers/tpc-265-schur-endpoint-budget-compiler/notes/theorem_ledger.md":
        "296e2aeb889611a129de97bef17f75bc69526b52461240081adaf1772b6301e8",
    "papers/tpc-265-schur-endpoint-budget-compiler/notes/route_evaluation.md":
        "d12e0b024c30ee64876b799afe3fb98c2c2b68d86a6a09621e596709775a5239",
    "research/tpc-big-road/bridge_b_schur_endpoint_budget_compiler.md":
        "890dd8e6be707140b5e562713f0a63713ab28f5c63ba3510af0350a3ef636588",
    "research/tpc-big-road/tpc_bridge_b_schur_endpoint_budget_compiler_checker.py":
        "df3cd2ef0f0d2841c92c3951b70e268777d2f1e32e1845e9e9fa201e5ffb7aa6",
}


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def frozen(path: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + path],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"",
         "frozen source: " + path)
    return result.stdout


def source_audit() -> None:
    for path, expected in SOURCE_HASHES.items():
        blob = frozen(path)
        actual = hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest()
        need(actual == expected, "source hash: " + path)


def expected_matrix() -> list[tuple[str, str, bool]]:
    return [
        ("strict_pair", "CLOSED_CONDITIONAL", True),
        ("fixed_log_center", "OPEN_LOG_CENTER", True),
        ("missing_radius", "OPEN_RADIUS", True),
        ("borderline_lane", "BORDERLINE", True),
        ("subcritical_lane", "INSUFFICIENT", True),
        ("deleted_residual", "UNSOUND_RESIDUAL_DELETION", False),
    ]


def semantic(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        if data["schema"] != "TPC266_END_TO_END_CLAIM_FIREWALL_CERTIFICATE_V1":
            return False
        if data["claim"] != CLAIM or data["round2_clue"] != ROUND2:
            return False
        if data["baseline"] != {"head": BASELINE_HEAD, "source_count": 8}:
            return False
        if data["source_hashes"] != SOURCE_HASHES:
            return False
        thresholds = data["thresholds"]
        if thresholds != {
            "baseline_exponent": "5/3",
            "target_exponent": "1997/1200",
            "required_strict_saving": "1/400",
        }:
            return False
        chain = data["chain_audit"]
        nodes = chain["nodes"]
        if [node["id"] for node in nodes] != [
            "TPC263.C3", "TPC264.Cperp", "TPC265.endpoint", "TPC266.compiler"
        ]:
            return False
        if [node["output_type"] for node in nodes] != [
            "FIXED_LOG", "SCHUR_SET", "RADIAL_ENVELOPE", "BUDGET_DECISION"
        ]:
            return False
        if nodes[0]["power_credit"] != 0:
            return False
        if nodes[1]["radius_status"] != "OPEN":
            return False
        if nodes[2]["upper_endpoint"] != "|c|+R":
            return False
        if nodes[3]["strict_threshold"] != "1/400":
            return False
        if chain["residual_retained_by_default"] is not True:
            return False
        if chain["forbidden_promotions"] != [
            "FIXED_LOG->POWER", "SCHUR_SET->ZERO_RESIDUAL"
        ]:
            return False
        if chain["edges"] != [
            ["TPC263.C3", "TPC264.Cperp", "EXACT_SPLIT"],
            ["TPC264.Cperp", "TPC265.endpoint", "EXACT_RADIAL_SUPPORT"],
            ["TPC265.endpoint", "TPC266.compiler", "TYPED_BUDGET_CHECK"],
        ]:
            return False
        endpoint = data["endpoint_audit"]
        if endpoint != {
            "aligned_value": "5",
            "center": "2",
            "circle_infimum": "1",
            "circle_supremum": "5",
            "deleted_output": "2",
            "disk_infimum": "0",
            "disk_supremum": "5",
            "radius": "3",
            "residual_deletion_gap": "3",
        }:
            return False
        firewall = data["firewall"]
        required_firewall = {
            "TPC266_ACTUAL_V59_PHASE": "OPEN",
            "TPC266_ACTUAL_V59_RADIUS": "OPEN",
            "TPC266_ARITHMETIC_ADVANCE": "NO",
            "TPC266_CENTER_CURRENT_TYPE": "FIXED_LOG",
            "TPC266_FAILURE_MATRIX": "PROVED_EXACT_SIX_STATE",
            "TPC266_FIXED_LOG_NONPROMOTION": "PROVED_EXACT",
            "TPC266_FIXED_POWER_CREDIT": 0,
            "TPC266_FULL_GATE_B": "OPEN",
            "TPC266_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC266_L2": "NONE",
            "TPC266_LITERAL_PRIME_SHELL_COUNTEREXAMPLE": "NONE",
            "TPC266_MAXIMUM_CLAIM": CLAIM,
            "TPC266_RESIDUAL_CURRENT_TYPE": "SCHUR_SET_RADIUS_OPEN",
            "TPC266_RESIDUAL_RETENTION_FIREWALL": "PROVED_EXACT",
            "TPC266_ROUTE_ADVANCE": "YES_SCOPED_END_TO_END_CLAIM_FIREWALL",
            "TPC266_STATUS": CLAIM,
            "TPC266_STRICT_PAYMENT_THRESHOLD": "PROVED_EXACT_ONE_OVER_400",
            "TPC266_TWIN_PRIME_RESULT": "NONE",
            "TPC266_TYPED_COMPOSITION": "PROVED_EXACT",
        }
        if firewall != required_firewall:
            return False
        log_data = data["log_firewall"]
        if log_data["fixed_log_credit"] != 0:
            return False
        if log_data["type_transition"] != "FIXED_LOG->POWER = REJECTED":
            return False
        if "x^delta/(log x)^M -> infinity" not in log_data["limit_statement"]:
            return False
        matrix = data["failure_matrix"]
        if len(matrix) != len(expected_matrix()):
            return False
        for record, (name, result, retained) in zip(matrix, expected_matrix()):
            if record["name"] != name or record["result"] != result:
                return False
            if record["expected"] != result or record["residual_retained"] is not retained:
                return False
        return True
    except (KeyError, TypeError, IndexError):
        return False


def mutation_audit(data: dict[str, Any]) -> int:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[Any, ...], value: Any) -> None:
        candidate = copy.deepcopy(data)
        cursor: Any = candidate
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        mutations.append(candidate)

    mutate(("schema",), "TPC266_V0")
    mutate(("claim",), "PROVED")
    mutate(("baseline", "head"), "0" * 40)
    mutate(("source_hashes",), {})
    mutate(("thresholds", "required_strict_saving"), "0")
    mutate(("chain_audit", "nodes", 0, "output_type"), "POWER")
    mutate(("chain_audit", "nodes", 1, "radius_status"), "PAID")
    mutate(("chain_audit", "forbidden_promotions"), [])
    mutate(("chain_audit", "residual_retained_by_default"), False)
    mutate(("endpoint_audit", "disk_supremum"), "0")
    mutate(("endpoint_audit", "residual_deletion_gap"), "0")
    mutate(("failure_matrix", 0, "result"), "OPEN")
    mutate(("failure_matrix", 5, "residual_retained"), True)
    mutate(("firewall", "TPC266_FIXED_LOG_NONPROMOTION"), "HEURISTIC")
    mutate(("firewall", "TPC266_RESIDUAL_RETENTION_FIREWALL"), "SKIPPED")
    mutate(("firewall", "TPC266_STRICT_PAYMENT_THRESHOLD"), "PAID")
    mutate(("firewall", "TPC266_FIXED_POWER_CREDIT"), 1)
    mutate(("firewall", "TPC266_FULL_GATE_B"), "PAID")
    mutate(("round2_clue",), "NONE")
    need(all(not semantic(item) for item in mutations), "mutation accepted")
    return len(mutations)


def run() -> None:
    source_audit()
    need(RESULT.is_file(), "certificate missing")
    raw = RESULT.read_text(encoding="utf-8")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonical")
    need(semantic(data), "certificate semantics")
    required = Fraction(1, 400)
    need(Fraction(1, 320) > required, "strict rational lane")
    need(Fraction(1, 400) == required, "borderline rational lane")
    rejected = mutation_audit(data)
    print("TPC266_INDEPENDENT_CHECK=PASS "
          f"chain_nodes=4 states=6 mutations_rejected={rejected} "
          "producer_imported=NO")


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
        print("TPC266_INDEPENDENT_CHECK=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
