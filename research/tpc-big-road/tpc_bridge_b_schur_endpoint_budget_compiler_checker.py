#!/usr/bin/env python3
"""Fail-closed release checker for TPC-265."""

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
PROJECT = ROOT / "papers/tpc-265-schur-endpoint-budget-compiler"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_schur_endpoint_budget_compiler.md"
PRODUCER = PROJECT / "code/tpc265_endpoint_budget_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc265_independent_checker.py"
STRESS = PROJECT / "experiments/tpc265_budget_stress.py"
CERTIFICATE = PROJECT / "results/tpc265_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "c58404738b9943293d610f2cf87ef6fb5c01ed4e"
STATUS = "PROVED_EXACT_SCHUR_TO_ENDPOINT_BUDGET_COMPILER"
BRIDGE_SHA256 = "890dd8e6be707140b5e562713f0a63713ab28f5c63ba3510af0350a3ef636588"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "5c67ac0868e5535fb917d2fd6e8ea4d68a1b5e4e27d443d04029dbe58964b4d8",
    "papers/tpc-264-orthogonal-residual-schur-firewall/README.md":
        "9de5427069e964d4d351cdf49a78d7f3ab71b0e992e5698d49106cd1e5971b22",
    "papers/tpc-264-orthogonal-residual-schur-firewall/PROOF_PACKAGE.md":
        "f3da6e2fcf0f992e4782f10c83936f5dc8f9c88e2a3ec9b2ff16bfb94c5422fa",
    "papers/tpc-264-orthogonal-residual-schur-firewall/notes/theorem_ledger.md":
        "f4d01f5a5e759a04b046394dd7f41dd6df021ed0fd7dd388fdd79a29b1eec0bb",
    "papers/tpc-264-orthogonal-residual-schur-firewall/notes/route_evaluation.md":
        "08bdf96437fb4cd335c499eae2a1f495b89da4dbc2685e333d2f1e691221151b",
    "research/tpc-big-road/bridge_b_orthogonal_residual_schur_firewall.md":
        "d945a257c862a955d03e8931a365e57191a2099ac3bae74d858389a492d0a9fb",
    "research/tpc-big-road/tpc_bridge_b_orthogonal_residual_schur_firewall_checker.py":
        "609e8fe8f2c94c401e7a599b958d36267537c72fb20e1834de87891faed88f23",
}

PROJECT_HASHES = {
    ".gitignore": "f3c9a03240b1b7cdea120c494e482533729564039d037516225371f5aba8214c",
    "DERIVATION_PACKAGE.md": "58a354bfff98d5a199bdeef81ea000ed73c255ea66e4ef6884a65c091bd5bac1",
    "PAPER_PLAN.md": "d6236e7ed67f9e16d3479e7b8985a3ebe709d1e03aca7b3971a282b006b3a67a",
    "PROOF_PACKAGE.md": "de683a97b1d099778ee08f72fa1e12ea6a28bef418e04bf1f99c915412ba38f3",
    "README.md": "bb114657476ca2d10f34b9c5c96e93804d676a20b9e7ad1770df16d60719eedd",
    "code/tpc265_endpoint_budget_certificate.py": "5e64056d432482a45083e994a566f0915539f7807946220ad392bafbd284dfc2",
    "experiments/tpc265_independent_checker.py": "ab5b305ea0909818cd51c9e5f34799ccacf1d18d77168352c06dee24512f578f",
    "experiments/tpc265_budget_stress.py": "82ccb18c3246087e3adc661ef8646d451b8cbfeec6f38c5ad7cc7473e2e95957",
    "notes/citation_verification.md": "e0ecedb6e19b0d575b20053b98d127574ff960c456dbc7eb83b3e0e45438ad4a",
    "notes/claim_firewall.md": "e73a5837aeb815708acddfdffe0e5957a4a22aab3c5201d1f4cb2c1855394663",
    "notes/computational_protocol.md": "d28448781ce07eedd75e9d6841f9e346298f883618674d8798b87fb161f2183e",
    "notes/route_evaluation.md": "d12e0b024c30ee64876b799afe3fb98c2c2b68d86a6a09621e596709775a5239",
    "notes/theorem_ledger.md": "296e2aeb889611a129de97bef17f75bc69526b52461240081adaf1772b6301e8",
    "paper/main.pdf": "0f3677a5ae3bba29718b1b7e12de85fcfc5515af3f7ad1c531136551b7b2f74e",
    "paper/main.tex": "6c4d7b94615f2a2727d20a13e70f373fa5095940c95874df68c5747e1255c0ed",
    "paper/paper.pdf": "0f3677a5ae3bba29718b1b7e12de85fcfc5515af3f7ad1c531136551b7b2f74e",
    "paper/references.bib": "66d161c328a6a729a7efefe9b1a0dfe84e85f7a83a58f189fdfe192249c0a6ae",
    "results/tpc265_certificate.json": "e0762ca02a9af376950520d4adb7947ae6d235767a34c9942c2fee76f4d32eb8",
}
EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/main.aux", "paper/main.bbl", "paper/main.blg", "paper/main.log",
    "paper/main.out",
}

