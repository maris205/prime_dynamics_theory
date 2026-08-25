#!/usr/bin/env python3
"""Fail-closed release checker for TPC-244 sign localization."""

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
PROJECT = ROOT / "papers" / "tpc-244-common-multiplier-sign-localization"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_common_multiplier_sign_localization.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results/tpc244_certificate.json"
PRODUCER = PROJECT / "code/tpc244_common_multiplier_certificate.py"
PROOF_PACKAGE = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
INDEPENDENT = PROJECT / "experiments/tpc244_independent_checker.py"
STRESS = PROJECT / "experiments/tpc244_sign_localization_stress.py"
MAIN_TEX = PROJECT / "paper/main.tex"
DIRECT_PROOF = PROJECT / "paper/sections/3_direct_sum.tex"
CUT_PROOF = PROJECT / "paper/sections/4_sign_cut.tex"
WINDOW_PROOF = PROJECT / "paper/sections/5_hard_window.tex"
CERTIFICATE_SECTION = PROJECT / "paper/sections/6_certificate.tex"
COMPUTATIONAL_PROTOCOL = PROJECT / "notes/computational_protocol.md"
PDF = PROJECT / "paper/paper.pdf"

TEXT_LOCKS = {
    BRIDGE: "28d14c10c1e59a5d87c10508e974d776a641edb0075be4d569e256a0e6015439",
    README: "896774329bc242e370503fbabcb2ddca52caba07e2babed5564669926cdf6722",
    CERTIFICATE: "c74f4ba9608fb4a73d2d77e753b554be36a4ad4fcd582cfc562905930a11ddb6",
    PRODUCER: "e6a563f400354f49aa7d1d0e58248a25c51478e75f6fa2732e910a1d4e18a52c",
    PROOF_PACKAGE: "f24de94c94db9dadf15727fb72cfd1b8c1ae596585ed99a0615ff13534109b49",
    DERIVATION: "d8980983b689e01ba2c782469aa761528cafe3bf1bdf0d24bda6a009e98646a8",
    INDEPENDENT: "74221d8a6eb702297d51b73415ab8c82c56474dd49a576f4ebe7a934640329e8",
    STRESS: "db7d3e29922b67615780c030a9e199092b807611602eeb7c3b59d11ff55d1cb4",
    MAIN_TEX: "236b82c15b5f71aba9d9f29600152e85ad34d181d230eb4aeb11cffad9cbe39d",
    DIRECT_PROOF: "028cee0488b64eaa9259f13512cf8f877a94f17301f7ad2e6bbb85d16d4fc34d",
    CUT_PROOF: "faf526d7c781078801e67b247eeff1163b43b406c051841423b7aae29485216b",
    WINDOW_PROOF: "d1e6cfb75e18baa67071baa7f83ca0c2d982bfa3203e58687e975e5328adaa87",
    CERTIFICATE_SECTION: "a656a39731b7f700b846697c0ef20ed156e5ce26ab6e0b45cacbeb97396cf9fc",
    COMPUTATIONAL_PROTOCOL: "7683404957307bfcbaeec854816d250c2fa83c444e676e7e54ad280399798391",
}
PDF_RAW_SHA256 = "22a134b2adec640b73ddfb4ab8135c02a7bea3f9fa77ab202f4998d2da4c16b1"
PAYLOAD_SHA256 = "4846d4dc5e9a2d2927a21625e404d72edb51177a9b78a0d68bcad28864e40726"

STATUS = "PROVED_STRUCTURAL_L1_COMMON_MULTIPLIER_SIGN_LOCALIZATION"
MARKERS = (
    "TPC244_COMMON_MULTIPLIER_COVARIANCE = PROVED_SUM_ABS_C_H_SQUARED_LOCAL_COVARIANCE",
    "TPC244_COMMON_UNIT_PHASE_INVARIANCE = PROVED_EXACT_COVARIANCE_AND_BOTH_NORMS",
    "TPC244_INTERNAL_MOBIUS_CANCELLATION = PRESERVED_NOT_ESTIMATED",
    "TPC244_NONORTHOGONAL_SIGN_CUT = PROVED_EXACT",
    "TPC244_ALL_SIGN_INVARIANCE = PROVED_IFF_EVERY_SYMMETRIZED_EDGE_ZERO",
    "TPC244_COMPLEX_MULTIPLIER_EDGE = PROVED_WITH_CONJUGATED_CROSS_FACTORS",
    "TPC244_HARD_WINDOW_PAIRWISE_VARIATION = PROVED_AT_MOST_TWO_EPSILON_COEFFICIENT_NORM_PRODUCT",
    "TPC244_V59_SPECIALIZATION = CONDITIONAL_ON_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT",
    "TPC244_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT = OPEN",
    "TPC244_COEFFICIENT_NORM_PAYMENT = OPEN",
    "TPC244_SIGNED_C_H_CANCELLATION = NONE",
    "TPC244_ARITHMETIC_ADVANCE = NO",
    "TPC244_FIXED_ATOM_CREDIT = 0",
    "TPC244_L2 = NONE",
    "TPC244_FULL_GATE_B = OPEN",
    "TPC244_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC244_TWIN_PRIME_RESULT = NONE",
    "TPC244_STATUS = " + STATUS,
)


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


