#!/usr/bin/env python3
"""Fail-closed Bridge-B release checker for TPC-292."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-292-three-prime-sign-frustration-atlas"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_three_prime_sign_frustration_atlas.md"
PRODUCER = PROJECT / "code/tpc292_three_prime_sign_frustration_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc292_independent_checker.py"
STRESS = PROJECT / "experiments/tpc292_frustration_stress.py"
CERTIFICATE = PROJECT / "results/tpc292_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_TRIANGLE_SIGN_PARITY_AND_THREE_VECTOR_SCHUR_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_SIGN_FRUSTRATION_ATLAS")
SCHEMA = "TPC292_THREE_PRIME_SIGN_FRUSTRATION_CERTIFICATE_V1"
CERTIFICATE_SHA256 = "47c45d227fc6654a2e8dba9472630f2876ce88b387de79faf487178bf3e82ab8"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc292_three_prime_sign_frustration_certificate.py",
    "experiments/tpc292_independent_checker.py",
    "experiments/tpc292_frustration_stress.py", "results/tpc292_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex", "paper/references.bib",
    "paper/paper.pdf")


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


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    need(digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA, "certificate schema")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("total_triples") == 5727 and
         audit.get("positive_volume_triples") == 5727 and
         audit.get("zero_volume_triples") == 0 and
         audit.get("negative_volume_triples") == 0 and
         audit.get("zero_edge_triples") == 0 and
         audit.get("anti_alignable_triples") == 9 and
         audit.get("sign_frustrated_triples") == 5718,
         "triangle census")
    need(audit.get("edge_sign_pattern_totals") ==
         {"+++": 5715, "++-": 1, "+-+": 8, "+--": 3},
         "edge pattern census")
    need(audit.get("minimum_target_residual_totals") ==
         {"1/2": 5313, "1/4": 4413, "1/10": 3620},
         "residual census")
    need(payload.get("firewall", {}).get("TPC292_FULL_GATE_B") == "OPEN" and
         payload["firewall"].get("TPC292_FIXED_POWER_CREDIT") == 0 and
         payload["firewall"].get("TPC292_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC292_MAXIMUM_CLAIM = " + STATUS,
        "TPC292_ROUTE_ADVANCE = YES_SCOPED_PAIRWISE_TO_THREE_PRIME_COMPATIBILITY_OBSTRUCTION",
        "TPC292_TRIANGLE_SIGN_PARITY = PROVED_EXACT_CONDITIONAL",
        "TPC292_THREE_VECTOR_SCHUR_IDENTITY = PROVED_EXACT_FINITE",
        "TPC292_TRIANGLE_ATLAS = NUMERICALLY_CERTIFIED_FINITE_5727_TRIPLES",
        "TPC292_SIGN_FRUSTRATION = NUMERICALLY_CERTIFIED_FINITE_5718_OF_5727",
        "TPC292_ANTI_ALIGNABLE = NUMERICALLY_CERTIFIED_FINITE_9_OF_5727",
        "TPC292_GROWING_TRIANGLE_COMPATIBILITY = OPEN",
        "TPC292_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE",
        "TPC292_FIXED_POWER_CREDIT = 0",
        "TPC292_FULL_GATE_B = OPEN",
        "TPC292_TWIN_PRIME_RESULT = NONE",
        "TPC292_ROUND2_CLUE = TEST_SIGNED_GRAPH_MAXCUT_AND_MULTI_PRIME_RAYLEIGH_COMPATIBILITY",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def check_files() -> None:
    for item in REQUIRED:
        need((PROJECT / item).is_file(), "missing artifact: " + item)
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    need(LOG.is_file(), "LaTeX log")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("undefined", "LaTeX Warning:", "Package rerunfilecheck Warning:",
                "Overfull \\hbox", "Underfull \\hbox"):
        need(bad not in log, "LaTeX warning: " + bad)


def main() -> int:
    try:
        check_files()
        check_bridge()
        check_certificate()
        outputs = {}
        for script in (PRODUCER, INDEPENDENT, STRESS):
            normal = run(script, False)
            optimized = run(script, True)
            need(normal == optimized, script.name + " optimized mismatch")
            outputs[script.name] = normal
    except (Failure, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        print("TPC292_BRIDGE_CHECK=FAIL " + str(exc), file=sys.stderr)
        return 1
    print("TPC292_BRIDGE_CHECK=PASS rows=18 triples=5727 frustrated=5718 "
          "anti_alignable=9 residual_le_half=5313 residual_le_quarter=4413 "
          "residual_le_tenth=3620")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
