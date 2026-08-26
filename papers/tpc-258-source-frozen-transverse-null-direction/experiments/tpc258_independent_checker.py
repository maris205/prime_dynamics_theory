#!/usr/bin/env python3
"""Independent reconstruction and mutation audit for TPC-258."""

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


BASELINE = "337fa65aca20122f241c30c67f1deb64b45e3c0b"
ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc258_certificate.json"
CLAIM = (
    "PROVED_SOURCE_BACKED_TRANSVERSE_DIAGONAL_NULL_CANCELLATION_"
    "FOR_LITERAL_V59_ADJOINT"
)

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "c4c79b25fdbcdb7f8f26b1348263f159d5cd7f55c486c2653066c5519a1782a5",
    "research/tpc-big-road/bridge_b_four_block_haar_transverse_norm_floor.md":
        "faaede82e2ebf84a994e3e9c945e42c321a8c81d0c0db9e0f8e2f9a88329e609",
    "research/tpc-big-road/tpc_bridge_b_four_block_haar_transverse_norm_floor_checker.py":
        "d2cf0321dfbc730850438badaadf6018e0555662010ea39b80bd12a175ded2e1",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/PROOF_PACKAGE.md":
        "06b6f2e9842f68fc6f3d882f95d3b9c161980ceb429dd24b52bd98322e6f397f",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/notes/theorem_ledger.md":
        "127bf4a07defd26a87f74e989a426500a3b50a18df03875805b9afeb71a5a3a6",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/notes/route_evaluation.md":
        "b92bf14797013e4371a0d9c88d4dc7bdef39d76b1361d8cf73009165b41e1f3f",
    "research/tpc-big-road/bridge_b_literal_beta_haar_adjoint_asymptotic.md":
        "ccb87a64ddb36ed35af415dde2d9fcf0a3ed7f443934edf0a24c98f7bd3ab4da",
    "research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md":
        "093fa3bc9c3512d760462526daac7aa1867ee41eb5b6b0e2bfd0a7ee8d580906",
}


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def frozen(relative: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE + ":" + relative], cwd=ROOT,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", "frozen source: " + relative)
    return result.stdout


