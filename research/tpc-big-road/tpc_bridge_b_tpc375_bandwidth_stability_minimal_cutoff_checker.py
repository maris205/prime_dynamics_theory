#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-375."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-375-bandwidth-stability-minimal-cutoff"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc375_bandwidth_stability_minimal_cutoff.md")
PRODUCER = PROJECT / "code/tpc375_bandwidth_stability_minimal_cutoff.py"
INDEPENDENT = PROJECT / "experiments/tpc375_independent_checker.py"
STRESS = PROJECT / "experiments/tpc375_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc375_certificate.json"
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

# Filled after the package is final.  The bridge lock below refers to the
# markdown bridge, not this checker, avoiding a self-referential digest.
LOCKS = {
    "producer": "f3fee82fb6306a65a5f83cc8a90b9b04e22e41a6df623784304305c863d12a15",
    "independent": "7d8eb601f6ff95435456b90eebadec2aede838e03aa40a443e8bb55c8048ad3a",
    "stress": "057180652f421d2f287667b2da179ec10eef8b1cf52374f400cc2aeb3b5e5f66",
    "certificate": "3ad30c606b669512cfff63907f3876032efb9b566b03f01ff950e775e1b92e65",
    "main_tex": "9f3caca4ec9c543277af86d2ec8c74931a166602acbd81b67a6cac500bec726a",
    "main_pdf": "c315fcc110314d7997c7898b299c7dbbaa5e94024ca997aa99f1a8701a6a9de4",
    "pdf": "c315fcc110314d7997c7898b299c7dbbaa5e94024ca997aa99f1a8701a6a9de4",
    "log": "dcc4b63c236701e3b9c867d70b292c0fc2370039149e7605a08f025cc1c1f062",
    "readme": "67cc056b26d3792d5487d6c8a1d2b20df3b08ee31483293c4043c9dbc9c38aac",
    "plan": "3f4a9abd83dc6e92759ef305573beb9fded4b532ed666d90a155acb2c8a24d6a",
    "derivation": "08c975c7fd79a3e4d8b2cab4fbc6632a4dc064ffab0e865c9ac6e3e574ce801d",
    "proof": "1ccaf53c6ce63039682406fd3e0262b3287ab2f7bc5f0270e91dca3af3646759",
    "claim": "718b1f9861c0a2d986e4426181bd35d69b6fa7993bef28aa481c554549ebf0b3",
    "route": "a03263f980ec0c9857540d5ea1e867831eef30cdb94cffa2b1778a305bcf69ae",
    "protocol": "ca5a9000179ef2a7b6d7cb3f9d0df4fe1cb8e65e29a7541642db7c2cb3de002c",
    "theorem": "0c8b6e47f5a18248dd3055ddb260f77de2ec0d48930213e1fe93efc94c0d1283",
    "bridge": "8e56505d7faab0a189ef220747f636bb2de23fb7ed8df75cfa5ec1e42d18e036",
}

