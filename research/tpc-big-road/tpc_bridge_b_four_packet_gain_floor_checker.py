#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for the TPC-277 release."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-277-four-packet-gain-floor"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_four_packet_gain_floor.md"
PRODUCER = PROJECT / "code/tpc277_four_packet_gain_floor_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc277_independent_checker.py"
STRESS = PROJECT / "experiments/tpc277_gain_stress.py"
CERTIFICATE = PROJECT / "results/tpc277_certificate.json"
STATUS = "PROVED_EXACT_UNIVERSAL_FOUR_PACKET_GAIN_FLOOR_PLUS_NUMERICALLY_CERTIFIED_SOURCE_SCAN"
REQUIRED = (
    "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md",
    "code/tpc277_four_packet_gain_floor_certificate.py",
    "experiments/tpc277_independent_checker.py",
    "experiments/tpc277_gain_stress.py", "results/tpc277_certificate.json",
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


def run(script: Path, optimized: bool, args: list[str]) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script), *args])
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         f"subcheck failed: {script.name} opt={optimized}: "
         + result.stderr.decode("utf-8", "replace"))
    return result.stdout


def check_files() -> None:
    for relative in REQUIRED:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
    need("Liang Wang" in (PROJECT / "README.md").read_text(encoding="utf-8"),
         "author")
    need((PROJECT / "paper/main.pdf").read_bytes() ==
         (PROJECT / "paper/paper.pdf").read_bytes(), "PDF copies")
    pdf = (PROJECT / "paper/paper.pdf").read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 50_000, "PDF")


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    need(data["claim_status"] == STATUS, "status")
    payload = data["payload"]
    canonical = (json.dumps(payload, ensure_ascii=True, sort_keys=True,
                             separators=(",", ":")) + "\n").encode("ascii")
    need(data["payload_sha256"] == hashlib.sha256(canonical).hexdigest(),
         "payload hash")
    need(payload["schema"] == "TPC277_FOUR_PACKET_GAIN_FLOOR_CERTIFICATE_V1",
         "schema")
    need(payload["universal_theorem"]["sharp_general_floor"] == "1/4" and
         payload["universal_theorem"]["sharp_signed_floor"] == "1",
         "universal theorem")
    theorem = payload["finite_theorem"]
    need(theorem["total_rows"] == 8 and theorem["gain_above_one_rows"] == 8 and
         theorem["negative_cross_rows"] == 8 and
         theorem["one_percent_below_rows"] == 1, "finite counts")
    need(payload["firewall"]["TPC277_FIXED_POWER_CREDIT"] == 0,
         "power credit")


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
        "TPC277_MAXIMUM_CLAIM = " + STATUS,
        "TPC277_ROUTE_ADVANCE = YES_SCOPED_SOURCE_GAIN_FLOOR_AND_FINITE_ATTACK",
        "TPC277_UNIVERSAL_FOUR_PACKET_FLOOR = PROVED_EXACT_R>=1_OVER_4",
        "TPC277_GEOMETRIC_POWER_PROMOTION = REFUTED_EXACT_BY_ORTHOGONAL_ADVERSARY",
        "TPC277_SOURCE_SCAN = NUMERICALLY_CERTIFIED_FINITE_ALL_8_ROWS",
        "TPC277_ONE_PERCENT_FLOOR = REFUTED_SCOPED_FINITE",
        "TPC277_FIXED_POWER_CREDIT = 0", "TPC277_ARITHMETIC_ADVANCE = NO",
        "TPC277_L2 = NONE", "TPC277_FULL_GATE_B = OPEN",
        "TPC277_TWIN_PRIME_RESULT = NONE",
    ):
        need(marker in text, "bridge marker: " + marker)


def main() -> int:
    try:
        check_files(); check_certificate(); check_bridge()
        producer = [run(PRODUCER, opt, ["--check"]) for opt in (False, True)]
        independent = [run(INDEPENDENT, opt, []) for opt in (False, True)]
        stress = [run(STRESS, opt, []) for opt in (False, True)]
        need(producer[0] == producer[1], "producer stdout mismatch")
        need(independent[0] == independent[1], "independent stdout mismatch")
        need(stress[0] == stress[1], "stress stdout mismatch")
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC277_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC277_BRIDGE_CHECK=PASS")
    print("rows=8 universal_floor=1/4 one_percent_floor=REFUTED_SCOPED")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
