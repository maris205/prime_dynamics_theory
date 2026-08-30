#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-311."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-311-stratified-tau-holdout-replication"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc311_stratified_tau_holdout_replication.md")
PRODUCER = PROJECT / (
    "code/tpc311_stratified_tau_holdout_replication.py")
INDEPENDENT = PROJECT / "experiments/tpc311_independent_checker.py"
STRESS = PROJECT / "experiments/tpc311_stratification_stress.py"
CERTIFICATE = PROJECT / "results/tpc311_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/compile.log"
STATUS = (
    "PROVED_EXACT_FINITE_STRATIFIED_HOLDOUT_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_TAU_SLICE_NONREPLICATION_ATLAS")
SCHEMA = "TPC311_STRATIFIED_TAU_SLICE_HOLDOUT_REPLICATION_V1"
PRODUCER_SHA256 = (
    "9d10375def6b3b136c16fabbce806a854699c4b5d494a77aab07fab20aa7ece2")
INDEPENDENT_SHA256 = (
    "dc17be6ffa31b5883cd31c1299a07f71660cca9c6a9b93cbda7d96d35ff6aa03")
STRESS_SHA256 = (
    "c3c1c7ab77ba5adfd5ea228f0afa192abcd29807a63ae664e871471b632e9375")
CERTIFICATE_SHA256 = (
    "0e7ac4ef8d7f62d152ce364a46e5c6f09cabd8e38af3448f65b7249bdda95acd")
BRIDGE_SHA256 = (
    "73b6c9455fa772a44836b2898c3c3a25f33874bb4ce1e1a8a5f0426649a8f9ef")
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc311_stratified_tau_holdout_replication.py",
    "experiments/tpc311_independent_checker.py",
    "experiments/tpc311_stratification_stress.py",
    "results/tpc311_certificate.json", "notes/theorem_ledger.md",
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
        need(expected != "__" + label.upper().replace(" ", "_") + "_SHA256__"
             if label != "certificate" else expected != "__CERTIFICATE_SHA256__",
             label + " hash not sealed")
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
        "tpc310_code_sha256":
        "a3d47a7349d52ed94ac92d1a6c151a537d4655ab50947a0050a994318965882a",
        "tpc310_result_sha256":
        "5bb814e86e742752678d36925e5f719f0b7f998eac76b6c113913aa716f97866",
        "tpc309_code_sha256":
        "2284d9ccfcadd02eb5e82a301bdbfa85013e3e9a8352d8f3b078d020742890d9",
        "tpc309_result_sha256":
        "a4c8f7cd4aef327682b9457c21236f3756f454f4b82f5a901ab2933f1d4cad4a",
        "tpc309_profile_cases": 54,
        "tpc309_envelope_observations": 162,
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("ladders") == ["LOW", "BASE", "HIGH"] and
         protocol.get("transitions") == [[50, 60], [60, 70], [70, 90]] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("tolerances") == ["0.25", "0.5", "0.75"] and
         protocol.get("radii") == [0, 1, 2] and
         protocol.get("primary_radius") == 0, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("parent_observations") == 162 and
         audit.get("profile_pooled_strata") == 54 and
         audit.get("primary_and_control_blocks") == 6 and
         audit.get("sensitivity_blocks") == 22, "finite census")
    need(audit.get("native_calibration_class") ==
         "LEFT_COMPLETION_LOWER" and
         audit.get("native_confirmation_class") ==
         "RIGHT_COMPLETION_LOWER" and
         audit.get("native_replication") == "STRICT_CLASS_REVERSED",
         "native obstruction")
    need(audit.get("all_radii_calibration_class") ==
         "LEFT_COMPLETION_LOWER" and
         audit.get("all_radii_confirmation_class") ==
         "PREFERENCE_UNRESOLVED" and
         audit.get("all_radii_replication") ==
         "NONREPLICATED_WITH_UNRESOLVED_SLICE", "stress obstruction")
    need(audit.get("target_generation_leakage") ==
         "INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS" and
         audit.get("fresh_physical_holdout") ==
         "NONE_SAME_LOCKED_PARENT_ATLAS" and
         audit.get("formal_interval_certificate") ==
         "OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING" and
         audit.get("causal_identification") ==
         "NONE_PARAMETER_SLICE_DIAGNOSTIC_ONLY" and
         audit.get("fixed_power_credit") == 0 and
         audit.get("full_gate_b") == "OPEN" and
         audit.get("twin_prime_result") == "NONE", "claim firewall")
    need(len(payload.get("strata", [])) == 54 and
         len(payload.get("blocks", [])) == 6 and
         len(payload.get("sensitivity", [])) == 22, "atlas shape")
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
        "TPC311_MAXIMUM_CLAIM = " + STATUS,
        "TPC311_ROUTE_ADVANCE = YES_SCOPED_TAU_SLICE_HOLDOUT_OBSTRUCTION",
        "TPC311_STRATIFIED_PROTOCOL = PROVED_EXACT_FINITE",
        "TPC311_PROFILE_POOL_EXTREMA = PROVED_EXACT_FINITE",
        "TPC311_EQUAL_STRATUM_INTERVAL_MAP = PROVED_EXACT_FINITE",
        "TPC311_TAU_PARTITION = PROVED_EXACT_FINITE",
        "TPC311_STRATIFIED_ATLAS = NUMERICALLY_REPRODUCED_FINITE_54_STRATA_6_BLOCKS_22_SENSITIVITY_BLOCKS",
        "TPC311_NATIVE_TAU_REPLICATION = REFUTED_FINITE_STRICT_CALIBRATION_LEFT_CONFIRMATION_RIGHT",
        "TPC311_ALL_RADII_TAU_REPLICATION = REFUTED_FINITE_CALIBRATION_LEFT_CONFIRMATION_UNRESOLVED",
        "TPC311_PROFILE_ROBUSTNESS = REFUTED_FINITE_BASE_OMISSION_CHANGES_NATIVE_CALIBRATION_CLASS",
        "TPC311_EXPONENT_ROBUSTNESS = REFUTED_FINITE_NATIVE_CALIBRATION_EXPONENT_1_LEFT_EXPONENT_2_RIGHT",
        "TPC311_REGISTRATION_STATUS = DECLARED_CHILD_PROTOCOL_NOT_EXTERNALLY_TIMESTAMPED_PREREGISTRATION",
        "TPC311_FRESH_PHYSICAL_HOLDOUT = NONE_SAME_LOCKED_PARENT_ATLAS",
        "TPC311_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS",
        "TPC311_CAUSAL_IDENTIFICATION = NONE_PARAMETER_SLICE_DIAGNOSTIC_ONLY",
        "TPC311_FORMAL_INTERVAL_CERTIFICATE = OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
        "TPC311_EXTERNAL_WEIGHT_JUSTIFICATION = OPEN",
        "TPC311_UNIFORM_ASYMPTOTIC_BUDGET = OPEN",
        "TPC311_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC311_FIXED_POWER_CREDIT = 0",
        "TPC311_FULL_GATE_B = OPEN",
        "TPC311_TWIN_PRIME_RESULT = NONE",
        "TPC311_STATUS = " + STATUS,
        "TPC311_ROUND2_CLUE = REQUIRE_FRESH_SOURCE_HOLDOUT_AND_EXTERNALLY_JUSTIFIED_WEIGHT_LAW_BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM",
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
        print("TPC311_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC311_BRIDGE_CHECK=PASS strata=54 blocks=6 sensitivity=22 "
          "native=REVERSED all_radii=UNRESOLVED")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
