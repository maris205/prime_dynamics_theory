#!/usr/bin/env python3
"""Fail-closed release checker for TPC-257."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-257-four-block-haar-transverse-norm-floor"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_four_block_haar_transverse_norm_floor.md"
PRODUCER = PROJECT / "code/tpc257_four_block_haar_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc257_independent_checker.py"
STRESS = PROJECT / "experiments/tpc257_four_block_haar_stress.py"
CERTIFICATE = PROJECT / "results/tpc257_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
BASELINE_HEAD = "e593b6f85ff16c0c8fc99474ba50e74af4a93b51"
STATUS = "PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR_FOR_LITERAL_V59_ADJOINT"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "2d71869341393ad78c627cb84e306f0bfeca730f471f7e37dc4cb2f482dff5f0",
    "research/tpc-big-road/bridge_b_literal_beta_haar_adjoint_asymptotic.md":
        "ccb87a64ddb36ed35af415dde2d9fcf0a3ed7f443934edf0a24c98f7bd3ab4da",
    "research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md":
        "cd57bf302938946489a509991a50c3945b793371914e1fd7c99c5ace57ca1e97",
    "research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md":
        "31333053692ca404b6de9a5463cdc803f6b784bbdcc4ca3af36c9ebe16431b16",
    "papers/tpc-256-literal-beta-haar-adjoint-asymptotic/PROOF_PACKAGE.md":
        "cd6c0aecf0f88b3ad1988793998b98e883473b3c25af47244bebf97614e90f4f",
    "papers/tpc-256-literal-beta-haar-adjoint-asymptotic/notes/source_lock.md":
        "d195a076158087d7626e0f1ff1976009ed9c84610160b6d109547689aa1b3dc7",
    "research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md":
        "093fa3bc9c3512d760462526daac7aa1867ee41eb5b6b0e2bfd0a7ee8d580906",
    "papers/tpc-233-critical-depth-row-mass-obstruction/notes/source_lock.md":
        "a61a7a8f43ef4cbf46a69443b01bd2d4d41cc31a418612ad7a66fd5d54af6446",
}

# Filled after the project files and PDF have passed their final build.
PROJECT_HASHES = {
    ".gitignore": "877a508d3d5e64e6ed46e9d4e6f5bf913239ea84d48c5e551dee08616603f3ed",
    "DERIVATION_PACKAGE.md": "f3bc0a2fa4b99fee60d3596f52ab2ee0db9d213a28627f3e95f5a276b96fd8b1",
    "PAPER_PLAN.md": "a6d5dc24cfd71fbcaab241de8a6215c3b97e061a02ec517c6da9af8ba43f186f",
    "PROOF_PACKAGE.md": "06b6f2e9842f68fc6f3d882f95d3b9c161980ceb429dd24b52bd98322e6f397f",
    "README.md": "a865eec5b8c64212a9fbd47982ba57b961885730f8026a262803387c7a652d88",
    "code/tpc257_four_block_haar_certificate.py":
        "fc2dc515f7a10b1cf9589f530ca5a9dcf123335e389e0e747e6c7f2c25610038",
    "experiments/tpc257_four_block_haar_stress.py":
        "7c95cf35c88e96c1a7800a3fe4483b3b13b855c4722da424b929d13ad4c03f8a",
    "experiments/tpc257_independent_checker.py":
        "558b021b163ce53995a66e18035f4d5531be6d7e03971dd6b01b3a585a5d595c",
    "notes/citation_verification.md":
        "3b83cd53f730a093bfab2fb54e4ecdcac2f0d1190f657341b2c1899370b47503",
    "notes/claim_firewall.md":
        "84ff6e30b0c25074a869758ae66d2eaed4535095663dfc1e54f7070142e439a0",
    "notes/computational_protocol.md":
        "87183933ff55b7f6910a2f773c2d00eb9a1ee9881149d6002f1cd76a9e6b02cd",
    "notes/route_evaluation.md":
        "b92bf14797013e4371a0d9c88d4dc7bdef39d76b1361d8cf73009165b41e1f3f",
    "notes/source_lock.md":
        "a3bf5beb7ae07c1e1003cb3e690948950fecc2c22230c1bc544fbd5f6a38bdd1",
    "notes/theorem_ledger.md":
        "127bf4a07defd26a87f74e989a426500a3b50a18df03875805b9afeb71a5a3a6",
    "paper/main.tex": "4b3e26cb04976f9137cb71c00e94a5aa08fb660ddbc34e79d309c49eac6a8d90",
    "paper/paper.pdf": "b5f401cc652b4275a08c6b52e5283649078f8cedd04b1345e8c48cc4b1d47459",
    "paper/references.bib": "28b3af777b84dea45a31dacde4546e10d2f2ae412158e7b712b3471508514686",
    "results/tpc257_certificate.json":
        "a12f981c62ca1728624152d5e0720c47be152d7f0c1d4df88f7cbff3d70b18fd",
}

EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/paper.aux", "paper/paper.bbl", "paper/paper.blg",
    "paper/paper.log", "paper/paper.out",
}
MARKERS = (
    "TPC257_MAXIMUM_CLAIM = " + STATUS,
    "TPC257_ROUTE_ADVANCE = YES_SCOPED_TRANSVERSE_HAAR",
    "TPC257_ARITHMETIC_ADVANCE = YES_SCOPED_TRANSVERSE_LOWER_FLOOR",
    "TPC257_THREE_MODE_HAAR_ORTHOGONALITY = PROVED_EXACT",
    "TPC257_TRANSVERSE_OUTPUT_FLOOR = PROVED_SOURCE_BACKED",
    "TPC257_FULL_OUTPUT_NORM_FLOOR = PROVED_SOURCE_BACKED",
    "TPC257_L2 = NONE",
    "TPC257_FULL_GATE_B = OPEN",
    "TPC257_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC257_FIXED_ATOM_CREDIT = 0",
    "TPC257_TWIN_PRIME_RESULT = NONE",
    "TPC257_STATUS = PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR",
)
REQUIRED_SEMANTIC = (
    "3456/3125", "884736/823543", "55/48", "1/48", "Parseval",
    "lower floor", "not an upper", "full Gate B", "ROUND2_CLUE",
)
EXPECTED_PDF_PAGES = 5
EXPECTED_PDF_FONTS = 26


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def baseline_bytes(relative: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + relative], cwd=ROOT,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", "baseline source: " + relative)
    return result.stdout


def check_sources() -> None:
    for relative, expected in SOURCE_HASHES.items():
        need(digest(baseline_bytes(relative)) == expected, "source hash: " + relative)


def check_exact_geometry() -> None:
    for p in range(1, 25):
        for q in range(1, 25):
            rho2 = Fraction(p * q, p + q)
            need(rho2 * (Fraction(1, p) + Fraction(1, q)) == 1, "pair norm")
            need(rho2 * (Fraction(1, p) + Fraction(1, q)) ** 2 == 1 / rho2,
                 "pair jump")
    need(Fraction(133, 400) - Fraction(1, 2) == Fraction(-67, 400), "divisor exponent")
    need(Fraction(1, 3) + 2 * Fraction(21, 32) - Fraction(1, 2) == Fraction(55, 48),
         "boundary exponent")
    need(Fraction(2, 3) + Fraction(1, 2) == Fraction(7, 6), "main exponent")
    need(Fraction(7, 6) - Fraction(55, 48) == Fraction(1, 48), "boundary gap")


def child(path: Path, marker: bytes) -> bytes:
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_pdf() -> None:
    tools = [shutil.which(name) for name in ("pdftotext", "pdffonts", "pdfinfo")]
    need(all(tool is not None for tool in tools), "PDF tools")
    pdftotext, pdffonts, pdfinfo = tools
    text = subprocess.run([pdftotext, "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    need(b"Four-Block Haar Lifts" in text.stdout, "PDF title")
    need(b"Transverse Norm Floor" in text.stdout, "PDF title continuation")
    info = subprocess.run([pdfinfo, str(PDF)], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    need(info.returncode == 0 and
         ("Pages:           " + str(EXPECTED_PDF_PAGES)).encode() in info.stdout,
         "PDF pages")
    fonts = subprocess.run([pdffonts, str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = fonts.stdout.decode("ascii").splitlines()[2:]
    need(len(rows) == EXPECTED_PDF_FONTS, "PDF font count")
    for row in rows:
        columns = row.split()
        need(len(columns) >= 8 and columns[-5:-2] == ["yes", "yes", "yes"],
             "PDF fonts embedded")


def run() -> None:
    need(len(PROJECT_HASHES) == len(EXPECTED_FILES), "project hash manifest unset")
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*") if path.is_file()}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    need((actual & BUILD_INTERMEDIATES) in (set(), BUILD_INTERMEDIATES), "partial build manifest")
    for relative, expected in PROJECT_HASHES.items():
        need(expected != "PLACEHOLDER", "project hash placeholder: " + relative)
        need(digest((PROJECT / relative).read_bytes()) == expected, "project hash: " + relative)
    check_sources()
    check_exact_geometry()
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    joined = bridge_text + "\n" + "\n".join(
        (PROJECT / relative).read_text(encoding="utf-8", errors="replace")
        for relative in ("README.md", "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md",
                         "notes/route_evaluation.md", "paper/main.tex")
    )
    for marker in MARKERS:
        need(marker in joined, "marker: " + marker)
    for marker in REQUIRED_SEMANTIC:
        need(marker in joined, "semantic marker: " + marker)
    for script in (PRODUCER, INDEPENDENT, STRESS):
        need("as" + "sert " not in script.read_text(encoding="utf-8"),
             "unsafe assertion syntax")
    independent_text = INDEPENDENT.read_text(encoding="utf-8")
    need(("from " + "tpc257_four_block_haar_certificate") not in independent_text,
         "independent producer import")
    parsed = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    raw = CERTIFICATE.read_bytes()
    canonical = (json.dumps(parsed, sort_keys=True, separators=(",", ":"),
                            ensure_ascii=True) + "\n").encode("ascii")
    need(raw == canonical and parsed.get("claim") == STATUS, "canonical certificate")
    need(parsed.get("schema") == "TPC257_CERTIFICATE_V1", "certificate schema")
    need(parsed.get("epistemic_status", {}).get("theorem") == "PROVED_SOURCE_BACKED",
         "certificate theorem status")
    need(parsed.get("numerical_observation", {}).get("proof_credit") == "NONE",
         "numerical proof credit")
    need(parsed.get("firewall", {}).get("TPC257_FULL_GATE_B") == "OPEN" and
         parsed.get("firewall", {}).get("TPC257_L2") == "NONE" and
         parsed.get("firewall", {}).get("TPC257_TWIN_PRIME_RESULT") == "NONE",
         "certificate firewall")
    log = PROJECT.joinpath("paper/paper.log").read_text(encoding="utf-8", errors="replace")
    for forbidden in ("LaTeX Warning", "Undefined control sequence", "Overfull", "Underfull"):
        need(forbidden not in log, "LaTeX log: " + forbidden)
    check_pdf()
    child(PRODUCER, b"TPC257_CERTIFICATE=PASS")
    child(INDEPENDENT, b"TPC257_INDEPENDENT_CHECK=PASS")
    child(STRESS, b"TPC257_STRESS=PASS")
    print("TPC257_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("pdf_pages=" + str(EXPECTED_PDF_PAGES))
    print("pdf_fonts=" + str(EXPECTED_PDF_FONTS) + "_EMBEDDED_SUBSETTED_UNICODE")
    print("transverse_factor=0.061792126717520")
    print("boundary_gap=1_OVER_48")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC257_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, OSError, UnicodeError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC257_BRIDGE_CHECK=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
