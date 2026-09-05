#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for the TPC-398 release."""

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
PROJECT = ROOT / "papers/tpc-398-c1-interpolation-endpoint-microgrid"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc398_c1_interpolation_endpoint_microgrid.md"
PRODUCER = PROJECT / "code/tpc398_c1_interpolation_endpoint_microgrid.py"
INDEPENDENT = PROJECT / "experiments/tpc398_independent_checker.py"
STRESS = PROJECT / "experiments/tpc398_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc398_certificate.json"
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
    "producer": "10c55a6b9e3c4dc11674780f7d1d98508d223729e18ffde7f27a88d7790a3382",
    "independent": "1fd42173f634b3ea8514be4eb5bf33a561d39801d7e505abd7ea57dcdebdb8ac",
    "stress": "7979ad3758565eda5757a7b2a43873b53b63638cb1bcbc0879a3e6f2bbf5e613",
    "certificate": "3f944db8218d8c18a2f2c756dcaf26483afe18e4ac681695beba56b222256150",
    "main_tex": "1f4be3198072fbfa24af5d82a80a004081764b7cec42ad7d6988f9a5374e5f4f",
    "main_pdf": "ac6ff9c67ce55b94906d35bdd141b3d040674d5f47660268219bd9c912deb2a1",
    "pdf": "ac6ff9c67ce55b94906d35bdd141b3d040674d5f47660268219bd9c912deb2a1",
    "log": "d534c3ea94dd81d6845166659f82a3e9d0319fa32c1badfb21e34048cdf47637",
    "readme": "a0185116ff416efcc960b8aae623008f131ff1de54117a3462b847e13ed78e79",
    "plan": "23a0153772e71645cdecd97caa11ed3345ec850adfcc61c550bdbc733f6e50e6",
    "derivation": "cc4d772f70ff5131a53767d573bf8d0425ee8f410694e4af9a7fd1f5fac984d8",
    "proof": "cf86c9a57068c082d6eb5a1e2f3bafe44a992e092a8dd78b84ecdf8addffaec5",
    "claim": "de887114b37bcee69f9b5c19f56e88f96e0fae4bd2c80bc46028b468baf1ad5f",
    "route": "d016c1810615e1c8b7894d70d69a7b6c830df547ce4e004dc9d5c09c69d7d274",
    "protocol": "c276bd1bae4f561de8a5c8a7130c225b777a40e0641c6c6bec6cdae31425753b",
    "theorem": "2a48fb3df358a1fefb583133cafbd9fe2acb420212decdf1f33c17009cb6f5c3",
    "bridge": "7288eb185eded5e330886194c650f5e6aed347b54fecb00f434cbfaf40267976",
}

SCHEMA = "TPC398_C1_INTERPOLATION_ENDPOINT_MICROGRID_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_INTERPOLATION_ENDPOINT_MICROGRID_AUDIT"
PARENT_CODE_SHA256 = (
    "1a395050d130398161afba90e741e54ecbcd93eed0169018db8084aac91504b9")
PARENT_CERT_SHA256 = (
    "3d7a8241df38ffd3f4e527dd02f29d6e1653ed0d53a5a693dcd9c2a120e13fc2")
EXPECTED_PRODUCER_OUTPUT = (
    b"TPC398_CERTIFICATE=PASS rows=96 cells=16 "
    b"origin_passes={'local_diagonal': 3, 'pooled_train_scalar': 3, "
    b"'origin_scalar': 3, 'frozen_train_1024_scalar': 3} "
    b"cross_holdout={'local_diagonal': 3, 'pooled_train_scalar': 3, "
    b"'origin_scalar': 3, 'frozen_train_1024_scalar': 3} "
    b"transfer_passes={'local_diagonal': 4, 'pooled_train_scalar': 4, "
    b"'origin_scalar': 4, 'frozen_train_1024_scalar': 4} "
    b"spectral_failures=0 schur_failures=0\n")
