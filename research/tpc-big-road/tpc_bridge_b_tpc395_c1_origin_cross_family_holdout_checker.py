#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for the TPC-395 release."""

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
PROJECT = ROOT / "papers/tpc-395-c1-origin-cross-family-holdout"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc395_c1_origin_cross_family_holdout.md"
PRODUCER = PROJECT / "code/tpc395_c1_origin_cross_family_holdout.py"
INDEPENDENT = PROJECT / "experiments/tpc395_independent_checker.py"
STRESS = PROJECT / "experiments/tpc395_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc395_certificate.json"
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
    "producer": "97407a999cad62099fe9b786f0c47145418f168f59bb39d0af29d8d15601c86a",
    "independent": "851873d3bea45afd95f37cfe427c803f83d713bb81b2e90d0c340670f08055fa",
    "stress": "88fabb94ac5748035689ff34222cffa100fbbb081e331dc811d9b5df333be160",
    "certificate": "994555e235c1ebf87e615195fe4296b0f7b8229321b6189663cfcbd267f9b3ba",
    "main_tex": "c7cd011abff865d31669d9b74e429ee23f0d5550ad30664adbb60cf5b1cfa99a",
    "main_pdf": "ffdc1e69acf329973131e2c64fcfeab481da423c7f1d8144532328d89878c157",
    "pdf": "ffdc1e69acf329973131e2c64fcfeab481da423c7f1d8144532328d89878c157",
    "log": "6fbc26f7a7476487dbc258bb19d41d8164a5dc307bed93ba85277b5734becb2b",
    "readme": "98752b2baa2d56481e1f3fd52c592ad6ae9de1f14b9a08721f8d742d95f3b6c6",
    "plan": "54f6a2c811c42d532a66558761162276fff6f61a3686175b82d04b8e84c845a8",
    "derivation": "3f49f214bfcacbf7662795ef71b9d183c1596ab35fea394a2cf0adce5309d7ff",
    "proof": "2ec54f4c3c845bcc4f7a4f30fe59e20ed90a6e3cc9aee3f57772b85753950248",
    "claim": "87c8f2eeb03674d2f444a310cc80ab96430b54408e40084bcd384e2f8282ae25",
    "route": "f4f3240aebc3432a80b6d62060790c793842ed33749858ae5c17024e5cd80710",
    "protocol": "0d4f3129ed8bcc30dd718725760374f8a36ba66142a7103fce2c47671510fbf3",
    "theorem": "ef81633643e2b9c9b3c7a489b781cd1868be61d919e321d3df8217a0f51b0435",
    "bridge": "b3c19e7d34a521a27dab307b90f4c4719588e01a4e44afd0aa0025522effeb2d",
}

SCHEMA = "TPC395_C1_ORIGIN_CROSS_FAMILY_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_ORIGIN_CROSS_FAMILY_HOLDOUT_AUDIT"
PARENT_CODE_SHA256 = (
    "48b097109cd725b160fc52a40ae035c223fc7790d52c4afb561e664afcd2b5b6")
PARENT_CERT_SHA256 = (
    "03d5dc25ea4ff135e2b3a5693ba3b24865371babefc394c76662ce12b410b753")
EXPECTED_PRODUCER_OUTPUT = (
    b"TPC395_CERTIFICATE=PASS rows=48 cells=8 "
    b"origin_passes={'local_diagonal': 1, 'pooled_train_scalar': 1, "
    b"'origin_scalar': 1, 'frozen_train_1024_scalar': 1} "
    b"cross_holdout={'local_diagonal': 2, 'pooled_train_scalar': 2, "
    b"'origin_scalar': 2, 'frozen_train_1024_scalar': 2} "
    b"transfer_passes={'local_diagonal': 2, 'pooled_train_scalar': 2, "
    b"'origin_scalar': 2, 'frozen_train_1024_scalar': 2} "
    b"spectral_failures=24 schur_failures=0\n")
EXPECTED_INDEPENDENT_OUTPUT = (
    b"TPC395_INDEPENDENT_CHECK=PASS rows=48 cells=8 "
    b"origin_passes={'frozen_train_1024_scalar': 1, 'local_diagonal': 1, "
    b"'origin_scalar': 1, 'pooled_train_scalar': 1} "
    b"cross_holdout={'frozen_train_1024_scalar': 2, 'local_diagonal': 2, "
    b"'origin_scalar': 2, 'pooled_train_scalar': 2} "
    b"transfer_passes={'frozen_train_1024_scalar': 2, 'local_diagonal': 2, "
    b"'origin_scalar': 2, 'pooled_train_scalar': 2} "
    b"spectral_failures=24 schur_failures=0\n")
