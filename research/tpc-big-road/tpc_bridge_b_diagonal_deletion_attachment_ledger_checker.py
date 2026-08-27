#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for TPC-286."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-286-diagonal-deletion-attachment-ledger"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_diagonal_deletion_attachment_ledger.md")
PRODUCER = PROJECT / (
    "code/tpc286_diagonal_deletion_attachment_certificate.py")
INDEPENDENT = PROJECT / "experiments/tpc286_independent_checker.py"
STRESS = PROJECT / "experiments/tpc286_diagonal_sensitivity_stress.py"
CERTIFICATE = PROJECT / "results/tpc286_certificate.json"
STATUS = (
    "PROVED_EXACT_LINEAR_DIAGONAL_DELETION_ATTACHMENT_SPLIT_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_DIAGONAL_SENSITIVITY_LEDGER")
SCHEMA = "TPC286_DIAGONAL_DELETION_ATTACHMENT_CERTIFICATE_V1"
CERTIFICATE_SHA256 = (
    "d8f707f5a1297e6f286ed9e0c7330a90d99c699ab8c91b98d6c7c22e99078beb")
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc286_diagonal_deletion_attachment_certificate.py",
    "experiments/tpc286_independent_checker.py",
    "experiments/tpc286_diagonal_sensitivity_stress.py",
    "results/tpc286_certificate.json", "notes/theorem_ledger.md",
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
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check() -> None:
    bridge = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC286_MAXIMUM_CLAIM = " + STATUS,
        "TPC286_ATTACHMENT_SPLIT = PROVED_EXACT_LINEARITY",
        "TPC286_COMPONENT_SIGN_LEDGER = NUMERICALLY_CERTIFIED_FINITE_72_ROWS",
        "TPC286_FULL_VS_PHYSICAL_FLIPS = NUMERICALLY_CERTIFIED_FINITE_15_ROWS",
        "TPC286_DIAGONAL_OPPOSITION = NUMERICALLY_CERTIFIED_FINITE_30_ROWS",
        "TPC286_DIAGONAL_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_21_ROWS",
        "TPC286_ASYMPTOTIC_DIAGONAL_DOMINANCE = OPEN",
        "TPC286_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC286_FIXED_POWER_CREDIT = 0",
        "TPC286_FULL_GATE_B = OPEN",
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
    need(data["payload_sha256"] == digest(canonical(data["payload"])),
         "certificate payload hash")
    finite = data["payload"]["finite_audit"]
    need(finite == {
        "asymptotic_diagonal_dominance": "OPEN",
        "component_sign_separated_rows": 72,
        "diagonal_correction_negative_rows": 34,
        "diagonal_correction_positive_rows": 38,
        "diagonal_opposes_physical_rows": 30,
        "diagonal_ratio_lower_exceeds_10_rows": 4,
        "diagonal_ratio_lower_exceeds_2_rows": 13,
        "diagonal_strictly_dominates_physical_rows": 21,
        "fixed_power_credit": 0,
        "full_including_diagonal_negative_rows": 49,
        "full_including_diagonal_positive_rows": 23,
        "full_vs_physical_sign_flip_rows": 15,
        "physical_negative_rows": 60,
        "physical_positive_rows": 12,
        "reconstruction_contained_rows": 72,
        "rows": 72,
    }, "finite census")
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
    print("TPC286_BRIDGE_CHECK=PASS rows=72 full_negative=49 "
          "diagonal_negative=34 physical_negative=60 full_physical_flips=15 "
          "diagonal_opposes=30 diagonal_dominates=21 fixed_power_credit=0")
    print("claim_level=" + STATUS)


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC286_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
