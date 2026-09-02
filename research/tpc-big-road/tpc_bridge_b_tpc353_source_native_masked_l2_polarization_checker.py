#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-353."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-353-source-native-masked-l2-polarization"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc353_source_native_masked_l2_polarization.md"
PRODUCER = PROJECT / "code/tpc353_source_native_masked_l2_polarization.py"
INDEPENDENT = PROJECT / "experiments/tpc353_independent_checker.py"
STRESS = PROJECT / "experiments/tpc353_polarization_stress.py"
CERTIFICATE = PROJECT / "results/tpc353_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

PRODUCER_SHA256 = "2638df53704a08d6f278de7b60ddf472873c69b6eebdbdad172b4c225b2fb7e9"
INDEPENDENT_SHA256 = "4cd7c094dfa2b570edb6707bb1d11dcf9463ddb6cbd0beb5c020252fb62530e2"
STRESS_SHA256 = "eaedbb97337997a7ef4b85ac8f9574d466b317af68d24b1118f553f1a172cf5a"
CERTIFICATE_SHA256 = "bfe0199b687898f3b4bfd5ca4f2b9f645890d6c54fe434b1f2ceaf0ae8c6ef82"
PDF_SHA256 = "c306158ac33678389a9c444887684ce20a42245a6536a974bd303da3031e8476"
LOG_SHA256 = "1afa2062ce749b20957b7b1473d439dbe4cf0c4518e728cf95befa818b5b8a3c"
BRIDGE_SHA256 = "a9562cc4d4178d94ee40d818937a82b87e1408e95ae0a58455b95b036626829e"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SOURCE_NATIVE_MASKED_L2_POLARIZATION_AUDIT"
SCHEMA = "TPC353_SOURCE_NATIVE_MASKED_L2_POLARIZATION_V1"


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
    need(protocol.get("origins") == [6001, 8001, 10001] and
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
         summary.get("kappa_min") == "0.69291151430780062" and
         summary.get("kappa_max") == "0.99626802812598902", "all-plus summary")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC353_FINITE_OPERATOR_POLARIZATION") ==
         "PROVED_EXACT_FINITE" and
         firewall.get("TPC353_OPERATOR_REPLAY") ==
         "NUMERICALLY_CERTIFIED_FINITE_216_ROWS" and
         firewall.get("TPC353_POSITIVE_ALIGNMENT") ==
         "NUMERICALLY_CERTIFIED_FINITE_216_OF_216" and
         firewall.get("TPC353_UNIFORM_L2") == "OPEN" and
         firewall.get("TPC353_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC353_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC353_TWIN_PRIME_RESULT") == "NONE", "firewall")
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
        "TPC353_MAXIMUM_CLAIM = " + STATUS,
        "TPC353_FINITE_OPERATOR_POLARIZATION = PROVED_EXACT_FINITE",
        "TPC353_FINITE_CAUCHY_ENVELOPE = PROVED_EXACT_FINITE",
        "TPC353_SOURCE_NATIVE_MODEL = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC353_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS",
        "TPC353_POSITIVE_ALIGNMENT = NUMERICALLY_CERTIFIED_FINITE_216_OF_216",
        "TPC353_UNIFORM_L2 = OPEN",
        "TPC353_ARITHMETIC_ADVANCE = NO",
        "TPC353_FIXED_POWER_CREDIT = 0",
        "TPC353_FULL_GATE_B = OPEN",
        "TPC353_TWIN_PRIME_RESULT = NONE",
        "TPC353_STATUS = " + STATUS,
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
        print("TPC353_BRIDGE_CHECK=PASS rows=216 positive_alignment=216/216 "
              "all_plus_kappa=0.69291151430780062--0.99626802812598902")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC353_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
