#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-389."""

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
PROJECT = ROOT / "papers/tpc-389-c1-long-horizon-slope-stress"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc389_c1_long_horizon_slope_stress.md"
PRODUCER = PROJECT / "code/tpc389_long_horizon_slope_stress.py"
INDEPENDENT = PROJECT / "experiments/tpc389_independent_checker.py"
STRESS = PROJECT / "experiments/tpc389_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc389_certificate.json"
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

# Filled after all TPC-389 artifacts were finalized.
LOCKS = {
    "producer": "b914b8a3b4896e40b907e10f5a6dd8c0fef0d2680abf9fd7fa0b43fe890c576b",
    "independent": "c44aa44411fe1561bd792f11a2a47fef2ac06dabc049e64d1c7e3666cbf6b283",
    "stress": "515f0453b6671f20981970e26040be249b1c74f684cbcd187d91dfbf47ccbb85",
    "certificate": "776f98611560907fe3d2822e545875aa32b74d7880872f6e3ee1919ec85e7390",
    "main_tex": "06fa793730e8cb345de96745ac8f0f51bfd726f1db13eae61cde4410164ddaeb",
    "main_pdf": "98f031432ccf7844d5f19512c312d9d659b8d6d12a698a06469614730ac9a341",
    "pdf": "98f031432ccf7844d5f19512c312d9d659b8d6d12a698a06469614730ac9a341",
    "log": "9699147829da919398f9e036cebfdb44b6426adb826dc0958497392bf411601c",
    "readme": "8fc6ae2708753b43cc6cc2b98f4d679bd8dac5ec1fa7b88122fb2af9f08005a4",
    "plan": "d13311fdb3e3bd8aaabc979735ae914bbdc309442c46caec67690129bc303c4a",
    "derivation": "ed14cc19dea3a3499dd6027f9bc19114deda1fe909408ec77443d1577ac0dd41",
    "proof": "18f6b8245b07b3b327ae3c7b849c27afc5f1e5d7f477c854f171b42da072fb69",
    "claim": "efbfde151c35ec9d92e5840aa04ad3a02b160e4ee0f6f5661fa6e8465983b3b5",
    "route": "28eeabcaae8ee5993c9daa0d328a8a6c37749b8295cddc7d6c4ac5c6e4d45562",
    "protocol": "bc1a850c8bf11ef26f390cb8d3446b6563e6fae27cad2b847113d3a8cae01225",
    "theorem": "83ae5645d36977d9c716279b5fdac5f04bd51d5f3d7e13ad4d8aa05a6fffb258",
    "bridge": "dceb57441e14c572d36428b91bab61c73e7878fec11b1d19dd9664a657ffca67",
}

SCHEMA = "TPC389_C1_LONG_HORIZON_SLOPE_STRESS_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_LONG_HORIZON_SLOPE_STRESS"


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
         "TPC388_C1_CROSS_FAMILY_SLOPE_TRANSFER_V1" and
         parent.get("parent_certificate_sha256") ==
         "6808eb81b5f18c1add88685f82f1df61681abc4e9e61e432067eb88d7d5b67b1" and
         parent.get("parent_slopes_frozen") is True and
         parent.get("parent_slopes_refit_on_current_family") is False,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") ==
         [2800001, 2804011, 2808021, 2812031, 2816041] and
         selection.get("calibration_origins") == [2800001, 2804011, 2808021] and
         selection.get("holdout_origins") == [2812031, 2816041] and
         selection.get("calibration_counts") == [768, 1024] and
         selection.get("holdout_count") == 1280 and
         selection.get("response_used_for_selection") is False and
         selection.get("parent_slope_refit") is False and
         selection.get("holdout_role_fixed_before_readout") is True,
         "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 256, "row census")
    summary = payload.get("transfer_summary", {})
    need(summary.get("row_count") == 256 and summary.get("cell_count") == 32 and
         summary.get("parent_horizon_pass_count") == 32 and
         summary.get("local_control_pass_count") == 32 and
         summary.get("recursive_parent_pass_count") == 32 and
         summary.get("parent_horizon_max_abs_error") ==
         "0.017615584096739245" and
         summary.get("local_control_max_abs_error") ==
         "0.011997515978539264" and
         summary.get("recursive_parent_max_abs_error") ==
         "0.029949940590637381" and
         summary.get("stable_cells", {}).get("1280_holdout") == 24 and
         isinstance(summary.get("cells"), list) and len(summary["cells"]) == 32,
         "transfer summary")
    failures = summary.get("failure_counts_by_mode_normalization", {})
    need(sum(int(v.get("spectral", -1)) for v in failures.values()) == 64 and
         sum(int(v.get("schur", -1)) for v in failures.values()) == 0,
         "failure census")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC389_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC389_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC389_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC389_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    need(payload.get("round2_clue") == "TEST_C1_RECURSIVE_SLOPE_COMPOSITION",
         "round2 clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "LONG_HORIZON_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS",
            "PARENT_HORIZON_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "PARENT_HORIZON_PASS = 32/32",
            "ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_RECURSIVE_SLOPE_COMPOSITION"):
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
        need(outputs[0] ==
             b"TPC389_CERTIFICATE=PASS rows=256 cells=32 parent_pass=32/32 "
             b"local_pass=32/32 recursive_parent_pass=32/32 spectral_failures=64 stable_holdout=24/32\n",
             "producer output")
        need(outputs[1] ==
             b"TPC389_INDEPENDENT_CHECK=PASS rows=256 cells=32 parent_pass=32/32 "
             b"local_pass=32/32 recursive_parent_pass=32/32 spectral_failures=64 stable_holdout=24/32\n",
             "independent output")
        need(outputs[2] == b"TPC389_STRESS=PASS mutations=25\n",
             "stress output")
        print("TPC389_BRIDGE_CHECK=PASS rows=256 cells=32 parent_pass=32/32 "
              "local_pass=32/32 recursive_parent_pass=32/32 spectral_failures=64 stable_holdout=24/32")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC389_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
