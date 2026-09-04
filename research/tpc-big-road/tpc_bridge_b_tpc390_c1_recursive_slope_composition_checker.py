#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-390."""

from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-390-c1-recursive-slope-composition"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc390_c1_recursive_slope_composition.md"
PRODUCER = PROJECT / "code/tpc390_recursive_slope_composition.py"
INDEPENDENT = PROJECT / "experiments/tpc390_independent_checker.py"
STRESS = PROJECT / "experiments/tpc390_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc390_certificate.json"
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

# Filled after all TPC-390 artifacts are finalized.
LOCKS = {
    "producer": "ec9cc88a9b05a7561fc0f8fee41352c6639d3990ae593e1affc91a079ad7e144",
    "independent": "4fc111625dee47f2a1c33eac265105c15441a551b6a6d2ea92bcb52647b62ec4",
    "stress": "2449e80344e7f716fb74f357f3ae8d8cb5f461af6dba72779b8e85c8eace74cd",
    "certificate": "870c92db4c697a1a822554256019657e1c3c27ab78f9e76a41b4ade5911d34d0",
    "main_tex": "af5d2d7b75a2c66234d03413807d25b6464794cd0213059f1f6c5d696705861a",
    "main_pdf": "9d75ac7b77c5395ca8d5b83ecc87a531570940879df65c58abf2c8970e92892f",
    "pdf": "9d75ac7b77c5395ca8d5b83ecc87a531570940879df65c58abf2c8970e92892f",
    "log": "9f801490c75b1d29c2b2d2a0be540e12f5ece0910d47840d2ac58b5eafe6a43d",
    "readme": "6fa359ddd37a52399380991bfffc4d0ce0104f4c6912623c8206aaf6694759f2",
    "plan": "55149bcb2c8c46d19f105cbde20a8502483558997769787c350dd659561c641e",
    "derivation": "ea6a1246e5478d4addce1332d722c6e4f5ebbf0cc0e17d9329982a29d0fe3d5e",
    "proof": "71b392687e80ec2ce9c4c9aa62ee390b9bdb09db5bd215bde373935245c7b14f",
    "claim": "ff3a7fe6de871c434816e6ea1b921442c0ca3ef0eb66439f52f95a46e06ef950",
    "route": "6ea38d0931f921f964f6fd44c2a6253fe44153fd6ac9225f9a5dd288e9cb49db",
    "protocol": "3fb4ed4bc959ac23420f70921121f791f8e66b1de028d6887105c550f8bea30d",
    "theorem": "95ae1c6064cda9abad48664c1669a1b1aa148d71b12fb1bdf369e8875243b380",
    "bridge": "991ffcaa58b9b613ee4bd5715d801babafa7853fec0cfc1f749401965d1d9b0d",
}

SCHEMA = "TPC390_C1_RECURSIVE_SLOPE_COMPOSITION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_RECURSIVE_SLOPE_COMPOSITION_AUDIT"
EXPECTED_PRODUCER_OUTPUT = (
    b"TPC390_CERTIFICATE=PASS rows=256 cells=32 parent_pass=30/32 "
    b"local_pass=32/32 recursive_parent_pass=23/32 spectral_failures=64 "
    b"stable_holdout=26/32 composition_max=3.3306690738754696e-16\n")
EXPECTED_INDEPENDENT_OUTPUT = (
    b"TPC390_INDEPENDENT_CHECK=PASS rows=256 cells=32 parent_pass=30/32 "
    b"local_pass=32/32 recursive_parent_pass=23/32 spectral_failures=64 "
    b"stable_holdout=26/32 composition_max=3.3306690738754696e-16\n")
BRIDGE_PASS_OUTPUT = (
    "TPC390_BRIDGE_CHECK=PASS rows=256 cells=32 parent_pass=30/32 "
    "local_pass=32/32 recursive_parent_pass=23/32 spectral_failures=64 "
    "stable_holdout=26/32 composition_max=3.3306690738754696e-16")


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def finite_tree(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and finite_tree(v)
                   for k, v in value.items())
    if isinstance(value, list):
        return all(finite_tree(v) for v in value)
    return True


def lock(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED" and path.is_file() and
         digest(path.read_bytes()) == expected, label + " provenance")


