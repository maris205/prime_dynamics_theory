#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-305."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-305-counterfactual-transported-label-budget"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc305_counterfactual_transported_label_budget.md")
PRODUCER = PROJECT / (
    "code/tpc305_counterfactual_transported_label_budget.py")
INDEPENDENT = PROJECT / "experiments/tpc305_independent_checker.py"
STRESS = PROJECT / "experiments/tpc305_transport_stress.py"
CERTIFICATE = PROJECT / "results/tpc305_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FINITE_COUNTERFACTUAL_TARGET_SWAP_PROTOCOL_PLUS_"
    "NUMERICALLY_CERTIFIED_FIXED_OPERATOR_TRANSPORTED_LABEL_BUDGET_ATLAS")
SCHEMA = "TPC305_COUNTERFACTUAL_TRANSPORTED_LABEL_BUDGET_V1"
PRODUCER_SHA256 = "fa43b82a3a7a7adf8821cf8ebacbfadad80759b917787d00ce365e43adfd4c5d"
CERTIFICATE_SHA256 = "e2f243ed86132af0cd4a6de169723246f3e2fdc0e4fa595fa3b1ffafe657cad3"
BRIDGE_SHA256 = "bb22fd1ebd8d3a0f873f6c8a0c44711238e3c294c743b642cd496fdfbb7a4a64"
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc305_counterfactual_transported_label_budget.py",
    "experiments/tpc305_independent_checker.py",
    "experiments/tpc305_transport_stress.py",
    "results/tpc305_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/paper.pdf")


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script)]
    if script == PRODUCER:
        command.append("--check")
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    for relative in REQUIRED:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
    need(digest(PRODUCER.read_bytes()) == PRODUCER_SHA256,
         "producer provenance")
    need(digest(CERTIFICATE.read_bytes()) == CERTIFICATE_SHA256,
         "certificate provenance")
    need(digest(BRIDGE.read_bytes()) == BRIDGE_SHA256,
         "bridge provenance")
    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA, "certificate schema")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    audit = payload.get("finite_audit", {})
    need(audit.get("cases") == 18 and
         audit.get("operator_budget_tables") == 36 and
         audit.get("pair_groups") == 3 and
         audit.get("middle_pair") == [60, 70] and
         audit.get("middle_right_label_cheaper_cases") == 5 and
         audit.get("middle_cases") == 6 and
         audit.get("middle_same_prefix_cases") == 3 and
         audit.get("middle_same_prefix_right_label_cheaper_cases") == 3 and
         audit.get("orientation_counts_by_pair") == [
             {"CROSS_TARGET_FAVORED": 2, "HOME_OPERATOR_FAVORED": 0,
              "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS": 4,
              "ORIENTATION_UNRESOLVED": 0,
              "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS": 0},
             {"CROSS_TARGET_FAVORED": 0, "HOME_OPERATOR_FAVORED": 1,
              "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS": 0,
              "ORIENTATION_UNRESOLVED": 0,
              "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS": 5},
             {"CROSS_TARGET_FAVORED": 1, "HOME_OPERATOR_FAVORED": 2,
              "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS": 3,
              "ORIENTATION_UNRESOLVED": 0,
              "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS": 0}
         ] and
         audit.get("causal_target_operator_separation") ==
         "PARTIAL_COUNTERFACTUAL_ONLY" and
         audit.get("arithmetic_l2") == "OPEN_LITERAL_SOURCE" and
         audit.get("fixed_power_credit") == 0 and
         audit.get("uniform_asymptotic_budget_theorem") == "OPEN",
         "finite audit")
    need(len(payload.get("cases", [])) == 18 and
         len(payload.get("pair_summary", [])) == 3,
         "atlas shape")
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
        "TPC305_MAXIMUM_CLAIM = " + STATUS,
        "TPC305_ROUTE_ADVANCE = YES_SCOPED_COUNTERFACTUAL_TARGET_CONTROL",
        "TPC305_ALIGNMENT_EXTENSION = PROVED_EXACT_FINITE",
        "TPC305_COMMON_PREFIX_FEASIBILITY = PROVED_EXACT_FINITE",
        "TPC305_FIXED_OPERATOR_TARGET_SWAP = PROVED_EXACT_FINITE",
        "TPC305_COUNTERFACTUAL_BUDGET_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_CASES_36_TABLES",
        "TPC305_MIDDLE_TARGET_ORIENTATION = NUMERICALLY_CERTIFIED_FINITE_RIGHT_LABEL_CHEAPER_5_OF_6",
        "TPC305_MIDDLE_SAME_PREFIX_ORIENTATION = NUMERICALLY_CERTIFIED_FINITE_RIGHT_LABEL_CHEAPER_3_OF_3",
        "TPC305_OUTER_ORIENTATION_CENSUS = NUMERICALLY_CERTIFIED_FINITE_4_2__5_1__3_1_2",
        "TPC305_CAUSAL_SEPARATION = PARTIAL_COUNTERFACTUAL_ONLY",
        "TPC305_OPERATOR_INTERACTION_TERM = OPEN",
        "TPC305_UNIFORM_ASYMPTOTIC_BUDGET = OPEN",
        "TPC305_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC305_FIXED_POWER_CREDIT = 0",
        "TPC305_FULL_GATE_B = OPEN",
        "TPC305_TWIN_PRIME_RESULT = NONE",
        "TPC305_ROUND2_CLUE = TEST_TWO_WAY_OPERATOR_HOLDOUT_AND_INTERACTION_TERM_BEFORE_ANY_CAUSAL_TARGET_OPERATOR_CLAIM",
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
        print("TPC305_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC305_BRIDGE_CHECK=PASS cases=18 operator_tables=36 "
          "middle_right_label_cheaper=5/6 middle_same_prefix=3/3")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
