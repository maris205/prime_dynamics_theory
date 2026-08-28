#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for TPC-290."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-290-adaptive-shell-weighting-obstruction"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_adaptive_shell_weighting_obstruction.md"
PRODUCER = PROJECT / "code/tpc290_adaptive_shell_weighting_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc290_independent_checker.py"
STRESS = PROJECT / "experiments/tpc290_weighting_stress.py"
CERTIFICATE = PROJECT / "results/tpc290_certificate.json"
STATUS = (
    "PROVED_EXACT_NONNEGATIVE_WEIGHTED_GRAM_NO_DECAY_BOUND_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_ADAPTIVE_WEIGHTING_OBSTRUCTION")
SCHEMA = "TPC290_ADAPTIVE_SHELL_WEIGHTING_CERTIFICATE_V1"
CERTIFICATE_SHA256 = (
    "4e3bb7b23247b0f7e2272063a56e5527365136c1bd748e985d0c4d43d69905fc")
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc290_adaptive_shell_weighting_certificate.py",
    "experiments/tpc290_independent_checker.py",
    "experiments/tpc290_weighting_stress.py", "results/tpc290_certificate.json",
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
        "TPC290_MAXIMUM_CLAIM = " + STATUS,
        "TPC290_ROUTE_ADVANCE = YES_SCOPED_EFFECTIVE_SUPPORT_WEIGHTED_GRAM_FIREWALL",
        "TPC290_WEIGHTED_IDENTITY = PROVED_EXACT_FINITE",
        "TPC290_NONNEGATIVE_NO_DECAY = PROVED_EXACT_CONDITIONAL",
        "TPC290_DIFFUSE_ACCUMULATION_BOUND = PROVED_EXACT_CONDITIONAL",
        "TPC290_FULL_SUPPORT_POLICY_SCAN = NUMERICALLY_CERTIFIED_FINITE_54_OF_54_AMPLIFIED",
        "TPC290_SPARSE_SIGN_FLIP_ESCAPE = NUMERICALLY_CERTIFIED_FINITE_3_PAIRS_ONE_ROW",
        "TPC290_DROP_ONE_SCAN = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_AMPLIFIED",
        "TPC290_UNIFORM_NONNEGATIVE_NO_DECAY = REFUTED_FINITE_BY_SPARSE_SIGN_FLIP",
        "TPC290_GROWING_WEIGHTED_THEOREM = OPEN",
        "TPC290_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE",
        "TPC290_FIXED_POWER_CREDIT = 0",
        "TPC290_FULL_GATE_B = OPEN",
        "TPC290_TWIN_PRIME_RESULT = NONE",
        "TPC290_ROUND2_CLUE = TEST_SIGNED_TWO_PRIME_SCHUR_CANCELLATION_OR_SOURCE_RESTRICTED_DIFFUSE_WEIGHTS",
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
    audit = data["payload"]["finite_audit"]
    need(audit == {
        "all_full_support_policies_amplified_rows": 18,
        "control_signature_groups": 2,
        "diffuse_positive_block_obstruction": "CERTIFIED_FINITE",
        "drop_one_all_amplified_rows": 18,
        "equal_pair_subunit_rows": 1,
        "equal_pair_subunit_witnesses": 3,
        "fixed_power_credit": 0,
        "full_support_policy_rows": 54,
        "growing_weighted_theorem": "OPEN",
        "policy_rows": 54,
        "rows": 18,
        "source_native_L2": "OPEN",
        "strong_coherence_block_rows": 8,
        "uniform_nonnegative_no_decay": "REFUTED_FINITE_BY_SPARSE_SIGN_FLIP",
    }, "finite audit")
    need(len(data["payload"]["rows"]) == 18, "row census")
    need(data["payload"]["rows"][8]["equal_pair_subunit_count"] == 3,
         "exceptional sparse census")
    need(data["payload"]["rows"][8]["equal_pair_subunit_witnesses"][0][
        "prime_pair"] == [29, 53], "exceptional witness")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")
    pdf = (PROJECT / "paper/paper.pdf").read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log = (PROJECT / "paper/main.log").read_text(encoding="utf-8")
    need("undefined" not in log.lower() and "LaTeX Warning:" not in log and
         "Package rerunfilecheck Warning:" not in log and
         "Overfull \\hbox" not in log and "Underfull \\hbox" not in log,
         "LaTeX warning or undefined reference")
    for script in (PRODUCER, INDEPENDENT, STRESS):
        normal = run(script, False)
        optimized = run(script, True)
        need(normal == optimized, script.name + " optimized mismatch")
    print("TPC290_BRIDGE_CHECK=PASS rows=18 policy_rows=54 full_amplified=18 "
          "pair_subunit=3 drop_amplified=18")
    print("claim_level=" + STATUS)


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC290_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
