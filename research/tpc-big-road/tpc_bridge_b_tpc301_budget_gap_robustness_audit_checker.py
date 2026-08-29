#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-301."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-301-budget-gap-robustness-audit"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc301_budget_gap_robustness_audit.md")
PRODUCER = PROJECT / (
    "code/tpc301_budget_gap_robustness_audit.py")
INDEPENDENT = PROJECT / "experiments/tpc301_independent_checker.py"
STRESS = PROJECT / "experiments/tpc301_stress.py"
CERTIFICATE = PROJECT / "results/tpc301_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FINITE_TOLERANCE_MONOTONICITY_AND_HOMOGENEITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_GAP_ROBUSTNESS_ATLAS")
SCHEMA = "TPC301_NATIVE_BUDGET_GAP_ROBUSTNESS_AUDIT_V1"
PRODUCER_SHA256 = "7935d3908b67b6f6cc1c42a330c06ac3de70728268a2d38a6437fad9203b15a8"
CERTIFICATE_SHA256 = "f92a3c71855541f842b951b72e60e1bfcd641758ec7487d9dfbe3459a7e6e75d"
BRIDGE_SHA256 = "d36900a1902ab0a512efd7be7ccc39c5eb412bd34d865ad071796784bbb9eb11"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc301_budget_gap_robustness_audit.py",
    "experiments/tpc301_independent_checker.py",
    "experiments/tpc301_stress.py",
    "results/tpc301_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/paper.pdf")


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script)]
    if script == PRODUCER:
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    for relative in REQUIRED:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
    need(digest(PRODUCER.read_bytes()) == PRODUCER_SHA256,
         "producer provenance")
    raw = CERTIFICATE.read_bytes()
    need(digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    need(digest(BRIDGE.read_bytes()) == BRIDGE_SHA256,
         "bridge provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA, "certificate schema")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and
         audit.get("shell_target_count") == 219 and
         audit.get("inherited_grid_edge_count") == 1380 and
         audit.get("profile_count") == 17 and
         audit.get("tolerance_ladder") == ["0.25", "0.5", "0.75"] and
         audit.get("budget_cases") == 324 and
         audit.get("prefix_order_cases") == 54 and
         audit.get("normalization_invariance_cases") == 54 and
         audit.get("full_tolerance_monotonicity_cases") == 36 and
         audit.get("fixed_power_credit") == 0,
         "finite census")
    for label in ("0.25", "0.5", "0.75"):
        common = audit["common_gap_above_threshold_by_tau"][label]
        full = audit["full_gap_above_threshold_by_tau"][label]
        need(common == {"10": 18, "2": 18, "5": 18},
             "common gap census")
        need(full == {"10": 18, "2": 18, "5": 18},
             "full gap census")
    need(audit["common_weighted_budget_above_3e-5_by_normalization"] == {
        "beta_norm_squared": 54,
        "first_profile_norm_squared": 54,
        "profile_trace_mean": 54,
    }, "budget floor census")
    need(len(payload.get("rows", [])) == 18, "row payload")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(LOG.is_file(), "LaTeX log")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("undefined", "LaTeX Warning:",
                "Package rerunfilecheck Warning:", "Overfull \\hbox",
                "Underfull \\hbox"):
        need(bad not in log, "LaTeX warning: " + bad)
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC301_MAXIMUM_CLAIM = " + STATUS,
        "TPC301_ROUTE_ADVANCE = YES_SCOPED_SINGLE_TOLERANCE_TO_COMMON_PREFIX_ROBUSTNESS_LADDER",
        "TPC301_TOLERANCE_MONOTONICITY = PROVED_EXACT_FINITE",
        "TPC301_TARGET_HOMOGENEITY = PROVED_EXACT_FINITE",
        "TPC301_PREFIX_THRESHOLD_MONOTONICITY = PROVED_EXACT_FINITE",
        "TPC301_COMMON_NORMALIZATION_INVARIANCE = PROVED_EXACT_FINITE",
        "TPC301_COMMON_GAP_TAU_025 = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_10",
        "TPC301_COMMON_GAP_TAU_050 = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_10",
        "TPC301_COMMON_GAP_TAU_075 = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_10",
        "TPC301_FULL_GAP_TAU_025 = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_10",
        "TPC301_FULL_GAP_TAU_050 = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_10",
        "TPC301_FULL_GAP_TAU_075 = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_10",
        "TPC301_COMMON_WEIGHTED_BUDGET_FLOOR_BETA = NUMERICALLY_CERTIFIED_FINITE_54_OF_54_ABOVE_3E_MINUS_5",
        "TPC301_COMMON_WEIGHTED_BUDGET_FLOOR_TRACE = NUMERICALLY_CERTIFIED_FINITE_54_OF_54_ABOVE_3E_MINUS_5",
        "TPC301_COMMON_WEIGHTED_BUDGET_FLOOR_FIRST = NUMERICALLY_CERTIFIED_FINITE_54_OF_54_ABOVE_3E_MINUS_5",
        "TPC301_COMMON_GAP_NORMALIZATION_CHECKS = NUMERICALLY_CERTIFIED_FINITE_54",
        "TPC301_FULL_TOLERANCE_MONOTONICITY_CHECKS = NUMERICALLY_CERTIFIED_FINITE_36",
        "TPC301_SHELL_TARGET_COUNT = 219",
        "TPC301_INHERITED_GRID_EDGE_COUNT = 1380",
        "TPC301_PROFILE_BUDGET_GROWTH = OPEN",
        "TPC301_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC301_FIXED_POWER_CREDIT = 0",
        "TPC301_FULL_GATE_B = OPEN",
        "TPC301_TWIN_PRIME_RESULT = NONE",
        "TPC301_ROUND2_CLUE = EXTEND_TOLERANCE_AND_SOURCE_NORMALIZATION_AUDIT_TO_GROWING_SHELLS_AND_ARITHMETIC_L2_INTERFACE",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge()
        for script in (PRODUCER, INDEPENDENT, STRESS):
            normal = run(script, False)
            optimized = run(script, True)
            need(normal == optimized, script.name + " optimized mismatch")
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError) as error:
        print("TPC301_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC301_BRIDGE_CHECK=PASS rows=18 shell_targets=219 taus=3 "
          "common_gap_gt_10=18x3 full_gap_gt_10=18x3 "
          "normalization_invariance=54 monotone=36")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
