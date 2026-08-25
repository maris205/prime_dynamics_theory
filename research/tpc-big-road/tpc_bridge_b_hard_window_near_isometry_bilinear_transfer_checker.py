#!/usr/bin/env python3
"""Fail-closed release checker for TPC-243 hard-window transfer."""

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
PROJECT = ROOT / "papers" / "tpc-243-hard-window-near-isometry-bilinear-transfer"
BRIDGE = (ROOT / "research" / "tpc-big-road" /
          "bridge_b_hard_window_near_isometry_bilinear_transfer.md")
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results" / "tpc243_certificate.json"
PRODUCER = PROJECT / "code" / "tpc243_hard_window_certificate.py"
PROOF_PACKAGE = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
INDEPENDENT = PROJECT / "experiments" / "tpc243_independent_checker.py"
STRESS = PROJECT / "experiments" / "tpc243_hard_window_stress.py"
MAIN_TEX = PROJECT / "paper" / "main.tex"
SETUP_PROOF = PROJECT / "paper" / "sections" / "2_setup_source_lock.tex"
ROW_PROOF = PROJECT / "paper" / "sections" / "3_harmonic_row_bound.tex"
TRANSFER_PROOF = PROJECT / "paper" / "sections" / "4_near_isometry_bilinear.tex"
V59_PROOF = PROJECT / "paper" / "sections" / "5_primitive_v59.tex"
ORIENTATION_PROOF = PROJECT / "paper" / "sections" / "6_tpc242_transport.tex"
CERTIFICATE_SECTION = PROJECT / "paper" / "sections" / "7_exact_certificate.tex"
COMPUTATIONAL_PROTOCOL = PROJECT / "notes" / "computational_protocol.md"
PDF = PROJECT / "paper" / "paper.pdf"

TEXT_LOCKS = {
    BRIDGE: "14120b1b4b9a670737633ea9b323a80b4949cbad14efd97aafd11c7319f5e4fb",
    README: "0fe4977521902afabcd15b8a1f43e7e6533b975addb31792e5b484f562937dc8",
    CERTIFICATE: "5d534fb6b967a21925047ae228b2ad16865c7785add1eeefea98b5970d781387",
    PRODUCER: "7482550839001842f728ecbabd8a27923fab05412bae1f21d014753418c07ef8",
    PROOF_PACKAGE: "e7b17bd6babb1a00f690697ab4163053cfe33ddb61419bd73f8bf77d86e44faf",
    DERIVATION: "9cc59a95c60c34422d42417009df9c2fe9f213ba70e82a97d9aa6f587dd02a3d",
    INDEPENDENT: "f50e103ed7f1d201f05f695ccf3c4b8e75706550c785b40f8919b1afb411ad91",
    STRESS: "75413a7c5fa64eca38a85914b845ce3c48a5fc1ae12879957f8cc35b38dd0919",
    MAIN_TEX: "e713a3d35efcc1fefa1a819f4a2f30b1d8e2ae72d461e5635a4e32a3653b8a7f",
    SETUP_PROOF: "c303bf01463709728929ddb31abf8ec2ac5a7e91b1d3eb7de12bd6234d4192f5",
    ROW_PROOF: "b1e4e46b5a604cd946b3196adad9528666576bb5a5c6e4c3512a239788dbb96a",
    TRANSFER_PROOF: "65f7e96d8cf9f52ae493381043385fda43e5f4f73d7eb4da137aee4d960d3617",
    V59_PROOF: "9b7ecbfecef7f0dbc57b70bb2deece1318d9331ab0f45c97e1f41ef2d4db88cc",
    ORIENTATION_PROOF: "609746d2842d44627578c3a928b5c3ab78faa717f72f1e1b5edc957393e86188",
    CERTIFICATE_SECTION: "a58087ea8c84e7404894f631d4ff4ec19dcf31bd75f7ad8e7babd36883bffc19",
    COMPUTATIONAL_PROTOCOL: "c9aab44ce444d91abc8eb5814da43029be6f53d0560bb9d4b2fb672fa3510404",
}
PDF_RAW_SHA256 = "00a37a5c7f18c7574ff4e6ccc9ce78c6c8f4b4acb5aba351525af9d1c95de0b4"
PAYLOAD_SHA256 = "1ff81cf47defa1ce0520ba6e8bb50dab370d928adc453eb50880d9e359c0257d"

