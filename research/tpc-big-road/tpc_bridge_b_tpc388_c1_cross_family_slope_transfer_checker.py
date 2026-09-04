#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-388."""

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
PROJECT = ROOT / "papers/tpc-388-c1-cross-family-slope-transfer"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc388_c1_cross_family_slope_transfer.md"
PRODUCER = PROJECT / "code/tpc388_c1_cross_family_slope_transfer.py"
INDEPENDENT = PROJECT / "experiments/tpc388_independent_checker.py"
STRESS = PROJECT / "experiments/tpc388_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc388_certificate.json"
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

# Filled after all TPC-388 artifacts were finalized.
LOCKS = {
    "producer": "ee659c08d3af5d0ddd300ca89fa5cf7f4c7c9f7630d00577e943716966b6e411",
    "independent": "71fe8323d03fc9118829297870b3cb5bbec30998d6646f6374385022d684bda9",
    "stress": "942be396b300f89c16ba01cef0aae7a3fe87e88840f765f2a3e2bb67f28d7c03",
    "certificate": "6808eb81b5f18c1add88685f82f1df61681abc4e9e61e432067eb88d7d5b67b1",
    "main_tex": "96cf920c4e48f77910a929cc2ed5d367f3807993222d14e076cb320d63838ce6",
    "main_pdf": "3b0f703edf38c6efa4064a2273a4b4fd0b6e171f1ed4b285f63e089179152550",
    "pdf": "3b0f703edf38c6efa4064a2273a4b4fd0b6e171f1ed4b285f63e089179152550",
    "log": "744d3ad0ca96a96b1097f8f2daa0a875bb5e13c4fce3645d322b988bb5caa9af",
    "readme": "d5beca5f3618a37bf1f36f2858039c9f166f8a304a81081ede6769a1e2e88d3e",
    "plan": "581075e8f16c5b3024706efc3208e404342ef6860ebb6ff8017a45a2797eccc3",
    "derivation": "36bc87acf94543a7a9d9980f78c15fdf7839d4304da4897c24d672bbf32c29e6",
    "proof": "42ca572a45bd4c0bff18db3cc7052ccfa26e26b1a8bb4a2e6ebaa42dd65e8ac2",
    "claim": "8567e49bd09f0c3ba1da3d14d448f210bcfff98817ad8a8615d8ac059b30e248",
    "route": "c595958383fbdfa9a9acbb80c5ee696f876cb350f607e7d82f2bf8b06283ea7c",
    "protocol": "fcb65368e6c441a6ba2824e377bf953794f04c1f48434d33d5ace730a1a21cf9",
    "theorem": "0d0b0723c7a1db3b9be16e9991268b85a92c3ad3ed7efbb0deb258b9405142da",
    "bridge": "fd801b534f387e35b5e0c0c8aa2c96909ca582c2c2241abe1de39f6be106e149",
}

SCHEMA = "TPC388_C1_CROSS_FAMILY_SLOPE_TRANSFER_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_CROSS_FAMILY_SLOPE_TRANSFER"


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
         "TPC387_C1_COUNT_LADDER_RENORMALIZATION_V1" and
         parent.get("parent_certificate_sha256") ==
         "337aa65feedd4c729cd34c7d6de8865baeb96c4888ab44fbdf00f840d079e344" and
         parent.get("parent_slopes_frozen") is True and
         parent.get("parent_slopes_refit_on_current_family") is False,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") ==
         [2600001, 2604011, 2608021, 2612031, 2616041] and
         selection.get("calibration_origins") == [2600001, 2604011, 2608021] and
         selection.get("holdout_origins") == [2612031, 2616041] and
         selection.get("calibration_counts") == [512, 768] and
         selection.get("holdout_count") == 1024 and
         selection.get("response_used_for_selection") is False and
         selection.get("parent_slope_refit") is False and
         selection.get("holdout_role_fixed_before_readout") is True,
         "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 256, "row census")
    summary = payload.get("transfer_summary", {})
    need(summary.get("row_count") == 256 and summary.get("cell_count") == 32 and
         summary.get("parent_transfer_pass_count") == 32 and
         summary.get("local_control_pass_count") == 32 and
         summary.get("parent_transfer_max_abs_error") ==
         "0.023402666610706224" and
         summary.get("local_control_max_abs_error") ==
         "0.02447192072430493" and
         summary.get("stable_cells", {}).get("1024_holdout") == 28 and
         isinstance(summary.get("cells"), list) and len(summary["cells"]) == 32,
         "transfer summary")
    failures = summary.get("failure_counts_by_mode_normalization", {})
    need(sum(int(v.get("spectral", -1)) for v in failures.values()) == 40 and
         sum(int(v.get("schur", -1)) for v in failures.values()) == 0,
         "failure census")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC388_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC388_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC388_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC388_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    need(payload.get("round2_clue") == "TEST_C1_CROSS_FAMILY_SLOPE_STRESS",
         "round2 clue")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "CROSS_FAMILY_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS",
            "PARENT_SLOPE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "PARENT_TRANSFER_PASS = 32/32",
            "ARITHMETIC_ADVANCE = NO",
            "ROUND2_CLUE = TEST_C1_CROSS_FAMILY_SLOPE_STRESS"):
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
             b"TPC388_CERTIFICATE=PASS rows=256 cells=32 parent_pass=32/32 "
             b"local_pass=32/32 spectral_failures=40 stable_holdout=28/32\n",
             "producer output")
        need(outputs[1] ==
             b"TPC388_INDEPENDENT_CHECK=PASS rows=256 cells=32 parent_pass=32/32 "
             b"local_pass=32/32 spectral_failures=40 stable_holdout=28/32\n",
             "independent output")
        need(outputs[2] == b"TPC388_STRESS=PASS mutations=25\n",
             "stress output")
        print("TPC388_BRIDGE_CHECK=PASS rows=256 cells=32 parent_pass=32/32 "
              "local_pass=32/32 spectral_failures=40 stable_holdout=28/32")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC388_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
