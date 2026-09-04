#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-378."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-378-c1-scale-origin-crossholdout"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc378_c1_scale_origin_crossholdout.md")
PRODUCER = PROJECT / "code/tpc378_c1_scale_origin_crossholdout.py"
INDEPENDENT = PROJECT / "experiments/tpc378_independent_checker.py"
STRESS = PROJECT / "experiments/tpc378_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc378_certificate.json"
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
    "producer": "dd9289a390a1c52b9d22cd19766e4b2c5def87b6fa3c6eda530e4a81081997fa",
    "independent": "40af52314d3c282f7f9602d6237a86e106db0b1ebf15870b240fc0e3aee8b292",
    "stress": "3ab6e6e08956385873e0786725f30be62404c5fb8389d44fc96e49029329899c",
    "certificate": "4846b4cfd0bfb75b9eebb95fcdfb33dc0365c3aba0b7080278be2be96df540d1",
    "main_tex": "60ea54a85c5604c7f58c65c958129b152c0246d2fc6762387c74bc4f0c6cb884",
    "main_pdf": "2419d085b96917d7f119b45709615db02632724de1d20e9a625853ee26d185f6",
    "pdf": "2419d085b96917d7f119b45709615db02632724de1d20e9a625853ee26d185f6",
    "log": "db672ae2b22ab4dada3aa2d842b6e81f8fd7f0ddcfc12bad30d8952d0ec5babd",
    "readme": "a6faf8faf432c149556b119daddb5cdee0b0135b581a51afa8dfce137b098395",
    "plan": "4a5bf2fc548f8a89d314f4ad712c00496777012197fe6b0e330a675ebc3f2fa7",
    "derivation": "f3ff76cd64e1aa90cb9977020dff43a9be40d8342eb47d7a3240c350a5f76acf",
    "proof": "0fcd9461d560a46d8fd5ea5860b343149f48b8dec14ac3690be3ec576ae36bcf",
    "claim": "32599660da5c5ebfe9640b4f1231f0a71fa42a63e6a3025ed1f525bb00253a6b",
    "route": "c93c7c96b469ba2b8d837b1bc22180b8f1a24b53fcfaed85eeae99881b674207",
    "protocol": "ead8c4426c1f275d3cfed1a2aa4ca8d6dd709e7f383957194564ec61bccb28e5",
    "theorem": "0503165e78ac140ba0ff7049173eddbd2b13e39d2814bab3dbb5511e4be430f2",
    "bridge": "5be5643b374215408831245af979ec7805e8e231adfae346788d2cc041037a60",
}

