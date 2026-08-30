#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-315."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-315-fresh-source-locked-weight-holdout"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc315_fresh_source_locked_weight_holdout.md")
PRODUCER = PROJECT / (
    "code/tpc315_fresh_source_locked_weight_holdout.py")
INDEPENDENT = PROJECT / "experiments/tpc315_independent_checker.py"
STRESS = PROJECT / "experiments/tpc315_holdout_stress.py"
CERTIFICATE = PROJECT / "results/tpc315_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/compile.log"

STATUS = (
    "PROVED_EXACT_FINITE_FRESH_SOURCE_LOCKED_WEIGHT_MENU_HOLDOUT_"
    "REPLICATION_AND_LAW_ORDER_SHIFT")
SCHEMA = "TPC315_FRESH_SOURCE_LOCKED_WEIGHT_HOLDOUT_V1"

# These are sealed after all release artifacts are final.
PRODUCER_SHA256 = "1512673573768cd84cae0b908634b9d9e7f895c2f7113223a370fe315833ad8e"
INDEPENDENT_SHA256 = "5bcf84032008d2fdee6758df3490c5d59665f7efe25baa4de766403e7c2b7b95"
STRESS_SHA256 = "a706a0f95346f982cf5b6b51141756184b43d206e4c7ccdfa00e1a7bdf4bd30d"
CERTIFICATE_SHA256 = "4494b34b1d653694fe28b53b2f06ea6a88bee9717e2a954900cdaf62ac63a49f"
BRIDGE_SHA256 = "72037cbb777c22e6f5f409400260702ad203858bca5293e1d79638cb1178c7e3"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc315_fresh_source_locked_weight_holdout.py",
    "experiments/tpc315_independent_checker.py",
    "experiments/tpc315_holdout_stress.py",
    "results/tpc315_certificate.json", "notes/theorem_ledger.md",
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


def run(script: Path, optimized: bool, producer: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script)]
    if producer or script == INDEPENDENT:
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["TPC315_WORKERS"] = "8"
    environment["TPC315_CHECK_WORKERS"] = "8"
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
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA and
         data.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    protocol = payload.get("protocol", {})
    need(protocol.get("source_interval") == [641, 1280] and
         protocol.get("source_scale") == 1280 and
         protocol.get("height") == 66 and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == [
             "COUNTING", "REDUCED_RESIDUE", "VON_MANGOLDT"] and
         protocol.get("log_terms") == 120 and
         protocol.get("grid_digits") == 36 and
         protocol.get("weights_locked_before_target_readout") is True and
         protocol.get("target_generation_order") ==
         "lock laws and weights before recomputing fresh physical Gram labels",
         "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("fresh_source_rows") == 8 and
         audit.get("recomputed_target_rows") == 8 and
         audit.get("rows") == 8 and audit.get("laws") == 3 and
         audit.get("weighted_cases") == 48 and
         audit.get("minimum_cases_below_one") == 24 and
         audit.get("positive_cases_above_one") == 24 and
         audit.get("log_enclosed_cases") == 16 and
         audit.get("minimum_order_types") == 3 and
         audit.get("positive_order_types") == 2 and
         audit.get("fresh_replication_rows") == 8 and
         audit.get("fresh_full_rank_rows") == 8 and
         audit.get("fixed_power_credit") == 0, "finite audit")
    need(audit.get("minimum_order_census") == {
        "COUNTING<VON_MANGOLDT<REDUCED_RESIDUE": 1,
        "REDUCED_RESIDUE<COUNTING<VON_MANGOLDT": 1,
        "VON_MANGOLDT<COUNTING<REDUCED_RESIDUE": 6,
    } and audit.get("positive_order_census") == {
        "REDUCED_RESIDUE<COUNTING<VON_MANGOLDT": 6,
        "VON_MANGOLDT<REDUCED_RESIDUE<COUNTING": 2,
    }, "order census")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC315_FRESH_SOURCE_TARGET_RECOMPUTATION") ==
         "PROVED_EXACT_FINITE_8_ROWS" and
         firewall.get("TPC315_LOCKED_WEIGHT_MENU") ==
         "PROVED_EXACT_FINITE_PRE_TARGET" and
         firewall.get("TPC315_HOLDOUT_REPLICATION") ==
         "NUMERICALLY_CERTIFIED_FINITE_8_OF_8" and
         firewall.get("TPC315_MINIMUM_LAW_ORDER_SHIFT") ==
         "NUMERICALLY_CERTIFIED_FINITE_3_TYPES" and
         firewall.get("TPC315_POSITIVE_LAW_ORDER_SHIFT") ==
         "NUMERICALLY_CERTIFIED_FINITE_2_TYPES" and
         firewall.get("TPC315_EXTERNAL_INDEPENDENCE") ==
         "NONE_SAME_LOCKED_ENGINE" and
         firewall.get("TPC315_CANONICAL_WEIGHTING") == "OPEN" and
         firewall.get("TPC315_ARITHMETIC_L2") == "OPEN_LITERAL_SOURCE" and
         firewall.get("TPC315_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC315_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC315_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(),
         "main and published PDF differ")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error"):
        need(bad not in log, "LaTeX warning: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC315_MAXIMUM_CLAIM = " + STATUS,
        "TPC315_ROUTE_ADVANCE = YES_SCOPED_FRESH_SOURCE_CLASS_REPLICATION_AND_ORDER_OBSTRUCTION",
        "TPC315_FRESH_SOURCE_TARGET_RECOMPUTATION = PROVED_EXACT_FINITE_8_ROWS",
        "TPC315_LOCKED_WEIGHT_MENU = PROVED_EXACT_FINITE_PRE_TARGET",
        "TPC315_LOG_ATANH_ENCLOSURE = PROVED_EXACT_FINITE_120_TERMS",
        "TPC315_DIRECTED_INTERVAL_PROPAGATION = PROVED_EXACT_FINITE_GRID_1E_MINUS_36",
        "TPC315_HOLDOUT_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_8_OF_8",
        "TPC315_MINIMUM_LAW_ORDER_SHIFT = NUMERICALLY_CERTIFIED_FINITE_3_TYPES",
        "TPC315_POSITIVE_LAW_ORDER_SHIFT = NUMERICALLY_CERTIFIED_FINITE_2_TYPES",
        "TPC315_EXTERNAL_INDEPENDENCE = NONE_SAME_LOCKED_ENGINE",
        "TPC315_CANONICAL_WEIGHTING = OPEN",
        "TPC315_FRESH_PHYSICAL_HOLDOUT = NONE_SAME_LOCKED_ENGINE",
        "TPC315_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC315_FIXED_POWER_CREDIT = 0",
        "TPC315_FULL_GATE_B = OPEN",
        "TPC315_TWIN_PRIME_RESULT = NONE",
        "TPC315_ROUND2_CLUE = PROBE_LITERAL_ARITHMETIC_L2_INTERFACE_ON_THE_FRESH_PANEL_BEFORE_ANY_GROWING_CLAIM",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge_text()
        for script, producer in ((PRODUCER, True),
                                 (INDEPENDENT, False),
                                 (STRESS, False)):
            normal = run(script, False, producer)
            optimized = run(script, True, producer)
            need(normal == optimized, script.name + " optimized mismatch")
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError) as error:
        print("TPC315_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC315_BRIDGE_CHECK=PASS rows=8 laws=3 cases=48 "
          "minimum_below_one=24 positive_above_one=24 "
          "fresh_target_rows=8 log_enclosures=16 grid_digits=36")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
