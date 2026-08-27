#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for TPC-285."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-285-prime-shell-residue-rank-obstruction"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_prime_shell_residue_rank_obstruction.md"
PRODUCER = PROJECT / (
    "code/tpc285_prime_shell_residue_rank_certificate.py")
INDEPENDENT = PROJECT / "experiments/tpc285_independent_checker.py"
STRESS = PROJECT / "experiments/tpc285_rank_stress.py"
CERTIFICATE = PROJECT / "results/tpc285_certificate.json"
STATUS = (
    "PROVED_EXACT_CENTERED_RESIDUE_FACTORIZATION_AND_DELETED_DIAGONAL_"
    "FULL_RANK_PLUS_NUMERICALLY_CERTIFIED_KERNEL_RANK")
SCHEMA = "TPC285_PRIME_SHELL_RESIDUE_RANK_CERTIFICATE_V1"
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc285_prime_shell_residue_rank_certificate.py",
    "experiments/tpc285_independent_checker.py",
    "experiments/tpc285_rank_stress.py", "results/tpc285_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex", "paper/references.bib",
    "paper/paper.pdf",
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
    for marker in (
        "TPC285_MAXIMUM_CLAIM = " + STATUS,
        "TPC285_RESIDUE_FACTORIZATION = PROVED_EXACT",
        "TPC285_DELETED_DIAGONAL_FULL_RANK = PROVED_EXACT_UNDER_FULL_CLASS_COVERAGE",
        "TPC285_KERNEL_SCHUR_FULL_RANK = NUMERICALLY_CERTIFIED_FINITE_20_ROWS",
        "TPC285_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC285_FIXED_POWER_CREDIT = 0",
        "TPC285_FULL_GATE_B = OPEN",
    ):
        need(marker in bridge, "bridge marker")
    for item in REQUIRED:
        need((PROJECT / item).is_file(), "missing artifact: " + item)
    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data["claim_status"] == STATUS and
         data["payload"]["schema"] == SCHEMA, "certificate header")
    need(data["payload_sha256"] == digest(canonical(data["payload"])),
         "certificate payload hash")
    finite = data["payload"]["finite_audit"]
    need(finite == {
        "centered_rank_rows": 20,
        "deleted_diagonal_exact_full_rank_rows": 20,
        "deleted_diagonal_full_active_rank_rows": 20,
        "factorization_rows": 20,
        "fixed_power_credit": 0,
        "kernel_schur_full_active_rank_rows": 20,
        "literal_arithmetic_L2": "OPEN",
        "rows": 20,
    }, "finite census")
    pdf = (PROJECT / "paper/paper.pdf").read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 50_000, "PDF")
    for script in (PRODUCER, INDEPENDENT, STRESS):
        normal = run(script, False)
        optimized = run(script, True)
        need(normal == optimized, script.name + " optimized mismatch")
    print("TPC285_BRIDGE_CHECK=PASS rows=20 factorization=20 centered_rank=20 "
          "deleted_full_rank=20 kernel_full_rank=20 fixed_power_credit=0")
    print("claim_level=" + STATUS)


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC285_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
