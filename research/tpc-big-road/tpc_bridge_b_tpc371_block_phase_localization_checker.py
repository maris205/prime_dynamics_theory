#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-371."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-371-block-phase-localization"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc371_block_phase_localization.md"
PRODUCER = PROJECT / "code/tpc371_block_phase_localization.py"
INDEPENDENT = PROJECT / "experiments/tpc371_independent_checker.py"
STRESS = PROJECT / "experiments/tpc371_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc371_certificate.json"
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
LEDGER = PROJECT / "notes/theorem_ledger.md"

# Digests are normalized to LF.  This dictionary is filled only after all
# claim-bearing files and the PDF are final; the checker deliberately does not
# lock its own source file.
LOCKS = {
    "producer": "a2190210a2d43eefb1f37f81f55b2240b6b254fd4f9afa1c26cd5e0c097d8462",
    "independent": "6befa82d5e25e1f30e2316b50c6b434d811ffc45e7eeb1350d45b9f1e75dcf95",
    "stress": "4893aac71c3bcf46f7e893557ec0b788823d1f68bc8774cafbabd4ee7002accc",
    "certificate": "01ba3b91db1f2a58b70da6b5334127f07350244f07b34772bf83dc4e69ac1ba3",
    "main_tex": "9b19af1f905d66ca092f2335f80d148eba47e008a43138de8f7f8a21e285facc",
    "main_pdf": "dd2c041c1560a56314e987860ecda002eb1a3b318cb831d5a0ea7c7eb507f2c3",
    "pdf": "dd2c041c1560a56314e987860ecda002eb1a3b318cb831d5a0ea7c7eb507f2c3",
    "log": "4e78afe1c4b662b29f258cb95f39fd61c7417bf7e2c2eea70fa9232c6c33bfc7",
    "readme": "9b89689cf1b9bbb093bbc2fc85a839a0ccb0786d535caa9d0179f748714ab43e",
    "plan": "c25a8a069ebfe90987e01d10c87b8638f0dd40c8942393519ad1ef21fc891a76",
    "derivation": "34dedad86ac30f0204d4649bb98298667431f422a495cb34ba9aba5e3973e600",
    "proof": "0dd9db7b8b6d555c3962ce95fc37cc5239fad193eeee89d7ecf8fead3405852f",
    "claim": "290a65dbaa1709653e669096514f0b59eeb88f42316563b2ea3fcdc810317148",
    "route": "60d4d539e0b912e7ace7c79bd276a5c0f954d14b573a3fc123f7955c7d4795dd",
    "protocol": "f9abb377589d124bbfe342ea13402763486f43f61070d34960eb0ecc4168fb24",
    "ledger": "299c3e7c7a30bf7aa3bb5de26f3667b9f970400a1c357e61416b7900df8aad97",
    "bridge": "7b310ca84dda0695b2857dcc698e21668932c6f121a2ef0a1fd41f45cdc83068",
}

