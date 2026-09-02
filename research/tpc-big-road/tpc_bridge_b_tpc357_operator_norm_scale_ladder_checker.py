#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-357."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-357-operator-norm-scale-ladder"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc357_operator_norm_scale_ladder.md"
PRODUCER = PROJECT / "code/tpc357_operator_norm_scale_ladder.py"
INDEPENDENT = PROJECT / "experiments/tpc357_independent_checker.py"
STRESS = PROJECT / "experiments/tpc357_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc357_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

# Filled after all claim-bearing files are final.
PRODUCER_SHA256 = "44217207664b8bf08218458f102dacbdb03cf48c85a6fa0d72e7f23fe84a36a1"
INDEPENDENT_SHA256 = "63902457f8da131ca30686e23c0fd178eddc2c5bc06535576e5f3db88ba202b9"
STRESS_SHA256 = "d849bfc358316de9aaacddc45d1f59b43f9d09eb15fa612df66cdad697d8880c"
CERTIFICATE_SHA256 = "9eda189321af2233b6ff39eed97f8ead46ebe6853556b6baf3614e752a6e5fee"
PDF_SHA256 = "bba22933f2398ed5c7fa9339babc07721fd9a00334a08169231be9862e01f64c"
LOG_SHA256 = "bd6d4fc97fab988c093823c252fb41320fe1aba562a3ac0a503d63906cfd7c86"
BRIDGE_SHA256 = "c4a9646f301db3ca81f1e5367c5e12f2748e33ab13ad4d6e79690fa8cf6e9aa7"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_OPERATOR_NORM_SCALE_LADDER"
SCHEMA = "TPC357_OPERATOR_NORM_SCALE_LADDER_V1"


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
    need(protocol.get("origins") == [38423, 42010, 45597] and
         protocol.get("counts") == [256, 512, 1024, 2048] and
         protocol.get("q_anchors") == [24, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"] and
         protocol.get("spectral_laws") == ["all_plus"] and
         protocol.get("source_response_used") is False, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 288 and
         audit.get("all_plus_spectral_rows") == 72 and
         audit.get("finite_schur_violations") == 0 and
         audit.get("finite_frobenius_violations") == 0 and
         audit.get("normalized_schur_max") ==
         "0.8077815961017315" and
         audit.get("normalized_all_plus_spectral_max") ==
         "0.62665294142584216" and
         audit.get("raw_all_plus_spectral_max") ==
         "1542.7455490253569" and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    transitions = payload.get("scale_transition_audit", {}).get("census", {})
    need(transitions.get("normalized_spectral") ==
         {"increase": 15, "decrease": 35, "flat": 4},
         "scale transition census")
    firewall = payload.get("claim_firewall", {})
    for key, value in {
            "TPC357_FINITE_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC357_FINITE_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC357_OPERATOR_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
            "TPC357_NORMALIZED_SCHUR_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC357_ALL_PLUS_SPECTRAL_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC357_SCALE_MONOTONE_DECAY": "REFUTED_SCOPED_ON_DECLARED_LADDER",
            "TPC357_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC357_SOURCE_UNIFORM_L2": "OPEN",
            "TPC357_ARITHMETIC_ADVANCE": "NO",
            "TPC357_FIXED_POWER_CREDIT": 0,
            "TPC357_FULL_GATE_B": "OPEN",
            "TPC357_TWIN_PRIME_RESULT": "NONE",
    }.items():
        need(firewall.get(key) == value, "firewall " + key)
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
        "TPC357_MAXIMUM_CLAIM = " + STATUS,
        "TPC357_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE",
        "TPC357_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE",
        "TPC357_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
        "TPC357_NORMALIZED_SCHUR_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC357_ALL_PLUS_SPECTRAL_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC357_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER",
        "TPC357_GROWING_OPERATOR_BOUND = OPEN",
        "TPC357_SOURCE_UNIFORM_L2 = OPEN",
        "TPC357_ARITHMETIC_ADVANCE = NO",
        "TPC357_FIXED_POWER_CREDIT = 0",
        "TPC357_FULL_GATE_B = OPEN",
        "TPC357_TWIN_PRIME_RESULT = NONE",
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
        print("TPC357_BRIDGE_CHECK=PASS rows=288 spectral_rows=72 "
              "normalized_schur_max=0.8077815961017315 "
              "normalized_spectral_max=0.62665294142584216 "
              "increases=15 decreases=35 flats=4")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC357_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
