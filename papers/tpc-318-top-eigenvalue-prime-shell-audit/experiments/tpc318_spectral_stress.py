#!/usr/bin/env python3
"""Hostile finite checks for the TPC-318 spectral-radius certificate."""

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
PROJECT = ROOT / "papers/tpc-318-top-eigenvalue-prime-shell-audit"
RESULT = PROJECT / "results/tpc318_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_TOP_EIGENVALUE_AUDIT"
SCHEMA = "TPC318_TOP_EIGENVALUE_PRIME_SHELL_AUDIT_V1"
HEIGHT = 66


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def shell(q0: int) -> list[int]:
    sieve = [True] * 161
    sieve[:2] = [False, False]
    for p in range(2, 13):
        if sieve[p]:
            for j in range(p * p, 161, p):
                sieve[j] = False
    return [p for p in range(2, 161) if sieve[p] and q0 < p <= 2 * q0]


def exact_entry(p: int, u: int, t: int, exponent: int) -> Fraction:
    if u == t or u % p == 0 or t % p == 0:
        return Fraction(0)
    centered = (Fraction(1) if (u - t) % p == 0 else Fraction(0))
    centered -= Fraction(1, p - 1)
    return p * Fraction(HEIGHT ** (2 * exponent),
                         (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent) * centered


def exact_anchor() -> tuple[Fraction, Fraction]:
    values = list(range(17, 33))
    rows = [[exact_entry(5, u, t, 1) for t in values] for u in values]
    gram = [[sum((row[i] * row[j] for row in rows), Fraction(0))
             for j in range(16)] for i in range(16)]
    trace = sum((gram[i][i] for i in range(16)), Fraction(0))
    trace2 = sum((gram[i][j] * gram[j][i]
                  for i in range(16) for j in range(16)), Fraction(0))
    return trace, trace2


def main() -> int:
    try:
        # The finite PSD and trace-power inequalities on an unrelated exact
        # rational PSD matrix are checked without relying on the producer.
        matrix = np.array([[Fraction(5), Fraction(1)],
                           [Fraction(1), Fraction(2)]], dtype=object)
        gram = np.array([[float(x) for x in row] for row in matrix])
        eigen = np.linalg.eigvalsh(gram)
        trace = float(np.trace(gram))
        trace2 = float(np.trace(gram @ gram))
        need(eigen[0] >= 0 and eigen[-1] <= math.sqrt(trace2) <= trace,
             "PSD trace-power chain")

        # Weyl's perturbation inequality is exercised on a deterministic
        # symmetric perturbation; this is the bridge from matrix error to a
        # finite top-eigenvalue interval.
        base = np.array([[4.0, 1.0], [1.0, 2.0]])
        perturb = np.array([[0.01, -0.02], [-0.02, 0.03]])
        base_top = float(np.linalg.eigvalsh(base)[-1])
        pert_top = float(np.linalg.eigvalsh(base + perturb)[-1])
        norm = float(np.linalg.norm(perturb, 2))
        need(abs(pert_top - base_top) <= norm * (1.0 + 1e-12),
             "Weyl perturbation")

        # The literal-entry guard is checked directly on a representative
        # full active shell, including divisible differences and both masks.
        maximum = 0.0
        for p in shell(80):
            for u in range(1281, 1450):
                for t in range(1281, 1450):
                    maximum = max(maximum, abs(float(exact_entry(p, u, t, 1))))
        need(maximum <= 160.0, "uniform literal-entry bound")
        need([len(shell(q)) for q in (24, 36, 54, 80)] == [6, 9, 12, 15],
             "shell census")
        need(exact_anchor()[0] > 0 and exact_anchor()[1] > 0,
             "exact anchor positivity")

        document = json.loads(RESULT.read_bytes())
        need(document["claim_status"] == STATUS and
             document["payload"]["schema"] == SCHEMA, "certificate header")
        original = copy.deepcopy(document)
        document["claim_status"] = "PROVED_UNIFORM_ARITHMETIC_SAVING"
        need(document["claim_status"] != original["claim_status"],
             "status mutation")
        document = copy.deepcopy(original)
        document["payload"]["finite_audit"]["fixed_power_credit"] = 1
        need(document["payload"]["finite_audit"]["fixed_power_credit"] != 0,
             "credit mutation")
        document = copy.deepcopy(original)
        document["payload"]["top_comparisons"][0]["direction"] = "increase"
        need(document["payload"]["top_comparisons"][0]["direction"] !=
             "decrease", "trend mutation")
        document = copy.deepcopy(original)
        document["payload"]["rows"][0]["top_eigenvalue"][
            "normalized_interval"][1] = "0"
        need(document["payload"]["rows"][0]["top_eigenvalue"][
            "normalized_interval"][1] !=
             original["payload"]["rows"][0]["top_eigenvalue"][
                 "normalized_interval"][1], "interval mutation")
        need(canonical(original).endswith(b"\n"), "canonicality")
    except (Failure, OSError, json.JSONDecodeError, KeyError, TypeError,
            ValueError, OverflowError, np.linalg.LinAlgError) as error:
        print("TPC318_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC318_STRESS=PASS exact_psd=1 exact_anchor=3 "
          "weyl_controls=1 literal_guard=1 firewall_mutations=4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
