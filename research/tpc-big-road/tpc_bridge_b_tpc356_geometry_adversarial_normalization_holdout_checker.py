#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-356."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-356-geometry-adversarial-normalization-holdout"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc356_geometry_adversarial_normalization_holdout.md"
PRODUCER = PROJECT / "code/tpc356_geometry_adversarial_normalization_holdout.py"
INDEPENDENT = PROJECT / "experiments/tpc356_independent_checker.py"
STRESS = PROJECT / "experiments/tpc356_adversarial_selection_stress.py"
CERTIFICATE = PROJECT / "results/tpc356_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

# Filled after all claim-bearing files are final.
PRODUCER_SHA256 = "1e36e0417fbc6a3f76f459205cd519f9c2420f960c9b17133f27b70de1940244"
INDEPENDENT_SHA256 = "03a0c8ef32036778cdc96c28a4169d347445b0146b3149630f3689824276c534"
STRESS_SHA256 = "35dff6dd4d4d4ffcbba89a063143cac3b17080474fca44ced9da2bc89325f99b"
CERTIFICATE_SHA256 = "76afe58c8cf13c0cf122c9e167e031fa831335d0ff1cf2597efed9f130ca0ad6"
PDF_SHA256 = "86ba18ea06fe9932d0224bb1c6bf102fb2d99a031190d3973a7ba5bdb72e2fb3"
LOG_SHA256 = "f6aac4204613de3cc1aa1c20a69b000802752a57b6f9773ef53b5ee051b8c1e2"
BRIDGE_SHA256 = "fcac632a584f5e02e3247b249445ea650bb6c9fef806455ccabebbbbbf384219"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_NORMALIZATION_HOLDOUT"
SCHEMA = "TPC356_GEOMETRY_ADVERSARIAL_NORMALIZATION_HOLDOUT_V1"


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
    need(protocol.get("selected_origins") == [38423, 42010, 45597] and
         protocol.get("candidate_origins") == list(range(38001, 48552, 211)) and
         protocol.get("pilot_count") == 256 and
         protocol.get("minimum_separation") == 1536 and
         protocol.get("source_counts") == [256, 512, 1024] and
         protocol.get("q_anchors") == [24, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"],
         "protocol")
    need(protocol.get("selection_uses_response") is False and
         protocol.get("selection_uses_source") is False, "selection firewall")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 216 and
         audit.get("raw_positive_alignment") == 216 and
         audit.get("raw_negative_alignment") == 0 and
         audit.get("normalized_positive_alignment") == 216 and
         audit.get("normalized_negative_alignment") == 0 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("normalization_min_gain") ==
         "0.019062676850676086" and
         audit.get("normalization_mean_gain") ==
         "0.0068817732644231855", "finite audit")
    firewall = payload.get("claim_firewall", {})
    for key, value in {
            "TPC356_GEOMETRY_SELECTION":
            "PROVED_EXACT_FINITE_DETERMINISTIC",
            "TPC356_SELECTION_RESPONSE_INDEPENDENCE":
            "PROVED_EXACT_FINITE",
            "TPC356_PANEL_REPLAY":
            "NUMERICALLY_CERTIFIED_FINITE_216_ROWS",
            "TPC356_ALL_PLUS_MIN_GAIN":
            "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC356_ALL_PLUS_MEAN_GAIN":
            "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC356_SOURCE_UNIFORM_L2": "OPEN",
            "TPC356_ARITHMETIC_ADVANCE": "NO",
            "TPC356_FULL_GATE_B": "OPEN",
            "TPC356_TWIN_PRIME_RESULT": "NONE",
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
        "TPC356_MAXIMUM_CLAIM = " + STATUS,
        "TPC356_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_DETERMINISTIC",
        "TPC356_SELECTION_RESPONSE_INDEPENDENCE = PROVED_EXACT_FINITE",
        "TPC356_PANEL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS",
        "TPC356_RAW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS",
        "TPC356_NORMALIZED_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS",
        "TPC356_ALL_PLUS_MIN_GAIN = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC356_ALL_PLUS_MEAN_GAIN = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC356_SOURCE_UNIFORM_L2 = OPEN",
        "TPC356_ARITHMETIC_ADVANCE = NO",
        "TPC356_FIXED_POWER_CREDIT = 0",
        "TPC356_FULL_GATE_B = OPEN",
        "TPC356_TWIN_PRIME_RESULT = NONE",
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
        print("TPC356_BRIDGE_CHECK=PASS candidates=51 selected=3 rows=216 "
              "raw_positive=216/216 normalized_positive=216/216 "
              "min_gain=0.019062676850676086")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC356_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