def verify_pdf_text_layer() -> None:
    tool = shutil.which("pdftotext")
    require(tool is not None, "pdftotext unavailable")
    plain = subprocess.run(
        [tool, "-layout", str(PDF), "-"], capture_output=True, check=False
    )
    require(plain.returncode == 0 and plain.stderr == b"",
            "plain PDF text extraction")
    bad_controls = [
        value for value in plain.stdout
        if value < 32 and value not in (9, 10, 12, 13)
    ]
    require(not bad_controls, "PDF text layer contains semantic C0 controls")
    require(b"Common-Multiplier Sign Localization" in plain.stdout,
            "PDF title marker")
    require(b"Maximum claim: structural L1 common-multiplier sign localization." in
            plain.stdout, "PDF claim marker")
    require(b"conditional on a" in plain.stdout and
            b"literal phasewise primitive two-lane attachment" in plain.stdout,
            "PDF conditional boundary")

    bbox = subprocess.run(
        [tool, "-bbox-layout", str(PDF), "-"], capture_output=True, check=False
    )
    require(bbox.returncode == 0 and bbox.stderr == b"",
            "bbox PDF text extraction")
    try:
        ElementTree.fromstring(bbox.stdout)
    except ElementTree.ParseError as error:
        raise CheckFailure("bbox PDF text is not strict XML") from error


def load_producer():
    spec = importlib.util.spec_from_file_location("tpc244_producer", PRODUCER)
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


def validate(candidate: object, expected: object) -> None:
    require(type(candidate) is dict and same_typed(candidate, expected),
            "certificate payload mismatch")


def reject(candidate: object, expected: object, label: str) -> None:
    try:
        validate(candidate, expected)
    except CheckFailure:
        return
    raise CheckFailure("mutation accepted: " + label)


