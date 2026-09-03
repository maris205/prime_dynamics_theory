#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-362."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-362-shell-scale-cap-obstruction"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc362_shell_scale_cap_obstruction.md"
PRODUCER = PROJECT / "code/tpc362_shell_scale_cap_obstruction.py"
INDEPENDENT = PROJECT / "experiments/tpc362_independent_checker.py"
STRESS = PROJECT / "experiments/tpc362_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc362_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

# Filled after the paper and all claim-bearing files are final.
PRODUCER_SHA256 = "47d0dc48e64869a3a68daa9798359014f31c1ecfac976d5338a0e346c658a121"
INDEPENDENT_SHA256 = "65476c9f7a4c1ed95e71ac676793d187fba737817a81ba27b41b92a6578a712c"
STRESS_SHA256 = "481c77ef49ae1c838d752d42663ee833133cab6a767371a63776694d5c9e9ca1"
CERTIFICATE_SHA256 = "7780856a7394f8060121dd41fc7a0b7cd066cd2c858e8b2a4891090e5577a4a6"
PDF_SHA256 = "28873658645e969c7470c32d15beaa63d4f4b7528c1a0c2826fe5d758c0795b6"
LOG_SHA256 = "ea69fc7736d367c6943e9464d42dcd2edbc106e49f5de10675493b7f2cc63f81"
BRIDGE_SHA256 = "2d33966999b77e82f39699efc7ed042e08337312206a0716c3a6c57a37a036f0"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SHELL_SCALE_CAP_OBSTRUCTION"
SCHEMA = "TPC362_SHELL_SCALE_CAP_OBSTRUCTION_V1"


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
    need(protocol.get("origins") == [313030, 311166, 321651] and
         protocol.get("counts") == [256, 512] and
         protocol.get("q_anchors") == [12, 24, 36, 54, 80, 128, 256, 512] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"] and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 384 and audit.get("settings") == 96 and
         audit.get("laws") == 4 and audit.get("spectral_rows") == 384 and
         audit.get("normalized_schur_max") == "1.7172665118910415" and
         audit.get("normalized_spectral_max") == "1.6398895499394266" and
         audit.get("low_q_normalized_schur_max") == "0.80830232610282304" and
         audit.get("low_q_normalized_spectral_max") == "0.62690716242733457" and
         audit.get("first_schur_cap_failure_Q") == 128 and
         audit.get("first_spectral_cap_failure_Q") == 128 and
         audit.get("schur_cap_violations") == 33 and
         audit.get("spectral_cap_violations") == 30 and
         audit.get("finite_schur_violations") == 0 and
         audit.get("finite_frobenius_violations") == 0 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    need(payload.get("law_winner_audit", {}).get("winner_counts") == {
        "all_plus": 78, "alternating_index": 4,
        "half_split": 0, "mod4_character": 14}, "winner census")
    need(payload.get("q_transition_audit", {}).get("counts") == {
        "increase": 200, "decrease": 136, "flat": 0}, "Q transition census")
    expected = {
        "TPC362_SHELL_SCALE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_384_ROWS",
        "TPC362_FINITE_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC362_FINITE_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC362_LOW_Q_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC362_HIGH_Q_CAP_EXTENSION": "REFUTED_SCOPED_ON_DECLARED_Q_LADDER",
        "TPC362_LAW_WINNER_CENSUS": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC362_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC362_SOURCE_UNIFORM_L2": "OPEN",
        "TPC362_ARITHMETIC_ADVANCE": "NO",
        "TPC362_FIXED_POWER_CREDIT": 0,
        "TPC362_FULL_GATE_B": "OPEN", "TPC362_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        need(payload.get("claim_firewall", {}).get(key) == value,
             "firewall " + key)
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in ("TPC362_MAXIMUM_CLAIM = " + STATUS,
                   "TPC362_HIGH_Q_CAP_EXTENSION = REFUTED_SCOPED_ON_DECLARED_Q_LADDER",
                   "TPC362_ARITHMETIC_ADVANCE = NO"):
        need(marker in bridge_text, "bridge marker")
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
        print("TPC362_BRIDGE_CHECK=PASS rows=384 all_laws=4 "
              "first_cap_failure_Q=128 spectral_violations=30")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC362_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
