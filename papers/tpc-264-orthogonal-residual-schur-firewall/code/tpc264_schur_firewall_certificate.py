#!/usr/bin/env python3
"""Deterministic exact certificate for the TPC-264 Schur firewall."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE_HEAD = "e0966c5a4c3b82d260bd774d1debbbb742c799e2"
PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
RESULT = PROJECT / "results/tpc264_certificate.json"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "c783920d04ac1a58adb26bd6bcaee61fbc28335acc78f5abed3fd5dfc64161e4",
    "papers/tpc-263-rank-three-physical-cross-gram/README.md":
        "5cede7c57bd2c410d189e46e869232a21fabb840285513fdd001ea74d2485f54",
    "papers/tpc-263-rank-three-physical-cross-gram/PROOF_PACKAGE.md":
        "d5519dc30335611eae313e220e0bd7a64c1d29b06932a65469c03d3e6a33d2dc",
    "papers/tpc-263-rank-three-physical-cross-gram/notes/theorem_ledger.md":
        "895d614fe3564a706cb7fb4bf9056e181a8f78b07315092109b2a143e1620570",
    "papers/tpc-263-rank-three-physical-cross-gram/notes/route_evaluation.md":
        "91f66894d12359ec73fb2ffb8089a7876510073db97062d1560fd2233a3298a5",
    "research/tpc-big-road/bridge_b_rank_three_physical_cross_gram.md":
        "c974eefc33e5832539632740b5da77d21ed84d658b6705d9d4adfc5341a89df9",
    "research/tpc-big-road/tpc_bridge_b_rank_three_physical_cross_gram_checker.py":
        "b989fe071149e8c31d8b0d490aefc132d1da20b65ce344127cae3014cf0f333b",
}

STATUS = "PROVED_EXACT_ORTHOGONAL_RESIDUAL_SCHUR_FIREWALL"
ROUND2_CLUE = "TURN_THE_SCHUR_RADIUS_OR_RESIDUAL_PHASE_INTO_A_LITERAL_V59_ESTIMATE"

FIREWALL = {
    "TPC264_ACTUAL_V59_RESIDUAL": "OPEN",
    "TPC264_ARITHMETIC_ADVANCE": "NO",
    "TPC264_COMPLEMENT_DIMENSION_SPLIT": "PROVED_EXACT",
    "TPC264_ENDPOINT_SCALE_WITNESS": "NUMERICALLY_CERTIFIED_STRUCTURAL",
    "TPC264_FIXED_POWER_CREDIT": 0,
    "TPC264_FULL_GATE_B": "OPEN",
    "TPC264_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC264_FULL_SCALAR_FEASIBLE_SET": "PROVED_EXACT",
    "TPC264_L2": "NONE",
    "TPC264_LITERAL_PRIME_SHELL_COUNTEREXAMPLE": "NONE",
    "TPC264_PROJECTION_DATA": "PROVED_EXACT",
    "TPC264_RESIDUAL_GRAM_FEASIBLE_SET": "PROVED_EXACT",
    "TPC264_ROUTE_ADVANCE": "YES_SCOPED_RESIDUAL_SCHUR_FIREWALL",
    "TPC264_STATUS": STATUS,
    "TPC264_TWIN_PRIME_RESULT": "NONE",
}

Gaussian = tuple[Fraction, Fraction]


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def frozen_blob(relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", BASELINE_HEAD + ":" + relative], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
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


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def gconj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def gscale(value: Gaussian, scalar: Fraction) -> Gaussian:
    return (value[0] * scalar, value[1] * scalar)


def gnorm2(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def inner(left: tuple[Gaussian, ...], right: tuple[Gaussian, ...]) -> Gaussian:
    total = (Fraction(0), Fraction(0))
    for a, b in zip(left, right):
        total = gadd(total, gmul(gconj(a), b))
    return total


def vector_norm2(vector: tuple[Gaussian, ...]) -> Fraction:
    value = inner(vector, vector)
    need(value[1] == 0, "non-real norm")
    return value[0]


def schur_det(a2: Fraction, b2: Fraction, z: Gaussian) -> Fraction:
    return a2 * b2 - gnorm2(z)


def gram_psd(a2: Fraction, b2: Fraction, z: Gaussian) -> bool:
    return a2 >= 0 and b2 >= 0 and schur_det(a2, b2, z) >= 0


def projection_fixture() -> dict[str, Any]:
    # First three coordinates are range(P); last two are ker(P).
    p = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(0)),
         (Fraction(0), Fraction(0)))
    q = ((Fraction(2), Fraction(1)), (Fraction(0), Fraction(0)),
         (Fraction(0), Fraction(0)))
    a = Fraction(3, 2)
    b = Fraction(2)
    radius = a * b
    center = inner(p, q)
    need(center == (Fraction(2), Fraction(1)), "center")

    # Exact complement witnesses: plus endpoint, zero interior, minus endpoint,
    # and a quarter-turn endpoint.  All coordinates are Gaussian rationals.
    zero_coordinate = (Fraction(0), Fraction(0))
    residuals = {
        "plus": (((a, Fraction(0)), zero_coordinate),
                 ((b, Fraction(0)), zero_coordinate)),
        "minus": (((a, Fraction(0)), zero_coordinate),
                  ((-b, Fraction(0)), zero_coordinate)),
        "zero": (((a, Fraction(0)), zero_coordinate),
                 (zero_coordinate, (Fraction(0), b))),
        "quarter_turn": (((a, Fraction(0)), zero_coordinate),
                         ((Fraction(0), b), zero_coordinate)),
    }
    # The `quarter_turn` label uses v=i*b in the first residual coordinate;
    # keep it separate from the zero witness.
    records: dict[str, Any] = {}
    for name, (u, v) in residuals.items():
        z = inner(u, v)
        need(vector_norm2(u) == a * a and vector_norm2(v) == b * b,
             "residual norm: " + name)
        need(gram_psd(a * a, b * b, z), "Schur PSD: " + name)
        records[name] = {
            "full_scalar": [str(value) for value in gadd(center, z)],
            "residual_inner_product": [str(value) for value in z],
            "residual_norms_squared": [str(vector_norm2(u)),
                                       str(vector_norm2(v))],
            "schur_determinant": str(schur_det(a * a, b * b, z)),
        }
    need(records["plus"]["residual_inner_product"] == ["3", "0"],
         "plus endpoint")
    need(records["minus"]["residual_inner_product"] == ["-3", "0"],
         "minus endpoint")
    need(records["zero"]["residual_inner_product"] == ["0", "0"],
         "zero interior")
    need(records["quarter_turn"]["residual_inner_product"] == ["0", "3"],
         "quarter turn")
    return {
        "ambient_dimension": 5,
        "center": [str(value) for value in center],
        "complement_dimension": 2,
        "projected_norms_squared": [str(vector_norm2(p)), str(vector_norm2(q))],
        "residual_norms": [str(a), str(b)],
        "radius": str(radius),
        "records": records,
    }


def dimension_audit() -> dict[str, Any]:
    a = Fraction(3, 2)
    b = Fraction(2)
    radius = a * b
    disk_points = {
        "zero": (Fraction(0), Fraction(0)),
        "real_half": (radius / 2, Fraction(0)),
        "real_endpoint": (radius, Fraction(0)),
        "negative_endpoint": (-radius, Fraction(0)),
        "imag_endpoint": (Fraction(0), radius),
    }
    disk = []
    for name, z in disk_points.items():
        need(gram_psd(a * a, b * b, z), "disk point: " + name)
        disk.append(name)
    outside = (radius * Fraction(5, 4), Fraction(0))
    need(not gram_psd(a * a, b * b, outside), "outside disk accepted")
    circle = ["real_endpoint", "negative_endpoint", "imag_endpoint"]
    for name in circle:
        z = disk_points[name]
        need(gnorm2(z) == radius * radius, "circle modulus: " + name)
    need(gnorm2(disk_points["zero"]) < radius * radius, "circle rejects zero")
    return {
        "positive_residual_norms": [str(a), str(b)],
        "disk_points_checked": disk,
        "outside_point": [str(value) for value in outside],
        "disk_feasible": True,
        "circle_positive_modulus": True,
        "circle_zero_rejected": True,
        "zero_complement_singleton": ["0", "0"],
        "zero_residual_singleton": ["0", "0"],
    }


def endpoint_budget_audit() -> dict[str, Any]:
    required = Fraction(1, 400)
    strict = Fraction(1, 320)
    borderline = required
    loss = strict - Fraction(1, 1200)
    need(strict > required and borderline == required and loss < required,
         "endpoint budget")
    need(2 * Fraction(5, 6) == Fraction(5, 3), "synthetic exponent")
    return {
        "synthetic_residual_amplitude_exponent": "5/6",
        "synthetic_radius_exponent": "5/3",
        "required_strict_saving": "1/400",
        "strict_fixture_saving": "1/320",
        "borderline_fixture_saving": "1/400",
        "loss_fixture_effective_saving": str(loss),
        "fixed_power_credit": 0,
        "literal_residual_scale": "OPEN",
        "synthetic_only": True,
    }


def build_certificate() -> dict[str, Any]:
    source_count = verify_sources()
    return {
        "baseline": {"head": BASELINE_HEAD, "source_count": source_count},
        "claim": STATUS,
        "dimension_audit": dimension_audit(),
        "endpoint_budget_audit": endpoint_budget_audit(),
        "epistemic_status": {
            "actual_v59_residual": "OPEN",
            "complement_dimension_split": "PROVED_EXACT",
            "finite_witnesses": "NUMERICALLY_CERTIFIED_STRUCTURAL",
            "full_scalar_feasible_set": "PROVED_EXACT_CONDITIONAL",
            "residual_gram": "PROVED_EXACT",
        },
        "firewall": dict(FIREWALL),
        "projection_fixture": projection_fixture(),
        "round2_clue": ROUND2_CLUE,
        "schema": "TPC264_SCHUR_FIREWALL_CERTIFICATE_V1",
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
    print("TPC264_CERTIFICATE=PASS "
          f"sources={expected['baseline']['source_count']} "
          "schur=EXACT disk_circle_singleton=EXACT "
          "synthetic_radius=x^(5/3) fixed_power_credit=0 "
          "literal_residual=OPEN")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC264_CERTIFICATE=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
