#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-309."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-309-profile-prefix-shift-sensitivity"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc309_profile_prefix_shift_sensitivity.md")
PRODUCER = PROJECT / (
    "code/tpc309_profile_prefix_shift_sensitivity.py")
INDEPENDENT = PROJECT / "experiments/tpc309_independent_checker.py"
STRESS = PROJECT / "experiments/tpc309_profile_shift_stress.py"
CERTIFICATE = PROJECT / "results/tpc309_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FINITE_PROFILE_LADDER_SHIFT_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_PROFILE_SENSITIVITY_ATLAS")
SCHEMA = "TPC309_THREE_WINDOW_PROFILE_PREFIX_SHIFT_AUDIT_V1"
PRODUCER_SHA256 = (
    "2284d9ccfcadd02eb5e82a301bdbfa85013e3e9a8352d8f3b078d020742890d9")
INDEPENDENT_SHA256 = (
    "febf1092ec437c0692e898821b92d385d51621e376febe573a7ddded88121818")
STRESS_SHA256 = (
    "8aa69f5d760e38bce29f6f3cc8fb9981d87b303f3170733b7402097e20b3c330")
CERTIFICATE_SHA256 = (
    "a4c8f7cd4aef327682b9457c21236f3756f454f4b82f5a901ab2933f1d4cad4a")
