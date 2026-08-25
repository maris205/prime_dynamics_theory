#!/usr/bin/env python3
"""Fail-closed release checker for TPC-245 covariance disks."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-245-sharp-longitudinal-transverse-covariance-disks"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_sharp_longitudinal_transverse_covariance_disks.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results/tpc245_certificate.json"
PRODUCER = PROJECT / "code/tpc245_covariance_disk_certificate.py"
PROOF_PACKAGE = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
INDEPENDENT = PROJECT / "experiments/tpc245_independent_checker.py"
STRESS = PROJECT / "experiments/tpc245_covariance_disk_stress.py"
MAIN_TEX = PROJECT / "paper/main.tex"
CLASSIFICATION_PROOF = PROJECT / "paper/sections/4_proof.tex"
COROLLARIES = PROJECT / "paper/sections/5_sharp_corollaries.tex"
ROUTE_BOUNDARY = PROJECT / "paper/sections/7_route_boundary.tex"
COMPUTATIONAL_PROTOCOL = PROJECT / "notes/computational_protocol.md"
PDF = PROJECT / "paper/paper.pdf"

TEXT_LOCKS = {
    BRIDGE: "9fb4cb67b7c157666b0ad148f223e44c9f3c0e1b900df93373cea1bcbcef9129",
    README: "243fa87ed6ae9cc14e84a34b70cff6595a8f9c005853392d7822ccf1696a0648",
    CERTIFICATE: "d37fb776f80f6bacc8f2c151610d37b1e0d8bdf9ba911c10a707426f7f324bd3",
    PRODUCER: "aed69d977d191b15aeecb0a5812a8fba1fc70d54b84bbfd0f351432595344b30",
    PROOF_PACKAGE: "fca7b77605202974e5b87178a1540625058e54feaab27babd3a1267084745413",
    DERIVATION: "148ac7a28efccb10f76f09d12f92ebc9743dad011acc6be4029751d2a19ed94e",
    INDEPENDENT: "d7849f05b73316a02db947fc1274ce621c8a91948eefb771b8adf2eca913e36d",
    STRESS: "dd360493caf052054daeb1dcb4edb4bf9118ebb6774cfe0d8f33283fb09b23fa",
    MAIN_TEX: "df78be47f3f5ad6260bb38a96644cc0706603eb9d27a678d9c9972ed1ebaa577",
    CLASSIFICATION_PROOF: "7837f952355011c6da41d851763c1d3641ca288acce51b68a0e4053dccbe126b",
    COROLLARIES: "91aec0317a1ae703f4230010511a0263247c388fe09268566943a3dba681ae57",
    ROUTE_BOUNDARY: "f9ed85daebb9c2e201ed60d7e40ec28ec876b70f16f31af436d95779b6130673",
    COMPUTATIONAL_PROTOCOL: "50fc6edd1913a7bd4185999fc6ebef7a83594676ee8b0944d02ccb3e48e82dae",
}
PDF_RAW_SHA256 = "1493bd4eaa5a8d8149dabf7026f7441b148ed787bed412b9cb3d9239f70a9241"
PAYLOAD_SHA256 = "dbd271942b18afebd2d25fb6b3a4237f641c73ed0093e37dca5ac96b2422b702"

STATUS = "PROVED_STRUCTURAL_L1_SHARP_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISKS"
MARKERS = (
    "TPC245_EXACT_DECOMPOSITION = PROVED_CENTER_PLUS_TRANSVERSE_COVARIANCE",
    "TPC245_DIM_GE_2_FEASIBLE_SET = PROVED_CLOSED_DISK",
    "TPC245_DIM_EQ_1_FEASIBLE_SET = PROVED_CIRCLE_OR_SINGLETON",
    "TPC245_DIM_EQ_0_FEASIBLE_SET = PROVED_SINGLETON_OR_UNREALIZABLE",
    "TPC245_ZERO_FEASIBILITY = PROVED_DIMENSION_SENSITIVE",
    "TPC245_MINIMUM_MODULUS = PROVED_EXACT",
    "TPC245_PHASE_SECTOR = PROVED_SHARP_WHEN_RADIUS_LT_CENTER",
    "TPC245_TPC219_RELATION = PROJECTION_LINEAGE_ONLY_NOT_LITERAL_OBJECT_IDENTITY",
    "TPC245_CANONICAL_BLOCK_DIRECTION = OPEN",
    "TPC245_LITERAL_V59_TWO_LANE_ATTACHMENT = OPEN",
    "TPC245_ARITHMETIC_ADVANCE = NO",
    "TPC245_FIXED_ATOM_CREDIT = 0",
    "TPC245_L2 = NONE",
    "TPC245_FULL_GATE_B = OPEN",
    "TPC245_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC245_TWIN_PRIME_RESULT = NONE",
    "TPC245_STATUS = " + STATUS,
)
EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc245_covariance_disk_certificate.py",
    "experiments/tpc245_covariance_disk_stress.py",
    "experiments/tpc245_independent_checker.py", "notes/citation_verification.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/route_evaluation.md", "notes/source_lock.md", "notes/theorem_ledger.md",
    "paper/main.tex", "paper/math_commands.tex", "paper/paper.pdf",
    "paper/references.bib", "paper/sections/0_abstract.tex",
    "paper/sections/1_introduction.tex", "paper/sections/2_source_lock.tex",
    "paper/sections/3_classification.tex", "paper/sections/4_proof.tex",
    "paper/sections/5_sharp_corollaries.tex", "paper/sections/6_certificate.tex",
    "paper/sections/7_route_boundary.tex", "paper/sections/8_conclusion.tex",
    "paper/sections/A_status_ledger.tex", "results/tpc245_certificate.json",
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


def verify_pdf() -> None:
    tool = shutil.which("pdftotext")
    require(tool is not None, "pdftotext unavailable")
    plain = subprocess.run([tool, "-layout", str(PDF), "-"], capture_output=True,
                           check=False)
    require(plain.returncode == 0 and plain.stderr == b"", "plain PDF extraction")
    bad_controls = [value for value in plain.stdout
                    if value < 32 and value not in (9, 10, 12, 13)]
    require(not bad_controls, "PDF text layer contains semantic C0 controls")
    require(b"Sharp Longitudinal" in plain.stdout and
            b"Transverse Covariance Disks" in plain.stdout, "PDF title marker")
    require(b"Maximum claim" in plain.stdout and
            b"PROVED_STRUCTURAL_L1_SHARP_COVARIANCE_DISKS" in plain.stdout,
            "PDF claim marker")
    lowered = plain.stdout.lower()
    require(b"canonical block direction" in lowered and b"open" in lowered,
            "PDF physical boundary")
    bbox = subprocess.run([tool, "-bbox-layout", str(PDF), "-"], capture_output=True,
                          check=False)
    require(bbox.returncode == 0 and bbox.stderr == b"", "bbox extraction")
    try:
        ElementTree.fromstring(bbox.stdout)
    except ElementTree.ParseError as error:
        raise CheckFailure("bbox PDF text is not strict XML") from error


def load_producer():
    spec = importlib.util.spec_from_file_location("tpc245_producer", PRODUCER)
    require(spec is not None and spec.loader is not None, "producer module spec")
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


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


def reject(candidate: object, expected: object, label: str) -> None:
    if same_typed(candidate, expected):
        raise CheckFailure("mutation accepted: " + label)


def run() -> None:
    actual_files = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
                    if path.is_file()}
    require(actual_files == EXPECTED_FILES, "project file manifest mismatch")
    for path, expected_hash in TEXT_LOCKS.items():
        require(path.is_file() and canonical_text_hash(path) == expected_hash,
                "text lock mismatch: " + str(path))
    require(PDF.is_file() and raw_hash(PDF) == PDF_RAW_SHA256, "raw PDF lock mismatch")
    verify_pdf()

    bridge = BRIDGE.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    for marker in MARKERS:
        require(marker in bridge, "bridge marker missing: " + marker)
    require("<W,B>=conjugate(w)b+<W_perp,B_perp>" in bridge,
            "bridge decomposition")
    require("0 in S iff |c|<=r" in bridge, "bridge disk cancellation")
    require("NO_SOURCE_BACKED_CANONICAL_ONE_DIMENSIONAL_U_H_IN_H_H" in bridge,
            "bridge canonical-direction fatal")
    require("constant-prime-label subspace" in readme and
            "not a literal one-dimensional block direction" in readme,
            "README TPC219 type boundary")

    joined = "\n".join(path.read_text(encoding="utf-8") for path in
                         (PROOF_PACKAGE, DERIVATION, CLASSIFICATION_PROOF,
                          COROLLARIES, ROUTE_BOUNDARY))
    require("c+q" in joined and "fills the\ndisk" in joined,
            "explicit disk construction")
    require("boundary circle" in joined and "unrealizable" in joined,
            "dimension branches")
    require("arcsin" in joined and "tangent" in joined, "phase sharpness")
    require("does **not** prove" in joined, "claim boundary")

    producer = load_producer()
    raw = CERTIFICATE.read_bytes()
    stored = producer.strict_json_loads(raw.decode("ascii"))
    expected = producer.build_document()
    require(same_typed(stored, expected), "certificate payload mismatch")
    require(raw == producer.canonical_json(stored) + b"\n", "certificate canonical bytes")
    require(stored["payload_sha256"] == PAYLOAD_SHA256, "payload digest lock")
    require(type(stored["certificate_version"]) is int and
            stored["certificate_version"] == 1, "certificate version type")

    firewall = stored["payload"]["scope_firewall"]
    require(firewall["CANONICAL_BLOCK_DIRECTION"] == "OPEN" and
            firewall["LITERAL_V59_TWO_LANE_ATTACHMENT"] == "OPEN",
            "attachment firewalls")
    require(firewall["ARITHMETIC_ADVANCE"] == "NO" and
            firewall["ARITHMETIC_L2"] == "NONE", "arithmetic firewalls")
    require(type(firewall["FIXED_ATOM_CREDIT"]) is int and
            firewall["FIXED_ATOM_CREDIT"] == 0, "fixed-atom exact type")

    mutation = deepcopy(stored)
    mutation["payload"]["theorem"]["dimension_one"] = "CLOSED_DISK"
    reject(mutation, expected, "dimension-one disk promotion")
    mutation = deepcopy(stored)
    mutation["payload"]["scope_firewall"]["ARITHMETIC_ADVANCE"] = "YES"
    reject(mutation, expected, "arithmetic promotion")
    mutation = deepcopy(stored)
    mutation["certificate_version"] = True
    reject(mutation, expected, "bool-int confusion")

    independent_source = INDEPENDENT.read_text(encoding="utf-8")
    producer_source = PRODUCER.read_text(encoding="utf-8")
    require("import tpc245_covariance_disk_certificate" not in independent_source and
            "from tpc245_covariance_disk_certificate" not in independent_source,
            "independent checker imports producer")
    require("assert " not in producer_source and "assert " not in independent_source,
            "assert-based theorem guard")
    stress_source = STRESS.read_text(encoding="utf-8")
    require("ordered_pairs" in stress_source and "itertools.product" in stress_source,
            "stress census computed")

    print("TPC245_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("dimension_ge_2=CLOSED_DISK")
    print("dimension_eq_1=CIRCLE_OR_SINGLETON")
    print("phase_sector=SHARP")
    print("pdf_text_extraction=CLEAN_STRICT_XML")
    print("canonical_block_direction=OPEN")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC245_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, UnicodeError) as error:
        raise SystemExit("TPC245_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
