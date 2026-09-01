#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-330.

The bridge verifies the release manifest, certificate schema and headline
counts, then runs producer/independent/stress checks in normal and optimized
modes and requires byte-identical stdout with empty stderr.  It is a local
fallback because the Session-named Route-A/Route-B evaluator files are not in
this checkout.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-330-multi-permutation-response-spectrum"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc330_multi_permutation_response_spectrum.md")
PRODUCER = PROJECT / (
    "code/tpc330_multi_permutation_response_spectrum.py")
INDEPENDENT = PROJECT / "experiments/tpc330_independent_checker.py"
STRESS = PROJECT / "experiments/tpc330_multi_permutation_stress.py"
CERTIFICATE = PROJECT / "results/tpc330_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / (
    "papers/tpc-329-heldout-growing-source-native-audit/code/"
    "tpc329_heldout_growing_source_native_audit.py")
PARENT_CERT = ROOT / (
    "papers/tpc-329-heldout-growing-source-native-audit/results/"
    "tpc329_certificate.json")
V59_CODE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/code/"
    "tpc267_literal_residual_radius_certificate.py")
V59_CERT = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/results/"
    "tpc267_certificate.json")

STATUS = "NUMERICALLY_CERTIFIED_FINITE_MULTI_PERMUTATION_RESPONSE_SPECTRUM"
SCHEMA = "TPC330_MULTI_PERMUTATION_RESPONSE_SPECTRUM_V1"
PARENT_CODE_SHA256 = (
    "7f4155d2d24f0062ef358cb496d274afa9295831cb982f06454e6ce2464e3adb")
PARENT_CERT_SHA256 = (
    "38999e2aeda85f53bb4318de89361893cc08bf6c80f39c534cd7e33b1ef0b958")
V59_CODE_SHA256 = (
    "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750")
V59_CERT_SHA256 = (
    "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9")

# Filled after all TPC-330 source and bridge text is final.
PRODUCER_SHA256 = "d9bd669bfde610a8caeaa5253c71486323b6c84ad2c783d424fc65a3a56915b5"
INDEPENDENT_SHA256 = "6765eb8c34c020287ded68c532516a8d359b138f0dece614acd5e0eafdefec65"
STRESS_SHA256 = "a881ad5e6d49d11806aa8bbd6d0abb203cbe654f427d0ed382f508a227bdab43"
CERTIFICATE_SHA256 = "5ade3c1429589fbf84660414f459e99c5de8694229e2f3a49de9540a04573097"
BRIDGE_SHA256 = "a17bf07899b58eaf8f37fae4f6dc37eb32576799a99be3e250f8555f8c2561e3"

CONTROL_NAMES = ("identity", "affine_3_11", "affine_5_17",
                 "affine_7_29", "reversal")
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
PLACEMENT_RULE = (
    "five_predeclared_bijections: identity, affine_3_11, affine_5_17, "
    "affine_7_29, reversal")
EXPECTED_ACTUAL = {
    "all_plus": {"NEGATIVE_OFF_DIAGONAL": 31,
                 "POSITIVE_OFF_DIAGONAL": 1, "UNRESOLVED": 0},
    "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 25,
                          "POSITIVE_OFF_DIAGONAL": 7, "UNRESOLVED": 0},
    "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                       "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
    "half_split": {"NEGATIVE_OFF_DIAGONAL": 32,
                   "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
}
EXPECTED_CONTROLS = {
    "identity": EXPECTED_ACTUAL,
    "affine_3_11": {
        "all_plus": {"NEGATIVE_OFF_DIAGONAL": 0,
                     "POSITIVE_OFF_DIAGONAL": 32, "UNRESOLVED": 0},
        "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 20,
                               "POSITIVE_OFF_DIAGONAL": 12,
                               "UNRESOLVED": 0},
        "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 27,
                            "POSITIVE_OFF_DIAGONAL": 5,
                            "UNRESOLVED": 0},
        "half_split": {"NEGATIVE_OFF_DIAGONAL": 31,
                        "POSITIVE_OFF_DIAGONAL": 1,
                        "UNRESOLVED": 0},
    },
    "affine_5_17": {
        "all_plus": {"NEGATIVE_OFF_DIAGONAL": 0,
                     "POSITIVE_OFF_DIAGONAL": 32, "UNRESOLVED": 0},
        "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 30,
                               "POSITIVE_OFF_DIAGONAL": 2,
                               "UNRESOLVED": 0},
        "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                            "POSITIVE_OFF_DIAGONAL": 0,
                            "UNRESOLVED": 0},
        "half_split": {"NEGATIVE_OFF_DIAGONAL": 28,
                        "POSITIVE_OFF_DIAGONAL": 4,
                        "UNRESOLVED": 0},
    },
    "affine_7_29": {
        "all_plus": {"NEGATIVE_OFF_DIAGONAL": 0,
                     "POSITIVE_OFF_DIAGONAL": 32, "UNRESOLVED": 0},
        "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 21,
                               "POSITIVE_OFF_DIAGONAL": 11,
                               "UNRESOLVED": 0},
        "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                            "POSITIVE_OFF_DIAGONAL": 0,
                            "UNRESOLVED": 0},
        "half_split": {"NEGATIVE_OFF_DIAGONAL": 29,
                        "POSITIVE_OFF_DIAGONAL": 3,
                        "UNRESOLVED": 0},
    },
    "reversal": EXPECTED_ACTUAL,
}


