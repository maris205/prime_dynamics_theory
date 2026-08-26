#!/usr/bin/env python3
"""Independent exact checker for the TPC-265 radial budget compiler."""

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


BASELINE_HEAD = "c58404738b9943293d610f2cf87ef6fb5c01ed4e"
ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc265_certificate.json"
CLAIM = "PROVED_EXACT_SCHUR_TO_ENDPOINT_BUDGET_COMPILER"

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
        need(hashlib.sha256(frozen(path)).hexdigest() == expected,
             "source hash: " + path)


def radial_records(center: Fraction, radius: Fraction) -> dict[str, str]:
    upper = abs(center) + radius
    lower = max(abs(center) - radius, Fraction(0))
    need(upper == 5 and lower == 0, "disk radial values")
    circle_lower = abs(abs(center) - radius)
    need(circle_lower == 1, "circle radial value")
    return {"disk_supremum": str(upper), "disk_infimum": str(lower),
            "circle_supremum": str(upper), "circle_infimum": str(circle_lower)}


def budget_records() -> list[dict[str, str]]:
    required = Fraction(1, 400)
    tests = (
        ("strict_radius", Fraction(1, 320), Fraction(0), "STRICT"),
        ("borderline", Fraction(1, 400), Fraction(0), "BORDERLINE"),
        ("loss_dominated", Fraction(1, 320), Fraction(1, 1200),
         "INSUFFICIENT"),
    )
    output = []
    for name, delta, loss, expected in tests:
        effective = delta - loss
        classification = ("STRICT" if effective > required else
                          "BORDERLINE" if effective == required else
                          "INSUFFICIENT")
        need(classification == expected, "budget classification: " + name)
        output.append({"name": name, "effective": str(effective),
                       "classification": classification})
    return output


def semantic(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        firewall = data["firewall"]
        radial = data["radial_audit"]
        budget = data["budget_audit"]
        return (
            data["schema"] == "TPC265_SCHUR_ENDPOINT_BUDGET_CERTIFICATE_V1"
            and data["claim"] == CLAIM
            and data["baseline"]["head"] == BASELINE_HEAD
            and data["source_hashes"] == SOURCE_HASHES
            and radial["disk_supremum"] == "5"
            and radial["disk_infimum"] == "0"
            and radial["circle_supremum"] == "5"
            and radial["circle_infimum"] == "1"
            and radial["minkowski_radius"] == "6"
            and radial["minkowski_supremum"] == "8"
            and budget["baseline_exponent"] == "5/3"
            and budget["target_exponent"] == "1997/1200"
            and budget["required_strict_saving"] == "1/400"
            and firewall["TPC265_DISK_WORST_CASE"] == "PROVED_EXACT"
            and firewall["TPC265_CIRCLE_WORST_CASE"] == "PROVED_EXACT"
            and firewall["TPC265_STRICT_PAYMENT_THRESHOLD"] ==
                "PROVED_EXACT_ONE_OVER_400"
            and firewall["TPC265_LOG_CENTER_CREDIT"] == 0
            and firewall["TPC265_LOG_RADIUS_CREDIT"] == 0
            and firewall["TPC265_ACTUAL_V59_RADIUS"] == "OPEN"
            and firewall["TPC265_ACTUAL_V59_PHASE"] == "OPEN"
            and firewall["TPC265_ARITHMETIC_ADVANCE"] == "NO"
            and firewall["TPC265_FULL_GATE_B"] == "OPEN"
            and firewall["TPC265_L2"] == "NONE"
            and firewall["TPC265_TWIN_PRIME_RESULT"] == "NONE"
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

    mutate(("schema",), "TPC265_V0")
    mutate(("claim",), "PROVED")
    mutate(("baseline", "head"), "0" * 40)
    mutate(("source_hashes",), {})
    mutate(("radial_audit", "disk_supremum"), "0")
    mutate(("radial_audit", "minkowski_radius"), "0")
    mutate(("budget_audit", "required_strict_saving"), "0")
    mutate(("firewall", "TPC265_DISK_WORST_CASE"), "HEURISTIC")
    mutate(("firewall", "TPC265_STRICT_PAYMENT_THRESHOLD"), "PAID")
    mutate(("firewall", "TPC265_LOG_CENTER_CREDIT"), 1)
    mutate(("firewall", "TPC265_ACTUAL_V59_RADIUS"), "PROVED")
    mutate(("firewall", "TPC265_ARITHMETIC_ADVANCE"), "YES")
    mutate(("firewall", "TPC265_FULL_GATE_B"), "PAID")
    mutate(("firewall", "TPC265_TWIN_PRIME_RESULT"), "PROVED")
    need(all(not semantic(item) for item in mutations), "mutation accepted")
    return len(mutations)


def run() -> None:
    source_audit()
    need(RESULT.is_file(), "certificate missing")
    raw = RESULT.read_text(encoding="utf-8")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonical")
    need(semantic(data), "certificate semantics")
    need(data["radial_audit"]["disk_supremum"] ==
         radial_records(Fraction(2), Fraction(3))["disk_supremum"],
         "radial certificate")
    need(len(data["budget_audit"]["lanes"]) == 4, "lane count")
    need(budget_records()[0]["classification"] == "STRICT",
         "strict certificate")
    rejected = mutation_audit(data)
    print("TPC265_INDEPENDENT_CHECK=PASS "
          f"radial_cases=4 lanes=4 mutations_rejected={rejected} "
          "producer_imported=NO")


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
        print("TPC265_INDEPENDENT_CHECK=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
