#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-344."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-344-panel-contrast-nuisance-basis"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc344_panel_contrast_nuisance_basis.md"
PRODUCER = PROJECT / "code/tpc344_panel_contrast_nuisance_basis.py"
INDEPENDENT = PROJECT / "experiments/tpc344_independent_checker.py"
STRESS = PROJECT / "experiments/tpc344_meta_stress.py"
CERTIFICATE = PROJECT / "results/tpc344_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PRODUCER_SHA256 = "08daa3e1b5782e619f492039ed0b8f734de923dfc39797d88eea8a5650ce83ba"
INDEPENDENT_SHA256 = "47b03f7cc9ed1cbc8f92a70e39d67371850816809af68fc1d959a1b60e65513c"
STRESS_SHA256 = "4ee398ebbac3b0e696c8c29b7084a4006853b7440689e76dcaec2caf27a12659"
CERTIFICATE_SHA256 = "29da3486ef9c1fcb7ec4274203e93059959736b05ea0eb3bf7f8f69e69a63460"
MAIN_PDF_SHA256 = "41b9edfc2823e8ecef28944593b691debf2369a43d06744620afd37e5d82615f"
BRIDGE_SHA256 = "eb85bb4a0da89146a923a7e5d1431a1d29fa48d7e95b8d96a173895815916936"

TPC343_CODE = ROOT / "papers/tpc-343-cross-panel-meta-certificate/code/tpc343_cross_panel_meta_certificate.py"
TPC343_CERT = ROOT / "papers/tpc-343-cross-panel-meta-certificate/results/tpc343_certificate.json"
TPC343_CODE_SHA256 = "b10192be90572f210c2f0551576abd659c8d518845dee7e61793feab6de3d13b"
TPC343_CERT_SHA256 = "eff6671b5ef1345f9f88db438b962f19c714651839f0015c7cd1f7ebbb6a4568"

SCHEMA = "TPC344_PANEL_CONTRAST_NUISANCE_BASIS_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PANEL_CONTRAST_BASIS_AUDIT"


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
    command.extend(["-B", str(script), "--check"])
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["OMP_NUM_THREADS"] = "8"
    environment["OPENBLAS_NUM_THREADS"] = "8"
    environment["MKL_NUM_THREADS"] = "8"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    required = (
        ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
        "PROOF_PACKAGE.md", "code/tpc344_panel_contrast_nuisance_basis.py",
        "experiments/tpc344_independent_checker.py",
        "experiments/tpc344_meta_stress.py", "results/tpc344_certificate.json",
        "notes/theorem_ledger.md", "notes/claim_firewall.md",
        "notes/computational_protocol.md", "notes/route_evaluation.md",
        "notes/citation_verification.md", "paper/main.tex", "paper/main.pdf",
        "paper/paper.pdf", "paper/compile.log")
    for item in required:
        need((PROJECT / item).is_file(), "missing artifact: " + item)
    for path, expected, label in (
            (PRODUCER, PRODUCER_SHA256, "producer"),
            (INDEPENDENT, INDEPENDENT_SHA256, "independent"),
            (STRESS, STRESS_SHA256, "stress"),
            (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
            (MAIN_PDF, MAIN_PDF_SHA256, "main pdf"),
            (PDF, MAIN_PDF_SHA256, "paper pdf"),
            (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(digest(path.read_bytes()) == expected, label + " provenance")
    for path, expected, label in (
            (TPC343_CODE, TPC343_CODE_SHA256, "TPC343 producer"),
            (TPC343_CERT, TPC343_CERT_SHA256, "TPC343 certificate")):
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
        "panels": 2, "rows": 6, "origins": 6, "scales": 1,
        "controls": 9, "categories": 4, "raw_records": 216,
        "nonempty_raw_records": 171, "in_sample_records": 6,
        "holdout_records": 18, "crossfit_directions": 4,
        "basis_columns_declared": 6, "basis_rank_observed": 5,
        "fixed_power_credit": 0, "arithmetic_advance": "NO"}, "audit")
    rows = payload.get("rows", [])
    need(len(rows) == 6 and
         [row.get("origin") for row in rows] ==
         [48097, 48609, 49217, 40097, 40609, 41121], "rows")
    for row in rows:
        need(row.get("cutoff_safe") is True and
             len(row.get("raw_records", [])) == 36 and
             len(row.get("holdout", [])) == 9, "row geometry")
    summary = payload.get("summary", {})
    need(float(summary.get("contrast_raw_retention", 1)) < 0.30 and
         float(summary.get("contrast_equal_row_retention", 0)) >= 0.30 and
         float(summary.get("holdout_retention_min", 0)) > 0.40 and
         float(summary.get("crossfit_retention_min", 0)) > 0.30 and
         summary.get("weighting_stability") == "REFUTED_SCOPED" and
         summary.get("crossfit_transfer") == "REFUTED_SCOPED", "guards")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC344_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC344_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC344_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC344_TWIN_PRIME_RESULT") == "NONE", "firewall")
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
        "TPC344_MAXIMUM_CLAIM = " + STATUS,
        "TPC344_CONTRAST_SPAN_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC344_RAW_CONTRAST_GUARD = NUMERICALLY_CERTIFIED_FINITE_SCOPED_PASS",
        "TPC344_EQUAL_ROW_CONTRAST_GUARD = REFUTED_SCOPED",
        "TPC344_WEIGHTING_STABILITY = REFUTED_SCOPED",
        "TPC344_CROSSFIT_TRANSFER = REFUTED_SCOPED",
        "TPC344_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_18_RECORDS",
        "TPC344_ARITHMETIC_ADVANCE = NO",
        "TPC344_FIXED_POWER_CREDIT = 0",
        "TPC344_FULL_GATE_B = OPEN",
        "TPC344_TWIN_PRIME_RESULT = NONE",
        "TPC344_STATUS = " + STATUS,
        "TPC344_ROUND2_CLUE = PRINCIPAL_ANGLE_GRASSMANN_STABILITY_AUDIT")
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
        print("TPC344_BRIDGE_CHECK=PASS rows=6 raw_records=216 "
              "contrast_raw=0.2962189247 contrast_equal_row=0.3186506700 "
              "holdout_records=18")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC344_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
