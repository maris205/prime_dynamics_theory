#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-326."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-326-cross-origin-scale-replication"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc326_cross_origin_scale_replication.md"
PRODUCER = PROJECT / "code/tpc326_cross_origin_scale_replication.py"
INDEPENDENT = PROJECT / "experiments/tpc326_independent_checker.py"
STRESS = PROJECT / "experiments/tpc326_cross_origin_stress.py"
CERTIFICATE = PROJECT / "results/tpc326_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_PROJECT = ROOT / "papers/tpc-325-scale-ladder-profile"
PARENT_CERT = PARENT_PROJECT / "results/tpc325_certificate.json"
PARENT_PRODUCER = PARENT_PROJECT / "code/tpc325_scale_ladder_profile.py"

STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_ORIGIN_SCALE_LADDER_REPLICATION"
SCHEMA = "TPC326_CROSS_ORIGIN_SCALE_REPLICATION_V1"
PARENT_CERT_SHA256 = (
    "7afe4fcf56b4432dcf2e5320479cd144a53cdcea29ccbd5cb26c558fd9f06766")
PARENT_PRODUCER_SHA256 = (
    "3b1aabb54c7f7cd8c1a64164d24b8937e5d9ca4a41dd3735849a3fe37ec6d3f3")

# Sealed after the project and bridge artifacts are final.
PRODUCER_SHA256 = "2f9f5b813a070144affd20dc83d88f5a3cc3642b51e90a9fa3f48a69eb11d683"
INDEPENDENT_SHA256 = "78cb27824081a14524902b735d0b818884fed9a292bd3c4e576f4ec79219aebd"
STRESS_SHA256 = "119c0c5bf6da3311bf8cb0d2ddda852c1f2a34c5754494d218aaf54fd4e762b6"
CERTIFICATE_SHA256 = "9b52f8f74fe2edd5fa8c512fcb7a87c9bfef06cb4e888c93945419006bcff2ec"
BRIDGE_SHA256 = "5b2652afaba2119a5ab7fab7b4f4efadf87ebced6ce6cf937c7097b9cee8df44"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc326_cross_origin_scale_replication.py",
    "experiments/tpc326_independent_checker.py",
    "experiments/tpc326_cross_origin_stress.py",
    "results/tpc326_certificate.json", "notes/theorem_ledger.md",
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
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "parent certificate provenance")
    need(digest(PARENT_PRODUCER.read_bytes()) == PARENT_PRODUCER_SHA256,
         "parent producer provenance")

    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload", {})
    need(payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload hash")
    need(payload.get("parent_lock") == {
        "certificate_sha256": PARENT_CERT_SHA256,
        "producer_sha256": PARENT_PRODUCER_SHA256,
        "project": "TPC-325 source-scale ladder profile",
    }, "parent lock")

    protocol = payload.get("protocol", {})
    need(protocol.get("parent_origin") == 12001 and
         protocol.get("source_origin") == 16001 and
         protocol.get("source_scales") == [320, 640, 1280, 2560] and
         protocol.get("source_counts") == [160, 320, 640, 1280] and
         protocol.get("height") == 66 and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("paths") == ["scipy_forward", "numpy_forward",
                                    "numpy_reverse"], "protocol")

    audit = payload.get("finite_audit", {})
    expected_classes = {
        "all_plus": {"SIGNED_MAJORISES_DIRECT": 32,
                     "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 0,
                     "UNRESOLVED": 0},
        "alternating_index": {"SIGNED_MAJORISES_DIRECT": 21,
                              "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 11,
                              "UNRESOLVED": 0},
        "mod4_character": {"SIGNED_MAJORISES_DIRECT": 26,
                           "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 6,
                           "UNRESOLVED": 0},
        "half_split": {"SIGNED_MAJORISES_DIRECT": 23,
                       "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 9,
                       "UNRESOLVED": 0},
    }
    expected_energy = {
        "all_plus": {"below_one": 4, "above_one": 28},
        "alternating_index": {"below_one": 28, "above_one": 4},
        "mod4_character": {"below_one": 26, "above_one": 6},
        "half_split": {"below_one": 28, "above_one": 4},
    }
    need(audit.get("rows") == 32 and
         audit.get("profile_majorization_counts") == expected_classes and
         audit.get("energy_ratio_counts") == expected_energy and
         audit.get("all_plus_strict_majorization_rows") == 32 and
         audit.get("all_plus_tv_lower_envelope_strictly_descends") is True and
         audit.get("all_plus_energy_upper_envelope_strictly_descends") is True and
         audit.get("fixed_power_credit") == 0, "finite audit")

    ladder = payload.get("scale_ladder", [])
    need([item.get("scale") for item in ladder] == [320, 640, 1280, 2560],
         "ladder order")
    need(all(item.get("all_plus_majorization_rows") == 8 for item in ladder),
         "ladder majorization")
    need(all(float(item["all_plus_minimum_prefix_lower"]) > 0
             for item in ladder), "ladder prefix")
    need(all(float(a["all_plus_tv_lower_envelope"]) >
             float(b["all_plus_tv_lower_envelope"])
             for a, b in zip(ladder, ladder[1:])), "TV trend")
    need(all(float(a["all_plus_energy_ratio_max"]) >
             float(b["all_plus_energy_ratio_max"])
             for a, b in zip(ladder, ladder[1:])), "energy trend")

    cross = payload.get("cross_origin", {})
    need(cross.get("parent_origin") == 12001 and
         cross.get("new_origin") == 16001 and
         cross.get("profile_census_matches_parent") is True and
         cross.get("energy_census_matches_parent") is True and
         float(cross.get("max_tv_envelope_difference")) < 0.001 and
         float(cross.get("max_energy_upper_envelope_difference")) < 0.005 and
         cross.get("tv_agreement_threshold") == "0.001" and
         cross.get("energy_agreement_threshold") == "0.005", "cross-origin")

    anchor = payload.get("exact_small_audit", {})
    need(anchor.get("interval") == [16001, 16016] and
         anchor.get("Q") == 4 and anchor.get("shell") == [5, 7] and
         anchor.get("identity_exact") is True and
         anchor.get("direct_energy_digest") ==
         "e9855d70fb5f73e5c30c8ebe8de3673301a13a23fc6a85299dea816ff97fe2d0" and
         anchor.get("signed_energy_digest") ==
         "d97b7e1b65c517eb46f27efa9411dd1f574c61e703470480af2b68397afae136",
         "exact anchor")

    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC326_CROSS_ORIGIN_REPLICATION") ==
         "NUMERICALLY_CERTIFIED_FINITE_32_ROWS_2_ORIGINS" and
         firewall.get("TPC326_ALL_PLUS_REPLICATION") ==
         "NUMERICALLY_CERTIFIED_FINITE_32_OF_32" and
         firewall.get("TPC326_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC326_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC326_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC326_TWIN_PRIME_RESULT") == "NONE", "firewall")

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
        "TPC326_MAXIMUM_CLAIM = " + STATUS,
        "TPC326_CROSS_ORIGIN_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_ROWS_2_ORIGINS",
        "TPC326_ALL_PLUS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_OF_32",
        "TPC326_CENSUS_MATCH = NUMERICALLY_CERTIFIED_FINITE_PARENT_MATCH",
        "TPC326_ENVELOPE_AGREEMENT = NUMERICALLY_CERTIFIED_FINITE_WITHIN_DECLARED_THRESHOLDS",
        "TPC326_ARITHMETIC_ADVANCE = NO",
        "TPC326_FIXED_POWER_CREDIT = 0",
        "TPC326_FULL_GATE_B = OPEN",
        "TPC326_TWIN_PRIME_RESULT = NONE",
        "TPC326_STATUS = " + STATUS,
        "TPC326_ROUND2_CLUE = TEST_CROSS_ORIGIN_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2",
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
        print("TPC326_BRIDGE_CHECK=PASS rows=32 origins=2 "
              "all_plus=32/32 census=parent_match envelopes=within_thresholds")
    except (Failure, OSError, json.JSONDecodeError, ValueError) as error:
        print("TPC326_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
