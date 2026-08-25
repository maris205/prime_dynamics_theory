#!/usr/bin/env python3
"""Fail-closed release checker for TPC-251."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-251-literal-v59-declared-block-longitudinal-transverse-margin-compiler"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_literal_v59_declared_block_longitudinal_transverse_margin_compiler.md"
README = PROJECT / "README.md"
PROOF = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
PRODUCER = PROJECT / "code/tpc251_margin_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc251_independent_checker.py"
STRESS = PROJECT / "experiments/tpc251_margin_stress.py"
CERTIFICATE = PROJECT / "results/tpc251_certificate.json"
MAIN = PROJECT / "paper/main.tex"
PDF = PROJECT / "paper/paper.pdf"
PROTOCOL = PROJECT / "notes/computational_protocol.md"
STATUS = "PROVED_STRUCTURAL_L1_LITERAL_V59_DECLARED_BLOCK_LONGITUDINAL_TRANSVERSE_MARGIN_COMPILER"

HASHES = {
    BRIDGE: "283505a75f3038b4c4e8f3c296988afabd06fa28de0671adba55d18fbdcb445b",
    README: "9124697d17bc46d0b6eae0841c9c9eca1a005b52e4c74aa86b6eab1cfc3a4a54",
    PROOF: "7403d121b8d0860144645f0b15222f6bafdb343e99cadfb8b6dac5cdb0968bdd",
    DERIVATION: "288b4533a84f0c6a8e9449cc3488fe9c2ecfbcf34eb1bfe16d5c9f2564935d90",
    PRODUCER: "0662bf04d10944feb900e3f053ecd0dc0cf134fe89cd553d9e2a42af86eb4961",
    INDEPENDENT: "99f94871765310c85cbe0aa8fb1656f721c684ee6683723c071eafd4f5bbd960",
    STRESS: "eb95a7d19673e05cf83f239c2f6b8cf8c1ba41979580f65e49c33c73ae739035",
    CERTIFICATE: "3dba21afd43e1573ca201e0e1f5500232d29ff73ad491a26c43f437a8e32e79a",
    MAIN: "73a85534ef1f34ed52b1e18bbddb15980c0d8af9a6191aaa1d7dbc5b327177c7",
    PDF: "6a51fdc64ef8b6dbe4578c69a8f0dc07e44c9370264f71cc588f93b0c2a1d180",
    PROTOCOL: "bbfce979f17f59c817cec89d727798896f62414c0df708d14d3018560864b281",
}

EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc251_margin_certificate.py",
    "experiments/tpc251_independent_checker.py",
    "experiments/tpc251_margin_stress.py",
    "notes/citation_verification.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/source_lock.md", "notes/theorem_ledger.md", "paper/main.tex",
    "paper/paper.pdf", "paper/references.bib", "results/tpc251_certificate.json",
}

BUILD_INTERMEDIATES = {
    "paper/paper.aux", "paper/paper.bbl", "paper/paper.blg",
    "paper/paper.log", "paper/paper.out",
}

MARKERS = (
    "TPC251_LITERAL_LAMBDA_ONE_CONTRACTION = PROVED_EXACT",
    "TPC251_EXHAUSTIVE_HARD_PARTITION = PROVED_FOR_DECLARED_MODELING_CHOICE",
    "TPC251_BLOCK_FLAT_DIRECTION = PROVED_FOR_DECLARED_MODELING_CHOICE",
    "TPC251_LONGITUDINAL_TRANSVERSE_IDENTITY = PROVED_EXACT",
    "TPC251_PROJECTED_GRAM_SUBTRACTION = PROVED_EXACT",
    "TPC251_PROJECTED_COHERENCE_UPPER = PROVED_EXACT_TPC250_INHERITANCE",
    "TPC251_TRANSVERSE_RADIUS_CHAIN = PROVED_EXACT",
    "TPC251_EXTERNAL_MARGIN_COMPILER = CONDITIONAL_THEOREM_ON_CERTIFIED_E",
    "TPC251_STRICT_NONVANISHING = CONDITIONAL_THEOREM_ON_STRICT_MARGIN",
    "TPC251_EQUALITY_NONVANISHING = REFUTED_SCOPED",
    "TPC251_FIXED_SOURCE_DISK_IMAGE = NOT_CLAIMED",
    "TPC251_TPC243_EXTERNAL_ERROR = CONDITIONAL_INPUT_NOT_AUTOMATIC",
    "TPC251_ACTUAL_V59_PROJECTED_COHERENCE_ASYMPTOTIC = OPEN",
    "TPC251_PAYABLE_LONGITUDINAL_DOMINANCE = OPEN",
    "TPC251_ARITHMETIC_ADVANCE = NO",
    "TPC251_L2 = NONE",
    "TPC251_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC251_TWIN_PRIME_RESULT = NONE",
    "TPC251_STATUS = " + STATUS,
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def child(path: Path, marker: str) -> None:
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=PROJECT, capture_output=True, check=False)
    need(result.returncode == 0 and result.stderr == b"", "child: " + path.name)
    need(marker.encode("ascii") in result.stdout, "child marker: " + path.name)


def pdf_check() -> None:
    commands = [shutil.which(name) for name in ("pdftotext", "pdffonts", "pdfinfo")]
    need(all(command is not None for command in commands), "PDF tools")
    pdftotext, pdffonts, pdfinfo = commands
    text_result = subprocess.run(
        [pdftotext, "-layout", str(PDF), "-"], capture_output=True, check=False
    )
    need(text_result.returncode == 0 and text_result.stderr == b"", "PDF text")
    need(b"Declared-Block Longitudinal" in text_result.stdout and
         b"Transverse Margin Compiler" in text_result.stdout, "PDF title")
    need(b"LITERAL_V59_DECLARED_BLOCK_LONGITUDINAL_TRANSVERSE_MARGIN_COMPILER"
         in text_result.stdout, "PDF claim")
    need(b"modeling choice" in text_result.stdout and
         b"Full Gate B is open" in text_result.stdout, "PDF firewall")
    need(b"qquad" not in text_result.stdout and b"qqquad" not in text_result.stdout,
         "PDF lost backslash")
    info = subprocess.run([pdfinfo, str(PDF)], capture_output=True, check=False)
    need(info.returncode == 0 and info.stderr == b"" and
         b"Pages:           4" in info.stdout, "PDF pages")
    fonts = subprocess.run([pdffonts, str(PDF)], capture_output=True, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = fonts.stdout.decode("ascii").splitlines()[2:]
    need(len(rows) == 27, "font rows")
    for row in rows:
        columns = row.split()
        need(len(columns) >= 8 and columns[-5:-2] == ["yes", "yes", "yes"],
             "font embedding")


def run() -> None:
    actual = {
        str(path.relative_to(PROJECT))
        for path in PROJECT.rglob("*")
        if path.is_file()
    }
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    need((actual & BUILD_INTERMEDIATES) in (set(), BUILD_INTERMEDIATES),
         "partial build intermediates")
    for path, expected in HASHES.items():
        need(path.is_file() and digest(path) == expected, "hash: " + str(path))
    bridge = BRIDGE.read_text(encoding="utf-8")
    for marker in MARKERS:
        need(marker in bridge, "marker: " + marker)
    joined = chr(10).join(
        path.read_text(encoding="utf-8")
        for path in (README, PROOF, DERIVATION, MAIN)
    )
    need("Gperp" in joined and "conjugate(m_cb)" in joined,
         "projected Gram orientation")
    need("R_trans" in joined and "R_coh" in joined and "strict" in joined.lower(),
         "margin ledger")
    need("modeling choice" in joined.lower() and
         "not supplied automatically" in joined.lower(), "claim boundary")
    need("assert " not in PRODUCER.read_text(encoding="utf-8") and
         "assert " not in INDEPENDENT.read_text(encoding="utf-8") and
         "assert " not in STRESS.read_text(encoding="utf-8"), "assert guard")
    independent = INDEPENDENT.read_text(encoding="utf-8")
    need("import tpc251_margin_certificate" not in independent and
         "from tpc251_margin_certificate" not in independent,
         "independent imports producer")
    pdf_check()
    child(PRODUCER, "PASS TPC251_MARGIN_CERTIFICATE_V1")
    child(INDEPENDENT, "PASS TPC251_MARGIN_CERTIFICATE_V1")
    child(STRESS, "PASS exact_rational_declared_partition_probe_families=160")
    print("TPC251_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("pdf_pages=4")
    print("pdf_fonts=27_EMBEDDED_SUBSETTED_UNICODE")
    print("literal_margin=C_LONG_VS_PROJECTED_COHERENCE_PLUS_EXTERNAL_E")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC251_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError) as error:
        raise SystemExit("TPC251_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
