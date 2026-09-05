#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for the TPC-394 release."""

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
PROJECT = ROOT / "papers/tpc-394-c1-origin-uniformity-ladder"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc394_c1_origin_uniformity_ladder.md"
PRODUCER = PROJECT / "code/tpc394_c1_origin_uniformity_ladder.py"
INDEPENDENT = PROJECT / "experiments/tpc394_independent_checker.py"
STRESS = PROJECT / "experiments/tpc394_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc394_certificate.json"
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

# Filled only after every release artifact is final.
LOCKS = {
    "producer": "48b097109cd725b160fc52a40ae035c223fc7790d52c4afb561e664afcd2b5b6",
    "independent": "d93a903a5606c32ba557f7264c6a829735a0ed18326c15eed94e97a630889193",
    "stress": "4762d8124546735c964d7ce4732e47f9ed86db8abb360581f9a15cc7227cee2a",
    "certificate": "03d5dc25ea4ff135e2b3a5693ba3b24865371babefc394c76662ce12b410b753",
    "main_tex": "8bc3f4dd764b73ca9666e29c085bbf5e1d4ebd99935efc99c5ef5ad2f700458e",
    "main_pdf": "4588922ee2c8327031c22e707121f76b92c7377665842a6a4cd36bd770fa7400",
    "pdf": "4588922ee2c8327031c22e707121f76b92c7377665842a6a4cd36bd770fa7400",
    "log": "dc2c12d8eb0a04454539e6f8beec8e1cd6704c534683be4b39681bba57e0a491",
    "readme": "ed3b3ad1d9e418edc06e08911c1c2ee51095f6cb4d20c858aed1f1b6d8a8cbd9",
    "plan": "cc49313f627e5780ced9abcd7d7cdd09a1418424556da97522a0c807f56f6545",
    "derivation": "92178d913d44f4609afae79ed1f0c5a13e8f53f61d6d4dd988836313aa2c637b",
    "proof": "7da16b8e7f066fa69ff42ed22a07cdc356e749f98da870d60773e3193d5beb7a",
    "claim": "ded1a0cf727f657a4c7a201412da29b8541de574d2ab017f6773b3d8dad75984",
    "route": "b007e36ba6c491d4d882ec34a60e9487aa68e9069e90e45aee2f84d6f36fac38",
    "protocol": "99f38d6dc4db7a088cf1b2ce9073c6e63f4316f292caa9573fca696fce835982",
    "theorem": "bbba029327ad7dcf3a6cab2773f40cd6e2a98b7e3189ea418ea8e914722bc974",
    "bridge": "cb34f50ae8aec92e8e4f548fb7d7b4adee83a2881f7c08fd00c9550accbfa7da",
}

SCHEMA = "TPC394_C1_ORIGIN_UNIFORMITY_LADDER_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_ORIGIN_UNIFORMITY_LADDER_AUDIT"
PARENT_CODE_SHA256 = (
    "73ee391f0d4f467ee6fefdc57a1bb42dea93f01df2e2b22e35054b7a95cc6229")
PARENT_CERT_SHA256 = (
    "b983f4bae7836df57a8654fe51c37e72e28e1c0ca013aaaff71c9bdf79a229f1")
EXPECTED_PRODUCER_OUTPUT = (
    b"TPC394_CERTIFICATE=PASS rows=64 cells=8 "
    b"origin_passes={'local_diagonal': 1, 'pooled_train_scalar': 1, "
    b"'origin_scalar': 1, 'frozen_train_1024_scalar': 1} "
    b"transfer_passes={'local_diagonal': 2, 'pooled_train_scalar': 2, "
    b"'origin_scalar': 2, 'frozen_train_1024_scalar': 2} "
    b"spectral_failures=32 schur_failures=0\n")
EXPECTED_INDEPENDENT_OUTPUT = (
    b"TPC394_INDEPENDENT_CHECK=PASS rows=64 cells=8 "
    b"origin_passes={'frozen_train_1024_scalar': 1, 'local_diagonal': 1, "
    b"'origin_scalar': 1, 'pooled_train_scalar': 1} "
    b"transfer_passes={'frozen_train_1024_scalar': 2, 'local_diagonal': 2, "
    b"'origin_scalar': 2, 'pooled_train_scalar': 2} "
    b"spectral_failures=32 schur_failures=0\n")
