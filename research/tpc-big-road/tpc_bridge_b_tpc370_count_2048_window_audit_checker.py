#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-370."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-370-count-2048-window-audit"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc370_count_2048_window_audit.md"
PRODUCER = PROJECT / "code/tpc370_count_2048_window_audit.py"
INDEPENDENT = PROJECT / "experiments/tpc370_independent_checker.py"
STRESS = PROJECT / "experiments/tpc370_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc370_certificate.json"
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

# Filled after the claim-bearing files and PDF are final. Digests use LF.
LOCKS = {
    "producer": "4e5bb7a1e8af07afc2e405d60ea38683bee4c3ab7cb2654e7da8246073e24fe2",
    "independent": "977ed18ed50ee79bccf45ec3256c1d6707bc6726c2d7f387e1c1b6b1f5ba24e7",
    "stress": "d69b8b1127e7c3d082fecbd1d8ac23efad551f9c0157353b20df5c1a0983cc13",
    "certificate": "109cfbf11478b566c176a7bad2df3a579b4079e2ad8cbd64eb692168e91e1070",
    "main_tex": "91bc8448959f5c04b938f8d3b241e1b505bd9b57d0850005cf2a7606e01107cf",
    "main_pdf": "d6bde7a879df51c5fdfdd593bdb9c8567b8767e42a21d2c1b72c3d553df66223",
    "pdf": "d6bde7a879df51c5fdfdd593bdb9c8567b8767e42a21d2c1b72c3d553df66223",
    "log": "e3dae9504003e445ef02c673d1fe60f1028212bc918c09413bd2971921fbd283",
    "readme": "352e21ffdb79b3bf4766f18b546846dee8817dce5e4097d629f1af1bafe3ecc4",
    "plan": "8964ed6095fd4b5ec22d6adf80107ee5b2538b242db36ca639214b332d325770",
    "derivation": "cfeb83caca1fe76321d6ba142e1bd798d43e1366d8a4e67b48cd1a076f0e1f2c",
    "proof": "6064e530593e2ffa78c78052a49495494d01dd3fce325194c3614d828dbe42e0",
    "claim": "b5d8e97aea145897ccd29a2f1623e78797fd8411e58a1d216a56dd725858f672",
    "route": "4988f720de6773d9feda1d4c8787b8dd2d6b7d87e0bf31a4c72fc911ba2fb932",
    "protocol": "a0eda5bf4b847dfef9cbaa767380a068c16cb87c2bccf4149beab669b8123527",
    "bridge": "28f6ea2581677414cd61b85d469e4278b12c34dd367608fb195922e31b6c4483",
}

