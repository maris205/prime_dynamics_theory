#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-340."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc340_schur_frobenius_hybrid_envelope.md"
PRODUCER = PROJECT / "code/tpc340_schur_frobenius_hybrid_envelope.py"
INDEPENDENT = PROJECT / "experiments/tpc340_independent_checker.py"
STRESS = PROJECT / "experiments/tpc340_hybrid_stress.py"
CERTIFICATE = PROJECT / "results/tpc340_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / "papers/tpc-339-mask-aware-frobenius-envelope/code/"
PARENT_CODE = PARENT_CODE / "tpc339_mask_aware_frobenius_envelope.py"
PARENT_CERT = ROOT / "papers/tpc-339-mask-aware-frobenius-envelope/results/"
PARENT_CERT = PARENT_CERT / "tpc339_certificate.json"
PARENT_CODE_SHA256 = "df76022bfa5051477ec5bc04fef444aefc22abcb8f76fa02b339b7bc769fad18"
PARENT_CERT_SHA256 = "af6636eb7c9d9c6cbc0d392ae0b9effbaa9610dedafa12ee8d1272163fd48372"
SCHEMA = "TPC340_SCHUR_FROBENIUS_HYBRID_ENVELOPE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE"
PRODUCER_SHA256 = "218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f"
INDEPENDENT_SHA256 = "4cff79b0f5c300357af4889e87a0734bbfdcc7f538ee19d313d8f2176a1b583c"
STRESS_SHA256 = "bbf4db1242e3a89477a87ced4f5cc72d2e1bfd1115ae9b176863d47ee4dbcf62"
CERTIFICATE_SHA256 = "0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d"
BRIDGE_SHA256 = "84afccf4efe874728afbbc6d0d43d0e7351469fe5ef87945d1c15a7a1ee46d09"


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
        "PROOF_PACKAGE.md", "code/tpc340_schur_frobenius_hybrid_envelope.py",
        "experiments/tpc340_independent_checker.py",
        "experiments/tpc340_hybrid_stress.py",
        "results/tpc340_certificate.json", "notes/theorem_ledger.md",
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
        "rows": 6, "origins": 2, "scales": 3, "controls": 9,
        "categories": 4, "records": 216, "nonempty_records": 198,
        "bound_checks": 216, "bound_violations": 0,
        "schur_branch_records": 54, "frobenius_branch_records": 162,
        "fixed_power_credit": 0, "arithmetic_advance": "NO"}, "audit")
    summary = payload.get("summary", {})
    need(summary.get("bound_violations") == 0 and
         summary.get("branch_total") == {"FROBENIUS": 162, "SCHUR": 54} and
         float(summary.get("broad_hybrid_occupancy_max", 1)) < 0.2 and
         float(summary.get("frobenius_improvement_max", 1)) > 4.6,
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
        "TPC340_HYBRID_BOUND = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC340_HYBRID_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_RECORDS",
        "TPC340_BOUND_CENSUS = NUMERICALLY CERTIFIED FINITE_0_VIOLATIONS",
        "TPC340_SCHUR_BRANCH_CENSUS = NUMERICALLY_CERTIFIED_FINITE_54_RECORDS",
        "TPC340_FROBENIUS_BRANCH_CENSUS = NUMERICALLY_CERTIFIED_FINITE_162_RECORDS",
        "TPC340_ZERO_SUPPORT_IMPROVEMENT = NUMERICALLY CERTIFIED FINITE FACTOR 1.25 TO 4.70",
        "TPC340_BROAD_TIGHTNESS = REFUTED_SCOPED",
        "TPC340_ARITHMETIC_ADVANCE = NO", "TPC340_FIXED_POWER_CREDIT = 0",
        "TPC340_SOURCE_UNIFORM_L2 = OPEN", "TPC340_FULL_GATE_B = OPEN",
        "TPC340_TWIN_PRIME_RESULT = NONE", "TPC340_STATUS = " + STATUS,
        "TPC340_ROUND2_CLUE = TEST_NUISANCE_ORTHOGONALIZATION_OR_ADVERSARIAL_HOLDOUT")
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
        print("TPC340_BRIDGE_CHECK=PASS rows=6 controls=9 records=216 "
              "bound_violations=0 schur_branch=54 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC340_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
