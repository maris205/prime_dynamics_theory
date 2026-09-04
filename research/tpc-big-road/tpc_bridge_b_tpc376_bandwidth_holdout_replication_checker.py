#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-376."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-376-bandwidth-holdout-replication"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc376_bandwidth_holdout_replication.md")
PRODUCER = PROJECT / "code/tpc376_bandwidth_holdout_replication.py"
INDEPENDENT = PROJECT / "experiments/tpc376_independent_checker.py"
STRESS = PROJECT / "experiments/tpc376_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc376_certificate.json"
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

# The checker does not lock its own source, avoiding a self-referential hash.
LOCKS = {
    "producer": "7b742612df724689f4d27d17914436b3179c7fe75ea7bdad4decab02fc90ea36",
    "independent": "fec7015705d2017094dbbb1d90404ed6a40a78d79099cc32255685e0ef0e8b12",
    "stress": "79a95145b2830ad79492610e45c0cf2b6378631c7041d9b69c769bfe100075b0",
    "certificate": "4637f2a464f73423cc5e047c559f82a55c0fddaaa900216b3b2f1e6490cc78d2",
    "main_tex": "aab0c41888af0737120aeb5f3c8c79e7e34126e4f206d598544e3b07f63d044e",
    "main_pdf": "cbaf361d02799de7d6e7916b37fc9d7cd02c183b3c58e52869646476bbbd5dc8",
    "pdf": "cbaf361d02799de7d6e7916b37fc9d7cd02c183b3c58e52869646476bbbd5dc8",
    "log": "22196a3978984bd0b2a4b5141cef6932e1c5b5d9c3405262c5a7077a8124f27d",
    "readme": "3662b6836743c12f4e2b8c1e8f7735c5563a41b6b97f0ee2b340e1882b9ab273",
    "plan": "3a299267a9cf5a96b45cae713ad4068cc971881044f91457ea1a04b9e8b04816",
    "derivation": "e4a67f1d81bd5ea0b70c68a257f9dc817459fcdd1dae3491cf9a2eb8830dc7e8",
    "proof": "ed645f4fccce0cfe8f04213009515a7d0f1b8375f795f99895e6b62203e0f01b",
    "claim": "3f8901c685506126065053907240c7a9ee47763bdda46c48dd478a842ac69544",
    "route": "25d147690aba5d4173f304353d1f566e6c3ed4a65ddf5ad9c01280edca4d412b",
    "protocol": "73c0752b92ab4500e30b2e66fe6846d11d0d9908590cc3f7c6e7a85c97d01faf",
    "theorem": "e3ebab674fce56224f3fcd150a4ef3043b6a62c59c4b694d78ee1346552b5109",
    "bridge": "47e025a99bec9bebaae74490c104fa20d0b916869fa86261ac336ad5345ee034",
}