SCHEMA = "TPC378_C1_SCALE_ORIGIN_CROSSHOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_SCALE_ORIGIN_CROSSHOLDOUT"
ORIGINS = [1100001, 1108021, 1116041]
COUNTS = [1024, 2048]
Q_ANCHORS = [512, 2048, 8192]
PROFILE = [[0, 3, 3], [0, 3, 3]]
FIREWALL = {
    "TPC378_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC378_COORDINATE_DISJOINTNESS": "PROVED_EXACT_FINITE",
    "TPC378_COMMON_BAND_RULE": "PROVED_EXACT_FINITE_INHERITED",
    "TPC378_SCALE_ORIGIN_REPLAY":
        "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
    "TPC378_C1_PROFILE_TRANSFER":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC378_PARENT_PROFILE_REPLICATION":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC378_RAYLEIGH_TAIL": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC378_ORIGIN_UNIFORMITY": "OPEN",
    "TPC378_WINDOW_SCALE_UNIFORMITY": "OPEN",
    "TPC378_SPECTRAL_MAGNITUDE_UNIFORMITY": "OPEN",
    "TPC378_CROSS_BLOCK_CAUSALITY": "OPEN",
    "TPC378_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC378_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC378_SOURCE_UNIFORM_L2": "OPEN",
    "TPC378_ARITHMETIC_ADVANCE": "NO",
    "TPC378_FIXED_POWER_CREDIT": 0,
    "TPC378_FULL_GATE_B": "OPEN",
    "TPC378_TWIN_PRIME_RESULT": "NONE",
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
    need(payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "schema/hash")
    need(payload.get("parent_lock") == {
        "parent_code_sha256":
            "5200e29c0c26f61cb190de6dfcc186dd3ea80c9b7ebd0dc76b21f712b93ba966",
        "parent_certificate_sha256":
            "2e3061e406a0bb6542b27789411b3518207024f92bcf943ef67afa37b200668c",
        "parent_schema": "TPC377_C1_WINDOW_SCALE_HOLDOUT_V1",
        "parent_round2_clue": "TEST_C1_SCALE_ORIGIN_CROSSHOLDOUT",
        "parent_failure_profile_by_count_Q": [
            [0, 3, 3], [0, 3, 3], [0, 3, 3]],
    }, "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("grid_start") == 1100001 and
         selection.get("grid_step") == 401 and
         selection.get("grid_count") == 41 and
         selection.get("candidate_origins") ==
         [1100001 + 401 * i for i in range(41)] and
         selection.get("origin_indices") == [0, 20, 40] and
         selection.get("origins") == ORIGINS and
         selection.get("counts") == COUNTS and
         selection.get("block_length") == 256 and
         selection.get("block_counts") == [4, 8] and
         selection.get("q_anchors") == Q_ANCHORS and
         selection.get("response_used_for_selection") is False and
         selection.get("signed_metric_used_for_selection") is False and
         selection.get("panel_complete_before_metric_read") is True,
         "selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == ORIGINS and
         protocol.get("window_counts") == COUNTS and
         protocol.get("block_length") == 256 and
         protocol.get("block_counts") == [4, 8] and
         protocol.get("band_cutoff") == 1 and
         protocol.get("q_anchors") == Q_ANCHORS and
         protocol.get("kernel_exponents") == [1] and
         protocol.get("laws") == ["all_plus"] and
         protocol.get("betas") == [2] and protocol.get("height") == 66 and
         protocol.get("common_normalization") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False and
         protocol.get("count_selection_used") is False and
         protocol.get("row_selection_used") is False,
         "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 18, "rows")
    need({(row.get("origin"), row.get("count"), row.get("Q"))
          for row in rows} ==
         {(origin, count, q) for origin in ORIGINS for count in COUNTS
          for q in Q_ANCHORS}, "row keys")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    for row in rows:
        need(row.get("block_length") == 256 and
             row.get("block_count") == row.get("count") // 256 and
             row.get("kernel_exponent") == 1 and row.get("beta") == 2 and
             row.get("law") == "all_plus" and row.get("height") == 66 and
             row.get("band_failure") in (True, False) and
             row.get("schur_failure") in (True, False), "row header")
    phase = payload.get("phase_summary", {})
    need(phase.get("rows") == 18 and phase.get("band_cutoff") == 1 and
         phase.get("spectral_cap_violations") == 12 and
         phase.get("schur_cap_violations") == 0 and
         phase.get("failure_profile_by_count_Q") == PROFILE and
         phase.get("caps") == {
             "spectral": "0.64000000000000001",
             "schur": "0.82999999999999996"}, "phase")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("origin_count") == 3 and
         audit.get("count_count") == 2 and audit.get("q_count") == 3 and
         audit.get("spectral_rows") == 18 and
         audit.get("spectral_cap_violations") == 12 and
         audit.get("schur_cap_violations") == 0 and
         audit.get("failure_profile_by_count_Q") == PROFILE and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("profile_transfer") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    need(payload.get("claim_firewall") == FIREWALL, "firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_CROSSHOLDOUT_LAW_CONTROL", "clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC378_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC378_C1_PROFILE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC378_ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_CROSSHOLDOUT_LAW_CONTROL"):
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
             b"TPC378_CERTIFICATE=PASS rows=18 failures=12 "
             b"profiles=0,3,3;0,3,3\n", "producer output")
        need(normal[1] ==
             b"TPC378_INDEPENDENT_CHECK=PASS rows=18 failures=12 "
             b"profiles=0,3,3;0,3,3\n", "independent output")
        need(normal[2] == b"TPC378_STRESS=PASS mutations=24\n",
             "stress output")
        print("TPC378_BRIDGE_CHECK=PASS rows=18 failures=12 "
              "profiles=0,3,3;0,3,3")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC378_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
