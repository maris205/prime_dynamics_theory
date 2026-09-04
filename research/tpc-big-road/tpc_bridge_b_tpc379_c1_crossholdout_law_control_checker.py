#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for the TPC-379 finite release."""

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
PROJECT = ROOT / "papers/tpc-379-c1-crossholdout-law-control"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc379_c1_crossholdout_law_control.md"
PRODUCER = PROJECT / "code/tpc379_c1_crossholdout_law_control.py"
INDEPENDENT = PROJECT / "experiments/tpc379_independent_checker.py"
STRESS = PROJECT / "experiments/tpc379_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc379_certificate.json"
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
    "producer": "5f4a32af562127a158dcb9232ecc6e380717c27145857b1f814734c5d0597b82",
    "independent": "13203d8759bd03b73910dd984d449571fd8d81d7ce81a053ab61c3167096e94d",
    "stress": "29004cd38416ba6a3805bb38d034aa24d33b2bd0f01b891758cbb97a849bc256",
    "certificate": "a41800cb32f59b2d025a808b92fb52567fbef661181f89889074b861c40504c7",
    "main_tex": "93aec9c2c3b9986b2517aa53fe8e5bc72668b0c90acd203e24e6beec5b5745bd",
    "main_pdf": "b64bcd333482309b076634362850c113a22b4e03f44c09f13cd8788c9c6639cb",
    "pdf": "b64bcd333482309b076634362850c113a22b4e03f44c09f13cd8788c9c6639cb",
    "log": "4413ab1c94cf14b8429df5efaae8d06e16e0574deba9b9e614941737a1cd2760",
    "readme": "b6a9a5fb119628fa1f7925ad511eda21deb9448c409a46583966e9a6e81ddeb5",
    "plan": "1f731ac8d3bc648a03ae462741a39cb89fd0ffe5a833f57de1e1245f94c0b836",
    "derivation": "839cb3e4e0e9f57e1fa71b2db1e6368df1a85311bd7dfb416291c738ae5521f7",
    "proof": "781979dea253120b76a967d8516dbec621ce588faedec9bba5a8a129f8396e83",
    "claim": "aa6878eb674e04e58d0f01055ea15ec1e377a0a0d92f1eab927d645a7febb3e3",
    "route": "ce80bb6c2fe61a788cb94d7f176a3a777724007c0f9ec9375e39123d08e1da0f",
    "protocol": "3f042fb895e38ce564f1f20b5aae87c201be2d6daf66ba5ff9b29a45145a018f",
    "theorem": "0fefc519277df314ddb6cb27f861d38ac72cfcaed65b3741a577382e7dac59df",
    "bridge": "f5d928be494d43e2c42db5e3a3b6c306df0368f092cbc65a01391752ff9e2806",
}

SCHEMA = "TPC379_C1_CROSSHOLDOUT_LAW_CONTROL_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL"
ORIGINS = [1200001, 1208021, 1216041]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
QS = [512, 2048, 8192]
PROFILE = {
    "all_plus": [0, 3, 3],
    "alternating_index": [0, 0, 0],
    "mod4_character": [0, 0, 0],
    "half_split": [0, 0, 0],
}
FIREWALL = {
    "TPC379_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC379_COORDINATE_DISJOINTNESS": "PROVED_EXACT_FINITE",
    "TPC379_COMMON_GEOMETRY":
        "PROVED_EXACT_FINITE_LAW_INDEPENDENT",
    "TPC379_LAW_FAMILY": "PROVED_EXACT_FINITE_PREDECLARED",
    "TPC379_LAW_CONTROL_REPLAY":
        "NUMERICALLY_CERTIFIED_FINITE_36_ROWS",
    "TPC379_ALL_PLUS_FAILURE_PROFILE":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC379_SIGNED_CONTROL_SUBCAP":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC379_RAYLEIGH_TAIL": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC379_LAW_UNIFORMITY": "OPEN",
    "TPC379_ORIGIN_UNIFORMITY": "OPEN",
    "TPC379_WINDOW_SCALE_UNIFORMITY": "OPEN",
    "TPC379_CROSS_BLOCK_CAUSALITY": "OPEN",
    "TPC379_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC379_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC379_SOURCE_UNIFORM_L2": "OPEN",
    "TPC379_ARITHMETIC_ADVANCE": "NO",
    "TPC379_FIXED_POWER_CREDIT": 0,
    "TPC379_FULL_GATE_B": "OPEN",
    "TPC379_TWIN_PRIME_RESULT": "NONE",
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
            "dd9289a390a1c52b9d22cd19766e4b2c5def87b6fa3c6eda530e4a81081997fa",
        "parent_certificate_sha256":
            "4846b4cfd0bfb75b9eebb95fcdfb33dc0365c3aba0b7080278be2be96df540d1",
        "parent_schema": "TPC378_C1_SCALE_ORIGIN_CROSSHOLDOUT_V1",
        "parent_round2_clue": "TEST_C1_CROSSHOLDOUT_LAW_CONTROL",
        "parent_profile": [0, 3, 3],
    }, "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("grid_start") == 1200001 and
         selection.get("grid_step") == 401 and
         selection.get("grid_count") == 41 and
         selection.get("candidate_origins") ==
         [1200001 + 401 * i for i in range(41)] and
         selection.get("origin_indices") == [0, 20, 40] and
         selection.get("origins") == ORIGINS and
         selection.get("window_count") == 1024 and
         selection.get("block_length") == 256 and
         selection.get("block_count") == 4 and
         selection.get("q_anchors") == QS and
         selection.get("laws") == LAWS and
         selection.get("response_used_for_selection") is False and
         selection.get("signed_metric_used_for_selection") is False and
         selection.get("panel_complete_before_metric_read") is True,
         "selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == ORIGINS and
         protocol.get("window_count") == 1024 and
         protocol.get("block_length") == 256 and
         protocol.get("block_count") == 4 and
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
        need(row.get("count") == 1024 and row.get("block_length") == 256 and
             row.get("block_count") == 4 and row.get("kernel_exponent") == 1 and
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
         "TEST_C1_LAW_CONTROL_COUNT_REPLAY", "clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [1200001, 1200014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("laws") == LAWS and
         anchor.get("geometry_positive") is True and
         anchor.get("matrix_symmetric_by_law") ==
         {law: True for law in LAWS} and
         anchor.get("geometry_digest") ==
         "4436feb8f2abf5450599e5d9185c28e245f07c9829000812e8ab0eb18726eb86",
         "exact anchor")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC379_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC379_LAW_CONTROL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_36_ROWS",
            "TPC379_ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_LAW_CONTROL_COUNT_REPLAY"):
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
             b"TPC379_CERTIFICATE=PASS rows=36 failures=6 "
             b"profiles=all_plus:0,3,3;alternating_index:0,0,0;"
             b"mod4_character:0,0,0;half_split:0,0,0" + bytes([10]),
             "producer output")
        need(normal[1] ==
             b"TPC379_INDEPENDENT_CHECK=PASS rows=36 failures=6 "
             b"profiles=all_plus:0,3,3;alternating_index:0,0,0;"
             b"mod4_character:0,0,0;half_split:0,0,0" + bytes([10]),
             "independent output")
        need(normal[2] == b"TPC379_STRESS=PASS mutations=25" + bytes([10]),
             "stress output")
        print("TPC379_BRIDGE_CHECK=PASS rows=36 failures=6 "
              "profiles=all_plus:0,3,3;alternating_index:0,0,0;"
              "mod4_character:0,0,0;half_split:0,0,0")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC379_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
