#!/usr/bin/env python3
"""Fail-closed release checker for the TPC-240 top-prime energy floor."""

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
PROJECT = ROOT / "papers" / "tpc-240-top-prime-direct-energy-floor"
BRIDGE = ROOT / "research" / "tpc-big-road" / "bridge_b_top_prime_direct_energy_floor.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results" / "tpc240_certificate.json"
PRODUCER = PROJECT / "code" / "tpc240_top_prime_energy_certificate.py"
PROOF_PACKAGE = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
INDEPENDENT = PROJECT / "experiments" / "tpc240_independent_checker.py"
STRESS = PROJECT / "experiments" / "tpc240_profile_stress.py"
ROW_PROOF = PROJECT / "paper" / "sections" / "3_exact_row_riemann.tex"
AGGREGATION_PROOF = PROJECT / "paper" / "sections" / "4_weighted_pnt_aggregation.tex"
PDF = PROJECT / "paper" / "paper.pdf"

TEXT_LOCKS = {
    BRIDGE: "093fa3bc9c3512d760462526daac7aa1867ee41eb5b6b0e2bfd0a7ee8d580906",
    README: "c948c5ee3c21f5d22645379915a3daccf17bb58567452166e1bd5df58d82587e",
    CERTIFICATE: "e98ab437bdb37e5470ca893c0223fecb26aad4e61db968f63928032e0bfe2da8",
    PRODUCER: "8904b745cc23ffbf8fad4b1025b347cb2817d5dddcf6e93bd426d12d67511b0f",
    PROOF_PACKAGE: "e9060ead6ddb21d001e31f90eb42f5e97dbb24d6729fa837e86447dc5f43c61a",
    DERIVATION: "1b9fc0183061b3c08267a1da4f7af0636f3d9ecf2443c60deac4469b901be9de",
    INDEPENDENT: "56c4754c380e4853e82a8273c48e39f34f2a53c03118a4929ae9fa865d522dcb",
    STRESS: "08f81a0e5de0c66d8b17c80cd0c0471a428053d4e833d3d4fdbf29a5fddebf68",
    ROW_PROOF: "b76149e31271711edcfe1b8ac0646d722f9a498964afe28ba3676cc07bb2b137",
    AGGREGATION_PROOF: "b50c91a4846941d1d3b703966324fecae90b330e9028bb430c069d49f976d61c",
}
PDF_RAW_SHA256 = "52d28f6d4aee8844835c84adba0426df9a11cedb512cee10ec9c3771c51bee7d"
PAYLOAD_SHA256 = "5386127d91df47484e9713a191b20402beedbe3859fae09b86949bb59baf2b8b"

STATUS = "PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_DIRECT_ENERGY_FLOOR"
OBJECT_KIND = "Q_SPLIT_UNSIGNED_TOP_PRIME_DIRECT_RESIDUE_ROW_ENERGY"
PROFILE_KIND = "FIXED_REAL_CINF_NONNEGATIVE_LE_ONE_SUPPORT_MINUS1_PLUS1_INTEGRAL_ONE"

