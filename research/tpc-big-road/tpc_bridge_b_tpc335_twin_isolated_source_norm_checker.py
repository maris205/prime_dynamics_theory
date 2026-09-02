#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-335."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-335-twin-isolated-source-norm"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc335_twin_isolated_source_norm.md"
PRODUCER = PROJECT / "code/tpc335_twin_isolated_source_norm.py"
INDEPENDENT = PROJECT / "experiments/tpc335_independent_checker.py"
STRESS = PROJECT / "experiments/tpc335_norm_stress.py"
CERTIFICATE = PROJECT / "results/tpc335_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / "papers/tpc-334-cross-term-support-ledger/code/tpc334_cross_term_support_ledger.py"
PARENT_CERT = ROOT / "papers/tpc-334-cross-term-support-ledger/results/tpc334_certificate.json"
PARENT_CODE_SHA256 = "a7e6d5f77b17449eea11d8b673e0d7bfa1701bc3f0f92601cc86d4891f3beef8"
PARENT_CERT_SHA256 = "9e9639965d70b0d66b2d63d2dbe30cad7007db00ec77d8fc54dce5baca03b7c6"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_TWIN_ISOLATED_SOURCE_NORM"
SCHEMA = "TPC335_TWIN_ISOLATED_SOURCE_NORM_V1"
PRODUCER_SHA256 = "e6d66a3963f974c9d3f03b20441b327a34dd9e684fabb72e0777d31082c4e608"
INDEPENDENT_SHA256 = "3adaf3350dc08da41f86b0b8325e255684e630c46c286e30928a2a57f4e8dab8"
STRESS_SHA256 = "32f426b2f65bb919d6ecfbcb59b3382b859ec29a89066f5bb59e2f11c6e9f752"
CERTIFICATE_SHA256 = "cee2aee00208cbfe8331abc80e066c7a736824414f4d8208a73e4c545bfa4934"
BRIDGE_SHA256 = "ce808a7dfe451244f91407b668476b2e0b3a6bd2f68ce991547fb2dcaf460883"


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
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script), "--check"]
    env = dict(os.environ); env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    required = (".gitignore", "README.md", "PAPER_PLAN.md",
        "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md",
        "code/tpc335_twin_isolated_source_norm.py",
        "experiments/tpc335_independent_checker.py",
        "experiments/tpc335_norm_stress.py",
        "results/tpc335_certificate.json", "notes/theorem_ledger.md",
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
         digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256, "parent lock")
    raw = CERTIFICATE.read_bytes(); document = json.loads(raw)
    need(raw == canonical(document) and document.get("certificate_version") == 1
         and document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "payload")
    need(payload.get("finite_audit") == {
        "windows": 6, "categories": 4, "norm_partition_observations": 6,
        "arithmetic_advance": "NO", "fixed_power_credit": 0}, "audit")
    need(len(payload.get("rows", [])) == 6 and
         payload.get("summary", {}).get(
             "twin_norm_fraction_between_0.09_0.13") == 6 and
         payload.get("summary", {}).get(
             "background_norm_fraction_between_0.65_0.72") == 6,
         "summary census")
    fw = payload.get("claim_firewall", {})
    need(fw.get("TPC335_ARITHMETIC_ADVANCE") == "NO" and
         fw.get("TPC335_SOURCE_UNIFORM_L2") == "OPEN" and
         fw.get("TPC335_FIXED_POWER_CREDIT") == 0, "firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100000,
         "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error", "Fatal error"):
        need(bad not in log, "LaTeX diagnostic: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
        "TPC335_MASK_NORM_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC335_SIX_WINDOW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_WINDOWS",
        "TPC335_TWIN_RESIDUAL_SHARE = NUMERICALLY_CERTIFIED_FINITE_9.6_TO_12.3_PERCENT",
        "TPC335_BACKGROUND_RESIDUAL_SHARE = NUMERICALLY_CERTIFIED_FINITE_67.1_TO_69.1_PERCENT",
        "TPC335_TWIN_AMPLIFICATION = NUMERICALLY_CERTIFIED_FINITE_1.70_TO_1.78",
        "TPC335_ARITHMETIC_ADVANCE = NO", "TPC335_FIXED_POWER_CREDIT = 0",
        "TPC335_SOURCE_UNIFORM_L2 = OPEN", "TPC335_FULL_GATE_B = OPEN",
        "TPC335_TWIN_PRIME_RESULT = NONE", "TPC335_STATUS = " + STATUS,
        "TPC335_ROUND2_CLUE = TEST_TWIN_ISOLATED_AND_BACKGROUND_SIGNED_GRAM_RESPONSES"):
        need(marker in text, "bridge marker missing")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check_files(); check_bridge_text()
        normal = tuple(run(s, False) for s in (PRODUCER, INDEPENDENT, STRESS))
        optimized = tuple(run(s, True) for s in (PRODUCER, INDEPENDENT, STRESS))
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC335_BRIDGE_CHECK=PASS windows=6 categories=4 "
              "twin_norm_9_to_13pct=6 background_norm_65_to_72pct=6 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC335_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
