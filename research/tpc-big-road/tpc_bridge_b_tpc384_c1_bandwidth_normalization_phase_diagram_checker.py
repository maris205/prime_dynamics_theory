#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-384."""

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
PROJECT = ROOT / "papers/tpc-384-c1-bandwidth-normalization-phase-diagram"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc384_c1_bandwidth_normalization_phase_diagram.md"
PRODUCER = PROJECT / "code/tpc384_c1_bandwidth_normalization_phase_diagram.py"
INDEPENDENT = PROJECT / "experiments/tpc384_independent_checker.py"
STRESS = PROJECT / "experiments/tpc384_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc384_certificate.json"
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
    "producer": "1a4e152e0753be3bc851a962aa92108334863795881571cbd7b97f119ee37896",
    "independent": "1e2b7ab310d8d999d87ab7158240da28cbbabb034b5416798e2a7dfb8fd62a30",
    "stress": "f1e574e758d440fe125a330c85dd5e39081857e70cb0943c551345569aa10590",
    "certificate": "5e43adf62e172947b66a84c18da1509e57e0e015146cc6755c6a2d31b7135ee7",
    "main_tex": "30f23e31aafb8793f25e8992b6a8de0f8e1b8e9eb8b7c5e084288e483f1e2c08",
    "main_pdf": "ba804620799f0932a774902bbe1ef02529130aecd28bd3e7ff06cadc11636d9e",
    "pdf": "ba804620799f0932a774902bbe1ef02529130aecd28bd3e7ff06cadc11636d9e",
    "log": "e09976a60d00adfe66b7c1c023da00086943d1e8d016527d0c2268310e5e4168",
    "readme": "e6b9d7d311df6a9aad980e5283af5250df606c071b33779bb53847a326a7525f",
    "plan": "45afe2709aa91e1690102e548c5dcdfb59cefa7de1f266dda1f6878515dbd2e0",
    "derivation": "1124299f3da2759eb7630c193e14ad1d857cb1c877ebebdd777e785577cd6517",
    "proof": "839280675d6677392100f81f7c6b1b2190421f56c27e3819b91628952ef3ae2a",
    "claim": "f74cedc34e59ece28c272e50c1f63cac54983c9226ee8840dfadf87455132748",
    "route": "4bcf126bbe03f1daa24e6c06d3a9e9cea902d6074568fef703bc7d0dac14111b",
    "protocol": "008c1fe91021b52e3b2c9a6f6ca53bfe2825e8497b61573a4fed0f44629acbe6",
    "theorem": "c71ded944ca4fa2c8e8c07374d1dfcde594a26c1576f75d116477b38aee8273f",
    "bridge": "6bafc94af119927885b7199b2a2bb8ee1dc7de93896ebd00e1b4914cd2bdcf88",
}

SCHEMA = "TPC384_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM"
ORIGINS = [1800001, 1808021, 1816041]
QS = [512, 2048, 8192]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
NORMS = ["local_diagonal", "pooled_scalar"]
CUTOFFS = [0, 1, 2, 3]
STABLE = {
    "c0_local_diagonal": 6, "c0_pooled_scalar": 7,
    "c1_local_diagonal": 8, "c1_pooled_scalar": 7,
    "c2_local_diagonal": 8, "c2_pooled_scalar": 8,
    "c3_local_diagonal": 8, "c3_pooled_scalar": 8,
}


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
    selection = payload.get("selection_protocol", {})
    need(selection.get("grid_start") == 1800001 and
         selection.get("grid_step") == 401 and selection.get("grid_count") == 41 and
         selection.get("origin_indices") == [0, 20, 40] and
         selection.get("origins") == ORIGINS and selection.get("window_count") == 512 and
         selection.get("block_length") == 128 and selection.get("block_count") == 4 and
         selection.get("band_cutoffs") == CUTOFFS and selection.get("q_anchors") == QS and
         selection.get("laws") == LAWS and selection.get("normalizations") == NORMS and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False, "selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == ORIGINS and protocol.get("window_count") == 512 and
         protocol.get("block_length") == 128 and protocol.get("block_count") == 4 and
         protocol.get("band_cutoffs") == CUTOFFS and protocol.get("q_anchors") == QS and
         protocol.get("laws") == LAWS and protocol.get("normalizations") == NORMS and
         protocol.get("source_response_used") is False and
         protocol.get("bandwidth_selection_used") is False and
         protocol.get("normalization_selection_used") is False, "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 288, "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    need({(r.get("origin"), r.get("Q"), r.get("law"), r.get("normalization"),
            r.get("band_cutoff")) for r in rows} ==
         {(o, q, law, norm, c) for o in ORIGINS for q in QS
          for law in LAWS for norm in NORMS for c in CUTOFFS}, "row keys")
    phase = payload.get("phase_summary", {})
    need(phase.get("row_count") == 288 and phase.get("cell_count") == 96 and
         phase.get("stable_cells_by_cutoff_normalization") == STABLE and
         isinstance(phase.get("cells"), list) and len(phase["cells"]) == 96,
         "phase")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [1800001, 1800014] and anchor.get("Q") == 8 and
         anchor.get("shell") == [11, 13] and anchor.get("band_cutoffs") == CUTOFFS and
         anchor.get("geometry_positive") is True, "anchor")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 288 and audit.get("cell_count") == 96 and
         audit.get("bandwidth_count") == 4 and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC384_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC384_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC384_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC384_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(payload.get("round2_clue") == "TEST_C1_BANDWIDTH_ORIGIN_HOLDOUT", "clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC384_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC384_BANDWIDTH_PHASE_PANEL = NUMERICALLY CERTIFIED FINITE_288_ROWS",
            "TPC384_ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_BANDWIDTH_ORIGIN_HOLDOUT"):
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
        need(outputs[0].startswith(b"TPC384_CERTIFICATE=PASS rows=288 cells=96 "),
             "producer output")
        need(outputs[1] == b"TPC384_INDEPENDENT_CHECK=PASS rows=288 cells=96 bandwidths=4 normalizations=2\n",
             "independent output")
        need(outputs[2] == b"TPC384_STRESS=PASS mutations=25\n", "stress output")
        print("TPC384_BRIDGE_CHECK=PASS rows=288 cells=96 bandwidths=4 normalizations=2")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC384_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
