#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-308."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-308-adversarial-exclusive-completion-envelope"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc308_adversarial_exclusive_completion_envelope.md")
PRODUCER = PROJECT / (
    "code/tpc308_adversarial_exclusive_completion_envelope.py")
INDEPENDENT = PROJECT / "experiments/tpc308_independent_checker.py"
STRESS = PROJECT / "experiments/tpc308_completion_stress.py"
CERTIFICATE = PROJECT / "results/tpc308_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FINITE_HAMMING_COMPLETION_ENVELOPE_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_HOLDOUT_STABILITY_ATLAS")
SCHEMA = "TPC308_ADVERSARIAL_EXCLUSIVE_COMPLETION_ENVELOPE_V1"
PRODUCER_SHA256 = (
    "08a5058cc2229b2fde2af6d1ee79ed7b7857270dfede5a0109a53364dbfac35c")
INDEPENDENT_SHA256 = (
    "268504d476620fc17ae4e9070d3c85730db00015ffa53a1445f1a211298a4311")
STRESS_SHA256 = (
    "60236f1a65ed6f88ecf0c334dd8f5523c6b3808b1e4b9607846771da65da3f1b")
CERTIFICATE_SHA256 = (
    "b25f9317f26dc85231c9315bb87c1343b316c2afa760a0e00798d37da1541453")
BRIDGE_SHA256 = (
    "27b4a286b180e5d92231e8e33cc6d7588e55b8925fd7ab73d9414af9a2e06c4f")
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc308_adversarial_exclusive_completion_envelope.py",
    "experiments/tpc308_independent_checker.py",
    "experiments/tpc308_completion_stress.py",
    "results/tpc308_certificate.json", "notes/theorem_ledger.md",
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
    parent = payload.get("parent_lock", {})
    need(parent.get("tpc307_code_sha256") ==
         "50649f9f66dabf97879b38d73283fedcd363900918c838bfcc9f1be807b995b5" and
         parent.get("tpc307_result_sha256") ==
         "8513586b5e7343b257cdd293fe100a4d1680c5df193d568404ebc18539c5f593" and
         parent.get("tpc307_cases") == 18 and
         parent.get("tpc307_directional_holdout_fits") == 36,
         "parent lock")

    audit = payload.get("finite_audit", {})
    need(audit.get("cases") == 18 and audit.get("radii") == 3 and
         audit.get("envelope_observations") == 54 and
         audit.get("directional_envelope_records") == 108,
         "finite census")
    need(audit.get("candidate_evaluations_by_radius") ==
         {"0": 36, "1": 186, "2": 480}, "candidate census")
    need(audit.get("agreement_counts_by_radius") == {
        "0": {"CONCORDANT": 13, "DISCORDANT": 3, "UNRESOLVED": 2},
        "1": {"CONCORDANT": 11, "DISCORDANT": 2, "UNRESOLVED": 5},
        "2": {"CONCORDANT": 10, "DISCORDANT": 1, "UNRESOLVED": 7},
    }, "agreement census")
    need(audit.get("holdout_preference_counts_by_radius") == {
        "0": {"RIGHT_COMPLETION_LOWER": 13,
              "LEFT_COMPLETION_LOWER": 3,
              "PREFERENCE_UNRESOLVED": 2},
        "1": {"RIGHT_COMPLETION_LOWER": 11,
              "LEFT_COMPLETION_LOWER": 2,
              "PREFERENCE_UNRESOLVED": 5},
        "2": {"RIGHT_COMPLETION_LOWER": 9,
              "LEFT_COMPLETION_LOWER": 2,
              "PREFERENCE_UNRESOLVED": 7},
    }, "holdout census")
    need(audit.get("discordance_by_pair_and_radius") == {
        "0": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 3},
        "1": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 2},
        "2": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 1},
    }, "discordance localization")
    need(audit.get("radius_zero_parent_recovery") is True and
         audit.get("target_generation_leakage") ==
         "INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS" and
         audit.get("causal_identification") ==
         "NONE_FIXED_PREDICTION_ENVELOPE_DIAGNOSTIC_ONLY" and
         audit.get("formal_interval_certificate") ==
         "OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING" and
         audit.get("uniform_asymptotic_budget") == "OPEN" and
         audit.get("arithmetic_l2") == "OPEN_LITERAL_SOURCE" and
         audit.get("fixed_power_credit") == 0 and
         audit.get("full_gate_b") == "OPEN" and
         audit.get("twin_prime_result") == "NONE", "claim firewall")
    need(len(payload.get("cases", [])) == 18 and
         all(len(case.get("envelopes", [])) == 3
             for case in payload["cases"]) and
         len(payload.get("pair_summary", [])) == 9, "atlas shape")

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
        "TPC308_MAXIMUM_CLAIM = " + STATUS,
        "TPC308_ROUTE_ADVANCE = YES_SCOPED_ADVERSARIAL_EXCLUSIVE_COMPLETION_ENVELOPE_AUDIT",
        "TPC308_HAMMING_ENVELOPE_PROTOCOL = PROVED_EXACT_FINITE",
        "TPC308_FIXED_PREDICTION_EXTREMA = PROVED_EXACT_FINITE",
        "TPC308_RADIUS_MONOTONICITY = PROVED_EXACT_FINITE",
        "TPC308_RADIUS_ZERO_RECOVERY = PROVED_EXACT_FINITE",
        "TPC308_FINITE_STABILITY_ATLAS = NUMERICALLY_REPRODUCED_FINITE_54_ENVELOPE_OBSERVATIONS",
        "TPC308_AGREEMENT_R0 = NUMERICALLY_REPRODUCED_FINITE_13_CONCORDANT_3_DISCORDANT_2_UNRESOLVED",
        "TPC308_AGREEMENT_R1 = NUMERICALLY_REPRODUCED_FINITE_11_CONCORDANT_2_DISCORDANT_5_UNRESOLVED",
        "TPC308_AGREEMENT_R2 = NUMERICALLY_REPRODUCED_FINITE_10_CONCORDANT_1_DISCORDANT_7_UNRESOLVED",
        "TPC308_DISCORDANCE_SURVIVAL = NUMERICALLY_REPRODUCED_FINITE_3_TO_2_TO_1_AS_RADIUS_0_TO_2",
        "TPC308_DISCORDANCE_LOCALIZATION = NUMERICALLY_REPRODUCED_FINITE_FINAL_PAIR_70_TO_90_ONLY",
        "TPC308_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS",
        "TPC308_CAUSAL_IDENTIFICATION = NONE_FIXED_PREDICTION_ENVELOPE_DIAGNOSTIC_ONLY",
        "TPC308_FORMAL_INTERVAL_CERTIFICATE = OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
        "TPC308_UNIFORM_ASYMPTOTIC_BUDGET = OPEN",
        "TPC308_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC308_FIXED_POWER_CREDIT = 0",
        "TPC308_FULL_GATE_B = OPEN",
        "TPC308_TWIN_PRIME_RESULT = NONE",
        "TPC308_STATUS = " + STATUS,
        "TPC308_ROUND2_CLUE = TEST_PROFILE_PREFIX_PERTURBATION_AND_COMPLETION_INVARIANCE_ON_THE_SURVIVING_DISCORDANCE_CELLS_BEFORE_ANY_PREFERENCE_CLAIM",
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
        print("TPC308_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC308_BRIDGE_CHECK=PASS cases=18 observations=54 "
          "candidates=36/186/480 r0=13/3/2 r1=11/2/5 r2=10/1/7")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
