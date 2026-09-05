#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-393."""

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
PROJECT = ROOT / "papers/tpc-393-c1-normalization-adversarial-holdout"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc393_c1_normalization_adversarial_holdout.md"
PRODUCER = PROJECT / "code/tpc393_c1_normalization_adversarial_holdout.py"
INDEPENDENT = PROJECT / "experiments/tpc393_independent_checker.py"
STRESS = PROJECT / "experiments/tpc393_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc393_certificate.json"
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
    "producer": "73ee391f0d4f467ee6fefdc57a1bb42dea93f01df2e2b22e35054b7a95cc6229",
    "independent": "f4b04b07242408ca331b971005ed3c54b35b50b1539b2a465becc550df5c84cc",
    "stress": "da83dff1196d1bcc51f314b34e805ebe60a4c553215da7f8d0da972a8f7c2821",
    "certificate": "b983f4bae7836df57a8654fe51c37e72e28e1c0ca013aaaff71c9bdf79a229f1",
    "main_tex": "2e1301947de763f61dd96a9c57539b58765bb09b80614ba9a424762225e60726",
    "main_pdf": "a47e69fafb59b96030ea345f9a391ef0c9d31324ce87cfb4ac1c9ab991ad14a8",
    "pdf": "a47e69fafb59b96030ea345f9a391ef0c9d31324ce87cfb4ac1c9ab991ad14a8",
    "log": "5a35486cabb632ca6706e9ccc3f1722937071e117cd9a88f1581ebf87d2aa237",
    "readme": "afcfe214710240b72533772d5a770aa6173aa5b9cc051266e17687343fab63ed",
    "plan": "63e0e103d5b097835851b3c4a041df637ad68d11d7689ab8759ecd49a862cd2a",
    "derivation": "e342a36cefe11f56800b09e3d9ce6f42766bb29fe6a9c2407c280257c1dcad88",
    "proof": "5eb05d8e8a2f731384e99e8ee6efa45c793a6e048c073cef53ad6735a5976e5b",
    "claim": "21d0652eb8d6f42898c5a133353a25bd219349219f31c5d2205fe616db1f9dac",
    "route": "ce5133e233313e760875a250cdc5e2a9363c52f96eee1fe18c91690783f8cb11",
    "protocol": "99925d74540958d147059a431f942b3f2e9ac81b0db0ec64878da29c3c774265",
    "theorem": "28da33725cc09341eb33685739f0fef15f156987ed0464a42add4770c4450913",
    "bridge": "b5ef67f6d5ba8d4203be0cd7648aa4d6caaa56749f55f057e147253df7e50957",
}

SCHEMA = "TPC393_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_AUDIT"
PARENT_CERT_SHA256 = (
    "8481c38adffdf5ef51ca30fbf85b79deafc4ac7c499718509b6d35b243fe7e14")
PARENT_CODE_SHA256 = (
    "0b0847dee598e598875c73684176b67cafd2eae74c25f62c48b48267009f7b4e")
EXPECTED_PRODUCER_OUTPUT = (
    b"TPC393_CERTIFICATE=PASS rows=64 cells=8 "
    b"forecast_passes={'local_diagonal': 2, 'pooled_train_scalar': 2, "
    b"'origin_scalar': 2, 'frozen_train_1024_scalar': 2} spectral_failures=32 "
    b"schur_failures=0 stable_holdout=4/8 terminal_order="
    b"['frozen_train_1024_scalar', 'origin_scalar', 'pooled_train_scalar', "
    b"'local_diagonal']\n")
EXPECTED_INDEPENDENT_OUTPUT = (
    b"TPC393_INDEPENDENT_CHECK=PASS rows=64 cells=8 "
    b"forecast_passes={'frozen_train_1024_scalar': 2, 'local_diagonal': 2, "
    b"'origin_scalar': 2, 'pooled_train_scalar': 2} spectral_failures=32 "
    b"schur_failures=0 stable_holdout=4/8 terminal_order="
    b"['frozen_train_1024_scalar', 'origin_scalar', 'pooled_train_scalar', "
    b"'local_diagonal']\n")
