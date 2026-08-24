#!/usr/bin/env python3
"""Fail-closed checker for the TPC-237 collision-compressed reassembly."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-237-collision-compressed-finite-window-reassembly"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_collision_compressed_finite_window_reassembly.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
CODE = PROJECT / "code" / "finite_window_physical_reassembly.py"

LOCKS = {
    PROOF: "26bfc0e3bf42931b44ba4b82cd34ff3ef4d8b9188e146f46997d58a210ec0310",
    README: "e6a865d48ae84f2046736e21949d9f1ac5588dcd5a4eb6fa70d67f976cf4aa62",
    CERTIFICATE: "2fb55176600c3b2461ba9018e8c7369cfa0afdcb18800a9afeaf32aee3fe709d",
    CODE: "fe024c9c196dd5b318425277c23c132e64e02d00f9e8b2915fa1cad184cc7b49",
}

MARKERS = (
    "TPC237_PRIMITIVE_FREQUENCY_INDEX = REQUIRED_EXACT",
    "TPC237_Q_COLLISION_BEFORE_LARGE_SIEVE = PROVED_EXACT_COMPOSITION",
    "TPC237_PRIMITIVE_BUCKET_FACTOR = PROVED_LE_4Q_SQUARED_OVER_H_PLUS_4UQ_OVER_H",
    "TPC237_FINITE_WINDOW_PACKET_TRACE = PROVED_STRUCTURAL",
    "TPC237_NORMALIZED_MAIN_EXPONENT = PROVED_1_OVER_48",
    "TPC237_NORMALIZED_SECONDARY_EXPONENT = PROVED_1_OVER_50",
    "TPC237_UNNORMALIZED_MAIN_EXPONENT = PROVED_49_OVER_48",
    "TPC237_OLD_P_COLLAPSE = REPLACED_BY_PHYSICAL_COLLISION_FACTOR",
    "TPC237_SIMULTANEOUS_SATURATION = NOT_CLAIMED",
    "TPC237_C_H_SIGNED_CANCELLATION = NONE",
    "TPC237_SIGNED_FOUR_PACKET_GATE_B_SCALAR = OPEN",
    "TPC237_ARITHMETIC_ADVANCE = NO",
    "TPC237_FIXED_ATOM_CREDIT = 0",
    "TPC237_L2 = NONE",
    "TPC237_FULL_GATE_B = OPEN",
    "TPC237_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
)


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical_hash(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def module():
    spec = importlib.util.spec_from_file_location("tpc237_reassembly", CODE)
    require(spec is not None and spec.loader is not None, "module load")
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def validate(candidate: dict[str, object], expected: dict[str, object]) -> None:
    require(type(candidate) is dict and candidate == expected, "payload mismatch")


def reject(candidate: dict[str, object], expected: dict[str, object], label: str) -> None:
    try:
        validate(candidate, expected)
    except CheckFailure:
        return
    raise CheckFailure("mutation accepted: " + label)


def run() -> None:
    for path, expected in LOCKS.items():
        require(path.is_file() and canonical_hash(path) == expected, "lock mismatch: " + str(path))
    proof = PROOF.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    for marker in MARKERS:
        require(marker in proof and marker in readme, "marker missing: " + marker)

    loaded = module()
    stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    validate(loaded.build_certificate(), stored)
    require(stored["schema"] == "tpc237-collision-compressed-finite-window-reassembly-v1", "schema")
    finite = stored["finite_reproduction"]
    require(finite["digest"] == "41acb31d49f21e305e97941038b96ef0f6c938474e1e02cb0085f9ae01044848", "finite digest")
    exponents = finite["records"]["exponents"]
    require(exponents["Q2_over_H"] == "1/96", "collision exponent")
    require(exponents["UQ_over_H"] == "23/2400", "secondary factor")
    require(exponents["main_product"] == "1/48", "main exponent")
    require(exponents["secondary_product"] == "1/50", "secondary exponent")
    require(exponents["window_U2_over_x"] == "-67/200", "window exponent")
    require(exponents["unnormalized_main"] == "49/48", "unnormalized exponent")
    require(2 * Fraction(1, 96) == Fraction(1, 48), "independent main arithmetic")
    require(Fraction(1, 96) + Fraction(23, 2400) == Fraction(1, 50), "independent secondary arithmetic")

    fixture = finite["records"]["physical_window_fixture"]
    require((fixture["Q"], fixture["H"], fixture["U"], fixture["h"]) == (101, 8830, 99, 82), "fixture scales")
    require(fixture["selected_q"] == [109, 137, 191], "fixture primes")
    require(fixture["primitive_frequencies"] == [[82, 3], [82, 79]], "primitive frequencies")
    require(fixture["rational_C_h"] == "1/82", "rational source reproduction")
    require(fixture["direct_packet_energy"] == "3/1681", "direct energy")
    require(fixture["collapsed_packet_trace"] == "5/1681", "collapsed trace")
    require(fixture["packet_trace_collision_ratio"] == "5/3", "trace ratio")
    require(fixture["exact_window_energy"] == "10/41", "window energy")
    require(fixture["nonprimitive_frequency_mutation"] == "REJECTED", "primitive mutation")
    require(Fraction(fixture["exact_window_energy"]) <= Fraction(fixture["large_sieve_rhs"]), "large-sieve order")
    require(Fraction(fixture["large_sieve_rhs"]) <= Fraction(fixture["collision_composed_rhs"]), "collision composition order")

    loaded.validate_reduced_frequency_pairs(((82, 3), (82, 79)), 99)
    for bad in (((82, 6),), ((82, 3), (164, 6))):
        rejected = False
        try:
            loaded.validate_reduced_frequency_pairs(bad, 200)
        except loaded.ReassemblyFailure:
            rejected = True
        require(rejected, "bad frequency accepted")

    false_sign = deepcopy(stored)
    false_sign["firewall"]["C_h_signed_cancellation"] = "PROVED"
    reject(false_sign, stored, "signed C_h promotion")
    false_gate = deepcopy(stored)
    false_gate["firewall"]["full_gate_b"] = "PASS"
    reject(false_gate, stored, "Gate-B promotion")
    false_sharp = deepcopy(stored)
    false_sharp["firewall"]["sharpness"] = "PROVED"
    reject(false_sharp, stored, "sharpness promotion")
    hidden_p = deepcopy(stored)
    hidden_p["normalization_loss_ledger"]["hidden_P_factor"] = "P"
    reject(hidden_p, stored, "hidden P factor")

    print("TPC237_BRIDGE_CHECK=PASS")
    print("claim=PROVED_STRUCTURAL_L1")
    print("primitive_frequency_index=REQUIRED_EXACT")
    print("normalized_envelope=x^(1/48)+x^(1/50)")
    print("unnormalized_main_exponent=49/48")
    print("signed_C_h_cancellation=NONE")
    print("full_gate_b=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    try:
        run()
    except (CheckFailure, OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit("TPC237_BRIDGE_CHECK=FAIL: " + str(exc)) from exc


if __name__ == "__main__":
    main()