SCHEMA = "TPC376_BANDWIDTH_HOLDOUT_REPLICATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BANDWIDTH_HOLDOUT_REPLICATION"
ORIGINS = [1012006, 1016016, 1022031]
Q_ANCHORS = [512, 2048, 8192]
EXPECTED_FAILURES = [
    [1012006, 2048, 2048, 1, "all_plus"],
    [1012006, 2048, 8192, 1, "all_plus"],
    [1016016, 2048, 2048, 1, "all_plus"],
    [1016016, 2048, 8192, 1, "all_plus"],
    [1022031, 2048, 2048, 1, "all_plus"],
    [1022031, 2048, 8192, 1, "all_plus"],
]
FIREWALL = {
    "TPC376_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC376_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE_INHERITED",
    "TPC376_HOLDOUT_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_9_ROWS",
    "TPC376_C1_FAILURE_PROFILE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC376_PARENT_Q_PROFILE_REPLICATION":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC376_RAYLEIGH_TAIL": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC376_ORIGIN_UNIFORMITY": "OPEN",
    "TPC376_WINDOW_UNIFORMITY": "OPEN",
    "TPC376_C1_SCALE_STABILITY": "OPEN",
    "TPC376_CROSS_BLOCK_CAUSALITY": "OPEN",
    "TPC376_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC376_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC376_SOURCE_UNIFORM_L2": "OPEN",
    "TPC376_ARITHMETIC_ADVANCE": "NO",
    "TPC376_FIXED_POWER_CREDIT": 0,
    "TPC376_FULL_GATE_B": "OPEN",
    "TPC376_TWIN_PRIME_RESULT": "NONE",
}


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def lock(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED" and path.is_file() and
         digest(path.read_bytes()) == expected, label + " provenance")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload", {})
    need(payload.get("schema") == SCHEMA and payload.get("status") == STATUS and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "schema/hash")
    need(payload.get("parent_lock") == {
        "engine_code_sha256":
        "f3fee82fb6306a65a5f83cc8a90b9b04e22e41a6df623784304305c863d12a15",
        "parent_certificate_sha256":
        "3ad30c606b669512cfff63907f3876032efb9b566b03f01ff950e775e1b92e65",
        "parent_schema": "TPC375_BANDWIDTH_STABILITY_MINIMAL_CUTOFF_V1",
        "parent_round2_clue": "TEST_BANDWIDTH_HOLDOUT",
        "parent_failure_profile_by_Q": [0, 3, 3],
    }, "parent lock")
    need(payload.get("selection_protocol") == {
        "grid_start": 1010001, "grid_step": 401, "grid_count": 41,
        "candidate_rule": "a_j=1010001+401j, 0<=j<41",
        "training_indices": [0, 20, 40],
        "training_origins": [1010001, 1018021, 1026041],
        "holdout_indices": [5, 15, 30],
        "holdout_origins": ORIGINS,
        "holdout_rule": "first three predeclared reserved indices (5,15,30)",
        "response_used_for_selection": False,
        "signed_metric_used_for_selection": False,
    }, "selection")
    need(payload.get("protocol") == {
        "origins": ORIGINS, "window_count": 2048, "block_count": 256,
        "block_indices": list(range(8)),
        "partition": "fixed eight contiguous 256-point blocks",
        "band_cutoff": 1,
        "band_definition": "sum of layers with block distance <= 1",
        "q_anchors": Q_ANCHORS, "kernel_exponents": [1],
        "laws": ["all_plus"], "betas": [2], "height": 66,
        "common_normalization": True, "source_response_used": False,
        "origin_selection_used": False, "row_selection_used": False,
        "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
        "panel_complete_before_metric_read": True,
    }, "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 9 and
         {(r.get("origin"), r.get("Q")) for r in rows} ==
         {(o, q) for o in ORIGINS for q in Q_ANCHORS}, "rows")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    for row in rows:
        need(row.get("count") == 2048 and row.get("kernel_exponent") == 1 and
             row.get("beta") == 2 and row.get("law") == "all_plus" and
             row.get("height") == 66 and row.get("band_failure") in
             (True, False), "row header")
        need(row.get("mode", {}).get("mode_rule") ==
             "largest absolute eigenvalue; minimum mode wins ties" and
             float(row["mode"]["eigen_residual_inf"]) <= 1.0e-5 and
             float(row["mode"]["full_mode_norm_error"]) <= 1.0e-8,
             "mode")
    phase = payload.get("phase_summary", {})
    need(phase.get("rows") == 9 and phase.get("band_cutoff") == 1 and
         phase.get("band_definition") == "block distance <= 1" and
         phase.get("spectral_cap_violations") == 6 and
         phase.get("schur_cap_violations") == 0 and
         phase.get("failure_profile_by_Q") == [0, 3, 3] and
         phase.get("failure_keys") == EXPECTED_FAILURES, "phase")
    need(payload.get("finite_audit") == {
        "arithmetic_advance": "NO",
        "failure_keys": EXPECTED_FAILURES,
        "failure_profile_by_Q": [0, 3, 3],
        "fixed_power_credit": 0,
        "origin_count": 3,
        "q_count": 3,
        "rows": 9,
        "schur_cap_violations": 0,
        "spectral_cap_violations": 6,
        "spectral_rows": 9,
    }, "finite audit")
    need(payload.get("exact_theorem", {}).get("grid_index_holdout") ==
         "The holdout indices are distinct from the training indices; the grid-index protocol, not interval disjointness, defines the holdout.",
         "exact theorem")
    need(payload.get("claim_firewall") == FIREWALL, "firewall")
    need(payload.get("round2_clue") == "TEST_C1_WINDOW_SCALE_HOLDOUT",
         "clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC376_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC376_PARENT_Q_PROFILE_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC376_ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_WINDOW_SCALE_HOLDOUT"):
        need(bridge_text.count(marker) == 1, "bridge marker")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error", "Fatal error",
                "Citation", "Empty"):
        need(bad not in log, "LaTeX diagnostic " + bad)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100000,
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
    if "--check" not in sys.argv[1:]:
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
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        jobs = tuple((script, False) for script in scripts) + \
               tuple((script, True) for script in scripts)
        with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
            outputs = tuple(pool.map(lambda job: run(*job), jobs))
        normal, optimized = outputs[:3], outputs[3:]
        need(normal == optimized, "normal/optimized stdout mismatch")
        need(normal[0] ==
             b"TPC376_CERTIFICATE=PASS rows=9 failures=6 profile=0,3,3\n",
             "producer output")
        need(normal[1] ==
             b"TPC376_INDEPENDENT_CHECK=PASS rows=9 failures=6 profile=0,3,3\n",
             "independent output")
        need(normal[2] == b"TPC376_STRESS=PASS mutations=23\n",
             "stress output")
        print("TPC376_BRIDGE_CHECK=PASS rows=9 failures=6 profile=0,3,3")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC376_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
