#!/usr/bin/env python3
"""Fail-closed checker for TPC-234 normalized collision stability."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-234-normalized-collision-bessel-stability"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_normalized_collision_bessel_stability.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
CODE = PROJECT / "code" / "normalized_collision.py"

LOCKS = {
    PROOF: "cd59d17bbe6c1d27f40b64558ab64f7a7388debf5971d7f7510d95af29fcce22",
    README: "3182e17d3f4dcba923be71499adca2f5f4a1c4d2ab14ae78ce9486ba675b4f3d",
    CERTIFICATE: "d49a2fed0bdd1a69ecdabe02868fc0cef5d6c32ca20b8e0a47687c5b5173f115",
}

MARKERS = (
    "TPC234_BUCKET_MULTIPLICITY_TWO = INHERITED_PROVED_EXACT",
    "TPC234_UNIT_ROW_NORMALIZATION = MODELING_TRANSFORM",
    "TPC234_NORMALIZED_SYNTHESIS_BESSEL_BOUND = PROVED_EXACT_2",
    "TPC234_NORMALIZED_GRAM_SPECTRUM = PROVED_EXACT_IN_0_2",
    "TPC234_OFFDIAGONAL_GRAM_NORM = PROVED_EXACT_LE_1",
    "TPC234_Q39_LITERAL_NORMALIZED_RATIOS = PROVED_EXACT_4_OVER_3_AND_2_OVER_3",
    "TPC234_NORMALIZATION_AUTOMATIC_SAVING = REFUTED_SCOPED",
    "TPC234_SOURCE_VALID_NORMALIZATION = OPEN",
    "TPC234_ARITHMETIC_ADVANCE = NO",
    "TPC234_L2 = NONE",
    "TPC234_FULL_GATE_B = OPEN",
)


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def digest(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def load_module():
    spec = importlib.util.spec_from_file_location("tpc234_normalized_collision", CODE)
    require(spec is not None and spec.loader is not None, "module load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
        require(path.is_file() and digest(path) == expected, "lock mismatch: " + str(path))
    proof = PROOF.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    for marker in MARKERS:
        require(marker in proof and marker in readme, "missing marker: " + marker)
    module = load_module()
    stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    validate(module.build_certificate(), stored)
    finite = stored["finite_reproduction"]
    require(finite["digest"] == "d6c3c62ea5698c5941c14fab872b8951dd1939e6f45484651a13e7ccc473bed9", "finite digest")
    require(len(finite["records"]) == 5, "scale count")
    require(all(row["max_bucket_multiplicity"] <= 2 for row in finite["records"]), "bucket multiplicity")
    literal = finite["literal_q39"]
    require(Fraction(literal["symmetric_ratio"]) == Fraction(4, 3), "symmetric ratio")
    require(Fraction(literal["antisymmetric_ratio"]) == Fraction(2, 3), "antisymmetric ratio")
    require(literal["shared_coordinates"] == [277, 815], "literal coordinates")
    require(stored["theorem"]["normalized_gram"] == "0 <= G <= 2I", "operator theorem")

    changed_bound = deepcopy(stored)
    changed_bound["theorem"]["normalized_gram"] = "0 <= G <= I"
    reject(changed_bound, stored, "false saving")
    changed_bucket = deepcopy(stored)
    changed_bucket["finite_reproduction"]["records"][0]["max_bucket_multiplicity"] = 3
    reject(changed_bucket, stored, "triple bucket")
    changed_source = deepcopy(stored)
    changed_source["firewall"]["source_valid_normalization"] = "PROVED"
    reject(changed_source, stored, "source upgrade")

    print("TPC234_BRIDGE_CHECK=PASS")
    print("claim=PROVED_STRUCTURAL_L1")
    print("normalized_gram=0_TO_2")
    print("literal_ratios=4/3,2/3")
    print("source_valid_normalization=OPEN")
    print("full_gate_b=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    try:
        run()
    except (CheckFailure, OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit("TPC234_BRIDGE_CHECK=FAIL: " + str(exc)) from exc


if __name__ == "__main__":
    main()
