#!/usr/bin/env python3
"""Fail-closed checker for the TPC-236 physical multi-wrap envelope."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-236-physical-multiwrap-collision-envelope"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_physical_multiwrap_collision_envelope.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
CODE = PROJECT / "code" / "physical_multiwrap.py"

LOCKS = {
    PROOF: "db33e93fbe2b180abee190063244d8c7daa92ab8bbc063785a2b704b4f033eb6",
    README: "e46d19f7252625dbb19501758380121e6230cf5c63e0a0a19dc95cc6ba1249de",
    CERTIFICATE: "d8baed3c3a7c16da7ff7b43676a1ca7348a9c9e7e5b3dd8b06802dc87cdf33df",
}

MARKERS = (
    "TPC236_PHYSICAL_ROW_INTERNAL_INJECTIVITY = PROVED_FOR_H_GT_4Q",
    "TPC236_BUCKET_GCD_FIBER_BOUND = PROVED_EXACT",
    "TPC236_BUCKET_MULTIPLICITY = PROVED_LE_8Q_SQUARED_OVER_H",
    "TPC236_WEIGHTED_FIXED_H_BESSEL = PROVED_EXACT_WITHOUT_ROW_NORMALIZATION",
    "TPC236_WEIGHTED_PHYSICAL_H_DIRECT_SUM = PROVED_EXACT",
    "TPC236_COMMON_LINEAR_PACKET_TRANSFORM = PRESERVED_WITH_OPERATOR_NORM",
    "TPC236_DIVISOR_WEIGHT_C_H = PRESERVED_EXPLICITLY",
    "TPC236_V59_MULTIPLICITY_TOLL = PROVED_4X_1_OVER_96_PLUS_4X_23_OVER_2400",
    "TPC236_Q101_TRIPLE_COLLISION = PROVED_EXACT",
    "TPC236_Q101_EQUAL_ROW_RATIO = PROVED_EXACT_3",
    "TPC236_PHYSICAL_MULTIPLICITY_TWO_TRANSFER = REFUTED_SCOPED",
    "TPC236_GCD_FIBER_REDUCTION = REQUIRED",
    "TPC236_CROSS_H_RATIONAL_FREQUENCY_REASSEMBLY = OPEN",
    "TPC236_C_H_WEIGHTED_CANCELLATION = OPEN",
    "TPC236_ARITHMETIC_ADVANCE = NO",
    "TPC236_L2 = NONE",
    "TPC236_FULL_GATE_B = OPEN",
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
    spec = importlib.util.spec_from_file_location("tpc236_physical_multiwrap", CODE)
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
    finite = stored["finite_reproduction"]
    require(finite["digest"] == "6ce0173091ebdc11d91a2bc57b27018c8d7c147a162d5962f5c2a6ef83f73a10", "finite digest")
    records = finite["records"]
    require(records["exponents"]["Q2_over_H"] == "1/96", "multiplicity exponent")
    require(records["exponents"]["maximum_depth"] == "23/2400", "depth exponent")
    triple = records["triple_collision"]
    require((triple["Q"], triple["H"], triple["U"], triple["h"]) == (101, 8830, 99, 80), "V59-shaped floors")
    require(triple["selected_rows"] == [113, 127, 193], "triple rows")
    require(triple["supports"] == {"113": [17, 63], "127": [17, 63], "193": [17, 63]}, "triple supports")
    require((triple["diagonal_energy"], triple["combined_energy"], triple["bessel_ratio"]) == (6, 18, "3"), "ratio three")
    gcd_case = records["gcd_adversary"]
    require((gcd_case["actual_multiplicity"], gcd_case["naive_modulus_h_bound"], gcd_case["gcd_reduced_bound"]) == (5, 4, 8), "gcd adversary")
    require(loaded.gcd_fiber_bound(16, 65, 8, 6)["reduced_modulus"] == 4, "reduced modulus")
    require(loaded.row_support(101, 8830, 80, 113) == (17, 63), "literal row support")
    require(Fraction(4 * 101 * 101, 8830) + Fraction(4 * 80 * 101, 8830) < Fraction(8 * 101 * 101, 8830), "two-term refinement")
    require(Fraction(2, 3) - Fraction(21, 32) == Fraction(1, 96), "V59 exponent arithmetic")

    false_multiplicity = deepcopy(stored)
    false_multiplicity["theorem"]["multiplicity_two"] = "PROVED"
    reject(false_multiplicity, stored, "multiplicity-two upgrade")
    false_cross_h = deepcopy(stored)
    false_cross_h["firewall"]["cross_h_rational_frequency_reassembly"] = "PROVED"
    reject(false_cross_h, stored, "cross-h upgrade")
    missing_weight = deepcopy(stored)
    missing_weight["source_lock"].pop("divisor_weight_C_h")
    reject(missing_weight, stored, "missing C_h")
    false_margin = deepcopy(stored)
    false_margin["firewall"]["benchmark_margin"] = "POSITIVE"
    reject(false_margin, stored, "benchmark margin upgrade")

    print("TPC236_BRIDGE_CHECK=PASS")
    print("claim=PROVED_STRUCTURAL_L1")
    print("physical_bucket_bound=8Q^2/H")
    print("v59_toll=(4+o(1))x^(1/96)")
    print("physical_multiplicity_two=REFUTED_SCOPED")
    print("q101_bessel_ratio=3")
    print("full_gate_b=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    try:
        run()
    except (CheckFailure, OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit("TPC236_BRIDGE_CHECK=FAIL: " + str(exc)) from exc


if __name__ == "__main__":
    main()
