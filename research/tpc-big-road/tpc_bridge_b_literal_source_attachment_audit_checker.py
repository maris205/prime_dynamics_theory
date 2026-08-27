#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for the TPC-282 release."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-282-literal-source-attachment-audit"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_literal_source_attachment_audit.md"
PRODUCER = PROJECT / "code/tpc282_literal_source_attachment_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc282_independent_checker.py"
STRESS = PROJECT / "experiments/tpc282_attachment_stress.py"
CERTIFICATE = PROJECT / "results/tpc282_certificate.json"
STATUS = (
    "NUMERICALLY_CERTIFIED_FINITE_LITERAL_SOURCE_ATTACHMENT_LOCK_PLUS_"
    "ASYMPTOTIC_NONDEGENERACY_OPEN")
SCHEMA = "TPC282_LITERAL_SOURCE_ATTACHMENT_CERTIFICATE_V1"
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc282_literal_source_attachment_certificate.py",
    "experiments/tpc282_independent_checker.py",
    "experiments/tpc282_attachment_stress.py", "results/tpc282_certificate.json",
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
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script), "--check"] if script == PRODUCER
                   else ["-B", str(script)])
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name + " " +
         result.stderr.decode("utf-8", "replace"))
    return result.stdout


def check_files() -> None:
    need(BRIDGE.is_file(), "bridge missing")
    bridge = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC282_MAXIMUM_CLAIM = " + STATUS,
        "TPC282_ROUTE_ADVANCE = YES_SCOPED_FINITE_SOURCE_ATTACHMENT_AUDIT",
        "TPC282_SOURCE_ATTACHMENT = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC282_SOURCE_SIGN = 11_NEGATIVE_1_POSITIVE_FINITE",
        "TPC282_UNIFORM_ASYMPTOTIC_NONDEGENERACY = OPEN",
        "TPC282_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC282_FIXED_POWER_CREDIT = 0", "TPC282_FULL_GATE_B = OPEN",
        "TPC282_TWIN_PRIME_RESULT = NONE",
        "TPC282_ROUND2_CLUE = QUANTIFY_SOURCE_ATTACHMENT_STABILITY_RADIUS_AND_SIGN_FLIPS",
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
    need(data["payload_sha256"] == digest(canonical(payload)),
         "payload hash")
    finite = payload["finite_theorem"]
    need(finite["negative_rows"] == 11 and finite["positive_rows"] == 1 and
         finite["zero_crossing_rows"] == 0 and
         finite["fixed_power_credit"] == 0, "finite census")
    need(len(payload["rows"]) == 12, "row count")
    weakest = payload["weakest_rows"]["smallest_attachment_cosine_squared"]
    need((weakest["scale"], weakest["H"], weakest["Q"],
          weakest["kernel_exponent"]) == (256, 38, 6, 2), "weakest row")


def check_subchecks() -> None:
    outputs: dict[str, bytes] = {}
    for script in (PRODUCER, INDEPENDENT, STRESS):
        normal = run(script, False)
        optimized = run(script, True)
        need(normal == optimized, script.name + " stdout mismatch")
        outputs[script.name] = normal
    need(b"TPC282_CERTIFICATE=PASS" in outputs[PRODUCER.name],
         "producer output")
    need(b"TPC282_INDEPENDENT_CHECK=PASS" in outputs[INDEPENDENT.name],
         "independent output")
    need(b"TPC282_STRESS=PASS" in outputs[STRESS.name], "stress output")


def main() -> int:
    try:
        check_files(); check_certificate(); check_subchecks()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC282_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC282_BRIDGE_CHECK=PASS")
    print("theorem=FINITE_LITERAL_SOURCE_ATTACHMENT_LOCK rows=12 "
          "negative=11 positive=1 weakest_rho_squared=3.357e-05 "
          "fixed_power_credit=0")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
