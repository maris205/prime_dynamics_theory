#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-386."""

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
PROJECT = ROOT / "papers/tpc-386-c1-count-holdout-bandwidth"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc386_c1_count_holdout_bandwidth.md"
PRODUCER = PROJECT / "code/tpc386_c1_count_holdout_bandwidth.py"
INDEPENDENT = PROJECT / "experiments/tpc386_independent_checker.py"
STRESS = PROJECT / "experiments/tpc386_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc386_certificate.json"
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
    "producer": "24df166dee0b54f6503eb5dd03385e0702bb474ad0737a28c081a7d0dc1be006",
    "independent": "27f4b0f4fb286f1db4d44c4a7c7d5c1eb423f779e1b8a86f3440a1c010c46060",
    "stress": "28f6c354ce898caeebc199a970c16739235da8db98e2752694e5189e16cd254f",
    "certificate": "4f34aee5970006efce06586c90ad599a7b484fdb9fea3921ffcfab7560d2a285",
    "main_tex": "566221aa309937a64049f1d631a68b67afcd67821787917611ad02969ca74e92",
    "main_pdf": "0165405f9f0cc7d0b068522e21ff1442cc99eb9cce9688d7d14aa28e4a18427a",
    "pdf": "0165405f9f0cc7d0b068522e21ff1442cc99eb9cce9688d7d14aa28e4a18427a",
    "log": "a4d7b589eab0e5040aca609c727e2c6082e8b7c820cea9b3bb47134f62707acf",
    "readme": "ab877080d81b45846f7e669eca2b9c96af50179631a6f79abdaa86c43859f3aa",
    "plan": "4c3656979e6235a35c636b0861a4a0fd13865718703878a75f73b57762f67561",
    "derivation": "2135cbf4b1e87a1c1224ae052fe90a25b16c5e8209858c50ae8ef1938bc6749d",
    "proof": "480ccb11a0fa307cdfe2f28c7c9717032c4be9476e5a04e1a596b0cda1473c1d",
    "claim": "b81b077cac8fffe2ea433fb841c38838d53ccdf0c1e6398b974e90f4ed12bbc2",
    "route": "1151d224538915c11490d03966bf29db58cabdff44a45dd466f3dcc14ab48c17",
    "protocol": "a9c73cee237e549179c1494b4c56a7312c4bf2aa924e8873f2e0061165745d88",
    "theorem": "045936daf0be7b053f5f7e9de8190cbc9e16be00339ed64d99c4705eed5db968",
    "bridge": "d0988aa2f0957e3de2258a975906274ad0d4042b66f216dd28de738f80e09d8c",
}

SCHEMA = "TPC386_C1_COUNT_HOLDOUT_BANDWIDTH_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_COUNT_HOLDOUT_BANDWIDTH"
ORIGINS = [2200001, 2204011, 2208021, 2212031, 2216041]
CALIBRATION = [2200001, 2204011, 2208021]
HOLDOUT = [2212031, 2216041]
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
         "payload")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    parent = payload.get("parent_lock", {})
    need(parent.get("forecast_is_fitted") is False and
         parent.get("parent_schema") ==
         "TPC385_C1_BANDWIDTH_ORIGIN_HOLDOUT_V1", "parent")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") == ORIGINS and
         selection.get("calibration_origins") == CALIBRATION and
         selection.get("holdout_origins") == HOLDOUT and
         selection.get("calibration_count") == 512 and
         selection.get("holdout_count") == 1024 and
         selection.get("band_modes") == MODES and
         selection.get("q_anchors") == QS and
         selection.get("laws") == LAWS and
         selection.get("normalizations") == NORMS and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("holdout_role_fixed_before_readout") is True, "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 160, "row census")
    expected = {(o, q, law, norm, mode) for o in ORIGINS for q in QS
                for law in LAWS for norm in NORMS for mode in MODES}
    observed = {(r.get("origin"), r.get("Q"), r.get("law"),
                 r.get("normalization"), r.get("band_mode")) for r in rows}
    need(observed == expected, "row keys")
    need(all(r.get("origin_role") ==
             ("calibration" if r.get("origin") in CALIBRATION else "holdout")
             and r.get("count") == (512 if r.get("origin") in CALIBRATION else 1024)
             for r in rows), "row roles/counts")
    summary = payload.get("count_summary", {})
    need(summary.get("row_count") == 160 and summary.get("cell_count") == 32 and
         summary.get("stable_holdout_cells") == 28 and
         isinstance(summary.get("cells"), list) and len(summary["cells"]) == 32 and
         isinstance(summary.get("forecast_summary"), list) and
         len(summary["forecast_summary"]) == 4 and
         all(x.get("within_parent_reference_cap") is True
             for x in summary["forecast_summary"]), "summary")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 160 and audit.get("cell_count") == 32 and
         audit.get("calibration_count") == 512 and
         audit.get("holdout_count") == 1024 and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC386_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC386_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC386_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC386_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_COUNT_LADDER_RENORMALIZATION", "clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "COUNT_HOLDOUT_PANEL = NUMERICALLY_CERTIFIED_FINITE_160_ROWS",
            "FIXED_SPECTRAL_CAP_TRANSFER = REFUTED_FINITE_SCOPED",
            "ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_COUNT_LADDER_RENORMALIZATION"):
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
        need(outputs[0] ==
             b"TPC386_CERTIFICATE=PASS rows=160 cells=32 forecast_cap=4/4 "
             b"spectral_failures=16 stable_holdout=28/32\n", "producer output")
        need(outputs[1] ==
             b"TPC386_INDEPENDENT_CHECK=PASS rows=160 cells=32 forecast_cap=4/4 "
             b"spectral_failures=16 stable_holdout=28/32\n", "independent output")
        need(outputs[2] == b"TPC386_STRESS=PASS mutations=25\n", "stress output")
        print("TPC386_BRIDGE_CHECK=PASS rows=160 cells=32 forecast_cap=4/4 "
              "spectral_failures=16 stable_holdout=28/32")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC386_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
