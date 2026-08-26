#!/usr/bin/env python3
"""Independent reconstruction and mutation audit for TPC-259."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE = "dc1f6628cc4953eeaad015aac79e48e6ca546773"
ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc259_certificate.json"
CLAIM = (
    "PROVED_SOURCE_BACKED_SAME_CLOCK_NULL_CHANNEL_SUPPRESSION_"
    "FOR_LITERAL_V59_SIGNED_COUPLING"
)

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "de46b106bfdf26832e9fb9c1dfbe3066088d89bb4d299d1de2cbc4b24121ba2f",
    "papers/tpc-258-source-frozen-transverse-null-direction/README.md":
        "760687705f6e4f4edf83dc1753eab092d36bbefb7d74bd4a0f857dd719bf3083",
    "papers/tpc-258-source-frozen-transverse-null-direction/PROOF_PACKAGE.md":
        "9676295123b94cabc78a3e24b95475380557a5a3accc0b890ba33e18a5e09c19",
    "papers/tpc-258-source-frozen-transverse-null-direction/notes/theorem_ledger.md":
        "66f70e7d6594f01ce872d1b9d0ecfe83bd96d2549986a9bd456dc7f6d049618a",
    "papers/tpc-258-source-frozen-transverse-null-direction/notes/route_evaluation.md":
        "f45a8b300b8f1fc7aa02b76d58ab78a2186b53a744380c129b42eac724639b5f",
    "research/tpc-big-road/bridge_b_source_frozen_transverse_null_direction.md":
        "0f5d65ffc419ac07c47c282ce34f05800e6d7342b6ffd8588d06c102c4b4c75d",
    "research/tpc-big-road/tpc_bridge_b_source_frozen_transverse_null_direction_checker.py":
        "770e47e9495bee3ed5115a29f6b050c14a529f2b14814ab09fdfcdb8d4dc42c2",
    "papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/PROOF_PACKAGE.md":
        "bb23c4dfc5cced89b34db0d2741b570c07335ac9aa153ae123d056f29924b768",
    "research/tpc-big-road/bridge_b_source_backed_rank_midpoint_hybrid_mean_closure.md":
        "6e5cb92642bf8fc8f0a3a56a29c4c061359f3794e24345d76a62d2fccf5a21ee",
    "research/tpc-big-road/fm_local_comparison_compiler.md":
        "4f7537ff5a10d53634638afff508ee6e3401364dab7970852b327470918c644f",
}


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def frozen(relative: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE + ":" + relative],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"",
         "frozen source: " + relative)
    return result.stdout


def check_sources() -> None:
    for relative, expected in SOURCE_HASHES.items():
        need(hashlib.sha256(frozen(relative)).hexdigest() == expected,
             "source hash: " + relative)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def independent_sizes(clock: Fraction) -> tuple[int, int, list[int]]:
    left_endpoint = floor_fraction(clock / 2)
    right_endpoint = floor_fraction(clock)
    total = right_endpoint - left_endpoint
    left_half, left_remainder = divmod(total, 2)
    right_half = total - left_half
    a, b = divmod(left_half, 2)
    c, d = divmod(right_half, 2)
    sizes = [a, a + b, c, c + d]
    return left_endpoint, right_endpoint, sizes


def independent_geometry() -> dict[str, int]:
    clocks = [Fraction(300 + 13 * i, 1) for i in range(32)]
    clocks += [Fraction(2401 + 29 * i + 2 * (i % 7) + 1, 8)
               for i in range(32)]
    norms = dots = nulls = covers = projections = witnesses = 0
    l1 = math.log(3456.0 / 3125.0)
    l2 = math.log(884736.0 / 823543.0)
    length = math.hypot(l1, l2)
    q1, q2 = l2 / length, -l1 / length
    need(abs(q1 * q1 + q2 * q2 - 1.0) < 2e-15, "null unit")
    for clock in clocks:
        a, b, sizes = independent_sizes(clock)
        need(all(size > 0 for size in sizes), "short block")
        total = sum(sizes)
        ell = sizes[0] + sizes[1]
        right = sizes[2] + sizes[3]
        need(total == b - a and a + total == b, "source cover")
        covers += 1
        specs = [
            (Fraction(ell * right, total),
             [Fraction(1, ell), Fraction(1, ell),
              Fraction(-1, right), Fraction(-1, right)]),
            (Fraction(sizes[0] * sizes[1], ell),
             [Fraction(1, sizes[0]), Fraction(-1, sizes[1]),
              Fraction(0), Fraction(0)]),
            (Fraction(sizes[2] * sizes[3], right),
             [Fraction(0), Fraction(0), Fraction(1, sizes[2]),
              Fraction(-1, sizes[3])]),
        ]
        for rho2, vector in specs:
            norm = rho2 * sum((size * value * value
                               for size, value in zip(sizes, vector)),
                              Fraction(0))
            need(norm == 1, "frame norm")
            norms += 1
        for i in range(3):
            for j in range(i + 1, 3):
                dot = sum((size * left * right_value
                           for size, left, right_value
                           in zip(sizes, specs[i][1], specs[j][1])),
                          Fraction(0))
                need(dot == 0, "frame orthogonality")
                dots += 1
        need(abs(q1) + abs(q2) < 2, "null coefficient bound")
        nulls += 1

        # Independent exact check of the conjugate-safe rank-one split.
        z = [Fraction(1), Fraction(0)]
        w = [Fraction((-1) ** (int(clock) % 3)), Fraction(2 + int(clock) % 5)]
        output = [Fraction(3 + int(clock) % 4), Fraction(-4 - int(clock) % 6)]
        c = sum((z[i] * w[i] for i in range(2)), Fraction(0))
        residual_vector = [w[i] - c * z[i] for i in range(2)]
        lhs = sum((w[i] * output[i] for i in range(2)), Fraction(0))
        rhs = c * sum((z[i] * output[i] for i in range(2)), Fraction(0))
        rhs += sum((residual_vector[i] * output[i] for i in range(2)),
                   Fraction(0))
        need(lhs == rhs and residual_vector[0] == 0, "projection split")
        projections += 1

        for lam in (Fraction(-5, 2), Fraction(7, 3)):
            witness_z = [Fraction(1), Fraction(0)]
            witness_w = [Fraction(0), Fraction(1)]
            witness_output = [Fraction(0), lam]
            need(sum(witness_z[i] * witness_w[i] for i in range(2)) == 0,
                 "witness null")
            need(sum(witness_w[i] * witness_output[i] for i in range(2)) == lam,
                 "witness full")
            witnesses += 1
    need(Fraction(1, 2) + Fraction(55, 48) == Fraction(79, 48),
         "boundary exponent")
    need(Fraction(5, 3) - Fraction(79, 48) == Fraction(1, 48),
         "exponent gap")
    return {"clocks": len(clocks), "norms": norms, "dots": dots,
            "nulls": nulls, "covers": covers, "projections": projections,
            "witnesses": witnesses}


def semantic(candidate: Any) -> bool:
    if not isinstance(candidate, dict):
        return False
    try:
        firewall = candidate["firewall"]
        return (
            candidate["schema"] == "TPC259_CERTIFICATE_V1"
            and candidate["claim"] == CLAIM
            and candidate["baseline"]["head"] == BASELINE
            and candidate["source_hashes"] == SOURCE_HASHES
            and candidate["null_constants"]["weights"]
                == ["0.579956823172377", "-0.814647213986401"]
            and candidate["exponent_ledger"] == {
                "gap": "1/48", "null_product": "5/3",
                "residual_boundary": "79/48", "source_diagonal": "7/6"}
            and candidate["epistemic_status"]["null_channel"]
                == "PROVED_SOURCE_BACKED_o_ONE"
            and candidate["epistemic_status"]["residual"] == "OPEN"
            and candidate["epistemic_status"]["rate_refinement"]
                == "CONDITIONAL_THEOREM"
            and firewall["TPC259_ROUTE_ADVANCE"] == "YES_SCOPED_NULL_CHANNEL"
            and firewall["TPC259_ARITHMETIC_ADVANCE"]
                == "YES_SCOPED_SIGNED_COUPLING_CHANNEL"
            and firewall["TPC259_FIXED_POWER_SAVING"] == "NONE"
            and firewall["TPC259_L2"] == "NONE"
            and firewall["TPC259_FULL_GATE_B"] == "OPEN"
            and firewall["TPC259_TWIN_PRIME_RESULT"] == "NONE"
            and candidate["rate_diagnostic"]["proof_credit"] == "NONE"
            and candidate["synthetic_witness"]["status"]
                == "PROVED_EXACT_SYNTHETIC_NOT_LITERAL"
            and candidate["synthetic_witness"]["null_channel"] == "0"
            and candidate["synthetic_witness"]["residual"] == "3/2"
        )
    except (KeyError, TypeError):
        return False


def mutation_audit(expected: dict[str, Any]) -> int:
    candidates: list[dict[str, Any]] = []

    def mutate(path: tuple[str, ...], value: Any) -> None:
        item = deepcopy(expected)
        cursor: Any = item
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        candidates.append(item)

    mutate(("schema",), "TPC259_CERTIFICATE_V0")
    mutate(("claim",), "HEURISTIC")
    mutate(("baseline", "head"), "0" * 40)
    mutate(("source_hashes",), {})
    mutate(("null_constants", "weights"), ["0.814647213986401", "-0.579956823172377"])
    mutate(("exponent_ledger", "gap"), "1/400")
    mutate(("epistemic_status", "null_channel"), "PROVED_FULL_SCALAR")
    mutate(("epistemic_status", "residual"), "PROVED")
    mutate(("epistemic_status", "rate_refinement"), "PROVED")
    mutate(("firewall", "TPC259_FIXED_POWER_SAVING"), "PROVED")
    mutate(("firewall", "TPC259_L2"), "PAID")
    mutate(("firewall", "TPC259_FULL_GATE_B"), "PAID")
    mutate(("firewall", "TPC259_TWIN_PRIME_RESULT"), "PROVED")
    mutate(("rate_diagnostic", "proof_credit"), "THEOREM")
    mutate(("synthetic_witness", "null_channel"), "3/2")
    mutate(("synthetic_witness", "status"), "PROVED_LITERAL_COUNTEREXAMPLE")
    need(all(not semantic(candidate) for candidate in candidates),
         "mutation accepted")
    return len(candidates)


def run() -> None:
    independent_name = "tpc259" + "_null_coupling_certificate"
    text = Path(__file__).read_text(encoding="utf-8")
    need(("from " + independent_name) not in text, "producer import")
    check_sources()
    counts = independent_geometry()
    need(CERTIFICATE.is_file(), "certificate missing")
    raw = CERTIFICATE.read_text(encoding="utf-8")
    parsed = json.loads(raw)
    need(raw == canonical(parsed), "certificate not canonical")
    need(semantic(parsed), "certificate semantics")
    mutations = mutation_audit(parsed)
    print("TPC259_INDEPENDENT_CHECK=PASS "
          f"clocks={counts['clocks']} norms={counts['norms']} "
          f"dots={counts['dots']} projections={counts['projections']} "
          f"witnesses={counts['witnesses']} mutations_rejected={mutations} "
          f"source_hashes={len(SOURCE_HASHES)} producer_imported=NO")


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
        print("TPC259_INDEPENDENT_CHECK=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
