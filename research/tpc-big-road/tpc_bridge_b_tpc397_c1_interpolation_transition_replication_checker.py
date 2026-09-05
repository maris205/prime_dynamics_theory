#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for the TPC-397 release."""

from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-397-c1-interpolation-transition-replication"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc397_c1_interpolation_transition_replication.md"
PRODUCER = PROJECT / "code/tpc397_c1_interpolation_transition_replication.py"
INDEPENDENT = PROJECT / "experiments/tpc397_independent_checker.py"
STRESS = PROJECT / "experiments/tpc397_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc397_certificate.json"
MAIN_TEX = PROJECT / "paper/main.tex"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
README = PROJECT / "README.md"
PLAN = PROJECT / "PAPER_PLAN.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
PROOF = PROJECT / "PROOF_PACKAGE.md"
CLAIM = PROJECT / "notes/claim_firewall.md"
ROUTE = PROJECT / "notes/route_evaluation.md"
PROTOCOL = PROJECT / "notes/computational_protocol.md"
THEOREM = PROJECT / "notes/theorem_ledger.md"

LOCKS = {
    "producer": "1a395050d130398161afba90e741e54ecbcd93eed0169018db8084aac91504b9",
    "independent": "586b9315b4fc4c3da1bd56f6c56bcb6fbc5b6133d2ae297dbc89147bc0f2678e",
    "stress": "d535b82d7c9378faa5bd3ded9b38c6d00646d079bce5f0425babbc599e75e7e5",
    "certificate": "3d7a8241df38ffd3f4e527dd02f29d6e1653ed0d53a5a693dcd9c2a120e13fc2",
    "main_tex": "fe7e6c6294a75e76a65e146c1027a0893045635243f260a8f972f7787d48b60f",
    "main_pdf": "7b96dfe2ccc42ab3aff2056e8512c24f27363a2e1438c7c42fcf6b714fc6f84e",
    "pdf": "7b96dfe2ccc42ab3aff2056e8512c24f27363a2e1438c7c42fcf6b714fc6f84e",
    "log": "07997899295939b26da6074638b85f8e124b3598e2811f6e2ada6df121831554",
    "readme": "d7ec657a38059fa969a216a693949c279889b650b889994048416fa2cc4bcdba",
    "plan": "f8e04d16f0b747f8daed475471e84faaf698981166d17cfb98a2e5f26ccbf669",
    "derivation": "da68cdd6671819e097532d604684a944066fd1b12d3de03daa67517b54bf0887",
    "proof": "504a39632916582c7e7bdf07c3e2727645dd0367259b76f79f0671e1a4d8f54e",
    "claim": "21c9915d5bebe778ef739b42edeab48bd86aa853153f98bae6d518ceb5c80945",
    "route": "1515058bda32f0a598674a6b911dbcbc0d9e6c3983bcf6062a211e5a6106a622",
    "protocol": "3bf3f935cc6c04b96d1550e5d2c57301b8d4ecd98669bcdfe11fe7ee079ea5aa",
    "theorem": "ecee2ad8b3afa2b371afe2e50672c9230a6fd676eb67f2987231d34f5c136b69",
    "bridge": "ceb33d58adb27370272f502b8d19f3bcd0483d0da770c9c928a50cccc9a34532",
}

SCHEMA = "TPC397_C1_SIGNED_LAW_INTERPOLATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_INTERPOLATION_TRANSITION_REPLICATION_AUDIT"
PARENT_CODE_SHA256 = (
    "b83e4e268dd10ce3e74c7509eb846cda9ef0ddcb8deed198c82d19549d6a424a")
PARENT_CERT_SHA256 = (
    "3e5c71304a03772421ed921bcf067e35f5d4afa193e9c1568a7c244c2d3f100a")
EXPECTED_PRODUCER_OUTPUT = (
    b"TPC397_CERTIFICATE=PASS rows=96 cells=16 "
    b"origin_passes={'local_diagonal': 3, 'pooled_train_scalar': 3, "
    b"'origin_scalar': 3, 'frozen_train_1024_scalar': 3} "
    b"cross_holdout={'local_diagonal': 4, 'pooled_train_scalar': 4, "
    b"'origin_scalar': 4, 'frozen_train_1024_scalar': 4} "
    b"transfer_passes={'local_diagonal': 4, 'pooled_train_scalar': 4, "
    b"'origin_scalar': 4, 'frozen_train_1024_scalar': 4} "
    b"spectral_failures=0 schur_failures=0\n")
