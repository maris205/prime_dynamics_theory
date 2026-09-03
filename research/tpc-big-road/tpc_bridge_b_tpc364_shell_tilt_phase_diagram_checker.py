#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-364."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-364-shell-tilt-phase-diagram"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc364_shell_tilt_phase_diagram.md"
PRODUCER = PROJECT / "code/tpc364_shell_tilt_phase_diagram.py"
INDEPENDENT = PROJECT / "experiments/tpc364_independent_checker.py"
STRESS = PROJECT / "experiments/tpc364_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc364_certificate.json"
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

# Filled after the project and manuscript are final.
LOCKS = {
    "producer": "8b7428b02294cf1a7daca7317b2d312af44f64bf153b86f99f4a18cb27e02dd2",
    "independent": "244eff77f63c6323f65790d8e7bc0ec0c4dd459a0ca0ca453fa911b2f5c01fa7",
    "stress": "948ac6d517e0f04b1a313e3f0ee3c93042888e3b82100ec34cdac82e68bd4acd",
    "certificate": "5b6aa0e6f97a746d27a36c7866810b2450a84096d911734bd2065784486a4058",
    "main_tex": "947cb84cdf6db4fc614864e38f4faa19db4794d07bc9644e539130e0685a7995",
    "main_pdf": "9d3b033f971b9f1885b162ca51e1e38ff8916c8a6e2117de00a705b077229966",
    "pdf": "9d3b033f971b9f1885b162ca51e1e38ff8916c8a6e2117de00a705b077229966",
    "log": "2840a01442cd11eea1590bd13b3d379654cb2d27a333486952dfd66de4bc5670",
    "readme": "65a628b7c658b1ca3d94436559f374ebb4811824a1976b5330a514330940d30f",
    "plan": "120f84a092e75f14c77eacf27e976fa2d18d4e256b52e1fed6a58d9daef4b4c9",
    "derivation": "46e8af8ba690b4df52daae7c603a6f450390b5accdf84122caffd07d11fc63f0",
    "proof": "23071f80814e4e283b0f5d54106289652ac679471a7c080faaed6c709499a21b",
    "claim": "e0e6c51139299b4b81cc59f13b3357ced141bd07887afaa27b581c677dbf5594",
    "route": "15bf4592486492e71f9eb7b2daa049992ae05f2d7cb02ed5920c08ef7464cee0",
    "protocol": "631aa2f71abba5f83471e776ee27dc299b79acc3f29e1d8dd77fd1093df913a6",
    "bridge": "a5e4ee4c3330d6f8d9ad7013b7f39b95b7cee3dd8517f5cc81b9fa2d8991af44",
}

STATUS = "NUMERICALLY_CERTIFIED_FINITE_SHELL_TILT_PHASE_DIAGRAM"
SCHEMA = "TPC364_SHELL_TILT_PHASE_DIAGRAM_V1"


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
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "schema/hash")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [313030, 311166, 321651] and
         protocol.get("counts") == [256, 512] and
         protocol.get("q_anchors") == [80, 128, 256, 512] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"] and
         protocol.get("betas") == [-2, -1, 0, 1, 2] and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 960 and
         audit.get("settings_per_beta") == 48 and
         audit.get("beta_count") == 5 and
         audit.get("spectral_rows") == 960 and
         audit.get("beta2_cap_repair_rows") == 192 and
         audit.get("beta2_total_rows") == 192 and
         audit.get("baseline_beta0_cap_violations") == 30 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap_repair_betas") == [2], "phase repair")
    need({str(beta): phase.get("by_beta", {}).get(str(beta), {}).get(
              "spectral_cap_violations") for beta in (-2, -1, 0, 1, 2)} ==
         {"-2": 63, "-1": 36, "0": 30, "1": 30, "2": 0},
         "phase census")
    expected_firewall = {
        "TPC364_WEIGHTED_BLOCK_DEFINITION": "PROVED_EXACT_FINITE",
        "TPC364_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC364_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_960_ROWS",
        "TPC364_PHASE_DIAGRAM": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC364_BETA2_PANEL_CAP_REPAIR": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC364_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC364_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC364_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC364_SOURCE_UNIFORM_L2": "OPEN",
        "TPC364_ARITHMETIC_ADVANCE": "NO",
        "TPC364_FIXED_POWER_CREDIT": 0,
        "TPC364_FULL_GATE_B": "OPEN", "TPC364_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected_firewall.items():
        need(payload.get("claim_firewall", {}).get(key) == value,
             "firewall " + key)
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC364_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_960_ROWS",
            "TPC364_BETA2_PANEL_CAP_REPAIR = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC364_ARITHMETIC_ADVANCE = NO",
            "TPC364_FULL_GATE_B = OPEN"):
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
        print("TPC364_BRIDGE_CHECK=PASS rows=960 beta2_repaired=192 "
              "beta2_violations=0 baseline_beta0_violations=30")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC364_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
