#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-373."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-373-eigenmode-block-separation"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc373_eigenmode_block_separation.md")
PRODUCER = PROJECT / "code/tpc373_eigenmode_block_separation.py"
INDEPENDENT = PROJECT / "experiments/tpc373_independent_checker.py"
STRESS = PROJECT / "experiments/tpc373_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc373_certificate.json"
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

# Digests are LF-normalized, matching the repository bridge convention.
LOCKS = {
    "producer": "770877d4375f65b5eae61101e3bc8c8340737a19e3e2f22defc4f75c1640df49",
    "independent": "a40139e971e0413a2d3e8ac1492149b0ad0b46f8ebc95d4c26b30079b60391b9",
    "stress": "6ff2dba986dd6dc306e537b40fcc1eb59c5ac0cc49feed0355bda049a4aa82de",
    "certificate": "7f54603589c49085ec6f35bf7752a505e85f2f2e9f979d448f42a8e7776a80e5",
    "main_tex": "ba3c27dccae5233debb11d84634d5b3b2f91a41e6df71dd1abeb4c74ee4ce5e4",
    "main_pdf": "b11ed13c04afbd0008333c3a4f80fb89afe7bbfb7b8eb439aca89af88fdf09c8",
    "pdf": "b11ed13c04afbd0008333c3a4f80fb89afe7bbfb7b8eb439aca89af88fdf09c8",
    "log": "8918d1e25015c1f794a989f3f37fefe6f5471352e26969424be8a7ddc92cf510",
    "readme": "489d707100bf5e1b3075df03f36623d6adcc82f78c4bde609594054a16224991",
    "plan": "9d1e388c4a73bbb71514af7a761cf4d1f6bbbca712d4aa3d1317bce03494a381",
    "derivation": "2d3959ba7f3422d68fe3a91cf4daac63e99cc531bc92580ccbd378a37abba709",
    "proof": "aa6d2d283cfd969c7b2e82cb3f362148874c91d5807e51b10f5a26841bc363fa",
    "claim": "f95812b55b1474b6d76496743c04a6f5297c5eb9469bf3f64fad94a8edd9deca",
    "route": "9fcddbb1d6cae5b4037909582f70c152f69f6faa721965018cf9ac0683f2cdb3",
    "protocol": "e55676a14b844115c8a5ce7fecf611401712ea51fb0ca99a1f7481c435982285",
    "theorem": "cb4b40aa75088c2cd62a8bb8316737c62c2687d98f48ec30a028f7309bceed2d",
    "bridge": "e59cdc929d1fa65368bb3916e34c4bad2ea3001e9295dbd09cd25cdd42dbf689",
}

