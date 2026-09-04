#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-377."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-377-c1-window-scale-holdout"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc377_c1_window_scale_holdout.md"
PRODUCER = PROJECT / "code/tpc377_c1_window_scale_holdout.py"
INDEPENDENT = PROJECT / "experiments/tpc377_independent_checker.py"
STRESS = PROJECT / "experiments/tpc377_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc377_certificate.json"
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
    "producer": "5200e29c0c26f61cb190de6dfcc186dd3ea80c9b7ebd0dc76b21f712b93ba966",
    "independent": "08f6ddd875eb9f881acf123de75197eb385f80dac13432e80b9c074bb7efcda9",
    "stress": "07ab93d17f901320f9ab27353b5effbfca1d27cdd4988e59eefdedf1e7998a49",
    "certificate": "2e3061e406a0bb6542b27789411b3518207024f92bcf943ef67afa37b200668c",
    "main_tex": "03db7fc8f3e6255c887e2b58795ce997b214aad7838c07e9cfb8ab0debec9eb9",
    "main_pdf": "3d19c538689394337a6c3d6a04c524881f993fcda0749bf142ef460380feaab5",
    "pdf": "3d19c538689394337a6c3d6a04c524881f993fcda0749bf142ef460380feaab5",
    "log": "90af315961880f7bd2b2a0664b5bf64068925c22a20734bbef343d413bf6c495",
    "readme": "26e67e7ef007059e3955e2aaf49ea643d7d1324ed7c15dd4394742e254f5a7ed",
    "plan": "a1918cf1c5be6af64ede2e72dff952c42432a03135cf54764a74690963cf0d75",
    "derivation": "ee2ac58f636f7a92c8e10e21005ef1e19ed5a1f54b07bd5badfb6e2cf388fa39",
    "proof": "a3fb0e4dece304b632565504c48ceb1a960acb878f54702bedd5afed9822b26a",
    "claim": "3554852cf264f26c4d4e11b077b71695a91672e4139684d5379878cab16dc6a5",
    "route": "dd4ac0ce0eed827745aa74ce489c99ead593382433e556f75f1a49f0460f7b6f",
    "protocol": "281e7cfe2c03e795e5789c1012456807f843638d57c339ba8715eb7e0b30bf9f",
    "theorem": "19176c28455337322a4073ca48b15c18fd8e4ae8f2e7dd0466ba119134629235",
    "bridge": "0e81818b818d6d0d415b0930ebe724b21bd805169a577047496d2155119e56dc",
}

