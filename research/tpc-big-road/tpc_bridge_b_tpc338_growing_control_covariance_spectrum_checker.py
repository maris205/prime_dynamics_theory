#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-338."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-338-growing-control-covariance-spectrum"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc338_growing_control_covariance_spectrum.md"
PRODUCER = PROJECT / "code/tpc338_growing_control_covariance_spectrum.py"
INDEPENDENT = PROJECT / "experiments/tpc338_independent_checker.py"
STRESS = PROJECT / "experiments/tpc338_spectrum_stress.py"
CERTIFICATE = PROJECT / "results/tpc338_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / "papers/tpc-337-control-covariance-masked-response/code/"
PARENT_CODE = PARENT_CODE / "tpc337_control_covariance_masked_response.py"
PARENT_CERT = ROOT / "papers/tpc-337-control-covariance-masked-response/results/"
PARENT_CERT = PARENT_CERT / "tpc337_certificate.json"
PARENT_CODE_SHA256 = "e74d621fa48fe7c15ff4e520dc2a051e5b195a5045c706592f275a6ead6b384d"
PARENT_CERT_SHA256 = "558f9a2dc60cd6616230785b46934a415459211a2e1bc31083447c53dd40e1d2"
SCHEMA = "TPC338_GROWING_CONTROL_COVARIANCE_SPECTRUM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_COVARIANCE_SPECTRUM"
PRODUCER_SHA256 = "cb169ac486b4fc858a17f7e98533b387272671d9c8f24589b13c54dfd90b34e4"
INDEPENDENT_SHA256 = "2f3a3a0dcf60f3b2a914708952e3e5aad40763619d644de9346dc96f6e204f46"
STRESS_SHA256 = "41d12ad0c5c521e97c3277bb762aa659f5deba2fb8590e6576659d71d17cd674"
CERTIFICATE_SHA256 = "79b7a830f7277e186d73c2e2186412ca26861f47fc332ad9306ae22ec45c4a7d"
BRIDGE_SHA256 = "a91005245ba69ecd366465f922ae1dead3b9fbcf1503185b685d5115b9fb0649"


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
        "PROOF_PACKAGE.md", "code/tpc338_growing_control_covariance_spectrum.py",
        "experiments/tpc338_independent_checker.py",
        "experiments/tpc338_spectrum_stress.py",
        "results/tpc338_certificate.json", "notes/theorem_ledger.md",
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
    raw = CERTIFICATE.read_bytes(); document = json.loads(raw)
    need(raw == canonical(document) and document.get("certificate_version") == 1
         and document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    need(payload.get("finite_audit") == {
        "rows": 6, "origins": 2, "scales": 3, "five_controls": 5,
        "nine_controls": 9, "categories": 4, "nested_decompositions": 48,
        "normalized_spectrum_comparisons": 6, "pair_sign_ensembles": 2,
        "fixed_power_credit": 0, "arithmetic_advance": "NO"}, "audit")
    summary = payload.get("summary", {})
    need(summary.get("energy_dominance_rows") == 6 and
         summary.get("twin_zero_sign_reversal") is True and
         float(summary.get("nine_centered_fraction_min", 0)) > 0.85,
         "summary")
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
        "TPC338_NESTED_COVARIANCE_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC338_COVARIANCE_GRAM_PSD = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC338_ENERGY_DOMINANCE_STABILITY = NUMERICALLY_CERTIFIED_FINITE_6_OF_6",
        "TPC338_NORMALIZED_SPECTRUM_STABILITY = NUMERICALLY_CERTIFIED_FINITE_6_ROWS",
        "TPC338_TWIN_ZERO_SIGN_STABILITY = REFUTED_SCOPED",
        "TPC338_TWIN_ZERO_SIGN_REVERSAL = NUMERICALLY_CERTIFIED_FINITE_6_OF_6_NESTED_COMPARISON",
        "TPC338_TWIN_BACKGROUND_SIGN = NUMERICALLY_CERTIFIED_FINITE_POSITIVE_6_OF_6_BOTH_ENSEMBLES",
        "TPC338_BACKGROUND_ZERO_SIGN = NUMERICALLY_CERTIFIED_FINITE_NEGATIVE_6_OF_6_BOTH_ENSEMBLES",
        "TPC338_ARITHMETIC_ADVANCE = NO", "TPC338_FIXED_POWER_CREDIT = 0",
        "TPC338_SOURCE_UNIFORM_L2 = OPEN", "TPC338_FULL_GATE_B = OPEN",
        "TPC338_TWIN_PRIME_RESULT = NONE", "TPC338_STATUS = " + STATUS,
        "TPC338_ROUND2_CLUE = REPLACE_SIGN_HEURISTICS_BY_A_UNIFORM_MASKED_OPERATOR_ENVELOPE")
    for marker in markers:
        need(marker in text, "bridge marker missing")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check_files(); check_bridge_text()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        normal = tuple(run(script, False) for script in scripts)
        optimized = tuple(run(script, True) for script in scripts)
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC338_BRIDGE_CHECK=PASS rows=6 five_controls=5 nine_controls=9 "
              "energy_dominance=6 twin_zero_reversal=6 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC338_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
