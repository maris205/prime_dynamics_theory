#!/usr/bin/env python3
"""Fail-closed Bridge-B release checker for TPC-280."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-280-leakage-aware-endpoint-compiler"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_leakage_aware_endpoint_compiler.md"
PRODUCER = PROJECT / "code/tpc280_leakage_aware_endpoint_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc280_independent_checker.py"
STRESS = PROJECT / "experiments/tpc280_leakage_stress.py"
CERTIFICATE = PROJECT / "results/tpc280_certificate.json"
STATUS = (
    "PROVED_CONDITIONAL_TWO_TERM_LEAKAGE_ENDPOINT_COMPILER_PLUS_"
    "NUMERICALLY_CERTIFIED_TRANSFER"
)
REQUIRED = (
    "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md",
    "code/tpc280_leakage_aware_endpoint_certificate.py",
    "experiments/tpc280_independent_checker.py",
    "experiments/tpc280_leakage_stress.py",
    "results/tpc280_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/paper.pdf",
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
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         f"subcheck failed: {script.name}: " +
         result.stderr.decode("utf-8", "replace"))
    return result.stdout


def check_files() -> None:
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
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    need(data["claim_status"] == STATUS, "status")
    payload = data["payload"]
    need(data["payload_sha256"] == hashlib.sha256(canonical(payload)).hexdigest(),
         "payload hash")
    need(payload["schema"] ==
         "TPC280_LEAKAGE_AWARE_ENDPOINT_COMPILER_CERTIFICATE_V1", "schema")
    need(len(payload["budget_cases"]) == 6 and
         len(payload["margin_cases"]) == 4 and
         len(payload["endpoint_cases"]) == 4, "fixture counts")
    transfer = payload["finite_transfer"]
    need(transfer["total_rows"] == 12 and
         transfer["positive_deficit_rows"] == 8 and
         transfer["negative_deficit_rows"] == 4 and
         transfer["fixed_power_credit"] == 0, "transfer census")
    need(payload["exact_theorem"]["leakage_obstruction"] ==
         "delta<gamma makes additive leakage the asymptotic bottleneck",
         "leakage theorem")


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
        "TPC280_MAXIMUM_CLAIM = " + STATUS,
        "TPC280_ROUTE_ADVANCE = YES_SCOPED_ADDITIVE_LEAKAGE_ENDPOINT_COMPILER",
        "TPC280_TWO_TERM_COMPILER = PROVED_CONDITIONAL",
        "TPC280_DOMINANT_EXPONENT = PROVED_KAPPA_EQUALS_MIN_GAMMA_DELTA",
        "TPC280_LEAKAGE_BOTTLENECK = PROVED_CONDITIONAL_DELTA_LT_GAMMA",
        "TPC280_FINITE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC280_FIXED_POWER_CREDIT = 0", "TPC280_ARITHMETIC_ADVANCE = NO",
        "TPC280_L2 = NONE", "TPC280_FULL_GATE_B = OPEN",
        "TPC280_TWIN_PRIME_RESULT = NONE",
    ):
        need(marker in text, "bridge marker: " + marker)


def main() -> int:
    try:
        check_files(); check_certificate(); check_bridge()
        for script in (PRODUCER, INDEPENDENT, STRESS):
            normal = run(script, False)
            optimized = run(script, True)
            need(normal == optimized, script.name + " stdout mismatch")
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC280_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC280_BRIDGE_CHECK=PASS")
    print("theorem=TWO_TERM_LEAKAGE kappa=MIN_GAMMA_DELTA "
          "transfer_rows=12 fixed_power_credit=0")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