STATUS = "PROVED_STRUCTURAL_L1_HARD_WINDOW_NEAR_ISOMETRY_BILINEAR_TRANSFER"
SEMANTIC_MUTATIONS = [
    "bilinear_orientation_reversal",
    "bool_int_confusion",
    "duplicate_json_key",
    "finite_classification_promotion",
    "harmonic_row_bound_tamper",
    "nonfinite_json_constant",
    "source_digest_tamper",
    "v59_coefficient_tamper",
]
HOSTILE_REBOUND_MUTATIONS = [
    "arithmetic_advance_rebinding",
    "extra_scope_key_rebinding",
    "selected_mode_rebinding",
    "source_lock_rebinding",
    "strict_1_over_400_promotion",
    "twin_prime_result_promotion",
]
MARKERS = (
    "TPC243_HARD_WINDOW_DIRICHLET_GRAM = PROVED_EXACT",
    "TPC243_GEOMETRIC_SUM_BOUND = PROVED_ONE_OVER_TWO_CIRCULAR_DISTANCE",
    "TPC243_HARMONIC_CIRCLE_PACKING = PROVED_DELTA_INVERSE_H_K",
    "TPC243_TWO_SIDED_NEAR_ISOMETRY = PROVED_ONE_PLUS_MINUS_EPSILON",
    "TPC243_SIGNED_BILINEAR_TRANSFER = PROVED_WITH_ERROR_EPSILON_NORM_PRODUCT",
    "TPC243_PRIMITIVE_HEIGHT_SPECIALIZATION = PROVED_R_U_EQUALS_U_SQUARED_H_FLOOR_U_SQUARED_OVER_TWO",
    "TPC243_V59_EPSILON = PROVED_133_OVER_100_PLUS_O_ONE_TIMES_X_MINUS_67_OVER_200_LOG_X",
    "TPC243_TPC242_SELECTED_MODE_TRANSFER = PROVED_CONDITIONAL_ON_COEFFICIENT_LANE_ATTACHMENT",
    "TPC243_LITERAL_TOP_PRIME_ATTACHMENT = OPEN",
    "TPC243_ARITHMETIC_ADVANCE = NO",
    "TPC243_FIXED_ATOM_CREDIT = 0",
    "TPC243_L2 = NONE",
    "TPC243_FULL_GATE_B = OPEN",
    "TPC243_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC243_TWIN_PRIME_RESULT = NONE",
    "TPC243_STATUS = " + STATUS,
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
    require(b"Hard-Window Near-Isometry" in plain.stdout and
            STATUS.encode("ascii") in plain.stdout,
            "PDF text layer missing release markers")

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
    spec = importlib.util.spec_from_file_location("tpc243_producer", PRODUCER)
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
    require("R_delta=delta^(-1) H_(K_delta)" in bridge,
            "bridge harmonic row theorem")
    require("[1-epsilon_delta,N]_+" in bridge and
            "<=epsilon_delta,N ||z||_2||w||_2" in bridge,
            "bridge two-sided and bilinear statements")
    require("(133/100+o(1))x^(-67/200)log x" in bridge,
            "bridge V59 coefficient")
    require("not an arithmetic cancellation theorem" in bridge,
            "bridge arithmetic firewall")
    require("structural interface, not arithmetic cancellation" in readme,
            "README structural firewall")
    require("F_1=<Y,X>=N^(-1)<Tw,Tz>" in readme,
            "README orientation")

    proof_parts = (
        PROOF_PACKAGE.read_text(encoding="utf-8"),
        DERIVATION.read_text(encoding="utf-8"),
        ROW_PROOF.read_text(encoding="utf-8"),
        TRANSFER_PROOF.read_text(encoding="utf-8"),
        V59_PROOF.read_text(encoding="utf-8"),
        ORIENTATION_PROOF.read_text(encoding="utf-8"),
    )
    joined = "\n".join(proof_parts)
    compact_joined = " ".join(joined.split())
    require("R_\\delta=\\delta^{-1}H_K" in proof_parts[0],
            "proof row bound")
    require("[1-\\epsilon]_+" in proof_parts[0],
            "proof positive-part lower frame")
    require("\\frac{133}{100}+o(1)" in proof_parts[0],
            "proof exact V59 coefficient")
    require("F_1=\\langle Y,X\\rangle" in proof_parts[0],
            "proof selected orientation")
    require("does not prove arithmetic cancellation" in compact_joined,
            "proof arithmetic firewall")

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
    require(theorem["row_bound"] == "R_delta=delta^(-1)*H_K",
            "certificate row theorem")
    require(theorem["frame_lower"] ==
            "[1-epsilon]_+*||z||_2^2<=N^(-1)||Tz||_2^2",
            "certificate lower frame")
    require(theorem["bilinear"] ==
            "|N^(-1)<Tz,Tw>-<z,w>|<=epsilon*||z||_2*||w||_2",
            "certificate bilinear theorem")

    transport = stored["tpc242_transport"]
    require(transport["selected_mode"] ==
            "F_1=<Y,X>=N^(-1)<Tw,Tz>", "selected orientation")
    require(transport["target"] == "<w,z>", "selected target")
    require(transport["status"] ==
            "SIGNED_BILINEAR_INTERFACE_NOT_PHYSICAL_ATTACHMENT",
            "attachment firewall")

    ledger = stored["v59_ledger"]
    require(ledger["epsilon_log_x_coefficient"] ==
            {"denominator": 100, "numerator": 133},
            "V59 logarithmic coefficient")
    require(ledger["epsilon_power_exponent"] ==
            {"denominator": 200, "numerator": -67},
            "V59 power exponent")

    firewall = stored["scope_firewall"]
    require(firewall["LITERAL_TOP_PRIME_ATTACHMENT"] == "OPEN",
            "literal attachment firewall")
    require(firewall["SIGNED_C_H_THEOREM"] == "NONE",
            "signed multiplier firewall")
    require(firewall["ARITHMETIC_L2"] == "NONE" and
            firewall["FULL_GATE_B"] == "OPEN", "Gate-B promotion")
    require(type(firewall["FIXED_ATOM_CREDIT"]) is int and
            firewall["FIXED_ATOM_CREDIT"] == 0, "fixed-atom type")
    require(firewall["FINITE_CERTIFICATE_IS_THEOREM_EVIDENCE"] is False,
            "finite-evidence firewall")

    status = stored["status_ledger"]
    require(status["status"] == STATUS and status["claim_ceiling"] == STATUS,
            "status ceiling")
    require(status["arithmetic_advance"] == "NO", "arithmetic firewall")
    mutations = stored["mutation_firewalls"]
    require(mutations["semantic"] == SEMANTIC_MUTATIONS and
            mutations["semantic_count"] == len(SEMANTIC_MUTATIONS),
            "semantic mutation registry")
    require(mutations["hostile_rebound"] == HOSTILE_REBOUND_MUTATIONS and
            mutations["hostile_rebound_count"] == len(HOSTILE_REBOUND_MUTATIONS),
            "hostile mutation registry")

    bad_status = deepcopy(stored)
    bad_status["status_ledger"]["arithmetic_advance"] = "YES"
    reject(bad_status, expected, "status promotion")
    bad_orientation = deepcopy(stored)
    bad_orientation["tpc242_transport"]["target"] = "<z,w>"
    reject(bad_orientation, expected, "orientation reversal")
    bad_coefficient = deepcopy(stored)
    bad_coefficient["v59_ledger"]["epsilon_log_x_coefficient"]["numerator"] = 67
    reject(bad_coefficient, expected, "V59 coefficient")
    bad_type = deepcopy(stored)
    bad_type["certificate_version"] = True
    reject(bad_type, expected, "bool/int confusion")

    independent_source = INDEPENDENT.read_text(encoding="utf-8")
    producer_source = PRODUCER.read_text(encoding="utf-8")
    require("import tpc243_hard_window_certificate" not in independent_source,
            "independent checker imports producer")
    require("from tpc243_hard_window_certificate" not in independent_source,
            "independent checker imports producer symbols")
    require("assert " not in producer_source and "assert " not in independent_source,
            "assert-based theorem guard")
    stress_source = STRESS.read_text(encoding="utf-8")
    require("len(vectors) ** 2" in stress_source and
            "orientation_sensitive_pairs" in stress_source,
            "stress census construction")

    print("TPC243_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("hard_window_frame=ONE_PLUS_MINUS_EPSILON")
    print("bilinear_transfer=SIGNED_ORIENTATION_PRESERVED")
    print("v59_epsilon=X_MINUS_67_OVER_200_LOG_X")
    print("pdf_text_extraction=CLEAN_STRICT_XML")
    print("literal_top_prime_attachment=OPEN")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC243_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, UnicodeError) as error:
        raise SystemExit("TPC243_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
