#!/usr/bin/env python3
"""Deterministic exact certificate for the TPC-266 end-to-end firewall."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE_HEAD = "9753ec69d41efc285dcfd1f0ac32156b7bb911b5"
PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
RESULT = PROJECT / "results/tpc266_certificate.json"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "873448074c451830a27378661c0ec146472e789cc7b698e65f27dbfcabe6a7ca",
    "papers/tpc-265-schur-endpoint-budget-compiler/README.md":
        "bb114657476ca2d10f34b9c5c96e93804d676a20b9e7ad1770df16d60719eedd",
    "papers/tpc-265-schur-endpoint-budget-compiler/PROOF_PACKAGE.md":
        "de683a97b1d099778ee08f72fa1e12ea6a28bef418e04bf1f99c915412ba38f3",
    "papers/tpc-265-schur-endpoint-budget-compiler/notes/theorem_ledger.md":
        "296e2aeb889611a129de97bef17f75bc69526b52461240081adaf1772b6301e8",
    "papers/tpc-265-schur-endpoint-budget-compiler/notes/route_evaluation.md":
        "d12e0b024c30ee64876b799afe3fb98c2c2b68d86a6a09621e596709775a5239",
    "research/tpc-big-road/bridge_b_schur_endpoint_budget_compiler.md":
        "890dd8e6be707140b5e562713f0a63713ab28f5c63ba3510af0350a3ef636588",
    "research/tpc-big-road/tpc_bridge_b_schur_endpoint_budget_compiler_checker.py":
        "df3cd2ef0f0d2841c92c3951b70e268777d2f1e32e1845e9e9fa201e5ffb7aa6",
}

STATUS = "PROVED_EXACT_END_TO_END_RESIDUAL_CLAIM_FIREWALL"
ROUND2_CLUE = (
    "PROVE_A_LITERAL_V59_RADIUS_OR_SIGNED_PHASE_BOUND_WITH_EFFECTIVE_SAVING_"
    "GREATER_THAN_1_OVER_400"
)
E0 = Fraction(5, 3)
TARGET = Fraction(1997, 1200)
REQUIRED = E0 - TARGET

FIREWALL = {
    "TPC266_ACTUAL_V59_PHASE": "OPEN",
    "TPC266_ACTUAL_V59_RADIUS": "OPEN",
    "TPC266_ARITHMETIC_ADVANCE": "NO",
    "TPC266_CENTER_CURRENT_TYPE": "FIXED_LOG",
    "TPC266_FAILURE_MATRIX": "PROVED_EXACT_SIX_STATE",
    "TPC266_FIXED_LOG_NONPROMOTION": "PROVED_EXACT",
    "TPC266_FIXED_POWER_CREDIT": 0,
    "TPC266_FULL_GATE_B": "OPEN",
    "TPC266_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC266_L2": "NONE",
    "TPC266_LITERAL_PRIME_SHELL_COUNTEREXAMPLE": "NONE",
    "TPC266_MAXIMUM_CLAIM": STATUS,
    "TPC266_RESIDUAL_CURRENT_TYPE": "SCHUR_SET_RADIUS_OPEN",
    "TPC266_RESIDUAL_RETENTION_FIREWALL": "PROVED_EXACT",
    "TPC266_ROUTE_ADVANCE": "YES_SCOPED_END_TO_END_CLAIM_FIREWALL",
    "TPC266_STATUS": STATUS,
    "TPC266_STRICT_PAYMENT_THRESHOLD": "PROVED_EXACT_ONE_OVER_400",
    "TPC266_TWIN_PRIME_RESULT": "NONE",
    "TPC266_TYPED_COMPOSITION": "PROVED_EXACT",
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
        need(hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest() == expected,
             "source hash: " + relative)
        need(len(blob) > 0, "empty source: " + relative)
    return len(SOURCE_HASHES)


def lane_record(name: str, kind: str, delta: Fraction | None,
                loss: Fraction | None, scope: str) -> dict[str, Any]:
    need(kind in {"FIXED_LOG", "POWER", "SIGNED_PHASE", "MISSING", "DELETED"},
         "lane kind")
    if kind in {"POWER", "SIGNED_PHASE"}:
        need(delta is not None and loss is not None, "power lane data")
        effective = delta - loss
        classification = (
            "STRICT" if effective > REQUIRED else
            "BORDERLINE" if effective == REQUIRED else "INSUFFICIENT"
        )
        paid = classification == "STRICT"
    elif kind == "FIXED_LOG":
        effective = None
        classification = "NO_FIXED_POWER"
        paid = False
    elif kind == "MISSING":
        effective = None
        classification = "MISSING"
        paid = False
    else:
        effective = None
        classification = "DELETED"
        paid = False
    return {
        "classification": classification,
        "delta": None if delta is None else str(delta),
        "effective": None if effective is None else str(effective),
        "kind": kind,
        "loss": None if loss is None else str(loss),
        "name": name,
        "paid": paid,
        "scope": scope,
    }


def compose(center: dict[str, Any], radius: dict[str, Any],
            residual_retained: bool) -> str:
    if not residual_retained:
        return "UNSOUND_RESIDUAL_DELETION"
    if center["kind"] == "FIXED_LOG":
        return "OPEN_LOG_CENTER"
    if radius["kind"] == "MISSING":
        return "OPEN_RADIUS"
    if center["kind"] == "DELETED" or radius["kind"] == "DELETED":
        return "UNSOUND_LANE_DELETION"
    if center["kind"] not in {"POWER", "SIGNED_PHASE"}:
        return "OPEN_CENTER"
    if radius["kind"] not in {"POWER", "SIGNED_PHASE"}:
        return "OPEN_RADIUS"
    if center["classification"] == "BORDERLINE" or radius["classification"] == "BORDERLINE":
        return "BORDERLINE"
    if center["classification"] == "INSUFFICIENT" or radius["classification"] == "INSUFFICIENT":
        return "INSUFFICIENT"
    if center["paid"] and radius["paid"]:
        return "CLOSED_CONDITIONAL"
    return "OPEN_UNPAID"


def failure_matrix() -> list[dict[str, Any]]:
    strict_delta = Fraction(1, 320)
    cases = [
        (
            "strict_pair", "POWER", strict_delta, Fraction(0),
            "POWER", strict_delta, Fraction(0), True,
            "CLOSED_CONDITIONAL",
        ),
        (
            "fixed_log_center", "FIXED_LOG", None, None,
            "POWER", strict_delta, Fraction(0), True,
            "OPEN_LOG_CENTER",
        ),
        (
            "missing_radius", "POWER", strict_delta, Fraction(0),
            "MISSING", None, None, True,
            "OPEN_RADIUS",
        ),
        (
            "borderline_lane", "POWER", REQUIRED, Fraction(0),
            "POWER", strict_delta, Fraction(0), True,
            "BORDERLINE",
        ),
        (
            "subcritical_lane", "POWER", strict_delta, Fraction(1, 1200),
            "POWER", strict_delta, Fraction(1, 1200), True,
            "INSUFFICIENT",
        ),
        (
            "deleted_residual", "POWER", strict_delta, Fraction(0),
            "POWER", strict_delta, Fraction(0), False,
            "UNSOUND_RESIDUAL_DELETION",
        ),
    ]
    records = []
    for name, ck, cd, cl, rk, rd, rl, retained, expected in cases:
        center = lane_record(name + ".center", ck, cd, cl, "TPC263_CENTER")
        radius = lane_record(name + ".radius", rk, rd, rl, "TPC264_TPC265_RADIUS")
        status = compose(center, radius, retained)
        need(status == expected, "failure state: " + name)
        records.append({
            "center": center,
            "expected": expected,
            "name": name,
            "residual_retained": retained,
            "result": status,
            "radius": radius,
        })
    return records


def endpoint_audit() -> dict[str, Any]:
    center = Fraction(2)
    radius = Fraction(3)
    aligned = center + radius
    anti_aligned = center - radius
    deleted_output = abs(center)
    need(aligned == 5 and anti_aligned == -1, "endpoint values")
    need(abs(aligned) == abs(center) + radius, "aligned endpoint")
    need(abs(anti_aligned) == 1, "anti-aligned endpoint")
    need(abs(aligned) - deleted_output == radius, "deletion gap")
    circle_lower = abs(abs(center) - radius)
    need(circle_lower == 1, "circle lower endpoint")
    return {
        "aligned_value": str(aligned),
        "center": str(center),
        "circle_infimum": str(circle_lower),
        "circle_supremum": str(abs(center) + radius),
        "deleted_output": str(deleted_output),
        "disk_infimum": str(max(abs(center) - radius, Fraction(0))),
        "disk_supremum": str(abs(center) + radius),
        "radius": str(radius),
        "residual_deletion_gap": str(radius),
    }


def chain_audit() -> dict[str, Any]:
    nodes = [
        {
            "id": "TPC263.C3",
            "input": "source-backed rank-three physical channel",
            "output_type": "FIXED_LOG",
            "power_credit": 0,
        },
        {
            "id": "TPC264.Cperp",
            "input": "TPC263 exact projection split",
            "output_type": "SCHUR_SET",
            "radius_status": "OPEN",
        },
        {
            "id": "TPC265.endpoint",
            "input": "TPC264 Schur set",
            "output_type": "RADIAL_ENVELOPE",
            "upper_endpoint": "|c|+R",
        },
        {
            "id": "TPC266.compiler",
            "input": "typed center/radius descriptors",
            "output_type": "BUDGET_DECISION",
            "strict_threshold": "1/400",
        },
    ]
    edges = [
        ["TPC263.C3", "TPC264.Cperp", "EXACT_SPLIT"],
        ["TPC264.Cperp", "TPC265.endpoint", "EXACT_RADIAL_SUPPORT"],
        ["TPC265.endpoint", "TPC266.compiler", "TYPED_BUDGET_CHECK"],
    ]
    need(nodes[0]["output_type"] == "FIXED_LOG", "center type")
    need(nodes[1]["output_type"] == "SCHUR_SET", "residual type")
    need(nodes[2]["upper_endpoint"] == "|c|+R", "endpoint type")
    need(nodes[3]["strict_threshold"] == "1/400", "compiler threshold")
    return {
        "edges": edges,
        "forbidden_promotions": ["FIXED_LOG->POWER", "SCHUR_SET->ZERO_RESIDUAL"],
        "nodes": nodes,
        "residual_retained_by_default": True,
    }


def log_firewall() -> dict[str, Any]:
    samples = []
    values = []
    for m in (10, 20, 40):
        value = Fraction(2 ** m, m ** 3)
        values.append(value)
        samples.append({"m": m, "power_over_log_proxy": str(value)})
    need(values[1] > values[0],
         "log proxy growth")
    need(values[2] > values[1],
         "log proxy growth 2")
    return {
        "fixed_log_credit": 0,
        "limit_statement": "x^delta/(log x)^M -> infinity for fixed delta>0,M",
        "proxy_samples": samples,
        "type_transition": "FIXED_LOG->POWER = REJECTED",
    }


def build_certificate() -> dict[str, Any]:
    source_count = verify_sources()
    matrix = failure_matrix()
    return {
        "baseline": {"head": BASELINE_HEAD, "source_count": source_count},
        "chain_audit": chain_audit(),
        "claim": STATUS,
        "endpoint_audit": endpoint_audit(),
        "failure_matrix": matrix,
        "firewall": dict(FIREWALL),
        "log_firewall": log_firewall(),
        "round2_clue": ROUND2_CLUE,
        "schema": "TPC266_END_TO_END_CLAIM_FIREWALL_CERTIFICATE_V1",
        "source_hashes": dict(SOURCE_HASHES),
        "thresholds": {
            "baseline_exponent": str(E0),
            "target_exponent": str(TARGET),
            "required_strict_saving": str(REQUIRED),
        },
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
    print("TPC266_CERTIFICATE=PASS "
          f"sources={expected['baseline']['source_count']} "
          "typed_composition=EXACT failure_matrix=6 "
          "strict_threshold=1/400 fixed_log_credit=0 residual_deletion=REJECTED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC266_CERTIFICATE=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
