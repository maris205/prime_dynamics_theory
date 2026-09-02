#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-358."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-358-fresh-origin-spectral-holdout"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc358_fresh_origin_spectral_holdout.md")
PRODUCER = PROJECT / "code/tpc358_fresh_origin_spectral_holdout.py"
INDEPENDENT = PROJECT / "experiments/tpc358_independent_checker.py"
STRESS = PROJECT / "experiments/tpc358_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc358_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

# Filled after all claim-bearing files are final.
PRODUCER_SHA256 = "4bb40fc4a7aa7da4f222cb35bc2f1f5c115ff6ac03f374bcd1f7ef9204fd29e9"
INDEPENDENT_SHA256 = "6fb069c0a567c040b9b04c7b68e5ae9f08730b3b03d0718d4366a1459935f59e"
STRESS_SHA256 = "be3e21fbd0af86ec785abf877a325d8b6f4d5fdd135ff2ff959e64e6774783e0"
CERTIFICATE_SHA256 = "d87b1e0d2516d2476b44e780cc21f793ab7d3df11fd9d150cb3f8a48facac8f3"
PDF_SHA256 = "50f4ec4e8cc58b891ed3abaa84861e14b3f649755cc0e8336c6719c9c6980ebc"
LOG_SHA256 = "e8b51a3a2c7d569da8148e5ac05c5dca70b929d91fd7991394822a28ee3db201"
BRIDGE_SHA256 = "7edeb5670e76d3650ceaef32fc5413ea5cf10168e0bdb6715a8fe6e23870a8b8"

STATUS = "NUMERICALLY_CERTIFIED_FINITE_FRESH_ORIGIN_SPECTRAL_HOLDOUT"
SCHEMA = "TPC358_FRESH_ORIGIN_SPECTRAL_HOLDOUT_V1"


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
    need(expected != "TO_BE_FILLED", label + " placeholder")
    need(path.is_file() and digest(path.read_bytes()) == expected,
         label + " provenance")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload", {})
    need(payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "schema/payload hash")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [52001, 120001, 220001] and
         protocol.get("origin_rule") ==
         "fixed arithmetic spacing: 52001+100000j, j=0,1,2" and
         protocol.get("disjoint_from_tpc356") is True and
         protocol.get("counts") == [256, 512, 1024, 2048] and
         protocol.get("q_anchors") == [24, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("height") == 66 and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"] and
         protocol.get("spectral_laws") == ["all_plus"] and
         protocol.get("source_response_used") is False, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 288 and
         audit.get("origins") == 3 and
         audit.get("all_law_schur_rows") == 288 and
         audit.get("all_law_frobenius_rows") == 288 and
         audit.get("all_plus_spectral_rows") == 72 and
         audit.get("raw_and_normalized_spectral_metrics") == 144 and
         audit.get("origin_span") == 168000 and
         audit.get("normalized_schur_max") == "0.80850510742101689" and
         audit.get("normalized_all_plus_spectral_max") ==
         "0.62663944469203836" and
         audit.get("raw_all_plus_spectral_max") ==
         "1542.7492651981368" and
         audit.get("parent_normalized_schur_max") ==
         "0.8077815961017315" and
         audit.get("parent_normalized_spectral_max") ==
         "0.62665294142584216" and
         audit.get("parent_transfer_tolerance") == "0.001" and
         audit.get("finite_schur_violations") == 0 and
         audit.get("finite_frobenius_violations") == 0 and
         audit.get("normalized_spectral_increase_transitions") == 13 and
         audit.get("normalized_spectral_decrease_transitions") == 34 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    transitions = payload.get("scale_transition_audit", {}).get("census", {})
    need(transitions.get("normalized_spectral") ==
         {"increase": 13, "decrease": 34, "flat": 7},
         "scale transition census")
    firewall = payload.get("claim_firewall", {})
    for key, value in {
            "TPC358_FINITE_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC358_FINITE_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC358_FRESH_ORIGIN_REPLAY":
            "NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
            "TPC358_PARENT_CAP_TRANSFER":
            "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC358_NORMALIZED_SCHUR_CAP":
            "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC358_ALL_PLUS_SPECTRAL_CAP":
            "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC358_SCALE_MONOTONE_DECAY":
            "REFUTED_SCOPED_ON_DECLARED_LADDER",
            "TPC358_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC358_SOURCE_UNIFORM_L2": "OPEN",
            "TPC358_ARITHMETIC_ADVANCE": "NO",
            "TPC358_FIXED_POWER_CREDIT": 0,
            "TPC358_FULL_GATE_B": "OPEN",
            "TPC358_TWIN_PRIME_RESULT": "NONE",
    }.items():
        need(firewall.get(key) == value, "firewall " + key)
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [52031, 52044] and
         anchor.get("Q") == 4 and anchor.get("shell") == [5, 7] and
         anchor.get("kernel_exponent") == 1 and
         anchor.get("matrix_symmetric") is True and
         anchor.get("geometry_positive") is True and
         anchor.get("row_sums_digest") ==
         "207ab97f0fb7a8a86eaa8448312469a4b4f72319ea5fbf556a2cca252bb58347" and
         anchor.get("geometry_digest") ==
         "86d3fa41dc89af6adad256c3360d1be31568978525858a09c8f37973555a3364",
         "exact anchor")
    need(payload.get("round2_clue") ==
         "TEST_A_GEOMETRY_ADVERSARIAL_FRESH_ORIGIN_OR_SCHUR_TIGHTNESS_HOLDOUT_"
         "BEFORE_ANY_SOURCE_UNIFORM_OPERATOR_CLAIM", "round2 clue")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error", "Fatal error",
                "Citation", "Empty"):
        need(bad not in log, "LaTeX diagnostic: " + bad)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100_000,
         "PDF identity")


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC358_MAXIMUM_CLAIM = " + STATUS,
        "TPC358_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE",
        "TPC358_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE",
        "TPC358_FRESH_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
        "TPC358_PARENT_CAP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC358_NORMALIZED_SCHUR_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC358_ALL_PLUS_SPECTRAL_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC358_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER",
        "TPC358_GROWING_OPERATOR_BOUND = OPEN",
        "TPC358_SOURCE_UNIFORM_L2 = OPEN",
        "TPC358_ARITHMETIC_ADVANCE = NO",
        "TPC358_FIXED_POWER_CREDIT = 0",
        "TPC358_FULL_GATE_B = OPEN",
        "TPC358_TWIN_PRIME_RESULT = NONE",
    )
    for marker in markers:
        need(marker in text, "bridge marker missing")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script), "--check"])
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
        check_certificate()
        check_bridge_text()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        normal = tuple(run(script, False) for script in scripts)
        optimized = tuple(run(script, True) for script in scripts)
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC358_BRIDGE_CHECK=PASS rows=288 spectral_rows=72 "
              "fresh_origins=3 origin_span=168000 "
              "normalized_schur_max=0.80850510742101689 "
              "normalized_spectral_max=0.62663944469203836 "
              "increases=13 decreases=34 flats=7")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC358_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
