#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for the TPC-396 release."""

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
PROJECT = ROOT / "papers/tpc-396-c1-signed-law-interpolation"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc396_c1_signed_law_interpolation.md"
PRODUCER = PROJECT / "code/tpc396_c1_signed_law_interpolation.py"
INDEPENDENT = PROJECT / "experiments/tpc396_independent_checker.py"
STRESS = PROJECT / "experiments/tpc396_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc396_certificate.json"
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
    "producer": "b83e4e268dd10ce3e74c7509eb846cda9ef0ddcb8deed198c82d19549d6a424a",
    "independent": "0bcf1ff83641f5b7a738cb9388ade5d0cb69c96f3d104d7c1bf2a3b6f00e47b0",
    "stress": "63f7c7cc5e11a10021475ac815f171edb87561f3ab571142e4bc5ddbb8874ded",
    "certificate": "3e5c71304a03772421ed921bcf067e35f5d4afa193e9c1568a7c244c2d3f100a",
    "main_tex": "4a466e42ae079573ed9100228b99d7d27435451109a77d7976408d541cbe34f2",
    "main_pdf": "c98a7f50a686bea738d98fd832d5f1aafb16d7fd4261f5955f9a9291bf0e8aa2",
    "pdf": "c98a7f50a686bea738d98fd832d5f1aafb16d7fd4261f5955f9a9291bf0e8aa2",
    "log": "aea6e91ed96d284e85c325d3ddba6061450a4a84c919ec800982a12a82f1515f",
    "readme": "827fa4ba6ac0409871003d4e7d8c44ea79edeef99868364da6eb8035b07c619f",
    "plan": "ea9b59680a1d4dfa700fe9a253b5dc33c256f992587b7267272bdff56fed7d6f",
    "derivation": "efddbd6465f17c746cfd52c884d29f04bb3b35c0546e1d26a2a0a1556ed71859",
    "proof": "99da7312c3648895eb7b9e6a1e3a4ef7b723016ace3b367ebfa40b3a642cfb9e",
    "claim": "791c5aa223c7910626dbdfd370176843152327501279a7d850d4930e1ce9d7be",
    "route": "2fa9c3aea99771348408187632ecb32d67c92565306640f004132a604d8179a2",
    "protocol": "9eb83e9604f72cdba15130e8db552879ea179579bcea7992521ad6a5b19f1584",
    "theorem": "6ba5af2c37b236f6354fca63abe9c0a0ef7373b094992be317b72a08fa9a2424",
    "bridge": "daece5e7221c956c4885732bf257764fa65f353724e804d1deb12a77a6de0303",
}

SCHEMA = "TPC396_C1_SIGNED_LAW_INTERPOLATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_SIGNED_LAW_INTERPOLATION_AUDIT"
PARENT_CODE_SHA256 = (
    "97407a999cad62099fe9b786f0c47145418f168f59bb39d0af29d8d15601c86a")
PARENT_CERT_SHA256 = (
    "994555e235c1ebf87e615195fe4296b0f7b8229321b6189663cfcbd267f9b3ba")
EXPECTED_PRODUCER_OUTPUT = (
    b"TPC396_CERTIFICATE=PASS rows=96 cells=16 "
    b"origin_passes={'local_diagonal': 3, 'pooled_train_scalar': 3, "
    b"'origin_scalar': 3, 'frozen_train_1024_scalar': 3} "
    b"cross_holdout={'local_diagonal': 4, 'pooled_train_scalar': 4, "
    b"'origin_scalar': 4, 'frozen_train_1024_scalar': 4} "
    b"transfer_passes={'local_diagonal': 4, 'pooled_train_scalar': 3, "
    b"'origin_scalar': 3, 'frozen_train_1024_scalar': 3} "
    b"spectral_failures=24 schur_failures=0\n")
EXPECTED_INDEPENDENT_OUTPUT = (
    b"TPC396_INDEPENDENT_CHECK=PASS rows=96 cells=16 "
    b"origin_passes={'frozen_train_1024_scalar': 3, 'local_diagonal': 3, "
    b"'origin_scalar': 3, 'pooled_train_scalar': 3} "
    b"cross_holdout={'frozen_train_1024_scalar': 4, 'local_diagonal': 4, "
    b"'origin_scalar': 4, 'pooled_train_scalar': 4} "
    b"transfer_passes={'frozen_train_1024_scalar': 3, 'local_diagonal': 4, "
    b"'origin_scalar': 3, 'pooled_train_scalar': 3} "
    b"spectral_failures=24 schur_failures=0\n")
