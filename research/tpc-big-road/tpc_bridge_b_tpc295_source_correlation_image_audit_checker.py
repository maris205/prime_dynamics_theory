#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-295."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-295-source-correlation-image-audit"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc295_source_correlation_image_audit.md")
PRODUCER = PROJECT / (
    "code/tpc295_source_correlation_image_certificate.py")
INDEPENDENT = PROJECT / "experiments/tpc295_independent_checker.py"
STRESS = PROJECT / "experiments/tpc295_source_image_stress.py"
CERTIFICATE = PROJECT / "results/tpc295_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_FULL_RANK_IMPLIES_SOURCE_CORRELATION_SURJECTIVITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_MODULAR_FULL_RANK_ATLAS")
SCHEMA = "TPC295_SOURCE_CORRELATION_IMAGE_CERTIFICATE_V1"
PRODUCER_SHA256 = (
    "3cdb1ea78f0fd04fd70d268997ffb1ee6842c2b523dd0c69a28adff6fab8c6c4")
CERTIFICATE_SHA256 = (
    "5e0e723aa93f221f77d5ee84cf20b0ed968adae67669d04e9d70032128212aff")

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc295_source_correlation_image_certificate.py",
    "experiments/tpc295_independent_checker.py",
    "experiments/tpc295_source_image_stress.py",
    "results/tpc295_certificate.json", "notes/theorem_ledger.md",
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
    need(audit.get("full_rank_mod_1000000007_rows") == 18 and
         audit.get("full_rank_mod_998244353_rows") == 18 and
         audit.get("source_correlation_surjective_rows") == 18 and
         audit.get("weighted_minimizer_source_realizable_rows") == 18,
         "finite image atlas")
    firewall = payload.get("firewall", {})
    need(firewall.get("TPC295_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC295_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC295_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC295_RESTRICTED_NATIVE_PROFILE") ==
         "OPEN_LITERAL_SOURCE", "claim firewall")
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
        "TPC295_MAXIMUM_CLAIM = " + STATUS,
        "TPC295_ROUTE_ADVANCE = YES_SCOPED_AMBIENT_SIGN_TARGETS_TO_UNRESTRICTED_FINITE_SOURCE_IMAGE",
        "TPC295_FULL_RANK_IMPLICATION = PROVED_EXACT_FINITE",
        "TPC295_LEAST_NORM_WITNESS_FORMULA = PROVED_EXACT_FINITE",
        "TPC295_MODULAR_FULL_RANK_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_TWO_MODULI",
        "TPC295_UNRESTRICTED_SOURCE_CORRELATION_SURJECTIVITY = NUMERICALLY_CERTIFIED_FINITE_18_OF_18",
        "TPC295_WEIGHTED_MINIMIZER_SOURCE_REALIZABILITY = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_UNRESTRICTED",
        "TPC295_NATIVE_RESTRICTED_PROFILE = OPEN_LITERAL_SOURCE",
        "TPC295_SOURCE_WITNESS_NORM = OPEN",
        "TPC295_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC295_FIXED_POWER_CREDIT = 0",
        "TPC295_FULL_GATE_B = OPEN",
        "TPC295_TWIN_PRIME_RESULT = NONE",
        "TPC295_ROUND2_CLUE = TEST_SOURCE_NORM_COST_AND_RESTRICTED_NATIVE_PROFILE_IMAGE",
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
        print("TPC295_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC295_BRIDGE_CHECK=PASS rows=18 edges=1380 mod_p1=18 "
          "mod_p2=18 surjective=18 weighted_realizable=18")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
