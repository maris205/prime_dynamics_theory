#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-297."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-297-literal-source-profile-span-audit"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc297_literal_source_profile_span_audit.md"
PRODUCER = PROJECT / "code/tpc297_literal_source_profile_span_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc297_independent_checker.py"
STRESS = PROJECT / "experiments/tpc297_profile_stress.py"
CERTIFICATE = PROJECT / "results/tpc297_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FINITE_RESTRICTED_PROFILE_PROJECTION_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_FOUR_CUTOFF_PROFILE_ATLAS")
SCHEMA = "TPC297_LITERAL_SOURCE_PROFILE_SPAN_CERTIFICATE_V1"
PRODUCER_SHA256 = (
    "ae60f5400e083875012cb817285916e1370064f1d55599878def5c59a89a6aa5")
CERTIFICATE_SHA256 = (
    "2ffe4cfd0f564fb2cd63669dccbd8dc99f5911123b3b4a3f8b766262f88d97b6")
BRIDGE_SHA256 = (
    "0aebd6646a3d1cceb18345a53f27417275c2c9a2414493b9da2cf495b3c977b8")

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc297_literal_source_profile_span_certificate.py",
    "experiments/tpc297_independent_checker.py",
    "experiments/tpc297_profile_stress.py", "results/tpc297_certificate.json",
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
    need(digest(BRIDGE.read_bytes()) == BRIDGE_SHA256,
         "bridge provenance")
    raw = CERTIFICATE.read_bytes()
    need(digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA, "certificate schema")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("shell_edges") == 1380,
         "finite counts")
    need(audit.get("rank_3_rows") == 1 and audit.get("rank_4_rows") == 17,
         "rank census")
    need(audit.get("weighted_rms_at_least_0_6_rows_large_shell") == 17 and
         audit.get("all_positive_rms_at_most_0_15_rows") == 18 and
         audit.get("profile_no_worse_than_one_ray_rows") == 18,
         "residual census")
    need(audit.get("fixed_power_credit") == 0, "credit firewall")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(LOG.is_file(), "LaTeX log")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("undefined", "LaTeX Warning:", "Package rerunfilecheck Warning:",
                "Overfull \\hbox", "Underfull \\hbox"):
        need(bad not in log, "LaTeX warning: " + bad)
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC297_MAXIMUM_CLAIM = " + STATUS,
        "TPC297_ROUTE_ADVANCE = YES_SCOPED_NATIVE_PROFILE_RAY_TO_FOUR_LITERAL_CUTOFF_SPAN",
        "TPC297_PROJECTION_IDENTITY = PROVED_EXACT_FINITE",
        "TPC297_NESTED_PROFILE_MONOTONICITY = PROVED_EXACT_FINITE",
        "TPC297_TWO_MODULUS_IMAGE_RANK = NUMERICALLY_CERTIFIED_FINITE_3_PLUS_4",
        "TPC297_WEIGHTED_PROFILE_SEPARATION = NUMERICAL_OBSERVATION_17_OF_17_AT_LEAST_0_6",
        "TPC297_ALL_POSITIVE_PROFILE_CAPTURE = NUMERICAL_OBSERVATION_18_OF_18_AT_MOST_0_15",
        "TPC297_GROWING_PROFILE_DIMENSION = OPEN",
        "TPC297_PRINCIPAL_ANGLE_THEOREM = OPEN",
        "TPC297_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC297_FIXED_POWER_CREDIT = 0",
        "TPC297_FULL_GATE_B = OPEN",
        "TPC297_TWIN_PRIME_RESULT = NONE",
        "TPC297_ROUND2_CLUE = TEST_NATIVE_PROFILE_PRINCIPAL_ANGLES_AND_MINIMUM_DIMENSION",
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
        print("TPC297_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC297_BRIDGE_CHECK=PASS rows=18 rank3=1 rank4=17 "
          "weighted_large=17 plus=18")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
