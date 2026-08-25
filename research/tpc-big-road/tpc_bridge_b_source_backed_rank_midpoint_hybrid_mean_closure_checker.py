#!/usr/bin/env python3
"""Fail-closed release checker for TPC-254."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_source_backed_rank_midpoint_hybrid_mean_closure.md"
README = PROJECT / "README.md"
PLAN = PROJECT / "PAPER_PLAN.md"
PROOF = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
PRODUCER = PROJECT / "code/tpc254_midpoint_hybrid_mean_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc254_independent_checker.py"
STRESS = PROJECT / "experiments/tpc254_midpoint_hybrid_mean_stress.py"
CERTIFICATE = PROJECT / "results/tpc254_certificate.json"
MAIN = PROJECT / "paper/main.tex"
PDF = PROJECT / "paper/paper.pdf"
REFERENCES = PROJECT / "paper/references.bib"
PROTOCOL = PROJECT / "notes/computational_protocol.md"
STATUS = (
    "PROVED_SOURCE_BACKED_L1_RANK_MIDPOINT_HYBRID_MEAN_CLOSURE_"
    "WITH_ADJOINT_LANE_SOURCE_GAP"
)

HASHES = {
    BRIDGE: "6e5cb92642bf8fc8f0a3a56a29c4c061359f3794e24345d76a62d2fccf5a21ee",
    PROJECT / ".gitignore": "ed82d323efd7bb6c7fe2b80f492770f6d8903f983f94d7a8395734f3c641e5fd",
    DERIVATION: "6368dfb1369b315d67bae23d1768ef1edf6b0462577f920c472b7a1397c7178b",
    PLAN: "7c9ca4e9d6c1b11286fa718cbd482485716be3f11c1bbaf618bcd22996fc7219",
    PROOF: "bb23c4dfc5cced89b34db0d2741b570c07335ac9aa153ae123d056f29924b768",
    README: "2342cac6919e9db9e4e66547373cc3c98166ad03b2d3c41959848ee517615ce2",
    PRODUCER: "308786989cb8c7c02e68bc1ec99038aeb2a6123b00258531669fccba17cf6b37",
    INDEPENDENT: "d8468a6021202e9132d3281c2e07491af30938584b5df706ff8ff2578c4ff301",
    STRESS: "e239350c99b6c8187ca02645cfa7386b7c4d36e9bb060933264d992d95d02ff4",
    PROJECT / "notes/citation_verification.md": "4370c82b107ccbbd594cd7ffacefe655c109c22528608e0fed3b01c66fa40138",
    PROJECT / "notes/claim_firewall.md": "728c0a7e87e5071edf871507667c313a4e8db9b7ecc802c0415b243286113934",
    PROTOCOL: "1ccfa32356880ed53cb11b62a0329ade8ad9e5efb37ac9308d54dcc89f3280b5",
    PROJECT / "notes/route_evaluation.md": "1fe5e47a6dd11e3deec1112e0be192d94295f045bda4f0bc66809134cdfa5fba",
    PROJECT / "notes/source_lock.md": "f7dd363a51361e3c1e13eacc932513a61e7ffaf8788ba46372437afa5a94106d",
    PROJECT / "notes/theorem_ledger.md": "ea138a0cd5839bdb62633a38389f82a4e6f4346641757b05729722daec89aa2b",
    MAIN: "5d1bb10430c3f56e720e62c5d58a018a2c56d7b771eb815d4e8a1127555150a6",
    PDF: "7fefe585dfffb185218eae4a400abd5e772467442eb75667ddf9dcb3fc9fa3d3",
    REFERENCES: "279d307eacdb0e2ca70c88b683dc85e832c8a17cc37f89d4e5986c49b58e466b",
    CERTIFICATE: "d9129d421ec6afd017e0ab2de4530c5835df9b58c7ea5a973fe64fe68459b796",
}

EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc254_midpoint_hybrid_mean_certificate.py",
    "experiments/tpc254_independent_checker.py",
    "experiments/tpc254_midpoint_hybrid_mean_stress.py",
    "notes/citation_verification.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/source_lock.md", "notes/theorem_ledger.md", "paper/main.tex",
    "paper/paper.pdf", "paper/references.bib", "results/tpc254_certificate.json",
}

BUILD_INTERMEDIATES = {
    "paper/paper.aux", "paper/paper.bbl", "paper/paper.blg",
    "paper/paper.log", "paper/paper.out",
}

MARKERS = (
    "TPC254_MAXIMUM_CLAIM = SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER_CONTROL_OF_THE_LITERAL_V59_RANK_MIDPOINT_W_CONTRAST_WITH_ONLY_EXACT_ADJOINT_CAUCHY_TRANSFER",
    "TPC254_HYBRID_CUTOFF = SOURCE_LOCKED_FIXED_FINITE_K_NO_K_UNIFORMITY",
    "TPC254_RANK_CHILD_INTERVAL_ADMISSIBILITY = PROVED_EXACT_FOR_REAL_X",
    "TPC254_MAXIMAL_TYPE_I_M1_EXTRACTION = PROVED_SOURCE_BACKED",
    "TPC254_CHILD_SUM_HYBRID_MEAN = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER",
    "TPC254_CHILD_MEAN_DIFFERENCE = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER",
    "TPC254_W_MIDPOINT_HAAR_MOMENT = PROVED_SOURCE_BACKED_X_ONE_HALF_TIMES_ARBITRARY_FIXED_LOG_SAVING",
    "TPC254_SAFE_ADJOINT_CAUCHY_TRANSFER = PROVED_EXACT",
    "TPC254_G_MIDPOINT_HAAR_ESTIMATE = OPEN_NO_FROZEN_SOURCE_ATTACHMENT",
    "TPC254_G_LANE_SOURCE_ATTACHMENT = STOP_SCOPED_DECLARED_CORPUS_NO_FIXED_HAAR_ADJOINT_ESTIMATE",
    "TPC254_ZERO_DIAGONAL_DERANGEMENT_OBSTRUCTION = PROVED_SYNTHETIC_NOT_LITERAL_V59",
    "TPC254_CAUCHY_CONSTANT_ONE_SHARPNESS = PROVED_EXACT_N2_SYNTHETIC",
    "TPC254_ARBITRARY_LOG_TO_FIXED_POWER_PROMOTION = NOT_CLAIMED",
    "TPC254_W_CONTRAST_SIGN_OR_NONZERO = NOT_CLAIMED",
    "TPC254_G_CONTRAST_SIGN_OR_NONZERO = OPEN",
    "TPC254_JOINT_TRANSFER_LOWER_BOUND = OPEN",
    "TPC254_V21_CHILD_OR_ADJOINT_SUBSTITUTION = NOT_CLAIMED",
    "TPC254_ARITHMETIC_ADVANCE = YES_SCOPED_LITERAL_W_LANE",
    "TPC254_FIXED_ATOM_CREDIT = 0",
    "TPC254_L2 = NONE",
    "TPC254_FULL_GATE_B = OPEN",
    "TPC254_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC254_TWIN_PRIME_RESULT = NONE",
    "TPC254_STATUS = " + STATUS,
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
    need(result.stdout.startswith(marker.encode("ascii")), "child marker: " + path.name)


def certificate_check() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw.decode("utf-8"))
    canonical = (
        json.dumps(document, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")
    need(raw == canonical, "canonical JSON")
    need(type(document) is dict and type(document.get("payload")) is dict,
         "certificate schema")


def pdf_check() -> None:
    commands = [shutil.which(name) for name in ("pdftotext", "pdffonts", "pdfinfo")]
    need(all(command is not None for command in commands), "PDF tools")
    pdftotext, pdffonts, pdfinfo = commands
    text_result = subprocess.run(
        [pdftotext, "-layout", str(PDF), "-"], capture_output=True, check=False
    )
    need(text_result.returncode == 0 and text_result.stderr == b"", "PDF text")
    need(b"Source-Backed Rank-Midpoint Hybrid-Mean Closure" in text_result.stdout and
         b"Adjoint-Lane Source Gap" in text_result.stdout, "PDF title")
    need(b"not a fixed power saving" in text_result.stdout and
         b"no twin-prime result follows" in text_result.stdout and
         b"Gate B: open" in text_result.stdout, "PDF claim firewall")
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
    joined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (README, PLAN, PROOF, DERIVATION, MAIN)
    )
    need("gamma_0=1/4" in joined and "m=1" in joined and
         "tau(1)^B=1" in joined, "nonnegative m=1 extraction")
    need("N=x/2+O(1)" in joined and "rho^2=N/4" in joined and
         "nonintegral" in joined, "real-clock rank and parity ledger")
    need("x^(1/2)(log x)^(-M)" in joined and
         "not a fixed power saving" in joined, "log-saving firewall")
    need("<z_mid,A_x beta>=<A_x^*z_mid,beta>" in joined and
         "||A_x^*z_mid||_2||beta||_2" in joined, "safe adjoint transfer")
    need("synthetic" in joined and "not literal V59" in joined and
         "no twin-prime result" in joined, "scope firewall")
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"), "assert guard")
    independent = INDEPENDENT.read_text(encoding="utf-8")
    need("import tpc254_midpoint_hybrid_mean_certificate" not in independent and
         "from tpc254_midpoint_hybrid_mean_certificate" not in independent,
         "independent imports producer")
    need("type(value) is not int" in independent and
         "fixture_count_bool" in independent, "strict integer and bool firewall")
    if BUILD_INTERMEDIATES <= actual:
        log = (PROJECT / "paper/paper.log").read_text(encoding="utf-8", errors="replace")
        for forbidden in ("LaTeX Warning", "Undefined control sequence", "Overfull", "Underfull"):
            need(forbidden not in log, "LaTeX log: " + forbidden)
    certificate_check()
    pdf_check()
    child(PRODUCER, "TPC254_CERTIFICATE=PASS")
    child(INDEPENDENT, "TPC254_INDEPENDENT_CHECK=PASS mutations_rejected=82")
    child(STRESS, "TPC254_STRESS=PASS families=192")
    print("TPC254_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("pdf_pages=4")
    print("pdf_fonts=27_EMBEDDED_SUBSETTED_UNICODE")
    print("arithmetic_advance=YES_SCOPED_LITERAL_W_LANE")
    print("adjoint_lane=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC254_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError, json.JSONDecodeError) as error:
        raise SystemExit("TPC254_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
