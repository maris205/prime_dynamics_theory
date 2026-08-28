#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for TPC-291."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-291-signed-schur-cancellation-atlas"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_signed_schur_cancellation_atlas.md"
PRODUCER = PROJECT / "code/tpc291_signed_schur_cancellation_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc291_independent_checker.py"
STRESS = PROJECT / "experiments/tpc291_schur_stress.py"
CERTIFICATE = PROJECT / "results/tpc291_certificate.json"
STATUS = (
    "PROVED_EXACT_SIGNED_TWO_PRIME_SCHUR_CANCELLATION_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_COHERENCE_TO_CANCELLATION_ATLAS")
SCHEMA = "TPC291_SIGNED_SCHUR_CANCELLATION_CERTIFICATE_V1"
CERTIFICATE_SHA256 = (
    "b6743bcc574e3fe865832e4867a6d696aa70dd700bceaf1f8b1b7b1f866344b0")
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc291_signed_schur_cancellation_certificate.py",
    "experiments/tpc291_independent_checker.py",
    "experiments/tpc291_schur_stress.py", "results/tpc291_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex", "paper/references.bib",
    "paper/paper.pdf",
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script)]
    if script == PRODUCER:
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check() -> None:
    bridge = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC291_MAXIMUM_CLAIM = " + STATUS,
        "TPC291_ROUTE_ADVANCE = YES_SCOPED_SIGNED_SCHUR_COHERENCE_TO_CANCELLATION_ATLAS",
        "TPC291_SCHUR_PROJECTION_IDENTITY = PROVED_EXACT_FINITE",
        "TPC291_SIGNED_TWO_PRIME_CANCELLATION = PROVED_EXACT_CONDITIONAL",
        "TPC291_RESIDUAL_NONNEGATIVITY = PROVED_EXACT_FROM_CAUCHY",
        "TPC291_COHERENCE_TO_CANCELLATION_ATLAS = NUMERICALLY_CERTIFIED_FINITE_1380_PAIRS",
        "TPC291_LOW_RESIDUAL_COUNTS = NUMERICALLY_CERTIFIED_FINITE_1074_852_477",
        "TPC291_SIGN_COST_CENSUS = NUMERICALLY_CERTIFIED_FINITE_1377_OPPOSITE_3_SAME",
        "TPC291_GROWING_SIGNED_THEOREM = OPEN",
        "TPC291_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE",
        "TPC291_FIXED_POWER_CREDIT = 0",
        "TPC291_FULL_GATE_B = OPEN",
        "TPC291_TWIN_PRIME_RESULT = NONE",
        "TPC291_ROUND2_CLUE = TEST_SOURCE_RESTRICTED_DIFFUSE_WEIGHTS_OR_MULTI_PRIME_SIGNED_NULL_DIRECTIONS",
    )
    for marker in markers:
        need(marker in bridge, "bridge marker")
    for item in REQUIRED:
        need((PROJECT / item).is_file(), "missing artifact: " + item)

    raw = CERTIFICATE.read_bytes()
    need(digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS and
         data.get("payload", {}).get("schema") == SCHEMA,
         "certificate header")

    payload = data["payload"]
    audit = payload["finite_audit"]
    need(audit["rows"] == 18 and audit["total_pairs"] == 1380 and
         audit["positive_pairs"] == 1377 and
         audit["negative_pairs"] == 3 and audit["zero_pairs"] == 0,
         "pair census")
    need(audit["residual_totals"] ==
         {"1/2": 1074, "1/4": 852, "1/10": 477},
         "residual census")
    need(audit["coherence_totals"] == {"9/25": 1189, "3/4": 852},
         "coherence census")
    need(audit["same_sign_cancellation_pairs"] == 3 and
         audit["opposite_sign_cancellation_pairs"] == 1377 and
         audit["all_schur_residuals_nonnegative"] is True,
         "sign/residual audit")
    need(audit["global_best_row"] == {
        "axis": "GROWTH_S2", "scale": 512, "H": 58, "Q": 90,
        "comparison_cutoff_z": 5, "kernel_exponent": 2},
         "global best row")
    best = audit["global_best_pair"]
    need(best["prime_pair"] == [173, 179] and
         best["sign"] == "POSITIVE" and
         best["schur_residual_decimal"] == "0.0151239492702",
         "global best pair")
    need(audit["growing_signed_cancellation_theorem"] == "OPEN" and
         audit["source_native_L2"] == "OPEN" and
         audit["fixed_power_credit"] == 0,
         "claim firewall")
    need(len(payload["rows"]) == 18, "row count")
    need(payload["rows"][8]["pair_negative"] == 3 and
         payload["rows"][8]["negative_pair_records"][0]["prime_pair"] == [29, 53],
         "exceptional row")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")

    pdf = (PROJECT / "paper/paper.pdf").read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log_path = PROJECT / "paper/main.log"
    need(log_path.is_file(), "LaTeX log")
    log = log_path.read_text(encoding="utf-8")
    need("undefined" not in log.lower() and "LaTeX Warning:" not in log and
         "Package rerunfilecheck Warning:" not in log and
         "Overfull \\hbox" not in log and "Underfull \\hbox" not in log,
         "LaTeX warning or undefined reference")

    outputs = {}
    for script in (PRODUCER, INDEPENDENT, STRESS):
        normal = run(script, False)
        optimized = run(script, True)
        need(normal == optimized, script.name + " optimized mismatch")
        outputs[script.name] = normal
    print("TPC291_BRIDGE_CHECK=PASS rows=18 pairs=1380 "
          "residual_le_half=1074 residual_le_quarter=852 "
          "residual_le_tenth=477 negative=3")
    print("claim_level=" + STATUS)


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC291_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
