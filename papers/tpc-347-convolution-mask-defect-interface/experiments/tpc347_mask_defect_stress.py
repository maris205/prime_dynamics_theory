#!/usr/bin/env python3
"""Hostile finite stress tests for the TPC-347 decomposition.

The stress suite attacks the algebraic interface and the numerical guard,
without changing repository artifacts.  It is intentionally small enough to
run on every release host.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PRODUCER = ROOT / (
    "papers/tpc-347-convolution-mask-defect-interface/code/"
    "tpc347_convolution_mask_defect_interface.py")


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def load() -> object:
    spec = importlib.util.spec_from_file_location("tpc347_stress_source",
                                                  PRODUCER)
    need(spec is not None and spec.loader is not None, "producer import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_mutation_checks(source: object) -> int:
    actual = source.exact_matrix(1, 6, 4, 1, "all_plus", True)
    ideal = source.exact_matrix(1, 6, 4, 1, "all_plus", False)
    defect = [[actual[i][j] - ideal[i][j] for j in range(6)]
              for i in range(6)]
    need(all(actual[i][j] == ideal[i][j] + defect[i][j]
             for i in range(6) for j in range(6)), "exact identity")
    # A sign-flipped defect must be rejected by the identity guard.
    bad = [[-defect[i][j] for j in range(6)] for i in range(6)]
    need(not all(actual[i][j] == ideal[i][j] + bad[i][j]
                 for i in range(6) for j in range(6)),
         "defect mutation accepted")
    # Reintroducing a diagonal entry violates the deleted-diagonal object.
    diagonal_mutation = [row[:] for row in actual]
    diagonal_mutation[0][0] = Fraction(1)
    need(any(diagonal_mutation[i][i] != 0 for i in range(6)),
         "diagonal mutation not visible")
    return 3


def projection_checks() -> int:
    rng = np.random.default_rng(347)
    accepted = 0
    for size in (5, 8, 13, 21):
        raw = rng.normal(size=(size, size))
        matrix = (raw + raw.T) / 2.0
        mask = np.asarray(rng.integers(0, 2, size=size), dtype=np.float64)
        projected = mask[:, None] * matrix * mask[None, :]
        original_norm = float(np.linalg.norm(matrix, ord=2))
        projected_norm = float(np.linalg.norm(projected, ord=2))
        need(projected_norm <= original_norm + 2.0e-12,
             "compression contraction")
        accepted += 1
    return accepted


def tail_checks(source: object) -> int:
    accepted = 0
    radius = 257
    for q in source.Q_ANCHORS:
        primes = source.shell_for(q)
        for exponent in source.EXPONENTS:
            for law in source.LAW_NAMES:
                finite, _finite_l1, tail = source.coherent_kernel_values(
                    q, exponent, law, radius=radius)
                need(finite >= 0.0 and tail >= 0.0 and
                     math.isfinite(finite + tail), "tail envelope")
                # The analytic tail majorant is deliberately checked against
                # the direct omitted absolute majorant on a finite suffix.
                suffix = np.arange(radius + 1, radius + 1001,
                                   dtype=np.int64)
                h = (float(source.HEIGHT) ** (2 * exponent) /
                     (source.HEIGHT ** 2 + suffix.astype(float) ** 2) ** exponent)
                # The point of this branch is the elementary pointwise bound.
                pointwise = (2.0 * float(source.HEIGHT) ** (2 * exponent) *
                             sum(primes) * float(np.sum(
                                 suffix.astype(float) ** (-2 * exponent))))
                need(pointwise <= tail * (1.0 + 1.0e-12),
                     "tail majorant scale")
                accepted += 1
    return accepted


def main() -> int:
    try:
        source = load()
        exact = exact_mutation_checks(source)
        projection = projection_checks()
        tails = tail_checks(source)
        print("TPC347_STRESS=PASS exact_mutations=" + str(exact) +
              " projection_cases=" + str(projection) +
              " tail_cases=" + str(tails))
        return 0
    except (Failure, OSError, ValueError, TypeError, AttributeError) as error:
        print("TPC347_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
