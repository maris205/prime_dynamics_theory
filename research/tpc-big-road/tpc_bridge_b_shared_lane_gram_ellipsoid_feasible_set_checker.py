#!/usr/bin/env python3
"""Fail-closed release checker for TPC-248."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-248-shared-lane-gram-ellipsoid-feasible-set"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_shared_lane_gram_ellipsoid_feasible_set.md"
README = PROJECT / "README.md"
PROOF = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
PRODUCER = PROJECT / "code/tpc248_gram_ellipsoid_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc248_independent_checker.py"
STRESS = PROJECT / "experiments/tpc248_gram_ellipsoid_stress.py"
CERTIFICATE = PROJECT / "results/tpc248_certificate.json"
MAIN = PROJECT / "paper/main.tex"
PDF = PROJECT / "paper/paper.pdf"
PROTOCOL = PROJECT / "notes/computational_protocol.md"
STATUS = "PROVED_STRUCTURAL_L1_SHARED_LANE_GRAM_ELLIPSOID_FEASIBLE_SET"

HASHES = {
    BRIDGE: "4fe1bcf2a753da0f942e43ee7c9f569d90a36b8d55f51183b7ba06da6fb1f725",
    README: "453e283cffe7069d035da603bb56889d2041708136ff1b4f7e0e7de247fcd805",
    PROOF: "efad80840fa1378914cabb3f3793000efbbe47a0d59f84bf9767643a471c06e3",
    DERIVATION: "772d44fe2e65866b96b2fd9284faeafea6c3606fd38d2c7cedd647240a02a879",
    PRODUCER: "68543d77fbbf020ee0877313ea8cb8272f04a39a858beeda63c953fae6b4db98",
    INDEPENDENT: "fd52f5700eeaebba9a398b63e02c192b4bdd13a5720693806388783d1a72a95b",
    STRESS: "4eb73fb7df92a65ffd5e15093a589edfb9ce44ca0ad8edd13afc5889c0c74d67",
    CERTIFICATE: "86b8880dcc0589b59318799644d52ada5e8140cc69ab1aceaeb2688c7cdd36b3",
    MAIN: "8715071252050013628ef4770d857d2e49d23aacf49bb2d9f2b4298c7887ce82",
    PDF: "883bbd66fdb7887aa772ca07f60962281fb7615c6c5fd241616aee853e5f3aec",
    PROTOCOL: "75eb61c0c13a3be955dbe81a1d5e9ad61f94a14ad580423e719ac705e1ee4fc8",
}

EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc248_gram_ellipsoid_certificate.py",
    "experiments/tpc248_gram_ellipsoid_stress.py",
    "experiments/tpc248_independent_checker.py", "notes/citation_verification.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/source_lock.md", "notes/theorem_ledger.md",
    "paper/main.tex", "paper/paper.pdf", "paper/references.bib",
    "results/tpc248_certificate.json",
}

MARKERS = (
    "TPC248_SHARED_LANE_SOURCE_LOCK = PROVED_EXACT_FROM_TPC247",
    "TPC248_BALL_IMAGE = PROVED_EXACT_GRAM_ELLIPSOID",
    "TPC248_MINIMUM_NORM_PREIMAGE = PROVED_EXACT",
    "TPC248_SPHERE_IMAGE_WITH_SLACK = PROVED_EXACT_SOLID_ELLIPSOID",
    "TPC248_SPHERE_IMAGE_WITHOUT_SLACK = PROVED_EXACT_BOUNDARY_SHELL",
    "TPC248_PHYSICAL_CONJUGATE_ORIENTATION = PROVED_EXACT",
    "TPC248_CARTESIAN_GROUP_PRODUCT = PROVED_FOR_DECLARED_PRODUCT_DOMAIN",
    "TPC248_CARTESIAN_PRODUCT_FROM_MARGINALS = UNJUSTIFIED",
    "TPC248_GLOBAL_NORM_BUDGET = PROVED_EXACT_COUPLED_ELLIPSOID",
    "TPC248_POLYDISK_PROMOTION = REFUTED_SCOPED",
    "TPC248_ARITHMETIC_ADVANCE = NO",
    "TPC248_L2 = NONE",
    "TPC248_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC248_TWIN_PRIME_RESULT = NONE",
    "TPC248_STATUS = " + STATUS,
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
    pdfinfo = shutil.which("pdfinfo")
    need(pdftotext is not None and pdffonts is not None and pdfinfo is not None,
         "PDF tools")
    text = subprocess.run([pdftotext, "-layout", str(PDF), "-"],
                          capture_output=True, check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    need(b"Shared-Lane Gram Ellipsoids" in text.stdout and
         b"Exact Joint Covariance Geometry" in text.stdout, "PDF title")
    need(b"Maximum claim" in text.stdout and
         b"SHARED_LANE_GRAM_ELLIPSOID_FEASIBLE_SET" in text.stdout,
         "PDF maximum claim")
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
    need("shared lane" in joined.lower() and "gram" in joined.lower() and
         "pseudoinverse" in joined.lower(), "shared Gram prose")
    need("bidisk" in joined.lower() and "global" in joined.lower(),
         "joint obstruction prose")
    need("assert " not in PRODUCER.read_text(encoding="utf-8") and
         "assert " not in INDEPENDENT.read_text(encoding="utf-8"), "assert guard")
    independent = INDEPENDENT.read_text(encoding="utf-8")
    need("import tpc248_gram_ellipsoid_certificate" not in independent and
         "from tpc248_gram_ellipsoid_certificate" not in independent,
         "independent imports producer")
    pdf_check()
    child(PRODUCER, "TPC248_CERTIFICATE=PASS")
    child(INDEPENDENT, "TPC248_INDEPENDENT_CHECK=PASS")
    child(STRESS, "TPC248_GRAM_ELLIPSOID_STRESS=PASS")
    print("TPC248_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("pdf_pages=4")
    print("pdf_fonts=20_EMBEDDED_SUBSETTED_UNICODE")
    print("shared_lane_joint_set=GRAM_ELLIPSOID")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC248_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError) as error:
        raise SystemExit("TPC248_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