STATUS = "NUMERICALLY_CERTIFIED_FINITE_BLOCK_PHASE_LOCALIZATION"
SCHEMA = "TPC371_COUNT_2048_BLOCK_PHASE_LOCALIZATION_V1"
ORIGINS = [1010001, 1018021, 1026041]
Q_ANCHORS = [512, 2048, 8192]
BETAS = [0, 2]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
BLOCK_INDICES = list(range(8))


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
         origin.get("grid_start") == 1010001 and
         origin.get("grid_step") == 401 and
         origin.get("grid_indices") == [0, 20, 40] and
         origin.get("selected_origins") == ORIGINS and
         origin.get("response_used") is False and
         origin.get("geometry_used_for_selection") is False and
         origin.get("source_used") is False, "origin protocol")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == ORIGINS and
         protocol.get("window_count") == 2048 and
         protocol.get("block_count") == 256 and
         protocol.get("block_indices") == BLOCK_INDICES and
         protocol.get("q_anchors") == Q_ANCHORS and
         protocol.get("kernel_exponents") == [1] and
         protocol.get("laws") == LAWS and protocol.get("betas") == BETAS and
         protocol.get("height") == 66 and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False and
         protocol.get("block_selection_used") is False, "protocol")
    rows = payload.get("rows")
    expected = {(o, b, q, 1, beta, law)
                for beta in BETAS for o in ORIGINS for b in BLOCK_INDICES
                for q in Q_ANCHORS for law in LAWS}
    need(isinstance(rows, list) and len(rows) == 576 and
         {(row.get("origin"), row.get("block_index"), row.get("Q"),
           row.get("kernel_exponent"), row.get("beta"), row.get("law"))
          for row in rows} == expected, "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap") == "0.64000000000000001" and
         phase.get("schur_cap") == "0.82999999999999996" and
         phase.get("cap_repair_betas") == [], "phase caps")
    expected_counts = {0: (72, 72), 2: (0, 0)}
    for beta in BETAS:
        selected = [row for row in rows if row["beta"] == beta]
        item = phase.get("by_beta", {}).get(str(beta), {})
        need(item.get("rows") == 288 and item.get("blocks") == 24 and
             item.get("spectral_cap_violations") == expected_counts[beta][0] and
             item.get("schur_cap_violations") == expected_counts[beta][1] and
             item.get("spectral_cap_violations") == sum(
                 float(row["normalized"]["spectral"]) > .64
                 for row in selected) and
             item.get("schur_cap_violations") == sum(
                 float(row["normalized"]["schur"]) > .83
                 for row in selected), "phase beta")
        for q0 in Q_ANCHORS:
            setting = [row for row in selected if row["Q"] == q0]
            qitem = phase.get("by_beta_q", {}).get(f"{beta}:{q0}", {})
            need(qitem.get("rows") == 96 and
                 qitem.get("spectral_cap_violations") == sum(
                     float(row["normalized"]["spectral"]) > .64
                     for row in setting) and
                 qitem.get("schur_cap_violations") == sum(
                     float(row["normalized"]["schur"]) > .83
                     for row in setting), "phase q")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 576 and
         audit.get("settings_per_beta") == 288 and
         audit.get("origin_count") == 3 and audit.get("block_count") == 8 and
         audit.get("rows_per_origin") == 96 and audit.get("beta_count") == 2 and
         audit.get("spectral_rows") == 576 and audit.get("beta2_rows") == 288 and
         audit.get("window_count") == 2048 and
         audit.get("block_count_fixed") == 256 and
         audit.get("q_min") == 512 and audit.get("q_max") == 8192 and
         audit.get("beta2_spectral_cap_violations") == 0 and
         audit.get("beta2_schur_cap_violations") == 0 and
         audit.get("baseline_beta0_spectral_cap_violations") == 72 and
         audit.get("baseline_beta0_schur_cap_violations") == 72 and
         audit.get("beta2_failure_keys") == [] and
         audit.get("beta2_failure_block_count") == 0 and
         audit.get("beta2_all_declared_blocks_pass") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    need(payload.get("exact_theorem", {}).get("anchor_inheritance") == {
        "interval": [1010346, 1010359], "Q": 4, "kernel_exponent": 1,
        "source_project": "TPC-370 count-2048 finite-window audit",
    }, "anchor inheritance")
    firewall = payload.get("claim_firewall", {})
    expected_firewall = {
        "TPC371_ORIGIN_FAMILY_PROTOCOL": "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC371_BLOCK_PARTITION": "PROVED_EXACT_FINITE_PREDECLARED",
        "TPC371_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC371_BLOCK_LOCAL_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_576_ROWS",
        "TPC371_BETA2_BLOCK_PHASE_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC371_BETA2_LOCAL_FAILURE": "REFUTED_SCOPED",
        "TPC371_CROSS_BLOCK_COHERENCE": "OPEN",
        "TPC371_ORIGIN_UNIFORMITY": "OPEN",
        "TPC371_WINDOW_UNIFORMITY": "OPEN",
        "TPC371_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC371_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC371_SOURCE_UNIFORM_L2": "OPEN",
        "TPC371_ARITHMETIC_ADVANCE": "NO",
        "TPC371_FIXED_POWER_CREDIT": 0,
        "TPC371_FULL_GATE_B": "OPEN",
        "TPC371_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected_firewall.items():
        need(firewall.get(key) == value, "firewall " + key)
    need(BRIDGE.read_text(encoding="utf-8").count(
        "TPC371_BETA2_LOCAL_FAILURE = REFUTED_SCOPED") == 1,
         "bridge firewall")
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
            "ledger": LEDGER, "bridge": BRIDGE,
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
             b"TPC371_CERTIFICATE=PASS rows=576 beta2_rows=288 "
             b"beta2_violations=0 baseline_beta0_violations=72\n",
             "producer output")
        need(normal[1] ==
             b"TPC371_INDEPENDENT_CHECK=PASS rows=576 beta2_rows=288 "
             b"beta2_violations=0 baseline_beta0_violations=72\n",
             "independent output")
        need(normal[2] == b"TPC371_STRESS=PASS exact_baseline=1 mutations=36\n",
             "stress output")
        print("TPC371_BRIDGE_CHECK=PASS rows=576 beta2_rows=288 "
              "beta2_violations=0 baseline_beta0_violations=72")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC371_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
