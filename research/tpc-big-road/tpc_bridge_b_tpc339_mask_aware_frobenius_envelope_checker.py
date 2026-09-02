#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-339."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-339-mask-aware-frobenius-envelope"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc339_mask_aware_frobenius_envelope.md"
PRODUCER = PROJECT / "code/tpc339_mask_aware_frobenius_envelope.py"
INDEPENDENT = PROJECT / "experiments/tpc339_independent_checker.py"
STRESS = PROJECT / "experiments/tpc339_envelope_stress.py"
CERTIFICATE = PROJECT / "results/tpc339_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / "papers/tpc-338-growing-control-covariance-spectrum/code/"
PARENT_CODE = PARENT_CODE / "tpc338_growing_control_covariance_spectrum.py"
PARENT_CERT = ROOT / "papers/tpc-338-growing-control-covariance-spectrum/results/"
PARENT_CERT = PARENT_CERT / "tpc338_certificate.json"
PARENT_CODE_SHA256 = "cb169ac486b4fc858a17f7e98533b387272671d9c8f24589b13c54dfd90b34e4"
PARENT_CERT_SHA256 = "79b7a830f7277e186d73c2e2186412ca26861f47fc332ad9306ae22ec45c4a7d"
SCHEMA = "TPC339_MASK_AWARE_FROBENIUS_ENVELOPE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_MASK_AWARE_FROBENIUS_ENVELOPE"
PRODUCER_SHA256 = "df76022bfa5051477ec5bc04fef444aefc22abcb8f76fa02b339b7bc769fad18"
INDEPENDENT_SHA256 = "0fa57252c5f10ef4d79e65890a5e149e16eb65d56d73f95ff027ecca53eae727"
STRESS_SHA256 = "3510f0362c75b760a6f58d45f0d57cb62f012a3cfa15c0c3fb2ddaacabd09257"
CERTIFICATE_SHA256 = "af6636eb7c9d9c6cbc0d392ae0b9effbaa9610dedafa12ee8d1272163fd48372"
BRIDGE_SHA256 = "fcca88d7806408391938769adf1ae34ec08a8ba49b4c6712f286a08a792ac7ec"


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
        "PROOF_PACKAGE.md", "code/tpc339_mask_aware_frobenius_envelope.py",
        "experiments/tpc339_independent_checker.py",
        "experiments/tpc339_envelope_stress.py",
        "results/tpc339_certificate.json", "notes/theorem_ledger.md",
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
             canonical(payload)).hexdigest(), "payload")
    need(payload.get("finite_audit") == {
        "rows": 6, "origins": 2, "scales": 3, "controls": 9,
        "categories": 4, "records": 216, "nonempty_records": 198,
        "bound_checks": 216, "bound_violations": 0,
        "broad_mask_records": 162, "fixed_power_credit": 0,
        "arithmetic_advance": "NO"}, "audit")
    summary = payload.get("summary", {})
    need(summary.get("bound_violations") == 0 and
         summary.get("nonempty_records") == 198 and
         float(summary.get("broad_mask_occupancy_max", 1)) < 0.2,
         "summary")
    need(payload.get("exact_anchor", {}).get("equality_exact") is True,
         "anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC339_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC339_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC339_FULL_GATE_B") == "OPEN", "firewall")
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
        "TPC339_SUPPORT_FROBENIUS_BOUND = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC339_MASKED_CONTROL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_RECORDS",
        "TPC339_BOUND_CENSUS = NUMERICALLY CERTIFIED FINITE_0_VIOLATIONS",
        "TPC339_BROAD_MASK_SLACK = NUMERICALLY CERTIFIED FINITE OCCUPANCY_BELOW_0.2",
        "TPC339_SIGN_FREE_REPLACEMENT = PROVED_FINITE_ONLY",
        "TPC339_SIMPLE_ENVELOPE_TIGHTNESS = REFUTED_SCOPED",
        "TPC339_ARITHMETIC_ADVANCE = NO", "TPC339_FIXED_POWER_CREDIT = 0",
        "TPC339_SOURCE_UNIFORM_L2 = OPEN", "TPC339_FULL_GATE_B = OPEN",
        "TPC339_TWIN_PRIME_RESULT = NONE", "TPC339_STATUS = " + STATUS,
        "TPC339_ROUND2_CLUE = TEST_A_SHARPER_MASKED_GRAM_OR_NUISANCE_ORTHOGONALIZATION")
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
        print("TPC339_BRIDGE_CHECK=PASS rows=6 controls=9 records=216 "
              "bound_violations=0 broad_mask_slack=1 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC339_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
