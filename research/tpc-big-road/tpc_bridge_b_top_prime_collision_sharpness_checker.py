#!/usr/bin/env python3
"""Fail-closed release checker for TPC-241 collision sharpness."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-241-top-prime-collision-sharpness"
BRIDGE = ROOT / "research" / "tpc-big-road" / "bridge_b_top_prime_collision_sharpness.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results" / "tpc241_certificate.json"
PRODUCER = PROJECT / "code" / "tpc241_collision_sharpness_certificate.py"
PROOF_PACKAGE = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
INDEPENDENT = PROJECT / "experiments" / "tpc241_independent_checker.py"
STRESS = PROJECT / "experiments" / "tpc241_collision_stress.py"
ROW_PROOF = PROJECT / "paper" / "sections" / "3_row_mass_and_cauchy.tex"
COEFFICIENT_PROOF = PROJECT / "paper" / "sections" / "4_coefficient_liminf.tex"
WINDOW_PROOF = PROJECT / "paper" / "sections" / "5_finite_window_transfer.tex"
SHARPNESS_PROOF = PROJECT / "paper" / "sections" / "6_sharpness_and_route.tex"
PDF = PROJECT / "paper" / "paper.pdf"

TEXT_LOCKS = {
    BRIDGE: "1f169ec36a5d6e2fe8d2e4161c02613de04aad1b591a985fc6e22cbe12be5f86",
    README: "6679b8b47b6d40d9f2b93fd36c90a6061b1901bd8a5c3db5754783bf082c66aa",
    CERTIFICATE: "f0cecbf328868a09d1933a7a8970e9508e0f27b814ce75af0f821afcc4e41860",
    PRODUCER: "4586c5ebd3c06dc9ac85cf86e8465ac35a03ecd22832e15b4bb7fea21ee3bdb3",
    PROOF_PACKAGE: "f5ba7b04a432cac12d576a34e69c887e9f925b2b6906cc41a5a588ef32d19d8c",
    DERIVATION: "71078fc11f2dc87902f29b4ab62dfce99835413a95dcd8ac98f2cb1c7086e9a7",
    INDEPENDENT: "443c5b7726c6fb430855e7e2ec5b5094116a47424e3504b875ce0f4dcfa610d6",
    STRESS: "1252f03409d9617d38f8e6deef4c9ddb14bcecb6f3f5724e350ad0691b42ee10",
    ROW_PROOF: "55808d3714d6069ae189a8edc88e1f00386427fe5add37b5c216594fa4839e27",
    COEFFICIENT_PROOF: "0213962e8bcea848325cbb072e6ee0236c7ec6c0655272887447ece2347ac150",
    WINDOW_PROOF: "44f1c876bd48601d670b17b255a27c2d32e6434adc0d6e0d6e469ef685985a1e",
    SHARPNESS_PROOF: "90fec097463f72faa3bf2934b46c0075fa7dd5938dd6ead81c43f985b3c23e5c",
}
PDF_RAW_SHA256 = "d644863c9185f4360dc3f5dcb9868d10340269ed82ce3d66a3b6789a0b21d03a"
PAYLOAD_SHA256 = "0551296104f4f80d07cb25adce2d9b6438bd5b7ab86904e6d0bc075fd2b16118"

STATUS = "PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_COLLISION_SHARPNESS"
OBJECT_KIND = (
    "Q_COLLAPSED_UNSIGNED_TOP_PRIME_COMMON_PROFILE_COEFFICIENT_"
    "AND_FINITE_WINDOW_ENERGY"
)
PROFILE_KIND = "FIXED_REAL_CINF_NONNEGATIVE_LE_ONE_SUPPORT_MINUS1_PLUS1_INTEGRAL_ONE"
FRAME_ORDER = "FULL_PRIMITIVE_VECTOR_FRAME_THEN_NONNEGATIVE_TOP_PRIME_RESTRICTION"

MARKERS = (
    "TPC241_TOP_PRIME_ROW_MASS = PROVED_UNIFORM_THREE_OVER_TWO",
    "TPC241_PRIMITIVE_RESIDUE_CAUCHY = PROVED_EXACT",
    "TPC241_COEFFICIENT_LIMINF = PROVED_10773_LOG_2_OVER_1600",
    "TPC241_FINITE_WINDOW_LIMINF = PROVED_10773_LOG_2_OVER_3200",
    "TPC241_NORMALIZED_FIXED_POWER = PROVED_1_OVER_48_SHARP_UP_TO_LOGARITHMS",
    "TPC241_UNSIGNED_FIXED_POWER_IMPROVEMENT = REFUTED_ON_EXACT_FIXED_PROFILE_COMMON_SOURCE_KERNEL",
    "TPC241_FULL_VECTOR_FRAME_BEFORE_TOP_PRIME_RESTRICTION = REQUIRED_EXACT",
    "TPC241_CLASS_UNIFORM_PROFILE_THRESHOLD = NOT_CLAIMED",
    "TPC241_PLATEAU_PROFILE_SUBSTITUTION = FORBIDDEN",
    "TPC241_C_H_SIGNED_CANCELLATION = NONE",
    "TPC241_SIGNED_FOUR_PACKET_GATE_B_SCALAR = OPEN",
    "TPC241_ARITHMETIC_ADVANCE = NO",
    "TPC241_L2 = NONE",
    "TPC241_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC241_STATUS = " + STATUS,
)


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical_text_hash(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def raw_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_producer():
    spec = importlib.util.spec_from_file_location("tpc241_producer", PRODUCER)
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


def validate(candidate: dict[str, object], expected: dict[str, object]) -> None:
    require(type(candidate) is dict and same_typed(candidate, expected),
            "certificate payload mismatch")


def reject(candidate: dict[str, object], expected: dict[str, object], label: str) -> None:
    try:
        validate(candidate, expected)
    except CheckFailure:
        return
    raise CheckFailure("mutation accepted: " + label)


def exact_fraction(record: object, expected: Fraction, label: str) -> None:
    require(type(record) is dict, label + " record type")
    require(type(record.get("numerator")) is int, label + " numerator type")
    require(type(record.get("denominator")) is int
            and record["denominator"] > 0, label + " denominator")
    value = Fraction(record["numerator"], record["denominator"])
    require(value == expected and record.get("value") == str(expected), label + " value")


def run() -> None:
    for path, expected_hash in TEXT_LOCKS.items():
        require(path.is_file(), "missing locked source: " + str(path))
        require(canonical_text_hash(path) == expected_hash,
                "text lock mismatch: " + str(path))
    require(PDF.is_file() and raw_hash(PDF) == PDF_RAW_SHA256, "raw PDF lock mismatch")

    bridge = BRIDGE.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    for marker in MARKERS:
        require(marker in bridge, "bridge marker missing: " + marker)
    require("Status: `" + STATUS + "`" in readme, "README status marker")
    require("10773 log(2)/1600" in bridge and "10773 log(2)/3200" in bridge,
            "explicit liminf constants missing")
    require("x^(1/48)/log x" in bridge, "sharpness scale missing")
    require("Only after (4.1)" in bridge, "frame-order proof missing")
    require("fixed admissible `psi`, fixed `delta>0`, and fixed real `A`" in bridge,
            "fixed-power quantifiers missing")
    require("does not say that the signed four-packet scalar" in bridge,
            "signed-object firewall missing")

    proof_parts = (
        PROOF_PACKAGE.read_text(encoding="utf-8"),
        DERIVATION.read_text(encoding="utf-8"),
        ROW_PROOF.read_text(encoding="utf-8"),
        COEFFICIENT_PROOF.read_text(encoding="utf-8"),
        WINDOW_PROOF.read_text(encoding="utf-8"),
        SHARPNESS_PROOF.read_text(encoding="utf-8"),
    )
    joined = "\n".join(proof_parts)
    require("10773" in joined and "1/48" in joined, "proof constant/exponent")
    require("p-1" in proof_parts[0] and "Cauchy" in proof_parts[0],
            "post-collapse Cauchy proof")
    require("complete primitive-frequency" in proof_parts[0]
            and "Only after" in proof_parts[0], "full-vector frame order")
    require("x^delta/(log x)^(A+1)" in proof_parts[0], "sharpness comparison")
    require("=left(" not in joined, "malformed LaTeX delimiter")

    producer = load_producer()
    stored = json.loads(CERTIFICATE.read_text(encoding="ascii"))
    expected = producer.expected_document()
    validate(stored, expected)
    require(type(stored["certificate_version"]) is int
            and stored["certificate_version"] == 1, "certificate version")
    require(stored["payload_sha256"] == PAYLOAD_SHA256, "payload digest")

    ledger = stored["exact_fraction_ledger"]
    exact_fraction(ledger["H_exponent"], Fraction(21, 32), "H")
    exact_fraction(ledger["Q_exponent"], Fraction(1, 3), "Q")
    exact_fraction(ledger["U_exponent"], Fraction(133, 400), "U")
    exact_fraction(ledger["coefficient_constant"], Fraction(10773, 1600),
                   "coefficient constant")
    exact_fraction(ledger["finite_window_constant"], Fraction(10773, 3200),
                   "window constant")
    exact_fraction(ledger["collision_exponent"], Fraction(1, 48), "collision exponent")
    exact_fraction(ledger["direct_exponent"], Fraction(1, 96), "direct exponent")
    exact_fraction(ledger["frame_defect_exponent"], Fraction(-67, 100),
                   "frame defect")
    exact_fraction(ledger["row_depth_exponent"], Fraction(23, 2400), "row depth")
    exact_fraction(ledger["row_error_exponent"], Fraction(-23, 2400), "row error")
    require(Fraction(4, 3) - 2 * Fraction(21, 32) == Fraction(1, 48),
            "collision exponent arithmetic")
    require(Fraction(9, 4) * Fraction(399, 400) * 3 == Fraction(10773, 1600),
            "coefficient arithmetic")
    require(Fraction(10773, 1600) / 2 == Fraction(10773, 3200),
            "window arithmetic")

    lock = stored["object_lock"]
    require(lock["main_object"] == OBJECT_KIND, "object lock")
    require(lock["profile_class"] == PROFILE_KIND, "profile lock")
    require(lock["coefficient"] == "C_p=-log(p)/p", "coefficient lock")
    require(lock["frame_order"] == FRAME_ORDER, "frame-order lock")
    require(lock["p_domain"] == "PRIMES_U_OVER_2_LT_P_LE_U", "p-shell lock")
    require(lock["q_domain"] == "PRIMES_Q_LT_Q_LE_2Q", "q-shell lock")
    require(lock["plateau_profile"] == "REJECTED_NOT_LITERAL_V59_CLASS",
            "plateau firewall")

    theorem = stored["theorem"]
    require(theorem["classification"] == "PROVED", "theorem classification")
    require("10773*log(2)/1600" in theorem["coefficient_liminf"],
            "coefficient liminf")
    require("10773*log(2)/3200" in theorem["finite_window_liminf"],
            "window liminf")
    require("DELTA_POSITIVE" in theorem["fixed_power_refutation"],
            "fixed-power theorem")
    require("PROFILEWISE_THRESHOLD" in theorem["quantifier"],
            "profilewise quantifier")

    markers = stored["markers"]
    require(markers["TPC241_STATUS"] == STATUS, "status promotion")
    require(markers["TPC241_ROUTE_LEVEL"] == "PROVED_STRUCTURAL_L1_OBSTRUCTION",
            "route level")
    require(markers["TPC241_ARITHMETIC_ADVANCE"] == "NO", "arithmetic firewall")
    require(type(markers["TPC241_FIXED_ATOM_CREDIT"]) is int
            and markers["TPC241_FIXED_ATOM_CREDIT"] == 0, "fixed atom firewall")
    require(markers["TPC241_L2"] == "NONE", "L2 firewall")
    require(markers["TPC241_FULL_GATE_B"] == "OPEN", "Gate-B firewall")
    require(markers["TPC241_STRICT_1_OVER_400"] == "UNPAID_GLOBAL",
            "strict-saving firewall")

    firewall = stored["scope_firewall"]
    require(firewall["CLASS_UNIFORM_X0"] == "NOT_CLAIMED", "uniformity firewall")
    require(firewall["PHYSICAL_WINDOW_CROSS_TERM_DELETION"] == "FORBIDDEN",
            "cross-term firewall")
    require(firewall["SIGNED_C_H_CANCELLATION"] == "NONE", "signed C_h firewall")
    require(firewall["SIGNED_FOUR_PACKET_PROJECTION"] == "OPEN",
            "four-packet firewall")
    require(firewall["FINITE_FIXTURE_IS_THEOREM_EVIDENCE"] is False,
            "numerical firewall")

    fixture = stored["finite_fixture"]
    require((fixture["Q"], fixture["H"], fixture["U"]) == (101, 509, 97),
            "fixture scales")
    require(fixture["q_count"] == len(fixture["q_values"]) == 20,
            "fixture q census")
    require(fixture["top_prime_rows"] == len(fixture["rows"]) == 3,
            "fixture row count")
    for row in fixture["rows"]:
        require(row["classification"] == "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
                "row evidence class")
        require(row["primitive_support"] is True and row["cauchy_pass"] is True,
                "row primitive/Cauchy")
        require(row["collision_excess_positive"] is True, "row collision")
        require(row["occupied_primitive_residues"] <= row["p"] - 1,
                "row residue count")

    require(stored["mutation_firewalls"]["rejected_count"] == 11,
            "mutation count")
    bad_status = deepcopy(stored)
    bad_status["markers"]["TPC241_STATUS"] = "PROVED_ARITHMETIC_L2_FULL_GATE_B"
    reject(bad_status, expected, "status promotion")
    bad_order = deepcopy(stored)
    bad_order["object_lock"]["frame_order"] = "TOP_RESTRICTION_BEFORE_FRAME"
    reject(bad_order, expected, "frame-order reversal")
    bad_constant = deepcopy(stored)
    bad_constant["exact_fraction_ledger"]["coefficient_constant"]["numerator"] = 10772
    reject(bad_constant, expected, "wrong coefficient constant")
    bad_type = deepcopy(stored)
    bad_type["certificate_version"] = True
    reject(bad_type, expected, "bool/int confusion")

    independent_source = INDEPENDENT.read_text(encoding="utf-8")
    producer_source = PRODUCER.read_text(encoding="utf-8")
    require("import tpc241_collision_sharpness_certificate" not in independent_source,
            "independent checker imports producer")
    require("from tpc241_collision_sharpness_certificate" not in independent_source,
            "independent checker imports producer symbols")
    require("assert " not in producer_source, "producer uses assert")
    require("QUADRATIC_BUMP" in STRESS.read_text(encoding="utf-8")
            and "QUARTIC_BUMP" in STRESS.read_text(encoding="utf-8"),
            "stress profiles missing")

    print("TPC241_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("coefficient_liminf=10773*log(2)/1600")
    print("finite_window_liminf=10773*log(2)/3200")
    print("fixed_power=1/48_SHARP_UP_TO_LOGARITHMS")
    print("unsigned_fixed_power_improvement=REFUTED_SCOPED")
    print("signed_gate_b=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC241_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError) as error:
        raise SystemExit("TPC241_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
