#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-333."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-333-source-polarization-cross-term"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc333_source_polarization_cross_term.md"
PRODUCER = PROJECT / "code/tpc333_source_polarization_cross_term.py"
INDEPENDENT = PROJECT / "experiments/tpc333_independent_checker.py"
STRESS = PROJECT / "experiments/tpc333_polarization_stress.py"
CERTIFICATE = PROJECT / "results/tpc333_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / "papers/tpc-332-growing-control-average-ensemble/code/tpc332_growing_control_average_ensemble.py"
PARENT_CERT = ROOT / "papers/tpc-332-growing-control-average-ensemble/results/tpc332_certificate.json"
PARENT_CODE_SHA256 = "ea742cfaaf7aa2be3c4cfad2ca603baadd65dc77619d8a1ba5ef686dd1fea5d9"
PARENT_CERT_SHA256 = "ddb0c33d09edf648df9a32c0e7cec6e8bac638cae6aba895ebf8084da5d580b9"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SOURCE_POLARIZATION_LEDGER"
SCHEMA = "TPC333_SOURCE_POLARIZATION_CROSS_TERM_V1"

# These are sealed after all release text and scripts are final.
PRODUCER_SHA256 = "1e8b104db281b6998875f2fb5b4691910c3a22ef365c796bdc879f396f8a6bde"
INDEPENDENT_SHA256 = "6f311c2cdc03bba484081f54c58add9d87ca136e622808ac1fafc1e0b352383b"
STRESS_SHA256 = "1c4cfaf79700cdfc2caf14121d2bd35dcbca31536f8df92731b56b7d1c0582b7"
CERTIFICATE_SHA256 = "3722702ab29b397c836b5ceb4cddd0b063d35e10139952dd93eb849ced2f53eb"
BRIDGE_SHA256 = "4d007c85e547a7310a57fced6d63030935c6ffb58f7f90ffb4353db58a031650"


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
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script), "--check"]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    required = (
        ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
        "PROOF_PACKAGE.md", "code/tpc333_source_polarization_cross_term.py",
        "experiments/tpc333_independent_checker.py",
        "experiments/tpc333_polarization_stress.py",
        "results/tpc333_certificate.json", "notes/theorem_ledger.md",
        "notes/claim_firewall.md", "notes/computational_protocol.md",
        "notes/route_evaluation.md", "notes/citation_verification.md",
        "paper/main.tex", "paper/references.bib", "paper/main.pdf",
        "paper/paper.pdf", "paper/compile.log")
    for relative in required:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
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
         and document.get("claim_status") == STATUS,
         "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    need(payload.get("finite_audit") == {
        "windows": 6, "growth_pairs": 4,
        "source_uniform_theorem": "OPEN", "arithmetic_advance": "NO",
        "fixed_power_credit": 0}, "finite audit")
    need(payload.get("summary", {}).get("kappa_within_[.35,.37]") == 6,
         "kappa census")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC333_SOURCE_UNIFORM_L2") == "OPEN" and
         firewall.get("TPC333_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC333_FIXED_POWER_CREDIT") == 0,
         "claim firewall")
    need(len(payload.get("rows", [])) == 6 and
         len(payload.get("growth_pairs", [])) == 4, "row geometry")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")
    need(PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100000,
         "PDF integrity")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error", "Fatal error"):
        need(bad not in log, "LaTeX diagnostic: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
        "TPC333_POLARIZATION_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC333_SIX_WINDOW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_WINDOWS",
        "TPC333_CANCELLATION_COEFFICIENT = NUMERICALLY_CERTIFIED_FINITE_0.35_TO_0.37",
        "TPC333_NEAR_ORTHOGONALITY = REFUTED_SCOPED_FINITE_PANEL",
        "TPC333_NEAR_TOTAL_CANCELLATION = REFUTED_SCOPED_FINITE_PANEL",
        "TPC333_ARITHMETIC_ADVANCE = NO", "TPC333_FIXED_POWER_CREDIT = 0",
        "TPC333_SOURCE_UNIFORM_L2 = OPEN", "TPC333_FULL_GATE_B = OPEN",
        "TPC333_TWIN_PRIME_RESULT = NONE",
        "TPC333_STATUS = " + STATUS,
        "TPC333_ROUND2_CLUE = CLASSIFY_CROSS_TERM_SUPPORT_BY_PRIME_POWER_AND_TWIN_MASK"):
        need(marker in text, "bridge marker missing")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check_files()
        check_bridge_text()
        normal = tuple(run(s, False) for s in (PRODUCER, INDEPENDENT, STRESS))
        optimized = tuple(run(s, True) for s in (PRODUCER, INDEPENDENT, STRESS))
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC333_BRIDGE_CHECK=PASS windows=6 growth_pairs=4 "
              "kappa_interval_census=6 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC333_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
