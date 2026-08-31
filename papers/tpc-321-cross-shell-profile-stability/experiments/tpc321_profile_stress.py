#!/usr/bin/env python3
"""Deterministic stress tests for TPC-321 profile diagnostics."""

from __future__ import annotations

import argparse
import math
import sys

try:
    import numpy as np
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC321 stress suite requires numpy: " + str(error))

SIGN_TOL = 1.0e-8


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def profile(values: list[float]) -> np.ndarray:
    result = np.asarray(values, dtype=np.float64)
    result = result / float(np.sum(result, dtype=np.float64))
    need(np.all(result >= 0) and math.isclose(float(result.sum()), 1.0,
                                               rel_tol=1e-14, abs_tol=1e-14),
         "profile normalization")
    return result


def metrics(left: np.ndarray, right: np.ndarray) -> tuple[float, float, float,
                                                              float, float, str]:
    delta = np.cumsum(left - right, dtype=np.float64)[:-1]
    tv = 0.5 * float(np.sum(np.abs(left - right), dtype=np.float64))
    ks = float(np.max(np.abs(delta)))
    integrated = float(np.mean(np.abs(delta)))
    minimum, maximum = float(delta.min()), float(delta.max())
    if minimum >= -SIGN_TOL and maximum > SIGN_TOL:
        label = "P_MAJORIZES_Q"
    elif maximum <= SIGN_TOL and minimum < -SIGN_TOL:
        label = "Q_MAJORIZES_P"
    elif minimum < -SIGN_TOL and maximum > SIGN_TOL:
        label = "MIXED"
    else:
        label = "UNRESOLVED"
    return tv, ks, integrated, minimum, maximum, label


def test_scalar_invariance() -> None:
    base = profile([12.0, 5.0, 2.0, 1.0, 0.25])
    for scalar in (0.125, 1.0, 7.5, 1.0e9):
        scaled = profile((base * scalar).tolist())
        values = metrics(base, scaled)
        need(max(abs(value) for value in values[:5]) < 3.0e-15 and
             values[5] == "UNRESOLVED", "positive-scalar profile invariance")


def test_metric_geometry() -> None:
    p = profile([8.0, 4.0, 2.0, 1.0])
    q = profile([5.0, 4.0, 3.0, 3.0])
    r = profile([7.0, 3.0, 2.0, 1.0])
    pq = metrics(p, q)
    qp = metrics(q, p)
    pr = metrics(p, r)
    qr = metrics(q, r)
    need(math.isclose(pq[0], qp[0], rel_tol=1e-14, abs_tol=1e-14) and
         math.isclose(pq[1], qp[1], rel_tol=1e-14, abs_tol=1e-14),
         "distance symmetry")
    need(0 <= pq[0] <= 1 and 0 <= pq[1] <= 1 and 0 <= pq[2] <= 1,
         "distance range")
    need(pr[0] <= pq[0] + qr[0] + 1e-14 and
         pr[1] <= pq[1] + qr[1] + 1e-14,
         "profile triangle bounds")


def test_majorization_labels() -> None:
    p = profile([6.0, 2.0, 1.0, 1.0])
    q = profile([4.0, 3.0, 2.0, 1.0])
    mixed_left = profile([5.0, 2.0, 2.0, 1.0])
    mixed_right = profile([4.0, 3.5, 1.0, 1.5])
    need(metrics(p, q)[5] == "P_MAJORIZES_Q" and
         metrics(q, p)[5] == "Q_MAJORIZES_P" and
         metrics(mixed_left, mixed_right)[5] == "MIXED",
         "majorization classification")
    near_left = profile([1.0, 1.0, 1.0])
    near_right = profile([1.0 + 2e-10, 1.0 - 2e-10, 1.0])
    need(metrics(near_left, near_right)[5] == "UNRESOLVED",
         "near-tie sign guard")


def test_interval_and_thresholds() -> None:
    values = [0.0321298129, 0.0321298131, 0.0321298128]
    guard = 1e-12
    lower = min(values) - guard
    upper = max(values) + guard
    need(lower <= min(values) <= max(values) <= upper and lower > 0.03,
         "outward separation interval")
    ks = [0.0233972220, 0.0233972221]
    need(min(ks) - guard > 0.02, "Lorenz threshold")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("--check is required")
    try:
        test_scalar_invariance()
        test_metric_geometry()
        test_majorization_labels()
        test_interval_and_thresholds()
    except (Failure, ValueError, np.linalg.LinAlgError) as error:
        print("TPC321_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC321_STRESS=PASS scalar_invariance=4 metric_geometry=1 "
          "majorization_labels=1 interval_thresholds=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
