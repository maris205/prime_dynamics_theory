#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-346."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-346-third-panel-hostile-replication"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc346_third_panel_hostile_replication.md"
PRODUCER = PROJECT / "code/tpc346_third_panel_hostile_replication.py"
INDEPENDENT = PROJECT / "experiments/tpc346_independent_checker.py"
STRESS = PROJECT / "experiments/tpc346_hostile_stress.py"
CERTIFICATE = PROJECT / "results/tpc346_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PRODUCER_SHA256 = "2c0bb5fd2e8738fa18dc419491a91b29c5a1fb8cc4f5fabaaec19e0a45752d4a"
INDEPENDENT_SHA256 = "485641b63d9e51220c681013f73ac9bf74f80057636f00e7fc77f8978d66772e"
STRESS_SHA256 = "6521750349f83b79b401260dcea995baa044b663b16306c5460947e2109e5a5c"
CERTIFICATE_SHA256 = "f15c5a5bf3ef9f14a5bdd9503bb74dbcc218b82b0598db0726d61deb01ee1e46"
PDF_SHA256 = "e3fc03fb10c33f5be7d2b0b1eae0df2dd0fd89974ba8215c99a3183f3a80812a"
BRIDGE_SHA256 = "6a6e9930157f514d1244fdaff8af7210e394e6ef1c3d1269c2d08ded44d896b2"

