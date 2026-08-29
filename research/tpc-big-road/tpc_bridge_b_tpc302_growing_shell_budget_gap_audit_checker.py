#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-302."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-302-growing-shell-budget-gap-audit"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc302_growing_shell_budget_gap_audit.md")
PRODUCER = PROJECT / (
    "code/tpc302_growing_shell_budget_gap_audit.py")
INDEPENDENT = PROJECT / "experiments/tpc302_independent_checker.py"
STRESS = PROJECT / "experiments/tpc302_stress.py"
CERTIFICATE = PROJECT / "results/tpc302_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FINITE_SOURCE_FIRST_SIGN_ENUMERATION_AND_BUDGET_"
    "MONOTONICITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_GRID_AUDIT")
SCHEMA = "TPC302_GROWING_SHELL_BUDGET_GAP_AUDIT_V1"
# Filled after the final source, certificate, bridge, and PDF are frozen.
PRODUCER_SHA256 = "1edd94f87af501e59ddaa07a6f2c9a5d458d7cb28e0623064f51bfb3d10ae517"
CERTIFICATE_SHA256 = "469431136dd2b80ccdddeeedeabe48be8e74405c6df36eead2ae58936a8c24d6"
BRIDGE_SHA256 = "e5043923e3a28a241e6404a81b2895aa86db9d40dae165b67c742422c023e5d0"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc302_growing_shell_budget_gap_audit.py",
    "experiments/tpc302_independent_checker.py",
    "experiments/tpc302_stress.py", "results/tpc302_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex",
    "paper/references.bib", "paper/paper.pdf")


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
    need(audit.get("rows") == 34 and
         audit.get("explicit_shell_target_count") == 430 and
         audit.get("inherited_parent_grid_edge_count") == 1380 and
         audit.get("profile_count") == 17 and
         audit.get("frontier_cases") == 612 and
         audit.get("weighted_below_one_rows") == 34 and
         audit.get("positive_above_one_rows") == 34 and
         audit.get("common_normalization_cases") == 102 and
         audit.get("full_tolerance_monotonicity_cases") == 68 and
         audit.get("fixed_power_credit") == 0,
         "finite census")
    for label in ("0.25", "0.5", "0.75"):
        need(audit["common_gap_above_10_by_tau"][label] == 34,
             "common gap census")
        need(audit["full_gap_above_10_by_tau"][label] == 34,
             "full gap census")
    need(all(value == 102 for value in
             audit["common_budget_above_1e-5_by_normalization"].values()),
         "budget floor census")
    need(len(payload.get("rows", [])) == 34, "row payload")
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
        "TPC302_MAXIMUM_CLAIM = " + STATUS,
        "TPC302_ROUTE_ADVANCE = YES_SCOPED_FINITE_GROWING_GRID_SOURCE_FIRST_EXTENSION",
        "TPC302_SOURCE_FIRST_SIGN_ENUMERATION = PROVED_EXACT_FINITE",
        "TPC302_PHYSICAL_GRAM_PSD = PROVED_EXACT_FINITE",
        "TPC302_BUDGET_MONOTONICITY = PROVED_EXACT_FINITE",
        "TPC302_COMMON_GAP_TAU_025 = NUMERICALLY_CERTIFIED_FINITE_34_OF_34_ABOVE_10",
        "TPC302_COMMON_GAP_TAU_050 = NUMERICALLY_CERTIFIED_FINITE_34_OF_34_ABOVE_10",
        "TPC302_COMMON_GAP_TAU_075 = NUMERICALLY_CERTIFIED_FINITE_34_OF_34_ABOVE_10",
        "TPC302_FULL_GAP_TAU_075 = NUMERICALLY_CERTIFIED_FINITE_34_OF_34_ABOVE_10",
        "TPC302_SOURCE_FIRST_LABELS = NUMERICALLY_CERTIFIED_FINITE_34_OF_34",
        "TPC302_COMMON_BUDGET_FLOOR = NUMERICALLY_CERTIFIED_FINITE_102_OF_102_PER_NORMALIZATION",
        "TPC302_EXPLICIT_SHELL_TARGET_COUNT = 430",
        "TPC302_INHERITED_GRID_EDGE_COUNT = 1380",
        "TPC302_UNIFORM_GROWING_PROFILE_BUDGET = OPEN",
        "TPC302_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC302_FIXED_POWER_CREDIT = 0",
        "TPC302_FULL_GATE_B = OPEN",
        "TPC302_TWIN_PRIME_RESULT = NONE",
        "TPC302_ROUND2_CLUE = TEST_UNIFORM_NATIVE_BUDGET_GROWTH_OR_CONSTRUCT_A_GROWING_SHELL_COUNTEREXAMPLE",
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
        print("TPC302_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC302_BRIDGE_CHECK=PASS rows=34 shell_targets=430 "
          "frontier_cases=612 common_gap_gt_10=34x3 "
          "source_first_labels=34 normalization=102 monotone=68")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
