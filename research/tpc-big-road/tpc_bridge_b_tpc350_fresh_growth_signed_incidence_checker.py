#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-350."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-350-fresh-growth-signed-incidence"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc350_fresh_growth_signed_incidence.md")
PRODUCER = PROJECT / "code/tpc350_fresh_growth_signed_incidence.py"
INDEPENDENT = PROJECT / "experiments/tpc350_independent_checker.py"
STRESS = PROJECT / "experiments/tpc350_growth_stress.py"
CERTIFICATE = PROJECT / "results/tpc350_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PRODUCER_SHA256 = (
    "7819fb38be3f6d33688ca3a4caa1920da2dd8624805356411d8099fc069e185d")
INDEPENDENT_SHA256 = (
    "7a92f23098ddccf532f70390a5ff2f76462ea14fdfe6bb9686ca9c1c32688ce7")
STRESS_SHA256 = (
    "2f11a0f57cd3f5e33d083666c8541908170a8f7b9f9d52f32d820cae505ce016")
CERTIFICATE_SHA256 = (
    "bc874009cfdd8fd7d6ea06d5d109a46d8bd9a732cd4933852f9176c5801bb086")
PDF_SHA256 = (
    "d1084a59f23cc6430022a1662224bc637c23296baee638f3d12ba86736c35277")
LOG_SHA256 = (
    "e0e4ecbf6e4ef7441a4c2922c5a9fa09b98dffb3186642c5c0cec9941c089f2a")
BRIDGE_SHA256 = (
    "bb21c896c4a98efed2321c5537fee8f7bace0519f9fd506f5f94bfdf0dfaad62")
STATUS = (
    "PROVED_EXACT_FINITE_SIGNED_INCIDENCE_LOWER_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_FRESH_GROWTH_AND_SCALE_AUDIT")
SCHEMA = "TPC350_FRESH_GROWTH_SIGNED_INCIDENCE_V1"


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
        "TPC349_producer_sha256":
        "ed3b543a44a270301f3cc7543533c1ce35a6f9ea433e9581df19759b2bca3a03",
        "TPC349_certificate_sha256":
        "baceb7b6cbf32fbbf84289d302551ed7f42abb45c39333a7d235a229c9a7a741",
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
         audit.get("positive_signed_witness_rows") == 192 and
         audit.get("balanced_sum_records") == 192 and
         audit.get("incidence_gram_records") == 192 and
         audit.get("coordinate_beaten_rows") == 70 and
         audit.get("half_defect_rows") == 91 and
         audit.get("min_signed_support") == 24 and
         audit.get("max_signed_support") == 294 and
         audit.get("min_signed_to_defect_ratio") == "0.0657381187306" and
         audit.get("max_signed_to_defect_ratio") == "0.8797933448" and
         audit.get("nondecreasing_series") == 24 and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "audit")
    need(len(payload.get("rows", [])) == 192 and
         len(payload.get("growth_series", [])) == 48, "payload census")
    need(payload.get("exact_anchor", {}).get("interval") == [97, 110] and
         payload.get("exact_anchor", {}).get("identity_exact") is True,
         "exact anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC350_UNIFORM_QUARTER_FLOOR") == "REFUTED_SCOPED" and
         firewall.get("TPC350_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC350_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC350_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC350_TWIN_PRIME_RESULT") == "NONE",
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
        "TPC350_MAXIMUM_CLAIM = " + STATUS,
        "TPC350_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA",
        "TPC350_FRESH_GROWTH_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS",
        "TPC350_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192",
        "TPC350_SIGNED_TO_DEFECT_FLOOR = NUMERICALLY_CERTIFIED_FINITE_0.0657381187306",
        "TPC350_UNIFORM_QUARTER_FLOOR = REFUTED_SCOPED",
        "TPC350_ARITHMETIC_ADVANCE = NO",
        "TPC350_FIXED_POWER_CREDIT = 0",
        "TPC350_FULL_GATE_B = OPEN",
        "TPC350_TWIN_PRIME_RESULT = NONE",
        "TPC350_ROUND2_CLUE = TEST_SCALE_ADAPTIVE_ZERO_SUM_CONTRAST_ON_HIGH_SHELLS",
        "TPC350_STATUS = " + STATUS)
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
        print("TPC350_BRIDGE_CHECK=PASS rows=192 positive_witness=192 "
              "ratio_floor=0.0657381187306 nondecreasing_series=24/48")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC350_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
