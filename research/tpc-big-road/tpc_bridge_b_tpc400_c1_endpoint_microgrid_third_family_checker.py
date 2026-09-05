#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for the TPC-400 release."""

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
PROJECT = ROOT / "papers/tpc-400-c1-endpoint-microgrid-third-family"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc400_c1_endpoint_microgrid_third_family.md"
PRODUCER = PROJECT / "code/tpc400_c1_endpoint_microgrid_third_family.py"
INDEPENDENT = PROJECT / "experiments/tpc400_independent_checker.py"
STRESS = PROJECT / "experiments/tpc400_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc400_certificate.json"
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
    "producer": "9d9447dd825703d41a35e6794273e9b623f4ad684afd3cf71a82ab0f52777a0d",
    "independent": "2ee2e7e953d5716be648ead7dd302befbcc5f3ce10afdb229de871aa7f419623",
    "stress": "f43994d9abcbc06172bcc5d49caac24a976466598f63e718a4369cf96ba809a3",
    "certificate": "38b30fb35548b20e2b4eb7e509433d182f16d6f994938f9c34594c0a02c11c3c",
    "main_tex": "686121fd91b93caf12ea57e697db0531b572db1a720f28e2afd60d7056861874",
    "main_pdf": "7d286fd8acb8eb849d814b99ab86c9ad75ad6312d2bf8742d4cf04f7503b5a14",
    "pdf": "7d286fd8acb8eb849d814b99ab86c9ad75ad6312d2bf8742d4cf04f7503b5a14",
    "log": "85c38d1eef43e3e87625d1d64d540b1e483b52811e775178d4b77ee48c0baf1f",
    "readme": "c2b138ad15f2ab039c216b15c427f8f140c7df943114d27cdeaff44a06f15f9f",
    "plan": "40ac0a8268c613cef22e0b45817ef83d8d618d3aa5ccf45caf8ad78cae016c31",
    "derivation": "442114ad4edfcdfbd8bb4bda35f898bb2509c3bb828a4db72ed214ee113b964e",
    "proof": "8f255efe4a6de15e2e891800fb9fae53a7b11377cc88f9d7545bcae20bab2aa6",
    "claim": "915fc148d83129891295d0f77c05e47de7d74af3ee8a7c89b2133751fe10a4b5",
    "route": "f4ebbac26b311f2334dd0ed094ea974c1666162b4357171813ab237386952671",
    "protocol": "3d6d213c590f0abcfa22fa953c9de3273dffa922177ac6b90799896e58177f0d",
    "theorem": "83394f82d5e8549a2197d9b7c27880ebad779c277744f470aeef4d65fc395a34",
    "bridge": "5d5e3ad9207bf113cb196a668606b836e46ca2095e678f30463f285d55e20fbb",
}

SCHEMA = "TPC400_C1_ENDPOINT_MICROGRID_THIRD_FAMILY_V1"
STATUS = "NUMERICAL_OBSERVATION_FINITE_C1_ENDPOINT_MICROGRID_THIRD_FAMILY_AUDIT"
PARENT_CODE_SHA256 = (
    "6b65f30fd6aa3f54e58596635a1248c892c01eb71d4156a37578bb71a1079d2b")
PARENT_CERT_SHA256 = (
    "6f632add733947838c4268969748068633b2b85fadbd8fba7c21a146d98b7896")
EXPECTED_PRODUCER_OUTPUT = (
    b"TPC400_CERTIFICATE=PASS rows=96 cells=16 "
    b"origin_passes={'local_diagonal': 3, 'pooled_train_scalar': 3, "
    b"'origin_scalar': 3, 'frozen_train_1024_scalar': 3} "
    b"cross_holdout={'local_diagonal': 4, 'pooled_train_scalar': 4, "
    b"'origin_scalar': 4, 'frozen_train_1024_scalar': 4} "
    b"transfer_passes={'local_diagonal': 4, 'pooled_train_scalar': 4, "
    b"'origin_scalar': 4, 'frozen_train_1024_scalar': 4} "
    b"spectral_failures=0 schur_failures=0\n")
EXPECTED_INDEPENDENT_OUTPUT = (
    b"TPC400_INDEPENDENT_CHECK=PASS rows=96 cells=16 "
    b"origin_passes={'frozen_train_1024_scalar': 3, 'local_diagonal': 3, "
    b"'origin_scalar': 3, 'pooled_train_scalar': 3} "
    b"cross_holdout={'frozen_train_1024_scalar': 4, 'local_diagonal': 4, "
    b"'origin_scalar': 4, 'pooled_train_scalar': 4} "
    b"transfer_passes={'frozen_train_1024_scalar': 4, 'local_diagonal': 4, "
    b"'origin_scalar': 4, 'pooled_train_scalar': 4} "
    b"spectral_failures=0 schur_failures=0\n")
