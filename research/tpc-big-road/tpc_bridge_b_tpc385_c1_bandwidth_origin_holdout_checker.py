#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-385."""

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
PROJECT = ROOT / "papers/tpc-385-c1-bandwidth-origin-holdout"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc385_c1_bandwidth_origin_holdout.md"
PRODUCER = PROJECT / "code/tpc385_c1_bandwidth_origin_holdout.py"
INDEPENDENT = PROJECT / "experiments/tpc385_independent_checker.py"
STRESS = PROJECT / "experiments/tpc385_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc385_certificate.json"
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
    "producer": "68825812bfffd90733472103fd4de200adb7b81ed3d02b57f992cc8d0d21e4b0",
    "independent": "98192a2313f8aa93590d646785ece9f83d2acfb0d17fe7f5885ac49df7aad18d",
    "stress": "20e90e1aac118f59e9e1fd6decc2623de686e8b87d7a5fd9ab7a5167a7dcc717",
    "certificate": "ecac4403e2f803fd36c764509f2cd7cbb385e8c45aa5bba103f5b734341f391e",
    "main_tex": "38be1c1e548e17857c6ffbe502d1b0dc7255dc781b2442613d3ddbc12ac36d4b",
    "main_pdf": "e2046b41bc69b27e43001e1c468b51d014e2aeb8f6388e3dfeed403cae544fee",
    "pdf": "e2046b41bc69b27e43001e1c468b51d014e2aeb8f6388e3dfeed403cae544fee",
    "log": "37a99c03f0f54832a9bf0e2b3af22fd136813aead25dcdc68d8ad9f3de3aac6a",
    "readme": "85d3453129ccaacdf1edf1dfe4c63c4b722b933ed3b0a2a572d8d5997a20285b",
    "plan": "ef768ca9a03ec4e1e4118ee82c004cc79089dba59cf5168b0f34fdf4e663e9cc",
    "derivation": "e279950f99f2e213a4e0f12da3c37d21cb12d77f0b5b12f673547e499196b909",
    "proof": "42fc5f0f226404233b4845a2802e58cb3da78bb3184e070d41f28668ab51a850",
    "claim": "f45bec115a262dbe17040e9fb3fa672960c235d1a51e99d2031cc690c45e8764",
    "route": "1b69ee85c9ecb449a808d19f43b6bae9d85f0626a43735b326a41970a929d73c",
    "protocol": "69e561098f2c4e31a6a535e213617c4b12f3fba4885d054c3c4cc0135e01af3c",
    "theorem": "d5ff609aa59806a4d6c4f923bb9da613e8db2c72b8f3e3d6ba0b8d01ecc7b31a",
    "bridge": "555e7c3670ed739155336d521f7f8488d427c4e1a619d48f14a7ca3dde9f3418",
}

SCHEMA = "TPC385_C1_BANDWIDTH_ORIGIN_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_BANDWIDTH_ORIGIN_HOLDOUT"
ORIGINS = [2000001, 2004011, 2008021, 2012031, 2016041]
CALIBRATION = [2000001, 2004011, 2008021]
HOLDOUT = [2012031, 2016041]
QS = [2048, 8192]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
NORMS = ["local_diagonal", "pooled_train_scalar"]
CUTOFFS = [2, 3]


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


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and finite_tree(payload) and
         payload.get("schema") == SCHEMA and payload.get("status") == STATUS,
         "payload")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    parent = payload.get("parent_lock", {})
    need(parent.get("forecast_is_fitted") is False and
         parent.get("parent_schema") ==
         "TPC384_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM_V1", "parent")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") == ORIGINS and
         selection.get("calibration_origins") == CALIBRATION and
         selection.get("holdout_origins") == HOLDOUT and
         selection.get("origin_indices") == [0, 10, 20, 30, 40] and
         selection.get("calibration_indices") == [0, 10, 20] and
         selection.get("holdout_indices") == [30, 40] and
         selection.get("window_count") == 512 and
         selection.get("block_length") == 128 and
         selection.get("band_cutoffs") == CUTOFFS and
         selection.get("q_anchors") == QS and
         selection.get("laws") == LAWS and
         selection.get("normalizations") == NORMS and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("holdout_role_fixed_before_readout") is True, "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 160, "row census")
    expected = {(o, q, law, norm, c) for o in ORIGINS for q in QS
                for law in LAWS for norm in NORMS for c in CUTOFFS}
    observed = {(r.get("origin"), r.get("Q"), r.get("law"),
                 r.get("normalization"), r.get("band_cutoff")) for r in rows}
    need(observed == expected, "row keys")
    need(all(r.get("origin_role") ==
             ("calibration" if r.get("origin") in CALIBRATION else "holdout")
             for r in rows), "row roles")
    phase = payload.get("phase_summary", {})
    need(phase.get("row_count") == 160 and phase.get("cell_count") == 32 and
         phase.get("stable_calibration_cells") == 26 and
         phase.get("stable_holdout_cells") == 28 and
         isinstance(phase.get("cells"), list) and len(phase["cells"]) == 32 and
         isinstance(phase.get("forecast_summary"), list) and
         len(phase["forecast_summary"]) == 4 and
         all(x.get("within_one_percent") is True
             for x in phase["forecast_summary"]), "phase")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [2000001, 2000014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True and
         anchor.get("band_cutoffs") == CUTOFFS, "anchor")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 160 and audit.get("cell_count") == 32 and
         audit.get("calibration_origin_count") == 3 and
         audit.get("holdout_origin_count") == 2 and
         audit.get("bandwidth_count") == 2 and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC385_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC385_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC385_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC385_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(payload.get("round2_clue") == "TEST_C1_HOLDOUT_COUNT_BANDWIDTH", "clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC385_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC385_ORIGIN_HOLDOUT_PANEL = NUMERICALLY_CERTIFIED_FINITE_160_ROWS",
            "TPC385_ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_HOLDOUT_COUNT_BANDWIDTH"):
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
        paths = {
            "producer": PRODUCER, "independent": INDEPENDENT, "stress": STRESS,
            "certificate": CERTIFICATE, "main_tex": MAIN_TEX,
            "main_pdf": MAIN_PDF, "pdf": PDF, "log": LOG, "readme": README,
            "plan": PLAN, "derivation": DERIVATION, "proof": PROOF,
            "claim": CLAIM, "route": ROUTE, "protocol": PROTOCOL,
            "theorem": THEOREM, "bridge": BRIDGE,
        }
        for key, path in paths.items():
            lock(path, LOCKS[key], key)
        check_certificate()
        jobs = tuple((script, False) for script in (PRODUCER, INDEPENDENT, STRESS)) + \
               tuple((script, True) for script in (PRODUCER, INDEPENDENT, STRESS))
        with ThreadPoolExecutor(max_workers=6) as pool:
            outputs = tuple(pool.map(lambda job: run(*job), jobs))
        need(outputs[:3] == outputs[3:], "normal/optimized mismatch")
        need(outputs[0] == b"TPC385_CERTIFICATE=PASS rows=160 cells=32 holdout_forecasts=4/4 stable_holdout=28/32\n",
             "producer output")
        need(outputs[1] == b"TPC385_INDEPENDENT_CHECK=PASS rows=160 cells=32 holdout_forecasts=4/4 stable_holdout=28/32\n",
             "independent output")
        need(outputs[2] == b"TPC385_STRESS=PASS mutations=25\n", "stress output")
        print("TPC385_BRIDGE_CHECK=PASS rows=160 cells=32 "
              "holdout_forecasts=4/4 stable_holdout=28/32")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC385_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
