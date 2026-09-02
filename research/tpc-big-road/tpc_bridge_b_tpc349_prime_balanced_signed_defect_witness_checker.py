#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-349."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-349-prime-balanced-signed-defect-witness"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc349_prime_balanced_signed_defect_witness.md")
PRODUCER = PROJECT / "code/tpc349_prime_balanced_signed_defect_witness.py"
INDEPENDENT = PROJECT / "experiments/tpc349_independent_checker.py"
STRESS = PROJECT / "experiments/tpc349_signed_witness_stress.py"
CERTIFICATE = PROJECT / "results/tpc349_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PRODUCER_SHA256 = "ed3b543a44a270301f3cc7543533c1ce35a6f9ea433e9581df19759b2bca3a03"
INDEPENDENT_SHA256 = "6a2e547c34511610be2d1e7c61804851c2cbec0fef1934cd7f4459b76bbadb7e"
STRESS_SHA256 = "9aa5e423f425ca7234c317d1c717aab1216a5d885b66d5dcd33e2c9d3b524d60"
CERTIFICATE_SHA256 = "baceb7b6cbf32fbbf84289d302551ed7f42abb45c39333a7d235a229c9a7a741"
PDF_SHA256 = "1ce9574dabf23c42a18e97576921678c84bf4b633754ed8bed92765e5c3f68e2"
LOG_SHA256 = "2f879298c0bb67d8ea26c6f4462fb14c0d83f6d58f469fb309b2d6fd43ac5081"
BRIDGE_SHA256 = "6bab6e7086ef0e1b87c0f607cfd68174cb3526e8d7234ae56763bb3aa3595600"
STATUS = (
    "PROVED_EXACT_FINITE_PRIME_BALANCED_INCIDENCE_LOWER_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_AUDIT")
