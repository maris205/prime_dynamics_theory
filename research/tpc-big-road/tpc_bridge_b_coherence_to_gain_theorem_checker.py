#!/usr/bin/env python3
"""Fail-closed Bridge-B release checker for TPC-279."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-279-coherence-to-gain-theorem"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_coherence_to_gain_theorem.md"
PRODUCER = PROJECT / "code/tpc279_coherence_to_gain_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc279_independent_checker.py"
STRESS = PROJECT / "experiments/tpc279_coherence_stress.py"
CERTIFICATE = PROJECT / "results/tpc279_certificate.json"
STATUS = "PROVED_EXACT_MINIMAL_COHERENCE_TO_GAIN_CRITERION_PLUS_NUMERICALLY_CERTIFIED_TRANSFER"
REQUIRED = (
    "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md",
    "code/tpc279_coherence_to_gain_certificate.py",
    "experiments/tpc279_independent_checker.py",
    "experiments/tpc279_coherence_stress.py",
    "results/tpc279_certificate.json", "notes/theorem_ledger.md",
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
    need(payload["schema"] == "TPC279_COHERENCE_TO_GAIN_THEOREM_CERTIFICATE_V1",
         "schema")
    need(payload["finite_transfer"]["total_rows"] == 12 and
         payload["finite_transfer"]["positive_deficit_rows"] == 8 and
         payload["finite_transfer"]["negative_deficit_rows"] == 4 and
         payload["finite_transfer"]["fixed_power_credit"] == 0,
         "transfer census")
    need(payload["exact_theorem"]["pairwise_coherence_envelope"] ==
         "G/D<=min(4,1+3*mu)", "coherence theorem")


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
        "TPC279_MAXIMUM_CLAIM = " + STATUS,
        "TPC279_ROUTE_ADVANCE = YES_SCOPED_EXACT_COHERENCE_TO_GAIN_CRITERION",
        "TPC279_PAIRWISE_COHERENCE_POWER = REFUTED_EXACT_BY_ORTHOGONAL_WITNESS",
        "TPC279_FINITE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC279_SOURCE_LEVEL_DEFICIT = OPEN_ASYMPTOTIC",
        "TPC279_FIXED_POWER_CREDIT = 0", "TPC279_ARITHMETIC_ADVANCE = NO",
        "TPC279_FULL_GATE_B = OPEN", "TPC279_TWIN_PRIME_RESULT = NONE",
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
        print("TPC279_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC279_BRIDGE_CHECK=PASS")
    print("theorem=EXACT_MINIMAL_DEFICIT pairwise_envelope=SHARP "
          "transfer_rows=12 fixed_power_credit=0")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
