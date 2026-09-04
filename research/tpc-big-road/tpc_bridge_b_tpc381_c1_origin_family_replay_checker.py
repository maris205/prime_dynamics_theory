#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for the TPC-381 finite release."""

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
PROJECT = ROOT / "papers/tpc-381-c1-origin-family-replay"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc381_c1_origin_family_replay.md"
PRODUCER = PROJECT / "code/tpc381_c1_origin_family_replay.py"
INDEPENDENT = PROJECT / "experiments/tpc381_independent_checker.py"
STRESS = PROJECT / "experiments/tpc381_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc381_certificate.json"
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
    "producer": "107932b1671c12baaabad0a53ff68a4944f6f54d45e88cfa4212468db0b7b354",
    "independent": "5227b6750149224ac57bf33f536a86c40d30ba52af26b9bcdc7ae407a3384e1b",
    "stress": "4cb31b886a6f249112afcbbe109d596ce3fd8b44d30c689ef87b4b45e0d3160d",
    "certificate": "c217a475d0e0a0aa440840e02f2e73bd0e0ba52f478143540dcd8772c4742c2b",
    "main_tex": "0b7ec09219e688a463e4f5c6e939403ceb9c25bb289fb38380b677f22021788d",
    "main_pdf": "35b5ccaac81d41fa75c4e2f7f26244acceeca330c321d9ef5ee43fa0fef6c389",
    "pdf": "35b5ccaac81d41fa75c4e2f7f26244acceeca330c321d9ef5ee43fa0fef6c389",
    "log": "5bf35992cd41f70546dfbbd8e23aecc1594ba58d45605ab382b88df76e9a86aa",
    "readme": "9be05139547c6aba62380414efe12eeeb38d7a3f1d9ba876d74b93b5ff49f32b",
    "plan": "cf40c249afbb336952f4a5e6956b06e589c71dd9557437613a669c72e47a4398",
    "derivation": "a4e645305d963ef3be4ce1cbebd71167969ee73ad757d0054a335b28ffb13add",
    "proof": "de8f9eb504da7a45ab02e317f92ed60d29e90127d2e0dfd6420f6f1d4da07438",
    "claim": "07a84ad9c188749a3ae80479b88e2fc8b884380151bf410116b545eb3ee1e56f",
    "route": "d36feffa82883910e2d604f9bd04d1f34b5474d90a2e925aac280db784698b55",
    "protocol": "da7c203d6d51ccbdaeeaa7ed56d28c10050e6053b29ba11252c5e27afa79b05f",
    "theorem": "030914f02689aef3b02ee9117197423297589c0d47be8bd1637f938c0c7c26aa",
    "bridge": "7430d5f0da8a1240e24dcf7a6dc986347be939f668f0d675e6ad0a16fc246e78",
}

SCHEMA = "TPC381_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY"
ORIGINS = [1400001, 1408021, 1416041]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
QS = [512, 2048, 8192]
PROFILE = {
    "all_plus": [0, 3, 3],
    "alternating_index": [0, 0, 0],
    "mod4_character": [0, 0, 0],
    "half_split": [0, 0, 0],
}
FIREWALL = {
    "TPC381_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC381_COORDINATE_DISJOINTNESS": "PROVED_EXACT_FINITE",
    "TPC381_COMMON_GEOMETRY":
        "PROVED_EXACT_FINITE_LAW_INDEPENDENT",
    "TPC381_LAW_FAMILY": "PROVED_EXACT_FINITE_PREDECLARED",
    "TPC381_ORIGIN_FAMILY_REPLAY":
        "NUMERICALLY_CERTIFIED_FINITE_36_ROWS",
    "TPC381_ALL_PLUS_FAILURE_PROFILE":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC381_SIGNED_CONTROL_SUBCAP":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC381_RAYLEIGH_TAIL": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC381_LAW_UNIFORMITY": "OPEN",
    "TPC381_ORIGIN_UNIFORMITY": "OPEN",
    "TPC381_WINDOW_SCALE_UNIFORMITY": "OPEN",
    "TPC381_CROSS_BLOCK_CAUSALITY": "OPEN",
    "TPC381_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC381_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC381_SOURCE_UNIFORM_L2": "OPEN",
    "TPC381_ARITHMETIC_ADVANCE": "NO",
    "TPC381_FIXED_POWER_CREDIT": 0,
    "TPC381_FULL_GATE_B": "OPEN",
    "TPC381_TWIN_PRIME_RESULT": "NONE",
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
            "8cb9e8373b51571b32fdbb0c6e1115274366b339371c59b1711ab166da7874ce",
        "parent_certificate_sha256":
            "c80dbfab3d375ac63b12c46dc2aaedc9718c21be0d8768d6e682c292619ddeeb",
        "parent_schema": "TPC380_C1_LAW_CONTROL_COUNT_REPLAY_V1",
        "parent_round2_clue": "TEST_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY",
        "parent_profile": [0, 3, 3],
    }, "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("grid_start") == 1400001 and
         selection.get("grid_step") == 401 and
         selection.get("grid_count") == 41 and
         selection.get("candidate_origins") ==
         [1400001 + 401 * i for i in range(41)] and
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
         "TEST_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT", "clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [1400001, 1400014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("laws") == LAWS and
         anchor.get("geometry_positive") is True and
         anchor.get("matrix_symmetric_by_law") ==
         {law: True for law in LAWS} and
         anchor.get("geometry_digest") ==
         "bf086c54b42280dda167bc5dc19f53c45afed4c5a51e0338a9555c65a6474d1f",
         "exact anchor")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC381_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC381_ORIGIN_FAMILY_REPLAY = NUMERICALLY_CERTIFIED_FINITE_36_ROWS",
            "TPC381_ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT"):
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
             b"TPC381_CERTIFICATE=PASS rows=36 failures=6 "
             b"profiles=all_plus:0,3,3;alternating_index:0,0,0;"
             b"mod4_character:0,0,0;half_split:0,0,0" + bytes([10]),
             "producer output")
        need(normal[1] ==
             b"TPC381_INDEPENDENT_CHECK=PASS rows=36 failures=6 "
             b"profiles=all_plus:0,3,3;alternating_index:0,0,0;"
             b"mod4_character:0,0,0;half_split:0,0,0" + bytes([10]),
             "independent output")
        need(normal[2] == b"TPC381_STRESS=PASS mutations=25" + bytes([10]),
             "stress output")
        print("TPC381_BRIDGE_CHECK=PASS rows=36 failures=6 "
              "profiles=all_plus:0,3,3;alternating_index:0,0,0;"
              "mod4_character:0,0,0;half_split:0,0,0")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC381_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
