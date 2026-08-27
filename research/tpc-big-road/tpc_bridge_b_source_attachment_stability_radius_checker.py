#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for TPC-283."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-283-source-attachment-stability-radius"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_source_attachment_stability_radius.md"
PRODUCER = PROJECT / "code/tpc283_source_attachment_stability_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc283_independent_checker.py"
STRESS = PROJECT / "experiments/tpc283_stability_stress.py"
CERTIFICATE = PROJECT / "results/tpc283_certificate.json"
STATUS = (
    "PROVED_EXACT_HILBERT_SOURCE_ZEROING_RADIUS_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_VULNERABILITY_AUDIT")
SCHEMA = "TPC283_SOURCE_ATTACHMENT_STABILITY_RADIUS_CERTIFICATE_V1"
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc283_source_attachment_stability_certificate.py",
    "experiments/tpc283_independent_checker.py",
    "experiments/tpc283_stability_stress.py", "results/tpc283_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex", "paper/references.bib",
    "paper/paper.pdf",
)


class Failure(RuntimeError):
    pass


def need(c: bool, m: str) -> None:
    if type(c) is not bool or not c:
        raise Failure(m)


def canonical(v: object) -> bytes:
    return (json.dumps(v, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(b: bytes) -> str:
    return hashlib.sha256(b.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script), "--check"] if script == PRODUCER else [
        "-B", str(script)]
    env = dict(os.environ); env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check() -> None:
    bridge = BRIDGE.read_text(encoding="utf-8")
    for marker in (
        "TPC283_MAXIMUM_CLAIM = " + STATUS,
        "TPC283_ZEROING_RADIUS = PROVED_EXACT",
        "TPC283_FINITE_VULNERABILITY = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC283_ADMISSIBLE_LITERAL_SOURCE_STABILITY = OPEN",
        "TPC283_FIXED_POWER_CREDIT = 0", "TPC283_FULL_GATE_B = OPEN",
    ):
        need(marker in bridge, "bridge marker")
    for item in REQUIRED:
        need((PROJECT / item).is_file(), "missing artifact: " + item)
    raw = CERTIFICATE.read_bytes(); data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data["claim_status"] == STATUS and
         data["payload"]["schema"] == SCHEMA, "certificate header")
    need(data["payload_sha256"] == digest(canonical(data["payload"])), "hash")
    audit = data["payload"]["finite_audit"]
    need(audit["rows"] == 12 and audit["positive_radius_rows"] == 12 and
         audit["relative_radius_upper_below_3_over_10"] == 12 and
         audit["relative_radius_upper_below_1_over_10"] == 6 and
         audit["fixed_power_credit"] == 0, "audit census")
    pdf = (PROJECT / "paper/paper.pdf").read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 50_000, "PDF")
    for script in (PRODUCER, INDEPENDENT, STRESS):
        normal = run(script, False); optimized = run(script, True)
        need(normal == optimized, script.name + " optimized mismatch")
    print("TPC283_BRIDGE_CHECK=PASS theorem=EXACT_ZEROING_RADIUS rows=12 "
          "under_30_percent=12 under_10_percent=6 fixed_power_credit=0")
    print("claim_level=" + STATUS)


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC283_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
