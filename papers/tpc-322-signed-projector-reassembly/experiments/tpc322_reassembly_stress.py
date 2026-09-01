#!/usr/bin/env python3
"""Small deterministic algebra and adversarial tests for TPC-322."""

from __future__ import annotations

import itertools
import math
import sys

try:
    import numpy as np
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC322 stress requires numpy: " + str(error))


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def test_projector_identity() -> None:
    blocks = [
        np.asarray([[1.0, 2.0], [0.5, -1.0]]),
        np.asarray([[2.0, -1.0], [1.5, 0.25]]),
        np.asarray([[-1.0, 0.5], [2.0, 1.0]]),
    ]
    signs = np.asarray([1.0, -1.0, 1.0])
    direct = sum(float(np.sum(block * block)) for block in blocks)
    coherent = sum(signs[i] * blocks[i] for i in range(len(blocks)))
    projected = float(np.sum(coherent * coherent)) / len(blocks)
    # Build E and P explicitly in the direct-sum output space.
    identity = np.eye(2)
    e = np.vstack([signs[i] * identity / math.sqrt(len(blocks))
                   for i in range(len(blocks))])
    a = np.vstack(blocks)
    projection = e @ e.T
    lhs = float(np.sum((projection @ a) ** 2))
    need(math.isclose(lhs, projected, rel_tol=1e-14, abs_tol=1e-14),
         "projector identity")
    need(projected <= direct + 1e-14 and projected >= -1e-14,
         "projection contraction")


def test_sign_gauge_and_extrema() -> None:
    gram = np.asarray([[4.0, 1.5, -0.25],
                       [1.5, 3.0, 0.75],
                       [-0.25, 0.75, 2.0]])
    minimum = math.inf
    maximum = -math.inf
    for tail in itertools.product((1.0, -1.0), repeat=2):
        signs = np.asarray((1.0,) + tail)
        value = float(signs @ gram @ signs)
        opposite = float((-signs) @ gram @ (-signs))
        need(math.isclose(value, opposite, rel_tol=1e-14, abs_tol=1e-14),
             "global sign gauge")
        minimum = min(minimum, value)
        maximum = max(maximum, value)
    need(minimum < maximum and minimum > 0, "finite sign extrema")


def test_pattern_and_interval_semantics() -> None:
    primes = [29, 31, 37, 41, 43]
    alternating = [1 if i % 2 == 0 else -1 for i in range(len(primes))]
    mod4 = [1 if p % 4 == 1 else -1 for p in primes]
    need(alternating == [1, -1, 1, -1, 1], "alternating labels")
    need(mod4 == [1, -1, 1, 1, -1], "mod4 labels")
    values = [0.5990575656, 0.5990575657]
    guard = 1e-12
    low, high = min(values) - guard, max(values) + guard
    need(low < min(values) <= max(values) < high and low > 0,
         "outward interval")


def main() -> int:
    try:
        test_projector_identity()
        test_sign_gauge_and_extrema()
        test_pattern_and_interval_semantics()
    except (Failure, ValueError, np.linalg.LinAlgError) as error:
        print("TPC322_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC322_STRESS=PASS projector_identity=1 sign_gauge=1 "
          "extrema=1 pattern_labels=2 interval=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
