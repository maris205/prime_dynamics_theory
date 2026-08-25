#!/usr/bin/env python3
"""Fail-closed release checker for TPC-250."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-250-coherence-controlled-gram-quadratic-sharpness"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_coherence_controlled_gram_quadratic_sharpness.md"
README = PROJECT / "README.md"
PROOF = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
PRODUCER = PROJECT / "code/tpc250_coherence_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc250_independent_checker.py"
STRESS = PROJECT / "experiments/tpc250_coherence_stress.py"
CERTIFICATE = PROJECT / "results/tpc250_certificate.json"
MAIN = PROJECT / "paper/main.tex"
PDF = PROJECT / "paper/paper.pdf"
PROTOCOL = PROJECT / "notes/computational_protocol.md"
STATUS = "PROVED_STRUCTURAL_L1_COHERENCE_CONTROLLED_GRAM_QUADRATIC_SHARPNESS"

HASHES = {
    BRIDGE: "05a9b2e66d152e5325fa0f823f8e6f9c3365dcd515f579dfd199ebe0e7b03d7b",
    README: "cb71292de5ad5ac431f5cc015e0814a3bcf3ad92a17918f466bd0155989b69cb",
    PROOF: "5b39722a776ca876a360d412b4bf3718b76fc54615a450ba908b56f9121c8ce6",
    DERIVATION: "37dc924d06fcde625ccee12e4618dd9c24b5c3074b67a593bf310a69f3e39ecd",
    PRODUCER: "ce1187fec2768e9018a89a75c295a32bfb547ff5f9fce4164bf9b9d9bc36f394",
    INDEPENDENT: "35ad63d874619cb682f41eed96faf7efbff77afa7f1f7e5c470e936c41dd4ee2",
    STRESS: "69a92c1e51c3f19485ef639911b4cf09589d7a523c6e60c237d2bd726d98065a",
    CERTIFICATE: "8e13c563bc33b4904a33a19f0d9cb5686326d2713c7a1ef4a305b93e3ae34acf",
    MAIN: "128aef3815f6a847be76108fc072c5e2c9d9dfca085f1189443f17d5984d15a6",
    PDF: "fb4cc845e597559e124ac092f259a2fbfacae2e8c7aafca182c8fee33c1369e5",
    PROTOCOL: "57613cd6f7409fe951a002e97f25b174a4ec53357dc9d257e8e75c601aefbee0",
}

EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc250_coherence_certificate.py",
    "experiments/tpc250_independent_checker.py",
    "experiments/tpc250_coherence_stress.py",
    "notes/citation_verification.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/source_lock.md", "notes/theorem_ledger.md", "paper/main.tex",
    "paper/paper.pdf", "paper/references.bib", "results/tpc250_certificate.json",
}

BUILD_INTERMEDIATES = {
    "paper/paper.aux", "paper/paper.bbl", "paper/paper.blg",
    "paper/paper.log", "paper/paper.out",
}

MARKERS = (
    "TPC250_GRAM_DEVIATION_BOUND = PROVED_EXACT",
    "TPC250_TWO_SIDED_COHERENCE_ENVELOPE = PROVED_EXACT",
    "TPC250_EMPTY_PAIR_COHERENCE = PROVED_TOTAL_MU_ZERO",
    "TPC250_KAPPA_DOMAIN = PROVED_ONLY_FOR_D_POSITIVE",
    "TPC250_NONCANCELLATION_CONDITION = PROVED_IF_MU_TIMES_KAPPA_MINUS_ONE_LT_ONE",
    "TPC250_INDEPENDENT_RADIUS_ENVELOPE = PROVED_EXACT_INHERITANCE",
    "TPC250_GLOBAL_RADIUS_ENVELOPE = PROVED_EXACT_INHERITANCE",
    "TPC250_UPPER_CONSTANT_SHARPNESS = PROVED_PSD_EQUICORRELATED",
    "TPC250_SIGNED_LOWER_CONSTANT_SHARPNESS = PROVED_PSD_TWO_VECTOR",
    "TPC250_NONNEGATIVE_FLOOR = PROVED_NECESSARY",
    "TPC250_MARGINAL_ONLY_IMPROVEMENT = REFUTED_SCOPED",
    "TPC250_ACTUAL_V59_COHERENCE_ASYMPTOTIC = OPEN",
    "TPC250_ARITHMETIC_ADVANCE = NO",
    "TPC250_L2 = NONE",
    "TPC250_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC250_TWIN_PRIME_RESULT = NONE",
    "TPC250_STATUS = " + STATUS,
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
    need(b"Coherence-Controlled Gram Quadratic" in text_result.stdout,
         "PDF title")
    need(b"COHERENCE_CONTROLLED_GRAM_QUADRATIC_SHARPNESS" in text_result.stdout,
         "PDF claim")
    need(b"TPC250_ACTUAL_V59_COHERENCE_ASYMPTOTIC = OPEN" in text_result.stdout and
         b"TPC250_L2 = NONE" in text_result.stdout, "PDF firewall")
    info = subprocess.run([pdfinfo, str(PDF)], capture_output=True, check=False)
    need(info.returncode == 0 and info.stderr == b"" and
         b"Pages:           5" in info.stdout, "PDF pages")
    fonts = subprocess.run([pdffonts, str(PDF)], capture_output=True, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = fonts.stdout.decode("ascii").splitlines()[2:]
    need(len(rows) == 19, "font rows")
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
    need(actual & BUILD_INTERMEDIATES in (set(), BUILD_INTERMEDIATES),
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
    need("mu=0" in joined and "D>0" in joined, "edge conventions")
    need("marginal" in joined.lower() and "positive semidefinite" in joined.lower(),
         "sharpness prose")
    need("assert " not in PRODUCER.read_text(encoding="utf-8") and
         "assert " not in INDEPENDENT.read_text(encoding="utf-8") and
         "assert " not in STRESS.read_text(encoding="utf-8"), "assert guard")
    independent = INDEPENDENT.read_text(encoding="utf-8")
    need("import tpc250_coherence_certificate" not in independent and
         "from tpc250_coherence_certificate" not in independent,
         "independent imports producer")
    pdf_check()
    child(PRODUCER, "PASS TPC250_CERTIFICATE_V1")
    child(INDEPENDENT, "PASS independent_checker")
    child(STRESS, "PASS NUMERICAL_FINITE_ILLUSTRATION_ONLY")
    print("TPC250_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("pdf_pages=5")
    print("pdf_fonts=19_EMBEDDED_SUBSETTED_UNICODE")
    print("sharpness=UPPER_LOWER_CONSTANTS_AND_ZERO_FLOOR")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC250_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError) as error:
        raise SystemExit("TPC250_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
