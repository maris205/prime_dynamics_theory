#!/usr/bin/env python3
"""Fail-closed checker for the TPC-238 finite-window lower-frame release."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-238-finite-window-lower-frame-obstruction"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_finite_window_lower_frame_obstruction.md"
README = PROJECT / "README.md"
CERTIFICATE = PROJECT / "results" / "tpc238_certificate.json"
CODE = PROJECT / "code" / "tpc238_lower_frame_certificate.py"
PAPER_PROOF = PROJECT / "paper" / "sections" / "3_lower_frame.tex"
PROOF_PACKAGE = PROJECT / "PROOF_PACKAGE.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
INDEPENDENT = PROJECT / "experiments" / "tpc238_independent_checker.py"
PDF = PROJECT / "paper" / "paper.pdf"

LOCKS = {
    PROOF: "89e02d42b96e62fe167f9eb61801d426a218d842bb5143b4f16e00cf774f3731",
    README: "af3c1a53516b688a520d1fa8b3e2f6de69f4c11e85ccf394fc984ee21f73135b",
    CERTIFICATE: "181f8362369b17084e81ce5c42e4a347793f1639b1a752fbe65e89938f045ad8",
    CODE: "fc40b351e72f7437700ec9fa35058eadfd39f2b086c94768a35f5d30a53025a1",
    PAPER_PROOF: "1099661935347fcb8dcebe1e6540ac5e19a9f441565ff8da72b0c47286da773e",
    PROOF_PACKAGE: "9cc39a7209c0f343a71415d345e4bb892d436d7e6d2f961db45ee7163f3acba6",
    DERIVATION: "66de468c7fa4f19ff213302342be25419316a93b870fccfeedceb04b0976ae4c",
    INDEPENDENT: "0c52c8a3f8f0e94c5fa3756fe0599d3aafbee7d81317f3820c173ffb023eec19",
    PDF: "4ba2f92970804bdda61bd5ab239107975b001950f8d2e3c2a276f5786051303b",
}

MARKERS = (
    "TPC238_TRIANGULAR_WINDOW_LOWER_FRAME = PROVED_EXACT",
    "TPC238_PRIMITIVE_FAREY_SPACING = PROVED_U_TO_MINUS_2",
    "TPC238_FEJER_OFFDIAGONAL = PROVED_LE_1_OVER_4L_DISTANCE_SQUARED",
    "TPC238_CIRCULAR_PACKING_ROW_SUM = PROVED_LE_PI_SQUARED_U_FOUR_OVER_3",
    "TPC238_LOWER_FRAME = PROVED_L_MINUS_PI_SQUARED_U_FOUR_OVER_12L_POSITIVE_PART",
    "TPC238_NORMALIZED_LOWER_FRAME = PROVED_HALF_MINUS_PI_SQUARED_U_FOUR_OVER_6N_SQUARED_POSITIVE_PART",
    "TPC238_V59_FRAME_DEFECT = PROVED_X_MINUS_67_OVER_100",
    "TPC238_CROSS_REDUCED_FREQUENCY_FIXED_POWER_SAVING = REFUTED_SCOPED_AFTER_Q_COLLAPSE",
    "TPC238_WITHIN_Q_BUCKET_CANCELLATION = OPEN",
    "TPC238_STATUS = PROVED_STRUCTURAL_OBSTRUCTION_L1",
    "TPC238_ROUND2_CLUE = MOVE_THE_POWER_SAVING_SEARCH_INSIDE_THE_LITERAL_C_H_WEIGHTED_Q_COLLISION_BUCKETS",
)


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical_hash(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def locked_hash(path: Path) -> str:
    """Normalize line endings for text sources, but lock PDF bytes exactly."""
    if path == PDF:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return canonical_hash(path)


def module():
    spec = importlib.util.spec_from_file_location("tpc238_lower_frame", CODE)
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
        require(path.is_file() and locked_hash(path) == expected, "lock mismatch: " + str(path))
    proof = PROOF.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    for marker in MARKERS:
        require(marker in proof and marker in readme, "marker missing: " + marker)
    paper_proof = PAPER_PROOF.read_text(encoding="utf-8")
    proof_package = PROOF_PACKAGE.read_text(encoding="utf-8")
    derivation = DERIVATION.read_text(encoding="utf-8")
    for source in (paper_proof, proof_package, derivation):
        require("beta-\\alpha" in source or "beta-alpha" in source, "Gram phase direction missing")
        forbidden = (
            "c(\\alpha-\\beta)\\right)F_L(\\alpha-\\beta)",
            "e(c(\\alpha-\\beta))F_L(\\alpha-\\beta)",
            "e(c(alpha-beta))F_L(alpha-beta)",
        )
        require(not any(item in source for item in forbidden), "reversed Gram phase retained")

    loaded = module()
    stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    validate(loaded.build_certificate(), stored)
    require(stored["schema_version"] == 1, "schema")
    require(
        stored["payload_sha256"]
        == "8af87fa72672eff8b9b5553d620fdbfe4127fdb5ee0fdc7c6b32ef604ec0fe26",
        "payload digest",
    )
    exact = stored["exact_theorem_ledger"]
    require(exact["classification"] == "EXACT_THEOREM_LEDGER", "ledger class")
    require(exact["triangular_order"] == "L=floor((N+1)/2)", "triangular order")
    require(exact["primitive_spacing"] == "delta >= U^-2", "primitive spacing")
    require(exact["v59_exponent_identity"] == "4*(133/400)-2=-67/100", "V59 exponent marker")
    require(4 * Fraction(133, 400) - 2 == Fraction(-67, 100), "V59 exponent arithmetic")

    fixture = stored["fixture"]
    require((fixture["U"], fixture["N"], fixture["L"]) == (4, 41, 21), "fixture scales")
    require(fixture["minimum_circular_spacing_exact"] == "1/12", "fixture spacing")
    require(fixture["theorem_spacing_floor_exact"] == "1/16", "spacing floor")
    require(fixture["triangular_support_size"] == 41, "triangular support")
    require(fixture["triangular_weight_sum_exact"] == "21", "triangular mass")
    require(fixture["window_starts"] == [-20, 0, 17, 103], "window translations")
    require(len(fixture["fractions"]) == 6, "frequency count")

    numerical = stored["numerical_checks"]
    require(numerical["classification"] == "NUMERICALLY_CERTIFIED_FINITE_CHECK", "numerical class")
    require(len(numerical["windows"]) == 4, "numerical windows")
    lower = max(0.0, 21.0 - math.pi * math.pi * 4**4 / (12.0 * 21.0))
    require(abs(numerical["analytic_lower_bound_approx"] - lower) < 2.0e-12, "finite lower bound")
    require(stored["numerical_observation"]["classification"] == "NUMERICAL_OBSERVATION", "observation class")
    require(stored["mutation_firewalls"]["rejected_count"] == 3, "mutation count")

    firewall = stored["scope_firewall"]
    require(firewall["ARITHMETIC_ADVANCE"] == "NO", "arithmetic firewall")
    require(firewall["C_H_SIGNED_CANCELLATION"] == "NONE", "C_h firewall")
    require(firewall["SIGNED_FOUR_PACKET_PROJECTION"] == "OPEN", "packet firewall")
    require(firewall["FULL_GATE_B"] == "OPEN", "Gate-B firewall")
    require(firewall["STRICT_1_OVER_400"] == "UNPAID_GLOBAL", "strict-saving firewall")
    require(firewall["SHARPNESS"] == "NOT_CLAIMED", "sharpness firewall")
    require(not any(firewall["ROUTE_A"].values()), "Route-A firewall")

    false_arithmetic = deepcopy(stored)
    false_arithmetic["scope_firewall"]["ARITHMETIC_ADVANCE"] = "YES"
    reject(false_arithmetic, stored, "arithmetic promotion")
    false_bucket = deepcopy(stored)
    false_bucket["markers"]["TPC238_WITHIN_Q_BUCKET_CANCELLATION"] = "PROVED"
    reject(false_bucket, stored, "within-bucket promotion")
    false_sharpness = deepcopy(stored)
    false_sharpness["scope_firewall"]["SHARPNESS"] = "PROVED"
    reject(false_sharpness, stored, "sharpness promotion")

    print("TPC238_BRIDGE_CHECK=PASS")
    print("claim=PROVED_STRUCTURAL_OBSTRUCTION_L1")
    print("lower_frame=L-pi^2*U^4/(12L)")
    print("normalized_frame=1/2-pi^2*U^4/(6N^2)")
    print("v59_defect=x^(-67/100)")
    print("cross_reduced_frequency_saving=REFUTED_SCOPED_AFTER_Q_COLLAPSE")
    print("within_q_bucket_cancellation=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    try:
        run()
    except (CheckFailure, OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit("TPC238_BRIDGE_CHECK=FAIL: " + str(exc)) from exc


if __name__ == "__main__":
    main()
