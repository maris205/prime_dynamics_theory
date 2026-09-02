#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-347."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-347-convolution-mask-defect-interface"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc347_convolution_mask_defect_interface.md"
PRODUCER = PROJECT / "code/tpc347_convolution_mask_defect_interface.py"
INDEPENDENT = PROJECT / "experiments/tpc347_independent_checker.py"
STRESS = PROJECT / "experiments/tpc347_mask_defect_stress.py"
CERTIFICATE = PROJECT / "results/tpc347_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PRODUCER_SHA256 = "2b423b1863fa054b8987934824e0637e464ea5192ba560076abbcfc2394076fb"
INDEPENDENT_SHA256 = "5d4c64b040bb91947e38d5a2aac36f7221e34031d07eaad23b01036e93feaabc"
STRESS_SHA256 = "c1b453e10f1233e31df839be697c8f83e739111808e75312cea946ae30c93e30"
CERTIFICATE_SHA256 = "fa7b97ece4dbd165bcf1d81df6b7c021422d9b448a418d036daba8d1f7d828a9"
PDF_SHA256 = "acee998c8860fd0031b08a731c716157c042b68b172fffce14a6a97fd61261d9"
BRIDGE_SHA256 = "287f4e55b67082238faaf705a32af59ed77005bd9b4a7793f7e4170565a84b2d"
STATUS = (
    "PROVED_EXACT_FINITE_CONVOLUTION_MASK_DEFECT_INTERFACE_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_SPECTRAL_AUDIT")
SCHEMA = "TPC347_CONVOLUTION_MASK_DEFECT_INTERFACE_V1"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def lock(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED", label + " hash placeholder")
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script)])
    if script in (PRODUCER, INDEPENDENT):
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
    audit = payload.get("finite_audit", {})
    need(audit == {
        "arithmetic_advance": "NO",
        "combined_bound_records": 192,
        "combined_bound_violations": 0,
        "defect_ratio_gt_quarter": 93,
        "fixed_power_credit": 0,
        "kernel_exponents": 2,
        "laws": 4,
        "origins": 2,
        "q_anchors": 4,
        "rows": 192,
        "source_counts": 3,
        "translation_invariance_records": 96,
    }, "audit census")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [40097, 48097] and
         protocol.get("source_counts") == [256, 512, 1024] and
         protocol.get("q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("height") == 66 and
         protocol.get("young_radius") == 65536, "protocol")
    rows = payload.get("rows", [])
    need(len(rows) == 192 and all(item.get("finite_bound_holds") is True
                                  for item in rows), "rows")
    invariance = payload.get("translation_invariance_audit", [])
    need(len(invariance) == 96 and
         all(item.get("invariant") is True for item in invariance),
         "invariance")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC347_SOURCE_UNIFORM_ARITHMETIC_L2") == "OPEN" and
         firewall.get("TPC347_UNIFORM_MASKED_OPERATOR_BOUND") == "OPEN" and
         firewall.get("TPC347_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC347_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC347_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100_000,
         "PDF identity")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error", "Fatal error", "Citation"):
        need(bad not in log, "LaTeX diagnostic: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC347_MAXIMUM_CLAIM = " + STATUS,
        "TPC347_MASK_FACTORISATION = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC347_UNMASKED_FOURIER_INTERFACE = PROVED_EXACT_CONDITIONAL",
        "TPC347_TRANSLATION_INVARIANCE = NUMERICALLY_CERTIFIED_FINITE_96_OF_96",
        "TPC347_MASK_DEFECT_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS",
        "TPC347_DEFECT_DISCARDABILITY = REFUTED_SCOPED",
        "TPC347_ARITHMETIC_ADVANCE = NO",
        "TPC347_FIXED_POWER_CREDIT = 0",
        "TPC347_FULL_GATE_B = OPEN",
        "TPC347_TWIN_PRIME_RESULT = NONE",
        "TPC347_ROUND2_CLUE = QUANTIFY_MASK_DEFECT_LOWER_WITNESSES_BEFORE_SOURCE_NATIVE_L2",
        "TPC347_STATUS = " + STATUS)
    for marker in markers:
        need(marker in text, "bridge marker missing")


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
        lock(BRIDGE, BRIDGE_SHA256, "bridge")
        check_certificate()
        check_bridge_text()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        normal = tuple(run(script, False) for script in scripts)
        optimized = tuple(run(script, True) for script in scripts)
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC347_BRIDGE_CHECK=PASS rows=192 invariance=96 "
              "bound_violations=0 defect_ratio_gt_quarter=93")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC347_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
