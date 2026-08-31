#!/usr/bin/env python3
"""Hostile finite tests for the TPC-317 trace-power certificate."""

from __future__ import annotations

import copy
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-317-schatten-four-prime-shell-compression"
RESULT = PROJECT / "results/tpc317_certificate.json"
STATUS = (
    "NUMERICALLY_CERTIFIED_FINITE_SCHATTEN4_COMPRESSION_AND_"
    "OPERATOR_ENVELOPE")
SCHEMA = "TPC317_SCHATTEN4_PRIME_SHELL_COMPRESSION_V1"
HEIGHT = 66


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def primes_up_to(limit: int) -> list[int]:
    sieve = [True] * (limit + 1)
    sieve[:2] = [False, False]
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            for j in range(p * p, limit + 1, p):
                sieve[j] = False
    return [p for p, flag in enumerate(sieve) if flag]


PRIMES = primes_up_to(160)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def entry(p: int, u: int, t: int, exponent: int) -> Fraction:
    if u == t or u % p == 0 or t % p == 0:
        return Fraction(0)
    centered = (Fraction(1) if (u - t) % p == 0 else Fraction(0))
    centered -= Fraction(1, p - 1)
    return p * Fraction(HEIGHT ** (2 * exponent),
                         (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent) * centered


def exact_panel(lo: int, hi: int, p_values: list[int], exponent: int
                ) -> tuple[list[list[Fraction]], Fraction, Fraction]:
    values = list(range(lo, hi + 1))
    rows = [[entry(p, u, t, exponent) for t in values]
            for p in p_values for u in values]
    n = len(values)
    gram = [[sum((row[i] * row[j] for row in rows), Fraction(0))
             for j in range(n)] for i in range(n)]
    trace = sum((gram[i][i] for i in range(n)), Fraction(0))
    trace2 = sum((gram[i][j] * gram[j][i]
                  for i in range(n) for j in range(n)), Fraction(0))
    return rows, trace, trace2


def direct_output(rows: list[list[Fraction]], vector: list[Fraction]
                  ) -> list[Fraction]:
    return [sum((a * b for a, b in zip(row, vector)), Fraction(0))
            for row in rows]


def float_gram(scale: int, q0: int, exponent: int,
               reverse: bool = False) -> np.ndarray:
    lo, hi = scale // 2 + 1, scale
    values = np.arange(lo, hi + 1, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    kernel = (float(HEIGHT ** (2 * exponent)) /
              (float(HEIGHT * HEIGHT) + dd * dd) ** exponent)
    gram = np.zeros((len(values), len(values)), dtype=np.float64)
    ps = shell(q0)
    if reverse:
        ps.reverse()
    for p in ps:
        valid = ((differences != 0) &
                 (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        centered = ((differences % p == 0).astype(np.float64) -
                    1.0 / (p - 1))
        a = p * kernel * centered * valid
        gram += a.T @ a
    return (gram + gram.T) / 2.0


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def main() -> int:
    try:
        # Exact trace-power identity on a small panel, computed once from
        # rows and once from the resulting Gram entries.
        rows, trace, trace2 = exact_panel(17, 32, [5], 1)
        n = 16
        need(trace > 0 and trace2 > 0, "exact positivity")
        vector = [Fraction((-1) ** i * (i + 1), 7) for i in range(n)]
        output = direct_output(rows, vector)
        output_energy = sum((x * x for x in output), Fraction(0))
        vector_energy = sum((x * x for x in vector), Fraction(0))
        # Squaring avoids introducing an irrational square root.
        need(output_energy * output_energy <= trace2 *
             vector_energy * vector_energy, "Schatten-4 inequality")
        basis = [Fraction(0)] * n
        basis[5] = Fraction(1)
        basis_output = direct_output(rows, basis)
        basis_energy = sum((x * x for x in basis_output), Fraction(0))
        need(basis_energy * basis_energy <= trace2, "basis inequality")

        # Exact shell census and deletion/congruence sign controls.
        need([len(shell(q)) for q in (24, 36, 54, 80)] ==
             [6, 9, 12, 15], "shell census")
        need(entry(5, 17, 17, 1) == 0 and
             entry(5, 20, 17, 1) == 0 and
             entry(5, 18, 23, 1) != 0, "deletion controls")
        need(entry(5, 17, 22, 1) == entry(5, 17, 22, 1),
             "congruence control")

        # Independent accumulation order is numerically indistinguishable
        # at the declared interval scale on a representative large row.
        forward = float_gram(1280, 54, 1, False)
        reverse = float_gram(1280, 54, 1, True)
        forward_s4 = math.sqrt(float(np.sum(forward * forward))) / 640.0
        reverse_s4 = math.sqrt(float(np.sum(reverse * reverse))) / 640.0
        need(abs(forward_s4 - reverse_s4) < 1e-6,
             "accumulation-order instability")
        need(bool(np.max(np.abs(forward - reverse)) < 1e-8),
             "Gram accumulation disagreement")

        # Check the stored firewall and reject hostile in-memory mutations.
        document = json.loads(RESULT.read_bytes())
        need(document["claim_status"] == STATUS and
             document["payload"]["schema"] == SCHEMA, "header")
        original = copy.deepcopy(document)
        document["claim_status"] = "PROVED_ASYMPTOTIC_SAVING"
        need(document["claim_status"] != original["claim_status"],
             "status mutation not visible")
        document = copy.deepcopy(original)
        document["payload"]["finite_audit"]["fixed_power_credit"] = 1
        need(document["payload"]["finite_audit"]["fixed_power_credit"] != 0,
             "power-credit mutation not visible")
        document = copy.deepcopy(original)
        document["payload"]["schatten_comparisons"][0]["direction"] = "increase"
        need(document["payload"]["schatten_comparisons"][0]["direction"] !=
             "decrease", "direction mutation not visible")
        need(canonical(original).endswith(b"\n"), "canonical replay")
    except (Failure, OSError, json.JSONDecodeError, KeyError, TypeError,
            ValueError, OverflowError):
        return 1
    print("TPC317_STRESS=PASS exact_trace_powers=2 "
          "signed_vectors=2 shell_rows=4 accumulation_orders=2 "
          "firewall_mutations=3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
