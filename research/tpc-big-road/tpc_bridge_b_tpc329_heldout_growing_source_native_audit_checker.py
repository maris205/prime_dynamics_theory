#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-329."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-329-heldout-growing-source-native-audit"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc329_heldout_growing_source_native_audit.md")
PRODUCER = PROJECT / (
    "code/tpc329_heldout_growing_source_native_audit.py")
INDEPENDENT = PROJECT / "experiments/tpc329_independent_checker.py"
STRESS = PROJECT / "experiments/tpc329_heldout_growing_stress.py"
CERTIFICATE = PROJECT / "results/tpc329_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / (
    "papers/tpc-328-source-native-l2-cancellation/code/"
    "tpc328_source_native_l2_cancellation.py")
PARENT_CERT = ROOT / (
    "papers/tpc-328-source-native-l2-cancellation/results/"
    "tpc328_certificate.json")
V59_CODE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/code/"
    "tpc267_literal_residual_radius_certificate.py")
V59_CERT = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/results/"
    "tpc267_certificate.json")

STATUS = "NUMERICALLY_CERTIFIED_FINITE_HELDOUT_GROWING_SOURCE_NATIVE_AUDIT"
SCHEMA = "TPC329_HELDOUT_GROWING_SOURCE_NATIVE_AUDIT_V1"
PARENT_CODE_SHA256 = (
    "d9e0e534d8cf5f75172cdb55ecd872cf74cb6ed2e4b13782cccb5c645843e1c9")
PARENT_CERT_SHA256 = (
    "0b772ad7810b282a2961f82f7e0ff5d11f0844e60728669268e95188d31cfe4d")
V59_CODE_SHA256 = (
    "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750")
V59_CERT_SHA256 = (
    "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9")

# Sealed after the project and bridge text are final.
PRODUCER_SHA256 = "7f4155d2d24f0062ef358cb496d274afa9295831cb982f06454e6ce2464e3adb"
INDEPENDENT_SHA256 = "a8c2572a64899a8eb7654ee80499986be149dd4b37dfa7cfcbf4908778b1d499"
STRESS_SHA256 = "ce2ec81f7b329933b4a0bd07d886f55514805c068f1615b443f787226c106aff"
CERTIFICATE_SHA256 = "38999e2aeda85f53bb4318de89361893cc08bf6c80f39c534cd7e33b1ef0b958"
BRIDGE_SHA256 = "776518130807a3648fcb45bc10d6c61f448535c92e4235635aa20b8d780acfd2"