EXPECTED_STRESS_OUTPUT = b"TPC400_STRESS=PASS mutations=28\n"
BRIDGE_PASS_OUTPUT = (
    "TPC400_BRIDGE_CHECK=PASS rows=96 cells=16 "
    "origin_passes=local:3/4,pooled:3/4,origin:3/4,frozen:3/4 "
    "cross_holdout=local:4/4,pooled:4/4,origin:4/4,frozen:4/4 "
    "transfer_passes=local:4/4,pooled:4/4,origin:4/4,frozen:4/4 "
    "spectral_failures=0 schur_failures=0 "
    "max_cross_holdout_error=0.0024091869655593623")


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
         parent.get("parent_schema") == "TPC399_C1_ENDPOINT_MICROGRID_CROSS_FAMILY_V1" and
         parent.get("parent_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_ENDPOINT_MICROGRID_CROSS_FAMILY_AUDIT" and
         parent.get("parent_endpoint_laws") ==
         ["blend_7_8", "blend_15_16", "blend_31_32", "blend_1"] and
         parent.get("parent_segment") ==
         "lambda in {7/8,15/16,31/32,1}" and
         parent.get("parent_baseline_definition") ==
         "direct same-law TPC399 all-origin mean" and
         parent.get("parent_interpolation_is_modeling_choice") is False and
         parent.get("parent_interface_frozen") is True and
         parent.get("parent_interface_used_for_current_fit") is False and
         parent.get("parent_means_used_as_response_blind_baseline") is True,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") ==
         [7600001, 7603209, 7606417, 7609625, 7612833, 7616041] and
         selection.get("calibration_origins") == [7600001, 7603209, 7606417] and
         selection.get("holdout_origins") == [7609625, 7612833, 7616041] and
         selection.get("window_count") == 1024 and
         selection.get("q_anchors") == [8192] and
         selection.get("laws") == ["blend_7_8", "blend_15_16", "blend_31_32", "blend_1"] and
         selection.get("normalizations") == [
             "local_diagonal", "pooled_train_scalar", "origin_scalar",
             "frozen_train_1024_scalar"] and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("parent_means_frozen_before_current_readout") is True and
         selection.get("holdout_role_fixed_before_readout") is True and
         selection.get("interpolation_coefficients") == {
             "blend_7_8": [7, 8], "blend_15_16": [15, 16],
             "blend_31_32": [31, 32], "blend_1": [1, 1]} and
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
    close(float(maximum["local_diagonal"]), 0.0001317871615125199,
          "local cross holdout maximum")
    close(float(maximum["pooled_train_scalar"]), 0.0024016862760729563,
          "pooled cross holdout maximum")
    close(float(maximum["origin_scalar"]), 0.002385057413556213,
          "origin cross holdout maximum")
    close(float(maximum["frozen_train_1024_scalar"]), 0.0024091869655593623,
          "frozen cross holdout maximum")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC400_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC400_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC400_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC400_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC400_INTERPOLATION_PANEL") ==
         "NUMERICAL_OBSERVATION_FINITE_FLOAT64_96_ROWS" and
         firewall.get("TPC400_INTERPOLATION_IDENTITY") ==
         "PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY" and
         firewall.get("TPC400_PARENT_CROSS_FAMILY_TRANSFER") ==
         "NUMERICAL_OBSERVATION_FINITE_FLOAT64_SCOPED" and
         firewall.get("TPC400_SPECTRAL_ENVELOPE") ==
         "NUMERICAL_OBSERVATION_FINITE_FLOAT64_SCOPED_ONLY" and
         firewall.get("TPC400_SCHUR_ENVELOPE") ==
         "NUMERICAL_OBSERVATION_FINITE_FLOAT64_SCOPED_ONLY", "firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_ENDPOINT_MICROGRID_FOURTH_FAMILY_REPLICATION",
         "clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [7600001, 7600014] and
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
            "TPC400_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC400_INTERPOLATION_PANEL = NUMERICAL OBSERVATION FINITE FLOAT64_96_ROWS",
            "TPC400_PARENT_CROSS_FAMILY_TRANSFER = NUMERICAL OBSERVATION FINITE FLOAT64 SCOPED",
            "TPC400_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY",
            "TPC400_ARITHMETIC_ADVANCE = NO",
            "TPC400_ROUND2_CLUE = TEST_C1_ENDPOINT_MICROGRID_FOURTH_FAMILY_REPLICATION"):
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
        print("TPC400_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
