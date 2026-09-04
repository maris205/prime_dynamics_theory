#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-387."""

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
PROJECT = ROOT / "papers/tpc-387-c1-count-ladder-renormalization"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc387_c1_count_ladder_renormalization.md"
PRODUCER = PROJECT / "code/tpc387_c1_count_ladder_renormalization.py"
INDEPENDENT = PROJECT / "experiments/tpc387_independent_checker.py"
STRESS = PROJECT / "experiments/tpc387_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc387_certificate.json"
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
    "producer": "35a5f739e709ba14fc218fa7e52d9f587e8d0b7cbea76a22eb3cbedea775b2d7",
    "independent": "4c281e9adc34c1b2f897bb0febe82a906e4609cb8b1001bdbf04481583645495",
    "stress": "95f47aacd15326364936fdcb536125cdb37d4a33fee92e244ee05a89006625c7",
    "certificate": "337aa65feedd4c729cd34c7d6de8865baeb96c4888ab44fbdf00f840d079e344",
    "main_tex": "92bb127a4ff130eff5cdadf90a1fffe5d6ad665c53083f8378f0cf6439080fb4",
    "main_pdf": "0ba44838970367c52f2ac44c53644994050506e6c1907fe69239dc9f98990401",
    "pdf": "0ba44838970367c52f2ac44c53644994050506e6c1907fe69239dc9f98990401",
    "log": "5a50e4f00b3d85193c9f3f61ca1d636c488882daf1133fda18280f9af66a279e",
    "readme": "301dc8f81f118d12686741f87b13d92ee09160cbd5a3c1a57e4fa332792e7f9d",
    "plan": "9328e8e858eb9b3b9e852c48fff36df72cc422edd5e784d585f20055f1dbf8f9",
    "derivation": "13a0524903fcbb7f7e7b47bdf8cb57f2d6d5d3e47e1f544dc6478826888d9071",
    "proof": "290502d78804a1f391996db4b23f156cee3e5c15f4a53574cc292b12d4f2484a",
    "claim": "0a4a5283e4f90cf6b82b38ebf1058290f83c6aeadd4d14eda7af4bcb858f25cf",
    "route": "e9161b138e6314a7da18f253c2f08db683c46e407e505fe99198bd399dc34b5b",
    "protocol": "1dba7e63f65df2417bfb664dd9ee5c03ad7cb44539d4f3cb4ef0f5523ce47771",
    "theorem": "abd7183dee7ca6136b4e5c667d25dc20d96b0f3b84d562c58cdcfa22aeef0eee",
    "bridge": "5a79670df93a836a944897a2cca7d14ac6f8383536ff838ee124b335e16448a1",
}