class Failure(RuntimeError):
    pass


class DuplicateKey(ValueError):
    pass


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey(key)
        result[key] = value
    return result


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
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script), "--check"]
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["OMP_NUM_THREADS"] = "1"
    environment["OPENBLAS_NUM_THREADS"] = "1"
    environment["MKL_NUM_THREADS"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    required = (
        ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
        "PROOF_PACKAGE.md", "code/tpc330_multi_permutation_response_spectrum.py",
        "experiments/tpc330_independent_checker.py",
        "experiments/tpc330_multi_permutation_stress.py",
        "results/tpc330_certificate.json", "notes/theorem_ledger.md",
        "notes/claim_firewall.md", "notes/computational_protocol.md",
        "notes/route_evaluation.md", "notes/citation_verification.md",
        "paper/main.tex", "paper/references.bib", "paper/main.pdf",
        "paper/paper.pdf", "paper/compile.log",
    )
    for relative in required:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
    for path, expected, label in (
            (PRODUCER, PRODUCER_SHA256, "producer"),
            (INDEPENDENT, INDEPENDENT_SHA256, "independent checker"),
            (STRESS, STRESS_SHA256, "stress checker"),
            (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
            (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(len(expected) == 64 and not expected.startswith("__"),
             label + " hash not sealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent producer provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "parent certificate provenance")
    need(digest(V59_CODE.read_bytes()) == V59_CODE_SHA256,
         "V59 producer provenance")
    need(digest(V59_CERT.read_bytes()) == V59_CERT_SHA256,
         "V59 certificate provenance")

    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw, object_pairs_hook=no_duplicates)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    need(payload.get("parent_lock") == {
        "TPC329_producer_sha256": PARENT_CODE_SHA256,
        "TPC329_certificate_sha256": PARENT_CERT_SHA256,
        "TPC267_V59_producer_sha256": V59_CODE_SHA256,
        "TPC267_V59_certificate_sha256": V59_CERT_SHA256,
    }, "parent lock")

    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [28001, 36001] and
         protocol.get("scales") == [4096, 8192] and
         protocol.get("source_counts") == [2048, 4096] and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("height") == 66 and
         protocol.get("comparison_cutoff") == 2 and
         protocol.get("euler_tail_cutoff") == 50000 and
         protocol.get("placement_null") == {
             "rule": PLACEMENT_RULE,
             "preserves_source_multiset": True,
             "controls": [
                 {"name": "identity", "multiplier": 1, "offset": 0,
                  "rule": "pi_0(i)=i"},
                 {"name": "affine_3_11", "multiplier": 3, "offset": 11,
                  "rule": "pi_3,11(i)=(3*i+11) mod source_count"},
                 {"name": "affine_5_17", "multiplier": 5, "offset": 17,
                  "rule": "pi_5,17(i)=(5*i+17) mod source_count"},
                 {"name": "affine_7_29", "multiplier": 7, "offset": 29,
                  "rule": "pi_7,29(i)=(7*i+29) mod source_count"},
                 {"name": "reversal", "multiplier": -1, "offset": -1,
                  "rule": "pi_rev(i)=source_count-1-i"},
             ],
         }, "protocol")
    need(payload.get("round2_clue") ==
         "DECOMPOSE_POSITION_RESPONSE_INTO_AFFINE_REVERSAL_AND_SOURCE_ALIGNED_COMPONENTS",
         "round2 clue")

    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 32, "row census")
    keys = {(row.get("origin"), row.get("scale"), row.get("Q"),
             row.get("kernel_exponent")) for row in rows}
    need(keys == {(origin, scale, q0, exponent)
                  for origin in (28001, 36001) for scale in (4096, 8192)
                  for q0 in (24, 36, 54, 80) for exponent in (1, 2)},
         "row keys")
    need({law: {label: sum(row["laws"][law]["classification"] == label
                           for row in rows)
                for label in ("NEGATIVE_OFF_DIAGONAL",
                              "POSITIVE_OFF_DIAGONAL", "UNRESOLVED")}
          for law in LAW_NAMES} == EXPECTED_ACTUAL, "actual census")

    placement = payload.get("placement_audit", {})
    need(placement.get("rule") == PLACEMENT_RULE and
         placement.get("controls") == list(CONTROL_NAMES) and
         placement.get("control_count") == 5 and
         placement.get("rows") == 32 and
         placement.get("law_observations") == 640 and
         placement.get("comparisons") == 640 and
         placement.get("source_l2_norm_equal_rows") == 160 and
         placement.get("all_plus_affine_positive_rows") == 32 and
         placement.get("all_plus_affine_consensus_rows") == 32 and
         placement.get("all_plus_identity_reversal_same_rows") == 32,
         "placement audit header")
    summaries = placement.get("control_summaries", {})
    need(set(summaries) == set(CONTROL_NAMES), "control summary keys")
    need({name: summaries[name].get("classification_census")
          for name in CONTROL_NAMES} == EXPECTED_CONTROLS,
         "control census")
    need(isinstance(placement.get("details"), list) and
         len(placement["details"]) == 640 and
         isinstance(placement.get("law_spectrum"), dict) and
         set(placement["law_spectrum"]) == set(LAW_NAMES) and
         isinstance(placement.get("pairwise_controls"), dict) and
         len(placement["pairwise_controls"]) == 10,
         "placement summaries")

    growth = payload.get("growth_audit", {})
    need(growth.get("small_scale") == 4096 and
         growth.get("large_scale") == 8192 and growth.get("pairs") == 64 and
         growth.get("all_plus_sign_persistent_pairs") == 15 and
         growth.get("all_plus_sign_crossings") == 1 and
         len(growth.get("pairs_detail", [])) == 64, "growth audit")

    finite = payload.get("finite_audit", {})
    need(finite.get("rows") == 32 and
         finite.get("component_lambda_positive_controls") == 32 and
         finite.get("component_comparison_positive_controls") == 32 and
         finite.get("fixed_power_credit") == 0, "finite audit")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [36001, 36016] and
         anchor.get("Q") == 4 and anchor.get("shell") == [5, 7] and
         anchor.get("identity_exact") is True, "exact anchor")

    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC330_EXACT_GRAM_DECOMPOSITION") ==
         "PROVED_EXACT_FINITE" and
         firewall.get("TPC330_SOURCE_NATIVE_VECTOR") ==
         "PROVED_EXACT_FINITE_DECLARED_MODEL" and
         firewall.get("TPC330_COMPONENT_CONTROLS") ==
         "NUMERICALLY_CERTIFIED_FINITE_32_OF_32" and
         firewall.get("TPC330_MULTI_PERMUTATION_SPECTRUM") ==
         "NUMERICALLY_CERTIFIED_FINITE_5_CONTROLS" and
         firewall.get("TPC330_AFFINE_ALL_PLUS_CONSENSUS") ==
         "NUMERICALLY_CERTIFIED_FINITE_32_OF_32" and
         firewall.get("TPC330_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC330_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC330_GROWING_SOURCE_NATIVE_L2") == "OPEN" and
         firewall.get("TPC330_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC330_TWIN_PRIME_RESULT") == "NONE",
         "firewall")

    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")
    pdf_bytes = PDF.read_bytes()
    need(pdf_bytes.startswith(b"%PDF-") and len(pdf_bytes) > 100_000,
         "PDF integrity")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error"):
        need(bad not in log, "LaTeX diagnostic: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC330_MAXIMUM_CLAIM = " + STATUS,
        "TPC330_EXACT_GRAM_DECOMPOSITION = PROVED_EXACT_FINITE",
        "TPC330_SOURCE_NATIVE_VECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC330_COMPONENT_CONTROLS = NUMERICALLY_CERTIFIED_FINITE_32_OF_32",
        "TPC330_MULTI_PERMUTATION_SPECTRUM = NUMERICALLY_CERTIFIED_FINITE_5_CONTROLS",
        "TPC330_AFFINE_ALL_PLUS_CONSENSUS = NUMERICALLY_CERTIFIED_FINITE_32_OF_32",
        "TPC330_SIGN_AT_SCALE_GROWTH = NUMERICALLY_CERTIFIED_FINITE",
        "TPC330_ARITHMETIC_ADVANCE = NO",
        "TPC330_FIXED_POWER_CREDIT = 0",
        "TPC330_GROWING_SOURCE_NATIVE_L2 = OPEN",
        "TPC330_FULL_GATE_B = OPEN",
        "TPC330_TWIN_PRIME_RESULT = NONE",
        "TPC330_STATUS = " + STATUS,
        "TPC330_ROUND2_CLUE = DECOMPOSE_POSITION_RESPONSE_INTO_AFFINE_REVERSAL_AND_SOURCE_ALIGNED_COMPONENTS",
    )
    for marker in markers:
        need(marker in text, "bridge marker missing")


def main() -> int:
    try:
        check_files()
        check_bridge_text()
        normal = (run(PRODUCER, False), run(INDEPENDENT, False),
                  run(STRESS, False))
        optimized = (run(PRODUCER, True), run(INDEPENDENT, True),
                     run(STRESS, True))
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC330_BRIDGE_CHECK=PASS rows=32 laws=4 growth_pairs=64 "
              "placement_controls=5 placement_comparisons=640 "
              "affine_all_plus=32/32 identity_reversal=32/32 "
              "exact_anchor=1")
    except (Failure, DuplicateKey, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError) as error:
        print("TPC330_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
