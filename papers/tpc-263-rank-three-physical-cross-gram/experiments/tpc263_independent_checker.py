#!/usr/bin/env python3
"""Independent replay and mutation audit for TPC-263."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc263_certificate.json"
BASELINE = "6c32d179c7225add34dfcc3a4d43a0c59da14424"
CLAIM = "PROVED_SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL"
ROUND2 = "ATTACK_THE_ORTHOGONAL_COMPLEMENT_AFTER_PAYING_THE_RANK_THREE_LOG_CHANNEL"
SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "344c75a6c41730703b04d5474e385986f8c66dcf5639531848da99c3bec574f4",
    "papers/tpc-262-literal-mode-zero-cross-gram/README.md":
        "d93b364a110103a81cdf3e766586da0f43af1f2b090aecb7514e875d4f8365d6",
    "papers/tpc-262-literal-mode-zero-cross-gram/PROOF_PACKAGE.md":
        "520f74acd0fc39f50c53d1cef31e2a9a599630384b4f888b190a8a64842364b1",
    "papers/tpc-262-literal-mode-zero-cross-gram/notes/theorem_ledger.md":
        "ef8c6d834dfda217a412c99d9f70a93961ac7e501fa7a86c8b9286d92dcb8556",
    "papers/tpc-262-literal-mode-zero-cross-gram/notes/route_evaluation.md":
        "4951487298f1cb5ec0062d75512d4d05b7de3893b26b98a148b70d2a311147cc",
    "research/tpc-big-road/bridge_b_four_block_haar_transverse_norm_floor.md":
        "faaede82e2ebf84a994e3e9c945e42c321a8c81d0c0db9e0f8e2f9a88329e609",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/PROOF_PACKAGE.md":
        "06b6f2e9842f68fc6f3d882f95d3b9c161980ceb429dd24b52bd98322e6f397f",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/notes/theorem_ledger.md":
        "127bf4a07defd26a87f74e989a426500a3b50a18df03875805b9afeb71a5a3a6",
    "research/tpc-big-road/bridge_b_source_backed_rank_midpoint_hybrid_mean_closure.md":
        "6e5cb92642bf8fc8f0a3a56a29c4c061359f3794e24345d76a62d2fccf5a21ee",
    "papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/notes/theorem_ledger.md":
        "ea138a0cd5839bdb62633a38389f82a4e6f4346641757b05729722daec89aa2b",
}


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def frozen(path: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE + ":" + path],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", "frozen: " + path)
    return result.stdout


def source_replay() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(hashlib.sha256(frozen(path)).hexdigest() == expected,
             "source hash: " + path)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def frame_data(clock: Fraction) -> tuple[list[int], list[dict[str, Any]]]:
    a = floor_fraction(clock / 2)
    b = floor_fraction(clock)
    n = b - a
    ell = n // 2
    right = n - ell
    sizes = [ell // 2, ell - ell // 2, right // 2, right - right // 2]
    need(min(sizes) > 0, "empty block")
    specs = [
        {"rho2": Fraction(ell * right, n),
         "coeff": [Fraction(1, ell), Fraction(1, ell),
                   Fraction(-1, right), Fraction(-1, right)]},
        {"rho2": Fraction(sizes[0] * sizes[1], sizes[0] + sizes[1]),
         "coeff": [Fraction(1, sizes[0]), Fraction(-1, sizes[1]),
                   Fraction(0), Fraction(0)]},
        {"rho2": Fraction(sizes[2] * sizes[3], sizes[2] + sizes[3]),
         "coeff": [Fraction(0), Fraction(0), Fraction(1, sizes[2]),
                   Fraction(-1, sizes[3])]},
    ]
    return sizes, specs


def geometry_replay() -> int:
    clocks = [Fraction(80 + 5 * i, 1) for i in range(20)]
    clocks += [Fraction(641 + 9 * i, 2) for i in range(20)]
    checks = 0
    for clock in clocks:
        sizes, specs = frame_data(clock)
        for spec in specs:
            norm = spec["rho2"] * sum((s * c * c for s, c in
                                        zip(sizes, spec["coeff"])), Fraction(0))
            need(norm == 1, "norm")
            jumps = [Fraction(0)] + spec["coeff"] + [Fraction(0)]
            variation = sum((abs(jumps[i + 1] - jumps[i])
                             for i in range(len(jumps) - 1)), Fraction(0))
            need(spec["rho2"] * variation * variation ==
                 Fraction(4, 1) / spec["rho2"], "variation")
            checks += 2
        for i in range(3):
            for j in range(i + 1, 3):
                dot = sum((s * a * b for s, a, b in zip(
                    sizes, specs[i]["coeff"], specs[j]["coeff"])), Fraction(0))
                need(dot == 0, "orthogonality")
                checks += 1
    return checks


Gaussian = tuple[Fraction, Fraction]


def add(a: Gaussian, b: Gaussian) -> Gaussian:
    return (a[0] + b[0], a[1] + b[1])


def mul(a: Gaussian, b: Gaussian) -> Gaussian:
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def conj(a: Gaussian) -> Gaussian:
    return (a[0], -a[1])


def dot(left: list[Gaussian], right: list[Gaussian]) -> Gaussian:
    total = (Fraction(0), Fraction(0))
    for a, b in zip(left, right):
        total = add(total, mul(conj(a), b))
    return total


def projection_replay() -> dict[str, list[str]]:
    w = [(Fraction(3), Fraction(1)), (Fraction(-2), Fraction(3)),
         (Fraction(5), Fraction(-1)), (Fraction(7), Fraction(2)),
         (Fraction(-4), Fraction(1)), (Fraction(1), Fraction(-3))]
    h = [(Fraction(-1), Fraction(2)), (Fraction(4), Fraction(-1)),
         (Fraction(2), Fraction(3)), (Fraction(-3), Fraction(1)),
         (Fraction(5), Fraction(0)), (Fraction(-2), Fraction(-4))]
    pw = w[:3] + [(Fraction(0), Fraction(0))] * 3
    ph = h[:3] + [(Fraction(0), Fraction(0))] * 3
    rw = [(Fraction(0), Fraction(0))] * 3 + w[3:]
    rh = [(Fraction(0), Fraction(0))] * 3 + h[3:]
    projected = dot(pw, ph)
    residual = dot(rw, rh)
    total = dot(w, h)
    need(total == add(projected, residual), "split")
    need(residual != (Fraction(0), Fraction(0)), "zero residual")
    return {"projected": [str(projected[0]), str(projected[1])],
            "residual": [str(residual[0]), str(residual[1])],
            "total": [str(total[0]), str(total[1])]}


def semantic(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        constants = data["constants_and_exponents"]
        firewall = data["firewall"]
        projection = data["projection_audit"]
        return (
            data["schema"] == "TPC263_RANK_THREE_PHYSICAL_CROSS_GRAM_CERTIFICATE_V1"
            and data["claim"] == CLAIM
            and data["baseline"] == {"head": BASELINE, "source_count": 11}
            and data["source_hashes"] == SOURCE_HASHES
            and constants["channel_exponent"] == "5/3"
            and constants["channel_log_power"] == "M+3"
            and constants["endpoint_gap"] == "1/400"
            and constants["fixed_power_credit"] == 0
            and projection["projection_rank"] == 3
            and projection["residual_nonzero"] is True
            and firewall["TPC263_ROUTE_ADVANCE"] ==
                "YES_SCOPED_RANK_THREE_LOG_CHANNEL"
            and firewall["TPC263_RANK_THREE_CHANNEL"] ==
                "PROVED_SOURCE_BACKED_X_5_OVER_3_LOG_M_PLUS_3"
            and firewall["TPC263_ORTHOGONAL_RESIDUAL"] == "OPEN"
            and firewall["TPC263_FIXED_POWER_CREDIT"] == 0
            and firewall["TPC263_L2"] == "NONE"
            and firewall["TPC263_FULL_GATE_B"] == "OPEN"
            and firewall["TPC263_TWIN_PRIME_RESULT"] == "NONE"
            and data["round2_clue"] == ROUND2
        )
    except (KeyError, TypeError, IndexError):
        return False


def mutation_replay(data: dict[str, Any]) -> int:
    mutations: list[tuple[tuple[str, ...], Any]] = [
        (("schema",), "TPC263_V0"),
        (("claim",), "PROVED"),
        (("baseline", "head"), "0" * 40),
        (("constants_and_exponents", "channel_exponent"), "1/2"),
        (("constants_and_exponents", "fixed_power_credit"), 1),
        (("projection_audit", "projection_rank"), 2),
        (("projection_audit", "residual_nonzero"), False),
        (("firewall", "TPC263_ORTHOGONAL_RESIDUAL"), "PAID"),
        (("firewall", "TPC263_FULL_GATE_B"), "PAID"),
        (("round2_clue",), "SHORTCUT"),
    ]
    rejected = 0
    for path, value in mutations:
        item = json.loads(json.dumps(data))
        cursor: Any = item
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        need(not semantic(item), "mutation accepted")
        rejected += 1
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    source_replay()
    geometry_checks = geometry_replay()
    projection = projection_replay()
    raw = CERTIFICATE.read_text(encoding="utf-8")
    data = json.loads(raw)
    need(raw == canonical(data), "noncanonical certificate")
    need(semantic(data), "certificate semantics")
    need(data["projection_audit"]["projected_cross_gram"] ==
         projection["projected"], "projection mismatch")
    need(data["projection_audit"]["orthogonal_residual"] ==
         projection["residual"], "residual mismatch")
    mutations = mutation_replay(data)
    print("TPC263_INDEPENDENT_CHECK=PASS "
          f"geometry_checks={geometry_checks} mutation_cases={mutations} "
          "projection=rank3 residual=explicit channel=log_only")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC263_INDEPENDENT_CHECK=FAIL " + str(exc))
        raise SystemExit(1)
