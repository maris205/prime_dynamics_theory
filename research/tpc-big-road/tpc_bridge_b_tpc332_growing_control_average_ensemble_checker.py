#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-332.

The checker validates the release manifest and then runs the producer,
independent replay, and stress suite in normal and optimized modes.  It is a
local fallback only: the Session-named Route-A/Route-B evaluators are not in
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
PROJECT = ROOT / "papers/tpc-332-growing-control-average-ensemble"
BRIDGE = ROOT / (
    "research/tpc-big-road/"
    "bridge_b_tpc332_growing_control_average_ensemble.md")
PRODUCER = PROJECT / "code/tpc332_growing_control_average_ensemble.py"
INDEPENDENT = PROJECT / "experiments/tpc332_independent_checker.py"
STRESS = PROJECT / "experiments/tpc332_growing_ensemble_stress.py"
CERTIFICATE = PROJECT / "results/tpc332_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / (
    "papers/tpc-331-control-average-centered-response-decomposition/code/"
    "tpc331_control_average_centered_response_decomposition.py")
PARENT_CERT = ROOT / (
    "papers/tpc-331-control-average-centered-response-decomposition/results/"
    "tpc331_certificate.json")
V59_CODE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/code/"
    "tpc267_literal_residual_radius_certificate.py")
V59_CERT = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/results/"
    "tpc267_certificate.json")

STATUS = "NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_AVERAGE_ENSEMBLE"
SCHEMA = "TPC332_GROWING_CONTROL_AVERAGE_ENSEMBLE_V1"
PARENT_CODE_SHA256 = (
    "c96095bd951d80e9147eeba99241761ba31a78b04a6b01bfcd120397f7e0eebc")
PARENT_CERT_SHA256 = (
    "eacd8b5e508956b362cbc0bb3c8da2b245a2155f91d8f48e794121f3e7a4997c")
V59_CODE_SHA256 = (
    "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750")
V59_CERT_SHA256 = (
    "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9")

# Filled only after the project source, certificate, stress checker, and
# bridge text are final.
PRODUCER_SHA256 = "ea742cfaaf7aa2be3c4cfad2ca603baadd65dc77619d8a1ba5ef686dd1fea5d9"
INDEPENDENT_SHA256 = "ad0efae28ce231637840483b97eae67da8bf93e5751322e1bff163691f0ef25d"
STRESS_SHA256 = "bc3f12ca61ec753ecbda0d5217f2b29d2270290e96e9cd9494cb27a083a24fcc"
CERTIFICATE_SHA256 = "ddb0c33d09edf648df9a32c0e7cec6e8bac638cae6aba895ebf8084da5d580b9"
BRIDGE_SHA256 = "c796a2f03db32e244f4a289497eb1a76cca07acfd1ec5a5c883e718556491990"


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


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script), "--check"]
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    # The release is deterministic under this fixed BLAS setting and is much
    # faster than the single-thread fallback on the 32-vCPU host.
    environment["OMP_NUM_THREADS"] = "8"
    environment["OPENBLAS_NUM_THREADS"] = "8"
    environment["MKL_NUM_THREADS"] = "8"
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    required = (
        ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
        "PROOF_PACKAGE.md", "code/tpc332_growing_control_average_ensemble.py",
        "experiments/tpc332_independent_checker.py",
        "experiments/tpc332_growing_ensemble_stress.py",
        "results/tpc332_certificate.json", "notes/theorem_ledger.md",
        "notes/claim_firewall.md", "notes/computational_protocol.md",
        "notes/route_evaluation.md", "notes/citation_verification.md",
        "paper/main.tex", "paper/references.bib", "paper/main.pdf",
        "paper/paper.pdf", "paper/compile.log")
    for relative in required:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
    for path, expected, label in (
            (PRODUCER, PRODUCER_SHA256, "producer"),
            (INDEPENDENT, INDEPENDENT_SHA256, "independent"),
            (STRESS, STRESS_SHA256, "stress"),
            (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
            (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(len(expected) == 64 and not expected.startswith("__"),
             label + " hash not sealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256 and
         digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256 and
         digest(V59_CODE.read_bytes()) == V59_CODE_SHA256 and
         digest(V59_CERT.read_bytes()) == V59_CERT_SHA256,
         "parent provenance")

    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw, object_pairs_hook=no_duplicates)
    need(raw == canonical(document) and document.get("certificate_version") == 1
         and document.get("claim_status") == STATUS,
         "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    need(payload.get("parent_lock") == {
        "TPC331_producer_sha256": PARENT_CODE_SHA256,
        "TPC331_certificate_sha256": PARENT_CERT_SHA256,
    }, "parent lock")
    finite = payload.get("finite_audit", {})
    need(finite.get("rows") == 48 and finite.get("origins") == 2 and
         finite.get("scales") == 3 and finite.get("laws") == 4 and
         finite.get("decomposition_observations") == 192 and
         finite.get("control_count") == 5 and
         finite.get("fixed_power_credit") == 0 and
         finite.get("arithmetic_advance") == "NO", "finite audit")
    source = payload.get("source_ensemble_audit", {})
    need(source.get("source_l2_observations") == 6 and
         len(source.get("windows", [])) == 6 and
         len(source.get("growth_pairs", [])) == 4 and
         source.get("all_plus_actual_census") == {
             "NEGATIVE_OFF_DIAGONAL": 27,
             "POSITIVE_OFF_DIAGONAL": 21,
             "UNRESOLVED": 0}, "source audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC332_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC332_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC332_GROWING_SOURCE_NATIVE_L2") == "OPEN" and
         firewall.get("TPC332_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC332_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
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
        "TPC332_EXACT_MEAN_CENTERED_DECOMPOSITION = PROVED_EXACT_FINITE",
        "TPC332_SOURCE_L2_IDENTITY = PROVED_EXACT_FINITE_FLOAT64_REPLAY",
        "TPC332_GROWING_ENSEMBLE = NUMERICALLY_CERTIFIED_FINITE_48_ROWS",
        "TPC332_CONTROL_AVERAGE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_48_OF_48",
        "TPC332_CENTERED_POSITION_CENSUS = NUMERICALLY_CERTIFIED_FINITE_48_OF_48",
        "TPC332_COHERENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_47_OF_48",
        "TPC332_ARITHMETIC_ADVANCE = NO",
        "TPC332_FIXED_POWER_CREDIT = 0",
        "TPC332_GROWING_SOURCE_NATIVE_L2 = OPEN",
        "TPC332_FULL_GATE_B = OPEN",
        "TPC332_TWIN_PRIME_RESULT = NONE",
        "TPC332_STATUS = " + STATUS,
        "TPC332_ROUND2_CLUE = SEPARATE_SOURCE_L2_CROSS_TERM_AND_TEST_CONTROL_COVARIANCE_SPECTRUM",
    )
    for marker in markers:
        need(marker in text, "bridge marker missing")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check_files()
        check_bridge_text()
        normal = tuple(run(script, False) for script in
                       (PRODUCER, INDEPENDENT, STRESS))
        optimized = tuple(run(script, True) for script in
                          (PRODUCER, INDEPENDENT, STRESS))
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC332_BRIDGE_CHECK=PASS rows=48 origins=2 scales=3 laws=4 "
              "decomposition_observations=192 source_windows=6 "
              "growth_pairs=4 control_count=5 exact_anchor=1")
    except (Failure, DuplicateKey, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError) as error:
        print("TPC332_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