EXPECTED_INDEPENDENT_OUTPUT = (
    b"TPC397_INDEPENDENT_CHECK=PASS rows=96 cells=16 "
    b"origin_passes={'frozen_train_1024_scalar': 3, 'local_diagonal': 3, "
    b"'origin_scalar': 3, 'pooled_train_scalar': 3} "
    b"cross_holdout={'frozen_train_1024_scalar': 4, 'local_diagonal': 4, "
    b"'origin_scalar': 4, 'pooled_train_scalar': 4} "
    b"transfer_passes={'frozen_train_1024_scalar': 4, 'local_diagonal': 4, "
    b"'origin_scalar': 4, 'pooled_train_scalar': 4} "
    b"spectral_failures=0 schur_failures=0\n")
EXPECTED_STRESS_OUTPUT = b"TPC397_STRESS=PASS mutations=28\n"
BRIDGE_PASS_OUTPUT = (
    "TPC397_BRIDGE_CHECK=PASS rows=96 cells=16 "
    "origin_passes=local:3/4,pooled:3/4,origin:3/4,frozen:3/4 "
    "cross_holdout=local:4/4,pooled:4/4,origin:4/4,frozen:4/4 "
    "transfer_passes=local:4/4,pooled:4/4,origin:4/4,frozen:4/4 "
    "spectral_failures=0 schur_failures=0 "
    "max_cross_holdout_error=0.024669590049843704")


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def finite_tree(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and finite_tree(v)
                   for k, v in value.items())
    if isinstance(value, list):
        return all(finite_tree(v) for v in value)
    return True


def lock(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED" and path.is_file() and
         digest(path.read_bytes()) == expected, label + " provenance")