STATUS = "NUMERICALLY_CERTIFIED_FINITE_EIGENMODE_BLOCK_SEPARATION"
SCHEMA = "TPC373_EIGENMODE_BLOCK_SEPARATION_V1"
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
    parent = payload.get("parent_lock")
    need(parent == {
        "base_code_sha256":
        "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9",
        "parent_code_sha256":
        "deff2866697eb308112fe516fe5313bcac766624d13ffdbb2fad534afbdbf563",
        "parent_certificate_sha256":
        "ecbaa0f8f1549bcd565135f70f3e36ee0edda36719f69a14d95ca77c1509e257",
        "parent_schema": "TPC372_FULL_WINDOW_OFFBLOCK_DECOMPOSITION_V1",
        "parent_round2_clue": "TEST_EIGENMODE_BLOCK_SEPARATION",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == ORIGINS and
         protocol.get("window_count") == 2048 and
         protocol.get("block_count") == 256 and
         protocol.get("block_indices") == list(range(8)) and
         protocol.get("partition") ==
         "fixed eight contiguous 256-point blocks" and
         protocol.get("layer_definition") ==
         "absolute block-index distance 0..7" and
         protocol.get("q_anchors") == Q_ANCHORS and
         protocol.get("kernel_exponents") == [1] and
         protocol.get("laws") == ["all_plus"] and
         protocol.get("betas") == BETAS and protocol.get("height") == 66 and
         protocol.get("common_normalization") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False and
         protocol.get("row_selection_used") is False and
         protocol.get("component_selection_used") is False and
         protocol.get("panel_complete_before_mode_read") is True and
         protocol.get("mode_rule") ==
         "largest absolute eigenvalue; minimum mode wins ties", "protocol")
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
        metrics = row.get("full", {})
        need(row.get("count") == 2048 and row.get("height") == 66 and
             row.get("shell_cardinality", 0) > 0 and
             row.get("parent_failure") in (True, False), "row header")
        for key in ("spectral", "schur", "frobenius", "minimum_eigenvalue",
                    "maximum_eigenvalue"):
            need(key in metrics, "metric " + key)
            need(float(metrics[key]) == float(metrics[key]),
                 "finite metric " + key)
        mode = row.get("eigenmode", {})
        need(mode.get("mode_rule") ==
             "largest absolute eigenvalue; minimum mode wins ties" and
             mode.get("layer_count") == 8 and
             mode.get("selected_mode") in
             ("minimum_eigenvalue", "maximum_eigenvalue") and
             len(mode.get("layers", [])) == 8 and
             [layer.get("block_distance") for layer in mode["layers"]] ==
             list(range(8)), "mode record")
        need(float(mode.get("layer_reconstruction_error")) <= 1.0e-12 and
             float(mode.get("rayleigh_sum_error")) <= 1.0e-8 and
             float(mode.get("eigen_residual_inf")) <= 1.0e-5,
             "mode errors")
    beta2 = [r for r in rows if r["beta"] == 2]
    beta0 = [r for r in rows if r["beta"] == 0]
    actual_failures = [[r["origin"], r["count"], r["Q"],
                        r["kernel_exponent"], r["law"]]
                       for r in beta2 if float(r["full"]["spectral"]) > .64]
    need(actual_failures == EXPECTED_FAILURES, "failure census")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap") == "0.64000000000000001" and
         phase.get("schur_cap") == "0.82999999999999996" and
         phase.get("mode_selection") ==
         "largest absolute eigenvalue; min wins ties" and
         phase.get("layer_partition") ==
         "absolute block-index distance 0..7" and
         phase.get("cap_repair_betas") == [], "phase header")
    expected_phase = {"0": (9, 9, 9), "2": (9, 6, 0)}
    for beta_text, values in expected_phase.items():
        item = phase.get("by_beta", {}).get(beta_text, {})
        need(item.get("rows") == values[0] and
             item.get("full_spectral_cap_violations") == values[1] and
             item.get("full_schur_cap_violations") == values[2] and
             item.get("minimum_mode_rows") == 9 and
             item.get("maximum_mode_rows") == 0 and
             item.get("dominant_distance_histogram", {}).get("0") == 9 and
             sum(item.get("dominant_distance_histogram", {}).values()) == 9,
             "phase beta " + beta_text)
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("beta2_rows") == 9 and
         audit.get("baseline_beta0_rows") == 9 and
         audit.get("origin_count") == 3 and audit.get("q_count") == 3 and
         audit.get("spectral_rows") == 18 and
         audit.get("beta2_full_spectral_cap_violations") == 6 and
         audit.get("beta2_full_schur_cap_violations") == 0 and
         audit.get("baseline_beta0_full_spectral_cap_violations") == 9 and
         audit.get("baseline_beta0_full_schur_cap_violations") == 9 and
         audit.get("full_failure_keys") == EXPECTED_FAILURES and
         audit.get("layer_reconstruction_max_error") == "0" and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    failure_rows = [r for r in beta2 if r["parent_failure"]]
    need(len(failure_rows) == 6 and all(
         float(layer["rayleigh"]) < 0.0
         for row in failure_rows for layer in row["eigenmode"]["layers"]),
         "failure-mode sign coherence")
    need(max(float(row["eigenmode"]["far_block_abs_fraction"])
             for row in failure_rows) <= 0.008428824 and
         min(sum(float(layer["abs_fraction"])
                 for layer in row["eigenmode"]["layers"][:4])
             for row in failure_rows) >= 0.991571176,
         "near-block mass profile")
    need(payload.get("exact_theorem", {}).get("anchor_inheritance") == {
        "interval": [1010346, 1010359], "Q": 4, "kernel_exponent": 1,
        "source_project": "TPC-372 full-window off-block decomposition",
    }, "anchor")
    firewall = payload.get("claim_firewall", {})
    expected_firewall = {
        "TPC373_FULL_WINDOW_PROTOCOL":
            "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC373_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
        "TPC373_BLOCK_DISTANCE_PARTITION":
            "PROVED_EXACT_FINITE_PREDECLARED",
        "TPC373_EIGENMODE_SELECTION_RULE":
            "PROVED_EXACT_FINITE_DETERMINISTIC",
        "TPC373_EIGENMODE_REPLAY":
            "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
        "TPC373_LAYER_RECONSTRUCTION": "NUMERICALLY_CERTIFIED_FINITE",
        "TPC373_RAYLEIGH_PROFILE":
            "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC373_CROSS_BLOCK_DECAY": "OPEN",
        "TPC373_CROSS_BLOCK_CAUSALITY": "OPEN",
        "TPC373_ORIGIN_UNIFORMITY": "OPEN",
        "TPC373_WINDOW_UNIFORMITY": "OPEN",
        "TPC373_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC373_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC373_SOURCE_UNIFORM_L2": "OPEN",
        "TPC373_ARITHMETIC_ADVANCE": "NO",
        "TPC373_FIXED_POWER_CREDIT": 0,
        "TPC373_FULL_GATE_B": "OPEN",
        "TPC373_TWIN_PRIME_RESULT": "NONE",
    }
    need(firewall == expected_firewall, "firewall")
    need(payload.get("round2_clue") == "TEST_LAYERWISE_CROSS_BLOCK_DECAY",
         "clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC373_RAYLEIGH_PROFILE = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC373_CROSS_BLOCK_DECAY = OPEN",
            "TPC373_ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_LAYERWISE_CROSS_BLOCK_DECAY"):
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
             b"TPC373_CERTIFICATE=PASS rows=18 beta2_rows=9 "
             b"beta2_violations=6 max_cross_abs=0.34415392242278348\n",
             "producer output")
        need(normal[1] ==
             b"TPC373_INDEPENDENT_CHECK=PASS rows=18 beta2_rows=9 "
             b"beta2_violations=6 max_cross_abs=0.34415392242278348\n",
             "independent output")
        need(normal[2] == b"TPC373_STRESS=PASS exact_baseline=1 mutations=39\n",
             "stress output")
        print("TPC373_BRIDGE_CHECK=PASS rows=18 beta2_rows=9 "
              "beta2_violations=6 min_mode_rows=18 dominant_distance_zero=18")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC373_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