def parse_no_duplicates(raw: bytes) -> dict[str, Any]:
    def hook(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise Failure("duplicate JSON key")
            out[key] = value
        return out
    value = json.loads(raw, object_pairs_hook=hook)
    need(isinstance(value, dict), "certificate object")
    return value


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = parse_no_duplicates(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and finite_tree(payload) and
         payload.get("schema") == SCHEMA and payload.get("status") == STATUS,
         "payload header")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    parent = payload.get("parent_lock", {})
    need(parent.get("parent_schema") ==
         "TPC389_C1_LONG_HORIZON_SLOPE_STRESS_V1" and
         parent.get("parent_certificate_sha256") ==
         "776f98611560907fe3d2822e545875aa32b74d7880872f6e3ee1919ec85e7390" and
         parent.get("parent_slopes_frozen") is True and
         parent.get("parent_slopes_refit_on_current_family") is False,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") ==
         [3000001, 3004011, 3008021, 3012031, 3016041] and
         selection.get("calibration_origins") == [3000001, 3004011, 3008021] and
         selection.get("holdout_origins") == [3012031, 3016041] and
         selection.get("calibration_counts") == [1024, 1280] and
         selection.get("holdout_count") == 1536 and
         selection.get("response_used_for_selection") is False and
         selection.get("parent_slope_refit") is False and
         selection.get("holdout_role_fixed_before_readout") is True,
         "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 256, "row census")
    summary = payload.get("transfer_summary", {})
    need(summary.get("row_count") == 256 and summary.get("cell_count") == 32 and
         summary.get("parent_horizon_pass_count") == 30 and
         summary.get("local_control_pass_count") == 32 and
         summary.get("recursive_parent_pass_count") == 23 and
         summary.get("parent_horizon_max_abs_error") ==
         "0.03633754623843255" and
         summary.get("local_control_max_abs_error") ==
         "0.025804438647033412" and
         summary.get("recursive_parent_max_abs_error") ==
         "0.049074165168337847" and
         summary.get("recursive_composition_max_abs_error") ==
         "3.3306690738754696e-16" and
         summary.get("stable_cells", {}).get("1536_holdout") == 26 and
         isinstance(summary.get("cells"), list) and len(summary["cells"]) == 32,
         "transfer summary")
    failures = summary.get("failure_counts_by_mode_normalization", {})
    need(sum(int(v.get("spectral", -1)) for v in failures.values()) == 64 and
         sum(int(v.get("schur", -1)) for v in failures.values()) == 0,
         "failure census")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC390_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC390_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC390_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC390_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    need(payload.get("round2_clue") == "LOCALIZE_C1_RECURSIVE_HORIZON_OBSTRUCTION",
         "round2 clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "RECURSIVE_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS",
            "PARENT_ONE_STEP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = LOCALIZE_C1_RECURSIVE_HORIZON_OBSTRUCTION"):
        need(bridge_text.count(marker) == 1, "bridge marker")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull ", "Underfull ",
                "LaTeX Error", "Fatal error", "Citation", "Empty"):
        need(bad not in log, "LaTeX diagnostic " + bad)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and len(PDF.read_bytes()) > 100000,
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
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        paths = {"producer": PRODUCER, "independent": INDEPENDENT,
                 "stress": STRESS, "certificate": CERTIFICATE,
                 "main_tex": MAIN_TEX, "main_pdf": MAIN_PDF, "pdf": PDF,
                 "log": LOG, "readme": README, "plan": PLAN,
                 "derivation": DERIVATION, "proof": PROOF, "claim": CLAIM,
                 "route": ROUTE, "protocol": PROTOCOL, "theorem": THEOREM,
                 "bridge": BRIDGE}
        for key, path in paths.items():
            lock(path, LOCKS[key], key)
        check_certificate()
        jobs = tuple((script, False) for script in (PRODUCER, INDEPENDENT, STRESS)) + \
               tuple((script, True) for script in (PRODUCER, INDEPENDENT, STRESS))
        with ThreadPoolExecutor(max_workers=6) as pool:
            outputs = tuple(pool.map(lambda job: run(*job), jobs))
        need(outputs[:3] == outputs[3:], "normal/optimized mismatch")
        need(outputs[0] == EXPECTED_PRODUCER_OUTPUT,
             "producer output")
        need(outputs[1] == EXPECTED_INDEPENDENT_OUTPUT,
             "independent output")
        need(outputs[2] == b"TPC390_STRESS=PASS mutations=25\n",
             "stress output")
        print(BRIDGE_PASS_OUTPUT)
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC390_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
