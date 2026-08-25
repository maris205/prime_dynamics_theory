#!/usr/bin/env python3
"""Fail-closed release checker for TPC-256."""

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
PROJECT = ROOT / "papers/tpc-256-literal-beta-haar-adjoint-asymptotic"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_literal_beta_haar_adjoint_asymptotic.md"
PRODUCER = PROJECT / "code/tpc256_literal_beta_haar_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc256_independent_checker.py"
STRESS = PROJECT / "experiments/tpc256_beta_haar_asymptotic_stress.py"
CERTIFICATE = PROJECT / "results/tpc256_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
BASELINE_HEAD = "4695df00b1c6962bc94e21474e101c698f39f4bd"
STATUS = "PROVED_SOURCE_BACKED_L1_LITERAL_BETA_RANK_MIDPOINT_AND_DIAGONAL_DOMINANT_ADJOINT_ASYMPTOTIC"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "1da1d8a74c5fd85a2401a389762966aaa0cb0405e2df16465edae09ead47600e",
    "research/tpc-big-road/bridge_b_proper_factor_unit_ratio_reduction.md":
        "705b0dfd4d94d70bad798ca6cccf7e0f37f049683d30373ea895d97a6db93da1",
    "research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md":
        "b45ef249175c84758f6052a647f54f74c227351d317034766c5988c7c98f7c5e",
    "research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md":
        "31333053692ca404b6de9a5463cdc803f6b784bbdcc4ca3af36c9ebe16431b16",
    "research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md":
        "cd57bf302938946489a509991a50c3945b793371914e1fd7c99c5ace57ca1e97",
    "research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md":
        "fd02eaf5504b7a7c2182a8a045b9ec03488ef72ef7b88e750ba781163c10525a",
    "research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md":
        "093fa3bc9c3512d760462526daac7aa1867ee41eb5b6b0e2bfd0a7ee8d580906",
    "papers/tpc-233-critical-depth-row-mass-obstruction/notes/source_lock.md":
        "a61a7a8f43ef4cbf46a69443b01bd2d4d41cc31a418612ad7a66fd5d54af6446",
}

PROJECT_HASHES: dict[str, str] = {
    ".gitignore": "877a508d3d5e64e6ed46e9d4e6f5bf913239ea84d48c5e551dee08616603f3ed",
    "DERIVATION_PACKAGE.md": "78bc8ff489783bde407513e1eed6f3034b004098be45f34633feaa0acedf7e38",
    "PAPER_PLAN.md": "b739702b127a2d36bd7349ac47dbfe81cf602d94ec0fc3b035d7cd253f277186",
    "PROOF_PACKAGE.md": "cd6c0aecf0f88b3ad1988793998b98e883473b3c25af47244bebf97614e90f4f",
    "README.md": "aee0d9fd92fd80f056b84ca3ee409e62f3e5c0b136f8d1c124dd4965d16b73c1",
    "code/tpc256_literal_beta_haar_certificate.py":
        "ad520b43dab6090353ddc83284f2b471b9d36c89dc1596371ad9cdc4c3aba7ee",
    "experiments/tpc256_beta_haar_asymptotic_stress.py":
        "dd21886ada64b37dbc0cd7ff116b7c72f4005fe7c721991f8ec0d0289af4447e",
    "experiments/tpc256_independent_checker.py":
        "3634052f16cd0c0066853e33bce62a5a2cdb742c6367ec79e7b923f4a48d574d",
    "notes/citation_verification.md":
        "9f723b12b7882632066b3ec6abfc2ba29dd4e1d9a4a1a20b52c323236901e220",
    "notes/claim_firewall.md":
        "b4dcef3cbb4214232983832713b9199435e422bcbf3a086a8fdecfeaa97a572e",
    "notes/computational_protocol.md":
        "58f0d1b2123b1b44892c5419ffa42918ca87a70fbeb8334d8d701467a3004f8a",
    "notes/route_evaluation.md":
        "f67d30941259d57d66262dce5a1d2d9a30cbe487fe667a8250c70f8116cfdd40",
    "notes/source_lock.md":
        "d195a076158087d7626e0f1ff1976009ed9c84610160b6d109547689aa1b3dc7",
    "notes/theorem_ledger.md":
        "cb727d7ba7fb6ecf91064d18a7d92a956b7d99cdf09706a7b3eb8c4962d6c1de",
    "paper/main.tex": "fbc08044fddd1a9b692ab5c45f32b9846a6d484a5642aa672df53cd9b4dd6961",
    "paper/paper.pdf": "6b771b0cdcfbed343b91ca28476fbc68fa6b565d613220213e3c82db6f7896f6",
    "paper/references.bib": "0189a39a77e3326d1dca1b3c2330751c11697410ecbd8b0f9b46b4d720b70ec6",
    "results/tpc256_certificate.json":
        "e9b9a3ea5d01a1f11d3c51a0c055cbe881f4cf7451b608f108ac114c185c1acc",
}

EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc256_literal_beta_haar_certificate.py",
    "experiments/tpc256_beta_haar_asymptotic_stress.py",
    "experiments/tpc256_independent_checker.py", "notes/citation_verification.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/source_lock.md", "notes/theorem_ledger.md",
    "paper/main.tex", "paper/paper.pdf", "paper/references.bib",
    "results/tpc256_certificate.json",
}
BUILD_INTERMEDIATES = {
    "paper/paper.aux", "paper/paper.bbl", "paper/paper.blg",
    "paper/paper.log", "paper/paper.out",
}
MARKERS = (
    "TPC256_ROUTE_ADVANCE = YES_LITERAL_ARITHMETIC",
    "TPC256_ARITHMETIC_ADVANCE = YES_SCOPED_LITERAL_BETA_ADJOINT_HAAR_LANE",
    "TPC256_LITERAL_BETA_HAAR_ASYMPTOTIC = PROVED_SOURCE_BACKED",
    "TPC256_ADJOINT_NORMALIZED_COMPLEX_ASYMPTOTIC = PROVED_SOURCE_BACKED",
    "TPC256_REAL_PART_EVENTUALLY_NEGATIVE = PROVED",
    "TPC256_SCALAR_EVENTUALLY_NONZERO = PROVED",
    "TPC256_NORMALIZED_PHASE_TO_MINUS_ONE = PROVED",
    "TPC256_SCALAR_IS_REAL = NOT_CLAIMED",
    "TPC256_UNQUALIFIED_PRINCIPAL_ARGUMENT_TO_PLUS_PI = NOT_CLAIMED",
    "TPC256_FIXED_ATOM_CREDIT = 0",
    "TPC256_L2 = NONE",
    "TPC256_FULL_GATE_B = OPEN",
    "TPC256_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC256_TWIN_PRIME_RESULT = NONE",
    "TPC256_STATUS = " + STATUS,
)
EXPECTED_PDF_PAGES = 6
EXPECTED_PDF_FONTS = 29


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def baseline_bytes(relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", BASELINE_HEAD + ":" + relative],
        cwd=ROOT, capture_output=True, check=False,
    )
    need(result.returncode == 0 and result.stderr == b"", "baseline source: " + relative)
    return result.stdout


def check_sources() -> None:
    for relative, expected in SOURCE_HASHES.items():
        need(digest(baseline_bytes(relative)) == expected, "source hash: " + relative)
    need(digest(BRIDGE.read_bytes()) ==
         "ccb87a64ddb36ed35af415dde2d9fcf0a3ed7f443934edf0a24c98f7bd3ab4da",
         "bridge hash")


def check_exact_algebra() -> None:
    need(Fraction(133, 400) - Fraction(1, 2) == Fraction(-67, 400),
         "divisor endpoint exponent")
    boundary = Fraction(1, 3) + 2 * Fraction(21, 32) - Fraction(1, 2)
    main = Fraction(2, 3) + Fraction(1, 2)
    unit = 1 + Fraction(1, 3) - Fraction(1, 2)
    need(boundary == Fraction(55, 48), "boundary exponent")
    need(main == Fraction(7, 6), "main exponent")
    need(unit == Fraction(5, 6), "unit exponent")
    need(main - boundary == Fraction(1, 48), "boundary gap")

    for ell in range(1, 33):
        for r in range(1, 33):
            rho2 = Fraction(ell * r, ell + r)
            reciprocal_identity = rho2 * (Fraction(1, ell) + Fraction(1, r)) ** 2
            need(reciprocal_identity == 1 / rho2, "rho identity")
            need(rho2 / (ell * ell) <= 1 / rho2, "left Haar height")
            need(rho2 / (r * r) <= 1 / rho2, "right Haar height")

    for start in range(-9, 28):
        for length in range(1, 37):
            end = start + length - 1
            for divisor in range(1, 20):
                count = end // divisor - (start - 1) // divisor
                need(abs(Fraction(count) - Fraction(length, divisor)) <= 1,
                     "interval divisor endpoint")

    for q in (3, 5, 7, 11, 13):
        for t in range(-2 * q, 2 * q + 1):
            if t % q == 0:
                continue
            for h in range(-3 * q, 3 * q + 1):
                u = t + h
                value = Fraction(0)
                if u % q != 0:
                    value = (Fraction(1) if h % q == 0 else Fraction(0)) - Fraction(1, q - 1)
                bound = Fraction(1) if h % q == 0 else Fraction(2, q)
                need(abs(value) <= bound, "combined unit-row bound")

    for split in range(-5, 18):
        for h in range(-25, 26):
            points = range(-30, 31)
            crossing = sum(1 for t in points if (t <= split) != (t + h <= split))
            need(crossing <= abs(h), "rank-boundary crossing count")


