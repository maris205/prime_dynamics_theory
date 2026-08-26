#!/usr/bin/env python3
"""Fail-closed release checker for TPC-261."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-261-strict-endpoint-budget-compiler"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_strict_endpoint_budget_compiler.md"
PRODUCER = PROJECT / "code/tpc261_endpoint_budget_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc261_independent_checker.py"
STRESS = PROJECT / "experiments/tpc261_budget_stress.py"
CERTIFICATE = PROJECT / "results/tpc261_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "7837a9186f489684152645ab6c89bf78560250c5"
STATUS = "PROVED_STRUCTURAL_ENDPOINT_BUDGET_OBSTRUCTION_FOR_LITERAL_V59_REASSEMBLY"
BRIDGE_SHA256 = "31081a1a0f92cce5c7b7175b27d9d3e250f3fd505002093719b8bb4ea8becb47"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "bb320d9bc39933193f5a15f89e285678fef029818d958f7d506401a5e5550af1",
    "papers/tpc-260-four-packet-residual-reassembly/README.md":
        "f45e54e26672327578535e88d948e5559d1e7c6517cfe7a3cefcd29f19630949",
    "papers/tpc-260-four-packet-residual-reassembly/PROOF_PACKAGE.md":
        "e5cfb3d7b1f5b32ddc59270656ec2ff11e2d97c90c2deb68395d03aab55a03b2",
    "papers/tpc-260-four-packet-residual-reassembly/notes/theorem_ledger.md":
        "32ef275efbecb0175dbb01bfc068f654106f9ab3accb89703350ea9628aad746",
    "papers/tpc-260-four-packet-residual-reassembly/notes/route_evaluation.md":
        "2cee2e6e166c4e484bf8f88b7f9ef80ec72d893d8c829606b4353aab39f2f9dd",
    "research/tpc-big-road/bridge_b_four_packet_residual_reassembly.md":
        "01daeff6289bfa857a1f108bea785b908139f749b8233a227a00002dd239561a",
    "research/tpc-big-road/tpc_bridge_b_four_packet_residual_reassembly_checker.py":
        "74f2cc8ee0aa610f21d8e5010fcc419502c678c0ea9d01b849bc075fa24549b3",
}

# These values are filled after every project source and the final PDF are frozen.
PROJECT_HASHES = {
    ".gitignore": "b3c3b3177a5ed79072b60737ac96c92856ad4769ade6a1bf913a003db57256c9",
    "DERIVATION_PACKAGE.md": "107a484565c6fc545989ec700450d98136dba2e7b2c6105fe00c4f9bbb12bcc0",
    "PAPER_PLAN.md": "93ef7f2e49693991df9cec4db47bc5fc0f3be46b3974eec34b72e332ed5bd656",
    "PROOF_PACKAGE.md": "0bcecbebfb00609cb1f9a429f715e5ab493811225b8c2b4f337e48d571599dd8",
    "README.md": "a3a3f1c33b48eaab75e503657290421b2d092c640c3a95bc0713bd7f6ba6b977",
    "code/tpc261_endpoint_budget_certificate.py": "9c18f3dbb3b21d506447b500869090bcd250c7d24348b21e75d4e8c0916cf2c9",
    "experiments/tpc261_budget_stress.py": "7fc681994b012b9f4f8b9cadfc6b3bba71a1856fe6d3805cb7de1e005e5601b5",
    "experiments/tpc261_independent_checker.py": "b0dd0c4b38c389ce9783b75c89a34c51d2bdbff86948d9d00807412a044a7b3b",
    "notes/citation_verification.md": "3b342fe7868acb8e9cfb22dfe592f8df53fb435fc2081d78866bb0372d729353",
    "notes/claim_firewall.md": "84718775d109818a594b87431d76475c33e00a55e5a731da67cd41ab3481b5b4",
    "notes/computational_protocol.md": "c160c64240541d9fe4c3ebcb8ac1d4b41e2b63ff4cd290e10054252d71f2496b",
    "notes/route_evaluation.md": "7860c4a756ccf4002c7ed8d0fe14b346d439f9aa5244f462255f23677a7d51ee",
    "notes/theorem_ledger.md": "731928d3fddbc3014e52e0fec887fe6980787577b4945f2d5fc95d3116214ce8",
    "paper/main.pdf": "b8c63dca6541b3c050a35a027655885a9068ab2a93558846df37db8278627702",
    "paper/main.tex": "d1b1b2c273a36631d8df9adbf740bd64a58e0fd016e9ef4fdb720deb988f6b19",
    "paper/paper.pdf": "b8c63dca6541b3c050a35a027655885a9068ab2a93558846df37db8278627702",
    "paper/references.bib": "dffb80e41f3b89a9cff625d5e56dba091570d9f4734992c1a3c2aa2330f709a2",
    "results/tpc261_certificate.json": "1ceba5ad05e9670bbb62242ed090349d3afb9fe2b789284a4fc9c38323f0c6e3",
}

EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/main.aux", "paper/main.bbl", "paper/main.blg",
    "paper/main.log", "paper/main.out",
}

MARKERS = (
    "TPC261_MAXIMUM_CLAIM = " + STATUS,
    "TPC261_ROUTE_ADVANCE = YES_SCOPED_ENDPOINT_BUDGET_COMPILER",
    "TPC261_BUDGET_IDENTITY = PROVED_EXACT",
    "TPC261_STRICT_THRESHOLD = PROVED_EXACT_ONE_OVER_400",
    "TPC261_BORDERLINE_EQUALITY = PROVED_EXACT_POWER_LEVEL_ONLY",
    "TPC261_LOG_ONLY_TO_POWER_PROMOTION = REFUTED_SCOPED",
    "TPC261_SCALED_NULL_COMPATIBLE_WITNESS = PROVED_STRUCTURAL_SYNTHETIC",
    "TPC261_GLOBAL_FIXED_POWER_CREDIT = NONE",
    "TPC261_LITERAL_MODE_ZERO_ESTIMATE = OPEN",
    "TPC261_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE",
    "TPC261_ARITHMETIC_ADVANCE = NO",
    "TPC261_FIXED_ATOM_CREDIT = 0",
    "TPC261_L2 = NONE",
    "TPC261_FULL_GATE_B = OPEN",
    "TPC261_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC261_TWIN_PRIME_RESULT = NONE",
    "TPC261_STATUS = " + STATUS,
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_digest(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return digest(data)


def baseline_bytes(relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", BASELINE_HEAD + ":" + relative], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0 and result.stderr == b"",
         "baseline source: " + relative)
    return result.stdout


def check_sources() -> None:
    for relative, expected in SOURCE_HASHES.items():
        need(digest(baseline_bytes(relative)) == expected,
             "source hash: " + relative)


def check_project() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
              if path.is_file() and "__pycache__" not in path.parts}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    for relative, expected in PROJECT_HASHES.items():
        need(expected != "PLACEHOLDER", "project hash placeholder: " + relative)
        need(normalized_digest(PROJECT / relative) == expected,
             "project hash: " + relative)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")


def check_bridge() -> None:
    need(BRIDGE_SHA256 != "PLACEHOLDER_BRIDGE_HASH", "bridge hash placeholder")
    need(normalized_digest(BRIDGE) == BRIDGE_SHA256, "bridge hash")
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in MARKERS:
        need(marker in text, "bridge marker: " + marker)
    need("ROUND2_CLUE = PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE" in text,
         "round-two clue")
    need("TPC261_GLOBAL_FIXED_POWER_CREDIT = NONE" in text, "credit firewall")


def run_child(path: Path, marker: str) -> str:
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    need(result.returncode == 0 and result.stderr == "", "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    producer = run_child(PRODUCER, "TPC261_CERTIFICATE=PASS")
    independent = run_child(INDEPENDENT, "TPC261_INDEPENDENT_CHECK=PASS")
    stress = run_child(STRESS, "TPC261_STRESS=PASS")
    need("strict_threshold=1/400" in producer, "producer threshold")
    need("producer_imported=NO" in independent, "independent isolation")
    need("log_power_credit=NONE" in stress, "stress firewall")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, sort_keys=True, separators=(",", ":")) +
                 "\n").encode("ascii")
    need(raw == canonical, "certificate canonical")
    need(parsed.get("schema") == "TPC261_CERTIFICATE_V1", "certificate schema")
    need(parsed.get("claim") == STATUS, "certificate claim")
    need(parsed.get("baseline", {}).get("head") == BASELINE_HEAD,
         "certificate baseline")
    budget = parsed.get("budget_audit", {})
    need(budget.get("baseline_exponent") == "5/3" and
         budget.get("target_exponent") == "1997/1200" and
         budget.get("required_strict_saving") == "1/400",
         "budget constants")
    lanes = budget.get("lanes", [])
    need(len(lanes) == 5, "lane count")
    need(lanes[0].get("effective") == "11/1200" and
         lanes[0].get("margin_over_required") == "1/150" and
         lanes[0].get("classification") == "STRICT", "strict lane")
    need(lanes[1].get("classification") == "BORDERLINE", "borderline lane")
    need(lanes[2].get("effective") == "1/600" and
         lanes[2].get("classification") == "INSUFFICIENT", "loss lane")
    need(lanes[3].get("scope") == "LOCAL_ONLY", "local scope")
    need(lanes[4].get("classification") == "NO_FIXED_POWER", "log lane")
    witness = parsed.get("scaled_witness", {})
    need(witness.get("plus_energy_coefficient") == "16" and
         witness.get("alternating_energy_coefficient") == "0" and
         witness.get("same_null_projection") is True and
         witness.get("synthetic") is True, "scaled witness")
    firewall = parsed.get("firewall", {})
    need(firewall.get("TPC261_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC261_GLOBAL_FIXED_POWER_CREDIT") == "NONE" and
         firewall.get("TPC261_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC261_L2") == "NONE" and
         firewall.get("TPC261_TWIN_PRIME_RESULT") == "NONE",
         "certificate firewall")


def check_pdf() -> None:
    for name in ("pdftotext", "pdffonts", "pdfinfo"):
        need(shutil.which(name) is not None, "PDF tool: " + name)
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Endpoint-Budget Compiler", "Liang Wang", "strict saving",
                   "mode-zero", "residual", "References", "1/400"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    info_text = info.stdout.decode("ascii", errors="replace")
    need(info.returncode == 0 and
         re.search(r"(?m)^Pages:\s+5\s*$", info_text) is not None,
         "PDF pages")
    fonts = subprocess.run(["pdffonts", str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = [row for row in fonts.stdout.decode("ascii").splitlines()[2:]
            if row.strip()]
    need(len(rows) == 18, "PDF font count")
    for row in rows:
        columns = row.split()
        need(len(columns) >= 8 and columns[-5:-2] == ["yes", "yes", "yes"],
             "PDF font embedding")
    if LOG.is_file():
        log_text = LOG.read_text(encoding="utf-8", errors="replace")
        bad = re.search(
            r"(?m)^(?:LaTeX Warning:|Package .* Warning:|Overfull \\\\|"
            r"Underfull \\\\|There were undefined references)",
            log_text,
        )
        need(bad is None, "LaTeX log: " + (bad.group(0) if bad else "unknown"))


def check_source_hygiene() -> None:
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"),
             "unsafe assertion syntax: " + path.name)
    independent_text = INDEPENDENT.read_text(encoding="utf-8")
    need("tpc261_endpoint_budget_certificate" not in independent_text,
         "producer import")


def main() -> int:
    try:
        check_sources()
        check_project()
        check_bridge()
        check_source_hygiene()
        check_certificate()
        check_children()
        check_pdf()
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError) as exc:
        print("TPC261_BRIDGE_CHECK=FAIL: " + str(exc), file=sys.stderr)
        return 1
    print("TPC261_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("budget=PROVED_EXACT")
    print("log_firewall=REFUTED_SCOPED")
    print("scaled_witness=PROVED_STRUCTURAL_SYNTHETIC")
    print("literal_mode_zero=OPEN")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
