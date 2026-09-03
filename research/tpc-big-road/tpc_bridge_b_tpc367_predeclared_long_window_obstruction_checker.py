#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-367."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-367-predeclared-long-window-obstruction"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc367_predeclared_long_window_obstruction.md")
PRODUCER = PROJECT / "code/tpc367_predeclared_long_window_obstruction.py"
INDEPENDENT = PROJECT / "experiments/tpc367_independent_checker.py"
STRESS = PROJECT / "experiments/tpc367_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc367_certificate.json"
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

# Filled after all claim-bearing files are final.  Digests use normalized LF.
LOCKS = {
    "producer": "a4d70e6a62351d41867e014f4a1e7f8792240c5dfcb58df1da192caa8e180899",
    "independent": "9bdc4bb2aefa3bd2584e2c8f74bf4eee2e814d3bc2c5352544aa5d7a183c3b0a",
    "stress": "1ea396d591224041bfdcb93115f6c75e14ec8529f6a3f06c9a99c18d6ef0b855",
    "certificate": "7d5c7d41e6b7c427791f9652dd4837908ffb6bd14576621ade0993ce513ea385",
    "main_tex": "fd041e8b82be27c64664400d330690e7fba63296fa4f1081fa8ce335746d08b8",
    "main_pdf": "3cfe849a481616f55ad01b7b16075f2bafe711e71a06a05dfa2a83808441030a",
    "pdf": "3cfe849a481616f55ad01b7b16075f2bafe711e71a06a05dfa2a83808441030a",
    "log": "14cfdb0558dead4c2372f31ce45b292f000f889585b018e20fde8131314e1671",
    "readme": "3bc19c6cf1fb51d71ccbafe67b1b33f45d6682afd17ae166c7ec343aad038333",
    "plan": "46f23eeec9a916919d735730e970918d47062f24de86f643d8f474bd220edbd2",
    "derivation": "685aa52a4ee21f7c024392dc883f6c601f2fc23d2686b3556b53da944e2a438b",
    "proof": "9cc8f134662359b837a3d708b50daf5b3307cbd247c1ea36ad68e745e6aca2ee",
    "claim": "e1cfcd617858ed44fad10a6990ebb7d5c3e148927f11505d76cdd8ac97a79400",
    "route": "bc7f52f9fab9196b10a155aa5074421713a852d18ab24d1d04a49b7c496c4ceb",
    "protocol": "638b3e9897c9ea1a7907dea6ac02ad5d09d3d117211e04a6933684fa5d27eb58",
    "bridge": "ec4de09066c2d3e2e83b0b67b0e909cc2bdd224ea6336842a5d1392a16a54c4f",
}

STATUS = "NUMERICALLY_CERTIFIED_FINITE_PREDECLARED_LONG_WINDOW_OBSTRUCTION"
SCHEMA = "TPC367_PREDECLARED_LONG_WINDOW_OBSTRUCTION_V1"


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
         origin.get("grid_start") == 620001 and origin.get("grid_step") == 307 and
         origin.get("grid_indices") == [0, 20, 40] and
         origin.get("selected_origins") == [620001, 626141, 632281] and
         origin.get("response_used") is False and
         origin.get("geometry_used_for_selection") is False and
         origin.get("source_used") is False, "origin protocol")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [620001, 626141, 632281] and
         protocol.get("counts") == [512, 1024] and
         protocol.get("q_anchors") == [512, 2048, 8192] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"] and
         protocol.get("betas") == [0, 2] and protocol.get("height") == 66 and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False, "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 288 and
         len({(row.get("origin"), row.get("count"), row.get("Q"),
               row.get("kernel_exponent"), row.get("beta"), row.get("law"))
              for row in rows}) == 288, "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap_repair_betas") == [], "repair beta")
    for beta, violations, schur_violations in ((0, 36, 36), (2, 6, 0)):
        item = phase.get("by_beta", {}).get(str(beta), {})
        need(item.get("rows") == 144 and
             item.get("spectral_cap_violations") == violations and
             item.get("schur_cap_violations") == schur_violations,
             "phase " + str(beta))
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 288 and audit.get("settings_per_beta") == 144 and
         audit.get("beta_count") == 2 and audit.get("spectral_rows") == 288 and
         audit.get("beta2_rows") == 144 and
         audit.get("beta2_spectral_cap_violations") == 6 and
         audit.get("beta2_schur_cap_violations") == 0 and
         audit.get("baseline_beta0_spectral_cap_violations") == 36 and
         audit.get("baseline_beta0_schur_cap_violations") == 36 and
         audit.get("q_min") == 512 and audit.get("q_max") == 8192 and
         audit.get("count_min") == 512 and audit.get("count_max") == 1024 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    expected = {
        "TPC367_ORIGIN_PROTOCOL": "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
        "TPC367_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC367_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
        "TPC367_LONG_WINDOW_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC367_UNSELECTED_ORIGIN_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC367_BETA2_LONG_WINDOW_TRANSFER": "REFUTED_SCOPED",
        "TPC367_BETA2_EXPONENT_SENSITIVITY": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC367_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC367_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC367_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC367_SOURCE_UNIFORM_L2": "OPEN",
        "TPC367_ARITHMETIC_ADVANCE": "NO",
        "TPC367_FIXED_POWER_CREDIT": 0,
        "TPC367_FULL_GATE_B": "OPEN",
        "TPC367_TWIN_PRIME_RESULT": "NONE",
    }
    firewall = payload.get("claim_firewall", {})
    for key, value in expected.items():
        need(firewall.get(key) == value, "firewall " + key)
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC367_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
            "TPC367_BETA2_LONG_WINDOW_TRANSFER = REFUTED_SCOPED",
            "TPC367_ARITHMETIC_ADVANCE = NO",
            "TPC367_FULL_GATE_B = OPEN"):
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
        need(normal[0] == b"TPC367_CERTIFICATE=PASS rows=288 beta2_rows=144\n",
             "producer output")
        need(normal[1] == b"TPC367_INDEPENDENT_CHECK=PASS rows=288 beta2_rows=144 "
             b"beta2_violations=6 baseline_beta0_violations=36\n",
             "independent output")
        need(normal[2] == b"TPC367_STRESS=PASS exact_baseline=1 mutations=28\n",
             "stress output")
        print("TPC367_BRIDGE_CHECK=PASS rows=288 beta2_rows=144 "
              "beta2_violations=6 baseline_beta0_violations=36")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC367_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
