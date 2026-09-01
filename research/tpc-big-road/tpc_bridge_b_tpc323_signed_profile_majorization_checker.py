#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-323."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-323-signed-profile-majorization"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc323_signed_profile_majorization.md"
PRODUCER = PROJECT / "code/tpc323_signed_profile_majorization.py"
INDEPENDENT = PROJECT / "experiments/tpc323_independent_checker.py"
STRESS = PROJECT / "experiments/tpc323_profile_stress.py"
CERTIFICATE = PROJECT / "results/tpc323_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CERT = ROOT / (
    "papers/tpc-322-signed-projector-reassembly/results/"
    "tpc322_certificate.json")

STATUS = "NUMERICALLY_CERTIFIED_FINITE_SIGNED_PROFILE_MAJORISATION_AUDIT"
SCHEMA = "TPC323_SIGNED_PROFILE_MAJORISATION_V1"
PARENT_SHA256 = (
    "4961b34ebb755e8216d4fbc6d9d6d59781c9a8203c8687b5990385c7e0a57b0c")

# Sealed after the source, certificate, bridge, and PDF are final.
PRODUCER_SHA256 = "275c147e63b2edd7df6eec51212780c57d8d589d6cf2cc288baa5b38cb470430"
INDEPENDENT_SHA256 = "89222b22c9e1b9e462d689a642ca85bbdbaef9404bde78477904a0daa513b02f"
STRESS_SHA256 = "0ae35717f34f073a05dda126d2e5a747e2ad229077fa155356aa8835178d493a"
CERTIFICATE_SHA256 = "5f7d3c35a83f0176fa5e3573377bc96514ffa105203129995a2bd16e73c31faa"
BRIDGE_SHA256 = "1f52060e395141d3c22d35d1d2e6408866117b5eccc9ffb0efba1bb723da8883"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc323_signed_profile_majorization.py",
    "experiments/tpc323_independent_checker.py",
    "experiments/tpc323_profile_stress.py", "results/tpc323_certificate.json",
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


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script), "--check"]
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
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
    need(digest(PARENT_CERT.read_bytes()) == PARENT_SHA256,
         "parent certificate provenance")

    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload", {})
    need(payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    need(payload.get("parent_lock", {}).get("certificate_sha256") ==
         PARENT_SHA256, "parent lock")

    protocol = payload.get("protocol", {})
    need(protocol.get("source_scales") == [640, 1280, 2560] and
         protocol.get("height") == 66 and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("profile") ==
         "pi_j(G)=lambda_j(G)/tr(G), descending" and
         protocol.get("paths") == ["scipy_forward", "numpy_forward",
                                    "numpy_reverse"], "protocol")

    audit = payload.get("finite_audit", {})
    expected = {
        "all_plus": {"SIGNED_MAJORISES_DIRECT": 24,
                     "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 0,
                     "UNRESOLVED": 0},
        "alternating_index": {"SIGNED_MAJORISES_DIRECT": 17,
                              "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 7,
                              "UNRESOLVED": 0},
        "mod4_character": {"SIGNED_MAJORISES_DIRECT": 21,
                            "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 3,
                            "UNRESOLVED": 0},
        "half_split": {"SIGNED_MAJORISES_DIRECT": 18,
                        "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 6,
                        "UNRESOLVED": 0},
    }
    need(audit.get("rows") == 24 and
         audit.get("profile_majorization_counts") == expected and
         audit.get("energy_ratio_counts", {}).get("all_plus") ==
         {"below_one": 3, "above_one": 21} and
         audit.get("all_plus_strict_majorization_rows") == 24 and
         float(audit.get("all_plus_minimum_prefix_lower")) > 0 and
         audit.get("fixed_power_credit") == 0, "finite audit")

    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC323_SIGNED_PROFILE_FACTORISATION") ==
         "PROVED_EXACT_FINITE" and
         firewall.get("TPC323_ALL_PLUS_PROFILE_MAJORISATION") ==
         "NUMERICALLY_CERTIFIED_FINITE_24_OF_24" and
         firewall.get("TPC323_NAMED_LAW_SELECTION") ==
         "NUMERICAL_OBSERVATION_ALL_PLUS_UNIQUE_ON_PANEL" and
         firewall.get("TPC323_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC323_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC323_TWIN_PRIME_RESULT") == "NONE", "firewall")

    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error"):
        need(bad not in log, "LaTeX warning: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC323_MAXIMUM_CLAIM = " + STATUS,
        "TPC323_ROUTE_ADVANCE = YES_SCOPED_FINITE_SIGNED_PROFILE_READOUT",
        "TPC323_SIGNED_PROFILE_FACTORISATION = PROVED_EXACT_FINITE",
        "TPC323_ALL_PLUS_PROFILE_MAJORISATION = NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
        "TPC323_ALTERNATIVE_PROFILE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_24_ROWS",
        "TPC323_NAMED_LAW_SELECTION = NUMERICAL_OBSERVATION_ALL_PLUS_UNIQUE_ON_PANEL",
        "TPC323_ARITHMETIC_ADVANCE = NO",
        "TPC323_FIXED_POWER_CREDIT = 0",
        "TPC323_FULL_GATE_B = OPEN",
        "TPC323_TWIN_PRIME_RESULT = NONE",
        "TPC323_STATUS = " + STATUS,
        "TPC323_ROUND2_CLUE = TEST_PROFILE_MAJORISATION_HOLDOUT_OR_SOURCE_NATIVE_ARITHMETIC_L2",
    )
    for marker in markers:
        need(marker in text, "bridge marker missing")


def main() -> int:
    try:
        check_files()
        check_bridge_text()
        normal = (run(PRODUCER, False), run(INDEPENDENT, False),
                  run(STRESS, False))
        optimized = (run(PRODUCER, True), run(INDEPENDENT, True),
                     run(STRESS, True))
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC323_BRIDGE_CHECK=PASS rows=24 all_plus_profile=24/24 "
              "alternating=17/7 mod4=21/3 half_split=18/6")
    except (Failure, OSError, json.JSONDecodeError, ValueError) as error:
        print("TPC323_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
