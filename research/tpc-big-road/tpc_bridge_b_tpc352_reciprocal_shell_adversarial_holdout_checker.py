#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-352."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-352-reciprocal-shell-adversarial-holdout"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc352_reciprocal_shell_adversarial_holdout.md"
PRODUCER = PROJECT / "code/tpc352_reciprocal_shell_adversarial_holdout.py"
INDEPENDENT = PROJECT / "experiments/tpc352_independent_checker.py"
STRESS = PROJECT / "experiments/tpc352_holdout_stress.py"
CERTIFICATE = PROJECT / "results/tpc352_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PRODUCER_SHA256 = "5fc838faef2832b1d8a2aac1613b94506ff0b08fd4c905820a6194f23ebe0cbe"
INDEPENDENT_SHA256 = "fb45df9d90d7b44e025303e7c95e5a3ea228fe55b387d189fa6f5c11da174178"
STRESS_SHA256 = "0834f667b648180ad193590ef6039866fdc10e120662195dfae445e905363c4b"
CERTIFICATE_SHA256 = "e4219b0efaf22c7cbe818341a8240f07fc8252550e8c4d1b02ef5dea3419a888"
PDF_SHA256 = "3fc82d96dc50a72f77758e97429f081147f466ea4edfd7c756e0a9915a7bae06"
LOG_SHA256 = "6cc2500a4ec5438e3b80be55bbbe47573e24733574178fd95ab549eb8da6d8e1"
BRIDGE_SHA256 = "5730eb4ec4c37baafbc5d28429d695d08c27ded19bdab9a214d19b73548b20f9"
STATUS = (
    "PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_DISJOINT_HOLDOUT_AUDIT")
SCHEMA = "TPC352_RECIPROCAL_ADVERSARIAL_HOLDOUT_V1"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def lock(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED", label + " hash placeholder")
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload", {})
    need(payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "schema/digest")
    need(payload.get("parent_lock") == {
        "TPC351_producer_sha256":
        "820f6195408a4d0fbbfed46f5bdd8054d812ae24eb87aaa1169791055f33328a",
        "TPC351_certificate_sha256":
        "74ca0045ca201712a69870669612b7bc16ccd0c019f27f3ea1d3dccb4b687db0",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [96097, 120097, 144097] and
         protocol.get("source_counts") == [256, 512, 1024] and
         protocol.get("q_anchors") == [64, 128, 256, 512] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index"] and
         protocol.get("height") == 66, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 144 and audit.get("series") == 48 and
         audit.get("positive_reciprocal_rows") == 144 and
         audit.get("positive_balanced_rows") == 144 and
         audit.get("zero_sum_records") == 144 and
         audit.get("incidence_gram_records") == 144 and
         audit.get("improved_parent_rows") == 118 and
         audit.get("coordinate_beaten_reciprocal") == 47 and
         audit.get("half_defect_reciprocal") == 49 and
         audit.get("reciprocal_nondecreasing_series") == 22 and
         audit.get("balanced_nondecreasing_series") == 22 and
         audit.get("reciprocal_ratio_min") == "0.0801262572786" and
         audit.get("reciprocal_ratio_max") == "0.829632172143" and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "audit")
    need(len(payload.get("rows", [])) == 144 and
         len(payload.get("growth_series", [])) == 48, "payload census")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [193, 206] and
         anchor.get("coefficients") == ["1/35", "-1/35"] and
         anchor.get("incidence_vector_squared_norm") == "1/245" and
         anchor.get("identity_exact") is True, "exact anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC352_UNIFORM_REPAIR_TRANSFER") == "REFUTED_SCOPED" and
         firewall.get("TPC352_HIGH_SHELL_REPAIR") == "REFUTED_SCOPED" and
         firewall.get("TPC352_PARENT_IMPROVEMENT_CENSUS") ==
         "NUMERICALLY_CERTIFIED_FINITE_118_OF_144" and
         firewall.get("TPC352_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC352_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC352_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC352_TWIN_PRIME_RESULT") == "NONE", "firewall")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error", "Fatal error", "Citation"):
        need(bad not in log, "LaTeX diagnostic: " + bad)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100_000,
         "PDF identity")


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC352_MAXIMUM_CLAIM = " + STATUS,
        "TPC352_RECIPROCAL_RULE = PROVED_EXACT_FINITE_DECLARED_RATIONAL_RULE",
        "TPC352_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA",
        "TPC352_DISJOINT_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
        "TPC352_RECIPROCAL_POSITIVE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_144_OF_144",
        "TPC352_PARENT_IMPROVEMENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_118_OF_144",
        "TPC352_UNIFORM_REPAIR_TRANSFER = REFUTED_SCOPED",
        "TPC352_HIGH_SHELL_REPAIR = REFUTED_SCOPED",
        "TPC352_ARITHMETIC_ADVANCE = NO",
        "TPC352_FIXED_POWER_CREDIT = 0",
        "TPC352_FULL_GATE_B = OPEN",
        "TPC352_TWIN_PRIME_RESULT = NONE",
        "TPC352_ROUND2_CLUE = FREEZE_FINITE_RECIPROCAL_BRANCH_AND_RETURN_TO_SOURCE_NATIVE_L2",
        "TPC352_STATUS = " + STATUS)
    for marker in markers:
        need(marker in text, "bridge marker missing")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script)])
    if script == PRODUCER or script == INDEPENDENT:
        command.append("--check")
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "OMP_NUM_THREADS": "1",
                "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


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
        lock(LOG, LOG_SHA256, "compile log")
        lock(BRIDGE, BRIDGE_SHA256, "bridge")
        check_certificate(); check_bridge_text()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        normal = tuple(run(script, False) for script in scripts)
        optimized = tuple(run(script, True) for script in scripts)
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC352_BRIDGE_CHECK=PASS rows=144 positive_reciprocal=144 "
              "improved_parent=118/144 ratio_floor=0.0801262572786")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC352_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
