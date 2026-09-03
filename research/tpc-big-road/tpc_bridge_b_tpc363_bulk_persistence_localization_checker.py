#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-363."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-363-bulk-persistence-localization"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc363_bulk_persistence_localization.md"
PRODUCER = PROJECT / "code/tpc363_bulk_persistence_localization.py"
INDEPENDENT = PROJECT / "experiments/tpc363_independent_checker.py"
STRESS = PROJECT / "experiments/tpc363_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc363_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

# Filled after all claim-bearing files are final.
PRODUCER_SHA256 = "63fd778f820f5ab8df3dc502dee399e4fc221bb83ff6995123c5007e3075d0d7"
INDEPENDENT_SHA256 = "6c97e469cc9bccb269c520d1c37f7d21f4524270717d774970cf21c714a2c61b"
STRESS_SHA256 = "3755958e69ac9b67ef5e9873c26e03b7255ac6023aa89dbd44f0f583b9308938"
CERTIFICATE_SHA256 = "101297c4f4fbf6e9ffc007d2afb460e80c7de82f90ee82a4c0a73b8689cd97af"
PDF_SHA256 = "2c8e7fbc2acb80f3c35154e60e32a63f1a49b77faa331678ae92956a33371ef1"
LOG_SHA256 = "f20b2e6eb536849814ca280654998396ddccd0bd9461ca20c37a35fd0f37a4b4"
BRIDGE_SHA256 = "d36b27cb156b90f78bb003c155882ad24b52da05dc17f7b7976bdaf174854b5d"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BULK_PERSISTENCE_OBSTRUCTION"
SCHEMA = "TPC363_BULK_PERSISTENCE_LOCALIZATION_V1"


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
         protocol.get("q_anchors") == [80, 128, 256] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"] and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False and
         protocol.get("trim_denominator") == 20, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 144 and audit.get("settings") == 36 and
         audit.get("laws") == 4 and audit.get("spectral_rows") == 144 and
         audit.get("first_spectral_cap_failure_Q") == 128 and
         audit.get("spectral_cap_violations") == 18 and
         audit.get("spectral_cap_violations_Q128") == 6 and
         audit.get("spectral_cap_violations_Q256") == 12 and
         audit.get("bulk_persistence_after_schur_trim") == 18 and
         audit.get("bulk_persistence_after_eigenvector_trim") == 18 and
         audit.get("finite_schur_violations") == 0 and
         audit.get("finite_frobenius_violations") == 0 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO" and
         float(audit["min_trimmed_spectral_over_violations"]) > 0.64 and
         float(audit["max_trimmed_spectral_Q80_control"]) < 0.64,
         "finite audit")
    need(payload.get("law_census", {}).get("violation_law_counts") == {
        "all_plus": 18, "alternating_index": 0,
        "mod4_character": 0, "half_split": 0}, "law census")
    expected = {
        "TPC363_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
        "TPC363_FINITE_ENVELOPE_INEQUALITIES": "PROVED_EXACT_FINITE",
        "TPC363_FIRST_Q128_FAILURE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC363_BULK_PERSISTENCE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC363_SINGLE_ROW_SPIKE_EXPLANATION": "REFUTED_SCOPED_ON_DECLARED_TRIMS",
        "TPC363_EIGENVECTOR_DELOCALIZATION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC363_RENORMALIZED_REPAIR": "OPEN",
        "TPC363_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC363_SOURCE_UNIFORM_L2": "OPEN",
        "TPC363_ARITHMETIC_ADVANCE": "NO",
        "TPC363_FIXED_POWER_CREDIT": 0,
        "TPC363_FULL_GATE_B": "OPEN", "TPC363_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        need(payload.get("claim_firewall", {}).get(key) == value,
             "firewall " + key)
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC363_MAXIMUM_CLAIM = " + STATUS,
            "TPC363_BULK_PERSISTENCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC363_ARITHMETIC_ADVANCE = NO"):
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
        print("TPC363_BRIDGE_CHECK=PASS rows=144 violations=18 "
              "persistent_schur=18 persistent_eigenvector=18")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC363_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
