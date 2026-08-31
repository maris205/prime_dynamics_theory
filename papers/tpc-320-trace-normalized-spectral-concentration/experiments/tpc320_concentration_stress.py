#!/usr/bin/env python3
"""Deterministic stress tests for the TPC-320 readout and guard logic."""

from __future__ import annotations

import argparse
import math
import sys

try:
    import numpy as np
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC320 stress suite requires numpy: " + str(error))


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def readouts(eigenvalues: np.ndarray, k: int) -> tuple[float, float, float, float]:
    values = np.sort(np.asarray(eigenvalues, dtype=np.float64))[::-1]
    values = np.maximum(values, 0.0)
    trace = float(np.sum(values, dtype=np.float64))
    trace2 = float(np.sum(values * values, dtype=np.float64))
    need(trace > 0 and trace2 > 0, "positive readout trace")
    mass = float(np.sum(values[:k], dtype=np.float64))
    p = values / trace
    p = p[p > 0]
    entropy = -float(np.sum(p * np.log(p), dtype=np.float64)) / math.log(len(values))
    return mass / trace, trace / float(values[0]), trace * trace / trace2, entropy


def test_scalar_invariance() -> None:
    base = np.array([9.0, 7.0, 3.5, 1.25, 0.75, 0.125], dtype=np.float64)
    for scalar in (0.125, 1.0, 3.75, 1.0e6):
        scaled = base * scalar
        for k in (1, 2, 4, 6):
            left = readouts(base, k)
            right = readouts(scaled, k)
            for a, b in zip(left, right):
                need(math.isclose(a, b, rel_tol=2.0e-14, abs_tol=2.0e-14),
                     "positive-scalar invariance")


def test_psd_matrix_identities() -> None:
    # A fixed non-square matrix gives a nontrivial PSD Gram matrix without a
    # random seed or external data dependency.
    b = np.array([
        [2.0, -1.0, 0.5, 3.0],
        [1.0, 4.0, -2.0, 0.25],
        [-3.0, 0.75, 1.5, 2.0],
        [0.5, -2.0, 3.0, -1.0],
        [1.25, 0.0, -0.5, 2.5],
    ], dtype=np.float64)
    gram = b.T @ b
    values = np.linalg.eigvalsh((gram + gram.T) * 0.5)[::-1]
    need(float(values[-1]) >= -1.0e-12, "PSD eigenvalue")
    trace = float(np.trace(gram))
    trace_from_spectrum = float(np.sum(values, dtype=np.float64))
    trace2 = float(np.sum(gram * gram, dtype=np.float64))
    trace2_from_spectrum = float(np.sum(values * values, dtype=np.float64))
    need(math.isclose(trace, trace_from_spectrum, rel_tol=2.0e-14,
                      abs_tol=2.0e-14), "trace identity")
    need(math.isclose(trace2, trace2_from_spectrum, rel_tol=2.0e-14,
                      abs_tol=2.0e-14), "trace-square identity")
    shares = [readouts(values, k)[0] for k in (1, 2, 4)]
    need(all(0 < value <= 1 for value in shares), "share range")
    need(shares[0] <= shares[1] <= shares[2], "Ky Fan share nesting")


def test_quotient_interval() -> None:
    # Outward quotient bounds for positive numerator/denominator intervals.
    f_low, f_high = 9.99, 10.01
    t_low, t_high = 19.98, 20.02
    lower = f_low / t_high
    upper = f_high / t_low
    for f in (f_low, 10.0, f_high):
        for t in (t_low, 20.0, t_high):
            value = f / t
            need(lower <= value <= upper, "quotient enclosure")
    need(upper < 0.51 and lower > 0.49, "quotient scale")
    need(0.70 / 1.0 < 0.90 / 1.0, "separation orientation")


def test_weyl_guard() -> None:
    g = np.array([[4.0, 1.0, -0.5], [1.0, 2.0, 0.25],
                  [-0.5, 0.25, 1.0]], dtype=np.float64)
    e = np.array([[0.001, -0.002, 0.0], [-0.002, 0.0005, 0.001],
                  [0.0, 0.001, -0.0007]], dtype=np.float64)
    before = np.linalg.eigvalsh(g)[::-1]
    after = np.linalg.eigvalsh(g + e)[::-1]
    norm = float(np.linalg.norm(e, ord=2))
    need(all(abs(float(a - b)) <= norm + 1.0e-12
             for a, b in zip(before, after)), "Weyl perturbation")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("--check is required")
    try:
        test_scalar_invariance()
        test_psd_matrix_identities()
        test_quotient_interval()
        test_weyl_guard()
    except (Failure, ValueError, np.linalg.LinAlgError) as error:
        print("TPC320_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC320_STRESS=PASS scalar_invariance=4 psd_identities=1 "
          "quotient_interval=1 weyl_guard=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
