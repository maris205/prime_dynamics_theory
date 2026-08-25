#!/usr/bin/env python3
"""Fail-closed release checker for TPC-249."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-249-sharp-weighted-shared-lane-contraction"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_sharp_weighted_shared_lane_contraction.md"
README = PROJECT / "README.md"
PROOF = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
PRODUCER = PROJECT / "code/tpc249_weighted_contraction_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc249_independent_checker.py"
STRESS = PROJECT / "experiments/tpc249_weighted_contraction_stress.py"
CERTIFICATE = PROJECT / "results/tpc249_certificate.json"
MAIN = PROJECT / "paper/main.tex"
PDF = PROJECT / "paper/paper.pdf"
PROTOCOL = PROJECT / "notes/computational_protocol.md"
STATUS = "PROVED_STRUCTURAL_L1_SHARP_WEIGHTED_SHARED_LANE_CONTRACTION"

HASHES = {
    BRIDGE: "74485407966ae20b5f175fb9e788109999a191b340e43d41d251764fe028cc3a",
    README: "642489977693adfa0af9aa7d433615831e8f96eb6c19dc90a60138867b4c42e9",
    PROOF: "3fb400a90a41310c164bfb644a3668343fed7f4430ed99b7335493a0975c9b64",
    DERIVATION: "1a24ed6aa2b74c48c7e48afa6f0397d14ebb77f6eaa5352da70a3d993296d09a",
    PRODUCER: "0cde0f7bd64c24c7bb32d9f8bbdf955f2f668da859e8f0e9bafc264373cfc5ce",
    INDEPENDENT: "131da9fc06ccf7f563caaab69f9401428c7f83587f52ed19fa79589a61cf65a0",
    STRESS: "e587f573bca1e7df4b9337c1599ace8ba02618471edf9a5aebaebad568760d25",
    CERTIFICATE: "461a210e1ec33f21ac6c4349cf5fe23454d6f4124e301edb8404d631b94cda73",
    MAIN: "6d8846f878b7ff3b54b0964264d31d31e246687bc9d758254b7676b4f546cc8a",
    PDF: "4e00ae77e8debd8b40584bc29a034757158a2d2065c662c2ce4e966158965995",
    PROTOCOL: "79afefb4003df56a4eeb383f1e653492e2f802793dda9e35b4cbd47756ef744f",
}

EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc249_weighted_contraction_certificate.py",
    "experiments/tpc249_independent_checker.py",
    "experiments/tpc249_weighted_contraction_stress.py",
    "notes/citation_verification.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/source_lock.md", "notes/theorem_ledger.md", "paper/main.tex",
    "paper/paper.pdf", "paper/references.bib", "results/tpc249_certificate.json",
}

MARKERS = (
    "TPC249_LITERAL_WEIGHTED_PROBE_CONTRACTION = PROVED_EXACT",
    "TPC249_INDEPENDENT_BALL_AGGREGATE_IMAGE = PROVED_EXACT_DISK",
    "TPC249_GRAM_RADIUS = PROVED_EXACT",
    "TPC249_EXPLICIT_REVERSE_REALIZATION = PROVED_EXACT",
    "TPC249_AFFINE_CENTER_TRANSLATION = PROVED_FOR_DECLARED_MODELING_CHOICE",
    "TPC249_GLOBAL_BUDGET_RADIUS = PROVED_EXACT_DIRECT_SUM_SUPPORT",
    "TPC249_TAGGED_RADIUS_DOMINANCE = PROVED_EXACT",
    "TPC249_TAGGED_RADIUS_EQUALITY = PROVED_IFF_COMMON_NONNEGATIVE_RAY_PER_ACTIVE_GROUP",
    "TPC249_REPEATED_PROBE_CANCELLATION = PROVED_EXACT",
    "TPC249_ACTUAL_GRAM_ASYMPTOTIC = OPEN",
    "TPC249_ARITHMETIC_ADVANCE = NO",
    "TPC249_L2 = NONE",
    "TPC249_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC249_TWIN_PRIME_RESULT = NONE",
    "TPC249_STATUS = " + STATUS,
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
    text = subprocess.run([pdftotext, "-layout", str(PDF), "-"],
                          capture_output=True, check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    need(b"Sharp Weighted Contraction" in text.stdout and
         b"Shared Gram Lanes" in text.stdout, "PDF title")
    need(b"Maximum claim" in text.stdout and
         b"SHARP_WEIGHTED_SHARED_LANE_CONTRACTION" in text.stdout, "PDF claim")
    need(b"ARITHMETIC_L2=NONE" in text.stdout and
         b"FULL_GATE_B=OPEN" in text.stdout, "PDF firewall")
    info = subprocess.run([pdfinfo, str(PDF)], capture_output=True, check=False)
    need(info.returncode == 0 and info.stderr == b"" and
         b"Pages:           4" in info.stdout, "PDF pages")
    fonts = subprocess.run([pdffonts, str(PDF)], capture_output=True, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = fonts.stdout.decode("ascii").splitlines()[2:]
    need(len(rows) == 20, "font rows")
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
    need("g_c=sum" in joined and "tagged" in joined.lower(), "weighted prose")
    need("modeling choice" in joined.lower() and "common nonnegative" in joined.lower(),
         "boundary/equality prose")
    need("assert " not in PRODUCER.read_text(encoding="utf-8") and
         "assert " not in INDEPENDENT.read_text(encoding="utf-8"), "assert guard")
    independent = INDEPENDENT.read_text(encoding="utf-8")
    need("import tpc249_weighted_contraction_certificate" not in independent and
         "from tpc249_weighted_contraction_certificate" not in independent,
         "independent imports producer")
    pdf_check()
    child(PRODUCER, "TPC249_CERTIFICATE=PASS")
    child(INDEPENDENT, "TPC249_INDEPENDENT_CHECK=PASS")
    child(STRESS, "TPC249_WEIGHTED_CONTRACTION_STRESS=PASS")
    print("TPC249_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("pdf_pages=4")
    print("pdf_fonts=20_EMBEDDED_SUBSETTED_UNICODE")
    print("exact_radius=SUM_RHO_SQRT_LAMBDA_STAR_G_LAMBDA")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC249_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError) as error:
        raise SystemExit("TPC249_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
