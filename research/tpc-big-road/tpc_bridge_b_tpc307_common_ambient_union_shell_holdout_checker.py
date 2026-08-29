#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-307."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-307-common-ambient-union-shell-holdout"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc307_common_ambient_union_shell_holdout.md")
PRODUCER = PROJECT / (
    "code/tpc307_common_ambient_union_shell_holdout.py")
INDEPENDENT = PROJECT / "experiments/tpc307_independent_checker.py"
STRESS = PROJECT / "experiments/tpc307_holdout_stress.py"
CERTIFICATE = PROJECT / "results/tpc307_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FINITE_COMMON_AMBIENT_UNION_SHELL_HOLDOUT_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_BUDGET_HOLDOUT_DISCORDANCE_ATLAS")
SCHEMA = "TPC307_COMMON_AMBIENT_UNION_SHELL_HOLDOUT_V1"
PRODUCER_SHA256 = "50649f9f66dabf97879b38d73283fedcd363900918c838bfcc9f1be807b995b5"
CERTIFICATE_SHA256 = "8513586b5e7343b257cdd293fe100a4d1680c5df193d568404ebc18539c5f593"
BRIDGE_SHA256 = "08d4a6b01a7a39474aedf3aac154de5d3ab23256b0e04684d1103c9d8302d0d4"
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc307_common_ambient_union_shell_holdout.py",
    "experiments/tpc307_independent_checker.py",
    "experiments/tpc307_holdout_stress.py", "results/tpc307_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex", "paper/references.bib",
    "paper/paper.pdf")


class Failure(RuntimeError):
    pass


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def interval(value: object) -> tuple[Decimal, Decimal]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = Decimal(str(value[0])), Decimal(str(value[1]))
    need(lo <= hi, "interval order")
    return lo, hi


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script)]
    if script == PRODUCER:
        command.append("--check")
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    for relative in REQUIRED:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
    need(digest(PRODUCER.read_bytes()) == PRODUCER_SHA256,
         "producer provenance")
    need(digest(CERTIFICATE.read_bytes()) == CERTIFICATE_SHA256,
         "certificate provenance")
    need(BRIDGE_SHA256 != "__BRIDGE_SHA256__" and
         digest(BRIDGE.read_bytes()) == BRIDGE_SHA256,
         "bridge provenance")

    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA, "certificate schema")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    audit = payload.get("finite_audit", {})
    need(audit.get("cases") == 18 and audit.get("observations") == 18 and
         audit.get("directional_holdout_fits") == 36 and
         audit.get("normalizer_rows") == 54 and audit.get("union_shells") == 6,
         "finite census")
    need(audit.get("agreement_counts") ==
         {"CONCORDANT": 13, "DISCORDANT": 3, "UNRESOLVED": 2},
         "agreement census")
    need(audit.get("budget_preference_counts") ==
         {"LEFT_COMPLETION_LOWER": 5, "PREFERENCE_UNRESOLVED": 0,
          "RIGHT_COMPLETION_LOWER": 13}, "budget census")
    need(audit.get("holdout_preference_counts") ==
         {"LEFT_COMPLETION_LOWER": 3, "PREFERENCE_UNRESOLVED": 2,
          "RIGHT_COMPLETION_LOWER": 13}, "holdout census")
    need(audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_l2") == "OPEN_LITERAL_SOURCE" and
         audit.get("uniform_asymptotic_budget") == "OPEN" and
         audit.get("causal_identification") ==
         "NONE_DIRECTIONAL_HOLDOUT_DIAGNOSTIC_ONLY" and
         audit.get("full_gate_b") == "OPEN" and
         audit.get("twin_prime_result") == "NONE", "firewall")
    need(len(payload.get("cases", [])) == 18 and
         len(payload.get("pair_summary", [])) == 3, "atlas shape")

    need(MAIN_PDF.is_file(), "missing main PDF build")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(),
         "published PDF differs from compiled PDF")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 10_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("undefined", "LaTeX Warning:",
                "Package rerunfilecheck Warning:", "Overfull \\hbox",
                "Underfull \\hbox"):
        need(bad not in log, "LaTeX warning: " + bad)


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC307_MAXIMUM_CLAIM = " + STATUS,
        "TPC307_ROUTE_ADVANCE = YES_SCOPED_COMMON_AMBIENT_DIRECTIONAL_HOLDOUT_DIAGNOSTIC",
        "TPC307_COMMON_AMBIENT_UNION = PROVED_EXACT_FINITE",
        "TPC307_OVERLAP_ONLY_FIT = PROVED_EXACT_FINITE",
        "TPC307_EXCLUSIVE_HOLDOUT = PROVED_EXACT_FINITE",
        "TPC307_FINITE_HOLDOUT_ATLAS = NUMERICALLY_REPRODUCED_FINITE_18_CASES_36_DIRECTIONAL_FITS_54_NORMALIZER_ROWS",
        "TPC307_AGREEMENT_CENSUS = NUMERICALLY_REPRODUCED_FINITE_CONCORDANT_13_DISCORDANT_3_UNRESOLVED_2",
        "TPC307_BUDGET_PREFERENCE = NUMERICALLY_REPRODUCED_FINITE_RIGHT_13_LEFT_5_UNRESOLVED_0",
        "TPC307_HOLDOUT_PREFERENCE = NUMERICALLY_REPRODUCED_FINITE_RIGHT_13_LEFT_3_UNRESOLVED_2",
        "TPC307_DISCORDANCE_LOCALIZATION = NUMERICALLY_REPRODUCED_FINITE_ALL_3_AT_Q70_TO_90_EXPONENT_1",
        "TPC307_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS",
        "TPC307_CAUSAL_IDENTIFICATION = NONE_DIRECTIONAL_HOLDOUT_DIAGNOSTIC_ONLY",
        "TPC307_FORMAL_INTERVAL_CERTIFICATE = OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
        "TPC307_UNIFORM_ASYMPTOTIC_BUDGET = OPEN",
        "TPC307_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC307_FIXED_POWER_CREDIT = 0",
        "TPC307_FULL_GATE_B = OPEN",
        "TPC307_TWIN_PRIME_RESULT = NONE",
        "TPC307_STATUS = " + STATUS,
        "TPC307_ROUND2_CLUE = STRESS_COMMON_AMBIENT_HOLDOUT_AGAINST_EXCLUSIVE_COMPLETION_ENVELOPES_AND_PROFILE_PREFIX_PERTURBATIONS_BEFORE_ANY_CAUSAL_PREFERENCE_CLAIM",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge()
        for script in (PRODUCER, INDEPENDENT, STRESS):
            normal = run(script, False)
            optimized = run(script, True)
            need(normal == optimized, script.name + " optimized mismatch")
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError) as error:
        print("TPC307_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC307_BRIDGE_CHECK=PASS cases=18 directional_fits=36 "
          "concordant=13 discordant=3 unresolved=2")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
