#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for the TPC-380 finite release."""

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
PROJECT = ROOT / "papers/tpc-380-c1-law-control-count-replay"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc380_c1_law_control_count_replay.md"
PRODUCER = PROJECT / "code/tpc380_c1_law_control_count_replay.py"
INDEPENDENT = PROJECT / "experiments/tpc380_independent_checker.py"
STRESS = PROJECT / "experiments/tpc380_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc380_certificate.json"
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

# The checker intentionally does not lock its own source.
LOCKS = {
    "producer": "8cb9e8373b51571b32fdbb0c6e1115274366b339371c59b1711ab166da7874ce",
    "independent": "59fc81fb0f2943ecc82311204086379751e98ac2ebc859411982f4e39bcb6791",
    "stress": "ceec8741f876f16883f8b305b5e90d05cd36d1d4dddab4b6c8fe2b3c0cff859f",
    "certificate": "c80dbfab3d375ac63b12c46dc2aaedc9718c21be0d8768d6e682c292619ddeeb",
    "main_tex": "381a85624245b7177946e9678b6ff7bb50184a4fe5dc0cc72874e679d6d0c2c6",
    "main_pdf": "c07083ac9e6faabdf9066f0c736eee8c84bbb476c73af0241f15600b7db92eeb",
    "pdf": "c07083ac9e6faabdf9066f0c736eee8c84bbb476c73af0241f15600b7db92eeb",
    "log": "879518aa077fa8056e21546ce5bca53097f8b03c08d1b7c0672e831b5173bb53",
    "readme": "c4f99144064a2e16de0d894990bfcfd6b5cfbb6fae10991099c6d03233fc29a7",
    "plan": "096e1fd51d6606f1e719999de23eb518c7c82878367ea46a7072c90248c96dff",
    "derivation": "e137365908665381774b263844cba62cdec225cd8c84d30af54d01baaacf5820",
    "proof": "ba1470eea079ffd56dc2862913a5bc4a51100dc70dd1ecd3148d32f9978bc4e4",
    "claim": "96f5d97e6be873e6f2fc15e19a025198d3cb5eb296af8013438dc89907d5bdb2",
    "route": "0a8a16621e24d2e78f5440f3d25f749ca950613bcf717be38037d5076cb664bb",
    "protocol": "1829a1907ac23f76448c97c27e0dc594dabff7d71cfedfdda4ed16884567abb1",
    "theorem": "e57cae0d2a9915afa6b7628d5c88fb8240b51f897d6b9845ee55dee80f6aaafa",
    "bridge": "eba7b581bd805426b80655e07d982d14583e2e62240cecaaad67558acfe9d8f7",
}

SCHEMA = "TPC380_C1_LAW_CONTROL_COUNT_REPLAY_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL_COUNT_REPLAY"
ORIGINS = [1300001, 1308021, 1316041]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
QS = [512, 2048, 8192]
PROFILE = {
    "all_plus": [0, 3, 3],
    "alternating_index": [0, 0, 0],
    "mod4_character": [0, 0, 0],
    "half_split": [0, 0, 0],
}
FIREWALL = {
    "TPC380_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC380_COORDINATE_DISJOINTNESS": "PROVED_EXACT_FINITE",
    "TPC380_COMMON_GEOMETRY":
        "PROVED_EXACT_FINITE_LAW_INDEPENDENT",
    "TPC380_LAW_FAMILY": "PROVED_EXACT_FINITE_PREDECLARED",
    "TPC380_COUNT_REPLAY":
        "NUMERICALLY_CERTIFIED_FINITE_36_ROWS",
    "TPC380_ALL_PLUS_FAILURE_PROFILE":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC380_SIGNED_CONTROL_SUBCAP":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC380_RAYLEIGH_TAIL": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC380_LAW_UNIFORMITY": "OPEN",
    "TPC380_ORIGIN_UNIFORMITY": "OPEN",
    "TPC380_WINDOW_SCALE_UNIFORMITY": "OPEN",
    "TPC380_CROSS_BLOCK_CAUSALITY": "OPEN",
    "TPC380_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC380_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC380_SOURCE_UNIFORM_L2": "OPEN",
    "TPC380_ARITHMETIC_ADVANCE": "NO",
    "TPC380_FIXED_POWER_CREDIT": 0,
    "TPC380_FULL_GATE_B": "OPEN",
    "TPC380_TWIN_PRIME_RESULT": "NONE",
}


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(bytes([13, 10]), bytes([10]))
                          .replace(bytes([13]), bytes([10]))).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + chr(10)).encode("ascii")


