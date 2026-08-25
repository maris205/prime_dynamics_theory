#!/usr/bin/env python3
"""Fail-closed release checker for TPC-252."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-252-declared-partition-refinement-degeneracy"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_declared_partition_refinement_degeneracy.md"
README = PROJECT / "README.md"
PROOF = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
PRODUCER = PROJECT / "code/tpc252_partition_refinement_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc252_independent_checker.py"
STRESS = PROJECT / "experiments/tpc252_partition_refinement_stress.py"
CERTIFICATE = PROJECT / "results/tpc252_certificate.json"
MAIN = PROJECT / "paper/main.tex"
PDF = PROJECT / "paper/paper.pdf"
PROTOCOL = PROJECT / "notes/computational_protocol.md"
STATUS = "PROVED_STRUCTURAL_L1_DECLARED_PARTITION_REFINEMENT_DEGENERACY"

HASHES = {
    BRIDGE: "2763e2b1b67e1ad0e7dd68f0429eed7ae250691d60fdb1c94fcdff89a579f5f3",
    README: "901bc4f065fd60e11eb700eeaa8f08197b078ced6e649226ff5a449bc0a2ae9a",
    PROOF: "82e47f33ad60bc3a3b4164415f348d8b236d3d816e05169907a20a878dbd737e",
    DERIVATION: "2bc89f90ea730eb3385020ab883ec5a381da830b9f1702ee7cfcdd2bfda82b3f",
    PRODUCER: "a8295df73e131ab9bc0c3b4643981b1acaac5912fccb5f93351a43ee47705d28",
    INDEPENDENT: "e4addb9b89281d240b6eadac8fc89165237b2362d178119dcf689a2f9931b9bc",
    STRESS: "977fe7317b3058b837ec33344829a2c867c3c7a2dda517397757123e6bd28859",
    CERTIFICATE: "baba6a39f39f44302d1fdcb8538052f0b5d1f963c15e4929fe6ee580b910d0d8",
    MAIN: "46105cd2fafd9f308822ed2f29723ef1886820b651322f014b9e2d8ae47a2051",
    PDF: "b88c2ed4af43b751d02fb96b529858624b659bb57ce172b95e6e7c82d99482f7",
    PROTOCOL: "7b55211b5938a415bd933fd9d4cfa571d1da163dee5ba1cccafebefc179b1a23",
}

EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc252_partition_refinement_certificate.py",
    "experiments/tpc252_independent_checker.py",
    "experiments/tpc252_partition_refinement_stress.py",
    "notes/citation_verification.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/source_lock.md", "notes/theorem_ledger.md", "paper/main.tex",
    "paper/paper.pdf", "paper/references.bib", "results/tpc252_certificate.json",
}

BUILD_INTERMEDIATES = {
    "paper/paper.aux", "paper/paper.bbl", "paper/paper.blg",
    "paper/paper.log", "paper/paper.out",
}

MARKERS = (
    "TPC252_LITERAL_V59_SINGLETON_IDENTITY = PROVED_EXACT_FINITE",
    "TPC252_BINARY_REFINEMENT_PROJECTION = PROVED_EXACT_RANK_ONE",
    "TPC252_BINARY_REFINEMENT_COVARIANCE_TRANSFER = PROVED_EXACT",
    "TPC252_FIXED_PROBE_PROJECTED_GRAM_UPDATE = PROVED_EXACT_WITH_FIXED_PROBE_FIREWALL",
    "TPC252_TRANSVERSE_RADIUS_REFINEMENT = PROVED_NONINCREASING",
    "TPC252_SINGLETON_PROJECTED_GRAM_AND_RADIUS = PROVED_ZERO",
    "TPC252_PARTITION_MARGIN_OPTIMIZATION = PROVED_EQUAL_TO_DIRECT_BOUND",
    "TPC252_SAME_SOURCE_SYNTHETIC_NONINVARIANCE = PROVED_EXACT",
    "TPC252_EVERY_SOURCE_PARTITION_INSTABILITY = REFUTED_SCOPED",
    "TPC252_ACTUAL_V59_ARITHMETIC_INSTABILITY = OPEN",
    "TPC252_CANONICAL_PARTITION = NOT_CLAIMED",
    "TPC252_ARITHMETIC_ADVANCE = NO",
    "TPC252_FIXED_ATOM_CREDIT = 0",
    "TPC252_L2 = NONE",
    "TPC252_FULL_GATE_B = OPEN",
    "TPC252_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC252_TWIN_PRIME_RESULT = NONE",
    "TPC252_STATUS = " + STATUS,
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
    need(b"Binary Refinement Calculus and Singleton Degeneracy" in text_result.stdout and
         b"for Declared-Block V59 Margins" in text_result.stdout, "PDF title")
    need(b"maximum supported claim is structural L1 only" in text_result.stdout and
         b"Gate-B closure" in text_result.stdout and
         b"twin-prime" in text_result.stdout, "PDF firewall")
    need(b"qquad" not in text_result.stdout and b"qqquad" not in text_result.stdout,
         "PDF lost backslash")
    info = subprocess.run([pdfinfo, str(PDF)], capture_output=True, check=False)
    need(info.returncode == 0 and info.stderr == b"" and
         b"Pages:           4" in info.stdout, "PDF pages")
    fonts = subprocess.run([pdffonts, str(PDF)], capture_output=True, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = fonts.stdout.decode("ascii").splitlines()[2:]
    need(len(rows) == 24, "font rows")
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
    need("M_P'=M_P+z tensor z" in joined and
         "conjugate(<z,w>)<z,g>" in joined, "rank-one covariance transfer")
    need("R_trans(P')<=R_trans(P)" in joined and
         "max_P [|C_long(P)|-R_coh(P)-E]_+" in joined, "radius and margin")
    need("kappa" in joined and "undefined" in joined and
         "fixed" in joined.lower() and "probe" in joined.lower(), "domain and scope")
    need("synthetic" in joined.lower() and "not a literal V59" in joined,
         "synthetic evidence firewall")
    need("assert " not in PRODUCER.read_text(encoding="utf-8") and
         "assert " not in INDEPENDENT.read_text(encoding="utf-8") and
         "assert " not in STRESS.read_text(encoding="utf-8"), "assert guard")
    independent = INDEPENDENT.read_text(encoding="utf-8")
    need("import tpc252_partition_refinement_certificate" not in independent and
         "from tpc252_partition_refinement_certificate" not in independent,
         "independent imports producer")
    pdf_check()
    child(PRODUCER, "PASS TPC252_PARTITION_REFINEMENT_CERTIFICATE_V1")
    child(INDEPENDENT, "PASS TPC252_PARTITION_REFINEMENT_CERTIFICATE_V1")
    child(STRESS, "PASS exact_gaussian_rational_refinement_families=192")
    print("TPC252_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("pdf_pages=4")
    print("pdf_fonts=24_EMBEDDED_SUBSETTED_UNICODE")
    print("partition_optimization=EXACT_DIRECT_BOUND_SINGLETON_ATTAINMENT")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC252_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError) as error:
        raise SystemExit("TPC252_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
