#!/usr/bin/env python3
"""Fail-closed checker for the TPC-233 critical row-mass obstruction."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-233-critical-depth-row-mass-obstruction"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_critical_depth_row_mass_obstruction.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
CODE = PROJECT / "code" / "critical_row_mass.py"

LOCKS = {
    PROOF: "412a94d174f6242f8390c0e33b93b898c0dda5223d61b12e3df800723c38edbc",
    README: "c25a25e41e17b32615dd87b531b9582cdaf02890d00566dd152f54d963f057e8",
    CERTIFICATE: "328534ea9335d2a88375e8863a197c7061bc216e96e0675610771d7172a54ac3",
}

REQUIRED_MARKERS = (
    "TPC233_CRITICAL_PRIMORIAL_CLOCK = PROVED_EXACT",
    "TPC233_CRITICAL_SCALE_RELATION = PROVED_ASYMPTOTIC",
    "TPC233_LOW_HIGH_PRIME_ROWS = PROVED_SOURCE_BACKED",
    "TPC233_RAW_COMPARABILITY_DIVERGES = PROVED_ASYMPTOTIC",
    "TPC233_FIXED_COMPARABILITY_FROM_GEOMETRY = REFUTED_SCOPED",
    "TPC233_ROW_NORMALIZATION_REPAIR = OPEN",
    "TPC233_ACTUAL_V59_ROW_WEIGHTS = OPEN",
    "TPC233_ARITHMETIC_ADVANCE = NO",
    "TPC233_L2 = NONE",
    "TPC233_FULL_GATE_B = OPEN",
)


class CheckFailure(RuntimeError):
    pass


def canonical_hash(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def load_module():
    spec = importlib.util.spec_from_file_location("tpc233_critical_row_mass", CODE)
    require(spec is not None and spec.loader is not None, "cannot load TPC233 code")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_payload(candidate: dict[str, object], expected: dict[str, object]) -> None:
    require(type(candidate) is dict, "payload must be a dictionary")
    require(candidate == expected, "certificate payload mismatch")


def must_reject(candidate: dict[str, object], expected: dict[str, object], label: str) -> None:
    try:
        validate_payload(candidate, expected)
    except CheckFailure:
        return
    raise CheckFailure("mutation accepted: " + label)


def run() -> None:
    for path, expected_hash in LOCKS.items():
        require(path.is_file(), "missing locked file: " + str(path))
        require(canonical_hash(path) == expected_hash, "hash mismatch: " + str(path))
    proof_text = PROOF.read_text(encoding="utf-8")
    readme_text = README.read_text(encoding="utf-8")
    for marker in REQUIRED_MARKERS:
        require(marker in proof_text, "proof marker missing: " + marker)
        require(marker in readme_text, "README marker missing: " + marker)

    module = load_module()
    generated = module.build_certificate()
    stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    validate_payload(generated, stored)
    require(stored["schema"] == "tpc233-critical-depth-row-mass-obstruction-v1", "schema")
    finite = stored["finite_reproduction"]
    require(finite["record_count"] == 4, "fixture count")
    records = finite["records"]
    require([row["L"] for row in records] == [5, 7, 11, 13], "fixture depths")
    require(all(row["low_atoms"] == 2 for row in records), "low atom identity")
    require(all(row["high_atoms"] == 2 * (1 + row["prime_interval_count"]) for row in records), "high atom identity")
    require(all(row["row_mass_ratio"] <= row["universal_kappa_cap"] for row in records), "universal cap")
    require(finite["records_sha256"] == "93fec725ce67b017dffcf4b04ecb4125dd67b241d6e5cd12f18015fb0ee0f15c", "record digest")

    changed_ratio = deepcopy(stored)
    changed_ratio["finite_reproduction"]["records"][0]["row_mass_ratio"] += 1
    must_reject(changed_ratio, stored, "row mass ratio")
    changed_firewall = deepcopy(stored)
    changed_firewall["firewall"]["row_normalization_repair"] = "PROVED"
    must_reject(changed_firewall, stored, "normalization upgrade")
    missing_record = deepcopy(stored)
    missing_record["finite_reproduction"]["records"].pop()
    must_reject(missing_record, stored, "missing fixture")

    print("TPC233_BRIDGE_CHECK=PASS")
    print("claim=PROVED_ARITHMETIC_OBSTRUCTION_L1")
    print("critical_raw_comparability=REFUTED_SCOPED")
    print("fixtures=4")
    print("arithmetic_advance=NO")
    print("full_gate_b=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    try:
        run()
    except (CheckFailure, OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit("TPC233_BRIDGE_CHECK=FAIL: " + str(exc)) from exc


if __name__ == "__main__":
    main()