def parse_no_duplicates(raw: bytes) -> dict[str, Any]:
    def hook(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise Failure("duplicate JSON key")
            result[key] = value
        return result
    value = json.loads(raw, object_pairs_hook=hook)
    need(isinstance(value, dict), "certificate object")
    return value


def close(actual: float, recorded: Any, label: str,
          tolerance: float = 8.0e-8) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " is not numeric") from error
    need(math.isfinite(actual) and math.isfinite(target) and
         abs(actual - target) <= tolerance * max(1.0, abs(actual), abs(target)),
         label + " mismatch")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = parse_no_duplicates(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and finite_tree(payload) and
         payload.get("schema") == SCHEMA and payload.get("status") == STATUS,
         "payload header")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    parent = payload.get("parent_lock", {})
    need(parent.get("parent_code_sha256") == PARENT_CODE_SHA256 and
         parent.get("parent_certificate_sha256") == PARENT_CERT_SHA256 and
         parent.get("parent_schema") == "TPC396_C1_SIGNED_LAW_INTERPOLATION_V1" and
         parent.get("parent_interface_frozen") is True and
         parent.get("parent_interface_used_for_current_fit") is False and
         parent.get("parent_means_used_as_response_blind_baseline") is True,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") ==
         [6400001, 6403209, 6406417, 6409625, 6412833, 6416041] and
         selection.get("calibration_origins") == [6400001, 6403209, 6406417] and
         selection.get("holdout_origins") == [6409625, 6412833, 6416041] and
         selection.get("window_count") == 1024 and
         selection.get("q_anchors") == [8192] and
         selection.get("laws") == ["blend_3_4", "blend_5_6", "blend_11_12", "blend_1"] and
         selection.get("normalizations") == [
             "local_diagonal", "pooled_train_scalar", "origin_scalar",
             "frozen_train_1024_scalar"] and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("parent_means_frozen_before_current_readout") is True and
         selection.get("holdout_role_fixed_before_readout") is True and
         selection.get("interpolation_coefficients") == {
             "blend_3_4": [3, 4], "blend_5_6": [5, 6],
             "blend_11_12": [11, 12], "blend_1": [1, 1]} and
         selection.get("intermediate_laws_are_modeling_probes") is True,
         "selection protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 96 and
         payload.get("row_digest") == hashlib.sha256(canonical(rows)).hexdigest(),
         "row census")
    expected_keys = {(origin, law, norm) for origin in selection["origins"]
                     for law in selection["laws"] for norm in selection["normalizations"]}
    need({(r.get("origin"), r.get("law"), r.get("normalization")) for r in rows} ==
         expected_keys, "row keys")
    summary = payload.get("origin_summary", {})
    need(summary.get("row_count") == 96 and summary.get("cell_count") == 16 and
         summary.get("within_family_origin_pass_counts") == {
             "local_diagonal": 3, "pooled_train_scalar": 3,
             "origin_scalar": 3, "frozen_train_1024_scalar": 3} and
         summary.get("cross_family_calibration_pass_counts") == {
             "local_diagonal": 4, "pooled_train_scalar": 4,
             "origin_scalar": 4, "frozen_train_1024_scalar": 4} and
         summary.get("cross_family_holdout_pass_counts") == {
             "local_diagonal": 4, "pooled_train_scalar": 4,
             "origin_scalar": 4, "frozen_train_1024_scalar": 4} and
         summary.get("within_family_transfer_pass_counts") == {
             "local_diagonal": 4, "pooled_train_scalar": 4,
             "origin_scalar": 4, "frozen_train_1024_scalar": 4} and
         summary.get("spectral_failures_by_normalization") == {
             "local_diagonal": 0, "pooled_train_scalar": 0,
             "origin_scalar": 0, "frozen_train_1024_scalar": 0} and
         summary.get("schur_failures_by_normalization") == {
             "local_diagonal": 0, "pooled_train_scalar": 0,
             "origin_scalar": 0, "frozen_train_1024_scalar": 0},
         "summary census")
    maximum = summary.get("maximum_cross_family_holdout_abs_error", {})
    close(float(maximum["local_diagonal"]), 0.024669590049843704,
          "local cross holdout maximum")
    close(float(maximum["pooled_train_scalar"]), 0.02341348042930802,
          "pooled cross holdout maximum")
    close(float(maximum["origin_scalar"]), 0.023426110102541475,
          "origin cross holdout maximum")
    close(float(maximum["frozen_train_1024_scalar"]), 0.02339044284750269,
          "frozen cross holdout maximum")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC397_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC397_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC397_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC397_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC397_INTERPOLATION_PANEL") ==
         "NUMERICALLY_CERTIFIED_FINITE_96_ROWS" and
         firewall.get("TPC397_INTERPOLATION_IDENTITY") ==
         "PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY" and
         firewall.get("TPC397_SPECTRAL_ENVELOPE") ==
         "NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY", "firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_INTERPOLATION_ENDPOINT_MICROGRID",
         "clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [6400001, 6400014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True and
         all(anchor.get("interpolation_identity_exact", {}).values()), "anchor")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 96 and audit.get("cell_count") == 16 and
         audit.get("complete_cartesian_panel") is True and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("parent_baseline_frozen") is True and
         audit.get("interpolation_identity_exact_at_anchor") is True and
         audit.get("interpolation_panel_complete") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC397_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC397_INTERPOLATION_PANEL = NUMERICALLY CERTIFIED FINITE_96_ROWS",
            "TPC397_PARENT_INTERPOLATED_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED",
            "TPC397_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY",
            "TPC397_ARITHMETIC_ADVANCE = NO",
            "TPC397_ROUND2_CLUE = TEST_C1_INTERPOLATION_ENDPOINT_MICROGRID"):
        need(bridge_text.count(marker) == 1, "bridge marker")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull ", "Underfull ",
                "LaTeX Error", "Fatal error", "Citation", "Empty"):
        need(bad not in log, "LaTeX diagnostic " + bad)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and len(PDF.read_bytes()) > 100000,
         "PDF identity")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script), "--check"])
    environment = dict(os.environ)
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "OMP_NUM_THREADS": "1",
                        "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed " + script.name)
    return result.stdout


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        paths = {"producer": PRODUCER, "independent": INDEPENDENT,
                 "stress": STRESS, "certificate": CERTIFICATE,
                 "main_tex": MAIN_TEX, "main_pdf": MAIN_PDF, "pdf": PDF,
                 "log": LOG, "readme": README, "plan": PLAN,
                 "derivation": DERIVATION, "proof": PROOF, "claim": CLAIM,
                 "route": ROUTE, "protocol": PROTOCOL, "theorem": THEOREM,
                 "bridge": BRIDGE}
        for key, path in paths.items():
            lock(path, LOCKS[key], key)
        check_certificate()
        jobs = ((PRODUCER, False), (INDEPENDENT, False), (STRESS, False),
                (PRODUCER, True), (INDEPENDENT, True), (STRESS, True))
        with ThreadPoolExecutor(max_workers=6) as pool:
            outputs = tuple(pool.map(lambda job: run(*job), jobs))
        need(outputs[0] == outputs[3], "producer normal/optimized mismatch")
        need(outputs[1] == outputs[4], "independent normal/optimized mismatch")
        need(outputs[2] == outputs[5], "stress normal/optimized mismatch")
        need(outputs[0] == EXPECTED_PRODUCER_OUTPUT, "producer output")
        need(outputs[1] == EXPECTED_INDEPENDENT_OUTPUT, "independent output")
        need(outputs[2] == EXPECTED_STRESS_OUTPUT, "stress output")
        print(BRIDGE_PASS_OUTPUT)
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC397_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