PLACEMENT_RULE = "pi(i)=(5*i+17) mod source_count"
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
EXPECTED_PERMUTED = {
    "all_plus": {"NEGATIVE_OFF_DIAGONAL": 0,
                 "POSITIVE_OFF_DIAGONAL": 32, "UNRESOLVED": 0},
    "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 30,
                          "POSITIVE_OFF_DIAGONAL": 2, "UNRESOLVED": 0},
    "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                       "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
    "half_split": {"NEGATIVE_OFF_DIAGONAL": 28,
                   "POSITIVE_OFF_DIAGONAL": 4, "UNRESOLVED": 0},
}
LAW_NAMES = tuple(EXPECTED_ACTUAL)
LABELS = ("NEGATIVE_OFF_DIAGONAL", "POSITIVE_OFF_DIAGONAL", "UNRESOLVED")

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc329_heldout_growing_source_native_audit.py",
    "experiments/tpc329_independent_checker.py",
    "experiments/tpc329_heldout_growing_stress.py",
    "results/tpc329_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/citation_verification.md",
    "paper/main.tex", "paper/references.bib", "paper/main.pdf",
    "paper/paper.pdf", "paper/compile.log",
)


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
    for relative in REQUIRED:
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
        "TPC328_producer_sha256": PARENT_CODE_SHA256,
        "TPC328_certificate_sha256": PARENT_CERT_SHA256,
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
             "rule": PLACEMENT_RULE, "multiplier": 5, "offset": 17,
             "preserves_source_multiset": True,
         }, "protocol")
    need(payload.get("round2_clue") ==
         "SEPARATE_SOURCE_NORM_FROM_ARITHMETIC_PLACEMENT_WITH_MULTIPLE_PREDECLARED_CONTROLS",
         "round2 clue")

    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 32, "row census")
    counts = {law: {label: 0 for label in LABELS} for law in LAW_NAMES}
    placement_counts = {law: {label: 0 for label in LABELS}
                        for law in LAW_NAMES}
    keys = set()
    for row in rows:
        key = (row.get("origin"), row.get("scale"), row.get("Q"),
               row.get("kernel_exponent"))
        need(key not in keys, "duplicate row")
        keys.add(key)
        origin, scale, q0, exponent = key
        need(row.get("source_interval") == [
            origin, origin + scale // 2 - 1] and
             row.get("source_count") == scale // 2 and
             row.get("operator_shape") == [scale // 2, scale // 2] and
             row.get("height") == 66, "row geometry")
        for law in LAW_NAMES:
            actual = row["laws"][law]
            label = actual.get("classification")
            need(label in LABELS, "unknown actual row label")
            counts[law][label] += 1
            placement = row["placement_control"]
            need(placement.get("rule") == PLACEMENT_RULE and
                 placement.get("multiplier") == 5 and
                 placement.get("offset") == 17 and
                 placement.get("bijection") is True and
                 placement.get("source_l2_norm_equal") is True,
                 "placement row metadata")
            plabel = placement["laws"][law].get("classification")
            need(plabel in LABELS, "unknown placement row label")
            placement_counts[law][plabel] += 1
        controls = row["component_controls_all_plus"]
        need(controls["lambda"].get("classification") ==
             "POSITIVE_OFF_DIAGONAL" and
             controls["comparison"].get("classification") ==
             "POSITIVE_OFF_DIAGONAL", "component controls")
    need(keys == {(o, n, q, s) for o in (28001, 36001)
                  for n in (4096, 8192)
                  for q in (24, 36, 54, 80) for s in (1, 2)} and
         counts == EXPECTED_ACTUAL and placement_counts == EXPECTED_PERMUTED,
         "finite census")

    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 32 and audit.get("origins") == 2 and
         audit.get("scales") == 2 and
         audit.get("component_lambda_positive_controls") == 32 and
         audit.get("component_comparison_positive_controls") == 32 and
         audit.get("fixed_power_credit") == 0, "finite audit")

    growth = payload.get("growth_audit", {})
    need(growth.get("small_scale") == 4096 and
         growth.get("large_scale") == 8192 and
         growth.get("pairs") == 64 and
         growth.get("all_plus_sign_persistent_pairs") == 15 and
         growth.get("all_plus_sign_crossings") == 1 and
         isinstance(growth.get("pairs_detail"), list) and
         len(growth["pairs_detail"]) == 64, "growth audit")

    placement = payload.get("placement_audit", {})
    need(placement.get("rule") == PLACEMENT_RULE and
         placement.get("multiplier") == 5 and
         placement.get("offset") == 17 and
         placement.get("comparisons") == 128 and
         placement.get("all_plus_comparisons") == 32 and
         placement.get("source_l2_norm_equal_rows") == 32 and
         placement.get("all_plus_classification_equal") == 1 and
         placement.get("all_plus_classification_changed") == 31 and
         placement.get("actual_classification_census") == EXPECTED_ACTUAL and
         placement.get("permuted_classification_census") ==
         EXPECTED_PERMUTED and
         isinstance(placement.get("details"), list) and
         len(placement["details"]) == 128, "placement audit")

    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [28001, 28016] and
         anchor.get("Q") == 4 and anchor.get("shell") == [5, 7] and
         anchor.get("identity_exact") is True and
         anchor.get("energy_digest") ==
         "031f9a525f90ab196de1ae14ab7fd421f714523729919e939ee213e0f1f73312" and
         anchor.get("coordinate_diagonal_digest") ==
         "2a6749e1d49aef201792a755454767d19ae2613049bbab2f8ed3ca898d5a6dc2" and
         anchor.get("off_diagonal_digest") ==
         "7dc1a942e30b9e242c9d3189f1aee7267f6f99e3276015f2fa80fc739e84dd63",
         "exact anchor")

    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC329_EXACT_GRAM_DECOMPOSITION") ==
         "PROVED_EXACT_FINITE" and
         firewall.get("TPC329_SOURCE_NATIVE_VECTOR") ==
         "PROVED_EXACT_FINITE_DECLARED_MODEL" and
         firewall.get("TPC329_COMPONENT_CONTROLS") ==
         "NUMERICALLY_CERTIFIED_FINITE_32_OF_32" and
         firewall.get("TPC329_SIGN_AT_SCALE_GROWTH") ==
         "NUMERICALLY_CERTIFIED_FINITE" and
         firewall.get("TPC329_PLACEMENT_NULL") ==
         "NUMERICALLY_CERTIFIED_FINITE_MULTISET_PRESERVING_CONTROL" and
         firewall.get("TPC329_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC329_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC329_GROWING_SOURCE_NATIVE_L2") == "OPEN" and
         firewall.get("TPC329_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC329_TWIN_PRIME_RESULT") == "NONE",
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
        "TPC329_MAXIMUM_CLAIM = " + STATUS,
        "TPC329_EXACT_GRAM_DECOMPOSITION = PROVED_EXACT_FINITE",
        "TPC329_SOURCE_NATIVE_VECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC329_COMPONENT_CONTROLS = NUMERICALLY_CERTIFIED_FINITE_32_OF_32",
        "TPC329_PLACEMENT_NULL = NUMERICALLY_CERTIFIED_FINITE_MULTISET_PRESERVING_CONTROL",
        "TPC329_ALL_PLUS_ACTUAL = NUMERICALLY_CERTIFIED_FINITE_31_NEGATIVE_1_POSITIVE",
        "TPC329_ALL_PLUS_PERMUTED = NUMERICALLY_CERTIFIED_FINITE_0_NEGATIVE_32_POSITIVE",
        "TPC329_PLACEMENT_CHANGES = NUMERICALLY_CERTIFIED_FINITE_31_OF_32",
        "TPC329_ARITHMETIC_ADVANCE = NO",
        "TPC329_FIXED_POWER_CREDIT = 0",
        "TPC329_GROWING_SOURCE_NATIVE_L2 = OPEN",
        "TPC329_FULL_GATE_B = OPEN",
        "TPC329_TWIN_PRIME_RESULT = NONE",
        "TPC329_STATUS = " + STATUS,
        "TPC329_ROUND2_CLUE = SEPARATE_SOURCE_NORM_FROM_ARITHMETIC_PLACEMENT_WITH_MULTIPLE_PREDECLARED_CONTROLS",
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
        print("TPC329_BRIDGE_CHECK=PASS rows=32 laws=4 growth_pairs=64 "
              "placement_comparisons=128 all_plus_actual=31/1 "
              "all_plus_permuted=0/32 components=32/32 exact_anchor=1")
    except (Failure, DuplicateKey, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError) as error:
        print("TPC329_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
