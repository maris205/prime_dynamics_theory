#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-368."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-368-predeclared-origin-replication"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc368_predeclared_origin_replication.md")
PRODUCER = PROJECT / "code/tpc368_predeclared_origin_replication.py"
INDEPENDENT = PROJECT / "experiments/tpc368_independent_checker.py"
STRESS = PROJECT / "experiments/tpc368_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc368_certificate.json"
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
    "producer": "621be17f620896f38ddfd72df0e09276e4266f3526d28ff6e91f3ff981bc7b6e",
    "independent": "9c3a6d8212ae62ef505169f6ebbadde72666386cc648de3bd4322289fcd1f5af",
    "stress": "fe9af031187d2859ba2a8e158efc81b2a5f6f173395e8b9605036e1b18ce6fe8",
    "certificate": "6b2911c3bdb03d6e53d6aa3839e83f1a688735a41c88db76dff404196ed8ff5b",
    "main_tex": "77397e82c262fddf2a2926a9542308b8edf65149291c65b73ca63ed257bd71ad",
    "main_pdf": "75d41a1a9d2dfc97de35448c1d047fdd9384e9672b20d90ca6f752f4592be0db",
    "pdf": "75d41a1a9d2dfc97de35448c1d047fdd9384e9672b20d90ca6f752f4592be0db",
    "log": "78c23113986005e64e218ab83b5957e8c4b0e70a1e82192b85a10d13e79cd35b",
    "readme": "666a541b9cb94c007c293cfd92d229d0719ae1e558d21ce5a6af0e9e497054bd",
    "plan": "6ad878a76add9aeddd5a166e68d64b4e855b013eceef356a974f0b9c6795ac34",
    "derivation": "16ecb32a519fe8028b2bfb32cb297abe4ddee7efceaea6c25038821d7fea573e",
    "proof": "15e54ba13687258f4a46dd3390c1713a2ba6a457f58cba6b3377994c9740316a",
    "claim": "ef006cf402405fdd585081d6743d2893bc0b7e9050074d89c537cde97b5b52bf",
    "route": "9fab91817a6f8d30cf1cb830608e1d69464a94f77985fe4718ba935a6fef5b10",
    "protocol": "288f688a0981531d92fe9e50ef65b59d3ee39d0aaa4938f343446f9c96fa4e0c",
    "bridge": "7091c46e430b8a16d643a30a5acaf2a8f506322bd16f454ab148b7bb2b566d05",
}

STATUS = "NUMERICALLY_CERTIFIED_FINITE_PREDECLARED_ORIGIN_REPLICATION"
SCHEMA = "TPC368_PREDECLARED_ORIGIN_REPLICATION_V1"


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
         origin.get("grid_start") == 810001 and origin.get("grid_step") == 353 and
         origin.get("grid_indices") == [0, 20, 40] and
         origin.get("selected_origins") == [810001, 817061, 824121] and
         origin.get("response_used") is False and
         origin.get("geometry_used_for_selection") is False and
         origin.get("source_used") is False, "origin protocol")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [810001, 817061, 824121] and
         protocol.get("counts") == [512, 1024] and
         protocol.get("q_anchors") == [512, 2048, 8192] and
         protocol.get("kernel_exponents") == [1] and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"] and
         protocol.get("betas") == [0, 2] and protocol.get("height") == 66 and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False, "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 144 and
         len({(row.get("origin"), row.get("count"), row.get("Q"),
               row.get("kernel_exponent"), row.get("beta"), row.get("law"))
              for row in rows}) == 144, "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap_repair_betas") == [], "repair beta")
    for beta, violations, schur_violations in ((0, 18, 18), (2, 6, 0)):
        item = phase.get("by_beta", {}).get(str(beta), {})
        need(item.get("rows") == 72 and
             item.get("spectral_cap_violations") == violations and
             item.get("schur_cap_violations") == schur_violations,
             "phase " + str(beta))
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 144 and audit.get("settings_per_beta") == 72 and
         audit.get("beta_count") == 2 and audit.get("spectral_rows") == 144 and
         audit.get("beta2_rows") == 72 and
         audit.get("beta2_spectral_cap_violations") == 6 and
         audit.get("beta2_schur_cap_violations") == 0 and
         audit.get("baseline_beta0_spectral_cap_violations") == 18 and
         audit.get("baseline_beta0_schur_cap_violations") == 18 and
         audit.get("q_min") == 512 and audit.get("q_max") == 8192 and
         audit.get("count_min") == 512 and audit.get("count_max") == 1024 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    expected = {
        "TPC368_ORIGIN_FAMILY_PROTOCOL": "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
        "TPC368_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC368_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
        "TPC368_SECOND_ORIGIN_FAMILY": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC368_BETA2_LONG_WINDOW_REPLICATION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC368_BETA2_FAILURE_PATTERN": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC368_ORIGIN_UNIFORMITY": "OPEN",
        "TPC368_WINDOW_UNIFORMITY": "OPEN",
        "TPC368_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC368_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC368_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC368_SOURCE_UNIFORM_L2": "OPEN",
        "TPC368_ARITHMETIC_ADVANCE": "NO",
        "TPC368_FIXED_POWER_CREDIT": 0,
        "TPC368_FULL_GATE_B": "OPEN",
        "TPC368_TWIN_PRIME_RESULT": "NONE",
    }
    firewall = payload.get("claim_firewall", {})
    for key, value in expected.items():
        need(firewall.get(key) == value, "firewall " + key)
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC368_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
            "TPC368_BETA2_LONG_WINDOW_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC368_ARITHMETIC_ADVANCE = NO",
            "TPC368_FULL_GATE_B = OPEN"):
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
        need(normal[0] == b"TPC368_CERTIFICATE=PASS rows=144 beta2_rows=72\n",
             "producer output")
        need(normal[1] == b"TPC368_INDEPENDENT_CHECK=PASS rows=144 beta2_rows=72 "
             b"beta2_violations=6 baseline_beta0_violations=18\n",
             "independent output")
        need(normal[2] == b"TPC368_STRESS=PASS exact_baseline=1 mutations=29\n",
             "stress output")
        print("TPC368_BRIDGE_CHECK=PASS rows=144 beta2_rows=72 "
              "beta2_violations=6 baseline_beta0_violations=18")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC368_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