EXPECTED_STRESS_OUTPUT = b"TPC394_STRESS=PASS mutations=25\n"
BRIDGE_PASS_OUTPUT = (
    "TPC394_BRIDGE_CHECK=PASS rows=64 cells=8 "
    "origin_passes=local:1/2,pooled:1/2,origin:1/2,frozen:1/2 "
    "transfer_passes=local:2/2,pooled:2/2,origin:2/2,frozen:2/2 "
    "spectral_failures=32 schur_failures=0 "
    "alternating_spread_max=0.092863374514779065")


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
         parent.get("parent_schema") ==
         "TPC393_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_V1" and
         parent.get("parent_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_AUDIT" and
         parent.get("parent_interface_frozen") is True and
         parent.get("parent_interface_used_for_current_fit") is False,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") ==
         [5000001, 5002006, 5004011, 5006016, 5008021, 5010026,
          5012031, 5014036] and
         selection.get("calibration_origins") ==
         [5000001, 5002006, 5004011, 5006016, 5008021] and
         selection.get("holdout_origins") == [5010026, 5012031, 5014036] and
         selection.get("window_count") == 1024 and
         selection.get("band_modes") == ["fixed_c3"] and
         selection.get("q_anchors") == [8192] and
         selection.get("laws") == ["all_plus", "alternating_index"] and
         selection.get("normalizations") == [
             "local_diagonal", "pooled_train_scalar", "origin_scalar",
             "frozen_train_1024_scalar"] and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("holdout_role_fixed_before_readout") is True and
         selection.get("parent_interface_used_for_current_fit") is False,
         "selection protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 64 and
         payload.get("row_digest") == hashlib.sha256(canonical(rows)).hexdigest(),
         "row census")
    expected_keys = {(origin, 8192, law, norm)
                     for origin in selection["origins"]
                     for law in ("all_plus", "alternating_index")
                     for norm in selection["normalizations"]}
    actual_keys = {(row.get("origin"), row.get("Q"), row.get("law"),
                    row.get("normalization")) for row in rows}
    need(actual_keys == expected_keys, "row keys")
    summary = payload.get("origin_summary", {})
    need(summary.get("row_count") == 64 and summary.get("cell_count") == 8 and
         summary.get("origin_uniformity_pass_counts") == {
             "local_diagonal": 1, "pooled_train_scalar": 1,
             "origin_scalar": 1, "frozen_train_1024_scalar": 1} and
         summary.get("holdout_transfer_pass_counts") == {
             "local_diagonal": 2, "pooled_train_scalar": 2,
             "origin_scalar": 2, "frozen_train_1024_scalar": 2} and
         summary.get("spectral_failures_by_normalization") == {
             "local_diagonal": 8, "pooled_train_scalar": 8,
             "origin_scalar": 8, "frozen_train_1024_scalar": 8} and
         summary.get("schur_failures_by_normalization") == {
             "local_diagonal": 0, "pooled_train_scalar": 0,
             "origin_scalar": 0, "frozen_train_1024_scalar": 0} and
         summary.get("origin_uniformity_stable_cells") == 4 and
         summary.get("holdout_transfer_stable_cells") == 8,
         "origin summary census")
    maximum = summary.get("maximum_all_origin_relative_spread", {})
    close(float(maximum["local_diagonal"]), 0.084824884787110394,
          "local spread maximum")
    close(float(maximum["pooled_train_scalar"]), 0.092862570673886716,
          "pooled spread maximum")
    close(float(maximum["origin_scalar"]), 0.092863374514779065,
          "origin spread maximum")
    close(float(maximum["frozen_train_1024_scalar"]), 0.092862570673886591,
          "frozen spread maximum")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC394_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC394_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC394_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC394_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC394_ORIGIN_LADDER_PANEL") ==
         "NUMERICALLY_CERTIFIED_FINITE_64_ROWS", "claim firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_ORIGIN_CROSS_FAMILY_HOLDOUT", "round2 clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [5000001, 5000014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True, "exact anchor")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 64 and audit.get("cell_count") == 8 and
         audit.get("complete_cartesian_panel") is True and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("same_count_across_all_origins") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC394_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC394_ORIGIN_LADDER_PANEL = NUMERICALLY_CERTIFIED_FINITE_64_ROWS",
            "TPC394_ORIGIN_UNIFORMITY_AUDIT = NUMERICALLY CERTIFIED FINITE SCOPED",
            "TPC394_ARITHMETIC_ADVANCE = NO",
            "TPC394_ROUND2_CLUE = TEST_C1_ORIGIN_CROSS_FAMILY_HOLDOUT"):
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
        print("TPC394_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
