#!/usr/bin/env python3
"""Independent exact checker for the TPC-264 Schur firewall."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE_HEAD = "e0966c5a4c3b82d260bd774d1debbbb742c799e2"
ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc264_certificate.json"
CLAIM = "PROVED_EXACT_ORTHOGONAL_RESIDUAL_SCHUR_FIREWALL"

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

Gaussian = tuple[Fraction, Fraction]


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def frozen(path: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + path],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"",
         "frozen source: " + path)
    return result.stdout


def source_audit() -> None:
    for path, expected in SOURCE_HASHES.items():
        blob = frozen(path)
        need(hashlib.sha256(blob).hexdigest() == expected,
             "source hash: " + path)


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def conjugate(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def modulus_squared(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def ip(left: tuple[Gaussian, ...], right: tuple[Gaussian, ...]) -> Gaussian:
    total = (Fraction(0), Fraction(0))
    for a, b in zip(left, right):
        total = gadd(total, gmul(conjugate(a), b))
    return total


def norm_squared(value: tuple[Gaussian, ...]) -> Fraction:
    result = ip(value, value)
    need(result[1] == 0, "complex norm")
    return result[0]


def feasible(a2: Fraction, b2: Fraction, z: Gaussian) -> bool:
    return a2 >= 0 and b2 >= 0 and a2 * b2 >= modulus_squared(z)


def fixture_audit() -> dict[str, Any]:
    one = (Fraction(1), Fraction(0))
    zero = (Fraction(0), Fraction(0))
    p = (one, zero, zero)
    q = ((Fraction(2), Fraction(1)), zero, zero)
    u_plus = ((Fraction(3, 2), Fraction(0)), zero)
    u_minus = ((Fraction(3, 2), Fraction(0)), zero)
    u_zero = ((Fraction(3, 2), Fraction(0)), zero)
    u_turn = ((Fraction(3, 2), Fraction(0)), zero)
    v_plus = ((Fraction(2), Fraction(0)), zero)
    v_minus = ((Fraction(-2), Fraction(0)), zero)
    v_zero = (zero, (Fraction(0), Fraction(2)))
    v_turn = ((Fraction(0), Fraction(2)), zero)
    pairs = {
        "plus": (u_plus, v_plus), "minus": (u_minus, v_minus),
        "zero": (u_zero, v_zero), "quarter_turn": (u_turn, v_turn),
    }
    center = ip(p, q)
    need(center == (Fraction(2), Fraction(1)), "center mismatch")
    result: dict[str, Any] = {}
    for name, (u, v) in pairs.items():
        need(norm_squared(u) == Fraction(9, 4), "u norm: " + name)
        need(norm_squared(v) == Fraction(4), "v norm: " + name)
        z = ip(u, v)
        need(feasible(Fraction(9, 4), Fraction(4), z),
             "Schur feasibility: " + name)
        full = gadd(center, z)
        result[name] = {
            "z": [str(z[0]), str(z[1])],
            "full": [str(full[0]), str(full[1])],
            "det": str(Fraction(9, 4) * 4 - modulus_squared(z)),
        }
    need(result["plus"]["z"] == ["3", "0"], "plus value")
    need(result["minus"]["z"] == ["-3", "0"], "minus value")
    need(result["zero"]["z"] == ["0", "0"], "zero value")
    need(result["quarter_turn"]["z"] == ["0", "3"], "turn value")
    return {"center": ["2", "1"], "radius": "3", "records": result}


def dimension_audit() -> dict[str, Any]:
    a2 = Fraction(9, 4)
    b2 = Fraction(4)
    radius2 = a2 * b2
    points = (
        (Fraction(0), Fraction(0)),
        (Fraction(3, 2), Fraction(0)),
        (Fraction(-3), Fraction(0)),
        (Fraction(0), Fraction(3)),
    )
    for point in points:
        need(feasible(a2, b2, point), "disk point rejected")
    outside = (Fraction(15, 4), Fraction(0))
    need(not feasible(a2, b2, outside), "outside accepted")
    need(modulus_squared(points[2]) == radius2 and
         modulus_squared(points[3]) == radius2, "circle endpoints")
    need(modulus_squared(points[0]) < radius2, "zero in circle")
    return {
        "disk_points": len(points), "outside_rejected": True,
        "circle_endpoint_modulus_squared": str(radius2),
        "zero_complement_value": ["0", "0"],
        "zero_residual_value": ["0", "0"],
    }


def semantic(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        firewall = data["firewall"]
        budget = data["endpoint_budget_audit"]
        return (
            data["schema"] == "TPC264_SCHUR_FIREWALL_CERTIFICATE_V1"
            and data["claim"] == CLAIM
            and data["baseline"]["head"] == BASELINE_HEAD
            and data["source_hashes"] == SOURCE_HASHES
            and data["projection_fixture"]["radius"] == "3"
            and data["projection_fixture"]["records"]["plus"]
                ["residual_inner_product"] == ["3", "0"]
            and data["projection_fixture"]["records"]["zero"]
                ["residual_inner_product"] == ["0", "0"]
            and data["dimension_audit"]["disk_feasible"] is True
            and data["dimension_audit"]["circle_positive_modulus"] is True
            and data["dimension_audit"]["circle_zero_rejected"] is True
            and budget["synthetic_radius_exponent"] == "5/3"
            and budget["fixed_power_credit"] == 0
            and firewall["TPC264_RESIDUAL_GRAM_FEASIBLE_SET"] == "PROVED_EXACT"
            and firewall["TPC264_FULL_SCALAR_FEASIBLE_SET"] == "PROVED_EXACT"
            and firewall["TPC264_ACTUAL_V59_RESIDUAL"] == "OPEN"
            and firewall["TPC264_ARITHMETIC_ADVANCE"] == "NO"
            and firewall["TPC264_FULL_GATE_B"] == "OPEN"
            and firewall["TPC264_L2"] == "NONE"
            and firewall["TPC264_TWIN_PRIME_RESULT"] == "NONE"
            and firewall["TPC264_LITERAL_PRIME_SHELL_COUNTEREXAMPLE"] == "NONE"
        )
    except (KeyError, TypeError):
        return False


def mutation_audit(data: dict[str, Any]) -> int:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[str, ...], value: Any) -> None:
        candidate = deepcopy(data)
        cursor: Any = candidate
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        mutations.append(candidate)

    mutate(("schema",), "TPC264_V0")
    mutate(("claim",), "PROVED")
    mutate(("baseline", "head"), "0" * 40)
    mutate(("source_hashes",), {})
    mutate(("projection_fixture", "radius"), "0")
    mutate(("projection_fixture", "records", "plus",
            "residual_inner_product"), ["0", "0"])
    mutate(("dimension_audit", "disk_feasible"), False)
    mutate(("endpoint_budget_audit", "fixed_power_credit"), 1)
    mutate(("firewall", "TPC264_ACTUAL_V59_RESIDUAL"), "PROVED")
    mutate(("firewall", "TPC264_ARITHMETIC_ADVANCE"), "YES")
    mutate(("firewall", "TPC264_FULL_GATE_B"), "PAID")
    mutate(("firewall", "TPC264_L2"), "PAID")
    mutate(("firewall", "TPC264_TWIN_PRIME_RESULT"), "PROVED")
    need(all(not semantic(candidate) for candidate in mutations),
         "mutation accepted")
    return len(mutations)


def run() -> None:
    source_audit()
    need(RESULT.is_file(), "certificate missing")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    need(RESULT.read_text(encoding="utf-8") == canonical(data),
         "certificate is not canonical")
    need(semantic(data), "certificate semantics")
    fixture = fixture_audit()
    need(data["projection_fixture"]["center"] == fixture["center"],
         "center certificate")
    need(data["projection_fixture"]["records"]["plus"]
         ["residual_inner_product"] == fixture["records"]["plus"]["z"],
         "plus certificate")
    rejected = mutation_audit(data)
    print("TPC264_INDEPENDENT_CHECK=PASS "
          f"fixture_records={len(fixture['records'])} "
          f"disk_points={len(data['dimension_audit']['disk_points_checked'])} "
          f"mutations_rejected={rejected} producer_imported=NO")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    run()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC264_INDEPENDENT_CHECK=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
