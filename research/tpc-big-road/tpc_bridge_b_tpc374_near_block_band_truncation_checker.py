#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-374."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-374-near-block-band-truncation"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc374_near_block_band_truncation.md")
PRODUCER = PROJECT / "code/tpc374_near_block_band_truncation.py"
INDEPENDENT = PROJECT / "experiments/tpc374_independent_checker.py"
STRESS = PROJECT / "experiments/tpc374_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc374_certificate.json"
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

# Filled after the package is final.  Digests are LF-normalized.
LOCKS = {
    "producer": "09851134f9c2d2444c42702b1649e49d259cb9316291ee5b7c275a92b96a9cd0",
    "independent": "1c929915cc5924323538186409e420cb9280bcc0c701ea218067dd9396f3d7d9",
    "stress": "0ec221d7097823758ae620865bf3433118ceb974978be9d9b02ab80fe1659647",
    "certificate": "c49310bd080f609f90ee03a74beeda7fbd7ebae0b5f25012a06235f42a047c40",
    "main_tex": "88884da96fa89613f1d95d36589334ae4078dfac3453d2706e6d8f4e04e8656d",
    "main_pdf": "f66b845d46c5c57b8c64d132a33bcebff102c47fad3a8fd693fbd4ac108d11d0",
    "pdf": "f66b845d46c5c57b8c64d132a33bcebff102c47fad3a8fd693fbd4ac108d11d0",
    "log": "9d65211110fb8ad351aaaffe72ba6e38c484d7315196f6ab9137bc5dddb7bb25",
    "readme": "3a9c64a3c18f7bd4102fa91a28d4be8fa0199c9d46a7cf8355b5b8b2d026798e",
    "plan": "504e8696084f982ac1210bffc8591f55dc414cb9c1c521efae5b304ebb08bdf5",
    "derivation": "eb2ae431bc2136972474594c3c4d4c958362e0ebc5aee282301ac6a98a1fd206",
    "proof": "1f9911199096ec23353fbd4b8998915c398f94b532e1783690c69314c1964125",
    "claim": "5865e1eddce86c034a8243c02fa9f7b59a51f4219d9e70207d4a7268610e3df0",
    "route": "fd194fd739e784dd009863242f52f79d1d93c3691ad3535443306edd14558add",
    "protocol": "deee6b44536962186d0027acc4f887cefe7a57fa46f4db628bca7f1b0e546da2",
    "theorem": "de8e3ecba4f5d5537e885baf9752fb97437f890354d8e4b4045af1956b22b4cd",
    "bridge": "ec82d4499bf2dfe2a2da9e58ac158376f8ced21717516e38177c4b4635f36993",
}

