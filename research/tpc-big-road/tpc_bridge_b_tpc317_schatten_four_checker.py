#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-317."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-317-schatten-four-prime-shell-compression"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc317_schatten_four_checker.md"
PRODUCER = PROJECT / "code/tpc317_schatten_four_prime_shell_compression.py"
INDEPENDENT = PROJECT / "experiments/tpc317_independent_checker.py"
STRESS = PROJECT / "experiments/tpc317_spectral_stress.py"
CERTIFICATE = PROJECT / "results/tpc317_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

STATUS = (
    "NUMERICALLY_CERTIFIED_FINITE_SCHATTEN4_COMPRESSION_AND_"
    "OPERATOR_ENVELOPE")
SCHEMA = "TPC317_SCHATTEN4_PRIME_SHELL_COMPRESSION_V1"

# Sealed after all release artifacts and dynamic documentation are final.
PRODUCER_SHA256 = "45af83d3661dbbf1154839d335740f3f5698d28299555793f0d62d94b29656dd"
INDEPENDENT_SHA256 = "e3b8db6d6aaadb147a5f6b863ba0c9db9f97611e3b07ab095531d05241781ad8"
STRESS_SHA256 = "293fb8e325f7241b0c36d88cb87677fc44334a0940ff1b197a0deed9206be6c1"
CERTIFICATE_SHA256 = "e0096b03630ca09a52369ba4fc5c6e4321ee919f8bb415c6d9c12cc0e22d6e7c"
BRIDGE_SHA256 = "ef3147d834af318d833818c56d79ead23c8b1af134aaac41c847e15c08da3b2b"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc317_schatten_four_prime_shell_compression.py",
    "experiments/tpc317_independent_checker.py",
    "experiments/tpc317_spectral_stress.py",
    "results/tpc317_certificate.json", "notes/theorem_ledger.md",
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
    need(parent.get("certificate_sha256") ==
         "3bb9f3463daf7583ca07a672bf19be827af5404c2c7005b6e6bf6b766bd8ef26",
         "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("source_scales") == [640, 1280, 2560] and
         protocol.get("height") == 66 and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("domain") == "ell^2(I_X)" and
         protocol.get("codomain") == "ell^2(S_Q x I_X)", "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("scales") == 3 and audit.get("rows") == 24 and
         audit.get("schatten4_strict_decreases") == 16 and
         audit.get("frobenius_strict_increases") == 16 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("growing_operator_theorem") == "OPEN", "finite audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC317_SCHATTEN4_IDENTITY") ==
         "PROVED_EXACT_FINITE" and
         firewall.get("TPC317_SCHATTEN4_DECREASE") ==
         "NUMERICALLY_CERTIFIED_FINITE_16_OF_16" and
         firewall.get("TPC317_FROBENIUS_INCREASE") ==
         "NUMERICALLY_CERTIFIED_FINITE_16_OF_16" and
         firewall.get("TPC317_TRUE_OPERATOR_NORM") == "OPEN" and
         firewall.get("TPC317_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC317_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC317_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC317_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "main and paper PDF differ")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error"):
        need(bad not in log, "LaTeX warning: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC317_MAXIMUM_CLAIM = " + STATUS,
        "TPC317_ROUTE_ADVANCE = YES_SCOPED_TRACE_POWER_ENVELOPE",
        "TPC317_SCHATTEN4_IDENTITY = PROVED_EXACT_FINITE",
        "TPC317_FINITE_L2_ENVELOPE = PROVED_EXACT_FINITE",
        "TPC317_SMALL_RATIONAL_TRACE_AUDIT = PROVED_EXACT_FINITE",
        "TPC317_DUAL_PRECISION_ROWS = NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
        "TPC317_SCHATTEN4_DECREASE = NUMERICALLY_CERTIFIED_FINITE_16_OF_16",
        "TPC317_FROBENIUS_INCREASE = NUMERICALLY_CERTIFIED_FINITE_16_OF_16",
        "TPC317_FROBENIUS_PROXY = REFUTED_SCOPED_AS_A_SHARP_SPECTRAL_PROXY",
        "TPC317_TRUE_OPERATOR_NORM = OPEN",
        "TPC317_ARITHMETIC_CANCELLATION = OPEN",
        "TPC317_FIXED_POWER_CREDIT = 0",
        "TPC317_ARITHMETIC_ADVANCE = NO",
        "TPC317_FULL_GATE_B = OPEN",
        "TPC317_TWIN_PRIME_RESULT = NONE",
        "TPC317_ROUND2_CLUE = "
        "AUDIT_THE_TRUE_TOP_EIGENVALUE_OR_A_CERTIFIED_TRACE_POWER_LADDER_"
        "BEFORE_ANY_ARITHMETIC_CANCELLATION_PROMOTION",
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
        print("TPC317_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC317_BRIDGE_CHECK=PASS scales=3 rows=24 "
          "schatten_decreases=16 frobenius_increases=16 "
          "fixed_power_credit=0")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