EXPECTED_STRESS_OUTPUT = b"TPC393_STRESS=PASS mutations=25\n"
BRIDGE_PASS_OUTPUT = (
    "TPC393_BRIDGE_CHECK=PASS rows=64 cells=8 "
    "forecast_passes=local:2/2,pooled:2/2,origin:2/2,frozen:2/2 "
    "spectral_failures=32 schur_failures=0 stable_holdout=4/8 "
    "local_max_error=0.01010300962072197")


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
         "TPC392_C1_NORMALIZATION_PHASE_DIAGRAM_V1" and
         parent.get("parent_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_NORMALIZATION_PHASE_DIAGRAM_AUDIT" and
         parent.get("parent_interface_frozen") is True and
         parent.get("parent_interface_used_for_current_fit") is False,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") ==
         [4200001, 4204011, 4208021, 4212031, 4216041] and
         selection.get("calibration_origins") == [4200001, 4204011, 4208021] and
         selection.get("holdout_origins") == [4212031, 4216041] and
         selection.get("calibration_counts") == [1024, 1280] and
         selection.get("holdout_count") == 1536 and
         selection.get("band_modes") == ["fixed_c3"] and
         selection.get("normalizations") == [
             "local_diagonal", "pooled_train_scalar", "origin_scalar",
             "frozen_train_1024_scalar"] and
         selection.get("response_used_for_selection") is False and
         selection.get("parent_interface_used_for_current_fit") is False and
         selection.get("holdout_role_fixed_before_readout") is True,
         "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 64 and
         payload.get("row_digest") == hashlib.sha256(canonical(rows)).hexdigest(),
         "row census")
    summary = payload.get("transfer_summary", {})
    need(summary.get("row_count") == 64 and summary.get("cell_count") == 8 and
         summary.get("normalizations") == [
             "local_diagonal", "pooled_train_scalar", "origin_scalar",
             "frozen_train_1024_scalar"] and
         summary.get("forecast_pass_counts_by_normalization") == {
             "local_diagonal": 2, "pooled_train_scalar": 2,
             "origin_scalar": 2, "frozen_train_1024_scalar": 2} and
         summary.get("forecast_max_abs_error_by_normalization") == {
             "local_diagonal": "0.01010300962072197",
             "pooled_train_scalar": "0.0097142554430971195",
             "origin_scalar": "0.011039357664235361",
             "frozen_train_1024_scalar": "0.0097142554430980077"} and
         summary.get("terminal_mean_ordering") == [
             "frozen_train_1024_scalar", "origin_scalar",
             "pooled_train_scalar", "local_diagonal"] and
         summary.get("spectral_failures_by_normalization") == {
             "local_diagonal": 8, "pooled_train_scalar": 8,
             "origin_scalar": 8, "frozen_train_1024_scalar": 8} and
         summary.get("schur_failures_by_normalization") == {
             "local_diagonal": 0, "pooled_train_scalar": 0,
             "origin_scalar": 0, "frozen_train_1024_scalar": 0} and
         summary.get("stable_cells") == {"1024": 4, "1280": 4,
                                         "1536": 4} and
         isinstance(summary.get("cells"), list) and len(summary["cells"]) == 8,
         "phase summary")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 64 and audit.get("cell_count") == 8 and
         audit.get("complete_cartesian_panel") is True and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC393_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC393_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC393_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC393_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC393_NORMALIZATION_PANEL") ==
         "NUMERICALLY_CERTIFIED_FINITE_64_ROWS", "claim firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_ORIGIN_UNIFORMITY_AFTER_REPLICATION", "round2 clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [4200001, 4200014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True, "exact anchor")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "NORMALIZATION_PANEL = NUMERICALLY_CERTIFIED_FINITE_64_ROWS",
            "PHASE_COMPARISON = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_ORIGIN_UNIFORMITY_AFTER_REPLICATION"):
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
        print("TPC393_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
