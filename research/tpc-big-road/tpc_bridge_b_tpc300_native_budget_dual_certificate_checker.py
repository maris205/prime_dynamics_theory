#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-300."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-300-native-budget-dual-certificate"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc300_native_budget_dual_certificate.md"
PRODUCER = PROJECT / "code/tpc300_native_budget_dual_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc300_independent_checker.py"
STRESS = PROJECT / "experiments/tpc300_dual_stress.py"
CERTIFICATE = PROJECT / "results/tpc300_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FINITE_NATIVE_BUDGET_DUALITY_AND_RECIPROCAL_"
    "MULTIPLIER_CORRECTION_PLUS_NUMERICALLY_CERTIFIED_FINITE_"
    "RATIONAL_DUAL_WITNESS_ATLAS")
SCHEMA = "TPC300_NATIVE_BUDGET_DUAL_CERTIFICATE_V1"
PRODUCER_SHA256 = "eb45a6c301b55ffb9816e84b55d73f46a52846b394f5677e80cabfb38f510e1e"
CERTIFICATE_SHA256 = "c07a45ecce710e98281556018f9976e7ba36b28efdb2582bdc3b72c5857acc71"
BRIDGE_SHA256 = "c928e0d2330a07d4da38d562bee62d6930020d6a6c8ba36b9e511a60e140df4c"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc300_native_budget_dual_certificate.py",
    "experiments/tpc300_independent_checker.py",
    "experiments/tpc300_dual_stress.py", "results/tpc300_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex",
    "paper/references.bib", "paper/paper.pdf")


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


def run_script(script: Path, optimized: bool, producer: bool = False) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script)]
    if producer:
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def run_binary(command: list[str]) -> None:
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "binary audit failed: " + command[0])


def check_files() -> None:
    for relative in REQUIRED:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
    need(digest(PRODUCER.read_bytes()) == PRODUCER_SHA256,
         "producer provenance")
    raw = CERTIFICATE.read_bytes()
    need(digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    need(digest(BRIDGE.read_bytes()) == BRIDGE_SHA256,
         "bridge provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA, "certificate schema")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    correction = payload.get("parameter_correction", {})
    need(correction.get("parent_field") == "lagrange_multiplier" and
         correction.get("correct_interpretation") == "ridge_parameter_rho" and
         correction.get("kkt_multiplier") == "mu=1/rho" and
         correction.get("parent_budget_values_affected") is False,
         "parameter correction")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("shell_edges") == 1380 and
         audit.get("dual_witness_cases") == 72 and
         audit.get("exact_rational_dual_cases") == 72,
         "finite census")
    need(audit.get("dual_tightness_floor_cases") == 72 and
         audit.get("weighted_threshold_dual_above_9e-5_rows") == 18 and
         audit.get("weighted_threshold_dual_above_5e-4_rows") == 15 and
         audit.get("weighted_threshold_dual_above_1e-3_rows") == 14 and
         audit.get("weighted_full_prefix_dual_above_1e-3_rows") == 11 and
         audit.get("fixed_power_credit") == 0, "dual census")
    rows = payload.get("rows", [])
    need(len(rows) == 18 and
         all(len(row.get("dual_cases", [])) == 4 for row in rows),
         "row payload")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("LaTeX Warning:", "Package rerunfilecheck Warning:",
                "Overfull \\hbox", "Underfull \\hbox", "undefined"):
        need(bad not in log, "LaTeX warning: " + bad)
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    run_binary(["pdfinfo", str(PDF)])
    run_binary(["pdffonts", str(PDF)])
    run_binary(["gs", "-q", "-dNOPAUSE", "-dBATCH",
                "-sDEVICE=nullpage", str(PDF)])


def check_bridge_markers() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC300_MAXIMUM_CLAIM = " + STATUS,
        "TPC300_ROUTE_ADVANCE = YES_SCOPED_PRIMAL_FRONTIER_TO_RATIONAL_DUAL_CERTIFICATE",
        "TPC300_DUAL_LOWER_BOUND = PROVED_EXACT_FINITE",
        "TPC300_STRONG_DUALITY_ACTIVE_FRONTIER = PROVED_EXACT_FINITE_SLATER",
        "TPC300_RIDGE_KKT_RECIPROCITY = PROVED_EXACT_FINITE",
        "TPC300_TPC299_PARAMETER_LABEL = CORRECTED_SCOPED_RIDGE_PARAMETER_NOT_KKT_MULTIPLIER",
        "TPC300_RATIONAL_DUAL_WITNESSES = NUMERICALLY_CERTIFIED_FINITE_72_OF_72",
        "TPC300_DUAL_TIGHTNESS = NUMERICALLY_CERTIFIED_FINITE_72_OF_72_ABOVE_0_999999999",
        "TPC300_WEIGHTED_THRESHOLD_DUAL_FLOOR = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_9E_MINUS_5",
        "TPC300_WEIGHTED_THRESHOLD_DUAL_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_14_OF_18_ABOVE_1E_MINUS_3",
        "TPC300_WEIGHTED_FULL_PREFIX_DUAL_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_11_OF_18_ABOVE_1E_MINUS_3",
        "TPC300_PROFILE_BUDGET_GROWTH = OPEN",
        "TPC300_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC300_FIXED_POWER_CREDIT = 0",
        "TPC300_FULL_GATE_B = OPEN",
        "TPC300_TWIN_PRIME_RESULT = NONE",
        "TPC300_ROUND2_CLUE = HOSTILE_TEST_THE_DUAL_BUDGET_GAP_ACROSS_TOLERANCE_AND_SOURCE_NORMALIZATION_LADDERS",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge_markers()
        outputs = {}
        for script, producer in ((PRODUCER, True),
                                 (INDEPENDENT, False),
                                 (STRESS, False)):
            outputs[script.name] = (
                run_script(script, False, producer),
                run_script(script, True, producer))
            need(outputs[script.name][0] == outputs[script.name][1],
                 script.name + " optimized mismatch")
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError) as error:
        print("TPC300_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC300_BRIDGE_CHECK=PASS rows=18 cases=72 tight_cases=72 "
          "weighted_gt_9e-5=18 weighted_gt_1e-3=14 full_gt_1e-3=11")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
