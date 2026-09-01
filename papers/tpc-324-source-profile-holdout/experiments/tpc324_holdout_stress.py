#!/usr/bin/env python3
"""Algebraic and protocol stress tests for the TPC-324 holdout."""

from __future__ import annotations

import argparse
import math
import sys

try:
    import numpy as np
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC324 stress suite requires numpy: " + str(error))

HEIGHT = 66
TRAINING_INTERVALS = ((321, 640), (641, 1280), (1281, 2560))
PANEL_INTERVALS = {
    "continuation": {
        640: (2561, 2880),
        1280: (2881, 3520),
        2560: (3521, 4800),
    },
    "gap_offset": {
        640: (5001, 5320),
        1280: (6001, 6640),
        2560: (8001, 9280),
    },
}


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def literal_block(values: np.ndarray, prime: int, exponent: int) -> np.ndarray:
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    kernel = HEIGHT ** (2 * exponent) / (
        HEIGHT * HEIGHT + dd * dd) ** exponent
    valid = ((differences != 0) &
             (values[:, None] % prime != 0) &
             (values[None, :] % prime != 0))
    centered = (np.equal(np.mod(differences, prime), 0).astype(np.float64) -
                1.0 / (prime - 1))
    return prime * kernel * centered * valid


def profile(values: list[float]) -> np.ndarray:
    array = np.maximum(np.asarray(values, dtype=np.float64), 0.0)
    total = float(array.sum(dtype=np.float64))
    need(total > 0, "profile domain")
    result = array / total
    need(math.isclose(float(result.sum(dtype=np.float64)), 1.0,
                      rel_tol=1e-14, abs_tol=1e-14),
         "profile normalisation")
    return result


def metrics(signed: np.ndarray, direct: np.ndarray) -> tuple[float, float, float,
                                                               float, str]:
    delta = np.cumsum(signed - direct, dtype=np.float64)[:-1]
    minimum, maximum = float(delta.min()), float(delta.max())
    if minimum >= -1e-10 and maximum > 1e-10:
        label = "SIGNED_MAJORISES_DIRECT"
    elif maximum <= 1e-10 and minimum < -1e-10:
        label = "DIRECT_MAJORISES_SIGNED"
    elif minimum < -1e-10 and maximum > 1e-10:
        label = "MIXED"
    else:
        label = "UNRESOLVED"
    return (0.5 * float(np.abs(signed - direct).sum(dtype=np.float64)),
            float(np.max(np.abs(delta))), minimum, maximum, label)


def test_disjoint_frozen_panels() -> None:
    training = set()
    for lo, hi in TRAINING_INTERVALS:
        training.update(range(lo, hi + 1))
    seen = set()
    for panel in PANEL_INTERVALS.values():
        for lo, hi in panel.values():
            need(hi - lo + 1 in (320, 640, 1280), "holdout cardinality")
            values = set(range(lo, hi + 1))
            need(not values & training and not values & seen,
                 "source overlap")
            seen.update(values)


def test_conditional_translation_covariance() -> None:
    # A shift divisible by every prime in the shell preserves both residue
    # masks and differences.  This is the exact finite covariance lemma.
    values = np.arange(401, 417, dtype=np.int64)
    shift = 5 * 7
    shifted = values + shift
    for prime in (5, 7):
        left = literal_block(values, prime, 1)
        right = literal_block(shifted, prime, 1)
        need(float(np.max(np.abs(left - right))) == 0.0,
             "conditional translation covariance")


def test_holdout_is_not_trivial_covariance() -> None:
    # The selected offsets are not common multiples of the complete Q=24
    # shell, so the replication cannot be explained by the covariance lemma.
    shell = (29, 31, 37, 41, 43, 47)
    shift = 5001 - 321
    need(any(shift % prime != 0 for prime in shell),
         "hostile offset accidentally common multiple")
    values = np.arange(321, 641, dtype=np.int64)
    shifted = values + shift
    changed = 0
    for prime in shell:
        changed += int(np.any((values % prime == 0) !=
                              (shifted % prime == 0)))
    need(changed > 0, "residue masks did not change")


def test_amplitude_shape_separation() -> None:
    b1 = np.diag(np.asarray([1.0, 1.0]))
    b2 = np.diag(np.asarray([0.0, 1.0]))
    direct = b1.T @ b1 + b2.T @ b2
    coherent = b1 - b2
    rho = float(np.trace(coherent.T @ coherent) / np.trace(direct))
    signed = profile(np.linalg.eigvalsh(coherent.T @ coherent)[::-1].tolist())
    baseline = profile(np.linalg.eigvalsh(direct)[::-1].tolist())
    result = metrics(signed, baseline)
    need(rho < 1.0 and result[-1] == "SIGNED_MAJORISES_DIRECT" and
         result[2] >= -1e-10, "amplitude/shape geometry")
    need(0.0 <= rho / 2.0 <= 1.0, "projector fraction")


def test_majorization_labels() -> None:
    concentrated = profile([8.0, 3.0, 1.0, 0.5])
    diffuse = profile([5.0, 4.0, 2.5, 1.0])
    left = profile([7.0, 2.0, 2.0, 1.0])
    right = profile([5.5, 3.5, 2.5, 1.0])
    need(metrics(concentrated, diffuse)[-1] ==
         "SIGNED_MAJORISES_DIRECT" and
         metrics(diffuse, concentrated)[-1] == "DIRECT_MAJORISES_SIGNED" and
         metrics(left, right)[-1] == "MIXED", "majorization geometry")


def test_metric_bounds() -> None:
    left = profile([12.0, 6.0, 2.0, 1.0])
    right = profile([8.0, 7.0, 4.0, 2.0])
    result = metrics(left, right)
    reverse = metrics(right, left)
    need(math.isclose(result[0], reverse[0], rel_tol=1e-14,
                      abs_tol=1e-14) and
         math.isclose(result[1], reverse[1], rel_tol=1e-14,
                      abs_tol=1e-14) and 0.0 <= result[0] <= 1.0 and
         0.0 <= result[1] <= 1.0, "metric bounds/symmetry")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("--check is required")
    try:
        test_disjoint_frozen_panels()
        test_conditional_translation_covariance()
        test_holdout_is_not_trivial_covariance()
        test_amplitude_shape_separation()
        test_majorization_labels()
        test_metric_bounds()
    except (Failure, ValueError, np.linalg.LinAlgError) as error:
        print("TPC324_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC324_STRESS=PASS disjointness=1 covariance=1 "
          "nontrivial_offset=1 amplitude_shape=1 majorization=1 metrics=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
