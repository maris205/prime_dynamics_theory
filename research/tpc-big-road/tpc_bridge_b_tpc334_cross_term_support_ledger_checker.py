#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-334."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-334-cross-term-support-ledger"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc334_cross_term_support_ledger.md"
PRODUCER = PROJECT / "code/tpc334_cross_term_support_ledger.py"
INDEPENDENT = PROJECT / "experiments/tpc334_independent_checker.py"
STRESS = PROJECT / "experiments/tpc334_support_stress.py"
CERTIFICATE = PROJECT / "results/tpc334_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / "papers/tpc-333-source-polarization-cross-term/code/tpc333_source_polarization_cross_term.py"
PARENT_CERT = ROOT / "papers/tpc-333-source-polarization-cross-term/results/tpc333_certificate.json"
PARENT_CODE_SHA256 = "1e8b104db281b6998875f2fb5b4691910c3a22ef365c796bdc879f396f8a6bde"
PARENT_CERT_SHA256 = "3722702ab29b397c836b5ceb4cddd0b063d35e10139952dd93eb849ced2f53eb"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_TERM_SUPPORT_LEDGER"
SCHEMA = "TPC334_CROSS_TERM_SUPPORT_LEDGER_V1"
PRODUCER_SHA256 = "a7e6d5f77b17449eea11d8b673e0d7bfa1701bc3f0f92601cc86d4891f3beef8"
INDEPENDENT_SHA256 = "f7f1dfc7e8626c4f6792140578edf015a4e94dce003343c03efbd0f0ffb6487c"
STRESS_SHA256 = "30942f207932555186e7db9d6b0fb759dede37c687a0211aa99f1b7004bf8211"
CERTIFICATE_SHA256 = "9e9639965d70b0d66b2d63d2dbe30cad7007db00ec77d8fc54dce5baca03b7c6"
BRIDGE_SHA256 = "5ed15a5c1e8cc1b1f2f5447daa3c7673474bf524ae9476dd56d04433da43385c"


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
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    required = (".gitignore", "README.md", "PAPER_PLAN.md",
        "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md",
        "code/tpc334_cross_term_support_ledger.py",
        "experiments/tpc334_independent_checker.py",
        "experiments/tpc334_support_stress.py",
        "results/tpc334_certificate.json", "notes/theorem_ledger.md",
        "notes/claim_firewall.md", "notes/computational_protocol.md",
        "notes/route_evaluation.md", "notes/citation_verification.md",
        "paper/main.tex", "paper/main.pdf", "paper/paper.pdf",
        "paper/compile.log")
    for relative in required:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
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
    document = json.loads(CERTIFICATE.read_bytes())
    raw = CERTIFICATE.read_bytes()
    need(raw == canonical(document) and document.get("certificate_version") == 1
         and document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    need(payload.get("finite_audit") == {
        "windows": 6, "categories": 4, "partition_observations": 6,
        "arithmetic_advance": "NO", "fixed_power_credit": 0},
         "finite audit")
    need(len(payload.get("rows", [])) == 6 and
         payload.get("summary", {}).get("twin_fraction_below_0.10") == 6 and
         payload.get("summary", {}).get("non_twin_fraction_above_0.90") == 6,
         "support census")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC334_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC334_SOURCE_UNIFORM_L2") == "OPEN" and
         firewall.get("TPC334_FIXED_POWER_CREDIT") == 0,
         "claim firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100000,
         "PDF integrity")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error", "Fatal error"):
        need(bad not in log, "LaTeX diagnostic: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
        "TPC334_SUPPORT_PARTITION = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC334_SIX_WINDOW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_WINDOWS",
        "TPC334_TWIN_SUPPORT_SHARE = NUMERICALLY_CERTIFIED_FINITE_5.4_TO_7.2_PERCENT",
        "TPC334_NON_TWIN_BACKGROUND = NUMERICALLY_CERTIFIED_FINITE_92.8_TO_94.5_PERCENT",
        "TPC334_PRIME_POWER_SHARE = NUMERICALLY_CERTIFIED_FINITE_0_TO_0.286_PERCENT",
        "TPC334_ARITHMETIC_ADVANCE = NO", "TPC334_FIXED_POWER_CREDIT = 0",
        "TPC334_SOURCE_UNIFORM_L2 = OPEN", "TPC334_TWIN_PRIME_RESULT = NONE",
        "TPC334_FULL_GATE_B = OPEN", "TPC334_STATUS = " + STATUS,
        "TPC334_ROUND2_CLUE = ISOLATE_TWIN_MASK_OR_COMPENSATED_SOURCE_BEFORE_OPERATOR_REASSEMBLY"):
        need(marker in text, "bridge marker missing")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check_files(); check_bridge_text()
        normal = tuple(run(s, False) for s in (PRODUCER, INDEPENDENT, STRESS))
        optimized = tuple(run(s, True) for s in (PRODUCER, INDEPENDENT, STRESS))
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC334_BRIDGE_CHECK=PASS windows=6 categories=4 "
              "twin_below_10pct=6 non_twin_above_90pct=6 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC334_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
