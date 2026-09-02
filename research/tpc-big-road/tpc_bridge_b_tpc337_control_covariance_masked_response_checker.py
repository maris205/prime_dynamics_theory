#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-337."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-337-control-covariance-masked-response"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc337_control_covariance_masked_response.md"
PRODUCER = PROJECT / "code/tpc337_control_covariance_masked_response.py"
INDEPENDENT = PROJECT / "experiments/tpc337_independent_checker.py"
STRESS = PROJECT / "experiments/tpc337_covariance_stress.py"
CERTIFICATE = PROJECT / "results/tpc337_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / "papers/tpc-336-masked-signed-gram-response/code/"
PARENT_CODE = PARENT_CODE / "tpc336_masked_signed_gram_response.py"
PARENT_CERT = ROOT / "papers/tpc-336-masked-signed-gram-response/results/"
PARENT_CERT = PARENT_CERT / "tpc336_certificate.json"
PARENT_CODE_SHA256 = "0c2febd76d6bfdc5af4b58145739bcc04b435303f15c66b31e2d0b2e63497442"
PARENT_CERT_SHA256 = "926859be38cc601ef728363328899d4e9ab2001f77e7e1106ab028d64cf2814a"
SCHEMA = "TPC337_CONTROL_COVARIANCE_MASKED_RESPONSE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CONTROL_COVARIANCE_MASKED_RESPONSE"
PRODUCER_SHA256 = "e74d621fa48fe7c15ff4e520dc2a051e5b195a5045c706592f275a6ead6b384d"
INDEPENDENT_SHA256 = "3322350c00fa5a79a2c5a9a6147993dc15636424a48b32c99120c440e3d4957b"
STRESS_SHA256 = "1bf3b2ad619157d902e96021e696f63f6621f3c765a152bc725f501068b9ca4a"
CERTIFICATE_SHA256 = "558f9a2dc60cd6616230785b46934a415459211a2e1bc31083447c53dd40e1d2"
BRIDGE_SHA256 = "0d974ae981a439e51a3f05fbc8e4e5aa15c3419fe00b408d2fa63640281a829f"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script), "--check"])
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["OMP_NUM_THREADS"] = "8"
    environment["OPENBLAS_NUM_THREADS"] = "8"
    environment["MKL_NUM_THREADS"] = "8"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    required = (
        ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
        "PROOF_PACKAGE.md", "code/tpc337_control_covariance_masked_response.py",
        "experiments/tpc337_independent_checker.py",
        "experiments/tpc337_covariance_stress.py",
        "results/tpc337_certificate.json", "notes/theorem_ledger.md",
        "notes/claim_firewall.md", "notes/computational_protocol.md",
        "notes/route_evaluation.md", "notes/citation_verification.md",
        "paper/main.tex", "paper/main.pdf", "paper/paper.pdf",
        "paper/compile.log")
    for item in required:
        need((PROJECT / item).is_file(), "missing artifact: " + item)
    for path, expected, label in (
            (PRODUCER, PRODUCER_SHA256, "producer"),
            (INDEPENDENT, INDEPENDENT_SHA256, "independent"),
            (STRESS, STRESS_SHA256, "stress"),
            (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
            (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(len(expected) == 64 and not expected.startswith("__"),
             label + " hash not sealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256 and
         digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "parent provenance")
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document) and document.get("certificate_version") == 1
         and document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    need(payload.get("finite_audit") == {
        "rows": 6, "origins": 2, "scales": 3, "controls": 5,
        "categories": 4, "class_decomposition_observations": 24,
        "pair_covariance_observations": 36,
        "full_decomposition_observations": 6,
        "covariance_spectrum_observations": 6,
        "fixed_power_credit": 0, "arithmetic_advance": "NO"}, "audit")
    need(len(payload.get("rows", [])) == 6 and
         payload.get("summary", {}).get(
             "twin_background_covariance_positive_rows") == 6,
         "row summary")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC337_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC337_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC337_SOURCE_UNIFORM_L2") == "OPEN" and
         firewall.get("TPC337_FULL_GATE_B") == "OPEN", "firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100_000,
         "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox", "Underfull \\hbox",
                "LaTeX Error", "Fatal error"):
        need(bad not in log, "LaTeX diagnostic: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC337_MEAN_CENTERED_OUTPUT_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC337_COVARIANCE_GRAM_PSD = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC337_MASKED_CONTROL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_ROWS_5_CONTROLS",
        "TPC337_FULL_CENTERED_COVARIANCE_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_6_OF_6",
        "TPC337_TWIN_BACKGROUND_COVARIANCE_SIGN = NUMERICALLY_CERTIFIED_FINITE_POSITIVE_6_OF_6",
        "TPC337_ZERO_BACKGROUND_COVARIANCE_SIGN = NUMERICALLY_CERTIFIED_FINITE_NEGATIVE_6_OF_6",
        "TPC337_SOURCE_SHARE_TRANSFER = REFUTED_SCOPED",
        "TPC337_ARITHMETIC_ADVANCE = NO", "TPC337_FIXED_POWER_CREDIT = 0",
        "TPC337_SOURCE_UNIFORM_L2 = OPEN", "TPC337_FULL_GATE_B = OPEN",
        "TPC337_TWIN_PRIME_RESULT = NONE",
        "TPC337_STATUS = " + STATUS,
        "TPC337_ROUND2_CLUE = GROW_THE_CONTROL_ORBIT_AND_TEST_COVARIANCE_SPECTRUM_STABILITY")
    for marker in markers:
        need(marker in text, "bridge marker missing")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check_files()
        check_bridge_text()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        normal = tuple(run(script, False) for script in scripts)
        optimized = tuple(run(script, True) for script in scripts)
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC337_BRIDGE_CHECK=PASS rows=6 controls=5 categories=4 "
              "centered_dominance=6 covariance_psd=1 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC337_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
