#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-361."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-361-independent-high-origin-tightness-replication"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc361_independent_high_origin_tightness_replication.md"
PRODUCER = PROJECT / "code/tpc361_independent_high_origin_tightness_replication.py"
INDEPENDENT = PROJECT / "experiments/tpc361_independent_checker.py"
STRESS = PROJECT / "experiments/tpc361_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc361_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

# Filled after all claim-bearing files are final.
PRODUCER_SHA256 = "5e48902f49f999cf314ea924796369310b48046a906189388fb9cfc43bcd418e"
INDEPENDENT_SHA256 = "f713c554d7d30af4cdd62d121803748e6f42103e9acd4afd9a50e9feaefc997f"
STRESS_SHA256 = "a7e2c7436275feb82be5af96af7ef208060a11ed6d9c52fe1579ce6267773bbe"
CERTIFICATE_SHA256 = "0b42332a836e8b0392ce8cd02ffc4840770952c15e0c0c9302b1adc34ea62d41"
PDF_SHA256 = "dbbb707c5369ed433a485e1de9b7c83a4b8d9111fa59913a093e4e0bb49ce126"
LOG_SHA256 = "6c34aa87daac8140ce233cdfd2b9b1926983eea385eb5d8bcdbe4ef220e9fce7"
BRIDGE_SHA256 = "f992f7076b850badb648d5d9a0bd4fdbf26ef1388a67d8bb441767a9dfa4a45d"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_HIGH_ORIGIN_TIGHTNESS_REPLICATION"
SCHEMA = "TPC361_INDEPENDENT_HIGH_ORIGIN_TIGHTNESS_REPLICATION_V1"


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
    need(expected != "TO_BE_FILLED" and path.is_file() and
         digest(path.read_bytes()) == expected, label + " provenance")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload", {})
    need(payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "schema/hash")
    protocol = payload.get("protocol", {})
    need(protocol.get("candidate_origins") ==
         [310001 + 233 * j for j in range(51)] and
         protocol.get("pilot_count") == 256 and
         protocol.get("minimum_separation") == 1536 and
         protocol.get("origins") == [313030, 311166, 321651] and
         protocol.get("counts") == [256, 512, 1024, 2048] and
         protocol.get("q_anchors") == [24, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"] and
         protocol.get("source_response_used") is False and
         protocol.get("sign_response_used") is False, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 288 and audit.get("settings") == 72 and
         audit.get("laws") == 4 and audit.get("spectral_rows") == 180 and
         audit.get("normalized_schur_max") == "0.80830232610282304" and
         audit.get("normalized_spectral_max") == "0.62690716242733457" and
         audit.get("max_spectral_over_schur") == "0.77585950058997" and
         audit.get("max_spectral_over_frobenius") == "0.62120835204021907" and
         audit.get("finite_schur_violations") == 0 and
         audit.get("finite_frobenius_violations") == 0 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    need(payload.get("selection", {}).get("selected_origins") ==
         [313030, 311166, 321651], "selection")
    need(payload.get("law_winner_audit", {}).get("winner_counts") == {
        "all_plus": 30, "alternating_index": 0,
        "half_split": 0, "mod4_character": 6}, "winner census")
    need(payload.get("transition_audit", {}).get("counts") == {
        "increase": 12, "decrease": 36, "flat": 6}, "transition census")
    expected = {
        "TPC361_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_RESPONSE_BLIND",
        "TPC361_HIGH_ORIGIN_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
        "TPC361_FINITE_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC361_FINITE_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC361_TIGHTNESS_REPLICATION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC361_LAW_UNIFORM_SHORT_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC361_SCALE_MONOTONE_DECAY": "REFUTED_SCOPED_ON_DECLARED_LADDER",
        "TPC361_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC361_SOURCE_UNIFORM_L2": "OPEN",
        "TPC361_ARITHMETIC_ADVANCE": "NO",
        "TPC361_FIXED_POWER_CREDIT": 0,
        "TPC361_FULL_GATE_B": "OPEN", "TPC361_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        need(payload.get("claim_firewall", {}).get(key) == value,
             "firewall " + key)
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in ("TPC361_MAXIMUM_CLAIM = " + STATUS,
                   "TPC361_ARITHMETIC_ADVANCE = NO",
                   "TPC361_FULL_GATE_B = OPEN"):
        need(marker in text, "bridge marker")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error", "Fatal error",
                "Citation", "Empty"):
        need(bad not in log, "LaTeX diagnostic " + bad)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100000,
         "PDF identity")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script), "--check"])
    environment = dict(os.environ)
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "OMP_NUM_THREADS": "1",
                         "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed " + script.name)
    return result.stdout


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        for path, expected, label in (
                (PRODUCER, PRODUCER_SHA256, "producer"),
                (INDEPENDENT, INDEPENDENT_SHA256, "independent"),
                (STRESS, STRESS_SHA256, "stress"),
                (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
                (MAIN_PDF, PDF_SHA256, "main PDF"),
                (PDF, PDF_SHA256, "paper PDF"),
                (LOG, LOG_SHA256, "compile log"),
                (BRIDGE, BRIDGE_SHA256, "bridge")):
            lock(path, expected, label)
        check_certificate()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        normal = tuple(run(script, False) for script in scripts)
        optimized = tuple(run(script, True) for script in scripts)
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC361_BRIDGE_CHECK=PASS rows=288 spectral_rows=180 "
              "selection=51 origins=3 max_spectral=0.62690716242733457")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC361_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
