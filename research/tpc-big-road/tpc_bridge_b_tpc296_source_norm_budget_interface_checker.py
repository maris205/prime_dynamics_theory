#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-296."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-296-source-norm-budget-interface"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc296_source_norm_budget_interface.md")
PRODUCER = PROJECT / (
    "code/tpc296_source_norm_budget_certificate.py")
INDEPENDENT = PROJECT / "experiments/tpc296_independent_checker.py"
STRESS = PROJECT / "experiments/tpc296_budget_stress.py"
CERTIFICATE = PROJECT / "results/tpc296_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_LEAST_NORM_SOURCE_BUDGET_AND_SOURCE_ENERGY_TRADEOFF_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_COST_PROFILE_ATLAS")
SCHEMA = "TPC296_SOURCE_NORM_BUDGET_CERTIFICATE_V1"
PRODUCER_SHA256 = (
    "a30fe40b88eda0f9f257c18fb4d438f129ad5d01ea70d72e54bfe2418d8e0a26")
CERTIFICATE_SHA256 = (
    "469076735f28d1bf55dd7cdc882fe312b74f821f089d9ed352f47c5b26ffe88c")

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc296_source_norm_budget_certificate.py",
    "experiments/tpc296_independent_checker.py",
    "experiments/tpc296_budget_stress.py",
    "results/tpc296_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/paper.pdf")


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
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    for item in REQUIRED:
        need((PROJECT / item).is_file(), "missing artifact: " + item)
    need(digest(PRODUCER.read_bytes()) == PRODUCER_SHA256,
         "producer provenance")
    raw = CERTIFICATE.read_bytes()
    need(digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA, "certificate schema")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("shell_edges") == 1380,
         "finite counts")
    need(audit.get("weighted_minimizer_budget_below_threshold_rows") == 18 and
         audit.get("maxcut_budget_below_threshold_rows") == 18 and
         audit.get("plus_budget_below_threshold_rows") == 18,
         "finite budget atlas")
    need(audit.get("weighted_minimizer_profile_ray_rms_at_least_threshold_rows")
         == 18 and
         audit.get("maxcut_profile_ray_rms_at_least_threshold_rows") == 18 and
         audit.get("plus_profile_ray_rms_at_most_threshold_rows") == 18,
         "finite profile atlas")
    need(audit.get("tradeoff_inequality_failures") == 0 and
         audit.get("fixed_power_credit") == 0, "finite tradeoff/firewall")
    firewall = payload.get("firewall", {})
    need(firewall.get("TPC296_NATIVE_RESTRICTED_PROFILE") ==
         "OPEN_LITERAL_SOURCE" and
         firewall.get("TPC296_ARITHMETIC_L2") == "OPEN_LITERAL_SOURCE" and
         firewall.get("TPC296_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC296_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC296_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(LOG.is_file(), "LaTeX log")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("undefined", "LaTeX Warning:",
                "Package rerunfilecheck Warning:", "Overfull \\hbox",
                "Underfull \\hbox"):
        need(bad not in log, "LaTeX warning: " + bad)
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC296_MAXIMUM_CLAIM = " + STATUS,
        "TPC296_ROUTE_ADVANCE = YES_SCOPED_SOURCE_IMAGE_TO_LEAST_NORM_BUDGET_AND_PROFILE_GEOMETRY",
        "TPC296_LEAST_NORM_IDENTITY = PROVED_EXACT_FINITE",
        "TPC296_BUDGET_FEASIBILITY_CRITERION = PROVED_EXACT_FINITE",
        "TPC296_SOURCE_ENERGY_TRADEOFF = PROVED_EXACT_FINITE",
        "TPC296_COST_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_ROWS_HIGH_PRECISION_REPLAY",
        "TPC296_UNRESTRICTED_BUDGET_TEST = NUMERICAL_OBSERVATION_FINITE_18_OF_18_BELOW_1E_MINUS_3",
        "TPC296_ONE_RAY_PROFILE_OBSTRUCTION = NUMERICAL_OBSERVATION_FINITE_18_OF_18_RMS_AT_LEAST_0_9",
        "TPC296_NATIVE_RESTRICTED_PROFILE = OPEN_LITERAL_SOURCE",
        "TPC296_GROWING_SOURCE_BUDGET = OPEN",
        "TPC296_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC296_FIXED_POWER_CREDIT = 0",
        "TPC296_FULL_GATE_B = OPEN",
        "TPC296_TWIN_PRIME_RESULT = NONE",
        "TPC296_ROUND2_CLUE = TEST_RESTRICTED_PROFILE_DIMENSION_AND_GROWING_SOURCE_BUDGET",
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
        print("TPC296_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC296_BRIDGE_CHECK=PASS rows=18 edges=1380 min_budget=18 "
          "min_profile=18 trade_failures=0")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