SCHEMA = "TPC377_C1_WINDOW_SCALE_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_WINDOW_SCALE_HOLDOUT"
ORIGINS = [1012006, 1016016, 1022031]
COUNTS = [1024, 1536, 2048]
Q_ANCHORS = [512, 2048, 8192]
EXPECTED_PROFILE = [[0, 3, 3], [0, 3, 3], [0, 3, 3]]
FIREWALL = {
    "TPC377_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC377_NESTED_PREFIX_PROTOCOL": "PROVED_EXACT_FINITE",
    "TPC377_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE_INHERITED",
    "TPC377_SCALE_LADDER_REPLAY":
        "NUMERICALLY_CERTIFIED_FINITE_27_ROWS",
    "TPC377_C1_PROFILE_STABILITY":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC377_PARENT_Q_PROFILE_PERSISTENCE":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC377_RAYLEIGH_TAIL": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC377_ORIGIN_UNIFORMITY": "OPEN",
    "TPC377_WINDOW_SCALE_UNIFORMITY": "OPEN",
    "TPC377_CROSS_BLOCK_CAUSALITY": "OPEN",
    "TPC377_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC377_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC377_SOURCE_UNIFORM_L2": "OPEN",
    "TPC377_ARITHMETIC_ADVANCE": "NO",
    "TPC377_FIXED_POWER_CREDIT": 0,
    "TPC377_FULL_GATE_B": "OPEN",
    "TPC377_TWIN_PRIME_RESULT": "NONE",
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
        "parent_code_sha256":
            "7b742612df724689f4d27d17914436b3179c7fe75ea7bdad4decab02fc90ea36",
        "parent_certificate_sha256":
            "4637f2a464f73423cc5e047c559f82a55c0fddaaa900216b3b2f1e6490cc78d2",
        "parent_schema": "TPC376_BANDWIDTH_HOLDOUT_REPLICATION_V1",
        "parent_round2_clue": "TEST_C1_WINDOW_SCALE_HOLDOUT",
        "parent_failure_profile_by_Q": [0, 3, 3],
    }, "parent lock")
    need(payload.get("selection_protocol") == {
        "origins": ORIGINS,
        "origin_rule":
            "TPC376 response-blind holdout origins, inherited unchanged",
        "counts": COUNTS,
        "count_rule":
            "predeclared nested prefixes of lengths 1024,1536,2048",
        "block_length": 256, "block_counts": [4, 6, 8],
        "q_anchors": Q_ANCHORS,
        "response_used_for_selection": False,
        "signed_metric_used_for_selection": False,
        "panel_complete_before_metric_read": True,
    }, "selection")
    need(payload.get("protocol") == {
        "origins": ORIGINS, "window_counts": COUNTS,
        "block_length": 256, "block_counts": [4, 6, 8],
        "partition": "nested prefixes with contiguous 256-point blocks",
        "band_cutoff": 1,
        "band_definition": "sum of layers with block distance <= 1",
        "q_anchors": Q_ANCHORS, "kernel_exponents": [1],
        "laws": ["all_plus"], "betas": [2], "height": 66,
        "common_normalization": True, "source_response_used": False,
        "origin_selection_used": False, "count_selection_used": False,
        "row_selection_used": False,
        "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
    }, "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 27, "row count")
    need({(r.get("origin"), r.get("count"), r.get("Q")) for r in rows} ==
         {(o, n, q) for o in ORIGINS for n in COUNTS for q in Q_ANCHORS},
         "row keys")
    for row in rows:
        need(row.get("count") in COUNTS and row.get("origin") in ORIGINS and
             row.get("Q") in Q_ANCHORS and row.get("block_length") == 256 and
             row.get("block_count") == row.get("count") // 256 and
             row.get("kernel_exponent") == 1 and row.get("beta") == 2 and
             row.get("law") == "all_plus" and row.get("height") == 66,
             "row header")
        need(row.get("band_failure") in (True, False) and
             row.get("schur_failure") in (True, False), "failure type")
    phase = payload.get("phase_summary", {})
    need(phase.get("rows") == 27 and phase.get("band_cutoff") == 1 and
         phase.get("spectral_cap_violations") == 18 and
         phase.get("schur_cap_violations") == 0 and
         phase.get("failure_profile_by_count_Q") == EXPECTED_PROFILE and
         phase.get("caps") == {
             "spectral": "0.64000000000000001",
             "schur": "0.82999999999999996"}, "phase")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 27 and audit.get("origin_count") == 3 and
         audit.get("count_count") == 3 and audit.get("q_count") == 3 and
         audit.get("spectral_rows") == 27 and
         audit.get("spectral_cap_violations") == 18 and
         audit.get("schur_cap_violations") == 0 and
         audit.get("failure_profile_by_count_Q") == EXPECTED_PROFILE and
         audit.get("scale_profile_invariant") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    need(payload.get("claim_firewall") == FIREWALL, "firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_SCALE_ORIGIN_CROSSHOLDOUT", "clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC377_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC377_C1_PROFILE_STABILITY = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC377_ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_SCALE_ORIGIN_CROSSHOLDOUT"):
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
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        jobs = tuple((script, False) for script in scripts) + \
               tuple((script, True) for script in scripts)
        with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
            outputs = tuple(pool.map(lambda job: run(*job), jobs))
        normal, optimized = outputs[:3], outputs[3:]
        need(normal == optimized, "normal/optimized stdout mismatch")
        need(normal[0] ==
             b"TPC377_CERTIFICATE=PASS rows=27 failures=18 "
             b"profiles=0,3,3;0,3,3;0,3,3\n", "producer output")
        need(normal[1] ==
             b"TPC377_INDEPENDENT_CHECK=PASS rows=27 failures=18 "
             b"profiles=0,3,3;0,3,3;0,3,3\n", "independent output")
        need(normal[2] == b"TPC377_STRESS=PASS mutations=24\n",
             "stress output")
        print("TPC377_BRIDGE_CHECK=PASS rows=27 failures=18 "
              "profiles=0,3,3;0,3,3;0,3,3")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC377_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
