#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-345."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-345-principal-angle-grassmann-audit"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc345_principal_angle_grassmann_audit.md"
PRODUCER = PROJECT / "code/tpc345_principal_angle_grassmann_audit.py"
INDEPENDENT = PROJECT / "experiments/tpc345_independent_checker.py"
STRESS = PROJECT / "experiments/tpc345_geometry_stress.py"
CERTIFICATE = PROJECT / "results/tpc345_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PRODUCER_SHA256 = "da6e4a72f3aee7a744cb2d15e9060260c380c25568efd19204968fd5ed63df9e"
INDEPENDENT_SHA256 = "407769c68686e30353de20d75b2fb1469fa5d6953a701d786d9a1fb84ab6e5f7"
STRESS_SHA256 = "0decdd54c2d499abcf758ba02c694189c0ff8f14f2d45fb96a2c3fc2ef26370d"
CERTIFICATE_SHA256 = "b50a54ac77f4ec9a02d9223a5eab97c55f49203b8f921b4e2696ae014a06c3a2"
PDF_SHA256 = "01ae3e88a67c758c4a5190381e19f22a378ddc156f4172444b7ac2a096ba7ab8"
BRIDGE_SHA256 = "937da588cb71fb4525a201d280b58b3d5e3d164c366eb8173b38eb504f25345d"

TPC344_CODE = ROOT / "papers/tpc-344-panel-contrast-nuisance-basis/code/tpc344_panel_contrast_nuisance_basis.py"
TPC344_CERT = ROOT / "papers/tpc-344-panel-contrast-nuisance-basis/results/tpc344_certificate.json"
TPC344_CODE_SHA256 = "08daa3e1b5782e619f492039ed0b8f734de923dfc39797d88eea8a5650ce83ba"
TPC344_CERT_SHA256 = "29da3486ef9c1fcb7ec4274203e93059959736b05ea0eb3bf7f8f69e69a63460"

SCHEMA = "TPC345_PRINCIPAL_ANGLE_GRASSMANN_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PRINCIPAL_ANGLE_GRASSMANN_AUDIT"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script)])
    if script == PRODUCER:
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["OMP_NUM_THREADS"] = "32"
    environment["OPENBLAS_NUM_THREADS"] = "32"
    environment["MKL_NUM_THREADS"] = "32"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    required = (
        ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
        "PROOF_PACKAGE.md", "code/tpc345_principal_angle_grassmann_audit.py",
        "experiments/tpc345_independent_checker.py",
        "experiments/tpc345_geometry_stress.py", "results/tpc345_certificate.json",
        "notes/theorem_ledger.md", "notes/claim_firewall.md",
        "notes/computational_protocol.md", "notes/route_evaluation.md",
        "notes/citation_verification.md", "paper/main.tex", "paper/main.pdf",
        "paper/paper.pdf", "paper/compile.log")
    for item in required:
        need((PROJECT / item).is_file(), "missing artifact: " + item)
    for path, expected, label in (
            (PRODUCER, PRODUCER_SHA256, "producer"),
            (INDEPENDENT, INDEPENDENT_SHA256, "independent"),
            (STRESS, STRESS_SHA256, "stress"),
            (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
            (MAIN_PDF, PDF_SHA256, "main pdf"),
            (PDF, PDF_SHA256, "paper pdf"),
            (BRIDGE, BRIDGE_SHA256, "bridge"),
            (TPC344_CODE, TPC344_CODE_SHA256, "TPC344 producer"),
            (TPC344_CERT, TPC344_CERT_SHA256, "TPC344 certificate")):
        need(digest(path.read_bytes()) == expected, label + " provenance")

    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document) and
         document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    need(payload.get("finite_audit") == {
        "panels": 2, "rows": 6, "controls": 9, "categories": 4,
        "raw_records": 216, "nonempty_raw_records": 171,
        "weightings": 2, "principal_angle_pairs": 2,
        "loo_angle_pairs": 18, "basis_invariance_checks": 2,
        "fixed_power_credit": 0, "arithmetic_advance": "NO"}, "audit")
    rows = payload.get("rows", [])
    need(len(rows) == 6 and
         [row.get("origin") for row in rows] ==
         [48097, 48609, 49217, 40097, 40609, 41121], "rows")
    for row in rows:
        need(row.get("cutoff_safe") is True and
             row.get("source_interval") == [
                 row["origin"], row["origin"] + 511] and
             len(row.get("raw_records", [])) == 36, "row geometry")
    weightings = payload.get("weighting_results", [])
    need([item.get("label") for item in weightings] == ["raw", "equal_row"],
         "weighting labels")
    for item in weightings:
        geo = item.get("principal_geometry", {})
        cosines = geo.get("principal_cosines", [])
        need(geo.get("left_rank") == 3 and geo.get("right_rank") == 2 and
             len(cosines) == 2 and
             item.get("basis_invariance", {}).get("span_invariant") is True,
             "principal geometry")
        need(float(item.get("target_panel_1_on_panel_0", {}).get(
            "residual_retention", 0.0)) >= 0.30,
             "transfer obstruction")
        need(len(item.get("leave_one_control_out", [])) == 9,
             "loo geometry")
    summary = payload.get("summary", {})
    need(float(summary.get("raw_principal_cosines", [0])[0]) > 0.99 and
         float(summary.get("raw_principal_cosines", [1, 1])[1]) < 0.20 and
         float(summary.get("equal_row_principal_cosines", [1, 1])[1]) < 0.20 and
         float(summary.get("dominant_angle_shift_degrees", 0.0)) > 10.0 and
         summary.get("basis_invariance") == "NUMERICALLY_CERTIFIED_FINITE" and
         summary.get("weighting_stability") == "REFUTED_SCOPED" and
         summary.get("cross_panel_transfer_relevance") == "REFUTED_SCOPED",
         "summary guards")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC345_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC345_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC345_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC345_TWIN_PRIME_RESULT") == "NONE",
         "firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100_000,
         "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox", "Underfull \\hbox",
                "LaTeX Error", "Fatal error", "Citation"):
        need(bad not in log, "LaTeX diagnostic: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC345_MAXIMUM_CLAIM = " + STATUS,
        "TPC345_PRINCIPAL_ANGLE_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC345_BASIS_INVARIANCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC345_RAW_DOMINANT_ALIGNMENT = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC345_TRANSVERSE_ALIGNMENT = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC345_WEIGHTING_STABILITY = REFUTED_SCOPED",
        "TPC345_MUTUAL_TRANSFER = REFUTED_SCOPED",
        "TPC345_RANK_MISMATCH = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC345_ARITHMETIC_ADVANCE = NO",
        "TPC345_FIXED_POWER_CREDIT = 0",
        "TPC345_FULL_GATE_B = OPEN",
        "TPC345_TWIN_PRIME_RESULT = NONE",
        "TPC345_STATUS = " + STATUS,
        "TPC345_ROUND2_CLUE = FINITE_NO_GO_OR_FREEZE_PANEL_ADAPTIVE_ROUTE")
    for marker in markers:
        need(marker in text, "bridge marker missing")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check_files()
        check_bridge_text()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        normal = tuple(run(script, False) for script in scripts)
        optimized = tuple(run(script, True) for script in scripts)
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC345_BRIDGE_CHECK=PASS panels=2 rows=6 raw_records=216 "
              "loo_angle_pairs=18 raw_cosines=0.9957018010,0.0799456793 "
              "equal_cosines=0.9144519860,0.0787084493")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC345_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