MARKERS = (
    "TPC265_MAXIMUM_CLAIM = " + STATUS,
    "TPC265_ROUTE_ADVANCE = YES_SCOPED_RESIDUAL_RADIUS_BUDGET_COMPILER",
    "TPC265_SCHUR_RADIAL_ENVELOPE = PROVED_EXACT",
    "TPC265_DISK_WORST_CASE = PROVED_EXACT",
    "TPC265_CIRCLE_WORST_CASE = PROVED_EXACT",
    "TPC265_TWO_LANE_ENDPOINT_COMPILER = PROVED_EXACT_CONDITIONAL",
    "TPC265_STRICT_PAYMENT_THRESHOLD = PROVED_EXACT_ONE_OVER_400",
    "TPC265_LOG_CENTER_CREDIT = 0",
    "TPC265_LOG_RADIUS_CREDIT = 0",
    "TPC265_ACTUAL_V59_RADIUS = OPEN",
    "TPC265_ACTUAL_V59_PHASE = OPEN",
    "TPC265_FIXED_POWER_CREDIT = 0",
    "TPC265_ARITHMETIC_ADVANCE = NO",
    "TPC265_L2 = NONE",
    "TPC265_FULL_GATE_B = OPEN",
    "TPC265_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC265_TWIN_PRIME_RESULT = NONE",
    "TPC265_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE",
    "TPC265_STATUS = " + STATUS,
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def normalized_digest(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def frozen(path: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + path],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", "frozen source: " + path)
    return result.stdout


def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(hashlib.sha256(frozen(path)).hexdigest() == expected,
             "source hash: " + path)


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
    need("ROUND2_CLUE = TEST_LITERAL_RESIDUAL_RADIUS_OR_PHASE" in text,
         "round-two clue")


def child(path: Path, marker: str, optimized: bool = False) -> str:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    need(result.returncode == 0 and result.stderr == "", "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    producer = child(PRODUCER, "TPC265_CERTIFICATE=PASS")
    independent = child(INDEPENDENT, "TPC265_INDEPENDENT_CHECK=PASS")
    independent_opt = child(INDEPENDENT, "TPC265_INDEPENDENT_CHECK=PASS", True)
    stress = child(STRESS, "TPC265_BUDGET_STRESS=PASS")
    stress_opt = child(STRESS, "TPC265_BUDGET_STRESS=PASS", True)
    need(independent == independent_opt, "independent stdout mismatch")
    need(stress == stress_opt, "stress stdout mismatch")
    need("radial_envelope=EXACT" in producer and
         "strict_threshold=1/400" in producer, "producer fields")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, sort_keys=True, separators=(",", ":")) +
                 "\n").encode("ascii")
    need(raw == canonical, "certificate canonical")
    need(parsed.get("schema") == "TPC265_SCHUR_ENDPOINT_BUDGET_CERTIFICATE_V1",
         "certificate schema")
    need(parsed.get("claim") == STATUS, "certificate claim")
    need(parsed.get("baseline", {}).get("head") == BASELINE_HEAD and
         parsed.get("baseline", {}).get("source_count") == 8,
         "certificate baseline")
    radial = parsed.get("radial_audit", {})
    need(radial.get("disk_supremum") == "5" and
         radial.get("disk_infimum") == "0" and
         radial.get("circle_supremum") == "5" and
         radial.get("circle_infimum") == "1" and
         radial.get("minkowski_radius") == "6",
         "radial audit")
    budget = parsed.get("budget_audit", {})
    need(budget.get("baseline_exponent") == "5/3" and
         budget.get("target_exponent") == "1997/1200" and
         budget.get("required_strict_saving") == "1/400" and
         len(budget.get("lanes", [])) == 4,
         "budget audit")
    firewall = parsed.get("firewall", {})
    need(firewall.get("TPC265_LOG_CENTER_CREDIT") == 0 and
         firewall.get("TPC265_LOG_RADIUS_CREDIT") == 0 and
         firewall.get("TPC265_ACTUAL_V59_RADIUS") == "OPEN" and
         firewall.get("TPC265_ACTUAL_V59_PHASE") == "OPEN" and
         firewall.get("TPC265_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC265_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC265_L2") == "NONE" and
         firewall.get("TPC265_TWIN_PRIME_RESULT") == "NONE",
         "firewall")


def check_pdf() -> None:
    for name in ("pdftotext", "pdffonts", "pdfinfo"):
        need(shutil.which(name) is not None, "PDF tool: " + name)
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Schur Radius to Endpoint-Budget Compiler", "Liang Wang",
                   "radial envelope", "fixed-power", "1/400", "References"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    info_text = info.stdout.decode("ascii", errors="replace")
    need(info.returncode == 0 and
         re.search(r"(?m)^Pages:\s+4\s*$", info_text) is not None,
         "PDF pages")
    fonts = subprocess.run(["pdffonts", str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = [row for row in fonts.stdout.decode("ascii").splitlines()[2:]
            if row.strip()]
    need(len(rows) >= 10, "PDF font count")
    for row in rows:
        columns = row.split()
        need(len(columns) >= 8 and columns[-5:-2] == ["yes", "yes", "yes"],
             "PDF font embedding")
    if LOG.is_file():
        log_text = LOG.read_text(encoding="utf-8", errors="replace")
        bad = re.search(r"(?m)^(?:LaTeX Warning:|Package .* Warning:|"
                        r"Overfull \\\\|Underfull \\\\|"
                        r"There were undefined references)", log_text)
        need(bad is None, "LaTeX log")


def check_source_hygiene() -> None:
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"),
             "unsafe assertion syntax: " + path.name)
    need("tpc265_endpoint_budget_certificate" not in
         INDEPENDENT.read_text(encoding="utf-8"), "producer import")


def main() -> int:
    try:
        check_sources()
        check_project()
        check_bridge()
        check_source_hygiene()
        check_certificate()
        check_children()
        check_pdf()
    except (Failure, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        print("TPC265_BRIDGE_CHECK=FAIL: " + str(exc), file=sys.stderr)
        return 1
    print("TPC265_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("radial_envelope=PROVED_EXACT")
    print("two_lane_compiler=PROVED_EXACT_CONDITIONAL")
    print("actual_v59_radius=OPEN")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
