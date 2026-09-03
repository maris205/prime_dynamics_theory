#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-372."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-372-full-window-offblock-decomposition"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc372_full_window_offblock_decomposition.md"
PRODUCER = PROJECT / "code/tpc372_full_window_offblock_decomposition.py"
INDEPENDENT = PROJECT / "experiments/tpc372_independent_checker.py"
STRESS = PROJECT / "experiments/tpc372_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc372_certificate.json"
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

# Digests are LF-normalized.  Binary PDFs are normalized by the same historical
# helper used throughout the local bridge chain.
LOCKS = {
    "producer": "deff2866697eb308112fe516fe5313bcac766624d13ffdbb2fad534afbdbf563",
    "independent": "b66ff1a8d38eb1acc2e431f0d5a1f271b02810c4ce4261dc49a610f40e1ef254",
    "stress": "a09496baccbb0f49e9aaa1a343376a9cfe3c5a55cf4564195d4d242c8db0033a",
    "certificate": "ecbaa0f8f1549bcd565135f70f3e36ee0edda36719f69a14d95ca77c1509e257",
    "main_tex": "180a850a6f08a77eeae10d841f8c867af78c9528ee5b61089c7f54199307340d",
    "main_pdf": "a732dd2f1a17045022701e8200f3c2f95c50d9ee1827231f6d83d6a74f6ac8a6",
    "pdf": "a732dd2f1a17045022701e8200f3c2f95c50d9ee1827231f6d83d6a74f6ac8a6",
    "log": "5a7c8f428cbf7e61d527de8f03969a25bc977adc26e043b3cd27e9b7d9d6656e",
    "readme": "7e9793724edc0f6b1478f88422df220d27cdb7ec868a44cf4bdec874805d414b",
    "plan": "8075e516176582f57bc658df2fc90b1a6fa60f343df96b3ea47ff15bf8be2ccf",
    "derivation": "09e0be45207a911ad57b0ae5f8fc26e66736a5f6e8169bc2329631e45275142e",
    "proof": "42410cd7c72e9e098d1fdfc7aeb670e4164c321352bddfb811078e16db3f7d64",
    "claim": "2b47e93ad995ec038c4339532045312a8349ef6baf62f54ad6feaa0f72d850aa",
    "route": "30ba85b415bf32bf2dab7633d18aa3ed6688c1eea2d1acb2e4c9e7cdb0d8476e",
    "protocol": "9916c2d9498b34cc90746739e45f9001ed8b1e05e4711cb13ca10176b2c5bf8e",
    "theorem": "baa26a2c02458ff2dae02b148a2c7a2c2d123a13e54fdb6cd9925a82ad27e782",
    "bridge": "fc1f542843b4cd121e3496b9d3b10de2beba1134221ef13efd98f61c38a51134",
}

