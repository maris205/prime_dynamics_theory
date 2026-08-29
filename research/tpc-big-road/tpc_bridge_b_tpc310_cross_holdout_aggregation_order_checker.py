#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-310."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-310-cross-holdout-aggregation-order"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc310_cross_holdout_aggregation_order.md")
PRODUCER = PROJECT / (
    "code/tpc310_cross_holdout_aggregation_order.py")
INDEPENDENT = PROJECT / "experiments/tpc310_independent_checker.py"
STRESS = PROJECT / "experiments/tpc310_aggregation_stress.py"
CERTIFICATE = PROJECT / "results/tpc310_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FINITE_CROSS_HOLDOUT_AGGREGATION_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_AGGREGATION_ORDER_OBSTRUCTION_ATLAS")
SCHEMA = "TPC310_CROSS_HOLDOUT_AGGREGATION_ORDER_AUDIT_V1"
PRODUCER_SHA256 = (
    "a3d47a7349d52ed94ac92d1a6c151a537d4655ab50947a0050a994318965882a")
INDEPENDENT_SHA256 = (
    "bf04343c93119f8632501868a46bac49e9a1e2e4d674dca6c8aaeb1065fc2237")
STRESS_SHA256 = (
    "4dffe5644aa8b9aa145385fc2c1bc0c0eb0856361dce1d7e2534c518964f1ef2")
CERTIFICATE_SHA256 = (
    "5bb814e86e742752678d36925e5f719f0b7f998eac76b6c113913aa716f97866")
BRIDGE_SHA256 = (
    "6ce4e1e97e30364a9038d36e6764ab2d9fe3491b11b175719305d8bb6aed13f4")
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc310_cross_holdout_aggregation_order.py",
    "experiments/tpc310_independent_checker.py",
    "experiments/tpc310_aggregation_stress.py",
    "results/tpc310_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/main.pdf",
    "paper/paper.pdf", "paper/compile.log",
)


class Failure(RuntimeError):
    """A fail-closed release validation error."""


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script), "--check"]
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
    for path, expected, label in (
            (PRODUCER, PRODUCER_SHA256, "producer"),
            (INDEPENDENT, INDEPENDENT_SHA256, "independent checker"),
            (STRESS, STRESS_SHA256, "stress checker"),
            (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
            (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(expected != "__BRIDGE_SHA256__", "bridge hash not sealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")

    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA, "certificate schema")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(payload.get("parent_lock") == {
        "tpc309_code_sha256":
        "2284d9ccfcadd02eb5e82a301bdbfa85013e3e9a8352d8f3b078d020742890d9",
        "tpc309_result_sha256":
        "a4c8f7cd4aef327682b9457c21236f3756f454f4b82f5a901ab2933f1d4cad4a",
        "tpc309_profile_cases": 54,
        "tpc309_envelope_observations": 162,
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("ladders") == ["LOW", "BASE", "HIGH"] and
         protocol.get("radii") == [0, 1, 2] and
         protocol.get("aggregation_modes") ==
         ["POOLED_MSE", "BALANCED_RATIO", "GEOMETRIC_RATIO"] and
         protocol.get("selector_count") == 49, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("parent_profile_cases") == 54 and
         audit.get("parent_envelope_observations") == 162 and
         audit.get("parent_candidate_evaluations") == 2106 and
         audit.get("ladder_subset_count") == 7 and
         audit.get("radius_subset_count") == 7 and
         audit.get("selectors") == 49 and
         audit.get("aggregate_observations") == 147, "finite census")
    need(audit.get("class_counts_by_mode") == {
        "POOLED_MSE": {"RIGHT_COMPLETION_LOWER": 42,
                       "LEFT_COMPLETION_LOWER": 1,
                       "PREFERENCE_UNRESOLVED": 6},
        "BALANCED_RATIO": {"RIGHT_COMPLETION_LOWER": 1,
                           "LEFT_COMPLETION_LOWER": 32,
                           "PREFERENCE_UNRESOLVED": 16},
        "GEOMETRIC_RATIO": {"RIGHT_COMPLETION_LOWER": 26,
                             "LEFT_COMPLETION_LOWER": 0,
                             "PREFERENCE_UNRESOLVED": 23},
    }, "class census")
    need(audit.get("full_selector_classes") == {
        "POOLED_MSE": "RIGHT_COMPLETION_LOWER",
        "BALANCED_RATIO": "LEFT_COMPLETION_LOWER",
        "GEOMETRIC_RATIO": "RIGHT_COMPLETION_LOWER",
    }, "full-selector reversal")
    need(audit.get("target_generation_leakage") ==
         "INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS" and
         audit.get("formal_interval_certificate") ==
         "OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING" and
         audit.get("causal_identification") ==
         "NONE_AGGREGATION_DIAGNOSTIC_ONLY" and
         audit.get("fixed_power_credit") == 0 and
         audit.get("full_gate_b") == "OPEN" and
         audit.get("twin_prime_result") == "NONE", "claim firewall")
    need(len(payload.get("selectors", [])) == 49 and
         all(len(s.get("aggregates", [])) == 3
             for s in payload["selectors"]), "atlas shape")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(),
         "published PDF differs from compiled PDF")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error"):
        need(bad not in log, "LaTeX warning: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC310_MAXIMUM_CLAIM = " + STATUS,
        "TPC310_ROUTE_ADVANCE = YES_SCOPED_AGGREGATION_ORDER_OBSTRUCTION",
        "TPC310_SELECTOR_PROTOCOL = PROVED_EXACT_FINITE",
        "TPC310_POOLED_EXTREMA = PROVED_EXACT_FINITE",
        "TPC310_POSITIVE_INTERVAL_MAPS = PROVED_EXACT_FINITE",
        "TPC310_WEIGHTED_MEAN_IDENTITY = PROVED_EXACT_FINITE",
        "TPC310_AGGREGATION_ATLAS = NUMERICALLY_REPRODUCED_FINITE_49_SELECTORS_147_AGGREGATES",
        "TPC310_FULL_SELECTOR_REVERSAL = NUMERICALLY_REPRODUCED_FINITE_POOLED_RIGHT_BALANCED_LEFT_GEOMETRIC_RIGHT",
        "TPC310_PROFILE_ROBUSTNESS = REFUTED_FINITE_NO_UNIVERSAL_AGGREGATION_CLASS",
        "TPC310_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS",
        "TPC310_CAUSAL_IDENTIFICATION = NONE_AGGREGATION_DIAGNOSTIC_ONLY",
        "TPC310_FORMAL_INTERVAL_CERTIFICATE = OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
        "TPC310_UNIFORM_ASYMPTOTIC_BUDGET = OPEN",
        "TPC310_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC310_FIXED_POWER_CREDIT = 0",
        "TPC310_FULL_GATE_B = OPEN",
        "TPC310_TWIN_PRIME_RESULT = NONE",
        "TPC310_STATUS = " + STATUS,
        "TPC310_ROUND2_CLUE = TEST_PREREGISTERED_STRATIFIED_WEIGHTS_AND_HOLDOUT_REPLICATION_BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge_text()
        for script in (PRODUCER, INDEPENDENT, STRESS):
            normal = run(script, False)
            optimized = run(script, True)
            need(normal == optimized, script.name + " optimized mismatch")
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError) as error:
        print("TPC310_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC310_BRIDGE_CHECK=PASS selectors=49 aggregates=147 "
          "full=pooled:R balanced:L geometric:R")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
