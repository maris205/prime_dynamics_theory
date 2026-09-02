#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-360."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-360-schur-tightness-law-uniform-audit"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc360_schur_tightness_law_uniform_audit.md"
PRODUCER = PROJECT / "code/tpc360_schur_tightness_law_uniform_audit.py"
INDEPENDENT = PROJECT / "experiments/tpc360_independent_checker.py"
STRESS = PROJECT / "experiments/tpc360_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc360_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PRODUCER_SHA256 = "0c12d88546fdf11a02e26c588c23c8298cb2a6caa8d841efb2dfd814deb3c10e"
INDEPENDENT_SHA256 = "3c37184717ef46691f9a8b00bf25f62bb57cd365a0d690d7ff82b35ce5c03014"
STRESS_SHA256 = "36453a21289324bc90d8bdece53dfe2d2ad193c4978c715f0b391c330fa44a81"
CERTIFICATE_SHA256 = "3d2e07983768d421757ff75c2122366de4e676fbe3f088fc688bff5046ecfadf"
PDF_SHA256 = "1972e40d4dbd6080dd115ed7757e2463c3e2491a0d1ac018431358330945603f"
LOG_SHA256 = "597a0911ae4350958cad97a60d3506ca221df890ed90bf7f7336c2bd1d96f61d"
BRIDGE_SHA256 = "12b69c9ed59059f66cff35ec07b0968ac31cb368dcf07ba62fd0decf86318ed4"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SCHUR_TIGHTNESS_LAW_UNIFORM_AUDIT"
SCHEMA = "TPC360_SCHUR_TIGHTNESS_LAW_UNIFORM_AUDIT_V1"


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
    need(protocol.get("origins") == [267175, 261267, 269074] and
         protocol.get("counts") == [256, 512] and
         protocol.get("q_anchors") == [24, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 144 and audit.get("settings") == 36 and
         audit.get("laws") == 4 and
         audit.get("max_spectral") == "0.6271657593674812" and
         audit.get("max_spectral_over_schur") == "0.77628391453148915" and
         audit.get("max_spectral_over_frobenius") ==
         "0.62110877254133434" and
         audit.get("finite_schur_violations") == 0 and
         audit.get("finite_frobenius_violations") == 0 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    need(payload.get("law_winner_audit", {}).get("winner_counts") == {
        "all_plus": 30, "alternating_index": 0,
        "mod4_character": 6, "half_split": 0}, "winner census")
    expected = {
        "TPC360_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC360_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC360_ALL_LAW_SPECTRAL_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
        "TPC360_SCHUR_SLACK": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC360_LAW_UNIFORM_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC360_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC360_SOURCE_UNIFORM_L2": "OPEN",
        "TPC360_ARITHMETIC_ADVANCE": "NO",
        "TPC360_FIXED_POWER_CREDIT": 0,
        "TPC360_FULL_GATE_B": "OPEN", "TPC360_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        need(payload.get("claim_firewall", {}).get(key) == value,
             "firewall " + key)
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in ("TPC360_MAXIMUM_CLAIM = " + STATUS,
                   "TPC360_ARITHMETIC_ADVANCE = NO",
                   "TPC360_FULL_GATE_B = OPEN"):
        need(marker in text, "bridge marker")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox", "Underfull \\hbox",
                "LaTeX Error", "Fatal error", "Citation", "Empty"):
        need(bad not in log, "LaTeX diagnostic " + bad)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100000,
         "PDF identity")


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
         "subcheck failed " + script.name)
    return result.stdout


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        for path, expected, label in ((PRODUCER, PRODUCER_SHA256, "producer"),
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
        print("TPC360_BRIDGE_CHECK=PASS rows=144 settings=36 all_law_spectra=144 "
              "max_schur_ratio=0.77628391453148915 "
              "max_frobenius_ratio=0.62110877254133434 winners=30/6")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC360_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
