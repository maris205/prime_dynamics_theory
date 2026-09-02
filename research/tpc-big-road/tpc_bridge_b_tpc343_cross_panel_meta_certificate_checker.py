#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-343."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-343-cross-panel-meta-certificate"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc343_cross_panel_meta_certificate.md"
PRODUCER = PROJECT / "code/tpc343_cross_panel_meta_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc343_independent_checker.py"
STRESS = PROJECT / "experiments/tpc343_meta_stress.py"
CERTIFICATE = PROJECT / "results/tpc343_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PARENT_CODE = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/code/tpc340_schur_frobenius_hybrid_envelope.py"
PARENT_CERT = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/results/tpc340_certificate.json"
PARENT_CODE_SHA256 = "218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f"
PARENT_CERT_SHA256 = "0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d"
TPC341_CODE = ROOT / "papers/tpc-341-fresh-holdout-nuisance-orthogonalization/code/tpc341_fresh_holdout_nuisance_orthogonalization.py"
TPC341_CERT = ROOT / "papers/tpc-341-fresh-holdout-nuisance-orthogonalization/results/tpc341_certificate.json"
TPC341_CODE_SHA256 = "66269d586493a51adefeb8f17638df6b2eccf7e55aeab83e099b26c7768d52ac"
TPC341_CERT_SHA256 = "50f8f81f4c401924187ae90327cf787139489570cbda68707b846e3d89f36218"
TPC342_CODE = ROOT / "papers/tpc-342-independent-fresh-holdout-reproduction/code/tpc342_independent_fresh_holdout_reproduction.py"
TPC342_CERT = ROOT / "papers/tpc-342-independent-fresh-holdout-reproduction/results/tpc342_certificate.json"
TPC342_CODE_SHA256 = "1c57ccd3519f20f9283b0a4f678bd2b0f81ef60e94b9db7780f4f263684e6014"
TPC342_CERT_SHA256 = "7dbb39b8d38ef5d09a7b21e829d2e70469f7e9e2a1e1b135588c1413fb7cd52f"

SCHEMA = "TPC343_CROSS_PANEL_META_CERTIFICATE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_PANEL_META_CERTIFICATE"
PRODUCER_SHA256 = "b10192be90572f210c2f0551576abd659c8d518845dee7e61793feab6de3d13b"
INDEPENDENT_SHA256 = "d2a7dd8b7dce41fbecebdabe1c9ac30538f177778207c7dfdc9d207d64104d31"
STRESS_SHA256 = "32295d5b198a1ee193b1ce03e09648b70bd1a35dfa47ddae010120d098fd4d58"
CERTIFICATE_SHA256 = "eff6671b5ef1345f9f88db438b962f19c714651839f0015c7cd1f7ebbb6a4568"
BRIDGE_SHA256 = "c40a0670ff0a7f1f85c00188bb0a94739c0d0dfb43f62f506c0cd96c9c61adca"


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
        "PROOF_PACKAGE.md", "code/tpc343_cross_panel_meta_certificate.py",
        "experiments/tpc343_independent_checker.py",
        "experiments/tpc343_meta_stress.py", "results/tpc343_certificate.json",
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
            (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(len(expected) == 64 and not expected.startswith("__"),
             label + " hash not sealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")
    for path, expected, label in (
            (PARENT_CODE, PARENT_CODE_SHA256, "TPC340 code"),
            (PARENT_CERT, PARENT_CERT_SHA256, "TPC340 certificate"),
            (TPC341_CODE, TPC341_CODE_SHA256, "TPC341 code"),
            (TPC341_CERT, TPC341_CERT_SHA256, "TPC341 certificate"),
            (TPC342_CODE, TPC342_CODE_SHA256, "TPC342 code"),
            (TPC342_CERT, TPC342_CERT_SHA256, "TPC342 certificate")):
        need(digest(path.read_bytes()) == expected, label + " provenance")
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document) and document.get("certificate_version") == 1
         and document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    need(payload.get("finite_audit") == {
        "panels": 2, "rows": 6, "origins": 6, "scales": 1,
        "controls": 9, "categories": 4, "raw_records": 216,
        "nonempty_raw_records": 171, "in_sample_records": 6,
        "holdout_records": 54, "fixed_power_credit": 0,
        "arithmetic_advance": "NO"}, "audit")
    rows = payload.get("rows", [])
    need(len(rows) == 6 and [row.get("origin") for row in rows] ==
         [48097, 48609, 49217, 40097, 40609, 41121], "rows")
    for row in rows:
        need(row.get("cutoff_safe") is True and
             len(row.get("raw_records", [])) == 36 and
             len(row.get("holdout", [])) == 9 and
             row.get("in_sample", {}).get("identity_holds") is True,
             "row geometry")
    summary = payload.get("summary", {})
    need(float(summary.get("row_block_meta_retention", 1)) < 0.30 and
         float(summary.get("shared_raw_meta_retention", 0)) >= 0.30 and
         float(summary.get("shared_equal_row_meta_retention", 0)) >= 0.30 and
         float(summary.get("shared_holdout_raw_min", 0)) > 0.40 and
         summary.get("shared_coefficient_guard") == "REFUTED_SCOPED",
         "meta guards")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC343_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC343_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC343_SHARED_COEFFICIENT_STABILITY") ==
         "REFUTED_SCOPED" and firewall.get("TPC343_FULL_GATE_B") == "OPEN",
         "claim firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100_000,
         "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox", "Underfull \\hbox",
                "LaTeX Error", "Fatal error"):
        need(bad not in log, "LaTeX diagnostic: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC343_STACKED_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC343_ROW_BLOCK_META = NUMERICALLY_CERTIFIED_FINITE_6_ROW_POOLED_PROJECTION",
        "TPC343_SHARED_COEFFICIENT_RAW = NUMERICAL_OBSERVATION_0.319_TO_0.320",
        "TPC343_SHARED_COEFFICIENT_EQUAL_ROW = NUMERICAL_OBSERVATION_0.354_TO_0.355",
        "TPC343_SHARED_COEFFICIENT_STABILITY = REFUTED_SCOPED",
        "TPC343_HOLDOUT_META = NUMERICALLY_CERTIFIED_FINITE_54_RECORDS",
        "TPC343_ARITHMETIC_ADVANCE = NO", "TPC343_FIXED_POWER_CREDIT = 0",
        "TPC343_FULL_GATE_B = OPEN", "TPC343_STATUS = " + STATUS,
        "TPC343_ROUND2_CLUE = ALTERNATIVE_NUISANCE_BASIS_OR_PRINCIPAL_ANGLE_AUDIT")
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
        print("TPC343_BRIDGE_CHECK=PASS panels=2 rows=6 controls=9 "
              "raw_records=216 holdout_records=54 shared_guard=REFUTED_SCOPED")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC343_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