STATUS = "NUMERICALLY_CERTIFIED_FINITE_COUNT_2048_WINDOW_AUDIT"
SCHEMA = "TPC370_COUNT_2048_WINDOW_AUDIT_V1"
ORIGINS = [1010001, 1018021, 1026041]
COUNTS = [2048]
Q_ANCHORS = [512, 2048, 8192]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
BETAS = [0, 2]


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
    origin = payload.get("origin_protocol", {})
    need(origin.get("candidate_count") == 41 and
         origin.get("grid_start") == 1010001 and origin.get("grid_step") == 401 and
         origin.get("grid_indices") == [0, 20, 40] and
         origin.get("selected_origins") == ORIGINS and
         origin.get("response_used") is False and
         origin.get("geometry_used_for_selection") is False and
         origin.get("source_used") is False, "origin protocol")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == ORIGINS and
         protocol.get("counts") == COUNTS and
         protocol.get("q_anchors") == Q_ANCHORS and
         protocol.get("kernel_exponents") == [1] and
         protocol.get("laws") == LAWS and protocol.get("betas") == BETAS and
         protocol.get("height") == 66 and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False, "protocol")
    rows = payload.get("rows")
    expected = {(o, n, q, 1, b, law)
                for b in BETAS for o in ORIGINS for n in COUNTS
                for q in Q_ANCHORS for law in LAWS}
    need(isinstance(rows, list) and len(rows) == 72 and
         len({(row.get("origin"), row.get("count"), row.get("Q"),
               row.get("kernel_exponent"), row.get("beta"), row.get("law"))
              for row in rows}) == 72 and
         {(row.get("origin"), row.get("count"), row.get("Q"),
           row.get("kernel_exponent"), row.get("beta"), row.get("law"))
          for row in rows} == expected, "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap_repair_betas") == [] and
         phase.get("cap") == "0.64000000000000001" and
         phase.get("schur_cap") == "0.82999999999999996", "phase caps")
    for beta in BETAS:
        selected = [row for row in rows if row["beta"] == beta]
        spectral = sum(float(row["normalized"]["spectral"]) > 0.64
                       for row in selected)
        schur = sum(float(row["normalized"]["schur"]) > 0.83
                    for row in selected)
        item = phase.get("by_beta", {}).get(str(beta), {})
        need(item.get("rows") == 36 and
             item.get("spectral_cap_violations") == spectral and
             item.get("schur_cap_violations") == schur, "phase " + str(beta))
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 72 and audit.get("settings_per_beta") == 36 and
         audit.get("beta_count") == 2 and audit.get("spectral_rows") == 72 and
         audit.get("beta2_rows") == 36 and
         audit.get("beta2_spectral_cap_violations") ==
         phase["by_beta"]["2"]["spectral_cap_violations"] and
         audit.get("beta2_schur_cap_violations") ==
         phase["by_beta"]["2"]["schur_cap_violations"] and
         audit.get("baseline_beta0_spectral_cap_violations") ==
         phase["by_beta"]["0"]["spectral_cap_violations"] and
         audit.get("baseline_beta0_schur_cap_violations") ==
         phase["by_beta"]["0"]["schur_cap_violations"] and
         audit.get("q_min") == 512 and audit.get("q_max") == 8192 and
         audit.get("count_min") == 2048 and audit.get("count_max") == 2048 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    actual_failure_keys = [
        [row["origin"], row["count"], row["Q"], row["kernel_exponent"],
         row["law"]]
        for row in rows if row["beta"] == 2 and
        float(row["normalized"]["spectral"]) > 0.64
    ]
    actual_signature = sorted([[key[0], key[2], key[3], key[4]]
                                for key in actual_failure_keys])
    parent_keys = audit.get("parent_failure_keys")
    parent_signature = audit.get("parent_failure_signature")
    need(isinstance(parent_keys, list) and
         parent_signature == sorted([[key[0], key[2], key[3], key[4]]
                                     for key in parent_keys]) and
         audit.get("replicated_failure_keys") == actual_failure_keys and
         audit.get("replicated_failure_signature") == actual_signature and
         audit.get("failure_signature_matches_parent") ==
         (actual_signature == parent_signature), "failure signature")
    need(payload.get("exact_theorem", {}).get("anchor_inheritance") == {
        "interval": [1010346, 1010359], "Q": 4,
        "kernel_exponent": 1,
        "source_project": "TPC-369 third predeclared origin-family audit",
    }, "anchor inheritance")
    expected_firewall = {
        "TPC370_ORIGIN_FAMILY_PROTOCOL": "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC370_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC370_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_72_ROWS",
        "TPC370_COUNT_2048_WINDOW": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC370_BETA2_PHASE_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC370_BETA2_PARENT_SIGNATURE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC370_ORIGIN_UNIFORMITY": "OPEN",
        "TPC370_WINDOW_UNIFORMITY": "OPEN",
        "TPC370_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC370_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC370_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC370_SOURCE_UNIFORM_L2": "OPEN",
        "TPC370_ARITHMETIC_ADVANCE": "NO",
        "TPC370_FIXED_POWER_CREDIT": 0,
        "TPC370_FULL_GATE_B": "OPEN",
        "TPC370_TWIN_PRIME_RESULT": "NONE",
    }
    firewall = payload.get("claim_firewall", {})
    for key, value in expected_firewall.items():
        need(firewall.get(key) == value, "firewall " + key)
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC370_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_72_ROWS",
            "TPC370_BETA2_PARENT_SIGNATURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC370_ARITHMETIC_ADVANCE = NO",
            "TPC370_FULL_GATE_B = OPEN"):
        need(marker in text, "bridge marker")
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
            "bridge": BRIDGE,
        }
        for key, path in paths.items():
            lock(path, LOCKS[key], key)
        check_certificate()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        jobs = (tuple((script, False) for script in scripts) +
                tuple((script, True) for script in scripts))
        with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
            outputs = tuple(pool.map(lambda job: run(*job), jobs))
        normal, optimized = outputs[:3], outputs[3:]
        need(normal == optimized, "normal/optimized stdout mismatch")
        need(normal[0] == b"TPC370_CERTIFICATE=PASS rows=72 beta2_rows=36\n",
             "producer output")
        need(normal[1] ==
             b"TPC370_INDEPENDENT_CHECK=PASS rows=72 beta2_rows=36 "
             b"beta2_violations=6 baseline_beta0_violations=9\n",
             "independent output")
        need(normal[2] ==
             b"TPC370_STRESS=PASS exact_baseline=1 mutations=32\n",
             "stress output")
        print("TPC370_BRIDGE_CHECK=PASS rows=72 beta2_rows=36 "
              "beta2_violations=6 baseline_beta0_violations=9")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC370_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
