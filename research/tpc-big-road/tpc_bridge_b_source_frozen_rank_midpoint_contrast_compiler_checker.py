#!/usr/bin/env python3
"""Fail-closed release checker for TPC-253."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md"
README = PROJECT / "README.md"
PROOF = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
PRODUCER = PROJECT / "code/tpc253_midpoint_contrast_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc253_independent_checker.py"
STRESS = PROJECT / "experiments/tpc253_midpoint_contrast_stress.py"
CERTIFICATE = PROJECT / "results/tpc253_certificate.json"
MAIN = PROJECT / "paper/main.tex"
PDF = PROJECT / "paper/paper.pdf"
PROTOCOL = PROJECT / "notes/computational_protocol.md"
STATUS = "PROVED_STRUCTURAL_L1_SOURCE_FROZEN_RANK_MIDPOINT_CONTRAST_COMPILER"

HASHES = {
    BRIDGE: "31333053692ca404b6de9a5463cdc803f6b784bbdcc4ca3af36c9ebe16431b16",
    README: "3e25e3e4eabbcceb3cdeaf782a85413fd1806b6841c871ad6532b805309662a6",
    PROOF: "d655ae6c576161cea9411ec31a66a4f077977e7efa36c199e1fa4d5bbf2dd1c6",
    DERIVATION: "3eb55d86643cb1af5ba77148b3dc1e5b894b348583549dfc922bdde4420d3f7d",
    PRODUCER: "2f63783e4ebd35ffc987018be679bcd2e4f103d9fe6b2c81b9e4aa69191509e6",
    INDEPENDENT: "3ae91ed644d1a9d3bfcb11ef48f536c3e69828b3cbac3da6ab385f49aff40d72",
    STRESS: "d0ea209b60ade1f5318f0b37538006e8917e9950193d9590cfc77da9e5938592",
    CERTIFICATE: "78733424554a62ba74986616816ee8eebf2c54b6aad99364acf2ab9f9b51fc56",
    MAIN: "15d2b88c709c4f65ddf941f7ecbc97d1558d41fa8ab3966e8e8bb909646c78ee",
    PDF: "a1b46c00c91e0cdc8bbb6a307b706c950c8bf4b69e102c2ace60adf23eee3194",
    PROTOCOL: "93e5fa0d455619d06591c41d9b08e01dc2d33039da212c55338299ded4ea23ea",
}

EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc253_midpoint_contrast_certificate.py",
    "experiments/tpc253_independent_checker.py",
    "experiments/tpc253_midpoint_contrast_stress.py",
    "notes/citation_verification.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/source_lock.md", "notes/theorem_ledger.md", "paper/main.tex",
    "paper/paper.pdf", "paper/references.bib", "results/tpc253_certificate.json",
}

BUILD_INTERMEDIATES = {
    "paper/paper.aux", "paper/paper.bbl", "paper/paper.blg",
    "paper/paper.log", "paper/paper.out",
}

MARKERS = (
    "TPC253_RANK_MIDPOINT_PARTITION = PROVED_SOURCE_ONLY_DETERMINISTIC",
    "TPC253_INTEGER_THREE_QUARTER_CROSSWALK = PROVED_EXACT",
    "TPC253_MIDPOINT_CONTRAST_NORMALIZATION = PROVED_EXACT",
    "TPC253_PARTIAL_SUM_MOMENT_COMPILER = PROVED_EXACT",
    "TPC253_LITERAL_V59_G_MOMENT_EXPANSION = PROVED_EXACT",
    "TPC253_MIDPOINT_LONGITUDINAL_FORMULA = PROVED_EXACT",
    "TPC253_COARSE_TO_MIDPOINT_COVARIANCE_TRANSFER = PROVED_EXACT",
    "TPC253_WITHIN_CHILD_COVARIANCE_DECOMPOSITION = PROVED_EXACT",
    "TPC253_SAFE_ADJOINT_CROSSWALK = PROVED_EXACT",
    "TPC253_A_X_SELF_ADJOINTNESS = NOT_CLAIMED",
    "TPC253_MIDPOINT_V59_CANONICALITY = NOT_CLAIMED_SOURCE_ONLY_MODELING_CHOICE",
    "TPC253_SMOOTH_V59_PARTITION_IDENTIFICATION = NOT_CLAIMED",
    "TPC253_ACTUAL_V59_NUMERICAL_REPLAY = NOT_TESTABLE_FROM_LOCKED_MATERIAL",
    "TPC253_MIDPOINT_CONTRAST_SIGN_OR_NONZERO = OPEN",
    "TPC253_ARITHMETIC_ADVANCE = NO",
    "TPC253_FIXED_ATOM_CREDIT = 0",
    "TPC253_L2 = NONE",
    "TPC253_FULL_GATE_B = OPEN",
    "TPC253_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC253_TWIN_PRIME_RESULT = NONE",
    "TPC253_STATUS = " + STATUS,
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
    need(result.stdout.startswith(b"PASS "), "child status: " + path.name)
    need(marker.encode("ascii") in result.stdout, "child marker: " + path.name)


def pdf_check() -> None:
    commands = [shutil.which(name) for name in ("pdftotext", "pdffonts", "pdfinfo")]
    need(all(command is not None for command in commands), "PDF tools")
    pdftotext, pdffonts, pdfinfo = commands
    text_result = subprocess.run(
        [pdftotext, "-layout", str(PDF), "-"], capture_output=True, check=False
    )
    need(text_result.returncode == 0 and text_result.stderr == b"", "PDF text")
    need(b"Source-Frozen Rank-Midpoint Contrasts" in text_result.stdout and
         b"for the Literal V59 Scalar" in text_result.stdout, "PDF title")
    need(b"not V59-canonical" in text_result.stdout and
         b"Gate-B closure" in text_result.stdout and
         b"twin-prime result" in text_result.stdout, "PDF firewall")
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
    need("M_mid=M_coarse+z tensor z" in joined and
         "conjugate(<z,w>)<z,A_x beta>" in joined, "rank midpoint transfer")
    need("floor(3k/4)" in joined and "nonintegral" in joined,
         "integer crosswalk firewall")
    need("<z,A_x beta>=<A_x^*z,beta>" in joined and
         "deleted diagonal" in joined and "both unit masks" in joined,
         "literal adjoint ledger")
    need("not V59-canonical" in joined and "not literal numerical V59" in joined,
         "model and synthetic firewalls")
    need("assert " not in PRODUCER.read_text(encoding="utf-8") and
         "assert " not in INDEPENDENT.read_text(encoding="utf-8") and
         "assert " not in STRESS.read_text(encoding="utf-8"), "assert guard")
    independent = INDEPENDENT.read_text(encoding="utf-8")
    need("import tpc253_midpoint_contrast_certificate" not in independent and
         "from tpc253_midpoint_contrast_certificate" not in independent,
         "independent imports producer")
    need("type(value) is not int" in independent and
         "typed_bool_count" in independent,
         "strict integer and mutation ledger")
    pdf_check()
    child(PRODUCER, "PASS TPC253_RANK_MIDPOINT_CONTRAST_CERTIFICATE_V1")
    child(INDEPENDENT, "mutations_rejected=59")
    child(STRESS, "PASS exact_rational_rank_midpoint_families=192")
    print("TPC253_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("pdf_pages=4")
    print("pdf_fonts=27_EMBEDDED_SUBSETTED_UNICODE")
    print("rank_midpoint=SOURCE_ONLY_FIXED_BEFORE_COEFFICIENTS")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC253_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError) as error:
        raise SystemExit("TPC253_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
