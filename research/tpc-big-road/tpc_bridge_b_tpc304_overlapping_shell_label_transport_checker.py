#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-304."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-304-overlapping-shell-label-transport"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc304_overlapping_shell_label_transport.md")
PRODUCER = PROJECT / (
    "code/tpc304_overlapping_shell_label_transport.py")
INDEPENDENT = PROJECT / "experiments/tpc304_independent_checker.py"
STRESS = PROJECT / "experiments/tpc304_transport_stress.py"
CERTIFICATE = PROJECT / "results/tpc304_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FINITE_GAUGE_INVARIANT_OVERLAP_CORRELATION_IDENTITY_"
    "PLUS_NUMERICALLY_CERTIFIED_LABEL_TRANSPORT_FRACTURE_AND_BUDGET_"
    "DESCENT_LOCALIZATION")
SCHEMA = "TPC304_OVERLAPPING_SHELL_LABEL_TRANSPORT_V1"
PRODUCER_SHA256 = "5f1eeab4ad8200fad7d1a06af0b2a25534bd07f2d471250e6e22d22a856b25d9"
CERTIFICATE_SHA256 = "4c139ca46127df5294e2fba54fe3c0e72a41b198ea739bdcce22be7529528404"
BRIDGE_SHA256 = "522643818d0cad51f35db0e7f5cb4a754459b47069910dc1f3e06640970148c2"
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc304_overlapping_shell_label_transport.py",
    "experiments/tpc304_independent_checker.py",
    "experiments/tpc304_transport_stress.py",
    "results/tpc304_certificate.json", "notes/theorem_ledger.md",
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
    need(audit.get("transport_rows") == 6 and
         audit.get("adjacent_Q_groups") == 3 and
         audit.get("fracture_rows_at_one_third") == 2 and
         audit.get("unique_fracture_transition") == [60, 70] and
         audit.get("budget_descents_by_Q_group") == [3, 15, 3] and
         audit.get("budget_ascents_by_Q_group") == [15, 3, 15] and
         audit.get("same_prefix_descents_by_Q_group") == [0, 9, 0] and
         audit.get("minimum_correlation_and_maximum_descent_coincide") is True and
         audit.get("all_same_prefix_descents_localized_at_fracture") is True and
         audit.get("fixed_power_credit") == 0,
         "finite audit")
    need(len(payload.get("transport_rows", [])) == 6 and
         len(payload.get("spine_crosswalk", [])) == 3,
         "crosswalk shape")
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
        "TPC304_MAXIMUM_CLAIM = " + STATUS,
        "TPC304_ROUTE_ADVANCE = YES_SCOPED_OVERLAPPING_SHELL_LOCALIZATION",
        "TPC304_OVERLAP_CORRELATION_IDENTITY = PROVED_EXACT_FINITE",
        "TPC304_GLOBAL_SIGN_GAUGE_INVARIANCE = PROVED_EXACT_FINITE",
        "TPC304_LABEL_TRANSPORT_CROSSWALK = NUMERICALLY_CERTIFIED_FINITE_6_ROWS",
        "TPC304_TRANSPORT_FRACTURE = NUMERICALLY_CERTIFIED_FINITE_Q60_TO_70_2_OF_2_EXPONENTS",
        "TPC304_BUDGET_DESCENT_LOCALIZATION = NUMERICALLY_CERTIFIED_FINITE_15_3_3_AND_SAME_PREFIX_9_0_0",
        "TPC304_CAUSAL_SEPARATION = OPEN",
        "TPC304_UNIFORM_ASYMPTOTIC_BUDGET = OPEN",
        "TPC304_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC304_FIXED_POWER_CREDIT = 0",
        "TPC304_FULL_GATE_B = OPEN",
        "TPC304_TWIN_PRIME_RESULT = NONE",
        "TPC304_ROUND2_CLUE = COMPUTE_COUNTERFACTUAL_TRANSPORTED_LABEL_BUDGETS_TO_SEPARATE_TARGET_SWITCHING_FROM_OPERATOR_CHANGE",
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
        print("TPC304_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC304_BRIDGE_CHECK=PASS transport_rows=6 fracture_rows=2 "
          "mean_correlations=1/2,1/11,1/2 budget_descents=3,15,3 "
          "same_prefix_descents=0,9,0")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
