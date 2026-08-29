#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-306."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-306-two-way-operator-target-interaction"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc306_two_way_operator_target_interaction.md")
PRODUCER = PROJECT / (
    "code/tpc306_two_way_operator_target_interaction.py")
INDEPENDENT = PROJECT / "experiments/tpc306_independent_checker.py"
STRESS = PROJECT / "experiments/tpc306_interaction_stress.py"
CERTIFICATE = PROJECT / "results/tpc306_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_TWO_WAY_LOG_BUDGET_DECOMPOSITION_AND_DOMINANCE_IDENTITY_"
    "PLUS_NUMERICALLY_CERTIFIED_FINITE_OPERATOR_TARGET_INTERACTION_ATLAS")
SCHEMA = "TPC306_TWO_WAY_OPERATOR_TARGET_INTERACTION_V1"
PRODUCER_SHA256 = (
    "7f5a8b424c0c24d431581ea9acfa938a36c1e7ec2900a76e2517c228dda21405")
CERTIFICATE_SHA256 = (
    "ab9eba3317e4e22d4955c15cb7a0c22e55fd0495696f34be1476985f2232a34b")
BRIDGE_SHA256 = "33910d317349df7a610038966a88aa4480c86bfd6d7d88a19368fad6cc70775a"
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc306_two_way_operator_target_interaction.py",
    "experiments/tpc306_independent_checker.py",
    "experiments/tpc306_interaction_stress.py",
    "results/tpc306_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/paper.pdf")


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
    need(digest(BRIDGE.read_bytes()) == BRIDGE_SHA256,
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
    need(audit.get("cases") == 18 and
         audit.get("decomposition_rows") == 54 and
         audit.get("target_main_dominates_cases") == 12 and
         audit.get("operator_interaction_dominates_cases") == 6 and
         audit.get("unresolved_cases") == 0 and
         audit.get("middle_pair") == [60, 70] and
         audit.get("middle_target_main_dominates") == 5 and
         audit.get("middle_operator_interaction_dominates") == 1 and
         audit.get("middle_same_prefix_target_main_dominates") == 3 and
         audit.get("all_main_ratio_intervals_below_0_88") is True and
         audit.get("all_interaction_ratio_intervals_above_1_2") is True and
         audit.get("middle_same_prefix_max_ratio_below_0_64") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_l2") == "OPEN_LITERAL_SOURCE" and
         audit.get("uniform_asymptotic_budget") == "OPEN" and
         audit.get("causal_identification") ==
         "OPEN_COMMON_AMBIENT_HOLDOUT", "finite audit")
    need(len(payload.get("cases", [])) == 18 and
         len(payload.get("pair_summary", [])) == 3 and
         payload.get("firewall", {}).get("TPC306_FULL_GATE_B") == "OPEN" and
         payload.get("firewall", {}).get("TPC306_TWIN_PRIME_RESULT") == "NONE",
         "atlas shape/firewall")

    max_main = interval(audit["max_main_ratio_interval"])
    min_interaction = interval(audit["min_interaction_ratio_interval"])
    max_same = interval(audit["middle_same_prefix_max_ratio_interval"])
    need(max_main[1] < Decimal("0.88") and
         min_interaction[0] > Decimal("1.2") and
         max_same[1] < Decimal("0.64"), "ratio margins")

    need(MAIN_PDF.is_file(), "missing main PDF build")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(),
         "published PDF differs from compiled PDF")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("undefined", "LaTeX Warning:",
                "Package rerunfilecheck Warning:", "Overfull \\hbox",
                "Underfull \\hbox", "[VERIFY]"):
        need(bad not in log, "LaTeX warning/marker: " + bad)


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC306_MAXIMUM_CLAIM = " + STATUS,
        "TPC306_ROUTE_ADVANCE = YES_SCOPED_TWO_WAY_INTERACTION_DECOMPOSITION",
        "TPC306_LOG_DECOMPOSITION = PROVED_EXACT_FINITE",
        "TPC306_SQUARED_DOMINANCE_IDENTITY = PROVED_EXACT_FINITE",
        "TPC306_ROW_SCALING_INVARIANCE = PROVED_EXACT_FINITE",
        "TPC306_DECOMPOSITION_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_CASES_54_ROWS",
        "TPC306_TARGET_MAIN_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_12_OF_18",
        "TPC306_INTERACTION_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_6_OF_18",
        "TPC306_MIDDLE_TARGET_MAIN = NUMERICALLY_CERTIFIED_FINITE_5_OF_6",
        "TPC306_MIDDLE_SAME_PREFIX_TARGET_MAIN = NUMERICALLY_CERTIFIED_FINITE_3_OF_3",
        "TPC306_RATIO_GAP = NUMERICALLY_CERTIFIED_FINITE_MAIN_LT_0_88_INTERACTION_GT_1_2",
        "TPC306_CAUSAL_IDENTIFICATION = OPEN_COMMON_AMBIENT_HOLDOUT",
        "TPC306_UNIFORM_ASYMPTOTIC_BUDGET = OPEN",
        "TPC306_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC306_FIXED_POWER_CREDIT = 0",
        "TPC306_FULL_GATE_B = OPEN",
        "TPC306_TWIN_PRIME_RESULT = NONE",
        "TPC306_ROUND2_CLUE = TEST_COMMON_AMBIENT_UNION_SHELL_COMPLETIONS_AND_INTERACTION_STABILITY_BEFORE_ANY_GROWING_TARGET_PREFERENCE_CLAIM",
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
        print("TPC306_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC306_BRIDGE_CHECK=PASS cases=18 decomposition_rows=54 "
          "target_main=12/18 interaction=6/18 middle=5/6 same_prefix=3/3")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
