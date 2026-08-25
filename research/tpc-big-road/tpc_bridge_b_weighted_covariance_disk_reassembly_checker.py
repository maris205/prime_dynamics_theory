#!/usr/bin/env python3
"""Fail-closed release checker for TPC-246 weighted disk reassembly."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-246-weighted-covariance-disk-reassembly"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_weighted_covariance_disk_reassembly.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results/tpc246_certificate.json"
PRODUCER = PROJECT / "code/tpc246_weighted_disk_certificate.py"
PROOF_PACKAGE = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
INDEPENDENT = PROJECT / "experiments/tpc246_independent_checker.py"
STRESS = PROJECT / "experiments/tpc246_weighted_disk_stress.py"
MAIN_TEX = PROJECT / "paper/main.tex"
JOINT_GEOMETRY = PROJECT / "paper/sections/2_joint_geometry.tex"
EXACT_PROOF = PROJECT / "paper/sections/3_exact_reassembly.tex"
SOURCE_TRANSFER = PROJECT / "paper/sections/5_source_transfer.tex"
ROUTE_BOUNDARY = PROJECT / "paper/sections/7_route_boundary.tex"
COMPUTATIONAL_PROTOCOL = PROJECT / "notes/computational_protocol.md"
PDF = PROJECT / "paper/paper.pdf"

TEXT_LOCKS = {
    BRIDGE: "c395a4a49640f9b1b8a2eebf15afd1405d824a968c52c94d23e660f2414f2d80",
    README: "bdbddaf398de600690df49859f30e88aac8a161876d2f45db439c41d4d04d82a",
    CERTIFICATE: "7b6a85c425df5fb690b2938d264403d83320fa0f70c998f2a6db48796e270bd6",
    PRODUCER: "f39fd8d4b2b659a74426266ef59c96b8ccd0a42695d011594875e78b906514be",
    PROOF_PACKAGE: "b47f9aca13c12eaec4de58d1787b1f7cd126b08db08425bad1b9e14fe455cf41",
    DERIVATION: "4d0da6f182898b9d67396f20f33f3c40172f7fd67b8130cc104c194618519762",
    INDEPENDENT: "4d1d2db70701ee5ca3d51ff45658899c8701cb49c34246acfe12ba369395fb5c",
    STRESS: "82664087872147aa3efd2a1d2a6de11593ca2a194a0ac83b4fce06d36cdc88ec",
    MAIN_TEX: "10d0c7a5483e18e2246f1ad4388f2ce3884a13b01081bc247be5e545a3e93165",
    JOINT_GEOMETRY: "f588f4f48b1face54973cec11f19e5b263cc73f2d20b75211cb0ca926b1e0488",
    EXACT_PROOF: "612ce2f939f43543d71df00707b1ceaaeb0f53b7b949f700465417f38fbc0781",
    SOURCE_TRANSFER: "d3f3a48213d80912e8101fddf8618e475958b086d3de7d74856971153d584172",
    ROUTE_BOUNDARY: "2cb8aef2dfa42f9d58518568cc909b7cc5e81c6fa2cc670d2e0dbad7973ef2a1",
    COMPUTATIONAL_PROTOCOL: "a056010bf840e54ec055a478730d8da299323ff6a38861ba87a59f07545e0904",
}
PDF_RAW_SHA256 = "18e9f2c50dfaff35953be9d8f439a5d32ae0ce6bdfedb27d2c498dbd1ad49c54"
PAYLOAD_SHA256 = "06cb3544b74674e7dcc6a7748d87d8d6d00109460af319fdd77a532210290f0f"

STATUS = "PROVED_STRUCTURAL_L1_WEIGHTED_COVARIANCE_DISK_REASSEMBLY"
MARKERS = (
    "TPC246_WEIGHTED_DISK_IDENTITY = PROVED_EXACT",
    "TPC246_COUPLED_FAMILY_CONTAINMENT = PROVED",
    "TPC246_REVERSE_REALIZATION = PROVED_EXPLICIT",
    "TPC246_AGGREGATE_ZERO_CRITERION = PROVED_EXACT",
    "TPC246_COMMON_MULTIPLIER_SPECIALIZATION = PROVED_STRUCTURAL",
    "TPC246_HARD_WINDOW_RADIUS_INFLATION = PROVED_CONDITIONAL_ON_ATTACHMENT",
    "TPC246_HARD_WINDOW_IMAGE_EXACTNESS = NOT_CLAIMED",
    "TPC246_POSITIVE_RADIUS_CIRCLE_AS_DISK = FORBIDDEN",
    "TPC246_ARBITRARY_COMPLEX_WEIGHT_AS_COMMON_MULTIPLIER = FORBIDDEN",
    "TPC246_INDEPENDENT_SOURCE_REALIZABILITY = OPEN",
    "TPC246_LITERAL_V59_TWO_LANE_ATTACHMENT = OPEN",
    "TPC246_CANONICAL_BLOCK_DIRECTIONS = OPEN",
    "TPC246_PAYABLE_ARITHMETIC_MARGIN = OPEN",
    "TPC246_ARITHMETIC_ADVANCE = NO",
    "TPC246_FIXED_ATOM_CREDIT = 0",
    "TPC246_L2 = NONE",
    "TPC246_FULL_GATE_B = OPEN",
    "TPC246_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC246_TWIN_PRIME_RESULT = NONE",
    "TPC246_STATUS = " + STATUS,
)
EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc246_weighted_disk_certificate.py",
    "experiments/tpc246_independent_checker.py",
    "experiments/tpc246_weighted_disk_stress.py", "notes/citation_verification.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/source_lock.md", "notes/theorem_ledger.md",
    "paper/main.tex", "paper/math_commands.tex", "paper/paper.pdf",
    "paper/references.bib", "paper/sections/0_abstract.tex",
    "paper/sections/1_introduction.tex", "paper/sections/2_joint_geometry.tex",
    "paper/sections/3_exact_reassembly.tex",
    "paper/sections/4_sharp_corollaries.tex",
    "paper/sections/5_source_transfer.tex", "paper/sections/6_certificate.tex",
    "paper/sections/7_route_boundary.tex", "paper/sections/8_conclusion.tex",
    "paper/sections/A_status_ledger.tex", "results/tpc246_certificate.json",
}


class CheckFailure(RuntimeError):
    """Fail-closed release-check error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical_text_hash(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def raw_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_producer():
    spec = importlib.util.spec_from_file_location("tpc246_producer", PRODUCER)
    require(spec is not None and spec.loader is not None, "producer module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def same_typed(candidate: object, expected: object) -> bool:
    if type(candidate) is not type(expected):
        return False
    if type(expected) is dict:
        return candidate.keys() == expected.keys() and all(
            same_typed(candidate[key], expected[key]) for key in expected
        )
    if type(expected) is list:
        return len(candidate) == len(expected) and all(
            same_typed(left, right) for left, right in zip(candidate, expected)
        )
    return candidate == expected


def verify_pdf() -> None:
    pdftotext = shutil.which("pdftotext")
    pdffonts = shutil.which("pdffonts")
    require(pdftotext is not None and pdffonts is not None, "PDF tools unavailable")
    plain = subprocess.run([pdftotext, "-layout", str(PDF), "-"],
                           capture_output=True, check=False)
    require(plain.returncode == 0 and plain.stderr == b"", "plain PDF extraction")
    bad_controls = [value for value in plain.stdout
                    if value < 32 and value not in (9, 10, 12, 13)]
    require(not bad_controls, "PDF text layer contains semantic C0 controls")
    require(b"Weighted Covariance-Disk Reassembly" in plain.stdout and
            b"Hard-Window Margins" in plain.stdout, "PDF title marker")
    require(b"Maximum claim" in plain.stdout and
            b"WEIGHTED_DISK_REASSEMBLY" in plain.stdout, "PDF claim marker")
    lowered = plain.stdout.lower()
    require(b"blockwise product realizability" in lowered and
            b"no twin-prime conclusion" in lowered, "PDF claim boundary")
    bbox = subprocess.run([pdftotext, "-bbox-layout", str(PDF), "-"],
                          capture_output=True, check=False)
    require(bbox.returncode == 0 and bbox.stderr == b"", "bbox extraction")
    try:
        root = ElementTree.fromstring(bbox.stdout)
    except ElementTree.ParseError as error:
        raise CheckFailure("bbox PDF text is not strict XML") from error
    require(len(root.findall(".//{*}page")) == 5, "PDF page count")
    fonts = subprocess.run([pdffonts, str(PDF)], capture_output=True, check=False)
    require(fonts.returncode == 0 and fonts.stderr == b"", "pdffonts execution")
    rows = fonts.stdout.decode("ascii", errors="strict").splitlines()[2:]
    require(len(rows) == 17, "font row count")
    for row in rows:
        columns = row.split()
        require(len(columns) >= 8 and columns[-5:-2] == ["yes", "yes", "yes"],
                "font embedding/subset/Unicode")


def run_child(script: Path, expected_marker: str) -> None:
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend(["-B", str(script), "--check"])
    result = subprocess.run(command, cwd=PROJECT, capture_output=True, check=False)
    require(result.returncode == 0 and result.stderr == b"", "child checker: " + script.name)
    require(expected_marker.encode("ascii") in result.stdout,
            "child output marker: " + script.name)


def run() -> None:
    actual_files = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
                    if path.is_file()}
    require(actual_files == EXPECTED_FILES, "project file manifest mismatch")
    for path, expected_hash in TEXT_LOCKS.items():
        require(path.is_file() and canonical_text_hash(path) == expected_hash,
                "text lock mismatch: " + str(path))
    require(PDF.is_file() and raw_hash(PDF) == PDF_RAW_SHA256,
            "raw PDF lock mismatch")
    verify_pdf()

    bridge = BRIDGE.read_text(encoding="utf-8")
    for marker in MARKERS:
        require(marker in bridge, "bridge marker missing: " + marker)
    joined = "\n".join(path.read_text(encoding="utf-8") for path in
                         (README, PROOF_PACKAGE, DERIVATION, JOINT_GEOMETRY,
                          EXACT_PROOF, SOURCE_TRANSFER, ROUTE_BOUNDARY))
    require("complete Cartesian product" in joined and
            "Coupled-family enclosure" in joined, "product/containment split")
    require("conjugate(lambda_h)/|lambda_h|" in joined and
            "fills" not in bridge.split("hard-window transfer")[-1].lower(),
            "reverse construction / physical exactness")
    require("annulus" in joined and "not the radius-three disk" in joined,
            "circle counterexample")
    require("one factor of" in joined and "sufficient, not necessary" in joined,
            "single-transfer boundary")

    producer = load_producer()
    raw = CERTIFICATE.read_bytes()
    stored = producer.strict_json_loads(raw.decode("ascii"))
    expected = producer.build_document()
    require(same_typed(stored, expected), "certificate payload mismatch")
    require(raw == producer.canonical_json(stored) + b"\n",
            "certificate canonical bytes")
    require(stored["payload_sha256"] == PAYLOAD_SHA256, "payload digest lock")
    require(type(stored["certificate_version"]) is int and
            stored["certificate_version"] == 1, "certificate version type")
    firewall = stored["payload"]["scope_firewall"]
    require(firewall["ARITHMETIC_ADVANCE"] == "NO" and
            firewall["ARITHMETIC_L2"] == "NONE", "arithmetic firewalls")
    require(type(firewall["FIXED_ATOM_CREDIT"]) is int and
            firewall["FIXED_ATOM_CREDIT"] == 0, "fixed atom exact type")

    independent_source = INDEPENDENT.read_text(encoding="utf-8")
    producer_source = PRODUCER.read_text(encoding="utf-8")
    require("import tpc246_weighted_disk_certificate" not in independent_source and
            "from tpc246_weighted_disk_certificate" not in independent_source,
            "independent checker imports producer")
    require("assert " not in producer_source and "assert " not in independent_source,
            "assert-based theorem guard")
    require("digest_rebound_mutations_rejected=16/16" in independent_source,
            "mutation-census marker")
    stress_source = STRESS.read_text(encoding="utf-8")
    require("itertools.product" in stress_source and "reverse_disk_targets=27" in stress_source,
            "stress census computed")

    run_child(PRODUCER, "TPC246_CERTIFICATE=PASS")
    run_child(INDEPENDENT, "TPC246_INDEPENDENT_CHECK=PASS")
    run_child(STRESS, "TPC246_WEIGHTED_DISK_STRESS=PASS")

    print("TPC246_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("coupled_family=CONTAINMENT")
    print("cartesian_product=EXACT_DISK")
    print("explicit_reverse_realization=PASS")
    print("hard_window_image=CONTAINMENT_ONLY")
    print("robust_margin=STRICT_SUFFICIENT")
    print("pdf_pages=5")
    print("pdf_fonts=17_EMBEDDED_SUBSETTED_UNICODE")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC246_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError,
            UnicodeError) as error:
        raise SystemExit("TPC246_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
