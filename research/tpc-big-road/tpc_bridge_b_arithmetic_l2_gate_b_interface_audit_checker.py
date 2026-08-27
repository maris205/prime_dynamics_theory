#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for the TPC-281 release."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-281-arithmetic-l2-gate-b-interface-audit"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_arithmetic_l2_gate_b_interface_audit.md"
PRODUCER = PROJECT / "code/tpc281_arithmetic_l2_interface_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc281_independent_checker.py"
STRESS = PROJECT / "experiments/tpc281_attachment_stress.py"
CERTIFICATE = PROJECT / "results/tpc281_certificate.json"
STATUS = (
    "PROVED_EXACT_TYPED_ARITHMETIC_L2_INTERFACE_FIREWALL_PLUS_"
    "NUMERICALLY_CERTIFIED_ATTACHMENT_AUDIT"
)
SCHEMA = "TPC281_ARITHMETIC_L2_GATE_B_INTERFACE_CERTIFICATE_V1"
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc281_arithmetic_l2_interface_certificate.py",
    "experiments/tpc281_independent_checker.py",
    "experiments/tpc281_attachment_stress.py", "results/tpc281_certificate.json",
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


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script), "--check"] if script == PRODUCER
                   else ["-B", str(script)])
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         f"subcheck failed: {script.name}: " +
         result.stderr.decode("utf-8", "replace"))
    return result.stdout


def check_files() -> None:
    need(BRIDGE.is_file(), "bridge missing")
    bridge = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC281_MAXIMUM_CLAIM = " + STATUS,
        "TPC281_ROUTE_ADVANCE = YES_SCOPED_TYPED_ARITHMETIC_L2_GATE_B_INTERFACE_AUDIT",
        "TPC281_TYPED_ARITHMETIC_L2 = PROVED_CONDITIONAL_INTERFACE_ONLY",
        "TPC281_ATTACHMENT_IDENTIFIABILITY = REFUTED_EXACT_BY_ORTHOGONAL_FUNCTIONAL",
        "TPC281_FINITE_ATTACHMENT_AUDIT = NUMERICALLY_CERTIFIED_FINITE_4_PACKET_FIXTURES",
        "TPC281_FINITE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC281_ARITHMETIC_ADVANCE = NO", "TPC281_L2 = OPEN_LITERAL_SOURCE",
        "TPC281_FIXED_POWER_CREDIT = 0", "TPC281_FULL_GATE_B = OPEN",
        "TPC281_TWIN_PRIME_RESULT = NONE", "TPC281_ROUND2_CLUE = "
        "REQUIRE_LITERAL_SOURCE_ARITHMETIC_L2_AND_TYPED_ATTACHMENT_NONDEGENERACY",
    )
    for marker in markers:
        need(marker in bridge, "bridge marker: " + marker)
    for relative in REQUIRED:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
    need("Liang Wang" in (PROJECT / "README.md").read_text(encoding="utf-8"),
         "author")
    pdf = (PROJECT / "paper/paper.pdf").read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 50_000, "PDF")
    main_pdf = PROJECT / "paper/main.pdf"
    if main_pdf.is_file():
        need(main_pdf.read_bytes() == pdf, "PDF copies")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "noncanonical certificate")
    need(data["certificate_version"] == 1 and data["claim_status"] == STATUS,
         "certificate status")
    payload = data["payload"]
    need(payload["schema"] == SCHEMA, "schema")
    need(data["payload_sha256"] == hashlib.sha256(canonical(payload)).hexdigest(),
         "payload hash")
    need(len(payload["packets"]) == 4 and len(payload["interface_cases"]) == 4,
         "fixture count")
    transfer = payload["finite_transfer"]
    need(transfer["total_rows"] == 12 and
         transfer["positive_deficit_rows"] == 8 and
         transfer["negative_deficit_rows"] == 4 and
         transfer["fixed_power_credit"] == 0, "transfer census")
    exact = payload["exact_theorem"]
    need(exact["typed_two_term_L2"] ==
         "||A_X S||_2^2<=K^2 X^(-2sigma) Q_X D" and
         exact["typed_collapsed_L2"] ==
         "||A_X S||_2^2<=(K^2 d_+ (B+ell/d)) X^(a-2sigma-kappa)",
         "theorem marker")


def check_subchecks() -> None:
    outputs = {}
    for script in (PRODUCER, INDEPENDENT, STRESS):
        normal = run(script, False)
        optimized = run(script, True)
        need(normal == optimized, script.name + " stdout mismatch")
        outputs[script.name] = normal
    need(b"TPC281_CERTIFICATE=PASS" in outputs[PRODUCER.name], "producer output")
    need(b"TPC281_INDEPENDENT_CHECK=PASS" in outputs[INDEPENDENT.name],
         "independent output")
    need(b"TPC281_STRESS=PASS" in outputs[STRESS.name], "stress output")


def main() -> int:
    try:
        check_files(); check_certificate(); check_subchecks()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC281_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC281_BRIDGE_CHECK=PASS")
    print("theorem=TYPED_L2_INTERFACE attachment=EXACT_NONIDENTIFIABILITY "
          "packet_fixtures=4 interface_cases=4 transfer_rows=12 "
          "fixed_power_credit=0")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
