#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-321."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-321-cross-shell-profile-stability"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc321_cross_shell_profile.md"
PRODUCER = PROJECT / "code/tpc321_cross_shell_profile.py"
INDEPENDENT = PROJECT / "experiments/tpc321_independent_checker.py"
STRESS = PROJECT / "experiments/tpc321_profile_stress.py"
CERTIFICATE = PROJECT / "results/tpc321_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"

STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_SHELL_PROFILE_SEPARATION_AUDIT"
SCHEMA = "TPC321_CROSS_SHELL_PROFILE_STABILITY_V1"
PARENT_SHA256 = (
    "e8f272423fc14a1d5396549ced921eb66aeae28fbfc978e141230f1d1b0e6230")

# These hashes are sealed after all TPC-321 artifacts and bridge text are final.
PRODUCER_SHA256 = "1adaa6711d56fe5109180ee8f887a23bf00d8b49c9bfe8e4ea6f173d7c42d0f8"
INDEPENDENT_SHA256 = "7b74ad9ded9380bbac2901bdb6353765a832a30e825eab05b16a4b1c10681c7e"
STRESS_SHA256 = "86023f42f0bcae0455d35e3b2b23205576716e672b1248f9f1d6fa0e5f5f7a63"
CERTIFICATE_SHA256 = "f7048edce7260bceb14acc674311ce0268fb5ae4fdb9914edc0138a5cb7cc6be"
BRIDGE_SHA256 = "cc43777938a14a4fc844e341d23d608eed7ef8a1b1fd51383dbc8f48d97295ab"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md",
    "code/tpc321_cross_shell_profile.py",
    "experiments/tpc321_independent_checker.py",
    "experiments/tpc321_profile_stress.py",
    "results/tpc321_certificate.json", "notes/theorem_ledger.md",
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


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script), "--check"]
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
    need(payload.get("schema") == SCHEMA, "payload schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "certificate payload digest")
    need(payload.get("parent_lock", {}).get("certificate_sha256") ==
         PARENT_SHA256, "parent lock")

    protocol = payload.get("protocol", {})
    need(protocol.get("source_scales") == [640, 1280, 2560] and
         protocol.get("height") == 66 and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("profile") == "p_j=lambda_j/tr(G), descending" and
         protocol.get("comparison_axis") ==
         "adjacent Q shells at fixed X and exponent" and
         protocol.get("profile_paths") ==
         ["numpy_forward", "numpy_reverse", "scipy_forward"],
         "protocol")
    thresholds = protocol.get("distance_thresholds", {})
    need(float(thresholds.get("tv_lower")) == 0.03 and
         float(thresholds.get("lorenz_ks_lower")) == 0.02,
         "distance thresholds")

    audit = payload.get("finite_audit", {})
    need(audit.get("scales") == 3 and audit.get("rows") == 24 and
         audit.get("adjacent_Q_pairs") == 3 and
         audit.get("comparisons") == 18 and
         audit.get("profile_separation_strict") == 18 and
         audit.get("majorization_counts") ==
         {"P_MAJORIZES_Q": 3, "Q_MAJORIZES_P": 2, "MIXED": 13} and
         audit.get("uniform_shell_profile") == "REFUTED_FINITE_PANEL" and
         audit.get("uniform_majorization_direction") ==
         "REFUTED_FINITE_PANEL" and audit.get("fixed_power_credit") == 0,
         "audit")
    need(float(audit["tv_lower_min"]) > 0.03 and
         float(audit["lorenz_ks_lower_min"]) > 0.02,
         "audit lower endpoints")

    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC321_PROFILE_SEPARATION") ==
         "NUMERICALLY_CERTIFIED_FINITE_18_OF_18" and
         firewall.get("TPC321_TV_SEPARATION") ==
         "NUMERICALLY_CERTIFIED_FINITE_ALL_GT_0_03" and
         firewall.get("TPC321_LORENZ_KS_SEPARATION") ==
         "NUMERICALLY_CERTIFIED_FINITE_ALL_GT_0_02" and
         firewall.get("TPC321_MAJORISATION_PATTERN") ==
         "NUMERICAL_OBSERVATION_3_FORWARD_2_REVERSE_13_MIXED" and
         firewall.get("TPC321_UNIFORM_SHELL_PROFILE") ==
         "REFUTED_FINITE_PANEL" and
         firewall.get("TPC321_UNIFORM_MAJORISATION") ==
         "REFUTED_FINITE_PANEL" and
         firewall.get("TPC321_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC321_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC321_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC321_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")

    rows = payload.get("rows", [])
    need(len(rows) == 24, "row census")
    indexed = {}
    for row in rows:
        key = (row.get("scale"), row.get("Q"),
               row.get("kernel_exponent"))
        need(key not in indexed and key[0] in [640, 1280, 2560] and
             key[1] in [24, 36, 54, 80] and key[2] in [1, 2],
             "row key")
        need(row.get("source_count") == key[0] // 2 and
             row.get("source_interval") == [key[0] // 2 + 1, key[0]] and
             row.get("profile_dimension") == key[0] // 2 and
             len(row.get("profile_digests", {})) == 3,
             "row geometry/profile")
        agreement = row.get("path_agreement", {})
        need(float(agreement["l1_max"]) < 1e-7 and
             float(agreement["lorenz_ks_max"]) < 1e-7,
             "path agreement")
        indexed[key] = row

    comparisons = payload.get("comparisons", [])
    need(len(comparisons) == 18, "comparison census")
    counts = {"P_MAJORIZES_Q": 0, "Q_MAJORIZES_P": 0, "MIXED": 0}
    for item in comparisons:
        low_key = (item.get("scale"), item.get("lower_Q"),
                   item.get("kernel_exponent"))
        high_key = (item.get("scale"), item.get("upper_Q"),
                    item.get("kernel_exponent"))
        need(low_key in indexed and high_key in indexed and
             high_key[1] > low_key[1] and
             item.get("strict_profile_separation") is True and
             item.get("scale_invariant_readout") is True,
             "comparison record")
        tv_low, tv_high = map(float, item["tv_interval"])
        ks_low, ks_high = map(float, item["lorenz_ks_interval"])
        tv_estimate = float(item["tv_estimate"])
        ks_estimate = float(item["lorenz_ks_estimate"])
        need(0.03 < tv_low <= tv_estimate <= tv_high <= 1 and
             0.02 < ks_low <= ks_estimate <= ks_high <= 1 and
             item.get("majorization") in counts and
             item.get("path_majorization_consensus") ==
             [item.get("majorization")], "comparison interval")
        counts[item["majorization"]] += 1
    need(counts == {"P_MAJORIZES_Q": 3, "Q_MAJORIZES_P": 2,
                    "MIXED": 13}, "comparison labels")

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
        "TPC321_MAXIMUM_CLAIM = " + STATUS,
        "TPC321_ROUTE_ADVANCE = YES_SCOPED_CROSS_SHELL_PROFILE_OBSTRUCTION",
        "TPC321_PROFILE_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_18_OF_18",
        "TPC321_TV_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_ALL_GT_0_03",
        "TPC321_LORENZ_KS_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_ALL_GT_0_02",
        "TPC321_MAJORISATION_PATTERN = NUMERICAL_OBSERVATION_3_FORWARD_2_REVERSE_13_MIXED",
        "TPC321_UNIFORM_SHELL_PROFILE = REFUTED_FINITE_PANEL",
        "TPC321_UNIFORM_MAJORISATION = REFUTED_FINITE_PANEL",
        "TPC321_ARITHMETIC_ADVANCE = NO",
        "TPC321_FIXED_POWER_CREDIT = 0",
        "TPC321_FULL_GATE_B = OPEN",
        "TPC321_TWIN_PRIME_RESULT = NONE",
        "TPC321_ROUND2_CLUE = TEST_SIGNED_PROJECTOR_REASSEMBLY_OR_PROVE_A_UNIFORM_SHELL_PROFILE_BOUND_BEFORE_ANY_ARITHMETIC_POWER_CLAIM",
    )
    for marker in markers:
        need(marker in text, "bridge marker")


def main() -> int:
    try:
        check_files()
        check_bridge_text()
        outputs = []
        for script in (PRODUCER, INDEPENDENT, STRESS):
            normal = run(script, False)
            optimized = run(script, True)
            need(normal == optimized, script.name + " optimized mismatch")
            outputs.append(normal)
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print("TPC321_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC321_BRIDGE_CHECK=PASS rows=24 comparisons=18 "
          "profile_separation=18 tv_gt_003=18 ks_gt_002=18 "
          "majorization=3/2/13 fixed_power_credit=0")
    print("claim_level=" + STATUS)
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
