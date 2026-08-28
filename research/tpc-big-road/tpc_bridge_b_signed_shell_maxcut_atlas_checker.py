#!/usr/bin/env python3
"""Fail-closed Bridge-B release checker for TPC-293."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-293-signed-shell-maxcut-atlas"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_signed_shell_maxcut_atlas.md"
PRODUCER = PROJECT / "code/tpc293_signed_shell_maxcut_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc293_independent_checker.py"
STRESS = PROJECT / "experiments/tpc293_signed_graph_stress.py"
CERTIFICATE = PROJECT / "results/tpc293_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/main.log"
STATUS = (
    "PROVED_EXACT_ALL_POSITIVE_MAXCUT_PLUS_NUMERICALLY_CERTIFIED_FINITE_"
    "SIGNED_SHELL_FRUSTRATION_ATLAS")
SCHEMA = "TPC293_SIGNED_SHELL_MAXCUT_CERTIFICATE_V1"
PRODUCER_SHA256 = (
    "2fdaa5e1bce7a70e520ab4fe89b93b3e43383423a0277d82bc5a8689f2764d71")
CERTIFICATE_SHA256 = (
    "14dae97ac94398612af49860b364e2fac8d112ea288fb95114d974eacd2d07b2")

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc293_signed_shell_maxcut_certificate.py",
    "experiments/tpc293_independent_checker.py",
    "experiments/tpc293_signed_graph_stress.py",
    "results/tpc293_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/paper.pdf")


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


def check_files() -> None:
    for item in REQUIRED:
        need((PROJECT / item).is_file(), "missing artifact: " + item)
    need(digest(PRODUCER.read_bytes()) == PRODUCER_SHA256,
         "producer provenance")
    raw = CERTIFICATE.read_bytes()
    need(digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA, "certificate schema")
    audit = payload.get("finite_audit", {})
    need(audit == {
        "all_positive_rows": 17,
        "fixed_power_credit": 0,
        "global_maxcut_gain_row": {
            "H": 38, "Q": 27, "axis": "EXPONENT_CROSSOVER",
            "comparison_cutoff_z": 5, "kernel_exponent": 1,
            "scale": 256,
        },
        "growing_signed_graph_theorem": "OPEN",
        "magnitude_weighted_objective": "OPEN",
        "rows": 18,
        "signed_gain_rows": 1,
        "source_native_L2": "OPEN",
        "total_edges": 1380,
        "total_max_favorable_edges": 744,
        "total_minimum_unsatisfied_edges": 636,
        "total_sign_frustrated_triangles": 5718,
        "total_signed_gain_over_all_positive": 3,
        "total_triangles": 5727,
    }, "finite audit")
    need(payload.get("firewall", {}).get("TPC293_FULL_GATE_B") == "OPEN" and
         payload["firewall"].get("TPC293_FIXED_POWER_CREDIT") == 0 and
         payload["firewall"].get("TPC293_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(LOG.is_file(), "LaTeX log")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("undefined", "LaTeX Warning:",
                "Package rerunfilecheck Warning:", "Overfull \\hbox",
                "Underfull \\hbox"):
        need(bad not in log, "LaTeX warning: " + bad)
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")


def check_bridge() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC293_MAXIMUM_CLAIM = " + STATUS,
        "TPC293_ROUTE_ADVANCE = YES_SCOPED_THREE_PRIME_TO_WHOLE_SHELL_SIGNED_GRAPH",
        "TPC293_ALL_POSITIVE_MAXCUT = PROVED_EXACT_CONDITIONAL",
        "TPC293_SIGNED_OBJECTIVE = PROVED_EXACT_FINITE",
        "TPC293_SWITCHING_INVARIANCE = PROVED_EXACT_FINITE",
        "TPC293_SIGNED_MAXCUT_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
        "TPC293_EDGE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_1380_EDGES",
        "TPC293_MAX_FAVORABLE = NUMERICALLY_CERTIFIED_FINITE_744",
        "TPC293_MINIMUM_UNSATISFIED = NUMERICALLY_CERTIFIED_FINITE_636",
        "TPC293_EXCEPTIONAL_GAIN = NUMERICALLY_CERTIFIED_FINITE_PLUS_3_EDGES_ONE_ROW",
        "TPC293_GROWING_SIGNED_GRAPH = OPEN",
        "TPC293_MAGNITUDE_WEIGHTED_RAYLEIGH = OPEN",
        "TPC293_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE",
        "TPC293_FIXED_POWER_CREDIT = 0",
        "TPC293_FULL_GATE_B = OPEN",
        "TPC293_TWIN_PRIME_RESULT = NONE",
        "TPC293_ROUND2_CLUE = TEST_MAGNITUDE_WEIGHTED_SIGNED_RAYLEIGH_AND_SOURCE_IMAGE",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge()
        outputs = {}
        for script in (PRODUCER, INDEPENDENT, STRESS):
            normal = run(script, False)
            optimized = run(script, True)
            need(normal == optimized, script.name + " optimized mismatch")
            outputs[script.name] = normal
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError) as exc:
        print("TPC293_BRIDGE_CHECK=FAIL " + str(exc), file=sys.stderr)
        return 1
    print("TPC293_BRIDGE_CHECK=PASS rows=18 edges=1380 "
          "max_favorable=744 unsatisfied=636 signed_gain=3 "
          "frustrated_triangles=5718")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
