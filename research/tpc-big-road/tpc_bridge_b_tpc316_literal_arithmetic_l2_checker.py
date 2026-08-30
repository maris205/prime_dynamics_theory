#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-316."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-316-literal-arithmetic-l2-fresh-panel"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc316_literal_arithmetic_l2.md")
PRODUCER = PROJECT / (
    "code/tpc316_literal_arithmetic_l2_fresh_panel.py")
INDEPENDENT = PROJECT / (
    "experiments/tpc316_independent_checker.py")
STRESS = PROJECT / "experiments/tpc316_l2_stress.py"
CERTIFICATE = PROJECT / "results/tpc316_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

STATUS = (
    "PROVED_EXACT_FINITE_LITERAL_ARITHMETIC_L2_ENVELOPE_PLUS_"
    "TWO_SCALE_OBSTRUCTION")
SCHEMA = "TPC316_LITERAL_ARITHMETIC_L2_FRESH_PANEL_V1"

# Sealed after the release artifacts and dynamic documentation are final.
PRODUCER_SHA256 = "c652fff9a382e88350f5d95915e2d4a2aa52d461d3b2a6f2faf9c904ab144dcc"
INDEPENDENT_SHA256 = "9d1b3115318760273f9a3c61677de4f396a39f9c9e3b1b1dc415979817ceeb8e"
STRESS_SHA256 = "e778a4ef42b6e9c3c18c1f2de5f2289d4e4e0e99b765e2ba137851300f8e8266"
CERTIFICATE_SHA256 = "3bb9f3463daf7583ca07a672bf19be827af5404c2c7005b6e6bf6b766bd8ef26"
BRIDGE_SHA256 = "9bd89af292b86d992c159a731e8c3b82771453e6f1791e282e2dac0811758477"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc316_literal_arithmetic_l2_fresh_panel.py",
    "experiments/tpc316_independent_checker.py",
    "experiments/tpc316_l2_stress.py",
    "results/tpc316_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/main.pdf",
    "paper/paper.pdf", "paper/compile.log",
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def run(script: Path, optimized: bool, needs_check_flag: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script)]
    if needs_check_flag:
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["TPC316_WORKERS"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    for relative in REQUIRED:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
    for path, expected, label in (
            (PRODUCER, PRODUCER_SHA256, "producer"),
            (INDEPENDENT, INDEPENDENT_SHA256, "independent checker"),
            (STRESS, STRESS_SHA256, "stress checker"),
            (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
            (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(not expected.startswith("__"), label + " hash not sealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")

    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload", {})
    need(payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    parent = payload.get("parent_lock", {})
    need(parent.get("engine_sha256") ==
         "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3",
         "engine lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("source_scales") == [640, 1280] and
         protocol.get("fresh_scale") == 1280 and
         protocol.get("height") == 66 and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("deleted_diagonal") is True and
         protocol.get("domain") == "ell^2(I_X)" and
         protocol.get("codomain") == "ell^2(S_Q x I_X)", "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("scales") == 2 and audit.get("rows") == 16 and
         audit.get("comparison_rows") == 8 and
         audit.get("probe_columns_per_row") == 5 and
         audit.get("normalized_hs_increased_rows") == 8 and
         audit.get("normalized_hs_increased_all_rows") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("growing_theorem") == "OPEN", "finite audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC316_FINITE_LITERAL_OPERATOR") ==
         "PROVED_EXACT_FINITE" and
         firewall.get("TPC316_FROBENIUS_L2_ENVELOPE") ==
         "PROVED_EXACT_FINITE" and
         firewall.get("TPC316_NORMALIZED_HS_TWO_SCALE_RISE") ==
         "NUMERICALLY_CERTIFIED_FINITE_8_OF_8" and
         firewall.get("TPC316_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC316_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC316_GROWING_ARITHMETIC_L2") == "OPEN" and
         firewall.get("TPC316_OPERATOR_NORM_DECAY") == "OPEN" and
         firewall.get("TPC316_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC316_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "main and paper PDF differ")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error"):
        need(bad not in log, "LaTeX warning: " + bad)


def check_bridge_text() -> None:
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC316_MAXIMUM_CLAIM = " + STATUS,
        "TPC316_ROUTE_ADVANCE = YES_SCOPED_LITERAL_FINITE_L2_ENVELOPE",
        "TPC316_LITERAL_OPERATOR = PROVED_EXACT_FINITE",
        "TPC316_FROBENIUS_L2_ENVELOPE = PROVED_EXACT_FINITE",
        "TPC316_DIFFERENCE_RESIDUE_COUNT = PROVED_EXACT_FINITE",
        "TPC316_COORDINATE_LOWER_WITNESSES = PROVED_EXACT_FINITE_5_PER_ROW",
        "TPC316_NORMALIZED_HS_TWO_SCALE_RISE = NUMERICALLY_CERTIFIED_FINITE_8_OF_8",
        "TPC316_HS_DECAY_PROXY = REFUTED_SCOPED_TWO_DECLARED_PANELS",
        "TPC316_GROWING_ARITHMETIC_L2 = OPEN",
        "TPC316_TRUE_OPERATOR_NORM_DECAY = OPEN",
        "TPC316_ARITHMETIC_ADVANCE = NO",
        "TPC316_FIXED_POWER_CREDIT = 0",
        "TPC316_FULL_GATE_B = OPEN",
        "TPC316_TWIN_PRIME_RESULT = NONE",
        "TPC316_ROUND2_CLUE = " + (
            "REPLACE_THE_FROBENIUS_ENVELOPE_BY_A_GROWING_OPERATOR_OR_"
            "ARITHMETIC_CANCELLATION_ESTIMATE_WITHOUT_IMPORTING_A_POWER_CLAIM"),
    )
    for marker in markers:
        need(marker in bridge_text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge_text()
        for script, flag in ((PRODUCER, True),
                             (INDEPENDENT, True),
                             (STRESS, False)):
            normal = run(script, False, flag)
            optimized = run(script, True, flag)
            need(normal == optimized, script.name + " optimized mismatch")
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError) as error:
        print("TPC316_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC316_BRIDGE_CHECK=PASS scales=2 rows=16 comparisons=8 "
          "probe_columns=80 normalized_hs_rise=8 fixed_power_credit=0")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
