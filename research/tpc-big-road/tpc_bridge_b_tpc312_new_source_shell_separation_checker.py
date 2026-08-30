#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-312."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-312-new-source-shell-separation-atlas"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc312_new_source_shell_separation.md"
PRODUCER = PROJECT / "code/tpc312_new_source_shell_separation.py"
INDEPENDENT = PROJECT / "experiments/tpc312_independent_checker.py"
STRESS = PROJECT / "experiments/tpc312_exact_stress.py"
CERTIFICATE = PROJECT / "results/tpc312_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/compile.log"

STATUS = "PROVED_EXACT_FINITE_NEW_SOURCE_SHELL_GRAM_AND_SIGN_SEPARATION_ATLAS"
SCHEMA = "TPC312_NEW_SOURCE_SHELL_SIGN_SEPARATION_V1"

PRODUCER_SHA256 = (
    "dc0d371c71069e97cf685f46163efc285ba8a38801f3732b9283ec990426ddb9")
INDEPENDENT_SHA256 = (
    "c1d60547635c64ee8440b3692c1e4b8dc2c7d0f44b7200054e3677ee97d2b081")
STRESS_SHA256 = (
    "7ace225c45170c7ce309ce55ee466a77be2ddf822cfc5a177f212239dc826472")
CERTIFICATE_SHA256 = (
    "04528d9b7381d2f1b3e1e8ff7854114752816fca49ff8779de5a07714b95224d")
BRIDGE_SHA256 = (
    "11773b77edfab3a2b9555a0222ee621728774b6cc97f3d15cf6293265ecfe2c5")

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc312_new_source_shell_separation.py",
    "experiments/tpc312_independent_checker.py",
    "experiments/tpc312_exact_stress.py", "results/tpc312_certificate.json",
    "notes/theorem_ledger.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/citation_verification.md", "paper/main.tex",
    "paper/references.bib", "paper/main.pdf", "paper/paper.pdf",
    "paper/compile.log",
)


class Failure(RuntimeError):
    pass


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script), "--check"]
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
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
    need(payload.get("schema") == SCHEMA, "certificate schema")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(payload.get("protocol", {}).get("source_scale") == 640 and
         payload["protocol"].get("index_interval") == [321, 640] and
         payload["protocol"].get("height") == 66 and
         payload["protocol"].get("Q_anchors") == [24, 36, 54, 80] and
         payload["protocol"].get("kernel_exponents") == [1, 2],
         "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 8 and
         audit.get("explicit_shell_targets") == 84 and
         audit.get("enumerated_labelings_mod_global_sign") == 37440 and
         audit.get("full_rank_rows") == 8 and
         audit.get("strict_separation_rows") == 8,
         "finite audit")
    firewall = payload.get("firewall", {})
    need(firewall.get("TPC312_EXTERNAL_INDEPENDENCE") == "NONE" and
         firewall.get("TPC312_ARITHMETIC_L2") == "OPEN_LITERAL_SOURCE" and
         firewall.get("TPC312_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC312_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC312_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(),
         "published PDF differs from compiled PDF")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error"):
        need(bad not in log, "LaTeX warning: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC312_MAXIMUM_CLAIM = " + STATUS,
        "TPC312_ROUTE_ADVANCE = YES_SCOPED_NEW_SOURCE_SHELL_ATLAS",
        "TPC312_NEW_SOURCE_SHELL_ROWS = PROVED_EXACT_FINITE_8_ROWS",
        "TPC312_PHYSICAL_GRAM_PSD = PROVED_EXACT_FINITE",
        "TPC312_RATIONAL_FULL_RANK = PROVED_EXACT_FINITE_8_OF_8",
        "TPC312_SIGN_EXTREMA = PROVED_EXACT_FINITE_37440_CLASSES",
        "TPC312_STRICT_SIGN_SEPARATION = PROVED_EXACT_FINITE_8_OF_8",
        "TPC312_Q_SPINE_ORDERING = PROVED_EXACT_FINITE_4_Q_BY_2_EXPONENTS",
        "TPC312_FRESHNESS = NEW_SOURCE_SHELL_ROWS_WITHIN_SAME_LOCKED_ENGINE",
        "TPC312_EXTERNAL_INDEPENDENCE = NONE",
        "TPC312_PROFILE_BUDGET_INTERVAL_CERTIFICATE = OPEN",
        "TPC312_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE",
        "TPC312_FIXED_POWER_CREDIT = 0",
        "TPC312_FULL_GATE_B = OPEN",
        "TPC312_TWIN_PRIME_RESULT = NONE",
        "TPC312_STATUS = " + STATUS,
        "TPC312_ROUND2_CLUE = CERTIFY_NEW_PANEL_PROFILE_BUDGETS_WITH_OUTWARD_ROUNDING_BEFORE_ANY_HOLDOUT_PREFERENCE_CLAIM",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge_text()
        for script in (PRODUCER, INDEPENDENT, STRESS):
            normal = run(script, False)
            optimized = run(script, True)
            need(normal == optimized, script.name + " optimized mismatch")
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError) as error:
        print("TPC312_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC312_BRIDGE_CHECK=PASS rows=8 shell_targets=84 "
          "sign_classes=37440 full_rank=8 strict_separation=8")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
