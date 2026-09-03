#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-365."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-365-beta2-fresh-holdout"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc365_beta2_fresh_holdout.md")
PRODUCER = PROJECT / "code/tpc365_beta2_fresh_holdout.py"
INDEPENDENT = PROJECT / "experiments/tpc365_independent_checker.py"
STRESS = PROJECT / "experiments/tpc365_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc365_certificate.json"
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

# Filled after all project files are final.
LOCKS = {
    "producer": "2017e42834eda4f015ae33c75a2b34516d6a0cc0c49a91aee98abb1adb0fb7db",
    "independent": "a3db8a90fb89e183f3317432090a87c236f7d3da1888bcdf0a3d219ae5d61370",
    "stress": "851c9b7f2a57e955b1e241603ebbd6fdda119870fc64a67e9dfb6f270f56c298",
    "certificate": "39a55a6bd7c2ed05d02b7524236d0cbcb67c2a9467940825b170c138ad8ed5c8",
    "main_tex": "0930e954fd125264c343caf2a4a3d23dbda5af1a1550988b3d521bb06694f0c7",
    "main_pdf": "5cd4073e96359a63710d38f6cd2057a871b9d55aa1102588030bfc05a10d37d2",
    "pdf": "5cd4073e96359a63710d38f6cd2057a871b9d55aa1102588030bfc05a10d37d2",
    "log": "d9b71c242ae2903635e4269d091d395d365bd9e6dbff31050327eb078754f06e",
    "readme": "fb2cedf3871b9a0c4902325607115aff868a2f5d0252cf1b9afe7d7932214171",
    "plan": "d2b7b9d74ad15562ef49e9c6491ab4e8b3804639ba33753a3d6afecf130c5fcf",
    "derivation": "76a3c7066ba38774550cfe92fdacf650cf2ae94034ed7ee7e1b9d3a92d34ebec",
    "proof": "e276dc70c691a22b47c39ee29cdd45d019206551e906480c228c4b02bead89b7",
    "claim": "f778a86f646307f31fe1feb782cabe07ad54d4b2a694463b94294f17b2c30243",
    "route": "e4d5177b4297bb9586524a643f1877b60b1d511fc0122a0c665093fb41373e84",
    "protocol": "a290c18ae7a2603270beb6c5e7d71749aae2e1581433ef92411b5227f3d407a6",
    "bridge": "accc623c4c037f18bd8c4a2d25ee483de5b67719d82df39256e9147fc065e4a6",
}

STATUS = "NUMERICALLY_CERTIFIED_FINITE_BETA2_FRESH_HOLDOUT"
SCHEMA = "TPC365_BETA2_FRESH_HOLDOUT_V1"


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
    need(protocol.get("origins") == [413342, 410258, 416940] and
         protocol.get("counts") == [256, 512] and
         protocol.get("q_anchors") == [80, 128, 256, 512] and
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
    need(selection.get("candidate_count") == 51 and
         selection.get("selected_origins") == [413342, 410258, 416940] and
         selection.get("selection_beta") == 2 and
         selection.get("pilot_count") == 256 and
         selection.get("minimum_separation") == 2048, "selection")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 384 and
         audit.get("settings_per_beta") == 48 and
         audit.get("beta_count") == 2 and
         audit.get("spectral_rows") == 384 and
         audit.get("beta2_holdout_rows") == 192 and
         audit.get("beta2_holdout_cap_violations") == 0 and
         audit.get("baseline_beta0_cap_violations") == 30 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 384 and
         len({(row.get("origin"), row.get("count"), row.get("Q"),
               row.get("kernel_exponent"), row.get("beta"), row.get("law"))
              for row in rows}) == 384, "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap_repair_betas") == [2] and
         phase.get("by_beta", {}).get("0", {}).get(
             "spectral_cap_violations") == 30 and
         phase.get("by_beta", {}).get("2", {}).get(
             "spectral_cap_violations") == 0, "phase census")
    expected_firewall = {
        "TPC365_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_RESPONSE_BLIND",
        "TPC365_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC365_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_384_ROWS",
        "TPC365_BETA2_HOLDOUT": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC365_BETA2_CAP_TRANSFER": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC365_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC365_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC365_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC365_SOURCE_UNIFORM_L2": "OPEN",
        "TPC365_ARITHMETIC_ADVANCE": "NO",
        "TPC365_FIXED_POWER_CREDIT": 0,
        "TPC365_FULL_GATE_B": "OPEN", "TPC365_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected_firewall.items():
        need(payload.get("claim_firewall", {}).get(key) == value,
             "firewall " + key)
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC365_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_384_ROWS",
            "TPC365_BETA2_CAP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC365_ARITHMETIC_ADVANCE = NO",
            "TPC365_FULL_GATE_B = OPEN"):
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
        print("TPC365_BRIDGE_CHECK=PASS rows=384 beta2_holdout=192 "
              "beta2_violations=0 baseline_beta0_violations=30")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC365_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