MARKERS = (
    "TPC240_TOP_PRIME_COEFFICIENT = PROVED_C_P_EQUALS_MINUS_LOG_P_OVER_P",
    "TPC240_FIXED_Q_PRIMITIVE_ROW_NORM = PROVED_EXACT",
    "TPC240_RIEMANN_ROW_ASYMPTOTIC = PROVED_UNIFORM_ON_TOP_PRIME_SHELL_FOR_EACH_FIXED_PROFILE",
    "TPC240_KAPPA_RANGE = PROVED_ONE_HALF_LE_KAPPA_LE_ONE",
    "TPC240_DIRECT_ENERGY_CONSTANT = PROVED_1197_KAPPA_LOG_2_OVER_800",
    "TPC240_DIRECT_ENERGY_POWER = PROVED_X_1_OVER_96",
    "TPC240_DIRECT_FIXED_POWER_SAVING = REFUTED_ON_EXACT_Q_SPLIT_UNSIGNED_OBJECT",
    "TPC240_X_1_OVER_48_SHARPNESS = NOT_CLAIMED",
    "TPC240_CLASS_UNIFORM_PROFILE_THRESHOLD = NOT_CLAIMED",
    "TPC240_PLATEAU_PROFILE_SUBSTITUTION = FORBIDDEN",
    "TPC240_ARITHMETIC_ADVANCE = NO",
    "TPC240_L2 = NONE",
    "TPC240_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC240_STATUS = " + STATUS,
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
    spec = importlib.util.spec_from_file_location("tpc240_producer", PRODUCER)
    require(spec is not None and spec.loader is not None, "producer module spec")
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


def same_typed(candidate: object, expected: object) -> bool:
    if type(candidate) is not type(expected):
        return False
    if type(expected) is dict:
        return (
            candidate.keys() == expected.keys()
            and all(same_typed(candidate[key], expected[key]) for key in expected)
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
    require(type(record.get("denominator")) is int, label + " denominator type")
    require(record["denominator"] > 0, label + " denominator sign")
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
    require("1197 kappa_psi log(2)/800" in bridge, "leading constant missing")
    require("x^(1/96" in bridge, "direct exponent missing")
    require("x^(-23/2400)" in bridge, "relative error exponent missing")
    require("No threshold uniform over the entire profile class" in bridge,
            "profilewise quantifier firewall missing")
    require("It is not" in bridge and "the signed four-packet Gate-B scalar" in bridge,
            "signed-object firewall missing")

    proof_sources = (
        PROOF_PACKAGE.read_text(encoding="utf-8"),
        DERIVATION.read_text(encoding="utf-8"),
        ROW_PROOF.read_text(encoding="utf-8"),
        AGGREGATION_PROOF.read_text(encoding="utf-8"),
    )
    joined_proof = "\n".join(proof_sources)
    require("1197" in joined_proof and "1/96" in joined_proof,
            "proof constant/exponent missing")
    require("2M" in proof_sources[0] and "primitive" in proof_sources[0],
            "primitive injectivity proof missing")
    require("O_psi(H/(UQ))" in proof_sources[0], "aggregate error proof missing")
    require("=left(" not in joined_proof, "malformed LaTeX left delimiter")

    producer = load_producer()
    stored = json.loads(CERTIFICATE.read_text(encoding="ascii"))
    expected = producer.expected_document()
    validate(stored, expected)
    require(type(stored["certificate_version"]) is int
            and stored["certificate_version"] == 1, "certificate version")
    require(stored["payload_sha256"] == PAYLOAD_SHA256, "payload digest")

    ledger = stored["exact_fraction_ledger"]
    require(type(ledger) is dict, "fraction ledger type")
    exact_fraction(ledger["H_exponent"], Fraction(21, 32), "H exponent")
    exact_fraction(ledger["Q_exponent"], Fraction(1, 3), "Q exponent")
    exact_fraction(ledger["U_exponent"], Fraction(133, 400), "U exponent")
    exact_fraction(ledger["direct_energy_exponent"], Fraction(1, 96), "direct exponent")
    exact_fraction(ledger["leading_rational"], Fraction(1197, 800), "leading rational")
    exact_fraction(ledger["log_ratio"], Fraction(399, 400), "log ratio")
    exact_fraction(ledger["profile_kappa_lower"], Fraction(1, 2), "kappa lower")
    exact_fraction(ledger["profile_kappa_upper"], Fraction(1, 1), "kappa upper")
    exact_fraction(ledger["relative_error_exponent"], Fraction(-23, 2400),
                   "relative error")
    exact_fraction(ledger["row_depth_exponent"], Fraction(23, 2400), "row depth")
    require(Fraction(2, 3) - Fraction(21, 32) == Fraction(1, 96),
            "direct exponent arithmetic")
    require(Fraction(133, 400) + Fraction(1, 3) - Fraction(21, 32)
            == Fraction(23, 2400), "row-depth arithmetic")
    require(Fraction(3, 2) * Fraction(399, 400) == Fraction(1197, 800),
            "leading-rational arithmetic")

    lock = stored["object_lock"]
    require(type(lock) is dict, "object lock type")
    require(lock["main_object"] == OBJECT_KIND, "q-split object lock")
    require(lock["coefficient"] == "C_p=-log(p)/p", "coefficient lock")
    require(lock["profile_class"] == PROFILE_KIND, "profile class lock")
    require(lock["p_domain"] == "PRIMES_U_OVER_2_LT_P_LE_U", "p-shell lock")
    require(lock["q_domain"] == "PRIMES_Q_LT_Q_LE_2Q", "q-shell lock")
    require(lock["plateau_profile"] == "REJECTED_NOT_LITERAL_V59_CLASS",
            "plateau firewall")

    theorem = stored["theorem"]
    require(type(theorem) is dict and theorem["classification"] == "PROVED",
            "theorem classification")
    require(theorem["asymptotic"]
            == "D_top^psi=[1197*kappa_psi*log(2)/800+o_psi(1)]Q^2/H",
            "theorem asymptotic")
    require(theorem["quantifier"]
            == "FOR_EVERY_FIXED_ADMISSIBLE_PSI_AND_EPS_EXISTS_X0_PSI_EPS_FOR_ALL_X_GE_X0",
            "theorem quantifier")

    markers = stored["markers"]
    require(markers["TPC240_STATUS"] == STATUS, "status promotion")
    require(markers["TPC240_ROUTE_LEVEL"] == "PROVED_STRUCTURAL_L1_OBSTRUCTION",
            "route level")
    require(markers["TPC240_ARITHMETIC_ADVANCE"] == "NO", "arithmetic firewall")
    require(markers["TPC240_L2"] == "NONE", "L2 firewall")
    require(markers["TPC240_FULL_GATE_B"] == "OPEN", "Gate-B firewall")
    require(markers["TPC240_STRICT_1_OVER_400"] == "UNPAID_GLOBAL",
            "strict-saving firewall")

    firewall = stored["scope_firewall"]
    require(firewall["CLASS_UNIFORM_X0"] == "NOT_CLAIMED", "uniformity firewall")
    require(firewall["Q_COLLAPSED_X_1_OVER_48_SHARPNESS"] == "OPEN",
            "collision-sharpness firewall")
    require(firewall["SIGNED_C_H_CANCELLATION"] == "NONE", "signed C_h firewall")
    require(firewall["SIGNED_FOUR_PACKET_PROJECTION"] == "OPEN",
            "four-packet firewall")
    require(firewall["NUMERICAL_CHECKS_ARE_THEOREM_EVIDENCE"] is False,
            "numerical firewall")

    fixture = stored["finite_fixture"]
    require(type(fixture) is dict and fixture["classification"]
            == "NUMERICAL_FINITE_ILLUSTRATION_ONLY", "fixture classification")
    require((fixture["Q"], fixture["H"], fixture["U"]) == (101, 509, 97),
            "fixture scales")
    require(fixture["four_Q_less_than_H"] is True
            and fixture["U_less_than_Q"] is True, "fixture inequalities")
    require(fixture["top_prime_rows"] == 3 and len(fixture["rows"]) == 3,
            "fixture row count")
    for row in fixture["rows"]:
        require(type(row) is dict and row["injective"] is True, "row injectivity")
        require(row["primitive_support"] is True, "row primitive support")
        require(row["classification"] == "FINITE_ALGEBRAIC_FIXTURE_NOT_THEOREM_PROFILE",
                "row evidence class")
        direct_record = row["direct_energy"]
        residue_record = row["row_energy"]
        require(type(direct_record) is dict and type(residue_record) is dict,
                "row energy record type")
        direct_value = Fraction(direct_record["numerator"], direct_record["denominator"])
        residue_value = Fraction(residue_record["numerator"], residue_record["denominator"])
        require(direct_value == residue_value, "row energy identity")
        require(row["atom_count"] == 2 * row["cutoff"], "row atom count")

    require(stored["mutation_firewalls"]["rejected_count"] == 9, "mutation count")
    bad_status = deepcopy(stored)
    bad_status["markers"]["TPC240_STATUS"] = "PROVED_ARITHMETIC_L2_FULL_GATE_B"
    reject(bad_status, expected, "status promotion")
    bad_constant = deepcopy(stored)
    bad_constant["exact_fraction_ledger"]["leading_rational"]["numerator"] = 1196
    reject(bad_constant, expected, "wrong 1197/800")
    bad_type = deepcopy(stored)
    bad_type["certificate_version"] = True
    reject(bad_type, expected, "bool/int confusion")

    stress_source = STRESS.read_text(encoding="utf-8")
    independent_source = INDEPENDENT.read_text(encoding="utf-8")
    require("STANDARD_BUMP" in stress_source and "QUADRATIC_TILT_BUMP" in stress_source,
            "two smooth profile stresses missing")
    require("NUMERICAL_FINITE_ILLUSTRATION_ONLY" in stress_source,
            "stress evidence label missing")
    require("import tpc240_top_prime_energy_certificate" not in independent_source,
            "independent checker imports producer")
    require("assert " not in PRODUCER.read_text(encoding="utf-8"),
            "producer uses assert")

    print("TPC240_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("constant=1197*kappa_psi*log(2)/800")
    print("direct_energy=x^(1/96+o_psi(1))")
    print("fixed_power_direct_saving=REFUTED_SCOPED")
    print("q_collapsed_x_1_over_48_sharpness=OPEN")
    print("signed_gate_b=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC240_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError) as error:
        raise SystemExit("TPC240_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
