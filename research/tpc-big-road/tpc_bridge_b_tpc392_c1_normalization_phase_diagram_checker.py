#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-392."""

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
PROJECT = ROOT / "papers/tpc-392-c1-normalization-phase-diagram"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc392_c1_normalization_phase_diagram.md"
PRODUCER = PROJECT / "code/tpc392_c1_normalization_phase_diagram.py"
INDEPENDENT = PROJECT / "experiments/tpc392_independent_checker.py"
STRESS = PROJECT / "experiments/tpc392_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc392_certificate.json"
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
    "producer": "0b0847dee598e598875c73684176b67cafd2eae74c25f62c48b48267009f7b4e",
    "independent": "5232e183dccb830c1b578645f3b14bcbc2c52f33d4d649bd64c97319f82a7748",
    "stress": "7d884235128458839651d10cf1b54bedd5aa8fd3e7384fe846e5869d7a716080",
    "certificate": "8481c38adffdf5ef51ca30fbf85b79deafc4ac7c499718509b6d35b243fe7e14",
    "main_tex": "aaaa03076242b229cb65b6702ebd04aad42d0aa3ab60975c26845e1716a594b5",
    "main_pdf": "801f01156c864c532c4a0ae9e3ee6397f5c9cd4fb1361bb12a0fefa26517b0b7",
    "pdf": "801f01156c864c532c4a0ae9e3ee6397f5c9cd4fb1361bb12a0fefa26517b0b7",
    "log": "2045aabfc81bf4292a54961226712efcb10356e78711d42966dd659a4ff4a814",
    "readme": "23601398984d545d4d2f081d3a999aaf4075527f9f81da9fbe93815aec936347",
    "plan": "5b6300c30b7e0823e8c5445cff4ad0acb0d8bf17ee1d527abfa4e42031086dc8",
    "derivation": "cf51e9d31283352050756b0ea1e919326f6858797e7eabe5e6731c7afcf765fa",
    "proof": "ad65d8994844ff4e190d775bb83cf555fb899a0f8e5bb1b9b4f9b910369bd5de",
    "claim": "1baeb666fbb7bbd7586a91b54eea43ef44db99a8dad2bd97f16dd7f049b50535",
    "route": "53a9eeae4171c3cd0e8a3b76a91661e338959904e20708cfc93376edca8fe058",
    "protocol": "3b14ad4ed886aa639509770de086cdb6f69b76a8738fbeb53e99077852c18c39",
    "theorem": "52d73c10f318c7952e8e54382a5429ba8c0dce235bf8b214844a4a400ee3f027",
    "bridge": "e40c5778b39a75e5ce7bf4364c5795d889faa70b6ac28e427dae462c892d1fe8",
}

SCHEMA = "TPC392_C1_NORMALIZATION_PHASE_DIAGRAM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_NORMALIZATION_PHASE_DIAGRAM_AUDIT"
PARENT_CERT_SHA256 = (
    "79727a822f1d3f98067af2b92cc89de38b06f17bfa833d28f19f908dfa54b095")
PARENT_CODE_SHA256 = (
    "a9ea75fc03e5e87ef9cd64dc638d87d549d78f225d66a18093aaa6897dfb3e98")
EXPECTED_PRODUCER_OUTPUT = (
    b"TPC392_CERTIFICATE=PASS rows=256 cells=32 "
    b"forecast_passes={'local_diagonal': 7, 'pooled_train_scalar': 8, "
    b"'origin_scalar': 8, 'frozen_train_1024_scalar': 8} spectral_failures=64 "
    b"schur_failures=0 stable_holdout=24/32 terminal_order="
    b"['frozen_train_1024_scalar', 'origin_scalar', 'pooled_train_scalar', "
    b"'local_diagonal']\n")
EXPECTED_INDEPENDENT_OUTPUT = (
    b"TPC392_INDEPENDENT_CHECK=PASS rows=256 cells=32 "
    b"forecast_passes={'frozen_train_1024_scalar': 8, 'local_diagonal': 7, "
    b"'origin_scalar': 8, 'pooled_train_scalar': 8} spectral_failures=64 "
    b"schur_failures=0 stable_holdout=24/32 terminal_order="
    b"['frozen_train_1024_scalar', 'origin_scalar', 'pooled_train_scalar', "
    b"'local_diagonal']\n")
EXPECTED_STRESS_OUTPUT = b"TPC392_STRESS=PASS mutations=25\n"
BRIDGE_PASS_OUTPUT = (
    "TPC392_BRIDGE_CHECK=PASS rows=256 cells=32 "
    "forecast_passes=local:7/8,pooled:8/8,origin:8/8,frozen:8/8 "
    "spectral_failures=64 schur_failures=0 stable_holdout=24/32 "
    "local_max_error=0.034106850682897649")


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
         "TPC391_C1_RECURSIVE_HORIZON_LOCALIZATION_V1" and
         parent.get("parent_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_RECURSIVE_HORIZON_LOCALIZATION_AUDIT" and
         parent.get("parent_interface_frozen") is True and
         parent.get("parent_interface_used_for_current_fit") is False,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") ==
         [3800001, 3804011, 3808021, 3812031, 3816041] and
         selection.get("calibration_origins") == [3800001, 3804011, 3808021] and
         selection.get("holdout_origins") == [3812031, 3816041] and
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
    need(isinstance(rows, list) and len(rows) == 256 and
         payload.get("row_digest") == hashlib.sha256(canonical(rows)).hexdigest(),
         "row census")
    summary = payload.get("transfer_summary", {})
    need(summary.get("row_count") == 256 and summary.get("cell_count") == 32 and
         summary.get("normalizations") == [
             "local_diagonal", "pooled_train_scalar", "origin_scalar",
             "frozen_train_1024_scalar"] and
         summary.get("forecast_pass_counts_by_normalization") == {
             "local_diagonal": 7, "pooled_train_scalar": 8,
             "origin_scalar": 8, "frozen_train_1024_scalar": 8} and
         summary.get("forecast_max_abs_error_by_normalization") == {
             "local_diagonal": "0.034106850682897649",
             "pooled_train_scalar": "0.0275714873542654",
             "origin_scalar": "0.028962999969161629",
             "frozen_train_1024_scalar": "0.02757148735426429"} and
         summary.get("terminal_mean_ordering") == [
             "frozen_train_1024_scalar", "origin_scalar",
             "pooled_train_scalar", "local_diagonal"] and
         summary.get("spectral_failures_by_normalization") == {
             "local_diagonal": 16, "pooled_train_scalar": 16,
             "origin_scalar": 16, "frozen_train_1024_scalar": 16} and
         summary.get("schur_failures_by_normalization") == {
             "local_diagonal": 0, "pooled_train_scalar": 0,
             "origin_scalar": 0, "frozen_train_1024_scalar": 0} and
         summary.get("stable_cells") == {"1024": 25, "1280": 28,
                                         "1536": 24} and
         isinstance(summary.get("cells"), list) and len(summary["cells"]) == 32,
         "phase summary")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 256 and audit.get("cell_count") == 32 and
         audit.get("complete_cartesian_panel") is True and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC392_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC392_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC392_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC392_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC392_NORMALIZATION_PANEL") ==
         "NUMERICALLY_CERTIFIED_FINITE_256_ROWS", "claim firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT", "round2 clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [3800001, 3800014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True, "exact anchor")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "NORMALIZATION_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS",
            "PHASE_COMPARISON = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT"):
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
        print("TPC392_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
