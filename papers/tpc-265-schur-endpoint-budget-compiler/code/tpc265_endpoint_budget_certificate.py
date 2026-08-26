#!/usr/bin/env python3
"""Deterministic exact certificate for the TPC-265 budget compiler."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE_HEAD = "c58404738b9943293d610f2cf87ef6fb5c01ed4e"
PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
RESULT = PROJECT / "results/tpc265_certificate.json"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "5c67ac0868e5535fb917d2fd6e8ea4d68a1b5e4e27d443d04029dbe58964b4d8",
    "papers/tpc-264-orthogonal-residual-schur-firewall/README.md":
        "9de5427069e964d4d351cdf49a78d7f3ab71b0e992e5698d49106cd1e5971b22",
    "papers/tpc-264-orthogonal-residual-schur-firewall/PROOF_PACKAGE.md":
        "f3da6e2fcf0f992e4782f10c83936f5dc8f9c88e2a3ec9b2ff16bfb94c5422fa",
    "papers/tpc-264-orthogonal-residual-schur-firewall/notes/theorem_ledger.md":
        "f4d01f5a5e759a04b046394dd7f41dd6df021ed0fd7dd388fdd79a29b1eec0bb",
    "papers/tpc-264-orthogonal-residual-schur-firewall/notes/route_evaluation.md":
        "08bdf96437fb4cd335c499eae2a1f495b89da4dbc2685e333d2f1e691221151b",
    "research/tpc-big-road/bridge_b_orthogonal_residual_schur_firewall.md":
        "d945a257c862a955d03e8931a365e57191a2099ac3bae74d858389a492d0a9fb",
    "research/tpc-big-road/tpc_bridge_b_orthogonal_residual_schur_firewall_checker.py":
        "609e8fe8f2c94c401e7a599b958d36267537c72fb20e1834de87891faed88f23",
}

STATUS = "PROVED_EXACT_SCHUR_TO_ENDPOINT_BUDGET_COMPILER"
ROUND2_CLUE = "TEST_LITERAL_RESIDUAL_RADIUS_OR_PHASE_AGAINST_THE_TWO_LANE_BUDGET"

E0 = Fraction(5, 3)
TARGET = Fraction(1997, 1200)
REQUIRED = E0 - TARGET

FIREWALL = {
    "TPC265_ACTUAL_V59_PHASE": "OPEN",
    "TPC265_ACTUAL_V59_RADIUS": "OPEN",
    "TPC265_ARITHMETIC_ADVANCE": "NO",
    "TPC265_CIRCLE_WORST_CASE": "PROVED_EXACT",
    "TPC265_DISK_WORST_CASE": "PROVED_EXACT",
    "TPC265_FIXED_POWER_CREDIT": 0,
    "TPC265_FULL_GATE_B": "OPEN",
    "TPC265_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC265_L2": "NONE",
    "TPC265_LITERAL_PRIME_SHELL_COUNTEREXAMPLE": "NONE",
    "TPC265_LOG_CENTER_CREDIT": 0,
    "TPC265_LOG_RADIUS_CREDIT": 0,
    "TPC265_MAXIMUM_CLAIM": STATUS,
    "TPC265_ROUTE_ADVANCE": "YES_SCOPED_RESIDUAL_RADIUS_BUDGET_COMPILER",
    "TPC265_SCHUR_RADIAL_ENVELOPE": "PROVED_EXACT",
    "TPC265_STATUS": STATUS,
    "TPC265_STRICT_PAYMENT_THRESHOLD": "PROVED_EXACT_ONE_OVER_400",
    "TPC265_TWIN_PRIME_RESULT": "NONE",
    "TPC265_TWO_LANE_ENDPOINT_COMPILER": "PROVED_EXACT_CONDITIONAL",
}


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def frozen_blob(relative: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + relative],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"",
         "frozen source: " + relative)
    return result.stdout


def verify_sources() -> int:
    for relative, expected in SOURCE_HASHES.items():
        blob = frozen_blob(relative)
        need(hashlib.sha256(blob).hexdigest() == expected,
             "source hash: " + relative)
        need(len(blob) > 0, "empty source: " + relative)
    return len(SOURCE_HASHES)


def classify(effective: Fraction) -> str:
    if effective > REQUIRED:
        return "STRICT"
    if effective == REQUIRED:
        return "BORDERLINE"
    return "INSUFFICIENT"


def radial_audit() -> dict[str, Any]:
    center = Fraction(2)
    radius = Fraction(3)
    plus = center + radius
    minus = center - radius
    cancel = center - center
    need(plus == 5 and minus == -1 and cancel == 0, "disk endpoints")
    need(abs(plus) == abs(center) + radius, "disk supremum")
    need(abs(cancel) == max(abs(center) - radius, Fraction(0)),
         "disk infimum")
    circle_min = abs(abs(center) - radius)
    need(circle_min == 1, "circle infimum")
    independent_radii = (Fraction(1), Fraction(2), Fraction(3))
    total_radius = sum(independent_radii, Fraction(0))
    need(total_radius == 6, "Minkowski radius")
    need(abs(center) + total_radius == 8, "Minkowski supremum")
    return {
        "center": str(center),
        "disk_radius": str(radius),
        "disk_supremum": str(abs(center) + radius),
        "disk_infimum": str(max(abs(center) - radius, Fraction(0))),
        "disk_endpoint_values": [str(plus), str(minus), str(cancel)],
        "circle_supremum": str(abs(center) + radius),
        "circle_infimum": str(circle_min),
        "independent_lane_radii": [str(value) for value in independent_radii],
        "minkowski_radius": str(total_radius),
        "minkowski_supremum": str(abs(center) + total_radius),
    }


def budget_audit() -> dict[str, Any]:
    lanes = [
        ("strict_radius", Fraction(1, 320), Fraction(0), "RADIUS_POWER"),
        ("borderline", Fraction(1, 400), Fraction(0), "THRESHOLD"),
        ("loss_dominated", Fraction(1, 320), Fraction(1, 1200), "LOSS_TEST"),
        ("log_only", Fraction(0), Fraction(0), "LOG_ONLY"),
    ]
    records = []
    for name, delta, loss, scope in lanes:
        effective = delta - loss
        records.append({
            "classification": ("NO_FIXED_POWER" if name == "log_only"
                                else classify(effective)),
            "delta": str(delta),
            "effective": str(effective),
            "loss": str(loss),
            "margin_over_required": str(effective - REQUIRED),
            "name": name,
            "scope": scope,
        })
    need(records[0]["classification"] == "STRICT" and
         records[0]["effective"] == "1/320", "strict lane")
    need(records[1]["classification"] == "BORDERLINE", "borderline lane")
    need(records[2]["effective"] == "11/4800" and
         records[2]["classification"] == "INSUFFICIENT", "loss lane")
    need(records[3]["classification"] == "NO_FIXED_POWER", "log lane")
    return {
        "baseline_exponent": str(E0),
        "target_exponent": str(TARGET),
        "required_strict_saving": str(REQUIRED),
        "lanes": records,
    }


def build_certificate() -> dict[str, Any]:
    source_count = verify_sources()
    return {
        "baseline": {"head": BASELINE_HEAD, "source_count": source_count},
        "budget_audit": budget_audit(),
        "claim": STATUS,
        "epistemic_status": {
            "actual_v59_phase": "OPEN",
            "actual_v59_radius": "OPEN",
            "finite_radial_geometry": "PROVED_EXACT",
            "two_lane_compiler": "PROVED_EXACT_CONDITIONAL",
        },
        "firewall": dict(FIREWALL),
        "radial_audit": radial_audit(),
        "round2_clue": ROUND2_CLUE,
        "schema": "TPC265_SCHUR_ENDPOINT_BUDGET_CERTIFICATE_V1",
        "source_hashes": dict(SOURCE_HASHES),
    }


def check_result(expected: dict[str, Any]) -> None:
    need(RESULT.is_file(), "certificate missing")
    raw = RESULT.read_text(encoding="utf-8")
    need(raw == canonical_json(expected), "certificate is not canonical")
    need(json.loads(raw) == expected, "certificate semantics")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    need(args.check != args.emit, "choose exactly one mode")
    expected = build_certificate()
    if args.emit:
        sys.stdout.write(canonical_json(expected))
        return 0
    check_result(expected)
    print("TPC265_CERTIFICATE=PASS "
          f"sources={expected['baseline']['source_count']} "
          "radial_envelope=EXACT two_lane_compiler=CONDITIONAL "
          "strict_threshold=1/400 log_credit=0 actual_radius=OPEN")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC265_CERTIFICATE=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