SCHEMA = "TPC387_C1_COUNT_LADDER_RENORMALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_COUNT_LADDER_RENORMALIZATION"
ORIGINS = [2400001, 2404011, 2408021, 2412031, 2416041]
CALIBRATION = [2400001, 2404011, 2408021]
HOLDOUT = [2412031, 2416041]
CALIBRATION_COUNTS = [512, 768]
HOLDOUT_COUNT = 1024
MODES = ["fixed_c3", "full_relative"]
QS = [2048, 8192]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
NORMS = ["local_diagonal", "pooled_train_scalar"]


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


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
         "certificate payload")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")

    parent = payload.get("parent_lock", {})
    need(parent.get("parent_schema") ==
         "TPC386_C1_COUNT_HOLDOUT_BANDWIDTH_V1" and
         parent.get("forecast_is_fitted") is False and
         parent.get("parent_code_sha256") ==
         "24df166dee0b54f6503eb5dd03385e0702bb474ad0737a28c081a7d0dc1be006" and
         parent.get("parent_certificate_sha256") ==
         "4f34aee5970006efce06586c90ad599a7b484fdb9fea3921ffcfab7560d2a285",
         "parent lock")

    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") == ORIGINS and
         selection.get("calibration_origins") == CALIBRATION and
         selection.get("holdout_origins") == HOLDOUT and
         selection.get("calibration_counts") == CALIBRATION_COUNTS and
         selection.get("holdout_count") == HOLDOUT_COUNT and
         selection.get("band_modes") == MODES and
         selection.get("q_anchors") == QS and
         selection.get("laws") == LAWS and
         selection.get("normalizations") == NORMS and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("slope_fit_uses_holdout") is False, "selection")

    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 256, "row census")
    expected = ({(o, n, q, law, norm, mode)
                 for o in CALIBRATION for n in CALIBRATION_COUNTS
                 for q in QS for law in LAWS for norm in NORMS for mode in MODES} |
                {(o, HOLDOUT_COUNT, q, law, norm, mode)
                 for o in HOLDOUT for q in QS for law in LAWS
                 for norm in NORMS for mode in MODES})
    observed = {(r.get("origin"), r.get("count"), r.get("Q"),
                 r.get("law"), r.get("normalization"), r.get("band_mode"))
                for r in rows}
    need(observed == expected, "row keys")
    for row in rows:
        if row.get("origin") in CALIBRATION:
            expected_role = "calibration_" + str(row.get("count"))
            need(row.get("count") in CALIBRATION_COUNTS, "calibration count")
        else:
            expected_role = "holdout_1024"
            need(row.get("count") == HOLDOUT_COUNT, "holdout count")
        need(row.get("origin_role") == expected_role and
             isinstance(row.get("spectral_failure"), bool) and
             isinstance(row.get("schur_failure"), bool), "row roles")

    summary = payload.get("ladder_summary", {})
    need(summary.get("row_count") == 256 and
         summary.get("cell_count") == 32 and
         summary.get("renorm_pass_count_all_cells") == 32 and
         summary.get("stable_N512_cells") == 24 and
         summary.get("stable_N768_cells") == 24 and
         summary.get("stable_N1024_holdout_cells") == 28 and
         isinstance(summary.get("cells"), list) and len(summary["cells"]) == 32 and
         isinstance(summary.get("forecast_summary_all_plus_Q8192"), list) and
         len(summary["forecast_summary_all_plus_Q8192"]) == 4, "ladder summary")
    failures = summary.get("failure_counts_by_mode_normalization", {})
    need(isinstance(failures, dict) and len(failures) == 4 and
         sum(int(v.get("spectral", -1)) for v in failures.values()) == 40 and
         sum(int(v.get("schur", -1)) for v in failures.values()) == 0,
         "failure census")

    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 256 and audit.get("cell_count") == 32 and
         audit.get("calibration_counts") == CALIBRATION_COUNTS and
         audit.get("holdout_count") == HOLDOUT_COUNT and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "finite audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC387_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC387_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC387_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC387_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(payload.get("round2_clue") == "TEST_C1_COUNT_LADDER_SECOND_HOLDOUT",
         "round2 clue")

    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "COUNT_LADDER_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS",
            "CALIBRATION_SLOPE_REPAIR = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "RENORM_PASS = 32/32",
            "ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_COUNT_LADDER_SECOND_HOLDOUT"):
        need(bridge_text.count(marker) == 1, "bridge marker")

    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull ", "Underfull ",
                "LaTeX Error", "Fatal error", "Citation", "Empty"):
        need(bad not in log, "LaTeX diagnostic " + bad)
    main_pdf = MAIN_PDF.read_bytes()
    pdf = PDF.read_bytes()
    need(main_pdf == pdf and pdf.startswith(b"%PDF-") and len(pdf) > 100000,
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
        jobs = tuple((script, False) for script in (PRODUCER, INDEPENDENT, STRESS)) + \
               tuple((script, True) for script in (PRODUCER, INDEPENDENT, STRESS))
        with ThreadPoolExecutor(max_workers=6) as pool:
            outputs = tuple(pool.map(lambda job: run(*job), jobs))
        need(outputs[:3] == outputs[3:], "normal/optimized mismatch")
        need(outputs[0] ==
             b"TPC387_CERTIFICATE=PASS rows=256 cells=32 renorm_pass=32/32 "
             b"spectral_failures=40 stable_holdout=28/32\n", "producer output")
        need(outputs[1] ==
             b"TPC387_INDEPENDENT_CHECK=PASS rows=256 cells=32 renorm_pass=32/32 "
             b"spectral_failures=40 stable_holdout=28/32\n", "independent output")
        need(outputs[2] == b"TPC387_STRESS=PASS mutations=25\n",
             "stress output")
        print("TPC387_BRIDGE_CHECK=PASS rows=256 cells=32 renorm_pass=32/32 "
              "spectral_failures=40 stable_holdout=28/32")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC387_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
