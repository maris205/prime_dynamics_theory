#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for TPC-278."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-278-cross-scale-gain-stability"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_cross_scale_gain_stability.md"
PRODUCER = PROJECT / "code/tpc278_cross_scale_gain_stability_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc278_independent_checker.py"
STRESS = PROJECT / "experiments/tpc278_stability_stress.py"
CERTIFICATE = PROJECT / "results/tpc278_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_GAIN_STABILITY_OBSTRUCTION"
REQUIRED = (
    "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md",
    "code/tpc278_cross_scale_gain_stability_certificate.py",
    "experiments/tpc278_independent_checker.py",
    "experiments/tpc278_stability_stress.py", "results/tpc278_certificate.json",
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
    need((PROJECT / "paper/main.pdf").read_bytes() ==
         (PROJECT / "paper/paper.pdf").read_bytes(), "PDF copies")
    pdf = (PROJECT / "paper/paper.pdf").read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 50_000, "PDF")


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    need(data["claim_status"] == STATUS, "status")
    payload = data["payload"]
    raw = (json.dumps(payload, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n").encode("ascii")
    need(data["payload_sha256"] == hashlib.sha256(raw).hexdigest(),
         "payload hash")
    need(payload["schema"] == "TPC278_CROSS_SCALE_GAIN_STABILITY_CERTIFICATE_V1",
         "schema")
    theorem = payload["finite_theorem"]
    need(theorem == {
        "natural_controls": 3, "negative_cross_rows": 8,
        "positive_cross_rows": 4, "shell_or_clock_sign_flips": 4,
        "stable_natural_gain": "r>1 on 3 controls",
        "stability_claim": "r>=1 is REFUTED_SCOPED under declared finite Q/H perturbations",
        "total_rows": 12,
    }, "theorem census")
    need(payload["firewall"]["TPC278_FIXED_POWER_CREDIT"] == 0,
         "power credit")


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
        "TPC278_MAXIMUM_CLAIM = " + STATUS,
        "TPC278_ROUTE_ADVANCE = YES_SCOPED_SIGNED_GAIN_STABILITY_OBSTRUCTION",
        "TPC278_LITERAL_SOURCE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC278_SHELL_CLOCK_FLIPS = NUMERICALLY_CERTIFIED_FINITE_4_FLIPS",
        "TPC278_SIGNED_GAIN_STABILITY = REFUTED_SCOPED_FINITE",
        "TPC278_FIXED_POWER_CREDIT = 0", "TPC278_ARITHMETIC_ADVANCE = NO",
        "TPC278_FULL_GATE_B = OPEN", "TPC278_TWIN_PRIME_RESULT = NONE",
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
        print("TPC278_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC278_BRIDGE_CHECK=PASS")
    print("rows=12 controls=3 sign_flips=4 stability=REFUTED_SCOPED")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
