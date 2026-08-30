#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-313."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-313-outward-budget-interval-certificate"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc313_outward_budget_interval_certificate.md")
PRODUCER = PROJECT / (
    "code/tpc313_outward_budget_interval_certificate.py")
INDEPENDENT = PROJECT / "experiments/tpc313_independent_checker.py"
STRESS = PROJECT / "experiments/tpc313_exact_stress.py"
CERTIFICATE = PROJECT / "results/tpc313_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/compile.log"

STATUS = (
    "PROVED_EXACT_FINITE_PROFILE_PREFIX_FEASIBILITY_AND_OUTWARD_"
    "INTERVAL_BUDGET_CERTIFICATES_PLUS_NUMERICALLY_CERTIFIED_NEW_PANEL_"
    "SEPARATION")
SCHEMA = "TPC313_OUTWARD_PROFILE_BUDGET_INTERVAL_CERTIFICATE_V1"

PRODUCER_SHA256 = (
    "d0560f6d1b5373eb9eb6aa16a19c94e7db6984f579a6f009c935c427f2fd35b0")
INDEPENDENT_SHA256 = (
    "d0bbd4d7e157b9150a26e6f315a1772a8f71ba0fb86bebf1a173c6856233a70b")
STRESS_SHA256 = (
    "b00e0244952f0451fd15c94dce42e1f2e66f3784b74d4405b643b9cec5d959ad")
CERTIFICATE_SHA256 = (
    "8f2d5190d923121b4ecd8ce5f8377fe6fb15d3817edf2b50eafdef7356f5c68b")
BRIDGE_SHA256 = (
    "875efeb0121b5bdd9e40954f984bba56500bfea2c02f90dcabaf9ed01b45254f")

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc313_outward_budget_interval_certificate.py",
    "experiments/tpc313_independent_checker.py",
    "experiments/tpc313_exact_stress.py", "results/tpc313_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex",
    "paper/references.bib", "paper/main.pdf", "paper/paper.pdf",
    "paper/compile.log",
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def run(script: Path, optimized: bool, producer: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script)]
    if producer:
        command.append("--check")
    else:
        if script == INDEPENDENT:
            command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["TPC313_WORKERS"] = "8"
    environment["TPC313_CHECK_WORKERS"] = "8"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    for relative in REQUIRED:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
    for path, expected, label in (
            (PRODUCER, PRODUCER_SHA256, "producer"),
            (INDEPENDENT, INDEPENDENT_SHA256, "independent checker"),
            (STRESS, STRESS_SHA256, "stress checker"),
            (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
            (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(not expected.startswith("__"), label + " hash not sealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")
    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA and
         data.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    protocol = payload.get("protocol", {})
    need(protocol.get("source_interval") == [321, 640] and
         protocol.get("source_scale") == 640 and
         protocol.get("height") == 66 and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("grid_digits") == 36, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 8 and audit.get("budget_cases") == 16 and
         audit.get("common_prefix_cases") == 8 and
         audit.get("outward_interval_cases") == 16 and
         audit.get("weighted_dual_above_5e-5") == 8 and
         audit.get("positive_primal_below_1e-5") == 8 and
         audit.get("fixed_power_credit") == 0, "finite audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC313_EXTERNAL_INDEPENDENCE") == "NONE" and
         firewall.get("TPC313_ARITHMETIC_L2") == "OPEN_LITERAL_SOURCE" and
         firewall.get("TPC313_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC313_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC313_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(),
         "main and published PDF differ")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error"):
        need(bad not in log, "LaTeX warning: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC313_MAXIMUM_CLAIM = " + STATUS,
        "TPC313_ROUTE_ADVANCE = YES_SCOPED_OUTWARD_PROFILE_BUDGET_CERTIFICATE",
        "TPC313_PROFILE_PREFIX_FEASIBILITY = PROVED_EXACT_FINITE_8_OF_8",
        "TPC313_RATIONAL_PRIMAL_WITNESSES = PROVED_EXACT_FINITE_16_OF_16",
        "TPC313_RATIONAL_DUAL_LOWER_BOUNDS = PROVED_EXACT_FINITE_16_OF_16",
        "TPC313_OUTWARD_GRID_ENCLOSURES = PROVED_EXACT_FINITE_16_OF_16_GRID_1E_MINUS_36",
        "TPC313_WEIGHTED_LOWER_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_8_OF_8_ABOVE_5E_MINUS_5",
        "TPC313_POSITIVE_UPPER_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_8_OF_8_BELOW_1E_MINUS_5",
        "TPC313_EXTERNAL_INDEPENDENCE = NONE_SAME_LOCKED_ENGINE",
        "TPC313_EXTERNAL_WEIGHTING = OPEN",
        "TPC313_FRESH_PHYSICAL_HOLDOUT = OPEN",
        "TPC313_UNIFORM_GROWING_BUDGET = OPEN",
        "TPC313_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC313_FIXED_POWER_CREDIT = 0",
        "TPC313_FULL_GATE_B = OPEN",
        "TPC313_TWIN_PRIME_RESULT = NONE",
        "TPC313_ROUND2_CLUE = AUDIT_EXTERNALLY_JUSTIFIED_WEIGHTING_ON_A_FRESH_PHYSICAL_HOLDOUT_AFTER_FORMAL_BUDGET_CERTIFICATION",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge_text()
        for script, producer in ((PRODUCER, True),
                                 (INDEPENDENT, False),
                                 (STRESS, False)):
            normal = run(script, False, producer)
            optimized = run(script, True, producer)
            need(normal == optimized, script.name + " optimized mismatch")
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError) as error:
        print("TPC313_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC313_BRIDGE_CHECK=PASS rows=8 cases=16 common_prefixes=8 "
          "outward_intervals=16 weighted_dual_gt_5e-5=8 "
          "positive_primal_lt_1e-5=8")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