BRIDGE_SHA256 = (
    "c197b05a8b795f5fe305e8e8449f32ed6c1f286e250ba5a8359aa2857cc465b8")
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc309_profile_prefix_shift_sensitivity.py",
    "experiments/tpc309_independent_checker.py",
    "experiments/tpc309_profile_shift_stress.py",
    "results/tpc309_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/paper.pdf",
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
    command += ["-B", str(script)]
    if script == PRODUCER:
        command.append("--check")
    if script == INDEPENDENT:
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
    for path, expected, label in (
            (PRODUCER, PRODUCER_SHA256, "producer"),
            (INDEPENDENT, INDEPENDENT_SHA256, "independent checker"),
            (STRESS, STRESS_SHA256, "stress checker"),
            (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
            (BRIDGE, BRIDGE_SHA256, "bridge")):
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
        "tpc308_code_sha256":
        "08a5058cc2229b2fde2af6d1ee79ed7b7857270dfede5a0109a53364dbfac35c",
        "tpc308_result_sha256":
        "b25f9317f26dc85231c9315bb87c1343b316c2afa760a0e00798d37da1541453",
        "tpc308_cases": 18,
        "tpc308_envelope_observations": 54,
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("profile_pool") ==
         [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
          47, 53, 59, 61, 67], "profile pool")
    need(protocol.get("profile_ladders") == {
        "LOW": [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                47, 53, 59],
        "BASE": [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                 47, 53, 59, 61],
        "HIGH": [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                 47, 53, 59, 61, 67],
    }, "profile ladders")
    audit = payload.get("finite_audit", {})
    need(audit.get("profile_ladders") == 3 and
         audit.get("cases_per_ladder") == 18 and
         audit.get("profile_case_observations") == 54 and
         audit.get("envelope_observations") == 162 and
         audit.get("directional_envelope_records") == 324,
         "finite census")
    need(audit.get("candidate_evaluations_by_radius") ==
         {"0": 108, "1": 558, "2": 1440}, "candidate census")
    expected = {
        "LOW": {
            "agreement_counts_by_radius": {
                "0": {"CONCORDANT": 13, "DISCORDANT": 4, "UNRESOLVED": 1},
                "1": {"CONCORDANT": 10, "DISCORDANT": 2, "UNRESOLVED": 6},
                "2": {"CONCORDANT": 8, "DISCORDANT": 1, "UNRESOLVED": 9},
            },
            "discordance_by_pair_and_radius": {
                "0": {"(50, 60)": 2, "(60, 70)": 1, "(70, 90)": 1},
                "1": {"(50, 60)": 2, "(60, 70)": 0, "(70, 90)": 0},
                "2": {"(50, 60)": 1, "(60, 70)": 0, "(70, 90)": 0},
            },
        },
        "BASE": {
            "agreement_counts_by_radius": {
                "0": {"CONCORDANT": 13, "DISCORDANT": 3, "UNRESOLVED": 2},
                "1": {"CONCORDANT": 11, "DISCORDANT": 2, "UNRESOLVED": 5},
                "2": {"CONCORDANT": 10, "DISCORDANT": 1, "UNRESOLVED": 7},
            },
            "discordance_by_pair_and_radius": {
                "0": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 3},
                "1": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 2},
                "2": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 1},
            },
        },
        "HIGH": {
            "agreement_counts_by_radius": {
                "0": {"CONCORDANT": 10, "DISCORDANT": 5, "UNRESOLVED": 3},
                "1": {"CONCORDANT": 5, "DISCORDANT": 0, "UNRESOLVED": 13},
                "2": {"CONCORDANT": 5, "DISCORDANT": 0, "UNRESOLVED": 13},
            },
            "discordance_by_pair_and_radius": {
                "0": {"(50, 60)": 2, "(60, 70)": 2, "(70, 90)": 1},
                "1": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 0},
                "2": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 0},
            },
        },
    }
    summaries = {s["profile_ladder"]: s
                 for s in payload.get("ladder_summary", [])}
    need(set(summaries) == set(expected), "summary coverage")
    for ladder, exp in expected.items():
        summary = summaries[ladder]
        need(summary.get("agreement_counts_by_radius") ==
             exp["agreement_counts_by_radius"] and
             summary.get("discordance_by_pair_and_radius") ==
             exp["discordance_by_pair_and_radius"], ladder + " summary")
    need(audit.get("baseline_tpc308_class_recovery") is True and
         audit.get("target_generation_leakage") ==
         "INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS" and
         audit.get("causal_identification") ==
         "NONE_PROFILE_SENSITIVITY_DIAGNOSTIC_ONLY" and
         audit.get("formal_interval_certificate") ==
         "OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING" and
         audit.get("uniform_asymptotic_budget") == "OPEN" and
         audit.get("arithmetic_l2") == "OPEN_LITERAL_SOURCE" and
         audit.get("fixed_power_credit") == 0 and
         audit.get("full_gate_b") == "OPEN" and
         audit.get("twin_prime_result") == "NONE", "claim firewall")
    need(len(payload.get("cases", [])) == 54 and
         all(len(case.get("envelopes", [])) == 3
             for case in payload["cases"]) and
         len(payload.get("ladder_summary", [])) == 3, "atlas shape")
    need(MAIN_PDF.is_file(), "missing compiled main PDF")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(),
         "published PDF differs from compiled PDF")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 10_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox"):
        need(bad not in log, "LaTeX warning: " + bad)


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC309_MAXIMUM_CLAIM = " + STATUS,
        "TPC309_ROUTE_ADVANCE = YES_SCOPED_PROFILE_SENSITIVITY_OBSTRUCTION",
        "TPC309_WINDOW_PROTOCOL = PROVED_EXACT_FINITE",
        "TPC309_PREFIX_NESTING = PROVED_EXACT_FINITE",
        "TPC309_HAMMING_EXTREMA = PROVED_EXACT_FINITE",
        "TPC309_NORMALIZER_INVARIANCE = PROVED_EXACT_FINITE",
        "TPC309_PROFILE_ATLAS = NUMERICALLY_REPRODUCED_FINITE_54_PROFILE_CASES_162_ENVELOPES",
        "TPC309_BASELINE_RECOVERY = NUMERICALLY_REPRODUCED_FINITE_TPC308_CLASSES",
        "TPC309_PROFILE_ROBUSTNESS = OPEN_PROFILE_INDEPENDENT_PREFERENCE",
        "TPC309_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS",
        "TPC309_CAUSAL_IDENTIFICATION = NONE_PROFILE_SENSITIVITY_DIAGNOSTIC_ONLY",
        "TPC309_FORMAL_INTERVAL_CERTIFICATE = OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
        "TPC309_UNIFORM_ASYMPTOTIC_BUDGET = OPEN",
        "TPC309_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC309_FIXED_POWER_CREDIT = 0",
        "TPC309_FULL_GATE_B = OPEN",
        "TPC309_TWIN_PRIME_RESULT = NONE",
        "TPC309_STATUS = " + STATUS,
        "TPC309_ROUND2_CLUE = TEST_CROSS_HOLDOUT_AGGREGATION_AND_PROFILE_ROBUSTNESS_BEFORE_ANY_PREFERENCE_CLAIM",
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
        print("TPC309_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC309_BRIDGE_CHECK=PASS ladders=3 cases=54 envelopes=162 "
          "candidates=108/558/1440")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
