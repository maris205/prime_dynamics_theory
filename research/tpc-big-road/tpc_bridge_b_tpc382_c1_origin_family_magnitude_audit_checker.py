#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-382."""

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
PROJECT = ROOT / "papers/tpc-382-c1-origin-family-magnitude-audit"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc382_c1_origin_family_magnitude_audit.md"
PRODUCER = PROJECT / "code/tpc382_c1_origin_family_magnitude_audit.py"
INDEPENDENT = PROJECT / "experiments/tpc382_independent_checker.py"
STRESS = PROJECT / "experiments/tpc382_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc382_certificate.json"
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
    "producer": "d68231e2f547f6102373f3c34e013663eb350e6ede59cf805d7b2f7b35d3e215",
    "independent": "c480b97fb9368bb403c4ed315a3e2e834f6eaad579f6787a8b7b90aee8074eaa",
    "stress": "a3fb4f928a9044fe8f10c2546bbaaf2a12e3d6519d3d9c9f20a14269218ee745",
    "certificate": "1bd35889f40e911aa2faa4f2f5a636583f905a388b0dda0417c1ed031f492b6e",
    "main_tex": "f1b2e8f52496c7a698b5bb281ba5b28691be833e52f902c8e2fe7d014766e187",
    "main_pdf": "95cb42b1553d89b930280b485a040f5b68f5297a63c10fcdaed594d28afcc2e1",
    "pdf": "95cb42b1553d89b930280b485a040f5b68f5297a63c10fcdaed594d28afcc2e1",
    "log": "8e24e46bc22da91389e5561c0260155bffffafe6c2cb0dc97b3d451bb16e90fe",
    "readme": "7d2f1511df46f80d033f9ae9584a5361806fa4addaf31989614aa25168889a3d",
    "plan": "27f9d62311c140c53ba27651586b854f7a6f6c7b6e640da7cf49364c1f9997c6",
    "derivation": "cb6960d672f682aa575a2219b330d01a4d1d801f2302df51aa479505fa529cd3",
    "proof": "52b0d48440a050e5f8e7e864116b6c61c7fbecae456d03e89b336cbff9b5fd65",
    "claim": "5ea0f556f9c63b5a7aafdd6bd6aa23a9dec98b133a0bd07527ebec493bc8b2a7",
    "route": "6c1bc9f6c6f3765e519e498f3b89684eab5c987d1508708b5431b90fb98e969f",
    "protocol": "666955cdadc01ad6a4bb761eea036d3f10fac6def41203cdecfdc36c03c7dba3",
    "theorem": "47fcd0a60180472ca41b119738d0887944a27bb1f8e88ed184684e7bd0d2d116",
    "bridge": "4d593ebc55eb1ae744abf14e960bbe2d6b6572531c0e6348071b1d8d37009c9c",
}

SCHEMA = "TPC382_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT"


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
         "payload header")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    selection = payload.get("selection_protocol", {})
    need(selection.get("parent_panels_fixed_before_metric_read") is True and
         selection.get("parent_hashes_fixed_before_aggregation") is True and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("same_count_labels") == ["TPC380", "TPC381"] and
         selection.get("scale_control_label") == "TPC379" and
         selection.get("relative_spread_cap") == "0.01" and
         selection.get("scale_contrast_cap") == "0.01" and
         selection.get("high_q") == 8192, "selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("same_count") == 2048 and
         protocol.get("same_count_panels") == ["TPC380", "TPC381"] and
         protocol.get("scale_control_count") == 1024 and
         protocol.get("same_count_value_count") == 72 and
         protocol.get("scale_control_value_count") == 36 and
         protocol.get("cells_per_panel") == 12, "protocol")
    same = payload.get("same_count_cells")
    scale = payload.get("scale_control_cells")
    contrasts = payload.get("scale_contrasts")
    need(isinstance(same, list) and len(same) == 12 and
         isinstance(scale, list) and len(scale) == 12 and
         isinstance(contrasts, list) and len(contrasts) == 12,
         "cell census")
    summary = payload.get("phase_summary", {})
    need(summary.get("same_count_values") == 72 and
         summary.get("same_count_cells") == 12 and
         summary.get("same_count_cells_within_one_percent") == 8 and
         summary.get("signed_cells_over_one_percent") == 4 and
         summary.get("all_plus_high_q_within_one_percent") is True and
         summary.get("all_plus_high_q_scale_within_one_percent") is False,
         "summary")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC382_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC382_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC382_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC382_TWIN_PRIME_RESULT") == "NONE",
         "firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_POOLED_NORMALIZATION_CROSS_ORIGIN", "clue")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script), "--check"])
    environment = dict(os.environ)
    environment.update({"PYTHONDONTWRITEBYTECODE": "1"})
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
        jobs = tuple((script, False) for script in (PRODUCER, INDEPENDENT, STRESS)) + \
               tuple((script, True) for script in (PRODUCER, INDEPENDENT, STRESS))
        with ThreadPoolExecutor(max_workers=6) as pool:
            outputs = tuple(pool.map(lambda job: run(*job), jobs))
        need(outputs[:3] == outputs[3:], "normal/optimized mismatch")
        need(outputs[0] ==
             b"TPC382_CERTIFICATE=PASS cells=12 same_values=72 stable_cells=8 "
             b"signed_over_1pct=4 scale_refuted=True\n", "producer output")
        need(outputs[1] ==
             b"TPC382_INDEPENDENT_CHECK=PASS cells=12 same_values=72 "
             b"stable_cells=8 signed_over_1pct=4 scale_refuted=True\n",
             "independent output")
        need(outputs[2] == b"TPC382_STRESS=PASS mutations=25\n",
             "stress output")
        print("TPC382_BRIDGE_CHECK=PASS cells=12 same_values=72 "
              "stable_cells=8 signed_over_1pct=4 scale_refuted=True")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC382_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
