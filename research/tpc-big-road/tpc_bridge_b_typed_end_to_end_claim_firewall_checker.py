#!/usr/bin/env python3
"""Fail-closed release checker for TPC-266."""

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
PROJECT = ROOT / "papers/tpc-266-end-to-end-claim-firewall"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_typed_end_to_end_claim_firewall.md"
PRODUCER = PROJECT / "code/tpc266_end_to_end_claim_firewall.py"
INDEPENDENT = PROJECT / "experiments/tpc266_independent_checker.py"
STRESS = PROJECT / "experiments/tpc266_hostile_matrix.py"
CERTIFICATE = PROJECT / "results/tpc266_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "9753ec69d41efc285dcfd1f0ac32156b7bb911b5"
STATUS = "PROVED_EXACT_END_TO_END_RESIDUAL_CLAIM_FIREWALL"
BRIDGE_SHA256 = "3f0a6787e8177e17207217f69f3fb89d8b50f97d8791cdd48be8e575dacce84a"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "873448074c451830a27378661c0ec146472e789cc7b698e65f27dbfcabe6a7ca",
    "papers/tpc-265-schur-endpoint-budget-compiler/README.md":
        "bb114657476ca2d10f34b9c5c96e93804d676a20b9e7ad1770df16d60719eedd",
    "papers/tpc-265-schur-endpoint-budget-compiler/PROOF_PACKAGE.md":
        "de683a97b1d099778ee08f72fa1e12ea6a28bef418e04bf1f99c915412ba38f3",
    "papers/tpc-265-schur-endpoint-budget-compiler/notes/theorem_ledger.md":
        "296e2aeb889611a129de97bef17f75bc69526b52461240081adaf1772b6301e8",
    "papers/tpc-265-schur-endpoint-budget-compiler/notes/route_evaluation.md":
        "d12e0b024c30ee64876b799afe3fb98c2c2b68d86a6a09621e596709775a5239",
    "research/tpc-big-road/bridge_b_schur_endpoint_budget_compiler.md":
        "890dd8e6be707140b5e562713f0a63713ab28f5c63ba3510af0350a3ef636588",
    "research/tpc-big-road/tpc_bridge_b_schur_endpoint_budget_compiler_checker.py":
        "df3cd2ef0f0d2841c92c3951b70e268777d2f1e32e1845e9e9fa201e5ffb7aa6",
}

PROJECT_HASHES = {
    ".gitignore": "8f8b01c6c0e0d7c02224c6f2cf1b95a6726cf2bb6d2296dedb3c6e34630c901b",
    "DERIVATION_PACKAGE.md": "b1b548e5ed18e7456fffd3ccaa4867cbeabf9b2997fa2f96d8aa7069bf4ff128",
    "PAPER_PLAN.md": "13341b8ae48519ac8aa460fd95a96a6f3e675de7247b95f55f581f534530d8fd",
    "PROOF_PACKAGE.md": "6220d5590a963d25c6fc063a4f33b484fd68c5645cbfffe9e05c467c9df7b52c",
    "README.md": "40165bd0b8e47975ad97c14080e69180490c33258f234b4e27cc56c3f824a753",
    "code/tpc266_end_to_end_claim_firewall.py": "d4bc0d243aa926d229eed6b53d9765e8eaf0b531b877dc953b9daf822da585f6",
    "experiments/tpc266_hostile_matrix.py": "08f5396b9cae5423b27c369f8e12ff7cfa5a5158d5e11e67c42a3117e7c761c2",
    "experiments/tpc266_independent_checker.py": "7c48909ea7b88aee68bda884964b0f46feb5d5c8ccddb5e4880bf80474b271e0",
    "notes/citation_verification.md": "2fd45ec199a3c52ce7b12c0fce8a1d61150262ba49b89291d215305d90aa49cb",
    "notes/claim_firewall.md": "edcb1eeb2f7375a2fd3a31ee46a060004bb9e456a75dc1694a58f0aad9d6af01",
    "notes/computational_protocol.md": "055fae4d45e2297fe41ef71f5e3a51e8d35fa0f9e7db10ab2147173c92ca4428",
    "notes/route_evaluation.md": "3cee9e6001b92f666ed908d7fd7662d2931bc7c6b4e939e61fbc857987691646",
    "notes/theorem_ledger.md": "6f137c516d42f85792f080602fe0bfbc8e3bc077db40dea9b1844795a66ff0c1",
    "paper/main.pdf": "5562a4f1ee1df980e124916b21376b6aafd52d8f9380c145af563519e3da13a0",
    "paper/main.tex": "f0d34afefafa49ebc2184e719d62b37dded7a9916195db83a6ac42abf959c160",
    "paper/paper.pdf": "5562a4f1ee1df980e124916b21376b6aafd52d8f9380c145af563519e3da13a0",
    "paper/references.bib": "3f734086ad60e3a24d9f7905e69e99ab904ae3cc6c103cc2df9b61d353aada61",
    "results/tpc266_certificate.json": "b393b37f7fcfa584a12a81bebd88d28cac4ef9caf7951324b82d20feb264bd48",
}
EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/main.aux", "paper/main.bbl", "paper/main.blg", "paper/main.log",
    "paper/main.out",
}

