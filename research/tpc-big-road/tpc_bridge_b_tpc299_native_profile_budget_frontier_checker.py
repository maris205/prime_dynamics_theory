#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-299."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-299-native-profile-budget-frontier"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc299_native_profile_budget_frontier.md")
PRODUCER = PROJECT / (
    "code/tpc299_native_profile_budget_frontier_certificate.py")
INDEPENDENT = PROJECT / "experiments/tpc299_independent_checker.py"
STRESS = PROJECT / "experiments/tpc299_budget_stress.py"
CERTIFICATE = PROJECT / "results/tpc299_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FINITE_PROFILE_BUDGET_KKT_FRONTIER_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_OBSTRUCTION_ATLAS")
SCHEMA = "TPC299_NATIVE_PROFILE_BUDGET_FRONTIER_CERTIFICATE_V1"
PRODUCER_SHA256 = (
    "94cb7f191378698de2f08157a475586864c59bba02621e447da98f5ffbbc7279")
CERTIFICATE_SHA256 = (
    "9be51f5bcb93e3a297a70e1c12985d52aee2b74e5e3fe4a64fbf7d5a054c559e")
BRIDGE_SHA256 = (
    "e2c500f9d16b7de1a431c0513e431d50792f224f20802410af0e69d65c859768")

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc299_native_profile_budget_frontier_certificate.py",
    "experiments/tpc299_independent_checker.py",
    "experiments/tpc299_budget_stress.py", "results/tpc299_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex", "paper/references.bib",
    "paper/paper.pdf")


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
    need(audit.get("rows") == 18 and audit.get("shell_edges") == 1380 and
         audit.get("profile_count") == 17 and
         audit.get("tested_prefix_entries") == 219,
         "finite counts")
    need(audit.get("weighted_threshold_budget_ratio_floor") == "9e-5" and
         audit.get("weighted_threshold_budget_floor_rows") == 15 and
         audit.get("weighted_threshold_budget_above_5e-4_rows") == 15 and
         audit.get("weighted_threshold_budget_above_1e-3_rows") == 14 and
         audit.get("weighted_full_prefix_budget_above_1e-3_rows") == 11 and
         audit.get("all_positive_threshold_budget_ratio_ceiling") == "1e-4" and
         audit.get("all_positive_threshold_budget_ceiling_rows") == 18 and
         audit.get("weighted_to_positive_threshold_budget_gap_floor") == "20" and
         audit.get("weighted_to_positive_gap_floor_rows") == 18,
         "budget census")
    need(audit.get("fixed_power_credit") == 0, "credit firewall")
    need(len(payload.get("rows", [])) == 18, "row payload")
    for row in payload["rows"]:
        need(len(row.get("least_squares_prefixes", [])) ==
             row.get("tested_prefix_count"), "prefix length")
        need(set(row.get("threshold_budget_frontiers", {})) ==
             {"minimum", "maxcut", "plus"}, "threshold targets")
        need(set(row.get("full_prefix_budget_frontiers", {})) ==
             {"minimum", "maxcut", "plus"}, "full targets")
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
        "TPC299_MAXIMUM_CLAIM = " + STATUS,
        "TPC299_ROUTE_ADVANCE = YES_SCOPED_PROFILE_ANGLE_TO_NATIVE_BUDGET_FRONTIER",
        "TPC299_PROFILE_BUDGET_KKT_FRONTIER = PROVED_EXACT_FINITE",
        "TPC299_NESTED_BUDGET_MONOTONICITY = PROVED_EXACT_FINITE",
        "TPC299_WEIGHTED_HALF_RMS_BUDGET_FLOOR = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_9E_MINUS_5",
        "TPC299_WEIGHTED_HALF_RMS_BUDGET_MID_FLOOR = NUMERICALLY_CERTIFIED_FINITE_15_OF_18_ABOVE_5E_MINUS_4",
        "TPC299_WEIGHTED_HALF_RMS_BUDGET_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_14_OF_18_ABOVE_1E_MINUS_3",
        "TPC299_WEIGHTED_FULL_PREFIX_BUDGET_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_11_OF_18_ABOVE_1E_MINUS_3",
        "TPC299_PLUS_HALF_RMS_BUDGET_CEILING = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_BELOW_1E_MINUS_4",
        "TPC299_WEIGHTED_PLUS_BUDGET_GAP = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_20",
        "TPC299_PROFILE_BUDGET_GROWTH = OPEN",
        "TPC299_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC299_FIXED_POWER_CREDIT = 0",
        "TPC299_FULL_GATE_B = OPEN",
        "TPC299_TWIN_PRIME_RESULT = NONE",
        "TPC299_ROUND2_CLUE = TEST_BUDGET_CONSTRAINED_PROFILE_FRONTIER_ON_GROWING_SHELLS_AND_SOURCE_NORMALIZATION",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge()
        outputs = {}
        for script in (PRODUCER, INDEPENDENT, STRESS):
            outputs[script.name] = (run(script, False), run(script, True))
            need(outputs[script.name][0] == outputs[script.name][1],
                 script.name + " optimized mismatch")
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError) as error:
        print("TPC299_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC299_BRIDGE_CHECK=PASS rows=18 prefixes=219 "
          "weighted_gt_1e-3=14 full_gt_1e-3=11 plus_lt_1e-4=18 gap_gt_20=18")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