STATUS = "NUMERICALLY_CERTIFIED_FINITE_FULL_WINDOW_DECOMPOSITION"
SCHEMA = "TPC372_FULL_WINDOW_OFFBLOCK_DECOMPOSITION_V1"
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
EXPECTED_OFF = [[key[0], key[2]] for key in EXPECTED_FAILURES]


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
    parent = payload.get("parent_lock", {})
    need(parent == {
        "base_code_sha256": "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9",
        "parent_block_phase": True,
        "parent_certificate_sha256": "01ba3b91db1f2a58b70da6b5334127f07350244f07b34772bf83dc4e69ac1ba3",
        "parent_code_sha256": "a2190210a2d43eefb1f37f81f55b2240b6b254fd4f9afa1c26cd5e0c097d8462",
        "parent_schema": "TPC371_COUNT_2048_BLOCK_PHASE_LOCALIZATION_V1",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == ORIGINS and
         protocol.get("window_count") == 2048 and
         protocol.get("block_count") == 256 and
         protocol.get("block_indices") == list(range(8)) and
         protocol.get("partition") == "fixed eight contiguous 256-point blocks" and
         protocol.get("q_anchors") == Q_ANCHORS and
         protocol.get("kernel_exponents") == [1] and
         protocol.get("laws") == ["all_plus"] and
         protocol.get("betas") == BETAS and protocol.get("height") == 66 and
         protocol.get("common_normalization") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False and
         protocol.get("component_selection_used") is False, "protocol")
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
        for component in ("full", "block_diagonal", "off_block"):
            metrics = row.get(component, {})
            need(float(metrics.get("spectral")) > 0 and
                 float(metrics.get("schur")) > 0 and
                 float(metrics.get("frobenius")) > 0 and
                 float(metrics.get("symmetry_error")) <= 1.0e-12,
                 component + " metrics")
        need(float(row.get("decomposition_error")) <= 1.0e-15,
             "decomposition error")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap") == "0.64000000000000001" and
         phase.get("schur_cap") == "0.82999999999999996" and
         phase.get("cap_repair_betas") == [], "phase caps")
    expected_phase = {
        "0": (9, 9, 9, 9, 6),
        "2": (6, 0, 0, 0, 0),
    }
    for beta_text, values in expected_phase.items():
        item = phase.get("by_beta", {}).get(beta_text, {})
        need(item.get("rows") == 9 and
             tuple(item.get(key) for key in (
                 "full_spectral_cap_violations", "full_schur_cap_violations",
                 "block_diagonal_spectral_cap_violations",
                 "block_diagonal_schur_cap_violations",
                 "off_block_spectral_cap_violations")) == values,
             "phase beta " + beta_text)
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("beta2_rows") == 9 and
         audit.get("baseline_beta0_rows") == 9 and
         audit.get("origin_count") == 3 and audit.get("q_count") == 3 and
         audit.get("spectral_rows") == 18 and
         audit.get("beta2_full_spectral_cap_violations") == 6 and
         audit.get("beta2_full_schur_cap_violations") == 0 and
         audit.get("beta2_block_diagonal_spectral_cap_violations") == 0 and
         audit.get("beta2_block_diagonal_schur_cap_violations") == 0 and
         audit.get("beta2_off_block_spectral_cap_violations") == 0 and
         audit.get("baseline_beta0_full_spectral_cap_violations") == 9 and
         audit.get("baseline_beta0_full_schur_cap_violations") == 9 and
         audit.get("full_failure_keys") == EXPECTED_FAILURES and
         audit.get("block_diagonal_beta2_failure_keys") == [] and
         audit.get("required_off_block_keys") == EXPECTED_OFF and
         audit.get("decomposition_max_error") == "0" and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    theorem = payload.get("exact_theorem", {})
    need(theorem.get("anchor_inheritance") == {
        "interval": [1010346, 1010359], "Q": 4, "kernel_exponent": 1,
        "source_project": "TPC-371 block-local phase localization",
    } and theorem.get("common_normalization") ==
         "The full-window square-energy geometry is used for A, D, and R." and
         theorem.get("decomposition") ==
         "The fixed block mask gives the exact finite identity A=D+R." and
         theorem.get("triangle_bound") ==
         "The reverse triangle inequality gives ||R||_2 >= ||A||_2-||D||_2.",
         "exact theorem")
    firewall = payload.get("claim_firewall", {})
    expected_firewall = {
        "TPC372_FULL_WINDOW_PROTOCOL": "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC372_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
        "TPC372_DECOMPOSITION_IDENTITY": "NUMERICALLY_CERTIFIED_FINITE",
        "TPC372_FULL_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
        "TPC372_BETA2_FULL_FAILURE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC372_BLOCK_DIAGONAL_PHASE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC372_OFF_BLOCK_NECESSITY": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC372_CROSS_BLOCK_CAUSALITY": "OPEN",
        "TPC372_ORIGIN_UNIFORMITY": "OPEN",
        "TPC372_WINDOW_UNIFORMITY": "OPEN",
        "TPC372_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC372_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC372_SOURCE_UNIFORM_L2": "OPEN",
        "TPC372_ARITHMETIC_ADVANCE": "NO",
        "TPC372_FIXED_POWER_CREDIT": 0,
        "TPC372_FULL_GATE_B": "OPEN",
        "TPC372_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected_firewall.items():
        need(firewall.get(key) == value, "firewall " + key)
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC372_COMMON_NORMALIZATION = PROVED_EXACT_FINITE",
            "TPC372_OFF_BLOCK_NECESSITY = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC372_ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_EIGENMODE_BLOCK_SEPARATION"):
        need(text.count(marker) == 1, "bridge marker")
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
             b"TPC372_CERTIFICATE=PASS rows=18 beta2_rows=9 "
             b"beta2_violations=6 diagonal_beta2_violations=0\n",
             "producer output")
        need(normal[1] ==
             b"TPC372_INDEPENDENT_CHECK=PASS rows=18 beta2_rows=9 "
             b"beta2_violations=6 diagonal_beta2_violations=0\n",
             "independent output")
        need(normal[2] == b"TPC372_STRESS=PASS exact_baseline=1 mutations=33\n",
             "stress output")
        print("TPC372_BRIDGE_CHECK=PASS rows=18 beta2_rows=9 "
              "beta2_violations=6 diagonal_beta2_violations=0")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC372_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