EXPECTED_STRESS_OUTPUT = b"TPC396_STRESS=PASS mutations=28\n"
BRIDGE_PASS_OUTPUT = (
    "TPC396_BRIDGE_CHECK=PASS rows=96 cells=16 "
    "origin_passes=local:3/4,pooled:3/4,origin:3/4,frozen:3/4 "
    "cross_holdout=local:4/4,pooled:4/4,origin:4/4,frozen:4/4 "
    "transfer_passes=local:4/4,pooled:3/4,origin:3/4,frozen:3/4 "
    "spectral_failures=24 schur_failures=0 "
    "max_cross_holdout_error=0.0033105775404086435")


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
         parent.get("parent_schema") == "TPC395_C1_ORIGIN_CROSS_FAMILY_HOLDOUT_V1" and
         parent.get("parent_interface_frozen") is True and
         parent.get("parent_interface_used_for_current_fit") is False and
         parent.get("parent_means_used_as_response_blind_baseline") is True,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") ==
         [6000001, 6003209, 6006417, 6009625, 6012833, 6016041] and
         selection.get("calibration_origins") == [6000001, 6003209, 6006417] and
         selection.get("holdout_origins") == [6009625, 6012833, 6016041] and
         selection.get("window_count") == 1024 and
         selection.get("q_anchors") == [8192] and
         selection.get("laws") == ["blend_0", "blend_1_3", "blend_2_3", "blend_1"] and
         selection.get("normalizations") == [
             "local_diagonal", "pooled_train_scalar", "origin_scalar",
             "frozen_train_1024_scalar"] and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("parent_means_frozen_before_current_readout") is True and
         selection.get("holdout_role_fixed_before_readout") is True and
         selection.get("interpolation_coefficients") == {
             "blend_0": [0, 1], "blend_1_3": [1, 3],
             "blend_2_3": [2, 3], "blend_1": [1, 1]} and
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
             "local_diagonal": 4, "pooled_train_scalar": 3,
             "origin_scalar": 3, "frozen_train_1024_scalar": 3} and
         summary.get("cross_family_holdout_pass_counts") == {
             "local_diagonal": 4, "pooled_train_scalar": 4,
             "origin_scalar": 4, "frozen_train_1024_scalar": 4} and
         summary.get("within_family_transfer_pass_counts") == {
             "local_diagonal": 4, "pooled_train_scalar": 3,
             "origin_scalar": 3, "frozen_train_1024_scalar": 3} and
         summary.get("spectral_failures_by_normalization") == {
             "local_diagonal": 6, "pooled_train_scalar": 6,
             "origin_scalar": 6, "frozen_train_1024_scalar": 6} and
         summary.get("schur_failures_by_normalization") == {
             "local_diagonal": 0, "pooled_train_scalar": 0,
             "origin_scalar": 0, "frozen_train_1024_scalar": 0},
         "summary census")
    maximum = summary.get("maximum_cross_family_holdout_abs_error", {})
    close(float(maximum["local_diagonal"]), 0.0032911710708237729,
          "local cross holdout maximum")
    close(float(maximum["pooled_train_scalar"]), 0.0033105775404086435,
          "pooled cross holdout maximum")
    close(float(maximum["origin_scalar"]), 0.0032932605306436047,
          "origin cross holdout maximum")
    close(float(maximum["frozen_train_1024_scalar"]), 0.0033062541332148365,
          "frozen cross holdout maximum")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC396_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC396_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC396_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC396_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC396_INTERPOLATION_PANEL") ==
         "NUMERICALLY_CERTIFIED_FINITE_96_ROWS" and
         firewall.get("TPC396_INTERPOLATION_IDENTITY") ==
         "PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY", "firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_INTERPOLATION_TRANSITION_REPLICATION",
         "clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [6000001, 6000014] and
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
            "TPC396_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC396_INTERPOLATION_PANEL = NUMERICALLY CERTIFIED FINITE_96_ROWS",
            "TPC396_PARENT_INTERPOLATED_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED",
            "TPC396_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY",
            "TPC396_ARITHMETIC_ADVANCE = NO",
            "TPC396_ROUND2_CLUE = TEST_C1_INTERPOLATION_TRANSITION_REPLICATION"):
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
        print("TPC396_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