EXPECTED_STRESS_OUTPUT = b"TPC395_STRESS=PASS mutations=25\n"
BRIDGE_PASS_OUTPUT = (
    "TPC395_BRIDGE_CHECK=PASS rows=48 cells=8 "
    "origin_passes=local:1/2,pooled:1/2,origin:1/2,frozen:1/2 "
    "cross_holdout=local:2/2,pooled:2/2,origin:2/2,frozen:2/2 "
    "transfer_passes=local:2/2,pooled:2/2,origin:2/2,frozen:2/2 "
    "spectral_failures=24 schur_failures=0 "
    "max_cross_holdout_error=0.023289195722825839")


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
         parent.get("parent_schema") == "TPC394_C1_ORIGIN_UNIFORMITY_LADDER_V1" and
         parent.get("parent_interface_frozen") is True and
         parent.get("parent_interface_used_for_current_fit") is False and
         parent.get("parent_means_used_as_response_blind_baseline") is True,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") ==
         [5600001, 5603209, 5606417, 5609625, 5612833, 5616041] and
         selection.get("calibration_origins") == [5600001, 5603209, 5606417] and
         selection.get("holdout_origins") == [5609625, 5612833, 5616041] and
         selection.get("window_count") == 1024 and
         selection.get("q_anchors") == [8192] and
         selection.get("laws") == ["all_plus", "alternating_index"] and
         selection.get("normalizations") == [
             "local_diagonal", "pooled_train_scalar", "origin_scalar",
             "frozen_train_1024_scalar"] and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("parent_means_frozen_before_current_readout") is True and
         selection.get("holdout_role_fixed_before_readout") is True,
         "selection protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 48 and
         payload.get("row_digest") == hashlib.sha256(canonical(rows)).hexdigest(),
         "row census")
    expected_keys = {(origin, law, norm) for origin in selection["origins"]
                     for law in selection["laws"] for norm in selection["normalizations"]}
    need({(r.get("origin"), r.get("law"), r.get("normalization")) for r in rows} ==
         expected_keys, "row keys")
    summary = payload.get("origin_summary", {})
    need(summary.get("row_count") == 48 and summary.get("cell_count") == 8 and
         summary.get("within_family_origin_pass_counts") == {
             "local_diagonal": 1, "pooled_train_scalar": 1,
             "origin_scalar": 1, "frozen_train_1024_scalar": 1} and
         summary.get("cross_family_calibration_pass_counts") == {
             "local_diagonal": 2, "pooled_train_scalar": 2,
             "origin_scalar": 2, "frozen_train_1024_scalar": 2} and
         summary.get("cross_family_holdout_pass_counts") == {
             "local_diagonal": 2, "pooled_train_scalar": 2,
             "origin_scalar": 2, "frozen_train_1024_scalar": 2} and
         summary.get("within_family_transfer_pass_counts") == {
             "local_diagonal": 2, "pooled_train_scalar": 2,
             "origin_scalar": 2, "frozen_train_1024_scalar": 2} and
         summary.get("spectral_failures_by_normalization") == {
             "local_diagonal": 6, "pooled_train_scalar": 6,
             "origin_scalar": 6, "frozen_train_1024_scalar": 6} and
         summary.get("schur_failures_by_normalization") == {
             "local_diagonal": 0, "pooled_train_scalar": 0,
             "origin_scalar": 0, "frozen_train_1024_scalar": 0},
         "summary census")
    maximum = summary.get("maximum_cross_family_holdout_abs_error", {})
    close(float(maximum["local_diagonal"]), 0.019120856868882985,
          "local cross holdout maximum")
    close(float(maximum["pooled_train_scalar"]), 0.023261029846088688,
          "pooled cross holdout maximum")
    close(float(maximum["origin_scalar"]), 0.023245265196004006,
          "origin cross holdout maximum")
    close(float(maximum["frozen_train_1024_scalar"]), 0.023289195722825839,
          "frozen cross holdout maximum")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC395_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC395_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC395_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC395_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC395_CROSS_FAMILY_PANEL") ==
         "NUMERICALLY_CERTIFIED_FINITE_48_ROWS", "firewall")
    need(payload.get("round2_clue") == "TEST_C1_SIGNED_LAW_INTERPOLATION",
         "clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [5600001, 5600014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True, "anchor")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 48 and audit.get("cell_count") == 8 and
         audit.get("complete_cartesian_panel") is True and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("parent_baseline_frozen") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC395_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC395_CROSS_FAMILY_PANEL = NUMERICALLY CERTIFIED FINITE_48_ROWS",
            "TPC395_CROSS_FAMILY_MEAN_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED",
            "TPC395_ARITHMETIC_ADVANCE = NO",
            "TPC395_ROUND2_CLUE = TEST_C1_SIGNED_LAW_INTERPOLATION"):
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
        print("TPC395_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
