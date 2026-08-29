#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-303."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-303-cardinality-monotonicity-obstruction"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc303_cardinality_monotonicity_obstruction.md")
PRODUCER = PROJECT / "code/tpc303_cardinality_monotonicity_obstruction.py"
INDEPENDENT = PROJECT / "experiments/tpc303_independent_checker.py"
STRESS = PROJECT / "experiments/tpc303_stress.py"
CERTIFICATE = PROJECT / "results/tpc303_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_INTERVAL_DESCENT_CRITERION_PLUS_NUMERICALLY_CERTIFIED_"
    "FIXED_SOURCE_CARDINALITY_MONOTONICITY_OBSTRUCTION")
SCHEMA = "TPC303_CARDINALITY_MONOTONICITY_OBSTRUCTION_V1"
PRODUCER_SHA256 = "8f6112aa89899dfd5f6f5fdd90307ed9bf56ab2264d66158b064d76623b21c4c"
CERTIFICATE_SHA256 = "4d282a8a32ac1e916ac328a2579bb25744d8a00cfca4911f14b908387391255a"
BRIDGE_SHA256 = "c51e3cd4502478495a10850fe1ae321fcf3a1ac78da5e79eb416a8447fadbbab"
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc303_cardinality_monotonicity_obstruction.py",
    "experiments/tpc303_independent_checker.py", "experiments/tpc303_stress.py",
    "results/tpc303_certificate.json", "notes/theorem_ledger.md",
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
    audit = payload.get("finite_audit", {})
    need(audit.get("series") == 18 and
         audit.get("adjacent_transitions") == 54 and
         audit.get("certified_descents") == 21 and
         audit.get("certified_ascents") == 33 and
         audit.get("unresolved_transitions") == 0 and
         audit.get("nonmonotone_series") == 18 and
         audit.get("same_prefix_descents") == 9 and
         audit.get("fixed_power_credit") == 0,
         "finite census")
    need(len(payload.get("series", [])) == 18, "series payload")
    need(payload["firewall"].get("TPC303_CARDINALITY_MONOTONICITY") ==
         "REFUTED_SCOPED_DECLARED_FINITE_SPINE", "firewall status")
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
        "TPC303_MAXIMUM_CLAIM = " + STATUS,
        "TPC303_ROUTE_ADVANCE = YES_SCOPED_CARDINALITY_ONLY_GROWTH_REFUTATION",
        "TPC303_INTERVAL_ORDER = PROVED_EXACT_FINITE",
        "TPC303_CARDINALITY_MONOTONICITY = REFUTED_SCOPED_DECLARED_FINITE_SPINE",
        "TPC303_TRANSITION_CENSUS = NUMERICALLY_CERTIFIED_FINITE_21_DESCENTS_33_ASCENTS_0_UNRESOLVED",
        "TPC303_NONMONOTONE_SERIES = NUMERICALLY_CERTIFIED_FINITE_18_OF_18",
        "TPC303_SAME_PREFIX_DESCENTS = NUMERICALLY_CERTIFIED_FINITE_9",
        "TPC303_UNIFORM_ASYMPTOTIC_BUDGET = OPEN",
        "TPC303_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC303_FIXED_POWER_CREDIT = 0",
        "TPC303_FULL_GATE_B = OPEN",
        "TPC303_TWIN_PRIME_RESULT = NONE",
        "TPC303_ROUND2_CLUE = LOCALIZE_BUDGET_DESCENTS_BY_TRANSPORTING_SIGN_LABELS_ACROSS_OVERLAPPING_SHELLS",
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
        print("TPC303_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC303_BRIDGE_CHECK=PASS series=18 transitions=54 descents=21 "
          "ascents=33 same_prefix_descents=9 nonmonotone=18")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
