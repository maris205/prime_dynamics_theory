#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-355."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-355-position-aware-mask-energy-normalization"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc355_position_aware_mask_energy_normalization.md")
PRODUCER = PROJECT / (
    "code/tpc355_position_aware_mask_energy_normalization.py")
INDEPENDENT = PROJECT / "experiments/tpc355_independent_checker.py"
STRESS = PROJECT / "experiments/tpc355_normalization_stress.py"
CERTIFICATE = PROJECT / "results/tpc355_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

# Filled after all claim-bearing files are final.
PRODUCER_SHA256 = "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9"
INDEPENDENT_SHA256 = "203c4ce5342d349e7e04c5e17e884b98b9a7f766ddcbecb2f21cc79af2f8405b"
STRESS_SHA256 = "2cad87479bf044010ced3a69ed13fc62998e0a9641235eac0ce50558a2ffcd66"
CERTIFICATE_SHA256 = "29c5e824b415e675c931396567337cbb583b8f952b489ea2a386a63c649fff7b"
PDF_SHA256 = "83716c2f61baf2e5b20d552b33a69900e19efb60f754092c68847c663c1aac0d"
LOG_SHA256 = "2b83007925f566fcef3b25cfc3278949d59840d2f5ccce3f96d78e3665963a72"
BRIDGE_SHA256 = "059bf58c7fe2cbf543fda3351673985106c8f84fa9be6e84613b57ae72fa0e3e"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_POSITION_AWARE_MASK_ENERGY_NORMALIZATION_AUDIT"
SCHEMA = "TPC355_POSITION_AWARE_MASK_ENERGY_NORMALIZATION_V1"


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
    need(protocol.get("panel_names") == ["low_parent", "higher_parent",
                                          "fresh_holdout"] and
         protocol.get("source_counts") == [256, 512, 1024] and
         protocol.get("q_anchors") == [24, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"],
         "protocol")
    normalization = protocol.get("normalization", {})
    need(normalization.get("response_independent") is True and
         normalization.get("source_independent") is True and
         normalization.get("sign_law_independent") is True,
         "normalization independence")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 648 and
         audit.get("raw_positive_alignment") == 647 and
         audit.get("raw_negative_alignment") == 1 and
         audit.get("raw_unresolved") == 0 and
         audit.get("normalized_positive_alignment") == 647 and
         audit.get("normalized_negative_alignment") == 1 and
         audit.get("normalized_unresolved") == 0 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    floor = payload.get("transfer_summary", {}).get("all_plus_floor", {})
    need(floor.get("raw_higher_drop") == "0.042151146184724153" and
         floor.get("normalized_higher_drop") == "0.026236988152766205" and
         floor.get("drop_reduction_fraction") ==
         "0.37754982894688971", "floor summary")
    mean = payload.get("transfer_summary", {}).get("all_plus_mean", {})
    need(mean.get("raw_higher_drop") == "0.021249745559872912" and
         mean.get("normalized_higher_drop") == "0.024839744603963321",
         "mean obstruction")
    firewall = payload.get("claim_firewall", {})
    for key, value in {
            "TPC355_GEOMETRY_DEFINITION":
            "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC355_DIAGONAL_CONGRUENCE": "PROVED_EXACT_FINITE",
            "TPC355_OPERATOR_POLARIZATION": "PROVED_EXACT_FINITE",
            "TPC355_PANEL_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_648_ROWS",
            "TPC355_ALL_PLUS_FLOOR_REPAIR":
            "NUMERICALLY_CERTIFIED_FINITE_PARTIAL",
            "TPC355_ALL_PLUS_MEAN_REPAIR": "REFUTED_SCOPED",
            "TPC355_ALL_LAW_POSITIVE_ALIGNMENT": "REFUTED_SCOPED",
            "TPC355_SOURCE_UNIFORM_L2": "OPEN",
            "TPC355_ARITHMETIC_ADVANCE": "NO",
            "TPC355_FULL_GATE_B": "OPEN",
            "TPC355_TWIN_PRIME_RESULT": "NONE",
    }.items():
        need(firewall.get(key) == value, "firewall " + key)
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
        "TPC355_MAXIMUM_CLAIM = " + STATUS,
        "TPC355_GEOMETRY_DEFINITION = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC355_DIAGONAL_CONGRUENCE = PROVED_EXACT_FINITE",
        "TPC355_OPERATOR_POLARIZATION = PROVED_EXACT_FINITE",
        "TPC355_PANEL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_648_ROWS",
        "TPC355_RAW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_648_ROWS",
        "TPC355_NORMALIZED_REPLAY = NUMERICALLY_CERTIFIED_FINITE_648_ROWS",
        "TPC355_ALL_PLUS_FLOOR_REPAIR = NUMERICALLY_CERTIFIED_FINITE_PARTIAL",
        "TPC355_ALL_PLUS_MEAN_REPAIR = REFUTED_SCOPED",
        "TPC355_ALL_LAW_POSITIVE_ALIGNMENT = REFUTED_SCOPED",
        "TPC355_SOURCE_UNIFORM_L2 = OPEN",
        "TPC355_ARITHMETIC_ADVANCE = NO",
        "TPC355_FIXED_POWER_CREDIT = 0",
        "TPC355_FULL_GATE_B = OPEN",
        "TPC355_TWIN_PRIME_RESULT = NONE",
        "TPC355_STATUS = " + STATUS,
    )
    for marker in markers:
        need(marker in text, "bridge marker missing")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script), "--check"])
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
        print("TPC355_BRIDGE_CHECK=PASS panels=3 rows=648 "
              "raw_positive=647/648 normalized_positive=647/648 "
              "floor_drop_reduction=0.37754982894688971")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC355_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
