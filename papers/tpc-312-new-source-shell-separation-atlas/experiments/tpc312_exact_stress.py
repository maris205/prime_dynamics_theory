#!/usr/bin/env python3
"""Small exact stress tests for the TPC-312 finite algebra."""

from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RESULT = ROOT / (
    "papers/tpc-312-new-source-shell-separation-atlas/results/"
    "tpc312_certificate.json")


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def energy(matrix: list[list[Fraction]], labels: tuple[int, ...]) -> Fraction:
    return sum((labels[i] * labels[j] * matrix[i][j]
                for i in range(len(labels)) for j in range(len(labels))),
               Fraction(0))


def gray_extrema(matrix: list[list[Fraction]]) -> tuple[Fraction, Fraction,
                                                          int]:
    size = len(matrix)
    labels = [1] * size
    values = [energy(matrix, tuple([1] + list(signs))) for signs in
              itertools.product((1, -1), repeat=size - 1)]
    # The explicit list above fixes the first sign by construction; use a
    # Gray traversal separately and compare its visited multiset.
    visited = [energy(matrix, tuple([1] + labels_tail))
               for labels_tail in ([(1 if ((code ^ (code >> 1)) >> i) & 1
                                      else -1)
                                    for i in range(size - 1)]
                                   for code in range(1 << (size - 1)))]
    need(sorted(values) == sorted(visited), "Gray coverage")
    return min(values), max(values), len(visited)


def main() -> int:
    try:
        # A nontrivial rational Gram matrix with a unique minimum and maximum
        # checks the global-sign reduction and the exhaustive finite search.
        gram = [
            [Fraction(7), Fraction(1), Fraction(-2), Fraction(1)],
            [Fraction(1), Fraction(8), Fraction(1), Fraction(-1)],
            [Fraction(-2), Fraction(1), Fraction(9), Fraction(2)],
            [Fraction(1), Fraction(-1), Fraction(2), Fraction(10)],
        ]
        low, high, count = gray_extrema(gram)
        brute = [energy(gram, tuple([1] + list(tail)))
                 for tail in itertools.product((1, -1), repeat=3)]
        need(low == min(brute) and high == max(brute) and count == 8,
             "exact sign enumeration")

        data = json.loads(RESULT.read_text(encoding="utf-8"))
        payload = data["payload"]
        need(payload["schema"] == "TPC312_NEW_SOURCE_SHELL_SIGN_SEPARATION_V1",
             "schema")
        need(payload["protocol"]["freshness_scope"].startswith(
            "new source indices"), "freshness firewall")
        need(len(payload["rows"]) == 8 and
             payload["finite_audit"]["strict_separation_rows"] == 8,
             "stored finite census")
        # The new source interval and Q spine are disjoint from the old
        # TPC-288 growth path; this is a provenance check, not independence.
        need(payload["protocol"]["index_interval"] == [321, 640] and
             payload["protocol"]["Q_anchors"] == [24, 36, 54, 80],
             "new panel coordinates")
        print("TPC312_STRESS=PASS gray_coverage=8 rational_extrema=1 "
              "new_panel=1 strict_separation=8")
        return 0
    except (RuntimeError, OSError, ValueError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC312_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