EXPECTED_INDEPENDENT_OUTPUT = (
    b"TPC398_INDEPENDENT_CHECK=PASS rows=96 cells=16 "
    b"origin_passes={'frozen_train_1024_scalar': 3, 'local_diagonal': 3, "
    b"'origin_scalar': 3, 'pooled_train_scalar': 3} "
    b"cross_holdout={'frozen_train_1024_scalar': 3, 'local_diagonal': 3, "
    b"'origin_scalar': 3, 'pooled_train_scalar': 3} "
    b"transfer_passes={'frozen_train_1024_scalar': 4, 'local_diagonal': 4, "
    b"'origin_scalar': 4, 'pooled_train_scalar': 4} "
    b"spectral_failures=0 schur_failures=0\n")
EXPECTED_STRESS_OUTPUT = b"TPC398_STRESS=PASS mutations=28\n"
BRIDGE_PASS_OUTPUT = (
    "TPC398_BRIDGE_CHECK=PASS rows=96 cells=16 "
    "origin_passes=local:3/4,pooled:3/4,origin:3/4,frozen:3/4 "
    "cross_holdout=local:3/4,pooled:3/4,origin:3/4,frozen:3/4 "
    "transfer_passes=local:4/4,pooled:4/4,origin:4/4,frozen:4/4 "
    "spectral_failures=0 schur_failures=0 "
    "max_cross_holdout_error=0.044971523016385406")


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
         parent.get("parent_schema") == "TPC397_C1_SIGNED_LAW_INTERPOLATION_V1" and
         parent.get("parent_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_INTERPOLATION_TRANSITION_REPLICATION_AUDIT" and
         parent.get("parent_endpoint_laws") == ["blend_3_4", "blend_1"] and
         parent.get("parent_segment") == "lambda in [3/4,1]" and
         parent.get("parent_interface_frozen") is True and
         parent.get("parent_interface_used_for_current_fit") is False and
         parent.get("parent_means_used_as_response_blind_baseline") is True,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") ==
         [6800001, 6803209, 6806417, 6809625, 6812833, 6816041] and
         selection.get("calibration_origins") == [6800001, 6803209, 6806417] and
         selection.get("holdout_origins") == [6809625, 6812833, 6816041] and
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
             "local_diagonal": 3, "pooled_train_scalar": 3,
             "origin_scalar": 3, "frozen_train_1024_scalar": 3} and
         summary.get("cross_family_holdout_pass_counts") == {
             "local_diagonal": 3, "pooled_train_scalar": 3,
             "origin_scalar": 3, "frozen_train_1024_scalar": 3} and
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
    close(float(maximum["local_diagonal"]), 0.044967550979353899,
          "local cross holdout maximum")
    close(float(maximum["pooled_train_scalar"]), 0.044966909612749628,
          "pooled cross holdout maximum")
    close(float(maximum["origin_scalar"]), 0.044962188402154379,
          "origin cross holdout maximum")
    close(float(maximum["frozen_train_1024_scalar"]), 0.044971523016385406,
          "frozen cross holdout maximum")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC398_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC398_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC398_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC398_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC398_INTERPOLATION_PANEL") ==
         "NUMERICALLY_CERTIFIED_FINITE_96_ROWS" and
         firewall.get("TPC398_INTERPOLATION_IDENTITY") ==
         "PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY" and
         firewall.get("TPC398_SPECTRAL_ENVELOPE") ==
         "NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY", "firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_ENDPOINT_MICROGRID_CROSS_FAMILY_REPLICATION",
         "clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [6800001, 6800014] and
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
            "TPC398_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC398_INTERPOLATION_PANEL = NUMERICALLY CERTIFIED FINITE_96_ROWS",
            "TPC398_PARENT_INTERPOLATED_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED",
            "TPC398_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY",
            "TPC398_ARITHMETIC_ADVANCE = NO",
            "TPC398_ROUND2_CLUE = TEST_C1_ENDPOINT_MICROGRID_CROSS_FAMILY_REPLICATION"):
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
        print("TPC398_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