def child(path: Path, marker: bytes) -> bytes:
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)
    need(result.returncode == 0 and result.stderr == b"", "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def pdf_check() -> None:
    need(EXPECTED_PDF_PAGES > 0 and EXPECTED_PDF_FONTS > 0, "PDF constants unset")
    tools = [shutil.which(name) for name in ("pdftotext", "pdffonts", "pdfinfo")]
    need(all(tool is not None for tool in tools), "PDF tools")
    pdftotext, pdffonts, pdfinfo = tools
    text = subprocess.run([pdftotext, "-layout", str(PDF), "-"], capture_output=True, check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    need(b"Literal Beta Rank-Midpoint Asymptotics" in text.stdout, "PDF title")
    for marker in (
        b"TPC256_ARITHMETIC_ADVANCE", b"YES_SCOPED_LITERAL_BETA_ADJOINT_HAAR_LANE",
        b"TPC256_L2", b"NONE", b"TPC256_FULL_GATE_B", b"OPEN",
        b"TPC256_TWIN_PRIME_RESULT",
    ):
        need(marker in text.stdout, "PDF firewall")
    info = subprocess.run([pdfinfo, str(PDF)], capture_output=True, check=False)
    need(info.returncode == 0 and
         ("Pages:           " + str(EXPECTED_PDF_PAGES)).encode() in info.stdout,
         "PDF pages")
    fonts = subprocess.run([pdffonts, str(PDF)], capture_output=True, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = fonts.stdout.decode("ascii").splitlines()[2:]
    need(len(rows) == EXPECTED_PDF_FONTS, "PDF font count")
    for row in rows:
        columns = row.split()
        need(len(columns) >= 8 and columns[-5:-2] == ["yes", "yes", "yes"],
             "PDF fonts embedded")


def run() -> None:
    need(len(PROJECT_HASHES) == len(EXPECTED_FILES), "project hashes unset")
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*") if path.is_file()}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    need((actual & BUILD_INTERMEDIATES) in (set(), BUILD_INTERMEDIATES), "partial build files")
    for relative, expected in PROJECT_HASHES.items():
        path = PROJECT / relative
        need(path.is_file() and digest(path.read_bytes()) == expected, "project hash: " + relative)
    check_sources()
    check_exact_algebra()

    bridge = BRIDGE.read_text(encoding="utf-8")
    joined = bridge + "\n" + "\n".join(
        (PROJECT / relative).read_text(encoding="utf-8")
        for relative in ("README.md", "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md", "paper/main.tex")
    )
    for marker in MARKERS:
        need(marker in joined, "marker: " + marker)
    for required in (
        "log(32/27)", "55/48", "1/48", "H^2/q", "ordered-rank",
        "normalized phase", "principal argument", "output-unit",
    ):
        need(required in joined, "semantic marker: " + required)
    for script in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in script.read_text(encoding="utf-8"), "assert guard")
    independent_text = INDEPENDENT.read_text(encoding="utf-8")
    need("import tpc256_literal_beta_haar_certificate" not in independent_text,
         "independent checker imports producer")

    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, sort_keys=True, separators=(",", ":"),
                            ensure_ascii=True) + "\n").encode("ascii")
    need(raw == canonical and parsed.get("claim") == STATUS,
         "canonical certificate")
    need(parsed.get("schema") == "TPC256_CERTIFICATE_V1" and
         parsed.get("epistemic_status", {}).get("theorem") == "PROVED_SOURCE_BACKED" and
         parsed.get("numerical_observation", {}).get("proof_credit") == "NONE",
         "certificate epistemic firewall")
    need(parsed.get("firewall", {}).get("TPC256_ARITHMETIC_ADVANCE") ==
         "YES_SCOPED_LITERAL_BETA_ADJOINT_HAAR_LANE" and
         parsed.get("firewall", {}).get("TPC256_FULL_GATE_B") == "OPEN" and
         parsed.get("firewall", {}).get("TPC256_TWIN_PRIME_RESULT") == "NONE",
         "certificate route firewall")

    if BUILD_INTERMEDIATES <= actual:
        log = (PROJECT / "paper/paper.log").read_text(encoding="utf-8", errors="replace")
        for forbidden in ("LaTeX Warning", "Undefined control sequence", "Overfull", "Underfull"):
            need(forbidden not in log, "LaTeX log: " + forbidden)
    pdf_check()
    child(PRODUCER, b"TPC256_CERTIFICATE=PASS")
    child(INDEPENDENT, b"TPC256_INDEPENDENT_CHECK=PASS")
    child(STRESS, b"TPC256_STRESS=PASS")
    print("TPC256_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("pdf_pages=" + str(EXPECTED_PDF_PAGES))
    print("pdf_fonts=" + str(EXPECTED_PDF_FONTS) + "_EMBEDDED_SUBSETTED_UNICODE")
    print("arithmetic_advance=YES_SCOPED_LITERAL_BETA_ADJOINT_HAAR_LANE")
    print("boundary_gap=1_OVER_48")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    if not arguments.check:
        raise SystemExit("TPC256_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, OSError, UnicodeError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC256_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
