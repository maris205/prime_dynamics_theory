#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-366."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-366-beta2-higher-q-ladder"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc366_beta2_higher_q_ladder.md")
PRODUCER = PROJECT / "code/tpc366_beta2_higher_q_ladder.py"
INDEPENDENT = PROJECT / "experiments/tpc366_independent_checker.py"
STRESS = PROJECT / "experiments/tpc366_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc366_certificate.json"
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

# Filled after all project files are final.  Digests are normalized to LF.
LOCKS = {
    "producer": "69708452e8d37f8be249b85d2d206019459b07fd32b995ab33ea098535b23c75",
    "independent": "1a23e86c8a8a7a646a4ead31781c70b26008f7940f485c21d11fbfcc943260fa",
    "stress": "354f6cd04a83cfc97a6c722a3c5e46a10f51d67d9e2419231a26440a28fc5e1b",
    "certificate": "6e4b29ba36a074717d27846149797c69eba7b1a2c3a362c98866d0eb8d8d43c5",
    "main_tex": "e061dd122c2990d8864fc0fbb0a70831a5a04679a7cc2b13e984a3fc874789e1",
    "main_pdf": "e55df843ae714d53e990890bc917374d89d76244ce88e9d7e46846afde877548",
    "pdf": "e55df843ae714d53e990890bc917374d89d76244ce88e9d7e46846afde877548",
    "log": "4474ed39a86047641f8dcd2c78adcd4cd8f5030811b06c76496052e73d33a2e7",
    "readme": "f9925a7e6f2ba5ecbb716d5944eade692fa88cdaa5cdfceb6d48dec0f357ef4f",
    "plan": "bfc20cd034cf08a7e2de78cff77e8fbc007006cdad44bbc8308808e05780cd1d",
    "derivation": "09084c43013399eb630c6c6e63a76a5082df4cccd51722c664dec3fca1c54eab",
    "proof": "5e17bb82ce232c3d0cc0c6a93731af0a56cba0aa3fbeeffac9c0e2a0c5718a82",
    "claim": "7decdd76be2583935f1abd22e9d4d84588d864a8fde6d34e1e7a74d469996ec4",
    "route": "f0184a954047fe8a8dbcdc8fd462f9c1fb51d9cf4e0b1285d1440a02ffd36746",
    "protocol": "045a77d36d8c370abb3bf78f767dc95b61e24b8b7a259af5309d6da5a038867d",
    "bridge": "f91cd6701591985bd7c9a35988a55233394e54a9728ba4b5dccbba073d541e35",
}

STATUS = "NUMERICALLY_CERTIFIED_FINITE_BETA2_HIGHER_Q_LADDER"
SCHEMA = "TPC366_BETA2_HIGHER_Q_LADDER_V1"


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
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [623071, 631360, 629211] and
         protocol.get("counts") == [256, 512] and
         protocol.get("q_anchors") == [512, 1024, 2048, 4096, 8192] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"] and
         protocol.get("betas") == [0, 2] and
         protocol.get("selection_beta") == 2 and
         protocol.get("pilot_count") == 256 and
         protocol.get("minimum_separation") == 2048 and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False and
         protocol.get("selection_response_blind") is True, "protocol")
    selection = payload.get("selection", {})
    need(selection.get("candidate_count") == 41 and
         selection.get("selected_origins") == [623071, 631360, 629211] and
         selection.get("selection_beta") == 2 and
         selection.get("pilot_count") == 256 and
         selection.get("minimum_separation") == 2048, "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 480 and
         len({(row.get("origin"), row.get("count"), row.get("Q"),
               row.get("kernel_exponent"), row.get("beta"), row.get("law"))
              for row in rows}) == 480, "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap_repair_betas") == [2], "repair beta")
    for beta, violations, schur_violations in ((0, 60, 60), (2, 0, 0)):
        item = phase.get("by_beta", {}).get(str(beta), {})
        need(item.get("rows") == 240 and
             item.get("spectral_cap_violations") == violations and
             item.get("schur_cap_violations") == schur_violations,
             "phase " + str(beta))
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 480 and
         audit.get("settings_per_beta") == 240 and
         audit.get("beta_count") == 2 and
         audit.get("spectral_rows") == 480 and
         audit.get("beta2_rows") == 240 and
         audit.get("beta2_cap_violations") == 0 and
         audit.get("beta2_schur_cap_violations") == 0 and
         audit.get("baseline_beta0_cap_violations") == 60 and
         audit.get("baseline_beta0_schur_cap_violations") == 60 and
         audit.get("q_min") == 512 and audit.get("q_max") == 8192 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    firewall = payload.get("claim_firewall", {})
    expected = {
        "TPC366_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_RESPONSE_BLIND",
        "TPC366_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC366_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_480_ROWS",
        "TPC366_HIGHER_Q_LADDER": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC366_BETA2_HIGHER_Q_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC366_BETA2_SCALE_UNIFORMITY": "OPEN",
        "TPC366_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC366_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC366_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC366_SOURCE_UNIFORM_L2": "OPEN",
        "TPC366_ARITHMETIC_ADVANCE": "NO",
        "TPC366_FIXED_POWER_CREDIT": 0,
        "TPC366_FULL_GATE_B": "OPEN",
        "TPC366_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        need(firewall.get(key) == value, "firewall " + key)
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC366_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_480_ROWS",
            "TPC366_BETA2_HIGHER_Q_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC366_ARITHMETIC_ADVANCE = NO",
            "TPC366_FULL_GATE_B = OPEN"):
        need(marker in bridge_text, "bridge marker")
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
        normal = tuple(run(script, False) for script in scripts)
        optimized = tuple(run(script, True) for script in scripts)
        need(normal == optimized, "normal/optimized stdout mismatch")
        need(normal[0] == b"TPC366_CERTIFICATE=PASS rows=480 beta2_rows=240 "
             b"beta2_violations=0 baseline_beta0_violations=60\n",
             "producer output")
        need(normal[1] == b"TPC366_INDEPENDENT_CHECK=PASS rows=480 beta2_rows=240 "
             b"beta2_violations=0 baseline_beta0_violations=60\n",
             "independent output")
        need(normal[2] == b"TPC366_STRESS=PASS exact_baseline=1 mutations=23\n",
             "stress output")
        print("TPC366_BRIDGE_CHECK=PASS rows=480 beta2_rows=240 "
              "beta2_violations=0 baseline_beta0_violations=60")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC366_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
