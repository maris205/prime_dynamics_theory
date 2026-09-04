#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-391."""

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
PROJECT = ROOT / "papers/tpc-391-c1-recursive-horizon-localization"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc391_c1_recursive_horizon_localization.md"
PRODUCER = PROJECT / "code/tpc391_recursive_horizon_localization.py"
INDEPENDENT = PROJECT / "experiments/tpc391_independent_checker.py"
STRESS = PROJECT / "experiments/tpc391_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc391_certificate.json"
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

# Filled after all TPC-391 artifacts are finalized.
LOCKS = {
    "producer": "a9ea75fc03e5e87ef9cd64dc638d87d549d78f225d66a18093aaa6897dfb3e98",
    "independent": "9ac1148ef866248feb7fadad33e7382c7af763578701bcc654d594b4e65e60da",
    "stress": "09a5c038d244428663142cb941e6ace208cd072ed6b4520265c1dcc6e76a39dd",
    "certificate": "79727a822f1d3f98067af2b92cc89de38b06f17bfa833d28f19f908dfa54b095",
    "main_tex": "46480bc66366188408a8f9979b1023e71244fc57b26096a3403accb50df076a7",
    "main_pdf": "be856166a0334eb072d407ec12cd6f0fe7bfc9d5b324f6136b14a5487f6bba61",
    "pdf": "be856166a0334eb072d407ec12cd6f0fe7bfc9d5b324f6136b14a5487f6bba61",
    "log": "4118e9535827895f3b4b21a5131424f5789165022cb757e30e974443f3b14b88",
    "readme": "e2bda9cb030a995d09c2d6df050b53d858e7e4373104b0fb612839ee5710254c",
    "plan": "216c6fef8109d5963cc0f6df49b01e772d35c40b7286a4ff18fe6b5b20d84ac2",
    "derivation": "be88950bab5468f8de454c7715defdce5c9a829170aececb0e5e8e1019a3ebce",
    "proof": "450178a586bbf42470faf30625c600a4af1bfec5db47ca66d5833ea3a2d3411c",
    "claim": "5e94614b30d341d78edd78c30bb08bef968ae540b86411a9b12576ce6a709618",
    "route": "fbc4faed797668ef9bbb6953c0b11515ad193b6074a7daadb93beb74dde17447",
    "protocol": "4e951238182524c65923328b118e884e037565aa7bcaa34f1619160bf69e5fa1",
    "theorem": "9f132cea8b92c263b89c9763f139e7b5294ff9d32de88b4bc1e2d798cd719915",
    "bridge": "016a3f1c76ed1abca2cd7bcdbef7762f464336c618d38523df6a59e701c0fd87",
}

SCHEMA = "TPC391_C1_RECURSIVE_HORIZON_LOCALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_RECURSIVE_HORIZON_LOCALIZATION_AUDIT"
EXPECTED_PRODUCER_OUTPUT = (
    b"TPC391_CERTIFICATE=PASS rows=448 cells=32 parent_pass_1536=23/32 "
    b"local_pass_1536=32/32 recursive_pass_1536=23/32 spectral_failures=112 "
    b"stable_holdout=30/32 first_crossing_1536=9 "
    b"composition_max=4.4408920985006262e-16\n")
EXPECTED_INDEPENDENT_OUTPUT = (
    b"TPC391_INDEPENDENT_CHECK=PASS rows=448 cells=32 parent_pass_1536=23/32 "
    b"local_pass_1536=32/32 recursive_pass_1536=23/32 spectral_failures=112 "
    b"stable_holdout=30/32 first_crossing_1536=9 "
    b"composition_max=4.4408920985006262e-16\n")
BRIDGE_PASS_OUTPUT = (
    "TPC391_BRIDGE_CHECK=PASS rows=448 cells=32 parent_pass_1536=23/32 "
    "local_pass_1536=32/32 recursive_pass_1536=23/32 spectral_failures=112 "
    "stable_holdout=30/32 first_crossing_1536=9 "
    "composition_max=4.4408920985006262e-16")


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
         "TPC390_C1_RECURSIVE_SLOPE_COMPOSITION_V1" and
         parent.get("parent_certificate_sha256") ==
         "870c92db4c697a1a822554256019657e1c3c27ab78f9e76a41b4ade5911d34d0" and
         parent.get("parent_slopes_frozen") is True and
         parent.get("parent_slopes_refit_on_current_family") is False,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") ==
         [3400001, 3404011, 3408021, 3412031, 3416041] and
         selection.get("calibration_origins") == [3400001, 3404011, 3408021] and
         selection.get("holdout_origins") == [3412031, 3416041] and
         selection.get("calibration_counts") == [1024, 1152, 1280, 1408] and
         selection.get("holdout_count") == 1536 and
         selection.get("response_used_for_selection") is False and
         selection.get("parent_slope_refit") is False and
         selection.get("holdout_role_fixed_before_readout") is True,
         "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 448, "row census")
    summary = payload.get("transfer_summary", {})
    need(summary.get("row_count") == 448 and summary.get("cell_count") == 32 and
         summary.get("parent_pass_counts_by_horizon") ==
         {"1152": 32, "1280": 32, "1408": 32, "1536": 23} and
         summary.get("local_pass_counts_by_horizon") ==
         {"1152": 32, "1280": 32, "1408": 32, "1536": 32} and
         summary.get("recursive_pass_counts_by_horizon") ==
         {"1280": 32, "1408": 32, "1536": 23} and
         summary.get("recursive_composition_max_abs_error") ==
         "4.4408920985006262e-16" and
         summary.get("stable_cells", {}).get("1536_holdout") == 30 and
         isinstance(summary.get("cells"), list) and len(summary["cells"]) == 32,
         "transfer summary")
    failures = summary.get("failure_counts_by_mode_normalization", {})
    need(sum(int(v.get("spectral", -1)) for v in failures.values()) == 112 and
         sum(int(v.get("schur", -1)) for v in failures.values()) == 0,
         "failure census")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC391_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC391_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC391_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC391_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    need(payload.get("round2_clue") == "TEST_C1_NORMALIZATION_PHASE_DIAGRAM",
         "round2 clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "HORIZON_PANEL = NUMERICALLY_CERTIFIED_FINITE_448_ROWS",
            "PARENT_HORIZON_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_NORMALIZATION_PHASE_DIAGRAM"):
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
        need(outputs[2] == b"TPC391_STRESS=PASS mutations=25\n",
             "stress output")
        print(BRIDGE_PASS_OUTPUT)
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC391_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
