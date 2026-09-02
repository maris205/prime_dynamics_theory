#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-359."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-359-geometry-adversarial-high-origin-holdout"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc359_geometry_adversarial_high_origin_holdout.md"
PRODUCER = PROJECT / "code/tpc359_geometry_adversarial_high_origin_holdout.py"
INDEPENDENT = PROJECT / "experiments/tpc359_independent_checker.py"
STRESS = PROJECT / "experiments/tpc359_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc359_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

# Filled after all claim-bearing files are final.
PRODUCER_SHA256 = "ff5088daefb615fb02077662cded3d3c8493789ffa1064609072efe6c0216bb5"
INDEPENDENT_SHA256 = "6909df5520249dd6ef79a4b9c1ef4b05bec7fd732071a6dbe244bf9214e0b561"
STRESS_SHA256 = "7fbbc00cb8622d16f753b94252b733bc114ab83eb3802715840e318aa7b801c9"
CERTIFICATE_SHA256 = "b4edaf61b951acb79222e7d8f7b0cbc7a9278b3de802b11bea5908da89b7bced"
PDF_SHA256 = "cf43bdd7e417ca223104a991f56d2771aee4c29650eaba1f58ac16e09aa49a7b"
LOG_SHA256 = "9728ba824a8f5981c1372369b2ff8f84adfa39b6bd9cb2ce56804c24d7ea6b16"
BRIDGE_SHA256 = "ab136f8ddcab3937a7488c87a6f33af4b85b2bca6603ecdad0c43f76098f1b69"

STATUS = "NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_HIGH_ORIGIN_HOLDOUT"
SCHEMA = "TPC359_GEOMETRY_ADVERSARIAL_HIGH_ORIGIN_HOLDOUT_V1"


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
    need(protocol.get("candidate_origins") == list(range(260001, 270552, 211)) and
         protocol.get("origins") == [267175, 261267, 269074] and
         protocol.get("counts") == [256, 512, 1024, 2048] and
         protocol.get("q_anchors") == [24, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("source_response_used") is False and
         protocol.get("sign_response_used") is False, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 288 and audit.get("origins") == 3 and
         audit.get("candidate_count") == 51 and
         audit.get("origin_span") == 7807 and
         audit.get("normalized_schur_max") == "0.80834744529310265" and
         audit.get("normalized_all_plus_spectral_max") ==
         "0.6271657593674812" and
         audit.get("raw_all_plus_spectral_max") == "1542.7354827195263" and
         audit.get("finite_schur_violations") == 0 and
         audit.get("finite_frobenius_violations") == 0 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    need(audit.get("normalized_spectral_transitions") ==
         {"increase": 12, "decrease": 36, "flat": 6}, "transitions")
    firewall = payload.get("claim_firewall", {})
    expected = {
        "TPC359_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_RESPONSE_BLIND",
        "TPC359_HIGH_ORIGIN_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
        "TPC359_FINITE_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC359_FINITE_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC359_PARENT_CAP_TRANSFER": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC359_NORMALIZED_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC359_SPECTRAL_MONOTONE_DECAY": "REFUTED_SCOPED_ON_DECLARED_LADDER",
        "TPC359_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC359_SOURCE_UNIFORM_L2": "OPEN",
        "TPC359_ARITHMETIC_ADVANCE": "NO",
        "TPC359_FIXED_POWER_CREDIT": 0, "TPC359_FULL_GATE_B": "OPEN",
        "TPC359_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        need(firewall.get(key) == value, "firewall " + key)
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [267205, 267218] and
         anchor.get("Q") == 4 and anchor.get("shell") == [5, 7] and
         anchor.get("kernel_exponent") == 1 and
         anchor.get("matrix_symmetric") is True and
         anchor.get("geometry_positive") is True, "anchor")
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in ("TPC359_MAXIMUM_CLAIM = " + STATUS,
                   "TPC359_ARITHMETIC_ADVANCE = NO",
                   "TPC359_FULL_GATE_B = OPEN"):
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
        print("TPC359_BRIDGE_CHECK=PASS rows=288 origins=3 "
              "origin_span=7807 normalized_schur_max=0.80834744529310265 "
              "normalized_spectral_max=0.6271657593674812 "
              "increases=12 decreases=36 flats=6")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC359_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
