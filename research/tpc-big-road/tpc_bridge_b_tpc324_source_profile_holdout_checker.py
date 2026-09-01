#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-324."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-324-source-profile-holdout"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc324_source_profile_holdout.md"
PRODUCER = PROJECT / "code/tpc324_source_profile_holdout.py"
INDEPENDENT = PROJECT / "experiments/tpc324_independent_checker.py"
STRESS = PROJECT / "experiments/tpc324_holdout_stress.py"
CERTIFICATE = PROJECT / "results/tpc324_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CERT = ROOT / (
    "papers/tpc-323-signed-profile-majorization/results/"
    "tpc323_certificate.json")

STATUS = "NUMERICALLY_CERTIFIED_FINITE_SOURCE_LOCATION_HOLDOUT_REPLICATION"
SCHEMA = "TPC324_SOURCE_PROFILE_HOLDOUT_V1"
PARENT_SHA256 = (
    "5f7d3c35a83f0176fa5e3573377bc96514ffa105203129995a2bd16e73c31faa")

# These are filled after all project artifacts are final.
PRODUCER_SHA256 = "bd487c60aedab124603be6308f80f852bc53e7c24ac44d3e78a497e182332faa"
INDEPENDENT_SHA256 = "b67d212f7e30457780a6a0a8cae502e8af691ca52b6b84e3e93b543e4f18262a"
STRESS_SHA256 = "26f5a96152359b8ac5fd7bc7fc53216d4d0683f1ced48f99b41198dbc269c775"
CERTIFICATE_SHA256 = "b92b119118bd0888463aa609de7d9c0cd5289dd1dedf267b9ab215034bf22e3c"
BRIDGE_SHA256 = "66d0f60d8e7026dd84272e329537bd7c733fb155e248109e8d8c022d999fc382"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc324_source_profile_holdout.py",
    "experiments/tpc324_independent_checker.py",
    "experiments/tpc324_holdout_stress.py",
    "results/tpc324_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/main.pdf",
    "paper/paper.pdf", "paper/compile.log",
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
    expected_panels = {
        "continuation": {"640": [2561, 2880], "1280": [2881, 3520],
                          "2560": [3521, 4800]},
        "gap_offset": {"640": [5001, 5320], "1280": [6001, 6640],
                        "2560": [8001, 9280]},
    }
    need(protocol.get("source_panels") == expected_panels and
         protocol.get("source_scales") == [640, 1280, 2560] and
         protocol.get("height") == 66 and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("profile") ==
         "pi_j(G)=lambda_j(G)/tr(G), descending" and
         protocol.get("paths") == ["scipy_forward", "numpy_forward",
                                    "numpy_reverse"], "protocol")

    audit = payload.get("finite_audit", {})
    expected_classes = {
        "all_plus": {"SIGNED_MAJORISES_DIRECT": 48,
                     "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 0,
                     "UNRESOLVED": 0},
        "alternating_index": {"SIGNED_MAJORISES_DIRECT": 34,
                              "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 14,
                              "UNRESOLVED": 0},
        "mod4_character": {"SIGNED_MAJORISES_DIRECT": 42,
                            "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 6,
                            "UNRESOLVED": 0},
        "half_split": {"SIGNED_MAJORISES_DIRECT": 36,
                        "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 12,
                        "UNRESOLVED": 0},
    }
    one = {
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
    need(audit.get("rows") == 48 and
         audit.get("panel_rows") == {"continuation": 24, "gap_offset": 24} and
         audit.get("profile_majorization_counts") == expected_classes and
         audit.get("per_panel_profile_majorization_counts") ==
         {"continuation": one, "gap_offset": one} and
         audit.get("all_plus_strict_majorization_rows") == 48 and
         float(audit.get("all_plus_minimum_prefix_lower")) > 0 and
         audit.get("replication_match_to_tpc323") is True and
         audit.get("fixed_power_credit") == 0, "finite audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC324_SOURCE_LOCATION_HOLDOUT") ==
         "NUMERICALLY_CERTIFIED_FINITE_48_ROWS_2_PANELS" and
         firewall.get("TPC324_ALL_PLUS_PROFILE_REPLICATION") ==
         "NUMERICALLY_CERTIFIED_FINITE_48_OF_48" and
         firewall.get("TPC324_PER_PANEL_REPLICATION") ==
         "NUMERICALLY_CERTIFIED_FINITE_24_OF_24_EACH" and
         firewall.get("TPC324_TRANSLATION_COVARIANCE") ==
         "PROVED_EXACT_FINITE_CONDITIONAL" and
         firewall.get("TPC324_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC324_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC324_TWIN_PRIME_RESULT") == "NONE", "firewall")

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
        "TPC324_MAXIMUM_CLAIM = " + STATUS,
        "TPC324_ROUTE_ADVANCE = YES_SCOPED_SOURCE_LOCATION_HOLDOUT_REPLICATION",
        "TPC324_SOURCE_LOCATION_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_48_ROWS_2_PANELS",
        "TPC324_ALL_PLUS_PROFILE_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_48_OF_48",
        "TPC324_PER_PANEL_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_24_OF_24_EACH",
        "TPC324_TRANSLATION_COVARIANCE = PROVED_EXACT_FINITE_CONDITIONAL",
        "TPC324_ARITHMETIC_ADVANCE = NO",
        "TPC324_FIXED_POWER_CREDIT = 0",
        "TPC324_FULL_GATE_B = OPEN",
        "TPC324_TWIN_PRIME_RESULT = NONE",
        "TPC324_STATUS = " + STATUS,
        "TPC324_ROUND2_CLUE = TEST_HOLDOUT_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2",
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
        print("TPC324_BRIDGE_CHECK=PASS rows=48 panels=2 "
              "all_plus_profile=48/48 per_panel=24/24 "
              "alternative=34/14,42/6,36/12")
    except (Failure, OSError, json.JSONDecodeError, ValueError) as error:
        print("TPC324_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
