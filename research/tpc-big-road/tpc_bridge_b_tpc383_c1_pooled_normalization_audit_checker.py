#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-383."""

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
PROJECT = ROOT / "papers/tpc-383-c1-pooled-normalization-audit"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc383_c1_pooled_normalization_audit.md"
PRODUCER = PROJECT / "code/tpc383_c1_pooled_normalization_audit.py"
INDEPENDENT = PROJECT / "experiments/tpc383_independent_checker.py"
STRESS = PROJECT / "experiments/tpc383_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc383_certificate.json"
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
    "producer": "3593d9db35080d9aae3e8d7e6f2d8d9a5111a4ccd7e8c847a8a33d4eadc2ba48",
    "independent": "d9a67972a0fc967aaad4209492d48747a39aba25d17c70e89a68b971c9035730",
    "stress": "d90d8ec1dea616daa553af431779d492d487a67f0d8c8846830f7dd503e7ae7c",
    "certificate": "eb6be49c04a196e3cf0aed0fa996960058bc219f391047d090bde21d130d29ee",
    "main_tex": "32e89a786ef1a9e88d28ce06f2ace80b84423207a5dccef5da4d79292112f4e4",
    "main_pdf": "5c4476862008c32d13c5077a02b14a21c39370c83beff813b920734adfd7a9c0",
    "pdf": "5c4476862008c32d13c5077a02b14a21c39370c83beff813b920734adfd7a9c0",
    "log": "959a3d32fc7fd307541c42f216378e0e40d67a27752a0350217c853caaec8564",
    "readme": "19491de68608e4007d031dd6b090e599e3fd38ecf8d8368b12a86edb0bb19eed",
    "plan": "666fac7ec497f48b1ba9e87c7463259fd86e56269ed17e7b3c94d62e85844008",
    "derivation": "ea872fb8b2c9fda5a57f2b0812dadb7ed5fe2bc3182161579339a6dbe53aa3f1",
    "proof": "aa017aa05813f81468b44945928ea699686aff4c63e6f752efc8fa318679f355",
    "claim": "8472099a52e9f8cde3cf996d2d13227a9e420bf8c380e471328f078ade9abab1",
    "route": "ea0637ee40dffb48d71bf9d2fdcc055a25a1b6cb24e0ff713dc375a95a62c0e4",
    "protocol": "d261cb87335f8d3b9594808d55c0bd5565f03394cf82bde1e4de39004720281c",
    "theorem": "5b11928d62168e3e248acedafdd9352ca27fc97d9e8c5248672d3cafa3ea9455",
    "bridge": "dd7eeb3abbb16915abadf90aa9718f5f59fc0a404bf5695c7d8be9b448dec3bc",
}

SCHEMA = "TPC383_C1_POOLED_NORMALIZATION_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_POOLED_NORMALIZATION_AUDIT"


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
    need(selection.get("grid_start") == 1600001 and
         selection.get("grid_step") == 401 and
         selection.get("grid_count") == 41 and
         selection.get("origin_indices") == [0, 20, 40] and
         selection.get("origins") == [1600001, 1608021, 1616041] and
         selection.get("window_count") == 512 and
         selection.get("block_length") == 128 and
         selection.get("q_anchors") == [512, 2048, 8192] and
         selection.get("laws") ==
         ["all_plus", "alternating_index", "mod4_character", "half_split"] and
         selection.get("normalizations") == ["local_diagonal", "pooled_scalar"] and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("spread_cap") == "0.01", "selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [1600001, 1608021, 1616041] and
         protocol.get("window_count") == 512 and
         protocol.get("block_length") == 128 and
         protocol.get("block_count") == 4 and
         protocol.get("band_cutoff") == 1 and
         protocol.get("normalizations") == ["local_diagonal", "pooled_scalar"] and
         protocol.get("source_response_used") is False and
         protocol.get("normalization_selection_used") is False, "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 72, "row census")
    need(len({(r.get("origin"), r.get("Q"), r.get("law"),
               r.get("normalization")) for r in rows}) == 72, "row keys")
    phase = payload.get("phase_summary", {})
    need(phase.get("row_count") == 72 and phase.get("cell_count") == 24 and
         phase.get("stable_cells_local") == 9 and
         phase.get("stable_cells_pooled") == 9 and
         phase.get("all_plus_high_q_local_stable") is True and
         phase.get("all_plus_high_q_pooled_stable") is True and
         float(phase.get("all_plus_high_q_pooled_vs_local_relative_shift")) > 0.03,
         "phase")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [1600001, 1600014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True, "anchor")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 72 and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC383_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC383_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC383_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC383_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM", "clue")
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
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "OMP_NUM_THREADS": "1",
                "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
    result = subprocess.run(command, cwd=ROOT, env=env,
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
             b"TPC383_CERTIFICATE=PASS rows=72 local_stable=9 pooled_stable=9 "
             b"all_plus_high_q_transfer=True\n", "producer output")
        need(outputs[1] ==
             b"TPC383_INDEPENDENT_CHECK=PASS rows=72 local_stable=9 pooled_stable=9 "
             b"all_plus_high_q_transfer=True\n", "independent output")
        need(outputs[2] == b"TPC383_STRESS=PASS mutations=25\n", "stress output")
        print("TPC383_BRIDGE_CHECK=PASS rows=72 local_stable=9 pooled_stable=9 "
              "all_plus_high_q_transfer=True")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC383_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