STATUS = "NUMERICALLY_CERTIFIED_FINITE_BANDWIDTH_STABILITY"
SCHEMA = "TPC375_BANDWIDTH_STABILITY_MINIMAL_CUTOFF_V1"
ORIGINS = [1010001, 1018021, 1026041]
Q_ANCHORS = [512, 2048, 8192]
BAND_CUTOFFS = [0, 1, 2, 3]
PARENT_FAILURES = [
    [1010001, 2048, 2048, 1, "all_plus"],
    [1010001, 2048, 8192, 1, "all_plus"],
    [1018021, 2048, 2048, 1, "all_plus"],
    [1018021, 2048, 8192, 1, "all_plus"],
    [1026041, 2048, 2048, 1, "all_plus"],
    [1026041, 2048, 8192, 1, "all_plus"],
]


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
        "base_code_sha256":
        "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9",
        "parent_code_sha256":
        "09851134f9c2d2444c42702b1649e49d259cb9316291ee5b7c275a92b96a9cd0",
        "parent_certificate_sha256":
        "c49310bd080f609f90ee03a74beeda7fbd7ebae0b5f25012a06235f42a047c40",
        "parent_schema": "TPC374_NEAR_BLOCK_BAND_TRUNCATION_V1",
        "parent_round2_clue": "TEST_BANDWIDTH_STABILITY",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol == {
        "origins": ORIGINS, "window_count": 2048, "block_count": 256,
        "block_indices": list(range(8)),
        "partition": "fixed eight contiguous 256-point blocks",
        "band_cutoffs": BAND_CUTOFFS,
        "band_definition": "sum of layers with block distance <= cutoff",
        "q_anchors": Q_ANCHORS, "kernel_exponents": [1],
        "laws": ["all_plus"], "betas": [2], "height": 66,
        "common_normalization": True, "source_response_used": False,
        "origin_selection_used": False, "row_selection_used": False,
        "component_selection_used": False,
        "panel_complete_before_cutoff_read": True,
        "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
    }, "protocol")
    rows = payload.get("rows")
    expected = {(o, q, 1, 2, "all_plus")
                for o in ORIGINS for q in Q_ANCHORS}
    need(isinstance(rows, list) and len(rows) == 9 and
         {(r.get("origin"), r.get("Q"), r.get("kernel_exponent"),
           r.get("beta"), r.get("law")) for r in rows} == expected,
         "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    for row in rows:
        need(row.get("count") == 2048 and row.get("height") == 66 and
             row.get("shell_cardinality", 0) > 0 and
             set(row.get("bands", {})) == {str(c) for c in BAND_CUTOFFS},
             "row header")
        need(set(row.get("mode", {}).get("by_cutoff", {})) ==
             {str(c) for c in BAND_CUTOFFS}, "mode cutoff census")
        need(row.get("mode", {}).get("mode_rule") ==
             "largest absolute eigenvalue; minimum mode wins ties" and
             float(row["mode"]["eigen_residual_inf"]) <= 1.0e-5 and
             float(row["mode"]["full_mode_norm_error"]) <= 1.0e-8,
             "mode")
    phase = payload.get("phase_summary", {})
    need(phase.get("cutoffs") == BAND_CUTOFFS and
         phase.get("band_definition") == "block distance <= cutoff" and
         phase.get("caps") == {"spectral": "0.64000000000000001",
                                "schur": "0.82999999999999996"},
         "phase header")
    expected_counts = {"0": (0, 0), "1": (6, 0),
                       "2": (6, 0), "3": (6, 0)}
    for key, (spectral, schur) in expected_counts.items():
        item = phase.get("by_cutoff", {}).get(key, {})
        need(item.get("rows") == 9 and
             item.get("spectral_cap_violations") == spectral and
             item.get("schur_cap_violations") == schur, "phase counts")
        actual = [[r["origin"], r["count"], r["Q"],
                   r["kernel_exponent"], r["law"]]
                  for r in rows if r["band_failure_flags"][key]]
        need(item.get("failure_keys") == actual, "phase support")
    need(phase.get("minimal_failure_cutoff_census") ==
         {"0": 0, "1": 6, "2": 0, "3": 0} and
         phase.get("never_failure_rows") == 3, "minimal census")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 9 and audit.get("origin_count") == 3 and
         audit.get("q_count") == 3 and audit.get("cutoff_count") == 4 and
         audit.get("spectral_rows") == 9 and
         audit.get("spectral_cap_violations_by_cutoff") ==
         {k: v[0] for k, v in expected_counts.items()} and
         audit.get("schur_cap_violations_by_cutoff") ==
         {k: v[1] for k, v in expected_counts.items()} and
         audit.get("failure_keys_by_cutoff") ==
         {k: phase["by_cutoff"][k]["failure_keys"]
          for k in expected_counts} and
         audit.get("parent_failure_keys") == PARENT_FAILURES and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    need(payload.get("exact_theorem", {}).get("anchor_inheritance") == {
        "interval": [1010346, 1010359], "Q": 4, "kernel_exponent": 1,
        "source_project": "TPC-374 near-block band truncation",
    }, "anchor")
    need(payload.get("claim_firewall") == {
        "TPC375_FULL_WINDOW_PROTOCOL":
            "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC375_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
        "TPC375_NESTED_BAND_MASKS": "PROVED_EXACT_FINITE_PREDECLARED",
        "TPC375_BANDWIDTH_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_9_ROWS",
        "TPC375_FAILURE_CUTOFF_CENSUS": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC375_PARENT_SUPPORT_REPRODUCTION":
            "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC375_RAYLEIGH_RETENTION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC375_MINIMAL_CUTOFF": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC375_BANDWIDTH_UNIFORMITY": "OPEN",
        "TPC375_CROSS_BLOCK_CAUSALITY": "OPEN",
        "TPC375_ORIGIN_UNIFORMITY": "OPEN",
        "TPC375_WINDOW_UNIFORMITY": "OPEN",
        "TPC375_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC375_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC375_SOURCE_UNIFORM_L2": "OPEN",
        "TPC375_ARITHMETIC_ADVANCE": "NO",
        "TPC375_FIXED_POWER_CREDIT": 0,
        "TPC375_FULL_GATE_B": "OPEN",
        "TPC375_TWIN_PRIME_RESULT": "NONE",
    }, "firewall")
    need(payload.get("round2_clue") == "TEST_BANDWIDTH_HOLDOUT", "clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC375_FAILURE_CUTOFF_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC375_MINIMAL_CUTOFF = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC375_ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_BANDWIDTH_HOLDOUT"):
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
             b"TPC375_CERTIFICATE=PASS rows=9 failures=0,6,6,6 "
             b"b3_parent_match=1\n", "producer output")
        need(normal[1] ==
             b"TPC375_INDEPENDENT_CHECK=PASS rows=9 failures=0,6,6,6 "
             b"b3_parent_match=1\n", "independent output")
        need(normal[2] == b"TPC375_STRESS=PASS exact_baseline=1 mutations=24\n",
             "stress output")
        print("TPC375_BRIDGE_CHECK=PASS rows=9 failures=0,6,6,6 "
              "minimal_cutoff=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC375_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