def run() -> None:
    for path, expected_hash in TEXT_LOCKS.items():
        require(path.is_file(), "missing locked source: " + str(path))
        require(canonical_text_hash(path) == expected_hash,
                "text lock mismatch: " + str(path))
    require(PDF.is_file() and raw_hash(PDF) == PDF_RAW_SHA256,
            "raw PDF lock mismatch")
    verify_pdf_text_layer()

    bridge = BRIDGE.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    for marker in MARKERS:
        require(marker in bridge, "bridge marker missing: " + marker)
    require("<W,B>=sum_h conjugate(C_h)C_h<w_h,b_h>" in bridge,
            "bridge common-multiplier identity")
    require("Q(s)-Q(1)=-2sum_(h<k,s_h!=s_k)S_hk" in bridge,
            "bridge sign-cut identity")
    require("|Q_I(eta)-Q_I(xi)|<=2epsilon||W||||B||" in bridge,
            "bridge factor-two transfer")
    require("does not prove a literal V59 two-lane" in bridge,
            "bridge physical firewall")
    require("aggregate outer sign" in readme and
            "internal Möbius signs still" in readme,
            "README outer/internal distinction")
    require("CONDITIONAL_ON_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT" in
            readme, "README conditional boundary")

    proof_parts = (
        PROOF_PACKAGE.read_text(encoding="utf-8"),
        DERIVATION.read_text(encoding="utf-8"),
        DIRECT_PROOF.read_text(encoding="utf-8"),
        CUT_PROOF.read_text(encoding="utf-8"),
        WINDOW_PROOF.read_text(encoding="utf-8"),
    )
    joined = "\n".join(proof_parts)
    require("<W,B> = sum_h |C_h|^2<w_h,b_h>" in proof_parts[0],
            "proof common-multiplier theorem")
    require("Q(s)-Q(1)=-2 sum_(h<k,s_h!=s_k)S_hk" in proof_parts[0],
            "proof cut theorem")
    require("if and only if" in joined and "Walsh character" in joined,
            "proof all-sign iff")
    require("2epsilon||W||||B||" in proof_parts[0],
            "proof hard-window factor two")
    require("do **not** prove" in proof_parts[0],
            "proof source boundary")

    producer = load_producer()
    raw = CERTIFICATE.read_bytes()
    stored = producer.strict_json_loads(raw.decode("ascii"))
    expected = producer.build_document()
    validate(stored, expected)
    require(raw == producer.canonical_json(stored) + b"\n",
            "noncanonical certificate bytes")
    require(stored["payload_sha256"] == PAYLOAD_SHA256, "payload digest")
    require(type(stored["certificate_version"]) is int and
            stored["certificate_version"] == 1, "certificate version")

    theorem = stored["theorem"]
    require(theorem["direct_sum_covariance"] ==
            "<W,B>=sum_h|C_h|^2<w_h,b_h>", "certificate diagonal theorem")
    require(theorem["common_unit_phase_invariance"] ==
            "EXACT_COVARIANCE_AND_BOTH_NORMS", "certificate phase theorem")
    require(theorem["internal_mobius_signs"] ==
            "PRESERVED_INSIDE_ABS_C_H", "internal Möbius firewall")
    require(theorem["sign_cut_identity"] ==
            "Q(s)-Q(1)=-2sum_(cut_edges)S_hk", "certificate cut theorem")
    require(theorem["all_sign_invariance"] ==
            "IFF_EVERY_SYMMETRIZED_EDGE_S_HK_IS_ZERO", "certificate iff")
    require(theorem["hard_window_pairwise_transfer"] ==
            "<=2epsilon||W||_2||B||_2", "certificate factor two")

    fixtures = stored["fixtures"]
    require(fixtures["direct_sum"]["pattern_count"] == 8 and
            fixtures["direct_sum"]["all_common_sign_patterns_invariant"] is True,
            "direct fixture")
    require(fixtures["overlap"]["pattern_count"] == 8 and
            fixtures["overlap"]["sign_sensitive"] is True,
            "overlap fixture")
    require(fixtures["hard_window"]["ordered_pair_count"] == 64 and
            fixtures["hard_window"]["pairwise_factor_two_all_ordered_pairs"] is True,
            "hard-window fixture")

    firewall = stored["scope_firewall"]
    require(firewall["LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT"] == "OPEN",
            "literal attachment firewall")
    require(firewall["PHYSICAL_SPECIALIZATION"] ==
            "CONDITIONAL_ON_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT",
            "conditional specialization")
    require(firewall["SIGNED_C_H_CANCELLATION"] == "NONE",
            "signed C_h firewall")
    require(firewall["ARITHMETIC_L2"] == "NONE" and
            firewall["ARITHMETIC_ADVANCE"] == "NO", "arithmetic firewall")
    require(type(firewall["FIXED_ATOM_CREDIT"]) is int and
            firewall["FIXED_ATOM_CREDIT"] == 0, "fixed-atom type")
    require(firewall["STRICT_1_OVER_400"] == "UNPAID_GLOBAL" and
            firewall["FULL_GATE_B"] == "OPEN", "Gate-B firewall")
    require(firewall["FINITE_CERTIFICATE_IS_THEOREM_EVIDENCE"] is False,
            "finite-evidence firewall")

    bad_arithmetic = deepcopy(stored)
    bad_arithmetic["scope_firewall"]["ARITHMETIC_ADVANCE"] = "YES"
    reject(bad_arithmetic, expected, "arithmetic promotion")
    bad_attachment = deepcopy(stored)
    bad_attachment["scope_firewall"][
        "LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT"
    ] = "PROVED"
    reject(bad_attachment, expected, "attachment promotion")
    bad_factor = deepcopy(stored)
    bad_factor["theorem"]["hard_window_pairwise_transfer"] = "<=epsilon||W||_2||B||_2"
    reject(bad_factor, expected, "factor two removal")
    bad_mobius = deepcopy(stored)
    bad_mobius["theorem"]["internal_mobius_signs"] = "ERASED"
    reject(bad_mobius, expected, "internal Möbius erasure")
    bad_type = deepcopy(stored)
    bad_type["certificate_version"] = True
    reject(bad_type, expected, "bool/int confusion")

    independent_source = INDEPENDENT.read_text(encoding="utf-8")
    producer_source = PRODUCER.read_text(encoding="utf-8")
    require("import tpc244_common_multiplier_certificate" not in independent_source,
            "independent checker imports producer")
    require("from tpc244_common_multiplier_certificate" not in independent_source,
            "independent checker imports producer symbols")
    require("assert " not in producer_source and "assert " not in independent_source,
            "assert-based theorem guard")
    stress_source = STRESS.read_text(encoding="utf-8")
    require("104976" not in stress_source and
            "direct_covariance_checks" in stress_source and
            "cut_pattern_checks" in stress_source,
            "stress census must be computed")

    print("TPC244_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("common_outer_phase=INVISIBLE_IN_ORTHOGONAL_MAIN_COVARIANCE")
    print("nonorthogonal_sign_dependence=EXACT_CUT_EDGES")
    print("hard_window_pairwise_variation=TWO_EPSILON_NORM_PRODUCT")
    print("pdf_text_extraction=CLEAN_STRICT_XML")
    print("literal_v59_two_lane_attachment=OPEN")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC244_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, UnicodeError) as error:
        raise SystemExit("TPC244_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