SCHEMA = "TPC349_PRIME_BALANCED_SIGNED_DEFECT_WITNESS_V1"


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

    need(payload.get("parent_lock") == {
        "TPC348_producer_sha256":
        "fe29f0adeea6234c637a479ba2447068a1e6b1c91731761ed2d2af73464d20b8",
        "TPC348_certificate_sha256":
        "5f0b1cb66431f6a57fa97335808f30fdbe86ffc0b31ce074d7a1dbbdc692a294",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [40097, 48097] and
         protocol.get("source_counts") == [256, 512, 1024] and
         protocol.get("q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("height") == 66 and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                   "mod4_character", "half_split"] and
         protocol.get("balanced_rule") ==
         "beta_j=+1 for j<floor(r/2), -1 for j>=r-floor(r/2), "
         "and 0 for a possible middle prime" and
         protocol.get("incidence_vector") ==
         "b_I(t)=sum_j beta_j 1_(p_j divides t)",
         "protocol")

    theorem = payload.get("exact_theorem", {})
    need(theorem.get("incidence_identity") ==
         "b_I=sum_j beta_j h_{p_j,I}" and
         theorem.get("gram_expansion") ==
         "||D_I b_I||_2^2=sum_{j,k} beta_j beta_k "
         "<D_I h_{p_j,I},D_I h_{p_k,I}>" and
         theorem.get("normalized_lower_bound") ==
         "||D_I||_(2->2)>=||D_I b_I||_2/||b_I||_2 for b_I != 0",
         "theorem ledger")

    audit = payload.get("finite_audit", {})
    need(audit == {
        "arithmetic_advance": "NO",
        "balanced_sum_records": 192,
        "coordinate_beaten_rows": 136,
        "fixed_power_credit": 0,
        "half_defect_rows": 175,
        "incidence_gram_max_error": "1.06581410364e-14",
        "incidence_gram_records": 192,
        "kernel_exponents": 2,
        "laws": 4,
        "max_signed_support": 150,
        "min_signed_support": 28,
        "origins": 2,
        "positive_signed_witness_rows": 192,
        "q_anchors": 4,
        "rows": 192,
        "source_counts": 3,
    }, "audit census")

    summary = payload.get("summary", {})
    need(summary == {
        "coordinate_beaten_rows": 136,
        "half_defect_rows": 175,
        "incidence_gram_max_error": "1.06581410364e-14",
        "route_readout":
        "PRIME_BALANCED_SIGNED_INCIDENCE_GIVES_A_FINITE_DEFECT_LOWER_WITNESS",
        "signed_support_max": 150,
        "signed_support_min": 28,
        "signed_to_coordinate_ratio_max": "2.04702542827",
        "signed_to_coordinate_ratio_min": "0.542800508699",
        "signed_to_defect_ratio_max": "0.954375010719",
        "signed_to_defect_ratio_mean": "0.774201744064",
        "signed_to_defect_ratio_min": "0.39083565842",
        "signed_to_ideal_ratio_max": "0.430061305156",
        "signed_to_ideal_ratio_min": "0.0125941959067",
    }, "summary")

    rows = payload.get("rows", [])
    need(len(rows) == 192 and all(
        item.get("balanced_coefficient_sum") == 0 and
        item.get("balanced_active_prime_count") in (6, 8, 12, 14) and
        item.get("signed_incidence_support", 0) > 0 and
        item.get("signed_witness_response_norm") != "0" and
        item.get("coordinate_lower_bound_holds") is True and
        float(item.get("incidence_gram_max_error", "inf")) <= 2.0e-9
        for item in rows), "rows")
    need(sum(item.get("beats_coordinate_baseline") is True for item in rows)
         == 136 and
         sum(item.get("at_least_half_defect") is True for item in rows) == 175,
         "row census flags")

    need(payload.get("exact_anchor") == {
        "coefficients": [1, -1],
        "height": 66,
        "identity_exact": True,
        "incidence_vector": [0, 0, 0, 0, 1, 0, -1, 0, 0, 1, 0, 0, 0, -1],
        "incidence_vector_squared_norm": "4",
        "interval": [1, 14],
        "kernel_exponent": 1,
        "matrix_shape": [14, 14],
        "q": 4,
        "response_vector_digest":
        "22bb4ab64b4c3b0bc0b2513d983fda17b614e22125432ae666b7956573ffa2fc",
        "response_vector_squared_norm":
        "1580136191762341638715051100269721298390649257672312877072677225319/"
        "4277374121662663268940652066711233824047030196831076541809000000",
        "shell": [5, 7],
    }, "exact anchor")

    need(payload.get("claim_firewall") == {
        "TPC349_COORDINATE_BASELINE_BEATEN":
        "NUMERICALLY_CERTIFIED_FINITE_136_OF_192",
        "TPC349_FINITE_SIGNED_AUDIT":
        "NUMERICALLY_CERTIFIED_FINITE_192_ROWS",
        "TPC349_FIXED_POWER_CREDIT": 0,
        "TPC349_FULL_GATE_B": "OPEN",
        "TPC349_HALF_DEFECT_CENSUS":
        "NUMERICALLY_CERTIFIED_FINITE_175_OF_192",
        "TPC349_INCIDENCE_GRAM_IDENTITY":
        "PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC349_POSITIVE_WITNESS_CENSUS":
        "NUMERICALLY_CERTIFIED_FINITE_192_OF_192",
        "TPC349_PRIME_BALANCE_RULE":
        "PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC349_SIGNED_INCIDENCE_LOWER_WITNESS":
        "PROVED_EXACT_FINITE_LINEAR_ALGEBRA",
        "TPC349_SOURCE_UNIFORM_ARITHMETIC_L2": "OPEN",
        "TPC349_TWIN_PRIME_RESULT": "NONE",
        "TPC349_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
        "TPC349_UNIVERSAL_BALANCED_GAIN": "REFUTED_SCOPED",
    }, "claim firewall")
    need(payload.get("round2_clue") ==
         "REPLICATE_SIGNED_INCIDENCE_GRAM_ON_GROWING_FRESH_PANELS",
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
        "TPC349_MAXIMUM_CLAIM = " + STATUS,
        "TPC349_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA",
        "TPC349_PRIME_BALANCE_RULE = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC349_INCIDENCE_GRAM_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC349_FINITE_SIGNED_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS",
        "TPC349_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192",
        "TPC349_COORDINATE_BASELINE_BEATEN = NUMERICALLY_CERTIFIED_FINITE_136_OF_192",
        "TPC349_HALF_DEFECT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_175_OF_192",
        "TPC349_UNIVERSAL_BALANCED_GAIN = REFUTED_SCOPED",
        "TPC349_ARITHMETIC_ADVANCE = NO",
        "TPC349_FIXED_POWER_CREDIT = 0",
        "TPC349_FULL_GATE_B = OPEN",
        "TPC349_TWIN_PRIME_RESULT = NONE",
        "TPC349_ROUND2_CLUE = REPLICATE_SIGNED_INCIDENCE_GRAM_ON_GROWING_FRESH_PANELS",
        "TPC349_STATUS = " + STATUS)
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
        print("TPC349_BRIDGE_CHECK=PASS rows=192 positive_witness=192 "
              "coordinate_beaten=136 half_defect=175")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC349_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