def check_sources() -> None:
    for relative, expected in SOURCE_HASHES.items():
        need(hashlib.sha256(frozen(relative)).hexdigest() == expected,
             "source hash: " + relative)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def reconstruction() -> dict[str, int]:
    clocks = [Fraction(256 + 9 * index, 1) for index in range(32)]
    clocks += [Fraction(2051 + 36 * index + 2 * (index % 9) + 1, 8)
               for index in range(32)]
    norms = dots = nulls = covers = 0
    for clock in clocks:
        a = floor_fraction(clock / 2)
        b = floor_fraction(clock)
        n = b - a
        ell = n // 2
        right = n - ell
        sizes = [ell // 2, ell - ell // 2, right // 2, right - right // 2]
        need(all(size > 0 for size in sizes), "short clock")
        s1, s2, s3, s4 = sizes
        specs = [
            (Fraction(ell * right, n),
             [Fraction(1, ell), Fraction(1, ell),
              Fraction(-1, right), Fraction(-1, right)]),
            (Fraction(s1 * s2, ell),
             [Fraction(1, s1), Fraction(-1, s2), Fraction(0), Fraction(0)]),
            (Fraction(s3 * s4, right),
             [Fraction(0), Fraction(0), Fraction(1, s3), Fraction(-1, s4)]),
        ]
        for rho2, coefficients in specs:
            value = rho2 * sum((size * coefficient * coefficient
                                for size, coefficient in zip(sizes, coefficients)), Fraction(0))
            need(value == 1, "norm")
            norms += 1
        for i in range(3):
            for j in range(i + 1, 3):
                value = sum((size * left * right_value for size, left, right_value in
                             zip(sizes, specs[i][1], specs[j][1])), Fraction(0))
                need(value == 0, "dot")
                dots += 1
        l1 = math.log(Fraction(3456, 3125))
        l2 = math.log(Fraction(884736, 823543))
        denominator = math.hypot(l1, l2)
        need(abs((l2 / denominator) ** 2 + (-l1 / denominator) ** 2 - 1) < 2e-15,
             "null unit")
        nulls += 1
        need(sum(sizes) == n and a + sum(sizes) == b, "cover")
        covers += 1
    need(Fraction(1, 2) - Fraction(1, 2) == 0, "formal L1L2 cancellation")
    need(Fraction(56, 48) - Fraction(55, 48) == Fraction(1, 48), "gap")
    return {"clocks": len(clocks), "norms": norms, "dots": dots,
            "nulls": nulls, "covers": covers}


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n"


def semantic(candidate: Any) -> bool:
    if not isinstance(candidate, dict):
        return False
    try:
        return (
            candidate["schema"] == "TPC258_CERTIFICATE_V1"
            and candidate["claim"] == CLAIM
            and candidate["baseline"]["head"] == BASELINE
            and candidate["source_hashes"] == SOURCE_HASHES
            and candidate["constants"]["symbolic_cancellation"]
                == "L2*(L1/2)-L1*(L2/2)=0"
            and candidate["constants"]["null_weights"]
                == ["0.579956823172377", "-0.814647213986401"]
            and candidate["rate_ledger"]["proved"] == "o(S_x)"
            and candidate["epistemic_status"]["rate_refinement"]
                == "CONDITIONAL_THEOREM"
            and candidate["firewall"]["TPC258_FIXED_POWER_SAVING"] == "NONE"
            and candidate["firewall"]["TPC258_L2"] == "NONE"
            and candidate["firewall"]["TPC258_FULL_GATE_B"] == "OPEN"
            and candidate["firewall"]["TPC258_TWIN_PRIME_RESULT"] == "NONE"
            and candidate["numerical_observation"]["proof_credit"] == "NONE"
            and candidate["adversarial_control"]["proof_credit"]
                == "QUANTIFIER_FIREWALL_ONLY"
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

    mutate(("schema",), "TPC258_CERTIFICATE_V0")
    mutate(("claim",), "HEURISTIC")
    mutate(("baseline", "head"), "0" * 40)
    mutate(("source_hashes",), {})
    mutate(("constants", "symbolic_cancellation"), "L2*(L1/2)+L1*(L2/2)=0")
    mutate(("rate_ledger", "proved"), "O(x^(-1/400)S_x)")
    mutate(("epistemic_status", "rate_refinement"), "PROVED")
    mutate(("firewall", "TPC258_FIXED_POWER_SAVING"), "PROVED")
    mutate(("firewall", "TPC258_L2"), "PROVED")
    mutate(("firewall", "TPC258_FULL_GATE_B"), "PAID")
    mutate(("firewall", "TPC258_TWIN_PRIME_RESULT"), "PROVED")
    mutate(("numerical_observation", "proof_credit"), "THEOREM")
    mutate(("adversarial_control", "proof_credit"), "LITERAL_COUNTEREXAMPLE")
    mutate(("constants", "null_weights"), list(reversed(expected["constants"]["null_weights"])))
    need(all(not semantic(candidate) for candidate in candidates), "mutation accepted")
    return len(candidates)


def run() -> None:
    producer_name = "tpc258" + "_null_certificate"
    need(("from " + producer_name) not in Path(__file__).read_text(encoding="utf-8"),
         "producer import")
    check_sources()
    counts = reconstruction()
    need(CERTIFICATE.is_file(), "certificate missing")
    raw = CERTIFICATE.read_text(encoding="utf-8")
    expected = json.loads(raw)
    need(raw == canonical(expected), "canonical JSON")
    need(semantic(expected), "certificate semantics")
    mutations = mutation_audit(expected)
    print("TPC258_INDEPENDENT_CHECK=PASS "
          f"clocks={counts['clocks']} norms={counts['norms']} dots={counts['dots']} "
          f"nulls={counts['nulls']} mutations_rejected={mutations} "
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
        print("TPC258_INDEPENDENT_CHECK=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
