#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for TPC-284."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-284-admissible-source-control-atlas"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_admissible_source_control_atlas.md"
PRODUCER = PROJECT / (
    "code/tpc284_admissible_source_control_atlas_certificate.py")
INDEPENDENT = PROJECT / "experiments/tpc284_independent_checker.py"
STRESS = PROJECT / "experiments/tpc284_atlas_stress.py"
CERTIFICATE = PROJECT / "results/tpc284_certificate.json"
STATUS = (
    "NUMERICALLY_CERTIFIED_FINITE_ADMISSIBLE_CONTROL_ATLAS_PLUS_"
    "SIGN_FLIP_OBSTRUCTION")
SCHEMA = "TPC284_ADMISSIBLE_SOURCE_CONTROL_ATLAS_CERTIFICATE_V1"
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc284_admissible_source_control_atlas_certificate.py",
    "experiments/tpc284_independent_checker.py",
    "experiments/tpc284_atlas_stress.py", "results/tpc284_certificate.json",
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
        "TPC284_MAXIMUM_CLAIM = " + STATUS,
        "TPC284_CONTROL_ATLAS = NUMERICALLY_CERTIFIED_FINITE_72_ROWS",
        "TPC284_CONTROL_SIGN_CENSUS = 60_NEGATIVE_12_POSITIVE_0_CROSSING",
        "TPC284_SIGN_FLIP_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_8_FLIPS",
        "TPC284_ASYMPTOTIC_CONTROL_STABILITY = OPEN",
        "TPC284_FIXED_POWER_CREDIT = 0",
        "TPC284_FULL_GATE_B = OPEN",
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
    finite = data["payload"]["finite_theorem"]
    need(finite == {
        "all_rows_finite_nonzero": True,
        "asymptotic_control_stability": "OPEN",
        "fixed_power_credit": 0,
        "literal_source_class_exhaustion": "NOT_CLAIMED",
        "negative_rows": 60,
        "positive_rows": 12,
        "rows": 72,
        "sign_flip_rows_against_baseline": 8,
        "statement": "six declared local schedule controls are sign-separated on all 72 registered finite rows",
        "zero_crossing_rows": 0,
    }, "finite census")
    pdf = (PROJECT / "paper/paper.pdf").read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 50_000, "PDF")
    for script in (PRODUCER, INDEPENDENT, STRESS):
        normal = run(script, False)
        optimized = run(script, True)
        need(normal == optimized, script.name + " optimized mismatch")
    print("TPC284_BRIDGE_CHECK=PASS rows=72 negative=60 positive=12 "
          "sign_flips=8 fixed_power_credit=0")
    print("claim_level=" + STATUS)


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC284_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
