#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-342."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-342-independent-fresh-holdout-reproduction"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc342_independent_fresh_holdout_reproduction.md"
PRODUCER = PROJECT / "code/tpc342_independent_fresh_holdout_reproduction.py"
INDEPENDENT = PROJECT / "experiments/tpc342_independent_checker.py"
STRESS = PROJECT / "experiments/tpc342_holdout_stress.py"
CERTIFICATE = PROJECT / "results/tpc342_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/code/"
PARENT_CODE = PARENT_CODE / "tpc340_schur_frobenius_hybrid_envelope.py"
PARENT_CERT = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/results/"
PARENT_CERT = PARENT_CERT / "tpc340_certificate.json"
PARENT_CODE_SHA256 = "218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f"
PARENT_CERT_SHA256 = "0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d"

PROTOCOL_PROJECT = ROOT / "papers/tpc-341-fresh-holdout-nuisance-orthogonalization"
PROTOCOL_CODE = PROTOCOL_PROJECT / "code/tpc341_fresh_holdout_nuisance_orthogonalization.py"
PROTOCOL_CERT = PROTOCOL_PROJECT / "results/tpc341_certificate.json"
PROTOCOL_CODE_SHA256 = "66269d586493a51adefeb8f17638df6b2eccf7e55aeab83e099b26c7768d52ac"
PROTOCOL_CERT_SHA256 = "50f8f81f4c401924187ae90327cf787139489570cbda68707b846e3d89f36218"
SCHEMA = "TPC342_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION"
PRODUCER_SHA256 = "1c57ccd3519f20f9283b0a4f678bd2b0f81ef60e94b9db7780f4f263684e6014"
INDEPENDENT_SHA256 = "7efe03b7d24682a3f350644f563d41c314793c7d2c19bfecdf20a63164e8a349"
STRESS_SHA256 = "3944faedac41ac44be45142d3b6d2115474968a7feb0c21708cebf834f35f9ea"
CERTIFICATE_SHA256 = "7dbb39b8d38ef5d09a7b21e829d2e70469f7e9e2a1e1b135588c1413fb7cd52f"
BRIDGE_SHA256 = "dcdae57eafcb406c0b99aa9f9246cd980afecff1bf199c67e3809375d4f0f607"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


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
        "PROOF_PACKAGE.md", "code/tpc342_independent_fresh_holdout_reproduction.py",
        "experiments/tpc342_independent_checker.py",
        "experiments/tpc342_holdout_stress.py",
        "results/tpc342_certificate.json", "notes/theorem_ledger.md",
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
            (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(len(expected) == 64 and not expected.startswith("__"),
             label + " hash not sealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")
    need(digest(PROTOCOL_CODE.read_bytes()) == PROTOCOL_CODE_SHA256 and
         digest(PROTOCOL_CERT.read_bytes()) == PROTOCOL_CERT_SHA256,
         "TPC341 protocol provenance")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256 and
         digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "parent provenance")
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document) and document.get("certificate_version") == 1
         and document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    need(payload.get("finite_audit") == {
        "rows": 3, "origins": 3, "scales": 1, "controls": 9,
        "categories": 4, "raw_records": 108,
        "nonempty_raw_records": 81,
        "in_sample_projection_records": 3,
        "leave_one_control_out_records": 27,
        "rank_failures": 0, "fixed_power_credit": 0,
        "arithmetic_advance": "NO"}, "audit")
    summary = payload.get("summary", {})
    need(summary.get("rank_failures") == 0 and
         summary.get("raw_records") == 108 and
         summary.get("nonempty_raw_records") == 81 and
         summary.get("holdout_records") == 27 and
         summary.get("rank_values") == [2] and
         float(summary.get("in_sample_retention_max", 1)) < 0.30 and
         float(summary.get("holdout_retention_min", 0)) > 0.40,
         "summary")
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
        "TPC342_PROJECTION_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC342_INDEPENDENT_FRESH_REPLAY = NUMERICALLY_CERTIFIED_FINITE_108_RAW_RECORDS",
        "TPC342_IN_SAMPLE_PROJECTION = NUMERICALLY_CERTIFIED_FINITE_3_ROWS",
        "TPC342_HOLDOUT_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_27_RECORDS",
        "TPC342_IN_SAMPLE_RETENTION = NUMERICAL_OBSERVATION_0.270_TO_0.296",
        "TPC342_HOLDOUT_RETENTION = NUMERICAL_OBSERVATION_0.589_TO_0.943",
        "TPC342_CONTROL_STABILITY = REFUTED_SCOPED",
        "TPC342_ARITHMETIC_ADVANCE = NO", "TPC342_FIXED_POWER_CREDIT = 0",
        "TPC342_SOURCE_UNIFORM_L2 = OPEN", "TPC342_FULL_GATE_B = OPEN",
        "TPC342_TWIN_PRIME_RESULT = NONE", "TPC342_STATUS = " + STATUS,
        "TPC342_ROUND2_CLUE = CROSS_PANEL_META_CERTIFICATE_OR_ALTERNATIVE_NUISANCE_BASIS")
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
        print("TPC342_BRIDGE_CHECK=PASS rows=3 controls=9 raw_records=108 "
              "holdout_records=27 rank_failures=0 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC342_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
