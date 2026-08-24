#!/usr/bin/env python3
"""Fail-closed release checker for the TPC-239 primitive-bucket envelope."""

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
PROJECT = ROOT / "papers" / "tpc-239-brun-titchmarsh-primitive-bucket-envelope"
BRIDGE = ROOT / "research" / "tpc-big-road" / "bridge_b_brun_titchmarsh_primitive_bucket_envelope.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results" / "tpc239_certificate.json"
PRODUCER = PROJECT / "code" / "tpc239_bt_bucket_certificate.py"
PROOF_PACKAGE = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
INDEPENDENT = PROJECT / "experiments" / "tpc239_independent_checker.py"
PAPER_PROOF = PROJECT / "paper" / "sections" / "3_primitive_ap_compiler.tex"
PDF = PROJECT / "paper" / "paper.pdf"

TEXT_LOCKS = {
    BRIDGE: "45e53bd46346743b84c7a32a74354cc60eeae3bef6f9e73da43b5c4d653416fc",
    README: "38e65fde2e26415d1f627c75dd4f3382631b046d3455a6f05d230499335726ef",
    CERTIFICATE: "efb0ed53c65b5aa7825cb457e85b0102a66652dc4cd4e8eec13c2955347bee52",
    PRODUCER: "b789fd81e608df0ca0ef47952f352f3abe8915a3f411e3229e6b2d36f14758c0",
    PROOF_PACKAGE: "4d995e4630b38262d5ce032b0c18a18d184359699ea4f84d6ca7cb1637e6cd0c",
    DERIVATION: "7a9958b1994f9dce2cd6451ee92a100028a71c49667c4daa79755f8a84605606",
    INDEPENDENT: "eebd1592382960b174d549f3d7f44a3772e5220b4fda416c7e5da432dd030e9a",
    PAPER_PROOF: "354885fc0787509cc20eea4762439e044120ae17480470addc8a0856e80c473b",
}
PDF_RAW_SHA256 = "fb66154b3253ad1ef53250ce823bd0d271607b55844a6aeee7b7da52a4b33a88"