MARKERS = (
    "TPC266_MAXIMUM_CLAIM = " + STATUS,
    "TPC266_ROUTE_ADVANCE = YES_SCOPED_END_TO_END_CLAIM_FIREWALL",
    "TPC266_TYPED_COMPOSITION = PROVED_EXACT",
    "TPC266_FIXED_LOG_NONPROMOTION = PROVED_EXACT",
    "TPC266_RESIDUAL_RETENTION_FIREWALL = PROVED_EXACT",
    "TPC266_FAILURE_MATRIX = PROVED_EXACT_SIX_STATE",
    "TPC266_STRICT_PAYMENT_THRESHOLD = PROVED_EXACT_ONE_OVER_400",
    "TPC266_CENTER_CURRENT_TYPE = FIXED_LOG",
    "TPC266_RESIDUAL_CURRENT_TYPE = SCHUR_SET_RADIUS_OPEN",
    "TPC266_ACTUAL_V59_RADIUS = OPEN",
    "TPC266_ACTUAL_V59_PHASE = OPEN",
    "TPC266_FIXED_POWER_CREDIT = 0",
    "TPC266_ARITHMETIC_ADVANCE = NO",
    "TPC266_L2 = NONE",
    "TPC266_FULL_GATE_B = OPEN",
    "TPC266_TWIN_PRIME_RESULT = NONE",
    "TPC266_STATUS = " + STATUS,
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
    need(result.returncode == 0 and result.stderr == b"",
         "frozen source: " + path)
    return result.stdout


def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        blob = frozen(path)
        need(hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest() == expected,
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
    need("ROUND2_CLUE = PROVE_A_LITERAL_V59_RADIUS_OR_SIGNED_PHASE_BOUND" in text,
         "round-two clue")


def child(path: Path, marker: str, optimized: bool = False) -> str:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    need(result.returncode == 0 and result.stderr == "",
         "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    producer = child(PRODUCER, "TPC266_CERTIFICATE=PASS")
    producer_opt = child(PRODUCER, "TPC266_CERTIFICATE=PASS", True)
    independent = child(INDEPENDENT, "TPC266_INDEPENDENT_CHECK=PASS")
    independent_opt = child(INDEPENDENT, "TPC266_INDEPENDENT_CHECK=PASS", True)
    stress = child(STRESS, "TPC266_HOSTILE_MATRIX=PASS")
    stress_opt = child(STRESS, "TPC266_HOSTILE_MATRIX=PASS", True)
    need(producer == producer_opt, "producer stdout mismatch")
    need(independent == independent_opt, "independent stdout mismatch")
    need(stress == stress_opt, "stress stdout mismatch")
    need("typed_composition=EXACT" in producer and
         "residual_deletion=REJECTED" in producer, "producer fields")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, sort_keys=True, separators=(",", ":")) +
                 "\n").encode("ascii")
    need(raw == canonical, "certificate canonical")
    need(parsed.get("schema") ==
         "TPC266_END_TO_END_CLAIM_FIREWALL_CERTIFICATE_V1",
         "certificate schema")
    need(parsed.get("claim") == STATUS, "certificate claim")
    need(parsed.get("baseline", {}).get("head") == BASELINE_HEAD and
         parsed.get("baseline", {}).get("source_count") == 8,
         "certificate baseline")
    thresholds = parsed.get("thresholds", {})
    need(thresholds == {
        "baseline_exponent": "5/3",
        "target_exponent": "1997/1200",
        "required_strict_saving": "1/400",
    }, "certificate thresholds")
    chain = parsed.get("chain_audit", {})
    nodes = chain.get("nodes", [])
    need([node.get("output_type") for node in nodes] == [
        "FIXED_LOG", "SCHUR_SET", "RADIAL_ENVELOPE", "BUDGET_DECISION"
    ], "certificate chain")
    endpoint = parsed.get("endpoint_audit", {})
    need(endpoint.get("disk_supremum") == "5" and
         endpoint.get("circle_supremum") == "5" and
         endpoint.get("residual_deletion_gap") == "3",
         "certificate endpoint")
    matrix = parsed.get("failure_matrix", [])
    need(len(matrix) == 6 and
         [row.get("result") for row in matrix] == [
             "CLOSED_CONDITIONAL", "OPEN_LOG_CENTER", "OPEN_RADIUS",
             "BORDERLINE", "INSUFFICIENT", "UNSOUND_RESIDUAL_DELETION"
         ], "certificate matrix")
    firewall = parsed.get("firewall", {})
    need(firewall.get("TPC266_FIXED_LOG_NONPROMOTION") == "PROVED_EXACT" and
         firewall.get("TPC266_RESIDUAL_RETENTION_FIREWALL") == "PROVED_EXACT" and
         firewall.get("TPC266_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC266_ACTUAL_V59_RADIUS") == "OPEN" and
         firewall.get("TPC266_ACTUAL_V59_PHASE") == "OPEN" and
         firewall.get("TPC266_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC266_L2") == "NONE" and
         firewall.get("TPC266_TWIN_PRIME_RESULT") == "NONE",
         "certificate firewall")


def check_pdf() -> None:
    for name in ("pdftotext", "pdffonts", "pdfinfo"):
        need(shutil.which(name) is not None, "PDF tool: " + name)
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Typed End-to-End Claim Firewall", "Liang Wang",
                   "fixed-log", "Schur", "1/400", "References"):
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
    need("tpc266_end_to_end_claim_firewall" not in
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
        print("TPC266_BRIDGE_CHECK=FAIL: " + str(exc), file=sys.stderr)
        return 1
    print("TPC266_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("typed_composition=PROVED_EXACT")
    print("failure_matrix=PROVED_EXACT_SIX_STATE")
    print("actual_v59_radius=OPEN")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