STATUS = "NUMERICALLY_CERTIFIED_FINITE_NEAR_BLOCK_BAND_TRUNCATION"
SCHEMA = "TPC374_NEAR_BLOCK_BAND_TRUNCATION_V1"
ORIGINS = [1010001, 1018021, 1026041]
Q_ANCHORS = [512, 2048, 8192]
BETAS = [0, 2]
EXPECTED_FAILURES = [
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
        "770877d4375f65b5eae61101e3bc8c8340737a19e3e2f22defc4f75c1640df49",
        "parent_certificate_sha256":
        "7f54603589c49085ec6f35bf7752a505e85f2f2e9f979d448f42a8e7776a80e5",
        "parent_schema": "TPC373_EIGENMODE_BLOCK_SEPARATION_V1",
        "parent_round2_clue": "TEST_LAYERWISE_CROSS_BLOCK_DECAY",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol == {
        "origins": ORIGINS, "window_count": 2048, "block_count": 256,
        "block_indices": list(range(8)),
        "partition": "fixed eight contiguous 256-point blocks",
        "band_cutoff": 3,
        "band_definition": "sum of layers with block distance <= 3",
        "q_anchors": Q_ANCHORS, "kernel_exponents": [1],
        "laws": ["all_plus"], "betas": BETAS, "height": 66,
        "common_normalization": True, "source_response_used": False,
        "origin_selection_used": False, "row_selection_used": False,
        "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
        "component_selection_used": False,
        "panel_complete_before_mode_read": True,
    }, "protocol")
    rows = payload.get("rows")
    expected = {(o, q, 1, beta, "all_plus")
                for beta in BETAS for o in ORIGINS for q in Q_ANCHORS}
    need(isinstance(rows, list) and len(rows) == 18 and
         {(r.get("origin"), r.get("Q"), r.get("kernel_exponent"),
           r.get("beta"), r.get("law")) for r in rows} == expected,
         "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    for row in rows:
        need(row.get("count") == 2048 and row.get("height") == 66 and
             row.get("shell_cardinality", 0) > 0 and
             row.get("parent_failure") in (True, False), "row header")
        for component in ("full", "band"):
            metrics = row.get(component, {})
            for key in ("spectral", "schur", "frobenius",
                        "minimum_eigenvalue", "maximum_eigenvalue"):
                need(key in metrics and float(metrics[key]) ==
                     float(metrics[key]), component + " metric")
        tail = row.get("tail", {})
        need(all(key in tail for key in ("schur", "frobenius",
                                         "symmetry_error")), "tail")
        mode = row.get("mode", {})
        need(mode.get("mode_rule") ==
             "largest absolute eigenvalue; minimum mode wins ties" and
             mode.get("selected_mode") == "minimum_eigenvalue" and
             float(mode.get("eigen_residual_inf")) <= 1.0e-5 and
             float(mode.get("full_mode_norm_error")) <= 1.0e-8 and
             float(mode.get("rayleigh_sum_error")) <= 1.0e-8, "mode")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap") == "0.64000000000000001" and
         phase.get("schur_cap") == "0.82999999999999996" and
         phase.get("band_cutoff") == 3 and
         phase.get("band_definition") ==
         "sum of layers with block distance <= 3" and
         phase.get("cap_repair_betas") == [], "phase header")
    expected_phase = {"0": (9, 9, 9, 9, 9), "2": (9, 6, 0, 6, 0)}
    for beta_text, values in expected_phase.items():
        item = phase.get("by_beta", {}).get(beta_text, {})
        need((item.get("rows"), item.get("full_spectral_cap_violations"),
              item.get("full_schur_cap_violations"),
              item.get("band_spectral_cap_violations"),
              item.get("band_schur_cap_violations")) == values and
             item.get("minimum_mode_rows") == 9, "phase beta")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("beta2_rows") == 9 and
         audit.get("baseline_beta0_rows") == 9 and
         audit.get("origin_count") == 3 and audit.get("q_count") == 3 and
         audit.get("spectral_rows") == 18 and
         audit.get("beta2_full_spectral_cap_violations") == 6 and
         audit.get("beta2_full_schur_cap_violations") == 0 and
         audit.get("beta2_band_spectral_cap_violations") == 6 and
         audit.get("beta2_band_schur_cap_violations") == 0 and
         audit.get("baseline_beta0_full_spectral_cap_violations") == 9 and
         audit.get("baseline_beta0_full_schur_cap_violations") == 9 and
         audit.get("full_failure_keys") == EXPECTED_FAILURES and
         audit.get("band_failure_keys") == EXPECTED_FAILURES and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    need(payload.get("exact_theorem", {}).get("anchor_inheritance") == {
        "interval": [1010346, 1010359], "Q": 4, "kernel_exponent": 1,
        "source_project": "TPC-373 eigenmode block separation",
    }, "anchor")
    need(payload.get("claim_firewall") == {
        "TPC374_FULL_WINDOW_PROTOCOL":
            "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC374_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
        "TPC374_NEAR_BLOCK_BAND": "PROVED_EXACT_FINITE_PREDECLARED",
        "TPC374_BAND_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
        "TPC374_BAND_FAILURE_CENSUS": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC374_PARENT_FAILURE_REPRODUCTION":
            "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC374_RAYLEIGH_RETENTION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC374_TAIL_PROFILE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC374_BAND_OPERATOR_UNIFORMITY": "OPEN",
        "TPC374_CROSS_BLOCK_CAUSALITY": "OPEN",
        "TPC374_ORIGIN_UNIFORMITY": "OPEN",
        "TPC374_WINDOW_UNIFORMITY": "OPEN",
        "TPC374_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC374_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC374_SOURCE_UNIFORM_L2": "OPEN",
        "TPC374_ARITHMETIC_ADVANCE": "NO",
        "TPC374_FIXED_POWER_CREDIT": 0,
        "TPC374_FULL_GATE_B": "OPEN",
        "TPC374_TWIN_PRIME_RESULT": "NONE",
    }, "firewall")
    need(payload.get("round2_clue") == "TEST_BANDWIDTH_STABILITY", "clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC374_BAND_REPLAY = NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
            "TPC374_BAND_FAILURE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC374_ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_BANDWIDTH_STABILITY"):
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
             b"TPC374_CERTIFICATE=PASS rows=18 beta2_rows=9 "
             b"beta2_violations=6 band_beta2_violations=6\n",
             "producer output")
        need(normal[1] ==
             b"TPC374_INDEPENDENT_CHECK=PASS rows=18 beta2_rows=9 "
             b"beta2_violations=6 band_beta2_violations=6\n",
             "independent output")
        need(normal[2] == b"TPC374_STRESS=PASS exact_baseline=1 mutations=29\n",
             "stress output")
        print("TPC374_BRIDGE_CHECK=PASS rows=18 beta2_rows=9 "
              "beta2_violations=6 band_beta2_violations=6")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC374_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
