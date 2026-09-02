#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-348."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-348-position-aware-mask-defect-lower-witness"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc348_position_aware_mask_defect_lower_witness.md")
PRODUCER = PROJECT / "code/tpc348_position_aware_mask_defect_lower_witness.py"
INDEPENDENT = PROJECT / "experiments/tpc348_independent_checker.py"
STRESS = PROJECT / "experiments/tpc348_witness_stress.py"
CERTIFICATE = PROJECT / "results/tpc348_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PRODUCER_SHA256 = "fe29f0adeea6234c637a479ba2447068a1e6b1c91731761ed2d2af73464d20b8"
INDEPENDENT_SHA256 = "256a8bc83bf72b318ad51f016277472326ee253d6a431a5451dfbad21a68fdbc"
STRESS_SHA256 = "ed280a9fb8ae41ec701614ca29d83975bcc97d0de65055cb9e98201cbd899cbc"
CERTIFICATE_SHA256 = "5f0b1cb66431f6a57fa97335808f30fdbe86ffc0b31ce074d7a1dbbdc692a294"
PDF_SHA256 = "8f8d9a1e38524ac9a21d8132bd36dce27aebb4fb4a0f2123574aefcfec2bdab0"
LOG_SHA256 = "72d6b8bb49fbf5dd3ff485c85b396d09b7514382d9eb570015ba4703df48cb93"
BRIDGE_SHA256 = "6c4067e34ea62094a5edd9ecc2ae395530885290321885aeba4f306ecd359c9c"
STATUS = (
    "PROVED_EXACT_FINITE_COORDINATE_LOWER_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_POSITION_AUDIT")
