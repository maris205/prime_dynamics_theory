#!/usr/bin/env python3
"""Fail-closed release checker for TPC-255."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-255-exact-adjoint-diagonal-boundary-compiler"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md"
PRODUCER = PROJECT / "code/tpc255_adjoint_diagonal_boundary_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc255_independent_checker.py"
STRESS = PROJECT / "experiments/tpc255_adjoint_diagonal_boundary_stress.py"
CERTIFICATE = PROJECT / "results/tpc255_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
STATUS = "PROVED_EXACT_SOURCE_BACKED_L1_ADJOINT_DIAGONAL_HARD_WINDOW_CHILD_JUMP_COMPILER"

HASHES = {
    BRIDGE: "cd57bf302938946489a509991a50c3945b793371914e1fd7c99c5ace57ca1e97",
    PROJECT / ".gitignore": "d92f5c8f90059cd13dc2b16e79d88d4b4d7bfb936cb1ae88d90f407177332bb3",
    PROJECT / "DERIVATION_PACKAGE.md": "6e1be7d81ac112cd59ecfd2d71d563130ddf4425c24347767a068c19a92e73cf",
    PROJECT / "PAPER_PLAN.md": "9fb26b2beb9d8728e8acd58f169bef5749e5bc73d932ce74a348739f0d776193",
    PROJECT / "PROOF_PACKAGE.md": "a03ce2d299fa85ea6498e1a6e531a4f4d3ee39413696a7e53adeebfd3985c899",
    PROJECT / "README.md": "5c0fa4cd2fe479175ff3573506a8f0e335e602d81960417be967d13cef96a538",
    PRODUCER: "a518ea214e7dd37db1dd4316b5fefbfc6330fdd67d7e5db154cab8e1c9cb1bf7",
    STRESS: "8bf7f853279f185cbbb9b8c7a3071b3bd841e351fb26451805eb1822e1684413",
    INDEPENDENT: "9502feb4b0d55e39a2290fba4cfd8f34b770f6a05521711cb4a24a79a294ab2c",
    PROJECT / "notes/citation_verification.md": "e88164bb18937d5465b30a703423d05443fb97075c808d080b47cdcb9b733974",
    PROJECT / "notes/claim_firewall.md": "55a5ed972286998c4c26eb856757000318db6308bb1dd8f60180a10622e562da",
    PROJECT / "notes/computational_protocol.md": "8656686bbcaa0d70c64d446b5a61c072f582c17aff84c721cad3c8eb7615ccc5",
    PROJECT / "notes/route_evaluation.md": "80d1291c2b9a2fea0ed39569e6631b2e63ab205993fde00d9d4ea0a30382d76b",
    PROJECT / "notes/source_lock.md": "1e3c35388cab5e9a36c0e6aaf68ac30150938802be834cc095a7e02a9a82d78b",
    PROJECT / "notes/theorem_ledger.md": "517cfaccdbc11bf857361afd7ac4c1348bd0761e31783405832bebad5710222c",
    PROJECT / "paper/main.tex": "372f84d7b590d0f927a75b603fa7b62b3e15ad1ef04c01aac6c4892e418278f1",
    PDF: "0a1c608ec09ef53ebc928269b877c54a8ee7574c1ba607ede890a64fb4c1dd66",
    PROJECT / "paper/references.bib": "63573811e67fb865b9ff83c87d668271058b0cb60d0e4807cc6c637196342c56",
    CERTIFICATE: "61ac918286d673097c0c0d210f00db473df49b3b14db84ad983c88f8d32ec4be",
}

EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc255_adjoint_diagonal_boundary_certificate.py",
    "experiments/tpc255_adjoint_diagonal_boundary_stress.py",
    "experiments/tpc255_independent_checker.py", "notes/citation_verification.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/source_lock.md", "notes/theorem_ledger.md",
    "paper/main.tex", "paper/paper.pdf", "paper/references.bib",
    "results/tpc255_certificate.json",
}
BUILD_INTERMEDIATES = {
    "paper/paper.aux", "paper/paper.bbl", "paper/paper.blg",
    "paper/paper.log", "paper/paper.out",
}
MARKERS = (
    "TPC255_ROUTE_ADVANCE = YES_EXACT_LITERAL_STRUCTURE",
    "TPC255_LITERAL_ARITHMETIC_STRUCTURE_ADVANCE = YES",
    "TPC255_ARITHMETIC_ADVANCE = NO",
    "TPC255_COMPLETE_UNIT_CENTERED_ROW = PROVED_EXACT_SOURCE_BACKED_ZERO_FOR_H_GREATER_THAN_2Q",
    "TPC255_DELETED_DIAGONAL_RETURN = PROVED_EXACT",
    "TPC255_HARD_WINDOW_LEAKAGE = PROVED_EXACT_IDENTITY_NO_ESTIMATE",
    "TPC255_CHILD_JUMP_LEAKAGE = PROVED_EXACT_WITH_COEFFICIENT_PLUS_MINUS_ONE_OVER_RHO",
    "TPC255_BQ_WEIGHTED_BETA_MIDPOINT = PROVED_EXACT_REDUCTION_NO_ESTIMATE",
    "TPC255_SIGN_OR_NONZERO = OPEN",
    "TPC255_FIXED_ATOM_CREDIT = 0",
    "TPC255_L2 = NONE",
    "TPC255_FULL_GATE_B = OPEN",
    "TPC255_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC255_TWIN_PRIME_RESULT = NONE",
    "TPC255_STATUS = " + STATUS,
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def child(path: Path, marker: bytes) -> None:
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)
    need(result.returncode == 0 and result.stderr == b"", "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)


def pdf_check() -> None:
    tools = [shutil.which(name) for name in ("pdftotext", "pdffonts", "pdfinfo")]
    need(all(tool is not None for tool in tools), "PDF tools")
    pdftotext, pdffonts, pdfinfo = tools
    text = subprocess.run([pdftotext, "-layout", str(PDF), "-"], capture_output=True, check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    need(b"Exact Adjoint Diagonal Return and Hard-Boundary Decomposition" in text.stdout,
         "PDF title")
    need(b"ARITHMETIC_ADVANCE=NO" in text.stdout and b"Gate B" in text.stdout and
         b"no twin-prime" in text.stdout, "PDF firewall")
    info = subprocess.run([pdfinfo, str(PDF)], capture_output=True, check=False)
    need(info.returncode == 0 and b"Pages:           4" in info.stdout, "PDF pages")
    fonts = subprocess.run([pdffonts, str(PDF)], capture_output=True, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = fonts.stdout.decode("ascii").splitlines()[2:]
    need(len(rows) == 26, "PDF font count")
    for row in rows:
        columns = row.split()
        need(len(columns) >= 8 and columns[-5:-2] == ["yes", "yes", "yes"], "PDF fonts embedded")


def run() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*") if path.is_file()}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    need((actual & BUILD_INTERMEDIATES) in (set(), BUILD_INTERMEDIATES), "partial build files")
    for path, expected in HASHES.items():
        need(path.is_file() and sha(path) == expected, "hash: " + str(path))
    bridge = BRIDGE.read_text(encoding="utf-8")
    for marker in MARKERS:
        need(marker in bridge, "marker: " + marker)
    joined = "\n".join(
        (PROJECT / relative).read_text(encoding="utf-8")
        for relative in ("README.md", "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md", "paper/main.tex")
    )
    for required in (
        "P*", "E*", "J*", "B_Q", "H>2Q", "ordered-rank", "input-unit",
        "output-unit", "ARITHMETIC_ADVANCE=NO", "no twin-prime",
    ):
        need(required in joined, "semantic marker: " + required)
    for script in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in script.read_text(encoding="utf-8"), "assert guard")
    need("import tpc255_adjoint_diagonal_boundary_certificate" not in INDEPENDENT.read_text(encoding="utf-8"),
         "independent checker imports producer")
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")
    payload = parsed.get("payload")
    need(raw == canonical and type(payload) is dict and payload.get("status") == STATUS,
         "canonical certificate")
    need(parsed.get("payload_sha256") == hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    ).hexdigest(), "certificate payload digest")
    if BUILD_INTERMEDIATES <= actual:
        log = (PROJECT / "paper/paper.log").read_text(encoding="utf-8", errors="replace")
        for forbidden in ("LaTeX Warning", "Undefined control sequence", "Overfull", "Underfull"):
            need(forbidden not in log, "LaTeX log: " + forbidden)
    pdf_check()
    child(PRODUCER, b"TPC255_CERTIFICATE=PASS")
    child(INDEPENDENT, b"TPC255_INDEPENDENT_CHECK=PASS")
    child(STRESS, b"TPC255_STRESS=PASS")
    print("TPC255_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("pdf_pages=4")
    print("pdf_fonts=26_EMBEDDED_SUBSETTED_UNICODE")
    print("arithmetic_advance=NO")
    print("literal_arithmetic_structure_advance=YES")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    if not arguments.check:
        raise SystemExit("TPC255_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, OSError, UnicodeError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        raise SystemExit("TPC255_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
