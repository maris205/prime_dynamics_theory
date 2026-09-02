#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-354."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-354-higher-origin-masked-l2-holdout"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc354_higher_origin_masked_l2_holdout.md"
PRODUCER = PROJECT / "code/tpc354_higher_origin_masked_l2_holdout.py"
INDEPENDENT = PROJECT / "experiments/tpc354_independent_checker.py"
STRESS = PROJECT / "experiments/tpc354_holdout_stress.py"
CERTIFICATE = PROJECT / "results/tpc354_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PRODUCER_SHA256 = "effb33810ea773467c367679b9a7bf755b626b4759d812c916336cb226877aed"
INDEPENDENT_SHA256 = "6b56da7f2567281aa4110104bc540e04a175acbdde6e98878e4c17874436eb6a"
STRESS_SHA256 = "885d42a330a826e87863d07bafd68f3ff7a7fe7c6d99f76695b2c825d27102c3"
CERTIFICATE_SHA256 = "033be8d4e2b2f977975a35f014b564ed0f7523578ec2909eb66405fa789e4ceb"
PDF_SHA256 = "d1efeb1a5172152af250185bcdc31e7ddeb3cd8e0dc9ee3e46ae44e2c4f83503"
LOG_SHA256 = "db008c231c115663dc39fb273ded3bf81a65b22b71d661caeda3def79b6cf534"
BRIDGE_SHA256 = "4f1d8bbdc16fffc1d8c1b4ecb83b15086ae88a53bc263f0d8c426b2a04ca6d3a"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_HIGHER_ORIGIN_MASKED_L2_HOLDOUT"
SCHEMA = "TPC354_HIGHER_ORIGIN_MASKED_L2_HOLDOUT_V1"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def lock(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED", label + " placeholder")
    need(path.is_file() and digest(path.read_bytes()) == expected,
         label + " provenance")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload", {})
    need(payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "schema/payload hash")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [21001, 23001, 25001] and
         protocol.get("source_counts") == [256, 512, 1024] and
         protocol.get("q_anchors") == [24, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"],
         "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 216 and
         audit.get("positive_output_alignment") == 216 and
         audit.get("negative_output_alignment") == 0 and
         audit.get("unresolved") == 0 and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "finite audit")
    summary = payload.get("law_summaries", {}).get("all_plus", {})
    need(summary.get("positive_output_alignment") == 54 and
         summary.get("negative_output_alignment") == 0 and
         summary.get("kappa_min") == "0.65076036812307647" and
         summary.get("kappa_max") == "0.99135023146539858", "all-plus summary")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC354_FINITE_OPERATOR_POLARIZATION") ==
         "PROVED_EXACT_FINITE" and
         firewall.get("TPC354_OPERATOR_REPLAY") ==
         "NUMERICALLY_CERTIFIED_FINITE_216_ROWS" and
         firewall.get("TPC354_POSITIVE_ALIGNMENT") ==
         "NUMERICALLY_CERTIFIED_FINITE_216_OF_216" and
         firewall.get("TPC354_HIGHER_ORIGIN_HOLDOUT") ==
         "NUMERICALLY_CERTIFIED_FINITE_216_ROWS" and
         firewall.get("TPC354_UNIFORM_L2") == "OPEN" and
         firewall.get("TPC354_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC354_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC354_TWIN_PRIME_RESULT") == "NONE", "firewall")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error", "Fatal error",
                "Citation"):
        need(bad not in log, "LaTeX diagnostic: " + bad)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100_000,
         "PDF identity")


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC354_MAXIMUM_CLAIM = " + STATUS,
        "TPC354_FINITE_OPERATOR_POLARIZATION = PROVED_EXACT_FINITE",
        "TPC354_FINITE_CAUCHY_ENVELOPE = PROVED_EXACT_FINITE",
        "TPC354_SOURCE_NATIVE_MODEL = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC354_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS",
        "TPC354_POSITIVE_ALIGNMENT = NUMERICALLY_CERTIFIED_FINITE_216_OF_216",
        "TPC354_HIGHER_ORIGIN_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_216_ROWS",
        "TPC354_UNIFORM_L2 = OPEN",
        "TPC354_ARITHMETIC_ADVANCE = NO",
        "TPC354_FIXED_POWER_CREDIT = 0",
        "TPC354_FULL_GATE_B = OPEN",
        "TPC354_TWIN_PRIME_RESULT = NONE",
        "TPC354_STATUS = " + STATUS,
    )
    for marker in markers:
        need(marker in text, "bridge marker missing")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script)])
    if script in (PRODUCER, INDEPENDENT, STRESS):
        command.append("--check")
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "OMP_NUM_THREADS": "1",
                "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
    result = subprocess.run(command, cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        lock(PRODUCER, PRODUCER_SHA256, "producer")
        lock(INDEPENDENT, INDEPENDENT_SHA256, "independent checker")
        lock(STRESS, STRESS_SHA256, "stress checker")
        lock(CERTIFICATE, CERTIFICATE_SHA256, "certificate")
        lock(MAIN_PDF, PDF_SHA256, "main PDF")
        lock(PDF, PDF_SHA256, "paper PDF")
        lock(LOG, LOG_SHA256, "compile log")
        lock(BRIDGE, BRIDGE_SHA256, "bridge")
        check_certificate()
        check_bridge_text()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        normal = tuple(run(script, False) for script in scripts)
        optimized = tuple(run(script, True) for script in scripts)
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC354_BRIDGE_CHECK=PASS rows=216 positive_alignment=216/216 "
              "all_plus_kappa=0.65076036812307647--0.99135023146539858")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC354_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
