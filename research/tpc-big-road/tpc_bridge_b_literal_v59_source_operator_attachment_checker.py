#!/usr/bin/env python3
"""Fail-closed release checker for TPC-247."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-247-literal-v59-source-operator-attachment"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_literal_v59_source_operator_attachment.md"
README = PROJECT / "README.md"
PROOF = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
PRODUCER = PROJECT / "code/tpc247_source_operator_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc247_independent_checker.py"
STRESS = PROJECT / "experiments/tpc247_source_operator_stress.py"
CERTIFICATE = PROJECT / "results/tpc247_certificate.json"
MAIN = PROJECT / "paper/main.tex"
PDF = PROJECT / "paper/paper.pdf"
PROTOCOL = PROJECT / "notes/computational_protocol.md"
STATUS = "PROVED_STRUCTURAL_L1_LITERAL_V59_SOURCE_OPERATOR_ATTACHMENT_WITH_NORM_OBSTRUCTION"

HASHES = {
    BRIDGE: "54bb956ad55245970a7d5d8852f1472d6a9dae68e940d1f9ced0b4c243271eed",
    README: "b14a68c2d9995b56f66f1ee7e39f79624bf3dfe7e6b0adbe0ebf99fd60398eac",
    PROOF: "856cb2c0f7dfbfe760f0120438e894c7360184bc220d7577c77d29415ed1259d",
    DERIVATION: "9a6adafe64123de7b59b347fc9ee3d7b3e1dc1d4491e2f8819c3e53bb5aec880",
    PRODUCER: "2aba74268ee8d0c966f33be751dd94d9bbf00ac6c7204722286cb681d7e3d9d1",
    INDEPENDENT: "84fe510b85f04644039a7ff3fdebf95a3fc5f8eb4ac4dfc68d05cd95e3ad47e2",
    STRESS: "8d2eddf363d7923fbe5eae55e496d7ec3e9800ff9f353067db4596c2996f3bf0",
    CERTIFICATE: "cb50fefb97d23edacf8bd3521150699436c382d3053fe011acbaa4f4a552c3e3",
    MAIN: "08686c00ceded09d8d88779c28cc1c7c28946445f86ef5b0aebfe33baf8b93eb",
    PDF: "f91abc64e8b6f4f4f9a478e2f78deccbf473c9dd2d587e7b4535f326d4fce959",
    PROTOCOL: "13eac892620f742eae20f1d386f63858f5d006f0b6585a26d8dd0832a8d0f9d5",
}

EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc247_source_operator_certificate.py",
    "experiments/tpc247_independent_checker.py",
    "experiments/tpc247_source_operator_stress.py",
    "notes/citation_verification.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/source_lock.md", "notes/theorem_ledger.md", "paper/main.tex",
    "paper/paper.pdf", "paper/references.bib", "results/tpc247_certificate.json",
}

MARKERS = (
    "TPC247_LITERAL_V59_SOURCE_INDEX_OPERATOR = PROVED_EXACT",
    "TPC247_HARD_SUPPORT_BLOCK_DECOMPOSITION = PROVED_EXACT",
    "TPC247_ADMISSIBLE_TRIPLE_EXACTLY_ONCE = PROVED_EXACT",
    "TPC247_TAGGED_EXTERNAL_TWO_LANE_COVARIANCE = PROVED_EXACT",
    "TPC247_W_LANE_NORM_INFLATION = PROVED_EXACT_SQRT_BLOCK_COUNT",
    "TPC247_B_LANE_NORM_PRESERVATION = REFUTED_SCOPED",
    "TPC247_PRIMITIVE_FREQUENCY_ATTACHMENT = OPEN",
    "TPC247_ARITHMETIC_ADVANCE = NO",
    "TPC247_L2 = NONE",
    "TPC247_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC247_TWIN_PRIME_RESULT = NONE",
    "TPC247_STATUS = " + STATUS,
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
    pdftotext = shutil.which("pdftotext")
    pdffonts = shutil.which("pdffonts")
    need(pdftotext is not None and pdffonts is not None, "PDF tools")
    text = subprocess.run([pdftotext, "-layout", str(PDF), "-"],
                          capture_output=True, check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    need(b"Literal V59 Source-Operator Two-Lane Block Attachment" in text.stdout,
         "PDF title")
    need(b"external-copy norm obstruction" in text.stdout and
         b"No arithmetic" in text.stdout, "PDF boundary")
    pdfinfo = shutil.which("pdfinfo")
    need(pdfinfo is not None, "pdfinfo")
    info = subprocess.run([pdfinfo, str(PDF)], capture_output=True, check=False)
    need(info.returncode == 0 and info.stderr == b"" and
         b"Pages:           4" in info.stdout, "PDF pages")
    fonts = subprocess.run([pdffonts, str(PDF)], capture_output=True, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = fonts.stdout.decode("ascii").splitlines()[2:]
    need(len(rows) == 19, "font rows")
    for row in rows:
        columns = row.split()
        need(len(columns) >= 8 and columns[-5:-2] == ["yes", "yes", "yes"],
             "font embedding")


def run() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
              if path.is_file()}
    need(actual == EXPECTED_FILES, "project manifest")
    for path, expected in HASHES.items():
        need(path.is_file() and digest(path) == expected, "hash: " + str(path))
    bridge = BRIDGE.read_text(encoding="utf-8")
    for marker in MARKERS:
        need(marker in bridge, "marker: " + marker)
    joined = "\n".join(path.read_text(encoding="utf-8")
                         for path in (README, PROOF, DERIVATION, MAIN))
    need("tagged external" in joined.lower() and "exactly-once" in joined.lower(),
         "tagged/exactly-once prose")
    need("m||w||^2" in joined and "primitive-frequency" in joined,
         "loss/source firewall")
    need("assert " not in PRODUCER.read_text(encoding="utf-8") and
         "assert " not in INDEPENDENT.read_text(encoding="utf-8"), "assert guard")
    independent_source = INDEPENDENT.read_text(encoding="utf-8")
    need("import tpc247_source_operator_certificate" not in independent_source and
         "from tpc247_source_operator_certificate" not in independent_source,
         "independent imports producer")
    pdf_check()
    child(PRODUCER, "TPC247_CERTIFICATE=PASS")
    child(INDEPENDENT, "TPC247_INDEPENDENT_CHECK=PASS")
    child(STRESS, "TPC247_SOURCE_OPERATOR_STRESS=PASS")
    print("TPC247_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("admissible_triples=60")
    print("pdf_pages=4")
    print("pdf_fonts=19_EMBEDDED_SUBSETTED_UNICODE")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC247_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError) as error:
        raise SystemExit("TPC247_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
