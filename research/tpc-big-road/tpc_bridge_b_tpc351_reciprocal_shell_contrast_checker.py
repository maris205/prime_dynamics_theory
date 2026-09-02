#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-351."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-351-reciprocal-shell-contrast"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc351_reciprocal_shell_contrast.md")
PRODUCER = PROJECT / "code/tpc351_reciprocal_shell_contrast.py"
INDEPENDENT = PROJECT / "experiments/tpc351_independent_checker.py"
STRESS = PROJECT / "experiments/tpc351_contrast_stress.py"
CERTIFICATE = PROJECT / "results/tpc351_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PRODUCER_SHA256 = "820f6195408a4d0fbbfed46f5bdd8054d812ae24eb87aaa1169791055f33328a"
INDEPENDENT_SHA256 = "a3e9bfd6ed81b1e0ed08bc18c92df1195bb23cc60d308ae478aee59eedaef3a7"
STRESS_SHA256 = "0bcd681289c2b1c5c5e4a696d55917e68b6cc4288440ec6c8a29ddd511428dd0"
CERTIFICATE_SHA256 = "74ca0045ca201712a69870669612b7bc16ccd0c019f27f3ea1d3dccb4b687db0"
PDF_SHA256 = "c73a76d95ca8b4ff32625cbe5de95270c452540dd3541e3c94affa8abbe7a57c"
LOG_SHA256 = "15fa46d54ac2f941e7900a810383ed09671e161e345e1b9641e8c77ea75c6c71"
BRIDGE_SHA256 = "1489ee165a7d67815be23995e324310896619112ea9680a04037a8f41ee46c32"
STATUS = (
    "PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_SCALE_REPAIR_AUDIT")
SCHEMA = "TPC351_RECIPROCAL_SHELL_CONTRAST_V1"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def lock(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED", label + " hash placeholder")
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "certificate schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload digest")
    need(payload.get("parent_lock") == {
        "TPC350_producer_sha256":
        "7819fb38be3f6d33688ca3a4caa1920da2dd8624805356411d8099fc069e185d",
        "TPC350_certificate_sha256":
        "bc874009cfdd8fd7d6ea06d5d109a46d8bd9a732cd4933852f9176c5801bb086",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [60097, 72097, 84097] and
         protocol.get("source_counts") == [256, 512, 1024, 2048] and
         protocol.get("q_anchors") == [36, 80, 128, 256] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index"],
         "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 192 and audit.get("series") == 48 and
         audit.get("positive_reciprocal_witness_rows") == 192 and
         audit.get("zero_sum_records") == 192 and
         audit.get("incidence_gram_records") == 192 and
         audit.get("improved_parent_rows") == 180 and
         audit.get("parent_comparison_records") == 192 and
         audit.get("coordinate_beaten_rows") == 86 and
         audit.get("half_defect_rows") == 111 and
         audit.get("min_reciprocal_support") == 24 and
         audit.get("max_reciprocal_support") == 339 and
         audit.get("min_reciprocal_to_defect_ratio") == "0.0917557319271" and
         audit.get("max_reciprocal_to_defect_ratio") == "0.901734353382" and
         audit.get("nondecreasing_series") == 25 and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "audit")
    need(len(payload.get("rows", [])) == 192 and
         len(payload.get("growth_series", [])) == 48, "payload census")
    need(payload.get("exact_anchor", {}).get("interval") == [97, 110] and
         payload.get("exact_anchor", {}).get("coefficients") ==
         ["1/35", "-1/35"] and
         payload.get("exact_anchor", {}).get("incidence_vector_squared_norm") ==
         "3/1225" and
         payload.get("exact_anchor", {}).get("identity_exact") is True,
         "exact anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC351_UNIFORM_QUARTER_FLOOR") == "REFUTED_SCOPED" and
         firewall.get("TPC351_PARENT_IMPROVEMENT_CENSUS") ==
         "NUMERICALLY_CERTIFIED_FINITE_180_OF_192" and
         firewall.get("TPC351_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC351_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC351_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC351_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error", "Fatal error", "Citation"):
        need(bad not in log, "LaTeX diagnostic: " + bad)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100_000,
         "PDF identity")


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC351_MAXIMUM_CLAIM = " + STATUS,
        "TPC351_RECIPROCAL_ZERO_SUM_RULE = PROVED_EXACT_FINITE_DECLARED_RATIONAL_RULE",
        "TPC351_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA",
        "TPC351_SCALE_REPAIR_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS",
        "TPC351_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192",
        "TPC351_PARENT_IMPROVEMENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_180_OF_192",
        "TPC351_UNIFORM_QUARTER_FLOOR = REFUTED_SCOPED",
        "TPC351_ARITHMETIC_ADVANCE = NO",
        "TPC351_FIXED_POWER_CREDIT = 0",
        "TPC351_FULL_GATE_B = OPEN",
        "TPC351_TWIN_PRIME_RESULT = NONE",
        "TPC351_ROUND2_CLUE = ADVERSARIAL_HOLDOUT_FOR_RECIPROCAL_CONTRAST_BEFORE_BRANCH_FREEZE",
        "TPC351_STATUS = " + STATUS)
    for marker in markers:
        need(marker in text, "bridge marker missing")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script)])
    if script is PRODUCER or script is INDEPENDENT:
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["OMP_NUM_THREADS"] = "1"
    environment["OPENBLAS_NUM_THREADS"] = "1"
    environment["MKL_NUM_THREADS"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        lock(PRODUCER, PRODUCER_SHA256, "producer")
        lock(INDEPENDENT, INDEPENDENT_SHA256, "independent checker")
        lock(STRESS, STRESS_SHA256, "stress checker")
        lock(CERTIFICATE, CERTIFICATE_SHA256, "certificate")
        lock(MAIN_PDF, PDF_SHA256, "main PDF")
        lock(PDF, PDF_SHA256, "paper PDF")
        lock(LOG, LOG_SHA256, "compile log")
        lock(BRIDGE, BRIDGE_SHA256, "bridge")
        check_certificate()
        check_bridge_text()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        normal = tuple(run(script, False) for script in scripts)
        optimized = tuple(run(script, True) for script in scripts)
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC351_BRIDGE_CHECK=PASS rows=192 positive_witness=192 "
              "improved_parent=180/192 ratio_floor=0.0917557319271")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC351_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
