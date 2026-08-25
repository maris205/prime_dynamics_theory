#!/usr/bin/env python3
"""Fail-closed release checker for TPC-242 phase-Fourier separation."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-242-phase-fourier-collision-separation"
BRIDGE = ROOT / "research" / "tpc-big-road" / "bridge_b_phase_fourier_collision_separation.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results" / "tpc242_certificate.json"
PRODUCER = PROJECT / "code" / "tpc242_phase_fourier_certificate.py"
PROOF_PACKAGE = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
INDEPENDENT = PROJECT / "experiments" / "tpc242_independent_checker.py"
STRESS = PROJECT / "experiments" / "tpc242_phase_stress.py"
SPECTRUM_PROOF = PROJECT / "paper" / "sections" / "3_phase_fourier_theorem.tex"
DISK_PROOF = PROJECT / "paper" / "sections" / "4_feasible_disk.tex"
NO_TRANSFER_PROOF = PROJECT / "paper" / "sections" / "5_tpc241_no_transfer.tex"
PDF = PROJECT / "paper" / "paper.pdf"

TEXT_LOCKS = {
    BRIDGE: "3a6783dc1e5798e2876bd0cdd1eee230a457749738e0f4b05685ca32e4ad0dac",
    README: "078e83b0803ef9acbee5e41a55f3aca306a2e8d643a7744821e954d39efb9f32",
    CERTIFICATE: "3fbfb15e80df38d4377bc166feaf43fd6da3e9a14d5436e6f3533b449fae551a",
    PRODUCER: "336e5a5dd8c7ed60f22e61a018ffd9cdd2e40efe1d291c4d3e86ff67aba4611b",
    PROOF_PACKAGE: "b195b1247b415499476c90c9e9e5cc7f20eff526b439790075152ceac7ce31ba",
    DERIVATION: "8862124bc5ecfb30a7b94240382cdd6f167b92ccd32e0bd140c2e2c9fcaee6c5",
    INDEPENDENT: "2e4dcd2e5f43f389f40b5a470cfdafdb32e3fb070f1bd846d76329e98641cc0c",
    STRESS: "a789e9082a4751090d5177cc996f22159576cd54a8fb694d2751fcbde41cc2fb",
    SPECTRUM_PROOF: "a05a6d80f7028df694c81326218f2161dea104581ca7a52c7ff31b66d2087cc0",
    DISK_PROOF: "a13a53c66db726e76608bb579b8e26626e762b57f0fbcdb2a769ba41e194f665",
    NO_TRANSFER_PROOF: "c387a12c8e2537d095c33960860036a7a48f5e38dcaee178e150955f4697d666",
}
PDF_RAW_SHA256 = "e661fd4ba04437a34d0b1aaec789ec271301244ccfa322767815a5e141a8e2e6"
PAYLOAD_SHA256 = "dc4b16ae202183f9e088bf4524627a74a98ca6f2b957667265a5be9d7913a8a3"

STATUS = "PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER"
MUTATIONS = [
    "bool_int_confusion",
    "common_offset_projection",
    "duplicate_json_key",
    "f2_zero",
    "inner_product_orientation",
    "nonfinite_json_constant",
    "phase_sign_i_j_vs_minus_i_j",
    "physical_attachment",
    "status_promotion",
]
MARKERS = (
    "TPC242_V59_PHASE_CONVENTION = PROVED_I_POWER_J_SELECTS_X_CONJUGATE_Y",
    "TPC242_COMPLETE_PHASE_SPECTRUM = PROVED_F0_TOTAL_F1_ORIENTED_CROSS_F2_ZERO_F3_CONJUGATE_CROSS",
    "TPC242_PHASE_BLIND_ADDITIVE_TERM = PROVED_TRIVIAL_CHARACTER_ONLY",
    "TPC242_FIXED_F0_FEASIBLE_SET = PROVED_CLOSED_DISK_RADIUS_F0_OVER_TWO",
    "TPC242_PHASE_DEFECT_IDENTITY = PROVED_IMBALANCE_SQUARED_PLUS_FOUR_GRAM_DETERMINANT",
    "TPC242_TPC241_DIRECT_SIGNED_CREDIT = ZERO",
    "TPC242_TPC241_TO_V59_IDENTIFICATION = OPEN",
    "TPC242_PHYSICAL_TOP_PRIME_ANNIHILATION = NOT_CLAIMED",
    "TPC242_LITERAL_C_H_SIGNED_CANCELLATION = NONE",
    "TPC242_ARITHMETIC_ADVANCE = NO",
    "TPC242_FIXED_ATOM_CREDIT = 0",
    "TPC242_L2 = NONE",
    "TPC242_FULL_GATE_B = OPEN",
    "TPC242_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC242_STATUS = " + STATUS,
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


def load_producer():
    spec = importlib.util.spec_from_file_location("tpc242_producer", PRODUCER)
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

    bridge = BRIDGE.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    for marker in MARKERS:
        require(marker in bridge, "bridge marker missing: " + marker)
    require("**not** claim\nthat the physical top-prime mode vanishes" in readme,
            "README physical-annihilation firewall")
    require("|F_1|<=S/2" in readme, "README sharp disk")
    require("F_2=0" in readme and "F_1=<Y,X>" in readme,
            "README complete-spectrum markers")
    require("does not prove that the physical top-prime contribution vanishes" in bridge,
            "bridge physical-annihilation firewall")
    require("A 1_(k=0)" in bridge, "bridge common-offset projection")

    proof_parts = (
        PROOF_PACKAGE.read_text(encoding="utf-8"),
        DERIVATION.read_text(encoding="utf-8"),
        SPECTRUM_PROOF.read_text(encoding="utf-8"),
        DISK_PROOF.read_text(encoding="utf-8"),
        NO_TRANSFER_PROOF.read_text(encoding="utf-8"),
    )
    joined = "\n".join(proof_parts)
    require("F_2 = 0" in proof_parts[0] and "F_1 = <Y,X>" in proof_parts[0],
            "proof complete spectrum")
    require("S^2-4|F_1|^2" in proof_parts[0], "proof defect identity")
    require("zero direct quantitative implication" in joined,
            "typed no-transfer statement")
    require("does not prove that the physical" in joined,
            "physical-value firewall")
    require("=left(" not in joined, "malformed LaTeX delimiter")

    producer = load_producer()
    raw = CERTIFICATE.read_bytes()
    stored = producer.strict_json_loads(raw.decode("ascii"))
    expected = producer.build_document()
    validate(stored, expected)
    require(raw == producer.canonical_json(stored) + b"\n",
            "noncanonical certificate bytes")
    require(stored["payload_sha256"] == PAYLOAD_SHA256, "payload digest")
    require(type(stored["certificate_version"]) is int
            and stored["certificate_version"] == 1, "certificate version")

    theorem = stored["theorem"]
    require(theorem["classification"] == "PROVED_STRUCTURAL_L1_ONLY",
            "theorem classification")
    require(theorem["complete_spectrum"] == {
        "F_0": "||X||^2+||Y||^2",
        "F_1": "<Y,X>",
        "F_2": "0",
        "F_3": "<X,Y>",
    }, "complete spectrum")
    require(theorem["fixed_energy_feasible_set"] ==
            "{z in C: |z|<=S/2},INCLUDING_S=0", "sharp disk")
    require(theorem["phase_blind_additive_scalar"] ==
            "DELTA_F_0=A_AND_DELTA_F_1=DELTA_F_2=DELTA_F_3=0",
            "common-offset theorem")

    lock = stored["object_lock"]
    require(lock["inner_product"] == "CONJUGATE_LINEAR_FIRST_LINEAR_SECOND",
            "inner-product convention")
    require(lock["energy_phase"] == "E_j=||X+i^jY||^2",
            "energy phase")
    require(lock["fourier_phase"] == "F_k=(1/4)sum_j i^(k*j)E_j",
            "Fourier phase")
    require(lock["selected_mode"] == "F_1=<Y,X>", "selected orientation")

    firewall = stored["scope_firewall"]
    require(firewall["TPC241_TO_V59_IDENTIFICATION"] == "OPEN",
            "attachment firewall")
    require(firewall["TPC241_DIRECT_QUANTITATIVE_IMPLICATION_FOR_F1"] == "ZERO",
            "direct-credit firewall")
    require(firewall["PHYSICAL_TOP_PRIME_MODE_ANNIHILATION"] == "NOT_CLAIMED",
            "annihilation firewall")
    require(firewall["ARITHMETIC_L2"] == "NONE"
            and firewall["FULL_GATE_B"] == "OPEN", "Gate-B promotion")
    require(type(firewall["FIXED_ATOM_CREDIT"]) is int
            and firewall["FIXED_ATOM_CREDIT"] == 0, "fixed-atom type")
    require(firewall["FINITE_CERTIFICATE_IS_THEOREM_EVIDENCE"] is False,
            "finite-evidence firewall")

    ledger = stored["status_ledger"]
    require(ledger["status"] == STATUS and ledger["claim_ceiling"] == STATUS,
            "status ceiling")
    require(ledger["arithmetic_advance"] == "NO", "arithmetic firewall")
    require(stored["mutation_firewalls"]["rejected"] == MUTATIONS,
            "mutation registry")
    require(type(stored["mutation_firewalls"]["rejected_count"]) is int
            and stored["mutation_firewalls"]["rejected_count"] == len(MUTATIONS),
            "mutation count")

    bad_status = deepcopy(stored)
    bad_status["status_ledger"]["arithmetic_advance"] = "YES"
    reject(bad_status, expected, "status promotion")
    bad_orientation = deepcopy(stored)
    bad_orientation["object_lock"]["selected_mode"] = "F_1=<X,Y>"
    reject(bad_orientation, expected, "orientation reversal")
    bad_second_mode = deepcopy(stored)
    bad_second_mode["theorem"]["complete_spectrum"]["F_2"] = "NONZERO"
    reject(bad_second_mode, expected, "nonzero F2")
    bad_type = deepcopy(stored)
    bad_type["certificate_version"] = True
    reject(bad_type, expected, "bool/int confusion")

    independent_source = INDEPENDENT.read_text(encoding="utf-8")
    producer_source = PRODUCER.read_text(encoding="utf-8")
    require("import tpc242_phase_fourier_certificate" not in independent_source,
            "independent checker imports producer")
    require("from tpc242_phase_fourier_certificate" not in independent_source,
            "independent checker imports producer symbols")
    require("assert " not in producer_source and "assert " not in independent_source,
            "assert-based theorem guard")
    stress_source = STRESS.read_text(encoding="utf-8")
    require("range(-1, 2)" in stress_source and "len(vectors) ** 2" in stress_source,
            "stress census construction")

    print("TPC242_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("complete_spectrum=F0_TOTAL_F1_ORIENTED_CROSS_F2_ZERO_F3_CONJUGATE")
    print("fixed_energy_feasible_set=CLOSED_DISK_RADIUS_S_OVER_TWO")
    print("tpc241_direct_F1_credit=ZERO")
    print("physical_top_prime_attachment=OPEN")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC242_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, UnicodeError) as error:
        raise SystemExit("TPC242_BRIDGE_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
