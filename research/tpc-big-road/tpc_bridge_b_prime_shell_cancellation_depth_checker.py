#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for TPC-287."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-287-prime-shell-cancellation-depth"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_prime_shell_cancellation_depth.md"
PRODUCER = PROJECT / (
    "code/tpc287_prime_shell_cancellation_certificate.py")
INDEPENDENT = PROJECT / "experiments/tpc287_independent_checker.py"
STRESS = PROJECT / "experiments/tpc287_cancellation_stress.py"
CERTIFICATE = PROJECT / "results/tpc287_certificate.json"
STATUS = (
    "PROVED_EXACT_FINITE_SHELL_ADDITIVE_ATTACHMENT_DECOMPOSITION_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_CANCELLATION_DEPTH_LEDGER")
SCHEMA = "TPC287_PRIME_SHELL_CANCELLATION_CERTIFICATE_V1"
CERTIFICATE_SHA256 = (
    "a72dd15e4b2977c04d3cba81b4f02d5736d9d8dcab6fcf7c8661d45ddc1fee30")
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc287_prime_shell_cancellation_certificate.py",
    "experiments/tpc287_independent_checker.py",
    "experiments/tpc287_cancellation_stress.py",
    "results/tpc287_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/paper.pdf",
)


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
    if script == PRODUCER:
        command += ["-B", str(script), "--check"]
    else:
        command += ["-B", str(script)]
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check() -> None:
    bridge = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC287_MAXIMUM_CLAIM = " + STATUS,
        "TPC287_ROUTE_ADVANCE = YES_SCOPED_PRIME_COMPONENT_LEDGER_AND_FINITE_CANCELLATION_DEPTH",
        "TPC287_SHELL_ADDITIVITY = PROVED_EXACT_FINITE",
        "TPC287_ATTACHMENT_ADDITIVITY = PROVED_EXACT_FINITE",
        "TPC287_RETENTION_ENVELOPE = PROVED_CONDITIONAL_INTERVAL",
        "TPC287_COMPONENT_LEDGER = NUMERICALLY_CERTIFIED_FINITE_336_COMPONENTS",
        "TPC287_MIXED_SIGN_ROWS = NUMERICALLY_CERTIFIED_FINITE_57_OF_84",
        "TPC287_RETENTION_THRESHOLDS = NUMERICALLY_CERTIFIED_FINITE_31_22_8",
        "TPC287_LEAVE_ONE_OUT = NUMERICALLY_CERTIFIED_FINITE_48_FLIPS_12_ZERO",
        "TPC287_GROWING_SHELL_STABILITY = OPEN",
        "TPC287_SOURCE_CONTROL_UNIFORMITY = OPEN",
        "TPC287_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC287_FIXED_POWER_CREDIT = 0",
        "TPC287_FULL_GATE_B = OPEN",
        "TPC287_TWIN_PRIME_RESULT = NONE",
        "TPC287_ROUND2_CLUE = TEST_CANCELLATION_STABILITY_UNDER_GROWING_SHELL_AND_SOURCE_CONTROLS",
    )
    for marker in markers:
        need(marker in bridge, "bridge marker")
    for item in REQUIRED:
        need((PROJECT / item).is_file(), "missing artifact: " + item)

    raw = CERTIFICATE.read_bytes()
    need(digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data["certificate_version"] == 1 and
         data["claim_status"] == STATUS and
         data["payload"]["schema"] == SCHEMA,
         "certificate header")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "certificate payload hash")
    audit = data["payload"]["finite_audit"]
    need(audit == {
        "component_intervals": 336,
        "component_negative": 175,
        "component_positive": 161,
        "component_sign_separated": 336,
        "fixed_power_credit": 0,
        "growing_shell_stability": "OPEN",
        "leave_one_out_same_sign_events": 276,
        "leave_one_out_sign_flip_events": 48,
        "leave_one_out_zero_events": 12,
        "literal_arithmetic_L2": "OPEN",
        "mixed_component_sign_rows": 57,
        "retention_upper_lt_half_rows": 31,
        "retention_upper_lt_quarter_rows": 22,
        "retention_upper_lt_tenth_rows": 8,
        "retention_upper_lt_twentieth_rows": 5,
        "rows": 84,
        "same_sign_component_rows": 27,
        "shell_negative": 52,
        "shell_positive": 32,
    }, "finite census")
    need(len(data["payload"]["rows"]) == 84 and
         len(data["payload"]["shell_ladder"]) == 7,
         "row or ladder census")
    need([item["cardinality"] for item in data["payload"]["shell_ladder"]]
         == list(range(1, 8)), "ladder cardinalities")
    pdf = (PROJECT / "paper/paper.pdf").read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 50_000, "PDF")
    log = (PROJECT / "paper/main.log").read_text(encoding="utf-8")
    need("undefined" not in log.lower() and "LaTeX Warning:" not in log and
         "Package rerunfilecheck Warning:" not in log,
         "LaTeX warning or undefined reference")
    for script in (PRODUCER, INDEPENDENT, STRESS):
        normal = run(script, False)
        optimized = run(script, True)
        need(normal == optimized, script.name + " optimized mismatch")
    print("TPC287_BRIDGE_CHECK=PASS rows=84 components=336 mixed=57 "
          "component_negative=175 shell_negative=52 retention_lt_half=31 "
          "retention_lt_quarter=22 retention_lt_tenth=8 leave_flips=48 "
          "leave_zero=12")
    print("claim_level=" + STATUS)


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC287_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