MARKERS = (
    "TPC239_PRIMITIVE_AP_REDUCTION = PROVED_EXACT_UPPER_COMPILER",
    "TPC239_BRUN_TITCHMARSH_INPUT = SOURCE_BACKED",
    "TPC239_BUCKET_MULTIPLICITY = PROVED_LE_16_Q_SQUARED_OVER_H_TIMES_H_OVER_PHI_H_OVER_LOG_2Q_OVER_H",
    "TPC239_V59_BUCKET_MULTIPLICITY = PROVED_X_1_OVER_96_LOGLOG_X_OVER_LOG_X",
    "TPC239_FINITE_WINDOW_PACKET_TRACE = PROVED_X_1_OVER_48_LOG_FOUR_LOGLOG",
    "TPC239_IMPROVEMENT_OVER_TPC237 = PROVED_FACTOR_LOG_X_OVER_LOGLOG_X",
    "TPC239_FIXED_POWER_IMPROVEMENT = NONE",
    "TPC239_ARITHMETIC_ADVANCE = NO",
    "TPC239_L2 = NONE",
    "TPC239_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC239_STATUS = PROVED_SOURCE_BACKED_PRIME_DENSITY_L1",
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


def producer_module():
    spec = importlib.util.spec_from_file_location("tpc239_producer", PRODUCER)
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
    for path, expected in TEXT_LOCKS.items():
        require(path.is_file(), "missing locked source: " + str(path))
        require(canonical_text_hash(path) == expected, "text lock mismatch: " + str(path))
    require(PDF.is_file() and raw_hash(PDF) == PDF_RAW_SHA256, "raw PDF lock mismatch")

    bridge = BRIDGE.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    for marker in MARKERS:
        require(marker in bridge, "bridge marker missing: " + marker)
    require("TPC239_STATUS = PROVED_SOURCE_BACKED_PRIME_DENSITY_L1" in readme,
            "README status marker")
    for source in (bridge, PROOF_PACKAGE.read_text(encoding="utf-8"),
                   DERIVATION.read_text(encoding="utf-8"),
                   PAPER_PROOF.read_text(encoding="utf-8")):
        require("16" in source and "log(2Q/h)" in source,
                "factor-16 or logarithmic denominator missing")
        require("a^(-1)m" in source or "a^{-1}m" in source or "a^{-1}m" in source,
                "primitive AP direction missing")

    loaded = producer_module()
    stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    validate(loaded.build_certificate(), stored)
    require(stored["schema_version"] == 1 and type(stored["schema_version"]) is int,
            "schema version")
    require(
        stored["payload_sha256"]
        == "8c11468ff035222a17a72a34d49322ea835a887b05310c821f5bb38cfede263e",
        "payload digest",
    )

    theorem = stored["exact_theorem_ledger"]
    require(type(theorem) is dict, "theorem ledger type")
    require(
        theorem["factor_16"]
        == "R_h(a) <= 16*(Q^2/H)*(h/phi(h))/log(2Q/h)",
        "factor-16 theorem",
    )
    require(theorem["h_one"] == "R_1(0)=0 because 2Q<H", "h=1 branch")
    require("x^(1/48)*(log x)^4*loglog x" in theorem["packet_trace"],
            "packet trace theorem")

    exponents = stored["exact_exponent_ledger"]
    exact_fraction(exponents["Q_over_U"], Fraction(1, 1200), "Q/U")
    exact_fraction(exponents["row_density_power"], Fraction(1, 96), "row density")
    exact_fraction(exponents["direct_energy_power"], Fraction(1, 96), "direct energy")
    exact_fraction(exponents["normalized_trace_power"], Fraction(1, 48), "normalized trace")
    exact_fraction(exponents["leading_unnormalized_power"], Fraction(49, 48), "unnormalized trace")
    exact_fraction(exponents["window_correction_power"], Fraction(-67, 200), "window correction")
    require(Fraction(1, 3) - Fraction(133, 400) == Fraction(1, 1200),
            "Q/U arithmetic")
    require(2 * Fraction(1, 3) - Fraction(21, 32) == Fraction(1, 96),
            "Q^2/H arithmetic")

    fixture = stored["finite_fixture"]
    require(type(fixture) is dict, "fixture type")
    require((fixture["Q"], fixture["H"], fixture["h"], fixture["M_h"]) == (101, 8830, 82, 1),
            "fixture scales")
    require(fixture["shell_prime_count"] == 20, "shell prime count")
    require(fixture["phi_h"] == 40 and len(fixture["buckets"]) == 40,
            "primitive bucket count")
    require(fixture["max_actual_R"] == 3 and fixture["max_ap_census"] == 3,
            "triple-collision fixture")
    for bucket in fixture["buckets"]:
        require(type(bucket) is dict, "bucket type")
        require(type(bucket["actual_R"]) is int and type(bucket["ap_census"]) is int,
                "bucket count type")
        require(bucket["actual_R"] <= bucket["ap_census"], "AP compiler order")
    require(stored["h_one_fixture"]["row_empty"] is True, "h=1 fixture")

    firewall = stored["scope_firewall"]
    require(firewall["ARITHMETIC_ADVANCE_IN_L2_GATE_B_SENSE"] == "NO",
            "arithmetic firewall")
    require(firewall["C_H_SIGNED_CANCELLATION"] == "NONE", "C_h firewall")
    require(firewall["SIGNED_FOUR_PACKET_PROJECTION"] == "NOT_PROVED",
            "packet firewall")
    require(firewall["FULL_GATE_B"] == "OPEN", "Gate-B firewall")
    require(firewall["STRICT_1_OVER_400"] == "UNPAID_GLOBAL", "strict-saving firewall")
    require(firewall["SHARPNESS"] == "NOT_CLAIMED", "sharpness firewall")
    require(firewall["NUMERICAL_CHECKS_ARE_THEOREM_EVIDENCE"] is False,
            "numerical firewall")
    require(stored["mutation_firewalls"]["rejected_count"] == 11, "mutation count")

    bad_factor = deepcopy(stored)
    bad_factor["exact_theorem_ledger"]["factor_16"] = "factor 15"
    reject(bad_factor, stored, "factor 15")
    bad_gate = deepcopy(stored)
    bad_gate["scope_firewall"]["FULL_GATE_B"] = "PASS"
    reject(bad_gate, stored, "Gate-B promotion")
    bad_type = deepcopy(stored)
    bad_type["schema_version"] = True
    reject(bad_type, stored, "bool schema")

    print("TPC239_BRIDGE_CHECK=PASS")
    print("claim=PROVED_SOURCE_BACKED_PRIME_DENSITY_L1")
    print("bucket=x^(1/96)*loglog(x)/log(x)")
    print("packet_trace=x^(1/48)*(log(x))^4*loglog(x)")
    print("fixed_power_improvement=NONE")
    print("signed_gate_b=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC239_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError) as error:
        raise SystemExit("TPC239_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
