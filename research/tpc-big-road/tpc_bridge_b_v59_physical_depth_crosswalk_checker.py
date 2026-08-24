#!/usr/bin/env python3
"""Fail-closed checker for the TPC-235 V59 physical-depth crosswalk."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-235-v59-physical-depth-crosswalk"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_v59_physical_depth_crosswalk.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
CODE = PROJECT / "code" / "v59_crosswalk.py"

LOCKS = {
    PROOF: "4fe34596423f53ac08e157678cadd5cf914058809341b4ade5b0c4b2ed6eccd7",
    README: "715e3f3ae24aa026ccd8a3cd08bdb49b59dae9afb7e66fae92743649b0dfa148",
    CERTIFICATE: "35a4fe3b77c77f4a893b8679c10ab97eadec45abccbec6e72fb8e4d35c056f89",
}

MARKERS = (
    "TPC235_V59_PHYSICAL_DEPTH_VARIABLE = PROVED_EXACT_LAMBDA_H_EQ_HQ_OVER_H",
    "TPC235_PHYSICAL_ROW_REPARAMETERIZATION = PROVED_EXACT",
    "TPC235_SINGLE_CLOCK_COMPATIBILITY_IFF_H_EQ_4Q_SQUARED = PROVED_EXACT",
    "TPC235_V59_CLOCK_RATIO = PROVED_EXACT_4X_TO_1_OVER_96",
    "TPC235_TPC226_EXACT_SINGLE_CLOCK_ATTACHMENT = REFUTED_SCOPED",
    "TPC235_PHYSICAL_DEPTH_RANGE = PROVED_EXACT_HALF_TO_X_23_OVER_2400",
    "TPC235_PHYSICAL_DENOMINATOR_GRID_PER_DEPTH = PROVED_X_31_OVER_96",
    "TPC235_FULL_H_SUM = SOURCE_LOCKED_REQUIRED",
    "TPC235_COMMON_PACKET_TRANSFORM = SOURCE_LOCKED_REQUIRED",
    "TPC235_OUTPUT_UNIT_NORMALIZATION_POLARIZATION = REFUTED_SCOPED",
    "TPC235_SOURCE_VALID_NORMALIZATION = OPEN_WEIGHTED_LINEAR_ONLY",
    "TPC235_ARITHMETIC_ADVANCE = NO",
    "TPC235_L2 = NONE",
    "TPC235_FULL_GATE_B = OPEN",
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
    spec = importlib.util.spec_from_file_location("tpc235_v59_crosswalk", CODE)
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
    stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    validate(module().build_certificate(), stored)
    finite = stored["finite_reproduction"]
    require(finite["digest"] == "f2c12f8cfc21d0cfe6ce95c68462d04da646fd06ee61b5b661ecd39c3be4c4b4", "finite digest")
    records = finite["records"]
    require(records["floor_profile"]["lambda"] == "10/3", "physical depth")
    require(records["floor_profile"]["physical_cutoff"] == 5, "physical cutoff")
    require(records["floor_profile"]["modulus_matched_model_cutoff"] == 0, "mismatch cutoff")
    require(records["exponents"]["Q2_over_H"] == "1/96", "clock exponent")
    require(records["exponents"]["H_over_Q"] == "31/96", "grid exponent")
    require(records["exponents"]["UQ_over_H"] == "23/2400", "depth exponent")
    polarization = records["polarization"]
    require(polarization["raw_polarized_value"] == ["2", "0"], "raw polarization")
    require(polarization["unit_output_polarized_value"] == ["0", "0"], "normalized polarization")
    require(Fraction(2, 3) - Fraction(21, 32) == Fraction(1, 96), "exponent arithmetic")

    false_attachment = deepcopy(stored)
    false_attachment["firewall"]["tpc226_exact_single_clock_attachment"] = "PROVED"
    reject(false_attachment, stored, "single-clock upgrade")
    false_normalization = deepcopy(stored)
    false_normalization["firewall"]["source_valid_normalization"] = "PROVED"
    reject(false_normalization, stored, "normalization upgrade")
    missing_weight = deepcopy(stored)
    missing_weight["source_lock"].pop("divisor_weight_C_h")
    reject(missing_weight, stored, "missing C_h")

    print("TPC235_BRIDGE_CHECK=PASS")
    print("claim=PROVED_STRUCTURAL_L1")
    print("physical_depth=lambda_h=hQ/H")
    print("single_clock_attachment=REFUTED_SCOPED")
    print("output_normalization=REFUTED_SCOPED")
    print("next=WEIGHTED_PHYSICAL_H_FIBER")
    print("full_gate_b=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    try:
        run()
    except (CheckFailure, OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit("TPC235_BRIDGE_CHECK=FAIL: " + str(exc)) from exc


if __name__ == "__main__":
    main()
