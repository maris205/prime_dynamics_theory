#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-294."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_magnitude_weighted_signed_rayleigh_atlas.md")
PRODUCER = PROJECT / (
    "code/tpc294_magnitude_weighted_signed_rayleigh_certificate.py")
INDEPENDENT = PROJECT / "experiments/tpc294_independent_checker.py"
STRESS = PROJECT / "experiments/tpc294_magnitude_weighted_stress.py"
CERTIFICATE = PROJECT / "results/tpc294_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_TRACE_NORMALIZED_SIGNED_QUADRATIC_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_GLOBAL_SIGN_ATLAS")
SCHEMA = "TPC294_MAGNITUDE_WEIGHTED_SIGNED_RAYLEIGH_CERTIFICATE_V1"
PRODUCER_SHA256 = (
    "74fadde1853e2e03aee223a61393ceb845326ce8c7baf5d2a4015be988dc62d2")
CERTIFICATE_SHA256 = (
    "a6304d622dc017b15277866c261287000eed119d1f19b7291f9ac191545d14f2")

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc294_magnitude_weighted_signed_rayleigh_certificate.py",
    "experiments/tpc294_independent_checker.py",
    "experiments/tpc294_magnitude_weighted_stress.py",
    "results/tpc294_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/paper.pdf")


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
    command += ["-B", str(script)]
    if script == PRODUCER:
        command.append("--check")
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    for item in REQUIRED:
        need((PROJECT / item).is_file(), "missing artifact: " + item)
    need(digest(PRODUCER.read_bytes()) == PRODUCER_SHA256,
         "producer provenance")
    raw = CERTIFICATE.read_bytes()
    need(digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA, "certificate schema")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("total_edges") == 1380,
         "finite counts")
    need(audit.get("minimum_below_one_rows") == 18 and
         audit.get("all_positive_above_one_rows") == 18 and
         audit.get("maxcut_below_one_rows") == 18 and
         audit.get("weighted_optimum_differs_from_maxcut_rows") == 18,
         "finite inequalities")
    need(audit.get("weighted_optimum_le_one_quarter_rows") == 13 and
         audit.get("weighted_optimum_le_one_tenth_rows") == 8,
         "finite thresholds")
    firewall = payload.get("firewall", {})
    need(firewall.get("TPC294_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC294_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC294_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(LOG.is_file(), "LaTeX log")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("undefined", "LaTeX Warning:",
                "Package rerunfilecheck Warning:", "Overfull \\hbox",
                "Underfull \\hbox"):
        need(bad not in log, "LaTeX warning: " + bad)
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC294_MAXIMUM_CLAIM = " + STATUS,
        "TPC294_ROUTE_ADVANCE = YES_SCOPED_FINITE_SIGN_LAYER_TO_MAGNITUDE_WEIGHTED_RAYLEIGH_LAYER",
        "TPC294_TRACE_NORMALIZED_IDENTITY = PROVED_EXACT_FINITE",
        "TPC294_GLOBAL_SIGN_ENUMERATION = PROVED_EXACT_FINITE",
        "TPC294_GRAM_NONNEGATIVITY = PROVED_EXACT_FINITE",
        "TPC294_WEIGHTED_RAYLEIGH_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
        "TPC294_EQUAL_SIGNED_CONTRACTION = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_BELOW_ONE",
        "TPC294_ALL_POSITIVE_AMPLIFICATION = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_ONE",
        "TPC294_MAXCUT_CANDIDATE_CONTRACTION = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_BELOW_ONE",
        "TPC294_WEIGHTED_VS_MAXCUT = NUMERICALLY_CERTIFIED_FINITE_DIFFERENT_18_OF_18",
        "TPC294_SOURCE_NATIVE_COEFFICIENT_IMAGE = OPEN_LITERAL_SOURCE",
        "TPC294_GROWING_WEIGHTED_THEOREM = OPEN",
        "TPC294_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC294_FIXED_POWER_CREDIT = 0",
        "TPC294_FULL_GATE_B = OPEN",
        "TPC294_TWIN_PRIME_RESULT = NONE",
        "TPC294_ROUND2_CLUE = TEST_SOURCE_IMAGE_OF_WEIGHTED_OPTIMAL_SIGN_PATTERNS_AND_DIFFUSE_SIGNED_WEIGHTS",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge()
        for script in (PRODUCER, INDEPENDENT, STRESS):
            normal = run(script, False)
            optimized = run(script, True)
            need(normal == optimized, script.name + " optimized mismatch")
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError) as error:
        print("TPC294_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC294_BRIDGE_CHECK=PASS rows=18 edges=1380 min_below_one=18 "
          "plus_above_one=18 maxcut_below_one=18 differing=18")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
