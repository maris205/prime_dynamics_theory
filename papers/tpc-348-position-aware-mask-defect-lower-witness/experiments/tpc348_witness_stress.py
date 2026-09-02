#!/usr/bin/env python3
"""Hostile finite stress tests for the TPC-348 witness contract.

The mutations target the selector, the two-sided mask formula, the exact
anchor, and the certificate firewall.  A passing stress run means that these
small adversarial changes are rejected; it is not an asymptotic theorem.
"""

from __future__ import annotations

import copy
import json
import math
import os
from fractions import Fraction
from pathlib import Path

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-348-position-aware-mask-defect-lower-witness/results/"
    "tpc348_certificate.json")
TOL = 1.0e-10


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            first = p * p
            sieve[first:limit + 1:p] = b"\x00" * (
                (limit - first) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


def shell(q: int) -> list[int]:
    return [p for p in primes_up_to(160) if q < p <= 2 * q]


def signs(primes: list[int], law: str) -> list[int]:
    if law == "all_plus":
        return [1] * len(primes)
    if law == "alternating_index":
        return [1 if i % 2 == 0 else -1 for i in range(len(primes))]
    if law == "mod4_character":
        return [1 if p % 4 == 1 else -1 for p in primes]
    return [1 if i < len(primes) / 2 else -1
            for i in range(len(primes))]


def matrices(origin: int, count: int, q: int, exponent: int,
             law: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[int]]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    distance = differences.astype(np.float64)
    kernel = (66.0 ** (2 * exponent) /
              (66.0 * 66.0 + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    physical = np.zeros((count, count), dtype=np.float64)
    ideal = np.zeros((count, count), dtype=np.float64)
    primes = shell(q)
    for p, sign in zip(primes, signs(primes, law)):
        centered = ((differences % p == 0).astype(np.float64) -
                    1.0 / (p - 1))
        np.fill_diagonal(centered, 0.0)
        block = float(sign * p) * kernel * centered
        ideal += block
        valid = ((differences != 0) &
                 (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        physical += block * valid
    physical = (physical + physical.T) / 2.0
    ideal = (ideal + ideal.T) / 2.0
    return physical, ideal, physical - ideal, primes


def formula_column(values: np.ndarray, differences: np.ndarray,
                   kernel: np.ndarray, primes: list[int], law: str,
                   column: int, omit_left: bool = False,
                   omit_right: bool = False) -> np.ndarray:
    result = np.zeros(len(values), dtype=np.float64)
    target = values[column]
    for p, sign in zip(primes, signs(primes, law)):
        centered = ((differences[:, column] % p == 0).astype(np.float64) -
                    1.0 / (p - 1))
        centered[column] = 0.0
        base = float(sign * p) * kernel[:, column] * centered
        if target % p == 0:
            if not omit_right:
                result -= base
        elif not omit_left:
            result -= base * (values % p == 0)
    result[column] = 0.0
    return result


def expect_reject(action, label: str) -> None:
    try:
        action()
    except Exception:
        return
    raise RuntimeError("mutation was accepted: " + label)


def selector_guard(row: dict, values: np.ndarray, primes: list[int],
                   defect: np.ndarray) -> None:
    hits = np.flatnonzero(np.any(np.array([(values % p) == 0 for p in primes]),
                                 axis=0))
    columns = np.linalg.norm(defect, axis=0)
    best = int(hits[int(np.argmax(columns[hits]))])
    if row.get("best_hit_index") != best:
        raise RuntimeError("selector mismatch")
    if row.get("best_hit_position") != int(values[best]):
        raise RuntimeError("position mismatch")


def main() -> int:
    document = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    row = document["payload"]["rows"][0]
    values = np.arange(40097, 40097 + 256, dtype=np.int64)
    physical, ideal, defect, primes = matrices(40097, 256, 24, 1,
                                               "all_plus")
    hits = np.flatnonzero(np.any(np.array([(values % p) == 0 for p in primes]),
                                 axis=0))
    columns = np.linalg.norm(defect, axis=0)
    best = int(hits[int(np.argmax(columns[hits]))])
    dvals = np.linalg.eigvalsh((defect + defect.T) / 2.0)
    dnorm = max(abs(float(dvals[0])), abs(float(dvals[-1])))
    need(best in hits and columns[best] > 0.0, "positive hit witness")
    need(columns[best] <= dnorm * (1.0 + TOL), "coordinate lower bound")
    selector_guard(row, values, primes, defect)

    differences = values[:, None] - values[None, :]
    kernel = 66.0 ** 2 / (66.0 * 66.0 + differences.astype(np.float64) ** 2)
    np.fill_diagonal(kernel, 0.0)
    formula = formula_column(values, differences, kernel, primes,
                             "all_plus", best)
    need(float(np.max(np.abs(formula - defect[:, best]))) < 1.0e-10,
         "two-sided formula")

    expect_reject(
        lambda: selector_guard({**row, "best_hit_index": int((best + 1) % 256)},
                                values, primes, defect),
        "wrong coordinate selector")
    expect_reject(
        lambda: selector_guard({**row, "best_hit_position": int(values[best] + 1)},
                                values, primes, defect),
        "wrong coordinate position")
    expect_reject(
        lambda: need(float(np.max(np.abs(
            formula_column(values, differences, kernel, primes, "all_plus", best,
                           omit_left=True) - defect[:, best]))) < 1.0e-10,
                         "left-mask omission accepted"),
        "omitted left mask")
    expect_reject(
        lambda: need(float(np.max(np.abs(
            formula_column(values, differences, kernel, primes, "all_plus", best,
                           omit_right=True) - defect[:, best]))) < 1.0e-10,
                         "right-mask omission accepted"),
        "omitted right mask")

    mutated = copy.deepcopy(document)
    mutated["payload"]["finite_audit"]["positive_witness_rows"] = 191
    expect_reject(
        lambda: need(mutated["payload"]["finite_audit"][
            "positive_witness_rows"] == 192, "census mutation accepted"),
        "census mutation")
    mutated = copy.deepcopy(document)
    mutated["payload"]["claim_firewall"]["TPC348_FULL_GATE_B"] = "CLOSED"
    expect_reject(
        lambda: need(mutated["payload"]["claim_firewall"][
            "TPC348_FULL_GATE_B"] == "OPEN", "firewall mutation accepted"),
        "firewall mutation")
    mutated = copy.deepcopy(document)
    mutated["payload"]["exact_anchor"]["witness_index"] = 3
    expect_reject(
        lambda: need(mutated["payload"]["exact_anchor"]["witness_index"] == 4,
                     "anchor mutation accepted"),
        "anchor mutation")

    # A second small case checks that the inequality is not tied to one origin.
    _, _, defect2, primes2 = matrices(48097, 32, 36, 2, "half_split")
    values2 = np.arange(48097, 48129, dtype=np.int64)
    hits2 = np.flatnonzero(np.any(np.array([(values2 % p) == 0
                                             for p in primes2]), axis=0))
    cols2 = np.linalg.norm(defect2, axis=0)
    ev2 = np.linalg.eigvalsh((defect2 + defect2.T) / 2.0)
    n2 = max(abs(float(ev2[0])), abs(float(ev2[-1])))
    need(len(hits2) > 0 and float(cols2[hits2].max()) <= n2 * (1.0 + TOL),
         "second finite inequality")
    print("TPC348_STRESS=PASS exact_anchor=1 selector_mutations=2 "
          "mask_formula_mutations=2 firewall_mutations=3 projection_cases=2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