def lock(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED" and path.is_file() and
         digest(path.read_bytes()) == expected, label + " provenance")


def finite_tree(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and finite_tree(v)
                   for k, v in value.items())
    if isinstance(value, list):
        return all(finite_tree(v) for v in value)
    return True


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and finite_tree(payload), "payload")
    need(payload.get("schema") == SCHEMA and payload.get("status") == STATUS and
         document.get("payload_sha256") ==
         hashlib.sha256(canonical(payload)).hexdigest(), "schema/hash")
    need(payload.get("parent_lock") == {
        "parent_code_sha256":
            "5f4a32af562127a158dcb9232ecc6e380717c27145857b1f814734c5d0597b82",
        "parent_certificate_sha256":
            "a41800cb32f59b2d025a808b92fb52567fbef661181f89889074b861c40504c7",
        "parent_schema": "TPC379_C1_CROSSHOLDOUT_LAW_CONTROL_V1",
        "parent_round2_clue": "TEST_C1_LAW_CONTROL_COUNT_REPLAY",
        "parent_profile": [0, 3, 3],
    }, "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("grid_start") == 1300001 and
         selection.get("grid_step") == 401 and
         selection.get("grid_count") == 41 and
         selection.get("candidate_origins") ==
         [1300001 + 401 * i for i in range(41)] and
         selection.get("origin_indices") == [0, 20, 40] and
         selection.get("origins") == ORIGINS and
         selection.get("window_count") == 2048 and
         selection.get("block_length") == 256 and
         selection.get("block_count") == 8 and
         selection.get("q_anchors") == QS and
         selection.get("laws") == LAWS and
         selection.get("response_used_for_selection") is False and
         selection.get("signed_metric_used_for_selection") is False and
         selection.get("panel_complete_before_metric_read") is True,
         "selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == ORIGINS and
         protocol.get("window_count") == 2048 and
         protocol.get("block_length") == 256 and
         protocol.get("block_count") == 8 and
         protocol.get("band_cutoff") == 1 and
         protocol.get("q_anchors") == QS and
         protocol.get("kernel_exponents") == [1] and
         protocol.get("laws") == LAWS and protocol.get("betas") == [2] and
         protocol.get("height") == 66 and
         protocol.get("common_geometry") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False and
         protocol.get("law_selection_used") is False and
         protocol.get("row_selection_used") is False,
         "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 36, "row count")
    need({(r.get("origin"), r.get("Q"), r.get("law")) for r in rows} ==
         {(o, q, law) for o in ORIGINS for q in QS for law in LAWS},
         "row keys")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    for row in rows:
        need(row.get("count") == 2048 and row.get("block_length") == 256 and
             row.get("block_count") == 8 and row.get("kernel_exponent") == 1 and
             row.get("beta") == 2 and row.get("height") == 66 and
             row.get("law") in LAWS and
             row.get("band_failure") in (True, False) and
             row.get("schur_failure") in (True, False), "row header")
    phase = payload.get("phase_summary", {})
    need(phase.get("rows") == 36 and phase.get("laws") == LAWS and
         phase.get("law_count") == 4 and
         phase.get("failure_profile_by_law_Q") == PROFILE and
         phase.get("spectral_cap_violations") == 6 and
         phase.get("schur_cap_violations") == 0 and
         phase.get("signed_controls_all_below_spectral_cap") is True and
         phase.get("caps") == {
             "spectral": "0.64000000000000001",
             "schur": "0.82999999999999996"}, "phase")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 36 and audit.get("origin_count") == 3 and
         audit.get("q_count") == 3 and audit.get("law_count") == 4 and
         audit.get("spectral_rows") == 36 and
         audit.get("spectral_cap_violations") == 6 and
         audit.get("schur_cap_violations") == 0 and
         audit.get("failure_profile_by_law_Q") == PROFILE and
         audit.get("all_plus_failure_profile") == [0, 3, 3] and
         audit.get("signed_control_failure_profiles") == {
             law: [0, 0, 0] for law in LAWS if law != "all_plus"} and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("law_control_complete") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    need(payload.get("claim_firewall") == FIREWALL, "claim firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY", "clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [1300014, 1300027] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("laws") == LAWS and
         anchor.get("geometry_positive") is True and
         anchor.get("matrix_symmetric_by_law") ==
         {law: True for law in LAWS} and
         anchor.get("geometry_digest") ==
         "d17b892caed9169be686d11e0e20cec8397e14834693e47a83fd972cb2423bd5",
         "exact anchor")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC380_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC380_COUNT_REPLAY = NUMERICALLY_CERTIFIED_FINITE_36_ROWS",
            "TPC380_ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY"):
        need(bridge_text.count(marker) == 1, "bridge marker")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull ", "Underfull ",
                "LaTeX Error", "Fatal error", "Citation", "Empty"):
        need(bad not in log, "LaTeX diagnostic " + bad)
    main_pdf = MAIN_PDF.read_bytes()
    pdf = PDF.read_bytes()
    need(main_pdf == pdf and pdf.startswith(b"%PDF-") and
         len(pdf) > 100000, "PDF identity")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script), "--check"])
    environment = dict(os.environ)
    environment.update({
        "PYTHONDONTWRITEBYTECODE": "1",
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
    })
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed " + script.name)
    return result.stdout


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        paths = {
            "producer": PRODUCER, "independent": INDEPENDENT,
            "stress": STRESS, "certificate": CERTIFICATE,
            "main_tex": MAIN_TEX, "main_pdf": MAIN_PDF, "pdf": PDF,
            "log": LOG, "readme": README, "plan": PLAN,
            "derivation": DERIVATION, "proof": PROOF, "claim": CLAIM,
            "route": ROUTE, "protocol": PROTOCOL, "theorem": THEOREM,
            "bridge": BRIDGE,
        }
        for key, path in paths.items():
            lock(path, LOCKS[key], key)
        check_certificate()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        jobs = tuple((script, False) for script in scripts) + \
               tuple((script, True) for script in scripts)
        with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
            outputs = tuple(pool.map(lambda job: run(*job), jobs))
        normal, optimized = outputs[:3], outputs[3:]
        need(normal == optimized, "normal/optimized stdout mismatch")
        need(normal[0] ==
             b"TPC380_CERTIFICATE=PASS rows=36 failures=6 "
             b"profiles=all_plus:0,3,3;alternating_index:0,0,0;"
             b"mod4_character:0,0,0;half_split:0,0,0" + bytes([10]),
             "producer output")
        need(normal[1] ==
             b"TPC380_INDEPENDENT_CHECK=PASS rows=36 failures=6 "
             b"profiles=all_plus:0,3,3;alternating_index:0,0,0;"
             b"mod4_character:0,0,0;half_split:0,0,0" + bytes([10]),
             "independent output")
        need(normal[2] == b"TPC380_STRESS=PASS mutations=25" + bytes([10]),
             "stress output")
        print("TPC380_BRIDGE_CHECK=PASS rows=36 failures=6 "
              "profiles=all_plus:0,3,3;alternating_index:0,0,0;"
              "mod4_character:0,0,0;half_split:0,0,0")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC380_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