SCHEMA = "TPC348_POSITION_AWARE_MASK_DEFECT_LOWER_WITNESS_V1"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def lock(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED", label + " hash placeholder")
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script)])
    if script in (PRODUCER, INDEPENDENT):
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["OMP_NUM_THREADS"] = "1"
    environment["OPENBLAS_NUM_THREADS"] = "1"
    environment["MKL_NUM_THREADS"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "certificate schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload digest")

    audit = payload.get("finite_audit", {})
    need(audit == {
        "arithmetic_advance": "NO",
        "best_hit_lower_bound_records": 192,
        "fixed_power_credit": 0,
        "kernel_exponents": 2,
        "laws": 4,
        "max_mask_hit_count": 169,
        "min_mask_hit_count": 30,
        "origins": 2,
        "position_formula_max_error": "2.0872192863e-14",
        "position_formula_records": 192,
        "positive_witness_rows": 192,
        "q_anchors": 4,
        "rows": 192,
        "source_counts": 3,
    }, "audit census")

    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [40097, 48097] and
         protocol.get("source_counts") == [256, 512, 1024] and
         protocol.get("q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("height") == 66 and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                   "mod4_character", "half_split"] and
         protocol.get("witness_set") ==
         "J_I={t in I: exists p in shell(q), p divides t}",
         "protocol")

    theorem = payload.get("exact_theorem", {})
    need(theorem.get("coordinate_lower_bound") ==
         "||D_I||_(2->2)>=||D_I e_t||_2 for every unit coordinate e_t" and
         theorem.get("mask_hit_lower_bound") ==
         "||D_I||_(2->2)>=max_{t in J_I}||D_I e_t||_2" and
         theorem.get("selector") ==
         "J_I={t in I: exists active shell prime p with p|t}",
         "theorem ledger")

    rows = payload.get("rows", [])
    need(len(rows) == 192 and all(
        item.get("coordinate_lower_bound_holds") is True and
        item.get("best_hit_column_norm") != "0" and
        item.get("mask_hit_count", 0) > 0 and
        float(item.get("position_formula_max_error", "inf")) <= 2.0e-9
        for item in rows), "rows")

    summary = payload.get("summary", {})
    need(summary == {
        "best_hit_to_defect_ratio_max": "0.897148966365",
        "best_hit_to_defect_ratio_min": "0.453958762219",
        "best_hit_to_ideal_ratio_max": "0.336311065586",
        "best_hit_to_ideal_ratio_min": "0.0183057714619",
        "first_hit_to_defect_ratio_max": "0.533179477634",
        "first_hit_to_defect_ratio_min": "0.188855872493",
        "first_hit_to_ideal_ratio_max": "0.133725875157",
        "first_hit_to_ideal_ratio_min": "0.00843336285503",
        "mask_hit_count_max": 169,
        "mask_hit_count_min": 30,
        "position_formula_max_error": "2.0872192863e-14",
        "route_readout":
        "POSITION_AWARE_MASK_HIT_COLUMNS_CERTIFY_A_FINITE_DEFECT_LOWER_WITNESS",
    }, "summary")

    anchor = payload.get("exact_anchor", {})
    need(anchor == {
        "height": 66,
        "hit_indices": [4],
        "identity_exact": True,
        "interval": [1, 6],
        "kernel_exponent": 1,
        "matrix_shape": [6, 6],
        "q": 4,
        "shell": [5, 7],
        "witness_column_digest":
        "7315d3a56bbcfe5cb292dded9d8fbbc028893d28c9b6337cbf892b841846afab",
        "witness_column_squared_norm":
        "1264004832717663389653333/162252681195863096059456",
        "witness_index": 4,
        "witness_position": 5,
    }, "exact anchor")

    firewall = payload.get("claim_firewall", {})
    need(firewall == {
        "TPC348_COORDINATE_LOWER_WITNESS":
        "PROVED_EXACT_FINITE_LINEAR_ALGEBRA",
        "TPC348_DEFECT_DISCARDABILITY": "REFUTED_SCOPED",
        "TPC348_FINITE_POSITION_AUDIT":
        "NUMERICALLY_CERTIFIED_FINITE_192_ROWS",
        "TPC348_FIXED_POWER_CREDIT": 0,
        "TPC348_FULL_GATE_B": "OPEN",
        "TPC348_MASK_HIT_SELECTOR":
        "PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC348_POSITION_FORMULA":
        "PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC348_POSITIVE_WITNESS_CENSUS":
        "NUMERICALLY_CERTIFIED_FINITE_192_OF_192",
        "TPC348_SOURCE_UNIFORM_ARITHMETIC_L2": "OPEN",
        "TPC348_TWIN_PRIME_RESULT": "NONE",
        "TPC348_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
    }, "claim firewall")
    need(payload.get("round2_clue") ==
         "TEST_PRIME_BALANCED_DEFECT_WITNESSES_BEFORE_SOURCE_NATIVE_L2",
         "round2 clue")

    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100_000,
         "PDF identity")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error", "Fatal error",
                "Citation"):
        need(bad not in log, "LaTeX diagnostic: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC348_MAXIMUM_CLAIM = " + STATUS,
        "TPC348_COORDINATE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA",
        "TPC348_MASK_HIT_SELECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC348_POSITION_FORMULA = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC348_FINITE_POSITION_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS",
        "TPC348_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192",
        "TPC348_MASK_DISCARDABILITY = REFUTED_SCOPED",
        "TPC348_BEST_HIT_TO_DEFECT_RATIO = 0.453958762219--0.897148966365",
        "TPC348_ARITHMETIC_ADVANCE = NO",
        "TPC348_FIXED_POWER_CREDIT = 0",
        "TPC348_FULL_GATE_B = OPEN",
        "TPC348_TWIN_PRIME_RESULT = NONE",
        "TPC348_ROUND2_CLUE = TEST_PRIME_BALANCED_DEFECT_WITNESSES_BEFORE_SOURCE_NATIVE_L2",
        "TPC348_STATUS = " + STATUS)
    for marker in markers:
        need(marker in text, "bridge marker missing")


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
        print("TPC348_BRIDGE_CHECK=PASS rows=192 positive_witness=192 "
              "position_formula=192")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC348_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
