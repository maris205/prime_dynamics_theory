#!/usr/bin/env python3
"""Independent equation-first reproduction for TPC-232."""

from __future__ import annotations

import json
import sys
from math import gcd
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from growing_resonance_depth import prime_shell, support_scan  # noqa: E402


class IndependentFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise IndependentFailure(message)


def equation_scan(Q: int, L: int) -> tuple[int, int]:
    h = 4 * L * Q
    primes = prime_shell(Q)
    channels = set()
    edges = set()
    for index, q1 in enumerate(primes):
        allowed1 = tuple(m for m in range(1, L * q1 // Q + 1) if gcd(m, h) == 1)
        for q2 in primes[index + 1 :]:
            allowed2 = {
                m for m in range(1, L * q2 // Q + 1) if gcd(m, h) == 1
            }
            for a in allowed1:
                remainder = h - a * q2
                if remainder > 0 and remainder % q1 == 0:
                    b = remainder // q1
                    if b in allowed2:
                        channels.add((q1, q2, a, b))
                        edges.add((q1, q2))
    return len(channels), len(edges)


def main() -> int:
    try:
        certificate = json.loads((PROJECT / "results/certificate.json").read_text(encoding="utf-8"))
        records = certificate["finite_scan"]["records"]
        for record in records:
            Q, L = record["Q"], record["L"]
            channels, edges = equation_scan(Q, L)
            need(channels == record["resonance_channels"], f"channel mismatch at {(Q, L)}")
            need(edges == record["unique_edges"], f"edge mismatch at {(Q, L)}")
            replay = support_scan(Q, L)
            need(replay == record, f"support replay mismatch at {(Q, L)}")
    except (IndependentFailure, OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"TPC232_INDEPENDENT_CHECK=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC232_INDEPENDENT_CHECK=PASS")
    print(f"scales={len(records)}")
    print("equation_vs_support=IDENTICAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
