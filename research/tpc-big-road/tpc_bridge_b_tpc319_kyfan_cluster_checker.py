#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-319."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-319-kyfan-cluster-normalization-firewall"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc319_kyfan_cluster.md"
PRODUCER = PROJECT / "code/tpc319_kyfan_cluster_normalization.py"
INDEPENDENT = PROJECT / "experiments/tpc319_independent_checker.py"
STRESS = PROJECT / "experiments/tpc319_cluster_stress.py"
CERTIFICATE = PROJECT / "results/tpc319_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

STATUS = "NUMERICALLY_CERTIFIED_FINITE_KY_FAN_CLUSTER_NORMALIZATION_AUDIT"
SCHEMA = "TPC319_KY_FAN_CLUSTER_NORMALIZATION_FIREWALL_V1"
PARENT_SHA256 = (
    "2465c91d3dcc5edb24bd1cdc8d5cd0748ddfa28efa7e352c2edbffcee2229ffa")

# These hashes are sealed after all project artifacts are final.
PRODUCER_SHA256 = "d02cb9a7de86830a8f78ff05fca107334ebd64a6960a23f3b8aacf3fb9f550e3"
INDEPENDENT_SHA256 = "abeea517099124809e6f5f14fc01bad0dcffac34fd54da5b8b72f150e549e7e2"
STRESS_SHA256 = "02d3dbaa4278c0aca7ea1f1a39e5f916d071ede9df23a8c60e64aafb21836c7b"
CERTIFICATE_SHA256 = "3bd20dfa30870b3e163861a6f712354d50e712f3a61ac1080939327a2da6d4f7"
BRIDGE_SHA256 = "11195dc7e03b9dd34937411833bab5a9f57f7b52331f02c211cdc529b8a41161"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc319_kyfan_cluster_normalization.py",
    "experiments/tpc319_independent_checker.py",
    "experiments/tpc319_cluster_stress.py",
    "results/tpc319_certificate.json", "notes/theorem_ledger.md",
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


def run(script: Path, optimized: bool, flag: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script)]
    if flag:
        command.append("--check")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=PROJECT, env=environment,
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
    need(parent.get("certificate_sha256") == PARENT_SHA256, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("source_scales") == [640, 1280, 2560] and
         protocol.get("height") == 66 and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("cluster_sizes") == [1, 2, 4, 8, 16] and
         protocol.get("domain") == "ell^2(I_X)" and
         protocol.get("codomain") == "ell^2(S_Q x I_X)", "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("scales") == 3 and audit.get("rows") == 24 and
         audit.get("cluster_sizes") == [1, 2, 4, 8, 16] and
         audit.get("cluster_intervals") == 120 and
         audit.get("comparisons") == 80 and
         audit.get("normalized_decrease_strict") == 80 and
         audit.get("unnormalized_increase_strict") == 80 and
         audit.get("normalization_flip_transitions") == 80 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("uniform_normalization_law") == "OPEN", "audit")
    need(audit.get("edge_gap_counts_lt_0_01") ==
         {"1": 10, "2": 5, "4": 2, "8": 4, "16": 13},
         "gap census")
    for row in payload.get("rows", []):
        need(set(row.get("ky_fan", {})) == {"1", "2", "4", "8", "16"},
             "row cluster keys")
        for k in ("1", "2", "4", "8", "16"):
            guard = row["ky_fan"][k]
            need(guard.get("uniform_entry_bound") == "160" and
                 guard.get("model") ==
                 "binary64 dual solver plus finite Weyl guard, Ky Fan factor k",
                 "guard")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC319_KY_FAN_AUDIT") ==
         "NUMERICALLY_CERTIFIED_FINITE_24_ROWS_5_K" and
         firewall.get("TPC319_NORMALIZED_DECREASES") ==
         "NUMERICALLY_CERTIFIED_FINITE_80_OF_80" and
         firewall.get("TPC319_UNNORMALIZED_INCREASES") ==
         "NUMERICALLY_CERTIFIED_FINITE_80_OF_80" and
         firewall.get("TPC319_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC319_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC319_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC319_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(len(payload.get("comparisons", [])) == 80, "comparison census")
    for item in payload["comparisons"]:
        need(item.get("k") in [1, 2, 4, 8, 16] and
             item.get("strict_normalized_separation") is True and
             item.get("strict_unnormalized_separation") is True and
             1.0 < float(item["unnormalized_ratio"]) < 2.0,
             "comparison record")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")
    pdf = PDF.read_bytes()
    need(pdf.startswith(b"%PDF-") and len(pdf) > 100_000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error"):
        need(bad not in log, "LaTeX warning: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC319_MAXIMUM_CLAIM = " + STATUS,
        "TPC319_ROUTE_ADVANCE = YES_SCOPED_KY_FAN_CLUSTER_AND_NORMALIZATION_FIREWALL",
        "TPC319_KY_FAN_AUDIT = NUMERICALLY_CERTIFIED_FINITE_24_ROWS_5_K",
        "TPC319_NORMALIZED_DECREASES = NUMERICALLY_CERTIFIED_FINITE_80_OF_80",
        "TPC319_UNNORMALIZED_INCREASES = NUMERICALLY_CERTIFIED_FINITE_80_OF_80",
        "TPC319_NORMALIZATION_FLIP = PROVED_EXACT_FINITE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_80",
        "TPC319_CLUSTER_GAP_CENSUS = NUMERICAL_OBSERVATION_FINITE",
        "TPC319_EFFECTIVE_RANK = NUMERICAL_OBSERVATION_FINITE",
        "TPC319_ARITHMETIC_ADVANCE = NO",
        "TPC319_FIXED_POWER_CREDIT = 0",
        "TPC319_FULL_GATE_B = OPEN",
        "TPC319_TWIN_PRIME_RESULT = NONE",
        "TPC319_ROUND2_CLUE = "
        "AUDIT_A_SCALE_INVARIANT_SPECTRAL_MEASURE_OR_PROVE_A_SOURCE_"
        "NORMALIZATION_LAW_BEFORE_ANY_POWER_CLAIM",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


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
            json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print("TPC319_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC319_BRIDGE_CHECK=PASS rows=24 k_values=5 comparisons=80 "
          "normalized_decreases=80 unnormalized_increases=80 fixed_power_credit=0")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
