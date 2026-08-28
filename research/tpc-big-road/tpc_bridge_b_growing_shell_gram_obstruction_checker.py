#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for TPC-288."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-288-growing-shell-gram-obstruction"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_growing_shell_gram_obstruction.md"
PRODUCER = PROJECT / "code/tpc288_growing_shell_gram_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc288_independent_checker.py"
STRESS = PROJECT / "experiments/tpc288_gram_stress.py"
CERTIFICATE = PROJECT / "results/tpc288_certificate.json"
STATUS = (
    "PROVED_EXACT_PHYSICAL_OUTPUT_GRAM_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_GROWING_SHELL_FULL_RANK_OBSTRUCTION")
SCHEMA = "TPC288_GROWING_SHELL_GRAM_OBSTRUCTION_CERTIFICATE_V1"
CERTIFICATE_SHA256 = (
    "39ab30b6701015bfaf85ebb670706182ecd7b52120e9963d58d0731a0a8e947d")
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc288_growing_shell_gram_certificate.py",
    "experiments/tpc288_independent_checker.py",
    "experiments/tpc288_gram_stress.py", "results/tpc288_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex",
    "paper/references.bib", "paper/paper.pdf",
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
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check() -> None:
    bridge = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC288_MAXIMUM_CLAIM = " + STATUS,
        "TPC288_ROUTE_ADVANCE = YES_SCOPED_GROWING_SHELL_GRAM_OBSTRUCTION_AND_FULL_RANK_AUDIT",
        "TPC288_EXACT_OPERATOR_ADDITIVITY = PROVED_EXACT_FINITE",
        "TPC288_EXACT_OUTPUT_GRAM_IDENTITY = PROVED_EXACT_FINITE",
        "TPC288_GRAM_PSD = PROVED_EXACT_FINITE",
        "TPC288_GRAM_FULL_RANK = NUMERICALLY_CERTIFIED_FINITE_34_OF_34",
        "TPC288_OPERATOR_FULL_ACTIVE_RANK = NUMERICALLY_CERTIFIED_FINITE_6_OF_6_SELECTED",
        "TPC288_SCALAR_ENERGY_MISMATCH = NUMERICALLY_CERTIFIED_FINITE_13_ROWS",
        "TPC288_ENERGY_AMPLIFIED = NUMERICALLY_CERTIFIED_FINITE_34_OF_34",
        "TPC288_MAX_SHELL_CARDINALITY = 17",
        "TPC288_GROWING_SHELL_STABILITY = OPEN",
        "TPC288_SOURCE_CONTROL_UNIFORMITY = OPEN",
        "TPC288_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC288_FIXED_POWER_CREDIT = 0",
        "TPC288_FULL_GATE_B = OPEN",
        "TPC288_TWIN_PRIME_RESULT = NONE",
        "TPC288_ROUND2_CLUE = TEST_SOURCE_NATIVE_CROSS_PRIME_GRAM_BOUNDS_BEYOND_FINITE_FULL_RANK_OBSTRUCTION",
    )
    for marker in markers:
        need(marker in bridge, "bridge marker")
    for item in REQUIRED:
        need((PROJECT / item).is_file(), "missing artifact: " + item)

    raw = CERTIFICATE.read_bytes()
    need(digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS and
         data.get("payload", {}).get("schema") == SCHEMA,
         "certificate header")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")
    audit = data["payload"]["finite_audit"]
    need(audit == {
        "component_scalar_crossings": 0,
        "distinct_shell_anchors": 8,
        "energy_amplified_rows": 34,
        "fixed_power_credit": 0,
        "gram_full_rank_rows": 34,
        "growing_shell_theorem": "OPEN",
        "growth_rows": 16,
        "literal_arithmetic_L2": "OPEN",
        "max_shell_cardinality": 17,
        "operator_full_active_rank_rows": 6,
        "operator_rank_audited_rows": 6,
        "rows": 34,
        "scalar_energy_mismatch_rows": 13,
        "scalar_upper_lt_tenth_rows": 13,
        "source_control_rows": 18,
    }, "finite audit")
    need(len(data["payload"]["rows"]) == 34, "row census")
    need(all(row["gram_positive_definite"] for row in data["payload"]["rows"]),
         "Gram positivity flags")
    pdf = (PROJECT / "paper/paper.pdf").read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 50_000, "PDF")
    log = (PROJECT / "paper/main.log").read_text(encoding="utf-8")
    need("undefined" not in log.lower() and "LaTeX Warning:" not in log and
         "Package rerunfilecheck Warning:" not in log and
         "Overfull \\hbox" not in log and "Underfull \\hbox" not in log,
         "LaTeX warning or undefined reference")

    for script in (PRODUCER, INDEPENDENT, STRESS):
        normal = run(script, False)
        optimized = run(script, True)
        need(normal == optimized, script.name + " optimized mismatch")
    print("TPC288_BRIDGE_CHECK=PASS rows=34 gram_full_rank=34 "
          "operator_full_rank=6 energy_amplified=34 scalar_lt_tenth=13 "
          "mismatch=13")
    print("claim_level=" + STATUS)


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC288_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