SCHEMA = "TPC346_THIRD_PANEL_HOSTILE_REPLICATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION"
ORIGINS = [48097, 48609, 49217, 40097, 40609, 41121, 44097, 44609, 45217]


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script)])
    if script == PRODUCER:
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["OMP_NUM_THREADS"] = "32"
    environment["OPENBLAS_NUM_THREADS"] = "32"
    environment["MKL_NUM_THREADS"] = "32"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    required = (
        ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
        "PROOF_PACKAGE.md", "code/tpc346_third_panel_hostile_replication.py",
        "experiments/tpc346_independent_checker.py",
        "experiments/tpc346_hostile_stress.py",
        "results/tpc346_certificate.json", "notes/theorem_ledger.md",
        "notes/claim_firewall.md", "notes/computational_protocol.md",
        "notes/route_evaluation.md", "notes/citation_verification.md",
        "paper/main.tex", "paper/main.pdf", "paper/paper.pdf",
        "paper/compile.log")
    for item in required:
        need((PROJECT / item).is_file(), "missing artifact: " + item)
    for path, expected, label in (
            (PRODUCER, PRODUCER_SHA256, "producer"),
            (INDEPENDENT, INDEPENDENT_SHA256, "independent"),
            (STRESS, STRESS_SHA256, "stress"),
            (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
            (MAIN_PDF, PDF_SHA256, "main pdf"),
            (PDF, PDF_SHA256, "paper pdf"),
            (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(expected != "TO_BE_FILLED", label + " hash not sealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")

    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document) and
         document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    need(payload.get("finite_audit") == {
        "panels": 3, "rows": 9, "origins": 9, "controls": 9,
        "categories": 4, "raw_records": 324,
        "nonempty_raw_records": 261, "weightings": 2,
        "pairwise_geometry_comparisons": 6,
        "directed_panel_predictions_per_weighting": 6,
        "leave_one_panel_out_per_weighting": 3,
        "fresh_control_loo_per_weighting": 9,
        "fixed_power_credit": 0, "arithmetic_advance": "NO"}, "audit census")
    protocol = payload.get("protocol", {})
    need(protocol.get("fresh_panel") == "TPC346" and
         protocol.get("scale") == 1024 and
         protocol.get("operator") == {
             "law": "all_plus", "Q": 54,
             "kernel_exponent": 1, "height": 66}, "protocol")
    rows = payload.get("rows", [])
    need(len(rows) == 9 and
         [item.get("origin") for item in rows] == ORIGINS, "row origins")
    for row in rows:
        need(row.get("source_interval") ==
             [row["origin"], row["origin"] + 511] and
             row.get("cutoff_safe") is True and
             len(row.get("raw_records", [])) == 36, "row geometry")
    weightings = payload.get("weighting_results", [])
    need([item.get("label") for item in weightings] == ["raw", "equal_row"],
         "weightings")
    for item in weightings:
        need(len(item.get("panel_geometry", [])) == 3 and
             len(item.get("pairwise_geometry", [])) == 3 and
             len(item.get("directed_predictions", [])) == 6 and
             len(item.get("leave_one_panel_out", [])) == 3 and
             len(item.get("fresh_control_loo", [])) == 9,
             "nested census")
        need(item.get("shared_three_panel", {}).get("identity_holds") is True and
             item.get("panel_adaptive_three_panel", {}).get(
                 "identity_holds") is True, "model identities")
    summary = payload.get("summary", {})
    need(float(summary.get("fresh_panel_raw_retention", 0)) >= 0.30 and
         float(summary.get("fresh_panel_equal_row_retention", 0)) >= 0.30 and
         float(summary.get("shared_three_panel_raw_retention", 0)) >= 0.30 and
         float(summary.get("shared_three_panel_equal_row_retention", 0)) >= 0.30 and
         float(summary.get("panel_adaptive_three_panel_raw_retention", 1)) < 0.30 and
         float(summary.get("panel_adaptive_three_panel_equal_row_retention", 0)) >= 0.30 and
         float(summary.get("directed_prediction_min", 0)) > 0.30 and
         float(summary.get("leave_one_panel_out_min", 0)) > 0.30 and
         float(summary.get("fresh_control_loo_min", 0)) > 0.30 and
         summary.get("panel_adaptive_raw_guard") == "PASS_FINITE_SCOPED" and
         summary.get("panel_adaptive_equal_row_guard") == "REFUTED_SCOPED" and
         summary.get("fresh_panel_own_fit") == "REFUTED_SCOPED" and
         summary.get("third_panel_transfer") == "REFUTED_SCOPED" and
         summary.get("route_decision") ==
         "FREEZE_PANEL_ADAPTIVE_ROUTE_FINITE_SCOPED", "summary guards")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC346_NESTED_MODEL_IDENTITY") ==
         "PROVED_EXACT_FINITE_DECLARED_MODEL" and
         firewall.get("TPC346_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC346_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC346_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC346_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100_000,
         "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox", "Underfull \\hbox",
                "LaTeX Error", "Fatal error", "Citation"):
        need(bad not in log, "LaTeX diagnostic: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC346_MAXIMUM_CLAIM = " + STATUS,
        "TPC346_NESTED_MODEL_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC346_FRESH_PANEL_OWN_FIT = REFUTED_SCOPED",
        "TPC346_SHARED_THREE_PANEL = REFUTED_SCOPED",
        "TPC346_PANEL_ADAPTIVE_RAW = NUMERICALLY_CERTIFIED_FINITE_SCOPED_PASS",
        "TPC346_PANEL_ADAPTIVE_EQUAL_ROW = REFUTED_SCOPED",
        "TPC346_PANEL_ADAPTIVE_WEIGHTING_STABILITY = REFUTED_SCOPED",
        "TPC346_THIRD_PANEL_TRANSFER = REFUTED_SCOPED",
        "TPC346_ARITHMETIC_ADVANCE = NO",
        "TPC346_FIXED_POWER_CREDIT = 0",
        "TPC346_FULL_GATE_B = OPEN",
        "TPC346_TWIN_PRIME_RESULT = NONE",
        "TPC346_ROUND2_CLUE = FREEZE_PANEL_ADAPTIVE_ROUTE_AND_RETURN_TO_ARITHMETIC_L2",
        "TPC346_STATUS = " + STATUS)
    for marker in markers:
        need(marker in text, "bridge marker missing")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check_files()
        check_bridge_text()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        normal = tuple(run(script, False) for script in scripts)
        optimized = tuple(run(script, True) for script in scripts)
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC346_BRIDGE_CHECK=PASS panels=3 rows=9 raw_records=324 "
              "nonempty=261 adaptive_raw=0.2999630725662 "
              "adaptive_equal_row=0.3222362713305 fresh_loo_pairs=18")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC346_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
