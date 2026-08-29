#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-298."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-298-profile-angle-dimension-ladder"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc298_profile_angle_dimension_ladder.md")
PRODUCER = PROJECT / "code/tpc298_profile_angle_dimension_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc298_independent_checker.py"
STRESS = PROJECT / "experiments/tpc298_ladder_stress.py"
CERTIFICATE = PROJECT / "results/tpc298_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FINITE_PRINCIPAL_ANGLE_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_PROFILE_DIMENSION_LADDER")
SCHEMA = "TPC298_PROFILE_ANGLE_DIMENSION_CERTIFICATE_V1"
PRODUCER_SHA256 = (
    "fe4703b3d6093f68c02186de83820dc02fc37abbda13cb34abb34b7b0f41d1b8")
CERTIFICATE_SHA256 = (
    "30650bc9e7fb2d942c7a4c03de0b5657040653fefb500c2b585bdea3013a7bf1")
BRIDGE_SHA256 = (
    "8f17c9c5187299b5e56adc21e02a977d1d48727adb6da4eeb9bac24b2f107c25")

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc298_profile_angle_dimension_certificate.py",
    "experiments/tpc298_independent_checker.py",
    "experiments/tpc298_ladder_stress.py", "results/tpc298_certificate.json",
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
         audit.get("profile_count") == 17, "finite counts")
    need(audit.get("prefix_rank_rows_both_moduli") == 18 and
         audit.get("rank_prefix_entries") == 306, "rank census")
    need(audit.get("weighted_half_rms_ratio_floor") == "2/3" and
         audit.get("weighted_half_rms_ratio_rows") == 18 and
         audit.get("all_positive_half_rms_dimension_max") == 6 and
         audit.get("all_positive_half_rms_dimension_rows") == 18 and
         audit.get("full_prefix_capture_rows") == 18, "dimension census")
    need(audit.get("fixed_power_credit") == 0, "credit firewall")
    for row in payload.get("rows", []):
        need(len(row.get("profile_rank_ladder_modular", [])) == 17,
             "row rank ladder length")
        need(len(row.get("prefixes", [])) ==
             min(row.get("shell_cardinality", 0), 17),
             "row prefix length")
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
        "TPC298_MAXIMUM_CLAIM = " + STATUS,
        "TPC298_ROUTE_ADVANCE = YES_SCOPED_FOUR_PROFILE_SNAPSHOT_TO_COMPLETE_LITERAL_PREFIX_LADDER",
        "TPC298_PROJECTION_IDENTITY = PROVED_EXACT_FINITE",
        "TPC298_PRINCIPAL_ANGLE_IDENTITY = PROVED_EXACT_FINITE",
        "TPC298_NESTED_PREFIX_MONOTONICITY = PROVED_EXACT_FINITE",
        "TPC298_TWO_MODULUS_PREFIX_RANK = NUMERICALLY_CERTIFIED_FINITE_18_OF_18",
        "TPC298_WEIGHTED_HALF_RMS_DIMENSION = NUMERICAL_OBSERVATION_18_OF_18_RATIO_AT_LEAST_2_OVER_3",
        "TPC298_PLUS_HALF_RMS_DIMENSION = NUMERICAL_OBSERVATION_18_OF_18_AT_MOST_6",
        "TPC298_FULL_PREFIX_CAPTURE = NUMERICALLY_CERTIFIED_FINITE_18_OF_18",
        "TPC298_GROWING_DIMENSION_THEOREM = OPEN",
        "TPC298_CONDITIONING_GROWTH = OPEN",
        "TPC298_SOURCE_BUDGET_GROWTH = OPEN",
        "TPC298_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC298_FIXED_POWER_CREDIT = 0",
        "TPC298_FULL_GATE_B = OPEN",
        "TPC298_TWIN_PRIME_RESULT = NONE",
        "TPC298_ROUND2_CLUE = TEST_WEIGHTED_PROFILE_DIMENSION_AGAINST_LEAST_NORM_SOURCE_BUDGET_AND_CONDITIONING",
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
        print("TPC298_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC298_BRIDGE_CHECK=PASS rows=18 prefixes=306 "
          "weighted_ratio=2/3 plus_dim_max=6 full_capture=18")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
