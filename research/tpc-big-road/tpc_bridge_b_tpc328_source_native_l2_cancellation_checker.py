#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-328."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-328-source-native-l2-cancellation"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc328_source_native_l2_cancellation.md"
PRODUCER = PROJECT / "code/tpc328_source_native_l2_cancellation.py"
INDEPENDENT = PROJECT / "experiments/tpc328_independent_checker.py"
STRESS = PROJECT / "experiments/tpc328_source_native_l2_stress.py"
CERTIFICATE = PROJECT / "results/tpc328_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / (
    "papers/tpc-327-three-origin-scale-triangulation/code/"
    "tpc327_three_origin_scale_triangulation.py")
PARENT_CERT = ROOT / (
    "papers/tpc-327-three-origin-scale-triangulation/results/"
    "tpc327_certificate.json")
V59_CODE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/code/"
    "tpc267_literal_residual_radius_certificate.py")
V59_CERT = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/results/"
    "tpc267_certificate.json")

STATUS = "NUMERICALLY_CERTIFIED_FINITE_SOURCE_NATIVE_L2_CANCELLATION_ATLAS"
SCHEMA = "TPC328_SOURCE_NATIVE_L2_CANCELLATION_V1"
PARENT_CODE_SHA256 = (
    "ddb5117b4533608a0f1ffb510f901d02d53ea6158c08d921aeced4f0c1653f47")
PARENT_CERT_SHA256 = (
    "1550f36b41c71dc09d68f220658a3fdf12f52822a4fd13fcebcf7aefea0f403f")
V59_CODE_SHA256 = (
    "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750")
V59_CERT_SHA256 = (
    "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9")

# These hashes are sealed only after every project file and this bridge text
# is final.  The checker intentionally refuses to run while any is open.
PRODUCER_SHA256 = "d9e0e534d8cf5f75172cdb55ecd872cf74cb6ed2e4b13782cccb5c645843e1c9"
INDEPENDENT_SHA256 = "2855d668ab3f20e238269939b525343769af8cb709d2145f9c5df6b5f306e611"
STRESS_SHA256 = "7280a1b329721673f4c17145fb5f1354e45ab86d60a765a536d468b9d2b94801"
CERTIFICATE_SHA256 = "0b772ad7810b282a2961f82f7e0ff5d11f0844e60728669268e95188d31cfe4d"
BRIDGE_SHA256 = "d15e3046006943a9f4aa1c005a6bfe2c5415a136bb5cb6969f3b3b0d50ce1046"

REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc328_source_native_l2_cancellation.py",
    "experiments/tpc328_independent_checker.py",
    "experiments/tpc328_source_native_l2_stress.py",
    "results/tpc328_certificate.json", "notes/theorem_ledger.md",
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
        "TPC327_producer_sha256": PARENT_CODE_SHA256,
        "TPC327_certificate_sha256": PARENT_CERT_SHA256,
        "TPC267_V59_producer_sha256": V59_CODE_SHA256,
        "TPC267_V59_certificate_sha256": V59_CERT_SHA256,
    }, "parent lock")

    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [12001, 16001, 20001] and
         protocol.get("scales") == [320, 640, 1280, 2560] and
         protocol.get("source_counts") == [160, 320, 640, 1280] and
         protocol.get("Q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("height") == 66 and
         protocol.get("comparison_cutoff") == 2 and
         protocol.get("euler_tail_cutoff") == 50000, "protocol")

    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 96, "row census")
    expected = {
        "all_plus": {"NEGATIVE_OFF_DIAGONAL": 81,
                     "POSITIVE_OFF_DIAGONAL": 15, "UNRESOLVED": 0},
        "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 73,
                              "POSITIVE_OFF_DIAGONAL": 23, "UNRESOLVED": 0},
        "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 74,
                           "POSITIVE_OFF_DIAGONAL": 22, "UNRESOLVED": 0},
        "half_split": {"NEGATIVE_OFF_DIAGONAL": 61,
                       "POSITIVE_OFF_DIAGONAL": 35, "UNRESOLVED": 0},
    }
    counts = {name: {label: 0 for label in next(iter(expected.values()))}
              for name in expected}
    keys = set()
    for row in rows:
        key = (row.get("origin"), row.get("scale"), row.get("Q"),
               row.get("kernel_exponent"))
        need(key not in keys, "duplicate row")
        keys.add(key)
        need(row.get("source_interval") == [
            row["origin"], row["origin"] + row["scale"] // 2 - 1],
             "source interval")
        need(row.get("source_count") == row["scale"] // 2 and
             row.get("operator_shape") ==
             [row["scale"] // 2, row["scale"] // 2],
             "row shape")
        for name in expected:
            label = row["laws"][name].get("classification")
            need(label in counts[name], "unknown row label")
            counts[name][label] += 1
        controls = row["component_controls_all_plus"]
        need(controls["lambda"].get("classification") ==
             "POSITIVE_OFF_DIAGONAL" and
             controls["comparison"].get("classification") ==
             "POSITIVE_OFF_DIAGONAL", "component controls")
    need(keys == {(o, n, q, s) for o in (12001, 16001, 20001)
                  for n in (320, 640, 1280, 2560)
                  for q in (24, 36, 54, 80) for s in (1, 2)} and
         counts == expected, "finite census")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 96 and audit.get("origins") == 3 and
         audit.get("scales") == 4 and
         audit.get("all_plus_negative_off_diagonal") == 81 and
         audit.get("all_plus_positive_off_diagonal") == 15 and
         audit.get("component_lambda_positive_controls") == 96 and
         audit.get("component_comparison_positive_controls") == 96 and
         audit.get("fixed_power_credit") == 0, "finite audit")

    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [20001, 20016] and
         anchor.get("Q") == 4 and anchor.get("shell") == [5, 7] and
         anchor.get("identity_exact") is True and
         anchor.get("energy_digest") ==
         "34a3720cc5edefae7d277fc91ac90846886a54860e76653f57ad5d7ea08241a1" and
         anchor.get("coordinate_diagonal_digest") ==
         "471ba6760b9567f1619c5e1a785c47b727c4b0a78488f9e9337085bbab33b262" and
         anchor.get("off_diagonal_digest") ==
         "cc7a9f5f61dea745d57fb30e041decb28a79afac5c383d87838b4d1f57738074",
         "exact anchor")

    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC328_EXACT_GRAM_DECOMPOSITION") ==
         "PROVED_EXACT_FINITE" and
         firewall.get("TPC328_SOURCE_NATIVE_VECTOR") ==
         "PROVED_EXACT_FINITE_DECLARED_MODEL" and
         firewall.get("TPC328_COMPONENT_CONTROLS") ==
         "NUMERICALLY_CERTIFIED_FINITE_96_OF_96" and
         firewall.get("TPC328_ALL_PLUS_CANCELLATION") ==
         "NUMERICALLY_CERTIFIED_FINITE_81_OF_96" and
         firewall.get("TPC328_ALL_PLUS_OBSTRUCTION") ==
         "NUMERICALLY_CERTIFIED_FINITE_15_OF_96" and
         firewall.get("TPC328_NO_UNIFORM_SIGNED_CONTRACTION") ==
         "REFUTED_SCOPED_FOUR_DECLARED_LAWS" and
         firewall.get("TPC328_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC328_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC328_GROWING_SOURCE_NATIVE_L2") == "OPEN" and
         firewall.get("TPC328_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC328_TWIN_PRIME_RESULT") == "NONE", "firewall")

    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")
    need(PDF.read_bytes().startswith(b"%PDF-") and
         len(PDF.read_bytes()) > 100_000, "PDF integrity")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error"):
        need(bad not in log, "LaTeX diagnostic: " + bad)


def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC328_MAXIMUM_CLAIM = " + STATUS,
        "TPC328_EXACT_GRAM_DECOMPOSITION = PROVED_EXACT_FINITE",
        "TPC328_SOURCE_NATIVE_VECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC328_COMPONENT_CONTROLS = NUMERICALLY_CERTIFIED_FINITE_96_OF_96",
        "TPC328_ALL_PLUS_CANCELLATION = NUMERICALLY_CERTIFIED_FINITE_81_OF_96",
        "TPC328_ALL_PLUS_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_15_OF_96",
        "TPC328_NO_UNIFORM_SIGNED_CONTRACTION = REFUTED_SCOPED_FOUR_DECLARED_LAWS",
        "TPC328_ARITHMETIC_ADVANCE = NO",
        "TPC328_FIXED_POWER_CREDIT = 0",
        "TPC328_GROWING_SOURCE_NATIVE_L2 = OPEN",
        "TPC328_FULL_GATE_B = OPEN",
        "TPC328_TWIN_PRIME_RESULT = NONE",
        "TPC328_STATUS = " + STATUS,
        "TPC328_ROUND2_CLUE = TEST_SOURCE_NATIVE_L2_ON_GROWING_ORIGIN_ENSEMBLE_OR_PROVE_SIGNED_GRAM_BOUND",
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
        print("TPC328_BRIDGE_CHECK=PASS rows=96 laws=4 "
              "all_plus_negative=81 all_plus_positive=15 components=96/96 "
              "exact_anchor=1")
    except (Failure, DuplicateKey, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError) as error:
        print("TPC328_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
