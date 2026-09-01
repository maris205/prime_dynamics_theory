#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-325."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-325-scale-ladder-profile"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc325_scale_ladder_profile.md"
PRODUCER = PROJECT / "code/tpc325_scale_ladder_profile.py"
INDEPENDENT = PROJECT / "experiments/tpc325_independent_checker.py"
STRESS = PROJECT / "experiments/tpc325_scale_stress.py"
CERTIFICATE = PROJECT / "results/tpc325_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CERT = ROOT / "papers/tpc-324-source-profile-holdout/results/tpc324_certificate.json"
PARENT_ENGINE = ROOT / "papers/tpc-324-source-profile-holdout/code/tpc324_source_profile_holdout.py"

STATUS = "NUMERICALLY_CERTIFIED_FINITE_SOURCE_SCALE_LADDER_AUDIT"
SCHEMA = "TPC325_SCALE_LADDER_PROFILE_V1"
PARENT_CERT_SHA256 = "b92b119118bd0888463aa609de7d9c0cd5289dd1dedf267b9ab215034bf22e3c"
PARENT_ENGINE_SHA256 = "bd487c60aedab124603be6308f80f852bc53e7c24ac44d3e78a497e182332faa"

# Filled after all release artifacts are final.
PRODUCER_SHA256 = "3b1aabb54c7f7cd8c1a64164d24b8937e5d9ca4a41dd3735849a3fe37ec6d3f3"
INDEPENDENT_SHA256 = "201e7e7a9f3be9275aa17ecd670090c78db5f0f579aecd25f0687b9af8bcce67"
STRESS_SHA256 = "0f20742e27281f5352009aabee46ffaecf0b8df82e1d2f6efe9679ec0b72f657"
CERTIFICATE_SHA256 = "7afe4fcf56b4432dcf2e5320479cd144a53cdcea29ccbd5cb26c558fd9f06766"
BRIDGE_SHA256 = "1d6f8b74092f7354c6ca98aa2a3c5d88a4e62ad6c747141dc53cd0ad4db04bbc"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc325_scale_ladder_profile.py",
    "experiments/tpc325_independent_checker.py",
    "experiments/tpc325_scale_stress.py", "results/tpc325_certificate.json",
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
            (INDEPENDENT, INDEPENDENT_SHA256, "independent"),
            (STRESS, STRESS_SHA256, "stress"),
            (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
            (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(not expected.startswith("__"), label + " hash not sealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "parent certificate provenance")
    need(digest(PARENT_ENGINE.read_bytes()) == PARENT_ENGINE_SHA256,
         "parent engine provenance")

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
        "engine_sha256": PARENT_ENGINE_SHA256,
        "project": "TPC-324 source profile holdout",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("source_origin") == 12001 and
         protocol.get("source_scales") == [320, 640, 1280, 2560] and
         protocol.get("source_counts") == [160, 320, 640, 1280] and
         protocol.get("height") == 66 and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("paths") == ["scipy_forward", "numpy_forward",
                                    "numpy_reverse"], "protocol")
    audit = payload.get("finite_audit", {})
    expected = {
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
    need(audit.get("rows") == 32 and
         audit.get("profile_majorization_counts") == expected and
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
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC325_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC325_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC325_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error"):
        need(bad not in log, "LaTeX warning: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
        "TPC325_MAXIMUM_CLAIM = " + STATUS,
        "TPC325_SCALE_LADDER = NUMERICALLY_CERTIFIED_FINITE_32_ROWS_4_SCALES",
        "TPC325_ALL_PLUS_SCALE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_32_OF_32",
        "TPC325_ALL_PLUS_PROFILE_MAJORISATION = NUMERICALLY_CERTIFIED_FINITE_32_OF_32",
        "TPC325_TV_ENVELOPE = NUMERICAL_OBSERVATION_STRICTLY_DESCENDING_4_SCALES",
        "TPC325_ENERGY_ENVELOPE = NUMERICAL_OBSERVATION_STRICTLY_DESCENDING_4_SCALES",
        "TPC325_ARITHMETIC_ADVANCE = NO",
        "TPC325_FIXED_POWER_CREDIT = 0",
        "TPC325_FULL_GATE_B = OPEN",
        "TPC325_TWIN_PRIME_RESULT = NONE",
        "TPC325_STATUS = " + STATUS,
        "TPC325_ROUND2_CLUE = TEST_SCALE_LADDER_SOURCE_REPLICATION_OR_SOURCE_NATIVE_ARITHMETIC_L2",
    ):
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
        print("TPC325_BRIDGE_CHECK=PASS rows=32 scales=4 "
              "all_plus=32/32 tv_envelope=descending energy_envelope=descending")
    except (Failure, OSError, json.JSONDecodeError, ValueError) as error:
        print("TPC325_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
