#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for TPC-289."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-289-cross-prime-gram-coherence"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_cross_prime_gram_coherence.md"
PRODUCER = PROJECT / "code/tpc289_cross_prime_gram_coherence_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc289_independent_checker.py"
STRESS = PROJECT / "experiments/tpc289_coherence_stress.py"
CERTIFICATE = PROJECT / "results/tpc289_certificate.json"
STATUS = (
    "PROVED_EXACT_NORMALIZED_GRAM_COHERENCE_ACCUMULATION_BOUND_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_SIGN_PHASE_DIAGRAM")
SCHEMA = "TPC289_CROSS_PRIME_GRAM_COHERENCE_CERTIFICATE_V1"
CERTIFICATE_SHA256 = (
    "9f0a2db34195fe93c8acb461bb7e0caa615a4a781f948732ad9572344c6efb1e")
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc289_cross_prime_gram_coherence_certificate.py",
    "experiments/tpc289_independent_checker.py",
    "experiments/tpc289_coherence_stress.py", "results/tpc289_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex",
    "paper/references.bib", "paper/paper.pdf",
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
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script)]
    if script == PRODUCER:
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check() -> None:
    bridge = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC289_MAXIMUM_CLAIM = " + STATUS,
        "TPC289_ROUTE_ADVANCE = YES_SCOPED_EXACT_COHERENCE_ENVELOPE_AND_FINITE_SIGN_PHASE_DIAGRAM",
        "TPC289_EXACT_GRAM_COHERENCE = PROVED_EXACT_FINITE",
        "TPC289_EXACT_ACCUMULATION_BOUND = PROVED_EXACT_CONDITIONAL",
        "TPC289_PAIRWISE_POSITIVITY = NUMERICALLY_CERTIFIED_FINITE_17_OF_18_ROWS",
        "TPC289_SIGN_FLIP_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_3_PAIRS_ONE_ROW",
        "TPC289_STRONG_COHERENCE_BLOCK = NUMERICALLY_CERTIFIED_FINITE_8_ROWS",
        "TPC289_ENERGY_AMPLIFIED = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ROWS",
        "TPC289_TOTAL_PAIR_COMPARISONS = 1380",
        "TPC289_CONTROL_EQUIVALENCE_GROUPS = 2",
        "TPC289_UNIFORM_PAIRWISE_POSITIVITY = REFUTED_FINITE_DECLARED_GRID",
        "TPC289_GROWING_COHERENCE_STABILITY = OPEN",
        "TPC289_SOURCE_CONTROL_UNIFORMITY = OPEN",
        "TPC289_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE",
        "TPC289_FIXED_POWER_CREDIT = 0",
        "TPC289_FULL_GATE_B = OPEN", "TPC289_TWIN_PRIME_RESULT = NONE",
        "TPC289_ROUND2_CLUE = TEST_ADAPTIVE_SHELL_WEIGHTING_OR_SOURCE_RESTRICTED_COHERENCE_BEYOND_FINITE_BLOCK",
    )
    for marker in markers:
        need(marker in bridge, "bridge marker")
    for item in REQUIRED:
        need((PROJECT / item).is_file(), "missing artifact: " + item)

    raw = CERTIFICATE.read_bytes()
    need(digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS and
         data.get("payload", {}).get("schema") == SCHEMA,
         "certificate header")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")
    audit = data["payload"]["finite_audit"]
    need(audit == {
        "control_cutoff_equivalence_groups": 2,
        "energy_amplified_rows": 18,
        "exponent_crossover_rows": 4,
        "fixed_power_credit": 0,
        "growing_coherence_theorem": "OPEN",
        "growth_s2_rows": 8,
        "pairwise_negative_pairs": 3,
        "pairwise_negative_rows": 1,
        "pairwise_positive_rows": 17,
        "pairwise_zero_pairs": 0,
        "rows": 18,
        "source_control_rows": 6,
        "source_native_L2": "OPEN",
        "strong_coherence_block_rows": 8,
        "total_pairs": 1380,
        "uniform_coherence_floor": "REFUTED_FINITE",
        "uniform_pairwise_positivity": "REFUTED_FINITE",
    }, "finite audit")
    need(len(data["payload"]["rows"]) == 18, "row census")
    exceptional = data["payload"]["rows"][8]
    need(exceptional["pair_negative"] == 3 and
         exceptional["minimum_coherence_pair"]["prime_pair"] == [31, 53],
         "exceptional row")
    need(sum(row["strong_coherence_block"]
             for row in data["payload"]["rows"]) == 8,
         "strong block")
    pdf = (PROJECT / "paper/paper.pdf").read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 50_000, "PDF")
    log = (PROJECT / "paper/main.log").read_text(encoding="utf-8")
    need("undefined" not in log.lower() and "LaTeX Warning:" not in log and
         "Package rerunfilecheck Warning:" not in log and
         "Overfull \\hbox" not in log and "Underfull \\hbox" not in log,
         "LaTeX warning or undefined reference")

    for script in (PRODUCER, INDEPENDENT, STRESS):
        normal = run(script, False)
        optimized = run(script, True)
        need(normal == optimized, script.name + " optimized mismatch")
    print("TPC289_BRIDGE_CHECK=PASS rows=18 positive_rows=17 "
          "negative_pairs=3 strong_block=8 amplified=18 pairs=1380")
    print("claim_level=" + STATUS)


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC289_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
