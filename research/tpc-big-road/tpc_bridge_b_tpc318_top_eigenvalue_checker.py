#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-318."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-318-top-eigenvalue-prime-shell-audit"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc318_top_eigenvalue.md"
PRODUCER = PROJECT / "code/tpc318_top_eigenvalue_prime_shell_audit.py"
INDEPENDENT = PROJECT / "experiments/tpc318_independent_checker.py"
STRESS = PROJECT / "experiments/tpc318_spectral_stress.py"
CERTIFICATE = PROJECT / "results/tpc318_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

STATUS = "NUMERICALLY_CERTIFIED_FINITE_TOP_EIGENVALUE_AUDIT"
SCHEMA = "TPC318_TOP_EIGENVALUE_PRIME_SHELL_AUDIT_V1"
PARENT_SHA256 = (
    "72bb54e0d50523e44b262092f1ad9305654114f16b7db4edbfd1e25caaa9f15a")

# These hashes are sealed after all project artifacts are final.
PRODUCER_SHA256 = "e0cbbd78da12f71f053ac714ef2f81d7a180da3340adb9a64f92488a8a90e7b7"
INDEPENDENT_SHA256 = "aad1763b9fac8048ae22c03a6ad9b61914135445b7ce70036d63d4d0c910e919"
STRESS_SHA256 = "d5074fc48251d68c79a6a5a88bc8d6231bbee2e1d5dcedbb36fb4ca8fd88afd7"
CERTIFICATE_SHA256 = "2465c91d3dcc5edb24bd1cdc8d5cd0748ddfa28efa7e352c2edbffcee2229ffa"
BRIDGE_SHA256 = "f6ccd06fe8e9f28eb6725d0a64c7a1cc9998f79eb3eb4fb18b26adf978d14f70"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc318_top_eigenvalue_prime_shell_audit.py",
    "experiments/tpc318_independent_checker.py",
    "experiments/tpc318_spectral_stress.py",
    "results/tpc318_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/main.pdf",
    "paper/paper.pdf", "paper/compile.log",
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def run(script: Path, optimized: bool, flag: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script)]
    if flag:
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment,
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
        need(not expected.startswith("__"), label + " hash not sealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")

    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload", {})
    need(payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    parent = payload.get("parent_lock", {})
    need(parent.get("certificate_sha256") == PARENT_SHA256, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("source_scales") == [640, 1280, 2560] and
         protocol.get("height") == 66 and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("domain") == "ell^2(I_X)" and
         protocol.get("codomain") == "ell^2(S_Q x I_X)", "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("scales") == 3 and audit.get("rows") == 24 and
         audit.get("top_eigenvalue_rows") == 24 and
         audit.get("top_decrease_strict") == 16 and
         audit.get("dual_solver_rows") == 24 and
         audit.get("residual_rows") == 24 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("growing_top_eigenvalue_theorem") == "OPEN", "audit")
    for row in payload.get("rows", []):
        guard = row.get("top_eigenvalue", {}).get("guard", {})
        need(guard.get("uniform_entry_bound") == "160" and
             guard.get("model") ==
             "binary64 dual solver plus finite Weyl guard", "guard")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC318_TOP_EIGENVALUE_AUDIT") ==
         "NUMERICALLY_CERTIFIED_FINITE_24_OF_24" and
         firewall.get("TPC318_TOP_EIGENVALUE_DECREASE") ==
         "NUMERICALLY_CERTIFIED_FINITE_16_OF_16" and
         firewall.get("TPC318_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC318_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC318_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC318_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error"):
        need(bad not in log, "LaTeX warning: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC318_MAXIMUM_CLAIM = " + STATUS,
        "TPC318_ROUTE_ADVANCE = YES_SCOPED_TOP_EIGENVALUE_READOUT",
        "TPC318_TOP_EIGENVALUE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
        "TPC318_TOP_EIGENVALUE_DECREASE = NUMERICALLY_CERTIFIED_FINITE_16_OF_16",
        "TPC318_DUAL_SOLVER_AGREEMENT = NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
        "TPC318_RESIDUAL_AUDIT = NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
        "TPC318_NEAR_DEGENERACY = NUMERICALLY_CERTIFIED_FINITE_CENSUS",
        "TPC318_NORMALIZED_TREND = NUMERICAL_OBSERVATION_FINITE_ONLY",
        "TPC318_UNNORMALIZED_POWER = OPEN",
        "TPC318_CLUSTERED_EIGENSPACE = OPEN",
        "TPC318_ARITHMETIC_CANCELLATION = OPEN",
        "TPC318_ARITHMETIC_ADVANCE = NO",
        "TPC318_FIXED_POWER_CREDIT = 0",
        "TPC318_FULL_GATE_B = OPEN",
        "TPC318_TWIN_PRIME_RESULT = NONE",
        "TPC318_ROUND2_CLUE = "
        "AUDIT_THE_TOP_EIGENSPACE_CLUSTER_AND_NORMALIZATION_LAW_BEFORE_"
        "ANY_ARITHMETIC_CANCELLATION_PROMOTION",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge_text()
        for script, flag in ((PRODUCER, True),
                             (INDEPENDENT, True),
                             (STRESS, False)):
            normal = run(script, False, flag)
            optimized = run(script, True, flag)
            need(normal == optimized, script.name + " optimized mismatch")
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print("TPC318_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC318_BRIDGE_CHECK=PASS scales=3 rows=24 "
          "top_decreases=16 near_degenerate=10 fixed_power_credit=0")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
