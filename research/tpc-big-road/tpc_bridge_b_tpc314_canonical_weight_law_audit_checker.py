#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-314."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-314-canonical-weight-law-audit"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc314_canonical_weight_law_audit.md")
PRODUCER = PROJECT / (
    "code/tpc314_canonical_weight_law_audit.py")
INDEPENDENT = PROJECT / "experiments/tpc314_independent_checker.py"
STRESS = PROJECT / "experiments/tpc314_exact_stress.py"
CERTIFICATE = PROJECT / "results/tpc314_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/compile.log"

STATUS = (
    "PROVED_EXACT_FINITE_EXTERNALLY_MOTIVATED_WEIGHT_LAW_ENCLOSURE_AND_"
    "NEW_PANEL_ROBUSTNESS_AUDIT")
SCHEMA = "TPC314_EXTERNALLY_MOTIVATED_WEIGHT_LAW_AUDIT_V1"

# Filled after the release files are final and checked.
PRODUCER_SHA256 = "ef1e27bd81691f04109af63455a2f187079c4a721787b93f7fc49e985608a2a0"
INDEPENDENT_SHA256 = "478a471d81c86fd95a68bee5cca5cdf796d476286b2c51358e97b9294cfb7305"
STRESS_SHA256 = "08d84695ee4d2e53da873d16136a0b625fe43b3d5092fd7a56171c8e6c8bb9f4"
CERTIFICATE_SHA256 = "d0b09fe5c3c33eae949b2b67a93302bdc5b557cdda7094df58027c39a6a8389b"
BRIDGE_SHA256 = "3e31488f8e85b6294e87ae7729b35d75e95a8a6c20f94819101d40e7a96358c9"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc314_canonical_weight_law_audit.py",
    "experiments/tpc314_independent_checker.py",
    "experiments/tpc314_exact_stress.py", "results/tpc314_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex",
    "paper/references.bib", "paper/main.pdf", "paper/paper.pdf",
    "paper/compile.log",
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
    if producer:
        command.append("--check")
    elif script == INDEPENDENT:
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["TPC314_WORKERS"] = "8"
    environment["TPC314_CHECK_WORKERS"] = "8"
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
    need(protocol.get("source_interval") == [321, 640] and
         protocol.get("source_scale") == 640 and
         protocol.get("height") == 66 and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == [
             "COUNTING", "REDUCED_RESIDUE", "VON_MANGOLDT"] and
         protocol.get("log_terms") == 120 and
         protocol.get("grid_digits") == 36, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 8 and audit.get("laws") == 3 and
         audit.get("weighted_cases") == 48 and
         audit.get("minimum_cases_below_one") == 24 and
         audit.get("positive_cases_above_one") == 24 and
         audit.get("log_enclosed_cases") == 16 and
         audit.get("positive_order_types") == 4 and
         audit.get("fixed_power_credit") == 0, "finite audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC314_EXTERNAL_INDEPENDENCE") ==
         "NONE_SAME_LOCKED_ENGINE" and
         firewall.get("TPC314_CANONICAL_WEIGHTING_THEOREM") == "OPEN" and
         firewall.get("TPC314_ARITHMETIC_L2") == "OPEN_LITERAL_SOURCE" and
         firewall.get("TPC314_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC314_TWIN_PRIME_RESULT") == "NONE",
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
        "TPC314_MAXIMUM_CLAIM = " + STATUS,
        "TPC314_ROUTE_ADVANCE = YES_SCOPED_FINITE_WEIGHT_CLASS_ROBUSTNESS",
        "TPC314_WEIGHTED_GRAM_IDENTITY = PROVED_EXACT_FINITE",
        "TPC314_LOG_ATANH_ENCLOSURE = PROVED_EXACT_FINITE_120_TERMS",
        "TPC314_DIRECTED_INTERVAL_PROPAGATION = PROVED_EXACT_FINITE_GRID_1E_MINUS_36",
        "TPC314_MINIMUM_BELOW_ONE = NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
        "TPC314_POSITIVE_ABOVE_ONE = NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
        "TPC314_EXTERNAL_INDEPENDENCE = NONE_SAME_LOCKED_ENGINE",
        "TPC314_CANONICAL_WEIGHTING = OPEN",
        "TPC314_FRESH_PHYSICAL_HOLDOUT = OPEN",
        "TPC314_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC314_FIXED_POWER_CREDIT = 0",
        "TPC314_FULL_GATE_B = OPEN",
        "TPC314_TWIN_PRIME_RESULT = NONE",
        "TPC314_ROUND2_CLUE = REPLICATE_THE_LOCKED_WEIGHT_LAW_MENU_ON_A_FRESH_SOURCE_INTERVAL_WITH_WEIGHTS_FIXED_BEFORE_TARGET_RECOMPUTATION",
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
        print("TPC314_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC314_BRIDGE_CHECK=PASS rows=8 laws=3 cases=48 "
          "minimum_below_one=24 positive_above_one=24 "
          "log_enclosures=16 grid_digits=36")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
